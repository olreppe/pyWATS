# AI-Assisted SPC Ringbuffer Cache — Detailed Brainstorming & Implementation Options (Python)

## 1) Goal and Constraints

You are building a **client-side analytical cache** in front of a **remote Web API** that exposes:
- Pre-calculated KPIs (yield, Cpk, Cp, std, var, min, max, counts, etc.)
- Aggregated step-level metrics
- Deep raw measurement data (double / bool / string)

Key requirements:

- Query data *as if it were live*
- Load **only missing data** on demand
- Avoid repeated API requests
- Support **dimension-based filtering** (part/process/station/operator/config/etc.)
- Recalculate KPIs *after filtering* (cohort analysis)
- Support **predictive / speculative loading** (drill-down when KPIs look suspicious)
- Keep **all data levels accessible through one unified structure**
- Designed to be consumed by an **analytic AI agent**
- Cache also acts like a **ringbuffer** for continuous SPC monitoring (hourly ingestion)
- No long-term persistence required (cache only)

Preference:
- Avoid DB/SQL unless there’s a compelling reason.

---

## 2) Core Concept: One In-Memory “Cube” With Streaming Windows

Even without SQL/DB, you can keep a single “data structure” by using:

- **Columnar in-memory tables** (Arrow / Polars) for storage and analytics
- A **single filter DSL** applied consistently across all levels
- A **Window Manager** to provide ringbuffer behavior per level and per cohort key
- An **Issue Engine** that consumes events produced by SPC detectors and AI assessments

### Data “levels” (facets) kept inside the cube
- **Unit / Yield level** (per unit/run summary)
- **Step aggregates level** (server precomputed per step/metric aggregates)
- **Raw measurements level** (deep readings, loaded only as needed)

Streaming twist:
- You keep **recent windows** plus selective retention for active issues, rather than everything.

---

## 3) Data Model Suggestions (Practical and Efficient)

### 3.1 Canonical IDs and Dimensions
Use stable identifiers for joining levels and defining cohorts:
- `unit_id` (or test-run id)
- `serial_number`
- `part_number`
- `process`
- `station`
- `operator`
- `config_hash` (or normalized config dimensions)
- `timestamp` (event time) and optionally `ingest_time`

### 3.2 Fact-like tables (in-memory)
Keep three main columnar tables/frames:

1) **units_frame**
- one row per unit/run
- pass/fail, yield flags, high-level KPIs from server, timestamps, dimensions

2) **step_agg_frame**
- one row per (unit/run or batch) × step × metric
- server aggregates + counts + spec limits if available
- include `timestamp` for windowing

3) **measurements_frame**
- one row per raw measurement
- include `unit_id`, `step_id`, `metric_name`, `value_*`, timestamps

> If raw measurements are huge, keep them optional and load only for suspicious cohorts/issues.

---

## 4) Ringbuffer / Windowing Strategy

### 4.1 Dual constraint: time window + memory cap
- Keep data for the **last N hours/days** (time-based window)
- Also enforce a **hard memory limit** (bytes / rows)
- Default eviction: drop **oldest** data first (FIFO by event time)

### 4.2 Retention exceptions: “Issue pinning”
When an issue is active:
- “Pin” relevant cohorts/chunks so they are not evicted until resolved/expired
- Or keep a compressed summary (downsampled series, quantiles, counts) even if raw is evicted

### 4.3 Chunking inside the cache (no DB required)
Store frames as **chunks** keyed by something like:
- time bucket (hour/day)
- plus a coarse dimension tuple (e.g., part_number, process, station) if typical queries align

This enables:
- fast eviction (drop chunk)
- fast missing-coverage checks
- faster filtering (select chunk subset first)

Implementation pattern:
- `Dict[ChunkKey, FrameChunk]`
- Each chunk has metadata: time range, dims coverage, size bytes, last access

---

## 5) Streaming SPC Pipeline (Deterministic + AI-Assisted)

