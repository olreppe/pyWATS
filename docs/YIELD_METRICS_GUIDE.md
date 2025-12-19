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

## Need Help?

If you're unsure which metric to use:

1. **Define what you're trying to measure** (units vs test attempts)
2. **Consider what data your filter will include** (all runs or partial)
3. **Choose the appropriate metric** (FPY-LPY for units, TRY for reports)

Contact support if you need assistance interpreting your yield data.
