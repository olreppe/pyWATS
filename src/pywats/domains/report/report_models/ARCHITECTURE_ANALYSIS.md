# Report Models v3 - Architecture Analysis & Implementation Plan

**Created:** January 30, 2026  
**Purpose:** Comprehensive analysis of v1, v2, C# implementations and v3 design plan

---

## 1. Executive Summary

### Key Insight
The current `report_models/` folder IS v1 (just not labeled as such). The `report_models_v2/` was an attempt using mixins that wasn't satisfactory. **v3 should be the "correct" implementation of v1** - fixing architectural issues while:

1. Preserving the C# factory method pattern (`add_numeric_step()`, etc.)
2. Also allowing direct constructors
3. Maintaining hierarchical SequenceCall structure  
4. Keeping same JSON output format for API compatibility
5. Fixing C# design flaws that were carried over to Python v1

---

## 2. Analysis of Existing Implementations

### 2.1 C# Implementation Analysis

**Strengths:**
- Clean inheritance: `Report` ← `UUTReport`, `Report` ← `UURReport`
- Step inheritance: `Step` ← `NumericLimitStep`, `Step` ← `SequenceCall`, etc.
- Factory methods on `SequenceCall`: `AddNumericLimitStep()`, `AddSequenceCall()`, etc.
- Separate `*Test` classes from `*Step` classes (e.g., `NumericLimitStep` contains `NumericLimitTest[]`)
- `TDM` as external API/factory (creates reports)

