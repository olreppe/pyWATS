# Component Diagrams - API-Client-UI Architecture

**Date:** February 8, 2026

This document contains comprehensive component diagrams showing class hierarchies, system architecture, and component relationships.

---

## 1. Three-Layer System Architecture

```mermaid
C4Context
    title System Context - pyWATS Three-Layer Architecture

    Person(user, "User", "Test engineer or operator")
    
    System_Boundary(pyWATS, "pyWATS System") {
        Container(ui, "UI Layer", "PySide6", "GUI applications for configuration and monitoring")
        Container(client, "Client Layer", "Python Service", "Background service for file monitoring and queue management")
        Container(api, "API Layer", "Python Library", "Synchronous API wrapper for WATS server")
    }
    
    System_Ext(wats, "WATS Server", "Test data management server")
    System_Ext(cfx, "IPC-CFX Devices", "Manufacturing equipment")
    
    Rel(user, ui, "Interacts with", "Qt GUI")
    Rel(ui, client, "Events, IPC", "Qt Signals, Named Pipes")
    Rel(client, api, "API Calls", "Function calls")
    Rel(api, wats, "HTTP REST", "JSON over HTTPS")
    Rel(cfx, client, "Test Results", "IPC-CFX protocol")
```

---

## 2. Layer Component View

```mermaid
graph TB
    subgraph UI["UI Layer (pywats_ui)"]
        Configurator[Configurator App]
        YieldMonitor[Yield Monitor App]
        Framework[UI Framework]
        
        Configurator --> Framework
        YieldMonitor --> Framework
        
        subgraph FrameworkComponents["Framework Components"]
            BasePage[BasePage]
            ErrorMixin[ErrorHandlingMixin]
            AsyncRunner[AsyncTaskRunner]
            APIRunner[AsyncAPIRunner]
        end
        
        Framework --> FrameworkComponents
    end
    
    subgraph Client["Client Layer (pywats_client)"]
        ClientService[Client Service]
        ConfigMgr[Config Manager]
        QueueMgr[Queue Manager]
        AppEventBus["Application EventBus<br/>(Qt Signals)"]
        IPCServer[IPC Server]
        
        ClientService --> ConfigMgr
        ClientService --> QueueMgr
        ClientService --> AppEventBus
        ClientService --> IPCServer
    end
    
    subgraph API["API Layer (pywats)"]
        PyWATS[pyWATS Class]
        AsyncClient[AsyncHttpClient]
        DomainServices[Domain Services]
        CoreExceptions[Core Exceptions]
        CoreLogging[Core Logging]
        
        PyWATS --> AsyncClient
        PyWATS --> DomainServices
        DomainServices --> AsyncClient
        DomainServices --> CoreExceptions
        DomainServices --> CoreLogging
    end
    
    subgraph Events["Event Infrastructure (pywats_events)"]
        ProtocolBus[Protocol EventBus]
        Handlers[Event Handlers]
        Transports[Transports<br/>CFX, MQTT]
        
        Transports --> ProtocolBus
        ProtocolBus --> Handlers
    end
    
    UI -->|Qt Signals,<br/>IPC| Client
    Client -->|Function Calls| API
    Client -.->|Optional| Events
    Handlers -.->|Can trigger| AppEventBus
    
    style UI fill:#e1f5fe
    style Client fill:#fff3e0
    style API fill:#f3e5f5
    style Events fill:#e8f5e9
```

---

## 3. Class Hierarchy - API Layer

