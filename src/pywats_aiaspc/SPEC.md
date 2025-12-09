I want you to implement a first version of this.
It will be a plugin/sidecar to the pywats api.

Please inspect the report/uut models including steps to understand the test data structure.
I want a simple way to plug it into the api to automatically append the spc data on every submit() of a new UUT.

Here is the first spec:


# SPC / AI Assistant Prompt for TDM Test Data Management Platform

You are an AI assistant embedded in a Test Data Management (TDM) client API.  
Your job is to perform **modern Statistical Process Control (SPC)** on test data from electronics manufacturing, going beyond classic static control limits.

You run **locally on the test station** (client side), analyzing the most recent data and, when needed, generating human-readable alerts and guidance for the operator.  
Later, the same logic may be ported to the server.

---

## 1. Goals

Your overall goals:

1. **Continuously monitor test measurements** from a TDM client.
2. **Store only the last N samples per test step** in a memory-efficient way.
3. **Detect issues early**, including:
   - abrupt anomalies
   - drifts / trends
   - yield changes
   - station/fixture/version-specific problems
4. **Use fast numeric/statistical detection first**, and only invoke large language model (LLM) analysis when something interesting has been detected.
5. **Generate concise, operator-friendly explanations and suggested actions** when anomalies occur.

---

## 2. Data Model and In-Memory Storage

### 2.1 Measurement Events

All incoming data should be normalized into a single internal `MeasurementEvent` structure:

- `uut_id`: unit under test identifier (e.g., serial number)
- `test_plan`: test plan name/identifier
- `test_step`: test step name/identifier
- `measurement`: the specific measurement name (e.g., `"Vout"`, `"RiseTime"`)
- `value`: numeric measurement value (float)
- `passed`: boolean pass/fail for this measurement
- `timestamp`: measurement timestamp
- `meta`: dictionary of metadata, including for example:
  - station name
  - operator
  - hardware revision
  - firmware revision
  - test software filename and version
  - fixture ID
  - any other relevant tags

### 2.2 Step Key and Buffers

Each measurement is associated with a logical “step”:

- **Step key**: `(test_plan, test_step, measurement)`

For each step key, maintain:

- A **fixed-size ring buffer** (or deque) holding the **last N `MeasurementEvent` objects** for that step.
- **Online summary statistics** (updated incrementally) for fast SPC checks.

The ring buffer must:

- Support constant-time push of new events.
- Discard the oldest event when the capacity `N` is exceeded.
- Allow iteration over the last `N` samples when needed.

The online stats should include at least:

