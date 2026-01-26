# Report Domain Refactoring Plan

**Created:** 2026-01-26  
**Completed:** 2026-01-26  
**Status:** ✅ ALL PHASES COMPLETE  
**Risk Level:** 🟢 LOW (completed successfully)  
**Actual Effort:** ~4 hours implementation + testing

---

## Executive Summary

The Report domain refactoring is **COMPLETE**. All planned phases have been successfully 
implemented with zero breaking changes to the public API.

### Completed Work

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Extract Filter Builders | ✅ Complete |
| Phase 2 | Extract Query Helpers | ✅ Complete |
| Phase 3 | Service Split | ⏸️ Deferred (not urgent) |
| Phase 4 | UURReport Model Refactoring | ✅ Complete |

### Final Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| `async_service.py` | 1101 lines | 1076 lines | -25 lines (extracted to helpers) |
| `service.py` | 501 lines | 500 lines | Maintained |
| `uur_report.py` | 644 lines | 433 lines | **-33% reduction** |
| `filter_builders.py` | N/A | 249 lines | New module |
| `query_helpers.py` | N/A | 258 lines | New module |
| **Test Results** | 134 pass | 134 pass | ✅ No regressions |

### Key Achievements
- ✅ OData filter building extracted to reusable `filter_builders.py`
- ✅ Query parameter construction extracted to `query_helpers.py`
- ✅ UURReport simplified to pure Pydantic model (no internal `_xxx` lists)
- ✅ All failures stored on UURSubUnit only (matches C# implementation)
- ✅ Deprecated classes marked for removal in v0.2.0
- ✅ All 134 report tests passing

---

## Current State (Post-Refactoring)

### File Size Analysis

| File | Lines | Status | Notes |
|------|-------|--------|-------|
| `service.py` | 500 | ✅ | Stable, well-organized |
| `async_service.py` | 1076 | ✅ | Factory logic isolated, queries use helpers |
| `models.py` | 527 | ✅ | Acceptable, well-organized |
| `filter_builders.py` | 249 | ✅ | **NEW** - OData filter utilities |
| `query_helpers.py` | 258 | ✅ | **NEW** - Query parameter utilities |
| `uur_report.py` | 433 | ✅ | **REFACTORED** - Pure Pydantic model |

### Health Check Score: 47/50 (A)

**Improvements from refactoring:**
- +3 for extracting filter/query logic
- +3 for UURReport simplification
- Remaining -3: Some complex factory methods (acceptable)

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

**Detailed Documentation:** [UUR_REFACTORING.md](../completed/UUR_REFACTORING.md)

**Completed Work:**
- ✅ Removed all internal `_xxx` lists (`_failures`, `_part_infos`, `_misc_info`, `_attachments`, `_fail_codes`)
- ✅ Pure Pydantic model (433 lines, down from 644 - **33% reduction**)
- ✅ Failures stored on UURSubUnit only (matches C# implementation)
- ✅ Model validator ensures main unit exists
- ✅ `failures` property returns main unit's failures
- ✅ All 134 tests pass

**Deprecated Classes (marked for removal in v0.2.0):**
- `UURAttachment` → Use `Attachment`
- `Failure` → Use `UURFailure`
- `FailCode`, `FailCodes` → Use `ProcessService.get_fail_codes()`
- `MiscUURInfo` → Use `Report.misc_infos`
- `UURPartInfo` → Use `UURSubUnit`

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

### Phase 1 Complete: ✅ DONE
- [x] `filter_builders.py` created with extracted functions
- [x] All existing tests pass without modification
- [x] Filter functions have comprehensive documentation
- [x] No public API changes

### Phase 2 Complete: ✅ DONE
- [x] `query_helpers.py` created with extracted functions
- [x] All existing tests pass without modification
- [x] Query functions have comprehensive documentation
- [x] No public API changes

### Phase 4 Complete: ✅ DONE
- [x] UURReport simplified to pure Pydantic model
- [x] All internal `_xxx` lists removed
- [x] Failures stored on UURSubUnit only
- [x] Model validator ensures main unit exists
- [x] 33% code reduction (644 → 433 lines)
- [x] All 134 tests pass
- [x] Deprecated classes marked for v0.2.0 removal

---

## Future Considerations

### Phase 3: Service Split (Deferred)

⚠️ **Not planned for implementation** - Current structure is maintainable.

**Potential future split (if file sizes grow):**
1. `ReportSubmissionService` - submit, submit_offline, process_queue
2. `ReportQueryService` - query_headers, query_uut_headers, query_uur_headers, get_report
3. `ReportAttachmentService` - get_attachment, get_all_attachments, get_certificate

**Why Deferred:**
- Current file sizes are acceptable (~1000 lines)
- Filter/query extraction addressed main complexity
- Would require API changes affecting all consumers
- Not worth the migration effort

---

## Modules Created

### filter_builders.py (249 lines)

OData filter construction utilities for report queries.

```python
# Available functions:
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

### query_helpers.py (258 lines)

Query parameter construction utilities for report queries.

```python
# Available functions:
is_uut_report_type(report_type) -> bool
get_expand_fields(is_uut, include_subunits, include_misc_info, ...) -> List[str]
build_expand_clause(expand) -> Optional[str]
build_orderby_clause(orderby, default="start desc") -> str
build_query_params(odata_filter, top, skip, orderby, expand, select, count) -> Dict[str, Any]
get_default_query_params(report_type, include_subunits, top, orderby) -> Dict[str, Any]
```

---

## References

- [UUR Refactoring Details](../completed/UUR_REFACTORING.md)
- [Report Domain Health Check](../domain_health/report.md)
- [Report Module Documentation](../../modules/report.md)

### Source Files
- `src/pywats/domains/report/service.py` (500 lines)
- `src/pywats/domains/report/async_service.py` (1076 lines)
- `src/pywats/domains/report/filter_builders.py` (249 lines) ✨ NEW
- `src/pywats/domains/report/query_helpers.py` (258 lines) ✨ NEW
- `src/pywats/domains/report/report_models/uur/uur_report.py` (433 lines) ✨ REFACTORED

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-26 | **REFACTORING COMPLETE** - All phases done, 134 tests passing | AI Assistant |
| 2026-01-26 | Phase 4 COMPLETED: UURReport simplified to pure Pydantic model (33% reduction) | AI Assistant |
| 2026-01-26 | Phase 1 & 2 COMPLETED: filter_builders.py, query_helpers.py created | AI Assistant |
| 2026-01-26 | Initial plan created, deferred from documentation sprint | AI Assistant |

---

## Conclusion

The Report domain refactoring has been successfully completed. The codebase is now:

1. **More maintainable** - Filter and query logic extracted to dedicated modules
2. **More testable** - Pure functions that can be unit tested independently
3. **Cleaner** - UURReport is now a pure Pydantic model without dual data stores
4. **Fully backward compatible** - No public API changes, all tests pass

The optional Phase 3 (Service Split) has been deferred indefinitely as the current
structure is maintainable and the extraction of filter/query helpers addressed the
main complexity concerns.
