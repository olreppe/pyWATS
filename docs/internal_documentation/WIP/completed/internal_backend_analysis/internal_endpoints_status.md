# Internal Backend Endpoints Analysis

> **Analysis Date**: January 26, 2026  
> **Branch**: feature/separate-service-gui-mode  
> **Total Internal Endpoints**: 68 across 6 modules

---

## 1. Executive Summary

### Status Overview

| Module | Internal Endpoints | Files | Proper ⚠️ Marking | Critical for Features |
|--------|-------------------|-------|-------------------|----------------------|
| **Analytics** | 13 endpoints | 3 files | ✅ All marked | Unit Flow, Measurement Filtering |
| **Asset** | 4 endpoints | 3 files | ✅ All marked | File Attachments |
| **Process** | 4 endpoints | 4 files | ✅ All marked | Detailed Process Info, Repair Ops |
| **Product** | 14 endpoints | 3 files | ✅ All marked | Box Build, Categories, Tags |
| **Production** | 20 endpoints | 3 files | ✅ All marked | Serial Numbers, Unit Hierarchy |
| **Software** | 13 endpoints | 3 files | ✅ All marked | Package Management |
| **TOTAL** | **68 endpoints** | **19 files** | ✅ **All properly marked** | |

### Key Findings

1. ✅ **All internal endpoints are properly flagged** with `⚠️ INTERNAL` warnings in docstrings
2. ✅ **Routes are centralized** in `pywats/core/routes.py` with `Routes.*.Internal` nested classes
3. ✅ **Consistent helper pattern** using `_internal_get()` and `_internal_post()` with Referer headers
4. ⚠️ **68 internal endpoints in use** - significant dependency on undocumented API
5. ⚠️ **No public API alternatives** exist for most internal endpoint features

---

## 2. Module-by-Module Analysis

### 2.1 Analytics Module

**Files**: 
- `src/pywats/domains/analytics/async_repository.py`
- `src/pywats/domains/analytics/async_service.py`
- `src/pywats/domains/analytics/service_internal.py`

#### Internal Endpoints Used

| Endpoint | Method | Purpose | Public Alternative |
|----------|--------|---------|-------------------|
| `POST /api/internal/UnitFlow` | `query_unit_flow()` | Query production flow with filters | ❌ None |
| `GET /api/internal/UnitFlow/Links` | `get_unit_flow_links()` | Get Sankey diagram edges | ❌ None |
| `GET /api/internal/UnitFlow/Nodes` | `get_unit_flow_nodes()` | Get Sankey diagram nodes | ❌ None |
| `POST /api/internal/UnitFlow/SN` | `get_unit_flow_by_sn()` | Trace serial number flow | ❌ None |
| `POST /api/internal/UnitFlow/SplitBy` | `split_unit_flow()` | Split by dimension | ❌ None |
| `POST /api/internal/UnitFlow/UnitOrder` | `set_unit_order()` | Control unit ordering | ❌ None |
| `GET /api/internal/UnitFlow/Units` | `get_unit_flow_units()` | Get units in flow | ❌ None |
| `GET /api/internal/App/MeasurementList` | `get_measurement_list()` | Simple measurement query | ❌ None |
| `POST /api/internal/App/MeasurementList` | `get_measurement_list_filtered()` | Filtered measurements | ❌ None |
| `GET /api/internal/App/StepStatusList` | `get_step_status_list()` | Simple step status query | ❌ None |
| `POST /api/internal/App/StepStatusList` | `get_step_status_list_filtered()` | Filtered step status | ❌ None |
| `GET /api/internal/App/TopFailed` | `get_top_failed()` | Top failed steps (simple) | ✅ Partial: `/api/App/TopFailed` |
| `POST /api/internal/App/TopFailed` | `get_top_failed_filtered()` | Top failed with filters | ❌ None |

#### Why Internal API is Necessary

1. **Unit Flow Analysis** - The entire unit flow visualization feature (Sankey diagrams, production path tracing) has NO public API equivalent. This powers the WATS dashboard's production flow visualization.

