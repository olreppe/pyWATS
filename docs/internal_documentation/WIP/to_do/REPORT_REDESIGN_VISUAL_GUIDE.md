# Report Model Architecture - Visual Guide

**Quick visual reference for report model structure and relationships**

---

## Current Architecture (v1) - Inheritance-Based

```
┌─────────────────────────────────────────────────────────────┐
│                     Report (Base Class)                     │
│ ─────────────────────────────────────────────────────────── │
│ + id: UUID                                                   │
│ + type: str  ("T" or "R")                                   │
│ + pn, sn, rev: str                                          │
│ + process_code: int                                         │
│ + station_name, location, purpose: str                      │
│ + start, start_utc: datetime                                │
│ + result: str                                               │
│ + misc_infos: Optional[list[MiscInfo]]  ← Anti-pattern!     │
│ + sub_units: Optional[list[SubUnit]]    ← Anti-pattern!     │
│ + assets: Optional[list[Asset]]         ← Anti-pattern!     │
└─────────────────────────────────────────────────────────────┘
                             △
                             │
                  ┌──────────┴──────────┐
                  │                     │
        ┌─────────┴─────────┐ ┌────────┴─────────┐
        │    UUTReport      │ │   UURReport      │
        │ ───────────────── │ │ ──────────────── │
        │ type: Literal["T"]│ │ type: Literal["R"]│ ← Type override!
        │ root: SequenceCall│ │ info: UURInfo    │
        │ info: UUTInfo     │ │ sub_units: list  │ ← Field override!
        └───────────────────┘ └──────────────────┘
                │
                │
        ┌───────┴───────┐
        │ SequenceCall  │
        │ ───────────── │
        │ steps: StepList[StepType]  ← Discriminated Union!
        └───────────────┘
                │
                │
        ┌───────┴────────────────────────────────────────┐
        │         StepType (Discriminated Union)         │
        │ ──────────────────────────────────────────── │
        │  NumericStep | StringStep | BooleanStep      │
        │  MultiNumericStep | MultiStringStep          │
        │  ChartStep | ActionStep | GenericStep        │
        │  SequenceCall (recursive!)                   │
        └───────────────────────────────────────────────┘
```

**Problems:**
- ❌ Type override conflicts (`type: str` → `type: Literal["T"]`)
- ❌ Field override issues (`Optional[list[SubUnit]]` → `list[UURSubUnit]`)
- ❌ Optional[list] with default_factory (never actually None)
- ❌ Inheritance complexity (Liskov violations)

---

## Proposed Architecture (v2) - Composition-Based

```
┌─────────────────────────────────────────────────────────────┐
│                   ReportCommon (Composition)                │
│ ─────────────────────────────────────────────────────────── │
│ + id: UUID                                                   │
│ + pn, sn, rev: str                                          │
│ + process_code: int                                         │
│ + station_name, location, purpose: str                      │
│ + start, start_utc: datetime                                │
│ + result: str                                               │
│ + misc_infos: list[MiscInfo]        ← Clean pattern!       │
│ + sub_units: list[SubUnit]          ← Never None!          │
│ + assets: list[Asset]               ← Always list!          │
└─────────────────────────────────────────────────────────────┘
                             ◇  (Composed by)
                             │
                  ┌──────────┴──────────┐
                  │                     │
        ┌─────────┴─────────┐ ┌────────┴─────────┐
        │    UUTReport      │ │   UURReport      │
        │ ───────────────── │ │ ──────────────── │
        │ common: ReportCmn │ │ common: ReportCmn│ ← Composition!
        │ type: Literal["T"]│ │ type: Literal["R"]│ ← No override!
        │ root: SequenceCall│ │ info: UURInfo    │
        │ info: UUTInfo     │ │ sub_units: list  │ ← Additional field
        └───────────────────┘ └──────────────────┘
                │                       │
                └───────────┬───────────┘
                            │
                     ┌──────┴───────┐
                     │ Report Union │
                     │ ──────────── │
                     │ UUTReport |  │
                     │ UURReport    │
                     └──────────────┘
```

