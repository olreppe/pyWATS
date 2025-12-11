# Production Scenario Test - Status

**Date:** December 10, 2025  
**Branch:** completing-the-report-module  
**Commit:** 95ce174

## Summary

Created a comprehensive production scenario test (`tests/test_production_scenario.py`) that simulates a complete manufacturing workflow from product setup through final testing.

## Test Coverage

### 10-Step Production Workflow

1. **Product Setup**
   - Creates/updates PRODUCTION-TEST-MODULE and PRODUCTION-TEST-PCBA products
   - Creates revisions with state=ACTIVE
   - Configures BoxBuild (BOM) for Module to contain PCBA as subunit

2. **PCBA Unit Creation**
   - Creates units with incrementing serial numbers (PCBA-0001, PCBA-0002, etc.)
   - Adds to production tracking system

3. **PCBA Production Setup**
   - Sets phase to "Under Production - Queued"
   - Adds LotNumber tag (changes every 5 test runs)

4. **ICT Test**
   - Changes phase to "Under Production"
   - Sets process to ICT (code 10)
   - Creates UUTReport with test steps using proper API

5. **PCBA-TEST**
   - Sets process to PCBA-TEST (code 20)
   - 30% failure rate simulation
   - Creates UUR (repair) reports for failures
   - Retests after repair

6. **PCBA Finalization & Assembly**
   - Creates Module unit
   - Builds PCBA into Module using add_child_to_assembly()
   - Note: Assembly happens before PCBA finalization (may need adjustment)

7. **Module Test Setup**
   - Sets Module phase to "Under Production - Queued"

8. **Insulation Test**
   - Sets process to Insulation (code 30)
   - 20% failure rate
   - Creates UUR reports and retests

9. **Burn-In Test**
   - Sets process to Burn-In (code 40)
   - 15% failure rate
   - **Returns to Insulation on failure** (as specified)
   - Re-runs complete sequence after repair

10. **Final Function Test**
    - Sets process to Final Function (code 50)
    - 10% failure rate
    - **Returns to Insulation on failure**
    - Re-runs complete sequence
    - Sets Module phase to "Finalized" on success

## Code Fixes Made

### 1. Setting Model Enhancement

**File:** `src/pywats/shared/common_types.py`

```python
value: Optional[str] = Field(default=None, alias="value")  # Now allows None
```

**Reason:** API returns tags with null values that were failing validation

### 2. Production Repository Enhancement

**File:** `src/pywats/domains/production/repository.py`

```python
# Now handles batch operation responses
if isinstance(response.data, dict):
    if response.data.get('errorCount', 0) == 0:
        # Success - API returns {'okCount': 1, 'errorCount': 0, 'errors': []}
        return units
```

**Reason:** PUT /api/Production/Units returns success dict, not unit list

### 3. Report API Usage

**Correctly uses:**

- `create_uut_report()` with `operation_type` parameter
- `get_root_sequence_call()` for adding test steps
- `create_uur_report(from_uut_report)` for repairs
- `add_failure_to_main_unit()` for documenting failures

## Current Issues

### 1. Test Operation Codes

**Status:** BLOCKED  
**Issue:** Test operation codes (10, 20, 30, 40, 50) don't exist on server  
**Error:** `NotFoundError` when calling `set_unit_process()`

**Solutions:**

- **Option A:** Configure these codes on WATS server
- **Option B:** Query available operation types and use those
- **Option C:** Skip process code setting (test continues without it)

**Current:** Test catches `NotFoundError` and continues without setting process

### 2. Assembly Timing

**Status:** NEEDS REVIEW  
**Issue:** Test builds PCBA into Module before finalizing PCBA  
**Question:** Should PCBA be finalized first, or is current order correct?

## Test Features

✅ **Implemented:**

- Incrementing serial numbers per test run
- LotNumber tags that change periodically
- Random failure simulation with configurable probabilities
- Complete UUR (repair) workflow
- Return-to-Insulation logic for post-Insulation failures
- Proper UUTReport structure with test steps
- Error handling for missing server configuration

❌ **Not Implemented:**

- Multiple test runs with --count parameter (counter resets)
- Process code auto-discovery from server
- Configurable operation codes via pytest fixtures
- Visual test result reporting

## Next Steps

### Immediate (Required for Test to Run)

1. **Configure test operation codes on server** OR
2. **Modify test to query and use available operation codes**

### Enhancements (Optional)

1. Make operation codes configurable via pytest parameters
2. Add fixture to query available operations from server
3. Improve counter persistence across pytest runs
4. Add verification of BoxBuild constraints
5. Add assertions for unit phase/process state
6. Create separate test classes for each workflow step

## Files Changed

```text
src/pywats/domains/production/repository.py  - Enhanced batch response handling
src/pywats/shared/common_types.py           - Allow None in Setting.value
tests/test_production_scenario.py           - New comprehensive test (871 lines)
```

## Running the Test

```bash
# Single run
pytest tests/test_production_scenario.py -v -s

# Multiple runs (serial counter will reset each time)
pytest tests/test_production_scenario.py -v --count=3

# With specific operation codes
# TODO: Add pytest parameter support
```

## Notes

- Test uses proper pyWATS API as intended (no custom functions)
- All report creation uses UUTReport models and factory methods
- Error handling allows test to continue even if server lacks configuration
- Comprehensive logging shows test progress and decision points
- Random failures make each test run unique