2. **Measurement/Step Filtering** - Advanced filtering by step path XML, measurement names with regex support. The public measurement endpoints don't support these filter capabilities.

3. **Top Failed Enhancement** - The internal POST version supports the full `WATSFilter` object for complex drill-down analysis.

#### Recommended Public API Extensions

```
# Proposed new public endpoints:

GET  /api/Analytics/UnitFlow
POST /api/Analytics/UnitFlow  (with filter body)
GET  /api/Analytics/UnitFlow/{serialNumber}
GET  /api/Analytics/MeasurementList (extend existing Measurements)
GET  /api/Analytics/StepStatusList
POST /api/App/TopFailed  (add filter body support to existing)
```

---

### 2.2 Asset Module

**Files**:
- `src/pywats/domains/asset/async_repository.py`
- `src/pywats/domains/asset/async_service.py`
- `src/pywats/domains/asset/service_internal.py`

#### Internal Endpoints Used

| Endpoint | Method | Purpose | Public Alternative |
|----------|--------|---------|-------------------|
| `POST /api/internal/Blob/Asset/{id}` | `upload_file()` | Upload file attachment | ❌ None |
| `GET /api/internal/Blob/Asset/{id}/{fileName}` | `download_file()` | Download file attachment | ❌ None |
| `GET /api/internal/Blob/Asset/List/{assetId}` | `list_files()` | List asset attachments | ❌ None |
| `DELETE /api/internal/Blob/Assets` | `delete_files()` | Delete asset files | ❌ None |

#### Why Internal API is Necessary

The entire asset file attachment system uses internal Blob API. The public Asset API has no file management endpoints at all.

**Missing from Public API:**
- Upload files to assets (calibration certs, maintenance docs, photos)
- Download asset attachments
- List/enumerate asset files
- Delete asset files

#### Recommended Public API Extensions

```
# Proposed new public endpoints:

POST   /api/Asset/{id}/Files              # Upload file
GET    /api/Asset/{id}/Files              # List files
GET    /api/Asset/{id}/Files/{fileName}   # Download file
DELETE /api/Asset/{id}/Files/{fileName}   # Delete file
DELETE /api/Asset/{id}/Files              # Delete multiple (body: fileNames[])
```

---

### 2.3 Process Module

**Files**:
- `src/pywats/domains/process/async_repository.py`
- `src/pywats/domains/process/async_service.py`
- `src/pywats/domains/process/repository_internal.py` *(deprecated)*
- `src/pywats/domains/process/service_internal.py` *(deprecated)*

#### Internal Endpoints Used

| Endpoint | Method | Purpose | Public Alternative |
|----------|--------|---------|-------------------|
| `GET /api/internal/Process/GetProcesses` | `get_processes_detailed()` | Full process details | ✅ Partial: `/api/App/Processes` |
| `GET /api/internal/Process/GetProcess/{id}` | `get_process()` | Single process by GUID | ❌ None |
| `GET /api/internal/Process/GetRepairOperations` | `get_repair_operations()` | All repair operation configs | ❌ None |
| `GET /api/internal/Process/GetRepairOperation/{id}` | `get_repair_operation()` | Single repair operation | ❌ None |

#### Why Internal API is Necessary

1. **Process Details** - Public `/api/App/Processes` returns minimal info (code, name, description). Internal version adds:
   - ProcessID (GUID)
   - processIndex
   - state
   - Properties dictionary
   - isTestOperation, isRepairOperation, isWipOperation flags

2. **Repair Operations** - The entire repair operation configuration retrieval has no public endpoint. This is needed for UUR (Unit Under Repair) report creation.

#### Recommended Public API Extensions

```
# Proposed public endpoint extensions:

GET /api/Process                         # Same as /api/App/Processes but with full details
GET /api/Process/{id}                    # Get process by GUID or code
GET /api/Process/RepairOperations        # Get repair operation configs
GET /api/Process/RepairOperation/{id}    # Get single repair operation
```

---

### 2.4 Product Module

**Files**:
- `src/pywats/domains/product/async_repository.py`
- `src/pywats/domains/product/async_service.py`
- `src/pywats/domains/product/service_internal.py`

