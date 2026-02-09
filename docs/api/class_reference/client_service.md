# pywats_client.service - Class Reference

Auto-generated class reference for `pywats_client.service`.

---

## `service.async_client_service`

### `AsyncClientService`

_Async-first WATS Client Service Controller._

**Class Variables:**
- `WATCHDOG_INTERVAL`
- `PING_INTERVAL`
- `REGISTER_INTERVAL`

**Properties:**
- `api_status`
- `is_running`
- `stats`
- `status`

**Methods:**
- `get_credentials() -> Optional[...]`
- `get_service_status() -> Dict[...]`
- `get_status() -> Dict[...]`
- `request_shutdown() -> Any`

---

### `AsyncServiceStatus(Enum)`

_Service status states_

**Class Variables:**
- `STOPPED`
- `START_PENDING`
- `RUNNING`
- `STOP_PENDING`
- `PAUSED`
- `ERROR`

---

## `service.async_converter_pool`

### `AsyncConversionItem`

_Represents a file to be converted asynchronously._

**Properties:**
- `processing_time`

---

### `AsyncConversionItemState(Enum)`

_State of an async conversion item_

**Class Variables:**
- `PENDING`
- `PROCESSING`
- `COMPLETED`
- `ERROR`
- `CANCELLED`

---

### `AsyncConverterPool`

_Async converter pool using asyncio.Queue and semaphore-limited workers._

**Properties:**
- `is_running`
- `stats`

---

### `_FileEventHandler(FileSystemEventHandler)`

_Watchdog event handler for file system changes._

**Methods:**
- `on_created(event) -> Any`
- `on_moved(event) -> Any`

---

## `service.async_ipc_client`

### `AsyncIPCClient`

_Pure asyncio IPC client for GUI<->service communication._

**Properties:**
- `connected`
- `server_capabilities`
- `server_version`

---

### `InstanceInfo`

_Information about a discovered service instance_

**Class Variables:**
- `instance_id: str`
- `socket_name: str`
- `connected: bool`
- `status: Optional[...]`

---

### `ServiceDiscoveryAsync`

_Async service discovery helper._

**Methods:**
- `add_callback(callback: callable) -> Any`
- `get_discovered() -> List[...]`
- `remove_callback(callback: callable) -> Any`

---

### `ServiceStatus`

_Service status data from IPC_

