# Report Models v3 - Architecture Document

**Version:** 3.0  
**Created:** January 30, 2026  
**Status:** Design Phase - Deep Analysis

---

## 1. Executive Summary

v3 is a **refined implementation of v1's inheritance-based design**, fixing flaws while preserving the elegant patterns that work. The philosophy is:

> **"Fix the bugs, not the architecture."**

### Core Principles

1. **Proper Inheritance** - `Report` base class with all common fields; UUT/UUR inherit and specialize
2. **Preserve StepList** - The polymorphic list pattern is core; it "just works" for type resolution
3. **Unified Info Classes** - `ReportInfo` base with UUT/UUR specializations; serialize to `uut`/`uur` aliases
4. **SubUnit Inheritance** - `SubUnit` base; `UURSubUnit` extends with failure tracking
5. **Keep Factory Methods** - SequenceCall's `add_*` methods are the primary API
6. **JSON Contract** - Output format is immutable

---

## 2. Deep Analysis of v1's Elegant Patterns

Before designing v3, we must understand what v1 does **right**.

### 2.1 The StepList Pattern - KEEP THIS

The `StepList` is a **polymorphic container** that automatically handles:

1. **Parent injection** - When you `append()` a step, it sets `step.parent = self.parent`
2. **Type resolution** - Items are stored and retrieved as their actual types (not base `Step`)
3. **Recursive hierarchy** - SequenceCalls contain StepLists, which can contain SequenceCalls

```python
class StepList(List[StepType]):
    """Custom list that behaves like a list but has a parent reference."""
    
    def __init__(self, items=None, parent: Optional["SequenceCall"] = None):
        super().__init__(items or [])
        self.parent = parent

    def append(self, item):
        """Ensure parent is set when appending."""
        if hasattr(item, "parent"):
            item.parent = self.parent
        super().append(item)
```

**Why this is elegant:**
- In C++, this would be `std::vector<std::unique_ptr<Step>>` with virtual dispatch
- In Python, we get this "for free" via duck typing + Pydantic's discriminated union
- The `StepType` union + discriminator function handles deserialization polymorphism

**v3 Action:** Keep `StepList` exactly as-is. It's not broken.

### 2.2 The Report Inheritance Pattern - KEEP THIS

v1's `Report` base class contains ALL common fields:

```python
class Report(WATSBase):
    id: UUID
    type: str  # "T" or "R"
    pn: str
    sn: str
    rev: str
    process_code: int
    result: str
    station_name: str
    location: str
    purpose: str
    start: datetime
    misc_infos: list[MiscInfo]
    sub_units: list[SubUnit]
    assets: list[Asset]
    # ... helper methods: add_misc_info(), add_sub_unit(), add_asset()
```

And `UUTReport` / `UURReport` inherit and specialize:

```python
class UUTReport(Report):
    type: Literal["T"] = "T"
    root: SequenceCall  # UUT-specific
    info: UUTInfo = Field(serialization_alias="uut")  # UUT-specific

class UURReport(Report):
    type: Literal["R"] = "R"
    uur_info: UURInfo = Field(serialization_alias="uur")  # UUR-specific
    sub_units: List[UURSubUnit]  # Override with repair-aware type
```

**Why this is elegant:**
- Common fields defined ONCE
- Helper methods (`add_misc_info()`) inherited by both
- Type discrimination via `type` field for union parsing
- Subclasses only add what's different

**v3 Action:** Keep inheritance. Fix the info/sub_unit naming issues.

### 2.3 The ReportInfo Inheritance Pattern - KEEP THIS

```python
class ReportInfo(WATSBase):
    """Base info for both UUT and UUR."""
    operator: str = Field(serialization_alias="user")
    comment: Optional[str]
    exec_time: Optional[float]

class UUTInfo(ReportInfo):
    """UUT-specific: fixture, socket, batch info."""
    fixture_id: str
    socket_index: int
    batch_number: str
    # ...

class UURInfo(ReportInfo):
    """UUR-specific: repair codes, ref_uut, timing."""
    repair_process_code: int
    ref_uut: UUID
    # ...
```

**Why this is elegant:**
- Common operator/comment/exec_time defined once
- Subclasses add domain-specific fields
- Serialization aliases handle JSON naming

**v3 Action:** Keep this pattern. Fix the accessor naming (`uut.info.operator` not `uut.uut.operator`).

### 2.4 The SubUnit Pattern - KEEP, WITH REFINEMENT

v1 has:
- `SubUnit` - basic part tracking (pn, sn, rev, part_type)
- `UURSubUnit` - extends with idx, parent_idx, failures

**Current issue:** They don't share a base class properly.

**v3 Action:** Make `UURSubUnit` properly inherit from `SubUnit`.

### 2.5 The Step Discriminator Pattern - KEEP THIS

```python
def _discriminate_step_type(v: Any) -> str:
    """Maps stepType values to the appropriate Step class tag."""
    step_type = v.get('stepType', '')
    if step_type in ['SequenceCall', 'WATS_SeqCall']:
        return 'SequenceCall'
    elif step_type in ['ET_NLT', 'NumericLimitStep']:
        return 'NumericStep'
    # ...

StepType = Annotated[
    Union[
        Annotated[SequenceCall, Tag('SequenceCall')],
        Annotated[NumericStep, Tag('NumericStep')],
        # ...
    ],
    Discriminator(_discriminate_step_type)
]
```

**Why this is elegant:**
- Single discriminator function handles ALL step type mapping
- Easy to extend with new step types
- Fallback to `UnknownStep` for forward compatibility

**v3 Action:** Keep this pattern exactly.

### 2.6 The Factory Method Pattern - KEEP THIS