### 5.1 Event types emitted by the pipeline
Treat findings as events:
- **FailureEvent**: any fail result (always important)
- **ShiftEvent**: mean/median shift beyond threshold
- **SpreadEvent**: std/variance increase
- **CapabilityEvent**: Cp/Cpk change beyond threshold
- **OutlierEvent**: spike in min/max or extreme tail
- **DriftEvent**: slow trend (slope over window)
- **ChangePointEvent**: likely regime change
- **DataQualityEvent**: missing data, sensor glitch, anomalies

These events flow into the Issue Engine.

### 5.2 Deterministic detectors (examples)
Run each ingest tick (hourly):

**A) Failures**
- Any failure creates or updates an issue candidate
- Track failure rate by cohort and compare to baseline

**B) Shewhart-style rules**
- X-bar/R/S or Individuals (I-MR) charts
- Western Electric / Nelson rules (out-of-control patterns)
- Pros: interpretable, cheap
- Cons: needs stable baselines

**C) Capability tracking**
- Maintain rolling mean/std and Cp/Cpk (vs spec)
- Detect deltas vs baseline or EWMA baseline
- Pros: aligns with your KPIs
- Cons: Cpk is noisy for small N and non-normal distributions

**D) EWMA / CUSUM**
- Better for small shifts and slow drift
- Pros: sensitive to drift
- Cons: needs parameter tuning

**E) Change-point detection**
- Detect structural changes in mean/variance
- Pros: good for “new regime” detection
- Cons: can false-trigger under noise without preprocessing

### 5.3 Noise handling (critical)
To avoid reacting to noise that looks like drift:
- require **minimum N**
- use **robust stats** (median, MAD, trimmed mean)
- downsample signals (hourly aggregates vs raw points)
- require **persistence** (condition holds for M consecutive windows)
- combine detectors (e.g., slope + out-of-control score)

---

## 6) Issue Lifecycle and Structures

### 6.1 Issue as a first-class object
Each issue record should include:
- `issue_id`
- `status`: new / investigating / monitoring / mitigated / resolved / false_positive
- `created_at`, `last_updated_at`
- `cohort_filter` (filter defining affected population)
- `signals`: triggering events with timestamps and severity scores
- `severity`: impact measure (yield loss, scrap risk, safety/customer risk)
- `priority`: operational urgency (stop line? eng review? monitor?)
- `confidence`: belief it’s real (AI-assisted)
- `hypotheses`: candidate root causes + evidence links
- `actions`: recommended/executed actions
- `attachments`: metric snapshots, small series extracts, references to raw samples

### 6.2 “New vs continuation” merging
When a new event arrives, classify it as:
- continuation of an existing issue
- a new issue
- a related issue

Merging heuristics:
- cohort similarity (same station/operator/part/config)
- time proximity
- same step_id/metric
- similar signature (event types + direction + magnitude)

Start deterministic; later AI can refine.

---

## 7) Deep Dive Triggering (Tiered Escalation)

Your workflow (yield low → scan step aggregates → drill raw) maps naturally into tiers:

### Tier 0: Always-on cheap checks (hourly)
- failure count/rate by key cohorts
- rolling mean/std deltas
- min/max tail monitoring
- out-of-control score

### Tier 1: Aggregate-only deepening
Triggered by Tier 0:
- scan step aggregates under affected cohort
- rank offenders (steps/metrics with worst deltas)
- compute “explainability slices”: which station/operator/config contributes most

### Tier 2: Raw measurement drill-down (expensive)
Only when:
- failures occur OR
- strong persistent drift OR
- AI requests evidence

Load raw for:
- specific steps/metrics
- limited time range
- cohort size cap

### Tier 3: Root cause search (targeted)
- compare affected vs control cohorts
- rank correlated dimensions (operator, station, config changes, etc.)
- propose top hypotheses + additional evidence to fetch

---

## 8) Technology Options (No DB/SQL-first)

### Option A (recommended): Polars + Arrow + custom window manager
- Cache chunks as Arrow Tables or Polars DataFrames
- Use Polars for filtering/groupby/rolling stats
- Your code manages ringbuffer + issue system

