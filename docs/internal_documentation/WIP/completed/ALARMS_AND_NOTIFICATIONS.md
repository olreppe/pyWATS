# Alarms and Notifications Analysis

**Date:** 2026-01-26  
**Status:** ✅ Implemented

---

## Implementation Summary

This feature has been implemented in pyWATS:

- **API Method:** `api.analytics.get_alarm_logs()`
- **Enum:** `AlarmType` with 5 types (REPORT, YIELD_VOLUME, SERIAL_NUMBER, MEASUREMENT, ASSET)
- **Model:** `AlarmLog` with comprehensive fields for all alarm types
- **Example:** `examples/analytics/alarm_monitor.py` - Production-ready polling service
- **Documentation:** `docs/modules/analytics.md` - Alarm section with usage examples
- **Tests:** `api-tests/analytics/test_integration.py::TestAlarmLogs`

---

## Background

In WATS you can define alarms that trigger an email sent to a user or user role. Customers have requested:
1. API access to retrieve triggered alarms
2. Webhook/event integration to receive alarms when triggered

**Naming Note:** Don't use "trigger" in the public API - use "alarm" or "notification" as that's the WATS terminology.

---

## Endpoint Analysis

### Available Endpoints (Internal API)

| Endpoint | Method | Permission | Description |
|----------|--------|------------|-------------|
| `/api/internal/Trigger/GetAlarmAndNotificationLogs` | POST | ✅ Standard | **Primary endpoint** - Retrieve alarm logs |
| `/api/internal/Trigger/GetTriggers` | GET | ❌ Admin | Get alarm definitions |
| `/api/internal/Trigger/GetTriggerActions` | GET | ❌ Admin | Get action types |
| `/api/internal/Trigger/GetTriggerFieldTypes` | GET | ❌ Admin | Get field types |
| `/api/internal/Trigger/GetTriggerOperators` | GET | ❌ Admin | Get operators |
| `/api/internal/Trigger/*` (write ops) | PUT/POST/DELETE | ❌ Admin | Alarm management |

**Key Finding:** Only `GetAlarmAndNotificationLogs` is accessible to standard API users. All alarm definition/management endpoints require admin permissions.

### GetAlarmAndNotificationLogs Response Structure

**Supported Filters (POST body):**
- `level` - Filter by alarm level
- `productGroup` - Filter by product group
- `dateFrom` - Start date filter
- `dateTo` - End date filter  
- `topCount` - Limit results

**Response Fields (111 records on test server):**

```json
{
  "logId": 140,
  "name": "FPY drops by 10% last 7 days",
  "logDate": "2026-01-26T00:01:10.3366667",
  "triggerId": 5,
  "reportGuid": null,
  "state": "C",
  "type": 2,
  "groupingSet": "partnumber, processcode",
  "calculationsString": "fpy, fpytrend",
  "clientGroupIds": [0],
  "productSelectionIds": [-1],
  "partNumber": "4494394418",
  "productName": "",
  "processCode": "50",
  "processName": "PCBA test",
  "fpy": 0.75,
  "spy": 0.928571,
  "tpy": 1.0,
  "lpy": 1.0,
  "testYield": 0.734177,
  "fpyTrend": -0.128316,
  "spyTrend": -0.0540957,
  "tpyTrend": 0.00990449,
  "lpyTrend": 0.00707464,
  "testYieldTrend": -0.141211,
  "uutCount": 79,
  "unitCount": 28,
  "fpCount": 21,
  "lpCount": 21,
  "retestCount": 51,
  "sequenceCount": 2,
  "sequentialMatch": 1,
  "isDaysSinceCalibrationUnknown": false,
  "isDaysSinceMaintenanceUnknown": false
}
```

### Alarm Types (5 Total)

From WATS Web GUI dropdown:

| Type | Name | Description | Key Fields |
|------|------|-------------|------------|
| **1** | **Reports (UUT)** | Unit-based alarms triggered by test results | `reportGuid`, `serialNumber`, `stationName`, `operator`, `result` |
| **2** | **Yield & volume** | Yield/statistics alarms on aggregated data | `fpy`, `spy`, `tpy`, `lpy`, `fpyTrend`, `uutCount`, `unitCount` |
| **3** | **Serial number handler** | Serial number pool monitoring | `free` (free count), `reserved` (reserved count), `serialNumberType` |
| **4** | **Measurements** | Measurement statistics and SPC alarms | `cp`, `cpk`, `min`, `max`, `avg`, `stdev`, `measurementPath` |
| **5** | **Assets** | Asset status and maintenance alarms | `assetname`, `serialnumber`, `typeid`, `state`, `bubbledstatus`, `tags` |

**Type 1 (Reports/UUT) Example:**
```json
{
  "logId": 138,
  "name": "Unit not passed after 5'th run",
  "type": 1,
  "reportGuid": "9e5e6e5a-b588-406b-973f-2c520a742124",
  "partNumber": "4494394418",
  "serialNumber": "244950015144",
  "revision": "03",
  "processName": "PCBA test",
  "stationName": "WVXM-NGH-Z-970",
  "operator": "te85",
  "startUtc": "2026-01-21T10:23:44"
}
```

**States Observed:** `C` (likely "Created" or "Completed")

---

## Implementation Recommendation

### Option 1: Add to Analytics Domain (Recommended)

**Rationale:**
- Most alarm types (Yield, Measurements) are analytics-related
- Analytics already handles yield statistics and KPIs
- Read-only method fits with existing analytics patterns
- Asset alarms could alternatively go to Asset domain, but analytics is the natural home for "monitoring"

