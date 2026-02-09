# pywats (API Entry Points) - Class Reference

Auto-generated class reference for `pywats (API Entry Points)`.

---

## `pywats.async_wats`

### `AsyncWATS`

_Async pyWATS API class._

**Properties:**
- `analytics`
- `asset`
- `http_client`
- `process`
- `product`
- `production`
- `report`
- `rootcause`
- `scim`
- `settings`
- `software`
- `stations`

---

## `pywats.pywats`

### `SyncProductServiceWrapper(SyncServiceWrapper)`

_Specialized sync wrapper for AsyncProductService._

---

### `SyncServiceWrapper`

_Generic synchronous wrapper for async services._

---

### `pyWATS`

_Main pyWATS API class._

**Properties:**
- `analytics`
- `asset`
- `base_url`
- `error_mode`
- `process`
- `product`
- `production`
- `report`
- `retry_config`
- `rootcause`
- `scim`
- `settings`
- `software`
- `station`
- `stations`
- `timeout`

**Methods:**
- `close() -> Any`
- `get_version() -> Optional[...]`
- `retry_config(value: RetryConfig) -> Any`
- `station(station: Optional[...]) -> Any`
- `test_connection() -> bool`
- `timeout(value: int)`

---
