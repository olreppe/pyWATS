# Report Models v2 - Import Strategy

**Created:** 2026-01-29  
**Purpose:** Document what to import from v1 vs create new in v2

---

## Verified Architecture

### Directory Structure Confirmed

```
src/pywats/domains/report/
├── models.py                    ⚠️ QUERY MODELS - NOT INVOLVED IN REFACTOR
├── report_models/               ← v1 (inheritance-based)
├── report_models_v2/            ← v2 (composition-based) - NEWLY CREATED
└── async_service.py             ← Service layer (imports from both)
```

### What's in models.py (NOT involved in refactor)

**Query/filter models:**
- WATSFilter
- ReportHeader
- HeaderSubUnit, HeaderMiscInfo, HeaderAsset
- AttachmentMetadata

**These are for searching/querying reports, NOT report structure!**

### What's in report_models/ (v1 - source for imports and replacement)

**Base class (REPLACE with composition):**
- report.py → Report base class (inheritance)

**Stable models (IMPORT to v2):**
- misc_info.py → MiscInfo
- asset.py → Asset, AssetStats
- sub_unit.py → SubUnit
- chart.py → Chart, ChartSeries, ChartType
- additional_data.py → AdditionalData
- binary_data.py → BinaryData
- wats_base.py → WATSBase

**UUT models:**
- uut/uut_report.py → UUTReport (REPLACE with composition)
- uut/uut_info.py → UUTInfo (IMPORT to v2)
- uut/steps/ → **IMPORT ALL (already perfect!)**
  - step.py → Step, StepStatus, StepType
  - sequence_call.py → SequenceCall, StepList (parent injection!)
  - numeric_step.py → NumericStep, MultiNumericStep
  - string_step.py → StringStep, MultiStringStep
  - boolean_step.py → BooleanStep, MultiBooleanStep
  - chart_step.py → ChartStep
  - action_step.py → ActionStep
  - generic_step.py → GenericStep

**UUR models:**
- uur/uur_report.py → UURReport (REPLACE with composition)
- uur/uur_info.py → UURInfo (IMPORT to v2)
- uur/uur_sub_unit.py → UURSubUnit (IMPORT to v2)

---

## Import Strategy for v2

### Create New (composition-based)

```python
# report_models_v2/report_common.py
class ReportCommon(BaseModel):
    """NEW: Replaces Report base class with composition pattern"""
    
# report_models_v2/uut_report.py
class UUTReport(BaseModel):
    """NEW: Composition-based UUTReport"""
    common: ReportCommon
    
# report_models_v2/uur_report.py
class UURReport(BaseModel):
    """NEW: Composition-based UURReport"""
    common: ReportCommon
    
# report_models_v2/report_union.py
Report = UUTReport | UURReport
"""NEW: Discriminated union for parsing"""
```

### Import from v1 (stable, reusable)

```python
# In report_models_v2 files, use relative imports:

# Import Step hierarchy (ALREADY PERFECT - DON'T COPY!)
from ..report_models.uut.steps import (
    SequenceCall,
    StepList,
    StepType,
    Step,
    NumericStep,
    StringStep,
    BooleanStep,
    # ... all step types
)

# Import Info models
from ..report_models.uut.uut_info import UUTInfo
from ..report_models.uur.uur_info import UURInfo
from ..report_models.uur.uur_sub_unit import UURSubUnit

# Import shared models
from ..report_models.misc_info import MiscInfo
from ..report_models.asset import Asset, AssetStats
from ..report_models.sub_unit import SubUnit
from ..report_models.chart import Chart
from ..report_models.wats_base import WATSBase
```

---

## What async_service.py Imports (Verified)

```python
# From line 10-14 of async_service.py:
from .models import WATSFilter, ReportHeader
from .report_models import UUTReport, UURReport
from .report_models.uut.uut_info import UUTInfo
from .report_models.uur.uur_info import UURInfo
from .report_models.uur.uur_sub_unit import UURSubUnit
```

**Key observations:**
- ✅ Only imports concrete report classes (UUTReport, UURReport)
- ✅ Only imports Info models (UUTInfo, UURInfo, UURSubUnit)
- ❌ Does NOT import Report base class
- ❌ Does NOT import Step classes

**Implications:**
- v2 must provide UUTReport and UURReport with same interface
- Feature flag will switch `from .report_models` to `from .report_models_v2`
- Step hierarchy stays internal (users access via `add_*_step()` methods)

---

## Implementation Order

1. **report_common.py** - Create composition model
2. **uut_report.py** - Import Steps from v1, compose with ReportCommon
3. **uur_report.py** - Import UURInfo/UURSubUnit from v1, compose with ReportCommon
4. **report_union.py** - Create discriminated union for parsing

---

## Critical Rules

### ✅ DO:
- Import Step hierarchy from v1 (relative imports)
- Import stable models (Info, MiscInfo, Asset, etc.)
- Create new composition-based report classes
- Use `from ..report_models.X import Y` pattern

### ❌ DON'T:
- Copy Step classes to v2 (parent injection will break!)
- Modify anything in report_models/ v1
- Import from models.py (different concern)
- Create circular imports (v2 → v1 only, never v1 → v2)

---

**Status:** Architecture verified ✓  
**Next:** Implement report_common.py
