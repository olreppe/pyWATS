# Understanding Yield Metrics in WATS

## Overview

Yield is a Key Performance Indicator (KPI) that measures the percentage of units that passed a manufacturing process. WATS provides several yield metrics to give you different perspectives on production quality.

**Critical Concept**: Yield should always be considered **per process/test_operation**. A product typically goes through multiple processes (ICT, FCT, EOL, etc.), and each has its own yield.

---

## Yield Metric Types

### Unit-Based Yield Metrics (FPY, SPY, TPY, LPY)

These metrics answer: **"What percentage of units passed the process?"**

| Metric | Name | Definition |
|--------|------|------------|
| **FPY** | First Pass Yield | % of units that passed on their first test run |
| **SPY** | Second Pass Yield | % of units that passed within 2 runs (includes FPY units) |
| **TPY** | Third Pass Yield | % of units that passed within 3 runs (includes SPY units) |
| **LPY** | Last Pass Yield | % of units that passed after all runs (final yield) |

**Relationship**: FPY ≤ SPY ≤ TPY ≤ LPY

**Example**: 
- 100 units tested
- 85 passed first run → FPY = 85%
- 10 more passed on second run → SPY = 95%
- 3 more passed on third run → TPY = 98%
- 1 more passed on fourth run → LPY = 99%

### Report-Based Yield Metrics (TRY)

| Metric | Name | Definition |
|--------|------|------------|
| **TRY** | Test Report Yield | Passed reports ÷ All reports |

**TRY** answers: **"What percentage of test reports passed?"**

This is a different question than FPY-LPY. A unit may have multiple reports (one per test run), so TRY reflects the success rate of individual test attempts, not units.

### Rolled Throughput Yield (RTY)

| Metric | Name | Definition |
|--------|------|------------|
| **RTY** | Rolled Throughput Yield | FPY₁ × FPY₂ × ... × FPYₙ (product of all process FPYs) |

**RTY** answers: **"What percentage of units pass ALL processes on their first try?"**

**Example**:
```
Product WIDGET-001 goes through 3 processes:
- ICT:  FPY = 98%
- FCT:  FPY = 95%
- EOL:  FPY = 99%

RTY = 0.98 × 0.95 × 0.99 = 92.2%

This means only 92.2% of units pass ALL processes without any retest.
```

**When to use RTY**:
- Overall product quality assessment
- Comparing products across entire production flow
- When someone asks "What's the yield for Product X?" without specifying a process

---

## Yield is Per Process (Critical!)

### The Common Misunderstanding

**Wrong**: "What's the yield for WIDGET-001?" (ambiguous!)

**Right**: 
- "What's the **FCT yield** for WIDGET-001?" (specific process)
- "What's the **RTY** for WIDGET-001?" (overall across all processes)

### Why This Matters

A product typically passes through multiple test operations/processes:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   ICT    │ → │   FCT    │ → │   EOL    │ → │  Ship    │
│  FPY=98% │    │  FPY=95% │    │  FPY=99% │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

Each process has different:
- Failure modes
- Volume (some processes may be skipped for certain configs)
- Historical trends
- Responsible teams

### Best Practice: Always Specify Process

When analyzing yield:
1. First, check what processes the product goes through: `perspective="by operation"`
2. Then analyze each process individually: `test_operation="FCT"`
3. Or calculate RTY for overall quality

---

## Yield Over Time (Temporal Analysis)

### Date Range Defaults

WATS always assumes you want the **most recent data**:

| Parameter | Default |
|-----------|---------|
| `date_from` | 30 days ago (if omitted) |
| `date_to` | Now (if omitted) |

**Important**: If you don't specify any date parameters, WATS returns the last 30 days of data.

### Time-Based Perspectives

Use these perspectives for yield over time:

| Perspective | Date Grouping | Example Use |
|-------------|---------------|-------------|
| `trend` | DAY | General yield trend |
| `daily` | DAY | Day-by-day analysis |
| `weekly` | WEEK | Week-by-week analysis |
| `monthly` | MONTH | Month-by-month analysis |