**Benefits:**
- ✅ No type conflicts (composition instead of inheritance)
- ✅ Clean list types (never Optional with default_factory)
- ✅ Discriminated union for parsing
- ✅ Liskov principle satisfied (no overrides)

---

## Directory Structure - Side by Side

```
src/pywats/domains/report/
│
├── models.py                         ⚠️ QUERY MODELS - NOT INVOLVED
│   ├── WATSFilter                    (Query builder)
│   ├── ReportHeader                  (Response model)
│   └── HeaderMiscInfo, etc.          (Query-related)
│
├── report_models/                    ← v1 STRUCTURE (inheritance)
│   │
│   ├── report.py                     ← Base class (REPLACE with composition)
│   ├── misc_info.py                  ← Import to v2
│   ├── asset.py                      ← Import to v2
│   ├── sub_unit.py                   ← Import to v2
│   │
│   ├── uut/
│   │   ├── uut_report.py             ← Inheritance-based
│   │   ├── uut_info.py               ← Import to v2
│   │   └── steps/                    ⚠️ IMPORT TO v2 (DON'T COPY!)
│   │       ├── step.py               (Already has discriminated union)
│   │       ├── sequence_call.py      (StepList parent injection)
│   │       ├── numeric_step.py
│   │       └── ...
│   │
│   └── uur/
│       ├── uur_report.py             ← Inheritance-based
│       ├── uur_info.py               ← Import to v2
│       └── uur_sub_unit.py           ← Import to v2
│
└── report_models_v2/                 ← v2 STRUCTURE (composition)
    │
    ├── __init__.py                   ← Feature flag exports
    │
    ├── report_common.py              ⭐ NEW: Composition model
    ├── uut_report.py                 ⭐ NEW: Composition-based
    ├── uur_report.py                 ⭐ NEW: Composition-based
    ├── report_union.py               ⭐ NEW: Discriminated union
    │
    └── shared/                       ← Imports or symlinks
        ├── misc_info.py  ──────────────► from ..report_models.misc_info
        ├── asset.py      ──────────────► from ..report_models.asset
        └── steps/        ──────────────► from ..report_models.uut.steps
```

---

## Parent Injection Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User creates report                                       │
│    report = UUTReport(pn="123", sn="456", ...)              │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. User gets root sequence                                   │
│    root = report.get_root_sequence_call()                   │
│    # Returns SequenceCall with StepList                     │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. User adds step via factory method                         │
│    step = root.add_numeric_step(name="V", value=3.3)        │
│                                                              │
│    Inside add_numeric_step():                               │
│    ┌────────────────────────────────────────────┐          │
│    │ ns = NumericStep(...)  # parent NOT set    │          │
│    │ self.steps.append(ns)  # ← INJECTION HERE! │          │
│    └────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. StepList.append() injects parent                          │
│                                                              │
│    class StepList(List[StepType]):                          │
│        def append(self, item):                              │
│            if hasattr(item, "parent"):                      │
│                item.parent = self.parent  # ← HERE!         │
│            super().append(item)                             │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Parent reference established                              │
│    step.parent == root  ✓                                   │
│                                                              │
│    Failure propagation works:                               │
│    if step.status == "F" and step.fail_parent_on_failure:  │
│        step.parent.status = "F"  # Propagate up!           │
└─────────────────────────────────────────────────────────────┘
```

**Key insight:** Parent is NOT a constructor parameter!

---

## Service Layer Integration

```
┌──────────────────────────────────────────────────────────────┐
│                   AsyncReportService                         │
│ ──────────────────────────────────────────────────────────── │
│                                                               │
│  Feature Flag Check:                                         │
│  ┌────────────────────────────────────────────┐             │
│  │ if USE_REPORT_V2:                          │             │
│  │     from .report_models_v2 import UUTReport│             │
│  │ else:                                      │             │
│  │     from .report_models import UUTReport   │             │
│  └────────────────────────────────────────────┘             │
│                                                               │
│  Factory Methods:                                            │
│  ┌────────────────────────────────────────────┐             │
│  │ def create_uut_report(pn, sn, process_code)│             │
│  │     # Station resolution                   │             │
│  │     # Defaults handling                    │             │
│  │     return UUTReport(...)                  │             │
│  └────────────────────────────────────────────┘             │
│                                                               │
│  Imports from report_models:                                 │
│  - UUTReport, UURReport (concrete classes)                   │
│  - UUTInfo, UURInfo (info models)                           │
│  - UURSubUnit (repair-specific)                             │
│                                                               │
│  Does NOT import:                                            │
│  - Report base class (not used)                             │
│  - Step classes (internal to reports)                       │
└──────────────────────────────────────────────────────────────┘
```

---

## Constructor vs Factory Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                  PATTERN 1: Factory                          │
│ ──────────────────────────────────────────────────────────── │
│                                                               │
│  service = AsyncReportService(repository)                    │
│  report = service.create_uut_report(                         │
│      pn="ABC123",                                            │
│      sn="SN-001",                                            │
│      process_code=100,                                       │
│      operator="John"                                         │
│  )                                                           │
│                                                               │
│  ✅ Station auto-resolved                                    │
│  ✅ Defaults applied                                         │
│  ✅ C# API compatibility                                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  PATTERN 2: Constructor                      │
│ ──────────────────────────────────────────────────────────── │
│                                                               │
│  report = UUTReport(                                         │
│      pn="ABC123",                                            │
│      sn="SN-001",                                            │
│      rev="A",                                                │
│      process_code=100,                                       │
│      station_name="Station1",                                │
│      location="TestLab",                                     │
│      purpose="Development"                                   │
│  )                                                           │
│                                                               │
│  ✅ Direct control                                           │
│  ✅ Python idiom                                             │
│  ✅ Scripting/testing friendly                               │
└─────────────────────────────────────────────────────────────┘

Both must work in v2!
```

