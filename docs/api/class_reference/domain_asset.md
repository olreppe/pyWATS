# pywats.domains.asset - Class Reference

Auto-generated class reference for `pywats.domains.asset`.

---

## `asset.async_repository`

### `AsyncAssetRepository`

_Async Asset data access layer._

---

## `asset.async_service`

### `AsyncAssetService`

_Async Asset business logic._

**Methods:**
- `is_in_alarm(asset: Asset) -> bool`
- `is_in_warning(asset: Asset) -> bool`

---

## `asset.enums`

### `AssetAlarmState(IntEnum)`

_Asset alarm state as returned by the Status endpoint._

**Class Variables:**
- `OK`
- `WARNING`
- `ALARM`

---

### `AssetLogType(IntEnum)`

_Asset log entry type._

**Class Variables:**
- `MESSAGE`
- `REGISTER`
- `UPDATE`
- `RESET_COUNT`
- `CALIBRATION`
- `MAINTENANCE`
- `STATE_CHANGE`
- `UNKNOWN`
- `CREATED`
- `COUNT_RESET`
- `COMMENT`

---

### `AssetState(IntEnum)`

_Asset state enumeration._

**Class Variables:**
- `UNKNOWN`
- `IN_OPERATION`
- `IN_TRANSIT`
- `IN_MAINTENANCE`
- `IN_CALIBRATION`
- `IN_STORAGE`
- `SCRAPPED`
- `OK`

---

### `IntervalMode(IntEnum)`

_Interval mode for calibration and maintenance intervals._

**Class Variables:**
- `NORMAL`
- `UNLIMITED`
- `EXTERNAL`

---

## `asset.models`

### `Asset(PyWATSModel)`

_Represents an asset in WATS._

**Class Variables:**
- `serial_number: str`
- `type_id: Optional[...]`
- `asset_id: Optional[...]`
- `parent_asset_id: Optional[...]`
- `parent_serial_number: Optional[...]`
- `asset_name: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `client_id: Optional[...]`
- `state: AssetState`
- `description: Optional[...]`
- `location: Optional[...]`
- `first_seen_date: Optional[...]`
- `last_seen_date: Optional[...]`
- `last_maintenance_date: Optional[...]`
- `next_maintenance_date: Optional[...]`
- `last_calibration_date: Optional[...]`
- `next_calibration_date: Optional[...]`
- `total_count: Optional[...]`
- `running_count: Optional[...]`
- `tags: List[...]`
- `asset_children: List[...]`
- `asset_type: Optional[...]`
- `asset_log: List[...]`

---

### `AssetLog(PyWATSModel)`

_Represents an asset log entry._

**Class Variables:**
- `log_id: Optional[...]`
- `asset_id: Optional[...]`
- `serial_number: Optional[...]`
- `date: Optional[...]`
- `user: Optional[...]`
- `log_type: Optional[...]`
- `comment: Optional[...]`

---

### `AssetType(PyWATSModel)`

_Represents an asset type in WATS._

**Class Variables:**
- `type_name: str`
- `type_id: Optional[...]`
- `running_count_limit: Optional[...]`
- `total_count_limit: Optional[...]`
- `maintenance_interval: Optional[...]`
- `calibration_interval: Optional[...]`
- `warning_threshold: Optional[...]`
- `alarm_threshold: Optional[...]`
- `is_readonly: bool`
- `icon: Optional[...]`

---
