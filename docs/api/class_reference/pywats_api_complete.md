# pyWATS API - Complete Class Reference

**Complete reference for the pyWATS API library (excluding client, service, and UI layers)**

**Generated:** pyWATS
**Generator:** `scripts/generate_class_reference.py`

---

## 📚 Table of Contents

1. [API Entry Points](#api-entry-points) - pyWATS, AsyncWATS
2. [Core Infrastructure](#core-infrastructure) - HTTP client, caching, exceptions
3. [Shared Models](#shared-models) - Base models and utilities
4. [Domain Services](#domain-services) - All business domains
   - [Analytics](#analytics-domain)
   - [Asset](#asset-domain)
   - [Process](#process-domain)
   - [Product](#product-domain)
   - [Production](#production-domain)
   - [Report](#report-domain)
   - [Root Cause](#rootcause-domain)
   - [SCIM](#scim-domain)
   - [Software](#software-domain)

---

<a name="api-entry-points"></a>

# API Entry Points

_Source: [pywats_root.md](pywats_root.md)_


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


---

<a name="core-infrastructure"></a>

# Core Infrastructure

_Source: [pywats_core.md](pywats_core.md)_


## `core.async_client`

### `AsyncHttpClient`

_Async HTTP client with Basic authentication for WATS API._

**Properties:**
- `cache`
- `cache_enabled`
- `rate_limiter`
- `retry_config`

**Methods:**
- `retry_config(value: RetryConfig) -> Any`

---

## `core.cache`

### `AsyncTTLCache(Unknown)`

_Async-safe TTL cache with async cleanup task._

**Properties:**
- `size`

---

### `CacheEntry(Unknown)`

_Single cache entry with TTL tracking._

**Class Variables:**
- `value: T`
- `cached_at: datetime`
- `ttl_seconds: float`
- `hits: int`

**Properties:**
- `age_seconds`
- `is_expired`

---

### `CacheStats`

_Cache statistics for monitoring and optimization._

**Class Variables:**
- `hits: int`
- `misses: int`
- `evictions: int`
- `refreshes: int`
- `total_size_bytes: int`

**Properties:**
- `hit_rate`

---

### `TTLCache(Unknown)`

_Thread-safe TTL (Time-To-Live) cache with automatic expiration._

**Properties:**
- `size`
- `stats`

**Methods:**
- `cleanup_expired() -> int`
- `clear() -> Any`
- `delete(key: str) -> bool`
- `get(key: str, default: Optional[...]) -> Optional[...]`
- `keys() -> list[...]`
- `set(key: str, value: T, ttl: Optional[...]) -> Any`

---

## `core.circuit_breaker`

### `CircuitBreaker`

_Circuit breaker to prevent cascading failures._

**Properties:**
- `is_closed`
- `is_half_open`
- `is_open`
- `state`

**Methods:**
- `call(func: Callable[...]) -> T`
- `get_metrics() -> dict[...]`
- `reset() -> Any`

---

### `CircuitBreakerConfig`

_Configuration for circuit breaker._

**Class Variables:**
- `failure_threshold: int`
- `success_threshold: int`
- `timeout_seconds: float`
- `excluded_exceptions: tuple`

---

### `CircuitBreakerOpenError(Exception)`

_Raised when circuit breaker is open and request is blocked._

---

### `CircuitState(Enum)`

_Circuit breaker states._

**Class Variables:**
- `CLOSED`
- `OPEN`
- `HALF_OPEN`

---

## `core.client`

### `HttpClient`

_HTTP client with Basic authentication for WATS API._

**Properties:**
- `cache`
- `cache_enabled`
- `client`
- `rate_limiter`
- `retry_config`

**Methods:**
- `capture_traces() -> Iterator[...]`
- `clear_cache() -> Any`
- `close() -> Any`
- `delete(endpoint: str, params: Optional[...]) -> Response`
- `get(endpoint: str, params: Optional[...]) -> Response`
- `invalidate_cache(endpoint_pattern: Optional[...]) -> Any`
- `patch(endpoint: str, data: Any, params: Optional[...]) -> Response`
- `post(endpoint: str, data: Any, params: Optional[...]) -> Response`
- `put(endpoint: str, data: Any, params: Optional[...]) -> Response`
- `retry_config(value: RetryConfig) -> Any`

---

### `Response(BaseModel)`

_HTTP Response wrapper._

**Class Variables:**
- `model_config`
- `status_code: int`
- `data: Any`
- `headers: Dict[...]`
- `raw: bytes`

**Properties:**
- `error_message`
- `is_client_error`
- `is_error`
- `is_not_found`
- `is_server_error`
- `is_success`

---

## `core.coalesce`

### `ChunkedProcessor(Unknown)`

_Process large lists in chunks to avoid overwhelming the server._

---

### `CoalesceConfig`

_Configuration for request coalescing._

**Class Variables:**
- `max_batch_size: int`
- `max_wait_time: float`
- `max_concurrent_batches: int`

---

### `CoalesceItem(Unknown)`

_Single item in a coalesced request._

**Class Variables:**
- `item: T`
- `future: asyncio.Future[...]`
- `timestamp: datetime`

---

### `RequestCoalescer(Unknown)`

_Coalesce multiple individual requests into bulk operations._

**Properties:**
- `stats`

---

## `core.config`

### `APISettings(BaseModel)`

_Main API configuration settings._

**Class Variables:**
- `model_config`
- `timeout_seconds: int`
- `max_retries: int`
- `retry_delay_seconds: int`
- `error_mode: ErrorMode`
- `log_requests: bool`
- `log_responses: bool`
- `verify_ssl: bool`
- `product: ProductDomainSettings`
- `report: ReportDomainSettings`
- `production: ProductionDomainSettings`
- `process: ProcessDomainSettings`
- `software: SoftwareDomainSettings`
- `asset: AssetDomainSettings`
- `rootcause: RootCauseDomainSettings`
- `app: AppDomainSettings`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `to_dict() -> Dict[...]`

---

### `AppDomainSettings(DomainSettings)`

_App/Statistics domain specific settings._

---

### `AssetDomainSettings(DomainSettings)`

_Asset domain specific settings._

---

### `DomainSettings(BaseModel)`

_Settings for a specific API domain._

**Class Variables:**
- `model_config`
- `enabled: bool`
- `cache_enabled: bool`
- `cache_ttl_seconds: int`

**Methods:**
- `from_dict(cls: Type[...], data: Dict[...]) -> T`
- `to_dict() -> Dict[...]`

---

### `ProcessDomainSettings(DomainSettings)`

_Process domain specific settings._

**Class Variables:**
- `refresh_interval_seconds: int`
- `auto_refresh: bool`

---

### `ProductDomainSettings(DomainSettings)`

_Product domain specific settings._

**Class Variables:**
- `auto_create_products: bool`
- `default_revision: str`

---

### `ProductionDomainSettings(DomainSettings)`

_Production domain specific settings._

**Class Variables:**
- `auto_reserve_serials: bool`
- `serial_reserve_count: int`
- `validate_serial_format: bool`

---

### `ReportDomainSettings(DomainSettings)`

_Report domain specific settings._

**Class Variables:**
- `auto_submit: bool`
- `validate_before_submit: bool`
- `include_attachments: bool`
- `max_attachment_size_mb: int`

---

### `RetryConfig(BaseModel)`

_Configuration for retry logic in synchronous wrapper._

**Class Variables:**
- `model_config`
- `max_retries: int`
- `backoff: float`
- `retry_on_errors: tuple`

---

### `RootCauseDomainSettings(DomainSettings)`

_RootCause domain specific settings._

---

### `SoftwareDomainSettings(DomainSettings)`

_Software domain specific settings._

**Class Variables:**
- `auto_download: bool`
- `download_path: str`

---

### `SyncConfig(BaseModel)`

_Configuration for synchronous API wrapper._

**Class Variables:**
- `model_config`
- `timeout: Optional[...]`
- `retry_enabled: bool`
- `retry: RetryConfig`
- `correlation_id_enabled: bool`

---

## `core.event_loop_pool`

### `EventLoopPool`

_Thread-safe event loop pool for sync API wrapper._

**Methods:**
- `get_or_create_loop(cls) -> asyncio.AbstractEventLoop`
- `run_coroutine(cls, coro: Coroutine[...]) -> T`
- `shutdown_all(cls) -> Any`

---

## `core.exceptions`

### `AuthenticationError(WatsApiError)`

_Raised when authentication fails (401/403)._

---

### `AuthorizationError(PyWATSError)`

_Permission denied (maps from HTTP 403)._

---

### `ConflictError(PyWATSError)`

_Resource conflict (maps from HTTP 409)._

---

### `ConnectionError(PyWATSError)`

_Network/connection failure._

---

### `EmptyResponseError(PyWATSError)`

_Received empty response when data was expected._

---

### `ErrorHandler`

_Translates HTTP responses to domain results based on error mode._

**Methods:**
- `handle_response(response: Any, operation: str, allow_empty: bool) -> Any`

---

### `ErrorMode(Enum)`

_Controls how the API handles ambiguous responses._

**Class Variables:**
- `STRICT`
- `LENIENT`

---

### `NotFoundError(PyWATSError)`

_Resource not found (maps from HTTP 404)._

---

### `PyWATSError(Exception)`

_Base exception for all pyWATS errors._

---

### `ServerError(PyWATSError)`

_Server-side error (maps from HTTP 5xx)._

---

### `TimeoutError(PyWATSError)`

_Raised when a request times out._

---

### `ValidationError(PyWATSError)`

_Request validation failed (maps from HTTP 400)._

---

### `WatsApiError(PyWATSError)`

_Base for errors returned by the WATS API (HTTP 4xx/5xx)._

---

## `core.logging`

### `CorrelationFilter(logging.Filter)`

_Logging filter that adds correlation ID to log records._

**Methods:**
- `filter(record)`

---

### `FileRotatingHandler(RotatingFileHandler)`

_File handler with automatic rotation based on size._

---

### `LoggingContext`

_Context manager for scoped logging context._

---

### `StructuredFormatter(logging.Formatter)`

_JSON formatter for structured logging._

**Methods:**
- `format(record: logging.LogRecord) -> str`

---

## `core.metrics`

### `MetricsCollector`

_Central metrics collection for pyWATS._

**Methods:**
- `get_metrics() -> bytes`
- `start_system_monitoring(interval: float)`
- `stop_system_monitoring()`
- `track_converter(converter_name: str) -> Callable`
- `track_queue_processing(queue_name: str, item_type: str, duration: float)`
- `track_request(method: str, endpoint: str) -> Callable`
- `update_queue_depth(queue_name: str, depth: int)`

---

## `core.pagination`

### `PaginationConfig`

_Configuration for pagination behavior._

**Class Variables:**
- `page_size: int`
- `max_items: Optional[...]`
- `start_index: int`

---

### `PaginationState`

_Tracks the current state of pagination._

**Class Variables:**
- `current_index: int`
- `items_retrieved: int`
- `total_items: Optional[...]`
- `pages_retrieved: int`
- `is_complete: bool`

---

### `Paginator(Unknown)`

_Reusable paginator for a specific API endpoint._

**Methods:**
- `all(page_size: int, max_items: Optional[...]) -> List[...]`
- `count() -> Optional[...]`
- `iterate(page_size: int, max_items: Optional[...], on_page: Optional[...]) -> Iterator[...]`

---

## `core.parallel`

### `ParallelConfig`

_Configuration for parallel operations._

**Class Variables:**
- `max_workers: int`
- `fail_fast: bool`
- `timeout: Optional[...]`

---

## `core.performance`

### `Serializer`

_High-performance serialization with multiple format support._

**Class Variables:**
- `FORMATS`

**Methods:**
- `compare_sizes(data: Any) -> dict`
- `dumps(data: Any) -> bytes`
- `loads(data: bytes) -> Any`

---

## `core.retry`

### `RetryConfig`

_Configuration for automatic retry behavior._

**Class Variables:**
- `enabled: bool`
- `max_attempts: int`
- `base_delay: float`
- `max_delay: float`
- `exponential_base: float`
- `jitter: bool`
- `retry_methods: Set[...]`
- `retry_status_codes: Set[...]`
- `retry_on_timeout: bool`
- `retry_on_connection_error: bool`
- `_total_retries: int`
- `_total_retry_time: float`

**Properties:**
- `stats`

**Methods:**
- `calculate_delay(attempt: int) -> float`
- `get_retry_after(response: Any) -> Optional[...]`
- `record_retry(delay: float) -> Any`
- `reset_stats() -> Any`
- `should_retry_method(method: str) -> bool`
- `should_retry_status(status_code: int) -> bool`

---

### `RetryExhaustedError(Exception)`

_Raised when all retry attempts have been exhausted._

---

## `core.retry_handler`

### `RetryContext`

_Context passed to retry callbacks for logging and tracing._

**Class Variables:**
- `method: str`
- `endpoint: str`
- `attempt: int`
- `max_attempts: int`
- `delay: float`
- `error_type: Optional[...]`
- `status_code: Optional[...]`

---

### `RetryHandler`

_Unified retry execution handler for HTTP requests._

**Properties:**
- `config`

**Methods:**
- `execute_sync(request_func: Callable[...], method: str, endpoint: str, handle_response: Callable[...], retry_enabled: Optional[...]) -> Any`

---

## `core.routes`

### `Analytics`

_Analytics domain routes (uses /api/App endpoints)._

**Class Variables:**
- `BASE`
- `YIELD`
- `FPY`
- `STEPS`
- `MEASUREMENTS`
- `PARETO`

**Methods:**
- `test_statistics(part_number: Any) -> str`

---

### `App`

_Application/Server metadata routes._

**Class Variables:**
- `BASE`
- `VERSION`
- `PROCESSES`
- `LEVELS`
- `PRODUCT_GROUPS`
- `DYNAMIC_YIELD`
- `VOLUME_YIELD`
- `HIGH_VOLUME`
- `HIGH_VOLUME_BY_GROUP`
- `WORST_YIELD`
- `WORST_YIELD_BY_GROUP`
- `DYNAMIC_REPAIR`
- `RELATED_REPAIR_HISTORY`
- `TOP_FAILED`
- `TEST_STEP_ANALYSIS`
- `MEASUREMENTS`
- `AGGREGATED_MEASUREMENTS`
- `OEE_ANALYSIS`
- `SERIAL_NUMBER_HISTORY`
- `UUT_REPORT`
- `UUR_REPORT`

---

### `Asset`

_Asset domain routes._

**Class Variables:**
- `BASE`
- `ASSETS`
- `TYPES`
- `STATUS`
- `STATE`
- `COUNT`
- `RESET_RUNNING_COUNT`
- `SET_RUNNING_COUNT`
- `SET_TOTAL_COUNT`
- `CALIBRATION`
- `CALIBRATION_EXTERNAL`
- `MAINTENANCE`
- `MAINTENANCE_EXTERNAL`
- `LOG`
- `MESSAGE`
- `SUB_ASSETS`

**Methods:**
- `asset(identifier: str) -> str`
- `asset_status(serial_number: str) -> str`
- `calibrations(serial_number: str) -> str`
- `maintenance(serial_number: str) -> str`

---

### `Internal`

_⚠️ Internal Production API routes._

**Class Variables:**
- `BASE`
- `MES_BASE`
- `IS_CONNECTED`
- `GET_UNIT`
- `GET_UNIT_INFO`
- `GET_UNIT_HIERARCHY`
- `GET_UNIT_STATE_HISTORY`
- `GET_UNIT_PHASE`
- `GET_UNIT_PROCESS`
- `GET_UNIT_CONTENTS`
- `CREATE_UNIT`
- `ADD_CHILD_UNIT`
- `REMOVE_CHILD_UNIT`
- `REMOVE_ALL_CHILD_UNITS`
- `CHECK_CHILD_UNITS`
- `SERIAL_NUMBERS`
- `SERIAL_NUMBERS_COUNT`
- `SERIAL_NUMBERS_FREE`
- `SERIAL_NUMBERS_RANGES`
- `SERIAL_NUMBERS_STATISTICS`
- `GET_SITES`
- `GET_UNIT_PHASES`

---

### `Internal`

_⚠️ Internal Product API routes._

**Class Variables:**
- `BASE`
- `BOM`
- `BOM_UPLOAD`
- `GET_PRODUCT_INFO`
- `GET_PRODUCT_BY_PN`
- `POST_REVISION_RELATION`
- `PUT_REVISION_RELATION`
- `DELETE_REVISION_RELATION`
- `GET_CATEGORIES`
- `PUT_CATEGORIES`
- `GET_PRODUCT_TAGS`
- `PUT_PRODUCT_TAGS`
- `GET_REVISION_TAGS`
- `PUT_REVISION_TAGS`
- `GET_GROUPS_FOR_PRODUCT`

---

### `Internal`

_⚠️ Internal Asset API routes._

**Class Variables:**
- `BLOB_BASE`
- `DELETE_FILES`

**Methods:**
- `download(asset_id: str, file_name: str) -> str`
- `list_files(asset_id: str) -> str`
- `upload(asset_id: str) -> str`

---

### `Internal`

_⚠️ Internal Software API routes._

**Class Variables:**
- `BASE`
- `IS_CONNECTED`
- `CHECK_FILE`
- `POST_FOLDER`
- `UPDATE_FOLDER`
- `DELETE_FOLDER`
- `DELETE_FOLDER_FILES`
- `GET_HISTORY`
- `GET_DOWNLOAD_HISTORY`
- `GET_REVOKED`
- `GET_AVAILABLE`
- `GET_DETAILS`
- `LOG`

**Methods:**
- `file(file_id: str) -> str`

---

### `Internal`

_⚠️ Internal Analytics API routes._

**Class Variables:**
- `UNIT_FLOW`
- `UNIT_FLOW_LINKS`
- `UNIT_FLOW_NODES`
- `UNIT_FLOW_SN`
- `UNIT_FLOW_SPLIT_BY`
- `UNIT_FLOW_UNIT_ORDER`
- `UNIT_FLOW_UNITS`
- `APP_BASE`
- `MEASUREMENT_LIST`
- `STEP_STATUS_LIST`
- `TOP_FAILED`
- `TRIGGER_BASE`
- `ALARM_LOGS`

---

### `Internal`

_⚠️ Internal Process API routes._

**Class Variables:**
- `BASE`
- `GET_PROCESSES`
- `GET_REPAIR_OPERATIONS`

**Methods:**
- `get_process(process_id: str) -> str`
- `get_repair_operation(operation_id: str) -> str`

---

### `Process`

_Process routes._

**Class Variables:**
- `BASE`
- `PROCESSES`

**Methods:**
- `process(process_id: str) -> str`

---

### `Product`

_Product domain routes._

**Class Variables:**
- `BASE`
- `QUERY`
- `PRODUCTS`
- `REVISION`
- `REVISIONS`
- `GROUPS`
- `GROUP`
- `BOM`
- `VENDORS`

**Methods:**
- `bom(part_number: str, revision: str) -> str`
- `product(part_number: str) -> str`
- `revision(part_number: str, revision: str) -> str`
- `revisions(part_number: str) -> str`
- `vendor(vendor_id: str) -> str`

---

### `Production`

_Production domain routes._

**Class Variables:**
- `BASE`
- `UNIT`
- `UNITS`
- `UNITS_CHANGES`
- `UNIT_VERIFICATION`
- `SET_UNIT_PHASE`
- `SET_UNIT_PROCESS`
- `ADD_CHILD_UNIT`
- `REMOVE_CHILD_UNIT`
- `CHECK_CHILD_UNITS`
- `SERIAL_NUMBERS`
- `SERIAL_NUMBER_TYPES`
- `SERIAL_NUMBERS_TAKE`
- `SERIAL_NUMBERS_BY_RANGE`
- `SERIAL_NUMBERS_BY_REFERENCE`
- `BATCH`
- `BATCHES`
- `PHASES`
- `SHIFT`
- `SHIFTS`
- `OPERATORS`
- `OPERATOR`

**Methods:**
- `batch(batch_id: str) -> str`
- `operator(operator_id: str) -> str`
- `shift(shift_id: str) -> str`
- `unit(serial_number: str, part_number: str) -> str`
- `unit_change(change_id: str) -> str`

---

### `Report`

_Report domain routes._

**Class Variables:**
- `BASE`
- `QUERY_HEADER`
- `QUERY_HEADER_BY_MISC`
- `WSJF`
- `WSXF`
- `ATTACHMENT`
- `UUT`
- `UUT_HEADERS`
- `UUR`
- `UUR_HEADERS`

**Methods:**
- `attachments(report_id: str) -> str`
- `certificate(report_id: str) -> str`
- `uur(report_id: str) -> str`
- `uut(report_id: str) -> str`
- `wsjf(report_id: str) -> str`
- `wsxf(report_id: str) -> str`

---

### `RootCause`

_RootCause/Ticketing routes._

**Class Variables:**
- `BASE`
- `TICKETS`
- `TICKET`
- `ARCHIVE_TICKETS`
- `ATTACHMENT`
- `TEAMS`

**Methods:**
- `ticket(ticket_id: str) -> str`
- `ticket_comment(ticket_id: str) -> str`
- `ticket_status(ticket_id: str) -> str`

---

### `Routes`

_Centralized API route definitions for all WATS domains._

---

### `SCIM`

_SCIM (User provisioning) routes._

**Class Variables:**
- `BASE`
- `TOKEN`
- `USERS`
- `GROUPS`

**Methods:**
- `group(group_id: str) -> str`
- `user(user_id: str) -> str`
- `user_by_name(username: str) -> str`

---

### `Software`

_Software distribution routes._

**Class Variables:**
- `BASE`
- `PACKAGES`
- `PACKAGE`
- `PACKAGE_BY_NAME`
- `PACKAGES_BY_TAG`
- `VIRTUAL_FOLDERS`
- `FILE`

**Methods:**
- `file_attribute(package_id: str) -> str`
- `package(package_id: str) -> str`
- `package_files(package_id: str) -> str`
- `package_status(package_id: str) -> str`
- `upload_zip(package_id: str) -> str`

---

## `core.station`

### `Purpose`

_Common station purpose values._

**Class Variables:**
- `PRODUCTION`
- `DEBUG`
- `DEVELOPMENT`
- `REPAIR`
- `QUALIFICATION`
- `CALIBRATION`
- `ENGINEERING`
- `RMA`

---

### `Station(BaseModel)`

_Represents a test station identity._

**Class Variables:**
- `model_config`
- `name: str`
- `location: str`
- `purpose: str`
- `description: str`

**Methods:**
- `copy() -> Any`
- `from_dict(cls, data: Dict[...]) -> Any`
- `from_hostname(cls, location: str, purpose: str, description: str) -> Any`
- `to_dict() -> Dict[...]`
- `validate_name(cls, v: str) -> str`

---

### `StationConfig(BaseModel)`

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
- `from_station(cls, key: str, station: Station, is_default: bool) -> Any`
- `to_dict() -> Dict[...]`
- `to_station() -> Station`

---

### `StationRegistry`

_Manages multiple station configurations._

**Properties:**
- `active`
- `active_key`
- `default`
- `keys`

**Methods:**
- `add(key: str, station: Station, set_active: bool) -> Any`
- `auto_detect() -> Station`
- `clear() -> Any`
- `from_list(cls, configs: List[...]) -> Any`
- `get(key: str) -> Optional[...]`
- `has(key: str) -> bool`
- `items() -> Iterator[...]`
- `remove(key: str) -> Optional[...]`
- `set_active(key: str) -> Any`
- `set_default(station: Station, key: Optional[...]) -> Any`
- `to_list() -> List[...]`
- `values() -> Iterator[...]`

---

## `core.sync_runner`

### `SyncWrapper`

_Base class for creating sync wrappers around async classes._

**Class Variables:**
- `_async: Any`

---

## `core.throttle`

### `RateLimiter`

_Thread-safe sliding window rate limiter._

**Properties:**
- `available_slots`
- `current_usage`
- `stats`

**Methods:**
- `acquire(timeout: Optional[...]) -> bool`
- `reset() -> Any`

---

## `core.validation`

### `ReportHeaderValidationError(ValidationError)`

_Raised when a report header field contains problematic characters._

---

### `ReportHeaderValidationWarning(UserWarning)`

_Warning issued when problematic characters are used with bypass enabled._

---


---

<a name="shared-models"></a>

# Shared Models

_Source: [pywats_shared.md](pywats_shared.md)_


## `shared.base_model`

### `PyWATSModel(BaseModel)`

_Base class for all pyWATS models._

**Class Variables:**
- `model_config`

---

## `shared.common_types`

### `ChangeType(IntEnum)`

_Change type for settings._

**Class Variables:**
- `NONE`
- `ADD`
- `UPDATE`
- `DELETE`
- `UNKNOWN_4`
- `UNKNOWN_5`
- `UNKNOWN_6`

---

### `Setting(PyWATSModel)`

_Key-value setting used for tags/custom data._

**Class Variables:**
- `key: str`
- `value: Optional[...]`
- `change: Optional[...]`

---

## `shared.enums`

### `CompOp(str, Enum)`

_Comparison operators for numeric limit steps._

**Class Variables:**
- `LOG`
- `EQ`
- `EQT`
- `NE`
- `LT`
- `LE`
- `GT`
- `GE`
- `CASESENSIT`
- `IGNORECASE`
- `GTLT`
- `GTLE`
- `GELT`
- `GELE`
- `LTGT`
- `LTGE`
- `LEGT`
- `LEGE`

**Methods:**
- `evaluate(value: Any, low_limit: Any, high_limit: Any) -> bool`
- `get_limits_requirement() -> tuple[...]`
- `validate_limits(low_limit: Any, high_limit: Any) -> bool`

---

### `QueueItemStatus(str, Enum)`

_Unified status for queue items across all queue implementations._

**Class Variables:**
- `PENDING`
- `PROCESSING`
- `COMPLETED`
- `FAILED`
- `SUSPENDED`

**Properties:**
- `can_process`
- `is_active`
- `is_terminal`

---

### `RunFilter(IntEnum)`

_Run filter for step/measurement analysis._

**Class Variables:**
- `FIRST`
- `SECOND`
- `THIRD`
- `LAST`
- `ALL`

---

### `SortDirection(str, Enum)`

_Sort direction for dimension queries._

**Class Variables:**
- `ASC`
- `DESC`

---

### `StatusFilter(str, Enum)`

_Status filter values for querying reports with flexible string conversion._

**Class Variables:**
- `PASSED`
- `FAILED`
- `ERROR`
- `TERMINATED`
- `DONE`
- `SKIPPED`

**Properties:**
- `full_name`
- `is_failure`
- `is_passing`

---

### `StepType(str, Enum)`

_Test step types in WATS._

**Class Variables:**
- `SEQUENCE_CALL`
- `NUMERIC_LIMIT`
- `STRING_VALUE`
- `PASS_FAIL`
- `MULTIPLE_NUMERIC`
- `ACTION`
- `MESSAGE_POPUP`
- `CALL_EXECUTABLE`
- `LABEL`
- `GOTO`
- `FLOW_CONTROL`
- `STATEMENT`
- `PROPERTY_LOADER`
- `GENERIC`
- `UNKNOWN`

---

## `shared.odata`

### `ODataFilterBuilder`

_Fluent builder for constructing OData filter expressions._

**Methods:**
- `build() -> str`
- `contains(value: str) -> Any`
- `endswith(value: str) -> Any`
- `eq(value: Any) -> Any`
- `field(name: str) -> Any`
- `ge(value: Any) -> Any`
- `gt(value: Any) -> Any`
- `in_list(values: List[...]) -> Any`
- `is_not_null() -> Any`
- `is_null() -> Any`
- `le(value: Any) -> Any`
- `lt(value: Any) -> Any`
- `ne(value: Any) -> Any`
- `or_group(builder: Any) -> Any`
- `raw(expression: str) -> Any`
- `startswith(value: str) -> Any`
- `use_and() -> Any`
- `use_or() -> Any`

---

## `shared.paths`

### `MeasurementPath(StepPath)`

_Represents a measurement path in WATS._

**Properties:**
- `measurement_name`
- `step_path`

---

### `StepPath`

_Represents a test step path in WATS._

**Properties:**
- `api_format`
- `display`
- `name`
- `parent`
- `parts`

**Methods:**
- `from_parts(cls) -> Any`

---

## `shared.result`

### `ErrorCode(str, Enum)`

_Standard error codes for pyWATS operations._

**Class Variables:**
- `INVALID_INPUT`
- `MISSING_REQUIRED_FIELD`
- `INVALID_FORMAT`
- `VALUE_OUT_OF_RANGE`
- `NOT_FOUND`
- `ALREADY_EXISTS`
- `CONFLICT`
- `OPERATION_FAILED`
- `SAVE_FAILED`
- `DELETE_FAILED`
- `UNAUTHORIZED`
- `FORBIDDEN`
- `CONNECTION_ERROR`
- `TIMEOUT`
- `API_ERROR`
- `UNKNOWN_ERROR`

---

### `Failure(BaseModel)`

_Represents a failed operation with structured error information._

**Class Variables:**
- `model_config`
- `error_code: str`
- `message: str`
- `details: Dict[...]`
- `suggestions: List[...]`

**Properties:**
- `is_failure`
- `is_success`
- `value`

---

### `Success(BaseModel, Unknown)`

_Represents a successful operation with a value._

**Class Variables:**
- `model_config`
- `value: Any`
- `message: str`

**Properties:**
- `error_code`
- `is_failure`
- `is_success`

---

## `shared.stats`

### `BatchResult`

_Result of a batch operation._

**Class Variables:**
- `total: int`
- `success: int`
- `failed: int`
- `results: List[...]`
- `errors: Dict[...]`

**Properties:**
- `all_succeeded`
- `success_rate`

---

### `CacheStats`

_Statistics about a cache's current state._

**Class Variables:**
- `hits: int`
- `misses: int`
- `size: int`
- `max_size: Optional[...]`

**Properties:**
- `hit_rate`
- `total_requests`
- `utilization`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `QueueProcessingResult`

_Result of processing a queue of reports._

**Class Variables:**
- `success: int`
- `failed: int`
- `skipped: int`
- `errors: List[...]`

**Properties:**
- `success_rate`
- `total`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `QueueStats`

_Statistics about a queue's current state._

**Class Variables:**
- `pending: int`
- `processing: int`
- `completed: int`
- `failed: int`

**Properties:**
- `active`
- `total`

**Methods:**
- `to_dict() -> Dict[...]`

---


---

<a name="analytics-domain"></a>

# Analytics Domain

_Source: [domain_analytics.md](domain_analytics.md)_


## `analytics.async_repository`

### `AsyncAnalyticsRepository`

_Async Analytics/Statistics data access layer._

---

## `analytics.async_service`

### `AsyncAnalyticsService`

_Async Analytics/Statistics business logic layer._

---

## `analytics.enums`

### `AlarmType(IntEnum)`

_Types of WATS alarms and notifications._

**Class Variables:**
- `REPORT`
- `YIELD_VOLUME`
- `SERIAL_NUMBER`
- `MEASUREMENT`
- `ASSET`

---

### `Dimension(str, Enum)`

_Dimension fields for dynamic yield/repair queries._

**Class Variables:**
- `PART_NUMBER`
- `PRODUCT_NAME`
- `PRODUCT_GROUP`
- `REVISION`
- `STATION_NAME`
- `LOCATION`
- `PURPOSE`
- `TEST_OPERATION`
- `PROCESS_CODE`
- `PERIOD`
- `SW_FILENAME`
- `SW_VERSION`
- `LEVEL`
- `BATCH_NUMBER`
- `OPERATOR`
- `FIXTURE_ID`
- `SOCKET_INDEX`
- `ERROR_CODE`
- `STEP_CAUSED_UUT_FAILURE`
- `STEP_PATH_CAUSED_UUT_FAILURE`
- `MISC_INFO_DESCRIPTION`
- `MISC_INFO_STRING`
- `ASSET_SERIAL_NUMBER`
- `ASSET_NAME`
- `UNIT_TYPE`

---

### `DimensionBuilder`

_Builder for constructing dimension query strings with type safety._

**Methods:**
- `add(dimension: Union[...], direction: Optional[...]) -> Any`
- `add_all() -> Any`
- `build() -> str`
- `clear() -> Any`
- `top_failing_products(cls) -> Any`
- `yield_by_product(cls, include_period: bool) -> Any`
- `yield_by_station(cls, include_period: bool) -> Any`

---

### `KPI(str, Enum)`

_Key Performance Indicators for yield/repair queries._

**Class Variables:**
- `UNIT_COUNT`
- `FP_COUNT`
- `SP_COUNT`
- `TP_COUNT`
- `LP_COUNT`
- `FP_FAIL_COUNT`
- `SP_FAIL_COUNT`
- `TP_FAIL_COUNT`
- `LP_FAIL_COUNT`
- `FPY`
- `SPY`
- `TPY`
- `LPY`
- `PPM_FPY`
- `PPM_SPY`
- `PPM_TPY`
- `PPM_LPY`
- `PPM_TEST_YIELD`
- `TEST_YIELD_COUNT`
- `TEST_REPORT_COUNT`
- `TEST_YIELD`
- `RETEST_COUNT`
- `FIRST_UTC`
- `LAST_UTC`

---

### `ProcessType(IntEnum)`

_Process/operation categories._

**Class Variables:**
- `TEST`
- `REPAIR`
- `CALIBRATION`

---

### `RepairDimension(str, Enum)`

_Additional dimensions specific to repair statistics._

**Class Variables:**
- `REPAIR_OPERATION`
- `REPAIR_CODE`
- `REPAIR_CATEGORY`
- `REPAIR_TYPE`
- `COMPONENT_REF`
- `COMPONENT_NUMBER`
- `COMPONENT_REVISION`
- `COMPONENT_VENDOR`
- `COMPONENT_DESCRIPTION`
- `FUNCTION_BLOCK`
- `REFERENCED_STEP`
- `REFERENCED_STEP_PATH`
- `TEST_PERIOD`
- `TEST_LEVEL`
- `TEST_STATION_NAME`
- `TEST_LOCATION`
- `TEST_PURPOSE`
- `TEST_OPERATOR`

---

### `RepairKPI(str, Enum)`

_KPIs specific to repair statistics._

**Class Variables:**
- `REPAIR_REPORT_COUNT`
- `REPAIR_COUNT`

---

### `YieldDataType(IntEnum)`

_Types of yield data calculations._

**Class Variables:**
- `FIRST_PASS`
- `FINAL`
- `ROLLED`

---

## `analytics.models`

### `AggregatedMeasurement(PyWATSModel)`

_Represents aggregated measurement statistics._

**Class Variables:**
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `count: Optional[...]`
- `min: Optional[...]`
- `max: Optional[...]`
- `avg: Optional[...]`
- `stdev: Optional[...]`
- `variance: Optional[...]`
- `limit_low: Optional[...]`
- `limit_high: Optional[...]`
- `cpk: Optional[...]`
- `cp: Optional[...]`
- `cp_lower: Optional[...]`
- `cp_upper: Optional[...]`
- `unit: Optional[...]`

---

### `AlarmLog(PyWATSModel)`

_Represents a triggered alarm or notification log entry._

**Class Variables:**
- `model_config`
- `log_id: Optional[...]`
- `name: Optional[...]`
- `log_date: Optional[...]`
- `trigger_id: Optional[...]`
- `type: Optional[...]`
- `state: Optional[...]`
- `grouping_set: Optional[...]`
- `calculations_string: Optional[...]`
- `client_group_ids: Optional[...]`
- `product_selection_ids: Optional[...]`
- `part_number: Optional[...]`
- `product_name: Optional[...]`
- `process_code: Optional[...]`
- `process_name: Optional[...]`
- `report_guid: Optional[...]`
- `serial_number: Optional[...]`
- `revision: Optional[...]`
- `station_name: Optional[...]`
- `operator: Optional[...]`
- `result: Optional[...]`
- `start_utc: Optional[...]`
- `fpy: Optional[...]`
- `spy: Optional[...]`
- `tpy: Optional[...]`
- `lpy: Optional[...]`
- `test_yield: Optional[...]`
- `fpy_trend: Optional[...]`
- `spy_trend: Optional[...]`
- `tpy_trend: Optional[...]`
- `lpy_trend: Optional[...]`
- `test_yield_trend: Optional[...]`
- `uut_count: Optional[...]`
- `unit_count: Optional[...]`
- `fp_count: Optional[...]`
- `lp_count: Optional[...]`
- `retest_count: Optional[...]`
- `sequence_count: Optional[...]`
- `sequential_match: Optional[...]`
- `free: Optional[...]`
- `reserved: Optional[...]`
- `serial_number_type: Optional[...]`
- `cp: Optional[...]`
- `cpk: Optional[...]`
- `min: Optional[...]`
- `max: Optional[...]`
- `avg: Optional[...]`
- `stdev: Optional[...]`
- `measurement_path: Optional[...]`
- `asset_name: Optional[...]`
- `asset_serial_number: Optional[...]`
- `type_id: Optional[...]`
- `asset_state: Optional[...]`
- `bubbled_status: Optional[...]`
- `tags: Optional[...]`
- `is_days_since_calibration_unknown: Optional[...]`
- `is_days_since_maintenance_unknown: Optional[...]`

**Properties:**
- `alarm_type_name`
- `fpy_percent`
- `fpy_trend_percent`

---

### `LevelInfo(PyWATSModel)`

_Represents production level information._

**Class Variables:**
- `level_id: Optional[...]`
- `level_name: Optional[...]`

---

### `MeasurementData(PyWATSModel)`

_Represents individual measurement data points._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `report_id: Optional[...]`
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `value: Optional[...]`
- `limit_low: Optional[...]`
- `limit_high: Optional[...]`
- `unit: Optional[...]`
- `status: Optional[...]`
- `timestamp: Optional[...]`

**Properties:**
- `step_path_display`

---

### `MeasurementListItem(PyWATSModel)`

_Represents measurement list data from the MeasurementList endpoint._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `report_id: Optional[...]`
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `value: Optional[...]`
- `string_value: Optional[...]`
- `limit_low: Optional[...]`
- `limit_high: Optional[...]`
- `unit: Optional[...]`
- `status: Optional[...]`
- `timestamp: Optional[...]`
- `station_name: Optional[...]`
- `model_config`

---

### `OeeAnalysisResult(PyWATSModel)`

_Represents OEE (Overall Equipment Effectiveness) analysis results._

**Class Variables:**
- `oee: Optional[...]`
- `availability: Optional[...]`
- `performance: Optional[...]`
- `quality: Optional[...]`
- `total_time: Optional[...]`
- `run_time: Optional[...]`
- `down_time: Optional[...]`
- `planned_production_time: Optional[...]`
- `total_count: Optional[...]`
- `good_count: Optional[...]`
- `reject_count: Optional[...]`
- `ideal_cycle_time: Optional[...]`
- `actual_cycle_time: Optional[...]`
- `period: Optional[...]`
- `part_number: Optional[...]`
- `station_name: Optional[...]`

---

### `ProcessInfo(PyWATSModel)`

_Represents process/test operation information._

**Class Variables:**
- `code: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`
- `is_test_operation: bool`
- `is_repair_operation: bool`
- `is_wip_operation: bool`
- `process_index: Optional[...]`
- `state: Optional[...]`

---

### `ProductGroup(PyWATSModel)`

_Represents a product group._

**Class Variables:**
- `product_group_id: Optional[...]`
- `product_group_name: Optional[...]`

---

### `RepairHistoryRecord(PyWATSModel)`

_Represents a repair history record for a specific part._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `report_id: Optional[...]`
- `repair_date: Optional[...]`
- `fail_step_name: Optional[...]`
- `fail_step_path: Optional[...]`
- `fail_code: Optional[...]`
- `repair_code: Optional[...]`
- `symptom: Optional[...]`
- `cause: Optional[...]`
- `action: Optional[...]`

---

### `RepairStatistics(PyWATSModel)`

_Represents repair statistics data from dynamic repair analysis._

**Class Variables:**
- `model_config`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `product_group: Optional[...]`
- `product_name: Optional[...]`
- `unit_type: Optional[...]`
- `repair_operation: Optional[...]`
- `station_name: Optional[...]`
- `test_operation: Optional[...]`
- `period: Optional[...]`
- `level: Optional[...]`
- `location: Optional[...]`
- `purpose: Optional[...]`
- `operator: Optional[...]`
- `misc_info_description: Optional[...]`
- `misc_info_string: Optional[...]`
- `repair_category: Optional[...]`
- `repair_type: Optional[...]`
- `component_ref: Optional[...]`
- `component_number: Optional[...]`
- `component_revision: Optional[...]`
- `component_vendor: Optional[...]`
- `component_description: Optional[...]`
- `function_block: Optional[...]`
- `referenced_step: Optional[...]`
- `referenced_step_path: Optional[...]`
- `test_period: Optional[...]`
- `test_level: Optional[...]`
- `test_station_name: Optional[...]`
- `test_location: Optional[...]`
- `test_purpose: Optional[...]`
- `test_operator: Optional[...]`
- `batch_number: Optional[...]`
- `sw_filename: Optional[...]`
- `sw_version: Optional[...]`
- `repair_report_count: Optional[...]`
- `repair_count: Optional[...]`
- `total_count: Optional[...]`
- `repair_rate: Optional[...]`
- `fail_code: Optional[...]`
- `repair_code: Optional[...]`

---

### `StepAnalysisRow(PyWATSModel)`

_Represents a single step (and optional measurement) KPI row._

**Class Variables:**
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `step_type: Optional[...]`
- `step_group: Optional[...]`
- `step_count: Optional[...]`
- `step_passed_count: Optional[...]`
- `step_done_count: Optional[...]`
- `step_skipped_count: Optional[...]`
- `step_failed_count: Optional[...]`
- `step_error_count: Optional[...]`
- `step_terminated_count: Optional[...]`
- `step_other_count: Optional[...]`
- `step_failed_error_terminated_count: Optional[...]`
- `step_caused_uut_failed_error_terminated: Optional[...]`
- `step_caused_uut_failed: Optional[...]`
- `step_caused_uut_error: Optional[...]`
- `step_caused_uut_terminated: Optional[...]`
- `limit1: Optional[...]`
- `limit1_wof: Optional[...]`
- `limit2: Optional[...]`
- `limit2_wof: Optional[...]`
- `comp_operator: Optional[...]`
- `step_time_avg: Optional[...]`
- `step_time_max: Optional[...]`
- `step_time_min: Optional[...]`
- `measure_name: Optional[...]`
- `measure_count: Optional[...]`
- `measure_count_wof: Optional[...]`
- `min: Optional[...]`
- `min_wof: Optional[...]`
- `max: Optional[...]`
- `max_wof: Optional[...]`
- `avg: Optional[...]`
- `avg_wof: Optional[...]`
- `stdev: Optional[...]`
- `stdev_wof: Optional[...]`
- `var: Optional[...]`
- `var_wof: Optional[...]`
- `cpk: Optional[...]`
- `cpk_wof: Optional[...]`
- `cp: Optional[...]`
- `cp_wof: Optional[...]`
- `cp_lower: Optional[...]`
- `cp_lower_wof: Optional[...]`
- `cp_upper: Optional[...]`
- `cp_upper_wof: Optional[...]`
- `sigma_high_3: Optional[...]`
- `sigma_high_3_wof: Optional[...]`
- `sigma_low_3: Optional[...]`
- `sigma_low_3_wof: Optional[...]`

**Properties:**
- `step_path_display`

---

### `StepStatusItem(PyWATSModel)`

_Represents step status data from the StepStatusList endpoint._

**Class Variables:**
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `step_type: Optional[...]`
- `step_group: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `pass_count: Optional[...]`
- `fail_count: Optional[...]`
- `total_count: Optional[...]`
- `status: Optional[...]`
- `timestamp: Optional[...]`
- `serial_number: Optional[...]`
- `report_id: Optional[...]`
- `model_config`

---

### `TopFailedStep(PyWATSModel)`

_Represents a top failed step from failure analysis._

**Class Variables:**
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `step_type: Optional[...]`
- `step_group: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `product_group: Optional[...]`
- `fail_count: Optional[...]`
- `total_count: Optional[...]`
- `fail_rate: Optional[...]`
- `first_fail_date: Optional[...]`
- `last_fail_date: Optional[...]`

**Properties:**
- `step_path_display`

---

### `UnitFlowFilter(PyWATSModel)`

_Filter parameters for Unit Flow queries._

**Class Variables:**
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `serial_number: Optional[...]`
- `serial_numbers: Optional[...]`
- `station_name: Optional[...]`
- `location: Optional[...]`
- `purpose: Optional[...]`
- `date_from: Optional[...]`
- `date_to: Optional[...]`
- `process_codes: Optional[...]`
- `include_passed: Optional[...]`
- `include_failed: Optional[...]`
- `split_by: Optional[...]`
- `unit_order: Optional[...]`
- `show_list: Optional[...]`
- `hide_list: Optional[...]`
- `expand_operations: Optional[...]`

**Methods:**
- `serialize_datetime(v: Optional[...]) -> Optional[...]`

---

### `UnitFlowLink(PyWATSModel)`

_Represents a link (edge) between nodes in the unit flow diagram._

**Class Variables:**
- `id: Optional[...]`
- `source_id: Optional[...]`
- `target_id: Optional[...]`
- `source_name: Optional[...]`
- `target_name: Optional[...]`
- `unit_count: Optional[...]`
- `pass_count: Optional[...]`
- `fail_count: Optional[...]`
- `avg_time: Optional[...]`
- `is_visible: Optional[...]`
- `model_config`

---

### `UnitFlowNode(PyWATSModel)`

_Represents a node in the unit flow diagram._

**Class Variables:**
- `id: Optional[...]`
- `name: Optional[...]`
- `process_code: Optional[...]`
- `process_name: Optional[...]`
- `station_name: Optional[...]`
- `location: Optional[...]`
- `purpose: Optional[...]`
- `unit_count: Optional[...]`
- `pass_count: Optional[...]`
- `fail_count: Optional[...]`
- `yield_percent: Optional[...]`
- `avg_time: Optional[...]`
- `is_expanded: Optional[...]`
- `is_visible: Optional[...]`
- `level: Optional[...]`
- `parent_id: Optional[...]`
- `model_config`

---

### `UnitFlowResult(PyWATSModel)`

_Complete result from a Unit Flow query._

**Class Variables:**
- `nodes: Optional[...]`
- `links: Optional[...]`
- `units: Optional[...]`
- `total_units: Optional[...]`
- `model_config`

---

### `UnitFlowUnit(PyWATSModel)`

_Represents a unit in the unit flow analysis._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `status: Optional[...]`
- `start_time: Optional[...]`
- `end_time: Optional[...]`
- `total_time: Optional[...]`
- `node_path: Optional[...]`
- `current_node: Optional[...]`
- `model_config`

---

### `YieldData(PyWATSModel)`

_Represents yield statistics data._

**Class Variables:**
- `model_config`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `product_name: Optional[...]`
- `product_group: Optional[...]`
- `station_name: Optional[...]`
- `test_operation: Optional[...]`
- `period: Optional[...]`
- `unit_count: Optional[...]`
- `fp_count: Optional[...]`
- `sp_count: Optional[...]`
- `tp_count: Optional[...]`
- `lp_count: Optional[...]`
- `fpy: Optional[...]`
- `spy: Optional[...]`
- `tpy: Optional[...]`
- `lpy: Optional[...]`

---


---

<a name="asset-domain"></a>

# Asset Domain

_Source: [domain_asset.md](domain_asset.md)_


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


---

<a name="process-domain"></a>

# Process Domain

_Source: [domain_process.md](domain_process.md)_


## `process.async_repository`

### `AsyncProcessRepository`

_Async Process data access layer._

---

## `process.async_service`

### `AsyncProcessService`

_Async Process business logic layer with enhanced TTL caching._

**Class Variables:**
- `DEFAULT_CACHE_TTL`
- `DEFAULT_TEST_PROCESS_CODE`
- `DEFAULT_REPAIR_PROCESS_CODE`

**Properties:**
- `cache_stats`
- `cache_ttl`
- `last_refresh`
- `refresh_interval`

**Methods:**
- `refresh_interval(value: float) -> Any`

---

## `process.models`

### `FailureCodeInfo(NamedTuple)`

_Flattened failure code info for easy lookup._

**Class Variables:**
- `category: str`
- `code: str`
- `guid: UUID`
- `category_guid: UUID`

---

### `ProcessInfo(PyWATSModel)`

_Process/operation information._

**Class Variables:**
- `code: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`
- `is_test_operation: bool`
- `is_repair_operation: bool`
- `is_wip_operation: bool`
- `process_id: Optional[...]`
- `process_index: Optional[...]`
- `state: Optional[...]`
- `properties: Optional[...]`
- `model_config`

---

### `RepairCategory(PyWATSModel)`

_Repair category (fail code category)._

**Class Variables:**
- `guid: UUID`
- `description: str`
- `selectable: bool`
- `sort_order: int`
- `failure_type: int`
- `image_constraint: Optional[...]`
- `status: int`
- `fail_codes: List[...]`

---

### `RepairOperationConfig(PyWATSModel)`

_Repair operation configuration._

**Class Variables:**
- `description: str`
- `uut_required: int`
- `comp_ref_mask: Optional[...]`
- `comp_ref_mask_description: Optional[...]`
- `bom_constraint: Optional[...]`
- `bom_required: int`
- `vendor_required: int`
- `categories: List[...]`
- `misc_infos: List[...]`

**Properties:**
- `failure_codes`

**Methods:**
- `get_fail_code_by_name(category: str, code: str) -> Optional[...]`
- `validate_fail_code(category: str, code: str) -> tuple[...]`

---


---

<a name="product-domain"></a>

# Product Domain

_Source: [domain_product.md](domain_product.md)_


## `product.async_box_build`

### `AsyncBoxBuildTemplate`

_Async builder class for managing box build templates (product-level definitions)._

**Properties:**
- `has_pending_changes`
- `parent_part_number`
- `parent_revision`
- `parent_revision_id`
- `subunits`

**Methods:**
- `clear_all() -> Any`
- `discard() -> Any`
- `get_matching_subunits(part_number: str) -> List[...]`
- `get_required_parts() -> List[...]`
- `validate_subunit(part_number: str, revision: str) -> bool`

---

## `product.async_repository`

### `AsyncProductRepository`

_Async Product data access layer._

---

## `product.async_service`

### `AsyncProductService`

_Async Product business logic._

**Methods:**
- `is_active(product: Product) -> bool`

---

## `product.box_build`

### `BoxBuildTemplate`

_Builder class for managing box build templates (product-level definitions)._

**Properties:**
- `has_pending_changes`
- `parent_part_number`
- `parent_revision`
- `parent_revision_id`
- `subunits`

**Methods:**
- `add_subunit(part_number: str, revision: str, quantity: int, item_number: Optional[...], revision_mask: Optional[...]) -> Any`
- `clear_all() -> Any`
- `discard() -> Any`
- `get_matching_subunits(part_number: str) -> List[...]`
- `get_required_parts() -> List[...]`
- `reload() -> Any`
- `remove_subunit(part_number: str, revision: str) -> Any`
- `save() -> Any`
- `set_quantity(part_number: str, revision: str, quantity: int) -> Any`
- `update_subunit(part_number: str, revision: str, quantity: Optional[...], item_number: Optional[...], revision_mask: Optional[...]) -> Any`
- `validate_subunit(part_number: str, revision: str) -> bool`

---

## `product.enums`

### `ProductState(IntEnum)`

_Product/Revision state._

**Class Variables:**
- `INACTIVE`
- `ACTIVE`

---

## `product.models`

### `BomItem(PyWATSModel)`

_Represents a Bill of Materials (BOM) item._

**Class Variables:**
- `bom_item_id: Optional[...]`
- `product_revision_id: Optional[...]`
- `component_ref: Optional[...]`
- `part_number: Optional[...]`
- `description: Optional[...]`
- `quantity: int`
- `manufacturer: Optional[...]`
- `manufacturer_pn: Optional[...]`
- `vendor: Optional[...]`
- `vendor_pn: Optional[...]`

---

### `Product(PyWATSModel)`

_Represents a product in WATS._

**Class Variables:**
- `part_number: str`
- `name: Optional[...]`
- `description: Optional[...]`
- `non_serial: bool`
- `state: ProductState`
- `product_id: Optional[...]`
- `xml_data: Optional[...]`
- `product_category_id: Optional[...]`
- `product_category_name: Optional[...]`
- `revisions: List[...]`
- `tags: List[...]`

---

### `ProductCategory(PyWATSModel)`

_Represents a product category._

**Class Variables:**
- `category_id: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`

---

### `ProductGroup(PyWATSModel)`

_Represents a product group._

**Class Variables:**
- `product_group_id: Optional[...]`
- `product_group_name: Optional[...]`

**Properties:**
- `name`

---

### `ProductRevision(PyWATSModel)`

_Represents a product revision in WATS._

**Class Variables:**
- `revision: str`
- `name: Optional[...]`
- `description: Optional[...]`
- `state: ProductState`
- `product_revision_id: Optional[...]`
- `product_id: Optional[...]`
- `xml_data: Optional[...]`
- `part_number: Optional[...]`
- `tags: List[...]`

---

### `ProductRevisionRelation(PyWATSModel)`

_Represents a parent-child relationship between product revisions._

**Class Variables:**
- `relation_id: Optional[...]`
- `parent_product_revision_id: UUID`
- `child_product_revision_id: UUID`
- `quantity: int`
- `item_number: Optional[...]`
- `child_part_number: Optional[...]`
- `child_revision: Optional[...]`
- `revision_mask: Optional[...]`

**Methods:**
- `matches_revision(revision: str) -> bool`

---

### `ProductView(PyWATSModel)`

_Simplified product view (used in list views)._

**Class Variables:**
- `part_number: str`
- `name: Optional[...]`
- `category: Optional[...]`
- `non_serial: bool`
- `state: ProductState`

---

## `product.sync_box_build`

### `SyncBoxBuildTemplate`

_Synchronous wrapper for AsyncBoxBuildTemplate._

**Properties:**
- `has_pending_changes`
- `parent_part_number`
- `parent_revision`
- `parent_revision_id`
- `subunits`

**Methods:**
- `add_subunit(part_number: str, revision: str, quantity: int, item_number: Optional[...], revision_mask: Optional[...]) -> Any`
- `clear_all() -> Any`
- `discard() -> Any`
- `get_matching_subunits(part_number: str) -> List[...]`
- `get_required_parts() -> List[...]`
- `reload() -> Any`
- `remove_subunit(part_number: str, revision: str) -> Any`
- `save() -> Any`
- `set_quantity(part_number: str, revision: str, quantity: int) -> Any`
- `update_subunit(part_number: str, revision: str, quantity: Optional[...], item_number: Optional[...], revision_mask: Optional[...]) -> Any`
- `validate_subunit(part_number: str, revision: str) -> bool`

---


---

<a name="production-domain"></a>

# Production Domain

_Source: [domain_production.md](domain_production.md)_


## `production.async_repository`

### `AsyncProductionRepository`

_Async Production data access layer._

---

## `production.async_service`

### `AsyncProductionService`

_Async Production business logic._

---

## `production.enums`

### `SerialNumberIdentifier(IntEnum)`

_Serial number identifier type._

**Class Variables:**
- `SERIAL_NUMBER`
- `MAC_ADDRESS`
- `IMEI`

---

### `UnitPhaseFlag(IntFlag)`

_Unit phase flags representing lifecycle states._

**Class Variables:**
- `UNKNOWN`
- `UNDER_PRODUCTION`
- `PRODUCTION_REPAIR`
- `SERVICE_REPAIR`
- `FINALIZED`
- `SCRAPPED`
- `EXTENDED_TEST`
- `CUSTOMIZATION`
- `REPAIRED`
- `MISSING`
- `IN_STORAGE`
- `SHIPPED`

---

## `production.models`

### `ProductionBatch(PyWATSModel)`

_Represents a production batch._

**Class Variables:**
- `batch_number: Optional[...]`
- `batch_size: Optional[...]`

---

### `SerialNumberType(PyWATSModel)`

_Represents a serial number type configuration._

**Class Variables:**
- `name: Optional[...]`
- `description: Optional[...]`
- `format: Optional[...]`
- `reg_ex: Optional[...]`
- `identifier: SerialNumberIdentifier`
- `identifier_name: Optional[...]`

---

### `Unit(PyWATSModel)`

_Represents a production unit in WATS._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `parent_serial_number: Optional[...]`
- `batch_number: Optional[...]`
- `serial_date: Optional[...]`
- `current_location: Optional[...]`
- `xml_data: Optional[...]`
- `unit_phase_id: Optional[...]`
- `unit_phase: Optional[...]`
- `process_code: Optional[...]`
- `tags: List[...]`
- `product_revision: Optional[...]`
- `product: Optional[...]`
- `sub_units: List[...]`

---

### `UnitChange(PyWATSModel)`

_Represents a unit change record._

**Class Variables:**
- `id: Optional[...]`
- `unit_serial_number: Optional[...]`
- `new_parent_serial_number: Optional[...]`
- `new_part_number: Optional[...]`
- `new_revision: Optional[...]`
- `new_unit_phase_id: Optional[...]`

---

### `UnitPhase(PyWATSModel)`

_Represents a unit phase in WATS._

**Class Variables:**
- `phase_id: int`
- `code: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`

---

### `UnitVerification(PyWATSModel)`

_Represents unit verification result for a single process._

**Class Variables:**
- `process_code: Optional[...]`
- `process_name: Optional[...]`
- `process_index: Optional[...]`
- `status: Optional[...]`
- `start_utc: Optional[...]`
- `station_name: Optional[...]`
- `total_count: Optional[...]`
- `non_passed_count: Optional[...]`
- `repair_count: Optional[...]`

---

### `UnitVerificationGrade(PyWATSModel)`

_Represents complete unit verification grade result._

**Class Variables:**
- `status: Optional[...]`
- `grade: Optional[...]`
- `all_processes_executed_in_correct_order: bool`
- `all_processes_passed_first_run: bool`
- `all_processes_passed_any_run: bool`
- `all_processes_passed_last_run: bool`
- `no_repairs: bool`
- `results: List[...]`

---


---

<a name="report-domain"></a>

# Report Domain

_Source: [domain_report.md](domain_report.md)_


## `report.async_repository`

### `AsyncReportRepository`

_Async Report data access layer._

**Properties:**
- `import_mode`

**Methods:**
- `import_mode(value: ImportMode) -> Any`

---

## `report.async_service`

### `AsyncReportService`

_Async Report business logic._

**Methods:**
- `create_uur_from_uut(uut_report: UUTReport, operator: Optional[...], comment: Optional[...]) -> UURReport`
- `create_uur_report(uut_or_guid_or_pn: UUID, test_operation_code_pos: Any) -> UURReport`
- `create_uur_report(uut_or_guid_or_pn: UUTReport, test_operation_code_pos: Any) -> UURReport`
- `create_uur_report(uut_or_guid_or_pn: Union[...], test_operation_code_pos: Optional[...]) -> UURReport`
- `create_uur_report(uut_or_guid_or_pn: str, test_operation_code_pos: int) -> UURReport`
- `create_uut_report(operator: str, part_number: str, revision: str, serial_number: str, operation_type: int) -> UUTReport`

---

### `StationInfo(Protocol)`

_Protocol for station information provider._

**Class Variables:**
- `name: str`
- `location: str`
- `purpose: str`

---

## `report.enums`

### `DateGrouping(IntEnum)`

_Date grouping options for filters._

**Class Variables:**
- `NONE`
- `YEAR`
- `QUARTER`
- `MONTH`
- `WEEK`
- `DAY`
- `HOUR`

---

### `ImportMode(Enum)`

_Import mode for UUT report creation._

**Class Variables:**
- `Import`
- `Active`

---

### `ReportType(str, Enum)`

_Report type for querying headers._

**Class Variables:**
- `UUT`
- `UUR`

---

## `report.models`

### `AttachmentMetadata(PyWATSModel)`

_Metadata for a report attachment from API responses._

**Class Variables:**
- `attachment_id: Optional[...]`
- `file_name: Optional[...]`
- `mime_type: Optional[...]`
- `size: Optional[...]`
- `description: Optional[...]`

---

### `HeaderAsset(PyWATSModel)`

_Asset info from OData expanded header query._

**Class Variables:**
- `serial_number: Optional[...]`
- `running_count: Optional[...]`
- `total_count: Optional[...]`
- `days_since_calibration: Optional[...]`
- `calibration_days_overdue: Optional[...]`

---

### `HeaderMiscInfo(PyWATSModel)`

_Misc info from OData expanded header query._

**Class Variables:**
- `description: Optional[...]`
- `value: Optional[...]`

---

### `HeaderSubUnit(PyWATSModel)`

_Sub-unit info from OData expanded header query._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `part_type: Optional[...]`

---

### `ReportHeader(PyWATSModel)`

_Represents a report header (summary info)._

**Class Variables:**
- `uuid: Optional[...]`
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `batch_number: Optional[...]`
- `report_type: Optional[...]`
- `station_name: Optional[...]`
- `location: Optional[...]`
- `purpose: Optional[...]`
- `process_code: Optional[...]`
- `process_name: Optional[...]`
- `result: Optional[...]`
- `start_utc: Optional[...]`
- `operator: Optional[...]`
- `comment: Optional[...]`
- `execution_time: Optional[...]`
- `sw_filename: Optional[...]`
- `sw_version: Optional[...]`
- `test_socket_index: Optional[...]`
- `fixture_id: Optional[...]`
- `run: Optional[...]`
- `passed_in_run: Optional[...]`
- `receive_count: Optional[...]`
- `report_size: Optional[...]`
- `caused_uut_failure: Optional[...]`
- `caused_uut_failure_path: Optional[...]`
- `error_code: Optional[...]`
- `error_message: Optional[...]`
- `referenced_uut: Optional[...]`
- `test_operation: Optional[...]`
- `root_node_type: Optional[...]`
- `sub_units: Optional[...]`
- `uur_sub_units: Optional[...]`
- `misc_info: Optional[...]`
- `assets: Optional[...]`

---

### `WATSFilter(PyWATSModel)`

_WATS filter for querying reports and statistics._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `batch_number: Optional[...]`
- `station_name: Optional[...]`
- `test_operation: Optional[...]`
- `status: Optional[...]`
- `yield_value: Optional[...]`
- `misc_description: Optional[...]`
- `misc_value: Optional[...]`
- `misc_info_description: Optional[...]`
- `misc_info_string: Optional[...]`
- `asset_serial_number: Optional[...]`
- `asset_name: Optional[...]`
- `product_group: Optional[...]`
- `level: Optional[...]`
- `sw_filename: Optional[...]`
- `sw_version: Optional[...]`
- `socket: Optional[...]`
- `date_from: Optional[...]`
- `date_to: Optional[...]`
- `date_grouping: Optional[...]`
- `period_count: Optional[...]`
- `include_current_period: Optional[...]`
- `max_count: Optional[...]`
- `min_count: Optional[...]`
- `top_count: Optional[...]`
- `dimensions: Optional[...]`
- `run: Optional[...]`
- `measurement_paths: Optional[...]`

**Methods:**
- `normalize_date_grouping(cls, v: object) -> object`
- `normalize_measurement_paths(cls, v: object) -> object`
- `normalize_run(cls, v: object) -> object`
- `normalize_status(cls, v: object) -> object`
- `serialize_datetime(v: Optional[...]) -> Optional[...]`

---

## `report.report_models.asset`

### `Asset(WATSBase)`

_Represents test equipment or assets used during testing._

**Class Variables:**
- `sn: str`
- `asset_type: Optional[...]`
- `pn: Optional[...]`
- `usage_count: Optional[...]`
- `calibration_date: Optional[...]`
- `calibration_due: Optional[...]`

**Methods:**
- `validate_sn(cls, v: str) -> str`

---

### `AssetStats(WATSBase)`

_Statistics about an asset._

**Class Variables:**
- `sn: Optional[...]`
- `running_count: Optional[...]`
- `running_count_exceeded: Optional[...]`
- `total_count: Optional[...]`
- `total_count_exceeded: Optional[...]`
- `days_since_calibration: Optional[...]`
- `is_days_since_calibration_unknown: Optional[...]`
- `calibration_days_overdue: Optional[...]`
- `days_since_maintenance: Optional[...]`
- `is_days_since_maintenance_unknown: Optional[...]`
- `maintenance_days_overdue: Optional[...]`
- `message: Optional[...]`

---

## `report.report_models.binary_data`

### `AdditionalData(WATSBase)`

_A collection of additional step, header, or station data._

**Class Variables:**
- `name: str`
- `props: List[...]`

---

### `AdditionalDataArray(WATSBase)`

_Information about array in additional data._

**Class Variables:**
- `dimension: int`
- `type: str`
- `indexes: List[...]`

---

### `AdditionalDataArrayIndex(WATSBase)`

_Information about an index in an array._

**Class Variables:**
- `text: str`
- `indexes: List[...]`
- `value: Optional[...]`

---

### `AdditionalDataProperty(WATSBase)`

_An additional data property._

**Class Variables:**
- `name: str`
- `type: str`
- `flags: Optional[...]`
- `value: Optional[...]`
- `comment: Optional[...]`
- `num_format: Optional[...]`
- `props: Optional[...]`
- `array: Optional[...]`

---

### `Attachment(WATSBase)`

_File attachment for reports or steps._

**Class Variables:**
- `DEFAULT_MAX_SIZE: ClassVar[...]`
- `name: str`
- `content_type: Optional[...]`
- `data: Optional[...]`
- `description: Optional[...]`
- `failure_idx: Optional[...]`

**Methods:**
- `from_bytes(cls, name: str, content: bytes, content_type: str, failure_idx: Optional[...], max_size: Optional[...]) -> Any`
- `get_bytes() -> bytes`

---

### `BinaryData(WATSBase)`

_Binary data embedded in a report._

**Class Variables:**
- `content_type: str`
- `data: str`
- `name: str`

**Methods:**
- `from_bytes(cls, data: bytes, name: str, content_type: str) -> Any`
- `get_bytes() -> bytes`

---

### `LoopInfo(WATSBase)`

_Loop iteration information for steps executed in loops._

**Class Variables:**
- `index: int`
- `count: Optional[...]`
- `parent: Optional[...]`

---

## `report.report_models.chart`

### `Chart(WATSBase)`

_Chart configuration and data for visualization._

**Class Variables:**
- `chart_type: ChartType`
- `label: str`
- `x_label: str`
- `x_unit: str`
- `y_label: str`
- `y_unit: str`
- `series: List[...]`

**Methods:**
- `AddSeries(name: str, y_label: str, y_values: List[...], x_label: str, x_values: Any) -> ChartSeries`
- `add_series(name: str, x_data: List[...], y_data: List[...], data_type: str) -> ChartSeries`

---

### `ChartSeries(WATSBase)`

_A single data series in a chart._

**Class Variables:**
- `data_type: str`
- `name: str`
- `x_data: Optional[...]`
- `y_data: Optional[...]`

---

## `report.report_models.common_types`

### `ChartType(str, Enum)`

_Chart visualization types._

**Class Variables:**
- `LINE`
- `LINE_LOG_XY`
- `LINE_LOG_X`
- `LINE_LOG_Y`

---

### `FlowType(str, Enum)`

_Flow control step types for GenericStep._

**Class Variables:**
- `NOP`
- `Statement`
- `Label`
- `Goto`
- `WATS_Goto`
- `Flow_If`
- `Flow_ElseIf`
- `Flow_Else`
- `Flow_End`
- `Flow_For`
- `Flow_ForEach`
- `Flow_Break`
- `Flow_Continue`
- `Flow_EndLoop`
- `Flow_While`
- `Flow_DoWhile`
- `Flow_Select`
- `Flow_Case`
- `Flow_Default`
- `Flow_EndSelect`

---

### `ReportStatus(str, Enum)`

_Overall report status with flexible string conversion._

**Class Variables:**
- `Passed`
- `Failed`
- `Done`
- `Error`
- `Terminated`

**Properties:**
- `full_name`
- `is_failure`
- `is_passing`

---

### `ReportType(str, Enum)`

_Report type discriminator._

**Class Variables:**
- `UUT`
- `UUR`

---

### `SequenceCallInfo(WATSBase)`

_Sequence call information for SequenceCall steps._

**Class Variables:**
- `path: str`
- `file_name: str`
- `version: str`

**Methods:**
- `set_defaults(cls, data)`

---

### `StepGroup(str, Enum)`

_Step group classification._

**Class Variables:**
- `Setup`
- `Main`
- `Cleanup`

---

### `StepStatus(str, Enum)`

_Step execution status with flexible string conversion._

**Class Variables:**
- `Passed`
- `Failed`
- `Skipped`
- `Done`
- `Error`
- `Terminated`

**Properties:**
- `full_name`
- `is_failure`
- `is_passing`

---

## `report.report_models.misc_info`

### `MiscInfo(WATSBase)`

_Miscellaneous information key-value pair._

**Class Variables:**
- `id: Optional[...]`
- `description: str`
- `string_value: Optional[...]`
- `numeric_value: Optional[...]`

**Methods:**
- `convert_numeric_to_string() -> Any`

---

### `UURMiscInfo(WATSBase)`

_UUR-specific miscellaneous information._

**Class Variables:**
- `key: str`
- `value: Optional[...]`

---

## `report.report_models.report`

### `Report(WATSBase, Unknown)`

_Base class for all WATS reports._

**Class Variables:**
- `id: UUID`
- `type: str`
- `pn: str`
- `sn: str`
- `rev: str`
- `process_code: int`
- `result: ReportResult`
- `station_name: str`
- `location: str`
- `purpose: str`
- `start: Optional[...]`
- `start_utc: Optional[...]`
- `info: Optional[...]`
- `sub_units: Optional[...]`
- `misc_infos: List[...]`
- `assets: Optional[...]`
- `asset_stats: Optional[...]`
- `binary_data: Optional[...]`
- `additional_data: Optional[...]`
- `origin: Optional[...]`
- `product_name: Optional[...]`
- `process_name: Optional[...]`
- `process_code_format: Optional[...]`

**Methods:**
- `add_asset(sn: str, usage_count: int) -> Asset`
- `add_binary_data(data: bytes, name: str, content_type: str) -> BinaryData`
- `add_misc_info(description: str, value: Any) -> MiscInfo`
- `add_sub_unit(part_type: str, sn: str, pn: str, rev: str) -> SubUnitT`
- `sync_start_times() -> Any`
- `validate_pn(cls, v: str) -> str`
- `validate_sn(cls, v: str) -> str`

---

## `report.report_models.report_info`

### `ReportInfo(WATSBase)`

_Base class for report-specific information._

**Class Variables:**
- `operator: str`
- `comment: Optional[...]`
- `exec_time: Optional[...]`

**Methods:**
- `serialize_exec_time(value: Optional[...]) -> Optional[...]`

---

## `report.report_models.sub_unit`

### `SubUnit(WATSBase)`

_Represents a sub-unit/component of a tested or repaired unit._

**Class Variables:**
- `pn: str`
- `rev: Optional[...]`
- `sn: str`
- `part_type: Optional[...]`

**Methods:**
- `validate_pn(cls, v: str) -> str`
- `validate_sn(cls, v: str) -> str`

---

## `report.report_models.uur.uur_failure`

### `UURFailure(WATSBase)`

_Failure record for UUR sub-units._

**Class Variables:**
- `category: str`
- `code: str`
- `comment: Optional[...]`
- `com_ref: Optional[...]`
- `func_block: Optional[...]`
- `ref_step_id: Optional[...]`
- `ref_step_name: Optional[...]`
- `art_number: Optional[...]`
- `art_rev: Optional[...]`
- `art_vendor: Optional[...]`
- `art_description: Optional[...]`

---

## `report.report_models.uur.uur_info`

### `UURInfo(ReportInfo)`

_UUR-specific information (serialized as 'uur' object)._

**Class Variables:**
- `process_code: Optional[...]`
- `process_code_format: Optional[...]`
- `process_name: Optional[...]`
- `test_operation_code: Optional[...]`
- `test_operation_name: Optional[...]`
- `test_operation_guid: Optional[...]`
- `ref_uut: Optional[...]`
- `confirm_date: Optional[...]`
- `finalize_date: Optional[...]`
- `active: bool`
- `parent: Optional[...]`

**Methods:**
- `get_repair_process_info() -> dict`
- `get_test_operation_info() -> dict`
- `set_dual_process_codes(repair_code: int, repair_name: str, test_code: int, test_name: str, test_guid: Optional[...]) -> Any`
- `sync_process_codes() -> Any`
- `to_dict() -> dict`
- `to_uur_type_dict() -> dict`
- `validate_dual_process_codes() -> tuple[...]`

---

## `report.report_models.uur.uur_report`

### `UURReport(Unknown)`

_Unit Under Repair (UUR) report._

**Class Variables:**
- `type: Literal[...]`
- `info: Optional[...]`
- `sub_units: List[...]`
- `asset_stats: Optional[...]`
- `attachments: List[...]`

**Properties:**
- `all_failures`
- `comment`
- `execution_time`
- `failures`
- `operator`
- `repair_operation_code`
- `repair_process_code`
- `test_operation_code`
- `uut_guid`

**Methods:**
- `add_attachment(attachment: Attachment) -> Any`
- `add_failure(category: str, code: str, comment: Optional[...], component_ref: Optional[...], ref_step_id: Optional[...], sub_unit_idx: Optional[...]) -> UURFailure`
- `add_failure_to_main_unit(category: str, code: str, comment: Optional[...], component_ref: Optional[...]) -> UURFailure`
- `add_failure_to_sub_unit(category: str, code: str, serial_number: Optional[...], idx: Optional[...], comment: Optional[...], component_ref: Optional[...], ref_step_id: Optional[...]) -> UURFailure`
- `add_main_failure(category: str, code: str) -> UURFailure`
- `add_sub_unit(pn: str, sn: str, rev: Optional[...], part_type: str, parent_idx: Optional[...]) -> UURSubUnit`
- `attach_bytes(name: str, content: bytes, mime_type: str) -> Attachment`
- `comment(value: str) -> Any`
- `copy_misc_from_uut(uut_report: Any) -> Any`
- `count_failures() -> int`
- `ensure_main_unit() -> Any`
- `execution_time(value: float) -> Any`
- `get_all_failures() -> List[...]`
- `get_main_unit() -> UURSubUnit`
- `get_sub_unit(idx: int) -> Optional[...]`
- `get_sub_unit_by_idx(idx: int) -> Optional[...]`
- `get_summary() -> dict`
- `link_to_uut(uut_id: UUID) -> Any`
- `operator(value: str) -> Any`
- `set_repair_process(code: int, name: Optional[...]) -> Any`
- `set_test_operation(code: int, name: Optional[...], guid: Optional[...]) -> Any`
- `uut_guid(value: UUID) -> Any`
- `validate_report() -> tuple[...]`

---

## `report.report_models.uur.uur_sub_unit`

### `UURSubUnit(SubUnit)`

_Extended sub-unit for UUR (repair) reports._

**Class Variables:**
- `sn: str`
- `part_type: Optional[...]`
- `idx: int`
- `parent_idx: Optional[...]`
- `position: Optional[...]`
- `replaced_idx: Optional[...]`
- `failures: Optional[...]`

**Methods:**
- `add_failure(category: str, code: str) -> UURFailure`
- `create_main_unit(cls, pn: str, sn: str, rev: str) -> Any`
- `get_failures() -> List[...]`
- `has_failures() -> bool`

---

## `report.report_models.uut.step`

### `Step(WATSBase, ABC)`

_Abstract base class for all WATS test steps._

**Class Variables:**
- `MAX_NAME_LENGTH: ClassVar[...]`
- `parent: Optional[...]`
- `fail_parent_on_failure: bool`
- `step_type: str`
- `name: str`
- `group: str`
- `status: StepStatus`
- `id: Optional[...]`
- `error_code: Optional[...]`
- `error_code_format: Optional[...]`
- `error_message: Optional[...]`
- `report_text: Optional[...]`
- `start: Optional[...]`
- `tot_time: Optional[...]`
- `tot_time_format: Optional[...]`
- `ts_guid: Optional[...]`
- `caused_seq_failure: Optional[...]`
- `caused_uut_failure: Optional[...]`
- `loop: Optional[...]`
- `additional_results: Optional[...]`
- `chart: Optional[...]`
- `attachment: Optional[...]`

**Methods:**
- `add_attachment(attachment: Attachment) -> Any`
- `add_chart(chart_type: ChartType, chart_label: str, x_label: str, x_unit: str, y_label: str, y_unit: str) -> Chart`
- `get_step_path() -> str`
- `propagate_failure() -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.action_step`

### `ActionStep(Step)`

_Action step with no measurement._

**Class Variables:**
- `step_type: Literal[...]`

**Methods:**
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.boolean_step`

### `MultiBooleanStep(Step)`

_Multi-boolean test step with multiple measurements._

**Class Variables:**
- `step_type: Literal[...]`
- `measurements: List[...]`

**Methods:**
- `add_measurement() -> MultiBooleanMeasurement`
- `check_for_duplicates(name: str) -> str`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

### `PassFailStep(Step)`

_Pass/Fail test step._

**Class Variables:**
- `step_type: Literal[...]`
- `measurement: Optional[...]`

**Properties:**
- `value`

**Methods:**
- `create(cls, name: str, value: Any) -> Any`
- `unwrap_measurement(cls, data: Any) -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`
- `value(val: Any) -> Any`
- `wrap_measurement(cls, value: Optional[...]) -> Optional[...]`

---

## `report.report_models.uut.steps.callexe_step`

### `CallExeStep(Step)`

_Represents a step that calls an external executable._

**Class Variables:**
- `step_type: str`
- `info: Optional[...]`

---

### `CallExeStepInfo(WATSBase)`

_Information about a CallExecutable step._

**Class Variables:**
- `exit_code: Optional[...]`

---

## `report.report_models.uut.steps.chart_step`

### `ChartStep(Step)`

_Chart step for standalone chart display._

**Class Variables:**
- `step_type: Literal[...]`

**Methods:**
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.generic_step`

### `FlowType(Enum)`

_Flow control step types from TestStand._

**Class Variables:**
- `FTPFiles`
- `If`
- `ElseIf`
- `Else`
- `End`
- `For`
- `ForEach`
- `Break`
- `Continue`
- `DoWhile`
- `While`
- `Select`
- `Case`
- `NI_Flow_StreamLoop`
- `NI_Flow_SweepLoop`
- `Lock`
- `Rendezvous`
- `Queue`
- `Notification`
- `Wait`
- `Batch_Sync`
- `AutoSchedule`
- `UseResource`
- `ThreadPriority`
- `Semaphore`
- `BatchSpec`
- `BatchSync`
- `OpenDatabase`
- `OpenSQLStatement`
- `CloseSQLStatement`
- `CloseDatabase`
- `DataOperation`
- `NI_CPUAffinity`
- `NI_IviDmm`
- `NI_IviScope`
- `NI_IviFgen`
- `NI_IviDCPower`
- `NI_IviSwitch`
- `NI_IviTools`
- `NI_LV_DeployLibrary`
- `LV_CheckSystemStatus`
- `LV_RunVIAsynchronously`
- `NI_PropertyLoader`
- `NI_VariableAndPropertyLoader`
- `NI_NewCsvFileInputRecordStream`
- `NI_NewCsvFileOutputRecordStream`
- `NI_WriteRecord`
- `Goto`
- `Action`
- `Statement`
- `Label`
- `GenericTest`

---

### `GenericStep(Step)`

_Generic test step for custom/arbitrary data._

**Class Variables:**
- `step_type: GenericStepLiteral`

**Methods:**
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.limit_measurement`

### `LimitMeasurement(BaseMeasurement)`

_A measurement with limit checking._

**Class Variables:**
- `value: Union[...]`
- `value_format: Optional[...]`
- `comp_op: Optional[...]`
- `high_limit: Optional[...]`
- `high_limit_format: Optional[...]`
- `low_limit: Optional[...]`
- `low_limit_format: Optional[...]`

**Methods:**
- `calculate_status() -> str`

---

## `report.report_models.uut.steps.measurement`

### `BaseMeasurement(WATSBase, ABC)`

_Abstract base for all measurement types._

**Class Variables:**
- `status: StepStatus`
- `name: Optional[...]`

---

### `BooleanMeasurement(BaseMeasurement)`

_Boolean (pass/fail) measurement._

**Class Variables:**
- `value: Optional[...]`

**Methods:**
- `validate_against_expected(expected: bool) -> tuple[...]`

---

### `MultiBooleanMeasurement(BooleanMeasurement)`

_Boolean measurement with required name for multi-measurement steps._

**Class Variables:**
- `name: str`

---

### `MultiNumericMeasurement(NumericMeasurement)`

_Numeric measurement with required name for multi-measurement steps._

**Class Variables:**
- `name: str`

---

### `MultiStringMeasurement(StringMeasurement)`

_String measurement with required name for multi-measurement steps._

**Class Variables:**
- `name: str`

---

### `NumericMeasurement(BaseMeasurement)`

_Numeric measurement with limits._

**Class Variables:**
- `value: Optional[...]`
- `value_format: Optional[...]`
- `unit: Optional[...]`
- `comp_op: Optional[...]`
- `high_limit: Optional[...]`
- `high_limit_format: Optional[...]`
- `low_limit: Optional[...]`
- `low_limit_format: Optional[...]`

**Methods:**
- `calculate_status() -> str`
- `validate_against_limits() -> tuple[...]`

---

### `SingleMeasurementMixin(Unknown)`

_Mixin that provides wrap/unwrap serialization for single-measurement steps._

**Class Variables:**
- `measurement: Optional[...]`
- `_measurement_class: ClassVar[...]`

**Methods:**
- `unwrap_measurement_list(cls, data: Any) -> Any`
- `wrap_measurement_list(cls, value: Optional[...]) -> Optional[...]`

---

### `StringMeasurement(BaseMeasurement)`

_String measurement with comparison._

**Class Variables:**
- `value: Optional[...]`
- `comp_op: Optional[...]`
- `limit: Optional[...]`

**Methods:**
- `validate_against_limit() -> tuple[...]`

---

## `report.report_models.uut.steps.message_popup_step`

### `MessagePopUpStep(Step)`

_Represents a step that displays a message popup to the user._

**Class Variables:**
- `step_type: str`
- `info: Optional[...]`

---

### `MessagePopupInfo(WATSBase)`

_Information about a MessagePopup step._

**Class Variables:**
- `response: Optional[...]`
- `button: Optional[...]`

**Methods:**
- `set_default_response() -> Any`

---

## `report.report_models.uut.steps.numeric_step`

### `MultiNumericStep(Step)`

_Multi-numeric limit test step._

**Class Variables:**
- `step_type: Literal[...]`
- `measurements: List[...]`

**Methods:**
- `add_measurement()`
- `check_for_duplicates(name)`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

### `NumericStep(Step)`

_Numeric limit test step._

**Class Variables:**
- `step_type: Literal[...]`
- `measurement: Optional[...]`

**Properties:**
- `comp_op`
- `high_limit`
- `low_limit`
- `unit`
- `value`

**Methods:**
- `comp_op(val: Any) -> Any`
- `create(cls, name: str, value: Any) -> Any`
- `high_limit(val: Any) -> Any`
- `low_limit(val: Any) -> Any`
- `unit(val: Any) -> Any`
- `unwrap_measurement(cls, data: Any) -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`
- `value(val: Any) -> Any`
- `wrap_measurement(cls, value: Optional[...]) -> Optional[...]`

---

## `report.report_models.uut.steps.sequence_call`

### `SequenceCall(Step)`

_Sequence call step - container for child steps._

**Class Variables:**
- `step_type: Literal[...]`
- `sequence: SequenceCallInfo`
- `caller: Optional[...]`
- `module: Optional[...]`
- `steps: StepList[...]`
- `add_pass_fail_step`

**Methods:**
- `add_action_step(name: str) -> ActionStep`
- `add_boolean_step() -> PassFailStep`
- `add_chart_step(name: str) -> ChartStep`
- `add_generic_step() -> GenericStep`
- `add_multi_boolean_step() -> MultiBooleanStep`
- `add_multi_numeric_step() -> MultiNumericStep`
- `add_multi_string_step() -> MultiStringStep`
- `add_numeric_step() -> NumericStep`
- `add_sequence_call(name: str) -> Any`
- `add_step(step: StepType) -> StepType`
- `add_string_step() -> StringValueStep`
- `assign_parent() -> Any`
- `count_steps(recursive: bool) -> int`
- `find_all_steps(name: Any, step_type: Any, recursive: bool) -> List[...]`
- `find_step(name: str, recursive: bool) -> Optional[...]`
- `get_failed_steps(recursive: bool) -> List[...]`
- `print_hierarchy(indent: int) -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.step_list`

### `StepList(Unknown)`

_A list that automatically sets parent reference on steps when added._

**Properties:**
- `parent`

**Methods:**
- `append(item: StepT) -> Any`
- `count_by_status() -> dict[...]`
- `extend(items: Iterable[...]) -> Any`
- `find_all_by_name(name: str) -> List[...]`
- `find_by_name(name: str) -> Optional[...]`
- `find_failed() -> List[...]`
- `get_by_status(status: Any) -> List[...]`
- `insert(index: int, item: StepT) -> Any`
- `parent(value: Optional[...]) -> Any`
- `set_parent(parent: Any) -> Any`

---

## `report.report_models.uut.steps.string_step`

### `MultiStringStep(Step)`

_Multi-string test step with multiple measurements._

**Class Variables:**
- `step_type: Literal[...]`
- `measurements: List[...]`

**Methods:**
- `add_measurement() -> MultiStringMeasurement`
- `check_for_duplicates(name: str) -> str`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

### `StringValueStep(Step)`

_String value test step._

**Class Variables:**
- `step_type: Literal[...]`
- `measurement: Optional[...]`

**Properties:**
- `comp`
- `limit`
- `value`

**Methods:**
- `comp(val: Any) -> Any`
- `create(cls, name: str, value: Any) -> Any`
- `limit(val: Any) -> Any`
- `unwrap_measurement(cls, data: Any) -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`
- `value(val: Any) -> Any`
- `wrap_measurement(cls, value: Optional[...]) -> Optional[...]`

---

## `report.report_models.uut.steps.unknown_step`

### `UnknownStep(Step)`

_Fallback step type for steps not recognized by this version._

**Class Variables:**
- `model_config`
- `step_type: str`

**Methods:**
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.uut_info`

### `RefUURs(WATSBase)`

_Repair reports that reference this test report._

**Class Variables:**
- `id: UUID`
- `start: Optional[...]`

---

### `UUTInfo(ReportInfo)`

_Unit Under Test information._

**Class Variables:**
- `fixture_id: Optional[...]`
- `socket_index: Optional[...]`
- `socket_index_format: Optional[...]`
- `error_code: Optional[...]`
- `error_code_format: Optional[...]`
- `error_message: Optional[...]`
- `batch_number: Optional[...]`
- `batch_fail_count: Optional[...]`
- `batch_fail_count_format: Optional[...]`
- `batch_loop_index: Optional[...]`
- `batch_loop_index_format: Optional[...]`
- `step_id_caused_uut_failure: Optional[...]`
- `referenced_by_uurs: Optional[...]`

---

## `report.report_models.uut.uut_report`

### `UUTReport(Unknown)`

_Complete UUT (Unit Under Test) report._

**Class Variables:**
- `info: Optional[...]`
- `root: SequenceCall`

**Properties:**
- `test_operation_code`

**Methods:**
- `add_sub_unit(part_type: str, sn: str, pn: str, rev: str) -> UUTSubUnit`
- `get_root_sequence_call() -> SequenceCall`
- `test_operation_code(value: int) -> Any`

---

### `UUTSubUnit(SubUnit)`

_UUT Sub-unit with its own test steps._

**Class Variables:**
- `root: Optional[...]`

---

## `report.report_models.wats_base`

### `DeserializationContext`

_Context for injecting default values during deserialization._

---

### `WATSBase(BaseModel)`

_Base class for all WATS Report Models._

**Class Variables:**
- `model_config`

**Methods:**
- `inject_defaults(cls, data: Any, info: ValidationInfo) -> Any`

---


---

<a name="rootcause-domain"></a>

# RootCause Domain

_Source: [domain_rootcause.md](domain_rootcause.md)_


## `rootcause.async_repository`

### `AsyncRootCauseRepository`

_Async RootCause (Ticketing) data access layer._

---

## `rootcause.async_service`

### `AsyncRootCauseService`

_Async RootCause (Ticketing) business logic layer._

---

## `rootcause.enums`

### `TicketPriority(IntEnum)`

_Ticket priority levels_

**Class Variables:**
- `LOW`
- `MEDIUM`
- `HIGH`

---

### `TicketStatus(IntFlag)`

_Ticket status flags._

**Class Variables:**
- `OPEN`
- `IN_PROGRESS`
- `ON_HOLD`
- `SOLVED`
- `CLOSED`
- `ARCHIVED`

---

### `TicketUpdateType(IntEnum)`

_Type of ticket update/history entry_

**Class Variables:**
- `CONTENT`
- `PROGRESS`
- `PROPERTIES`
- `NOTIFICATION`

---

### `TicketView(IntEnum)`

_Ticket view filter for listing tickets_

**Class Variables:**
- `ASSIGNED`
- `FOLLOWING`
- `ALL`

---

## `rootcause.models`

### `Ticket(PyWATSModel)`

_Represents a RootCause ticket in WATS._

**Class Variables:**
- `ticket_id: Optional[...]`
- `ticket_number: Optional[...]`
- `progress: Optional[...]`
- `owner: Optional[...]`
- `assignee: Optional[...]`
- `subject: Optional[...]`
- `status: Optional[...]`
- `priority: Optional[...]`
- `report_uuid: Optional[...]`
- `created_utc: Optional[...]`
- `updated_utc: Optional[...]`
- `team: Optional[...]`
- `origin: Optional[...]`
- `tags: Optional[...]`
- `history: Optional[...]`
- `update: Optional[...]`

---

### `TicketAttachment(PyWATSModel)`

_Represents an attachment in a RootCause ticket._

**Class Variables:**
- `attachment_id: Optional[...]`
- `filename: Optional[...]`

---

### `TicketUpdate(PyWATSModel)`

_Represents an update/history entry in a RootCause ticket._

**Class Variables:**
- `update_id: Optional[...]`
- `update_utc: Optional[...]`
- `update_user: Optional[...]`
- `content: Optional[...]`
- `update_type: Optional[...]`
- `attachments: Optional[...]`

---


---

<a name="scim-domain"></a>

# SCIM Domain

_Source: [domain_scim.md](domain_scim.md)_


## `scim.async_repository`

### `AsyncScimRepository`

_Async repository for SCIM API operations._

---

## `scim.async_service`

### `AsyncScimService`

_Async service for SCIM user provisioning operations._

---

## `scim.models`

### `ScimListResponse(PyWATSModel)`

_Represents a SCIM list response._

**Class Variables:**
- `total_results: Optional[...]`
- `items_per_page: Optional[...]`
- `start_index: Optional[...]`
- `resources: Optional[...]`
- `schemas: Optional[...]`
- `model_config`

---

### `ScimPatchOperation(PyWATSModel)`

_Represents a single SCIM patch operation._

**Class Variables:**
- `op: Optional[...]`
- `path: Optional[...]`
- `value: Optional[...]`

---

### `ScimPatchRequest(PyWATSModel)`

_Represents a SCIM patch request body._

**Class Variables:**
- `schemas: Optional[...]`
- `operations: Optional[...]`

---

### `ScimToken(PyWATSModel)`

_Represents a SCIM JWT token response._

**Class Variables:**
- `token: Optional[...]`
- `expires_utc: Optional[...]`
- `duration_days: Optional[...]`
- `model_config`

---

### `ScimUser(PyWATSModel)`

_Represents a SCIM user resource._

**Class Variables:**
- `id: Optional[...]`
- `user_name: Optional[...]`
- `display_name: Optional[...]`
- `active: Optional[...]`
- `external_id: Optional[...]`
- `name: Optional[...]`
- `emails: Optional[...]`
- `schemas: Optional[...]`
- `meta: Optional[...]`
- `model_config`

---

### `ScimUserEmail(PyWATSModel)`

_SCIM user email entry._

**Class Variables:**
- `value: Optional[...]`
- `type: Optional[...]`
- `primary: Optional[...]`

---

### `ScimUserName(PyWATSModel)`

_SCIM user name components._

**Class Variables:**
- `formatted: Optional[...]`
- `given_name: Optional[...]`
- `family_name: Optional[...]`

---


---

<a name="software-domain"></a>

# Software Domain

_Source: [domain_software.md](domain_software.md)_


## `software.async_repository`

### `AsyncSoftwareRepository`

_Async Software distribution data access layer._

---

## `software.async_service`

### `AsyncSoftwareService`

_Async Software distribution business logic layer._

---

## `software.enums`

### `PackageStatus(str, Enum)`

_Software package status_

**Class Variables:**
- `DRAFT`
- `PENDING`
- `RELEASED`
- `REVOKED`

---

## `software.models`

### `Package(PyWATSModel)`

_Represents a software distribution package._

**Class Variables:**
- `package_id: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`
- `version: Optional[...]`
- `status: Optional[...]`
- `install_on_root: Optional[...]`
- `root_directory: Optional[...]`
- `priority: Optional[...]`
- `tags: Optional[...]`
- `created_utc: Optional[...]`
- `modified_utc: Optional[...]`
- `created_by: Optional[...]`
- `modified_by: Optional[...]`
- `files: Optional[...]`

---

### `PackageFile(PyWATSModel)`

_Represents a file within a software package._

**Class Variables:**
- `file_id: Optional[...]`
- `filename: Optional[...]`
- `path: Optional[...]`
- `size: Optional[...]`
- `checksum: Optional[...]`
- `created_utc: Optional[...]`
- `modified_utc: Optional[...]`
- `attributes: Optional[...]`

---

### `PackageTag(PyWATSModel)`

_Represents a tag/metadata on a software package._

**Class Variables:**
- `key: Optional[...]`
- `value: Optional[...]`

---

### `VirtualFolder(PyWATSModel)`

_Represents a virtual folder in Production Manager._

**Class Variables:**
- `folder_id: Optional[...]`
- `name: Optional[...]`
- `path: Optional[...]`
- `description: Optional[...]`

---


---


## Related Documentation

- [Individual Component References](README.md) - Separate files per component
- [API Documentation](../README.md) - Sphinx-generated API docs
- [Architecture Analysis](../../projects/active/api-client-ui-communication-analysis.project/README.md)
- [Developer Guides](../../guides/)
- [Examples](../../examples/)

---

**Last Updated:** February 8, 2026
**Maintainer:** Auto-generated by CI/development workflow