SequenceCall provides factory methods:

```python
class SequenceCall(Step):
    def add_numeric_step(self, *, name, value, unit, ...) -> NumericStep:
        """Create, configure, append, and return a numeric step."""
        ns = NumericStep(name=name, ...)
        ns.measurement = NumericMeasurement(value=value, ...)
        self.steps.append(ns)
        return ns
```

**Why this is elegant:**
- Single method creates fully-configured step
- Automatic parent injection via StepList.append()
- Returns the step for chaining or further configuration
- Matches C# API pattern

**v3 Action:** Keep factory methods. Consider adding C#-style two-step pattern as alternative.

### 2.7 Edge Functionality - PRESERVE ALL

v1 has important edge functionality that must be preserved in v3:

#### 2.7.1 Validation Infrastructure

```python
# Step base class validation pattern
class Step(WATSBase, ABC):
    MAX_NAME_LENGTH: ClassVar[int] = 100
    
    @abstractmethod
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        """Validate step and optionally trigger child validation."""
        return True
```

Each step type implements `validate_step()`:
- `SequenceCall`: Validates itself + optionally all child steps
- `NumericStep`: Validates measurement bounds, CompOp logic
- `BooleanStep`, `StringStep`, etc.: Type-specific validation

**v3 Action:** Preserve the full validation infrastructure.

#### 2.7.2 Parent/Child Relationship Management

```python
# StepList automatic parent injection
class StepList(List[StepType]):
    def append(self, item):
        if hasattr(item, "parent"):
            item.parent = self.parent  # Auto-set parent
        super().append(item)

# Step has parent reference + failure propagation
class Step(WATSBase, ABC):
    parent: Optional['Step'] = Field(default=None, exclude=True)
    fail_parent_on_failure: bool = Field(default=True, exclude=True)
    
    def propagate_failure(self) -> None:
        """Propagate failure up the hierarchy."""
        self.status = StepStatus.Failed
        if self.fail_parent_on_failure and self.parent is not None:
            self.parent.propagate_failure()
    
    def get_step_path(self) -> str:
        """Get full path: 'Root/SubSeq/Step'."""
        path = []
        current = self
        while current is not None:
            path.append(current.name)
            current = current.parent
        return '/'.join(reversed(path))
```

**v3 Action:** Preserve parent injection, failure propagation, and path generation.

#### 2.7.3 Field Validators (Serial Number, Part Number)

```python
# Report base class
@field_validator('sn', mode='after')
@classmethod
def validate_sn(cls, v: str) -> str:
    return validate_serial_number(v)  # Checks for problematic chars

@field_validator('pn', mode='after')  
@classmethod
def validate_pn(cls, v: str) -> str:
    return validate_part_number(v)
```

Same validators in `SubUnit`, `Asset`, and other classes.

**v3 Action:** Preserve all field validators.

#### 2.7.4 Model Validators (Time Sync, Parent Assignment)

```python
# Report: Sync start/startUTC
@model_validator(mode='after')
def sync_start_times(self) -> 'Report':
    """Ensure start and start_utc are synchronized."""
    # ... handles timezone-aware conversions
    
# SequenceCall: Assign parents after construction
@model_validator(mode="after")
def assign_parent(self):
    """Ensure all steps have correct parent after model creation."""
    if not isinstance(self.steps, StepList):
        self.steps = StepList(self.steps)
    self.steps.set_parent(self)
    return self
```

**v3 Action:** Preserve all model validators.

#### 2.7.5 Measurement Validators (Wrap/Unwrap)

```python
# Single-measurement steps unpack from array:
@model_validator(mode='before')
def unpack_measurement(cls, data):
    if 'numericMeas' in data and isinstance(data['numericMeas'], list):
        data['numericMeas'] = data['numericMeas'][0]  # Unwrap
    return data

# And serialize back to array:
@field_serializer('measurement', when_used='json')
def serialize_measurement(self, measurement) -> list:
    return [measurement.model_dump(by_alias=True, exclude_none=True)]
```

**v3 Action:** Preserve but extract to `SingleMeasurementMixin` for DRY.

#### 2.7.6 Pydantic Field Constraints

```python
# Length limits matching WATS API:
name: str = Field(max_length=100, min_length=1)
comment: str = Field(max_length=5000)
operator: str = Field(max_length=100)
fixture_id: str = Field(max_length=100)

# Pattern constraints:
type: str = Field(pattern='^[TR]$')  # T=Test, R=Repair
group: str = Field(pattern='^[SMC]$')  # Setup/Main/Cleanup
status: str = Field(pattern='^[PFSDET]$')  # Pass/Fail/Skip/Done/Error/Terminated
```

**v3 Action:** Preserve all field constraints.

---

## 3. What's Wrong with v1 (Bugs to Fix)

### 3.1 Info Field Naming Confusion

**Problem:**
```python
class UUTReport(Report):
    info: UUTInfo = Field(serialization_alias="uut")  # Serializes as "uut"
    
# Usage becomes awkward:
report.info.operator  # OK
# But in JSON it's:
{"uut": {"user": "John"}}  # "uut" not "info"
```

**Fix in v3:**
- Keep the field name as `info` internally
- Keep serialization alias as `uut`/`uur` for JSON compatibility
- Document clearly: `report.info` in code, `"uut"` in JSON

### 3.2 SubUnit Type Override

**Problem:**
```python
class Report(WATSBase):
    sub_units: list[SubUnit] = ...

class UURReport(Report):
    sub_units: List[UURSubUnit] = ...  # type: ignore needed!
```

**Fix in v3:**
- Use Generic or TypeVar for SubUnit type
- Or: Keep sub_units in Report, add `uur_sub_units` property in UURReport that casts

