# Endpoint Risk Assessment Report

**Generated:** 2026-02-07 02:01:22  
**Total Endpoints:** 60  
**Internal Endpoints:** 16  
**Public Endpoints:** 44

---

## 📊 Executive Summary

### Priority Breakdown
- **CRITICAL:** 2 endpoints (2 internal)
- **HIGH:** 10 endpoints (1 internal)
- **MEDIUM:** 33 endpoints
- **LOW:** 15 endpoints

### Risk Assessment
- **2** critical internal endpoints need public alternatives
- **1** high-priority internal endpoints at risk
- **6** internal endpoints have identified alternatives

---

## CRITICAL Priority Endpoints (2 total)

| Endpoint | Domain | Type | Usage | Used By (Sample) | Notes |
|----------|--------|------|-------|------------------|-------|
| `{...}/GetProcess/{...}` | Process | ⚠️ Internal | 1x | async_repository.get_process | ⚠️ **No public alternative** |
| `{...}/GetRepairOperation/{...}` | Process | ⚠️ Internal | 1x | async_repository.get_repair_operation | ⚠️ **No public alternative** |

## HIGH Priority Endpoints (10 total)

| Endpoint | Domain | Type | Usage | Used By (Sample) | Notes |
|----------|--------|------|-------|------------------|-------|
| `{...}/Attachments/{...}` | Report | ✅ Public | 1x | async_repository.get_attachments_as_zip | - |
| `{...}/Certificate/{...}` | Report | ✅ Public | 1x | async_repository.get_certificate | - |
| `{...}/Wsjf/{...}` | Report | ✅ Public | 1x | async_repository.get_wsjf | - |
| `{...}/Wsxf/{...}` | Report | ✅ Public | 1x | async_repository.get_wsxf | - |
| `/api/Process` | Process | ✅ Public | 0x | - | _Unused_ |
| `/api/internal/Process` | Process | ⚠️ Internal | 0x | - | Alt: `/api/Process` _Unused_ |
| `{...}/{...}` | Process | ✅ Public | 0x | - | _Unused_ |
| `/api/Report` | Report | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}` | Report | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}` | Report | ✅ Public | 0x | - | _Unused_ |

## MEDIUM Priority Endpoints (33 total)

| Endpoint | Domain | Type | Usage | Used By (Sample) | Notes |
|----------|--------|------|-------|------------------|-------|
| `/api/Asset` | Asset | ✅ Public | 3x | async_repository.delete, async_repository.get_all (+1 more) | - |
| `{...}/{...}` | Software | ✅ Public | 3x | async_repository.delete_package, async_repository.get_package (+1 more) | - |
| `/api/internal/Blob/Asset` | Asset | ⚠️ Internal | 2x | async_repository.download_file, async_repository.upload_file | Alt: `/api/Asset` |
| `/api/Product` | Product | ✅ Public | 2x | async_repository.get_revision, async_repository.save | - |
| `/api/internal/Product` | Product | ⚠️ Internal | 2x | async_repository.get_revision, async_repository.save | Alt: `/api/Product` |
| `/api/internal/Blob/Assets` | Asset | ⚠️ Internal | 1x | async_repository.delete_files | Alt: `/api/Assets` |
| `{...}/List/{...}` | Asset | ⚠️ Internal | 1x | async_repository.list_files | - |
| `{...}/{...}` | Product | ✅ Public | 1x | async_repository.get_by_part_number | - |
| `{...}/{...}` | Product | ✅ Public | 1x | async_repository.delete_vendor | - |
| `{...}/{...}` | Production | ✅ Public | 1x | async_repository.delete_unit_change | - |
| `{...}/{...}/{...}` | Production | ✅ Public | 1x | async_repository.get_unit | - |
| `{...}/File/{...}` | Software | ⚠️ Internal | 1x | async_repository.get_file | - |
| `{...}/FileAttribute/{...}` | Software | ✅ Public | 1x | async_repository.update_file_attribute | - |
| `{...}/PackageFiles/{...}` | Software | ✅ Public | 1x | async_repository.get_package_files | - |
| `{...}/PackageStatus/{...}` | Software | ✅ Public | 1x | async_repository.update_package_status | - |
| `{...}/UploadZip/{...}` | Software | ✅ Public | 1x | async_repository.upload_package_zip | - |
| `/api/App` | App | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}` | Asset | ⚠️ Internal | 0x | - | _Unused_ |
| `{...}/{...}/Calibrations` | Asset | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}/Maintenance` | Asset | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}/Status` | Asset | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}/{...}` | Asset | ⚠️ Internal | 0x | - | _Unused_ |
| `{...}/{...}/Revisions` | Product | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}/{...}` | Product | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}/{...}/BOM` | Product | ✅ Public | 0x | - | _Unused_ |
| `/api/Production` | Production | ✅ Public | 0x | - | _Unused_ |
| `/api/internal/Mes` | Production | ⚠️ Internal | 0x | - | _Unused_ |
| `/api/internal/Production` | Production | ⚠️ Internal | 0x | - | Alt: `/api/Production` _Unused_ |
| `{...}/{...}` | Production | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}` | Production | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}` | Production | ✅ Public | 0x | - | _Unused_ |
| `/api/Software` | Software | ✅ Public | 0x | - | _Unused_ |
| `/api/internal/Software` | Software | ⚠️ Internal | 0x | - | Alt: `/api/Software` _Unused_ |