**Example**: Daily yield for the past week
```python
result = yield_tool.analyze(YieldFilter(
    part_number="WIDGET-001",
    test_operation="FCT",
    perspective="daily",
    days=7
))
```

### Date Grouping Options

For advanced control, you can specify `date_grouping` directly:

| Value | Groups By |
|-------|-----------|
| `HOUR` | Hour |
| `DAY` | Day |
| `WEEK` | Week |
| `MONTH` | Month |
| `QUARTER` | Quarter |
| `YEAR` | Year |

### Period Count

Use `period_count` to limit the number of time periods returned:

```python
# Get last 10 days of yield
result = yield_tool.analyze(YieldFilter(
    perspective="daily",
    period_count=10
))
```

### Yield Trend Metrics

Yield trend describes **change compared to the previous equally-sized period**:

| This Period | Compared To |
|-------------|-------------|
| Today | Yesterday |
| This week | Last week |
| This month | Last month |

**Use Case**: Detecting improvement or degradation patterns.

### Safe Period Aggregation

**Key Rule**: When fetching yield over periods, the **first-pass-included rule** applies to each period.

This means:
- Units are counted only in their first-run period
- Periods can be safely summed together
- No double-counting of units across periods

**Example**: You can sum Monday-Friday yields to get a weekly total without worrying about units being counted multiple times.

---

## Top Runners

### Definition

**Top runners** = Products with the highest test volume (unit count or report count)

### Important: Volume is Per Process

A product might be a top runner in one process but not another:

| Product | ICT Volume | FCT Volume | EOL Volume |
|---------|------------|------------|------------|
| WIDGET-A | 10,000 (Top runner) | 8,000 | 5,000 |
| WIDGET-B | 5,000 | 12,000 (Top runner) | 12,000 (Top runner) |
| WIDGET-C | 8,000 | 6,000 | 3,000 |

### Finding Top Runners

```python
# Top runners for FCT process
result = yield_tool.analyze(YieldFilter(
    test_operation="FCT",
    perspective="by product",
    days=30
))
# Sort results by unit_count to find top runners
```

### Volume Context for Yield

When comparing yield, always consider volume:
- High volume + low yield = Major problem (many defects)
- Low volume + low yield = Investigate but lower priority
- High volume + high yield = Star performer

---

## The Unit Inclusion Rule (Critical!)

### Why This Rule Exists

To calculate meaningful unit-based yield (FPY, SPY, TPY, LPY), we need to see ALL runs for each unit. You cannot determine if a unit passed on its first run if you only see its second run.

### The Rule

> **A unit is included in the dataset only if its FIRST RUN falls within the filter parameters.**
>
> **If the unit is included, ALL its runs are considered in the calculation, even if some runs fall outside the filter.**

### What This Means in Practice

When you filter by date range, station, operator, or any other dimension:

1. WATS finds all units where **Run 1** matches the filter
2. For those units, WATS includes **all runs** (Run 1, 2, 3, etc.) regardless of filter
3. This ensures mathematically correct FPY-LPY calculations

### Example

**Filter**: Station = "Line1-FCT", Date = "2024-12-01"

| Unit | Run 1 | Run 2 | Included? |
|------|-------|-------|-----------|
| SN001 | Line1-FCT on Dec 1 | Line2-FCT on Dec 2 | ✅ Yes (Run 1 matches) |
| SN002 | Line1-FCT on Nov 30 | Line1-FCT on Dec 1 | ❌ No (Run 1 outside date) |
| SN003 | Line2-FCT on Dec 1 | Line1-FCT on Dec 1 | ❌ No (Run 1 at different station) |

**Important**: SN001's Run 2 is counted even though it's at a different station and date!

---

## The Repair Line Problem

### The Scenario

Many production sites use a **dedicated repair line**:

