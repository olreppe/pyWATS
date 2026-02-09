# Architecture Analysis - API-Client-UI Communication

**Date:** February 8, 2026  
**Version:** 1.0

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Layer Architecture](#layer-architecture)
3. [Event Systems](#event-systems)
4. [Logging Infrastructure](#logging-infrastructure)
5. [Exception Propagation](#exception-propagation)
6. [Component Ownership](#component-ownership)
7. [Communication Patterns](#communication-patterns)

---

## System Overview

### Three-Layer Architecture

pyWATS implements a clean three-layer architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     UI Layer (pywats_ui)                     │
│  - Qt GUI Applications (Configurator, monitors, etc.)       │
│  - BasePage, ErrorHandlingMixin, AsyncTaskRunner            │
│  - Event subscriptions (Qt Signal-based)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │ Qt Signals / IPC
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                 Client Layer (pywats_client)                 │
│  - Background Service (file watcher, queue, API calls)      │
│  - Application EventBus (Qt Signal-based)                   │
│  - Configuration Management                                 │
│  - IPC Server (for GUI communication)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/HTTPS REST API
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (pywats)                        │
│  - Synchronous API Wrapper (pyWATS class)                   │
│  - Async HTTP Client                                        │
│  - Domain Services (Report, Product, Asset, etc.)           │
│  - Core Exceptions, Logging, Configuration                  │
└─────────────────────────────────────────────────────────────┘
                      │ HTTP/HTTPS
                      ↓
              ┌───────────────┐
              │  WATS Server  │
              └───────────────┘
```

### Design Principles

1. **Layer Independence:** Each layer can function independently
2. **Unidirectional Dependencies:** UI → Client → API → Server
3. **Event-Driven Communication:** Loose coupling via event buses
4. **Async-First Implementation:** Async core with sync wrappers
5. **Protocol Agnostic:** pywats_events supports multiple transports

---

## Layer Architecture

### 1. API Layer (pywats)

**Purpose:** Synchronous Python API for WATS server

**Key Components:**
- `pyWATS` - Main API class (sync wrapper)
- `AsyncHttpClient` - Async HTTP client (core)
- Domain services (`SyncServiceWrapper` + async services)
- Exception hierarchy (`PyWATSError`, `AuthenticationError`, etc.)
- Logging infrastructure (`configure_logging`, `get_logger`)
- Configuration (`APISettings`, `SyncConfig`)

**Responsibilities:**
- HTTP communication with WATS server
- Request/response serialization
- Retry logic with exponential backoff
- Response caching
- Exception handling and wrapping
- Correlation ID tracking

**Logging:**
```python
from pywats.core.logging import get_logger
logger = get_logger(__name__)  # Module-level logger
```

**Exception Strategy:**
- Wrap HTTP errors in domain exceptions
- Provide detailed error context
- Re-raise with additional information
- All exceptions inherit from `PyWATSError`

---

### 2. Client Layer (pywats_client)

**Purpose:** Background service for file monitoring, queue management, and API integration

**Key Components:**
- `ClientService` - Main service (sync wrapper)
- `AsyncClientService` - Async service implementation
- `ApplicationEventBus` - Qt Signal-based event bus (SEPARATE from pywats_events)
- `ConfigManager` - Configuration management
- `QueueManager` - Report queue with fallback
- `IPC Server` - Inter-process communication

**Responsibilities:**
- File system monitoring (PendingWatcher)
- Report converter execution
- Queue management with disk fallback
- API client lifecycle
- Configuration persistence
- Event broadcasting to UI
- IPC communication with GUI applications

**Event System:**
```python
from pywats_client.core.event_bus import event_bus, AppEvent

# Publish events
event_bus.publish(AppEvent.API_CLIENT_READY, client=api)
event_bus.publish(AppEvent.QUEUE_STATUS_CHANGED, pending=5, failed=2)

# Subscribe to events
event_bus.subscribe(AppEvent.CONNECTION_CHANGED, self._on_connection)
```

**Logging:**
```python
from pywats_client.core.logging import setup_client_logging
setup_client_logging(instance_id="default", log_level="INFO")
# Creates: {install_dir}/pywats.log with rotation
```

**Exception Strategy:**
- Catch and log API exceptions
- Surface critical errors via `QueueCriticalError`
- Broadcast errors via event bus
- Persist failed operations for retry

---

### 3. UI Layer (pywats_ui)

**Purpose:** Qt-based GUI applications with shared framework

**Key Components:**
- `BasePage` - Base class for all UI pages
- `ErrorHandlingMixin` - Centralized error dialogs
- `AsyncTaskRunner` - Non-blocking async operations
- `AsyncAPIRunner` - API call wrapper for GUI
- Event subscriptions via Qt Signals

**Responsibilities:**
- User interaction
- API calls via IPC or direct (degraded mode)
- Event subscription and handling
- Visual feedback for async operations
- Error display to users
- Configuration UI

**Event Subscription:**
```python
# In BasePage subclass
self.subscribe_event(AppEvent.API_CLIENT_READY, self._on_api_ready)
self.subscribe_event(AppEvent.QUEUE_STATUS_CHANGED, self._update_queue_status)
```

**Error Handling:**
```python
try:
    result = api.get_product(product_id)
except Exception as e:
    self.handle_error(e, "loading product")  # Shows appropriate QMessageBox
```

**Logging:**
```python
from pywats.core.logging import get_logger
logger = get_logger(__name__)  # Uses API logger hierarchy
```

---

## Event Systems

### Two Independent Event Systems

pyWATS uses **TWO SEPARATE** event systems for different purposes:

#### 1. Application EventBus (pywats_client.core.event_bus)

**Purpose:** GUI ↔ Service communication (Qt-based)

**Technology:** Qt Signals (thread-safe, cross-process capable)

**Scope:** Client service ↔ UI applications

**Event Types (`AppEvent`):**
- `CONNECTION_CHANGED` - Server connection status
- `API_CLIENT_READY` - pyWATS client available
- `APP_STATUS_CHANGED` - Service lifecycle
- `QUEUE_STATUS_CHANGED` - Report queue status
- `CONFIG_CHANGED` - Configuration updates
- etc.

**Architecture:**
```
┌─────────────┐    Qt Signal    ┌──────────────────┐
│ ClientService│ ──────────────→ │ ApplicationEvent │
│             │                  │      Bus         │
│ (Publisher) │                  │   (Singleton)    │
└─────────────┘                  └────────┬─────────┘
                                          │ Qt Signal
                                          ↓
                              ┌───────────────────────┐
                              │  GUI Pages            │
                              │  (Subscribers)        │
                              └───────────────────────┘
```

**Usage Pattern:**
```python
# Publish (from ClientService)
event_bus.publish(AppEvent.CONNECTION_CHANGED, status="Online")

# Subscribe (from GUI Page)
def _on_connection(self, data: dict):
    status = data.get('status')
    self.status_label.setText(status)

event_bus.subscribe(AppEvent.CONNECTION_CHANGED, self._on_connection)
```

#### 2. Protocol EventBus (pywats_events)

**Purpose:** Protocol-agnostic event infrastructure (IPC-CFX, MQTT, webhooks)

**Technology:** Python threading, async/await

**Scope:** External message sources → Domain handlers

**Event Types (`EventType`):**
- `TEST_RESULT` - Test execution results
- `UNIT_STATUS_CHANGED` - Unit lifecycle
- `STATION_STATUS` - Station status
- etc.

**Architecture:**
```
┌──────────────┐        ┌────────────┐        ┌─────────────┐
│   Transports │        │  EventBus  │        │  Handlers   │
│  (IPC-CFX,   │ ─────→ │  (Core)    │ ─────→ │  (Business  │
│   MQTT, etc.)│ Events │            │ Events │   Logic)    │
└──────────────┘        └────────────┘        └─────────────┘
```

**Usage Pattern:**
```python
from pywats_events import EventBus, Event, EventType

# Create handler
class MyHandler(BaseHandler):
    @property
    def event_types(self):
        return [EventType.TEST_RESULT]
    
    async def handle(self, event: Event):
        # Process event
        pass

# Wire up
bus = EventBus()
bus.register_handler(MyHandler())
bus.start()
```

### Event System Comparison

| Aspect | Application EventBus | Protocol EventBus |
|--------|---------------------|-------------------|
| **Layer** | Client ↔ UI | Event Infrastructure |
| **Technology** | Qt Signals | Python threading/async |
| **Thread Safety** | Yes (Qt) | Yes (manual locks) |
| **Cross-Process** | Via IPC | Via Transports |
| **Purpose** | App state broadcast | Protocol integration |
| **Event Types** | `AppEvent` (enum) | `EventType` (enum) |
| **Subscribers** | GUI Pages, Services | Domain Handlers |
| **Publishers** | ClientService, UI | Transports (CFX, MQTT) |
| **Pattern** | Observer (Qt) | Pub/Sub with routing |
| **Singleton** | Yes | No (instantiate) |
| **Async Support** | Via QMetaObject | Native async |

### When to Use Which?

**Use Application EventBus** (pywats_client.core.event_bus) when:
- GUI needs to react to service state changes
- Broadcasting configuration updates
- Notifying multiple pages of data changes
- Cross-widget communication without tight coupling

**Use Protocol EventBus** (pywats_events) when:
- Integrating external message sources (IPC-CFX, MQTT)
- Building domain event handlers
- Implementing event-driven architecture for business logic
- Need transport-agnostic event processing

**Both can coexist!**
```python
# Protocol events can trigger application events
class MyHandler(BaseHandler):
    async def handle(self, protocol_event: Event):
        # Do domain logic
        result = process_test_result(protocol_event)
        
        # Notify GUI
        event_bus.publish(AppEvent.DATA_CHANGED)
```

---

## Logging Infrastructure

### Logging Hierarchy

```
root logger
│
├─── pywats (API layer)
│    ├─── pywats.domains.report
│    ├─── pywats.domains.product
│    ├─── pywats.core.async_client
│    └─── pywats.core.cache
│
├─── pywats_client (Client layer)
│    ├─── pywats_client.service.client_service
│    ├─── pywats_client.core.queue_manager
│    └─── pywats_client.core.event_bus
│
├─── pywats_ui (UI layer)
│    ├─── pywats_ui.framework.base_page
│    └─── pywats_ui.apps.configurator.pages.*
│
└─── pywats_events (Event infrastructure)
     ├─── pywats_events.bus.event_bus
     └─── pywats_events.handlers.*
```

### Logger Initialization Patterns

**All layers use the same pattern:**
```python
from pywats.core.logging import get_logger
logger = get_logger(__name__)  # Creates logger with module name
```

**Result:** Clean hierarchy based on package structure

### Log Files and Ownership

| Layer | Log Location | Configured By | Purpose |
|-------|--------------|---------------|---------|
| **API** | Console (default) | API user | Development/debugging |
| **Client Service** | `{install_dir}/pywats.log` | `setup_client_logging()` | Production service logs |
| **Converters** | `{install_dir}/conversion_logs/*.log` | ConversionLog | Per-conversion results |
| **GUI** | Console + Service log | Inherited from API | User actions |

### Logging Configuration

**Client Service Setup:**
```python
from pywats_client.core.logging import setup_client_logging

setup_client_logging(
    instance_id="default",
    log_level="INFO",
    log_format="text",  # or "json"
    enable_console=True,
    rotate_size_mb=10,
    rotate_backups=5
)
```

**Features:**
- Rotating file handler (10MB default, 5 backups)
- JSON format support for structured logging
- Correlation ID support
- Context injection (instance_id, user_id, etc.)

### Correlation IDs

**Flow:**
1. API generates correlation ID for each request
2. Stored in context variable (thread-local)
3. Added to all log messages during request
4. Returned in response headers
5. Used in error messages for tracking

**Implementation:**
```python
import contextvars

correlation_id_var = contextvars.ContextVar('correlation_id', default=None)

def _run_sync(coro, correlation_id=None):
    token = None
    if correlation_id:
        token = correlation_id_var.set(correlation_id)
    try:
        return run_sync(coro)
    finally:
        if token:
            correlation_id_var.reset(token)
```

---

## Exception Propagation

### Exception Hierarchy

```
Exception
│
└─── PyWATSError (pywats.core.exceptions)
     ├─── AuthenticationError
     ├─── AuthorizationError
     ├─── ValidationError
     ├─── NotFoundError
     ├─── ConflictError
     ├─── ServerError
     ├─── ConnectionError
     ├─── TimeoutError
     └─── WatsApiError
          ├─── EmptyResponseError
          └─── InvalidResponseError

Exception
│
└─── ClientError (pywats_client.exceptions)
     ├─── ConfigurationError
     ├─── ServiceError
     ├─── QueueCriticalError
     └─── ConverterError
```

### Exception Flow Patterns

#### Pattern 1: API → Client → UI (Synchronous)

```
┌────────┐     ┌────────┐     ┌────────┐     ┌─────┐
│  User  │────→│   UI   │────→│ Client │────→│ API │
│ Action │     │  Page  │     │Service │     │     │
└────────┘     └───┬────┘     └───┬────┘     └──┬──┘
                   │              │             │
                   │              │             │ HTTP 404
                   │              │             │ throw NotFoundError
                   │              │     ←───────┘
                   │              │
                   │              │ catch, log, re-raise
                   │      ←───────┘
                   │
                   │ handle_error(e, "loading product")
                   │ show QMessageBox
                   ↓
              ┌─────────┐
              │  User   │
              │ Dialog  │
              └─────────┘
```

**Code:**
```python
# UI Layer
try:
    product = await api.product.get(product_id)
except NotFoundError as e:
    self.handle_error(e, "loading product")  # ErrorHandlingMixin
    # Shows: "The requested item was not found while loading product"
```

#### Pattern 2: Background Service Error → Event → UI

```
┌─────────────┐                    ┌────────────┐
│   Client    │                    │  EventBus  │
│   Service   │                    │            │
└──────┬──────┘                    └─────┬──────┘
       │                                 │
       │ Queue operation fails           │
       │ (both queue + fallback)         │
       │                                 │
       │ throw QueueCriticalError        │
       │                                 │
       │ catch, log with exc_info        │
       │                                 │
       │ publish(APP_ERROR, error=e) ───→│
       │                                 │
       │                                 │ emit signal
       │                                 ↓
       │                          ┌─────────────┐
       │                          │  UI Pages   │
       │                          │  (subscribed)│
       │                          └──────┬──────┘
       │                                 │
       │                                 │ show critical dialog
       │                                 ↓
       │                          ┌─────────────┐
       │                          │    User     │
       │                          └─────────────┘
```

**Code:**
```python
# Client Service
try:
    await queue_manager.enqueue(report)
except QueueCriticalError as e:
    logger.critical("Queue critical error", exc_info=True)
    event_bus.publish(AppEvent.APP_ERROR, error=str(e))

# UI Page
def _on_app_error(self, data: dict):
    error = data.get('error')
    self.show_error(f"Service error: {error}", "Critical Error")
```

### Error Handling by Layer

**API Layer:**
- **Strategy:** Raise exceptions (re-raise with context)
- **Logging:** Log at point of detection with `exc_info=True`
- **User Impact:** None (handled by caller)

**Client Layer:**
- **Strategy:** Catch, log, broadcast via events
- **Logging:** Comprehensive logging with correlation IDs
- **User Impact:** Events trigger UI notifications

**UI Layer:**
- **Strategy:** Catch all, show appropriate dialog
- **Logging:** Log user-facing errors
- **User Impact:** Direct (QMessageBox dialogs)

**Error Handling Mixin Usage:**
```python
class ErrorHandlingMixin:
    def handle_error(self, error: Exception, context: str = ""):
        """Show appropriate dialog based on exception type"""
        if isinstance(error, AuthenticationError):
            QMessageBox.warning(self, "Auth Error", "Please log in again")
        elif isinstance(error, ValidationError):
            QMessageBox.warning(self, "Invalid Input", str(error))
        elif isinstance(error, ConnectionError):
            QMessageBox.warning(self, "Connection Error", "Check network")
        elif isinstance(error, QueueCriticalError):
            QMessageBox.critical(self, "CRITICAL", "Data loss risk!")
        else:
            logger.exception(f"Unexpected error: {error}")
            QMessageBox.critical(self, "Error", str(error))
```

---

## Component Ownership

### Component Matrix

| Component | Package | Owns Lifecycle | Depends On | Used By |
|-----------|---------|---------------|-----------|---------|
| **pyWATS API** | pywats | User/Script | HTTP Client | Client Service, GUI |
| **AsyncHttpClient** | pywats.core | pyWATS | aiohttp | All domain services |
| **Domain Services** | pywats.domains | pyWATS | AsyncHttpClient | pyWATS API |
| **ClientService** | pywats_client.service | Service Manager | pyWATS, Config | Service Manager |
| **ApplicationEventBus** | pywats_client.core | Singleton | Qt | ClientService, GUI |
| **QueueManager** | pywats_client.core | ClientService | Config, FileSystem | ClientService |
| **BasePage** | pywats_ui.framework | QMainWindow | Config, EventBus | All GUI pages |
| **ErrorHandlingMixin** | pywats_ui.framework | Page (mixin) | Qt, Exceptions | All GUI pages |
| **AsyncTaskRunner** | pywats_client.core | BasePage | asyncio, Qt | BasePage |
| **ProtocolEventBus** | pywats_events.bus | User/Script | Handlers, Transports | Event-driven apps |

### Dependency Graph

```
┌────────────────────────────────────────────────────────┐
│                    UI Applications                      │
│  (Configurator, YieldMonitor, PackageManager, etc.)    │
└──────────────┬─────────────────────────────────────────┘
               │ depends on
               ↓
┌────────────────────────────────────────────────────────┐
│                  pywats_ui.framework                    │
│  (BasePage, ErrorHandlingMixin, AsyncTaskRunner)       │
└──────────────┬─────────────────────────────────────────┘
               │ depends on
               ↓
┌────────────────────────────────────────────────────────┐
│                   pywats_client                         │
│  (ClientService, EventBus, Config, Queue)              │
└──────────────┬─────────────────────────────────────────┘
               │ depends on
               ↓
┌────────────────────────────────────────────────────────┐
│                      pywats                             │
│  (pyWATS API, Domain Services, HTTP Client)            │
└──────────────┬─────────────────────────────────────────┘
               │ depends on
               ↓
         ┌─────────────┐
         │ WATS Server │
         └─────────────┘

      (Parallel dependency - optional)
               │
               ↓
┌────────────────────────────────────────────────────────┐
│                   pywats_events                         │
│  (EventBus, Handlers, Transports, Models)              │
└────────────────────────────────────────────────────────┘
```

---

## Communication Patterns

[Continue in next section...]

---

**Last Updated:** February 8, 2026