```mermaid
classDiagram
    class pyWATS {
        -AsyncHttpClient _http_client
        -Station _station
        -SyncConfig _sync_config
        +property report : SyncServiceWrapper
        +property product : SyncServiceWrapper
        +property asset : SyncServiceWrapper
        +test_connection() bool
        +close()
        +__enter__() pyWATS
        +__exit__()
    }
    
    class AsyncHttpClient {
        -str _base_url
        -str _token
        -ClientSession _session
        -RetryConfig _retry_config
        +async get(endpoint) dict
        +async post(endpoint, data) dict
        +async patch(endpoint, data) dict
        +async delete(endpoint) dict
        +async close()
    }
    
    class SyncServiceWrapper {
        -AsyncService _async_service
        -SyncConfig _config
        +__getattr__(name) method
        -_wrap_async(coro) result
    }
    
    class AsyncReportService {
        -AsyncHttpClient _client
        +async list(filters) List~Report~
        +async get(id) Report
        +async create(report) Report
        +async upload_file(file) str
    }
    
    class AsyncProductService {
        -AsyncHttpClient _client
        +async list() List~Product~
        +async get(id) Product
        +async search(query) List~Product~
    }
    
    class PyWATSError {
        +str error_type
        +str message
        +dict details
    }
    
    class AuthenticationError {
        +str auth_method
    }
    
    class NotFoundError {
        +str resource_type
        +str resource_id
    }
    
    class ValidationError {
        +dict validation_errors
    }
    
    pyWATS --> AsyncHttpClient : uses
    pyWATS --> SyncServiceWrapper : creates
    SyncServiceWrapper --> AsyncReportService : wraps
    SyncServiceWrapper --> AsyncProductService : wraps
    AsyncReportService --> AsyncHttpClient : uses
    AsyncProductService --> AsyncHttpClient : uses
    
    PyWATSError <|-- AuthenticationError
    PyWATSError <|-- NotFoundError
    PyWATSError <|-- ValidationError
    
    AsyncReportService --> PyWATSError : raises
    AsyncProductService --> PyWATSError : raises
```

---

## 4. Class Hierarchy - Client Layer

```mermaid
classDiagram
    class ClientService {
        -AsyncClientService _async
        -EventLoop _loop
        +instance_id : str
        +config : ClientConfig
        +status : ServiceStatus
        +start()
        +stop()
        +get_stats() dict
    }
    
    class AsyncClientService {
        -str _instance_id
        -ClientConfig _config
        -pyWATS _api
        -QueueManager _queue
        -PendingWatcher _watcher
        -AsyncServiceStatus _status
        +async run()
        +async stop()
        +async _initialize_api()
        +async _process_queue()
    }
    
    class ApplicationEventBus {
        <<singleton>>
        -dict _subscribers
        +Signal connection_changed
        +Signal api_client_ready
        +publish(event, **data)
        +subscribe(event, callback)
        +unsubscribe(event, callback)
    }
    
    class AppEvent {
        <<enumeration>>
        CONNECTION_CHANGED
        API_CLIENT_READY
        QUEUE_STATUS_CHANGED
        CONFIG_CHANGED
        APP_ERROR
    }
    
    class QueueManager {
        -Path _queue_dir
        -Path _fallback_dir
        -dict _pending
        +async enqueue(report) str
        +async mark_processed(op_id)
        +async mark_failed(op_id)
        +get_status() QueueStatus
    }
    
    class ClientConfig {
        +str instance_name
        +str server_url
        +str api_token
        +bool auto_connect
        +str log_level
        +save()
        +load() ClientConfig
    }
    
    class ClientError {
        +str error_type
        +str message
    }
    
    class QueueCriticalError {
        +Exception primary_error
        +Exception fallback_error
        +str operation_id
    }
    
    ClientService --> AsyncClientService : wraps
    AsyncClientService --> ApplicationEventBus : publishes to
    AsyncClientService --> QueueManager : uses
    AsyncClientService --> ClientConfig : uses
    AsyncClientService --> pyWATS : creates
    
    ApplicationEventBus --> AppEvent : uses
    QueueManager --> QueueCriticalError : raises
    ClientError <|-- QueueCriticalError
```

---

## 5. Class Hierarchy - UI Framework

