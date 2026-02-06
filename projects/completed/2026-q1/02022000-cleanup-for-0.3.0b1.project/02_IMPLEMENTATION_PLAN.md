# Implementation Plan - API Quality & Cleanup for v0.3.0b1

**Date:** February 2, 2026  
**Status:** 📋 Ready to Execute

---

## Phase 1: Remove Experimental Code (2 hours)

**Goal:** Clean up experimental report_builder module.

### Step 1.1: Identify Dependencies (30 min)

```powershell
# Search for report_builder imports
grep -r "from pywats.tools import report_builder" src/ examples/
grep -r "from pywats.tools.report_builder" src/ examples/
grep -r "import.*report_builder" src/ examples/

# Check documentation references
grep -r "report_builder" docs/
```

### Step 1.2: Remove Files (15 min)

```powershell
# Remove main file
rm src/pywats/tools/report_builder.py

# Remove test file (if exists)
rm tests/tools/test_report_builder.py

# Remove test utilities (if only for report_builder)
rm src/pywats/tools/test_uut.py
```

### Step 1.3: Update Exports (15 min)

**File:** `src/pywats/tools/__init__.py`
```python
# Remove report_builder exports
# Before:
from .report_builder import UUTReportBuilder

# After:
# (removed)
```

### Step 1.4: Remove Documentation References (30 min)

- Search `docs/` for any mention of report_builder
- Remove or update examples
- Update tools documentation

### Step 1.5: Verify (30 min)

```powershell
# Run tests
pytest tests/

# Check mypy
mypy src/pywats

# Verify import works
python -c "from pywats import pyWATS"
```

---

## Phase 2: Remove Backward Compatibility (3 hours)

**Goal:** Remove all deprecated backward compatibility properties.

### Step 2.1: Search for Backward Compatibility Code (1 hour)

```powershell
# Search for backward compatibility patterns
grep -r "Backward compatibility" src/pywats/
grep -ri "backward compat" src/pywats/
grep -r "@property" src/pywats/ | grep -i "backward"

# Search for common old property names
grep -r "uur_info" src/pywats/
grep -r "def uur_info" src/pywats/
```

### Step 2.2: Create Removal List (30 min)

Document all backward compatibility properties found:
```markdown
| File | Old Property | New Property | Line Number |
|------|--------------|--------------|-------------|
| uur_report.py | uur_info | info | 123 |
| ... | ... | ... | ... |
```

### Step 2.3: Remove Properties (1 hour)

**Example:** `src/pywats/domains/report/report_models/uur/uur_report.py`

```python
# REMOVE:
@property
def uur_info(self) -> Optional[UURInfo]:
    """Backward compatibility: uur_info is now just info."""
    return self.info

@uur_info.setter
def uur_info(self, value: UURInfo) -> None:
    """Backward compatibility: uur_info is now just info."""
    self.info = value
```

### Step 2.4: Update Tests (30 min)

- Remove tests using old property names
- Update to use new property names
- Run test suite

### Step 2.5: Document Breaking Changes (30 min)

**File:** `MIGRATION.md`

```markdown
## v0.3.0b1 Breaking Changes

### Removed Backward Compatibility Properties

The following deprecated properties have been removed:

#### UURReport
- `uur_info` → Use `info` instead

#### [Other models]
- `old_property` → Use `new_property` instead

**Migration Example:**
```python
# Before
uur.uur_info = UURInfo(...)

# After
uur.info = UURInfo(...)
```
```

---

## Phase 3: UUR Failure API Improvements (6 hours)

**Goal:** Simplify UUR failure addition with sub-unit support.

### Step 3.1: Implement add_failure() Enhancement (2 hours)

**File:** `src/pywats/domains/report/report_models/uur/uur_report.py`

```python
def add_failure(
    self,
    failure: UURFailure,
    sub_unit_idx: Optional[int] = None
) -> None:
    """Add failure to main unit or specific sub-unit.
    
    Args:
        failure: Failure instance to add
        sub_unit_idx: Optional sub-unit index (0-based). 
                     If None, adds to main unit.
    
    Raises:
        IndexError: If sub_unit_idx is out of range
        
    Examples:
        >>> # Add to main unit
        >>> uur.add_failure(failure)
        
        >>> # Add to sub-unit at index 2
        >>> uur.add_failure(failure, sub_unit_idx=2)
    """
    if sub_unit_idx is None:
        self.failures.append(failure)
    else:
        if sub_unit_idx < 0 or sub_unit_idx >= len(self.sub_units):
            raise IndexError(
                f"Sub-unit index {sub_unit_idx} out of range "
                f"(0-{len(self.sub_units)-1})"
            )
        self.sub_units[sub_unit_idx].failures.append(failure)
```

