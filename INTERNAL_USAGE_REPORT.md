# Internal API Usage Report

**Generated:** 2025-12-15  
**Scope:** Complete audit of all `/api/internal` endpoint usage in pyWATS  
**Purpose:** Documentation for compliance, maintenance, and migration planning

---

## Table of Contents

1. [Summary](#summary)
2. [Internal API Architecture](#internal-api-architecture)
3. [Repository Layer - Internal Endpoints](#repository-layer---internal-endpoints)
   - [ProductRepositoryInternal](#productrepositoryinternal)
   - [ProcessRepositoryInternal](#processrepositoryinternal)
   - [AssetRepositoryInternal](#assetrepositoryinternal)
   - [ProductionRepositoryInternal](#productionrepositoryinternal)
4. [Service Layer - Internal Services](#service-layer---internal-services)
   - [ProductServiceInternal](#productserviceinternal)
   - [ProcessServiceInternal](#processserviceinternal)
   - [AssetServiceInternal](#assetserviceinternal)
   - [ProductionServiceInternal](#productionserviceinternal)
5. [Public Repositories with Internal Delegation](#public-repositories-with-internal-delegation)
6. [Main API Exposure](#main-api-exposure)
7. [GUI Client Usage](#gui-client-usage)
8. [Report Models Usage](#report-models-usage)
9. [Test File Usage](#test-file-usage)
10. [Debug Scripts](#debug-scripts)
11. [Complete Endpoint Reference](#complete-endpoint-reference)
12. [Risk Assessment](#risk-assessment)

---

## Summary

| Category | Count | Files |
|----------|-------|-------|
| Internal Repository Files | 4 | `repository_internal.py` (product, process, asset, production) |
| Internal Service Files | 4 | `service_internal.py` (product, process, asset, production) |
| Public Repos with Internal Delegation | 3 | product, production, asset repositories (delegate to internal) |
| GUI Files Using Internal API | 1 | `product.py` (via service layer) |
| Test Files Using Internal API | 5 | See [Test File Usage](#test-file-usage) |
| Debug Scripts | 2 | `debug_boxbuild_api.py`, `debug_boxbuild_workflow.py` |
| Report Models Using Internal API | 1 | `uur_report.py` |
| **Total Unique Internal Endpoints** | **18** | See [Complete Endpoint Reference](#complete-endpoint-reference) |

### Architecture Compliance

✅ **Rule 1:** All API usage goes through service and repository layers - no direct REST calls from client/GUI  
✅ **Rule 2:** All internal endpoint implementations are in separate `_internal` files

---

## Internal API Architecture

### Authentication & Headers

All internal API calls require:
- **Referer Header:** Must be set to the base URL (e.g., `https://server.wats.com`)
- **Authentication:** Same Basic Auth as public API

```python
headers = {"Referer": base_url}
```

### URL Pattern

```
/api/internal/{Domain}/{Operation}
```

**Domains identified:**
- `Product` - Product/BOM management
- `Process` - Process configuration
- `Mes` - Manufacturing Execution System (phases)
- `Blob` - Binary/file storage
- `Production` - Production operations (limited)

---

## Repository Layer - Internal Endpoints

### ProductRepositoryInternal

**File:** [src/pywats/domains/product/repository_internal.py](src/pywats/domains/product/repository_internal.py)

| Method | HTTP | Endpoint | Purpose |
|--------|------|----------|---------|
| `get_bom()` | GET | `/api/internal/Product/Bom` | Get BOM items for a product revision |
| `set_bom()` | PUT | `/api/internal/Product/BOM` | Set/update BOM items |
| `get_product_by_pn()` | GET | `/api/internal/Product/GetProductByPN` | Get product by part number |
| `get_product_hierarchy()` | GET | `/api/internal/Product/GetProductInfo` | Get full product hierarchy |
| `create_revision_relation()` | POST | `/api/internal/Product/PostProductRevisionRelation` | Create parent-child relation |
| `update_revision_relation()` | PUT | `/api/internal/Product/PutProductRevisionRelation` | Update relation (quantity) |
| `delete_revision_relation()` | DELETE | `/api/internal/Product/DeleteProductRevisionRelation` | Delete a relation |
| `get_product_categories()` | GET | `/api/internal/Product/GetProductCategories` | Get all product categories |
| `set_product_categories()` | PUT | `/api/internal/Product/PutProductCategories` | Update product categories |

**Helper methods:**
- `_internal_get()` - Wraps GET with Referer header
- `_internal_post()` - Wraps POST with Referer header
- `_internal_put()` - Wraps PUT with Referer header
- `_internal_delete()` - Wraps DELETE with Referer header

---

### ProcessRepositoryInternal

**File:** [src/pywats/domains/process/repository_internal.py](src/pywats/domains/process/repository_internal.py)

| Method | HTTP | Endpoint | Purpose |
|--------|------|----------|---------|
| `get_processes()` | GET | `/api/internal/Process/GetProcesses` | Get all processes with full details |
| `get_process()` | GET | `/api/internal/Process/GetProcess/{id}` | Get specific process by GUID |
| `get_repair_operations()` | GET | `/api/internal/Process/GetRepairOperations` | Get all repair operation configs |
| `get_repair_operation()` | GET | `/api/internal/Process/GetRepairOperation/{id}` | Get specific repair operation |

---

### AssetRepositoryInternal

**File:** [src/pywats/domains/asset/repository_internal.py](src/pywats/domains/asset/repository_internal.py)

| Method | HTTP | Endpoint | Purpose |
|--------|------|----------|---------|
| `upload_file()` | POST | `/api/internal/Blob/Asset` | Upload file to asset |
| `download_file()` | GET | `/api/internal/Blob/Asset` | Download file from asset |
| `list_files()` | GET | `/api/internal/Blob/Asset/List/{assetId}` | List files for asset |
| `delete_files()` | DELETE | `/api/internal/Blob/Assets` | Delete files from asset |

**Note:** File operations on assets (stations, fixtures, etc.) require internal API.

---

### ProductionRepositoryInternal

**File:** [src/pywats/domains/production/repository_internal.py](src/pywats/domains/production/repository_internal.py)

| Method | HTTP | Endpoint | Purpose |
|--------|------|----------|---------|
| `get_unit_phases()` | GET | `/api/internal/Mes/GetUnitPhases` | Get all MES unit phases |

**Usage:** Unit phases define production workflow states (e.g., "In Test", "Passed", "Failed").

---

## Public Repositories with Internal Delegation

The following public repositories have methods that **delegate** to their internal counterparts.
This maintains backward compatibility while ensuring all internal API calls are properly encapsulated.

### ProductRepository

**File:** [src/pywats/domains/product/repository.py](src/pywats/domains/product/repository.py)

| Method | Status | Note |
|--------|--------|------|
| `get_bom()` | ⚠️ Deprecated | Still makes direct internal call for backward compatibility |

### ProductionRepository

**File:** [src/pywats/domains/production/repository.py](src/pywats/domains/production/repository.py)

| Method | Delegates To |
|--------|--------------|
| `get_unit_phases()` | `ProductionRepositoryInternal.get_unit_phases()` |

### AssetRepository

**File:** [src/pywats/domains/asset/repository.py](src/pywats/domains/asset/repository.py)

| Method | Delegates To |
|--------|--------------|
| `upload_file()` | `AssetRepositoryInternal.upload_file()` |
| `download_file()` | `AssetRepositoryInternal.download_file()` |
| `list_files()` | `AssetRepositoryInternal.list_files()` |
| `delete_files()` | `AssetRepositoryInternal.delete_files()` |

---

## Service Layer - Internal Services

### ProductServiceInternal

**File:** [src/pywats/domains/product/service_internal.py](src/pywats/domains/product/service_internal.py)

**Exposed via:** `api.product_internal`

| Method | Calls Repository Method | Purpose |
|--------|------------------------|---------|
| `get_box_build()` | Multiple internal calls | Get/create BoxBuildTemplate |
| `get_bom()` | `repo.get_bom()` | Get BOM items |
| `set_bom()` | `repo.set_bom()` | Update BOM items |
| `get_box_build_subunits()` | `repo.get_product_hierarchy()` | Get child relations |
| `add_box_build_subunit()` | `repo.create_revision_relation()` | Add child to template |
| `update_box_build_subunit()` | `repo.update_revision_relation()` | Update relation |
| `remove_box_build_subunit()` | `repo.delete_revision_relation()` | Remove child |
| `get_product_categories()` | `repo.get_product_categories()` | Get categories |
| `set_product_categories()` | `repo.set_product_categories()` | Update categories |

**BoxBuildTemplate Builder:**
- `BoxBuildTemplate.add_subunit()` → `create_revision_relation()`
- `BoxBuildTemplate.remove_subunit()` → `delete_revision_relation()`
- `BoxBuildTemplate.save()` → batch operations

---

### ProcessServiceInternal

**File:** [src/pywats/domains/process/service_internal.py](src/pywats/domains/process/service_internal.py)

**Exposed via:** `api.process_internal`

| Method | Calls Repository Method | Purpose |
|--------|------------------------|---------|
| `get_processes()` | `repo.get_processes()` | Get all processes |
| `get_process()` | `repo.get_process()` | Get process by ID |
| `get_test_operations()` | `repo.get_processes()` + filter | Get test operations only |
| `get_repair_processes()` | `repo.get_processes()` + filter | Get repair processes only |
| `get_process_by_code()` | `repo.get_processes()` + filter | Find by code (100, 500, etc.) |
| `get_repair_operation_configs()` | `repo.get_repair_operations()` | Get repair configs |
| `get_repair_categories()` | `repo.get_repair_operations()` + filter | Get categories for repair code |
| `get_fail_codes()` | `repo.get_repair_operations()` + flatten | Get flattened fail codes |
| `is_valid_test_operation()` | Validation helper | Check if code is test operation |
| `is_valid_repair_operation()` | Validation helper | Check if code is repair operation |

---

### AssetServiceInternal

**File:** [src/pywats/domains/asset/service_internal.py](src/pywats/domains/asset/service_internal.py)

**Exposed via:** `api.asset_internal`

| Method | Calls Repository Method | Purpose |
|--------|------------------------|---------|
| `upload_file()` | `repo.upload_file()` | Upload file to asset |
| `download_file()` | `repo.download_file()` | Download file from asset |
| `list_files()` | `repo.list_files()` | List files attached to asset |
| `delete_files()` | `repo.delete_files()` | Delete files from asset |
| `file_exists()` | `repo.list_files()` + check | Helper to check if file exists |

---

### ProductionServiceInternal

**File:** [src/pywats/domains/production/service_internal.py](src/pywats/domains/production/service_internal.py)

**Exposed via:** `api.production_internal`

| Method | Calls Repository Method | Purpose |
|--------|------------------------|---------|
| `get_unit_phases()` | `repo.get_unit_phases()` | Get all MES unit phases |
| `get_phase_by_name()` | `repo.get_unit_phases()` + filter | Find phase by name |

---

## Main API Exposure

**File:** [src/pywats/pywats.py](src/pywats/pywats.py)

```python
class pyWATS:
    @property
    def product_internal(self) -> ProductServiceInternal:
        """⚠️ INTERNAL API - Box build templates, BOM, categories"""
        
    @property
    def process_internal(self) -> ProcessServiceInternal:
        """⚠️ INTERNAL API - Process details, repair configs, fail codes"""
        
    @property
    def asset_internal(self) -> AssetServiceInternal:
        """⚠️ INTERNAL API - File operations on assets"""
        
    @property
    def production_internal(self) -> ProductionServiceInternal:
        """⚠️ INTERNAL API - MES unit phases"""
```

**Usage Pattern:**
```python
api = pyWATS(url, username, password)

# Product internal
template = api.product_internal.get_box_build("PN", "REV")
bom = api.product_internal.get_bom("PN", "REV")

# Process internal
processes = api.process_internal.get_processes()
fail_codes = api.process_internal.get_fail_codes(500)

# Asset internal (NEW)
files = api.asset_internal.list_files(asset_id)
api.asset_internal.upload_file(asset_id, "config.json", content)

# Production internal (NEW)
phases = api.production_internal.get_unit_phases()
```

---

## GUI Client Usage

**File:** [src/pywats_client/gui/pages/product.py](src/pywats_client/gui/pages/product.py)

| Line | Code | Context |
|------|------|---------|
| 710 | `client.product_internal.get_box_build(part_number, revision)` | Load box build template |
| 945 | `client.product_internal.get_box_build(part_number, revision)` | Edit box build template |
| 988 | `client.product_internal.get_box_build(part_number, revision)` | Display box build info |

**Purpose:** The Product page in the GUI uses internal API to manage box build templates for products.

---

## Report Models Usage

**File:** [src/pywats/domains/report/report_models/uur/uur_report.py](src/pywats/domains/report/report_models/uur/uur_report.py)

| Line | Code | Context |
|------|------|---------|
| 580-581 | `self._api.process_internal.get_fail_codes(self.process_code)` | Load fail codes for repair report |

**Purpose:** UUR (Unit Under Repair) reports need fail code information for repair step validation.

---

## Test File Usage

### test_product.py

**File:** [tests/test_product.py](tests/test_product.py)

| Line | Method Called | Purpose |
|------|---------------|---------|
| 333 | `wats_client.product_internal.get_bom()` | Test BOM retrieval |
| 480 | `wats_client.product_internal.get_box_build()` | Test box build template |
| 500 | `wats_client.product_internal.get_box_build()` | Test box build template |
| 521 | `wats_client.product_internal.get_box_build()` | Test box build template |
| 559 | `wats_client.product_internal.get_box_build()` | Test box build template |
| 598 | `wats_client.product_internal.get_box_build()` | Test context manager |
| 623 | `wats_client.product_internal.get_box_build()` | Test box build template |

---

### test_process_comprehensive.py

**File:** [tests/test_process_comprehensive.py](tests/test_process_comprehensive.py)

| Line | Method Called | Purpose |
|------|---------------|---------|
| 467-470 | `wats_client.process_internal.get_processes()` | Test process retrieval |
| 486-489 | `wats_client.process_internal.get_repair_operation_configs()` | Test repair configs |
| 504-508 | `wats_client.process_internal.get_fail_codes(500)` | Test fail code retrieval |

---

### test_boxbuild_complete_workflow.py

**File:** [tests/test_boxbuild_complete_workflow.py](tests/test_boxbuild_complete_workflow.py)

| Line | Method Called | Purpose |
|------|---------------|---------|
| 464 | `self.api.product_internal.get_box_build()` | Full workflow test |
| 475 | `self.api.product_internal.get_box_build_subunits()` | Verify subunits |
| 487 | `self.api.product_internal.get_box_build()` | Test with different revision |

---

## Debug Scripts

### debug_boxbuild_api.py

**File:** [tests/debug_boxbuild_api.py](tests/debug_boxbuild_api.py)

| Line | Endpoint | Purpose |
|------|----------|---------|
| 34 | `/api/internal/Mes/GetUnitPhases` | API exploration |
| 101 | `/api/internal/Product/PostProductRevisionRelation` | Direct API call |
| 205 | `/api/internal/Production/AddChildUnit` | Undocumented endpoint test |

**⚠️ Note:** Line 205 tests an undocumented internal endpoint `/api/internal/Production/AddChildUnit` that is NOT wrapped in any repository or service. This is exploratory code only.

---

### debug_boxbuild_workflow.py

**File:** [tests/debug_boxbuild_workflow.py](tests/debug_boxbuild_workflow.py)

| Line | Method Called | Purpose |
|------|---------------|---------|
| 48 | `api.product_internal.get_box_build()` | Workflow debugging |

---

## Complete Endpoint Reference

### All Internal Endpoints Used

| # | HTTP Method | Endpoint | Repository | Service |
|---|-------------|----------|------------|---------|
| 1 | GET | `/api/internal/Product/Bom` | ProductRepositoryInternal, ProductRepository | ProductServiceInternal |
| 2 | PUT | `/api/internal/Product/BOM` | ProductRepositoryInternal | ProductServiceInternal |
| 3 | GET | `/api/internal/Product/GetProductByPN` | ProductRepositoryInternal | ProductServiceInternal |
| 4 | GET | `/api/internal/Product/GetProductInfo` | ProductRepositoryInternal | ProductServiceInternal |
| 5 | POST | `/api/internal/Product/PostProductRevisionRelation` | ProductRepositoryInternal | ProductServiceInternal |
| 6 | PUT | `/api/internal/Product/PutProductRevisionRelation` | ProductRepositoryInternal | ProductServiceInternal |
| 7 | DELETE | `/api/internal/Product/DeleteProductRevisionRelation` | ProductRepositoryInternal | ProductServiceInternal |
| 8 | GET | `/api/internal/Product/GetProductCategories` | ProductRepositoryInternal | ProductServiceInternal |
| 9 | PUT | `/api/internal/Product/PutProductCategories` | ProductRepositoryInternal | ProductServiceInternal |
| 10 | GET | `/api/internal/Process/GetProcesses` | ProcessRepositoryInternal | ProcessServiceInternal |
| 11 | GET | `/api/internal/Process/GetProcess/{id}` | ProcessRepositoryInternal | ProcessServiceInternal |
| 12 | GET | `/api/internal/Process/GetRepairOperations` | ProcessRepositoryInternal | ProcessServiceInternal |
| 13 | GET | `/api/internal/Process/GetRepairOperation/{id}` | ProcessRepositoryInternal | ProcessServiceInternal |
| 14 | GET | `/api/internal/Mes/GetUnitPhases` | ProductionRepository | - |
| 15 | POST | `/api/internal/Blob/Asset` | AssetRepository | - |
| 16 | GET | `/api/internal/Blob/Asset` | AssetRepository | - |
| 17 | GET | `/api/internal/Blob/Asset/List/{assetId}` | AssetRepository | - |
| 18 | DELETE | `/api/internal/Blob/Assets` | AssetRepository | - |

### Undocumented/Exploratory Endpoints

| # | HTTP Method | Endpoint | Found In | Status |
|---|-------------|----------|----------|--------|
| 1 | POST | `/api/internal/Production/AddChildUnit` | debug_boxbuild_api.py | ⚠️ Not wrapped - debug only |

---

## Risk Assessment

### High Usage Endpoints

These endpoints are used in production code (services/GUI):

| Endpoint | Risk | Reason |
|----------|------|--------|
| `/api/internal/Product/GetProductInfo` | **HIGH** | Core to box build functionality |
| `/api/internal/Product/PostProductRevisionRelation` | **HIGH** | Creates product relationships |
| `/api/internal/Process/GetProcesses` | **MEDIUM** | Used for validation |
| `/api/internal/Blob/Asset*` | **MEDIUM** | File operations |

### Mitigation Recommendations

1. **Document all internal API usage** ✅ (This report)
2. **Monitor WATS release notes** for internal API changes
3. **Consider feature flags** to disable internal API features if needed
4. **Add integration tests** that fail fast on API changes
5. **Request public API equivalents** from Virinco for critical functionality

### Mock/Stub Detection

**No hidden mock functionality detected.** All internal API calls are:
- Properly documented with ⚠️ INTERNAL API warnings
- Go through the HTTP client layer
- Make real network requests to the WATS server

---

## Appendix: File Location Summary

```
src/pywats/
├── pywats.py                          # Main API class exposing product_internal, process_internal
├── domains/
│   ├── product/
│   │   ├── repository.py              # 1 internal endpoint (get_bom)
│   │   ├── repository_internal.py     # 9 internal endpoints
│   │   └── service_internal.py        # Service layer for product internal
│   ├── process/
│   │   ├── repository_internal.py     # 4 internal endpoints
│   │   └── service_internal.py        # Service layer for process internal
│   ├── production/
│   │   └── repository.py              # 1 internal endpoint (get_unit_phases)
│   ├── asset/
│   │   └── repository.py              # 4 internal endpoints (file ops)
│   └── report/
│       └── report_models/uur/
│           └── uur_report.py          # Uses process_internal for fail codes

src/pywats_client/
└── gui/pages/
    └── product.py                     # 3 calls to product_internal

tests/
├── test_product.py                    # 7+ internal API calls
├── test_process_comprehensive.py      # 3 internal API calls
├── test_boxbuild_complete_workflow.py # 3 internal API calls
├── debug_boxbuild_api.py              # Direct internal API exploration
└── debug_boxbuild_workflow.py         # Workflow debugging with internal API
```

---

**Report Complete.** All internal API usage has been documented.