```mermaid
classDiagram
    class QWidget {
        <<Qt>>
        +show()
        +hide()
        +setEnabled(bool)
    }
    
    class BasePage {
        -ClientConfig config
        -AsyncTaskRunner _async_runner
        -List~tuple~ _event_subscriptions
        +Signal config_changed
        +Signal loading_changed
        +property page_title : str
        +run_async(coro, name)
        +subscribe_event(event, callback)
        +save_config()
        +load_config()
    }
    
    class ErrorHandlingMixin {
        +handle_error(error, context)
        +show_success(message)
        +show_warning(message)
        +show_error(message)
        +confirm_action(message) bool
    }
    
    class AsyncTaskRunner {
        -QThreadPool _thread_pool
        -dict _tasks
        +Signal task_started
        +Signal task_finished
        +submit_task(coro, name) str
        +cancel_task(task_id) bool
        +get_status(task_id) TaskStatus
    }
    
    class TaskResult {
        +bool success
        +Any data
        +Exception error
        +str task_id
        +str name
    }
    
    class AsyncAPIRunner {
        -pyWATS _api_client
        -AsyncTaskRunner _runner
        +run(coro, on_complete)
        +get_product(id, callback)
        +list_reports(filters, callback)
    }
    
    class SetupPage {
        -QLineEdit server_url_input
        -QLineEdit api_token_input
        +save_config()
        +load_config()
        +_on_test_connection()
    }
    
    class ReportsPage {
        -QTableWidget reports_table
        -QComboBox filter_combo
        +load_config()
        +_on_refresh()
        +_load_reports()
        +_on_reports_loaded(reports)
    }
    
    QWidget <|-- BasePage
    BasePage <|-- ErrorHandlingMixin : mixin
    BasePage --> AsyncTaskRunner : uses
    BasePage --> TaskResult : receives
    
    AsyncAPIRunner --> AsyncTaskRunner : uses
    AsyncAPIRunner --> pyWATS : wraps
    
    BasePage <|-- SetupPage
    BasePage <|-- ReportsPage
```

---

## 6. Event System Architecture

```mermaid
graph TB
    subgraph AppEventSystem["Application Event System (Qt-based)"]
        AppBus["ApplicationEventBus<br/>(Singleton)"]
        
        subgraph Publishers["Publishers"]
            ClientSvc[Client Service]
            UIPagesP[UI Pages]
        end
        
        subgraph Subscribers["Subscribers"]
            UIPagesS[UI Pages]
            OtherSvc[Other Services]
        end
        
        Publishers -->|publish| AppBus
        AppBus -->|Qt Signal| Subscribers
    end
    
    subgraph ProtocolEventSystem["Protocol Event System"]
        ProtoBus[Protocol EventBus]
        
        subgraph TransportLayer["Transports"]
            CFX[CFX Transport]
            MQTT[MQTT Transport]
            WebHook[WebHook Transport]
        end
        
        subgraph HandlerLayer["Handlers"]
            TestHandler[TestResultHandler]
            StatusHandler[StatusHandler]
            CustomHandler[Custom Handlers]
        end
        
        TransportLayer -->|publish events| ProtoBus
        ProtoBus -->|route to| HandlerLayer
    end
    
    HandlerLayer -.->|can trigger| AppBus
    
    style AppEventSystem fill:#e1f5fe
    style ProtocolEventSystem fill:#e8f5e9
    style AppBus fill:#81d4fa
    style ProtoBus fill:#a5d6a7
```

---

## 7. Event Type Hierarchy