#### Internal Endpoints Used

| Endpoint | Method | Purpose | Public Alternative |
|----------|--------|---------|-------------------|
| `GET /api/internal/Product/Bom` | `get_bom_internal()` | Get BOM items | ✅ `/api/Product/{pn}/{rev}/BOM` |
| `PUT /api/internal/Product/BOM` | `upload_bom()` | Upload BOM items | ❌ None |
| `GET /api/internal/Product/GetProductInfo` | `get_product_info()` | Full product hierarchy | ❌ None |
| `GET /api/internal/Product/GetProductByPN` | `get_product_by_pn()` | Product with relations | ❌ None |
| `POST /api/internal/Product/PostProductRevisionRelation` | `create_revision_relation()` | Create box build relation | ❌ None |
| `PUT /api/internal/Product/PutProductRevisionRelation` | `update_revision_relation()` | Update box build relation | ❌ None |
| `DELETE /api/internal/Product/DeleteProductRevisionRelation` | `delete_revision_relation()` | Delete box build relation | ❌ None |
| `GET /api/internal/Product/GetProductCategories` | `get_categories()` | Get all categories | ❌ None |
| `PUT /api/internal/Product/PutProductCategories` | `save_categories()` | Save categories | ❌ None |
| `GET /api/internal/Product/GetProductTags` | `get_product_tags()` | Get product tags | ❌ None |
| `PUT /api/internal/Product/PutProductTags` | `set_product_tags()` | Set product tags | ❌ None |
| `GET /api/internal/Product/GetRevisionTags` | `get_revision_tags()` | Get revision tags | ❌ None |
| `PUT /api/internal/Product/PutRevisionTags` | `set_revision_tags()` | Set revision tags | ❌ None |
| `GET /api/internal/Product/GetGroupsForProduct` | `get_groups_for_product()` | Get product groups | ✅ Partial: Groups exist |

#### Why Internal API is Necessary

1. **Box Build Management** - The entire box build (multi-level product assembly) feature requires internal API:
   - Product revision relations define what child products make up a parent
   - No public CRUD for these relations
   - Essential for manufacturing hierarchical products

2. **Categories & Tags** - Product categorization and tagging system:
   - Categories are site-specific product groupings
   - Tags enable custom metadata on products and revisions
   - No public API for either

3. **BOM Upload** - While BOM read has a public endpoint, BOM creation/modification requires internal API.

#### Recommended Public API Extensions

```
# Proposed public endpoint extensions (backward compatible):

# Box Build Relations
GET    /api/Product/{pn}/Relations                    # Get all revision relations
POST   /api/Product/{pn}/{rev}/Relations              # Create relation
PUT    /api/Product/{pn}/{rev}/Relations/{childPn}    # Update relation
DELETE /api/Product/{pn}/{rev}/Relations/{childPn}    # Delete relation

# Categories & Tags
GET    /api/Product/Categories                        # Get all categories
PUT    /api/Product/Categories                        # Save categories
GET    /api/Product/{pn}/Tags                         # Get product tags
PUT    /api/Product/{pn}/Tags                         # Set product tags
GET    /api/Product/{pn}/{rev}/Tags                   # Get revision tags
PUT    /api/Product/{pn}/{rev}/Tags                   # Set revision tags

# BOM Management
PUT    /api/Product/{pn}/{rev}/BOM                    # Upload/update BOM (add to existing GET)
```

---

### 2.5 Production Module

**Files**:
- `src/pywats/domains/production/async_repository.py`
- `src/pywats/domains/production/async_service.py`
- `src/pywats/domains/production/repository_internal.py` *(deprecated)*

#### Internal Endpoints Used

