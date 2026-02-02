# Analysis - API Quality & Cleanup for v0.3.0b1

**Date:** February 2, 2026  
**Analyst:** Development Team  
**Status:** 🔍 In Progress

---

## 1. Issue #1: UUR Failure API Complexity

### Current State

**Problem:** The UUR add_failure() API for sub-units is confusing and inconsistent.

**Current Implementation:**
```python
# UURReport class
def add_failure(self, failure: UURFailure) -> None:
    """Add failure to main unit (unclear how to add to sub-units)"""
    self.failures.append(failure)

# No direct sub-unit methods
# User must manually access: uur.sub_units[idx].failures.append(failure)
```

**Pain Points:**
- No optional sub_unit_idx parameter on main add_failure()
- No dedicated add_failure_to_sub_unit() method
- UURSubUnit class doesn't have add_failure() method
- Users must directly manipulate .failures list (not Pythonic)

### Proposed Solution

**New API Design:**
```python
# UURReport class
def add_failure(
    self, 
    failure: UURFailure,
    sub_unit_idx: Optional[int] = None
) -> None:
    """Add failure to main unit or specific sub-unit.
    
    Args:
        failure: Failure instance to add
        sub_unit_idx: Optional sub-unit index (0-based). If None, adds to main unit.
    
    Raises:
        IndexError: If sub_unit_idx is out of range
    """
    if sub_unit_idx is None:
        self.failures.append(failure)
    else:
        self.sub_units[sub_unit_idx].failures.append(failure)

def add_failure_to_sub_unit(
    self,
    failure: UURFailure,
    serial_number: Optional[str] = None,
    idx: Optional[int] = None
) -> None:
    """Add failure to sub-unit by serial number or index.
    
    Args:
        failure: Failure instance to add
        serial_number: Sub-unit serial number (searches for match)
        idx: Sub-unit index (0-based)
    
    Raises:
        ValueError: If neither serial_number nor idx provided
        ValueError: If serial_number not found
        IndexError: If idx is out of range
    """
    if idx is not None:
        self.sub_units[idx].failures.append(failure)
    elif serial_number is not None:
        for sub in self.sub_units:
            if sub.serial_number == serial_number:
                sub.failures.append(failure)
                return
        raise ValueError(f"Sub-unit with serial '{serial_number}' not found")
    else:
        raise ValueError("Must provide either serial_number or idx")

# UURSubUnit class
def add_failure(self, failure: UURFailure) -> None:
    """Add failure directly to this sub-unit."""
    self.failures.append(failure)
```

**Usage Examples:**
```python
# Add to main unit
uur.add_failure(failure)

# Add to sub-unit by index
uur.add_failure(failure, sub_unit_idx=2)
uur.add_failure_to_sub_unit(failure, idx=2)

# Add to sub-unit by serial number
uur.add_failure_to_sub_unit(failure, serial_number="SUB-12345")

# Direct access pattern
uur.sub_units[2].add_failure(failure)
```

### Impact Assessment

**Files to Modify:**
- `src/pywats/domains/report/report_models/uur/uur_report.py`
- `src/pywats/domains/report/report_models/uur/uur_sub_unit.py`

**Tests to Update:**
- Add tests for new sub_unit_idx parameter
- Add tests for add_failure_to_sub_unit() with serial_number
- Add tests for add_failure_to_sub_unit() with idx
- Add tests for UURSubUnit.add_failure()
- Add error case tests (ValueError, IndexError)

**Documentation Impact:**
- Update UUR examples in docs/guides/
- Update Sphinx API docs for UURReport
- Add migration notes for users

**Breaking Changes:** None (backward compatible - adds optional parameter and new methods)

---

## 2. Issue #2: Backward Compatibility Properties

### Current State

**Problem:** Deprecated backward compatibility properties clutter the codebase.

**Found Instances:**
```python
# Example 1: uur_info -> info property
@property
def uur_info(self) -> Optional[UURInfo]:
    """Backward compatibility: uur_info is now just info."""
    return self.info

@uur_info.setter
def uur_info(self, value: UURInfo) -> None:
    """Backward compatibility: uur_info is now just info."""
    self.info = value
```

**Search Strategy:**
- Grep for "Backward compatibility" comments
- Grep for "@property" + "backward" (case-insensitive)
- Look for old property names with redirects to new names

### Proposed Solution

**Action:** Remove all backward compatibility properties and redirects.

