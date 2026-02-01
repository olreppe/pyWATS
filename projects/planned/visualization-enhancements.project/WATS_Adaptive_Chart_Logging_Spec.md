
# WATS Adaptive Chart Logging (ACL) – Conceptual Specification

## 1. Goals
- Byte-efficient chart logging under configurable budgets.
- Optional deterministic output to enable overlaying charts across UUTs.
- Edge-case escalation: detailed logging only when anomalies are detected.
- Generic applicability across audio and non-audio signals.
- First-class derived scalar metrics ("multinumeric") with independent pass/fail status.

---

## 2. Core Concepts

### 2.1 Input Model
A **Chart** consists of:
- `chart_id`, `title`
- `units_x`, `units_y`
- `domain_type`: `Timeseries | Spectrum | XY | Spectrogram | Other`
- `series[]`
  - `series_id`, `name`
  - Representation:
    - **1D implicit X**: `y[]` with defined `x_start`, `dx`
    - **XY**: `x[]`, `y[]`
  - Optional `quality_flags[]`

### 2.2 Output Model
A **LoggedChartArtifact** contains:
- `summary`
- `render_curves`
- `features`
- `attachments`
- `derived_metrics[]`
- `status` (step-level)

---

## 3. Deterministic Overlay Mode (DOM)

When enabled, the pipeline must produce identical X coordinates for all units.

### Strategies
1. **Fixed X Grid**
   - Linear or logarithmic grids
   - Explicit point count or points-per-decade
2. **Deterministic Bucketing**
   - Fixed bucket boundaries with aggregate values

Guarantees:
- Same X grid across units
- Same config + input → same output

### Why XY Can Be More Efficient Than 1D
Horizontal or constant regions can be represented with minimal points using segment encoding, reducing storage compared to dense 1D sampling.

---

## 4. Compression & Representation Toolbox

### 4.1 Resampling / Rebinning
- Linear resampling
- Log-frequency resampling
- Bucket aggregation (min/max/mean)
- Domain transforms (e.g., linear → dB)

### 4.2 Simplification
- Error-bound simplification
- LTTB (visual fidelity)
- Min/max envelope buckets

### 4.3 Segment Encoding
- Polylines
- Horizontal segments
- Step-like segments (optional)

---

## 5. Derived Metrics (Multinumeric)

Each metric includes:
- `metric_id`, `name`, `value`, `units`
- `scope`: chart / series / band / ROI
- `status`: PASS / FAIL / WARN / NA
- Optional limits or comparison rules

Examples:
- min, max, avg, std, var
- RMS, crest factor
- Band power
- Noise floor estimate

### Step Status Rule
If **any derived metric fails**, the step fails.

---

## 6. Edge-Case Detection & Escalation

### Always Logged
- Simplified render curves
- Features
- Derived metrics

### Triggers
- Metric failure
- Shape deviation vs baseline
- Excessive noise or clipping

### Escalation Attachments
- Higher-resolution curves
- ROI extracts
- Raw snippets
- Spectrogram images

---

## 7. Budgets & Limits

System limits:
- Max 50 series
- Max 10,000 points per series

Recommended budgets:
- Render points: 500–2000 per series
- Normal attachments: ≤ 50 KB
- Anomaly attachments: up to several MB

---

## 8. Series Prioritization

Series roles:
- `primary`
- `reference`
- `limit_line`
- `diagnostic`

Policy:
- Always include primary/reference
- Encode limit lines efficiently
- Drop or summarize diagnostic series unless triggered

---

## 9. Default Recipes

### Spectrum (Audio FFT)
- Log-frequency deterministic grid
- dB domain
- Peak & band extraction
- ROI escalation on failure

### Time Series
- Fixed linear grid or bucket envelopes
- Event detection
- Raw snippet escalation

### XY Transfer Function
- Fixed grid
- Knee & bandwidth metrics
- High-res attachment on failure

---

## 10. Configuration Surface

A **Recipe** defines:
- Overlay mode
- Grid/bucket specs
- Transforms
- Render policy
- Feature extractors
- Derived metrics & limits
- Detectors
- Escalation policy
- Series priority rules

---

## 11. Acceptance Criteria
1. Normal runs stay within budget.
2. Overlay mode produces identical X coordinates.
3. Metric failures reliably fail steps.
4. Triggered runs provide sufficient diagnostic detail.
5. Deterministic mode guarantees reproducibility.

---

*End of specification.*
