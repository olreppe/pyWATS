# Flow Charts - API-Client-UI Communication

**Date:** February 8, 2026

This document contains comprehensive flow charts showing data flows, event propagation, and communication patterns across all layers.

---

## 1. User Action → API Call → Response Flow

### Scenario: User loads a product in the GUI

```mermaid
sequenceDiagram
    actor User
    participant UI as UI Page
    participant EventBus as Qt EventBus
    participant Client as Client Service
    participant API as pyWATS API
    participant HTTP as AsyncHttpClient
    participant Server as WATS Server

    User->>UI: Click "Load Product"
    activate UI
    
    UI->>UI: run_async(load_product())
    Note over UI: BasePage.run_async<br/>creates async task
    
    UI->>EventBus: Emit loading_changed(true)
    EventBus-->>UI: Update loading indicator
    
    UI->>API: api.product.get(product_id)
    activate API
    Note over API: Sync wrapper calls<br/>async service
    
    API->>HTTP: await async_client.get(/product/{id})
    activate HTTP
    HTTP->>HTTP: Add auth headers<br/>Generate correlation ID
    HTTP->>Server: HTTP GET /api/product/12345
    activate Server
    
    alt Success Case
        Server-->>HTTP: 200 OK + Product JSON
        deactivate Server
        HTTP-->>API: Product model
        deactivate HTTP
        API-->>UI: Product
        deactivate API
        UI->>UI: Display product details
        UI->>EventBus: Emit loading_changed(false)
        EventBus-->>UI: Hide loading indicator
        UI-->>User: Show product datadeactivate UI
    
    else Error Case (404 Not Found)
        Server-->>HTTP: 404 Not Found
        deactivate Server
        HTTP->>HTTP: raise Not FoundError
        HTTP-->>API: NotFoundError
        deactivate HTTP
        API->>API: Log exception with exc_info
        API-->>UI: NotFoundError
        deactivate API
        UI->>UI: handle_error(e, "loading product")
        Note over UI: ErrorHandlingMixin shows<br/>appropriate QMessageBox
        UI-->>User: Show error dialog
        UI->>EventBus: Emit loading_changed(false)
        deactivate UI
    end
```

---

## 2. Background Service Event Flow

### Scenario: Client service monitors file, processes report, updates queue

```mermaid
sequenceDiagram
    participant FS as File System
    participant Watcher as PendingWatcher
    participant Service as ClientService
    participant Converter as ReportConverter
    participant Queue as QueueManager
    participant API as pyWATS API
    participant EventBus as Qt EventBus
    participant UI as GUI Pages

    FS->>Watcher: File created: report.txt
    activate Watcher
    Watcher->>Watcher: Debounce (wait 500ms)
    Watcher->>Service: File stable: report.txt
    deactivate Watcher
    
    activate Service
    Service->>Service: Identify converter
    Service->>Converter: convert(report.txt)
    activate Converter
    
    alt Conversion Success
        Converter->>FS: Write wats_report.xml
        Converter-->>Service: ConversionResult(success=True)
        deactivate Converter
        
        Service->>Queue: enqueue(wats_report.xml)
        activate Queue
        Queue->>FS: Write to queue directory
        
        alt Queue Success
            FS-->>Queue: File written
            Queue-->>Service: Operation ID
            deactivate Queue
            
            Service->>EventBus: publish(QUEUE_ITEM_ADDED)
            EventBus->>UI: Notify subscribers
            UI->>UI: Update queue count
            
            Service->>API: api.report.upload(wats_report.xml)
            activate API
            API-->>Service: Report ID
            deactivate API
            
            Service->>Queue: mark_processed(operation_id)
            Service->>EventBus: publish(QUEUE_ITEM_PROCESSED, success=True)
            EventBus->>UI: Update queue statusUI->>UI: Show success notification
        
        else Queue Failure (Primary)
            FS-->>Queue: Write failed (disk full)
            Queue->>Queue: Try fallback location
            FS-->>Queue: Fallback also failed
            
            Queue->>Queue: raise QueueCriticalError
            Queue-->>Service: QueueCriticalError
            deactivate Queue
            
            Service->>Service: Log critical error with exc_info
            Service->>EventBus: publish(APP_ERROR, error=str(e))
            EventBus->>UI: Notify subscribers
            UI->>UI: Show critical error dialog
            
            Note over UI: "CRITICAL: Queue Failure<br/>Data may be lost.<br/>Check disk space!"
        end
        deactivate Service
    
    else Conversion Failure
        Converter->>Converter: raise ConverterError
        Converter-->>Service: ConverterError
        deactivate Converter
        Service->>Service: Log error with exc_info
        Service->>EventBus: publish(APP_ERROR, error=str(e))
        deactivate Service
    end
```

