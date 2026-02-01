# Status Enums Comprehensive Analysis - pyWATS Codebase

**Date**: February 1, 2026  
**Purpose**: Complete documentation of all status-related enums, conversion patterns, and WATS API format requirements

---

## Executive Summary

The pyWATS codebase uses **TWO different status enum formats**:

1. **WSJF/API Format**: Single-letter codes (`"P"`, `"F"`, `"S"`, `"D"`, `"E"`, `"T"`) 
   - Used by: `StepStatus`, `ReportStatus` in report models
   - Required for WATS API serialization (WSJF format)

2. **Query Filter Format**: Full word values (`"Passed"`, `"Failed"`, `"Error"`, etc.)
   - Used by: `StatusFilter` for querying/filtering reports
   - Required by WATS query endpoints

**Critical Finding**: Currently NO flexible conversion logic exists. Status values must match the exact enum value strings.

---

## 1. All Status Enums - Complete Definitions

### 1.1 StepStatus (WSJF Format - Single Letter Codes)

**File**: [src/pywats/domains/report/report_models/common_types.py](src/pywats/domains/report/report_models/common_types.py#L63-L71)

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

**Inheritance**: `str, Enum`
- Inherits from `str` so it serializes directly to string value
- Pydantic handles it automatically

**Used In**:
- All step classes (NumericStep, PassFailStep, StringValueStep, etc.)
- Measurements (NumericMeasurement, BooleanMeasurement, StringMeasurement)
- WSJF JSON serialization
- Test report submissions to WATS API

**Default Value**: `StepStatus.Passed` (serializes to `"P"`)

---

### 1.2 ReportStatus (WSJF Format - Single Letter Codes)

**File**: [src/pywats/domains/report/report_models/common_types.py](src/pywats/domains/report/report_models/common_types.py#L73-L80)

```python
class ReportStatus(str, Enum):
    """Overall report status."""
    Passed = "P"
    Failed = "F"
    Done = "D"
    Error = "E"
    Terminated = "T"
```

**Inheritance**: `str, Enum`

**Alias**: `ReportResult = ReportStatus` (line 83)

**Used In**:
- UUTReport (overall test result)
- UURReport (overall repair result)
- WSJF JSON serialization

**Note**: Missing `Skipped = "S"` (unlike StepStatus)

---

### 1.3 StatusFilter (Query Format - Full Words)

**File**: [src/pywats/shared/enums.py](src/pywats/shared/enums.py#L14-L48)

```python
class StatusFilter(str, Enum):
    """
    Status filter values for querying reports.
    
    Used for filtering reports by test outcome in WATSFilter and analytics queries.
    Inherits from str so it serializes correctly to the API.
    
    Note: This is different from ReportStatus which uses single-letter codes
    for WSJF format. StatusFilter uses the full string values expected by 
    query endpoints.
    
    Example:
        >>> filter = WATSFilter(status=StatusFilter.PASSED)
        >>> # Or with string
        >>> filter = WATSFilter(status="Passed")
    """
    PASSED = "Passed"
    """Test passed successfully."""
    
    FAILED = "Failed"
    """Test failed with a failure condition."""
    
    ERROR = "Error"
    """Test encountered an error (not pass/fail)."""
    
    TERMINATED = "Terminated"
    """Test was terminated before completion."""
    
    DONE = "Done"
    """Test completed (neutral status, no pass/fail)."""
    
    SKIPPED = "Skipped"
    """Test was skipped."""
```

**Inheritance**: `str, Enum`

**Used In**:
- WATSFilter model for querying reports
- Analytics queries
- Query API endpoints

**Documentation Notes**:
- Explicitly states it's DIFFERENT from ReportStatus
- Uses full word values expected by query endpoints
- Has detailed docstrings for each value

---

### 1.4 Old Model Enums (Legacy - report_models_old)

#### StepStatus (Old Version)

**File**: [src/pywats/domains/report/report_models_old/uut/step.py](src/pywats/domains/report/report_models_old/uut/step.py#L24-L29)

```python
class StepStatus(Enum):
    Passed = 'P'
    Failed = 'F'
    Skipped = 'S'
    Terminated = 'T'
    Done = 'D'
```

**Difference**: Does NOT inherit from `str` (just `Enum`)

#### ReportStatus (Old Version)

**File**: [src/pywats/domains/report/report_models_old/report.py](src/pywats/domains/report/report_models_old/report.py#L26-L40)

```python
class ReportStatus(Enum):
    """
    UUT/UUR Report Status - matches C# UUTStatusType enum.
    
    P = Passed (0)
    F = Failed (1)
    E = Error (2)
    T = Terminated (3)
    S = Skipped (maps to Terminated on server)
    """
    Passed = 'P'
    Failed = 'F'
    Error = 'E'
    Terminated = 'T'
    Skipped = 'S'  # Maps to Terminated on server
```

**Important Notes**:
- Has C# enum value mappings documented
- States that Skipped maps to Terminated on server
- Does NOT inherit from `str`

---

### 1.5 Other Status Enums (Not Test/Report Status)

#### QueueItemStatus
**File**: [src/pywats/shared/enums.py](src/pywats/shared/enums.py#L340)
```python
class QueueItemStatus(str, Enum):
    # Queue processing status - not test results
```

#### PackageStatus  
**File**: [src/pywats/domains/software/enums.py](src/pywats/domains/software/enums.py#L8)
```python
class PackageStatus(str, Enum):
    # Software package lifecycle status
```

#### ConversionStatus
**File**: [src/pywats_client/converters/models.py](src/pywats_client/converters/models.py#L50)
```python
class ConversionStatus(Enum):
    # File conversion status
```

#### AsyncServiceStatus, ServiceStatus, CheckStatus
- Various service/client status enums
- Not related to test results

---

## 2. Enum Conversion Patterns

### 2.1 Field Validators

#### Status Filter Normalization

**File**: [src/pywats/domains/report/models.py](src/pywats/domains/report/models.py#L304-L322)

```python
@field_validator("status", mode="before")
@classmethod
def normalize_status(cls, v: object) -> object:
    """Normalize status to string value.

    Accepts:
    - StatusFilter enum values
    - String values: 'Passed', 'Failed', 'Error', etc.
    - 'all' is treated as None (unset)
    """
    if v is None:
        return None
    # Handle enum
    if isinstance(v, StatusFilter):
        return v.value
    # Handle 'all' as unset
    if isinstance(v, str) and v.strip().lower() == "all":
        return None
    return v
```

**Purpose**: Converts StatusFilter enum to string for WATSFilter queries  
**Special Case**: `"all"` → `None` (unset filter)  
**Location**: WATSFilter model only  
**Mode**: `mode="before"` (runs before Pydantic validation)

---

### 2.2 String to Enum Conversion in Factory Methods

#### NumericStep.create()

**File**: [src/pywats/domains/report/report_models/uut/steps/numeric_step.py](src/pywats/domains/report/report_models/uut/steps/numeric_step.py#L185-L187)

```python
# Convert string status to enum if needed
if isinstance(status, str):
    status = StepStatus(status)
```

**Pattern**: Direct enum constructor call  
**Requires**: Exact string match to enum value  
**Example**: `StepStatus("P")` ✓ but `StepStatus("Passed")` ✗

#### PassFailStep.create()

**File**: [src/pywats/domains/report/report_models/uut/steps/boolean_step.py](src/pywats/domains/report/report_models/uut/steps/boolean_step.py#L115-L117)

```python
# Convert string status to enum if needed
if isinstance(status, str):
    status = StepStatus(status)
```

**Same Pattern**: Used consistently across all step factory methods

---

### 2.3 Method Signatures Accepting Both Enum and String

**Pattern**: `status: StepStatus | str = StepStatus.Passed`

**Found In**:
- [NumericStep.create()](src/pywats/domains/report/report_models/uut/steps/numeric_step.py#L168)
- [PassFailStep.create()](src/pywats/domains/report/report_models/uut/steps/boolean_step.py#L102)
- [StringValueStep.create()](src/pywats/domains/report/report_models/uut/steps/string_step.py#L135)
- All add_*_step() methods in SequenceCall

**Example**:
```python
def create(
    cls,
    name: str,
    value: float | str,
    *,
    unit: str = "NA",
    comp_op: CompOp = CompOp.LOG,
    low_limit: float | str | None = None,
    high_limit: float | str | None = None,
    status: StepStatus | str = StepStatus.Passed,  # <-- Accepts both
) -> "NumericStep":
```

---

### 2.4 NO Flexible Conversion Logic Found

**Critical Finding**: There is NO:
- Case-insensitive matching
- Alias support (e.g., "Pass", "PASS", "Passed" all meaning Passed)
- Custom `__new__` methods
- `from_string()` classmethod (except in EventType, not status-related)
- Fuzzy matching or normalization

**Current Behavior**:
```python
# ✓ Works - exact match
status = StepStatus("P")

# ✗ Fails - ValueError
status = StepStatus("Passed")  
status = StepStatus("Pass")
status = StepStatus("PASSED")
status = StepStatus("pass")
```

---

## 3. Usage Patterns in Examples and Tests

### 3.1 Examples Use String Values (Not Enum Constants)

**File**: [examples/report/step_types.py](examples/report/step_types.py#L33)

```python
report.add_numeric_limit_step(
    name="Voltage Test",
    status="Passed",  # <-- String, not StepStatus.Passed
    value=5.02,
    units="V",
    low_limit=4.8,
    high_limit=5.2,
    comp_operator="GELE"
)
```

**File**: [examples/report/create_uut_report.py](examples/report/create_uut_report.py#L32-L36)

```python
report = UUTReport(
    pn="WIDGET-001",
    sn="SN-2024-001234",
    rev="A",
    result="Passed",  # <-- String
    start=datetime.now(),
)
```

**Pattern**: All examples use string literals like `"Passed"`, `"Failed"`

**Problem**: These strings don't match the actual enum values!
- Examples use: `"Passed"` 
- Enum value is: `"P"`

---

### 3.2 Test Files Use Enum Constants

**File**: [tests/domains/report/test_import_mode.py](tests/domains/report/test_import_mode.py#L208-L209)

```python
assert child.status == StepStatus.Failed
assert parent.status == StepStatus.Failed
```

**Pattern**: Tests use `StepStatus.Passed`, `StepStatus.Failed` constants

---

### 3.3 JSON Serialization Uses Single-Letter Codes

**File**: [tests/report_model_testing/files_after_conversion_and_reload/v3_submitted.json](tests/report_model_testing/files_after_conversion_and_reload/v3_submitted.json#L48)

```json
{
  "status": "P",
  "stepType": "NumericLimitTest",
  "name": "Test Step 1",
  "numericMeas": {
    "status": "P",
    "value": 10.0
  }
}
```

**Pattern**: Submitted JSON uses `"P"`, `"F"` etc. (single-letter codes)

---

### 3.4 XML Conversion Uses Full Word Values

**File**: [tests/report_model_testing/files_after_conversion_and_reload/converted_from_xml.json](tests/report_model_testing/files_after_conversion_and_reload/converted_from_xml.json#L67)

```json
{
  "status": "Passed",  // <-- Full word from XML conversion
  "stepType": "NumericLimitTest"
}
```

**Pattern**: XML imports may produce full words like `"Passed"`

---

## 4. WATS API Format Requirements

### 4.1 WSJF Format (JSON Submission)

**Evidence**: Test JSON files show WATS expects single-letter codes

**Report Level**:
```json
{
  "result": "P",  // P=Passed, F=Failed, D=Done, E=Error, T=Terminated
  "reportType": "T"
}
```

**Step Level**:
```json
{
  "status": "P",  // P=Passed, F=Failed, S=Skipped, D=Done, E=Error, T=Terminated
  "stepType": "NumericLimitTest"
}
```

**Source**: [v3_submitted.json](tests/report_model_testing/files_after_conversion_and_reload/v3_submitted.json)

---

### 4.2 Query API Format

**Evidence**: StatusFilter documentation states query endpoints expect full words

**From StatusFilter Docstring**:
```
StatusFilter uses the full string values expected by query endpoints.
```

**Filter Values**:
- `"Passed"` (not `"P"`)
- `"Failed"` (not `"F"`)
- `"Error"` (not `"E"`)
- etc.

---

### 4.3 Text File Converter Format

**File**: [src/pywats_client/converters/standard/wats_standard_text_converter.py](src/pywats_client/converters/standard/wats_standard_text_converter.py#L289)

```python
elif key == 'UUTStatus':
    report['result'] = self._map_uut_status(value)
```

**Example Text Format** (line 651):
```
UUTStatus	Passed
```

**Example Step Line** (line 658):
```
StepType	StepName	MeasureName	Value	LowLimit	HighLimit	CompOperator	Unit	StepStatus	StepExecutionTime
```

**Pattern**: Text converters accept full words and map them to single-letter codes

---

### 4.4 ATML Converter Mappings

**File**: [src/pywats_client/converters/standard/atml_converter.py](src/pywats_client/converters/standard/atml_converter.py#L189-L206)

```python
def _get_step_status(outcome_value: str, qualifier: Optional[str] = None) -> StepStatus:
    """Convert ATML outcome to WATS StepStatus."""
    value = outcome_value
    
    # Handle qualifier if present (e.g., "Passed" with qualifier "Conditional")
    # For now, we just use the outcome value
    
    status_map = {
        "Passed": StepStatus.PASSED,    # Maps to StepStatus.Passed = "P"
        "Failed": StepStatus.FAILED,    # Maps to StepStatus.Failed = "F"
        "Done": StepStatus.DONE,        # Maps to StepStatus.Done = "D"
        "Skipped": StepStatus.SKIPPED,  # Maps to StepStatus.Skipped = "S"
        "Error": StepStatus.ERROR,      # Maps to StepStatus.Error = "E"
        "Terminated": StepStatus.TERMINATED,  # Maps to StepStatus.Terminated = "T"
        "Running": StepStatus.RUNNING,  # No equivalent? Bug?
    }
    
    return status_map.get(value, StepStatus.DONE)
```

**ERROR FOUND**: Uses `StepStatus.PASSED` but enum values are `StepStatus.Passed`!
- Enum uses PascalCase: `Passed`, `Failed`
- Code uses UPPERCASE: `PASSED`, `FAILED`

---

### 4.5 C# Reference (If Available)

**Old Model Documentation** states:
```
UUT/UUR Report Status - matches C# UUTStatusType enum.

P = Passed (0)
F = Failed (1)
E = Error (2)
T = Terminated (3)
S = Skipped (maps to Terminated on server)
```

**Implication**: 
- C# backend uses integer enum (0-3)
- String values `"P"`, `"F"`, `"E"`, `"T"` map to these
- Skipped is special case that maps to Terminated server-side

---

## 5. Problems and Inconsistencies

### 5.1 CRITICAL: Examples Don't Work

**Problem**: All examples use `status="Passed"` but enum value is `"P"`

**Example Code**:
```python
report.add_numeric_limit_step(
    name="Voltage Test",
    status="Passed",  # <-- This will FAIL
    value=5.02,
)
```

**What Happens**:
1. `status="Passed"` passed to factory method
2. Factory calls `StepStatus("Passed")` 
3. **ValueError: 'Passed' is not a valid StepStatus**

**Impact**: 
- All documentation examples are broken
- New users copying examples get errors
- Confusing user experience

---

### 5.2 Inconsistent Naming Convention

**Issue**: ATML converter uses UPPERCASE enum names that don't exist

**Code**:
```python
"Passed": StepStatus.PASSED,  # Should be StepStatus.Passed
"Failed": StepStatus.FAILED,  # Should be StepStatus.Failed
```

**Actual Enum**:
```python
class StepStatus(str, Enum):
    Passed = "P"  # PascalCase, not UPPERCASE
    Failed = "F"
```

**Impact**: This code will fail with AttributeError

---

### 5.3 XML Conversion Produces Wrong Format

**Problem**: XML converters produce `"Passed"` but WATS expects `"P"`

**Evidence**: [converted_from_xml.json](tests/report_model_testing/files_after_conversion_and_reload/converted_from_xml.json#L67)
```json
{
  "status": "Passed",  // Wrong format for WSJF
}
```

**Should Be**:
```json
{
  "status": "P",  // Correct WSJF format
}
```

---

### 5.4 No Flexible String Conversion

**Problem**: Users must know exact enum value string

**What Works**:
```python
status = StepStatus("P")  # ✓
```

**What Fails**:
```python
status = StepStatus("Passed")  # ✗
status = StepStatus("Pass")    # ✗
status = StepStatus("PASSED")  # ✗
status = StepStatus("p")       # ✗
```

**User Expectation**: Natural language should work
- Reading code: `status="Passed"` is clear
- Using API: `"P"` is cryptic without documentation

---

### 5.5 Two Different Status Formats

**Problem**: API has two incompatible status formats

**WSJF Format** (Report submission):
- `"P"`, `"F"`, `"S"`, `"D"`, `"E"`, `"T"`

**Query Format** (Report filtering):
- `"Passed"`, `"Failed"`, `"Skipped"`, `"Done"`, `"Error"`, `"Terminated"`

**Impact**:
- Confusion: Which format to use when?
- Can't reuse values between submission and querying
- Need separate enums (StepStatus vs StatusFilter)

---

### 5.6 Missing Skipped in ReportStatus

**Issue**: StepStatus has Skipped but ReportStatus doesn't

**StepStatus**:
```python
Skipped = "S"  # ✓ Present
```

**ReportStatus**:
```python
# Skipped = "S"  # ✗ Missing
```

**Old Comment**: "Skipped maps to Terminated on server"

**Question**: Should reports support Skipped status?

---

## 6. Recommended Solutions

### 6.1 Add Flexible String Conversion

**Option A: Custom Enum Class with Aliases**

```python
class FlexibleStatusEnum(str, Enum):
    """Status enum with flexible string conversion."""
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive and alias lookups."""
        if isinstance(value, str):
            # Try case-insensitive match
            value_upper = value.upper()
            for member in cls:
                if member.name.upper() == value_upper:
                    return member
                if member.value.upper() == value_upper:
                    return member
            
            # Try common aliases
            aliases = {
                'PASS': cls.Passed,
                'P': cls.Passed,
                'FAIL': cls.Failed,
                'F': cls.Failed,
                'SKIP': cls.Skipped,
                'S': cls.Skipped,
            }
            return aliases.get(value_upper)
        return None

class StepStatus(FlexibleStatusEnum):
    Passed = "P"
    Failed = "F"
    Skipped = "S"
    Done = "D"
    Error = "E"
    Terminated = "T"
```

**Option B: Field Validator**

```python
@field_validator("status", mode="before")
@classmethod
def normalize_status(cls, v: object) -> StepStatus:
    """Normalize status from various formats."""
    if isinstance(v, StepStatus):
        return v
    
    if isinstance(v, str):
        # Normalize common variations
        mapping = {
            'P': StepStatus.Passed,
            'PASS': StepStatus.Passed,
            'PASSED': StepStatus.Passed,
            'F': StepStatus.Failed,
            'FAIL': StepStatus.Failed,
            'FAILED': StepStatus.Failed,
            # etc...
        }
        normalized = mapping.get(v.upper())
        if normalized:
            return normalized
        
        # Try direct enum lookup
        try:
            return StepStatus(v)
        except ValueError:
            pass
    
    raise ValueError(f"Invalid status: {v}")
```

---

### 6.2 Fix Documentation Examples

**Current**:
```python
status="Passed",  # ✗ Doesn't work
```

**Option 1: Use Enum Constants**
```python
status=StepStatus.Passed,  # ✓ Works
```

**Option 2: Use Correct String Values**
```python
status="P",  # ✓ Works but cryptic
```

**Option 3: Add Flexible Conversion + Keep Examples**
```python
status="Passed",  # ✓ Works after implementing flexible conversion
```

**Recommendation**: Option 3 (best user experience)

---

### 6.3 Fix ATML Converter

**Current (BROKEN)**:
```python
"Passed": StepStatus.PASSED,  # AttributeError
```

**Fixed**:
```python
"Passed": StepStatus.Passed,  # ✓
```

---

### 6.4 Standardize Conversion Strategy

**Recommendation**: 

1. **Internal Format**: Always use single-letter codes (`"P"`, `"F"`)
2. **User-Facing API**: Accept flexible strings (`"Passed"`, `"Pass"`, `"P"`)
3. **Serialization**: Always output single-letter codes for WATS API
4. **Query API**: Continue using full words for StatusFilter

**Implementation**:
```python
# Add to StepStatus and ReportStatus
@classmethod
def from_string(cls, value: str) -> "StepStatus":
    """Create from flexible string input."""
    if isinstance(value, cls):
        return value
    
    # Map full words to single letters
    mapping = {
        'PASSED': cls.Passed,
        'PASS': cls.Passed,
        'P': cls.Passed,
        'FAILED': cls.Failed,
        'FAIL': cls.Failed,
        'F': cls.Failed,
        # etc...
    }
    
    result = mapping.get(value.upper().strip())
    if result:
        return result
    
    raise ValueError(f"Invalid status: {value}")
```

---

## 7. Summary Table

| Enum | File | Inheritance | Values | Format | Purpose |
|------|------|-------------|--------|--------|---------|
| **StepStatus** | common_types.py | `str, Enum` | P, F, S, D, E, T | Single-letter | Step execution status (WSJF) |
| **ReportStatus** | common_types.py | `str, Enum` | P, F, D, E, T | Single-letter | Report result (WSJF) |
| **StatusFilter** | shared/enums.py | `str, Enum` | Passed, Failed, Error, Terminated, Done, Skipped | Full word | Query filtering |
| StepStatus (old) | report_models_old/ | `Enum` | P, F, S, T, D | Single-letter | Legacy |
| ReportStatus (old) | report_models_old/ | `Enum` | P, F, E, T, S | Single-letter | Legacy |

---

## 8. Action Items

### High Priority

1. **Fix Examples** - Update all examples to use correct enum values or implement flexible conversion
2. **Fix ATML Converter** - Change `StepStatus.PASSED` to `StepStatus.Passed`
3. **Add Flexible Conversion** - Implement `_missing_()` or validators to accept common string variations

### Medium Priority

4. **Standardize XML Conversion** - Ensure XML converters output `"P"` not `"Passed"`
5. **Add from_string() Methods** - Provide explicit conversion utility
6. **Document Dual Format System** - Clear docs explaining WSJF vs Query formats

### Low Priority

7. **Consider Adding Skipped to ReportStatus** - Match StepStatus capabilities
8. **Add Type Hints** - More explicit type annotations for status parameters
9. **Write Tests** - Comprehensive tests for flexible string conversion

---

## 9. References

### Key Files

- Status Definitions:
  - [src/pywats/domains/report/report_models/common_types.py](src/pywats/domains/report/report_models/common_types.py#L63-L80)
  - [src/pywats/shared/enums.py](src/pywats/shared/enums.py#L14-L48)

- Usage Examples:
  - [examples/report/step_types.py](examples/report/step_types.py)
  - [examples/report/create_uut_report.py](examples/report/create_uut_report.py)

- Converters:
  - [src/pywats_client/converters/standard/atml_converter.py](src/pywats_client/converters/standard/atml_converter.py#L189-L222)
  - [src/pywats_client/converters/standard/wats_standard_text_converter.py](src/pywats_client/converters/standard/wats_standard_text_converter.py)

- Test Data:
  - [tests/report_model_testing/files_after_conversion_and_reload/v3_submitted.json](tests/report_model_testing/files_after_conversion_and_reload/v3_submitted.json)
  - [tests/report_model_testing/files_after_conversion_and_reload/converted_from_xml.json](tests/report_model_testing/files_after_conversion_and_reload/converted_from_xml.json)

---

**End of Analysis**