### 3.3 Single vs Multi Step Classes

**Problem:** Six classes instead of three:
- `NumericStep` + `MultiNumericStep`
- `BooleanStep` + `MultiBooleanStep`  
- `StringStep` + `MultiStringStep`

Each pair has duplicated:
- Model validators (`unpack_measurement`)
- Field serializers (`serialize_measurement`)
- Validation logic

**Fix in v3:**
Keep separate classes (they ARE different step types with different `stepType` values), but:
- Extract common serialization logic to base class
- Use shared validator/serializer decorators
- Consider a `MeasurementStepMixin` for the wrap/unwrap logic

### 3.4 Measurement List Serialization

**Problem:** Single steps store `measurement: Measurement`, but JSON uses arrays:
```python
@field_serializer('measurement', when_used='json')
def serialize_measurement(self, measurement) -> list:
    return [measurement.model_dump(...)]  # Wrap in list

@model_validator(mode='before')
def unpack_measurement(cls, data):
    data['numericMeas'] = data['numericMeas'][0]  # Unwrap from list
```

This wrap/unwrap is repeated in EVERY single step class.

**Fix in v3:**
- Create `SingleMeasurementMixin` with reusable validators/serializers
- Or: Use a `MeasurementField` descriptor that handles this

### 3.5 Class Naming Inconsistency

**Problem:**
- Python: `BooleanStep` 
- C#: `PassFailStep`
- Python: `StringStep`
- C#: `StringValueStep`

**Fix in v3:**
Add C# aliases:
```python
# Keep existing names for compatibility
class BooleanStep(Step): ...

# Add C# aliases
PassFailStep = BooleanStep
StringValueStep = StringStep
```

### 3.6 StepList Type Checking Issues (GitHub Actions / mypy)

**Problem:** The `StepList` custom list class causes several type checking issues that surface during CI/release workflows:

**Issue 1: Generic type argument missing**
```python
# Current v1 code:
steps: StepList = Field(default_factory=StepList)  # type: ignore[type-arg]
```
The `StepList` is generic (`StepList[StepType]`) but Pydantic's `Field()` doesn't properly propagate the type argument. This requires a `# type: ignore[type-arg]` comment.

**Issue 2: Parent argument type mismatch**
```python
# Factory methods pass parent=self, but Step.parent expects Optional['Step']:
ns = NumericStep(name=name, ..., parent=self)  # type: ignore[arg-type]
```
All 8 factory methods in `SequenceCall` require `# type: ignore[arg-type]` because `SequenceCall` is being passed where `Step` is expected (even though `SequenceCall` inherits from `Step`).

**Issue 3: `__get_pydantic_core_schema__` complexity**
```python
@classmethod
def __get_pydantic_core_schema__(cls, source_type, handler):
    """Correctly handle serialization and validation for Pydantic with StepType (Union)."""
    return core_schema.list_schema(
        items_schema=handler.generate_schema(StepType),
        serialization=core_schema.plain_serializer_function_ser_schema(list),
    )
```
This custom schema generation is required for Pydantic to understand our custom list with a Union type. It works correctly but can produce warnings in strict type checking environments.

**Issue 4: arbitrary_types_allowed propagation**
To support `StepList`, several classes need:
```python
model_config = {"arbitrary_types_allowed": True}  # Fixes StepList issue
```
This is required in: `WATSBase`, `NumericMeasurement`, `MultiNumericMeasurement`, `NumericStep`, `MultiNumericStep`, and `Measurement` base classes.

**Impact on CI:** These issues cause mypy to report errors, but the workflow has `continue-on-error: true`:
```yaml
- name: Run mypy
  run: mypy src/pywats --ignore-missing-imports
  continue-on-error: true  # Don't fail build on type errors for now
```

**v3 Fix Strategy:**
1. **Keep StepList exactly as-is** - The functionality is correct and elegant
2. **Improve type annotations** to reduce `# type: ignore` comments:
   ```python
   # Better typing for parent
   parent: Optional['SequenceCall'] = Field(default=None, exclude=True)
   
   # Or use TYPE_CHECKING for forward reference:
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from .sequence_call import SequenceCall
   parent: Optional['SequenceCall'] = Field(default=None, exclude=True)
   ```
3. **Add proper generic type parameter to StepList annotation:**
   ```python
   from typing import TypeVar
   T = TypeVar('T', bound='Step')
   
   class StepList(List[T]):
       ...
   
   # In SequenceCall:
   steps: StepList[StepType] = Field(default_factory=lambda: StepList())
   ```
4. **Document remaining `# type: ignore` as intentional** - Some are unavoidable due to Pydantic/mypy interaction

**Current v1 `# type: ignore` locations (17 total):**
| File | Line | Issue |
|------|------|-------|
| `sequence_call.py` | 104 | `StepList` type-arg |
| `sequence_call.py` | 197, 221, 246, 264, 281, 299, 321, 340 | Factory method `parent=self` |
| `uur_report.py` | 66, 124 | SubUnit type override |
| `uur_info.py` | 250, 258 | Dict index assignment |
| `wats_base.py` | 18, 19, 26 | Validation context access |

**v3 Goal:** Reduce from 17 to ~5 necessary `# type: ignore` comments.

### 3.7 Complete mypy Error Analysis (v1 Report Models)

This section documents ALL type checking issues found in v1, analyzed with mypy on January 30, 2026.

#### Summary
```
Standard check: 10 errors in 4 files (35 files checked)
Strict check:   196 errors in 17 files
type: ignore:   17 explicit suppression comments
```

#### 3.7.1 Critical Type Errors (10 errors, standard mode)

