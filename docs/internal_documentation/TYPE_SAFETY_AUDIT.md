# Type Safety Audit - pywats_client

**Audit Date:** January 25, 2026  
**Scope:** `src/pywats_client/` (excluding test files)  
**Focus Areas:** GUI, Service, Core, Converters

---

## Summary

This audit identifies type safety issues across the `pywats_client` module. Issues are categorized by severity and location.

### Issue Statistics
| Category | Count |
|----------|-------|
| Missing return type hints | ~75+ |
| Functions returning raw `dict` | ~25+ |
| Functions returning `Dict[str, Any]` | ~20+ |
| Functions returning `Any` | ~15 |
| Qt signals with `object` type | ~10 |
| Parameters typed as `Any` | ~30+ |

---

## 1. Functions with Missing Return Type Hints

### 1.1 GUI Module (`src/pywats_client/gui/`)

#### main_window.py
| Line | Function | Issue |
|------|----------|-------|
| ~110 | `_setup_window(self)` | Missing `-> None` |
| ~122 | `_setup_ui(self)` | Missing `-> None` |
| ~145 | `_create_sidebar(self, layout)` | Missing `-> None` |
| ~250 | `_create_content_area(self, layout)` | Missing `-> None` (estimated) |
| ~300 | `_create_menu_bar(self)` | Missing `-> None` (estimated) |
| ~350 | `_create_status_bar(self)` | Missing `-> None` (estimated) |
| ~400 | `_build_nav_items(self)` | Missing return type |
| ~450 | `_update_nav_list(self)` | Missing `-> None` |

#### login_window.py
| Line | Function | Issue |
|------|----------|-------|
| 74 | `_setup_ui(self)` | Missing `-> None` |
| 190 | `_apply_styles(self)` | Missing `-> None` |
| 332 | `_on_auth_finished(self, success, error_message, token)` | Missing `-> None` |

#### settings_dialog.py
| Line | Function | Issue |
|------|----------|-------|
| 38 | `__init__(self, parent)` | OK - has hints |
| 47 | `setup_ui(self)` | Missing `-> None` |

#### widgets/script_editor.py
| Line | Function | Issue |
|------|----------|-------|
| 102 | `__init__(self, document)` | Missing `-> None` |
| 215 | `__init__(self, source_code)` | Missing `-> None` |
| 474 | `__init__(self, parent)` | Missing `-> None` |
| 1001 | `helper_function(arg1, arg2)` | Missing return type and parameter types |

#### widgets/instance_selector.py
| Line | Function | Issue |
|------|----------|-------|
| 36 | `__init__(self, parent)` | Missing `-> None` |

### 1.2 GUI Pages (`src/pywats_client/gui/pages/`)

#### base.py
| Line | Function | Issue |
|------|----------|-------|
| 62 | `_on_refresh(self)` | Missing `-> None` (docstring example) |
| 183 | `_on_refresh(self)` | Missing `-> None` (docstring example) |
| 190 | `async _fetch_assets(self)` | Missing return type (docstring example) |

#### asset.py
| Line | Function | Issue |
|------|----------|-------|
| 51 | `_setup_ui(self)` | Missing `-> None` |
| 182 | `_get_api_client(self)` | Missing return type - should return `Optional[pyWATS]` |
| 350+ | `_on_refresh(self)` | Missing `-> None` |
| 356 | `_load_assets(self)` | Missing `-> None` |
| 362 | `_load_assets_async(self)` | Missing `-> None` |

#### product.py
| Line | Function | Issue |
|------|----------|-------|
| 51 | `_setup_ui(self)` | Missing `-> None` |
| 217 | `_get_api_client(self)` | Missing return type |

#### rootcause.py
| Line | Function | Issue |
|------|----------|-------|
| 51 | `_setup_ui(self)` | Missing `-> None` |
| 177 | `_get_api_client(self)` | Missing return type |

#### production.py
| Line | Function | Issue |
|------|----------|-------|
| 35 | `__init__(self, parent)` | Missing `-> None` |
| 188 | `_get_api_client(self)` | Missing return type |

#### setup.py
| Line | Function | Issue |
|------|----------|-------|
| 36 | `__init__(self, config, parent)` | Missing `-> None` |
| Many | Multiple `_on_*` event handlers | Missing `-> None` |

