# Report Domain Refactoring Plan

**Created:** 2026-01-26  
**Status:** PHASE 1 & 2 COMPLETE ✅  
**Risk Level:** 🟡 MEDIUM-HIGH  
**Estimated Effort:** 4-6 hours implementation + 2-3 hours testing

---

## Executive Summary

The Report domain has been flagged for refactoring to improve maintainability. This document
outlines the proposed changes for future implementation. **This work should NOT be done
alongside other changes due to the critical nature of the Report domain.**

**Phase 1 & 2: COMPLETED (Jan 2026)**
- ✅ `filter_builders.py` - OData filter building utilities
- ✅ `query_helpers.py` - Query parameter building utilities
- ✅ All 134 report tests pass
- ✅ No public API changes

**Key Concerns:**
- Report submission is a core business function
- Breaking changes could prevent test data submission
- Complex UUT/UUR factory logic must remain stable
- Extensive test coverage required before and after changes

---

## Current State

### File Size Analysis

| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `service.py` | 501 | ⚠️ | Approaching maintainability threshold |
| `async_service.py` | 1101 | ⚠️ | Contains factory logic + queries + submission |
| `models.py` | 527 | ✅ | Acceptable, well-organized |
| `report_models/uur/uur_report.py` | 650+ | ⚠️ | Mixes schema with logic |

### Health Check Score: 41/50 (B+)

**Deductions:**
- Large files affecting maintainability (-4)
- Missing Raises documentation (-3)
- UURReport model complexity (-2)

---

## Proposed Refactoring

### Phase 1: Extract Filter Builders (Low Risk) ✅ COMPLETE

**Goal:** Extract OData filter building logic to a separate module.

**New File:** `src/pywats/domains/report/filter_builders.py` ✅ Created

**Functions Extracted:**
```python
# filter_builders.py - OData filter construction
build_serial_filter(serial_number: str) -> str
build_part_number_filter(part_number: str) -> str
build_date_range_filter(start_date, end_date, field_name="start") -> str
build_recent_filter(days=7, field_name="start") -> str
build_today_filter(field_name="start") -> str
build_subunit_part_filter(subunit_part_number, is_uut=True) -> str
build_subunit_serial_filter(subunit_serial_number, is_uut=True) -> str
build_header_filter(part_number, serial_number, start_date, end_date) -> str
combine_filters(filters, operator="and") -> Optional[str]
```

**Impact:**
- ✅ No public API changes
- ✅ Internal reorganization only
- ✅ All existing tests pass (134/134)

**Risk:** 🟢 LOW - COMPLETED

---

### Phase 2: Extract Query Helpers (Low Risk) ✅ COMPLETE

**Goal:** Extract query parameter building to a separate module.

**New File:** `src/pywats/domains/report/query_helpers.py` ✅ Created

**Functions Extracted:**
```python
# query_helpers.py - query construction utilities
is_uut_report_type(report_type) -> bool
get_expand_fields(is_uut, include_subunits, include_misc_info, ...) -> List[str]
build_expand_clause(expand) -> Optional[str]
build_orderby_clause(orderby, default="start desc") -> str
build_query_params(odata_filter, top, skip, orderby, expand, select, count) -> Dict[str, Any]
get_default_query_params(report_type, include_subunits, top, orderby) -> Dict[str, Any]
```

**Impact:**
- ✅ No public API changes
- ✅ Improved testability of query logic
- ✅ Enables reuse across report queries
- ✅ All existing tests pass (134/134)

**Risk:** 🟢 LOW - COMPLETED

---

### Phase 3: Service Split (Medium Risk) - FUTURE

⚠️ **DO NOT IMPLEMENT** - Reserved for future consideration.

**Potential Split:**
1. `ReportSubmissionService` - submit, submit_offline, process_queue
2. `ReportQueryService` - query_headers, query_uut_headers, query_uur_headers, get_report
3. `ReportAttachmentService` - get_attachment, get_all_attachments, get_certificate

**Why Deferred:**
- Requires API changes (new service classes)
- Affects all consumers of ReportService
- Complex dependency injection changes
- Not urgent - current file size is manageable

