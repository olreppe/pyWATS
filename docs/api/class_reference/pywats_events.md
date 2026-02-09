# pywats_events - Class Reference

Auto-generated class reference for `pywats_events`.

---

## `pywats_events.bus.async_event_bus`

### `AsyncEventBus`

_Asynchronous event bus for high-throughput event processing._

**Properties:**
- `handler_count`
- `is_running`
- `name`
- `queue_size`
- `transport_count`

**Methods:**
- `get_handlers(event_type: Any) -> List[...]`
- `on_error(callback: Callable[...]) -> Any`
- `on_event(callback: Callable[...]) -> Any`
- `register_handler(handler: Any) -> Any`
- `register_transport(transport: Any) -> Any`
- `unregister_handler(handler: Any) -> bool`

---

## `pywats_events.bus.event_bus`

### `EventBus`

_Synchronous event bus for the pyWATS event system._

**Properties:**
- `handler_count`
- `is_running`
- `name`
- `transport_count`

**Methods:**
- `get_handlers(event_type: Any) -> List[...]`
- `on_error(callback: Callable[...]) -> Any`
- `on_event(callback: Callable[...]) -> Any`
- `publish(event: Any) -> Any`
- `publish_async(event: Any) -> Any`
- `register_handler(handler: Any) -> Any`
- `register_transport(transport: Any) -> Any`
- `start() -> Any`
- `stop(timeout: float) -> Any`
- `unregister_handler(handler: Any) -> bool`
- `unregister_transport(transport: Any) -> bool`

---

## `pywats_events.handlers.base_handler`

### `BaseHandler(ABC)`

_Abstract base class for event handlers._

**Properties:**
- `enabled`
- `event_types`
- `name`
- `priority`

**Methods:**
- `can_handle(event: Any) -> bool`
- `enabled(value: bool) -> Any`

---

### `FilteringHandler(BaseHandler)`

_Handler with built-in event filtering capabilities._

**Methods:**
- `add_filter(filter_func: callable) -> Any`
- `can_handle(event: Any) -> bool`

---

### `SyncHandler(BaseHandler)`

_Base class for synchronous handlers._

**Methods:**
- `handle_sync(event: Any) -> Optional[...]`

---

## `pywats_events.handlers.handler_chain`

### `ChainMiddleware`

_Base class for chain middleware._

---

### `EnrichmentMiddleware(ChainMiddleware)`

_Middleware that enriches events with additional data._

---

### `HandlerChain`

_Middleware chain for event processing._

**Methods:**
- `add(middleware: Any) -> Any`
- `clear() -> Any`

---

### `LoggingMiddleware(ChainMiddleware)`

_Middleware that logs events passing through._

---

### `ValidationMiddleware(ChainMiddleware)`

_Middleware that validates events before processing._

---

## `pywats_events.handlers.handler_registry`

### `HandlerRegistry`

_Registry for managing event handlers._

**Properties:**
- `handler_count`

**Methods:**
- `clear() -> Any`
- `get_all_handlers() -> List[...]`
- `get_event_types() -> Set[...]`
- `get_handlers(event_type: Any) -> List[...]`
- `get_handlers_for_event(event: Any) -> List[...]`
- `register(handler: Any) -> Any`
- `unregister(handler: Any) -> bool`

---

## `pywats_events.lifecycle.manager`

### `LifecycleManager`

_Manages the lifecycle of event system components._

**Properties:**
- `is_running`
- `state`

**Methods:**
- `add_component(component: any, priority: int) -> Any`
- `add_event_bus(event_bus: Any, priority: int) -> Any`
- `add_transport(transport: Any, priority: int) -> Any`
- `on_error(callback: Callable[...]) -> Any`
- `on_start(callback: Callable[...]) -> Any`
- `on_stop(callback: Callable[...]) -> Any`

---

### `LifecycleState(Enum)`

_Lifecycle states._

**Class Variables:**
- `CREATED`
- `STARTING`
- `RUNNING`
- `STOPPING`
- `STOPPED`
- `ERROR`

---

## `pywats_events.models.domain_events`

### `AssetFaultEvent`

_Normalized asset fault event._

**Class Variables:**
- `asset_id: str`
- `fault_code: str`
- `fault_message: str`
- `severity: SeverityLevel`
- `timestamp: datetime`
- `cleared: bool`
- `cleared_time: Optional[...]`
- `custom_data: Dict[...]`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `AssetState(Enum)`

_Equipment state._

**Class Variables:**
- `ONLINE`
- `OFFLINE`
- `IDLE`
- `BUSY`
- `ERROR`
- `MAINTENANCE`

---

### `AssetStateChangedEvent`

_Normalized asset state change event._

**Class Variables:**
- `asset_id: str`
- `new_state: AssetState`
- `previous_state: Optional[...]`
- `timestamp: datetime`
- `reason: Optional[...]`
- `custom_data: Dict[...]`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `InspectionResultEvent`

