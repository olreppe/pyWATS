# pywats_client.core - Class Reference

Auto-generated class reference for `pywats_client.core`.

---

## `core.async_runner`

### `AsyncContextMixin`

_Mixin class providing async execution helpers for GUI widgets._

**Class Variables:**
- `_runner: AsyncTaskRunner`

**Properties:**
- `has_running_tasks`

**Methods:**
- `cancel_all_tasks() -> int`
- `cancel_task(task_id: str) -> bool`
- `run_async(coro: Awaitable[...], name: str, on_complete: Optional[...], on_error: Optional[...]) -> str`

---

### `AsyncTaskRunner(QObject)`

_Executes async coroutines in a background thread and signals results to Qt._

**Class Variables:**
- `task_started`
- `task_completed`
- `task_error`
- `task_progress`
- `task_cancelled`
- `task_finished`

**Methods:**
- `cancel(task_id: str) -> bool`
- `cancel_all() -> int`
- `cleanup() -> Any`
- `deleteLater() -> Any`
- `get_running_count() -> int`
- `has_running_tasks() -> bool`
- `is_running(task_id: str) -> bool`
- `run(coro: Awaitable[...], name: str, on_complete: Optional[...], on_error: Optional[...], on_progress: Optional[...]) -> str`

---

### `TaskInfo`

_Information about a running task_

**Class Variables:**
- `task_id: str`
- `name: str`
- `state: TaskState`
- `future: Optional[...]`
- `progress: int`
- `progress_message: str`

---

### `TaskResult(Unknown)`

_Result container for async task execution._

**Class Variables:**
- `task_id: str`
- `name: str`
- `state: TaskState`
- `result: Optional[...]`
- `error: Optional[...]`
- `traceback: Optional[...]`

**Properties:**
- `is_error`
- `is_success`

---

### `TaskState(Enum)`

_Task execution states_

**Class Variables:**
- `PENDING`
- `RUNNING`
- `COMPLETED`
- `FAILED`
- `CANCELLED`

---

## `core.auth`

### `AuthResult`

_Result of authentication attempt_

**Class Variables:**
- `success: bool`
- `token: Optional[...]`
- `error: Optional[...]`
- `base_url: Optional[...]`

---

## `core.config`

### `ClientConfig`

_Main configuration for pyWATS Client instance._

**Class Variables:**
- `CURRENT_SCHEMA_VERSION: str`
- `MIN_SCHEMA_VERSION: str`
- `schema_version: str`
- `instance_id: str`
- `instance_name: str`
- `service_address: str`
- `api_token: str`
- `username: str`
- `station_name: str`
- `location: str`
- `purpose: str`
- `station_description: str`
- `auto_detect_location: bool`
- `include_station_in_reports: bool`
- `station_name_source: str`
- `multi_station_enabled: bool`
- `station_presets: List[...]`
- `active_station_key: str`
- `sn_mode: str`
- `sn_prefix: str`
- `sn_start: int`
- `sn_padding: int`
- `sn_com_port: str`
- `sn_terminator: str`
- `sn_validate_format: bool`
- `sn_pattern: str`
- `sn_check_duplicates: bool`
- `proxy_mode: str`
- `proxy_host: str`
- `proxy_port: int`
- `proxy_auth: bool`
- `proxy_username: str`
- `proxy_password: str`
- `proxy_bypass: str`
- `proxy: ProxyConfig`
- `sync_interval_seconds: int`
- `process_sync_enabled: bool`
- `reports_folder: str`
- `offline_queue_enabled: bool`
- `max_retry_attempts: int`
- `retry_interval_seconds: int`
- `max_queue_size: int`
- `max_concurrent_uploads: int`
- `enable_cache: bool`
- `cache_ttl_seconds: float`
- `cache_max_size: int`
- `enable_metrics: bool`
- `metrics_port: int`
- `converters_folder: str`
- `converters: List[...]`
- `converters_enabled: bool`
- `yield_monitor_enabled: bool`
- `yield_threshold: float`
- `location_services_enabled: bool`
- `software_auto_update: bool`
- `api_enabled: bool`
- `api_host: str`
- `api_port: int`
- `api_base_path: str`
- `api_cors_enabled: bool`
- `api_cors_origins: str`
- `api_auth_type: str`
- `api_rate_limit_enabled: bool`
- `api_rate_limit_requests: int`
- `api_rate_limit_window: int`
- `webhook_converter_url: str`
- `webhook_report_url: str`
- `webhook_service_url: str`
- `webhook_auth_header: str`
- `webhook_auth_value: str`
- `show_software_tab: bool`
- `show_sn_handler_tab: bool`
- `show_converters_tab: bool`
- `show_location_tab: bool`
- `show_proxy_tab: bool`
- `auto_connect: bool`
- `was_connected: bool`
- `service_auto_start: bool`
- `log_level: str`
- `log_file: str`
- `start_minimized: bool`
- `minimize_to_tray: bool`
- `_config_path: Optional[...]`
- `_env_applied: bool`