**Risk:** 🟠 MEDIUM

---

### Phase 4: UURReport Model Refactoring (High Risk) - ✅ COMPLETE

**Status:** COMPLETED (Jan 26, 2026)

See: [UUR_REFACTORING.md](../completed/UUR_REFACTORING.md)

**Completed Work:**
- Removed all internal `_xxx` lists (dual data stores)
- Pure Pydantic model now (432 lines, down from 644)
- Failures stored on UURSubUnit only
- Model validator ensures main unit exists
- All 134 tests pass

**Remaining Future Work:**
- Refactor `UURAttachment` to pure Pydantic model
- Add fail code validation via ProcessService cache
- Clean up deprecated files: `failure.py`, `misc_uur_info.py`, `fail_code.py`

**Risk:** 🟢 LOW (completed successfully)

---

## What NOT to Touch

**Critical Factory Methods (LEAVE ALONE):**
- `create_uut_report()` - UUT factory, tested, stable
- `create_uur_report()` - UUR factory with complex overloads
- `create_uur_from_uut()` - UUT→UUR conversion
- `_copy_sub_units_to_uur()` - Sub-unit copying logic
- `_resolve_station()` - Station metadata resolution

**Reason:** These methods are the core of report creation and have been
carefully tested. Any changes risk breaking the test submission pipeline.

---

## Implementation Guidelines

### Before Starting Any Phase:

1. **Run full test suite** - Ensure 100% pass rate
2. **Create feature branch** - `feature/report-refactor-phase-N`
3. **Document current behavior** - Screenshot/log expected outputs
4. **Add integration tests** - Cover any untested scenarios

### During Implementation:

1. **One phase at a time** - Complete and merge before next phase
2. **No API changes in Phase 1-2** - Internal only
3. **Preserve all imports** - Re-export from original locations
4. **Run tests after each file change** - Catch issues early

### After Each Phase:

1. **Full test suite must pass** - No exceptions
2. **Manual testing** - Submit actual UUT/UUR reports
3. **Code review** - Second pair of eyes required
4. **Documentation update** - Update affected docs

---

## Testing Requirements

### Phase 1-2 (Filter Builders & Query Helpers)

```python
# Required test coverage:
def test_build_header_filter_all_params():
    """Filter with all parameters."""
    
def test_build_header_filter_partial():
    """Filter with some parameters."""
    
def test_build_header_filter_empty():
    """Filter with no parameters returns None."""
    
def test_build_date_range_filter():
    """Date range filter generation."""
    
def test_build_query_params():
    """Complete query params dict."""
```

### Integration Tests (All Phases)

```python
# Must pass before and after:
def test_submit_uut_report_roundtrip():
    """Create → Submit → Query → Verify."""
    
def test_submit_uur_report_roundtrip():
    """Create → Submit → Query → Verify."""
    
def test_offline_queue_processing():
    """Offline → Queue → Process → Verify."""
```

---

## Success Criteria

### Phase 1 Complete When: ✅ DONE
- [x] `filter_builders.py` created with extracted functions
- [x] All existing tests pass without modification
- [x] Filter functions have comprehensive documentation
- [x] No public API changes

### Phase 2 Complete When: ✅ DONE
- [x] `query_helpers.py` created with extracted functions
- [x] All existing tests pass without modification
- [x] Query functions have comprehensive documentation
- [x] No public API changes

---

## References

- [Report Domain Health Check](../domain_health/report.md)
- [Report Module Documentation](../../modules/report.md)
- Service: `src/pywats/domains/report/service.py`
- Async Service: `src/pywats/domains/report/async_service.py`
- Models: `src/pywats/domains/report/models.py`

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-26 | Phase 4 COMPLETED: UURReport simplified to pure Pydantic model | AI Assistant |
| 2026-01-26 | Phase 1 & 2 COMPLETED: filter_builders.py, query_helpers.py created | AI Assistant |
| 2026-01-26 | Initial plan created, deferred from documentation sprint | AI Assistant |
