# UUTReport Step Graph Model

## Overview

The UUTReport step graph model is a hierarchical structure for representing test execution sequences in the pyWATS testing system. It consists of a tree of Step objects organized under a root SequenceCall.

## Core Components

### 1. UUTReport
- The main report class for Unit Under Test (UUT) reports
- Has a `root` field containing a `SequenceCall` object
- Access via `report.get_root_sequence_call()`

### 2. SequenceCall
- A special Step type that can contain child steps
- Implements both `Step` interface and acts as a container
- Can be nested recursively to create multi-level test hierarchies
- Has a `steps` field containing a `StepList` of child steps
- Identified by `step_type: "SequenceCall"` or `"WATS_SeqCall"`

### 3. StepList
- Custom list class that extends Python's `list`
- Can hold any type of Step (NumericStep, BooleanStep, SequenceCall, etc.)
- Maintains parent references for all contained steps
- Supports standard list operations (append, extend, insert, etc.)
- Automatically sets parent reference when steps are added

### 4. Step (Abstract Base Class)
- Base class for all step types
- All steps have a `step_type` field (string literal) that identifies their type
- Common fields:
  - `name`: Step name (string)
  - `status`: Step status (StepStatus enum: Passed, Failed, Skipped, etc.)
  - `group`: Step group ("M", "S", or "C")
  - `parent`: Reference to parent SequenceCall (excluded from serialization)

## Step Types

### Identified by String Literals

Each step type is identified by its `step_type` field value:

| Step Class | step_type Values | Description |
|------------|------------------|-------------|
| NumericStep | "ET_NLT", "NumericLimitStep" | Single numeric measurement |
| MultiNumericStep | "ET_MNLT" | Multiple numeric measurements |
| BooleanStep | "ET_PFT", "PassFailTest" | Single boolean/pass-fail test |
| MultiBooleanStep | "ET_MPFT" | Multiple boolean tests |
| StringStep | "ET_SVT" | Single string value |
| MultiStringStep | "ET_MSVT" | Multiple string values |
| SequenceCall | "SequenceCall", "WATS_SeqCall" | Container for nested steps |
| ActionStep | "Action" | Action/procedure step |
| ChartStep | "WATS_XYGMNLT" | Chart/graph data |
| GenericStep | Various "NI_*" values | Generic/flow control steps |
| CallExeStep | "CallExecutable" | External executable call |
| MessagePopUpStep | "MessagePopup" | Message popup dialog |

## Single vs Multi Measurement Types

### Single Measurement Steps
- **Numeric, Boolean, and String steps have single-measurement variants**
- Single steps have ONE measurement with NO name required
- The measurement is stored in a `measurement` field (singular)
- Example:
  ```python
  numeric_step = root.add_numeric_step(
      name="VoltageTest",
      value=3.3,
      unit="V",
      status="P"
  )
  # numeric_step.measurement has no 'name' attribute
  ```

### Multi Measurement Steps
- **Numeric, Boolean, and String steps have multi-measurement variants**
- Multi steps have ONE OR MORE measurements, ALL with REQUIRED names
- The measurements are stored in a `measurements` field (plural, list)
- Example:
  ```python
  multi_numeric = root.add_multi_numeric_step(name="PowerTests", status="P")
  multi_numeric.add_measurement(name="Voltage", value=3.3, unit="V")
  multi_numeric.add_measurement(name="Current", value=1.2, unit="A")
  # Each measurement in multi_numeric.measurements has a 'name' attribute
  ```

### Comparison Table

| Aspect | Single Step | Multi Step |
|--------|-------------|------------|
| Field name | `measurement` | `measurements` |
| Field type | Single object | List of objects |
| Measurement name | Not present | Required for each |
| Use case | One test per step | Multiple related tests per step |

## Nested Structure Example

```python
from pyWATS.domains.report.report_models.uut.uut_report import UUTReport
from datetime import datetime

# Create report
report = UUTReport(
    pn="PROD-001", sn="SN-12345", rev="A",
    process_code=10, station_name="Station1",
    location="Lab", purpose="Testing",
    result="P", start=datetime.now().astimezone()
)

# Get root sequence
root = report.get_root_sequence_call()  # Returns SequenceCall

# Add steps directly to root
root.add_numeric_step(name="Test1", value=1.5, unit="V", status="P")
root.add_boolean_step(name="Test2", status="P")

# Create nested sequence
power_tests = root.add_sequence_call(
    name="PowerTests",
    file_name="power.seq",
    version="1.0.0"
)

# Add steps to nested sequence
power_tests.add_numeric_step(name="3V3Rail", value=3.3, unit="V", status="P")
power_tests.add_numeric_step(name="5VRail", value=5.0, unit="V", status="P")

# Even deeper nesting
calibration = power_tests.add_sequence_call(
    name="Calibration",
    file_name="cal.seq"
)
calibration.add_numeric_step(name="CalTest", value=1.0, unit="V", status="P")
```