_Normalized inspection result event (AOI, visual, X-ray, etc.)._

**Class Variables:**
- `unit_id: str`
- `result: TestResult`
- `part_number: Optional[...]`
- `station_id: Optional[...]`
- `inspection_type: str`
- `start_time: datetime`
- `end_time: Optional[...]`
- `defects: List[...]`
- `images: List[...]`
- `custom_data: Dict[...]`

---

### `InstalledComponent`

_A component installed on a unit._

**Class Variables:**
- `reference_designator: str`
- `part_number: Optional[...]`
- `serial_number: Optional[...]`
- `lot_number: Optional[...]`
- `installed_time: Optional[...]`

---

### `MaintenanceEvent`

_Normalized maintenance event._

**Class Variables:**
- `asset_id: str`
- `maintenance_type: str`
- `description: str`
- `performed_by: Optional[...]`
- `timestamp: datetime`
- `duration_minutes: Optional[...]`
- `parts_replaced: List[...]`
- `custom_data: Dict[...]`

---

### `MaterialInstalledEvent`

_Normalized material installation event._

**Class Variables:**
- `unit_id: str`
- `components: List[...]`
- `station_id: Optional[...]`
- `timestamp: datetime`
- `custom_data: Dict[...]`

**Properties:**
- `component_count`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `SeverityLevel(Enum)`

_Fault severity level._

**Class Variables:**
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

---

### `TestMeasurement`

_A single measurement from a test._

**Class Variables:**
- `name: str`
- `value: Optional[...]`
- `unit: str`
- `status: TestResult`
- `low_limit: Optional[...]`
- `high_limit: Optional[...]`
- `nominal: Optional[...]`
- `comp_op: str`

**Methods:**
- `is_within_limits() -> bool`

---

### `TestResult(Enum)`

_Test result status._

**Class Variables:**
- `PASS`
- `FAIL`
- `ERROR`
- `SKIPPED`
- `ABORTED`

---

### `TestResultEvent`

_Normalized test result event._

**Class Variables:**
- `unit_id: str`
- `result: TestResult`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `station_id: Optional[...]`
- `operator_id: Optional[...]`
- `start_time: datetime`
- `end_time: Optional[...]`
- `steps: List[...]`
- `test_socket: Optional[...]`
- `batch_sn: Optional[...]`
- `fixture_id: Optional[...]`
- `custom_data: Dict[...]`

**Properties:**
- `duration_ms`
- `measurement_count`
- `passed`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `TestStep`

_A test step with optional measurements._

**Class Variables:**
- `name: str`
- `status: TestResult`
- `start_time: Optional[...]`
- `end_time: Optional[...]`
- `measurements: List[...]`
- `message: Optional[...]`
- `step_type: str`

**Properties:**
- `duration_ms`

---

### `UnitDisqualifiedEvent`

_Normalized unit disqualification event._

**Class Variables:**
- `unit_id: str`
- `reason: str`
- `station_id: Optional[...]`
- `disqualification_type: str`
- `timestamp: datetime`
- `custom_data: Dict[...]`

---

### `WorkCompletedEvent`

_Normalized work completed event._

**Class Variables:**
- `unit_id: str`
- `station_id: str`
- `result: Literal[...]`
- `work_order_id: Optional[...]`
- `operator_id: Optional[...]`
- `start_time: Optional[...]`
- `end_time: datetime`
- `custom_data: Dict[...]`

**Properties:**
- `duration_ms`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `WorkOrderEvent`

_Normalized work order event._

**Class Variables:**
- `work_order_id: str`
- `action: Literal[...]`
- `part_number: Optional[...]`
- `quantity: Optional[...]`
- `status: Optional[...]`
- `timestamp: datetime`
- `custom_data: Dict[...]`

---

### `WorkStartedEvent`

_Normalized work started event._

**Class Variables:**
- `unit_id: str`
- `station_id: str`
- `work_order_id: Optional[...]`
- `operator_id: Optional[...]`
- `timestamp: datetime`
- `lane: Optional[...]`
- `custom_data: Dict[...]`

**Methods:**
- `to_dict() -> Dict[...]`

---

## `pywats_events.models.event`

### `Event`

_Core event class for the pyWATS event system._

**Class Variables:**
- `event_type: Any`
- `payload: Dict[...]`
- `metadata: EventMetadata`

**Properties:**
- `event_id`
- `id`
- `source`
- `timestamp`

**Methods:**
- `create(cls, event_type: Any, payload: Dict[...], source: str, correlation_id: Optional[...]) -> Any`
- `derive(event_type: Any, payload: Dict[...], source: Optional[...]) -> Any`
- `from_dict(cls, data: Dict[...]) -> Any`
- `to_dict() -> Dict[...]`
- `with_retry() -> Any`

