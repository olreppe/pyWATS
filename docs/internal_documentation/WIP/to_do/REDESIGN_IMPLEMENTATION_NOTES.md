# Report Model Redesign - Implementation Notes

**Quick Reference for Developers**

---

## Key Clarifications (Added 2026-01-29)

### 1. Understanding Existing Structure

**CRITICAL:** Don't confuse the two `models` locations:

```
src/pywats/domains/report/
├── models.py                   ⚠️ QUERY/FILTER MODELS - DON'T TOUCH
│                               (WATSFilter, ReportHeader, etc.)
│
└── report_models/              ✓ REPORT STRUCTURE - THIS IS WHAT WE REFACTOR
    ├── report.py               (Base Report class - inheritance)
    ├── uut/uut_report.py       (UUTReport - inheritance)
    └── uur/uur_report.py       (UURReport - inheritance)
```

**What each contains:**
- `models.py` = Query/filter classes for searching reports (NOT report structure)
- `report_models/` = Actual UUT/UUR report structure (inheritance-based)
- `report_models_v2/` = NEW parallel implementation (composition-based)

### 2. Parallel Implementation Strategy

Create `report_models_v2/` alongside existing `report_models/`:

```
report_models_v2/
├── report_common.py            # NEW: Composition pattern
├── uut_report.py               # NEW: Composition-based UUTReport
├── uur_report.py               # NEW: Composition-based UURReport
├── report_union.py             # NEW: Discriminated union
│
├── shared/                     # Copied or imported from v1
│   ├── misc_info.py
│   ├── asset.py
│   └── ...
│
├── uut/
│   └── steps/                  # ⚠️ DON'T COPY - Import from v1!
│       # Use: from ..report_models.uut.steps import *
│
└── uur/
    ├── uur_info.py
    └── uur_sub_unit.py
```

### 3. What to Reuse vs Create

**Reuse from v1 (relative imports):**
- ✓ Step hierarchy (`uut/steps/`) - already uses discriminated union!
- ✓ Small stable models (MiscInfo, Asset, Chart, SubUnit)
- ✓ Info models (UUTInfo, UURInfo) - unless they need changes

**Create new in v2:**
- ✓ `report_common.py` - replaces Report base class
- ✓ `uut_report.py` - composition-based version
- ✓ `uur_report.py` - composition-based version
- ✓ `report_union.py` - discriminated union parser

### 4. Common Pitfalls to Avoid

**❌ DON'T:**
- Touch `models.py` (query models - different concern)
- Rewrite Step classes (already perfect!)
- Create circular imports (v1 ← v2 is bad)
- Forget to update `__init__.py` exports

**✓ DO:**
- Only work in `report_models/` and `report_models_v2/`
- Import Steps from v1 via relative import
- Keep v1 and v2 completely isolated
- Use feature flag for switching (`USE_REPORT_V2=1`)

### 5. Testing Strategy

```bash
# Run with v1 (default)
pytest tests/domains/report/

# Run with v2
USE_REPORT_V2=1 pytest tests/domains/report/

# Compare v1 vs v2 outputs
pytest tests/report_models/test_v1_v2_comparison.py
```

### 6. Import Examples

**Good - v2 imports from v1:**
```python
# report_models_v2/uut_report.py
from ..report_models.uut.steps import SequenceCall  # ✓ OK
from ..report_models.misc_info import MiscInfo      # ✓ OK
```

**Bad - v1 imports from v2:**
```python
# report_models/uut/uut_report.py
from ..report_models_v2 import ReportCommon  # ✗ BAD - creates coupling
```

---

## Quick Start Checklist

1. [ ] Read full spec: `REDESIGNING_THE_REPORT_MODEL.md`
2. [ ] Verify you understand `models.py` vs `report_models/` distinction
3. [ ] Create `report_models_v2/` directory
4. [ ] Set up relative imports for Steps (don't copy!)
5. [ ] Implement `ReportCommon` composition model
6. [ ] Implement new `UUTReport` and `UURReport`
7. [ ] Create comparison tests (`test_v1_v2_comparison.py`)
8. [ ] Test both implementations produce identical JSON
9. [ ] Add feature flag to `__init__.py`
10. [ ] Submit for review with both v1 and v2 working

---

## Emergency Contact

If confused about architecture:
1. Check `src/pywats/domains/report/__init__.py` - shows what's exported
2. Look at Step implementation - `report_models/uut/step.py` - discriminated union reference
3. Review UUR spec - `UUR_IMPLEMENTATION_INSTRUCTIONS.md` - dual process code architecture
4. **Read architecture deep dive:** `REPORT_REDESIGN_ARCHITECTURE_NOTES.md` - detailed analysis

---

## Critical Architectural Context

**MUST READ:** [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md)

This document contains critical context discovered through codebase analysis:

1. **Service Layer Usage** - What async_service actually imports/needs
2. **Constructor vs Factory** - Why both patterns exist and must be supported
3. **Parent Injection** - How StepList injects parent references (DON'T CHANGE!)
4. **Legacy Validator** - Should be dropped (remove Optional[list] anti-pattern)
5. **Import Strategy** - What to import vs create in v2

**Key insights:**
- Parent references injected by StepList.append(), NOT constructors
- Import Step hierarchy from v1 unchanged (already perfect!)
- Drop legacy validator (Optional[list] with default_factory is anti-pattern)
- Support both constructor and factory patterns (users rely on both)

---

**Last Updated:** 2026-01-29  
**Related Docs:** 
- REDESIGNING_THE_REPORT_MODEL.md (main spec)
- REPORT_REDESIGN_ARCHITECTURE_NOTES.md (architecture deep dive)