---

## 3. Application Startup Flow

### Scenario: GUI launches and connects to service

```mermaid
sequenceDiagram
    actor User
    participant GUI as Configurator GUI
    participant EventBus as Qt EventBus
    participant IPC as IPC Client
    participant Service as Client Service
    participant API as pyWATS API
    participant Server as WATS Server

    User->>GUI: Launch configurator
    activate GUI
    
    GUI->>GUI: Load ClientConfig
    GUI->>EventBus: Initialize singleton
    GUI->>IPC: connect()
    activate IPC
    
    alt Service Running
        IPC->>Service: Connect via named pipe/socket
        Service-->>IPC: Connection accepted
        IPC-->>GUI: Connected
        deactivate IPC
        
        GUI->>Service: get_status()
        activate Service
        Service-->>GUI: {"running": true, "api_status": "Online"}
        deactivate Service
        
        GUI->>EventBus: Subscribe to events
        Note over GUI,EventBus: Subscribe to:<br/>API_CLIENT_READY<br/>CONNECTION_CHANGED<br/>QUEUE_STATUS_CHANGED
        
        Service->>EventBus: publish(API_CLIENT_READY, client=api)
        EventBus->>GUI: _on_api_ready(data)
        GUI->>GUI: Enable API-dependent features
        GUI-->>User: Show dashboard (connected)
    
    else Service Not Running
        IPC-->>GUI: Connection failed
        deactivate IPC
        
        GUI->>GUI: Enter degraded mode
        GUI-->>User: Show "Service Offline" banner
        
        alt Auto-start Enabled
            GUI->>Service: Start service
            activate Service
            
            Service->>Service: Load config
            Service->>API: Initialize pyWATS client
            activate API
            API->>Server: Test connection
            Server-->>API: Version info
            API-->>Service: Client ready
            deactivate API
            
            Service->>EventBus: publish(API_CLIENT_READY)
            Service->>EventBus: publish(CONNECTION_CHANGED, status="Online")
            
            GUI->>EventBus: Receive events
            GUI->>GUI: Exit degraded mode
            GUI-->>User: Show dashboard (connected)
            deactivate Service
        end
    end
    
    deactivate GUI
```

---

## 4. Configuration Change Flow

### Scenario: User updates server URL in GUI

