# Public API Endpoint Requirements

**Date:** February 18, 2026  
**Purpose:** Define every backend endpoint needed for the Report, Product, Software, Asset, Production, and Analytics modules to be fully usable via the public API — including process-loading for UUT/UUR report creation.  
**Audience:** Backend team (WATS Core)

---

## Table of Contents

1. [Summary](#summary)
2. [Report Module](#1-report-module)
3. [Product Module](#2-product-module)
4. [Production Module](#3-production-module)
5. [Software Module](#4-software-module)
6. [Asset Module](#5-asset-module)
7. [Analytics Module](#6-analytics-module)
8. [Process Loading (Cross-Cutting)](#7-process-loading-cross-cutting)
9. [Internal → Public Migration Checklist](#8-internal--public-migration-checklist)

---

## Summary

| Module | Already Public | Currently Internal | Total Needed |
|--------|:-:|:-:|:-:|
| **Report** | 9 | 0 | **9** (complete) |
| **Product** | 10 | 14 | **24** |
| **Production** | 15 | 18 | **33** |
| **Software** | 12 | 11 | **23** |
| **Asset** | 17 | 3 | **20** |
| **Analytics** | 11 | 14 | **25** |
| **Process** (for reports) | 1 | 2 | **3** |
| **Total** | **75** | **62** | **137** |

**62 internal endpoints need public equivalents** for full public API coverage.

All internal endpoints currently require a `Referer` header matching the base URL. Public endpoints use BASIC authentication with API token. The migration means each internal endpoint needs:
1. A new public route under `/api/{Module}/...`
2. BASIC authentication with API token (same as existing public endpoints)
3. Remove `Referer` header requirement
4. Apply same authorization/permission model as existing public endpoints

---

## 1. REPORT MODULE

**Status: Report submission/query endpoints are fully public.** However, **UUR report creation depends on internal Process endpoints** for failure categories and repair codes (see [Section 6](#6-process-loading-cross-cutting)).

All 9 report-specific endpoints are public and use standard BASIC auth with API token:

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | GET | `/api/Report/Query/Header` | Query report headers (OData: `$filter`, `$expand`, `$top`, `$orderby`, `$skip`, `reportType`) |
| 2 | GET | `/api/Report/Query/HeaderByMiscInfo` | Search headers by misc info field (`description`, `stringValue`) |
| 3 | POST | `/api/Report/WSJF` | Submit report (JSON). Body: UUT/UUR report object with `processCode` field |
| 4 | GET | `/api/Report/Wsjf/{id}` | Get report by ID (JSON). Query: `detailLevel`, `includeChartdata`, `includeAttachments` |
| 5 | POST | `/api/Report/WSXF` | Submit report (XML) |
| 6 | GET | `/api/Report/Wsxf/{id}` | Get report by ID (XML). Query: `includeAttachments`, `includeChartdata`, `includeIndexes` |
| 7 | GET | `/api/Report/Attachment` | Get attachment content. Query: `attachmentId`, `stepId` |
| 8 | GET | `/api/Report/Attachments/{id}` | Get all attachments for a report (zip) |
| 9 | GET | `/api/Report/Certificate/{id}` | Get report certificate |

### Report Creation & Process Codes

Report creation (`create_uut_report()`, `create_uur_report()`) is a **local factory** — no API call. The caller must supply the `process_code` (e.g., `100` for End-of-Line Test). The process code is embedded in the JSON body when submitting via `POST /api/Report/WSJF`.

To discover valid process codes, the caller uses `GET /api/App/Processes` (see [Section 6](#6-process-loading-cross-cutting)).

### ⚠️ UUR Reports: Failure Categories & Repair Codes (INTERNAL DEPENDENCY)

UUR reports contain `UURFailure` entries on each sub-unit, with two critical fields:

| Field | Type | Purpose |
|-------|------|---------|
| `UURFailure.category` | string | Failure/repair category (e.g., "Component", "Solder") |
| `UURFailure.code` | string | Specific failure/repair code within the category (e.g., "Defect Component") |

While these are technically free-text strings accepted by `POST /api/Report/WSJF`, **valid values must come from the repair operation configuration**. The only endpoints that provide this configuration are **internal**:

| # | Current Internal Endpoint | Method | Purpose | Data Returned |
|---|--------------------------|--------|---------|---------------|
| 1 | `/api/internal/Process/GetRepairOperations` | GET | Get all repair operation configs | `RepairOperationConfig[]` with `categories[]` → `fail_codes[]` hierarchy |
| 2 | `/api/internal/Process/GetRepairOperation/{id}` | GET | Get single repair operation config | `RepairOperationConfig` with `categories[]` → `fail_codes[]` |

**Data flow for UUR report creation:**

```
1. GET /api/App/Processes (PUBLIC)
   → Get process codes (500 = Repair, 100 = EOL Test, etc.)

2. GET /api/internal/Process/GetRepairOperations (INTERNAL ⚠️)
   → RepairOperationConfig (for repair code 500)
     → categories: [
         { description: "Component", fail_codes: [
             { description: "Defect Component", guid: "..." },
             { description: "Missing Component", guid: "..." }
           ]
         },
         { description: "Solder", fail_codes: [
             { description: "Cold Solder", guid: "..." },
             { description: "Bridge", guid: "..." }
           ]
         }
       ]

3. User selects category + code → populates UURFailure entries

4. POST /api/Report/WSJF (PUBLIC)
   → Body includes subUnits[].failures[].category = "Component"
                   subUnits[].failures[].code = "Defect Component"
```

**Without public equivalents for these 2 endpoints, UUR reports cannot be created with valid failure/repair data.** These endpoints are covered in [Section 6](#6-process-loading-cross-cutting) as needing public equivalents.

---

## 2. PRODUCT MODULE

### Already Public (10 endpoints)

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | GET | `/api/Product/Query` | List/search products (OData) |
| 2 | GET | `/api/Product/{partNumber}` | Get product by part number |
| 3 | PUT | `/api/Product` | Create or update a product |
| 4 | PUT | `/api/Product/Products` | Bulk save products |
| 5 | GET | `/api/Product/{pn}/Revisions` | Get revisions for a product |
| 6 | GET | `/api/Product/{pn}/{revision}` | Get specific revision |
| 7 | GET | `/api/Product/{pn}/{revision}/BOM` | Get BOM for a revision (public) |
| 8 | GET | `/api/Product/Groups` | List product groups |
| 9 | PUT | `/api/Product/Groups` | Create/update product groups |
| 10 | GET | `/api/Product/Vendors` | List vendors |

### Needs Public Equivalent (14 internal endpoints)

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route | Parameters |
|---|--------------------------|--------|---------|----------------------|------------|
| 1 | `/api/internal/Product/Bom` | GET | Get BOM with full detail | `/api/Product/Bom` | Query: `partNumber`, `revision` |
| 2 | `/api/internal/Product/BOM` | PUT | Upload/update BOM items | `/api/Product/Bom` | Query: `partNumber`, `revision`, `format`; Body: BOM item list |
| 3 | `/api/internal/Product/GetProductInfo` | GET | Get product hierarchy (all child revision relations) | `/api/Product/Hierarchy` | Query: `partNumber`, `revision` |
| 4 | `/api/internal/Product/GetProductByPN` | GET | Get product with revision relations (box build template) | `/api/Product/WithRelations` | Query: `PN` |
| 5 | `/api/internal/Product/PostProductRevisionRelation` | POST | Create revision relation (add subunit to box build) | `/api/Product/RevisionRelation` | Body: `{ParentProductRevisionId, ProductRevisionId, Quantity, ItemNumber?, RevisionMask?}` |
| 6 | `/api/internal/Product/PutProductRevisionRelation` | PUT | Update revision relation | `/api/Product/RevisionRelation` | Body: ProductRevisionRelation dict |
| 7 | `/api/internal/Product/DeleteProductRevisionRelation` | DELETE | Delete revision relation | `/api/Product/RevisionRelation` | Query: `productRevisionRelationId` (UUID) |
| 8 | `/api/internal/Product/GetGroupsForProduct` | GET | Get groups containing a product | `/api/Product/GroupsForProduct` | Query: `partNumber` |
| 9 | `/api/internal/Product/GetProductCategories` | GET | Get all product categories | `/api/Product/Categories` | _(none)_ |
| 10 | `/api/internal/Product/PutProductCategories` | PUT | Save product categories | `/api/Product/Categories` | Body: list of category dicts |
| 11 | `/api/internal/Product/GetProductTags` | GET | Get tags for a product | `/api/Product/Tags` | Query: `partNumber` |
| 12 | `/api/internal/Product/PutProductTags` | PUT | Set tags for a product | `/api/Product/Tags` | Query: `partNumber`; Body: list of tag strings |
| 13 | `/api/internal/Product/GetRevisionTags` | GET | Get tags for a specific revision | `/api/Product/RevisionTags` | Query: `partNumber`, `revision` |
| 14 | `/api/internal/Product/PutRevisionTags` | PUT | Set tags for a specific revision | `/api/Product/RevisionTags` | Query: `partNumber`, `revision`; Body: list of tag strings |

### Backend Changes Required

For each of the 14 endpoints:
- **Add route** in the Product controller under `/api/Product/...`
- **Authentication:** Use standard BASIC authentication with API token (same as `GET /api/Product/Query`)
- **Authorization:** Same permission level as existing product write endpoints (endpoints 5-7, 10, 12, 14 are write operations)
- **Remove Referer header check** — public endpoints don't require it
- **Response format:** Keep same JSON schemas as internal versions

**Specific notes:**
- Endpoints 1-2 (`Bom`): The public BOM endpoint `GET /api/Product/{pn}/{rev}/BOM` already exists but may return a different schema than the internal version. Verify parity or document differences.
- Endpoints 5-7 (`RevisionRelation`): Critical for box build template management. These are CRUD operations on the parent-child product structure.
- Endpoints 9-14 (`Categories`, `Tags`): Metadata management — relatively low risk to expose publicly.

---

## 3. PRODUCTION MODULE

### Already Public (15 endpoints)

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | GET | `/api/Production/Unit/{sn}/{pn}` | Get unit by serial + part number |
| 2 | GET | `/api/Production/Units` | List/search units (OData) |
| 3 | PUT | `/api/Production/Unit` | Create or update a unit |
| 4 | GET | `/api/Production/Units/Changes` | Get unit change history |
| 5 | DELETE | `/api/Production/Units/Changes/{id}` | Delete a unit change |
| 6 | POST | `/api/Production/UnitVerification` | Verify a unit |
| 7 | POST | `/api/Production/SetUnitPhase` | Set unit phase |
| 8 | POST | `/api/Production/SetUnitProcess` | Set unit process step |
| 9 | POST | `/api/Production/AddChildUnit` | Add child unit (basic) |
| 10 | POST | `/api/Production/RemoveChildUnit` | Remove child unit (basic) |
| 11 | POST | `/api/Production/CheckChildUnits` | Check child units (basic) |
| 12 | GET | `/api/Production/SerialNumbers` | List serial number pools |
| 13 | GET | `/api/Production/SerialNumbers/Types` | Get serial number types |
| 14 | POST | `/api/Production/SerialNumbers/Take` | Take serial numbers from pool |
| 15 | GET | `/api/Production/Batches` | List batches |

**Also public but not listed in route constants (used via OData on existing routes):**

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 16 | GET | `/api/Production/Batch/{id}` | Get batch by ID |
| 17 | GET | `/api/Production/Shift/{id}` | Get shift by ID |
| 18 | GET | `/api/Production/Shifts` | List shifts |
| 19 | GET | `/api/Production/Phases` | Get unit phases (public version) |
| 20 | GET | `/api/Production/Operators` | List operators |
| 21 | GET | `/api/Production/Operator/{id}` | Get operator by ID |

### Needs Public Equivalent (18 internal endpoints)

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route | Parameters |
|---|--------------------------|--------|---------|----------------------|------------|
| 1 | `/api/internal/Production/isConnected` | GET | Check Production module connectivity | `/api/Production/Status` | _(none)_ |
| 2 | `/api/internal/Mes/GetUnitPhases` | GET | Get all unit phases (MES workflow states) | `/api/Production/UnitPhases` | _(none)_ |
| 3 | `/api/internal/Production/GetSites` | GET | Get all production sites | `/api/Production/Sites` | _(none)_ |
| 4 | `/api/internal/Production/GetUnit` | GET | Get unit by serial number (part number optional) | `/api/Production/Unit` (GET with query) | Query: `serialNumber`, `partNumber?` |
| 5 | `/api/internal/Production/GetUnitInfo` | GET | Get unit info (summary) | `/api/Production/UnitInfo` | Query: `serialNumber`, `partNumber` |
| 6 | `/api/internal/Production/GetUnitHierarchy` | GET | Get complete unit parent/child tree | `/api/Production/UnitHierarchy` | Query: `serialNumber`, `partNumber` |
| 7 | `/api/internal/Production/GetUnitStateHistory` | GET | Get unit state change history | `/api/Production/UnitStateHistory` | Query: `serialNumber`, `partNumber` |
| 8 | `/api/internal/Production/GetUnitPhase` | GET | Get current phase of a specific unit | `/api/Production/UnitPhase` | Query: `serialNumber`, `partNumber` |
| 9 | `/api/internal/Production/GetUnitProcess` | GET | Get current process step of a unit | `/api/Production/UnitProcess` | Query: `serialNumber`, `partNumber` |
| 10 | `/api/internal/Production/GetUnitContents` | GET | Get unit BOM/components | `/api/Production/UnitContents` | Query: `serialNumber`, `partNumber`, `revision` |
| 11 | `/api/internal/Production/CreateUnit` | POST | Create a new unit in production | `/api/Production/CreateUnit` | Query: `serialNumber`, `partNumber`, `revision`, `batchNumber?`, `unitPhase?` |
| 12 | `/api/internal/Production/AddChildUnit` | POST | Add child unit with box build validation | `/api/Production/AddChildUnitValidated` | Query: `serialNumber`, `partNumber`, `childSerialNumber`, `childPartNumber`, `checkPartNumber`, `checkRevision`, `cultureCode`, `checkPhase?` |
| 13 | `/api/internal/Production/RemoveChildUnit` | POST | Remove child unit (localized errors) | `/api/Production/RemoveChildUnitLocalized` | Query: `serialNumber`, `partNumber`, `childSerialNumber`, `childPartNumber`, `cultureCode?` |
| 14 | `/api/internal/Production/RemoveAllChildUnits` | POST | Remove all child units from parent | `/api/Production/RemoveAllChildUnits` | Query: `serialNumber`, `partNumber`, `cultureCode?` |
| 15 | `/api/internal/Production/CheckChildUnits` | GET | Validate child units with localized messages | `/api/Production/ValidateChildUnits` | Query: `ParentSerialNumber`, `ParentPartNumber`, `CultureCode` |
| 16 | `/api/internal/Production/SerialNumbers` | GET | Find serial numbers in a range | `/api/Production/SerialNumbers/Find` | Query: `serialNumberType`, `startAddress`, `endAddress`, `startDate?`, `endDate?` |
| 17 | `/api/internal/Production/SerialNumbers/Count` | GET | Count serial numbers in range | `/api/Production/SerialNumbers/Count` | Query: `serialNumberType`, `startAddress?`, `endAddress?`, `fromDate?`, `toDate?` |
| 18 | `/api/internal/Production/SerialNumbers/Free` | PUT | Free reserved serial numbers | `/api/Production/SerialNumbers/Free` | Body: list of range dicts |

**Additional serial number endpoints (3 more, lower priority):**

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route |
|---|--------------------------|--------|---------|----------------------|
| 19 | `/api/internal/Production/SerialNumbers/Free` | DELETE | Delete free serial numbers | `/api/Production/SerialNumbers/Free` (DELETE) |
| 20 | `/api/internal/Production/SerialNumbers/Ranges` | GET | Get serial number ranges | `/api/Production/SerialNumbers/Ranges` |
| 21 | `/api/internal/Production/SerialNumbers/Statistics` | GET | Get serial number statistics | `/api/Production/SerialNumbers/Statistics` |

### Backend Changes Required

- **Endpoints 2, 3, 4-10:** Read-only queries — low risk. Same authorization as `GET /api/Production/Units`.
- **Endpoint 11 (`CreateUnit`):** Write operation. Needs same authorization as `PUT /api/Production/Unit`.
- **Endpoints 12-15 (child unit management with validation):** These are the **enhanced versions** of the publicly available `AddChildUnit`/`RemoveChildUnit`/`CheckChildUnits`. The internal versions add:
  - Box build template validation (`checkPartNumber`, `checkRevision`)
  - Phase validation (`checkPhase`)
  - Localized error messages (`cultureCode`)
  
  Consider extending the existing public endpoints with optional query parameters instead of creating separate routes.
- **Endpoints 16-21 (serial number management):** Extended serial number operations. Moderate risk — includes write operations (Free, Delete).

---

## 4. SOFTWARE MODULE

### Already Public (12 endpoints)

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | GET | `/api/Software/Packages` | List packages (OData) |
| 2 | GET | `/api/Software/Package/{id}` | Get package by ID |
| 3 | PUT | `/api/Software/Package/{id}` | Update package |
| 4 | DELETE | `/api/Software/Package/{id}` | Delete package |
| 5 | POST | `/api/Software/Package` | Create package |
| 6 | GET | `/api/Software/PackageByName` | Get package by name/tag |
| 7 | GET | `/api/Software/PackagesByTag` | Get packages by tag |
| 8 | GET | `/api/Software/PackageFiles/{id}` | Get package file tree |
| 9 | POST | `/api/Software/Package/UploadZip/{id}` | Upload zip to package |
| 10 | GET | `/api/Software/File` | Download a file |
| 11 | POST | `/api/Software/PackageStatus/{id}` | Set package status |
| 12 | GET | `/api/Software/VirtualFolders` | List virtual folders |

### Needs Public Equivalent (11 internal endpoints)

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route | Parameters |
|---|--------------------------|--------|---------|----------------------|------------|
| 1 | `/api/internal/Software/isConnected` | GET | Check Software module connectivity | `/api/Software/Status` | _(none)_ |
| 2 | `/api/internal/Software/File/{id}` | GET | Get file metadata by UUID | `/api/Software/FileInfo/{id}` | Path: `id` (UUID) |
| 3 | `/api/internal/Software/CheckFile` | GET | Check if file exists on server (dedup) | `/api/Software/CheckFile` | Query: `packageId`, `parentFolderId`, `filePath`, `checksum`, `fileDateEpoch` |
| 4 | `/api/internal/Software/PostPackageFolder` | POST | Create folder in package | `/api/Software/PackageFolder` | Query: `packageId`; Body: folder entity |
| 5 | `/api/internal/Software/UpdatePackageFolder` | PUT | Update package folder | `/api/Software/PackageFolder` | Body: folder entity |
| 6 | `/api/internal/Software/DeletePackageFolder` | DELETE | Delete package folder | `/api/Software/PackageFolder` | Query: `packageFolderId` |
| 7 | `/api/internal/Software/DeletePackageFolderFiles` | DELETE | Delete multiple files from folder | `/api/Software/PackageFolderFiles` | Query: `packageFolderFileIds` (comma-sep UUIDs) |
| 8 | `/api/internal/Software/GetPackageHistory` | GET | Get package version/status history | `/api/Software/PackageHistory` | Query: `tags`, `status?` (0-3), `allVersions?` |
| 9 | `/api/internal/Software/GetPackageDownloadHistory` | GET | Get download history for a client | `/api/Software/DownloadHistory` | Query: `clientId` |
| 10 | `/api/internal/Software/GetRevokedPackages` | GET | Check for revoked packages | `/api/Software/RevokedPackages` | Query: `installedPackages` (comma-sep UUIDs), `includeRevokedOnly?` |
| 11 | `/api/internal/Software/GetAvailablePackages` | GET | Check for newer versions | `/api/Software/AvailablePackages` | Query: `installedPackages` (comma-sep UUIDs) |

**Additional endpoints (2, lower priority):**

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route |
|---|--------------------------|--------|---------|----------------------|
| 12 | `/api/internal/Software/GetSoftwareEntityDetails` | GET | Get detailed package info | `/api/Software/PackageDetails` |
| 13 | `/api/internal/Software/Log` | GET | Log download event | `/api/Software/DownloadLog` |

### Backend Changes Required

- **Endpoints 1-3:** Read-only queries — low risk.
- **Endpoints 4-7 (folder management):** Write operations for package folder structure. These enable programmatic package building. Needs same auth as `POST /api/Software/Package`.
- **Endpoints 8-11 (history/availability):** Read-only operations important for software distribution clients. The `GetAvailablePackages` and `GetRevokedPackages` endpoints are essential for the client auto-update flow.
- **Endpoint 13 (`Log`):** Creates a download audit log entry. Consider whether this should be auto-triggered by the file download endpoint instead.

---

## 5. ASSET MODULE

### Already Public (17 endpoints)

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | GET | `/api/Assets` | List/search assets (OData) |
| 2 | GET | `/api/Asset/{id}` | Get asset by ID or serial |
| 3 | PUT | `/api/Asset` | Create or update asset |
| 4 | DELETE | `/api/Asset/{id}` | Delete asset |
| 5 | GET | `/api/Asset/Types` | Get asset types |
| 6 | GET | `/api/Asset/{sn}/Status` | Get asset status |
| 7 | PUT | `/api/Asset/Status` | Update asset status |
| 8 | PUT | `/api/Asset/State` | Set asset state |
| 9 | GET | `/api/Asset/Count` | Get asset count |
| 10 | POST | `/api/Asset/ResetRunningCount` | Reset running counter |
| 11 | POST | `/api/Asset/SetRunningCount` | Set running counter |
| 12 | POST | `/api/Asset/SetTotalCount` | Set total counter |
| 13 | GET | `/api/Asset/{sn}/Calibrations` | Get calibration history |
| 14 | POST | `/api/Asset/Calibration` | Record calibration |
| 15 | GET | `/api/Asset/{sn}/Maintenance` | Get maintenance history |
| 16 | POST | `/api/Asset/Maintenance` | Record maintenance |
| 17 | GET | `/api/Asset/SubAssets` | Get sub-assets |

### Needs Public Equivalent (3 internal endpoints)

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route | Parameters |
|---|--------------------------|--------|---------|----------------------|------------|
| 1 | `/api/internal/Blob/Asset` | POST | Upload file to asset | `/api/Asset/File` | Query: `assetId`, `filename`; Body: binary; Header: `Content-Type: application/octet-stream` |
| 2 | `/api/internal/Blob/Asset` | GET | Download file from asset | `/api/Asset/File` | Query: `assetId`, `filename` |
| 3 | `/api/internal/Blob/Asset/List/{id}` | GET | List files attached to asset | `/api/Asset/Files/{id}` | Path: `assetId` |

**Additional endpoint (1, lower priority):**

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route |
|---|--------------------------|--------|---------|----------------------|
| 4 | `/api/internal/Blob/Assets` | DELETE | Delete files from asset | `/api/Asset/Files` (DELETE) |

### Backend Changes Required

- These 4 endpoints are all **blob storage** operations under `/api/internal/Blob/Asset`. The pattern is different from the other modules — they're handled by a separate Blob controller.
- For public API: Move to the Asset controller under `/api/Asset/File` and `/api/Asset/Files`.
- File upload (POST) should preserve the `application/octet-stream` content type pattern.
- Authorization: Same level as `PUT /api/Asset` (asset write permission).

---

## 6. ANALYTICS MODULE

**Status: ⚠️ Mixed.** Public endpoints cover standard statistics/KPIs. **Unit Flow, advanced measurement/step filtering, top failure analysis, and alarm logs are internal-only.**

### Already Public (11 endpoints)

The public Analytics/App endpoints cover standard statistics:

| # | Method | Endpoint | Purpose |
|---|--------|----------|---------|
| 1 | POST | `/api/App/DynamicYield` | Yield over time (FPY, rolled throughput, etc.) |
| 2 | POST | `/api/App/DynamicStep` | Step analysis (failure Pareto, step statistics) |
| 3 | POST | `/api/App/DynamicMeasurement` | Measurement statistics (SPC, histogram) |
| 4 | POST | `/api/App/DynamicRepair` | Repair statistics (UUR repair data) |
| 5 | GET | `/api/App/RelatedRepairHistory` | Repair history for a serial number |
| 6 | GET | `/api/App/Processes` | Process list (shared with Report/Process) |
| 7 | GET | `/api/App/ProductGroups` | Product groups for filtering |
| 8 | GET | `/api/App/Levels` | Levels (sub-groups) for a product group |
| 9 | GET | `/api/App/TopFailed` | Top failed steps (simple, public) |
| 10 | POST | `/api/App/OEE` | OEE analysis |
| 11 | POST | `/api/App/AggregatedMeasurement` | Aggregated measurement data |

### Needs Public Equivalent (14 internal endpoints)

#### Unit Flow Analysis (7 endpoints via UnitFlow controller)

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route |
|---|--------------------------|--------|---------|----------------------|
| 1 | `/api/internal/UnitFlow` | POST | Query unit flow — main analysis endpoint (also handles visibility/expand via body params) | `/api/Analytics/UnitFlow` |
| 2 | `/api/internal/UnitFlow/Links` | GET | Get flow links (edges between process nodes) | `/api/Analytics/UnitFlow/Links` |
| 3 | `/api/internal/UnitFlow/Nodes` | GET | Get flow nodes (process operations) | `/api/Analytics/UnitFlow/Nodes` |
| 4 | `/api/internal/UnitFlow/SN` | POST | Trace flow for specific serial numbers | `/api/Analytics/UnitFlow/SerialNumbers` |
| 5 | `/api/internal/UnitFlow/SplitBy` | POST | Split flow by dimension (station, location, etc.) | `/api/Analytics/UnitFlow/SplitBy` |
| 6 | `/api/internal/UnitFlow/UnitOrder` | POST | Set unit ordering in flow visualization | `/api/Analytics/UnitFlow/UnitOrder` |
| 7 | `/api/internal/UnitFlow/Units` | GET | Get individual units from the flow | `/api/Analytics/UnitFlow/Units` |

#### Step/Measurement Filtering (6 endpoints via App controller, GET+POST variants)

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route |
|---|--------------------------|--------|---------|----------------------|
| 8 | `/api/internal/App/MeasurementList` | GET | Measurement list (simple params: productGroupId, levelId, days) | `/api/Analytics/MeasurementList` |
| 9 | `/api/internal/App/MeasurementList` | POST | Measurement list (advanced filter body + step/sequence filter XML) | `/api/Analytics/MeasurementList` |
| 10 | `/api/internal/App/StepStatusList` | GET | Step status list (simple params) | `/api/Analytics/StepStatusList` |
| 11 | `/api/internal/App/StepStatusList` | POST | Step status list (advanced filter body) | `/api/Analytics/StepStatusList` |
| 12 | `/api/internal/App/TopFailed` | GET | Top failed steps (simple params — internal variant with extra filter options) | `/api/Analytics/TopFailed` |
| 13 | `/api/internal/App/TopFailed` | POST | Top failed steps (advanced filter body) | `/api/Analytics/TopFailed` |

#### Alarm & Notification Logs (1 endpoint via Trigger controller)

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route |
|---|--------------------------|--------|---------|----------------------|
| 14 | `/api/internal/Trigger/GetAlarmAndNotificationLogs` | POST | Query alarm/notification logs (yield alarms, SPC alarms, asset alarms, etc.) | `/api/Analytics/AlarmLogs` |

### pyWATS Service Methods Using These Internal Endpoints

| Service Method | Internal Endpoint | Category |
|---------------|-------------------|----------|
| `get_unit_flow()` | `POST /api/internal/UnitFlow` | Unit Flow |
| `get_flow_links()` | `GET /api/internal/UnitFlow/Links` | Unit Flow |
| `get_flow_nodes()` | `GET /api/internal/UnitFlow/Nodes` | Unit Flow |
| `trace_serial_numbers()` | `POST /api/internal/UnitFlow/SN` | Unit Flow |
| `split_flow_by()` | `POST /api/internal/UnitFlow/SplitBy` | Unit Flow |
| `set_unit_order()` | `POST /api/internal/UnitFlow/UnitOrder` | Unit Flow |
| `get_flow_units()` | `GET /api/internal/UnitFlow/Units` | Unit Flow |
| `set_unit_flow_visibility()` | `POST /api/internal/UnitFlow` | Unit Flow |
| `show_operations()` / `hide_operations()` | `POST /api/internal/UnitFlow` | Unit Flow |
| `expand_operations()` | `POST /api/internal/UnitFlow` | Unit Flow |
| `get_bottlenecks()` | `POST /api/internal/UnitFlow` | Unit Flow |
| `get_flow_summary()` | `POST /api/internal/UnitFlow` | Unit Flow |
| `get_measurement_list()` | `POST /api/internal/App/MeasurementList` | Measurement |
| `get_measurement_list_by_product()` | `GET /api/internal/App/MeasurementList` | Measurement |
| `get_step_status_list()` | `POST /api/internal/App/StepStatusList` | Step Filter |
| `get_step_status_list_by_product()` | `GET /api/internal/App/StepStatusList` | Step Filter |
| `get_top_failed_internal()` | `GET+POST /api/internal/App/TopFailed` | Top Failures |
| `get_alarm_logs()` | `POST /api/internal/Trigger/GetAlarmAndNotificationLogs` | Alarms |

### Backend Changes Required

- **Unit Flow (7 endpoints):** The entire Unit Flow feature is internal. This is a stateful, session-based API on the server — the POST calls modify server-side state and subsequent GET calls return the current state. Consider whether the public version should maintain this pattern or switch to stateless queries.
- **Measurement/Step filtering (6 endpoints):** These use XML-format step and sequence filters. For the public API, consider accepting JSON filter format instead of XML.
- **TopFailed (2 endpoints):** The public `GET /api/App/TopFailed` already exists but has limited filtering. The internal variants add advanced filtering via body parameters.
- **Alarm logs (1 endpoint):** Lives on the Trigger controller. For public API, consolidate under Analytics.
- **Authorization:** All are read-only analytics — same permission level as existing `POST /api/App/DynamicYield`.

---

## 7. PROCESS LOADING (Cross-Cutting)

**Status: ⚠️ Partially public.** Process list is public, but **repair operation configuration** (failure categories, repair codes) is internal-only.

### Why Process Loading Matters for Reports

Every UUT/UUR report requires a `processCode` field (e.g., `100` = End-of-Line Test, `500` = Repair). This code must match a process defined on the server. The client needs to:

1. **Discover valid process codes** before creating reports
2. **Validate** that a given code is a test operation (UUT) or repair operation (UUR)
3. **Cache** the process list to avoid repeated calls
4. **For UUR reports:** Retrieve the failure categories and repair codes configured for a repair operation

### Already Public (1 endpoint)

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/api/App/Processes` | BASIC auth token | Returns all process definitions |

```json
[
  {
    "code": 100,
    "name": "End of line test",
    "description": "Final test before shipping",
    "isTestOperation": true,
    "isRepairOperation": false,
    "isWipOperation": false
  },
  {
    "code": 500,
    "name": "Repair",
    "description": "Board-level repair",
    "isTestOperation": false,
    "isRepairOperation": true,
    "isWipOperation": false
  }
]
```

### How It's Used in Report Creation

```
pyWATS Client                                           WATS Server
─────────────────────────────────────────────────────────────────────
1. GET /api/App/Processes ──────────────────────────────→ returns process list
   ← [{ code: 100, isTestOperation: true }, ...]

2. create_uut_report(operation_type=100, ...)           (local — no API call)
   → UUTReport { processCode: 100, sn, pn, ... }

3. POST /api/Report/WSJF ──────────────────────────────→ server validates
   Body: { "processCode": 100, "sn": "...", ... }         processCode exists
   ← 200 OK                                               and matches type
```

**For UUR reports**, two process codes are needed:
- `repair_process_code` (e.g., `500`) — the repair operation itself
- `test_operation_code` (e.g., `100`) — the original test that failed

Both must be valid process codes from `GET /api/App/Processes`.

### ⚠️ Needs Public Equivalent (2 internal endpoints — required for UUR reports)

| # | Current Internal Endpoint | Method | Purpose | Suggested Public Route | Response Data |
|---|--------------------------|--------|---------|----------------------|---------------|
| 1 | `/api/internal/Process/GetRepairOperations` | GET | Get all repair operation configs with failure categories and codes | `/api/Process/RepairOperations` | `RepairOperationConfig[]` with `categories[]` → `fail_codes[]` |
| 2 | `/api/internal/Process/GetRepairOperation/{id}` | GET | Get single repair operation config by process code | `/api/Process/RepairOperation/{id}` | `RepairOperationConfig` with `categories[]` → `fail_codes[]` |

#### Response Schema (RepairOperationConfig)

```json
{
  "description": "Repair",
  "uutRequired": true,
  "compRefMask": "...",
  "bomRequired": false,
  "vendorRequired": false,
  "categories": [
    {
      "guid": "...",
      "description": "Component",
      "selectable": true,
      "sortOrder": 1,
      "failureType": 0,
      "status": 0,
      "failCodes": [
        {
          "guid": "...",
          "description": "Defect Component",
          "selectable": true,
          "sortOrder": 1
        },
        {
          "guid": "...",
          "description": "Missing Component",
          "selectable": true,
          "sortOrder": 2
        }
      ]
    }
  ]
}
```

#### pyWATS Service Methods Using These Endpoints

| Service Method | Endpoint Used | What It Returns |
|---------------|---------------|-----------------|
| `get_fail_codes(repair_code)` | `GetRepairOperations` | Flat list of `FailureCodeInfo(category, code, guid, category_guid)` |
| `get_repair_categories(process_code)` | `GetRepairOperations` | List of `RepairCategory` with nested `fail_codes` |
| `get_repair_codes(process_code, category)` | `GetRepairOperations` | Fail code descriptions for a specific category |
| `get_repair_operation_configs()` | `GetRepairOperations` | All `RepairOperationConfig` objects |
| `get_repair_operation_config(code)` | `GetRepairOperation/{id}` | Single `RepairOperationConfig` by process code |

### Backend Changes Required

- These 2 endpoints return the **failure category → fail code hierarchy** that UUR report clients need to populate `UURFailure.category` and `UURFailure.code` fields with valid values.
- Without public equivalents, UUR reports can only be created by hardcoding or guessing category/code strings.
- **Priority: Phase 1** — these are essential for the UUR report workflow.
- Authorization: Read-only access, same permission level as `GET /api/App/Processes`.

### Other Internal Process Endpoints (Lower Priority)

The remaining internal process endpoints (`GetProcesses`, `GetProcess/{id}`) return additional administrative fields (`ProcessID`, `processIndex`, `state`, `Properties`). These are used by the configurator UI for process management and can remain internal unless full process administration via the public API is required.

---

## 8. Internal → Public Migration Checklist

For each internal endpoint being made public, the backend team should:

### Per-Endpoint Checklist

- [ ] **Route:** Add new public route under `/api/{Module}/...`
- [ ] **Authentication:** BASIC authentication with API token (same middleware as existing public endpoints)
- [ ] **Authorization:** Apply appropriate permission level:
  - Read endpoints → same as existing GET endpoints in the module
  - Write endpoints → same as existing PUT/POST endpoints in the module
- [ ] **Remove Referer check:** Public endpoints don't use Referer-based auth
- [ ] **Response schema:** Keep identical JSON response format (no breaking changes)
- [ ] **Error responses:** Use standard public API error format (HTTP status codes + error JSON)
- [ ] **Rate limiting:** Apply same rate limits as existing public endpoints
- [ ] **Documentation:** Add to Swagger/OpenAPI spec
- [ ] **Backward compatibility:** Keep internal endpoint operational during transition period

### Priority Order

**Phase 1 — Essential for report workflow:**
1. ✅ `GET /api/App/Processes` — already public
2. ✅ `POST /api/Report/WSJF` — already public
3. ✅ `GET /api/Report/Query/Header` — already public
4. ⚠️ `GET /api/internal/Process/GetRepairOperations` → needs public equivalent for UUR failure categories/codes
5. ⚠️ `GET /api/internal/Process/GetRepairOperation/{id}` → needs public equivalent for UUR failure categories/codes

**Phase 2 — Product management (box build):**
4. Product revision relations (endpoints 3-7) — needed for box build templates
5. Product BOM (endpoints 1-2) — needed for BOM management
6. Product categories & tags (endpoints 9-14) — metadata management

**Phase 3 — Production operations:**
7. Unit queries (endpoints 4-10) — read operations, low risk
8. Unit creation & child management (endpoints 11-15) — write operations
9. Serial number management (endpoints 16-21) — pool management
10. Sites & phases (endpoints 2-3) — configuration data

**Phase 4 — Software distribution:**
11. Package history & availability (endpoints 8-11) — client update flow
12. Folder management (endpoints 4-7) — package building
13. File operations (endpoints 2-3) — dedup and metadata

**Phase 5 — Asset files:**
14. File upload/download/list (endpoints 1-3) — blob storage
15. File deletion (endpoint 4)

**Phase 6 — Analytics (advanced):**
16. Unit Flow analysis (7 endpoints) — production flow visualization
17. Measurement/step filtering (6 endpoints) — advanced data queries
18. Alarm logs (1 endpoint) — alarm and notification history

---

## Appendix: Endpoint Count by Priority

| Priority | Phase | Endpoints | Risk Level |
|----------|-------|:---------:|:----------:|
| ✅ Done | Report (submission/query) | 10 | — |
| ⚠️ Phase 1 | Process repair configs (for UUR) | 2 | Low |
| Phase 2 | Product | 14 | Low–Medium |
| Phase 3 | Production | 21 | Medium |
| Phase 4 | Software | 13 | Low |
| Phase 5 | Asset | 4 | Low |
| Phase 6 | Analytics (Unit Flow, filtering, alarms) | 14 | Medium |
| **Total** | | **78** | |

*Excludes the 59 endpoints that are already public across these 6 modules + process.*
