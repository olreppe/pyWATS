# Report Models - Version Comparison Analysis

**Created:** January 30, 2026  
**Purpose:** Compare v1, v2, and v3 implementations with pros and cons

---

## Executive Summary

| Aspect | v1 | v2 | v3 |
|--------|----|----|----| 
| **Status** | Current/Production | Abandoned | Proposed |
| **Report Pattern** | Inheritance ✓ | Composition + Mixin | Inheritance (Refined) ✓ |
| **Step Pattern** | Separate Single/Multi | Imports v1 steps | Separate + Shared Mixin |
| **StepList** | Custom polymorphic list ✓ | Imports v1 | Preserved exactly ✓ |
| **Info Access** | `info` field → `uut` JSON | Same | Same (documented better) |
| **SubUnit** | Separate classes | Same | Proper inheritance |
| **Maintainability** | Medium | Low | High |
| **C# Alignment** | Good | Same | Better (aliases) |

**v3 Philosophy:** "Fix the bugs, not the architecture."

---

## 1. Version 1 (Current - `report_models/`)

### Description
The current production implementation. Inheritance-based with proper base classes.

### Architecture Pattern
- **`Report` base class** contains ALL common fields (correct!)
- **`UUTReport`/`UURReport`** inherit and specialize
- **`ReportInfo` base class** with `UUTInfo`/`UURInfo` inheriting
- **`StepList`** - Polymorphic container with parent injection (elegant!)
- **Discriminated Union** for step type resolution

```
Report (base - all common fields)
├── UUTReport (adds root: SequenceCall, info: UUTInfo)
└── UURReport (adds info: UURInfo, overrides sub_units)

ReportInfo (base)
├── UUTInfo (fixture, batch, socket)
└── UURInfo (repair codes, ref_uut)

Step (abstract base)
├── SequenceCall (container + factories)
├── NumericStep / MultiNumericStep
├── BooleanStep / MultiBooleanStep
├── StringStep / MultiStringStep
├── ChartStep, GenericStep, ActionStep, ...
```

### ✅ What v1 Does RIGHT (Preserve These)

| Pattern | Description | v3 Action |
|---------|-------------|-----------|
| **Report Inheritance** | Base class with all common fields | ✅ Keep |
| **StepList** | Polymorphic list with parent injection | ✅ Keep exactly |
| **Factory Methods** | `add_numeric_step()` etc. on SequenceCall | ✅ Keep |
| **Step Discriminator** | `_discriminate_step_type()` function | ✅ Keep |
| **ReportInfo Hierarchy** | Base with UUT/UUR specializations | ✅ Keep |
| **Measurement Hierarchy** | BooleanMeasurement → LimitMeasurement | ✅ Keep |
| **Parent Tracking** | `step.parent` for hierarchy traversal | ✅ Keep |

### ❌ What v1 Does WRONG (Fix These)

| Issue | Description | v3 Fix |
|-------|-------------|--------|
| **6 Step Classes** | NumericStep + MultiNumericStep duplicated logic | Extract `SingleMeasurementMixin` |
| **Repeated Validators** | `unpack_measurement` in every single step class | Share via mixin |
| **Repeated Serializers** | `serialize_measurement` in every single step class | Share via mixin |
| **SubUnit Hierarchy** | `UURSubUnit` doesn't properly inherit `SubUnit` | Fix inheritance |
| **Naming Confusion** | `BooleanStep` vs C#'s `PassFailStep` | Add C# aliases |
| **Info Confusion** | `info` field serializes as `uut` - undocumented | Document clearly |

### Code Example (v1)
```python
from pywats.domains.report.report_models import UUTReport

report = UUTReport(pn="ABC", sn="001", rev="A", process_code=100,
                   station_name="Sta1", location="Lab", purpose="Dev")
root = report.get_root_sequence_call()

# Single measurement - works great
root.add_numeric_step(name="Voltage", value=5.0, unit="V", comp_op=CompOp.GELE,
                      low_limit=4.5, high_limit=5.5)

# Multi measurement - different class, same factory pattern
multi = root.add_multi_numeric_step(name="MultiTest")
multi.add_measurement(name="M1", value=1.0, unit="V")
multi.add_measurement(name="M2", value=2.0, unit="V")

# Info access - works but undocumented
report.info.operator = "John"  # info field
# JSON: {"uut": {"user": "John"}}  # serializes as "uut"
```

---

## 2. Version 2 (Abandoned - `report_models_v2/`)

### Description
An attempt to fix v1 using composition with a proxy mixin. **Abandoned because it created more problems than it solved.**