**Class Variables:**
- `status: str`
- `api_status: str`
- `pending_count: int`
- `processing_count: int`
- `completed_count: int`
- `failed_count: int`
- `converter_active: int`
- `converter_pending: int`
- `uptime_seconds: float`
- `extra: Dict[...]`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`

---

## `service.async_ipc_server`

### `AsyncIPCServer`

_Pure asyncio IPC server for service<->GUI communication._

**Class Variables:**
- `CONNECTION_TIMEOUT`
- `READ_TIMEOUT`
- `WRITE_TIMEOUT`
- `REQUEST_TIMEOUT`

---

## `service.async_pending_queue`

### `AsyncPendingQueue`

_Async pending report queue with concurrent uploads._

**Class Variables:**
- `FILTER_QUEUED`
- `FILTER_PROCESSING`
- `FILTER_ERROR`
- `PROCESSING_TIMEOUT`
- `ERROR_RETRY_DELAY`
- `PERIODIC_CHECK_INTERVAL`
- `DEFAULT_MAX_QUEUE_SIZE`

**Properties:**
- `is_queue_full`
- `is_running`
- `queue_size`
- `stats`

**Methods:**
- `can_accept_report() -> tuple[...]`

---

### `AsyncPendingQueueState(Enum)`

_State of the pending queue_

**Class Variables:**
- `CREATED`
- `RUNNING`
- `STOPPING`
- `STOPPED`
- `PAUSED`

---

### `_QueueFileHandler(FileSystemEventHandler)`

_Watchdog event handler for queue directory._

**Methods:**
- `on_created(event) -> Any`
- `on_moved(event) -> Any`

---

## `service.client_service`

### `ClientService`

_Synchronous wrapper around AsyncClientService._

**Properties:**
- `api`
- `api_status`
- `config`
- `converter_pool`
- `instance_id`
- `pending_queue`
- `stats`
- `status`

**Methods:**
- `get_status_dict() -> Dict[...]`
- `start() -> Any`
- `stop() -> Any`

---

### `ServiceStatus(Enum)`

_Service status states_

**Class Variables:**
- `STOPPED`
- `START_PENDING`
- `RUNNING`
- `STOP_PENDING`
- `PAUSED`
- `ERROR`

---

## `service.health_server`

### `HealthHTTPServer(HTTPServer)`

_HTTPServer subclass that passes health_server reference to handlers_

**Methods:**
- `finish_request(request, client_address)`

---

### `HealthRequestHandler(BaseHTTPRequestHandler)`

_HTTP request handler for health endpoints_

**Class Variables:**
- `health_server: Optional[...]`

**Methods:**
- `do_GET() -> Any`
- `log_message(format: str) -> Any`

---

### `HealthServer`

_Lightweight HTTP server for health checks._

**Class Variables:**
- `DEFAULT_PORT`

**Properties:**
- `is_running`

**Methods:**
- `set_health_check(check_func: Callable[...]) -> Any`
- `set_service_reference(service: Any) -> Any`
- `start() -> bool`
- `stop() -> Any`

---

### `HealthStatus`

_Health check result container_

**Methods:**
- `to_dict() -> Dict[...]`
- `to_json() -> str`

---

## `service.ipc_protocol`

### `ConnectMessage`

_Client connect message_

**Class Variables:**
- `protocol_version: str`
- `client_version: str`
- `client_type: str`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `HelloMessage`

_Server hello message sent on connection._

**Class Variables:**
- `protocol_version: str`
- `server_version: str`
- `instance_id: str`
- `requires_auth: bool`
- `capabilities: List[...]`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `to_dict() -> Dict[...]`

---

### `IPCMessage`

_Base IPC message structure_

**Class Variables:**
- `command: str`
- `request_id: str`
- `protocol_version: str`
- `args: Dict[...]`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `from_json(cls, data: str) -> Any`
- `to_dict() -> Dict[...]`
- `to_json() -> str`

---

### `IPCResponse`

_IPC response structure_

**Class Variables:**
- `success: bool`
- `data: Optional[...]`
- `error: Optional[...]`
- `request_id: str`
- `protocol_version: str`

**Methods:**
- `error_response(cls, error: str, request_id: str) -> Any`
- `from_dict(cls, data: Dict[...]) -> Any`
- `success_response(cls, data: Any, request_id: str) -> Any`
- `to_dict() -> Dict[...]`
- `to_json() -> str`

---

### `MessageType(str, Enum)`

_IPC message types_

**Class Variables:**
- `HELLO`
- `CONNECT`
- `DISCONNECT`
- `AUTH`
- `AUTH_RESPONSE`
- `PING`
- `GET_STATUS`
- `GET_CONFIG`
- `SET_CONFIG`
- `GET_QUEUE`
- `CLEAR_QUEUE`
- `GET_CONVERTERS`
- `START_CONVERTER`
- `STOP_CONVERTER`
- `START_SERVICE`
- `STOP_SERVICE`
- `RESTART_SERVICE`
- `SYNC_NOW`
- `ERROR`

---

### `ServerCapability(str, Enum)`

_Server capability flags advertised in hello message_

**Class Variables:**
- `AUTH`
- `RATE_LIMIT`
- `CONVERTERS`
- `QUEUE`
- `CONFIG`
- `SYNC`
- `SANDBOX`

---

### `VersionMismatchError(Exception)`

_Raised when protocol versions are incompatible_

**Class Variables:**
- `client_version: str`
- `server_version: str`
- `message: str`

---
