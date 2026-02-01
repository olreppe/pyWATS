# ImportMode Specification

## Overview

This document specifies the `ImportMode` feature for the pyWATS Report domain. ImportMode controls how UUT reports behave when creating and modifying test data - specifically around automatic status calculation and failure propagation.

## ImportMode Enum

```
ImportMode.Import   - Passive mode, no automatic behaviors (DEFAULT)
ImportMode.Active   - Active mode, enables automatic status calculation and failure propagation
```

## Configuration

The ImportMode setting is a property of the Report module/repository object.

**Syntax:**
```python
from pywats import WATSClient
from pywats.domains.report import ImportMode

api = WATSClient(...)
api.report.import_mode = ImportMode.Import  # Default
api.report.import_mode = ImportMode.Active  # Enable active behaviors
```

**Default:** `ImportMode.Import`

---

## Step Properties

### `fail_parent_on_failure`

- **Location:** Property on the `Step` base class (applies to ALL step types)
- **Type:** `bool`
- **Default:** `True`
- **Description:** When `True` and the step status is set to `Failed` in Active mode, the failure will propagate up the step hierarchy.

---

## Behavior by Mode

### ImportMode.Import (Default)

In Import mode, no automatic behaviors are applied:

- Step status values are stored exactly as provided
- No automatic status calculation for measurements
- No failure propagation regardless of `fail_parent_on_failure` setting
- Useful for importing historical data or data from external systems where status has already been determined

### ImportMode.Active

In Active mode, the following automatic behaviors are enabled:

#### 1. Default Step Status

- All steps default to `status = "P"` (Passed) if not explicitly set
- This applies when a step is created without specifying a status

#### 2. Failure Propagation

When a step's status is set to `"F"` (Failed):

1. Check the step's `fail_parent_on_failure` property
2. If `True`:
   - Find the parent step (SequenceCall containing this step)
   - Set the parent's status to `"F"` (Failed)
   - Recursively check the parent's `fail_parent_on_failure`
   - Continue propagation until:
     - A step with `fail_parent_on_failure = False` is reached, OR
     - The root level (UUTReport) is reached
3. If propagation reaches the root level, set `UUTReport.result` to `"F"` (Failed)

**Propagation Chain Example:**
```
UUTReport (result)
  └── MainSequence (SequenceCall)
        └── TestGroup (SequenceCall)
              └── MeasurementStep (status = "F", fail_parent_on_failure = True)
                    ↑ Failure set here
                    
Propagation: MeasurementStep → TestGroup → MainSequence → UUTReport.result
```

#### 3. Measurement Auto-Status Calculation

For measurement steps that have:
- A `value` (measured value)
- A `comp` (comparison operator)
- Limits (`low_limit` and/or `high_limit`)

The status will be **automatically calculated** based on the comparison, **unless status is explicitly set**.

**Supported Comparisons:**

Uses the existing `CompOp` enum from `pywats.domains.report.report_models.uut.steps.comp_operator`.

| Comparison | Symbol | Pass Condition |
|------------|--------|----------------|
| `EQ` | `==` | `value == low_limit` |
| `NE` | `!=` | `value != low_limit` |
| `GT` | `>` | `value > low_limit` |
| `LT` | `<` | `value < low_limit` |
| `GE` | `>=` | `value >= low_limit` |
| `LE` | `<=` | `value <= low_limit` |
| `GTLT` | `><` | `value > low_limit AND value < high_limit` |
| `GELE` | `>=<=` | `value >= low_limit AND value <= high_limit` |
| `GELT` | `>=<` | `value >= low_limit AND value < high_limit` |
| `GTLE` | `><=` | `value > low_limit AND value <= high_limit` |
| `LTGT` | `<>` | `value < low_limit OR value > high_limit` |
| `LEGE` | `<=>=` | `value <= low_limit OR value >= high_limit` |
| `LEGT` | `<=>` | `value <= low_limit OR value > high_limit` |
| `LTGE` | `<>=` | `value < low_limit OR value >= high_limit` |
| `LOG` | - | No comparison. Always passes. |

**Note:** String comparisons (`CASESENSIT`, `IGNORECASE`, `EQT`) are not auto-calculated.

**Auto-calculation rules:**
1. Only triggers when `status` is not explicitly provided
2. Only triggers in `ImportMode.Active`
3. If comparison passes → `status = "P"`
4. If comparison fails → `status = "F"` (which then triggers propagation if `fail_parent_on_failure = True`)
5. If required values are missing (e.g., no limits for GELE), status remains unset or defaults to Passed

---

## Summary Table

| Feature | ImportMode.Import | ImportMode.Active |
|---------|-------------------|-------------------|
| Default step status | None (as provided) | `"P"` (Passed) |
| Failure propagation | Disabled | Enabled (when `fail_parent_on_failure = True`) |
| Measurement auto-status | Disabled | Enabled (when limits/comp defined) |
| `fail_parent_on_failure` effect | None | Controls propagation |

---

## Future Considerations

- Default mode may change from `Import` to `Active` in future versions
- Additional propagation rules may be added (e.g., warning propagation)
- Batch mode for setting multiple step statuses with single propagation pass