---

### `EventMetadata`

_Metadata for event tracing, correlation, and debugging._

**Class Variables:**
- `event_id: str`
- `correlation_id: Optional[...]`
- `causation_id: Optional[...]`
- `timestamp: datetime`
- `source: str`
- `source_topic: Optional[...]`
- `retry_count: int`
- `trace_id: Optional[...]`
- `span_id: Optional[...]`
- `custom: Dict[...]`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `increment_retry() -> Any`
- `to_dict() -> Dict[...]`
- `with_causation(causing_event: Any) -> Any`

---

## `pywats_events.models.event_types`

### `EventType(Enum)`

_Enumeration of all event types in the pyWATS event system._

**Class Variables:**
- `TEST_RESULT`
- `TEST_STARTED`
- `INSPECTION_RESULT`
- `INSPECTION_STARTED`
- `ASSET_FAULT`
- `ASSET_MAINTENANCE`
- `ASSET_STATE_CHANGED`
- `ASSET_CALIBRATION`
- `MATERIAL_INSTALLED`
- `MATERIAL_CONSUMED`
- `MATERIAL_REJECTED`
- `WORK_STARTED`
- `WORK_COMPLETED`
- `UNIT_ARRIVED`
- `UNIT_DEPARTED`
- `UNIT_DISQUALIFIED`
- `WORK_ORDER_CREATED`
- `WORK_ORDER_UPDATED`
- `TRANSPORT_CONNECTED`
- `TRANSPORT_DISCONNECTED`
- `TRANSPORT_ERROR`
- `HANDLER_ERROR`
- `EVENT_DEAD_LETTER`
- `CUSTOM`

**Methods:**
- `asset_events(cls) -> list[...]`
- `from_string(cls, value: str) -> Any`
- `material_events(cls) -> list[...]`
- `production_events(cls) -> list[...]`
- `system_events(cls) -> list[...]`
- `test_events(cls) -> list[...]`

---

## `pywats_events.policies.error_policy`

### `CircuitBreaker`

_Circuit breaker for protecting against cascading failures._

**Properties:**
- `is_closed`
- `is_open`
- `state`

**Methods:**
- `can_proceed() -> bool`
- `record_failure() -> Any`
- `record_success() -> Any`
- `reset() -> Any`

---

### `CircuitState(Enum)`

_Circuit breaker states._

**Class Variables:**
- `CLOSED`
- `OPEN`
- `HALF_OPEN`

---

### `DeadLetterEntry`

_Entry in the dead letter queue._

**Class Variables:**
- `event: Any`
- `error: Exception`
- `timestamp: datetime`
- `handler_name: Optional[...]`
- `retry_count: int`

**Methods:**
- `to_dict() -> Dict`

---

### `DeadLetterQueue`

_Dead letter queue for events that failed processing._

**Properties:**
- `is_empty`
- `size`

**Methods:**
- `add(event: Any, error: Exception, handler_name: Optional[...]) -> DeadLetterEntry`
- `clear() -> int`
- `get_entries(limit: Optional[...], event_type: Optional[...]) -> List[...]`
- `peek() -> Optional[...]`
- `pop() -> Optional[...]`

---

### `ErrorPolicy`

_Error handling policy for failed events._

**Properties:**
- `circuit_breaker`
- `dead_letter_queue`

**Methods:**
- `can_process() -> bool`
- `handle_failure(event: Any, error: Exception, handler_name: Optional[...]) -> Any`
- `on_failure(callback: Callable[...]) -> Any`
- `record_success() -> Any`

---

## `pywats_events.policies.retry_policy`

### `ImmediateRetryPolicy(RetryPolicy)`

_Policy that retries immediately without delay._

**Methods:**
- `get_delay(event: Any) -> float`

---

### `NoRetryPolicy(RetryPolicy)`

_Policy that never retries._

**Methods:**
- `should_retry(event: Any, error: Exception) -> bool`

---

### `RetryConfig`

_Configuration for retry behavior._

**Class Variables:**
- `max_retries: int`
- `initial_delay: float`
- `max_delay: float`
- `exponential_base: float`
- `jitter: bool`
- `jitter_factor: float`

---

### `RetryPolicy`

_Retry policy for handling event processing failures._

**Properties:**
- `config`
- `max_retries`

**Methods:**
- `add_predicate(predicate: Callable[...]) -> Any`
- `get_delay(event: Any) -> float`
- `no_retry_on() -> Any`
- `retry_on() -> Any`
- `should_retry(event: Any, error: Exception) -> bool`
- `wait_sync(event: Any) -> Any`

---

## `pywats_events.routing.filter`

### `EventFilter`

_Composable filter for events._