These errors appear in normal mypy runs and indicate real type safety issues:

| File | Line | Error Code | Issue |
|------|------|-----------|-------|
| `numeric_step.py` | 42 | `[assignment]` | `measurement: NumericMeasurement = None` - None assigned to non-Optional type |
| `numeric_step.py` | 82 | `[union-attr]` | `comp_op.validate_limits()` called when `comp_op` might be None |
| `numeric_step.py` | 82 | `[arg-type]` | `low_limit: float | str | None` passed where `float | None` expected |
| `numeric_step.py` | 82 | `[arg-type]` | `high_limit: float | str | None` passed where `float | None` expected |
| `numeric_step.py` | 120 | `[union-attr]` | Same as line 82 - MultiNumericStep validation |
| `numeric_step.py` | 120 | `[arg-type]` | Same limit type issue in MultiNumericStep |
| `numeric_step.py` | 120 | `[arg-type]` | Same limit type issue in MultiNumericStep |
| `sequence_call.py` | 182 | `[assignment]` | `value = "NaN"` but `value: float` - should be `float | str` |
| `chart_step.py` | 19 | `[assignment]` | `step_type: Literal["WATS_XYGMNLT"]` overrides base `Literal["ET_MNLT"]` |
| `uur_info.py` | 247 | `[index]` | Dict assignment to union type that includes non-dict |

**v3 Fixes:**

1. **NumericStep measurement default:**
```python
# v1 (wrong):
measurement: NumericMeasurement = Field(default=None, ...)

# v3 (correct):
measurement: Optional[NumericMeasurement] = Field(default=None, ...)
# Or use factory:
measurement: NumericMeasurement = Field(default_factory=lambda: NumericMeasurement())
```

2. **CompOp validation guard:**
```python
# v1 (unsafe):
if not comp_op.validate_limits(low_limit=..., high_limit=...)

# v3 (safe):
if comp_op is not None and not comp_op.validate_limits(
    low_limit=float(self.measurement.low_limit) if self.measurement.low_limit is not None else None,
    high_limit=float(self.measurement.high_limit) if self.measurement.high_limit is not None else None
)
```

3. **Limit types - allow str for formatted values:**
```python
# v1: Inconsistent typing
low_limit: Optional[float] = None  # But can receive "NaN" string

# v3: Accept what WATS API actually sends
low_limit: Optional[Union[float, str]] = None
# Update CompOp.validate_limits() signature to match
```

4. **ChartStep inheritance:**
```python
# v1: Overrides Literal with incompatible Literal
class ChartStep(MultiNumericStep):
    step_type: Literal["WATS_XYGMNLT"] = ...  # Conflicts with base

# v3: Don't inherit step_type, use discriminator properly
class ChartStep(Step):  # Inherit from Step directly, not MultiNumericStep
    step_type: Literal["WATS_XYGMNLT"] = ...
    measurements: list[MultiNumericMeasurement] = ...  # Composition over inheritance
```

5. **UURInfo dict assignment:**
```python
# v1: result type is too broad
result: bool | dict[str, ...] | str | None = ...
result['confirm_date'] = ...  # Error: might not be dict

# v3: Narrow the type first
result: dict[str, Any] = {...}  # Explicit dict type
result['confirm_date'] = ...  # Now safe
```

#### 3.7.2 Explicit Suppressions (17 `# type: ignore` comments)

Currently in v1:

| Location | Comment | Root Cause | v3 Action |
|----------|---------|------------|-----------|
| `wats_base.py:18` | `[union-attr]` | `info.context` might be None | Use `assert` or narrow type |
| `wats_base.py:19` | `[union-attr]` | Same context access | Same fix |
| `wats_base.py:26` | `[attr-defined]` | `cls.__qualname__` access | Use `getattr()` with default |
| `uur_info.py:250` | `[index]` | Dict type too broad | Narrow return type |
| `uur_info.py:258` | `[assignment]` | Similar issue | Same fix |
| `uur_report.py:66` | `[assignment]` | `sub_units: List[UURSubUnit]` overrides `List[SubUnit]` | Use Generic or TypeVar |
| `uur_report.py:124` | `[override]` | `add_sub_unit()` signature differs | Use `@overload` or rename |
| `sequence_call.py:104` | `[type-arg]` | `StepList` without type parameter | Add proper Generic support |
| `sequence_call.py:197` | `[arg-type]` | `parent=self` type mismatch | Fix parent type annotation |
| `sequence_call.py:221` | `[arg-type]` | Same - MultiNumericStep | Same fix |
| `sequence_call.py:246` | `[arg-type]` | Same - StringStep | Same fix |
| `sequence_call.py:264` | `[arg-type]` | Same - MultiStringStep | Same fix |
| `sequence_call.py:281` | `[arg-type]` | Same - BooleanStep | Same fix |
| `sequence_call.py:299` | `[arg-type]` | Same - MultiBooleanStep | Same fix |
| `sequence_call.py:321` | `[arg-type]` | Same - ChartStep | Same fix |
| `sequence_call.py:340` | `[arg-type]` | Same - GenericStep | Same fix |

**v3 Strategy for Factory Method `[arg-type]` (8 occurrences):**
```python
# v1: parent expects Optional['Step'], receives SequenceCall
class Step(WATSBase, ABC):
    parent: Optional['Step'] = Field(default=None, exclude=True)

# v3 Option A: Widen Step.parent type
parent: Optional['SequenceCall'] = Field(default=None, exclude=True)

# v3 Option B: Use Protocol for parent type
from typing import Protocol

class StepParent(Protocol):
    name: str
    def propagate_failure(self) -> None: ...
    
parent: Optional[StepParent] = Field(default=None, exclude=True)

# v3 Option C: Use TYPE_CHECKING conditional import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .sequence_call import SequenceCall
    
parent: Optional['SequenceCall'] = Field(default=None, exclude=True)
```