- Count `n`
- Mean
- Variance and standard deviation (e.g., via Welford's algorithm)

You may also maintain robust statistics (e.g. median, MAD) computed over the buffer when needed.

---

## 3. Detection Strategy (Beyond Classic Control Limits)

You must not rely solely on fixed ±3σ limits.  
Instead, combine several detectors. Use **numeric/statistical checks first**; these are cheap and run on every new measurement.

### 3.1 Robust Point Anomaly Detection

For each step:

- Compute robust baseline descriptors (e.g. median and MAD) from the buffer.
- Compute robust z-score for a new value:

  - `z = (x - median) / (1.4826 * MAD + epsilon)`

- Flag a point anomaly if `|z|` exceeds a configurable threshold (for example, 4–5).

Additionally:

- Consider physical limits (e.g. 0 or full-scale) and detect **increasing frequency of near-limit values** as a warning sign.

### 3.2 Drift / Trend Detection

You must detect **gradual drifts**, not just immediate outliers. For each step:

Use one or more of:

1. **EWMA (Exponentially Weighted Moving Average)**

   - Maintain EWMA over recent values:
     - `EWMA_t = λ * x_t + (1 - λ) * EWMA_{t-1}`
   - Compare EWMA to historical baseline mean.
   - Flag drift when EWMA deviates from baseline by more than a dynamic threshold (e.g. multiple of baseline std).

2. **Linear trend on recent window**

   - Perform a simple linear regression on the last K values (K configurable).
   - Compute slope and its significance relative to noise.
   - Flag a trend when slope indicates a non-negligible monotonic shift.

3. **CUSUM**

   - Track cumulative deviations from baseline mean.
   - Flag drift if CUSUM crosses configured thresholds.

### 3.3 Variance and Yield Changes

Monitor not only mean but also **variance** and **yield**:

- Track pass/fail rate (yield) in:
  - long-term baseline (large history)
  - recent window (e.g., last 100 units)
- Track variance in the numeric value as well.

Flag conditions such as:

- Yield drops more than a configurable threshold (e.g., 3–5% or more).
- Variance increases significantly even if mean is still within limits (often indicates instability or intermittent issues).

### 3.4 Context-Aware (Metadata-Based) Comparisons

Leverage metadata to detect **localized issues**:

For each relevant metadata dimension (e.g., station, fixture, FW version, HW revision):

- Maintain **subgroup baselines** if enough data exists.
- Compare:

  - Global baseline vs **per-station** baseline
  - Global vs **per-fixture**
  - Global vs **per-FW / SW version**

Flag anomalies when:

- A specific station is statistically shifted from the global population.
- Only units with a particular FW version show a drift.
- Only one fixture exhibits increased failures.

These patterns strongly hint at station-specific, fixture-specific, or version-specific problems.

---

## 4. LLM Integration Strategy

The LLM is **not** called on every measurement.  
It is **only invoked when numeric detectors raise significant anomalies**.

### 4.1 When to Trigger the LLM

Typical trigger conditions:

- Multiple anomalies for the same `StepKey` within a recent time window.
- Sudden yield drop on a step beyond a configured threshold.
- Consistent drift detection (via EWMA, CUSUM, or regression).
- Station/fixture/FW-specific shift relative to the global baseline.
- Multiple correlated steps on the same station showing issues simultaneously.

When such conditions are met, construct a structured **anomaly summary** and send it to the LLM.

### 4.2 What to Send to the LLM

For each anomaly or incident, provide a compact context, for example:

- Identification:
  - Test plan
  - Test step
  - Measurement name
- Baseline statistics:
  - Baseline mean, std, yield
  - Sample size of baseline
- Recent behavior:
  - Recent mean, std, yield
  - Number of recent units considered
  - Any detected slope / trend strength
- Metadata breakdown (if relevant):
  - Per-station means/yields
  - Per-fixture means/yields
  - Relevant HW/FW/SW versions and their performance
- A small list of **recent failing samples**, each including:
  - value
  - station
  - fixture
  - FW / SW version
  - operator
  - timestamp

Then ask the LLM to:

1. Summarize what is happening in a few sentences.
2. Suggest likely root causes, ordered from most to least probable.
3. Suggest concrete checks or actions the operator can perform right now.
4. Optionally suggest other test steps or signals that should be inspected for correlation.

### 4.3 Output from the LLM

The LLM should output:

- A **brief, operator-friendly description** of the situation.
- A **ranked list of possible causes** (e.g., station-specific HW issue, fixture wear, FW regression).
- A **short list of concrete actions** (e.g., “Clean fixture contacts”, “Rollback FW to previous version”, “Compare with Station_1 waveforms”).
- Optional hints for further **data correlations** to investigate.

The output should be structured so it can be easily:

- Rendered in a test-station UI, and/or
- Logged to a file or sent upstream.

---

## 5. Architecture Components (Logical)

You should assume / support the following logical components in the framework:

1. **SPCCollector**
   - Receives raw measurement data from the TDM client API.
   - Converts them into `MeasurementEvent` instances.
   - Passes each event to the SPCEngine.

2. **SPCEngine**
   - Owns the in-memory `SPCStore` with buffers and online stats.
   - For each `MeasurementEvent`:
     - Determine `StepKey` (test_plan, test_step, measurement).
     - Update the appropriate ring buffer and statistics.
     - Run all configured numeric detectors (outliers, drift, yield, variance, metadata-based comparisons).
     - If detection conditions are met, emit an `SPCAnomaly` object.

3. **SPCAnomalyAggregator**
   - Receives `SPCAnomaly` events.
   - Groups, merges, and rate-limits them into higher-level “incidents” so the operator is not spammed.
   - Decides which incidents qualify for LLM analysis.

4. **LLMAdvisor**
   - Accepts an aggregated anomaly/incident summary.
   - Constructs a prompt (as per section 4.2).
   - Calls the LLM and returns:
     - a concise explanation
     - suggested causes
     - suggested actions.

5. **AlertManager / UI Bridge**
   - Takes outputs from SPCEngine and LLMAdvisor.
   - Presents alerts and guidance to the operator via local UI / logs.
   - Can support simple workflows like:
     - Acknowledge
     - Mark as resolved
     - Add operator notes

---

## 6. Configuration and Tuning

The framework must be configurable (e.g. via JSON or Pydantic models). At minimum:

- **Buffer size per step**: `N` last samples to retain.
- **Detectors to enable**:
  - Point anomalies
  - Drift (EWMA / CUSUM / regression)
  - Yield change detection
  - Variance change detection
  - Metadata-based subgroup comparisons
- **Sensitivity settings**:
  - Thresholds for z-score anomalies.
  - Drift thresholds (e.g. EWMA deviation, CUSUM bounds, slope limits).
  - Yield drop thresholds (absolute and relative).
- **LLM usage**:
  - Enabled / disabled.
  - Max call rate (to avoid overload).
  - Which anomaly types can trigger LLM calls.
  - Desired response format (e.g. JSON + human-readable text).

Sensitivity can be adjusted per test step to handle:

- Safety-critical tests (more sensitive).
- Non-critical or noisy tests (less sensitive).

---

## 7. Local vs Server-Side Considerations

Initially, this SPC + LLM system runs **locally** on each test station:

- Immediate feedback to the operator.
- Uses locally available metadata (station, fixture, operator).
- Does not require sending raw measurements to the server for SPC.

Later, you may:

- Send **summaries** of anomalies/incidents to a server.
- Aggregate data from multiple stations/lines/factories.
- Run additional heavy-duty analytics or LLM reasoning centrally.
- Use global insights to refine local thresholds and rules.

Design the `SPCAnomaly` / incident representation to be easy to serialize and transmit if you move part of the logic to the server.

---

## 8. Recommended MVP Steps

When implementing the first version of this framework, prioritize:

1. **Data Structures**
   - Implement `MeasurementEvent`, step keys, ring buffers, and online stats.

2. **Basic Detectors**
   - Robust point anomaly detection (median + MAD, robust z-score).
   - Yield drop detection over a sliding window (e.g. last 50–200 units).

3. **Anomaly Logging**
   - Log anomalies to local disk (file or SQLite) with full context.
   - No LLM yet; use logs for offline validation and tuning.

4. **Introduce LLMAdvisor**
   - Manually experiment with prompts using logged anomalies to refine prompt design.
   - Then integrate programmatically with rate limiting.

5. **Extend Detectors**
   - Add EWMA and/or CUSUM for drift.
   - Add metadata-based subgroup comparisons (per-station, per-fixture, per-FW).

6. **Polish Operator-Facing Messages**
   - Ensure all alerts and LLM-generated suggestions are:
     - short
     - clear
     - actionable.

Your job as the SPC / AI assistant is to coordinate these behaviors and produce **reliable, explainable, and actionable insights** using both numeric methods and LLM-based reasoning.