### Step 3.2: Implement add_failure_to_sub_unit() (2 hours)

**File:** `src/pywats/domains/report/report_models/uur/uur_report.py`

```python
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
        
    Examples:
        >>> # Add by index
        >>> uur.add_failure_to_sub_unit(failure, idx=2)
        
        >>> # Add by serial number
        >>> uur.add_failure_to_sub_unit(
        ...     failure, 
        ...     serial_number="SUB-12345"
        ... )
    """
    if idx is not None:
        if idx < 0 or idx >= len(self.sub_units):
            raise IndexError(
                f"Sub-unit index {idx} out of range "
                f"(0-{len(self.sub_units)-1})"
            )
        self.sub_units[idx].failures.append(failure)
    elif serial_number is not None:
        for sub in self.sub_units:
            if sub.serial_number == serial_number:
                sub.failures.append(failure)
                return
        raise ValueError(
            f"Sub-unit with serial number '{serial_number}' not found"
        )
    else:
        raise ValueError(
            "Must provide either 'serial_number' or 'idx' parameter"
        )
```

### Step 3.3: Implement UURSubUnit.add_failure() (1 hour)

**File:** `src/pywats/domains/report/report_models/uur/uur_sub_unit.py`

```python
def add_failure(self, failure: UURFailure) -> None:
    """Add failure directly to this sub-unit.
    
    Args:
        failure: Failure instance to add
        
    Example:
        >>> sub_unit = uur.sub_units[2]
        >>> sub_unit.add_failure(failure)
    """
    self.failures.append(failure)
```

### Step 3.4: Write Tests (1 hour)

**File:** `tests/domains/report/test_uur_failures.py`

```python
import pytest
from pywats.domains.report.report_models.uur import (
    UURReport, UURSubUnit, UURFailure
)

def test_add_failure_to_main_unit():
    """Test adding failure to main unit (default)."""
    uur = UURReport(...)
    failure = UURFailure(...)
    
    uur.add_failure(failure)
    
    assert len(uur.failures) == 1
    assert uur.failures[0] == failure

def test_add_failure_to_sub_unit_by_idx():
    """Test adding failure to sub-unit by index."""
    uur = UURReport(...)
    uur.sub_units = [UURSubUnit(...), UURSubUnit(...)]
    failure = UURFailure(...)
    
    uur.add_failure(failure, sub_unit_idx=1)
    
    assert len(uur.failures) == 0
    assert len(uur.sub_units[1].failures) == 1

def test_add_failure_to_sub_unit_out_of_range():
    """Test IndexError when sub_unit_idx out of range."""
    uur = UURReport(...)
    uur.sub_units = [UURSubUnit(...)]
    failure = UURFailure(...)
    
    with pytest.raises(IndexError):
        uur.add_failure(failure, sub_unit_idx=5)

def test_add_failure_to_sub_unit_by_serial():
    """Test adding failure by serial number."""
    uur = UURReport(...)
    uur.sub_units = [
        UURSubUnit(serial_number="SUB-001", ...),
        UURSubUnit(serial_number="SUB-002", ...)
    ]
    failure = UURFailure(...)
    
    uur.add_failure_to_sub_unit(failure, serial_number="SUB-002")
    
    assert len(uur.sub_units[1].failures) == 1

def test_add_failure_to_sub_unit_serial_not_found():
    """Test ValueError when serial number not found."""
    uur = UURReport(...)
    uur.sub_units = [UURSubUnit(serial_number="SUB-001", ...)]
    failure = UURFailure(...)
    
    with pytest.raises(ValueError, match="not found"):
        uur.add_failure_to_sub_unit(failure, serial_number="INVALID")

def test_add_failure_to_sub_unit_no_params():
    """Test ValueError when neither idx nor serial provided."""
    uur = UURReport(...)
    failure = UURFailure(...)
    
    with pytest.raises(ValueError, match="Must provide"):
        uur.add_failure_to_sub_unit(failure)

def test_uur_sub_unit_add_failure():
    """Test direct add_failure on UURSubUnit."""
    sub = UURSubUnit(...)
    failure = UURFailure(...)
    
    sub.add_failure(failure)
    
    assert len(sub.failures) == 1
```

---

## Phase 4: Process/Operation Type Standardization (8 hours)

**Goal:** Consistent process/operation_type naming across all models.

### Step 4.1: Audit Current Usage (2 hours)