#### dashboard.py
| Line | Function | Issue |
|------|----------|-------|
| 34 | `__init__(self, parent)` | Missing `-> None` |

#### log.py
| Line | Function | Issue |
|------|----------|-------|
| 50 | `__init__(self, config, parent)` | Missing `-> None` |

#### about.py
| Line | Function | Issue |
|------|----------|-------|
| 23 | `__init__(self, config, parent)` | Missing `-> None` |

#### general.py
| Line | Function | Issue |
|------|----------|-------|
| 19 | `__init__(self, config, parent)` | Missing `-> None` |

#### proxy_settings.py
| Line | Function | Issue |
|------|----------|-------|
| 21 | `__init__(self, config, parent)` | Missing `-> None` |

#### converters.py
| Line | Function | Issue |
|------|----------|-------|
| 58 | `__post_init__(self)` | Missing `-> None` |

### 1.3 Service Module (`src/pywats_client/service/`)

#### client_service.py
| Line | Function | Issue |
|------|----------|-------|
| 54 | `__init__(self, instance_id)` | Missing `-> None` |
| 271 | `watchdog_check()` | Nested function - missing return type |
| 291 | `ping_check()` | Nested function - missing return type |
| 311 | `register_check()` | Nested function - missing return type |
| 406 | `__init__(self, callback)` | Inner class - missing return type |
| 410 | `on_modified(self, event)` | Inner class - missing return type |
| 483 | `_signal_handler(self, signum, frame)` | Missing `-> None` |
| 515 | `main(instance_id)` | Missing return type |

#### converter_pool.py
| Line | Function | Issue |
|------|----------|-------|
| 46 | `__post_init__(self)` | Missing `-> None` |
| 61 | `__init__(self, pool, worker_id)` | Missing `-> None` |
| 69 | `run(self)` | Missing `-> None` |
| 202 | `start(self)` | Missing `-> None` |
| 231 | `stop(self)` | Missing `-> None` |
| 241 | `_attach_watcher(self)` | Missing `-> None` |
| 272 | `_on_file_changed(self, file_path)` | Missing `-> None` |
| 281 | `_check_folder_single_thread(self)` | Missing `-> None` |
| 296 | `_check_folder(self)` | Missing `-> None` |
| 315 | `convert_file(self, item, api_client)` | Missing `-> None` |
| 340 | `_post_process_file(self, file_path, success, error)` | Missing `-> None` |
| 382 | `process_archive_queue(self)` | Missing `-> None` |
| 420 | `__init__(self, config, api_client)` | Missing `-> None` |
| 455 | `initialize_converters(self)` | Missing `-> None` |
| 543 | `_start_all_converters(self)` | Missing `-> None` |
| 622 | `remove_file(self, file_path)` | Missing `-> None` |
| 628 | `_check_worker_status(self)` | Missing `-> None` |
| 661 | `worker_shutdown(self, worker)` | Missing `-> None` |
| 684 | `check_state(self)` | Missing `-> None` |
| 715 | `dispose(self)` | Missing `-> None` |
| 744 | `create_api_client(self)` | Missing return type |

#### pending_watcher.py
| Line | Function | Issue |
|------|----------|-------|
| 97 | `_start(self)` | Missing `-> None` |
| 128 | `_setup_file_watcher(self)` | Missing `-> None` |
| 138-149 | Inner class methods | Missing `-> None` |
| 165 | `_setup_timer(self)` | Missing `-> None` |
| 189 | `_on_file_changed(self)` | Missing `-> None` |
| 197 | `_on_timer_elapsed(self)` | Missing `-> None` |
| 208 | `_start_pending_transfer(self)` | Missing `-> None` |
| 258 | `_check_transferring_timeout(self)` | Missing `-> None` |
| 307 | `_submit_pending_reports(self)` | Missing `-> None` |
| 325 | `_submit_report(self, file_path)` | Missing `-> None` |
| 377 | `trigger_submission(self)` | Missing `-> None` |
| 385 | `check_state(self)` | Missing `-> None` |
| 403 | `dispose(self)` | Missing `-> None` |

#### ipc_server.py
| Line | Function | Issue |
|------|----------|-------|
| 26 | `__init__(self, instance_id, service)` | Missing `-> None` |
| 81 | `stop(self)` | Missing `-> None` |
| 91 | `_on_connection(self)` | Missing `-> None` |
| 107 | `_handle_request(self, client)` | Missing `-> None` |
| 154 | `_send_error(self, client, message)` | Missing `-> None` |
| 163 | `_on_disconnect(self, client)` | Missing `-> None` |