```
┌─────────────────────┐     ┌─────────────────────┐
│    Main Line        │     │   Repair Line       │
│    (Station-A)      │     │   (Station-B)       │
│                     │     │                     │
│  Unit arrives       │     │  Failed units       │
│  Run 1 executed  ───┼────▶│  Run 2, 3, etc.     │
│                     │     │                     │
│  PASS → Ship        │     │  PASS → Ship        │
│  FAIL → Repair Line │     │  FAIL → Scrap/Retry │
└─────────────────────┘     └─────────────────────┘
```

### The Confusion

When you view yield **by station**, the repair line shows:

| Station | Units | Reports | FPY | Retests |
|---------|-------|---------|-----|---------|
| Station-A (Main) | 1,000 | 1,100 | 85% | 100 |
| Station-B (Repair) | **0** | 150 | **N/A** | 150 |

**Why 0 units for Station-B?**

Because Station-B never sees Run 1. All units arriving at Station-B already had their Run 1 at Station-A. Following the Unit Inclusion Rule, no units are attributed to Station-B for unit-based yield.

### Common Questions

> "Why does my repair station show 0 units but 150 test reports?"

The 150 reports are Run 2/3/4 etc. for units whose Run 1 happened at the main line. The unit count is 0 because no unit's first run was at the repair station.

> "Is the repair station working? How do I measure its performance?"

Use **TRY (Test Report Yield)** instead of FPY. This measures the success rate of test attempts at that specific station.

---

## When to Use Each Metric

### Use FPY, SPY, TPY, LPY When:

✅ Measuring **overall process quality**  
✅ Reporting **production yield** to stakeholders  
✅ Comparing yield **across products**  
✅ Tracking yield **over time**  
✅ Analyzing **entire production lines**  

### Use TRY When:

✅ Measuring **individual station performance**  
✅ Comparing **fixtures** or **test equipment**  
✅ Evaluating **operator performance**  
✅ Analyzing **repair line efficiency**  
✅ Any scenario where you're filtering to a subset of runs  

### Decision Guide

```
Is the filter likely to exclude some runs for a unit?
│
├─ NO  → The filter includes all stations/fixtures the unit touches
│        → Use FPY, SPY, TPY, LPY (unit-based yield)
│
└─ YES → Filtering by specific station, fixture, operator, etc.
         │
         ├─ Is this where Run 1 happens?
         │  ├─ YES → FPY/LPY are meaningful
         │  └─ NO  → FPY/LPY will show 0 units, use TRY instead
         │
         └─ Use TRY (report-based yield) for station/fixture/operator performance
```

---

## Interpreting the Metrics

### Comparing Unit Count vs Report Count

| Scenario | Units | Reports | Meaning |
|----------|-------|---------|---------|
| Units = Reports | 100 | 100 | No retests (FPY = LPY) |
| Units < Reports | 100 | 130 | 30 retests occurred |
| Units = 0, Reports > 0 | 0 | 50 | This filter only sees retests (use TRY) |

### Calculating Retest Rate

```
Retest Rate = (Reports - Units) / Units × 100%
```

**Note**: This only works when Units > 0. If Units = 0, you're looking at a retest-only view.

---

## Examples

### Example 1: Overall Production Yield

**Question**: "What's the yield for WIDGET-001 last month?"

**Answer**: Use FPY/LPY grouped by product or overall.
- FPY = 92% (92% passed first time)
- LPY = 98.5% (98.5% eventually passed)

### Example 2: Station Performance

**Question**: "How is our repair station (Station-B) performing?"

**Answer**: Use TRY for Station-B.
- TRY = 75% (75% of repair attempts succeed)
- This tells you 25% of units need multiple repair attempts

### Example 3: Operator Comparison

**Question**: "Which operator has the best test yield?"

**Answer**: Use TRY grouped by operator.
- Operator A: TRY = 94%
- Operator B: TRY = 91%
- Operator C: TRY = 96%

**Caution**: If operators only work at certain stations, make sure you're comparing apples to apples.

### Example 4: Fixture Analysis

**Question**: "Fixture-7 seems problematic. What's its yield?"

**Answer**: Use TRY for Fixture-7.
- If Fixture-7 TRY is significantly lower than other fixtures, it may need calibration or replacement.