```powershell
# Find all process/operation_type references
grep -r "operation_type" src/pywats/domains/report/
grep -r "process" src/pywats/domains/report/
grep -r "test_operation" src/pywats/domains/report/
grep -r "repair_operation" src/pywats/domains/report/

# Check examples
grep -r "operation" examples/
```

Create audit spreadsheet:
```markdown
| File | Current Field | Should Be | Notes |
|------|---------------|-----------|-------|
| uut_report.py | operation_type | test_operation | Primary field |
| uur_report.py | operation_type | repair_operation | Repair process |
| uur_report.py | test_operation | test_operation | ✓ Correct |
```

### Step 4.2: Update UUTReport Model (2 hours)

**File:** `src/pywats/domains/report/report_models/uut/uut_report.py`

```python
class UUTReport(PyWATSModel):
    """UUT (Unit Under Test) report model.
    
    Attributes:
        test_operation: The test process/operation type being performed.
                       This is the primary field name.
    """
    
    # Primary field
    test_operation: str = Field(
        ...,
        alias="operationType",  # API field name
        description="Test process/operation type"
    )
    
    # Convenience aliases
    @property
    def process(self) -> str:
        """Alias for test_operation (preferred in code)."""
        return self.test_operation
    
    @property
    def operation_type(self) -> str:
        """Alias for test_operation (API compatibility)."""
        return self.test_operation
```

### Step 4.3: Update UURReport Model (2 hours)

**File:** `src/pywats/domains/report/report_models/uur/uur_report.py`

```python
class UURReport(PyWATSModel):
    """UUR (Unit Under Repair) report model.
    
    Attributes:
        repair_operation: The repair process/operation type being performed.
        test_operation: The test that failed and triggered this repair.
    """
    
    # Primary fields
    repair_operation: str = Field(
        ...,
        alias="operationType",  # API field name for repair
        description="Repair process/operation type"
    )
    
    test_operation: str = Field(
        ...,
        alias="testOperation",  # API field name
        description="Test process that failed and triggered repair"
    )
    
    # Convenience aliases
    @property
    def process(self) -> str:
        """Alias for repair_operation (preferred in code)."""
        return self.repair_operation
    
    @property
    def operation_type(self) -> str:
        """Alias for repair_operation (API compatibility)."""
        return self.repair_operation
```

### Step 4.4: Remove Generic "Operations" (1 hour)

Search and replace:
- `operations` (plural, generic) → `operation_types` or `processes`
- Update all method parameters
- Update all variable names

### Step 4.5: Update Tests (1 hour)

- Update all UUT tests to use `test_operation`
- Update all UUR tests to use `repair_operation` and `test_operation`
- Verify aliases work correctly
- Test API serialization (check alias mapping)

---

## Phase 5: Documentation Data Validation (6 hours)

**Goal:** Fix all mock data to match actual Pydantic schemas.

### Step 5.1: Review User Guides (2 hours)

**Files to check:**
- `docs/guides/installation.md`
- `docs/guides/getting-started.md`
- `docs/guides/architecture.md`
- `docs/guides/report-submission.md`
- All other guides in `docs/guides/`

**Process:**
1. Extract each code example
2. Validate against actual Pydantic models
3. Fix any hallucinated fields
4. Verify dates are ISO 8601 format

### Step 5.2: Review Example Scripts (2 hours)

**Directories:**
- `examples/getting_started/*.py`
- `examples/report/*.py`
- `examples/product/*.py`
- `examples/production/*.py`
- All other example directories

**Common Fixes:**
```python
# BEFORE (hallucinated)
vendor = Vendor(
    name="ACME Corp",
    contact_name="John Doe",  # ✗ Field doesn't exist
    email="john@acme.com"     # ✗ Field doesn't exist
)

# AFTER (correct)
vendor_name = "ACME Corp"  # Vendor is just a string!
```

### Step 5.3: Review Sphinx Documentation (1 hour)

**Files:**
- `docs/api/product.rst`
- `docs/api/report.rst`
- All other `.rst` files

**Check:**
- Example code in docstrings
- Parameter examples
- Return value examples

### Step 5.4: Create Validation Script (Optional, 1 hour)

**File:** `scripts/validate_examples.py`

```python
"""Validate code examples in documentation."""
import ast
import re
from pathlib import Path

def extract_python_blocks(md_file: Path):
    """Extract Python code blocks from markdown."""
    content = md_file.read_text()
    pattern = r'```python\n(.*?)\n```'
    return re.findall(pattern, content, re.DOTALL)

def validate_code(code: str) -> bool:
    """Try to parse and validate code."""
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

# Run validation on all docs
for md_file in Path("docs").rglob("*.md"):
    for code in extract_python_blocks(md_file):
        if not validate_code(code):
            print(f"Invalid code in {md_file}")
```

