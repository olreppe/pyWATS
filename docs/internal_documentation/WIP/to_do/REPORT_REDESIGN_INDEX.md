# Report Model Redesign - Documentation Index

**Project:** pyWATS Report Models v2  
**Status:** Specification Complete - Ready for Implementation  
**Last Updated:** 2026-01-29

---

## Overview

This directory contains comprehensive documentation for redesigning the UUT/UUR report models from inheritance-based to composition-based architecture. The refactor addresses type safety issues while maintaining 100% JSON compatibility with existing WATS API.

---

## Documentation Structure

### 📘 1. Main Specification
**File:** [REDESIGNING_THE_REPORT_MODEL.md](REDESIGNING_THE_REPORT_MODEL.md)

**Purpose:** Complete technical specification for the redesign

**Contents:**
- Executive summary and goals
- Current problems analysis (inheritance type conflicts, Optional[list] anti-pattern)
- Proposed architecture (ReportCommon composition, discriminated unions)
- JSON compatibility strategy
- Parallel implementation approach (report_models_v2/)
- Service layer integration
- Testing framework
- **7-phase implementation plan** (6-7 days estimated)
- Timeline and milestones

**Read this:** For complete technical understanding and implementation plan

---

### 🔧 2. Architecture Deep Dive
**File:** [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md)

**Purpose:** Critical architectural context from codebase analysis