---

## Adaptive Time Filtering (High-Volume Production)

### The Problem with 30-Day Defaults

For **high-volume production environments**, the default 30-day window can be problematic:

| Volume Level | Daily Units | 30 Days = | Impact |
|--------------|-------------|-----------|--------|
| Very High | 100,000+ | 3 million+ | ❌ API timeout, memory issues |
| High | 10,000-100,000 | 300K-3M | ⚠️ Slow queries, excessive data |
| Medium | 1,000-10,000 | 30K-300K | ✅ Manageable |
| Low | <1,000 | <30K | ✅ Fine, might need more days |

### Adaptive Time Filter

The adaptive time filter **automatically adjusts the date range** based on production volume:

```python
# Enable adaptive time filtering
result = yield_tool.analyze(YieldFilter(
    part_number="HIGH-VOLUME-PRODUCT",
    test_operation="FCT",
    adaptive_time=True  # Let the system decide optimal window
))
```

### How It Works

1. **Start Small**: Begin with 1 day of data
2. **Evaluate Volume**: Check unit/report counts
3. **Expand if Needed**: If too few records, double the window
4. **Stop When Sufficient**: When target record count is reached (default: 100)

### Volume Categories

The system automatically categorizes production volume:

| Category | Units/Day | Typical Window |
|----------|-----------|----------------|
| Very High | >100,000 | 1-3 days |
| High | 10,000-100,000 | 3-7 days |
| Medium | 1,000-10,000 | 7-14 days |
| Low | 100-1,000 | 14-30 days |
| Very Low | <100 | 30-90 days |

### When to Use Adaptive Time

- ✅ High-volume production environments
- ✅ When you don't know the volume ahead of time
- ✅ For general queries without specific date requirements
- ❌ When you need a specific date range (use explicit dates instead)

---

## Process Terminology

### Types of Operations

WATS uses different terminology depending on the workflow:

| Term | Used For | Records |
|------|----------|---------|
| `test_operation` | Testing | UUT (Unit Under Test) / UUTReport |
| `repair_operation` | Repair logging | UUR (Unit Under Repair) / UURReport |
| `wip_operation` | Production tracking | WIP records |

### Common Confusion

When users ask about "process" or "operation", they almost always mean `test_operation`:

> "What's the yield for PCBA?" → Filter by `test_operation="PCBA test"`

> "Show FCT failures" → Filter by `test_operation="FCT"`

### Repair vs Test Operations

- **Test operations**: Where units are tested (FPY, yields apply)
- **Repair operations**: Where units are repaired (no yield concept, just repair actions)

Most yield analysis uses `test_operation`. Only use `repair_operation` when specifically analyzing repair workflow.

---

## The Mixed Process Problem

### The Scenario

Some customers send **different test types to the same process**:

```
┌─────────────────────────────────────────────────────────┐
│           Process: "Structural Tests"                   │
│                                                         │
│   AOI Test (sw_filename: "aoi_test.exe")               │
│   ICT Test (sw_filename: "ict_test.exe")               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### The Problem

When multiple test types share a process:

1. **First test type (AOI)** runs → Creates Run 1 → Determines units/FPY
2. **Second test type (ICT)** runs → Treated as "retest after pass"
3. **ICT shows 0 units** because AOI already "passed" those units

### Symptoms

| Symptom | Cause |
|---------|-------|
| "ICT shows 0 units but has reports" | AOI ran first, ICT is seen as retest |
| "FPY doesn't make sense for this process" | Mixed test types in one process |
| "Unit counts don't match between test types" | Different sw_filename = different "tests" |

### Diagnosis

Look for **different `sw_filename` values** in reports to the same process:

```sql
-- Conceptual query (internal use)
SELECT DISTINCT sw_filename, COUNT(*) 
FROM reports 
WHERE test_operation = 'Structural Tests'
GROUP BY sw_filename
```

If you see multiple sw_filename values (e.g., "aoi_test.exe" and "ict_test.exe"), you have a mixed process problem.

### Solutions

| Solution | Pros | Cons |
|----------|------|------|
| **Separate processes** | Clean data, proper yields | Requires reconfiguration |
| **Accept it** | No changes needed | Misleading yield numbers |
| **Use sw_filename filter** | Can analyze each test type | More complex queries |

### Recommendation

**Best practice**: Each test type should have its own `test_operation`.

```
❌ Wrong:
   Process "Structural Tests" → AOI + ICT