---

## Phase 6: Testing & Validation (3 hours)

**Goal:** Ensure all changes work correctly and nothing is broken.

### Step 6.1: Run Full Test Suite (1 hour)

```powershell
# Run all tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src/pywats --cov-report=term-missing

# Expected: 416+ tests passing
```

### Step 6.2: Type Checking (30 min)

```powershell
# Run mypy
mypy src/pywats --strict

# Expected: 16 errors or fewer (no new errors)
```

### Step 6.3: Integration Testing (1 hour)

```python
# Test UUR submission with new API
from pywats import pyWATS
from pywats.domains.report import UURReport, UURFailure

api = pyWATS(base_url="...", token="...")

# Create report with new field names
uur = UURReport(
    repair_operation="Repair-001",  # New field
    test_operation="Test-FCT",      # Correct field
    ...
)

# Add failure to sub-unit (new API)
failure = UURFailure(...)
uur.add_failure(failure, sub_unit_idx=0)

# Submit
result = api.report.submit_uur_report(uur)
assert result.success
```

### Step 6.4: Manual Testing Checklist (30 min)

- [ ] UUR add_failure() to main unit works
- [ ] UUR add_failure() to sub-unit by idx works
- [ ] UUR add_failure_to_sub_unit() by serial works
- [ ] UURSubUnit.add_failure() works
- [ ] test_operation field in UUT works
- [ ] repair_operation field in UUR works
- [ ] No backward compatibility properties exist
- [ ] report_builder import fails with ImportError
- [ ] All examples execute without errors

---

## Phase 7: Documentation & Finalization (2 hours)

### Step 7.1: Update CHANGELOG.md (30 min)

```markdown
## [0.3.0b1] - 2026-02-XX

### Changed
- **UURReport**: Enhanced `add_failure()` with optional `sub_unit_idx` parameter
- **UURReport**: Added `add_failure_to_sub_unit()` method (by serial or idx)
- **UURSubUnit**: Added `add_failure()` method for direct access
- **UUTReport**: Renamed `operation_type` → `test_operation` (aliases provided)
- **UURReport**: Renamed `operation_type` → `repair_operation` (aliases provided)

### Removed
- **Backward Compatibility**: Removed deprecated properties (uur_info → info)
- **Tools**: Removed experimental `report_builder` module

### Fixed
- **Documentation**: Fixed mock data to match actual Pydantic schemas
- **Examples**: Corrected hallucinated fields in example code
```

### Step 7.2: Create Migration Guide (1 hour)

**File:** `docs/MIGRATION_0.3.0b1.md`

```markdown
# Migration Guide: v0.3.0b1

## Breaking Changes

### 1. Removed Backward Compatibility Properties

#### UURReport
- `uur.uur_info` → Use `uur.info`

**Migration:**
```python
# Before
uur.uur_info = UURInfo(...)

# After
uur.info = UURInfo(...)
```

### 2. Removed report_builder Module

The experimental `report_builder` has been removed and will be redesigned.

**Migration:**
```python
# Before
from pywats.tools import UUTReportBuilder

# After
# Use direct model construction:
from pywats.domains.report import UUTReport
report = UUTReport(...)
```

## New Features

### Enhanced UUR Failure API

**Add failure to sub-unit:**
```python
# By index
uur.add_failure(failure, sub_unit_idx=2)

# By serial number
uur.add_failure_to_sub_unit(failure, serial_number="SUB-001")

# Direct access
uur.sub_units[2].add_failure(failure)
```

### Clearer Process/Operation Naming

**UUT Reports:**
```python
uut = UUTReport(
    test_operation="FCT-Test",  # New field name
    ...
)
# Aliases still work: .process, .operation_type
```

**UUR Reports:**
```python
uur = UURReport(
    repair_operation="Rework-001",  # The repair process
    test_operation="FCT-Test",       # The failed test
    ...
)
```
```

### Step 7.3: Update README.md Examples (30 min)

- Update quick start to use new API
- Update UUR example to show new failure methods
- Fix any mock data hallucinations

---

## Verification Checklist

Before marking project complete:

- [ ] All files in Phase 1 removed
- [ ] All backward compatibility properties removed
- [ ] UUR failure API implemented and tested
- [ ] Process/operation_type standardized
- [ ] Documentation mock data validated
- [ ] 416+ tests passing
- [ ] Mypy errors ≤ 16
- [ ] CHANGELOG.md updated
- [ ] Migration guide created
- [ ] Examples updated
- [ ] No import errors for removed modules

---

**Implementation Plan Complete:** Ready to execute phase by phase.