**Implementation:**
```python
# In AnalyticsService
def get_alarm_logs(
    self,
    alarm_type: Optional[AlarmType] = None,  # Filter by type (1-5)
    top_count: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    product_group: Optional[str] = None,
    level: Optional[str] = None
) -> List[AlarmLog]:
    """
    Retrieve triggered alarm and notification logs.
    
    Args:
        top_count: Maximum number of results
        date_from: Start date filter
        date_to: End date filter
        product_group: Filter by product group
        level: Filter by alarm level
        
    Returns:
        List of AlarmLog entries
    """
```

**Pros:**
- Logical grouping with yield/quality analytics
- Minimal new code/structure
- Consistent with pyWATS architecture

**Cons:**
- Analytics is already a large module

### Option 2: Standalone Utility on pyWATS Root

**Implementation:**
```python
# On pyWATS class directly
api.get_alarm_logs(top_count=10)
```

**Pros:**
- Simple, discoverable
- Not tied to any domain

**Cons:**
- Inconsistent with domain pattern
- pyWATS class should be thin facade

### Option 3: New Notifications/Alerts Domain

**Pros:**
- Clean separation
- Room to grow if more notification features added

**Cons:**
- Overkill for single read-only method
- Creates nearly empty module

---

## CFX/Events Integration

### Should This Be Part of CFX?

**No - Keep Separate.** Here's why:

1. **Different Data Flow:**
   - CFX = external events coming INTO WATS (test results, material, etc.)
   - Alarms = WATS-generated alerts going OUT to users

2. **Different Protocols:**
   - CFX uses AMQP with specific message schemas
   - WATS alarms use email and internal notification system

3. **Polling vs Push:**
   - Current API is poll-based (query alarm logs)
   - Webhooks would be a server-side feature (not pyWATS)

### Webhook Recommendation

For webhook/push notifications, this requires **server-side changes in WATS**, not pyWATS:

1. **WATS Server Enhancement:** Add webhook registration and callback on alarm trigger
2. **pyWATS Could Add:** A webhook receiver/handler if WATS adds webhook support

**Current pyWATS Scope:** Poll-based `get_alarm_logs()` only

---

## Proposed Implementation Plan

### Phase 1: Basic Read Access (Recommended Now)

1. Add `AlarmLog` model to analytics domain
2. Add `get_alarm_logs()` method to `AnalyticsService`
3. Add async version to `AsyncAnalyticsService`
4. Add tests and documentation

**Estimated Effort:** 2-3 hours

### Phase 2: Future (If WATS Adds Webhooks)

1. Add webhook handler to pywats_events package
2. Create `AlarmReceivedEvent` event type
3. Allow subscription to alarm events

---

## Decision Needed

**Recommended:** Option 1 - Add to Analytics Domain

```python
# Usage
from pywats import pyWATS

api = pyWATS(base_url="...", token="...")

# Get recent alarms (all types)
alarms = api.analytics.get_alarm_logs(top_count=50)

# Filter by type
yield_alarms = api.analytics.get_alarm_logs(
    alarm_type=AlarmType.YIELD_VOLUME,
    top_count=20
)

asset_alarms = api.analytics.get_alarm_logs(
    alarm_type=AlarmType.ASSET,
    date_from=datetime.now() - timedelta(days=7)
)

for alarm in alarms:
    if alarm.alarm_type == AlarmType.YIELD_VOLUME:
        print(f"Yield alert: {alarm.name} - FPY: {alarm.fpy:.1%}")
    elif alarm.alarm_type == AlarmType.REPORT:
        print(f"Unit alert: {alarm.serial_number} - {alarm.name}")
    elif alarm.alarm_type == AlarmType.ASSET:
        print(f"Asset alert: {alarm.asset_name} - {alarm.name}")
```

### Proposed AlarmType Enum

```python
from enum import IntEnum

class AlarmType(IntEnum):
    """WATS alarm types."""
    REPORT = 1           # Reports (UUT) - unit-based alarms
    YIELD_VOLUME = 2     # Yield & volume - yield statistics alarms
    SERIAL_NUMBER = 3    # Serial number handler - SN pool alarms
    MEASUREMENT = 4      # Measurements - SPC/measurement statistics
    ASSET = 5            # Assets - asset status/maintenance alarms
```

---

## Original Requirements Reference

> In WATS you can define alarms that trigger an email sent to a user or user role. I have gotten some requests from customers that want to be able to get these also from the api, or even better, by being able to hook on to an event & webhooks to receive the alarms when triggered.
>
> Please dont use the trigger/naming in the api's service layer, as this term is not used in WATS. Use alarms, or explore the endpoints to see what other triggers exists before choosing a final name. Im not really sure this should be a module, as we only want read-functionality to get alarms - not to be able to make them or alter them.

## Backend Endpoints Reference

```
put /api/internal/Trigger/CloneTrigger/{id}
delete /api/internal/Trigger/DeleteTrigger/{id}
get /api/internal/Trigger/GetAlarmAndNotificationLogs (deprecated)
post /api/internal/Trigger/GetAlarmAndNotificationLogs  ← PRIMARY ENDPOINT
get /api/internal/Trigger/GetTriggerActions
get /api/internal/Trigger/GetTriggerActionsByTrigger
get /api/internal/Trigger/GetTriggerFieldsByTrigger
get /api/internal/Trigger/GetTriggerFieldTypes
get /api/internal/Trigger/GetTriggerOperators
get /api/internal/Trigger/GetTriggers
post /api/internal/Trigger/PostTrigger
put /api/internal/Trigger/PutTrigger
put /api/internal/Trigger/PutTriggerActionsByTrigger
put /api/internal/Trigger/PutTriggerAllAtOnce
put /api/internal/Trigger/PutTriggerFieldsByTrigger
```