```mermaid
graph LR
    subgraph ApplicationEvents["Application Events (Qt)"]
        AE1[CONNECTION_CHANGED<br/>status: str]
        AE2[API_CLIENT_READY<br/>client: pyWATS]
        AE3[QUEUE_STATUS_CHANGED<br/>pending: int, failed: int]
        AE4[CONFIG_CHANGED<br/>key: str, value: Any]
        AE5[APP_ERROR<br/>error: str]
    end
    
    subgraph ProtocolEvents["Protocol Events"]
        PE1[TEST_RESULT<br/>unit_id, result, data]
        PE2[UNIT_STATUS_CHANGED<br/>unit_id, status]
        PE3[STATION_STATUS<br/>station_id, status]
        PE4[RESOURCE_UPDATED<br/>resource_type, id]
    end
    
    subgraph EventFlow["Event Flow"]
        UI[UI Pages] -->|subscribe| AE1
        UI -->|subscribe| AE2
        UI -->|subscribe| AE3
        UI -->|subscribe| AE4
        
        Service[Client Service] -->|publish| AE1
        Service -->|publish| AE2
        Service -->|publish| AE3
        
        Devices[Manufacturing Devices] -->|produce| PE1
        Devices -->|produce| PE2
        
        Handlers[Domain Handlers] -->|process| PE1
        Handlers -->|process| PE2
        Handlers -.->|can trigger| AE4
    end
    
    style ApplicationEvents fill:#fff3e0
    style ProtocolEvents fill:#f3e5f5
```

---

## 8. Logging Architecture

```mermaid
graph TB
    subgraph RootLogger["Root Logger Hierarchy"]
        Root[root]
        
        subgraph APILoggers["pywats.*"]
            APIRoot[pywats]
            APIReport[pywats.domains.report]
            APIProduct[pywats.domains.product]
            APIClient[pywats.core.async_client]
            APICache[pywats.core.cache]
            
            APIRoot --> APIReport
            APIRoot --> APIProduct
            APIRoot --> APIClient
            APIRoot --> APICache
        end
        
        subgraph ClientLoggers["pywats_client.*"]
            ClientRoot[pywats_client]
            ClientService[pywats_client.service]
            ClientQueue[pywats_client.core.queue_manager]
            ClientEventBus[pywats_client.core.event_bus]
            
            ClientRoot --> ClientService
            ClientRoot --> ClientQueue
            ClientRoot --> ClientEventBus
        end
        
        subgraph UILoggers["pywats_ui.*"]
            UIRoot[pywats_ui]
            UIFramework[pywats_ui.framework.base_page]
            UIApps[pywats_ui.apps.configurator]
            
            UIRoot --> UIFramework
            UIRoot --> UIApps
        end
        
        subgraph EventLoggers["pywats_events.*"]
            EventRoot[pywats_events]
            EventBus[pywats_events.bus.event_bus]
            EventHandlers[pywats_events.handlers]
            
            EventRoot --> EventBus
            EventRoot --> EventHandlers
        end
        
        Root --> APIRoot
        Root --> ClientRoot
        Root --> UIRoot
        Root --> EventRoot
    end
    
    subgraph LogDestinations["Log Destinations"]
        Console[Console Handler<br/>sys.stdout]
        ServiceLog[Service File Handler<br/>/ProgramData/pyWATS/pywats.log]
        ConversionLogs[Conversion Log Directory<br/>/ProgramData/pyWATS/conversion_logs/]
    end
    
    APIRoot -.->|development| Console
    ClientRoot -->|production| ServiceLog
    ClientRoot -->|converters| ConversionLogs
    UIRoot -.->|inherits| ClientRoot
    
    style APILoggers fill:#f3e5f5
    style ClientLoggers fill:#fff3e0
    style UILoggers fill:#e1f5fe
    style EventLoggers fill:#e8f5e9
```

---

## 9. Exception Hierarchy

