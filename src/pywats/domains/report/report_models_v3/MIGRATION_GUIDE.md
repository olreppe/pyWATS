# Report Models v3 - Migration & Compatibility Guide

**Created:** January 30, 2026  
**Audience:** pyWATS users migrating from v1 to v3

---

## 1. Executive Summary

**v3 is a refinement of v1, not a rewrite.**

| Change Type | Impact |
|-------------|--------|
| Import path | **Must change** |
| Report creation | **No change** |
| Factory methods | **No change** |
| StepList usage | **No change** |
| Info access | **No change** |
| JSON output | **Identical** |

**Most users:** Change import path, done.

---

## 2. What Stays THE SAME

### 2.1 Report Creation

```python
# v1 AND v3 - IDENTICAL
report = UUTReport(
    pn="PART-001",
    sn="SN-001", 
    rev="A",
    process_code=100,
    station_name="Station1",
    location="TestLab",
    purpose="Production"
)
```

### 2.2 Getting Root Sequence

```python
# v1 AND v3 - IDENTICAL
root = report.get_root_sequence_call()
```

### 2.3 Factory Methods

```python
# v1 AND v3 - IDENTICAL
root.add_numeric_step(
    name="VoltageTest",
    value=5.0,
    unit="V",
    comp_op=CompOp.GELE,
    low_limit=4.5,
    high_limit=5.5
)

root.add_boolean_step(name="SmokeTest", status="P")

root.add_string_step(name="FWVersion", value="1.2.3", comp_op=CompOp.LOG)

root.add_sequence_call(name="SubTest", file_name="sub.seq", version="1.0")

root.add_chart_step(name="WaveformChart", chart_type=ChartType.LineChart, ...)

root.add_generic_step(step_type=FlowType.Statement, name="Setup")
```

### 2.4 Multi-Measurement Steps

```python
# v1 AND v3 - IDENTICAL
multi = root.add_multi_numeric_step(name="MultiTest")
multi.add_measurement(name="M1", value=1.0, unit="V")
multi.add_measurement(name="M2", value=2.0, unit="V")
```

### 2.5 Report Helper Methods

```python
# v1 AND v3 - IDENTICAL
report.add_misc_info("BuildDate", "2026-01-30")
report.add_sub_unit(part_type="Module", sn="MOD-001", pn="MOD-PN", rev="A")
report.add_asset(sn="ASSET-001", usage_count=42)
```

### 2.6 Info Access

```python
# v1 AND v3 - IDENTICAL
report.info.operator = "John"
report.info.fixture_id = "FIX-001"
report.info.exec_time = 45.5

# JSON output is also identical:
# {"uut": {"user": "John", "fixtureId": "FIX-001", "execTime": 45.5}}
```

### 2.7 StepList Behavior

```python
# v1 AND v3 - IDENTICAL
# Parent injection happens automatically:
step = NumericStep(name="DirectStep", ...)
root.steps.append(step)
print(step.parent.name)  # "MainSequence Callback"

# Polymorphic retrieval works:
for step in root.steps:
    if isinstance(step, SequenceCall):
        print(f"Subsequence: {step.name}")
    elif isinstance(step, NumericStep):
        print(f"Numeric: {step.measurement.value}")
```

### 2.8 JSON Output

**v3 produces IDENTICAL JSON to v1.** This is non-negotiable.

```json
{
  "type": "T",
  "pn": "PART-001",
  "sn": "SN-001",
  "uut": {
    "user": "John",
    "fixtureId": "FIX-001"
  },
  "root": {
    "stepType": "SequenceCall",
    "name": "MainSequence Callback",
    "steps": [
      {
        "stepType": "ET_NLT",
        "name": "VoltageTest",
        "numericMeas": [{"value": 5.0, "unit": "V", "status": "P"}]
      }
    ]
  }
}
```

---

## 3. What Changes

### 3.1 Import Path (Required)

```python
# v1 (current)
from pywats.domains.report.report_models import UUTReport, UURReport
from pywats.domains.report.report_models import NumericStep, BooleanStep

# v3 (new)
from pywats.domains.report.report_models_v3 import UUTReport, UURReport
from pywats.domains.report.report_models_v3 import NumericStep, BooleanStep
```