#### 3.7.3 Strict Mode Issues (196 errors)

When running `mypy --strict`, additional categories of issues appear:

| Category | Count | Severity | v3 Action |
|----------|-------|----------|-----------|
| Missing imports (`Name "X" not defined`) | ~50 | **High** | Fix `common_types.py` wildcard imports |
| Missing return type annotations | ~30 | Medium | Add return types to all methods |
| Missing parameter type annotations | ~40 | Medium | Add parameter types |
| Missing generic type parameters | ~20 | Low | Add `list[X]` instead of `list` |
| Untyped decorator issues | ~10 | Low | Type decorators properly |
| Comparison overlap warnings | ~5 | Low | Fix membership tests |

**Critical Issue: Wildcard Imports**

```python
# common_types.py uses:
from typing import *
from pydantic import *

# Then sequence_call.py does:
from ...common_types import *

# In strict mode, these names are "not defined" because
# mypy doesn't follow * imports properly
```

**v3 Fix:**
```python
# common_types.py - explicit exports
from typing import (
    Optional, Union, List, Dict, Literal, 
    Annotated, Any, ClassVar, TYPE_CHECKING
)
from pydantic import Field, model_validator, field_serializer
# ... etc

__all__ = ['Optional', 'Union', 'List', ...]

# sequence_call.py - explicit imports
from ...common_types import Optional, Union, List, Field
# Or even better - import directly from typing/pydantic
```

#### 3.7.4 v3 Type Safety Roadmap

| Phase | Target | Est. Errors Fixed |
|-------|--------|-------------------|
| Phase 1 | Fix critical 10 errors | 10 |
| Phase 2 | Fix factory method parent types | 8 (of 17 ignores) |
| Phase 3 | Fix SubUnit type override | 2 |
| Phase 4 | Replace wildcard imports | ~50 strict errors |
| Phase 5 | Add missing type annotations | ~70 strict errors |

**v3 Goal: Pass `mypy --strict` with 0 errors and ≤5 documented `# type: ignore` comments.**

---