| Endpoint | Method | Purpose | Public Alternative |
|----------|--------|---------|-------------------|
| `GET /api/internal/Production/isConnected` | `is_connected()` | Check module availability | ❌ None |
| `GET /api/internal/Production/GetUnit` | `get_unit_internal()` | Flexible unit lookup | ✅ `/api/Production/Unit/{sn}/{pn}` |
| `GET /api/internal/Production/GetUnitInfo` | `get_unit_info()` | Unit extended info | ❌ None |
| `GET /api/internal/Production/GetUnitHierarchy` | `get_unit_hierarchy()` | Full unit tree | ❌ None |
| `GET /api/internal/Production/GetUnitStateHistory` | `get_unit_state_history()` | State change log | ❌ None |
| `GET /api/internal/Production/GetUnitPhase` | `get_unit_phase()` | Current phase | ❌ None |
| `GET /api/internal/Production/GetUnitProcess` | `get_unit_process()` | Current process | ❌ None |
| `GET /api/internal/Production/GetUnitContents` | `get_unit_contents()` | Unit BOM/components | ❌ None |
| `POST /api/internal/Production/CreateUnit` | `create_unit()` | Create new unit | ❌ None |
| `POST /api/internal/Production/AddChildUnit` | `add_child_unit()` | Box build assembly | ✅ `/api/Production/AddChildUnit` |
| `POST /api/internal/Production/RemoveChildUnit` | `remove_child_unit()` | Box build disassembly | ✅ `/api/Production/RemoveChildUnit` |
| `POST /api/internal/Production/RemoveAllChildUnits` | `remove_all_children()` | Clear all children | ❌ None |
| `GET /api/internal/Production/CheckChildUnits` | `check_child_units()` | Validate box build | ✅ `/api/Production/CheckChildUnits` |
| `GET /api/internal/Production/SerialNumbers` | `find_serial_numbers()` | Search in range | ❌ None |
| `GET /api/internal/Production/SerialNumbers/Count` | `count_serial_numbers()` | Count in range | ❌ None |
| `PUT /api/internal/Production/SerialNumbers/Free` | `free_serial_numbers()` | Free reserved | ❌ None |
| `DELETE /api/internal/Production/SerialNumbers/Free` | `delete_free_serials()` | Delete free serials | ❌ None |
| `GET /api/internal/Production/SerialNumbers/Ranges` | `get_serial_ranges()` | Get defined ranges | ❌ None |
| `GET /api/internal/Production/SerialNumbers/Statistics` | `get_serial_statistics()` | Usage statistics | ❌ None |
| `GET /api/internal/Production/GetSites` | `get_sites()` | Production sites | ❌ None |
| `GET /api/internal/Mes/GetUnitPhases` | `get_unit_phases()` | MES phase definitions | ✅ `/api/Production/Phases` |

#### Why Internal API is Necessary

1. **Unit Hierarchy & State** - Core production tracking features:
   - `GetUnitHierarchy` - Full parent/child tree for box build products
   - `GetUnitStateHistory` - Audit trail of state changes
   - `GetUnitContents` - What components are in a unit

2. **Unit Creation** - The `CreateUnit` endpoint creates units with validation. Public API only implicitly creates units via report submission.

3. **Serial Number Management** - Complete serial number lifecycle:
   - Range management (get defined ranges)
   - Search within ranges
   - Free/delete reserved serial numbers
   - Statistics (usage, available counts)
   - Public API only has Take and ByRange

4. **Sites** - Production site definitions have no public endpoint.

#### Recommended Public API Extensions

```
# Proposed public endpoint extensions:

# Unit Management
GET    /api/Production/Unit/{sn}                      # Get unit (flexible lookup)
GET    /api/Production/Unit/{sn}/Hierarchy            # Get unit hierarchy
GET    /api/Production/Unit/{sn}/StateHistory         # Get state change history
GET    /api/Production/Unit/{sn}/Contents             # Get unit BOM contents
POST   /api/Production/Unit                           # Create unit explicitly
DELETE /api/Production/Unit/{sn}/{pn}/Children        # Remove all children

# Serial Number Management  
GET    /api/Production/SerialNumbers/Search           # Search in range
GET    /api/Production/SerialNumbers/Count            # Count in range
PUT    /api/Production/SerialNumbers/Free             # Free reserved serials
DELETE /api/Production/SerialNumbers/Free             # Delete free serials
GET    /api/Production/SerialNumbers/Ranges           # Get all defined ranges
GET    /api/Production/SerialNumbers/Statistics       # Get usage statistics

# Sites
GET    /api/Production/Sites                          # Get production sites
```

