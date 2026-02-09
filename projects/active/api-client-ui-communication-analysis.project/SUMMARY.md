# API-Client-UI Communication Analysis - Summary

**Date:** February 8, 2026  
**Analysis Type:** Comprehensive Architecture Review  
**Scope:** Cross-layer communication patterns, event systems, logging, and exception handling

---

## Executive Summary

This analysis documents the complete communication architecture of the pyWATS system, covering three distinct layers (API, Client, UI) and their interaction patterns. The system implements a clean separation of concerns with well-defined boundaries and multiple communication mechanisms.

### Key Findings

1. **Two Independent Event Systems** - Qt-based application events (Client ↔ UI) and protocol-agnostic events (external sources → handlers)
2. **Hierarchical Logging** - Unified logging infrastructure across all layers with consistent patterns
3. **Clear Exception Propagation** - Exceptions flow from API → Client → UI with appropriate handling at each layer
4. **Clean Layer Separation** - Each layer has distinct responsibilities with minimal coupling

---

## Architecture Overview

### Three-Layer Design

```
UI Layer (pywats_ui)        ← User Interface, Qt GUI applications
    ↕ Qt Signals, IPC
Client Layer (pywats_client) ← Background service, queue management
    ↕ Function calls, HTTP
API Layer (pywats)          ← Synchronous API wrapper, domain services
    ↕ HTTP REST
WATS Server                 ← Test data management server
```

**Design Principles:**
- **Unidirectional dependencies:** UI → Client → API → Server
- **Event-driven communication:** Loose coupling via event buses
- **Async-first implementation:** Async core with sync wrappers for ergonomics
- **Layer independence:** Each layer can function standalone

---

## Event Systems

### 1. Application EventBus (pywats_client.core.event_bus)

**Purpose:** Real-time communication between Client Service and GUI applications

**Technology:** Qt Signals (thread-safe, cross-process)

**Singleton Pattern:** Single instance shared across all GUI components

**Event Types (`AppEvent` enum):**
- Connection events: `CONNECTION_CHANGED`, `CONNECTIONERROR`
- Lifecycle events: `APP_STARTING`, `APP_STARTED`, `APP_STOPPING`
- API events: `API_CLIENT_READY`, `API_CLIENT_DISCONNECTED`
- Data events: `ASSETS_CHANGED`, `PRODUCTS_CHANGED`, `PROCESSES_REFRESHED`
- Queue events: `QUEUE_ITEM_ADDED`, `QUEUE_ITEM_PROCESSED`, `QUEUE_STATUS_CHANGED`
- Config events: `CONFIG_CHANGED`, `CONFIG_SAVED`

**Communication Pattern:**
```python
# Publisher (Client Service)
event_bus.publish(AppEvent.API_CLIENT_READY, client=api_instance)

# Subscriber (GUI Page)
def _on_api_ready(self, data: dict):
    self.api_client = data.get('client')
    self.enable_api_features()

event_bus.subscribe(AppEvent.API_CLIENT_READY, self._on_api_ready)
```

