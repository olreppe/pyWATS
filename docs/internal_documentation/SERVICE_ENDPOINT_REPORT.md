# Service Function & Backend Endpoint Report

**Generated:** February 18, 2026  
**Modules:** Product, Production, Software, Asset, Report, Analytics, RootCause, SCIM, Process, Core, Client, UI  
**Source:** `src/pywats/domains/{module}/async_service.py` → `async_repository.py`  
**Note:** Includes dedicated helper classes (e.g., `AsyncBoxBuildTemplate`), core/client infrastructure, and UI components with direct HTTP calls.
**Non-HTTP packages** (no endpoint calls): queue, shared, tools, sync, cfx (AMQP), events (MQTT), dev, converters, control, io, launcher, persistent_queue

---

## Summary

| Module | Public Functions | Internal Functions | Public Endpoints | Internal Endpoints | Total Endpoints |
|--------|:---:|:---:|:---:|:---:|:---:|
| **Product** | 25 | 14 (+12 BoxBuild) | 10 | 13 | 23 |
| **Production** | 27 | 18 | 15 | 18 | 33 |
| **Software** | 19 | 12 | 12 | 11 | 23 |
| **Asset** | 22 | 4 | 17 | 3 | 20 |
| **Report** | 23 | 0 | 9 | 0 | 9 |
| **Analytics** | 23 | 20 | 20 | 11 | 31 |
| **RootCause** | 12 | 0 | 7 | 0 | 7 |
| **SCIM** | 11 | 0 | 7 | 0 | 7 |
| **Process** | 22 | 7 | 1 | 4 | 5 |
| **Core** | 2 | 1 | 0 | 0 | 0 |
| **Client** | 0 | 2 | 0 | 0 | 0 |
| **UI** | 0 | 3 | 0 | 0 | 0 |
| **TOTAL** | **188** | **81 (+12)** | **98** | **60** | **158** |

---

## 1. PRODUCT MODULE (`AsyncProductService` + `AsyncBoxBuildTemplate`)

**Files:** `async_service.py` (includes `AsyncBoxBuildTemplate` class - consolidated Feb 2026), `async_repository.py`

### Module Endpoints Overview

**Public API (10):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/Product/Query` |
| 2 | GET | `/api/Product/{partNumber}` |
| 3 | PUT | `/api/Product` |
| 4 | PUT | `/api/Product/Products` |
| 5 | PUT | `/api/Product/Revision` |
| 6 | PUT | `/api/Product/Revisions` |
| 7 | GET | `/api/Product/Groups` |
| 8 | PUT | `/api/Product/Group` |
| 9 | PUT | `/api/Product/BOM` (WSBF XML) |
| 10 | GET/PUT/DELETE | `/api/Product/Vendors` |

**Internal API (13):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/internal/Product/Bom` |
| 2 | PUT | `/api/internal/Product/BOM` |
| 3 | GET | `/api/internal/Product/GetProductInfo` |
| 4 | GET | `/api/internal/Product/GetProductByPN` |
| 5 | POST | `/api/internal/Product/PostProductRevisionRelation` |
| 6 | PUT | `/api/internal/Product/PutProductRevisionRelation` |
| 7 | DELETE | `/api/internal/Product/DeleteProductRevisionRelation` |
| 8 | GET | `/api/internal/Product/GetProductCategories` |
| 9 | PUT | `/api/internal/Product/PutProductCategories` |
| 10 | GET | `/api/internal/Product/GetProductTags` |
| 11 | PUT | `/api/internal/Product/PutProductTags` |
| 12 | GET | `/api/internal/Product/GetRevisionTags` |
| 13 | PUT | `/api/internal/Product/PutRevisionTags` |

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `get_products()` | Public | GET `/api/Product/Query` |
| 2 | `get_products_full()` | Public | GET `/api/Product/Query` (alias) |
| 3 | `get_product(part_number)` | Public | GET `/api/Product/{partNumber}` |
| 4 | `create_product(...)` | Public | PUT `/api/Product` |
| 5 | `update_product(product)` | Public | PUT `/api/Product` |
| 6 | `bulk_save_products(products)` | Public | PUT `/api/Product/Products` |
| 7 | `get_active_products()` | Public | GET `/api/Product/Query` (filtered client-side) |
| 8 | `is_active(product)` | Public | _(no endpoint — local check)_ |
| 9 | `get_revisions(part_number)` | Public | GET `/api/Product/{partNumber}` |
| 10 | `get_revision(pn, rev)` | Public | GET `/api/Product/{partNumber}` |
| 11 | `create_revision(...)` | Public | GET `/api/Product/{partNumber}` + PUT `/api/Product/Revision` |
| 12 | `update_revision(revision)` | Public | PUT `/api/Product/Revision` |
| 13 | `bulk_save_revisions(revisions)` | Public | PUT `/api/Product/Revision` (loop) |
| 14 | `get_groups()` | Public | GET `/api/Product/Groups` |
| 15 | `create_group(name)` | Public | PUT `/api/Product/Group` |
| 16 | `get_product_tags(pn)` | Public | GET `/api/Product/{partNumber}` (extract from model) |
| 17 | `set_product_tags(pn, tags)` | Public | GET `/api/Product/{partNumber}` + PUT `/api/Product` |
| 18 | `add_product_tag(pn, name, val)` | Public | GET `/api/Product/{partNumber}` + PUT `/api/Product` |
| 19 | `get_revision_tags(pn, rev)` | Public | GET `/api/Product/{partNumber}` (extract from model) |
| 20 | `set_revision_tags(pn, rev, tags)` | Public | GET `/api/Product/{partNumber}` + PUT `/api/Product/Revision` |
| 21 | `add_revision_tag(pn, rev, ...)` | Public | GET `/api/Product/{partNumber}` + PUT `/api/Product/Revision` |
| 22 | `update_bom(pn, rev, items)` | Public | PUT `/api/Product/BOM` (WSBF XML) |
| 23 | `get_groups_for_product(pn)` | Public | GET `/api/Product/{partNumber}` + GET `/api/internal/Product/GetGroupsForProduct` |
| 24 | `get_vendors()` | ⚠️ Internal | GET `/api/Product/Vendors` |
| 25 | `save_vendor(name, ...)` | ⚠️ Internal | PUT `/api/Product/Vendors` |
| 26 | `delete_vendor(vendor_id)` | ⚠️ Internal | DELETE `/api/Product/Vendors/{vendorId}` |
| 27 | `get_bom(pn, rev)` | ⚠️ Internal | GET `/api/internal/Product/Bom` |
| 28 | `upload_bom(pn, rev, items)` | ⚠️ Internal | PUT `/api/internal/Product/BOM` |
| 29 | `get_bom_items(pn, rev)` | ⚠️ Internal | GET `/api/internal/Product/Bom` (alias) |
| 30 | `get_product_hierarchy(pn, rev)` | ⚠️ Internal | GET `/api/internal/Product/GetProductInfo` |
| 31 | `add_subunit(...)` | ⚠️ Internal | GET `/api/Product/{pn}` ×2 + POST `/api/internal/Product/PostProductRevisionRelation` |
| 32 | `remove_subunit(relation_id)` | ⚠️ Internal | DELETE `/api/internal/Product/DeleteProductRevisionRelation` |
| 33 | `get_product_categories()` | ⚠️ Internal | GET `/api/internal/Product/GetProductCategories` |
| 34 | `save_product_categories(cats)` | ⚠️ Internal | PUT `/api/internal/Product/PutProductCategories` |
| 35 | `get_box_build_template(pn, rev)` | ⚠️ Internal | GET `/api/Product/{pn}` + GET `/api/internal/Product/GetProductInfo` |
| 36 | `get_box_build_subunits(pn, rev)` | ⚠️ Internal | GET `/api/internal/Product/GetProductInfo` |