---

### 2.6 Software Module

**Files**:
- `src/pywats/domains/software/async_repository.py`
- `src/pywats/domains/software/async_service.py`
- `src/pywats/domains/software/service_internal.py`

#### Internal Endpoints Used

| Endpoint | Method | Purpose | Public Alternative |
|----------|--------|---------|-------------------|
| `GET /api/internal/Software/isConnected` | `is_connected()` | Check module availability | ❌ None |
| `GET /api/internal/Software/File/{id}` | `get_file()` | File metadata by ID | ❌ None |
| `GET /api/internal/Software/CheckFile` | `check_file()` | Pre-upload deduplication | ❌ None |
| `POST /api/internal/Software/PostPackageFolder` | `create_folder()` | Create package folder | ❌ None |
| `POST /api/internal/Software/UpdatePackageFolder` | `update_folder()` | Update folder metadata | ❌ None |
| `POST /api/internal/Software/DeletePackageFolder` | `delete_folder()` | Delete package folder | ❌ None |
| `POST /api/internal/Software/DeletePackageFolderFiles` | `delete_files()` | Delete files from folder | ❌ None |
| `GET /api/internal/Software/GetPackageHistory` | `get_history()` | Version history by tags | ❌ None |
| `GET /api/internal/Software/GetPackageDownloadHistory` | `get_download_history()` | Client download log | ❌ None |
| `GET /api/internal/Software/GetRevokedPackages` | `get_revoked()` | Check for revoked packages | ❌ None |
| `GET /api/internal/Software/GetAvailablePackages` | `check_updates()` | Check for new versions | ❌ None |
| `GET /api/internal/Software/GetSoftwareEntityDetails` | `get_details()` | Full package details | ✅ `/api/Software/Package/{id}` |
| `GET /api/internal/Software/Log` | `log_download()` | Log download event | ❌ None |

#### Why Internal API is Necessary

1. **Package Folder Management** - The public API only manages packages at the top level. Internal API handles:
   - Creating folder structure within packages
   - Updating folder metadata
   - Deleting folders and files

2. **File Operations** - Pre-upload file checking and metadata retrieval not in public API.

3. **Client Update Management** - Critical for WATS Client:
   - `GetAvailablePackages` - Check if client needs updates
   - `GetRevokedPackages` - Check if installed packages have been revoked
   - `GetDownloadHistory` - Track what was downloaded when
   - `Log` - Record download events for auditing

4. **Package History** - Version history and changelog tracking.

#### Recommended Public API Extensions

```
# Proposed public endpoint extensions:

# Package Structure
POST   /api/Software/Package/{id}/Folders             # Create folder
PUT    /api/Software/Package/{id}/Folders/{folderId}  # Update folder
DELETE /api/Software/Package/{id}/Folders/{folderId}  # Delete folder
DELETE /api/Software/Package/{id}/Files               # Delete files (body: fileIds[])

# Package Metadata
GET    /api/Software/Package/{id}/History             # Get version history
GET    /api/Software/File/{id}                        # Get file metadata

# Client Update Management
GET    /api/Software/CheckUpdates                     # Check for available updates
GET    /api/Software/CheckRevoked                     # Check for revoked packages
GET    /api/Software/DownloadHistory                  # Get download history
POST   /api/Software/LogDownload                      # Log download event
```

---

## 3. Public API Extension Recommendations

### Prioritization

Based on feature importance and usage frequency:

#### Priority 1 - Critical (Blocks core functionality)

| Module | Feature | Proposed Endpoints |
|--------|---------|-------------------|
| **Production** | Serial Number Management | `/api/Production/SerialNumbers/*` |
| **Production** | Unit Hierarchy | `/api/Production/Unit/{sn}/Hierarchy` |
| **Product** | Box Build Relations | `/api/Product/{pn}/Relations/*` |
| **Asset** | File Attachments | `/api/Asset/{id}/Files/*` |