**Rationale:**
- pyWATS is pre-1.0 (beta releases), breaking changes are acceptable
- Clutter makes code harder to maintain
- Users on 0.3.0b1 should migrate to new API
- Reduces confusion about which property to use

### Impact Assessment

**Files to Search:**
- `src/pywats/domains/report/report_models/**/*.py`
- `src/pywats/domains/*/models.py`
- `src/pywats_client/core/*.py`

**Expected Removals:**
- ~10-20 backward compatibility properties across report models
- Any similar patterns in other domains

**Breaking Changes:** YES
- Users using old property names will get AttributeError
- **Mitigation:** Document in MIGRATION.md, clearly communicate in beta release notes

**Tests to Update:**
- Remove tests for old property names
- Ensure tests use new property names consistently

---

## 3. Issue #4: Process vs Operation Type Inconsistency

### Current State

**Problem:** Inconsistent terminology for process/operation_type/operations across codebase.

**Core Issue:**
- `process` and `operation_type` are the same concept (used interchangeably)
- Generic term "operations" has no clear meaning
- Need explicit names for specific operation types:
  - **UUT Reports** → `test_operation`
  - **UUR Reports** → `repair_operation` (the repair being performed)
  - **UUR Reports** → `test_operation` (the failed test that triggered repair)

**Current Inconsistencies:**
```python
# UUTReport - sometimes "process", sometimes "operation_type"
class UUTReport:
    operation_type: str  # Should be test_operation
    process: str  # Alias?

# UURReport - unclear naming
class UURReport:
    operation_type: str  # Should be repair_operation
    test_operation: str  # Reference to failed test (correct!)
```

### Proposed Solution

**Naming Standard:**

1. **Default Field Name:** `process` (preferred in front-facing API)
2. **Alias:** `operation_type` (for backward compatibility and API endpoints)
3. **Specific Names for UUR:**
   - `repair_operation` - The repair process being performed
   - `test_operation` - The test that failed and triggered repair

**Implementation:**
```python
# UUTReport
class UUTReport(PyWATSModel):
    # Primary field
    test_operation: str = Field(..., description="Test process/operation type")
    
    # Alias for API compatibility
    @property
    def process(self) -> str:
        """Alias for test_operation."""
        return self.test_operation
    
    @property
    def operation_type(self) -> str:
        """Alias for test_operation (API compatibility)."""
        return self.test_operation

# UURReport
class UURReport(PyWATSModel):
    # Primary fields
    repair_operation: str = Field(..., description="Repair process/operation type")
    test_operation: str = Field(..., description="Failed test that triggered repair")
    
    # Aliases
    @property
    def process(self) -> str:
        """Alias for repair_operation."""
        return self.repair_operation
    
    @property
    def operation_type(self) -> str:
        """Alias for repair_operation (API compatibility)."""
        return self.repair_operation
```

**Remove Generic "Operations":**
- Search for variables/parameters named `operations` (plural)
- Rename to `operation_types` or `processes`
- Update all documentation

### Impact Assessment

**Files to Modify:**
- `src/pywats/domains/report/report_models/uut/*.py`
- `src/pywats/domains/report/report_models/uur/*.py`
- `src/pywats/domains/process/*.py` (if affected)
- All example files using these models

**API Changes:**
- Field renames (but with aliases for compatibility)
- Parameter renames in methods

**Breaking Changes:** Minimal (aliases provide compatibility)

**Documentation Impact:**
- Update all references to "operation" vs "process"
- Clarify terminology in architecture docs
- Update examples to use new field names

**Tests to Update:**
- All UUT/UUR report tests
- Integration tests for report submission
- Ensure aliases work correctly

---

## 4. Issue #5: Documentation Mock Data Hallucinations

### Current State

**Problem:** Mock data in documentation doesn't match actual Pydantic model schemas.

**Example Issues:**
```python
# Documentation shows:
vendor = Vendor(
    name="ACME Corp",
    contact_name="John Doe",    # HALLUCINATION - field doesn't exist
    email="john@acme.com",       # HALLUCINATION - field doesn't exist
    phone="555-1234"             # HALLUCINATION - field doesn't exist
)

# Actual model:
class Vendor(PyWATSModel):
    name: str  # Only field is a simple string!
```

**Why This Happens:**
- Pydantic silently ignores extra fields during serialization
- Documentation written without validating against actual models
- Copy-paste from outdated examples
- AI-generated examples not validated

### Proposed Solution

**Validation Strategy:**

1. **Manual Review:**
   - Review all `.md` files in `docs/`
   - Review all `.py` files in `examples/`
   - Compare mock data against actual Pydantic models