**Pros**
- Fast, columnar, Python-native
- No SQL
- Strong rolling/window and grouping support
- Can keep everything inside one `CubeCache` abstraction

**Cons**
- You implement cache coverage, chunk planning, eviction
- Complex multi-level queries require more code than SQL would

Best fit: single-machine analytics + streaming SPC with strong simplicity constraints.

### Option B: Arrow storage + NumPy for detectors
- Arrow holds data
- Extract key columns to NumPy arrays for tight detector loops

**Pros**
- Very fast for custom SPC detectors
- Full control

**Cons**
- More glue code (types, missing values, join-like behavior)

### Option C: Dask for parallelism (still no SQL)
- Partitioned frames + scheduler
- Run detectors and deeper analysis concurrently

**Pros**
- Parallel execution, can scale out later

**Cons**
- Tuning/complexity overhead if you don’t truly need it

### Option D: Streaming infra (Kafka/Redpanda) + Python consumer (if needed)
If hourly becomes near-real-time and shared across services.

**Pros**
- Replay, consumer groups, robust pipeline semantics

**Cons**
- Infrastructure overhead; may be overkill for API polling

---

## 9) Useful Libraries for SPC / Drift / Change Detection

Not exclusive; mix per detector.

- Rolling stats: **Polars**, NumPy, SciPy
- Change points: **ruptures**
- Online drift detection / incremental learning: **river**
- Time-series modeling: **statsmodels** (only if you need it)

Recommendation: start with deterministic SPC + robust persistence rules, then add advanced methods where they clearly improve signal quality.

---

## 10) AI Agent Integration (Keep It Dead Simple)

Expose one handle and a small set of verbs:

- `cube.poll()` / `cube.ingest(time_range)`
- `cube.select(filter).units()`
- `cube.select(filter).step_agg()`
- `cube.select(filter).measurements(step_ids=..., metrics=...)`
- `cube.detect()` → returns events
- `cube.issues.list()` / `cube.issues.get(id)`
- `cube.issues.apply_ai_assessment(id, assessment)`

AI does:
- classify new vs continuation
- generate hypotheses
- request next evidence
- propose actions and prioritization

Deterministic rules do:
- first-line detection
- rate limiting / persistence gating
- what to fetch next (tier escalation)

---

## 11) Scheduling and Concurrency

Suggested internal pipeline:
- Ingest task (hourly poll)
- Cache update (append + evict)
- Detector task (emit events)
- Issue engine (merge/update/escalate)
- Prefetch task (tier 1/2 data loads)

Implementation options:
- `asyncio` (simple, single process)
- thread pool for blocking HTTP
- job queue (RQ/Celery) if you need separation

---

## 12) A Low-Risk First Implementation Plan

1) Implement `CubeCache` + chunking + time-window eviction
2) Implement Tier 0 + Tier 1 detectors:
   - failures
   - yield delta
   - rolling mean/std delta
   - basic EWMA or persistence rule
3) Implement Issue records + deterministic merging heuristics
4) Add Tier 2 raw drill-down only for high-confidence/high-severity signals
5) Add `ruptures` and/or `river` if noise vs drift remains a problem

---

## 13) When SQL/DuckDB Still Might Be Worth It (Later)

You can do this without SQL.

Add DuckDB later only if you feel pain from:
- complex cohort joins across levels
- repeated “explain which dimensions drive this delta” queries
- maintaining consistent semantics across many join/group/filter operations

DuckDB would be a convenience query engine, not a “database.”

---

## 14) Summary Recommendation

To meet the full spec **without DB/SQL**:

- **Polars + Arrow** as your unified cache tables
- **Chunked ringbuffer** (time + memory caps) with “issue pinning”
- **Tiered detectors** to reduce false triggers in noisy data
- **Issue Engine** for lifecycle + severity/priority + ongoing root cause search
- Optional: `ruptures`, `river` for change-point/drift where it adds clear value