#### ipc_client.py
| Line | Function | Issue |
|------|----------|-------|
| 43 | `__init__(self, instance_id)` | Missing `-> None` |
| 88 | `disconnect(self)` | Missing `-> None` |

#### service_tray.py
| Line | Function | Issue |
|------|----------|-------|
| 35 | `__init__(self, instance_id, parent)` | Missing `-> None` |
| 326 | `main(instance_id)` | Missing return type |

### 1.4 Core Module (`src/pywats_client/core/`)

#### async_runner.py
| Line | Function | Issue |
|------|----------|-------|
| 24 | `async fetch_data()` | Docstring example - missing return type |
| 32 | `async load_assets(self)` | Docstring example - missing return type |
| 122+ | Multiple docstring examples | Missing return types |

#### event_bus.py
| Line | Function | Issue |
|------|----------|-------|
| 116 | `__init__(self)` | Missing `-> None` |
| 189 | `on_connection(data)` | Docstring example - missing return type |

#### instance_manager.py
| Line | Function | Issue |
|------|----------|-------|
| 28 | `__init__(self, instance_id, base_path)` | Missing `-> None` |
| 120 | `__enter__(self)` | Missing return type |
| 125 | `__exit__(self, exc_type, exc_val, exc_tb)` | Missing return type |
| 140 | `__init__(self, base_path)` | Missing `-> None` |

#### config.py
| Line | Function | Issue |
|------|----------|-------|
| 328 | `__post_init__(self)` | Missing `-> None` |

#### config_manager.py
| Line | Function | Issue |
|------|----------|-------|
| 45 | `__init__(self, config_path, instance_id)` | Missing `-> None` |

#### connection_config.py
| Line | Function | Issue |
|------|----------|-------|
| 145 | `__post_init__(self)` | Missing `-> None` |

### 1.5 Control Module (`src/pywats_client/control/`)

#### cli.py
| Line | Function | Issue |
|------|----------|-------|
| 43 | `__init__(self, config_path)` | Missing `-> None` |
| 56 | `config(self)` | Property - missing return type |

#### service_adapter.py
| Line | Function | Issue |
|------|----------|-------|
| 131 | `__init__(self)` | Missing `-> None` |
| 362 | `__init__(self, user_agent)` | Missing `-> None` |

#### windows_native_service.py
| Line | Function | Issue |
|------|----------|-------|
| 84 | `__init__(self, args)` | Missing `-> None` |
| 103 | `SvcStop(self)` | Missing `-> None` |
| 123 | `SvcDoRun(self)` | Missing `-> None` |
| 144 | `_main(self)` | Missing `-> None` |

#### unix_service.py
| Line | Function | Issue |
|------|----------|-------|
| 255, 341, 573, 644 | `_print(msg)` | Nested functions - missing `-> None` |

### 1.6 Converters Module (`src/pywats_client/converters/`)

#### base.py
| Line | Function | Issue |
|------|----------|-------|
| 47 | `__init__(self, file_path)` | Missing `-> None` |
| 191 | `__init__(self, station_name)` | Docstring example - missing return type |
| 447 | `on_success(...)` | Docstring example - missing return type |
| 473 | `on_failure(...)` | Docstring example - missing return type |

#### context.py
| Line | Function | Issue |
|------|----------|-------|
| 28 | `convert(self, source, context)` | Docstring example - missing return type |

---

## 2. Functions Returning Raw `dict` or `Dict[...]`

### 2.1 Functions returning `-> dict` (untyped)

| File | Line | Function | Current Signature |
|------|------|----------|-------------------|
| service/client_service.py | 498 | `get_status_dict` | `-> dict` |
| gui/main_window.py | 845 | `send_test_uut` | `async ... -> dict` |
| converters/example_csv.py | 247 | `_row_to_step` | `(row: dict) -> dict` |

**Recommendation:** Use `-> Dict[str, Any]` or better, create TypedDict/dataclass models.

### 2.2 Functions returning `-> Dict[str, Any]`