#### Priority 2 - High (Important for advanced features)

| Module | Feature | Proposed Endpoints |
|--------|---------|-------------------|
| **Analytics** | Unit Flow | `/api/Analytics/UnitFlow/*` |
| **Analytics** | Measurement Filtering | Enhanced `/api/Analytics/Measurements` |
| **Software** | Client Updates | `/api/Software/CheckUpdates`, `/api/Software/CheckRevoked` |
| **Process** | Repair Operations | `/api/Process/RepairOperations/*` |

#### Priority 3 - Nice to Have

| Module | Feature | Proposed Endpoints |
|--------|---------|-------------------|
| **Product** | Categories & Tags | `/api/Product/Categories`, `/api/Product/{pn}/Tags` |
| **Software** | Package Structure | `/api/Software/Package/{id}/Folders/*` |
| **Production** | Sites | `/api/Production/Sites` |

### Backward Compatibility Guidelines

1. **Extend, don't replace** - Add new optional parameters to existing endpoints where possible
2. **POST for complex queries** - Add POST variants with filter bodies alongside existing GET endpoints
3. **Version in Accept header** - Use `Accept: application/vnd.wats.v2+json` for enhanced responses
4. **Deprecation path** - Keep internal endpoints working during migration period

---

## 4. Current Warning Implementation

### Standard Warning Pattern

All internal methods follow this documentation pattern:

```python
async def internal_method(self, ...) -> ...:
    """
    Method description.
    
    GET /api/internal/Module/Endpoint
    
    ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
    
    This method uses an undocumented internal endpoint that may change
    without notice in future WATS server versions.
    
    Args:
        ...
    Returns:
        ...
    """
```

### Routes Organization

Internal routes are isolated in nested `Internal` classes:

```python
class Routes:
    class Production:
        # Public routes
        UNIT = "/api/Production/Unit"
        
        class Internal:
            """⚠️ Internal Production API routes."""
            GET_UNIT = "/api/internal/Production/GetUnit"
```

### Verification Status

| Module | Docstring Warning | Route Isolation | Helper Methods |
|--------|------------------|-----------------|----------------|
| Analytics | ✅ All methods | ✅ `Routes.Analytics.Internal` | ✅ `_internal_get/post` |
| Asset | ✅ All methods | ✅ `Routes.Asset.Internal` | ✅ `_internal_get/post` |
| Process | ✅ All methods | ✅ `Routes.Process.Internal` | ✅ `_internal_get` |
| Product | ✅ All methods | ✅ `Routes.Product.Internal` | ✅ `_internal_get/post` |
| Production | ✅ All methods | ✅ `Routes.Production.Internal` | ✅ `_internal_get/post` |
| Software | ✅ All methods | ✅ `Routes.Software.Internal` | ✅ `_internal_get/post` |

---

## 5. Technical Implementation Notes

### Referer Header Requirement

All internal API calls require the `Referer` header set to the WATS server base URL:

```python
async def _internal_get(self, endpoint: str, params: Dict = None) -> Any:
    response = await self._http_client.get(
        endpoint,
        params=params,
        headers={"Referer": self._base_url}  # Required!
    )
    return response.data if response.is_success else None
```

### Error Handling Differences

Internal endpoints may return different error formats:
- Public API: Standardized error responses with error codes
- Internal API: May return raw exceptions or different status codes

### Authentication

Internal endpoints use the same authentication as public API (API token or session cookie), but some may require additional permissions not exposed in the public RBAC model.

---

## 6. Action Items

### For pyWATS Development

1. [ ] Keep internal warning documentation up to date
2. [ ] Add deprecation warnings when public alternatives become available
3. [ ] Document any breaking changes to internal endpoints in CHANGELOG
4. [ ] Consider feature flags for internal API usage

### For WATS Backend Team (Recommendations)

1. [ ] Review Priority 1 endpoints for public API promotion
2. [ ] Define versioning strategy for new public endpoints
3. [ ] Consider OpenAPI/Swagger documentation for promoted endpoints
4. [ ] Establish deprecation timeline for internal endpoints

