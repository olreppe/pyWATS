# Exception Handling Overhaul Plan

**Date:** January 2026  
**Status:** ✅ COMPLETED (January 2026)  
**Objective:** Fix ErrorHandler usage across all domains to match the Analytics pattern  
**Completion Note:** All domains migrated to async repositories with consistent ErrorHandler usage. See [EXCEPTION_HANDLING_EVALUATION.md](../EXCEPTION_HANDLING_EVALUATION.md) for verification.

---

## Current State Analysis

### ✅ CORRECT Pattern (Analytics Domain)

```python
# Analytics repository.py - THE CORRECT WAY
response = self._http_client.get("/api/App/Version")
data = self._error_handler.handle_response(
    response, operation="get_version", allow_empty=True
)
return str(data) if data else None
```

### ❌ INCORRECT Pattern (Most Other Domains)

```python
# Asset repository.py - THE WRONG WAY
response = self._http_client.get(f"/api/Asset/{asset_id}")
if response.is_success and response.data:  # ❌ Manual check, no ErrorHandler
    return Asset.model_validate(response.data)
return None  # ❌ Silent failure
```

---

## What ErrorHandler Provides

When `handle_response()` is called, it:

1. **Maps HTTP errors to proper exceptions:**
   - 400 → `ValidationError`
   - 401 → `AuthenticationError`
   - 403 → `AuthorizationError`
   - 404 → `NotFoundError` (STRICT) / `None` (LENIENT)
   - 409 → `ConflictError`
   - 5xx → `ServerError`

2. **Handles empty responses based on mode:**
   - STRICT: Raises `EmptyResponseError` if `allow_empty=False`
   - LENIENT: Returns `None`

3. **Provides consistent error context:**
   - Operation name for debugging
   - Structured error details

---

## Domains to Fix (Priority Order)

| # | Domain | Repository Files | Est. Methods | Priority |
|---|--------|------------------|--------------|----------|
| 1 | Asset | `repository.py`, `repository_internal.py` | ~21 | HIGH |
| 2 | Process | `repository.py`, `repository_internal.py` | ~8 | HIGH |
| 3 | Product | `repository.py`, `repository_internal.py` | ~30 | HIGH |
| 4 | Production | `repository.py`, `repository_internal.py` | ~46 | HIGH |
| 5 | Report | `repository.py` | ~12 | HIGH |
| 6 | RootCause | `repository.py` | ~8 | MEDIUM |
| 7 | Software | `repository.py`, `repository_internal.py` | ~30 | MEDIUM |

---

## Fix Pattern for Each Method

### Before (Incorrect)
```python
def get_asset(self, asset_id: str) -> Optional[Asset]:
    response = self._http_client.get(f"/api/Asset/{asset_id}")
    if response.is_success and response.data:
        return Asset.model_validate(response.data)
    return None
```

### After (Correct)
```python
def get_asset(self, asset_id: str) -> Optional[Asset]:
    response = self._http_client.get(f"/api/Asset/{asset_id}")
    data = self._error_handler.handle_response(
        response, operation="get_asset", allow_empty=True
    )
    if data:
        return Asset.model_validate(data)
    return None
```

---

## Execution Plan

### Phase 1: Asset Domain
**File:** `src/pywats/domains/asset/repository.py`
**Methods to fix:** ~15

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `get_all` | GET | True |
| `get_by_id` | GET | True |
| `get_by_serial_number` | GET | True |
| `save` | PUT | False |
| `delete` | DELETE | True |
| `get_asset_type` | GET | True |
| `get_status` | GET | True |
| `set_status` | PUT | False |
| `reset_status` | POST | False |
| `calibrate` | POST | False |
| `maintenance` | POST | False |
| `get_log` | GET | True |
| `add_message` | POST | False |
| `get_types` | GET | True |
| `create_type` | PUT | False |
| `get_children` | GET | True |

**File:** `src/pywats/domains/asset/repository_internal.py`
**Methods to fix:** ~4

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `upload_file` | POST | False |
| `download_file` | GET | True |
| `list_files` | GET | True |
| `delete_files` | DELETE | True |

---

### Phase 2: Process Domain
**File:** `src/pywats/domains/process/repository.py`
**Methods to fix:** ~1

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `get_processes` | GET | True |

**File:** `src/pywats/domains/process/repository_internal.py`
**Methods to fix:** ~6

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `_internal_get_json` | GET | True |
| `get_internal_processes` | GET | True |
| `get_internal_process` | GET | True |
| `get_repair_operations` | GET | True |
| `get_repair_operation` | GET | True |
| `get_repair_categories` | GET | True |

---