**Key Features:**
- Thread-safe (Qt's signal/slot mechanism)
- Type-safe signals for common events
- Automatic cleanup on page destruction
- Support for typed signals and generic signals

### 2. Protocol EventBus (pywats_events.bus.EventBus)

**Purpose:** Protocol-agnostic event infrastructure for external message sources

**Technology:** Python threading/async with manual synchronization

**Instantiation:** User creates instances as needed (not singleton)

**Event Types (`EventType` enum):**
- `TEST_RESULT` - Test execution complete
- `UNIT_STATUS_CHANGED` - Unit lifecycle updates
- `STATION_STATUS` - Station status changes
- `RESOURCE_UPDATED` - Resource modifications

**Communication Pattern:**
```python
# Create handler
class TestResultHandler(BaseHandler):
    @property
    def event_types(self):
        return [EventType.TEST_RESULT]
    
    async def handle(self, event: Event):
        # Process test result
        await store_result(event.payload)

# Wire up
bus = EventBus()
bus.register_handler(TestResultHandler())
bus.register_transport(CFXTransport())
bus.start()
```

**Key Features:**
- Transport adapters (IPC-CFX, MQTT, WebHooks)
- Handler registry with routing
- Retry and error policies
- Both sync and async variants

### Event System Comparison

| Feature | Application EventBus | Protocol EventBus |
|---------|---------------------|-------------------|
| **Purpose** | GUI ↔ Service communication | External integration |
| **Technology** | Qt Signals | Python threading |
| **Pattern** | Singleton | Instantiated |
| **Use Cases** | UI updates, config changes | IPC-CFX, MQTT, webhooks |
| **Thread Safety** | Yes (Qt) | Yes (manual) |
| **Async Support** | Via QMetaObject | Native async/await |

### Integration Point

Protocol events can trigger application events:
```python
class MyDomainHandler(BaseHandler):
    async def handle(self, protocol_event):
        # Process domain logic
        result = await process_test(protocol_event)
        
        # Notify GUI
        from pywats_client.core.event_bus import event_bus
        event_bus.publish(AppEvent.DATA_CHANGED)
```

---

## Logging Infrastructure

### Unified Logging Pattern

All layers use the same initialization:
```python
from pywats.core.logging import get_logger
logger = get_logger(__name__)  # Creates logger with module name
```

**Result:** Clean hierarchy based on package structure:
```
root
├── pywats
│   ├── pywats.domains.report
│   ├── pywats.domains.product
│   ├── pywats.core.async_client
│   └── pywats.core.cache
├── pywats_client
│   ├── pywats_client.service.client_service
│   ├── pywats_client.core.queue_manager
│   └── pywats_client.core.event_bus
├── pywats_ui
│   ├── pywats_ui.framework.base_page
│   └── pywats_ui.apps.configurator.*
└── pywats_events
    ├── pywats_events.bus.event_bus
    └── pywats_events.handlers.*
```

### Log Destinations

| Layer | Default Destination | Configuration |
|-------|-------------------|---------------|
| **API** | Console (stdout) | User configures |
| **Client Service** | `{install_dir}/pywats.log` | `setup_client_logging()` |
| **Converters** | `{install_dir}/conversion_logs/*.log` | `ConversionLog` class |
| **GUI** | Console + Service log | Inherits from API |

### Logging Configuration

**Client Service (Production):**
```python
from pywats_client.core.logging import setup_client_logging

setup_client_logging(
    instance_id="default",
    log_level="INFO",
    log_format="json",  # or "text"
    enable_console=True,
    rotate_size_mb=10,
    rotate_backups=5
)
```

**Features:**
- Rotating file handlers (configurable size and backup count)
- JSON format support for structured logging
- Correlation ID tracking
- Context injection (instance_id, user_id, etc.)

### Correlation IDs

**Flow:**
1. API generates UUID correlation ID per request
2. Stored in `contextvars.ContextVar` (thread-local)
3. Automatically added to all log messages
4. Included in HTTP request headers (`X-Correlation-ID`)
5. Returned in response headers
6. Used in error messages for end-to-end tracking

**Benefits:**
- Trace requests across all layers
- Group related log messages
- Debug distributed issues
- Support tickets include correlation ID

---

## Exception Propagation

### Exception Hierarchy

**API Layer (`pywats.core.exceptions`):**
```
PyWATSError (base)
├── AuthenticationError (401)
├── AuthorizationError (403)
├── ValidationError (400)
├── NotFoundError (404)
├── ConflictError (409)
├── ServerError (500)
├── ConnectionError (network)
├── TimeoutError (timeout)
└── WatsApiError (API-specific)
    ├── EmptyResponseError
    └── InvalidResponseError
```

**Client Layer (`pywats_client.exceptions`):**
```
ClientError (base)
├── ConfigurationError
├── ServiceError
├── QueueCriticalError (⚠️ critical)
└── ConverterError
```

### Exception Handling Strategy by Layer

#### API Layer
- **Strategy:** Raise exceptions with detailed context
- **Logging:** Log at detection point with `exc_info=True`
- **Propagation:** Re-raise to caller
- **User Impact:** None (handled by upper layers)

**Example:**
```python
# API Layer
try:
    response = await self._client.get(f"/product/{product_id}")
except HTTPError as e:
    if e.status == 404:
        logger.error(f"Product not found: {product_id}", exc_info=True)
        raise NotFoundError(f"Product {product_id} not found")
    raise
```

#### Client Layer
- **Strategy:** Catch, log, potentially broadcast via events
- **Logging:** Comprehensive logging with correlation IDs
- **Propagation:** Re-raise or convert to ClientError
- **User Impact:** Events trigger UI notifications

**Example:**
```python
# Client Service
try:
    await self._queue.enqueue(report)
except QueueCriticalError as e:
    logger.critical(
        "Queue critical error - data loss risk",
        exc_info=True,
        extra={
            'primary_error': e.primary_error,
            'fallback_error': e.fallback_error
        }
    )
    event_bus.publish(AppEvent.APP_ERROR, error=str(e))
```

#### UI Layer
- **Strategy:** Catch all exceptions, show appropriate dialog
- **Logging:** Log user-facing errors
- **Propagation:** Terminal (no re-raise)
- **User Impact:** Direct (QMessageBox dialogs with user-friendly messages)

**Example:**
```python
# UI Page
try:
    result = await api.product.get(product_id)
    self.display_product(result)
except NotFoundError as e:
    self.handle_error(e, "loading product")
    # Shows: "The requested item was not found while loading product"
except Exception as e:
    self.handle_error(e, "loading product")
    # Generic error dialog + logged
```

### ErrorHandlingMixin

Centralized error handling for all GUI pages:

```python
class ErrorHandlingMixin:
    def handle_error(self, error: Exception, context: str = ""):
        """Show appropriate dialog based on exception type"""
        
        if isinstance(error, AuthenticationError):
            QMessageBox.warning(self, "Auth Error", "Session expired")
        elif isinstance(error, ValidationError):
            QMessageBox.warning(self, "Invalid Input", str(error))
        elif isinstance(error, NotFoundError):
            QMessageBox.information(self, "Not Found", f"Item not found while {context}")
        elif isinstance(error, ConnectionError):
            QMessageBox.warning(self, "Connection Error", "Check network")
        elif isinstance(error, QueueCriticalError):
            QMessageBox.critical(self, "CRITICAL", "Data loss risk! Check disk space!")
        else:
            logger.exception(f"Unexpected error while {context}")
            QMessageBox.critical(self, "Error", str(error))
```

**Benefits:**
- Consistent error presentation
- User-friendly messages
- Appropriate severity levels
- Comprehensive logging

---

## Communication Patterns

### 1. Synchronous API Calls (UI → Client → API → Server)

**Pattern:** Direct function calls with blocking behavior

**Flow:**
```
User Action → UI Page → pyWATS API → AsyncHttpClient → WATS Server
           ←           ←            ←                ←
```

**Implementation:**
```python
# UI Page (BasePage)
def _on_load_button_click(self):
    self.run_async(
        self._load_product(),
        name="load_product",
        on_complete=self._on_product_loaded
    )

async def _load_product(self):
    # Calls API (blocks worker thread, not UI thread)
    product = await self.api.product.get(self.product_id)
    return product

def _on_product_loaded(self, result: TaskResult):
    if result.success:
        self.display_product(result.data)
    else:
        self.handle_error(result.error, "loading product")
```

**Key Features:**
- Non-blocking UI (AsyncTaskRunner uses QThreadPool)
- Progress indicators (loading spinner)
- Error handling at UI layer
- Type-safe result objects

### 2. Asynchronous Event Broadcasts (Client → UI)

**Pattern:** Publish/Subscribe via Qt Signals

**Flow:**
```
Client Service → Event Bus → GUI Pages (subscribers)
(publisher)      (Qt Signal)  (callbacks)
```

**Implementation:**
```python
# Client Service (publisher)
async def _on_queue_status_changed(self):
    status = await self._queue.get_status()
    event_bus.publish(
        AppEvent.QUEUE_STATUS_CHANGED,
        pending=status.pending_count,
        failed=status.failed_count
    )

# GUI Page (subscriber)
def __init__(self, config, parent):
    super().__init__(config, parent)
    self.subscribe_event(AppEvent.QUEUE_STATUS_CHANGED, self._update_queue_display)

def _update_queue_display(self, data: dict):
    pending = data.get('pending', 0)
    failed = data.get('failed', 0)
    self.queue_label.setText(f"Queue: {pending} pending, {failed} failed")
```

**Key Features:**
- Loose coupling (pages don't know about service)
- Thread-safe (Qt Signals)
- Automatic cleanup on page destruction
- Multiple subscribers per event

### 3. Inter-Process Communication (GUI ↔ Service)

**Pattern:** Named pipes (Windows) / Unix sockets (Linux/Mac)

**Flow:**
```
GUI Process → IPC Client → Named Pipe → IPC Server → Client Service
           ←             ←            ←            ←
```

**Implementation:**
```python
# GUI Application
from pywats_client.service.ipc_client import IPCClient

ipc = IPCClient(instance_id="default")
await ipc.connect()

# Get service status
status = await ipc.get_status()
print(f"Service running: {status['running']}")

# Call service method
result = await ipc.call_method("process_report", report_path="/path/to/report.txt")
```

**Key Features:**
- Cross-process communication
- Async/await support
- Service discovery (auto-find running instance)
- Fallback to degraded mode if service unavailable

### 4. Protocol Event Integration (External → pywats_events → Handlers)

**Pattern:** Transport → EventBus → Handlers

**Flow:**
```
IPC-CFX Device → CFX Transport → Protocol EventBus → Domain Handlers
(message)        (parse)         (route)             (process)
```

**Implementation:**
```python
# Transport (adapts protocol to events)
class CFXTransport(BaseTransport):
    def on_message(self, cfx_message):
        event = Event.create(
            EventType.TEST_RESULT,
            payload=self.parse_cfx(cfx_message)
        )
        self.publish_event(event)

# Handler (processes events)
class TestResultHandler(BaseHandler):
    @property
    def event_types(self):
        return [EventType.TEST_RESULT]
    
    async def handle(self, event: Event):
        # Store in database
        await self.store_test_result(event.payload)
        
        # Optionally trigger app event
        from pywats_client.core.event_bus import event_bus
        event_bus.publish(AppEvent.DATA_CHANGED)
```

**Key Features:**
- Protocol-agnostic design
- Multiple transport support (CFX, MQTT, WebHooks)
- Handler routing by event type
- Optional integration with application events

---

## Component Ownership and Responsibilities

### Component Matrix

| Component | Owner | Lifecycle Managed By | Primary Purpose |
|-----------|-------|---------------------|-----------------|
| **pyWATS API** | API User (script/app) | User's script/app | WATS server communication |
| **AsyncHttpClient** | pyWATS | pyWATS.__init__ | HTTP communication |
| **Domain Services** | pyWATS | pyWATS.__init__ | Domain-specific APIs |
| **ApplicationEventBus** | Singleton | First access | GUI ↔ Service events |
| **ClientService** | Service Manager | OS service manager | Background processing |
| **QueueManager** | ClientService | ClientService | Report queue management |
| **ConfigManager** | ClientService/GUI | Caller | Configuration persistence |
| **BasePage** | QMainWindow | Qt parent-child | UI page base class |
| **ErrorHandlingMixin** | Page (mixin) | Page lifecycle | Error dialog handling |
| **AsyncTaskRunner** | BasePage | BasePage | Non-blocking async ops |
| **ProtocolEventBus** | User/App | User's script | Protocol integration |

### Dependency Rules

1. **UI depends on Client:** UI imports from `pywats_client` but not vice versa
2. **Client depends on API:** Client imports from `pywats` but not vice versa
3. **API depends on Server:** API communicates with WATS server via HTTP
4. **Events are independent:** `pywats_events` can be used standalone

**Circular Dependencies:** None (clean unidirectional)

---

## Key Insights

### ✅ Strengths

1. **Clean Layer Separation** - Each layer has distinct responsibilities
2. **Flexible Event Systems** - Two specialized systems for different use cases
3. **Unified Logging** - Consistent patterns across all layers
4. **Type-Safe Exceptions** - Clear exception hierarchy with detailed context
5. **Async-First Design** - Performance and scalability built-in
6. **IPC Support** - GUI and service can run in separate processes
7. **Protocol Agnostic** - Easy to add new message sources (CFX, MQTT, etc.)

### ⚠️ Potential Confusion Points

1. **Two Event Systems** - Developers must understand when to use each
   - **Solution:** Clear documentation (this analysis!)
   - **Rule:** Use ApplicationEventBus for GUI/Service, ProtocolEventBus for external integration

2. **Sync vs. Async** - Mix of sync wrappers and async core
   - **Solution:** Sync wrappers provide ergonomic API, async core provides performance
   - **Rule:** GUI uses sync API via async runners, services use async directly

3. **Exception Hierarchy Split** - Some in `pywats`, some in `pywats_client`
   - **Solution:** Layer-specific exceptions (API errors vs. Client errors)
   - **Rule:** API exceptions for server communication, Client exceptions for local operations

### 🎯 Recommendations

1. **Document Event System Boundaries**
   - Add section to developer docs explaining both systems
   - Create decision tree for "which event system should I use?"

2. **Centralize Correlation ID Management**
   - Consider extracting correlation ID logic to shared utility
   - Add correlation IDs to application events for end-to-end tracing

3. **Standardize IPC Error Handling**
   - Document fallback behavior when service unavailable
   - Add reconnection logic for transient IPC failures

4. **Create Architecture Diagram Poster**
   - Use Mermaid diagrams in this analysis
   - Create visual reference for new developers

5. **Add Integration Examples**
   - Show how protocol events can trigger application events
   - Document common patterns for cross-system communication

---

## Quick Reference

### Event System Decision Tree

```
Need to communicate?
│
├─ Between GUI and Background Service?
│  └─ Use ApplicationEventBus (pywats_client.core.event_bus)
│
├─ Between external message source and your code?
│  └─ Use Protocol EventBus (pywats_events)
│
└─ Within same module/class?
   └─ Use direct function calls
```

### Logging Quick Start

```python
# All layers
from pywats.core.logging import get_logger
logger = get_logger(__name__)

# Use it
logger.info("Operation started")
logger.error("Operation failed", exc_info=True)  # Include stack trace
logger.warning("Deprecated API", extra={'correlation_id': 'abc123'})
```

### Exception Handling Quick Start

**API/Client Layer:**
```python
try:
    result = await operation()
except SpecificError as e:
    logger.error("Operation failed", exc_info=True)
    raise  # Re-raise to caller
```

**UI Layer:**
```python
try:
    result = await operation()
except Exception as e:
    self.handle_error(e, "performing operation")  # ErrorHandlingMixin
```

### Async Operation Quick Start

**UI Page:**
```python
def _on_button_click(self):
    self.run_async(
        self._do_async_work(),
        name="my_operation",
        on_complete=self._on_complete,
        on_error=self._on_error
    )

async def _do_async_work(self):
    return await api.product.list()

def _on_complete(self, result: TaskResult):
    products = result.data
    self.update_table(products)
```

---

## Related Documentation

- [Exception Handling Guide](../../../docs/guides/exception-handling.md)
- [Client Service Documentation](../../../src/pywats_client/service/README.md)
- [Event System Documentation](../../../src/pywats_events/__init__.py)
- [GUI Framework Documentation](../../../src/pywats_ui/framework/__init__.py)
- [Architecture Analysis (Detailed)](ARCHITECTURE_ANALYSIS.md)
- [Flow Charts](FLOW_CHARTS.md)
- [Component Diagrams](COMPONENT_DIAGRAMS.md)

---

**Last Updated:** February 8, 2026  
**Analysis Completed By:** GitHub Copilot (Claude Sonnet 4.5)  
**Total Documentation:** 4 files, 2000+ lines, 11 Mermaid diagrams
