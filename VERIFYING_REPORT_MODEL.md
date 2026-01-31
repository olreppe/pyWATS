# Verifying Report Model V3 Migration

## Overview

This document tracks the verification and bug-fixing process for the V3 report model migration in pyWATS. The V3 report models have been made the default implementation at `pywats.domains.report.report_models`, with V1 archived at `report_models_old`.

## Current Status

**Test Results:** 111 passed, 25 failed, 1 skipped (out of 137 report tests)

**Last Commit:** Fix V3 report model validation and serialization (c3c8e21)

## Completed Tasks

### 1. ✅ Fix validate_serial_number / validate_part_number
**Problem:** `common_types.py` had stub implementations that didn't actually validate problematic characters.

**Solution:** Replaced stub functions with imports from `pywats.core.validation`:
```python
# In common_types.py
from pywats.core.validation import (
    validate_serial_number,
    validate_part_number,
    PROBLEMATIC_CHARS,
)
```

**Files Modified:**
- `src/pywats/domains/report/report_models/common_types.py`

### 2. ✅ Fix CompOp Enum Values
**Problem:** V3 `common_types.py` defined its own `CompOp` enum with wrong values (`CASESENSITIVESTRINGCOMPARE`) instead of the WATS API values (`CASESENSIT`).

**Solution:** Removed the duplicate `CompOp` class and imported from `pywats.shared.enums`:
```python
# In common_types.py
from pywats.shared.enums import CompOp
```

**Files Modified:**
- `src/pywats/domains/report/report_models/common_types.py`

### 3. ✅ Fix StringMeasurement Field Name
**Problem:** V3 `StringMeasurement` used `comp` field without proper aliases. V1 uses `comp_op` with `validation_alias="compOp"` and `serialization_alias="compOp"`.

**Solution:** Updated field definition to match V1:
```python
# In measurement.py
comp_op: Optional[CompOp] = Field(
    default=CompOp.LOG,
    validation_alias="compOp",
    serialization_alias="compOp",
    description="String comparison operator."
)
```

**Files Modified:**
- `src/pywats/domains/report/report_models/uut/steps/measurement.py`
- `src/pywats/domains/report/report_models/uut/steps/string_step.py`

### 4. ✅ Remove Experimental Test Directories
**Problem:** Test directories for V2/V3 comparison tests referenced non-existent modules.

**Solution:** Deleted experimental test directories:
- `tests/domains/report_models_v2/`
- `tests/domains/report_models_v3/`

### 5. ✅ Simplify test_converter_roundtrip.py
**Problem:** Test compared V1 vs V3 implementations which is no longer relevant.

**Solution:** Rewrote to test only the current implementation (deserialize → submit → load → compare).

## Remaining Test Failures (25)

### Category 1: test_models_v3.py (1 failure)
**File:** `tests/domains/report/test_models_v3.py`
**Error:** `ModuleNotFoundError: No module named 'pywats.domains.report.report_models_v3'`
**Cause:** Test file still references deleted `report_models_v3` module
**Fix:** Update imports to use current `report_models` or delete if obsolete

### Category 2: test_import_mode.py (3 failures)
**Tests:**
- `test_add_numeric_step_auto_calculates_fail`
- `test_failure_propagates_to_parent`
- `test_nested_propagation`

**Error:** `AssertionError: assert 'P' == 'F'`
**Cause:** Active mode status propagation not working - steps with failing measurements not updating parent status
**Fix:** Review V3 step validation and status propagation logic

### Category 3: test_robustness.py (7 failures)
**Tests:**
- `test_unknown_step_type_parsed_as_unknown_step`
- `test_multiple_unknown_step_types`
- `test_unknown_step_preserves_step_type_in_serialization`
- `test_mixed_known_and_unknown_steps`
- `test_validate_step_uses_correct_high_limit`
- `test_validation_detects_invalid_limits`
- `test_nested_sequence_calls_with_unknown_steps`
- `test_parent_references_with_unknown_steps`

**Error:** Various assertion errors about unknown step handling
**Cause:** V3 step discriminator not handling unknown step types correctly
**Fix:** Review step type discrimination and unknown step fallback