**Methods:**
- `by_source() -> Any`
- `by_type() -> Any`
- `exclude_source() -> Any`
- `exclude_type() -> Any`
- `has_payload_key(key: str) -> Any`
- `matches(event: Any) -> bool`
- `payload_equals(key: str, value: any) -> Any`
- `payload_in(key: str, values: List[...]) -> Any`
- `where(predicate: Callable[...]) -> Any`

---

## `pywats_events.routing.router`

### `EventRouter`

_Router for directing events based on rules._

**Properties:**
- `rule_count`

**Methods:**
- `add_rule(rule: RoutingRule, handler: Any) -> Any`
- `clear() -> Any`
- `get_all_handlers(event: Any) -> List[...]`
- `route(event: Any) -> Optional[...]`
- `set_default_handler(handler: Any) -> Any`

---

### `RoutingRule`

_A rule for routing events._

**Methods:**
- `matches(event: Any) -> bool`

---

## `pywats_events.telemetry.metrics`

### `EventMetrics`

_Metrics collector for event system monitoring._

**Properties:**
- `events_per_second`
- `total_errors`
- `total_events`
- `uptime_seconds`

**Methods:**
- `get_all_stats() -> Dict[...]`
- `get_stats(event_type: str) -> Optional[...]`
- `get_summary() -> Dict`
- `record_end(event: Any, success: bool) -> Any`
- `record_error(event: Any) -> Any`
- `record_start(event: Any) -> Any`
- `reset() -> Any`

---

### `EventStats`

_Statistics for a single event type._

**Class Variables:**
- `event_type: str`
- `count: int`
- `success_count: int`
- `error_count: int`
- `total_latency_ms: float`
- `min_latency_ms: Optional[...]`
- `max_latency_ms: Optional[...]`
- `last_seen: Optional[...]`

**Properties:**
- `avg_latency_ms`
- `success_rate`

**Methods:**
- `record(latency_ms: float, success: bool) -> Any`
- `to_dict() -> Dict`

---

## `pywats_events.telemetry.tracing`

### `EventTracer`

_Event tracer for distributed tracing._

**Methods:**
- `add_exporter(exporter: callable) -> Any`
- `get_current_trace() -> Optional[...]`
- `set_current_trace(context: Optional[...]) -> Any`
- `span(name: str, attributes: Optional[...]) -> Generator[...]`
- `trace(name: str, trace_id: Optional[...]) -> Generator[...]`
- `trace_event(event: Any) -> Generator[...]`

---

### `Span`

_A span in a distributed trace._

**Class Variables:**
- `span_id: str`
- `name: str`
- `trace_id: str`
- `parent_span_id: Optional[...]`
- `start_time: datetime`
- `end_time: Optional[...]`
- `status: str`
- `attributes: Dict[...]`
- `events: List[...]`

**Properties:**
- `duration_ms`

**Methods:**
- `add_event(name: str, attributes: Optional[...]) -> Any`
- `end(status: str) -> Any`
- `set_attribute(key: str, value: Any) -> Any`
- `to_dict() -> Dict`

---

### `TraceContext`

_Context for a distributed trace._

**Properties:**
- `all_spans`
- `current_span`

**Methods:**
- `end_span(status: str) -> Optional[...]`
- `start_span(name: str, attributes: Optional[...]) -> Span`
- `to_dict() -> Dict`

---

## `pywats_events.transports.base_transport`

### `BaseTransport(ABC)`

_Abstract base class for transport adapters._

**Properties:**
- `is_connected`
- `name`
- `state`

**Methods:**
- `get_stats() -> Dict[...]`
- `get_subscribed_topics() -> List[...]`
- `on_connect(callback: Callable[...]) -> Any`
- `on_disconnect(callback: Callable[...]) -> Any`
- `on_error(callback: Callable[...]) -> Any`
- `publish_event(event: Any) -> Any`
- `set_async_event_bus(event_bus: Any) -> Any`
- `set_event_bus(event_bus: Any) -> Any`
- `start() -> Any`
- `stop() -> Any`

---

### `TransportState(Enum)`

_Transport connection states._

**Class Variables:**
- `DISCONNECTED`
- `CONNECTING`
- `CONNECTED`
- `RECONNECTING`
- `ERROR`

---

## `pywats_events.transports.mock_transport`

### `MockTransport(BaseTransport)`

_Mock transport for testing._

**Properties:**
- `event_count`
- `injected_events`
- `published_events`

**Methods:**
- `clear() -> Any`
- `configure_failure(fail_on_start: bool, fail_on_inject: bool) -> Any`
- `get_stats() -> Dict[...]`
- `inject_event(event: Any) -> Any`
- `inject_events(events: List[...]) -> Any`
- `reset() -> Any`
- `set_inject_delay(delay: float) -> Any`
- `simulate_disconnect() -> Any`
- `simulate_error(error: Exception) -> Any`
- `simulate_reconnect() -> Any`
- `start() -> Any`
- `stop() -> Any`

---