**Properties:**
- `config_path`
- `data_path`
- `formatted_identifier`
- `identifier`

**Methods:**
- `add_station_preset(preset: StationPreset) -> Any`
- `from_dict(cls, data: Dict[...]) -> Any`
- `get(key: str, default: Any) -> Any`
- `get_active_station_preset() -> Optional[...]`
- `get_effective_location() -> str`
- `get_effective_purpose() -> str`
- `get_effective_station_name() -> str`
- `get_reports_path() -> Path`
- `get_runtime_credentials() -> tuple[...]`
- `is_valid() -> bool`
- `load(cls, path: Path) -> Any`
- `load_and_repair(cls, path: Path) -> tuple[...]`
- `load_for_instance(cls, instance_id: str) -> Any`
- `load_or_create(cls, path: Path) -> Any`
- `remove_station_preset(key: str) -> bool`
- `repair() -> List[...]`
- `save(path: Optional[...]) -> Any`
- `set(key: str, value: Any) -> Any`
- `set_active_station(key: str) -> bool`
- `to_dict() -> Dict[...]`
- `validate() -> List[...]`

---

### `ConverterConfig`

_Configuration for a single converter instance._

**Class Variables:**
- `name: str`
- `module_path: str`
- `watch_folder: str`
- `done_folder: str`
- `error_folder: str`
- `pending_folder: str`
- `converter_type: Union[...]`
- `enabled: bool`
- `priority: int`
- `arguments: Dict[...]`
- `file_patterns: List[...]`
- `folder_patterns: List[...]`
- `alarm_threshold: float`
- `reject_threshold: float`
- `max_retries: int`
- `retry_delay_seconds: int`
- `schedule_interval_seconds: Optional[...]`
- `cron_expression: Optional[...]`
- `run_on_startup: bool`
- `readiness_marker: str`
- `min_file_count: Optional[...]`
- `post_action: str`
- `archive_folder: str`
- `description: str`
- `author: str`
- `version: str`

**Properties:**
- `is_file_converter`
- `is_folder_converter`
- `is_scheduled_converter`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `get(key: str, default: Any) -> Any`
- `set(key: str, value: Any) -> Any`
- `to_dict() -> Dict[...]`
- `validate() -> List[...]`

---

### `ProxyConfig`

_Proxy configuration_

**Class Variables:**
- `enabled: bool`
- `host: str`
- `port: int`
- `username: str`
- `password: str`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `to_dict() -> Dict[...]`

---

### `StationPreset`

_Configuration for a saved station preset._

**Class Variables:**
- `key: str`
- `name: str`
- `location: str`
- `purpose: str`
- `description: str`
- `is_default: bool`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `to_dict() -> Dict[...]`

---

## `core.config_manager`

### `ConfigManager`

_File-based configuration manager for pyWATS Client._

**Class Variables:**
- `DEFAULT_CONFIG_FILENAME`

**Properties:**
- `instance_id`
- `settings`

**Methods:**
- `exists() -> bool`
- `get_config_directory(instance_id: str) -> Path`
- `load() -> APISettings`
- `reset_to_defaults() -> APISettings`
- `save(settings: Optional[...]) -> Any`

---

## `core.connection_config`

### `ConnectionConfig`

_Connection-specific configuration with persistent state._

**Class Variables:**
- `server_url: str`
- `username: str`
- `token_encrypted: str`
- `token_version: int`
- `connection_state: str`
- `last_connected: Optional[...]`
- `last_disconnected: Optional[...]`
- `health_check_interval: int`
- `health_check_timeout: int`
- `auto_reconnect: bool`
- `max_reconnect_attempts: int`
- `reconnect_delay: int`
- `total_connections: int`
- `total_disconnections: int`
- `total_health_checks: int`
- `failed_health_checks: int`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `get_health_check_success_rate() -> float`
- `get_state() -> ConnectionState`
- `is_authenticated() -> bool`
- `is_connected() -> bool`
- `is_offline() -> bool`
- `mark_connected() -> Any`
- `mark_disconnected() -> Any`
- `mark_offline() -> Any`
- `record_health_check(success: bool) -> Any`
- `set_state(state: ConnectionState) -> Any`
- `to_dict() -> Dict[...]`

---

### `ConnectionState(Enum)`

_Connection state for persistent tracking_

**Class Variables:**
- `NOT_CONNECTED`
- `CONNECTED`
- `OFFLINE`

---

### `InstanceConfig`

_Instance-specific configuration._

**Class Variables:**
- `instance_id: str`
- `instance_name: str`
- `instance_type: str`
- `storage_path: str`
- `connection: ConnectionConfig`
- `created_at: Optional[...]`
- `last_used: Optional[...]`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `mark_used() -> Any`
- `to_dict() -> Dict[...]`