### Phase 3: Product Domain
**File:** `src/pywats/domains/product/repository.py`
**Methods to fix:** ~14

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `get_product_views` | GET | True |
| `get_products` | GET | True |
| `get_product` | GET | True |
| `get_products_by_name` | GET | True |
| `get_revisions` | GET | True |
| `get_revision` | GET | True |
| `create_revision` | POST | False |
| `update_revision` | PUT | False |
| `post_xml` | POST | False |
| `get_with_odata` | GET | True |
| `get_categories` | GET | True |
| `get_category` | GET | True |
| `get_vendors` | GET | True |
| `delete_vendor_mapping` | DELETE | True |

**File:** `src/pywats/domains/product/repository_internal.py`
**Methods to fix:** ~10

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `get_bom` | GET | True |
| `update_bom` | PUT | False |
| `get_subunits` | GET | True |
| `get_product_info` | GET | True |
| `create_revision` | POST | False |
| `update_revision` | PUT | False |
| `delete_revision` | DELETE | True |
| `get_internal_categories` | GET | True |
| `update_categories` | PUT | False |

---

### Phase 4: Production Domain
**File:** `src/pywats/domains/production/repository.py`
**Methods to fix:** ~19

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `get_unit` | GET | True |
| `get_unit_by_id` | GET | True |
| `create_unit` | POST | False |
| `update_unit` | PUT | False |
| `get_units_by_phase` | GET | True |
| `get_serial_numbers` | GET | True |
| `allocate_serial_numbers` | POST | False |
| `get_recent_serial_numbers` | GET | True |
| `get_active_serial_numbers` | GET | True |
| `get_stations` | GET | True |
| `get_station` | GET | True |
| `create_station` | POST | False |
| `update_station` | PUT | False |
| `delete_station` | DELETE | True |
| `get_subunits` | GET | True |
| `add_subunit` | POST | False |
| `remove_subunit` | DELETE | True |
| `get_xml_count` | GET | True |
| `get_unit_phases` | GET | True |

**File:** `src/pywats/domains/production/repository_internal.py`
**Methods to fix:** ~26

All internal methods need ErrorHandler added and used.

---

### Phase 5: Report Domain
**File:** `src/pywats/domains/report/repository.py`
**Methods to fix:** ~10

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `get_report` | GET | True |
| `get_reports` | GET | True |
| `post_wsjf` | POST | False |
| `get_uut_report` | GET | True |
| `get_uur_report` | GET | True |
| `post_attachments` | POST | True |
| `get_attachment` | GET | True |
| `post_attachment` | POST | False |
| `delete_report` | DELETE | True |
| `get_report_files` | GET | True |

---

### Phase 6: RootCause Domain
**File:** `src/pywats/domains/rootcause/repository.py`
**Methods to fix:** ~8

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `get_ticket` | GET | True |
| `get_tickets` | GET | True |
| `create_ticket` | POST | False |
| `update_ticket` | PUT | False |
| `add_update` | POST | False |
| `archive_tickets` | POST | False |
| `get_attachment` | GET | True |
| `upload_attachment` | POST | False |

---

### Phase 7: Software Domain
**File:** `src/pywats/domains/software/repository.py`
**Methods to fix:** ~12

| Method | HTTP | allow_empty |
|--------|------|-------------|
| `get_packages` | GET | True |
| `get_package` | GET | True |
| `get_packages_by_status` | GET | True |
| `get_packages_by_name` | GET | True |
| `create_package` | POST | False |
| `update_package` | PUT | False |
| `delete_package` | DELETE | True |
| `delete_package_file` | DELETE | True |
| `set_status` | POST | False |
| `get_package_files` | GET | True |
| `upload_file` | POST | False |
| `add_tag` | POST | False |

**File:** `src/pywats/domains/software/repository_internal.py`
**Methods to fix:** ~14

All internal methods need ErrorHandler added and used.

---

## Service Layer Validation

After fixing repositories, add `ValueError` validation to service methods:

```python
# Example pattern for service methods
def create_asset(self, serial_number: str, ...) -> Optional[Asset]:
    """Create an asset.
    
    Raises:
        ValueError: If serial_number is empty or whitespace
    """
    if not serial_number or not serial_number.strip():
        raise ValueError("serial_number is required and cannot be empty")
    # ... rest of method
```

---

## Verification Steps

After each phase:
1. Run domain-specific tests
2. Verify STRICT mode raises exceptions
3. Verify LENIENT mode returns None for 404
4. Check no silent failures remain

---

## Summary

| Phase | Domain | Files | Methods | Est. Time |
|-------|--------|-------|---------|-----------|
| 1 | Asset | 2 | ~19 | 15 min |
| 2 | Process | 2 | ~7 | 10 min |
| 3 | Product | 2 | ~24 | 20 min |
| 4 | Production | 2 | ~45 | 30 min |
| 5 | Report | 1 | ~10 | 10 min |
| 6 | RootCause | 1 | ~8 | 10 min |
| 7 | Software | 2 | ~26 | 20 min |

**Total:** ~139 methods to fix across 12 files

---

## Ready to Start?

Say **"Start Phase 1"** to begin with the Asset domain, or specify which phase to start with.