```mermaid
sequenceDiagram
    actor User
    participant Page as Setup Page
    participant Config as ClientConfig
    participant EventBus as Qt EventBus
    participant Service as Client Service
    participant API as pyWATS API
    participant Server as WATS Server

    User->>Page: Edit server URL
    User->>Page: Click "Save"
    activate Page
    
    Page->>Page: Validate input
    
    alt Validation Success
        Page->>Config: set("server_url", new_url)
        activate Config
        Config->>Config: Update in-memory
        Config->>Config: Write to config.json
        Config-->>Page: Success
        deactivate Config
        
        Page->>EventBus: publish(CONFIG_CHANGED, key="server_url")
        deactivate Page
        
        EventBus->>Service: _on_config_changed(data)
        activate Service
        Service->>Service: Reload configuration
        Service->>Service: Disconnect current API client
        
        Service->>API: Initialize new client with new URL
        activate API
        API->>Server: Test connection (GET /version)
        activate Server
        
        alt Connection Success
            Server-->>API: 200 OK + version
            deactivate Server
            API-->>Service: Client ready
            deactivate API
            
            Service->>EventBus: publish(API_CLIENT_READY, client=api)
            Service->>EventBus: publish(CONNECTION_CHANGED, status="Online")
            
            EventBus->>Page: _on_connection_changed(data)
            Page->>Page: Update status indicator
            Page-->>User: Show "Connected to new server"
            deactivate Service
        
        else Connection Failure
            Server-->>API: Connection timeout
            deactivate Server
            API->>API: raise ConnectionError
            API-->>Service: ConnectionError
            deactivate API
            
            Service->>Service: Log error with exc_info
            Service->>EventBus: publish(CONNECTION_ERROR, error=str(e))
            Service->>EventBus: publish(CONNECTION_CHANGED, status="Offline")
            
            EventBus->>Page: _on_connection_error(data)
            Page->>Page: Show error banner
            Page-->>User: Show "Failed to connect to new server"
            deactivate Service
        end
    
    else Validation Failure
        Page->>Page: Show validation error
        Page-->>User: Show "Invalid URL format"
        deactivate Page
    end
```

---

## 5. Exception Propagation Flow

### Scenario: Authentication error from API to UI

```mermaid
flowchart TD
    Start([User Action:<br/>Load Reports])
    
    Start --> UICall[UI Page calls<br/>api.report.list]
    
    UICall --> APISync[pyWATS.report.list<br/>sync wrapper]
    
    APISync --> APIAsync[SyncReportService<br/>calls async service]
    
    APIAsync --> HTTPClient[AsyncHttpClient.get<br/>/api/reports]
    
    HTTPClient --> HTTPRequest{HTTP Request}
    
    HTTPRequest -->|401 Unauthorized| HTTPError["HTTP Client:<br/>raise AuthenticationError"]
    
    HTTPError --> AsyncCatch["Async Service:<br/>NO CATCH<br/>(re-raise)"]
    
    AsyncCatch --> SyncCatch["Sync Wrapper:<br/>NO CATCH<br/>(re-raise)"]
    
    SyncCatch --> UITry["UI Page:<br/>try/except block"]
    
    UITry --> UIHandle["handle_error(e, 'loading reports')"]
    
    UIHandle --> ErrorMixin["ErrorHandlingMixin<br/>checks exception type"]
    
    ErrorMixin --> ShowDialog["QMessageBox.warning<br/>'Authentication Error<br/>Please reconnect'"]
    
    ShowDialog --> LogError["Logger.warning<br/>'Auth error while loading reports'<br/>exc_info=True"]
    
    LogError --> UserSees["User sees dialog<br/>+ option to reconnect"]
    
    style HTTPError fill:#f96
    style UIHandle fill:#9f6
    style ShowDialog fill:#69f
    style LogError fill:#fc9
```

---

## 6. Event System Integration Flow

### Scenario: External IPC-CFX message triggers GUI update

```mermaid
sequenceDiagram
    participant CFX as IPC-CFX Device
    participant Transport as CFX Transport
    participant EventBus as Protocol EventBus
    participant Handler as TestResultHandler
    participant AppBus as Application EventBus
    participant GUI as GUI Dashboard

    CFX->>Transport: IPC-CFX Message<br/>(TestExecuted)
    activate Transport
    Transport->>Transport: Parse CFX message
    Transport->>Transport: Create Event object
    
    Transport->>EventBus: publish(event)
    activate EventBus
    EventBus->>Handler: Get handlers for TEST_RESULT
    
    EventBus->>Handler: handle(event)
    activate Handler
    
    Handler->>Handler: Extract test data
    Handler->>Handler: Store in database
    Handler->>Handler: Update statistics
    
    Handler->>AppBus: publish(DATA_CHANGED)
    Note over Handler,AppBus: Bridge between<br/>protocol events and<br/>application events
    
    Handler-->>EventBus: Complete
    deactivate Handler
    EventBus-->>Transport: Event processed
    deactivate EventBus
    deactivate Transport
    
    AppBus->>GUI: Emit data_changed signal
    activate GUI
    GUI->>GUI: Refresh dashboard
    GUI->>GUI: Update test count
    GUI->>GUI: Update charts
    GUI-->>GUI: UI updated
    deactivate GUI
```

