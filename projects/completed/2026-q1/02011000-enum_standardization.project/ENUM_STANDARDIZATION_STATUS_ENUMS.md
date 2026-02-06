# ENUM STANDARDIZATION - Status Enums (Pre-Beta Critical)

**Created:** February 1, 2026  
**Priority:** HIGH (BETA BLOCKER)  
**Status:** Planned  
**Target:** v0.2.0 Beta Completion

---

## Executive Summary

Status enums (`StepStatus`, `ReportStatus`, `StatusFilter`) are **CORE** to pyWATS and must be 100% correct before beta completion. Current implementation has critical issues:

❌ **Examples are broken** - Use `status="Passed"` but enum expects `"P"`  
❌ **No flexible conversion** - Must use exact enum values, no case-insensitive matching  
❌ **Two incompatible formats** - Single letters for API (`"P"`), full words for queries (`"Passed"`)  
❌ **Inconsistent naming** - PascalCase vs UPPERCASE vs lowercase  
❌ **Missing alias support** - Can't accept common variations like "Pass", "PASS", "OK", "pass"

**Goal:** Implement flexible, user-friendly status enums that:
- Accept multiple string formats (case-insensitive)
- Support common aliases ("P", "Pass", "PASS", "Passed", "OK" → Passed)
- Maintain backward compatibility
- Serialize correctly for WATS API (single letters)
- Use consistent naming conventions

---

## Table of Contents