**Migration:** Find and replace `report_models` → `report_models_v3`

### 3.2 C# Name Aliases (Optional, New Feature)

v3 adds C# naming aliases for discoverability:

```python
# v3 adds these aliases - use whichever you prefer:
from pywats.domains.report.report_models_v3 import (
    BooleanStep,         # Python name (original)
    PassFailStep,        # C# name (alias)
    
    MultiBooleanStep,    # Python name (original)
    MultiPassFailStep,   # C# name (alias)
    
    StringStep,          # Python name (original)
    StringValueStep,     # C# name (alias)
    
    MultiStringStep,     # Python name (original)
    MultiStringValueStep,# C# name (alias)
)

# Both work identically:
PassFailStep is BooleanStep  # True
```

### 3.3 UURSubUnit Now Inherits SubUnit (Internal Fix)

```python
# v1 - UURSubUnit was standalone
# v3 - UURSubUnit properly inherits SubUnit

# This doesn't change your code, but enables:
from pywats.domains.report.report_models_v3 import SubUnit, UURSubUnit

sub = UURSubUnit(pn="PART", sn="SN", rev="A")
isinstance(sub, SubUnit)  # True in v3, was False in v1
```

---

## 4. Migration Checklist

### 4.1 Minimal Migration (5 minutes)

- [ ] Replace import: `report_models` → `report_models_v3`
- [ ] Run tests
- [ ] Done!

### 4.2 Full Migration (Optional)

- [ ] Replace imports
- [ ] Consider using C# aliases if team prefers those names
- [ ] Update documentation to clarify info/JSON naming
- [ ] Run tests
- [ ] Done!

---

## 5. Info Field Clarification

This isn't a code change, but v3 documents this better:

### The Pattern

| Python Code | JSON Field |
|-------------|------------|
| `report.info` | `"uut"` (for UUTReport) |
| `report.info` | `"uur"` (for UURReport) |
| `report.info.operator` | `"uut": {"user": "..."}` |

### Why?

The WATS API expects `"uut"` / `"uur"` in JSON. But in Python code, `report.info` is cleaner than `report.uut` because:

- Avoids `uut.uut.operator` (confusing!)
- `report.info.operator` reads naturally
- Works the same for UUT and UUR reports

**No code change needed** - this is just documentation clarification.

---

## 6. Coexistence Period

During migration, **both v1 and v3 are available**:

```python
# Use v1 for existing code
from pywats.domains.report.report_models import UUTReport as UUTReportV1

# Use v3 for new code
from pywats.domains.report.report_models_v3 import UUTReport as UUTReportV3

# Both produce identical JSON!
report_v1 = UUTReportV1(pn="ABC", sn="001", ...)
report_v3 = UUTReportV3(pn="ABC", sn="001", ...)

report_v1.model_dump_json() == report_v3.model_dump_json()  # True
```

---

## 7. FAQ

### Q: Do I need to change my step creation code?
**A:** No. All factory methods (`add_numeric_step()`, etc.) work identically.

### Q: Do I need to change how I access report fields?
**A:** No. `report.pn`, `report.info.operator`, etc. all work the same.

### Q: Will my JSON output change?
**A:** No. v3 produces byte-for-byte identical JSON to v1.

### Q: Do I need to update tests?
**A:** Only import paths. All assertions should pass unchanged.

### Q: What if I use `MultiNumericStep` directly?
**A:** It still exists and works the same way. Just update the import path.

### Q: Should I use `BooleanStep` or `PassFailStep`?
**A:** They're identical - use whichever your team prefers.

---

## 8. Getting Help

If you encounter issues:

1. Check this guide for the specific pattern
2. Compare JSON output: `report.model_dump_json(by_alias=True)`
3. Review [V3_ARCHITECTURE.md](V3_ARCHITECTURE.md) for design details
4. Review [VERSION_COMPARISON.md](VERSION_COMPARISON.md) for v1 vs v3 differences