### AsyncBoxBuildTemplate (part of `async_service.py`)

Returned by `get_box_build_template()`. Provides a fluent builder for managing product-level
box build definitions (which subunits are required to build a parent product).
**Consolidated into `async_service.py` (Feb 2026)** - previously in separate `async_box_build.py`, `box_build.py`, `sync_box_build.py` files.

| # | Class Method | Endpoint(s) Used |
|---|-------------|------------------|
| 1 | `add_subunit(pn, rev, qty, ...)` | GET `/api/Product/{pn}` (via `get_revision`) |
| 2 | `update_subunit(pn, rev, ...)` | _(no endpoint — local change tracking)_ |
| 3 | `remove_subunit(pn, rev)` | _(no endpoint — local change tracking)_ |
| 4 | `clear_all()` | _(no endpoint — local change tracking)_ |
| 5 | `set_quantity(pn, rev, qty)` | _(no endpoint — delegates to `update_subunit`)_ |
| 6 | `save()` | DELETE `/api/internal/Product/DeleteProductRevisionRelation` + PUT `/api/internal/Product/PutProductRevisionRelation` + POST `/api/internal/Product/PostProductRevisionRelation` |
| 7 | `discard()` | _(no endpoint — local only)_ |
| 8 | `reload()` | GET `/api/internal/Product/GetProductInfo` (via `_load_box_build_relations`) |
| 9 | `validate_subunit(pn, rev)` | _(no endpoint — local validation against revision mask)_ |
| 10 | `get_matching_subunits(pn)` | _(no endpoint — local filter)_ |
| 11 | `get_required_parts()` | _(no endpoint — local summary)_ |
| 12 | Context manager (`__aenter__`/`__aexit__`) | Same as `save()` on exit (if pending changes) |

---

## 2. PRODUCTION MODULE (`AsyncProductionService`)

### Module Endpoints Overview