2. **Automated Validation (Nice to Have):**
   - Script to extract code examples from docs
   - Run examples through Python interpreter
   - Validate Pydantic model instantiation

3. **Common Hallucinations to Fix:**
   - `Vendor` - should be simple string, not object with contact fields
   - `Product` - verify all fields exist
   - `UUT/UUR` report fields - check against actual models
   - Date/time formats - ensure ISO 8601 strings where required

**Validation Script (Optional):**
```python
# scripts/validate_examples.py
import ast
import re
from pathlib import Path
from pywats.domains.report.report_models import *

def extract_code_examples(md_file: Path) -> List[str]:
    """Extract Python code blocks from markdown."""
    content = md_file.read_text()
    pattern = r'```python\n(.*?)\n```'
    return re.findall(pattern, content, re.DOTALL)

def validate_example(code: str) -> bool:
    """Try to execute example code and validate."""
    try:
        exec(code)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
```

### Impact Assessment

**Files to Review:**
- `docs/guides/*.md` - All user guides
- `docs/api/*.rst` - Sphinx documentation
- `examples/**/*.py` - All example scripts
- `README.md` - Quick start examples

**Expected Changes:**
- 50-100 mock data corrections
- Vendor name field simplifications
- Product field corrections
- Date format standardizations

**Breaking Changes:** None (documentation only)

**Effort Estimate:** 6 hours (manual review is time-consuming)

---

## 5. Issue #6: Remove Experimental Report Builder

### Current State

**Problem:** `report_builder` module is experimental and incomplete.

**Current Status:**
- Located in `src/pywats/tools/report_builder.py`
- Marked as EXPERIMENTAL in comments
- Low test coverage (~50%)
- Not widely used
- Owner wants to redo it properly

**Dependencies:**
- Check if any examples use it
- Check if any tests depend on it
- Check if documented anywhere

### Proposed Solution

**Action:** Remove the report_builder module entirely.

**Steps:**
1. Remove `src/pywats/tools/report_builder.py`
2. Remove `src/pywats/tools/test_uut.py` (if only for report_builder)
3. Remove tests in `tests/tools/test_report_builder.py`
4. Remove from `src/pywats/tools/__init__.py` exports
5. Search for imports: `from pywats.tools import report_builder`
6. Remove from documentation if mentioned

### Impact Assessment

**Files to Remove:**
- `src/pywats/tools/report_builder.py`
- `tests/tools/test_report_builder.py` (if exists)

**Files to Update:**
- `src/pywats/tools/__init__.py` - Remove exports
- Any example files that import it
- Any documentation referencing it

**Breaking Changes:** YES
- Anyone using report_builder will get ImportError
- **Mitigation:** Clearly document removal, explain it's experimental and will be redone

**Health Score Impact:**
- Tools module currently at 58/80
- Removing experimental code may improve score (less unfinished code)

---

## 6. Summary of Required Changes

### Complexity Ranking

1. **Process/Operation Type Consistency** - High complexity, affects multiple domains
2. **Documentation Data Validation** - Medium complexity, time-consuming but straightforward
3. **UUR Failure API** - Medium complexity, requires careful testing
4. **Backward Compatibility Removal** - Low complexity, search and destroy
5. **Remove Report Builder** - Low complexity, simple deletion

### Risk Analysis

**High Risk:**
- Process/operation_type changes (widespread impact)

**Medium Risk:**
- UUR API changes (affects report submission workflows)

**Low Risk:**
- Backward compatibility removal (already deprecated)
- Report builder removal (experimental code)
- Documentation fixes (no code changes)

### Recommended Approach

**Phase 1:** Low-risk changes (build confidence)
- Remove report_builder
- Remove backward compatibility properties

**Phase 2:** Medium-risk changes (test thoroughly)
- UUR failure API improvements
- Documentation data validation

**Phase 3:** High-risk changes (extensive testing)
- Process/operation_type standardization

---

## 7. Testing Strategy

### Unit Tests
- Add tests for new UUR methods
- Update tests for renamed fields
- Remove tests for deprecated code

### Integration Tests
- Test UUR report submission with new API
- Test process/operation_type in actual API calls
- Validate examples execute without errors

### Regression Tests
- Run full test suite after each phase
- Verify 416+ tests still passing
- Check mypy errors don't increase

### Manual Testing
- Submit UUT report with test_operation
- Submit UUR report with repair_operation and test_operation
- Verify API responses use correct field names

---

**Analysis Complete:** Ready for implementation planning.