| File | Line | Function | Issue |
|------|------|----------|-------|
| core/config.py | 84 | `ConverterConfig.to_dict` | Should return typed model |
| core/config.py | 158 | `StationPreset.to_dict` | Should return typed model |
| core/config.py | 180 | `ProxyConfig.to_dict` | Should return typed model |
| core/config.py | 541 | `ClientConfig.to_dict` | Should return typed model |
| control/cli.py | 197 | `show_status` | Should return typed status model |
| converters/base.py | 528 | `get_arguments` | Should return `Dict[str, ArgumentDefinition]` |
| converters/base.py | 549 | `get_arguments` | Docstring example |
| converters/base.py | 580 | `get_parameters` | Deprecated - same issue |
| converters/base.py | 781 | `get_arguments` | Should return typed dict |
| service/ipc_client.py | 27 | `InstanceInfo.to_dict` | Should return typed model |
| converters/context.py | 326 | `ConverterContext.to_dict` | Should return typed model |
| core/connection_config.py | 112 | `ConnectionConfig.to_dict` | Should return typed model |
| core/connection_config.py | 157 | `LegacyConnectionConfig.to_dict` | Should return typed model |
| core/connection_config.py | 175 | `migrate_legacy_config` | Input/output both `Dict[str, Any]` |
| gui/pages/asset.py | 147 | `AssetDialog.get_asset_data` | Should return typed asset model |
| gui/pages/asset.py | 377 | `_fetch_assets` | Should return typed response model |
| converters/example_csv.py | 63 | `arguments_schema` | OK - returns typed dict |
| converters/file_converter.py | 56, 173, 187 | `arguments_schema` | OK - returns typed dict |

---

## 3. Functions Returning `Any`

### 3.1 Explicit `-> Any` Returns

| File | Line | Function | Issue |
|------|------|----------|-------|
| gui/pages/asset.py | 511 | `_create_asset` | `async ... -> Any` - should return Asset model |
| gui/pages/asset.py | 558 | `_update_asset` | `async ... -> Any` - should return Asset model |
| gui/pages/product.py | 879 | `_create_product` | `async ... -> Any` - should return Product model |
| gui/pages/product.py | 933 | `_update_product` | `async ... -> Any` - should return Product model |
| gui/pages/product.py | 988 | `_create_revision` | `async ... -> Any` - should return Revision model |
| gui/pages/rootcause.py | 539 | `_create_ticket` | `async ... -> Any` - should return Ticket model |
| gui/pages/rootcause.py | 598 | `_update_ticket_comment` | `async ... -> Any` |
| gui/pages/rootcause.py | 649 | `_add_ticket_comment` | `async ... -> Any` |
| gui/pages/rootcause.py | 721 | `_change_ticket_status` | `async ... -> Any` |
| converters/context.py | 147 | `get_argument` | `(name: str, default: Any = None) -> Any` |
| control/cli.py | 109 | `get_value` | `(key: str) -> Any` |

### 3.2 Parameters/Attributes Typed as `Any`

| File | Line | Context | Issue |
|------|------|---------|-------|
| converters/context.py | 50 | `api_client: Optional[Any]` | Should be `Optional[pyWATS]` |
| converters/context.py | 296 | `api_client: Optional[Any]` | Should be `Optional[pyWATS]` |
| converters/base.py | 168 | `api_client: Any` | Should be `pyWATS` |
| converters/base.py | 253 | `self._api_client: Optional[Any]` | Should be `Optional[pyWATS]` |
| service/client_service.py | 82 | `self._ipc_server: Optional[any]` | Should be `Optional[IPCServer]` |
| service/client_service.py | 92 | `self._config_watcher: Optional[any]` | Should be typed |
| core/event_bus.py | 255 | `emit_api_ready(self, client: Any)` | Should be `client: pyWATS` |
| queue/persistent_queue.py | 130 | `data: Any` | Should be more specific |
| gui/settings_dialog.py | 47-51 | `load_settings/save_settings(config: Any)` | Should be typed config |

---

## 4. Qt Signal/Slot Type Safety Issues

### 4.1 Signals Using `object` Type

| File | Line | Signal | Issue |
|------|------|--------|-------|
| core/async_runner.py | 143 | `task_completed = Signal(object)` | Should use typed TaskResult |
| core/async_runner.py | 144 | `task_error = Signal(object)` | Should use typed TaskResult |
| core/async_runner.py | 149 | `task_finished = Signal(object)` | Should use typed TaskResult |
| core/event_bus.py | 93 | `api_client_ready = Signal(object)` | Should be `Signal(pyWATS)` but Qt limitation |
| core/event_bus.py | 102 | `event_occurred = Signal(object, dict)` | First arg should be `AppEvent` |

