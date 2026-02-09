# pywats.core - Class Reference

Auto-generated class reference for `pywats.core`.

---

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
