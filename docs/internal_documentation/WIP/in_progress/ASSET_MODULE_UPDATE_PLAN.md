# Asset Module Update Implementation Plan

**Date:** 2026-01-26  
**Release Target:** WATS 25.3 Compatibility  
**Status:** ✅ IMPLEMENTED

---

## Implementation Complete

All WATS 25.3 asset enhancements have been implemented:

### New Methods Added

| Method | Endpoint | Description |
|--------|----------|-------------|
| `set_running_count()` | `PUT /api/Asset/SetRunningCount` | Set running count to specific value |
| `set_total_count()` | `PUT /api/Asset/SetTotalCount` | Set total count to specific value |
| `record_calibration_external()` | `POST /api/Asset/Calibration/External` | External calibration with date range |
| `record_maintenance_external()` | `POST /api/Asset/Maintenance/External` | External maintenance with date range |

### New Enum Added

```python
class IntervalMode(IntEnum):
    NORMAL = 0      # Standard interval-based
    UNLIMITED = -1  # No limit
    EXTERNAL = -2   # Managed by external system
```

### Files Modified

1. ✅ `src/pywats/core/routes.py` - Added 4 new route constants
2. ✅ `src/pywats/domains/asset/enums.py` - Added `IntervalMode` enum
3. ✅ `src/pywats/domains/asset/async_repository.py` - Added 4 repository methods
4. ✅ `src/pywats/domains/asset/async_service.py` - Added 4 async service methods
5. ✅ `src/pywats/domains/asset/service.py` - Added 4 sync wrapper methods
6. ✅ `src/pywats/domains/asset/__init__.py` - Added `IntervalMode` export
7. ✅ `api-tests/asset/test_integration.py` - Added integration tests
8. ✅ `docs/modules/asset.md` - Updated documentation

---

## Executive Summary

The WATS 25.3 release introduces significant enhancements to asset calibration and maintenance handling, including new "External" calibration/maintenance modes and direct count manipulation endpoints. This document analyzes the current pyWATS implementation against the new public API endpoints and provides a detailed implementation plan.

---

## 1. Current Implementation Analysis

### 1.1 Existing Public Endpoints (Implemented ✅)

| Endpoint | Method | Status | Current Implementation |
|----------|--------|--------|----------------------|
| `/api/Asset` | GET | ✅ | `get_assets()` - Full OData support |
| `/api/Asset` | PUT | ✅ | `create_asset()`, `update_asset()` |
| `/api/Asset` | DELETE | ✅ | `delete_asset()` |
| `/api/Asset/{assetId}` | GET | ✅ | `get_asset(asset_id=...)` |
| `/api/Asset/{serialNumber}` | GET | ✅ | `get_asset(serial_number=...)` |
| `/api/Asset/Calibration` | POST | ✅ | `record_calibration()` |
| `/api/Asset/Count` | PUT | ✅ | `increment_count()` |
| `/api/Asset/Log` | GET | ✅ | `get_asset_log()` |
| `/api/Asset/Maintenance` | POST | ✅ | `record_maintenance()` |
| `/api/Asset/Message` | POST | ✅ | `add_log_message()` |
| `/api/Asset/ResetRunningCount` | POST | ✅ | `reset_running_count()` |
| `/api/Asset/State` | PUT | ✅ | `set_asset_state()` |
| `/api/Asset/Status` | GET | ✅ | `get_status()` |
| `/api/Asset/SubAssets` | GET | ✅ | `get_child_assets()` |
| `/api/Asset/Types` | GET | ✅ | `get_asset_types()` |
| `/api/Asset/Types` | PUT | ✅ | `create_asset_type()` |

### 1.2 New Public Endpoints (Not Implemented ❌)

| Endpoint | Method | Priority | Description |
|----------|--------|----------|-------------|
| `/api/Asset/Calibration/External` | POST | **HIGH** | External calibration with custom date ranges |
| `/api/Asset/Maintenance/External` | POST | **HIGH** | External maintenance with custom date ranges |
| `/api/Asset/SetRunningCount` | PUT | **HIGH** | Set running count to specific value |
| `/api/Asset/SetTotalCount` | PUT | **HIGH** | Set total count to specific value |