**Note:** Qt signals have limitations with custom types. Using `object` is sometimes necessary but loses type checking.

### 4.2 Slots Without Proper Type Annotations

Many `@Slot()` decorated methods don't have corresponding Python type hints:

| File | Line | Slot | Issue |
|------|------|------|-------|
| gui/login_window.py | 260 | `@Slot()` decorated method | Missing Python return type hint |
| gui/login_window.py | 274 | `@Slot(int)` | Has Qt type but not Python hint |
| gui/login_window.py | 282 | `@Slot()` | Missing Python return type hint |
| gui/pages/setup.py | 193-666 | Multiple `@Slot` methods | Missing Python type hints |
| gui/main_window.py | 578-688 | Multiple `@Slot` methods | Missing Python type hints |

---

## 5. Converter-to-Dict Methods (Pattern Issue)

Multiple pages have `_*_to_dict(self, item: Any) -> Dict[str, Any]` methods that convert API response models to dictionaries:

| File | Line | Method | Input Type |
|------|------|--------|------------|
| gui/pages/asset.py | 421 | `_asset_to_dict` | `asset: Any` |
| gui/pages/product.py | 800 | `_product_to_dict` | `product: Any` |
| gui/pages/rootcause.py | 458 | `_ticket_to_dict` | `ticket: Any` |
| gui/pages/production.py | 358 | `_phase_to_dict` | `phase: Any` |
| gui/pages/production.py | 419 | `_unit_to_dict` | `unit: Any` |

**Recommendation:** These should accept the actual model types from `pywats` and use proper TypedDict or dataclass for the return type.

---

## 6. Priority Recommendations

### High Priority (Breaking Type Safety)

1. **Add return types to all public methods** in:
   - `gui/pages/*.py` 
   - `service/*.py`
   - `core/*.py`

2. **Replace `Any` with specific types** for:
   - `api_client` parameters → `pyWATS`
   - `_*_to_dict` method inputs → specific model types

3. **Create typed models** for:
   - Service status dictionaries
   - Config `to_dict()` returns
   - IPC request/response payloads

### Medium Priority (Improved Type Checking)

4. **Add TypedDict definitions** for:
   - Asset data structures
   - Product data structures
   - Ticket data structures
   - Converter argument schemas

5. **Use Protocol classes** for:
   - Converter interfaces
   - Service status interfaces

### Low Priority (Code Quality)

6. **Add `-> None`** to all `__init__` methods
7. **Add `-> None`** to all `_setup_ui`, `_apply_styles` methods
8. **Document signal types** in docstrings where Qt limitations apply

---

## 7. Example Fixes

### Before
```python
def _get_api_client(self):
    if self._facade and self._facade.has_api:
        return self._facade.api
    return None
```

### After
```python
from typing import Optional
from pywats import pyWATS

def _get_api_client(self) -> Optional[pyWATS]:
    """Get API client via facade."""
    if self._facade and self._facade.has_api:
        return self._facade.api
    return None
```

### Before
```python
async def _create_asset(self, data: Dict[str, Any]) -> Any:
    client = self._get_api_client()
    return client.asset.create_asset(...)
```

### After
```python
from pywats.models import Asset

async def _create_asset(self, data: AssetCreateRequest) -> Asset:
    """Create asset asynchronously."""
    client = self._get_api_client()
    if not client:
        raise RuntimeError("Not connected to WATS server")
    return client.asset.create_asset(...)
```

---

## 8. Files Requiring Most Attention

| File | Issues | Priority |
|------|--------|----------|
| gui/pages/asset.py | 15+ | High |
| gui/pages/product.py | 15+ | High |
| gui/pages/rootcause.py | 15+ | High |
| service/client_service.py | 20+ | High |
| service/converter_pool.py | 25+ | High |
| service/pending_watcher.py | 20+ | High |
| core/async_runner.py | 10+ | Medium |
| core/event_bus.py | 5+ | Medium |
| gui/settings_dialog.py | 20+ | Medium |
| converters/context.py | 10+ | Medium |
| converters/base.py | 15+ | Medium |

---

*End of Type Safety Audit*