**Weaknesses:**
- Internal WRML schema coupling (C# uses `reportRow`, `stepRow` internal XML types)
- `IsSingle` / `IsMultiple` boolean flags to track step mode (should be type-based)
- Mixing single/multiple logic within same class (violates Single Responsibility)
- Factory-only creation (no direct constructors exposed)

**C# Class Hierarchy:**
```
Report
├── UUTReport (has rootSequenceCall: SequenceCall)
└── UURReport

Step
├── SequenceCall (has child steps, factory methods)
├── NumericLimitStep (has tests: NumericLimitTest[])
├── PassFailStep (has tests: PassFailTest[])
├── StringValueStep (has tests: StringValueTest[])
├── CallExeStep
├── MessagePopupStep
├── GenericStep
└── PropertyLoaderStep
```

### 2.2 Python v1 Analysis (`report_models/`)

**Strengths:**
- Pydantic-based (good validation, serialization)
- Factory methods preserved: `add_numeric_step()`, `add_sequence_call()`, etc.
- `StepList` with parent injection (handles hierarchy)
- Discriminated union for polymorphic step deserialization
- `ImportMode` concept (Active vs Import) for auto-status calculation

**Weaknesses:**
- `Report` base class contains ALL fields (UUT/UUR specific mixed in)
- `Step` is abstract but uses complex discriminator function
- Single vs Multi step types are SEPARATE classes (`NumericStep` vs `MultiNumericStep`)
- Measurement wrapping/unwrapping logic duplicated (list ↔ single conversion)
- `StepList` is a custom list subclass (complex, fragile)
- No explicit `type` field in base `Report` (uses v1's pattern `"T"` or `"R"`)
- Deep coupling between step type and serialization format

**v1 Class Hierarchy:**
```
WATSBase
└── Report
    ├── UUTReport (root: SequenceCall)
    └── UURReport

WATSBase + ABC
└── Step (abstract)
    ├── SequenceCall (steps: StepList[StepType], factory methods)
    ├── NumericStep (measurement: NumericMeasurement)
    ├── MultiNumericStep (measurements: list[MultiNumericMeasurement])
    ├── BooleanStep (measurement: BooleanMeasurement)
    ├── MultiBooleanStep (measurements: list[MultiBooleanMeasurement])
    ├── StringStep (measurement: StringMeasurement)
    ├── MultiStringStep (measurements: list[MultiStringMeasurement])
    ├── ChartStep
    ├── ActionStep
    ├── GenericStep
    └── UnknownStep (fallback)
```

### 2.3 Python v2 Analysis (`report_models_v2/`)

**Approach:** Composition with proxy mixin

**Attempt:**
- `ReportCommon` class holds shared fields
- `UUTReport` uses `common: ReportCommon` composition
- `ReportProxyMixin` provides flat property access (`report.pn` → `report.common.pn`)

**Why It Failed:**
- Mixin pattern creates complexity without solving core issues
- 70+ property proxies needed just to maintain flat API
- Still imports v1 steps (doesn't fix step architecture)
- Type checker confusion with mixin + Pydantic
- Extra indirection without architectural benefit

---

## 3. JSON API Contract Analysis

The JSON format sent to WATS server is **fixed** and must be preserved. Key observations:

### Report Level
```json
{
  "id": "guid",
  "type": "T",           // "T" for UUT, "R" for UUR
  "pn": "PART-001",
  "sn": "SN-001",
  "rev": "A",
  "processCode": 100,
  "machineName": "Station1",
  "location": "Lab",
  "purpose": "Test",
  "result": "P",
  "start": "2024-01-01T12:00:00+00:00",
  "uut": { ... },        // UUT-specific info (only for type="T")
  "root": { ... }        // Root SequenceCall (only for type="T")
}
```

### Step Level (critical observation)
```json
// Single NumericStep serializes measurement as ARRAY with ONE element:
{
  "stepType": "ET_NLT",
  "name": "VoltageTest",
  "numericMeas": [{ "value": 5.0, "unit": "V", ... }]
}

// Multi NumericStep serializes measurements as ARRAY with MANY elements:
{
  "stepType": "ET_MNLT", 
  "name": "MultiTest",
  "numericMeas": [
    { "name": "Meas1", "value": 1.0, ... },
    { "name": "Meas2", "value": 2.0, ... }
  ]
}
```

**Key insight:** Both single and multi steps serialize to arrays, but:
- Single: stepType=`ET_NLT`, array length=1, measurement has NO `name`
- Multi: stepType=`ET_MNLT`, array length>=1, each measurement HAS `name`

---

## 4. v3 Design Goals

### 4.1 Primary Goals
1. **Fix v1's type confusion** - Clear distinction between single/multi step patterns
2. **Preserve factory methods** - `add_numeric_step()`, `add_sequence_call()` stay on SequenceCall
3. **Allow constructors** - Steps can be created directly, then added
4. **Clean inheritance** - Proper OOP without v2's mixin complexity
5. **Same JSON output** - API compatibility is non-negotiable
6. **Same user interface** - Minimize breaking changes from v1

### 4.2 Design Principles
- **Prefer inheritance over composition** for Step hierarchy (matches C# mental model)
- **Use composition for Report** (UUT/UUR have different payloads, not inherited)
- **Type discrimination via Literal types** (not runtime flags)
- **Custom serializers only where needed** (measurement list wrapping)
- **Parent injection stays** (hierarchy tracking is useful)

---

## 5. Proposed v3 Architecture

### 5.1 Report Hierarchy

```python
# Base shared fields (NOT a base class - just data)
@dataclass
class ReportHeader:
    """Common fields shared by all report types - not a base class."""
    id: UUID
    pn: str
    sn: str
    rev: str
    process_code: int
    station_name: str
    location: str
    purpose: str
    result: str
    start: datetime
    # ... misc_infos, assets, etc.

# UUTReport - standalone class, not inheriting Report
class UUTReport(WATSBase):
    """Unit Under Test Report"""
    # Direct fields (no composition layer)
    id: UUID = Field(default_factory=uuid4)
    type: Literal["T"] = "T"
    pn: str
    sn: str
    rev: str
    process_code: int = Field(serialization_alias="processCode")
    station_name: str = Field(serialization_alias="machineName")
    location: str
    purpose: str
    result: str = "P"
    start: datetime
    
    # UUT-specific
    info: UUTInfo | None = Field(default=None, serialization_alias="uut")
    root: SequenceCall = Field(default_factory=SequenceCall)
    
    def get_root_sequence_call(self) -> SequenceCall:
        self.root.name = "MainSequence Callback"
        return self.root

# UURReport - similar pattern
class UURReport(WATSBase):
    """Unit Under Repair Report"""
    id: UUID = Field(default_factory=uuid4)
    type: Literal["R"] = "R"
    # ... shared fields ...
    # UUR-specific
    info: UURInfo | None = Field(default=None, serialization_alias="uur")
```

**Rationale:** Flat fields on report class (no `common` wrapper), same as v1. The "type" discriminator allows union parsing.

### 5.2 Step Hierarchy - The Core Innovation

**Key insight:** Instead of separate `NumericStep` and `MultiNumericStep` classes, use a **single class with a smarter measurement container**.

```python
class Step(WATSBase, ABC):
    """Base class for all test steps."""
    step_type: str
    name: str
    status: StepStatus = StepStatus.Passed
    group: str = "M"
    # ... common step fields ...
    parent: Optional['Step'] = Field(default=None, exclude=True)

class SequenceCall(Step):
    """Container step that holds child steps."""
    step_type: Literal["SequenceCall", "WATS_SeqCall"] = "SequenceCall"
    sequence: SequenceCallInfo = Field(default_factory=SequenceCallInfo)
    steps: list[StepType] = Field(default_factory=list)
    
    # Factory methods (preserved from v1/C#)
    def add_sequence_call(self, name: str, ...) -> 'SequenceCall': ...
    def add_numeric_step(self, *, name: str, value: float, ...) -> 'NumericLimitStep': ...
    def add_pass_fail_step(self, *, name: str, passed: bool, ...) -> 'PassFailStep': ...
    def add_string_step(self, *, name: str, value: str, ...) -> 'StringValueStep': ...
    # etc.

class NumericLimitStep(Step):
    """Numeric limit test step - supports single OR multiple measurements."""
    step_type: str = Field(default="ET_NLT")  # Changes to "ET_MNLT" when multiple
    _tests: list[NumericLimitTest] = PrivateAttr(default_factory=list)
    
    @property
    def is_multiple(self) -> bool:
        return len(self._tests) > 1 or (len(self._tests) == 1 and self._tests[0].name is not None)
    
    def add_test(self, value: float, low: float | None, high: float | None, 
                 unit: str, comp: CompOp, status: StepStatus | None = None) -> 'NumericLimitTest':
        """Add single test (C# pattern)."""
        if self.is_multiple:
            raise InvalidOperationError("Use add_multiple_test for multi-test steps")
        # Create and add test...
    
    def add_multiple_test(self, name: str, value: float, ...) -> 'NumericLimitTest':
        """Add named test for multi-measurement step."""
        if not self.is_multiple and self._tests:
            raise InvalidOperationError("Cannot mix single and multiple tests")
        self.step_type = "ET_MNLT"
        # Create and add named test...
    
    # Custom serializer handles the array format
    @computed_field(alias="numericMeas")
    @property
    def numeric_meas(self) -> list[dict]:
        return [t.to_dict() for t in self._tests]
```

**Alternative: Keep separate classes but with shared base**

```python
class NumericStepBase(Step, ABC):
    """Base for numeric limit steps."""
    @abstractmethod
    def _get_measurements(self) -> list[dict]: ...
    
    @computed_field(alias="numericMeas")
    @property
    def numeric_meas(self) -> list[dict]:
        return self._get_measurements()

class NumericLimitStep(NumericStepBase):
    """Single numeric measurement step."""
    step_type: Literal["ET_NLT"] = "ET_NLT"
    measurement: NumericMeasurement
    
    def _get_measurements(self) -> list[dict]:
        return [self.measurement.model_dump(by_alias=True, exclude_none=True)]

class MultiNumericLimitStep(NumericStepBase):
    """Multiple numeric measurements step."""
    step_type: Literal["ET_MNLT"] = "ET_MNLT"
    measurements: list[NumericMeasurement] = Field(default_factory=list)
    
    def add_measurement(self, name: str, value: float, ...) -> NumericMeasurement: ...
    
    def _get_measurements(self) -> list[dict]:
        return [m.model_dump(by_alias=True, exclude_none=True) for m in self.measurements]
```

### 5.3 Measurement Classes

```python
class NumericMeasurement(WATSBase):
    """A single numeric measurement/test."""
    name: str | None = None  # None for single, required for multi
    value: float
    unit: str | None = None
    comp_op: CompOp = Field(default=CompOp.LOG, serialization_alias="compOp")
    low_limit: float | None = Field(default=None, serialization_alias="lowLimit")
    high_limit: float | None = Field(default=None, serialization_alias="highLimit")
    status: str = "P"
    
    def calculate_status(self, value: float) -> str:
        """Auto-calculate status based on comp_op and limits (Active mode)."""
        # Implementation from v1...

class StringMeasurement(WATSBase):
    """A single string measurement/test."""
    name: str | None = None
    value: str
    comp_op: CompOp = Field(default=CompOp.LOG, serialization_alias="compOp")
    limit: str | None = None
    status: str = "P"

class BooleanMeasurement(WATSBase):
    """A single pass/fail measurement."""
    name: str | None = None
    status: str = "P"  # "P" or "F"
```

### 5.4 Factory Method Signatures (C# Parity)

Mapping C# method signatures to Python v3:

| C# Method | Python v3 Method | Notes |
|-----------|------------------|-------|
| `AddNumericLimitStep(name)` | `add_numeric_limit_step(name)` | Returns step, user calls `.add_test()` |
| `step.AddTest(value, low, high, unit)` | `step.add_test(value, low, high, unit)` | Single test |
| `step.AddMultipleTest(name, value, ...)` | `step.add_test(name, value, ...)` | Named = multi |
| `AddPassFailStep(name)` | `add_pass_fail_step(name)` | Returns step |
| `step.AddTest(passed)` | `step.add_test(passed)` | Boolean test |
| `AddStringValueStep(name)` | `add_string_step(name)` | Returns step |
| `AddSequenceCall(name)` | `add_sequence_call(name)` | Nested sequence |
| `AddGenericStep(type, name)` | `add_generic_step(type, name)` | Flow control etc. |

**Python v3 convenience methods (keep from v1):**

```python
# These "shortcut" methods create step + test in one call
def add_numeric_step(self, *, name, value, unit, comp_op, low_limit, high_limit, status=None):
    """Convenience: Create NumericLimitStep with single test in one call."""
    step = self.add_numeric_limit_step(name)
    step.add_test(value, comp_op, low_limit, high_limit, unit, status)
    return step
```

---

## 6. Surface Diff from v1

### 6.1 Breaking Changes (Minimal)

| v1 | v3 | Migration |
|----|-----|-----------|
| `NumericStep` class | `NumericLimitStep` class | Rename import |
| `MultiNumericStep` class | `NumericLimitStep` (same class) | Use `.add_test(name=...)` |
| `BooleanStep` class | `PassFailStep` class | Rename import (matches C#) |
| `StringStep` class | `StringValueStep` class | Rename import (matches C#) |

### 6.2 Preserved (No Change)

- `UUTReport` constructor signature
- `get_root_sequence_call()` method
- `add_numeric_step()` convenience method
- `add_sequence_call()` method
- `add_chart_step()` method
- `add_generic_step()` method
- JSON output format
- Status calculation (Active mode)
- Parent injection / hierarchy tracking

### 6.3 New Capabilities (Additive)

- Direct step construction: `NumericLimitStep(name="Test")` then add
- C#-style two-step creation: `step = seq.add_numeric_limit_step("Test"); step.add_test(...)`
- Better type hints (single vs multi is clearer)
- Loop support (`start_loop()` / `stop_loop()` from C#)

---

## 7. Implementation Plan

### Phase 1: Core Infrastructure
1. Create `report_models_v3/` package structure
2. Implement `WATSBase` (may share from v1)
3. Implement `Step` base class with common fields
4. Implement `Measurement` base classes

### Phase 2: Step Classes
1. `SequenceCall` with factory methods
2. `NumericLimitStep` with `NumericMeasurement`
3. `PassFailStep` with `BooleanMeasurement`
4. `StringValueStep` with `StringMeasurement`
5. `GenericStep`, `ChartStep`, `ActionStep`
6. Step type union (`StepType`)

### Phase 3: Report Classes
1. `UUTReport` with all fields
2. `UUTInfo` (import or reimplement)
3. `UURReport` (similar pattern)
4. `UURInfo`, `UURSubUnit`, etc.

### Phase 4: Serialization & Validation
1. Custom serializers for measurement arrays
2. JSON round-trip tests
3. Parity tests with v1 output

### Phase 5: Integration
1. Update `async_service.py` to support v3 (feature flag)
2. Migration guide for users
3. Deprecation warnings on v1 (optional)

---

## 8. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| JSON format regression | Extensive round-trip tests comparing v1 vs v3 output |
| User API breakage | Keep convenience methods, provide clear migration guide |
| Type checker issues | Thorough mypy/pyright testing |
| Performance regression | Benchmark serialization paths |

---

## 9. Appendix: File Structure

```
report_models_v3/
├── __init__.py              # Public exports
├── ARCHITECTURE_ANALYSIS.md # This document
├── V3_REPORT_MODEL_INSTRUCTIONS.md # Original requirements
├── C#/                      # C# reference code
│
├── base/
│   ├── __init__.py
│   ├── wats_base.py         # Base model class
│   └── enums.py             # StepStatus, CompOp, etc.
│
├── measurements/
│   ├── __init__.py
│   ├── numeric.py           # NumericMeasurement
│   ├── string.py            # StringMeasurement
│   └── boolean.py           # BooleanMeasurement
│
├── steps/
│   ├── __init__.py
│   ├── step.py              # Step base class
│   ├── sequence_call.py     # SequenceCall with factories
│   ├── numeric_limit_step.py
│   ├── pass_fail_step.py
│   ├── string_value_step.py
│   ├── generic_step.py
│   └── chart_step.py
│
├── reports/
│   ├── __init__.py
│   ├── uut_report.py        # UUTReport
│   ├── uut_info.py          # UUTInfo
│   ├── uur_report.py        # UURReport
│   └── uur_info.py          # UURInfo
│
└── shared/
    ├── __init__.py
    ├── misc_info.py         # MiscInfo
    ├── asset.py             # Asset, AssetStats
    ├── attachment.py        # Attachment
    └── chart.py             # Chart, ChartSeries
```