---

## 2. Gap Analysis

### 2.1 Missing Functionality

#### 2.1.1 External Calibration Support (Critical)

**Current State:**
- `record_calibration()` only accepts `date_time` (calibration date)
- No support for `next_calibration_date` (custom "To Date")
- No way to integrate with external calibration systems

**Required:**
- New `record_calibration_external()` method
- Parameters: `from_date`, `to_date`, `comment`
- Endpoint: `POST /api/Asset/Calibration/External`

#### 2.1.2 External Maintenance Support (Critical)

**Current State:**
- `record_maintenance()` only accepts `date_time`
- No support for `next_maintenance_date` (custom "To Date")

**Required:**
- New `record_maintenance_external()` method
- Parameters: `from_date`, `to_date`, `comment`
- Endpoint: `POST /api/Asset/Maintenance/External`

#### 2.1.3 Direct Count Manipulation (Critical)

**Current State:**
- `increment_count()` can only increment
- `reset_running_count()` can only reset to 0
- No way to set counts to arbitrary values

**Required:**
- New `set_running_count()` method
- New `set_total_count()` method
- Both accept: `asset_id/serial_number`, `value`

### 2.2 Model Updates Required

The `AssetType` model should support new dropdown options:

| Field | Current | New Options |
|-------|---------|-------------|
| `running_count_limit` | `int` | Add support for `Unlimited` (-1 or null) |
| `total_count_limit` | `int` | Add support for `Unlimited` (-1 or null) |
| `calibration_interval` | `float` | Add support for `Unlimited` and `External` |
| `maintenance_interval` | `float` | Add support for `Unlimited` and `External` |

**Note:** Need to verify server API response to understand how `Unlimited` and `External` values are represented (likely -1 or -2).

---

## 3. Implementation Plan

### Phase 1: Routes Update (5 min)

Add new routes to `src/pywats/core/routes.py`:

```python
# In class Asset:
CALIBRATION_EXTERNAL = f"{BASE}/Calibration/External"
MAINTENANCE_EXTERNAL = f"{BASE}/Maintenance/External"
SET_RUNNING_COUNT = f"{BASE}/SetRunningCount"
SET_TOTAL_COUNT = f"{BASE}/SetTotalCount"
```

### Phase 2: Repository Layer (15 min)

Add to `src/pywats/domains/asset/async_repository.py`:

1. `post_calibration_external()`
2. `post_maintenance_external()`
3. `set_running_count()`
4. `set_total_count()`

### Phase 3: Service Layer (15 min)

Add to `src/pywats/domains/asset/async_service.py`:

1. `record_calibration_external()`
2. `record_maintenance_external()`
3. `set_running_count()`
4. `set_total_count()`

Add sync wrappers to `src/pywats/domains/asset/service.py`.

### Phase 4: Enum Updates (5 min)

Add to `src/pywats/domains/asset/enums.py`:

```python
class IntervalMode(IntEnum):
    """Interval mode for calibration/maintenance."""
    NORMAL = 0      # Standard interval-based
    UNLIMITED = -1  # No limit
    EXTERNAL = -2   # Managed by external system
```

### Phase 5: Documentation (10 min)

Update `docs/modules/asset.md` with:
- New external calibration/maintenance methods
- Direct count manipulation methods
- New interval modes

### Phase 6: Tests (15 min)

Add integration tests for:
- External calibration workflow
- External maintenance workflow
- Set running/total count

---

## 4. API Method Signatures

### 4.1 New Methods