**Public API (15):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/Production/Unit/{sn}/{pn}` |
| 2 | PUT | `/api/Production/Units` |
| 3 | GET | `/api/Production/UnitVerification` |
| 4 | GET | `/api/Production/SerialNumbers/Types` |
| 5 | GET | `/api/Production/Units/Changes` |
| 6 | DELETE | `/api/Production/Units/Changes/{id}` |
| 7 | PUT | `/api/Production/SetUnitPhase` |
| 8 | PUT | `/api/Production/SetUnitProcess` |
| 9 | POST | `/api/Production/AddChildUnit` |
| 10 | POST | `/api/Production/RemoveChildUnit` |
| 11 | GET | `/api/Production/CheckChildUnits` |
| 12 | POST | `/api/Production/SerialNumbers/Take` |
| 13 | GET | `/api/Production/SerialNumbers/ByRange` |
| 14 | GET | `/api/Production/SerialNumbers/ByReference` |
| 15 | GET/PUT | `/api/Production/SerialNumbers` |
| 16 | GET/PUT | `/api/Production/Batches` |
| 17 | PUT | `/api/Production/Batch` |

**Internal API (18):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/internal/Production/isConnected` |
| 2 | GET | `/api/internal/Production/GetUnit` |
| 3 | GET | `/api/internal/Production/GetUnitInfo` |
| 4 | GET | `/api/internal/Production/GetUnitHierarchy` |
| 5 | GET | `/api/internal/Production/GetUnitStateHistory` |
| 6 | GET | `/api/internal/Production/GetUnitPhase` |
| 7 | GET | `/api/internal/Production/GetUnitProcess` |
| 8 | GET | `/api/internal/Production/GetUnitContents` |
| 9 | POST | `/api/internal/Production/CreateUnit` |
| 10 | POST | `/api/internal/Production/AddChildUnit` |
| 11 | POST | `/api/internal/Production/RemoveChildUnit` |
| 12 | POST | `/api/internal/Production/RemoveAllChildUnits` |
| 13 | GET | `/api/internal/Production/CheckChildUnits` |
| 14 | GET | `/api/internal/Production/SerialNumbers` |
| 15 | GET | `/api/internal/Production/SerialNumbers/Count` |
| 16 | PUT | `/api/internal/Production/SerialNumbers/Free` |
| 17 | GET | `/api/internal/Production/SerialNumbers/Ranges` |
| 18 | GET | `/api/internal/Production/SerialNumbers/Statistics` |
| 19 | GET | `/api/internal/Production/GetSites` |
| 20 | GET | `/api/internal/Mes/GetUnitPhases` |

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `get_unit(sn, pn)` | Public | GET `/api/Production/Unit/{sn}/{pn}` |
| 2 | `create_units(units)` | Public | PUT `/api/Production/Units` |
| 3 | `update_unit(unit)` | Public | PUT `/api/Production/Units` |
| 4 | `verify_unit(sn, pn, rev)` | Public | GET `/api/Production/UnitVerification` |
| 5 | `get_unit_grade(sn, pn, rev)` | Public | GET `/api/Production/UnitVerification` |
| 6 | `is_unit_passing(sn, pn)` | Public | GET `/api/Production/UnitVerification` |
| 7 | `get_serial_number_types()` | Public | GET `/api/Production/SerialNumbers/Types` |
| 8 | `get_phases(force_refresh)` | Public | GET `/api/internal/Mes/GetUnitPhases` |
| 9 | `get_phase(id/code/name)` | Public | GET `/api/internal/Mes/GetUnitPhases` (cached) |
| 10 | `get_phase_id(phase)` | Public | GET `/api/internal/Mes/GetUnitPhases` (cached) |
| 11 | `get_all_unit_phases()` | Public | GET `/api/internal/Mes/GetUnitPhases` (alias) |
| 12 | `get_phase_by_name(name)` | Public | GET `/api/internal/Mes/GetUnitPhases` (cached) |
| 13 | `get_unit_history(sn, pn)` | Public | GET `/api/Production/Units/Changes` |
| 14 | `get_unit_changes(...)` | Public | GET `/api/Production/Units/Changes` |
| 15 | `delete_unit_change(id)` | Public | DELETE `/api/Production/Units/Changes/{id}` |
| 16 | `acknowledge_unit_change(id)` | Public | DELETE `/api/Production/Units/Changes/{id}` (alias) |
| 17 | `get_batches(pn, batch_id)` | Public | GET `/api/Production/Batches` |
| 18 | `create_batch(batch)` | Public | PUT `/api/Production/Batch` |
| 19 | `update_batch(batch)` | Public | PUT `/api/Production/Batch` |
| 20 | `save_batches(batches)` | Public | PUT `/api/Production/Batches` |
| 21 | `set_unit_phase(sn, pn, phase)` | Public | GET `/api/internal/Mes/GetUnitPhases` (resolve) + PUT `/api/Production/SetUnitPhase` |
| 22 | `set_unit_process(sn, pn, ...)` | Public | PUT `/api/Production/SetUnitProcess` |
| 23 | `add_child_to_assembly(...)` | Public | POST `/api/Production/AddChildUnit` |
| 24 | `remove_child_from_assembly(...)` | Public | POST `/api/Production/RemoveChildUnit` |
| 25 | `remove_all_children_from_assembly(...)` | Public | POST `/api/internal/Production/RemoveAllChildUnits` |
| 26 | `verify_assembly(sn, pn, rev)` | Public | GET `/api/Production/CheckChildUnits` |
| 27 | `allocate_serial_numbers(...)` | Public | POST `/api/Production/SerialNumbers/Take` |
| 28 | `find_serial_numbers_in_range(...)` | Public | GET `/api/Production/SerialNumbers/ByRange` |
| 29 | `find_serial_numbers_by_reference(...)` | Public | GET `/api/Production/SerialNumbers/ByReference` |
| 30 | `import_serial_numbers(content)` | Public | PUT `/api/Production/SerialNumbers` |
| 31 | `export_serial_numbers(type)` | Public | GET `/api/Production/SerialNumbers` |
| 32 | `is_connected()` | ⚠️ Internal | GET `/api/internal/Production/isConnected` |
| 33 | `get_sites()` | ⚠️ Internal | GET `/api/internal/Production/GetSites` |
| 34 | `get_unit_info(sn, pn)` | ⚠️ Internal | GET `/api/internal/Production/GetUnitInfo` |
| 35 | `get_unit_hierarchy(sn, pn)` | ⚠️ Internal | GET `/api/internal/Production/GetUnitHierarchy` |
| 36 | `get_unit_state_history(sn, pn)` | ⚠️ Internal | GET `/api/internal/Production/GetUnitStateHistory` |
| 37 | `get_unit_contents(sn, pn, rev)` | ⚠️ Internal | GET `/api/internal/Production/GetUnitContents` |
| 38 | `create_unit(sn, pn, rev, ...)` | ⚠️ Internal | POST `/api/internal/Production/CreateUnit` |
| 39 | `add_child_unit_validated(...)` | ⚠️ Internal | POST `/api/internal/Production/AddChildUnit` |
| 40 | `remove_child_unit_localized(...)` | ⚠️ Internal | POST `/api/internal/Production/RemoveChildUnit` |
| 41 | `remove_all_child_units(...)` | ⚠️ Internal | POST `/api/internal/Production/RemoveAllChildUnits` |
| 42 | `validate_child_units(...)` | ⚠️ Internal | GET `/api/internal/Production/CheckChildUnits` |
| 43 | `find_serial_numbers(...)` | ⚠️ Internal | GET `/api/internal/Production/SerialNumbers` |
| 44 | `get_serial_number_count(...)` | ⚠️ Internal | GET `/api/internal/Production/SerialNumbers/Count` |
| 45 | `free_serial_numbers(ranges)` | ⚠️ Internal | PUT `/api/internal/Production/SerialNumbers/Free` |
| 46 | `get_serial_number_ranges(type)` | ⚠️ Internal | GET `/api/internal/Production/SerialNumbers/Ranges` |
| 47 | `get_serial_number_statistics(type)` | ⚠️ Internal | GET `/api/internal/Production/SerialNumbers/Statistics` |

---

## 3. SOFTWARE MODULE (`AsyncSoftwareService`)

### Module Endpoints Overview