## LOW Priority Endpoints (15 total)

| Endpoint | Domain | Type | Usage | Used By (Sample) | Notes |
|----------|--------|------|-------|------------------|-------|
| `/api/internal/UnitFlow` | Analytics | ⚠️ Internal | 3x | async_repository.expand_unit_flow_operations, async_repository.query_unit_flow (+1 more) | - |
| `{...}/{...}` | SCIM | ✅ Public | 3x | async_repository.delete_user, async_repository.get_user (+1 more) | - |
| `{...}/{...}` | Asset | ✅ Public | 2x | async_repository.get_by_id, async_repository.get_by_serial_number | - |
| `{...}/userName={...}` | SCIM | ✅ Public | 1x | async_repository.get_user_by_username | - |
| `/api/Analytics` | Analytics | ✅ Public | 0x | - | _Unused_ |
| `/api/internal/App` | Analytics | ⚠️ Internal | 0x | - | _Unused_ |
| `/api/internal/Trigger` | Analytics | ⚠️ Internal | 0x | - | _Unused_ |
| `{...}/TestStatistics` | Analytics | ✅ Public | 0x | - | _Unused_ |
| `/api/Assets` | Asset | ✅ Public | 0x | - | _Unused_ |
| `/api/RootCause` | RootCause | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}` | RootCause | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}/Comment` | RootCause | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}/Status` | RootCause | ✅ Public | 0x | - | _Unused_ |
| `/api/SCIM/v2` | SCIM | ✅ Public | 0x | - | _Unused_ |
| `{...}/{...}` | SCIM | ✅ Public | 0x | - | _Unused_ |

## 🎯 Public API Gap Analysis

**2 critical/high-priority internal endpoints need public alternatives**

### Process Domain (2 gaps)

| Endpoint | Priority | Usage | Migration Effort |
|----------|----------|-------|------------------|
| `{...}/GetProcess/{...}` | CRITICAL | 1x | Low (<5 usages) |
| `{...}/GetRepairOperation/{...}` | CRITICAL | 1x | Low (<5 usages) |


## 📋 Migration Recommendations

### Phase 1: Critical Path (Immediate)


### Phase 2: High Priority (Next Quarter)


### Migration Strategy

1. **Create public endpoints** for Phase 1 critical path
2. **Deprecate internal endpoints** with 6-month sunset period
3. **Migrate usage** incrementally (domain by domain)
4. **Remove internal endpoints** after migration complete

---

## 📈 Usage Statistics

### Overall
- **Total Endpoints:** 60
- **Used Endpoints:** 26 (43.3%)
- **Unused Endpoints:** 34 (56.7%)
- **Total Usage Count:** 38
- **Average Usage:** 0.6 calls per endpoint

### Top 10 Most Used Endpoints

1. ✅ `/api/Asset` - **3** usages (MEDIUM)
2. ✅ `{...}/{...}` - **3** usages (MEDIUM)
3. ⚠️ `/api/internal/UnitFlow` - **3** usages (LOW)
4. ✅ `{...}/{...}` - **3** usages (LOW)
5. ✅ `/api/Product` - **2** usages (MEDIUM)
6. ⚠️ `/api/internal/Product` - **2** usages (MEDIUM)
7. ✅ `{...}/{...}` - **2** usages (LOW)
8. ⚠️ `/api/internal/Blob/Asset` - **2** usages (MEDIUM)
9. ✅ `{...}/{...}/{...}` - **1** usages (MEDIUM)
10. ✅ `{...}/{...}` - **1** usages (MEDIUM)