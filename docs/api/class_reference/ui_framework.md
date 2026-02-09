# pywats_ui.framework - Class Reference

Auto-generated class reference for `pywats_ui.framework`.

---

## `framework`

### `BaseApplication(QApplication)`

_Base class for all pyWATS GUI applications._

---

### `BaseMainWindow(QMainWindow)`

_Base class for main application windows._

---

## `framework.async_api_runner`

### `AsyncAPIRunner`

_Helper for running API calls from GUI pages using composition._

**Properties:**
- `has_api`
- `has_async_api`

**Methods:**
- `get_async_api_sync() -> Optional[...]`
- `get_sync_api() -> Optional[...]`
- `register_page(page: Any) -> Any`
- `require_api(page: Any, action: str) -> bool`
- `run(page: Any, api_call: Union[...], on_success: Optional[...], on_error: Optional[...], task_name: str, show_loading: bool) -> Optional[...]`
- `run_parallel(page: Any) -> Any`
- `run_sequence(page: Any) -> Any`

---

## `framework.base_page`

### `BasePage(QWidget, ErrorHandlingMixin)`

_Base class for configuration pages._

**Class Variables:**
- `config_changed`
- `loading_changed`

**Properties:**
- `async_runner`
- `is_loading`
- `page_title`

**Methods:**
- `cancel_all_tasks() -> int`
- `cancel_task(task_id: str) -> bool`
- `closeEvent(event) -> Any`
- `deleteLater() -> Any`
- `load_config() -> Any`
- `run_async(coro: Awaitable[...], name: str, on_complete: Optional[...], on_error: Optional[...], show_loading: bool) -> str`
- `save_config() -> Any`
- `set_loading(is_loading: bool, message: str) -> Any`
- `subscribe_event(event: AppEvent, callback: Callable[...]) -> Any`
- `unsubscribe_all_events() -> Any`
- `unsubscribe_event(event: AppEvent, callback: Callable[...]) -> Any`

---

## `framework.error_mixin`

### `ErrorHandlingMixin`

_Mixin providing centralized error handling for GUI pages._

**Methods:**
- `confirm_action(message: str, title: str) -> bool`
- `handle_error(error: Exception, context: str, on_auth_error: Optional[...]) -> Any`
- `show_error(message: str, title: str) -> Any`
- `show_success(message: str, title: str) -> Any`
- `show_warning(message: str, title: str) -> Any`

---

## `framework.reliability.connection_monitor`

### `ConnectionMonitor(QObject)`

_Monitors connection and handles auto-reconnect with exponential backoff._

**Class Variables:**
- `status_changed`
- `connected`
- `disconnected`
- `reconnecting`
- `reconnect_failed`

**Properties:**
- `current_retry_delay_seconds`
- `is_connected`
- `reconnect_attempt`
- `status`

**Methods:**
- `cleanup() -> Any`
- `manual_connect() -> Any`
- `stop_reconnecting() -> Any`

---

### `ConnectionStatus(Enum)`

_Connection status states_

**Class Variables:**
- `DISCONNECTED`
- `CONNECTING`
- `CONNECTED`
- `RECONNECTING`

---

## `framework.reliability.offline_capability`

### `OfflineCapability`

_Mixin to add offline capability to pages._

**Class Variables:**
- `online_mode_changed`

**Properties:**
- `has_unsaved_changes`
- `is_online`
- `online_mode`

**Methods:**
- `enable_server_features(enabled: bool) -> Any`
- `save_config_offline() -> Any`
- `set_online_mode(connection_status) -> Any`

---

### `OnlineMode(Enum)`

_Online mode states_

**Class Variables:**
- `ONLINE`
- `OFFLINE`
- `SYNCING`

---

## `framework.reliability.queue_manager`

### `QueueManager(QObject)`

_Manages local queue of operations with auto-retry._

**Class Variables:**
- `queue_changed`
- `operation_queued`
- `operation_sent`
- `operation_failed`
- `send_started`

**Methods:**
- `cleanup() -> Any`
- `delete_failed(operation_id: str) -> bool`
- `enqueue(operation_type: str, data: Dict[...]) -> str`
- `get_failed_count() -> int`
- `get_failed_operations() -> List[...]`
- `get_pending_count() -> int`
- `get_pending_operations() -> List[...]`
- `retry_failed(operation_id: str) -> bool`

---

### `QueueStatus(Enum)`

_Status of a queued operation_

**Class Variables:**
- `PENDING`
- `SENDING`
- `SENT`
- `FAILED`

---

### `QueuedOperation`

_Represents a queued operation_

**Class Variables:**
- `id: str`
- `operation_type: str`
- `data: Dict[...]`
- `created: str`
- `attempts: int`
- `last_attempt: Optional[...]`
- `error: Optional[...]`
- `status: QueueStatus`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `to_dict() -> Dict[...]`

---

## `framework.system_tray`

### `SystemTrayIcon(QSystemTrayIcon)`

_System tray icon with menu for pyWATS applications._

**Methods:**
- `add_application(name: str, callback: Callable, icon: Optional[...])`
- `add_quit_action(callback: Optional[...])`
- `add_separator()`

---