---

## Import Strategy Visual

```
report_models_v2/
│
├── uut_report.py
│   │
│   ├─┐ from ..report_models.uut.steps import SequenceCall
│   │ │                                       (v1 → v2)
│   │ │
│   │ └─► StepList parent injection still works!
│   │     No changes needed to Step hierarchy
│   │
│   ├─┐ from ..report_models.uut.uut_info import UUTInfo
│   │ │                                          (v1 → v2)
│   │ │
│   │ └─► Stable model, reuse unchanged
│   │
│   └─┐ from .report_common import ReportCommon
│     │                             (new in v2)
│     │
│     └─► Composition pattern (replaces inheritance)
│
├── uur_report.py
│   ├─► from ..report_models.uur.uur_info import UURInfo
│   ├─► from ..report_models.uur.uur_sub_unit import UURSubUnit
│   └─► from .report_common import ReportCommon
│
└── report_common.py
    └─┐ from ..report_models.misc_info import MiscInfo
      ├─ from ..report_models.asset import Asset
      └─ from ..report_models.sub_unit import SubUnit
```

**Key rules:**
- ✅ v2 imports from v1 (one-way dependency)
- ❌ v1 NEVER imports from v2 (isolated)
- ✅ Reuse stable models (Steps, Info, MiscInfo, etc.)
- ⭐ Create new composition models (ReportCommon, UUT/UURReport)

---

## Type Safety Comparison

### v1 (Inheritance) - Type Conflicts

```python
class Report:
    type: str = Field(default="T", pattern='^[TR]$')
    misc_infos: Optional[list[MiscInfo]] = Field(default_factory=list)

class UUTReport(Report):
    type: Literal["T"] = "T"  # ❌ Override! Mypy error!
    
class UURReport(Report):
    type: Literal["R"] = "R"  # ❌ Override! Mypy error!
    misc_infos: list[UURMiscInfo] = Field(...)  # ❌ Field type change!
```

**Mypy errors:**
```
error: Cannot override writable attribute with a final one
error: Incompatible types in assignment (expression has type "list[UURMiscInfo]", 
       base class "Report" defined the type as "Optional[list[MiscInfo]]")
```

### v2 (Composition) - Type Safe