### Architecture Pattern
- **Composition** for reports (`common: ReportCommon`)
- **Mixin** for flat API access (`ReportProxyMixin` - 276 lines!)
- **Imports v1 steps** (didn't address the real issues)

```
UUTReport
├── common: ReportCommon (attempted to isolate shared fields)
├── type: "T"
├── root: SequenceCall
└── (inherits ReportProxyMixin - 70+ property proxies!)
```

### ✅ Pros

| Pro | Why It Seemed Good |
|-----|-------------------|
| Isolated common fields | ReportCommon as single source |
| v1-compatible constructor | Model validator wrapped flat args |

### ❌ Cons (Why Abandoned)

| Con | Why It Failed |
|-----|---------------|
| **276 lines of proxies** | Every field needs getter+setter proxy |
| **Type checker confusion** | Mixin + Pydantic = mypy/pyright errors |
| **Didn't fix real problem** | Steps still had duplicated serialization |
| **Visible indirection** | `report.common.pn` exposed to users |
| **Maintenance nightmare** | New field = update 3 places |
| **Never completed** | Test failures, abandoned |

### Code Example (v2 - shows the problem)
```python
class ReportProxyMixin:
    """276 lines of this pattern repeated..."""
    
    @property
    def pn(self) -> str:
        return self.common.pn
    
    @pn.setter
    def pn(self, value: str) -> None:
        self.common.pn = value
    
    @property
    def sn(self) -> str:
        return self.common.sn
    
    @sn.setter
    def sn(self, value: str) -> None:
        self.common.sn = value
    
    # ... 70+ more properties ...
```

**Verdict:** Wrong solution to wrong problem. v1's inheritance IS correct.

---

## 3. Version 3 (Proposed - `report_models_v3/`)

### Description
**Refined v1** - Keep what works, fix what's broken. No architectural rewrites.

### Architecture Pattern
- **Keep `Report` inheritance** (it's correct!)
- **Keep `StepList`** exactly as-is (it's elegant!)
- **Keep `ReportInfo` hierarchy** (it's correct!)
- **Add `SingleMeasurementMixin`** to reduce code duplication
- **Fix `UURSubUnit` inheritance** from `SubUnit`
- **Add C# name aliases** for discoverability
- **Document info/JSON naming** clearly

```
Report (base - ALL common fields) ✓ UNCHANGED
├── UUTReport (root, info→uut) ✓ UNCHANGED  
└── UURReport (info→uur, uur_sub_units) ✓ UNCHANGED

ReportInfo (base) ✓ UNCHANGED
├── UUTInfo ✓ UNCHANGED
└── UURInfo ✓ UNCHANGED

SubUnit (base) ✓ UNCHANGED
└── UURSubUnit (idx, failures) ← NOW PROPERLY INHERITS

Step (abstract base) ✓ UNCHANGED
├── SequenceCall ✓ UNCHANGED
├── NumericStep ← + SingleMeasurementMixin (shared logic)
├── MultiNumericStep ✓ UNCHANGED
├── BooleanStep (alias: PassFailStep) ← + C# alias
├── MultiBooleanStep (alias: MultiPassFailStep)
├── StringStep (alias: StringValueStep)
├── MultiStringStep (alias: MultiStringValueStep)
└── ... other steps unchanged
```

### ✅ Pros

| Pro | Description |
|-----|-------------|
| **Preserves v1's elegance** | StepList, inheritance, factory methods all intact |
| **Fixes real issues** | Mixin extracts duplicated serialization code |
| **Proper SubUnit hierarchy** | UURSubUnit correctly inherits SubUnit |
| **C# discoverability** | `PassFailStep` alias for `BooleanStep` |
| **Documented naming** | `report.info` in code, `"uut"` in JSON - clear |
| **Minimal migration** | Import path change only for most users |
| **100% JSON compatible** | Output format unchanged |

### ❌ Cons

| Con | Description |
|-----|-------------|
| **Still 6 step classes** | But with shared logic via mixin |
| **One more concept** | SingleMeasurementMixin to understand |
| **Coexistence period** | v1 and v3 both exist during transition |

### Code Example (v3)
```python
from pywats.domains.report.report_models_v3 import (
    UUTReport,
    PassFailStep,       # C# alias for BooleanStep
    StringValueStep,    # C# alias for StringStep
)

report = UUTReport(pn="ABC", sn="001", rev="A", process_code=100,
                   station_name="Sta1", location="Lab", purpose="Dev")
root = report.get_root_sequence_call()

# EXACTLY THE SAME AS v1 - no changes needed!
root.add_numeric_step(name="Voltage", value=5.0, unit="V", comp_op=CompOp.GELE,
                      low_limit=4.5, high_limit=5.5)

# Multi measurement - same pattern
multi = root.add_multi_numeric_step(name="MultiTest")
multi.add_measurement(name="M1", value=1.0, unit="V")
multi.add_measurement(name="M2", value=2.0, unit="V")

# Info access - now documented clearly!
report.info.operator = "John"  # Python: report.info
# JSON output: {"uut": {"user": "John"}}  # Serializes as "uut" ✓
```

---

## 4. Side-by-Side Comparison

### 4.1 Report Layer

| Aspect | v1 | v2 | v3 |
|--------|----|----|----| 
| Base class | `Report` ✓ | Composition | `Report` ✓ |
| Common fields | In base ✓ | In `ReportCommon` | In base ✓ |
| Field access | Flat ✓ | Flat via mixin | Flat ✓ |
| Maintenance | Low | High | Low |

### 4.2 StepList

| Aspect | v1 | v2 | v3 |
|--------|----|----|----| 
| Implementation | Custom polymorphic list | Imports v1 | **Exactly same** |
| Parent injection | Automatic ✓ | Same | Same ✓ |
| Type resolution | Via StepType Union | Same | Same ✓ |

### 4.3 Step Classes

| Aspect | v1 | v2 | v3 |
|--------|----|----|----| 
| Single/Multi separate | Yes (6 classes) | Same | Yes (but shared mixin) |
| Serialization code | Duplicated 3x | Same | Shared via mixin |
| C# naming | No aliases | No aliases | Aliases added |

### 4.4 Info Classes

| Aspect | v1 | v2 | v3 |
|--------|----|----|----| 
| Access pattern | `report.info.x` | Same | Same |
| JSON serialization | `"uut"` / `"uur"` | Same | Same |
| Documentation | Unclear | Same | **Clear** |

### 4.5 SubUnit

| Aspect | v1 | v2 | v3 |
|--------|----|----|----| 
| `SubUnit` | Base class | Same | Same |
| `UURSubUnit` | Separate (no inherit) | Same | **Inherits SubUnit** |
| Type safety | `# type: ignore` | Same | Proper |

---

## 5. Migration Impact Analysis

### From v1 to v3

| Change Type | Impact | Effort |
|-------------|--------|--------|
| Import path | Must change | Search/replace |
| Report creation | **No change** | Zero |
| Factory methods | **No change** | Zero |
| Step construction | **No change** | Zero |
| Info access | **No change** | Zero |
| JSON output | **Identical** | Zero |
| C# aliases | Optional | Zero (additive) |

### Estimated Migration Time

| Codebase Size | Time |
|---------------|------|
| Small (<1000 LOC) | 5 minutes |
| Medium (1-10K LOC) | 30 minutes |
| Large (>10K LOC) | 1-2 hours |

---

## 6. Recommendation

### Use v3 Because:

1. **It's v1, but better** - Not a rewrite, a refinement
2. **Keeps what works** - StepList, inheritance, factories all intact
3. **Fixes what's broken** - Shared mixin, proper SubUnit inheritance
4. **Adds discoverability** - C# aliases for familiar names
5. **Documents clearly** - Info/JSON naming confusion resolved
6. **Minimal migration** - Import path change only

### Don't Use v2 Because:

1. **Abandoned** - Never completed, has test failures
2. **Wrong approach** - Composition + mixin added complexity
3. **276 lines of proxies** - Maintenance nightmare
4. **Type checker issues** - Mixin confuses mypy/pyright

---

## 7. Detailed Class Comparison

| Class | v1 | v2 | v3 |
|-------|----|----|----| 
| `Report` | Base with all fields | Replaced with composition | **Same as v1** |
| `UUTReport` | Inherits Report | Has `common: ReportCommon` | **Same as v1** |
| `UURReport` | Inherits Report | Has `common: ReportCommon` | **Same as v1** |
| `ReportInfo` | Base class | Same | **Same as v1** |
| `UUTInfo` | Inherits ReportInfo | Same | **Same as v1** |
| `UURInfo` | Inherits ReportInfo | Same | **Same as v1** |
| `SubUnit` | Standalone | Same | **Same as v1** |
| `UURSubUnit` | Standalone (no inherit) | Same | **Inherits SubUnit** |
| `StepList` | Polymorphic container | Imports v1 | **Same as v1** |
| `Step` | Abstract base | Imports v1 | **Same as v1** |
| `NumericStep` | Has unpack/serialize | Imports v1 | **+ Shared mixin** |
| `BooleanStep` | Has unpack/serialize | Imports v1 | **+ Shared mixin + alias** |
| `StringStep` | Has unpack/serialize | Imports v1 | **+ Shared mixin + alias** |