**Contents:**
- **Service layer usage** - What async_service actually imports
- **Constructor vs factory pattern** - Why both exist and must be supported
- **Parent injection mechanism** - How StepList works (DON'T CHANGE!)
- **Legacy validator analysis** - Why it should be dropped
- **Import strategy** - What to import vs create in v2
- Testing strategy for architectural features
- Migration impact analysis

**Read this:** Before starting implementation (prevents common mistakes)

**Critical insights:**
```python
# Parent injection happens in StepList, NOT constructors
class StepList(List[StepType]):
    def append(self, item):
        item.parent = self.parent  # ← Injection here

# Import Steps from v1 (already perfect!)
from ..report_models.uut.steps import SequenceCall

# Drop Optional[list] anti-pattern
# Bad:  misc_infos: Optional[list[MiscInfo]] = Field(default_factory=list)
# Good: misc_infos: list[MiscInfo] = Field(default_factory=list)
```

---

### 📋 3. Quick Reference Guide
**File:** [REDESIGN_IMPLEMENTATION_NOTES.md](REDESIGN_IMPLEMENTATION_NOTES.md)

**Purpose:** Quick reference for developers during implementation

**Contents:**
- Directory structure visual guide
- What to reuse vs create
- Common pitfalls to avoid
- Import examples (good vs bad)
- Testing strategy summary
- Quick start checklist

**Read this:** As a cheat sheet during implementation

**Visual guide:**
```
report_models/              # v1 - DON'T TOUCH (except to import)
├── models.py              # Query models (NOT part of refactor)
└── uut/steps/             # ⚠️ Import from here (DON'T COPY!)

report_models_v2/          # v2 - NEW parallel implementation
├── report_common.py       # NEW: Composition pattern
├── uut_report.py          # NEW: Composition-based
└── uur_report.py          # NEW: Composition-based
```

---

## Reading Order

### For Implementers

1. **Start here:** [REDESIGNING_THE_REPORT_MODEL.md](REDESIGNING_THE_REPORT_MODEL.md)
   - Read sections 1-4 (Executive Summary through Proposed Architecture)
   - Understand parallel implementation strategy (section 5)
   
2. **Then read:** [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md)
   - Focus on sections 2-4 (Constructor/Factory, Parent Injection, Legacy Validator)
   - Review import strategy (section 5)
   
3. **Keep open:** [REDESIGN_IMPLEMENTATION_NOTES.md](REDESIGN_IMPLEMENTATION_NOTES.md)
   - Quick reference during coding
   - Directory structure visual aid
   - Common pitfalls checklist

### For Reviewers

1. [REDESIGNING_THE_REPORT_MODEL.md](REDESIGNING_THE_REPORT_MODEL.md) - Section 2 (Proposed Architecture)
2. [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md) - Section 6 (Migration Notes)
3. [REDESIGNING_THE_REPORT_MODEL.md](REDESIGNING_THE_REPORT_MODEL.md) - Section 7 (Comparison Testing)

### For Stakeholders

1. [REDESIGNING_THE_REPORT_MODEL.md](REDESIGNING_THE_REPORT_MODEL.md) - Section 1 (Executive Summary)
2. [REDESIGNING_THE_REPORT_MODEL.md](REDESIGNING_THE_REPORT_MODEL.md) - Section 11 (Timeline)
3. [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md) - Section 8 (Migration Notes)

---

## Key Design Decisions

### ✅ Approved Decisions

1. **Parallel Implementation**
   - Create `report_models_v2/` alongside `report_models/`
   - Feature flag (`USE_REPORT_V2`) controls which version is used
   - Zero risk to existing code

2. **Composition Over Inheritance**
   - Extract shared fields into `ReportCommon`
   - UUTReport/UURReport compose (not inherit)
   - Eliminates type conflicts

3. **Reuse Step Hierarchy**
   - Import from v1 (already uses discriminated union!)
   - Don't copy or modify
   - Parent injection via StepList works perfectly

4. **Drop Legacy Validator**
   - Remove `Optional[list]` with `default_factory` anti-pattern
   - Use clean `list[T]` pattern
   - No WATS 5.1 compatibility layer

5. **Dual Pattern Support**
   - Keep constructor AND factory patterns
   - Don't force users into one approach
   - Service layer adds convenience, constructor gives control

### ❌ Rejected Alternatives

1. **Modify v1 in place** - Too risky, breaks existing code
2. **Copy Step hierarchy to v2** - Unnecessary duplication, parent injection would break
3. **Drop constructor pattern** - Users rely on it, breaking change
4. **Keep Optional[list] pattern** - Type confusion, legacy cruft

---

## Implementation Timeline

**Estimated Duration:** 6-7 days

### Phase 1: Setup (Day 1)
- Create `report_models_v2/` directory structure
- Verify existing architecture (models.py vs report_models/)
- Document import strategy

### Phase 2: ReportCommon (Days 1-2)
- Create composition model
- Field validators (PN/SN, time sync)
- Drop legacy validator
- Unit tests

### Phase 3: UUTReport (Days 2-3)
- Composition-based implementation
- Import Steps from v1
- Test parent injection
- JSON compatibility tests

### Phase 4: UURReport (Days 3-4)
- Composition-based implementation
- Dual process code handling
- JSON compatibility tests

### Phase 5: Testing (Days 4-5)
- Comparison framework (v1 vs v2 outputs)
- Integration tests
- Performance tests

### Phase 6: Service Integration (Days 5-6)
- Update `__init__.py` with feature flag
- Service layer compatibility
- Migration guide

### Phase 7: Documentation & Review (Days 6-7)
- Update user documentation
- Code review
- Migration plan for 0.3.0

---

## Success Criteria

### Must Have ✅

- [ ] v1 and v2 produce **identical JSON**
- [ ] All existing tests pass with v2
- [ ] Parent injection still works (StepList mechanism)
- [ ] Both constructor and factory patterns work
- [ ] Feature flag toggles between v1/v2
- [ ] No breaking changes to public API
- [ ] Type errors reduced (mypy clean on v2)

### Should Have ✨

- [ ] Comparison tests (v1 vs v2 automated validation)
- [ ] Performance benchmarks (no regression)
- [ ] Migration guide for 0.3.0
- [ ] Example code for common scenarios

### Nice to Have 🎁

- [ ] Deprecation warnings for v1 (prepare for 0.3.0)
- [ ] Profiling data (memory, serialization speed)
- [ ] Detailed migration timeline

---

## Related Documentation

### Internal References
- `UUR_IMPLEMENTATION_INSTRUCTIONS.md` - Dual process code architecture
- `src/pywats/domains/report/__init__.py` - Export structure
- `src/pywats/domains/report/report_models/uut/step.py` - Discriminated union reference

### External Resources
- Pydantic 2.x documentation (discriminated unions, composition)
- WATS API specification (JSON schemas)
- Type system best practices (composition over inheritance)

---

## Contact & Support

**Questions about:**
- **Directory confusion (models.py vs report_models/):** Read [REDESIGN_IMPLEMENTATION_NOTES.md](REDESIGN_IMPLEMENTATION_NOTES.md) section 1
- **Parent injection:** Read [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md) section 3
- **Import strategy:** Read [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md) section 5
- **Legacy validator:** Read [REPORT_REDESIGN_ARCHITECTURE_NOTES.md](REPORT_REDESIGN_ARCHITECTURE_NOTES.md) section 4
- **Testing approach:** Read [REDESIGNING_THE_REPORT_MODEL.md](REDESIGNING_THE_REPORT_MODEL.md) section 7

---

## Status Tracking

**Current Status:** ✅ Specification Complete

### Completed
- [x] Problem analysis (inheritance type conflicts)
- [x] Architecture design (composition pattern)
- [x] Parallel implementation strategy
- [x] Service layer analysis
- [x] Parent injection mechanism documented
- [x] Legacy validator analysis
- [x] Import strategy defined
- [x] Testing framework designed
- [x] Timeline estimated

### Next Steps
1. Create `report_models_v2/` directory
2. Implement ReportCommon
3. Implement UUTReport with composition
4. Implement UURReport with composition
5. Create comparison tests
6. Integrate with service layer
7. Submit for review

---

**Last Updated:** 2026-01-29  
**Specification Version:** 1.0  
**Ready for Implementation:** Yes ✅