✅ Correct:
   Process "AOI Test" → AOI only
   Process "ICT Test" → ICT only
```

---

## Process Name Matching

### Fuzzy Matching

Users often use imprecise process names. The system attempts fuzzy matching:

| User Says | Might Match |
|-----------|-------------|
| "PCBA" | "PCBA test", "PCBA Test Station" |
| "board test" | "PCBA test", "Board Test" |
| "ict" | "ICT", "ICT Test", "In-Circuit Test" |
| "fct" | "FCT", "FCT Test", "Functional Test" |
| "eol" | "EOL", "EOL Test", "End of Line" |

### Common Aliases

The system recognizes common manufacturing test abbreviations:

| Abbreviation | Full Name |
|--------------|-----------|
| ICT | In-Circuit Test |
| FCT | Functional Test |
| AOI | Automated Optical Inspection |
| AXI | Automated X-ray Inspection |
| EOL | End-of-Line |
| FQC | Final Quality Check |
| SPI | Solder Paste Inspection |

### When Matching Fails

If the system can't find a match:
1. **Suggestions** are provided (closest matches)
2. **User confirmation** may be requested
3. **List available processes** using `perspective="by operation"`

```python
# See all available processes
result = yield_tool.analyze(YieldFilter(
    part_number="WIDGET-001",
    perspective="by operation"
))
# Returns list of all processes with yield data for this product
```

---

## Summary Table

| Metric | Based On | Use For | Affected by Repair Line Problem? |
|--------|----------|---------|----------------------------------|
| FPY | Units | Overall process quality | ❌ No (when used correctly) |
| SPY | Units | Retest effectiveness | ❌ No |
| TPY | Units | Extended retest analysis | ❌ No |
| LPY | Units | Final production yield | ❌ No |
| TRY | Reports | Station/fixture/operator performance | ✅ Yes (this is the solution!) |

---

## Troubleshooting

### "My station shows 0 units but has test reports"

**Cause**: This station only performs retests. Units' first runs are at another station.

**Solution**: Use TRY to evaluate this station's performance.

### "Yield numbers don't match between reports"

**Possible causes**:
1. Different time filters (units included based on Run 1 date)
2. Comparing unit-based (FPY) vs report-based (TRY) yield
3. Different grouping dimensions

### "Retest count seems high"

**Check**: Are you looking at a retest-only station? If Units = 0, all reports are retests by definition.

---

## Glossary

| Term | Definition |
|------|------------|
| **Unit** | A single device/product being tested (identified by serial number) |
| **Run** | A single test execution for a unit (Run 1, Run 2, etc.) |
| **Report** | The test result document from a single run |
| **Retest** | Any run after Run 1 (Run 2, 3, 4, etc.) |
| **Process** | A test operation (e.g., FCT, EOL, ICT) |
| **RTY** | Rolled Throughput Yield - product of FPY across all processes |
| **Top Runner** | Product with highest test volume (per process) |

---

## Unit Verification Rules

### What Are They?

Unit Verification Rules define which test operations (processes) must pass for each product. They answer: "What tests must this product complete before it can ship?"

### Example Rule

```
Product: WIDGET-001
Required processes (in order):
1. ICT - In-Circuit Test
2. FCT - Functional Test  
3. EOL - End-of-Line Test
4. FQC - Final Quality Check (optional for some SKUs)
```

### Using Verification Rules

**Via API**: Functions exist to query and manage unit verification rules
- Get required processes for a product
- Check if a unit has completed all required tests
- Define new verification rules

### Common Issue: Rules Not Maintained

Many customers don't keep verification rules up-to-date. However, yield data can suggest what rules should be:

**Agent Opportunity**: Analyze yield data to auto-suggest verification rules:
1. Query yield by operation for a product
2. Identify all processes with significant volume
3. Suggest creating verification rule with those processes
4. Present to user for confirmation

```python
# Example: Discover processes for a product
result = yield_tool.analyze(YieldFilter(
    part_number="WIDGET-001",
    perspective="by operation",
    days=90  # Look at 3 months of data
))