**Resulting hierarchy:**
```
Root (SequenceCall)
├── Test1 (NumericStep)
├── Test2 (BooleanStep)
└── PowerTests (SequenceCall)
    ├── 3V3Rail (NumericStep)
    ├── 5VRail (NumericStep)
    └── Calibration (SequenceCall)
        └── CalTest (NumericStep)
```

## JSON Serialization

The step graph fully supports JSON serialization and deserialization:

```python
# Serialize
json_data = report.model_dump_json(by_alias=True, exclude_none=True)

# Deserialize
report2 = UUTReport.model_validate_json(json_data)
root2 = report2.get_root_sequence_call()
```

### Discriminator

The step graph uses Pydantic v2's discriminated union feature for efficient deserialization:
- The `step_type` field acts as the discriminator
- Pydantic automatically selects the correct Step subclass based on `step_type` value
- This makes deserialization fast and type-safe

## Parent References

All steps maintain a reference to their parent SequenceCall:

```python
step = power_tests.add_numeric_step(name="Test", value=1.0, status="P")
print(step.parent.name)  # Prints "PowerTests"
```

**Important Notes:**
- Parent references are automatically set by StepList
- Parent field is excluded from JSON serialization (`exclude=True`)
- Parent references are re-established during deserialization
- The root SequenceCall has `parent=None`

## Helper Methods

### SequenceCall.print_hierarchy()
Recursively prints the step hierarchy with indentation:

```python
root.print_hierarchy()
```

Output:
```
- SequenceCall: MainSequence Callback (Parent: None)
    - NumericStep: Test1 (Parent: MainSequence Callback)
    - SequenceCall: PowerTests (Parent: MainSequence Callback)
        - NumericStep: 3V3Rail (Parent: PowerTests)
```

### Adding Steps

SequenceCall provides helper methods for adding different step types:

```python
# Single measurement steps
root.add_numeric_step(name, value, unit, status, comp_op, low_limit, high_limit, ...)
root.add_boolean_step(name, status, ...)
root.add_string_step(name, value, status, ...)

# Multi measurement steps
multi_num = root.add_multi_numeric_step(name, status, ...)
multi_num.add_measurement(name, value, unit, status, comp_op, ...)

multi_bool = root.add_multi_boolean_step(name, status, ...)
multi_bool.add_measurement(name, status)

multi_str = root.add_multi_string_step(name, status, ...)
multi_str.add_measurement(name, value, status, comp_op, ...)

# Nested sequences
sub_seq = root.add_sequence_call(name, file_name, version, path)

# Other step types
root.add_chart_step(name, chart_type, label, x_label, y_label, ...)
root.add_generic_step(step_type, name, status, ...)
```

## Technical Implementation Notes

### Pydantic v2 Discriminator
- Base `Step.step_type` field is defined as `str` to allow subclasses to override with specific Literal values
- Each concrete step class defines `step_type` as a Literal with specific values
- StepList's `__get_pydantic_core_schema__` method preserves discriminator annotations
- This enables fast, type-safe deserialization without trying all union members

### Field Aliases
- Python field names use snake_case (e.g., `step_type`, `error_code`)
- JSON uses camelCase (e.g., `stepType`, `errorCode`)
- Controlled via `validation_alias` and `serialization_alias` parameters

### Model Validators
- SequenceCall uses an `@model_validator(mode="after")` to convert lists to StepList
- This runs AFTER Pydantic validates individual steps using the discriminator
- Parent references are set after deserialization completes

## Best Practices

1. **Always use helper methods** to add steps (`add_numeric_step()`, etc.)
2. **Multi-step measurements must have names** - the helper methods enforce this
3. **Use appropriate step types** - Single for one measurement, Multi for multiple
4. **Leverage nesting** - Group related tests in nested SequenceCall objects
5. **Check parent references** - Available for navigating up the hierarchy
6. **Use print_hierarchy()** - Useful for debugging step structure

## Migration Notes

If upgrading from an older version:
- MultiBooleanStep no longer inherits from BooleanStep (avoids field conflicts)
- Base Step.step_type changed from Literal to str (enables discriminator)
- StepList's __get_pydantic_core_schema__ preserves discriminator (fixes deserialization)
- Remove any "before" validators that convert steps to StepList (interferes with discriminator)