```python
class ReportCommon(BaseModel):
    # No 'type' field (moved to concrete classes)
    misc_infos: list[MiscInfo] = Field(default_factory=list)

class UUTReport(BaseModel):
    common: ReportCommon        # ✅ Composition
    type: Literal["T"] = "T"    # ✅ No override
    
class UURReport(BaseModel):
    common: ReportCommon              # ✅ Composition
    type: Literal["R"] = "R"          # ✅ No override
    sub_units: list[UURSubUnit] = ... # ✅ Additional field (not override)
```

**Mypy result:** ✅ Clean! No errors!

---

## Testing Strategy Visual

```
┌───────────────────────────────────────────────────────────┐
│                     Test Pyramid                          │
└───────────────────────────────────────────────────────────┘

                        ▲
                       ╱│╲
                      ╱ │ ╲
                     ╱  │  ╲
                    ╱   │   ╲
          E2E      ╱────┴────╲
                  ╱   Both    ╲
                 ╱  v1 and v2  ╲
                ╱───────────────╲
               ╱  Integration   ╲
              ╱ ─────────────── ╲
             ╱  v1 ↔ v2 Compare  ╲
            ╱─────────────────────╲
           ╱   Unit Tests (v2)    ╱
          ╱───────────────────────╱
         ╱   ReportCommon, UUT,  ╱
        ╱     UUR, Serialization ╱
       ───────────────────────────

Test Types:

1. Unit Tests (v2 only)
   - ReportCommon field validation
   - UUTReport/UURReport construction
   - Serialization/deserialization

2. Comparison Tests (v1 ↔ v2)
   - Identical JSON output
   - Same fields, same values
   - Performance parity

3. Integration Tests (both versions)
   - Service layer compatibility
   - Parent injection works
   - Factory + constructor patterns

4. E2E Tests (both versions)
   - Submit to WATS API
   - Query back reports
   - Verify roundtrip
```

---

## Migration Path

```
┌─────────────────┐
│ Current (0.2.0) │
│ ─────────────── │
│ report_models/  │ ← v1 only (inheritance)
│ (v1)            │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Next (0.2.1)    │
│ ─────────────── │
│ report_models/  │ ← v1 (default)
│ report_models_v2│ ← v2 (opt-in via feature flag)
│                 │
│ USE_REPORT_V2=0 │ ← Default: v1
│ USE_REPORT_V2=1 │ ← Opt-in: v2
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Future (0.3.0)  │
│ ─────────────── │
│ report_models/  │ ← v2 becomes default
│ (v2, renamed)   │
│                 │
│ report_models_v1│ ← v1 deprecated
│ (archived)      │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Later (0.4.0)   │
│ ─────────────── │
│ report_models/  │ ← v2 only
│                 │
│ v1 removed      │
└─────────────────┘
```

---

## Quick Decision Tree

```
┌─────────────────────────────────────────────────┐
│ Do I need to modify report models?              │
└─────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
       YES                     NO
        │                       │
        ▼                       ▼
┌──────────────┐         ┌──────────────┐
│ Which files? │         │ Just use it! │
└──────────────┘         └──────────────┘
        │
        ├─► models.py? ────────────────► Query models (WATSFilter)
        │                                NOT part of redesign!
        │
        ├─► report.py? ────────────────► Base class (v1)
        │                                → Create report_common.py (v2)
        │
        ├─► uut_report.py? ────────────► Inheritance (v1)
        │   uur_report.py?               → Create composition version (v2)
        │
        └─► steps/*.py? ───────────────► Already perfect!
                                         Import from v1 (DON'T COPY!)
```

---

## Related Documentation

- [REPORT_REDESIGN_INDEX.md](REPORT_REDESIGN_INDEX.md) - Documentation index
- [REDESIGNING_THE_REPORT_MODEL.md](REDESIGNING_THE_REPORT_MODEL.md) - Main specification
- [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md) - Architecture deep dive
- [REDESIGN_IMPLEMENTATION_NOTES.md](REDESIGN_IMPLEMENTATION_NOTES.md) - Quick reference

---

**Last Updated:** 2026-01-29