# Result might show:
# - ICT: 50,000 units, FPY 98%
# - FCT: 48,000 units, FPY 95%
# - EOL: 45,000 units, FPY 99%
# 
# Suggested verification rule: ICT → FCT → EOL
```

---

## Dimensional Analysis for Failure Modes

### The Analysis Workflow

When yield drops, use **dimensional analysis** to find the cause:

```
┌────────────────────────────────────────────────────────────────────┐
│                    YIELD ANALYSIS WORKFLOW                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  1. DETECT        2. DIAGNOSE         3. ISOLATE      4. FIX      │
│  ─────────        ───────────         ─────────       ────        │
│  Yield Tool   →   Dimensional     →   Root Cause  →  Action      │
│  (by process)     Analysis            Analysis                    │
│                   (by dimension)      (by step)                   │
│                                                                    │
│  "FPY dropped     "Station-3 is       "Voltage Test   "Calibrate  │
│   to 88%"         10% lower"          failing 25%"    Station-3"  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Using Dimensions for Root Cause

**Dimensions** are grouping factors. By querying yield with different dimensions, you can detect patterns:

| Query Dimension | Finding | Likely Cause |
|----------------|---------|--------------|
| `stationName` | One station is worse | Equipment issue |
| `batchNumber` | One batch is worse | Component lot issue |
| `operator` | One operator is worse | Training issue |
| `fixtureId` | One fixture is worse | Fixture wear |
| `period` | Yield declining over time | Equipment drift |
| `swFilename` | Different tests show different yields | Mixed process problem |

### Example: Finding a Batch-Specific Issue

```python
# Step 1: Notice overall yield is low
baseline = yield_tool.analyze(YieldFilter(
    part_number="WIDGET-001",
    test_operation="FCT",
    days=30
))
# FPY = 91% (target: 95%)

# Step 2: Query by batch to see if one batch is problematic
by_batch = yield_tool.analyze(YieldFilter(
    part_number="WIDGET-001",
    test_operation="FCT",
    days=30,
    dimensions="batchNumber"  # Group by batch
))

# Results:
# BATCH-001: FPY=96% (2,400 units)
# BATCH-002: FPY=97% (2,100 units)
# BATCH-003: FPY=73% (1,800 units)  ← Problem batch!
# BATCH-004: FPY=95% (1,900 units)

# Step 3: Investigate BATCH-003
# Check incoming inspection, supplier, component lot
```

### Multi-Dimensional Analysis

For complex issues, analyze multiple dimensions:

```python
# Analyze all common dimensions at once
failure_modes = dimensional_analysis_tool.analyze(FailureModeFilter(
    part_number="WIDGET-001",
    test_operation="FCT",
    days=30,
    dimensions=[
        "stationName",
        "batchNumber",
        "operator",
        "fixtureId",
        "period"
    ]
))

# Tool returns:
# - Baseline FPY
# - Each dimension value compared to baseline
# - Significance level (critical, high, moderate, low)
# - Recommendations for investigation
```

### Significance Thresholds

Not all variations matter. Look for:

| Significance | Delta from Baseline | Action |
|--------------|--------------------|---------| 
| 🔴 Critical | > 10% below | Immediate investigation |
| 🟠 High | 5-10% below | Schedule investigation |
| 🟡 Moderate | 2-5% below | Monitor and track |
| ⚪ Low | < 2% below | Normal variation |

Also consider **sample size**: 
- 100+ units = high confidence
- 20-100 units = moderate confidence
- <20 units = low confidence (could be noise)

---

