# Report Domain Refactoring Plan

**Created:** 2026-01-26  
**Status:** PLANNED (Do Not Implement Without Review)  
**Risk Level:** 🟡 MEDIUM-HIGH  
**Estimated Effort:** 4-6 hours implementation + 2-3 hours testing

---

## Executive Summary

The Report domain has been flagged for refactoring to improve maintainability. This document
outlines the proposed changes for future implementation. **This work should NOT be done
alongside other changes due to the critical nature of the Report domain.**

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

### Phase 1: Extract Filter Builders (Low Risk)

**Goal:** Extract OData filter building logic to a separate module.

**New File:** `src/pywats/domains/report/filter_builders.py`

**Functions to Extract:**
```python
# From async_service.py - filter construction logic
def build_header_filter(
    part_number: Optional[str] = None,
    serial_number: Optional[str] = None,
    station_name: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    status: Optional[str] = None
) -> str:
    """Build OData filter string for report headers."""
    ...

def build_date_range_filter(
    date_from: Optional[datetime],
    date_to: Optional[datetime],
    field_name: str = "startDateTime"
) -> Optional[str]:
    """Build date range filter clause."""
    ...
```

**Impact:**
- No public API changes
- Internal reorganization only
- Test existing tests still pass

**Risk:** 🟢 LOW

---

### Phase 2: Extract Query Helpers (Low Risk)

**Goal:** Extract query parameter building to a separate module.

**New File:** `src/pywats/domains/report/query_helpers.py`

**Functions to Extract:**
```python
# From async_service.py - query construction logic
def build_expand_clause(expand: Optional[List[str]]) -> Optional[str]:
    """Build OData $expand clause."""
    ...

def build_orderby_clause(
    orderby: Optional[str],
    default: str = "startDateTime desc"
) -> str:
    """Build OData $orderby clause with default."""
    ...

def build_query_params(
    odata_filter: Optional[str] = None,
    top: Optional[int] = None,
    skip: Optional[int] = None,
    orderby: Optional[str] = None,
    expand: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Build complete OData query parameters dict."""
    ...
```

**Impact:**
- No public API changes
- Improves testability of query logic
- Enables reuse across report queries

**Risk:** 🟢 LOW

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

### Phase 4: UURReport Model Refactoring (High Risk) - FUTURE

⚠️ **DO NOT IMPLEMENT** - Reserved for future consideration.

**Current Issues:**
- 650+ lines mixing schema with business logic
- Fail code navigation embedded in model
- Attachment bookkeeping in model
- Part info management in model

**Potential Extractions:**
1. `failures.py` - Fail code navigation and failure management
2. `part_info_manager.py` - Part information tracking
3. `attachment_registry.py` - Attachment bookkeeping

**Why Deferred:**
- Most complex refactoring
- UURReport is stable and well-tested
- Changes could break repair workflows
- Requires deep domain knowledge

**Risk:** 🔴 HIGH

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

### Phase 1 Complete When:
- [ ] `filter_builders.py` created with extracted functions
- [ ] All existing tests pass without modification
- [ ] Filter functions have 100% test coverage
- [ ] No public API changes

### Phase 2 Complete When:
- [ ] `query_helpers.py` created with extracted functions
- [ ] All existing tests pass without modification
- [ ] Query functions have 100% test coverage
- [ ] No public API changes

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
| 2026-01-26 | Initial plan created, deferred from documentation sprint | AI Assistant |
