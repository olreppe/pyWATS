# Internal Endpoint Audit — All Domain Modules

**Date:** February 18, 2026  
**Purpose:** Comprehensive audit of ALL internal API endpoint usage across every domain module, auxiliary file, and shared utility in pyWATS.  
**Cross-reference:** `PUBLIC_API_ENDPOINT_REQUIREMENTS.md` (covers Report, Product, Production, Software, Asset, Process only)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Complete File Listing Per Domain](#2-complete-file-listing-per-domain)
3. [Complete Internal Endpoint Inventory](#3-complete-internal-endpoint-inventory)
4. [Endpoints NOT Covered in Public API Requirements Doc](#4-endpoints-not-covered-in-public-api-requirements-doc)
5. [Cross-Module Internal Endpoint Dependencies](#5-cross-module-internal-endpoint-dependencies)
6. [Auxiliary File Inventory](#6-auxiliary-file-inventory)
7. [Naming Patterns](#7-naming-patterns)

---

## 1. Executive Summary

| Module | Standard Files | Auxiliary Files | Internal Endpoints Used | In Public API Doc? |
|--------|:---:|:---:|:---:|:---:|
| **Report** | 5 + report_models/ (20 files) | 3 (`filter_builders.py`, `query_helpers.py`, `import_mode.py`) | 0 (direct) | ✅ Yes |
| **Product** | 4 | 0 (consolidated into `async_service.py`) | 14 | ✅ Yes |
| **Production** | 4 | 0 | 21 | ✅ Yes |
| **Software** | 4 | 0 | 13 | ✅ Yes |
| **Asset** | 4 | 0 | 4 | ✅ Yes |
| **Process** | 3 | 0 | 4 | ⚠️ Partially (2 of 4) |
| **Analytics** | 4 | 0 | 12 | ❌ **NOT COVERED** |
| **RootCause** | 4 | 0 | 0 | N/A (no internal usage) |
| **SCIM** | 3 | 0 | 0 | N/A (no internal usage) |
| **Total** | 35 + 20 report_models | 6 | **68** | **12 MISSING** |

### Key Finding: **Analytics module is completely missing from the public API requirements doc** — it uses 12 internal endpoints across 3 controller paths (`/api/internal/UnitFlow`, `/api/internal/App`, `/api/internal/Trigger`).

### Key Finding: **Process module has 2 additional internal endpoints** (`GetProcesses`, `GetProcess/{id}`) not covered in the public API requirements doc Section 6 (which only covers the 2 repair operation endpoints).

---

## 2. Complete File Listing Per Domain

### 2.1 Report (`src/pywats/domains/report/`)

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init, exports |
| `async_repository.py` | Standard | HTTP calls to Report API (all public) |
| `async_service.py` | Standard | Business logic for report queries/submissions |
| `enums.py` | Standard | `ReportType`, `ImportMode`, etc. |
| `models.py` | Standard | `ReportHeader`, `WATSFilter`, etc. |
| `service.pyi` | Standard | Type stubs |
| **`filter_builders.py`** | **Auxiliary** | OData filter string builders (`build_serial_filter`, `build_date_range_filter`, `combine_filters`) — no API calls |
| **`query_helpers.py`** | **Auxiliary** | OData query param helpers (`build_query_params`, `get_expand_fields`, `is_uut_report_type`) — no API calls |
| **`import_mode.py`** | **Auxiliary** | `ImportMode` context variable, `apply_failure_propagation()` — no API calls |
| `report_models/` | Subpackage | 20 files for UUT/UUR report model hierarchy (see below) |

**Report Models subpackage** (`report_models/`):

| File | Description |
|------|-------------|
| `__init__.py` | Package init |
| `additional_data.py` | Additional data model |
| `asset.py` | Asset reference in reports |
| `attachment.py` | Report attachments |
| `binary_data.py` | Binary data handling |
| `chart.py` | Chart data models |
| `common_types.py` | `ReportStatus` and shared types |
| `misc_info.py` | Misc info fields |
| `report.py` | Base report model |
| `report_info.py` | Report info model |
| `sub_unit.py` | Sub-unit model |
| `wats_base.py` | Base WATS model class |
| `USER_GUIDE.md` | Usage documentation |
| `uur/` | UUR-specific (4 files: `__init__`, `uur_failure`, `uur_info`, `uur_report`, `uur_sub_unit`) |
| `uut/` | UUT-specific (3+ files: `__init__`, `uut_report`, `uut_info`, `step` + `steps/` subpackage with 13 files) |

**Internal endpoint usage: NONE** — Report module uses only public endpoints. However, **UUR creation depends on Process internal endpoints** (cross-module dependency — see Section 5).

---

### 2.2 Product (`src/pywats/domains/product/`)

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init, exports |
| `async_repository.py` | Standard | HTTP calls including 14 internal endpoints |
| `async_service.py` | Standard | Business logic for product management + `AsyncBoxBuildTemplate` fluent builder (1296 lines - consolidated Feb 2026) |
| `enums.py` | Standard | Product enums |
| `models.py` | Standard | `Product`, `ProductRevision`, `ProductRevisionRelation` |
| `service.pyi` | Standard | Type stubs |

---

### 2.3 Production (`src/pywats/domains/production/`)

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init; imports `Product`, `ProductRevision` from product domain |
| `async_repository.py` | Standard | HTTP calls including 21 internal endpoints |
| `async_service.py` | Standard | Business logic for production management |
| `enums.py` | Standard | Production enums |
| `models.py` | Standard | Production models; TYPE_CHECKING import of `Product`, `ProductRevision` |
| `service.pyi` | Standard | Type stubs |

**No auxiliary files.** Cross-module dependency: imports from `product.models`.

---

### 2.4 Software (`src/pywats/domains/software/`)

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init |
| `async_repository.py` | Standard | HTTP calls including 13 internal endpoints |
| `async_service.py` | Standard | Business logic for software distribution |
| `enums.py` | Standard | Software enums |
| `models.py` | Standard | Software package models |
| `service.pyi` | Standard | Type stubs |

**No auxiliary files.**

---

### 2.5 Asset (`src/pywats/domains/asset/`)

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init |
| `async_repository.py` | Standard | HTTP calls including 4 internal blob endpoints |
| `async_service.py` | Standard | Business logic for asset management |
| `enums.py` | Standard | Asset enums |
| `models.py` | Standard | Asset models |
| `service.pyi` | Standard | Type stubs |

**No auxiliary files.**

---

### 2.6 Process (`src/pywats/domains/process/`)

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init |
| `async_repository.py` | Standard | HTTP calls including 4 internal endpoints |
| `async_service.py` | Standard | Business logic with caching for process lookups |
| `models.py` | Standard | `ProcessInfo`, `RepairOperationConfig`, `RepairCategory` |
| `service.pyi` | Standard | Type stubs |

**No auxiliary files.** Note: No `enums.py` in this module.

---

### 2.7 Analytics (`src/pywats/domains/analytics/`) — ❌ NOT IN PUBLIC API DOC

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init; documents all 12 internal endpoints in docstring |
| `async_repository.py` | Standard | HTTP calls including 12 internal endpoints |
| `async_service.py` | Standard | Business logic; 15+ internal API methods |
| `enums.py` | Standard | `Dimension`, `KPI`, `RepairDimension`, `RepairKPI`, `DimensionBuilder`, `AlarmType` |
| `models.py` | Standard | `UnitFlowResult`, `UnitFlowNode`, `UnitFlowLink`, `MeasurementListItem`, `StepStatusItem`, `AlarmLog` |
| `service.pyi` | Standard | Type stubs |

**No auxiliary files.** Cross-module dependency: imports `WATSFilter`, `ReportHeader` from `report.models`.

---

### 2.8 RootCause (`src/pywats/domains/rootcause/`)

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init |
| `async_repository.py` | Standard | HTTP calls — **all public endpoints** |
| `async_service.py` | Standard | Business logic for RCA ticketing |
| `enums.py` | Standard | RootCause enums |
| `models.py` | Standard | RCA ticket models |
| `service.pyi` | Standard | Type stubs |

**No auxiliary files. No internal endpoint usage.**

---

### 2.9 SCIM (`src/pywats/domains/scim/`)

| File | Type | Description |
|------|------|-------------|
| `__init__.py` | Standard | Package init |
| `async_repository.py` | Standard | HTTP calls — **all public endpoints** |
| `async_service.py` | Standard | Business logic for user provisioning |
| `models.py` | Standard | SCIM user/group models |
| `service.pyi` | Standard | Type stubs |

**No auxiliary files. No internal endpoint usage.** Note: No `enums.py`.

---

## 3. Complete Internal Endpoint Inventory

### 3.1 Production Domain (21 endpoints)

| # | Endpoint | Method | File | Function | Data Provided | In Doc? |
|---|----------|--------|------|----------|---------------|:---:|
| 1 | `/api/internal/Production/isConnected` | GET | `async_repository.py` | `is_connected()` | Connection status bool | ✅ |
| 2 | `/api/internal/Mes/GetUnitPhases` | GET | `async_repository.py` | `get_unit_phases_internal()` | All MES unit phases | ✅ |
| 3 | `/api/internal/Production/GetSites` | GET | `async_repository.py` | `get_sites()` | Production site list | ✅ |
| 4 | `/api/internal/Production/GetUnit` | GET | `async_repository.py` | `get_unit_internal()` | Unit by SN (PN optional) | ✅ |
| 5 | `/api/internal/Production/GetUnitInfo` | GET | `async_repository.py` | `get_unit_info()` | Unit info summary | ✅ |
| 6 | `/api/internal/Production/GetUnitHierarchy` | GET | `async_repository.py` | `get_unit_hierarchy()` | Parent/child unit tree | ✅ |
| 7 | `/api/internal/Production/GetUnitStateHistory` | GET | `async_repository.py` | `get_unit_state_history()` | Unit state change log | ✅ |
| 8 | `/api/internal/Production/GetUnitPhase` | GET | `async_repository.py` | `get_unit_phase()` | Current unit phase | ✅ |
| 9 | `/api/internal/Production/GetUnitProcess` | GET | `async_repository.py` | `get_unit_process()` | Current unit process step | ✅ |
| 10 | `/api/internal/Production/GetUnitContents` | GET | `async_repository.py` | `get_unit_contents()` | Unit BOM/components | ✅ |
| 11 | `/api/internal/Production/CreateUnit` | POST | `async_repository.py` | `create_unit_internal()` | Create unit | ✅ |
| 12 | `/api/internal/Production/AddChildUnit` | POST | `async_repository.py` | `add_child_unit_internal()` | Add child with validation | ✅ |
| 13 | `/api/internal/Production/RemoveChildUnit` | POST | `async_repository.py` | `remove_child_unit_internal()` | Remove child unit | ✅ |
| 14 | `/api/internal/Production/RemoveAllChildUnits` | POST | `async_repository.py` | `remove_all_child_units()` | Remove all children | ✅ |
| 15 | `/api/internal/Production/CheckChildUnits` | GET | `async_repository.py` | `check_child_units_internal()` | Validate child units | ✅ |
| 16 | `/api/internal/Production/SerialNumbers` | GET | `async_repository.py` | `get_serial_numbers_internal()` | SN range query | ✅ |
| 17 | `/api/internal/Production/SerialNumbers/Count` | GET | `async_repository.py` | `get_serial_numbers_count()` | SN count in range | ✅ |
| 18 | `/api/internal/Production/SerialNumbers/Free` | PUT | `async_repository.py` | `free_serial_numbers()` | Free reserved SNs | ✅ |
| 19 | `/api/internal/Production/SerialNumbers/Free` | DELETE | `async_repository.py` | `delete_free_serial_numbers()` | Delete free SNs | ✅ |
| 20 | `/api/internal/Production/SerialNumbers/Ranges` | GET | `async_repository.py` | `get_serial_number_ranges()` | SN ranges | ✅ |
| 21 | `/api/internal/Production/SerialNumbers/Statistics` | GET | `async_repository.py` | `get_serial_number_statistics()` | SN pool stats | ✅ |

---

### 3.2 Product Domain (14 endpoints)

| # | Endpoint | Method | File | Function | Data Provided | In Doc? |
|---|----------|--------|------|----------|---------------|:---:|
| 1 | `/api/internal/Product/Bom` | GET | `async_repository.py` | `get_bom_internal()` | Full BOM detail | ✅ |
| 2 | `/api/internal/Product/BOM` | PUT | `async_repository.py` | `upload_bom()` | BOM upload/update | ✅ |
| 3 | `/api/internal/Product/GetProductInfo` | GET | `async_repository.py` | `get_product_info()` | Product hierarchy | ✅ |
| 4 | `/api/internal/Product/GetProductByPN` | GET | `async_repository.py` | `get_product_by_pn()` | Product w/ revision relations | ✅ |
| 5 | `/api/internal/Product/PostProductRevisionRelation` | POST | `async_repository.py` | `create_revision_relation()` | Create revision relation | ✅ |
| 6 | `/api/internal/Product/PutProductRevisionRelation` | PUT | `async_repository.py` | `update_revision_relation()` | Update revision relation | ✅ |
| 7 | `/api/internal/Product/DeleteProductRevisionRelation` | DELETE | `async_repository.py` | `delete_revision_relation()` | Delete revision relation | ✅ |
| 8 | `/api/internal/Product/GetGroupsForProduct` | GET | `async_repository.py` | `get_groups_for_product()` | Groups containing product | ✅ |
| 9 | `/api/internal/Product/GetProductCategories` | GET | `async_repository.py` | `get_product_categories()` | All categories | ✅ |
| 10 | `/api/internal/Product/PutProductCategories` | PUT | `async_repository.py` | `save_product_categories()` | Save categories | ✅ |
| 11 | `/api/internal/Product/GetProductTags` | GET | `async_repository.py` | `get_product_tags()` | Product tags | ✅ |
| 12 | `/api/internal/Product/PutProductTags` | PUT | `async_repository.py` | `save_product_tags()` | Set product tags | ✅ |
| 13 | `/api/internal/Product/GetRevisionTags` | GET | `async_repository.py` | `get_revision_tags()` | Revision tags | ✅ |
| 14 | `/api/internal/Product/PutRevisionTags` | PUT | `async_repository.py` | `save_revision_tags()` | Set revision tags | ✅ |

**Note:** Endpoints 5-7 are also called indirectly from `async_service.py` → `AsyncBoxBuildTemplate.save()` (consolidated Feb 2026).

---

### 3.3 Software Domain (13 endpoints)

| # | Endpoint | Method | File | Function | Data Provided | In Doc? |
|---|----------|--------|------|----------|---------------|:---:|
| 1 | `/api/internal/Software/isConnected` | GET | `async_repository.py` | `is_connected()` | Connection status | ✅ |
| 2 | `/api/internal/Software/File/{id}` | GET | `async_repository.py` | `get_file_metadata()` | File metadata by UUID | ✅ |
| 3 | `/api/internal/Software/CheckFile` | GET | `async_repository.py` | `check_file()` | File existence check | ✅ |
| 4 | `/api/internal/Software/PostPackageFolder` | POST | `async_repository.py` | `create_package_folder()` | Create folder | ✅ |
| 5 | `/api/internal/Software/UpdatePackageFolder` | POST | `async_repository.py` | `update_package_folder()` | Update folder | ✅ |
| 6 | `/api/internal/Software/DeletePackageFolder` | POST | `async_repository.py` | `delete_package_folder()` | Delete folder | ✅ |
| 7 | `/api/internal/Software/DeletePackageFolderFiles` | POST | `async_repository.py` | `delete_package_folder_files()` | Delete folder files | ✅ |
| 8 | `/api/internal/Software/GetPackageHistory` | GET | `async_repository.py` | `get_package_history()` | Version/status history | ✅ |
| 9 | `/api/internal/Software/GetPackageDownloadHistory` | GET | `async_repository.py` | `get_package_download_history()` | Client download history | ✅ |
| 10 | `/api/internal/Software/GetRevokedPackages` | GET | `async_repository.py` | `get_revoked_packages()` | Revoked package list | ✅ |
| 11 | `/api/internal/Software/GetAvailablePackages` | GET | `async_repository.py` | `get_available_packages()` | Newer versions | ✅ |
| 12 | `/api/internal/Software/GetSoftwareEntityDetails` | GET | `async_repository.py` | `get_software_entity_details()` | Detailed package info | ✅ |
| 13 | `/api/internal/Software/Log` | GET | `async_repository.py` | `log_download()` | Download audit log | ✅ |

---

### 3.4 Asset Domain (4 endpoints)

| # | Endpoint | Method | File | Function | Data Provided | In Doc? |
|---|----------|--------|------|----------|---------------|:---:|
| 1 | `/api/internal/Blob/Asset/{id}` | POST | `async_repository.py` | `upload_asset_file()` | File upload | ✅ |
| 2 | `/api/internal/Blob/Asset/{id}/{fileName}` | GET | `async_repository.py` | `download_asset_file()` | File download | ✅ |
| 3 | `/api/internal/Blob/Asset/List/{id}` | GET | `async_repository.py` | `list_asset_files()` | File listing | ✅ |
| 4 | `/api/internal/Blob/Assets` | DELETE | `async_repository.py` | `delete_asset_files()` | Delete files | ✅ |

---

### 3.5 Process Domain (4 endpoints)

| # | Endpoint | Method | File | Function | Data Provided | In Doc? |
|---|----------|--------|------|----------|---------------|:---:|
| 1 | `/api/internal/Process/GetRepairOperations` | GET | `async_repository.py` | `get_repair_operations()` | All repair op configs | ✅ |
| 2 | `/api/internal/Process/GetRepairOperation/{id}` | GET | `async_repository.py` | `get_repair_operation()` | Single repair op config | ✅ |
| 3 | `/api/internal/Process/GetProcesses` | GET | `async_repository.py` | `get_processes_detailed()` | All processes w/ full detail | ❌ **MISSING** |
| 4 | `/api/internal/Process/GetProcess/{id}` | GET | `async_repository.py` | `get_process()` | Single process by GUID | ❌ **MISSING** |

**Doc gap:** Section 6 ("Process Loading") of `PUBLIC_API_ENDPOINT_REQUIREMENTS.md` mentions endpoints 3-4 in the "Other Internal Process Endpoints (Lower Priority)" paragraph but does NOT include them in the formal table. They have no suggested public route listed.

---

### 3.6 Analytics Domain (12 endpoints) — ❌ ENTIRELY MISSING FROM DOC

| # | Endpoint | Method | File | Function | Data Provided | In Doc? |
|---|----------|--------|------|----------|---------------|:---:|
| 1 | `/api/internal/UnitFlow` | POST | `async_repository.py` | `query_unit_flow()` | Complete unit flow diagram (nodes + links) | ❌ |
| 2 | `/api/internal/UnitFlow/Links` | GET | `async_repository.py` | `get_unit_flow_links()` | Flow links (edges between operations) | ❌ |
| 3 | `/api/internal/UnitFlow/Nodes` | GET | `async_repository.py` | `get_unit_flow_nodes()` | Flow nodes (operations/stations) | ❌ |
| 4 | `/api/internal/UnitFlow/SN` | POST | `async_repository.py` | `query_unit_flow_by_serial_numbers()` | Flow for specific serial numbers | ❌ |
| 5 | `/api/internal/UnitFlow/SplitBy` | POST | `async_repository.py` | `set_unit_flow_split_by()` | Flow split by dimension | ❌ |
| 6 | `/api/internal/UnitFlow/UnitOrder` | POST | `async_repository.py` | `set_unit_flow_order()` | Reordered flow by criteria | ❌ |
| 7 | `/api/internal/UnitFlow/Units` | GET | `async_repository.py` | `get_unit_flow_units()` | Individual units in flow | ❌ |
| 8 | `/api/internal/App/MeasurementList` | GET | `async_repository.py` | `get_measurement_list()` | Measurement list w/ filters | ❌ |
| 9 | `/api/internal/App/MeasurementList` | POST | `async_repository.py` | `get_measurement_list_simple()` | Measurement list (POST body) | ❌ |
| 10 | `/api/internal/App/StepStatusList` | GET | `async_repository.py` | `get_step_status_list()` | Step status list w/ filters | ❌ |
| 11 | `/api/internal/App/StepStatusList` | POST | `async_repository.py` | `get_step_status_list_simple()` | Step status list (POST body) | ❌ |
| 12 | `/api/internal/Trigger/GetAlarmAndNotificationLogs` | POST | `async_repository.py` | `get_alarm_logs()` | Alarm/notification log entries | ❌ |

**Additional internal endpoint usage — also via internal routes but using GET/POST on same URL:**

| # | Endpoint | Method | File | Service Method | Data Provided |
|---|----------|--------|------|----------------|---------------|
| 13 | `/api/internal/App/TopFailed` | GET | `async_repository.py` | `get_top_failed_simple()` | Top failed steps (GET w/ params) |
| 14 | `/api/internal/App/TopFailed` | POST | `async_repository.py` | `get_top_failed_advanced()` | Top failed steps (POST w/ body) |

**Total unique Analytics internal URL paths: 10. Total including method variants: 14.**

---

### 3.7 RootCause Domain — 0 internal endpoints

All endpoints are public (`/api/RootCause/*`). No internal API usage.

### 3.8 SCIM Domain — 0 internal endpoints

All endpoints are public (`/api/SCIM/v2/*`). No internal API usage.

---

## 4. Endpoints NOT Covered in Public API Requirements Doc

### 4.1 Analytics Module (12-14 endpoints) — COMPLETELY MISSING

The entire Analytics module is absent from `PUBLIC_API_ENDPOINT_REQUIREMENTS.md`. This represents the **largest gap** in the document.

**Impact:** The Analytics module provides critical manufacturing intelligence:
- **Unit Flow analysis** — production flow visualization, bottleneck detection
- **Measurement filtering** — step-level measurement queries
- **Step status analysis** — step pass/fail status queries  
- **Top failed analysis** — advanced failure pareto (internal variant with more filters)
- **Alarm/notification logs** — triggered alarm history

**Recommended action:** Add a new **Section 7: Analytics Module** to `PUBLIC_API_ENDPOINT_REQUIREMENTS.md`.

**Suggested public routes:**

| # | Current Internal | Method | Suggested Public Route |
|---|-----------------|--------|----------------------|
| 1 | `/api/internal/UnitFlow` | POST | `/api/Analytics/UnitFlow` |
| 2 | `/api/internal/UnitFlow/Links` | GET | `/api/Analytics/UnitFlow/Links` |
| 3 | `/api/internal/UnitFlow/Nodes` | GET | `/api/Analytics/UnitFlow/Nodes` |
| 4 | `/api/internal/UnitFlow/SN` | POST | `/api/Analytics/UnitFlow/SerialNumbers` |
| 5 | `/api/internal/UnitFlow/SplitBy` | POST | `/api/Analytics/UnitFlow/SplitBy` |
| 6 | `/api/internal/UnitFlow/UnitOrder` | POST | `/api/Analytics/UnitFlow/Order` |
| 7 | `/api/internal/UnitFlow/Units` | GET | `/api/Analytics/UnitFlow/Units` |
| 8 | `/api/internal/App/MeasurementList` | GET/POST | `/api/Analytics/MeasurementList` |
| 9 | `/api/internal/App/StepStatusList` | GET/POST | `/api/Analytics/StepStatusList` |
| 10 | `/api/internal/App/TopFailed` | GET/POST | `/api/Analytics/TopFailed` |
| 11 | `/api/internal/Trigger/GetAlarmAndNotificationLogs` | POST | `/api/Analytics/AlarmLogs` |

### 4.2 Process Module — 2 Additional Endpoints

Two Process internal endpoints are **mentioned in prose** in the doc (Section 6, "Other Internal Process Endpoints (Lower Priority)") but lack formal table entries with suggested public routes:

| # | Current Internal | Method | Suggested Public Route | Notes |
|---|-----------------|--------|----------------------|-------|
| 1 | `/api/internal/Process/GetProcesses` | GET | `/api/Process/Processes` or `/api/App/ProcessesDetailed` | Returns admin-level detail (ProcessID, processIndex, state, Properties) |
| 2 | `/api/internal/Process/GetProcess/{id}` | GET | `/api/Process/{id}` | Get single process by GUID |

---

## 5. Cross-Module Internal Endpoint Dependencies

### 5.1 Report → Process (DOCUMENTED)

| Consumer | Provider | Internal Endpoint | Purpose |
|----------|----------|-------------------|---------|
| Report (UUR creation) | Process | `GET /api/internal/Process/GetRepairOperations` | Get failure categories/codes for UUR failure entries |
| Report (UUR creation) | Process | `GET /api/internal/Process/GetRepairOperation/{id}` | Get specific repair config |

**Status:** ✅ Documented in `PUBLIC_API_ENDPOINT_REQUIREMENTS.md` Section 1 and Section 6.

### 5.2 Analytics → Report (Model Import)

| Consumer | Provider | Import | Purpose |
|----------|----------|--------|---------|
| `analytics/async_repository.py` | `report.models` | `WATSFilter`, `ReportHeader` | Shared filter/header models for analytics queries |
| `analytics/async_service.py` | `report.models` | `WATSFilter`, `ReportHeader` | Pass-through for service methods |

**Note:** This is a **model import** only, not an endpoint dependency. Both modules use the same `WATSFilter` model to construct query parameters.

### 5.3 Production → Product (Model Import)

| Consumer | Provider | Import | Purpose |
|----------|----------|--------|---------|
| `production/__init__.py` | `product.models` | `Product`, `ProductRevision` | Re-exports product models for convenience |
| `production/models.py` | `product.models` | `Product`, `ProductRevision` | TYPE_CHECKING reference for type hints |

**Note:** Model import only, not an endpoint dependency.

### 5.4 Product Box Build → Product Internal (Same-Module)

| Consumer | Provider | Internal Endpoint | Purpose |
|----------|----------|-------------------|---------|
| `product/async_service.py` → `AsyncBoxBuildTemplate.save()` | `product/async_repository.py` | `POST .../PostProductRevisionRelation` | Create sub-unit relation |
| `product/async_service.py` → `AsyncBoxBuildTemplate.save()` | `product/async_repository.py` | `PUT .../PutProductRevisionRelation` | Update sub-unit relation |
| `product/async_service.py` → `AsyncBoxBuildTemplate.save()` | `product/async_repository.py` | `DELETE .../DeleteProductRevisionRelation` | Delete sub-unit relation |
| `product/async_service.py` → `AsyncBoxBuildTemplate.save()` | `product/async_repository.py` | `GET .../GetProductByPN` | Load product w/ relations |
| `product/async_service.py` → `AsyncBoxBuildTemplate.save()` | `product/async_repository.py` | `GET .../GetProductInfo` | Load product hierarchy |

**Note:** Same-module internal calls (Product → Product internal). `AsyncBoxBuildTemplate` is now part of `async_service.py` (consolidated Feb 2026). All documented in public API doc.
- **RootCause, SCIM:** No internal endpoint usage at all.

---

## 6. Auxiliary File Inventory

### Definition
"Auxiliary files" are domain module files that are NOT one of the standard patterns:
`__init__.py`, `async_service.py`, `async_repository.py`, `models.py`, `enums.py`, `service.pyi`

### Complete Listing

| Module | File | Class(es) | Purpose | Uses Internal Endpoints? |
|--------|------|-----------|---------|:---:|
| **Report** | `filter_builders.py` | _(functions only)_ | OData filter string builders: `build_serial_filter()`, `build_part_number_filter()`, `build_date_range_filter()`, `combine_filters()` | No |
| **Report** | `query_helpers.py` | _(functions only)_ | OData query helpers: `build_query_params()`, `get_expand_fields()`, `is_uut_report_type()` | No |
| **Report** | `import_mode.py` | _(functions + ContextVar)_ | Import mode context: `get_import_mode()`, `set_import_mode()`, `is_active_mode()`, `apply_failure_propagation()` | No |
| **Report** | `report_models/` (20 files) | Multiple model classes | UUT/UUR report object hierarchy | No |

### Key Observation

The Product domain previously had 3 auxiliary files (`box_build.py`, `async_box_build.py`, `sync_box_build.py`) with internal endpoint usage. **As of February 2026, these were consolidated into `async_service.py`** to eliminate naming confusion. `AsyncBoxBuildTemplate` (originally 433 lines) is now part of the main service file (1296 lines total). The Report auxiliary files remain as pure utility/model code with no API calls.

---

## 7. Naming Patterns

### Standard File Naming (per domain)

| File | Purpose | All Domains? |
|------|---------|:---:|
| `__init__.py` | Package init and exports | ✅ All 9 |
| `async_repository.py` | HTTP calls (public + internal) | ✅ All 9 |
| `async_service.py` | Business logic layer | ✅ All 9 |
| `models.py` | Pydantic data models | ✅ All 9 |
| `enums.py` | Domain-specific enumerations | 7/9 (missing in Process, SCIM) |
| `service.pyi` | Type stubs for sync service | ✅ All 9 |

### Internal Endpoint Naming Patterns

| Pattern | Controller | Example | Modules |
|---------|-----------|---------|---------|
| `/api/internal/{Module}/{Action}` | Named by module | `/api/internal/Production/GetUnit` | Production, Product, Software, Process |
| `/api/internal/Blob/{Module}` | Blob controller | `/api/internal/Blob/Asset/{id}` | Asset |
| `/api/internal/{Feature}` | Feature-specific | `/api/internal/UnitFlow` | Analytics |
| `/api/internal/App/{Action}` | App controller | `/api/internal/App/MeasurementList` | Analytics |
| `/api/internal/Mes/{Action}` | MES controller | `/api/internal/Mes/GetUnitPhases` | Production |
| `/api/internal/Trigger/{Action}` | Trigger controller | `/api/internal/Trigger/GetAlarmAndNotificationLogs` | Analytics |

### Route Constant Naming

All internal route constants follow the pattern: `Routes.{Domain}.Internal.{CONSTANT}`

```
Routes.Production.Internal.GET_UNIT
Routes.Product.Internal.BOM
Routes.Software.Internal.IS_CONNECTED
Routes.Asset.Internal.BLOB_BASE
Routes.Process.Internal.GET_PROCESSES
Routes.Analytics.Internal.UNIT_FLOW
```

### Auxiliary File Naming Patterns

| Pattern | Example | Used By |
|---------|---------|---------|
| `{utility}_builders.py` | `filter_builders.py` | Report |
| `{utility}_helpers.py` | `query_helpers.py` | Report |
| `{concept}_mode.py` | `import_mode.py` | Report |
| `report_models/` (subpackage) | – | Report |

**Note:** Product domain previously used `{concept}.py`, `async_{concept}.py`, `sync_{concept}.py` patterns (e.g., `box_build.py`). These were consolidated into `async_service.py` in February 2026.

---

## Appendix A: Routes.py Internal Route Summary

All internal route constants defined in `src/pywats/core/routes.py`:

| Class | Constants/Methods | Count |
|-------|------------------|:---:|
| `Routes.Production.Internal` | `IS_CONNECTED`, `GET_UNIT`, `GET_UNIT_INFO`, `GET_UNIT_HIERARCHY`, `GET_UNIT_STATE_HISTORY`, `GET_UNIT_PHASE`, `GET_UNIT_PROCESS`, `GET_UNIT_CONTENTS`, `CREATE_UNIT`, `ADD_CHILD_UNIT`, `REMOVE_CHILD_UNIT`, `REMOVE_ALL_CHILD_UNITS`, `CHECK_CHILD_UNITS`, `SERIAL_NUMBERS`, `SERIAL_NUMBERS_COUNT`, `SERIAL_NUMBERS_FREE`, `SERIAL_NUMBERS_RANGES`, `SERIAL_NUMBERS_STATISTICS`, `GET_SITES`, `GET_UNIT_PHASES` | 20 |
| `Routes.Product.Internal` | `BOM`, `BOM_UPLOAD`, `GET_PRODUCT_INFO`, `GET_PRODUCT_BY_PN`, `POST_REVISION_RELATION`, `PUT_REVISION_RELATION`, `DELETE_REVISION_RELATION`, `GET_CATEGORIES`, `PUT_CATEGORIES`, `GET_PRODUCT_TAGS`, `PUT_PRODUCT_TAGS`, `GET_REVISION_TAGS`, `PUT_REVISION_TAGS`, `GET_GROUPS_FOR_PRODUCT` | 14 |
| `Routes.Asset.Internal` | `BLOB_BASE`, `upload()`, `download()`, `list_files()`, `DELETE_FILES` | 5 |
| `Routes.Software.Internal` | `IS_CONNECTED`, `CHECK_FILE`, `POST_FOLDER`, `UPDATE_FOLDER`, `DELETE_FOLDER`, `DELETE_FOLDER_FILES`, `GET_HISTORY`, `GET_DOWNLOAD_HISTORY`, `GET_REVOKED`, `GET_AVAILABLE`, `GET_DETAILS`, `LOG`, `file()` | 13 |
| `Routes.Analytics.Internal` | `UNIT_FLOW`, `UNIT_FLOW_LINKS`, `UNIT_FLOW_NODES`, `UNIT_FLOW_SN`, `UNIT_FLOW_SPLIT_BY`, `UNIT_FLOW_UNIT_ORDER`, `UNIT_FLOW_UNITS`, `MEASUREMENT_LIST`, `STEP_STATUS_LIST`, `TOP_FAILED`, `ALARM_LOGS` | 11 |
| `Routes.Process.Internal` | `GET_PROCESSES`, `GET_REPAIR_OPERATIONS`, `get_process()`, `get_repair_operation()` | 4 |
| **Total route definitions** | | **67** |

## Appendix B: pywats_client Layer

The `src/pywats_client/` layer (70 files) does **not directly reference** internal API routes or `Routes.*.Internal` constants. It operates through the `pywats` domain services (which encapsulate the internal endpoint calls). No additional internal endpoint usage found in the client layer.