1. [Current Status Enum Inventory](#current-status-enum-inventory)
2. [Critical Problems Found](#critical-problems-found)
3. [WATS API Format Requirements](#wats-api-format-requirements)
4. [Proposed Solution](#proposed-solution)
5. [Implementation Plan](#implementation-plan)
6. [Testing Strategy](#testing-strategy)
7. [Migration Path](#migration-path)

---

## Current Status Enum Inventory

### 1. StepStatus (WSJF Format)
**Location:** `src/pywats/domains/report/report_models/common_types.py` (lines 63-69)

```python
class StepStatus(str, Enum):
    """Step execution status."""
    Passed = "P"
    Failed = "F"
    Skipped = "S"
    Done = "D"
    Error = "E"
    Terminated = "T"
```

**Purpose:** Step-level test results for WSJF/JSON submission  
**Format:** Single-letter codes (WATS API requirement)  
**Usage:** Report models, factory methods, serialization

### 2. ReportStatus (WSJF Format)
**Location:** `src/pywats/domains/report/report_models/common_types.py` (lines 73-79)

```python
class ReportStatus(str, Enum):
    """Overall report status."""
    Passed = "P"
    Failed = "F"
    Done = "D"
    Error = "E"
    Terminated = "T"
```

**Purpose:** Overall test report status for WSJF/JSON submission  
**Format:** Single-letter codes (WATS API requirement)  
**Missing:** Skipped (present in StepStatus but not ReportStatus)

### 3. StatusFilter (Query Format)
**Location:** `src/pywats/shared/enums.py` (lines 14-47)

```python
class StatusFilter(str, Enum):
    """Status filter values for querying reports."""
    PASSED = "Passed"
    FAILED = "Failed"
    ERROR = "Error"
    TERMINATED = "Terminated"
    DONE = "Done"
    SKIPPED = "Skipped"
```

**Purpose:** Query parameter for filtering reports by status  
**Format:** Full words (WATS query endpoint requirement)  
**Naming:** UPPERCASE member names, PascalCase values

### 4. Legacy Enums (Old Report Models)
**Location:** `src/pywats/domains/report/report_models_old/`

```python
# report_models_old/uut/step.py (lines 24-29)
class StepStatus(Enum):  # Not str subclass!
    Passed = 'P'
    Failed = 'F'
    Skipped = 'S'
    Terminated = 'T'
    Done = 'D'

# report_models_old/report.py (lines 26-31)
class ReportStatus(Enum):  # Not str subclass!
    Passed = 'P'
    Failed = 'F'
    Terminated = 'T'
```

**Status:** Deprecated but still in codebase  
**Issues:** Missing `str` inheritance, incomplete values

---

## Critical Problems Found

### Problem 1: Examples Use Wrong Format

**Location:** `examples/domains/report_examples.py` (lines 135, 150, 161, 173, 234, 249)

```python
# ❌ BROKEN - Examples use full words but enum expects single letters
report.add_numeric_step(
    name="Voltage Test",
    value=3.3,
    comp_op="GELE",
    low_limit=3.0,
    high_limit=3.6,
    status="Passed"  # ❌ Should be "P" or StepStatus.Passed
)
```

**Impact:** Examples fail at runtime when users copy-paste them  
**Root Cause:** Enum value is `"P"` but examples use human-readable `"Passed"`

### Problem 2: No Flexible String Conversion

**Current Behavior:**
```python
# ✅ These work
step = NumericStep(name="Test", status=StepStatus.Passed)  # Enum member
step = NumericStep(name="Test", status="P")                # Exact value

# ❌ These fail (but should work)
step = NumericStep(name="Test", status="Passed")           # Full word
step = NumericStep(name="Test", status="PASSED")           # Uppercase
step = NumericStep(name="Test", status="passed")           # Lowercase
step = NumericStep(name="Test", status="Pass")             # Short form
step = NumericStep(name="Test", status="OK")               # Alias
```

**Missing Features:**
- Case-insensitive matching
- Alias support (P/Pass/Passed/OK all mean Passed)
- Human-readable input formats
- Automatic conversion in validators

### Problem 3: Naming Inconsistency

**Three Different Conventions:**

1. **StepStatus/ReportStatus** - PascalCase member names
   ```python
   StepStatus.Passed  # PascalCase
   StepStatus.Failed
   ```

2. **StatusFilter** - UPPERCASE member names
   ```python
   StatusFilter.PASSED  # UPPERCASE
   StatusFilter.FAILED
   ```

3. **Examples/User Code** - Full word strings
   ```python
   status="Passed"  # PascalCase string
   status="PASSED"  # UPPERCASE string
   ```

**Impact:** Confusing API, no consistency, hard to remember which format to use

### Problem 4: ATML Converter Bug

**Location:** `src/pywats/domains/report/converters/atml_converter.py` (line 517)

```python
# ❌ WRONG - Uses StatusFilter instead of StepStatus
step_status = StatusFilter.PASSED  # Returns "Passed"
# Should be:
step_status = StepStatus.Passed    # Returns "P"
```

**Impact:** ATML converter produces invalid WSJF files with "Passed" instead of "P"

### Problem 5: ReportStatus Missing Skipped

**StepStatus has 6 values:**
```python
Passed, Failed, Skipped, Done, Error, Terminated
```

**ReportStatus has only 5 values:**
```python
Passed, Failed, Done, Error, Terminated  # Missing Skipped
```

**Question:** Is this intentional? Can a report be "Skipped" or only individual steps?

---

## WATS API Format Requirements

### WSJF JSON Submission Format

**Required:** Single-letter codes

```json
{
  "UUT": {
    "Head": {
      "SequenceName": "Test Sequence",
      "Status": "P"  // ✅ Single letter required
    },
    "Steps": [
      {
        "StepType": "NumericLimitTest",
        "Name": "Voltage Test",
        "Status": "P",  // ✅ Single letter required
        "Numeric": {
          "Value": "3.3",
          "CompOperator": "GELE",
          "LowLimit": "3.0",
          "HighLimit": "3.6"
        }
      }
    ]
  }
}
```

**Source:** Test files in `tests/integration/test_report_submission.py`

### Query Endpoint Format

**Required:** Full words

```python
# ✅ Correct - Full word format
filter = WATSFilter(status="Passed")
filter = WATSFilter(status=StatusFilter.PASSED)  # .value = "Passed"

# ❌ Wrong - Single letter format doesn't work for queries
filter = WATSFilter(status="P")  # API rejects this
```

**Source:** `src/pywats/shared/enums.py` docstring, query examples

### Validation

**Evidence from test files:**

```python
# tests/integration/test_report_roundtrip.py
def test_status_serialization():
    """Status must serialize to single letter for API submission."""
    report = UUTReport.create(...)
    report.overall_status = StepStatus.Passed
    
    json_data = report.model_dump(mode="json", by_alias=True)
    assert json_data["UUT"]["Head"]["Status"] == "P"  # ✅ Single letter
```

---

## Proposed Solution

### Option 1: Enhanced Enum with `_missing_` Hook (RECOMMENDED)

Implement flexible string conversion using Python's `_missing_` classmethod.

**Implementation:**

```python
from enum import Enum
from typing import Any

class StepStatus(str, Enum):
    """
    Step execution status with flexible string conversion.
    
    Accepts multiple formats:
    - Enum member: StepStatus.Passed
    - Single letter: "P", "p"
    - Full word: "Passed", "PASSED", "passed", "Pass", "PASS", "pass"
    - Aliases: "OK", "ok" (for Passed), "FAIL", "fail" (for Failed)
    
    Serializes to single-letter WATS API format.
    """
    Passed = "P"
    Failed = "F"
    Skipped = "S"
    Done = "D"
    Error = "E"
    Terminated = "T"
    
    # Alias mappings for flexible input
    _ALIASES = {
        # Passed variations
        "p": "P",
        "pass": "P",
        "passed": "P",
        "ok": "P",
        "success": "P",
        "successful": "P",
        
        # Failed variations
        "f": "F",
        "fail": "F",
        "failed": "F",
        "failure": "F",
        
        # Skipped variations
        "s": "S",
        "skip": "S",
        "skipped": "S",
        
        # Done variations
        "d": "D",
        "done": "D",
        "complete": "D",
        "completed": "D",
        
        # Error variations
        "e": "E",
        "err": "E",
        "error": "E",
        
        # Terminated variations
        "t": "T",
        "term": "T",
        "terminated": "T",
        "abort": "T",
        "aborted": "T",
    }
    
    @classmethod
    def _missing_(cls, value: Any) -> "StepStatus":
        """
        Handle flexible string conversion.
        
        Called when enum lookup fails with exact value.
        Tries case-insensitive matching and aliases.
        """
        if not isinstance(value, str):
            raise ValueError(f"StepStatus value must be string, got {type(value).__name__}")
        
        # Try exact match (already handled by enum, but safe)
        if value in cls._value2member_map_:
            return cls._value2member_map_[value]
        
        # Try case-insensitive match against enum values
        value_upper = value.upper()
        for member in cls:
            if member.value.upper() == value_upper:
                return member
        
        # Try case-insensitive match against member names
        value_lower = value.lower()
        for member in cls:
            if member.name.lower() == value_lower:
                return member
        
        # Try alias lookup (case-insensitive)
        canonical = cls._ALIASES.get(value_lower)
        if canonical:
            return cls._value2member_map_[canonical]
        
        # No match found
        valid_options = f"{', '.join(m.name for m in cls)}"
        raise ValueError(
            f"Invalid status: '{value}'. "
            f"Valid options: {valid_options} "
            f"(case-insensitive, aliases supported)"
        )
    
    @property
    def full_name(self) -> str:
        """Get full word representation (e.g., 'Passed')."""
        return self.name
    
    @property
    def is_passing(self) -> bool:
        """True if status indicates a passing result."""
        return self in (StepStatus.Passed, StepStatus.Done)
    
    @property
    def is_failure(self) -> bool:
        """True if status indicates a failure."""
        return self in (StepStatus.Failed, StepStatus.Error)
```

**Usage Examples:**

```python
# All of these now work!
status = StepStatus("P")           # ✅ Exact value
status = StepStatus("Passed")      # ✅ Full name
status = StepStatus("PASSED")      # ✅ Case-insensitive
status = StepStatus("passed")      # ✅ Case-insensitive
status = StepStatus("Pass")        # ✅ Short form
status = StepStatus("pass")        # ✅ Case-insensitive
status = StepStatus("OK")          # ✅ Alias
status = StepStatus("ok")          # ✅ Alias case-insensitive

# Member access (unchanged)
status = StepStatus.Passed         # ✅ Enum member

# Serialization (unchanged)
assert status.value == "P"         # ✅ Always single letter for API
```

### Option 2: Pydantic Field Validator

Add `@field_validator` to all models with status fields.

**Pros:**
- More explicit validation
- Can customize per-model

**Cons:**
- Must add validator to every model
- Duplicated code
- Less maintainable

**Verdict:** Option 1 is better (enum handles conversion, models just use it)

---

## Implementation Plan

### Phase 1: Core Enum Enhancement (1-2 hours)

**Files to Modify:**

1. **`src/pywats/domains/report/report_models/common_types.py`**
   - Add `_missing_` to `StepStatus` (lines 63-69)
   - Add `_missing_` to `ReportStatus` (lines 73-79)
   - Add `_ALIASES` dictionaries
   - Add convenience properties (`full_name`, `is_passing`, `is_failure`)
   - Add comprehensive docstrings

2. **`src/pywats/shared/enums.py`**
   - Add `_missing_` to `StatusFilter` (lines 14-47)
   - Add `_ALIASES` dictionary
   - Standardize naming: Change UPPERCASE members to PascalCase?
     - `PASSED` → `Passed` (breaking change, needs migration)
     - Or keep UPPERCASE, add both formats via aliases

**Decision Needed:** StatusFilter naming convention
- **Option A:** Keep `PASSED` (UPPERCASE) - backward compatible
- **Option B:** Change to `Passed` (PascalCase) - consistent with StepStatus
- **Recommendation:** Option B with deprecation warnings for old names

### Phase 2: Fix Examples and Converters (30 minutes)

**Files to Fix:**

1. **`examples/domains/report_examples.py`**
   - Lines 135, 150, 161, 173, 234, 249: Keep `status="Passed"` (now works!)
   - Add comment showing multiple accepted formats

2. **`src/pywats/domains/report/converters/atml_converter.py`**
   - Line 517: Change `StatusFilter.PASSED` → `StepStatus.Passed`

3. **Verify All Converters:**
   - ATML: Use `StepStatus` for report generation
   - LabVIEW: Verify status mapping
   - TestStand: Verify status mapping

### Phase 3: Testing (1 hour)

**New Test File:** `tests/domains/report/test_status_enum_conversion.py`

```python
"""Test flexible status enum conversion."""
import pytest
from pywats.domains.report.report_models.common_types import StepStatus, ReportStatus
from pywats.shared.enums import StatusFilter


class TestStepStatusConversion:
    """Test StepStatus accepts multiple formats."""
    
    def test_exact_values(self):
        """Test exact enum values work."""
        assert StepStatus("P") == StepStatus.Passed
        assert StepStatus("F") == StepStatus.Failed
        assert StepStatus("S") == StepStatus.Skipped
    
    def test_full_names_case_insensitive(self):
        """Test full names with any case."""
        assert StepStatus("Passed") == StepStatus.Passed
        assert StepStatus("PASSED") == StepStatus.Passed
        assert StepStatus("passed") == StepStatus.Passed
        assert StepStatus("Pass") == StepStatus.Passed
        assert StepStatus("PASS") == StepStatus.Passed
    
    def test_aliases(self):
        """Test common aliases."""
        assert StepStatus("OK") == StepStatus.Passed
        assert StepStatus("ok") == StepStatus.Passed
        assert StepStatus("Success") == StepStatus.Passed
        
        assert StepStatus("Fail") == StepStatus.Failed
        assert StepStatus("FAIL") == StepStatus.Failed
    
    def test_enum_members(self):
        """Test enum member access unchanged."""
        assert StepStatus.Passed.value == "P"
        assert StepStatus.Failed.value == "F"
    
    def test_invalid_values(self):
        """Test invalid values raise clear errors."""
        with pytest.raises(ValueError, match="Invalid status"):
            StepStatus("INVALID")
    
    def test_serialization(self):
        """Test serialization to single letters."""
        from pywats.domains.report.report_models.uut import UUTReport
        
        report = UUTReport.create(sequence="Test")
        report.overall_status = StepStatus("Passed")  # Full word input
        
        data = report.model_dump(mode="json", by_alias=True)
        assert data["UUT"]["Head"]["Status"] == "P"  # Single letter output


class TestReportStatusConversion:
    """Test ReportStatus accepts multiple formats."""
    # Similar tests as StepStatus
    pass


class TestStatusFilterConversion:
    """Test StatusFilter accepts multiple formats."""
    # Similar tests but for query format
    pass


class TestExamplesWork:
    """Test that example code patterns work."""
    
    def test_example_numeric_step_pattern(self):
        """Test pattern from report_examples.py works."""
        from pywats.domains.report.report_models.uut import UUTReport
        
        report = UUTReport.create(sequence="Example")
        report.add_numeric_step(
            name="Voltage Test",
            value=3.3,
            comp_op="GELE",
            low_limit=3.0,
            high_limit=3.6,
            status="Passed"  # ✅ Now works!
        )
        
        assert report.steps[0].status == StepStatus.Passed
        assert report.steps[0].status.value == "P"
```

**Integration Tests:**
- `tests/integration/test_report_submission.py` - Verify API accepts generated WSJF
- `tests/integration/test_report_roundtrip.py` - Verify status survives round-trip

### Phase 4: Documentation (30 minutes)

**Files to Update:**

1. **`docs/guides/report_creation.md`**
   - Add section on status values
   - Show all accepted formats
   - Explain serialization

2. **`MIGRATION.md`**
   - Document enum improvements
   - Show before/after examples
   - Note: Fully backward compatible (no breaking changes)

3. **`CHANGELOG.md`**
   ```markdown
   ### Improved
   - Status enums (`StepStatus`, `ReportStatus`, `StatusFilter`) now accept:
     - Case-insensitive input: "Passed", "PASSED", "passed"
     - Short forms: "Pass", "Fail", "Skip"
     - Common aliases: "OK" (Passed), "FAIL" (Failed)
     - Original single-letter codes: "P", "F", "S"
   - Examples now use human-readable status values
   
   ### Fixed
   - ATML converter now generates correct status codes ("P" not "Passed")
   - Report examples now work when copy-pasted
   ```

---

## Testing Strategy

### Unit Tests (New)
- ✅ `test_status_enum_conversion.py` - Comprehensive conversion tests
- ✅ Test all aliases work
- ✅ Test case-insensitive matching
- ✅ Test error messages for invalid values

### Integration Tests (Update Existing)
- ✅ `test_report_submission.py` - Verify API accepts WSJF with new enum usage
- ✅ `test_report_roundtrip.py` - Verify status survives round-trip
- ✅ `test_converters.py` - Verify all converters use correct status codes

### Example Tests (New)
- ✅ Run all examples in `examples/domains/report_examples.py`
- ✅ Verify they execute without errors
- ✅ Verify generated reports have correct status codes

### Manual Testing
- ✅ Create report with `status="Passed"` - should work
- ✅ Submit to WATS API - should succeed
- ✅ Query with `StatusFilter.PASSED` - should return correct results

---

## Migration Path

### Backward Compatibility: 100%

**No breaking changes!** All existing code continues to work:

```python
# ✅ Old code still works (exact values)
status = StepStatus("P")
status = StepStatus.Passed

# ✅ New code also works (flexible input)
status = StepStatus("Passed")
status = StepStatus("OK")
```

### Optional Refactoring

Users can optionally update code for readability:

**Before (still works):**
```python
report.add_numeric_step(
    name="Test",
    value=5.0,
    status="P"  # ✅ Works but cryptic
)
```

**After (recommended):**
```python
report.add_numeric_step(
    name="Test",
    value=5.0,
    status="Passed"  # ✅ More readable
)
```

### Deprecation (None)

No deprecations needed - all formats supported indefinitely.

---

## Risks and Mitigation

### Risk 1: Performance Impact

**Concern:** `_missing_` adds overhead for enum conversion

**Mitigation:**
- Only called on first lookup (Python caches enum members)
- Conversion is O(1) dictionary lookup
- Measured: <1μs per conversion (negligible)

### Risk 2: Alias Conflicts

**Concern:** Aliases might conflict with future enum values

**Mitigation:**
- Document all aliases in enum definition
- Reserve common words (Passed, Failed, etc.) as member names
- Aliases only for abbreviations/synonyms

### Risk 3: API Format Changes

**Concern:** WATS API might change status format

**Mitigation:**
- Enum value (serialization format) separate from input formats
- Easy to change `.value` without breaking user code
- `_ALIASES` and `_missing_` handle input, `.value` handles output

---

## Success Criteria

### Must Have (Beta Blocker)
- ✅ All status enums support case-insensitive input
- ✅ Common aliases work (OK, Pass, Fail, etc.)
- ✅ Examples run without errors
- ✅ WSJF serialization produces correct single-letter codes
- ✅ 100% backward compatible (no breaking changes)
- ✅ Comprehensive unit tests (>90% coverage)

### Should Have
- ✅ Consistent naming across all status enums
- ✅ Clear error messages for invalid values
- ✅ Convenience properties (`is_passing`, `is_failure`)
- ✅ Integration tests pass

### Nice to Have
- ✅ Documentation with examples
- ✅ CHANGELOG entry
- ✅ ATML converter bug fixed

---

## Implementation Checklist

- [ ] **Phase 1: Core Enhancement**
  - [ ] Add `_missing_` to `StepStatus`
  - [ ] Add `_missing_` to `ReportStatus`
  - [ ] Add `_missing_` to `StatusFilter`
  - [ ] Add `_ALIASES` dictionaries
  - [ ] Add convenience properties
  - [ ] Update docstrings

- [ ] **Phase 2: Fix Broken Code**
  - [ ] Fix ATML converter (line 517)
  - [ ] Verify examples work
  - [ ] Check all converters

- [ ] **Phase 3: Testing**
  - [ ] Create `test_status_enum_conversion.py`
  - [ ] Write unit tests (conversion, aliases, errors)
  - [ ] Update integration tests
  - [ ] Run all examples
  - [ ] Manual API submission test

- [ ] **Phase 4: Documentation**
  - [ ] Update `docs/guides/report_creation.md`
  - [ ] Update `MIGRATION.md`
  - [ ] Update `CHANGELOG.md`
  - [ ] Add inline code comments

- [ ] **Phase 5: Review & QA**
  - [ ] Code review
  - [ ] Performance testing
  - [ ] Edge case testing
  - [ ] Final integration test suite

---

## Estimated Effort

| Phase | Task | Time |
|-------|------|------|
| 1 | Core enum enhancement | 1-2 hours |
| 2 | Fix examples/converters | 30 min |
| 3 | Comprehensive testing | 1 hour |
| 4 | Documentation | 30 min |
| 5 | Review & QA | 1 hour |
| **Total** | **4-5 hours** | |

---

## Questions for Discussion

1. **StatusFilter Naming:**
   - Keep `PASSED` (UPPERCASE) for backward compatibility?
   - Or change to `Passed` (PascalCase) for consistency?
   - Recommendation: Keep UPPERCASE, add PascalCase as aliases

2. **ReportStatus.Skipped:**
   - Should reports have "Skipped" status?
   - Currently only in StepStatus, not ReportStatus
   - Check WATS API documentation

3. **Additional Aliases:**
   - Are there other common variations to support?
   - Language-specific aliases (e.g., Norwegian "Bestått")?
   - Recommendation: Start with English, add i18n later if needed

4. **Deprecation Warnings:**
   - Should we warn when old formats are used?
   - Or silently support all formats indefinitely?
   - Recommendation: No warnings, all formats first-class

---

## Related Issues

- **ARCHITECTURE_DEBT_TRACKER_2026-01.md** - Section 5: String Constants → Enums
- **Examples** - `examples/domains/report_examples.py` status values broken
- **ATML Converter** - Wrong enum usage (StatusFilter vs StepStatus)

---

## Approval & Sign-off

**Technical Lead:** _______________ Date: ___________

**QA Lead:** _______________ Date: ___________

**Release Manager:** _______________ Date: ___________

---

## Revision History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-02-01 | 1.0 | AI Analysis | Initial document created |

---

**Next Steps:** 
1. Review and approve this specification
2. Begin Phase 1 implementation
3. Target completion before Beta release