## Test Step Analysis (TSA)

### When to Use TSA

After dimensional analysis identifies WHERE failures occur, use **Test Step Analysis** to find WHICH STEP is failing:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    ROOT CAUSE ANALYSIS WORKFLOW                            │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. YIELD        2. DIMENSIONAL      3. TSA            4. MEASUREMENT     │
│  ──────          ───────────         ────              ───────────        │
│  "What's         "Where/When?"       "Which step?"     "Why exactly?"     │
│  failing?"                                                                 │
│                                                                            │
│  FPY=88%    →    Station-3     →    Voltage Test   →  Cpk=0.8, drift    │
│                  is -10%            causing 90%        near upper limit   │
│                                     of failures                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### TSA Key Concepts

#### Single Product + Process

TSA is designed for **ONE product in ONE process** at a time:
- Different products have different test sequences
- Different processes test different things
- Mixing creates confusing merged data

#### Data Integrity Check

Before analysis, TSA warns about potential data issues:

| Check | Warning | Action |
|-------|---------|--------|
| Multiple SW versions | Different test programs mixed | Filter to specific `sw_filename` |
| Multiple revisions | Different product revisions | Filter to specific `revision` |

#### Step Caused Unit Failure (Critical!)

The most important field in TSA is `step_caused_uut_failed`:

| Field | Meaning | Priority |
|-------|---------|----------|
| `step_failed_count` | Step reported failure | Medium |
| `step_caused_uut_failed` | **Step CAUSED unit to fail** | 🔴 HIGH |

**Important**: A step can fail (report failure) without being the root cause. The `step_caused_uut_*` fields identify true root causes.

### Process Capability (Cpk)

For measurements, TSA provides Cpk analysis:

| Cpk Value | Status | Meaning |
|-----------|--------|---------|
| ≥ 1.33 | ✅ Capable | Process is good (3-sigma coverage) |
| 1.0-1.33 | ⚠️ Marginal | Improvement needed |
| 0.67-1.0 | ❌ Incapable | Action required |
| < 0.67 | 🚨 Critical | URGENT - high defect rate |

### TSA Priority Order

When reviewing TSA results:

1. **🔴 CRITICAL**: Steps with `step_caused_uut_failed > 0` (root causes)
2. **⚠️ CpK CONCERNS**: Measurements with Cpk < 1.33
3. **📊 HIGH FAILURE**: Steps with >5% failure rate

### Example: TSA Workflow

```python
# Step 1: Get step analysis
result = step_analysis_tool.analyze(StepAnalysisInput(
    part_number="PCBA-001",
    test_operation="FCT",
    days=30
))

# Step 2: Review overall summary
print(f"Average Cpk: {result.overall_summary.avg_cpk}")
print(f"Capable: {result.overall_summary.capable_count}")
print(f"Incapable: {result.overall_summary.incapable_count}")

# Step 3: Check critical steps (caused failures)
for step in result.critical_steps:
    print(f"⚠️ {step.step_name}: {step.caused_unit_fail} unit failures")
    if step.cpk:
        print(f"   Cpk: {step.cpk:.2f}")

# Step 4: Check Cpk concerns
for step in result.cpk_concerns:
    print(f"📉 {step.step_name}: Cpk={step.cpk:.2f}")
```

### TSA vs Other Tools

| Tool | Question Answered | When to Use |
|------|-------------------|-------------|
| Yield Tool | What's failing? | First step - overall picture |
| Dimensional Analysis | Where/when? | Find failure modes |
| **TSA** | **Which step?** | **Find root cause step** |
| Process Capability | Is it stable? Dual Cpk? | Deep capability analysis |
| Measurement Tool | Why exactly? | Deep dive on specific measurement |

---

## Process Capability Analysis (Advanced)

Process Capability Analysis builds on TSA when you need deeper statistical assessment of measurements with Cpk concerns.

### When to Use Process Capability Analysis

Use after TSA when you see:
- Measurements with Cpk below 1.33 (marginal or incapable)
- Questions about process stability
- Need to understand failure impact on capability
- Looking for hidden modes (trends, outliers, drift)