---

## `core.constants`

### `ConverterType(str, Enum)`

_Types of converters supported._

**Class Variables:**
- `FILE`
- `FOLDER`
- `SCHEDULED`

---

### `ErrorHandling(str, Enum)`

_Error handling strategies for converters._

**Class Variables:**
- `MOVE`
- `RETRY`
- `IGNORE`
- `RAISE`

---

### `FolderName(str, Enum)`

_Standard folder names used by the client service._

**Class Variables:**
- `DONE`
- `ERROR`
- `PENDING`
- `PROCESSING`
- `ARCHIVE`

---

### `LogLevel(str, Enum)`

_Log level names for configuration._

**Class Variables:**
- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

---

### `ServiceMode(str, Enum)`

_Operating mode for the client service._

**Class Variables:**
- `SERVICE`
- `GUI`
- `CLI`

---

## `core.event_bus`

### `AppEvent(Enum)`

_Application event types._

**Class Variables:**
- `CONNECTION_CHANGED`
- `CONNECTION_ERROR`
- `APP_STARTING`
- `APP_STARTED`
- `APP_STOPPING`
- `APP_STOPPED`
- `APP_ERROR`
- `APP_STATUS_CHANGED`
- `API_CLIENT_READY`
- `API_CLIENT_DISCONNECTED`
- `ASSETS_CHANGED`
- `PRODUCTS_CHANGED`
- `SOFTWARE_CHANGED`
- `PROCESSES_REFRESHED`
- `QUEUE_ITEM_ADDED`
- `QUEUE_ITEM_PROCESSED`
- `QUEUE_EMPTY`
- `QUEUE_STATUS_CHANGED`
- `CONFIG_CHANGED`
- `CONFIG_SAVED`

---

### `EventBus(QObject)`

_Central event bus for application-wide communication._

**Class Variables:**
- `connection_changed`
- `api_client_ready`
- `app_status_changed`
- `queue_status_changed`
- `event_occurred`
- `_instance: Optional[...]`

**Methods:**
- `clear_subscribers() -> Any`
- `emit_api_disconnected() -> Any`
- `emit_api_ready(client: Any) -> Any`
- `emit_app_status(status: str) -> Any`
- `emit_connection_changed(status: str) -> Any`
- `emit_queue_status(pending: int, failed: int) -> Any`
- `emit_service_error(error: str) -> Any`
- `emit_service_started() -> Any`
- `emit_service_stopped() -> Any`
- `emit_status_changed(old_status: str, new_status: str) -> Any`
- `publish(event: AppEvent) -> Any`
- `subscribe(event: AppEvent, callback: Callable[...]) -> Any`
- `unsubscribe(event: AppEvent, callback: Callable) -> Any`

---

## `core.file_utils`

### `FileOperation(Enum)`

_Types of file operations for logging/tracking._

**Class Variables:**
- `READ`
- `WRITE`
- `DELETE`
- `RENAME`
- `COPY`

---

### `FileOperationResult`

_Result of a file operation._

**Class Variables:**
- `success: bool`
- `path: Path`
- `operation: FileOperation`
- `error: Optional[...]`
- `backup_path: Optional[...]`

---

### `SafeFileReader`

_Provides safe file reading operations with recovery capabilities._

**Methods:**
- `read_bytes_safe(path: Path, default: Optional[...], try_backup: bool) -> Optional[...]`
- `read_json_safe(path: Path, default: Optional[...], try_backup: bool) -> Optional[...]`
- `read_text_safe(path: Path, default: Optional[...], encoding: str, try_backup: bool) -> Optional[...]`

---

### `SafeFileWriter`

_Provides atomic file writing operations._

**Methods:**
- `write_bytes_atomic(path: Path, content: bytes, backup: bool) -> FileOperationResult`
- `write_json_atomic(path: Path, data: Dict[...], indent: int, backup: bool) -> FileOperationResult`
- `write_text_atomic(path: Path, content: str, encoding: str, backup: bool) -> FileOperationResult`

---

## `core.instance_manager`

### `InstanceLock`

_File-based instance lock for multi-instance support._

**Methods:**
- `acquire(instance_name: str, pid: Optional[...]) -> bool`
- `release() -> Any`

---

### `InstanceManager`

_Manages multiple pyWATS Client instances._

**Methods:**
- `cleanup_stale_locks() -> int`
- `get_running_instances() -> List[...]`
- `is_instance_running(instance_id: str) -> bool`

---

## `core.security`

### `RateLimiter`

_Simple token bucket rate limiter._

**Methods:**
- `check_rate_limit(client_id: str) -> bool`
- `cleanup_old_clients(max_age_seconds: int) -> int`
- `reset(client_id: str) -> Any`

---
