# WATS Domain Knowledge for AI Agents

This document contains essential domain knowledge for AI agents working with WATS (Web-based Automated Test System). Understanding these concepts is crucial for correctly interpreting and answering questions about manufacturing test data.

---

## Core Concepts

### Units, Reports, and Runs

| Term | Definition |
|------|------------|
| **Unit** | A single device/product being tested, identified by serial number |
| **Report** | The test result document from a single test execution |
| **Run** | A test execution sequence number (Run 1, Run 2, etc.) |
| **Retest** | Any run after Run 1 |

**Key relationship**: One unit can have multiple reports (one per run).

### Process / Test Operation

A **process** (also called **test_operation**) is a type of test a product goes through:

- ICT (In-Circuit Test)
- FCT (Functional Test)
- EOL (End-of-Line Test)
- FQC (Final Quality Check)
- etc.

**Critical**: A product typically goes through MULTIPLE processes. Each process has its own yield metrics.

---

## Yield Metrics (Critical Knowledge!)

### The Process Context Rule

**Every yield question must be considered in the context of a specific process.**

❌ **Ambiguous**: "What's the yield for WIDGET-001?"
✅ **Clear**: "What's the FCT yield for WIDGET-001?"
✅ **Clear**: "What's the RTY for WIDGET-001?" (overall across all processes)

### Unit-Based Yield (FPY, SPY, TPY, LPY)

| Metric | Name | Definition |
|--------|------|------------|
| FPY | First Pass Yield | % of units passed on Run 1 |
| SPY | Second Pass Yield | % of units passed by Run 2 |
| TPY | Third Pass Yield | % of units passed by Run 3 |
| LPY | Last Pass Yield | % of units eventually passed |

**Relationship**: FPY ≤ SPY ≤ TPY ≤ LPY

### Report-Based Yield (TRY)

| Metric | Name | Definition |
|--------|------|------------|
| TRY | Test Report Yield | Passed reports ÷ All reports |

**Use TRY for**: Station performance, fixture comparison, operator evaluation, repair line analysis.

### Rolled Throughput Yield (RTY)

**RTY = FPY₁ × FPY₂ × ... × FPYₙ**

RTY represents the probability that a unit passes ALL processes on the first try.

**Example**:
```
ICT FPY = 98%
FCT FPY = 95%
EOL FPY = 99%

RTY = 0.98 × 0.95 × 0.99 = 92.2%
```

**Use RTY for**: Overall product quality assessment, comparing products across entire flow.

### The Unit Inclusion Rule

**A unit is included in yield calculations ONLY if its FIRST RUN matches the filter.**

If included, ALL runs for that unit are counted (even runs outside the filter).

**Implications**:
- Filtering by retest-only stations shows 0 units
- Date filters apply to Run 1, not all runs
- Solution for retest stations: Use TRY instead of FPY

### The Repair Line Problem

Repair/retest stations never see Run 1 (they only handle failed units from main line).

**Result**: Unit-based yield shows 0 units for repair stations.
**Solution**: Use TRY (report-based yield) to evaluate repair station performance.

---

## Top Runners

### Definition

**Top runners** = Products with the highest test volume (unit count or report count).

### The Per-Process Rule

**Volume must be considered PER PROCESS.**

A product might be a top runner in FCT but not in EOL:

| Product | FCT Volume | EOL Volume |
|---------|------------|------------|
| WIDGET-A | 10,000 ⭐ | 5,000 |
| WIDGET-B | 8,000 | 12,000 ⭐ |

### Finding Top Runners

```python
# Top runners for FCT process
yield_tool.analyze(YieldFilter(
    test_operation="FCT",
    perspective="by product",
    days=30
))
# Results sorted by unit_count shows top runners
```

---

## Handling Ambiguous Questions

### Question: "What's the yield for WIDGET-001?"

**Best response approach**:

1. **Check if single process**: Query with `part_number="WIDGET-001"` and `perspective="by operation"`
   - If only ONE process: Answer with that process's yield
   - If MULTIPLE processes: Ask user to clarify

2. **Clarify with user**:
   - "WIDGET-001 goes through 3 processes (ICT, FCT, EOL). Which process yield would you like?"
   - "Or would you like the RTY (Rolled Throughput Yield) across all processes?"

3. **Default suggestion**: If user doesn't specify, show yield by operation so they can see all processes.

### Question: "Show me the top runners"

**Best response approach**:

1. Ask for process context: "Top runners for which process? (e.g., FCT, EOL)"
2. Or show overall volume by product across all processes as starting point
3. Then drill down to specific process if needed

---

## Unit Verification Rules

### What They Are

Rules that define which processes must pass for each product before it can ship.

### Example Rule

```
Product: WIDGET-001
Required tests: ICT → FCT → EOL
```

### Common Issue

Many customers don't maintain verification rules, even though the API supports them.

### Agent Opportunity

Analyze yield data to SUGGEST verification rules:

1. Query: `part_number="WIDGET-001", perspective="by operation", days=90`
2. Identify all processes with significant volume
3. Suggest: "Based on test data, WIDGET-001 should require: ICT → FCT → EOL"
4. Offer to create the rule (if agent has edit permissions)

---

## Quick Reference: When to Use Each Metric

| Question Type | Recommended Metric |
|--------------|-------------------|
| Product quality (single process) | FPY, LPY |
| Product quality (overall) | RTY |
| Station performance | TRY |
| Fixture comparison | TRY |
| Operator performance | TRY |
| Repair line efficiency | TRY |
| Trend analysis | FPY or TRY (per context) |
| Top runners | Unit count by product (per process) |

---

## Checklist for Yield Questions

1. ☐ Is the process/test_operation specified?
2. ☐ Is unit-based (FPY) or report-based (TRY) yield appropriate?
3. ☐ Are we dealing with a retest-only station? (Use TRY)
4. ☐ Is volume context needed? (Top runners = high volume)
5. ☐ Should RTY be calculated? (Overall quality across processes)

---

## API Tips

### Discover Processes for a Product

```python
yield_tool.analyze(YieldFilter(
    part_number="WIDGET-001",
    perspective="by operation",
    days=30
))
```

### Find Top Runners for a Process

```python
yield_tool.analyze(YieldFilter(
    test_operation="FCT",
    perspective="by product",
    days=30
))
# Sort results by unit_count descending
```

### Get RTY Components

Query each process individually and multiply FPYs:

```python
# Get all process yields
result = yield_tool.analyze(YieldFilter(
    part_number="WIDGET-001",
    perspective="by operation",
    days=30
))

# RTY = product of all FPY values
rty = 1.0
for process in result.data:
    rty *= (process.first_pass_yield / 100)
rty *= 100  # Convert back to percentage
```

---

## Summary

The most important things to remember:

1. **Yield is per process** - Always clarify which test operation
2. **RTY for overall quality** - Multiply FPYs across all processes
3. **TRY for equipment/operator** - Especially for retest stations
4. **Top runners are per process** - Volume varies by test operation
5. **Unit Inclusion Rule** - First run determines inclusion
