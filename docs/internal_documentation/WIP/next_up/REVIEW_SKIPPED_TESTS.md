# Review Skipped Tests

**Created:** 2026-01-27  
**Status:** Needs Review  
**Priority:** High

## Summary

13 tests are currently being skipped. Many use `pytest.skip()` inside test bodies, which hides test failures as "skipped" rather than failing properly. This needs architectural review.

## Skipped Tests Analysis

### 1. Analytics Domain (3 tests)

| Test | Skip Reason | Assessment |
|------|-------------|------------|
| `test_get_top_failed_advanced_with_filter` | "Test may require specific filter parameters" | ⚠️ **LAZY SKIP** - Test should define valid parameters or mock |
| `test_get_aggregated_measurements` | "Test may require specific filter parameters" | ⚠️ **LAZY SKIP** - Same issue |
| `test_trace_serial_numbers` | "No units in flow" | ⚠️ **DATA DEPENDENCY** - Test requires pre-existing data |

**Location:** `tests/domains/analytics/test_internal_endpoints.py`, `test_unit_flow.py`

### 2. Asset Domain (2 tests)

| Test | Skip Reason | Assessment |
|------|-------------|------------|
| `test_add_log_message` | "Asset log message endpoint not available: HTTP 404" | ❓ **API MISMATCH** - Either endpoint doesn't exist or wrong URL |
| `test_cleanup_assets` | "Keep test assets for inspection" | ⚠️ **INTENTIONAL** - But should use `@pytest.mark.skip` not runtime |

**Location:** `tests/domains/asset/test_workflow.py`

### 3. Process Domain (2 tests)

| Test | Skip Reason | Assessment |
|------|-------------|------------|
| `test_internal_get_processes` | "Internal process service not available" | ❓ **API MISMATCH** - Internal endpoint may not exist on test server |
| `test_internal_get_repair_configs` | "Internal process service not available" | ❓ **API MISMATCH** - Same |

**Location:** `tests/domains/process/test_models.py`

### 4. Product Domain (1 test)

| Test | Skip Reason | Assessment |
|------|-------------|------------|
| `test_get_groups` | "API endpoint /api/Product/Groups not available on server" | ❓ **API MISMATCH** - Endpoint may require specific WATS version |

**Location:** `tests/domains/product/test_integration.py`

### 5. Report Domain (2 tests)

| Test | Skip Reason | Assessment |
|------|-------------|------------|
| `test_send_uur_report` | "Failure categories/codes not configured in WATS" | ⚠️ **SERVER CONFIG** - Valid skip but should be `xfail` |
| `test_submit_simple_report` | "Requires live WATS server" | 🔴 **BAD SKIP** - All integration tests require live server! |

**Location:** `tests/domains/report/test_integration.py`, `test_report_builder.py`

### 6. Rootcause Domain (1 test)

| Test | Skip Reason | Assessment |
|------|-------------|------------|
| `test_get_ticket_by_id` | "No tickets available" | ⚠️ **DATA DEPENDENCY** - Should create test data or mock |

**Location:** `tests/domains/rootcause/test_integration.py`

### 7. Software Domain (1 test)

| Test | Skip Reason | Assessment |
|------|-------------|------------|
| `test_get_packages_by_tag` | "No packages with tags found" | ⚠️ **DATA DEPENDENCY** - Should create tagged package in setup |

**Location:** `tests/domains/software/test_comprehensive.py`

### 8. Integration Tests (1 test)

| Test | Skip Reason | Assessment |
|------|-------------|------------|
| `test_create_product_with_all_tags_at_once` | "Product tag test skipped: assert 0 >= 3" | 🔴 **HIDDEN FAILURE** - Assertion failed but skipped instead of failing |

**Location:** `tests/integration/test_boxbuild.py`

---

## Problem Patterns

### Pattern 1: Runtime Skip Hiding Failures 🔴
```python
# BAD - hides test failures
try:
    result = api.do_something()
    assert len(result) >= 3
except AssertionError as e:
    pytest.skip(f"Test skipped: {e}")  # This should FAIL not skip!
```

**Affected tests:** `test_create_product_with_all_tags_at_once`

### Pattern 2: Data Dependency Without Setup ⚠️
```python
# BAD - depends on external data existing
tickets = api.get_tickets()
if not tickets:
    pytest.skip("No tickets available")  # Should create test data!
```

**Affected tests:** `test_get_ticket_by_id`, `test_trace_serial_numbers`, `test_get_packages_by_tag`

### Pattern 3: Vague Skip Reasons ⚠️
```python
# BAD - doesn't explain what parameters are needed
pytest.skip("Test may require specific filter parameters")
```

**Affected tests:** `test_get_top_failed_advanced_with_filter`, `test_get_aggregated_measurements`

### Pattern 4: API Endpoint Mismatch ❓
```python
# QUESTIONABLE - is the test wrong or the API?
except ServerError as e:
    if e.status_code == 404:
        pytest.skip("Endpoint not available")
```

**Affected tests:** `test_add_log_message`, `test_internal_get_processes`, `test_get_groups`

---

## Recommended Actions

### Immediate (P0)
1. **Fix hidden failures** - `test_create_product_with_all_tags_at_once` should fail, not skip
2. **Remove "Requires live WATS server" skip** - All integration tests require this

### Short-term (P1)
3. **Add test data setup** - Tests should create their own data in fixtures
4. **Use `@pytest.mark.skipif`** for known server config issues
5. **Use `@pytest.mark.xfail`** for known API limitations

### Medium-term (P2)
6. **Verify API endpoints** - Check if 404 errors indicate wrong URLs or missing features
7. **Document WATS version requirements** - Some endpoints may require specific versions

---

## Test Count Summary

| Category | Count | Action Needed |
|----------|-------|---------------|
| 🔴 Hidden failures | 2 | Fix immediately |
| ⚠️ Data dependency | 4 | Add fixtures |
| ⚠️ Lazy skips | 3 | Define valid params |
| ❓ API mismatch | 4 | Investigate |
| **Total skipped** | **13** | |

---

## Files to Review

```
tests/domains/analytics/test_internal_endpoints.py  # Lines 214, 248
tests/domains/analytics/test_unit_flow.py           # Line 187
tests/domains/asset/test_workflow.py                # Lines 685, 693
tests/domains/process/test_models.py                # Lines 468, 487
tests/domains/product/test_integration.py           # Line 146
tests/domains/report/test_integration.py            # Line 409
tests/domains/report/test_report_builder.py         # Line 306
tests/domains/rootcause/test_integration.py         # Line 109
tests/domains/software/test_comprehensive.py        # Line 308
tests/integration/test_boxbuild.py                  # Line 1065
```