```mermaid
graph TB
    Exception[Exception<br/>Python built-in]
    
    subgraph APIExceptions["API Layer Exceptions"]
        PyWATSError[PyWATSError<br/>Base for all API errors]
        AuthError[AuthenticationError<br/>401 responses]
        AuthzError[AuthorizationError<br/>403 responses]
        ValidationError[ValidationError<br/>400 responses]
        NotFoundError[NotFoundError<br/>404 responses]
        ConflictError[ConflictError<br/>409 responses]
        ServerError[ServerError<br/>500 responses]
        ConnError[ConnectionError<br/>Network issues]
        TimeoutError[TimeoutError<br/>Request timeout]
        WatsAPIError[WatsApiError<br/>API-specific]
        EmptyResp[EmptyResponseError]
        InvalidResp[InvalidResponseError]
    end
    
    subgraph ClientExceptions["Client Layer Exceptions"]
        ClientError[ClientError<br/>Base for client errors]
        ConfigError[ConfigurationError<br/>Config issues]
        ServiceError[ServiceError<br/>Service lifecycle]
        QueueError[QueueCriticalError<br/>Double failure]
        ConverterError[ConverterError<br/>Conversion issues]
    end
    
    Exception --> PyWATSError
    PyWATSError --> AuthError
    PyWATSError --> AuthzError
    PyWATSError --> ValidationError
    PyWATSError --> NotFoundError
    PyWATSError --> ConflictError
    PyWATSError --> ServerError
    PyWATSError --> ConnError
    PyWATSError --> TimeoutError
    PyWATSError --> WatsAPIError
    WatsAPIError --> EmptyResp
    WatsAPIError --> InvalidResp
    
    Exception --> ClientError
    ClientError --> ConfigError
    ClientError --> ServiceError
    ClientError --> QueueError
    ClientError --> ConverterError
    
    style PyWATSError fill:#f3e5f5
    style ClientError fill:#fff3e0
    style QueueError fill:#ffcdd2
```

---

## 10. Dependency Graph

```mermaid
graph TB
    subgraph Applications["Applications"]
        Configurator[Configurator GUI]
        YieldMon[Yield Monitor]
        PkgMgr[Package Manager]
    end
    
    subgraph UIFramework["UI Framework"]
        BasePage
        ErrorMixin[ErrorHandlingMixin]
        AsyncRunner[AsyncTaskRunner]
    end
    
    subgraph ClientCore["Client Core"]
        ClientService
        EventBus[Application EventBus]
        QueueManager
        ConfigManager
    end
    
    subgraph APICore["API Core"]
        PyWATS
        AsyncHttpClient
        DomainServices[Domain Services]
        CoreExceptions[Core Exceptions]
        CoreLogging[Core Logging]
    end
    
    subgraph EventInfra["Event Infrastructure"]
        ProtocolBus[Protocol EventBus]
        Handlers
        Transports
    end
    
    subgraph External["External Dependencies"]
        Qt[PySide6/Qt]
        HTTP[aiohttp]
        FileSystem[watchdog]
    end
    
    Applications --> UIFramework
    UIFramework --> ClientCore
    UIFramework --> Qt
    
    ClientCore --> APICore
    ClientCore --> Qt
    ClientCore --> FileSystem
    
    APICore --> HTTP
    APICore --> CoreLogging
    APICore --> CoreExceptions
    
    EventInfra -.->|optional| ClientCore
    Transports --> ProtocolBus
    ProtocolBus --> Handlers
    
    style Applications fill:#e1f5fe
    style UIFramework fill:#e1f5fe
    style ClientCore fill:#fff3e0
    style APICore fill:#f3e5f5
    style EventInfra fill:#e8f5e9
    style External fill:#eceff1
```

---

## 11. Component Communication Matrix

| From ↓ To → | UI Layer | Client Service | Application EventBus | API Layer | Protocol EventBus |
|-------------|----------|----------------|---------------------|-----------|-------------------|
| **UI Layer** | - | IPC calls, Config updates | Subscribe, Publish | Direct calls (degraded mode) | - |
| **Client Service** | - | - | Publish events | Direct calls | Optional: Trigger app events |
| **Application EventBus** | Qt Signals | Qt Signals | - | - | - |
| **API Layer** | Return values, Exceptions | Return values, Exceptions | - | - | - |
| **Protocol EventBus** | - | Via handlers | Via handlers | - | - |

---

**Last Updated:** February 8, 2026