**Public API (12):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/Software/Packages` |
| 2 | GET | `/api/Software/Package/{id}` |
| 3 | GET | `/api/Software/PackageByName` |
| 4 | GET | `/api/Software/PackagesByTag` |
| 5 | POST | `/api/Software/Package` |
| 6 | PUT | `/api/Software/Package/{id}` |
| 7 | DELETE | `/api/Software/Package/{id}` |
| 8 | DELETE | `/api/Software/PackageByName` |
| 9 | POST | `/api/Software/PackageStatus/{id}` |
| 10 | GET | `/api/Software/PackageFiles/{id}` |
| 11 | POST | `/api/Software/Package/UploadZip/{id}` |
| 12 | POST | `/api/Software/Package/FileAttribute/{id}` |
| 13 | GET | `/api/Software/VirtualFolders` |

**Internal API (11):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/internal/Software/isConnected` |
| 2 | GET | `/api/internal/Software/File/{id}` |
| 3 | GET | `/api/internal/Software/CheckFile` |
| 4 | POST | `/api/internal/Software/PostPackageFolder` |
| 5 | POST | `/api/internal/Software/UpdatePackageFolder` |
| 6 | POST | `/api/internal/Software/DeletePackageFolder` |
| 7 | POST | `/api/internal/Software/DeletePackageFolderFiles` |
| 8 | GET | `/api/internal/Software/GetPackageHistory` |
| 9 | GET | `/api/internal/Software/GetPackageDownloadHistory` |
| 10 | GET | `/api/internal/Software/GetRevokedPackages` |
| 11 | GET | `/api/internal/Software/GetAvailablePackages` |
| 12 | GET | `/api/internal/Software/GetSoftwareEntityDetails` |
| 13 | GET | `/api/internal/Software/Log` |

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `get_packages()` | Public | GET `/api/Software/Packages` |
| 2 | `get_package(id)` | Public | GET `/api/Software/Package/{id}` |
| 3 | `get_package_by_name(name, ...)` | Public | GET `/api/Software/PackageByName` |
| 4 | `get_released_package(name)` | Public | GET `/api/Software/PackageByName` |
| 5 | `get_packages_by_tag(tag, val)` | Public | GET `/api/Software/PackagesByTag` |
| 6 | `create_package(name, ...)` | Public | POST `/api/Software/Package` |
| 7 | `update_package(package)` | Public | PUT `/api/Software/Package/{id}` |
| 8 | `delete_package(id)` | Public | DELETE `/api/Software/Package/{id}` |
| 9 | `delete_package_by_name(name)` | Public | DELETE `/api/Software/PackageByName` |
| 10 | `submit_for_review(id)` | Public | POST `/api/Software/PackageStatus/{id}` |
| 11 | `return_to_draft(id)` | Public | POST `/api/Software/PackageStatus/{id}` |
| 12 | `release_package(id)` | Public | POST `/api/Software/PackageStatus/{id}` |
| 13 | `revoke_package(id)` | Public | POST `/api/Software/PackageStatus/{id}` |
| 14 | `get_package_files(id)` | Public | GET `/api/Software/PackageFiles/{id}` |
| 15 | `upload_zip(id, content)` | Public | POST `/api/Software/Package/UploadZip/{id}` |
| 16 | `update_file_attribute(id, attr)` | Public | POST `/api/Software/Package/FileAttribute/{id}` |
| 17 | `get_virtual_folders()` | Public | GET `/api/Software/VirtualFolders` |
| 18 | `is_connected()` | ⚠️ Internal | GET `/api/internal/Software/isConnected` |
| 19 | `get_file(file_id)` | ⚠️ Internal | GET `/api/internal/Software/File/{id}` |
| 20 | `check_file(pkg_id, ...)` | ⚠️ Internal | GET `/api/internal/Software/CheckFile` |
| 21 | `create_package_folder(id, data)` | ⚠️ Internal | POST `/api/internal/Software/PostPackageFolder` |
| 22 | `update_package_folder(data)` | ⚠️ Internal | POST `/api/internal/Software/UpdatePackageFolder` |
| 23 | `delete_package_folder(id)` | ⚠️ Internal | POST `/api/internal/Software/DeletePackageFolder` |
| 24 | `delete_package_folder_files(ids)` | ⚠️ Internal | POST `/api/internal/Software/DeletePackageFolderFiles` |
| 25 | `get_package_history(tags, ...)` | ⚠️ Internal | GET `/api/internal/Software/GetPackageHistory` |
| 26 | `get_package_download_history(id)` | ⚠️ Internal | GET `/api/internal/Software/GetPackageDownloadHistory` |
| 27 | `get_revoked_packages(pkgs)` | ⚠️ Internal | GET `/api/internal/Software/GetRevokedPackages` |
| 28 | `get_available_packages(pkgs)` | ⚠️ Internal | GET `/api/internal/Software/GetAvailablePackages` |
| 29 | `get_software_entity_details(id)` | ⚠️ Internal | GET `/api/internal/Software/GetSoftwareEntityDetails` |
| 30 | `log_download(id, size)` | ⚠️ Internal | GET `/api/internal/Software/Log` |

---

## 4. ASSET MODULE (`AsyncAssetService`)

### Module Endpoints Overview

**Public API (17):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/Asset` |
| 2 | GET | `/api/Asset/{id_or_serial}` |
| 3 | PUT | `/api/Asset` |
| 4 | DELETE | `/api/Asset` |
| 5 | GET | `/api/Asset/Status` |
| 6 | PUT | `/api/Asset/State` |
| 7 | PUT | `/api/Asset/Count` |
| 8 | POST | `/api/Asset/ResetRunningCount` |
| 9 | PUT | `/api/Asset/SetRunningCount` |
| 10 | PUT | `/api/Asset/SetTotalCount` |
| 11 | POST | `/api/Asset/Calibration` |
| 12 | POST | `/api/Asset/Calibration/External` |
| 13 | POST | `/api/Asset/Maintenance` |
| 14 | POST | `/api/Asset/Maintenance/External` |
| 15 | GET | `/api/Asset/Log` |
| 16 | POST | `/api/Asset/Message` |
| 17 | GET | `/api/Asset/Types` |
| 18 | PUT | `/api/Asset/Types` |
| 19 | GET | `/api/Asset/SubAssets` |

**Internal API (3):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | POST | `/api/internal/Blob/Asset` |
| 2 | GET | `/api/internal/Blob/Asset` |
| 3 | GET | `/api/internal/Blob/Asset/List/{id}` |
| 4 | DELETE | `/api/internal/Blob/Assets` |

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `get_assets(filter, orderby, ...)` | Public | GET `/api/Asset` |
| 2 | `get_asset(id_or_serial)` | Public | GET `/api/Asset/{id_or_serial}` |
| 3 | `get_asset_by_serial(sn)` | Public | GET `/api/Asset/{serialNumber}` |
| 4 | `create_asset(sn, type, ...)` | Public | PUT `/api/Asset` |
| 5 | `update_asset(asset)` | Public | PUT `/api/Asset` |
| 6 | `delete_asset(id_or_serial)` | Public | DELETE `/api/Asset` |
| 7 | `get_status(id_or_serial)` | Public | GET `/api/Asset/Status` |
| 8 | `get_asset_state(id)` | Public | GET `/api/Asset/{id}` (extract state) |
| 9 | `set_asset_state(state, ...)` | Public | PUT `/api/Asset/State` |
| 10 | `is_in_alarm(asset)` | Public | _(no endpoint — local check)_ |
| 11 | `is_in_warning(asset)` | Public | _(no endpoint — local check)_ |
| 12 | `get_assets_in_alarm(top)` | Public | GET `/api/Asset` (OData filter) |
| 13 | `get_assets_in_warning(top)` | Public | GET `/api/Asset` (OData filter) |
| 14 | `get_assets_by_alarm_state(state)` | Public | GET `/api/Asset` (OData filter) |
| 15 | `increment_count(id, sn, ...)` | Public | PUT `/api/Asset/Count` |
| 16 | `reset_running_count(id, sn)` | Public | POST `/api/Asset/ResetRunningCount` |
| 17 | `set_running_count(value, ...)` | Public | PUT `/api/Asset/SetRunningCount` |
| 18 | `set_total_count(value, ...)` | Public | PUT `/api/Asset/SetTotalCount` |
| 19 | `record_calibration(id, sn, ...)` | Public | POST `/api/Asset/Calibration` |
| 20 | `record_maintenance(id, sn, ...)` | Public | POST `/api/Asset/Maintenance` |
| 21 | `record_calibration_external(...)` | Public | POST `/api/Asset/Calibration/External` |
| 22 | `record_maintenance_external(...)` | Public | POST `/api/Asset/Maintenance/External` |
| 23 | `get_asset_log(filter, ...)` | Public | GET `/api/Asset/Log` |
| 24 | `add_log_message(id, msg)` | Public | POST `/api/Asset/Message` |
| 25 | `get_asset_types()` | Public | GET `/api/Asset/Types` |
| 26 | `create_asset_type(name, ...)` | Public | PUT `/api/Asset/Types` |
| 27 | `get_child_assets(id, sn)` | Public | GET `/api/Asset/SubAssets` |
| 28 | `add_child_asset(parent, child)` | Public | GET `/api/Asset/{id}` + PUT `/api/Asset` |
| 29 | `upload_file(id, name, content)` | ⚠️ Internal | POST `/api/internal/Blob/Asset` |
| 30 | `download_file(id, name)` | ⚠️ Internal | GET `/api/internal/Blob/Asset` |
| 31 | `list_files(id)` | ⚠️ Internal | GET `/api/internal/Blob/Asset/List/{id}` |
| 32 | `delete_files(id, filenames)` | ⚠️ Internal | DELETE `/api/internal/Blob/Assets` |

---

## 5. REPORT MODULE (`AsyncReportService`)

**Files:** `async_service.py`, `async_repository.py`, `filter_builders.py`, `import_mode.py`, `query_helpers.py`, `report_models/`

### Module Endpoints Overview

**Public API (9):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/Report/Query/Header` |
| 2 | GET | `/api/Report/Query/HeaderByMiscInfo` |
| 3 | GET | `/api/Report/Wsjf/{id}` |
| 4 | POST | `/api/Report/WSJF` |
| 5 | GET | `/api/Report/Wsxf/{id}` |
| 6 | POST | `/api/Report/WSXF` |
| 7 | GET | `/api/Report/Attachment` |
| 8 | GET | `/api/Report/Attachments/{id}` |
| 9 | GET | `/api/Report/Certificate/{id}` |