### Category 4: test_step_discriminator.py (4 failures)
**Tests:**
- `test_step_type_literals_in_serialization`
- `test_step_type_discrimination_on_deserialization`
- `test_parent_references_after_deserialization`
- `test_step_path_generation`

**Error:** Various assertion errors about step types and parent references
**Cause:** V3 step type handling differs from V1 expectations
**Fix:** Review step_type literals (should use ET_NLT format) and parent reference restoration

### Category 5: test_integration.py (6 failures)
**Tests:**
- `test_send_uut_report` - Server validation: "Cannot have limit with LOG"
- `test_send_uut_report_from_test_tool` - Same
- `test_send_uur_report` - Missing required UUR fields
- `test_create_uur_from_uut_object` - `None == UUID` assertion
- `test_create_uur_from_part_and_process` - `None == 100` assertion
- `test_complete_repair_workflow` - `add_failure()` signature mismatch

**Cause:** Multiple issues - test data generation, UUR model fields, method signatures
**Fix:** Review test utilities and UUR model implementation

### Category 6: test_service.py (1 failure)
**Test:** `test_create_uur_report_from_uut_copies_sub_units`
**Error:** `None == 100` assertion
**Cause:** UUR creation from UUT not copying process_code correctly
**Fix:** Review UUR creation logic

### Category 7: test_timezone.py (1 failure)
**Test:** `test_server_roundtrip_preserves_timezone`
**Error:** Same "Cannot have limit with LOG" server validation
**Cause:** Test data uses LOG comp_op with limits
**Fix:** Update test data to use correct comp_op or remove limits

### Category 8: test_report_builder.py (1 failure)
**Test:** `test_misc_info`
**Error:** `'NoneType' object has no attribute 'append'`
**Cause:** misc_infos not initialized
**Fix:** Review ReportBuilder initialization

## Architecture Notes

### Directory Structure
```
src/pywats/domains/report/
├── report_models/          # V3 (current default)
│   ├── common_types.py     # Shared types, imports from pywats.shared.enums
│   ├── report.py           # Base Report class
│   ├── uut/                # UUT (test) report models
│   │   ├── uut_report.py
│   │   └── steps/          # Step types
│   └── uur/                # UUR (repair) report models
│       ├── uur_report.py
│       └── uur_sub_unit.py
├── report_models_old/      # V1 (archived)
└── report_models_v2/       # V2 (exists but not used)
```

### Key Patterns
- **Field naming:** Python uses `snake_case`, JSON uses `camelCase`
- **Aliases:** Use `validation_alias` for deserializing, `serialization_alias` for serializing
- **CompOp values:** Use WATS API values: `LOG`, `EQ`, `NE`, `GELE`, `CASESENSIT`, `IGNORECASE`, etc.
- **Step types:** Use TestStand format like `ET_NLT`, `ET_SVT`, `SequenceCall`

### Original API Surface (must maintain)
- `UUTReport(pn, sn, rev, process_code, station_name, location, purpose, ...)`
- `UURReport(pn, sn, rev, process_code, station_name, location, purpose, ...)`
- `report.root.add_numeric_step(name, value, comp_op, low_limit, high_limit, ...)`
- `report.root.add_string_step(name, value, comp_op, limit, ...)`
- `report.root.add_sequence_call(name, ...)`

## Next Steps

1. **Fix test_models_v3.py** - Update imports or delete if obsolete
2. **Fix test_import_mode.py** - Review active mode status propagation
3. **Fix test_robustness.py** - Review unknown step handling
4. **Fix test_step_discriminator.py** - Review step type literals
5. **Fix integration tests** - Review test utilities and UUR model
6. **Run full test suite** - Verify all report tests pass

## How to Continue

```powershell
# Run report tests
cd "c:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS"
python -m pytest tests/domains/report/ -v --tb=short

# Run specific failing test
python -m pytest tests/domains/report/test_import_mode.py -v --tb=long

# Run all tests
python -m pytest tests/ --tb=no -q
```

## References

- V1 implementation: `src/pywats/domains/report/report_models_old/`
- Shared enums: `src/pywats/shared/enums.py` (CompOp, StepStatus, etc.)
- Core validation: `src/pywats/core/validation.py` (validate_serial_number, etc.)
