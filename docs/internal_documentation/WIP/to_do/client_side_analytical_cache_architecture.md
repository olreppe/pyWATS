# Client-Side Analytical Data Cache Architecture (Python)

## Problem Context

You are building a **client-side analytical cache** in front of a **remote Web API** that exposes:
- Pre-calculated KPIs (yield, Cpk, Cp, std, var, min, max, counts, etc.)
- Aggregated step-level metrics
- Deep raw measurement data (double / bool / string)

Key requirements:

- Query data *as if it were live*
- Load **only missing data** on demand
- Avoid repeated API requests
- Support **dimension-based filtering** (serial, part, process, station, operator, config, time, etc.)
- Recalculate KPIs *after filtering* (cohort analysis)
- Support **predictive / speculative loading** (drill-down when KPIs look suspicious)
- Keep **all data levels accessible through one unified structure**
- Designed to be consumed by an **analytic AI agent**
- No long-term persistence required (cache only)

---

## Recommended Core Architecture (Best Fit)

### High-Level Choice

**DuckDB (in-memory) + Arrow / Polars + Explicit Cache Manager**

This combination provides:
- A **single unified query surface**
- Fast cohort filtering and aggregation
- Lazy loading and partial data coverage
- Minimal conceptual overhead for an AI agent

---

## Conceptual Model: One Cube, Multiple Levels

Expose **one object** to the AI agent:

```text
CubeCache
```

Internally, the cube manages multiple *levels* of data, all sharing the same dimension schema.

### Logical Levels (Facets)

1. **Unit / Yield Level**
   - One row per unit or per batch/run
   - Server-provided KPIs (yield, counts, metadata)

2. **Step Aggregate Level**
   - Precomputed step KPIs from server
   - (cpk, cp, std, var, min, max, n)

3. **Raw Measurement Level**
   - Individual readings (sample-level)

All levels share:
- Unit ID
- Serial number
- Part number
- Process
- Station
- Operator
- Configuration properties
- Time / run identifiers

The AI agent never needs to care which level is stored where.

---

## Unified Access Pattern (Critical for AI Use)

The agent interacts with **one consistent API**:

```text
view = cube.select(filter)
view.yield()
view.step_agg()
view.measurements()
view.stats(...)
```

- The filter is defined **once**
- The same filter applies across all levels
- Missing data is automatically fetched
- KPIs are recomputed on demand after filtering

This avoids duplicated logic and cognitive overhead.

---

## Why DuckDB (In-Memory)

DuckDB acts as the **semantic and analytical engine**, not as persistent storage.

### Benefits

- SQL is ideal for cohort analysis, grouping, joins, and KPI recomputation
- Excellent performance on columnar data
- Works directly with Arrow and Polars
- No server process required
- Can run fully in memory

DuckDB tables are populated incrementally as data is fetched from the API.

---

## Data Containers

### Arrow / Polars

Cached data chunks are stored as:
- Arrow Tables **or**
- Polars DataFrames

Reasons:
- Columnar
- Fast filtering and aggregation
- Cheap concatenation
- Easy to register with DuckDB

---

## Cache Strategy

### Cache What?
Not query results — **reusable data chunks**.

Examples:
- Unit-level KPI batches
- Step-aggregate batches
- Raw measurement batches

### Chunking Keys (Very Important)

Choose chunk boundaries that align with real queries:
- Time windows (day/week)
- Part + process + station
- Lot / batch / test-run identifiers

Good chunking prevents constant partial overlap and reloads.

---

## Cache Metadata (Per Chunk)

Each cached chunk tracks:
- Covered dimension ranges/sets
- Row count
- Memory size
- Last access timestamp
- Source endpoint
- Optional KPI summary (min cpk, yield, etc.)

This metadata enables:
- Load planning
- Eviction
- Predictive drill-down decisions

---

## Load-on-Demand Flow

1. Agent issues query with filter `F`
2. Cache computes required coverage
3. Missing chunks are identified
4. API requests are generated only for missing data
5. New chunks are appended
6. Query is executed via DuckDB
7. Result is returned

All of this is transparent to the agent.

---

## KPI Handling Philosophy

- **Do not store recalculated KPIs**
- Store only:
  - Server-provided aggregates
  - Raw counts where needed

Filtered KPIs are computed dynamically using:
- GROUP BY
- Aggregations
- Window functions

This avoids duplication and keeps logic centralized.

---

## Predictive / Speculative Loading

Triggered by KPI signals such as:
- Low yield
- Low Cpk
- High variance
- Anomalous distributions

Rules example:
- If `cpk < threshold` and cohort size < limit → load raw measurements
- If yield drops and clusters around `(station, operator)` → prefetch those

Speculative data is placed in a **lower-priority cache tier**.

---

## Eviction Policy

Use **size-based eviction** at chunk level:

Recommended:
- Segmented LRU (hot vs cold)
- Drop speculative chunks first
- Protect frequently reused or expensive-to-fetch chunks

Avoid row-level eviction — it breaks chunk coherence.

---

## Optional Enhancements

### Disk Spill (Not Persistence)
Use SQLite / LMDB / diskcache to:
- Store raw API responses
- Survive restarts
- Extend beyond RAM

### HTTP Optimizations
- ETag / If-None-Match
- Request memoization

### Async Prefetch
- Background tasks for speculative loading
- Non-blocking AI exploration

---

## Why This Is the Right Fit

This approach gives you:
- One mental model
- One access API
- One filter language
- One analytics engine

Yet still supports:
- Lazy loading
- Deep drill-down
- Large datasets
- AI-driven exploration

It scales from:
- Single-machine exploratory analytics
to
- Distributed backends later (ClickHouse / Spark) with minimal API changes.

---

## Final Recommendation (Short)

**Use:**
- DuckDB (in-memory)
- Arrow or Polars for cached chunks
- Explicit cache coverage index
- Optional disk-backed request cache

**Expose:**
- One `CubeCache` abstraction to the AI agent

This balances performance, simplicity, and future scalability.