---

## Appendix: Complete Internal Endpoint Inventory

### A. Production Module (20 endpoints)

```
GET  /api/internal/Production/isConnected
GET  /api/internal/Production/GetUnit
GET  /api/internal/Production/GetUnitInfo
GET  /api/internal/Production/GetUnitHierarchy
GET  /api/internal/Production/GetUnitStateHistory
GET  /api/internal/Production/GetUnitPhase
GET  /api/internal/Production/GetUnitProcess
GET  /api/internal/Production/GetUnitContents
POST /api/internal/Production/CreateUnit
POST /api/internal/Production/AddChildUnit
POST /api/internal/Production/RemoveChildUnit
POST /api/internal/Production/RemoveAllChildUnits
GET  /api/internal/Production/CheckChildUnits
GET  /api/internal/Production/SerialNumbers
GET  /api/internal/Production/SerialNumbers/Count
PUT  /api/internal/Production/SerialNumbers/Free
DELETE /api/internal/Production/SerialNumbers/Free
GET  /api/internal/Production/SerialNumbers/Ranges
GET  /api/internal/Production/SerialNumbers/Statistics
GET  /api/internal/Production/GetSites
GET  /api/internal/Mes/GetUnitPhases
```

### B. Product Module (14 endpoints)

```
GET  /api/internal/Product/Bom
PUT  /api/internal/Product/BOM
GET  /api/internal/Product/GetProductInfo
GET  /api/internal/Product/GetProductByPN
POST /api/internal/Product/PostProductRevisionRelation
PUT  /api/internal/Product/PutProductRevisionRelation
DELETE /api/internal/Product/DeleteProductRevisionRelation
GET  /api/internal/Product/GetProductCategories
PUT  /api/internal/Product/PutProductCategories
GET  /api/internal/Product/GetProductTags
PUT  /api/internal/Product/PutProductTags
GET  /api/internal/Product/GetRevisionTags
PUT  /api/internal/Product/PutRevisionTags
GET  /api/internal/Product/GetGroupsForProduct
```

### C. Software Module (13 endpoints)

```
GET  /api/internal/Software/isConnected
GET  /api/internal/Software/File/{id}
GET  /api/internal/Software/CheckFile
POST /api/internal/Software/PostPackageFolder
POST /api/internal/Software/UpdatePackageFolder
POST /api/internal/Software/DeletePackageFolder
POST /api/internal/Software/DeletePackageFolderFiles
GET  /api/internal/Software/GetPackageHistory
GET  /api/internal/Software/GetPackageDownloadHistory
GET  /api/internal/Software/GetRevokedPackages
GET  /api/internal/Software/GetAvailablePackages
GET  /api/internal/Software/GetSoftwareEntityDetails
GET  /api/internal/Software/Log
```

### D. Analytics Module (13 endpoints)

```
POST /api/internal/UnitFlow
GET  /api/internal/UnitFlow/Links
GET  /api/internal/UnitFlow/Nodes
POST /api/internal/UnitFlow/SN
POST /api/internal/UnitFlow/SplitBy
POST /api/internal/UnitFlow/UnitOrder
GET  /api/internal/UnitFlow/Units
GET  /api/internal/App/MeasurementList
POST /api/internal/App/MeasurementList
GET  /api/internal/App/StepStatusList
POST /api/internal/App/StepStatusList
GET  /api/internal/App/TopFailed
POST /api/internal/App/TopFailed
```

### E. Asset Module (4 endpoints)

```
POST /api/internal/Blob/Asset/{id}
GET  /api/internal/Blob/Asset/{id}/{fileName}
GET  /api/internal/Blob/Asset/List/{assetId}
DELETE /api/internal/Blob/Assets
```

### F. Process Module (4 endpoints)

```
GET  /api/internal/Process/GetProcesses
GET  /api/internal/Process/GetProcess/{id}
GET  /api/internal/Process/GetRepairOperations
GET  /api/internal/Process/GetRepairOperation/{id}
```