## 4. v3 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              WATS Base Layer                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────────────────────────────────────────────────────────────┐  │
│   │                         WATSBase                                      │  │
│   │  - model_config (aliases, enums, inf/nan handling)                   │  │
│   │  - inject_defaults() validator                                        │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                                      △                                       │
│                                      │ inherits                              │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────┼──────────────────────────────────────┐
│                              Report Layer                                    │
├──────────────────────────────────────┼──────────────────────────────────────┤
│                                      │                                       │
│   ┌──────────────────────────────────┴───────────────────────────────────┐  │
│   │                          Report (Base)                                │  │
│   │  id, type, pn, sn, rev, process_code, result                         │  │
│   │  station_name, location, purpose, start                               │  │
│   │  misc_infos, sub_units, assets, binary_data, additional_data         │  │
│   │                                                                       │  │
│   │  + add_misc_info(), add_sub_unit(), add_asset()                      │  │
│   └──────────────────────────────────────────────────────────────────────┘  │
│                          △                         △                         │
│                          │                         │                         │
│           ┌──────────────┴────────┐    ┌──────────┴──────────┐              │
│           │                       │    │                      │              │
│   ┌───────┴───────┐       ┌───────┴────┴──┐                                 │
│   │   UUTReport   │       │   UURReport    │                                 │
│   │   type="T"    │       │   type="R"     │                                 │
│   │               │       │                │                                 │
│   │ root: ────────┼───┐   │ sub_units: ────┼──► List[UURSubUnit]            │
│   │ info: ────────┼─┐ │   │ info: ─────────┼──► UURInfo (alias="uur")       │
│   └───────────────┘ │ │   └────────────────┘                                 │
│                     │ │                                                      │
│                     │ │   ┌────────────────────────────────────────────┐    │
│                     │ │   │              ReportInfo (Base)             │    │
│                     │ │   │  operator, comment, exec_time              │    │
│                     │ │   └────────────────────────────────────────────┘    │
│                     │ │                  △                △                  │
│                     │ │    ┌─────────────┴──┐    ┌───────┴─────────┐        │
│                     │ └──► │    UUTInfo     │    │    UURInfo      │        │
│                     │      │ fixture_id     │    │ repair_process  │        │
│                     │      │ socket_index   │    │ ref_uut         │        │
│                     │      │ batch_number   │    │ uur_operator    │        │
│                     │      └────────────────┘    └─────────────────┘        │
│                     │                                                        │
│                     │   ┌────────────────────────────────────────────┐      │
│                     │   │              SubUnit (Base)                 │      │
│                     │   │  pn, sn, rev, part_type                    │      │
│                     │   └────────────────────────────────────────────┘      │
│                     │                        △                               │
│                     │          ┌─────────────┴─────────────┐                │
│                     │          │        UURSubUnit         │                │
│                     │          │  idx, parent_idx          │                │
│                     │          │  failures: List[UURFailure]│               │
│                     │          └───────────────────────────┘                │
│                     │                                                        │
│                     ▼                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                              Step Layer                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌───────────────────────────────────────────────────────────────────────┐ │
│   │                           SequenceCall                                 │ │
│   │  - steps: StepList[StepType]  ◄── Polymorphic container!             │ │
│   │  - sequence: SequenceCallInfo                                         │ │
│   │                                                                        │ │
│   │  Factory Methods (THE primary API):                                   │ │
│   │  ├─ add_sequence_call(name, file_name, version)  → SequenceCall      │ │
│   │  ├─ add_numeric_step(name, value, unit, ...)     → NumericStep       │ │
│   │  ├─ add_multi_numeric_step(name)                 → MultiNumericStep  │ │
│   │  ├─ add_boolean_step(name, status)               → BooleanStep       │ │
│   │  ├─ add_multi_boolean_step(name)                 → MultiBooleanStep  │ │
│   │  ├─ add_string_step(name, value, ...)            → StringStep        │ │
│   │  ├─ add_multi_string_step(name)                  → MultiStringStep   │ │
│   │  ├─ add_chart_step(...)                          → ChartStep         │ │
│   │  └─ add_generic_step(step_type, name)            → GenericStep       │ │
│   └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│   ┌───────────────────────────────────────────────────────────────────────┐ │
│   │                        StepList[StepType]                             │ │
│   │  - Automatic parent injection on append/extend/insert                 │ │
│   │  - Polymorphic storage (actual types preserved)                       │ │
│   │  - Custom Pydantic schema for Union handling                          │ │
│   └───────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│   ┌───────────────────────────────────────────────────────────────────────┐ │
│   │                          Step (Abstract)                              │ │
│   │  name, status, step_type, group, id                                   │ │
│   │  error_code, error_message, report_text                               │ │
│   │  start, tot_time, loop                                                │ │
│   │  parent: Step (excluded from JSON)                                    │ │
│   │  additional_results, chart, attachment                                │ │
│   │                                                                        │ │
│   │  + get_step_path(), add_chart(), add_attachment()                     │ │
│   │  + propagate_failure(), validate_step()                               │ │
│   └───────────────────────────────────────────────────────────────────────┘ │
│              △           △           △           △           △              │
│              │           │           │           │           │              │
│   ┌──────────┴──┐  ┌─────┴─────┐  ┌──┴───┐  ┌────┴────┐  ┌───┴────┐        │
│   │SequenceCall │  │MeasureStep│  │Chart │  │ Generic │  │ Action │        │
│   │             │  │  (mixin)  │  │ Step │  │  Step   │  │  Step  │        │
│   └─────────────┘  └─────┬─────┘  └──────┘  └─────────┘  └────────┘        │
│                          │                                                   │
│          ┌───────────────┼───────────────┐                                  │
│          │               │               │                                  │
│   ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐                          │
│   │NumericStep  │ │BooleanStep  │ │StringStep   │                          │
│   │ET_NLT       │ │ET_PFT       │ │ET_SVT       │                          │
│   │measurement: │ │measurement: │ │measurement: │                          │
│   │NumericMeas  │ │BooleanMeas  │ │StringMeas   │                          │
│   └─────────────┘ └─────────────┘ └─────────────┘                          │
│                                                                              │
│   ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐                          │
│   │MultiNumeric │ │MultiBoolean │ │MultiString  │                          │
│   │ET_MNLT      │ │ET_MPFT      │ │ET_MSVT      │                          │
│   │measurements:│ │measurements:│ │measurements:│                          │
│   │list[Multi..]│ │list[Multi..]│ │list[Multi..]│                          │
│   └─────────────┘ └─────────────┘ └─────────────┘                          │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                           Measurement Layer                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌────────────────────────────────────────────────────────────────────┐    │
│   │                       Measurement (Base)                            │    │
│   │  parent_step (excluded)                                             │    │
│   └────────────────────────────────────────────────────────────────────┘    │
│                                    △                                         │
│                                    │                                         │
│   ┌────────────────────────────────┴─────────────────────────────────┐      │
│   │                     BooleanMeasurement                            │      │
│   │  status: str ("P"/"F"/"S")                                        │      │
│   └───────────────────────────────────────────────────────────────────┘      │
│              △                              △                                │
│              │                              │                                │
│   ┌──────────┴──────────┐        ┌─────────┴─────────────┐                  │
│   │  MultiBooleanMeas   │        │   LimitMeasurement    │                  │
│   │  + name: str        │        │   value, comp_op      │                  │
│   └─────────────────────┘        │   low_limit, high_limit│                 │
│                                  │   + calculate_status() │                 │
│                                  └───────────────────────┘                  │
│                                           △                                  │
│                     ┌─────────────────────┼────────────────────┐            │
│                     │                     │                    │            │
│          ┌──────────┴───────┐  ┌──────────┴───────┐  ┌────────┴────────┐   │
│          │NumericMeasurement│  │StringMeasurement │  │MultiNumericMeas │   │
│          │  value: float    │  │  value: str      │  │  + name: str    │   │
│          │  unit: str       │  │  limit: str      │  │                 │   │
│          └──────────────────┘  └──────────────────┘  └─────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Key Design Decisions for v3

### 5.1 Report Base Class - PROPER INHERITANCE

**Decision:** Keep `Report` as base with ALL common fields. UUT/UUR inherit.

```python
class Report(WATSBase):
    """Base class for all reports. Contains ALL common fields."""
    
    # Identity
    id: UUID = Field(default_factory=uuid4)
    type: str = Field(pattern='^[TR]$')
    pn: str
    sn: str  
    rev: str
    
    # Process
    process_code: int = Field(serialization_alias="processCode")
    result: str = Field(default="P")
    
    # Station
    station_name: str = Field(serialization_alias="machineName")
    location: str
    purpose: str
    
    # Timing
    start: datetime
    
    # Collections (shared)
    misc_infos: list[MiscInfo] = Field(default_factory=list, serialization_alias="miscInfos")
    sub_units: list[SubUnit] = Field(default_factory=list, serialization_alias="subUnits")
    assets: list[Asset] = Field(default_factory=list)
    
    # Helper methods
    def add_misc_info(self, description: str, value: Any) -> MiscInfo: ...
    def add_sub_unit(self, part_type: str, sn: str, pn: str, rev: str) -> SubUnit: ...
    def add_asset(self, sn: str, usage_count: int) -> Asset: ...
```