### Dual Cpk Analysis

WATS provides two Cpk datasets:

| Dataset | Description | Shows |
|---------|-------------|-------|
| **Cpk (all)** | Includes all measurements | Actual capability |
| **Cpk_wof** | Without failures | Potential capability |

**Key insight**: If Cpk << Cpk_wof, failures are significantly impacting capability. Address failure root cause FIRST.

```
Example:
  Cpk = 0.9 (actual with failures)
  Cpk_wof = 1.5 (potential without failures)
  
  Interpretation: Fix the failures and capability should improve to ~1.5
```

### Stability Assessment

**CRITICAL**: Always check stability before trusting Cpk!

An unstable process makes Cpk meaningless because it will change over time.

Stability issues to detect:
- **Trends**: Mean drifting up or down
- **Shifts**: Sudden mean changes
- **Outliers**: Values beyond 3σ
- **High variance**: 6σ spread exceeds spec range
- **Bimodal**: Two populations mixed (σ_wof << σ)

### Hidden Mode Detection

| Mode Type | Description | Action |
|-----------|-------------|--------|
| Centering | Process off-center (Cp >> Cpk) | Adjust process center |
| Approaching limit | Mean < 3σ from limit | High risk of failures |
| High variance | 6σ > spec range | Reduce variation |
| Bimodal | Two populations | Find root cause of split |

### Process Capability Workflow

```python
# Step 1: TSA identifies Cpk concerns
tsa_result = step_analysis_tool.analyze(...)

# Step 2: Deep dive on concerning measurements  
if tsa_result.cpk_concerns:
    cap_result = capability_tool.analyze(ProcessCapabilityInput(
        part_number="PCBA-001",
        test_operation="FCT",
        step_path="Main/Voltage Test/*",  # Focus on concern
        days=30
    ))
    
    # Step 3: Check stability first
    if cap_result.unstable_count > 0:
        print("⚠️ UNSTABLE - fix stability before trusting Cpk!")
        for m in cap_result.unstable_measurements:
            print(f"  {m.step_name}: {m.stability.issues}")
    
    # Step 4: Check dual Cpk
    for m in cap_result.failure_impacted:
        print(f"Failures impact: Cpk {m.dual_cpk.cpk_all:.2f} → "
              f"{m.dual_cpk.cpk_wof:.2f} (wof)")
    
    # Step 5: Check hidden modes
    for m in cap_result.all_measurements:
        for mode in m.stability.hidden_modes:
            print(f"Hidden mode: {mode.mode_type.value} - {mode.description}")
```

### Improvement Priority Matrix

| Priority | Criteria | Action |
|----------|----------|--------|
| 🔴 Critical | Cpk < 0.67 OR Unstable | Immediate action |
| 🟠 High | Cpk < 1.0 OR Approaching limits | Address soon |
| 🟡 Medium | Cpk 1.0-1.33 OR Centering issue | Plan improvement |
| 🟢 Low | Cpk ≥ 1.33 AND Stable | Monitor only |

### Dimensional Considerations

For dimensional analysis within process capability (by station, operator, etc.):
- Make separate API calls with dimension filters
- Compare results across dimensions
- Aggregate data can hide variation between dimensions

---

## Need Help?

If you're unsure which metric to use:

1. **Define what you're trying to measure** (units vs test attempts)
2. **Consider what data your filter will include** (all runs or partial)
3. **Choose the appropriate metric** (FPY-LPY for units, TRY for reports)

For failure mode detection:
1. **Start with yield_tool** to see overall yield by process
2. **Use dimensional analysis** to find which factors correlate with low yield
3. **Investigate specific findings** with test_step_analysis and measurement tools

For process capability analysis:
1. **Start with TSA** to identify measurements with Cpk concerns
2. **Use Process Capability Analysis** for stability, dual Cpk, hidden modes
3. **Deep dive with measurement tools** for distribution analysis

Contact support if you need assistance interpreting your yield data.