**Internal API:** _(none)_

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `create_uut_report(...)` | Public | _(no endpoint — local factory)_ |
| 2 | `create_uur_report(...)` | Public | _(no endpoint — local factory)_ |
| 3 | `create_uur_from_uut(uut, operator, comment)` | Public | _(no endpoint — delegates to #2)_ |
| 4 | `query_headers(report_type, expand, ...)` | Public | GET `/api/Report/Query/Header` |
| 5 | `query_uut_headers(expand, filter, top)` | Public | GET `/api/Report/Query/Header` |
| 6 | `query_uur_headers(expand, filter, top)` | Public | GET `/api/Report/Query/Header` |
| 7 | `get_report(report_id, detail_level)` | Public | GET `/api/Report/Wsjf/{id}` |
| 8 | `submit_report(report)` | Public | POST `/api/Report/WSJF` |
| 9 | `submit(report)` | Public | POST `/api/Report/WSJF` (alias) |
| 10 | `get_attachment(attachment_id, step_id)` | Public | GET `/api/Report/Attachment` |
| 11 | `get_all_attachments(report_id)` | Public | GET `/api/Report/Attachments/{id}` |
| 12 | `get_certificate(report_id)` | Public | GET `/api/Report/Certificate/{id}` |
| 13 | `query_headers_with_subunits(...)` | Public | GET `/api/Report/Query/Header` |
| 14 | `query_headers_by_subunit_part_number(pn)` | Public | GET `/api/Report/Query/Header` |
| 15 | `query_headers_by_subunit_serial(sn)` | Public | GET `/api/Report/Query/Header` |
| 16 | `query_headers_by_misc_info(desc, val)` | Public | GET `/api/Report/Query/HeaderByMiscInfo` |
| 17 | `get_headers_by_serial(sn, type, top)` | Public | GET `/api/Report/Query/Header` |
| 18 | `get_headers_by_part_number(pn, type, top)` | Public | GET `/api/Report/Query/Header` |
| 19 | `get_headers_by_date_range(start, end)` | Public | GET `/api/Report/Query/Header` |
| 20 | `get_recent_headers(days, type, top)` | Public | GET `/api/Report/Query/Header` |
| 21 | `get_todays_headers(type, top)` | Public | GET `/api/Report/Query/Header` |
| 22 | `get_report_xml(report_id, ...)` | Public | GET `/api/Report/Wsxf/{id}` |
| 23 | `submit_report_xml(xml_content)` | Public | POST `/api/Report/WSXF` |

---

## 6. ANALYTICS MODULE (`AsyncAnalyticsService`)

### Module Endpoints Overview

**Public API (20):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/App/Version` |
| 2 | GET | `/api/App/Processes` |
| 3 | GET | `/api/App/Levels` |
| 4 | GET | `/api/App/ProductGroups` |
| 5 | POST | `/api/App/DynamicYield` |
| 6 | POST | `/api/App/DynamicRepair` |
| 7 | GET/POST | `/api/App/VolumeYield` |
| 8 | GET/POST | `/api/App/WorstYield` |
| 9 | POST | `/api/App/WorstYieldByProductGroup` |
| 10 | GET/POST | `/api/App/HighVolume` |
| 11 | POST | `/api/App/HighVolumeByProductGroup` |
| 12 | GET/POST | `/api/App/TopFailed` |
| 13 | GET | `/api/App/RelatedRepairHistory` |
| 14 | POST | `/api/App/TestStepAnalysis` |
| 15 | POST | `/api/App/Measurements` |
| 16 | POST | `/api/App/AggregatedMeasurements` |
| 17 | POST | `/api/App/OeeAnalysis` |
| 18 | POST | `/api/App/SerialNumberHistory` |
| 19 | GET/POST | `/api/App/UutReport` |
| 20 | POST | `/api/App/UurReport` |

**Internal API (11):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | POST | `/api/internal/UnitFlow` |
| 2 | GET | `/api/internal/UnitFlow/Links` |
| 3 | GET | `/api/internal/UnitFlow/Nodes` |
| 4 | POST | `/api/internal/UnitFlow/SN` |
| 5 | GET | `/api/internal/UnitFlow/Units` |
| 6 | POST | `/api/internal/UnitFlow/SplitBy` |
| 7 | POST | `/api/internal/UnitFlow/UnitOrder` |
| 8 | GET/POST | `/api/internal/App/MeasurementList` |
| 9 | GET/POST | `/api/internal/App/StepStatusList` |
| 10 | GET/POST | `/api/internal/App/TopFailed` |
| 11 | POST | `/api/internal/Trigger/GetAlarmAndNotificationLogs` |

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `get_version()` | Public | GET `/api/App/Version` |
| 2 | `get_processes(...)` | Public | GET `/api/App/Processes` |
| 3 | `get_levels()` | Public | GET `/api/App/Levels` |
| 4 | `get_product_groups(include_filters)` | Public | GET `/api/App/ProductGroups` |
| 5 | `get_dynamic_yield(filter_data)` | Public | POST `/api/App/DynamicYield` |
| 6 | `get_yield_summary(pn, rev, days)` | Public | POST `/api/App/DynamicYield` |
| 7 | `get_station_yield(station, days)` | Public | POST `/api/App/DynamicYield` |
| 8 | `get_dynamic_repair(filter_data)` | Public | POST `/api/App/DynamicRepair` |
| 9 | `get_volume_yield(filter_data, ...)` | Public | GET/POST `/api/App/VolumeYield` |
| 10 | `get_worst_yield(filter_data, ...)` | Public | GET/POST `/api/App/WorstYield` |
| 11 | `get_worst_yield_by_product_group(...)` | Public | POST `/api/App/WorstYieldByProductGroup` |
| 12 | `get_high_volume(filter_data, ...)` | Public | GET/POST `/api/App/HighVolume` |
| 13 | `get_high_volume_by_product_group(...)` | Public | POST `/api/App/HighVolumeByProductGroup` |
| 14 | `get_top_failed(filter_data, ...)` | Public | GET/POST `/api/App/TopFailed` |
| 15 | `get_related_repair_history(pn, rev)` | Public | GET `/api/App/RelatedRepairHistory` |
| 16 | `get_test_step_analysis(filter_data)` | Public | POST `/api/App/TestStepAnalysis` |
| 17 | `get_test_step_analysis_for_operation(...)` | Public | POST `/api/App/TestStepAnalysis` |
| 18 | `get_measurements(filter_data, paths)` | Public | POST `/api/App/Measurements` |
| 19 | `get_aggregated_measurements(...)` | Public | POST `/api/App/AggregatedMeasurements` |
| 20 | `get_oee_analysis(filter_data)` | Public | POST `/api/App/OeeAnalysis` |
| 21 | `get_serial_number_history(filter_data)` | Public | POST `/api/App/SerialNumberHistory` |
| 22 | `get_uut_reports(filter_data, ...)` | Public | GET/POST `/api/App/UutReport` |
| 23 | `get_uur_reports(filter_data)` | Public | POST `/api/App/UurReport` |
| 24 | `get_unit_flow(filter_data)` | ⚠️ Internal | POST `/api/internal/UnitFlow` |
| 25 | `get_flow_links()` | ⚠️ Internal | GET `/api/internal/UnitFlow/Links` |
| 26 | `get_flow_nodes()` | ⚠️ Internal | GET `/api/internal/UnitFlow/Nodes` |
| 27 | `trace_serial_numbers(sns, filter)` | ⚠️ Internal | POST `/api/internal/UnitFlow/SN` |
| 28 | `get_flow_units()` | ⚠️ Internal | GET `/api/internal/UnitFlow/Units` |
| 29 | `split_flow_by(dimension, filter)` | ⚠️ Internal | POST `/api/internal/UnitFlow/SplitBy` |
| 30 | `set_unit_order(order_by, filter)` | ⚠️ Internal | POST `/api/internal/UnitFlow/UnitOrder` |
| 31 | `set_unit_flow_visibility(show, hide, ...)` | ⚠️ Internal | POST `/api/internal/UnitFlow` |
| 32 | `show_operations(operation_ids, filter)` | ⚠️ Internal | POST `/api/internal/UnitFlow` (via #31) |
| 33 | `hide_operations(operation_ids, filter)` | ⚠️ Internal | POST `/api/internal/UnitFlow` (via #31) |
| 34 | `expand_operations(expand, filter)` | ⚠️ Internal | POST `/api/internal/UnitFlow` |
| 35 | `get_bottlenecks(filter, threshold)` | ⚠️ Internal | POST `/api/internal/UnitFlow` (via #24) |
| 36 | `get_flow_summary(filter_data)` | ⚠️ Internal | POST `/api/internal/UnitFlow` (via #24) |
| 37 | `get_measurement_list(filter, ...)` | ⚠️ Internal | POST `/api/internal/App/MeasurementList` |
| 38 | `get_measurement_list_by_product(...)` | ⚠️ Internal | GET `/api/internal/App/MeasurementList` |
| 39 | `get_step_status_list(filter, ...)` | ⚠️ Internal | POST `/api/internal/App/StepStatusList` |
| 40 | `get_step_status_list_by_product(...)` | ⚠️ Internal | GET `/api/internal/App/StepStatusList` |
| 41 | `get_top_failed_internal(filter, top)` | ⚠️ Internal | POST `/api/internal/App/TopFailed` |
| 42 | `get_top_failed_by_product(pn, ...)` | ⚠️ Internal | GET `/api/internal/App/TopFailed` |
| 43 | `get_alarm_logs(alarm_type, ...)` | ⚠️ Internal | POST `/api/internal/Trigger/GetAlarmAndNotificationLogs` |

---

## 7. ROOTCAUSE MODULE (`AsyncRootCauseService`)

### Module Endpoints Overview

**Public API (7):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/RootCause/Ticket` |
| 2 | GET | `/api/RootCause/Tickets` |
| 3 | POST | `/api/RootCause/Ticket` |
| 4 | PUT | `/api/RootCause/Ticket` |
| 5 | POST | `/api/RootCause/ArchiveTickets` |
| 6 | GET | `/api/RootCause/Attachment` |
| 7 | POST | `/api/RootCause/Attachment` |

**Internal API:** _(none)_

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `get_ticket(ticket_id)` | Public | GET `/api/RootCause/Ticket` |
| 2 | `get_tickets(status, view, search)` | Public | GET `/api/RootCause/Tickets` |
| 3 | `get_open_tickets(view)` | Public | GET `/api/RootCause/Tickets` |
| 4 | `get_active_tickets(view)` | Public | GET `/api/RootCause/Tickets` |
| 5 | `create_ticket(subject, priority, ...)` | Public | POST `/api/RootCause/Ticket` |
| 6 | `update_ticket(ticket)` | Public | PUT `/api/RootCause/Ticket` |
| 7 | `add_comment(ticket_id, comment, ...)` | Public | GET + PUT `/api/RootCause/Ticket` |
| 8 | `change_status(ticket_id, status, ...)` | Public | GET + PUT `/api/RootCause/Ticket` |
| 9 | `assign_ticket(ticket_id, assignee)` | Public | GET + PUT `/api/RootCause/Ticket` |
| 10 | `archive_tickets(ticket_ids)` | Public | POST `/api/RootCause/ArchiveTickets` |
| 11 | `get_attachment(attachment_id, filename)` | Public | GET `/api/RootCause/Attachment` |
| 12 | `upload_attachment(file_content, filename)` | Public | POST `/api/RootCause/Attachment` |

---

## 8. SCIM MODULE (`AsyncScimService`)

### Module Endpoints Overview

**Public API (7):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/SCIM/v2/Token` |
| 2 | GET | `/api/SCIM/v2/Users` |
| 3 | POST | `/api/SCIM/v2/Users` |
| 4 | GET | `/api/SCIM/v2/Users/{id}` |
| 5 | PATCH | `/api/SCIM/v2/Users/{id}` |
| 6 | DELETE | `/api/SCIM/v2/Users/{id}` |
| 7 | GET | `/api/SCIM/v2/Users/userName={userName}` |

**Internal API:** _(none)_

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `get_token(duration_days)` | Public | GET `/api/SCIM/v2/Token` |
| 2 | `get_users(start_index, count)` | Public | GET `/api/SCIM/v2/Users` |
| 3 | `iter_users(page_size, max_users, ...)` | Public | GET `/api/SCIM/v2/Users` (paginated) |
| 4 | `create_user(user)` | Public | POST `/api/SCIM/v2/Users` |
| 5 | `get_user(user_id)` | Public | GET `/api/SCIM/v2/Users/{id}` |
| 6 | `delete_user(user_id)` | Public | DELETE `/api/SCIM/v2/Users/{id}` |
| 7 | `update_user(user_id, patch_request)` | Public | PATCH `/api/SCIM/v2/Users/{id}` |
| 8 | `get_user_by_username(username)` | Public | GET `/api/SCIM/v2/Users/userName={userName}` |
| 9 | `deactivate_user(user_id)` | Public | PATCH `/api/SCIM/v2/Users/{id}` (via #10) |
| 10 | `set_user_active(user_id, active)` | Public | PATCH `/api/SCIM/v2/Users/{id}` |
| 11 | `update_display_name(user_id, name)` | Public | PATCH `/api/SCIM/v2/Users/{id}` |

---

## 9. PROCESS MODULE (`AsyncProcessService`)

### Module Endpoints Overview

**Public API (1):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/App/Processes` |

**Internal API (4):**
| # | Method | Endpoint |
|---|--------|----------|
| 1 | GET | `/api/internal/Process/GetProcesses` |
| 2 | GET | `/api/internal/Process/GetProcess/{id}` |
| 3 | GET | `/api/internal/Process/GetRepairOperations` |
| 4 | GET | `/api/internal/Process/GetRepairOperation/{id}` |

### Per-Function Endpoint Mapping

| # | Service Function | Visibility | Endpoint(s) Used |
|---|-----------------|:---:|---|
| 1 | `get_processes()` | Public | GET `/api/App/Processes` (cached) |
| 2 | `get_test_operations()` | Public | GET `/api/App/Processes` (cached, filtered) |
| 3 | `get_repair_operations()` | Public | GET `/api/App/Processes` (cached, filtered) |
| 4 | `get_wip_operations()` | Public | GET `/api/App/Processes` (cached, filtered) |
| 5 | `get_process_by_code(code)` | Public | GET `/api/App/Processes` (cached) |
| 6 | `get_process_by_name(name)` | Public | GET `/api/App/Processes` (cached) |
| 7 | `get_test_operation(identifier)` | Public | GET `/api/App/Processes` (cached) |
| 8 | `get_repair_operation(identifier)` | Public | GET `/api/App/Processes` (cached) |
| 9 | `get_wip_operation(identifier)` | Public | GET `/api/App/Processes` (cached) |
| 10 | `get_process(identifier)` | Public | GET `/api/App/Processes` (cached) |
| 11 | `is_valid_test_operation(code)` | Public | GET `/api/App/Processes` (cached) |
| 12 | `is_valid_repair_operation(code)` | Public | GET `/api/App/Processes` (cached) |
| 13 | `is_valid_wip_operation(code)` | Public | GET `/api/App/Processes` (cached) |
| 14 | `get_default_test_code()` | Public | GET `/api/App/Processes` (cached) |
| 15 | `get_default_repair_code()` | Public | GET `/api/App/Processes` (cached) |
| 16 | `get_default_test_operation()` | Public | GET `/api/App/Processes` (cached) |
| 17 | `get_default_repair_operation()` | Public | GET `/api/App/Processes` (cached) |
| 18 | `process_exists(code)` | Public | GET `/api/App/Processes` (cached) |
| 19 | `list_process_codes()` | Public | GET `/api/App/Processes` (cached) |
| 20 | `list_process_names()` | Public | GET `/api/App/Processes` (cached) |
| 21 | `refresh()` | Public | GET `/api/App/Processes` |
| 22 | `clear_cache()` | Public | _(no endpoint — local cache only)_ |
| 23 | `get_fail_codes(repair_code)` | ⚠️ Internal | GET `/api/internal/Process/GetRepairOperations` |
| 24 | `get_processes_detailed()` | ⚠️ Internal | GET `/api/internal/Process/GetProcesses` |
| 25 | `get_process_detailed(process_id)` | ⚠️ Internal | GET `/api/internal/Process/GetProcess/{id}` |
| 26 | `get_repair_operation_configs()` | ⚠️ Internal | GET `/api/internal/Process/GetRepairOperations` |
| 27 | `get_repair_operation_config(id, code)` | ⚠️ Internal | GET `/api/internal/Process/GetRepairOperation/{id}` |
| 28 | `get_repair_categories(process_code)` | ⚠️ Internal | GET `/api/internal/Process/GetRepairOperations` |
| 29 | `get_repair_codes(process_code, cat)` | ⚠️ Internal | GET `/api/internal/Process/GetRepairOperations` |

---

## 10. CORE (`AsyncWATS` / `pyWATS` / `AsyncHttpClient`)

**Files:** `src/pywats/async_wats.py`, `src/pywats/pywats.py`, `src/pywats/core/async_client.py`

The core layer provides infrastructure (HTTP client, caching, retry, throttling) and the main API entry point.
It does **not** define domain endpoints — all domain calls are delegated to the 9 modules above.

| # | Function | Source | Visibility | Endpoint(s) Used |
|---|----------|--------|:---:|---|
| 1 | `AsyncWATS.test_connection()` | async_wats.py | Public | _(delegates to `analytics.get_version()`)_ |
| 2 | `AsyncWATS.get_version()` | async_wats.py | Public | _(delegates to `analytics.get_version()`)_ |
| 3 | `pyWATS.test_connection()` | pywats.py | Public | _(delegates to `analytics.get_version()` via sync wrapper)_ |
| 4 | `pyWATS.get_version()` | pywats.py | Public | _(delegates to `analytics.get_version()` via sync wrapper)_ |

**Non-HTTP infrastructure in `src/pywats/core/`:**

| File | Purpose | HTTP Calls? |
|------|---------|:-----------:|
| `async_client.py` / `client.py` | Generic HTTP transport (`.get()`, `.post()`, etc.) | Transport layer — called _by_ domain repos, no hardcoded endpoints |
| `routes.py` | Centralized route constants (`Routes.App.*`, `Routes.Product.*`, etc.) | None — consumed by repositories |
| `station.py` | Station identity & registration | None |
| `cache.py` | Response caching | None |
| `config.py` | Configuration parsing | None |
| `retry.py` / `retry_handler.py` | Retry logic | None |
| `circuit_breaker.py` | Circuit breaker pattern | None |
| `throttle.py` | Request throttling | None |
| `pagination.py` | OData pagination helpers | None |
| `parallel.py` | Parallel request helpers | None |
| `performance.py` | Performance monitoring | None |
| `validation.py` | Input validation | None |
| `sync_runner.py` | Async→sync bridge | None |
| `metrics.py` | Metrics collection | None |
| `coalesce.py` | Request coalescing | None |
| `event_loop_pool.py` | Event loop management | None |

---

## 11. CLIENT (`pywats_client`)

**Files:** `src/pywats_client/` — Client service, diagnostics, queue, control, IPC

The client package manages the pyWATS service lifecycle. Most components delegate to `AsyncWATS` domain services.
Only a few files make direct HTTP calls:

### Per-Function Endpoint Mapping

| # | Function | Source | Visibility | Endpoint(s) Used | Notes |
|---|----------|--------|:---:|---|---|
| 1 | `Diagnostics._check_wats_server()` | diagnostics.py | ⚠️ Internal | GET `/api/health`, GET `/api/version` | Direct httpx; infrastructure connectivity check |
| 2 | `_check_server_connectivity(url)` | __main__.py | ⚠️ Internal | GET `/api/health` | Direct httpx; startup preflight check |
| 3 | `AsyncPendingQueue._submit_report()` | service/async_pending_queue.py | ⚠️ Internal | _(delegates to `api.report.submit_raw()`)_ | Uses domain service, not direct HTTP |
| 4 | `AsyncClientService._init_api()` | service/async_client_service.py | ⚠️ Internal | _(delegates to `api.get_version()`)_ | Uses AsyncWATS delegation |
| 5 | `AsyncClientService._watchdog_loop()` | service/async_client_service.py | ⚠️ Internal | _(delegates to `api.get_version()`)_ | Health polling via AsyncWATS |

### Health Server (HTTP server — exposes local endpoints)

`health_server.py` runs a local HTTP server (default port 8080) for Docker/K8s health probes.
These are **served** endpoints, not WATS API client calls.

| # | Handler | Method | Endpoint Served | Purpose |
|---|---------|--------|-----------------|--------|
| 1 | `_handle_health()` | GET | `/health` | Basic health check (200/503) |
| 2 | `_handle_liveness()` | GET | `/health/live` | Liveness probe |
| 3 | `_handle_readiness()` | GET | `/health/ready` | Readiness probe |
| 4 | `_handle_details()` | GET | `/health/details` | Detailed health JSON |
| 5 | `_handle_metrics()` | GET | `/metrics` | Prometheus/JSON metrics |

### Non-HTTP Client Components

| Package | Purpose | HTTP Calls? |
|---------|---------|:-----------:|
| `control/` | OS service management (systemd, launchd, NSSM, Win32) | None |
| `converters/` | File format conversion (XML/CSV → WATS JSON) | None |
| `core/` | Config, auth, encryption, event bus | None |
| `queue/persistent_queue.py` | File-based persistent queue | None |
| `service/async_ipc_server.py` / `async_ipc_client.py` | Named pipe / Unix socket IPC | None |
| `service/service_tray.py` | System tray UI | None |
| `service/async_converter_pool.py` | Converter worker pool | None |
| `io.py` | File I/O utilities | None |
| `launcher.py` | Service instance launching | None |

---

## 12. UI (`pywats_ui`)

**Files:** `src/pywats_ui/apps/configurator/` — Qt-based configuration GUI

The UI layer has a few components that make direct `httpx` calls for connection testing and report submission,
bypassing the domain service layer.

### Per-Function Endpoint Mapping

| # | Function | Source | Visibility | Endpoint(s) Used | Notes |
|---|----------|--------|:---:|---|---|
| 1 | `MainWindow._send_queued_report(data)` | main_window.py | ⚠️ Internal | POST `{url}/api/Report/wats` | Direct httpx.AsyncClient; sends queued report |
| 2 | `MainWindow._bg_connection_check()` | main_window.py | ⚠️ Internal | GET `{url}/api/Report/wats/info` | Direct httpx.Client; background thread |
| 3 | `ConnectionPage._run_connection_test()` | pages/connection.py | ⚠️ Internal | GET `{url}/api/Report/wats/info` | Direct httpx.AsyncClient; retries + lowercase fallback |
| 4 | `ConnectionPage._run_send_uut_test()` | pages/connection.py | ⚠️ Internal | POST `{url}/api/Report/wats` | Via QueueManager.enqueue() → `_send_queued_report()` |

### Non-HTTP UI Components

| Package | Purpose | HTTP Calls? |
|---------|---------|:-----------:|
| `framework/` | Qt base classes, theming, reliability | None (except ConnectionMonitor which delegates to `_check_connection()`) |
| `widgets/` | Reusable Qt widgets | None |
| `dialogs/` | Dialog windows | None |
| `apps/configurator/pages/` (other pages) | Settings, dashboard, logs | None |

---

## 13. NON-HTTP PACKAGES (No Endpoint Calls)

The following packages were scanned and confirmed to make **zero** HTTP endpoint calls:

| Package | Location | Purpose |
|---------|----------|--------|
| **queue** | `src/pywats/queue/` | In-memory queuing, XML/JSON format parsing |
| **shared** | `src/pywats/shared/` | OData query building, service discovery, enums |
| **tools** | `src/pywats/tools/` | Test report builder utility |
| **sync** | `src/pywats/sync.py` | Sync wrapper — delegates to async services |
| **cfx** | `src/pywats_cfx/` | CFX integration via AMQP (RabbitMQ), not HTTP |
| **events** | `src/pywats_events/` | Event system via MQTT/AMQP patterns |
| **dev** | `src/pywats_dev/` | Endpoint scanner (static analysis tool) |
| **converters** | `converters/` | Top-level converter directory |

---

## Notes

- **Public endpoints** use `/api/{Domain}/...` and require API token authentication.
- **Internal endpoints** use `/api/internal/{Domain}/...` and require a `Referer` header matching the base URL.
- Functions marked ⚠️ Internal may change without notice between WATS versions.
- Some public service functions internally use internal endpoints (e.g., `get_phases()` uses `/api/internal/Mes/GetUnitPhases`).
- Functions like `is_active()`, `is_in_alarm()`, `is_in_warning()` are local helpers with no backend call.
- The Process module heavily caches — most functions use cached data from a single `GET /api/App/Processes` call.
- Analytics shares the `/api/App/...` endpoint namespace with Process for server-metadata routes.
- The UI module uses `/api/Report/wats` and `/api/Report/wats/info` — these are the **legacy WATS TDM endpoints** (different from the domain API's `/api/Report/WSJF`).
- The Client health server **serves** local endpoints (`/health`, `/metrics`) — these are not calls to the WATS backend.
- Non-HTTP packages use AMQP (CFX), MQTT (Events), named pipes (IPC), or filesystem (queue, converters) for communication.
