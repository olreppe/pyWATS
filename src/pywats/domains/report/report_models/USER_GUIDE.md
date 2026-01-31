# Report Models - User Guide

**Updated:** February 1, 2026  
**Audience:** pyWATS users

---

## 1. Overview

The pyWATS report models provide Pydantic-based classes for creating and submitting test reports to WATS. The models support:

- **UUT Reports** (Unit Under Test) - Test results from production testing
- **UUR Reports** (Unit Under Repair) - Repair documentation

---

## 2. Quick Start

### 2.1 Creating a UUT Report

```python
from datetime import datetime
from pywats.domains.report import UUTReport
from pywats.shared.enums import CompOp

# Create report
report = UUTReport(
    pn="PART-001",
    sn="SN-001", 
    rev="A",
    process_code=100,
    station_name="Station1",
    location="TestLab",
    purpose="Production",
    result="P",
    start=datetime.now().astimezone()
)

# Get root sequence to add steps
root = report.get_root_sequence_call()

# Add a numeric limit test
root.add_numeric_step(
    name="Voltage Test",
    value=3.3,
    unit="V",
    comp_op=CompOp.GELE,
    low_limit=3.0,
    high_limit=3.6,
    status="P"
)

# Add a pass/fail test
root.add_boolean_step(name="Self Test", status="P")

# Add a string value test
root.add_string_step(
    name="Firmware Version",
    value="1.2.3",
    comp_op=CompOp.LOG,
    status="P"
)
```

### 2.2 Creating a UUR Report

```python
from pywats.domains.report import UURReport

# Create repair report
uur = UURReport(
    pn="PART-001",
    sn="SN-001",
    rev="A",
    process_code=500,  # Repair process code
    station_name="RepairStation",
    location="RepairLab",
    purpose="Repair",
    result="P",
    start=datetime.now().astimezone()
)

# Add failure info
uur.add_failure_to_main_unit(
    category="Component",
    code="CAPACITOR",
    comment="Replaced C12"
)
```

---

## 3. Step Types

### 3.1 Numeric Steps

For testing measured values against limits:

```python
# Single numeric test
root.add_numeric_step(
    name="Current Draw",
    value=1.5,
    unit="A",
    comp_op=CompOp.GELE,  # Greater or Equal, Less or Equal
    low_limit=1.0,
    high_limit=2.0,
    status="P"
)

# Multi-numeric test (multiple measurements in one step)
multi = root.add_multi_numeric_step(name="Power Rails", status="P")
multi.add_measurement(name="3.3V", value=3.31, unit="V", 
                      comp_op=CompOp.GELE, low_limit=3.1, high_limit=3.5, status="P")
multi.add_measurement(name="5V", value=5.02, unit="V",
                      comp_op=CompOp.GELE, low_limit=4.8, high_limit=5.2, status="P")
```

### 3.2 Boolean Steps (Pass/Fail)

For simple pass/fail tests:

```python
# Single boolean test
root.add_boolean_step(name="Connectivity Test", status="P")

# Multi-boolean test
multi = root.add_multi_boolean_step(name="Health Checks", status="P")
multi.add_measurement(name="CPU OK", status="P")
multi.add_measurement(name="Memory OK", status="P")
```

### 3.3 String Steps

For testing string values:

```python
# Log a string value
root.add_string_step(
    name="Serial Number",
    value="ABC123",
    comp_op=CompOp.LOG,  # Just log, don't compare
    status="P"
)

# Compare string values
root.add_string_step(
    name="Model ID",
    value="MODEL-X",
    comp_op=CompOp.CASESENSIT,  # Case-sensitive comparison
    limit="MODEL-X",
    status="P"
)
```

### 3.4 Sequence Calls (Nesting)

For organizing tests into groups:

```python
# Add nested sequence
power_tests = root.add_sequence_call(
    name="Power Supply Tests",
    file_name="power_tests.seq",
    version="1.0"
)

# Add steps to nested sequence
power_tests.add_numeric_step(name="Voltage", value=5.0, ...)
power_tests.add_boolean_step(name="Regulation", status="P")
```

---

## 4. Comparison Operators (CompOp)

| Operator | Description | Limits Used |
|----------|-------------|-------------|
| `LOG` | Log value only | None |
| `EQ` | Equal to | `low_limit` |
| `NE` | Not equal to | `low_limit` |
| `GE` | Greater or equal | `low_limit` |
| `LE` | Less or equal | `low_limit`* |
| `GT` | Greater than | `low_limit` |
| `LT` | Less than | `low_limit`* |
| `GELE` | Between (inclusive) | Both |
| `GELT` | Low inclusive, high exclusive | Both |
| `GTLT` | Strictly between | Both |
| `GTLE` | Low exclusive, high inclusive | Both |

*Note: For `LE` and `LT`, the limit value goes in `low_limit` field.

---

## 5. Import Locations

```python
# Main report classes
from pywats.domains.report import UUTReport, UURReport

# Or from report_models directly
from pywats.domains.report.report_models import UUTReport, UURReport

# Enums
from pywats.shared.enums import CompOp, StepStatus

# Step types (if needed directly)
from pywats.domains.report.report_models.uut.steps import (
    SequenceCall,
    NumericStep,
    BooleanStep,
    StringValueStep,
)
```

---

## 6. JSON Serialization

```python
# Serialize to JSON (for API submission)
json_str = report.model_dump_json(by_alias=True, exclude_none=True)

# Deserialize from JSON
report = UUTReport.model_validate_json(json_str)
```

---

## 7. Common Patterns

### 7.1 Setting Report Result Based on Steps

```python
# After adding all steps
if any(step.status == "F" for step in root.steps):
    report.result = "F"
else:
    report.result = "P"
```

### 7.2 Adding Attachments

```python
from pywats.domains.report.report_models import Attachment

report.attachments = [
    Attachment(
        name="test_log.txt",
        content_type="text/plain",
        data=base64.b64encode(log_content.encode()).decode()
    )
]
```

### 7.3 Adding Misc Info

```python
from pywats.domains.report.report_models import MiscInfo

report.misc_infos.append(MiscInfo(
    description="Test Configuration",
    text="Test in debug mode"
))
```

---

## 8. Architecture Reference

```
pywats/domains/report/report_models/
├── __init__.py          # Main exports
├── report.py            # Base Report class
├── common_types.py      # Shared types and enums
├── uut/                 # UUT-specific models
│   ├── uut_report.py    # UUTReport class
│   ├── uut_info.py      # UUTInfo class
│   └── steps/           # Step types
│       ├── sequence_call.py
│       ├── numeric_step.py
│       ├── boolean_step.py
│       ├── string_step.py
│       └── ...
└── uur/                 # UUR-specific models
    ├── uur_report.py    # UURReport class
    ├── uur_info.py      # UURInfo class
    └── uur_sub_unit.py  # UURSubUnit with failures
```