### 5.2 Info Field Naming - CLEAN ACCESS

**Decision:** Field named `info`, serializes to `uut`/`uur`.

```python
class UUTReport(Report):
    type: Literal["T"] = "T"
    root: SequenceCall = Field(default_factory=SequenceCall)
    info: UUTInfo = Field(default_factory=UUTInfo, serialization_alias="uut")
    
# Usage:
report.info.operator  # Clean Python access
# JSON output:
{"type": "T", "uut": {"user": "John", ...}}  # Correct serialization
```

### 5.3 SubUnit Inheritance - PROPER TYPE HIERARCHY

**Decision:** `UURSubUnit` inherits from `SubUnit`.

```python
class SubUnit(WATSBase):
    """Base sub-unit for part tracking."""
    pn: str
    sn: str
    rev: Optional[str]
    part_type: str = Field(default="Unknown", serialization_alias="partType")

class UURSubUnit(SubUnit):
    """Extended sub-unit for repairs with failure tracking."""
    idx: int = 0
    parent_idx: Optional[int] = Field(default=None, serialization_alias="parentIdx")
    failures: Optional[list[UURFailure]] = None
    
    def add_failure(self, category: str, code: str, ...) -> UURFailure: ...
```

### 5.4 UURReport SubUnits - TYPE SPECIALIZATION

**Decision:** UURReport overrides `sub_units` type to `list[UURSubUnit]`.

```python
class UURReport(Report):
    type: Literal["R"] = "R"
    info: UURInfo = Field(default_factory=UURInfo, serialization_alias="uur")
    
    # Override with repair-aware type
    sub_units: list[UURSubUnit] = Field(default_factory=list, serialization_alias="subUnits")
    
    def get_main_unit(self) -> UURSubUnit: ...
    def add_sub_unit(self, pn: str, sn: str, ...) -> UURSubUnit: ...  # Override returns UURSubUnit
```

### 5.5 StepList - PRESERVE EXACTLY

**Decision:** Keep `StepList` implementation unchanged.

```python
class StepList(List[StepType]):
    """Polymorphic step container with automatic parent injection."""
    
    def __init__(self, items=None, parent: Optional["SequenceCall"] = None):
        super().__init__(items or [])
        self.parent = parent

    def set_parent(self, parent: "SequenceCall"):
        self.parent = parent
        for item in self:
            if hasattr(item, "parent"):
                item.parent = parent

    def append(self, item):
        if hasattr(item, "parent"):
            item.parent = self.parent
        super().append(item)
    
    # ... extend, insert with same pattern
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Handle Union[Step types] correctly."""
        return core_schema.list_schema(
            items_schema=handler.generate_schema(StepType),
            serialization=core_schema.plain_serializer_function_ser_schema(list),
        )
```

### 5.6 Single/Multi Steps - KEEP SEPARATE, SHARE LOGIC

**Decision:** Keep 6 step classes, but extract shared serialization logic.

```python
class SingleMeasurementMixin:
    """Mixin for single-measurement steps (NumericStep, BooleanStep, StringStep)."""
    
    _measurement_field: str  # Set by subclass: "numericMeas", "booleanMeas", "stringMeas"
    _measurement_class: type  # Set by subclass
    
    @model_validator(mode='before')
    def unpack_measurement(cls, data: dict) -> dict:
        alias = cls._measurement_field
        if alias in data and isinstance(data[alias], list):
            data[alias] = data[alias][0] if data[alias] else None
        return data
    
    def _serialize_measurement(self, measurement) -> list:
        if measurement is None:
            return []
        return [measurement.model_dump(by_alias=True, exclude_none=True)]

class NumericStep(SingleMeasurementMixin, Step):
    _measurement_field = "numericMeas"
    _measurement_class = NumericMeasurement
    
    step_type: Literal["ET_NLT", "NumericLimitStep"] = "ET_NLT"
    measurement: NumericMeasurement = Field(serialization_alias="numericMeas")
    
    @field_serializer('measurement', when_used='json')
    def serialize_measurement(self, m):
        return self._serialize_measurement(m)
```

### 5.7 C# Naming Aliases - ADD WITHOUT BREAKING

**Decision:** Add C# name aliases for discoverability.

```python
# In __init__.py
from .boolean_step import BooleanStep, MultiBooleanStep
from .string_step import StringStep, MultiStringStep

# C# naming aliases
PassFailStep = BooleanStep
MultiPassFailStep = MultiBooleanStep
StringValueStep = StringStep
MultiStringValueStep = MultiStringStep

__all__ = [
    # Python names (primary)
    'BooleanStep', 'MultiBooleanStep', 'StringStep', 'MultiStringStep',
    # C# aliases (secondary)
    'PassFailStep', 'MultiPassFailStep', 'StringValueStep', 'MultiStringValueStep',
]
```

---

## 6. File Structure for v3