```python
# External Calibration
async def record_calibration_external(
    self,
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    from_date: Optional[datetime] = None,  # lastCalibrationDate
    to_date: Optional[datetime] = None,    # nextCalibrationDate
    comment: Optional[str] = None
) -> bool:
    """
    Record external calibration with custom date range.
    
    Use when calibration is managed by an external system.
    Allows setting both 'last calibration' and 'next calibration' dates.
    
    Args:
        asset_id: Asset ID (GUID)
        serial_number: Asset serial number (alternative)
        from_date: Date calibration was performed (default: now)
        to_date: Date next calibration is due
        comment: Optional log message
        
    Returns:
        True if successful
    """

# External Maintenance
async def record_maintenance_external(
    self,
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    from_date: Optional[datetime] = None,  # lastMaintenanceDate
    to_date: Optional[datetime] = None,    # nextMaintenanceDate
    comment: Optional[str] = None
) -> bool:
    """
    Record external maintenance with custom date range.
    
    Use when maintenance is managed by an external system.
    Allows setting both 'last maintenance' and 'next maintenance' dates.
    """

# Set Running Count
async def set_running_count(
    self,
    value: int,
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    comment: Optional[str] = None
) -> bool:
    """
    Set the running count to a specific value.
    
    Requires 'Edit Total count' permission on server.
    
    Args:
        value: New running count value
        asset_id: Asset ID
        serial_number: Asset serial number (alternative)
        comment: Optional log message
        
    Returns:
        True if successful
    """

# Set Total Count
async def set_total_count(
    self,
    value: int,
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    comment: Optional[str] = None
) -> bool:
    """
    Set the total count to a specific value.
    
    Requires 'Edit Total count' permission on server.
    
    Args:
        value: New total count value
        asset_id: Asset ID
        serial_number: Asset serial number (alternative)
        comment: Optional log message
        
    Returns:
        True if successful
    """
```

---

## 5. Files to Modify

| File | Changes |
|------|---------|
| `src/pywats/core/routes.py` | Add 4 new route constants |
| `src/pywats/domains/asset/enums.py` | Add `IntervalMode` enum |
| `src/pywats/domains/asset/async_repository.py` | Add 4 new repository methods |
| `src/pywats/domains/asset/async_service.py` | Add 4 new service methods |
| `src/pywats/domains/asset/service.py` | Add 4 sync wrapper methods |
| `docs/modules/asset.md` | Document new functionality |
| `api-tests/asset/test_integration.py` | Add integration tests |

---

## 6. Backward Compatibility

All changes are **additive**:
- No existing methods are modified
- No signatures change
- No breaking changes to models

Existing code will continue to work without modification.

---

## 7. Testing Strategy

### Unit Tests
- Mock repository tests for new service methods
- Verify parameter passing

### Integration Tests (against test server)
```python
def test_external_calibration():
    """Test external calibration workflow."""
    # Create asset with External calibration mode
    # Record calibration with custom to_date
    # Verify next_calibration_date is set

def test_set_running_count():
    """Test setting running count directly."""
    # Get asset, note current count
    # Set to new value
    # Verify new count

def test_set_total_count():
    """Test setting total count directly."""
    # Get asset, note current count
    # Set to new value  
    # Verify new count (requires permission)
```

---

## 8. Implementation Checklist

- [ ] Add routes to `routes.py`
- [ ] Add `IntervalMode` enum
- [ ] Implement `post_calibration_external` in repository
- [ ] Implement `post_maintenance_external` in repository
- [ ] Implement `set_running_count` in repository
- [ ] Implement `set_total_count` in repository
- [ ] Add async service methods
- [ ] Add sync service wrapper methods
- [ ] Update `__init__.py` exports
- [ ] Update documentation
- [ ] Add integration tests
- [ ] Test against WATS server

---

## 9. Estimated Effort

| Phase | Time |
|-------|------|
| Routes | 5 min |
| Enums | 5 min |
| Repository | 15 min |
| Async Service | 15 min |
| Sync Service | 10 min |
| Documentation | 10 min |
| Tests | 15 min |
| **Total** | **~75 min** |

---

## 10. Ready to Implement

All analysis is complete. The implementation can proceed by following the phases outlined above. Start with Phase 1 (Routes) and proceed sequentially.

**Recommendation:** Implement in a single commit with message:
```
feat(asset): add external calibration/maintenance and direct count manipulation

- Add POST /api/Asset/Calibration/External support
- Add POST /api/Asset/Maintenance/External support  
- Add PUT /api/Asset/SetRunningCount support
- Add PUT /api/Asset/SetTotalCount support
- Add IntervalMode enum for Unlimited/External modes
- Update documentation and tests

Implements WATS 25.3 Asset Manager improvements
```