---

## 7. Async Operation Flow (BasePage)

### Scenario: Page runs async API call without blocking UI

```mermaid
sequenceDiagram
    participant User
    participant Page as BasePage
    participant Runner as AsyncTaskRunner
    participant Qt as Qt Event Loop
    participant Thread as Worker Thread
    participant API as pyWATS API

    User->>Page: Click "Refresh"
    activate Page
    
    Page->>Page: run_async(self._load_data())
    
    Page->>Runner: submit_task(coroutine, "load_data")
    activate Runner
    
    Runner->>Runner: Generate task_id
    Runner->>Page: Emit task_started(task_id, "load_data")
    
    Page->>Page: _on_task_started()
    Page->>Page: Show loading indicator
    Page-->>User: Show loading spinner
    
    Runner->>Thread: QThreadPool.start(worker)
    activate Thread
    
    Thread->>Thread: asyncio.run(coroutine)
    Thread->>API: await api.report.list()
    activate API
    API-->>Thread: List[Report]
    deactivate API
    
    Thread->>Thread: Create TaskResult(success=True, data=reports)
    Thread->>Qt: QMetaObject.invokeMethod(emit_finished)
    deactivate Thread
    
    Qt->>Runner: Emit task_finished(result)
    Runner->>Page: Emit task_finished(result)
    deactivate Runner
    
    Page->>Page: _on_task_finished(result)
    
    alt result.success
        Page->>Page: on_complete callback
        Page->>Page: Update table with reports
        Page->>Page: Hide loading indicator
        Page-->>User: Show report list
    else result.error
        Page->>Page: on_error callback
        Page->>Page: handle_error(result.error)
        Page->>Page: Hide loading indicator
        Page-->>User: Show error dialog
    end
    
    deactivate Page
```

---

## 8. Correlation ID Flow

### Scenario: Request tracking from UI through all layers

```mermaid
flowchart LR
    subgraph UI["UI Layer"]
        A[User clicks<br/>'Get Product'] --> B[run_async call]
    end
    
    subgraph API["API Layer"]
        B --> C[pyWATS.product.get]
        C --> D["generate_correlation_id<br/>→ 'a3b2c1d4'"]
        D --> E[Store in context_var]
        E --> F[AsyncHttpClient.get]
    end
    
    subgraph HTTP["HTTP Request"]
        F --> G["Add header:<br/>X-Correlation-ID: a3b2c1d4"]
        G --> H[Send to server]
    end
    
    subgraph Logging["Logging (all layers)"]
        I["Logger.info<br/>extra={'correlation_id': 'a3b2c1d4'}"]
    end
    
    D -.->|Context propagation| I
    F -.->|Log request| I
    
    subgraph Response["Server Response"]
        H --> J["Response headers:<br/>X-Correlation-ID: a3b2c 1d4"]
    end
    
    J --> K[Extract product data]
    K --> L[Return to UI]
    
    subgraph ErrorCase["Error Path"]
        M[Exception raised] --> N["Logger.error<br/>exc_info=True<br/>correlation_id='a3b2c1d4'"]
        N --> O["Stack trace<br/>+ correlation ID<br/>in logs"]
    end
    
    H -.->|If error| M
    
    style D fill:#9f6
    style I fill:#fc9
    style N fill:#f96
    style O fill:#f96
```

---

**Last Updated:** February 8, 2026
