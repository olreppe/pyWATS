# Converter Refactoring Status

## Overview

This document tracks the refactoring of all converters from dict-based to UUTReport model-based implementations.

**Critical Rule:** ALL converters MUST use the pyWATS UUTReport model - NO raw dictionaries! If a feature is missing from the API, that's an API problem to fix. NO WORKAROUNDS!

## Completed Refactoring (V2 Converters)

| Converter | Location | Status | Notes |
|-----------|----------|--------|-------|
| json_format_converter_v2.py | converters/ | ✅ Complete | Reference implementation |
| teradyne_ict_converter_v2.py | src/pywats_client/converters/standard/ | ✅ Complete | Uses UUTReport model |
| klippel_log_converter_v2.py | converters/ | ✅ Complete | Uses UUTReport model |
| teradyne_spectrum_ict_converter_v2.py | src/pywats_client/converters/standard/ | ✅ Complete | Uses UUTReport model |
| kitron_seica_xml_converter_v2.py | src/pywats_client/converters/standard/ | ✅ Complete | Uses UUTReport model |

## Pending Refactoring

| Converter | Location | Priority | Notes |
|-----------|----------|----------|-------|
| spea_converter.py | converters/ | High | 627 lines, uses dict |
| xj_log_converter.py | converters/ | High | 485 lines, uses dict |
| xml_format_converter.py | converters/ | Medium | Uses dict |
| ict_converter.py | converters/ | Medium | Uses dict |
| json_format_converter.py | converters/ | Low | Has V2 already |

## API Fixes Applied

1. **add_sequence_call() return type** - Added `-> 'SequenceCall'` return type annotation to `sequence_call.py`

## Key Patterns for Refactoring

### Old Pattern (BAD - DO NOT USE)
```python
report: Dict[str, Any] = {
    "type": "Test",
    "processCode": operation_code,
    "partNumber": part_number,
    # ...
}
root_step = {"type": "SEQ", "name": "Root", "stepResults": []}
root_step["stepResults"].append({"type": "NT", "name": step_name, ...})
```

### New Pattern (CORRECT - USE THIS)
```python
from pywats.domains.report.report_models import UUTReport
from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp

report = UUTReport(
    pn=part_number,
    sn=serial_number,
    rev=part_revision,
    process_code=operation_code,
    station_name=station_name,
    location="Production",
    purpose="Test Purpose",
    result="P",  # or "F"
    start=start_time,
)

# Add misc info
report.add_misc_info(description="key", value="value")

# Get root sequence
root = report.get_root_sequence_call()
root.name = sequence_name
root.sequence.version = sequence_version

# Add sequence
seq = root.add_sequence_call(name="TestGroup", file_name="TestGroup.seq")

# Add numeric step
seq.add_numeric_step(
    name=step_name,
    value=measurement,
    unit=unit,
    comp_op=CompOp.GELE,
    low_limit=low,
    high_limit=high,
    status="P",  # or "F"
)

# Add boolean step
seq.add_boolean_step(name=step_name, status="P")

# Add string step
seq.add_string_step(name=step_name, value=string_value, status="P")

# Return result with UUTReport instance
return ConverterResult.success_result(
    report=report,  # UUTReport instance, not dict!
    post_action=PostProcessAction.MOVE,
)
```

## C# to pyWATS Method Mapping

| C# WATS API | pyWATS API |
|------------|------------|
| `api.CreateUUTReport(...)` | `UUTReport(pn=..., sn=..., ...)` |
| `uut.GetRootSequenceCall()` | `report.get_root_sequence_call()` |
| `uut.AddMiscUUTInfo(desc, val)` | `report.add_misc_info(description=desc, value=val)` |
| `seq.AddSequenceCall(name)` | `seq.add_sequence_call(name=name)` |
| `seq.AddNumericLimitStep(name).AddTest(...)` | `seq.add_numeric_step(name=..., value=..., ...)` |
| `seq.AddPassFailStep(name).AddTest(passed)` | `seq.add_boolean_step(name=..., status=...)` |
| `seq.AddStringValueStep(name).AddTest(val)` | `seq.add_string_step(name=..., value=...)` |
| `seq.AddMultiNumericStep(name)` | `seq.add_multi_numeric_step(name=...)` |
| `multiStep.AddTest(...)` | `multi_step.add_measurement(...)` |

## Status Values

- Report result: `"P"` (Passed), `"F"` (Failed)
- Step status: `"P"` (Passed), `"F"` (Failed), `"S"` (Skipped), `"D"` (Done)

## CompOp Values

```python
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp

CompOp.LOG   # Log only, no limits
CompOp.EQ    # Equal to
CompOp.NE    # Not equal to
CompOp.LT    # Less than
CompOp.LE    # Less than or equal
CompOp.GT    # Greater than
CompOp.GE    # Greater than or equal
CompOp.GELE  # Greater/equal low, less/equal high (most common)
CompOp.GTLT  # Greater than low, less than high
CompOp.GELT  # Greater/equal low, less than high
CompOp.GTLE  # Greater than low, less/equal high
```

## Next Steps

1. Replace remaining converters with V2 versions
2. Test all V2 converters with real data
3. Deprecate and remove old dict-based converters
4. Update any examples/documentation to use V2 pattern