```
report_models_v3/
├── __init__.py                  # Public API + C# aliases
├── V3_ARCHITECTURE.md           # This document
├── VERSION_COMPARISON.md        # v1/v2/v3 comparison  
├── MIGRATION_GUIDE.md           # User migration guide
│
├── base/
│   ├── __init__.py
│   ├── wats_base.py             # Base model (from v1, unchanged)
│   ├── enums.py                 # StepStatus, CompOp, etc.
│   └── mixins.py                # SingleMeasurementMixin, etc.
│
├── shared/
│   ├── __init__.py
│   ├── misc_info.py             # MiscInfo (from v1)
│   ├── asset.py                 # Asset, AssetStats (from v1)
│   ├── attachment.py            # Attachment (from v1)
│   ├── additional_data.py       # AdditionalData (from v1)
│   ├── binary_data.py           # BinaryData (from v1)
│   └── chart.py                 # Chart, ChartSeries (from v1)
│
├── reports/
│   ├── __init__.py
│   ├── report.py                # Report base class (ALL common fields)
│   ├── report_info.py           # ReportInfo base class
│   ├── sub_unit.py              # SubUnit base class
│   │
│   ├── uut/
│   │   ├── __init__.py
│   │   ├── uut_report.py        # UUTReport(Report)
│   │   └── uut_info.py          # UUTInfo(ReportInfo)
│   │
│   └── uur/
│       ├── __init__.py
│       ├── uur_report.py        # UURReport(Report)
│       ├── uur_info.py          # UURInfo(ReportInfo)
│       ├── uur_sub_unit.py      # UURSubUnit(SubUnit)
│       └── uur_failure.py       # UURFailure
│
├── steps/
│   ├── __init__.py              # StepType union, all exports
│   ├── step.py                  # Step abstract base
│   ├── step_list.py             # StepList (from v1, unchanged)
│   ├── sequence_call.py         # SequenceCall + factory methods
│   │
│   ├── measurements/
│   │   ├── __init__.py
│   │   ├── measurement.py       # Measurement base
│   │   ├── numeric.py           # NumericMeasurement, MultiNumericMeasurement
│   │   ├── boolean.py           # BooleanMeasurement, MultiBooleanMeasurement
│   │   └── string.py            # StringMeasurement, MultiStringMeasurement
│   │
│   ├── numeric_step.py          # NumericStep, MultiNumericStep
│   ├── boolean_step.py          # BooleanStep, MultiBooleanStep
│   ├── string_step.py           # StringStep, MultiStringStep
│   ├── chart_step.py            # ChartStep
│   ├── generic_step.py          # GenericStep, FlowType
│   ├── action_step.py           # ActionStep
│   ├── callexe_step.py          # CallExeStep
│   ├── message_popup_step.py    # MessagePopUpStep
│   └── unknown_step.py          # UnknownStep (fallback)
│
└── C#/                          # Reference C# code (unchanged)
```

---

## 7. What Changes for Users (Surface Diff)

### 7.1 No Change Required

| Feature | Status |
|---------|--------|
| `UUTReport(pn=..., sn=..., ...)` constructor | ✅ Same |
| `report.get_root_sequence_call()` | ✅ Same |
| `root.add_numeric_step(...)` | ✅ Same |
| `root.add_sequence_call(...)` | ✅ Same |
| `root.add_boolean_step(...)` | ✅ Same |
| `root.add_string_step(...)` | ✅ Same |
| `root.add_chart_step(...)` | ✅ Same |
| `root.add_generic_step(...)` | ✅ Same |
| `report.add_misc_info(...)` | ✅ Same |
| `report.add_sub_unit(...)` | ✅ Same |
| JSON output format | ✅ Identical |

### 7.2 Import Path Change

```python
# v1
from pywats.domains.report.report_models import UUTReport

# v3
from pywats.domains.report.report_models_v3 import UUTReport
```

### 7.3 Optional C# Aliases (New)

```python
# v3 adds these aliases
from pywats.domains.report.report_models_v3 import (
    PassFailStep,        # alias for BooleanStep
    StringValueStep,     # alias for StringStep
)
```

### 7.4 Info Access Clarification

```python
# Both work in v1 and v3:
report.info.operator  # ✅ Preferred

# v1 had confusion because field serializes as "uut":
# JSON: {"uut": {"user": "John"}}
# But Python: report.info.operator

# v3 documents this clearly - no code change needed
```

---

## 8. Strengths of v3 Design

1. **Proper inheritance** - Report base has all common fields, no duplication
2. **StepList preserved** - The elegant polymorphic container stays intact
3. **Clean info access** - `report.info.operator` not `report.uut.operator`
4. **SubUnit hierarchy** - UURSubUnit properly inherits from SubUnit
5. **Shared serialization** - Mixin extracts repeated wrap/unwrap logic
6. **C# aliases** - Users can use familiar C# names if preferred
7. **100% JSON compatible** - Output format unchanged
8. **Minimal migration** - Only import path changes for most users

---

## 9. Potential Weaknesses

1. **Still 6 step classes** - Could be unified, but that changes stepType semantics
2. **SubUnit type override** - Needs `# type: ignore` for mypy
3. **Mixin complexity** - Adds one more concept to understand
4. **Coexistence period** - v1 and v3 both exist during transition

---

## 10. Implementation Priority

### Phase 1: Foundation (Critical)
1. `WATSBase` - Copy from v1
2. `Report` base class with all fields
3. `ReportInfo` base class
4. `SubUnit` base class

### Phase 2: Reports
1. `UUTInfo(ReportInfo)`
2. `UUTReport(Report)`
3. `UURInfo(ReportInfo)`
4. `UURSubUnit(SubUnit)`, `UURFailure`
5. `UURReport(Report)`

### Phase 3: Steps (Critical)
1. `Step` abstract base
2. `StepList` - Copy from v1
3. `Measurement` hierarchy
4. `SequenceCall` with factory methods
5. All step types with mixins

### Phase 4: Validation
1. JSON round-trip tests vs v1
2. Factory method behavior tests
3. StepList parent injection tests
4. Type checker (mypy/pyright) validation

### Phase 5: Integration
1. Update service layer to support v3
2. Migration guide finalization
3. C# alias documentation
