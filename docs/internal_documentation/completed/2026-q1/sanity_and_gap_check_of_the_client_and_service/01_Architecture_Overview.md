# WATS Client & Service Architecture - Complete Documentation

## Overview

The WATS (Web-based Automated Test System) Client & Service is a Windows service-based architecture that manages test report conversion, queuing, and submission to a WATS server. The system consists of multiple components working together to provide reliable, automated test data management.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Startup Sequence](#startup-sequence)
3. [Main Components](#main-components)
4. [Threading Model](#threading-model)
5. [Timers and Intervals](#timers-and-intervals)
6. [Communication Patterns](#communication-patterns)
7. [Data Flow](#data-flow)
8. [State Management](#state-management)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     WATS Client Ecosystem                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐        ┌──────────────┐                   │
│  │  WATS Tray   │◄──────►│ Status Files │                   │
│  │   Icon (GUI) │        │   (XML)      │                   │
│  └──────────────┘        └──────────────┘                   │
│         │                        ▲                            │
│         │                        │                            │
│         ▼                        │                            │
│  ┌─────────────────────────────────────────────────────────┐│
│  │         WATS Client Service (Windows Service)           ││
│  ├─────────────────────────────────────────────────────────┤│
│  │  ┌──────────┐  ┌───────────┐  ┌──────────────────┐     ││
│  │  │  TDM API │  │Conversion │  │ PendingWatcher   │     ││
│  │  │ (Core)   │  │  Engine   │  │ (File Watcher)   │     ││
│  │  └────┬─────┘  └─────┬─────┘  └────────┬─────────┘     ││
│  │       │              │                   │                ││
│  │       │         ┌────▼────┐         ┌───▼───┐           ││
│  │       │         │Converter│         │ Timer │           ││
│  │       │         │ Workers │         │ (5min)│           ││
│  │       │         └─────────┘         └───────┘           ││
│  │       │                                                   ││
│  │  ┌────▼──────────────────────────────────────────┐      ││
│  │  │  3 System Timers:                             │      ││
│  │  │  • Watchdog (1 min)                           │      ││
│  │  │  • Ping (5 min)                               │      ││
│  │  │  • Update Client Info (1 hour)               │      ││
│  │  └───────────────────────────────────────────────┘      ││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                    │
│                          ▼                                    │
│              ┌──────────────────────┐                        │
│              │  Reports Directory   │                        │
│              │  File System Queues  │                        │
│              └──────────────────────┘                        │
│                          │                                    │
└──────────────────────────┼────────────────────────────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │  WATS Server   │
                  │  (HTTP/HTTPS)  │
                  └────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **WATS Client Service** | Main Windows service orchestrating all operations |
| **TDM API** | Core interface for WATS operations and server communication |
| **Conversion Engine** | Manages file converters and worker threads |
| **PendingWatcher** | Monitors and processes queued reports |
| **WATS Tray Icon** | User interface showing service status |
| **Converter Workers** | Thread pool workers for parallel file processing |

---

## Startup Sequence

### Phase 1: Service Initialization (OnStart)

```
1. SERVICE STARTS
   ├─► Start logical trace operation
   ├─► Log: "WATS Client Service starting"
   ├─► Set status: StartPending
   └─► Try update GPS position (if enabled)

2. API INITIALIZATION
   ├─► Create TDM_ClientService instance
   ├─► InitializeAPI(Synchronous, tryConnect=true)
   │   ├─► Load configuration from registry/files
   │   ├─► Connect to WATS server
   │   ├─► Download metadata (codes, operation types)
   │   └─► Set status: Online/Offline/Error
   ├─► Reset startup statistics counters
   └─► Log: "API Initialized"

3. SET SERVICE STATUS
   └─► ServiceStatus: Running

4. DELAYED STATUS REPORT (if Online)
   └─► Wait 60 seconds then report initial status
       (Allows converters to initialize first)

5. START WATCHDOG TIMER
   ├─► Interval: 60,000 ms (1 minute)
   ├─► Handler: wdt_Elapsed
   └─► Log: "Watchdog timer initialized"

6. START PING TIMER
   ├─► Interval: 300,000 ms (5 minutes)
   ├─► Handler: tmr5m_Elapsed
   └─► Log: "Ping timer configured (5min)"

7. START UPDATE CLIENT TIMER
   ├─► Interval: 3,600,000 ms (1 hour)
   ├─► Handler: tmr1hr_Elapsed
   └─► Log: "Update client timer configured (1hr)"

8. START PENDING WATCHER
   ├─► Create PendingWatcher(async=true)
   ├─► Initializes in background thread
   │   ├─► Creates own TDM API instance
   │   ├─► Watches *.queued files
   │   ├─► Starts 5-minute timer
   │   └─► Processes existing queued files
   └─► Log: "PendingWatcher started"

9. MONITOR SERVICE CONTROLLER
   └─► Get ServiceController reference for self-monitoring

10. REGISTER STATUS CHANGED EVENT
    └─► api.StatusChanged += api_StatusChanged

11. WATCH SETTINGS FILE
    ├─► Create FileSystemWatcher for settings
    ├─► Monitor: WATS_WCF.config changes
    └─► Auto-reload configuration on change

12. INITIALIZE CONVERTERS
    ├─► Create Conversion instance
    ├─► Queue async: InitializeConverters
    │   ├─► Load converters.xml
    │   ├─► Create converter instances
    │   ├─► Wait 5 seconds
    │   └─► Start all converters
    └─► Each converter starts FileSystemWatcher

13. COMPLETE STARTUP
    ├─► Call base.OnStart()
    ├─► Log: "WATS Client Service started"
    └─► Stop trace operation
```

### Timing Summary
- **Synchronous operations**: ~2-10 seconds (API init, server connect)
- **Asynchronous operations**: 5+ seconds (converters, pending watcher)
- **Total startup time**: 7-15 seconds typical

---

## Main Components

### 1. ClientSvc (Main Service Class)

**File**: `ClientSvc.cs`  
**Type**: Windows Service (ServiceBase)

**Responsibilities**:
- Service lifecycle management (start, stop, pause, continue)
- Timer orchestration
- Status file management
- Configuration monitoring
- Component coordination

**Key Properties**:
- `api` - TDM_ClientService instance
- `cnv` - Conversion engine
- `tw` - PendingWatcher
- `wdt` - Watchdog timer (1 minute)
- `tmrPing` - Ping timer (5 minutes)
- `tmrReg` - Registration/update timer (1 hour)
- `fswSettings` - Configuration file watcher

**Service States**:
- StartPending
- Running
- PausePending
- Paused
- ContinuePending
- StopPending
- Stopped

### 2. TDM_ClientService (API Wrapper)

**File**: `TDMAPI.cs`  
**Base**: `Interface.TDM`

**Purpose**: Service-specific extensions to TDM API

**Additional Methods**:
- `CheckRemoteServer()` - Force server connectivity check
- `CheckTransferingTimeout()` - Reset stuck transfer states
- `PostClientLog()` - Submit diagnostic logs
- `SubmitFromFile()` - Submit specific report file

**Timeout Handling**:
- **Transferring timeout**: 30 minutes → Reset to Queued
- **Error timeout**: 5 minutes → Reset to Queued

### 3. Conversion Engine

**File**: `Conversion.cs`

**Purpose**: Manages file converters and worker threads

**Key Components**:
```
Conversion
├─► cnvList (List<Converter>)
│   └─► Each converter:
│       ├─► Name, Version
│       ├─► File patterns to watch
│       ├─► FileSystemWatcher
│       └─► Pending items queue
│
├─► pending (Dictionary<string, ConversionItem>)
│   └─► All pending conversions by file path
│
├─► pending_queue (Queue<ConversionItem>)
│   └─► FIFO queue for processing
│
└─► workers (List<ConverterWorkerClass>)
    └─► Thread pool workers (1-50)
```

**Worker Scaling**:
```csharp
Desired Workers = (Pending Count + 9) / 10
// Examples:
// 1-10 pending   → 1 worker
// 11-20 pending  → 2 workers
// 21-30 pending  → 3 workers
// ...
// Max from registry: MaxConversionWorkers (default: 1)
// Absolute max: 50 workers
```

**Configuration**:
- Registry key: `HKLM\SOFTWARE\Virinco\WATS\MaxConversionWorkers`
- Default: 1 worker
- Range: 1-50

### 4. PendingWatcher

**File**: `PendingWatcher.cs`

**Purpose**: Monitor and submit queued reports

**States**:
- Created
- Initializing
- Running
- Stopping
- Disposed
- Paused

**Monitors**:
- `*.queued` files in Reports directory
- File system events (Changed, Renamed)
- Timer triggers (5 minutes)

**Process Flow**:
```
1. File System Event Triggered
   OR Timer Elapsed (5 min)
   
2. TryEnter(api) - Ensure exclusive access
   
3. IF successful:
   ├─► Disable FileSystemWatcher
   ├─► Check API status
   ├─► CheckTransferingTimeout()
   ├─► IF Online: SubmitPendingReports()
   ├─► Enable FileSystemWatcher
   └─► Exit monitor
   
4. IF already running:
   └─► Log "already running" and skip
```

**Timeout Handling**:
- **Transferring**: 30 minutes
- **Error**: 5 minutes
- Files stuck in these states are reset to Queued

### 5. Converter Workers

**File**: `ConverterWorkerClass.cs`

**Purpose**: Process conversion jobs in thread pool

**Lifecycle**:
```
1. Created
   └─► Queue work item: DoWork()

2. DoWork() Loop:
   WHILE not shutting down:
   ├─► GetNextFileToConvert(out item)
   ├─► IF file available:
   │   ├─► Process conversion
   │   ├─► Update state
   │   └─► Remove from pending
   └─► IF no files:
       └─► Sleep and retry

3. Shutdown
   ├─► ShutDownInProgress = true
   ├─► Complete current work
   └─► WorkerShutDown(self)
```

---

## Threading Model

### Thread Types

#### 1. Main Service Thread
**Purpose**: Windows Service dispatcher  
**Lifecycle**: Entire service lifetime  
**Responsibilities**:
- Service message handling
- Timer events
- Event handlers

#### 2. ThreadPool Workers (Dynamic: 1-50)
**Purpose**: File conversion processing  
**Created**: By Conversion.CheckWorkerStatus()  
**Managed**: By ConverterWorkerClass  
**Work Items**:
- Convert file from source format
- Process through converter
- Update pending queue

**Scaling Logic**:
```csharp
// Spawn 1 worker per 10 pending items
int desiredWorkers = (pendingCount + 9) / 10;
// Respect registry max
if (desiredWorkers > MaxConversionWorkers)
    desiredWorkers = MaxConversionWorkers;
// Never exceed 50
if (desiredWorkers > 50)
    desiredWorkers = 50;
```

#### 3. Timer Threads (3 dedicated)

**a) Watchdog Timer Thread (1 minute)**
```csharp
Timer: wdt
Interval: 60,000 ms
Handler: wdt_Elapsed()
Actions:
├─► cnv.CheckState()
├─► tw.CheckState()
└─► SaveStatus()
```

**b) Ping Timer Thread (5 minutes)**
```csharp
Timer: tmrPing
Interval: 300,000 ms
Handler: tmr5m_Elapsed()
Actions:
├─► api.Ping()
└─► SaveStatus()
```

**c) Update Client Timer Thread (1 hour)**
```csharp
Timer: tmrReg
Interval: 3,600,000 ms
Handler: tmr1hr_Elapsed()
Actions:
├─► SaveStatus()
├─► api.ConnectServer(true, 5sec timeout)
├─► api.UpdateClientInfo()
└─► api.PostClientLog()
```

#### 4. PendingWatcher Thread
**Purpose**: Report submission  
**Created**: Async during startup  
**Own TDM API Instance**: Yes (thread-safe)  
**Monitors**:
- FileSystemWatcher events
- 5-minute timer events

#### 5. Converter Initialization Thread
**Purpose**: Load and start converters  
**Created**: During service start  
**Lifecycle**: Completes after 5+ seconds  
**Work**:
- Load converters.xml
- Create converter instances
- Start FileSystemWatchers

#### 6. FileSystemWatcher Threads (N converters)
**Created**: One per active converter  
**Monitors**: Specific file patterns  
**Events**: Created, Changed, Renamed  
**Handler**: Queues files for conversion

### Thread Synchronization

#### Lock Objects
```csharp
// API operations
lock (api) { ... }

// Pending queue
lock (pending) { ... }

// Worker list
lock (workers) { ... }

// Converter list
lock (cnvList) { ... }
```

#### Monitor Usage
```csharp
// PendingWatcher uses Monitor for exclusive access
if (Monitor.TryEnter(api))
{
    try { /* Submit reports */ }
    finally { Monitor.Exit(api); }
}
```

### Thread Safety Concerns

**Critical Sections**:
1. **Pending Queue Access**: Must lock `pending` dictionary
2. **API Operations**: Must lock `api` for state changes
3. **Worker Management**: Must lock `workers` list
4. **Status Updates**: Synchronized through SaveStatus()

**Race Condition Prevention**:
- Monitor.TryEnter prevents concurrent SubmitPendingReports
- Locks prevent concurrent pending queue modification
- FileSystemWatcher disabled during submission

---

## Timers and Intervals

### Complete Timer Summary

| Timer | Interval | Purpose | Handler | Started When |
|-------|----------|---------|---------|--------------|
| **Watchdog** | 1 minute (60,000 ms) | Health check, state monitoring | wdt_Elapsed | OnStart |
| **Ping** | 5 minutes (300,000 ms) | Server connectivity check | tmr5m_Elapsed | OnStart |
| **Update Client** | 1 hour (3,600,000 ms) | Client registration update | tmr1hr_Elapsed | OnStart |
| **Pending Watcher** | 5 minutes (300,000 ms) | Submit queued reports | tmr_Elapsed | PendingWatcher.Start |
| **Config Reload** | 500-1000 ms (one-shot) | Delayed config reload | tmrReloadConfig_Elapsed | Config file change |
| **Converter Check** | 600 seconds | Timeout detection | (in CheckState) | Watchdog trigger |

### Timer Details

#### 1. Watchdog Timer (wdt)
```csharp
Interval: 60,000 ms (1 minute)
AutoReset: true
Enabled: Service running

Actions every 1 minute:
├─► cnv.CheckState()
│   ├─► Check all converters
│   ├─► Restart timed-out items (600 sec)
│   └─► Check worker status
├─► tw.CheckState()
│   ├─► Check PendingWatcher state
│   └─► Trigger transfer if offline→online
└─► SaveStatus()
    └─► Update ServiceStatus.xml
```

#### 2. Ping Timer (tmrPing)
```csharp
Interval: 300,000 ms (5 minutes)
AutoReset: true
Enabled: Service running

Actions every 5 minutes:
├─► lock(api) api.Ping()
│   └─► HTTP GET to server /api/ping
└─► SaveStatus()
    └─► Update status file
```

#### 3. Update Client Timer (tmrReg)
```csharp
Interval: 3,600,000 ms (1 hour)
AutoReset: true
Enabled: Service running

Actions every 1 hour:
├─► SaveStatus()
├─► api.ConnectServer(force=true, timeout=5sec)
├─► api.UpdateClientInfo()
│   ├─► Send client metadata
│   ├─► Machine info
│   ├─► Version info
│   └─► Pending counts
└─► api.PostClientLog()
    └─► Upload diagnostic logs
```

#### 4. PendingWatcher Timer
```csharp
Interval: 300,000 ms (5 minutes)
AutoReset: true
Enabled: PendingWatcher.Running

Actions every 5 minutes:
└─► StartPendingTransfer()
    ├─► CheckTransferingTimeout()
    └─► IF Online: SubmitPendingReports()
```

#### 5. Config Reload Timer
```csharp
Interval: 500-1000 ms (dynamic)
AutoReset: false
Enabled: On file change only

Actions (one-shot):
└─► ReloadConfig()
    ├─► Dispose converters
    ├─► Reinitialize API
    └─► Reload converters.xml
```

### Timer Coordination

```
Service Running
│
├─► Every 1 minute (Watchdog)
│   ├─► Check converter health
│   ├─► Check pending watcher health
│   └─► Update status
│
├─► Every 5 minutes (Ping + PendingWatcher)
│   ├─► Ping server
│   ├─► Submit queued reports
│   └─► Update status
│
└─► Every 1 hour (Update Client)
    ├─► Reconnect to server
    ├─► Update client info
    ├─► Post diagnostic logs
    └─► Update status
```

---

## Communication Patterns

### 1. Service → Server (HTTP/HTTPS)

**API Endpoints Used**:
```
Base URL: {ServerAddress from config}

• /api/ping
  Method: GET
  Frequency: Every 5 minutes
  Purpose: Keep-alive, check connectivity

• /api/client/update
  Method: POST
  Frequency: Every 1 hour
  Purpose: Update client metadata

• /api/client/log
  Method: POST
  Frequency: Every 1 hour
  Purpose: Upload diagnostic logs

• /api/report/submit
  Method: POST
  Frequency: On-demand (queued reports)
  Purpose: Submit test reports

• /api/codes
  Method: GET
  Frequency: On startup, on demand
  Purpose: Download metadata
```

**Connection States**:
```
Online ───────► Server responding, authenticated
   ▲            Reports submit immediately
   │
   ├──────────► Offline (network/server issue)
   │            Reports queue to disk
   │
   ├──────────► NotRegistered
   │            Client not activated
   │
   └──────────► NotActivated
                License/activation issue
```

### 2. GUI → Service (Status Files)

**ServiceStatus.xml Structure**:
```xml
<WATS>
  <ServiceStatus>Running|Stopped|Paused</ServiceStatus>
  <APIStatus>Online|Offline|Error|...</APIStatus>
  <ClientStatus>Online|Offline|Stopped|Paused|Not Registered</ClientStatus>
  <ClientError>Error description if status=ERROR</ClientError>
  <pending total="100" current="50" future="0" 
           unprocessed="50" senderror="0" loaderror="0">
    <converter name="TestStandConverter" state="Running" 
               version="1.0" total="30" error="0"/>
    <converter name="ATMLConverter" state="Running" 
               version="1.0" total="20" error="0"/>
  </pending>
</WATS>
```

**Update Frequency**:
- Every 1 minute (watchdog)
- Every 5 minutes (ping)
- On state change
- On pending count change

**Location**: 
```
%ProgramData%\Virinco\WATS\ServiceStatus.xml
```

### 3. FileSystemWatcher Patterns

**Converters** (Multiple watchers):
```csharp
// Each converter watches specific patterns
Path: {ConverterInputDirectory}
Filter: "*.xml" | "*.atml" | "*.csv" | etc.
Events: Created, Changed, Renamed

On Event:
└─► AddFile(fileInfo, converter)
    └─► Queue for conversion
```

**PendingWatcher** (Single watcher):
```csharp
Path: {ReportsDirectory}
Filter: "*.queued"
Events: Changed, Renamed

On Event:
└─► StartPendingTransfer()
    └─► Submit reports to server
```

**Settings Watcher**:
```csharp
Path: {DataDir}
Filter: "WATS_WCF.config"
Events: Changed

On Event:
└─► Schedule reload (500-1000ms delay)
    └─► Reinitialize service components
```

### 4. Inter-Component Communication

**Event-Based**:
```
api.StatusChanged Event
├─► Fired when: API status changes
├─► Subscribers: ClientSvc
└─► Action: SaveStatus()
```

**Shared State**:
```
ServiceStatus.xml
├─► Written by: ClientSvc
└─► Read by: Tray Icon, Status Monitor

Pending Queue
├─► Written by: Converters, PendingWatcher
└─► Read by: Worker threads
```

**Callback Pattern**:
```
Conversion.GetNextFileToConvert(out item)
├─► Called by: Worker threads
└─► Returns: Next pending file or null
```

---

## Data Flow

### Complete Data Flow Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                    Test Report Journey                         │
└───────────────────────────────────────────────────────────────┘

1. EXTERNAL FILE ARRIVAL
   │
   ├─► TestStand creates "Report123.xml"
   └─► Drops in: C:\WATS\TestStandReports\

2. FILE DETECTION
   │
   ├─► FileSystemWatcher (Converter) detects "Report123.xml"
   └─► Event: Created

3. CONVERSION QUEUING
   │
   ├─► Converter.AddFile(fileInfo)
   ├─► Create ConversionItem
   ├─► Add to pending Dictionary
   └─► Add to pending_queue

4. WORKER ALLOCATION
   │
   ├─► CheckWorkerStatus()
   ├─► Calculate desired workers
   └─► Spawn worker if needed

5. CONVERSION PROCESS
   │
   ├─► Worker: GetNextFileToConvert()
   ├─► Lock item (state = Processing)
   ├─► Converter.ProcessFile()
   │   ├─► Load XML
   │   ├─► Transform to WRML
   │   └─► Create UUTReport/UURReport
   ├─► api.Submit(report, SubmitMethod.Automatic)
   └─► Remove from pending

6. SUBMISSION DECISION
   │
   ├─► IF API Status = Online:
   │   ├─► Submit immediately (HTTP POST)
   │   ├─► Get confirmation
   │   └─► Archive source file
   │
   └─► ELSE (Offline):
       ├─► Save as {GUID}.queued
       ├─► Write to: %ProgramData%\Virinco\WATS\Reports\
       └─► Archive source file

7. QUEUED REPORT PROCESSING
   │
   ├─► PendingWatcher detects "*.queued" file
   │   OR 5-minute timer
   │
   ├─► IF API Status = Online:
   │   ├─► SubmitPendingReports()
   │   ├─► Rename: .queued → .transferring
   │   ├─► HTTP POST to server
   │   ├─► Rename: .transferring → .transferred
   │   └─► Archive/delete
   │
   └─► ELSE (Offline):
       └─► Wait for next trigger

8. ERROR HANDLING
   │
   ├─► IF submission fails:
   │   └─► Rename: .transferring → .error
   │       └─► Wait 5 minutes → Reset to .queued
   │
   └─► IF timeout (30 min):
       └─► Rename: .transferring → .queued
           └─► Retry
```

### File State Transitions

```
Source File (*.xml/etc)
    │
    ├─► [InMemory] ──► Processing
    │                      │
    │                      ├─► Success, Online
    │                      │   └─► Archived
    │                      │
    │                      └─► Success, Offline
    │                          └─► Saved as *.queued
    │
    └─► *.queued ──► *.transferring ──► *.transferred ──► Deleted
            │              │                  
            │              └─► (timeout 30min)
            │              └─► (error)
            │                      │
            └──────────────────────┴─► *.error ──► *.queued
                                                 (wait 5min)
```

### Report File Extensions and Meanings

| Extension | State | Meaning |
|-----------|-------|---------|
| `.InMemory` | Created | Report created, not yet saved |
| `.queued` | Waiting | Ready for submission |
| `.transferring` | In-progress | Currently being sent |
| `.transferred` | Complete | Successfully sent |
| `.error` | Failed | Submission failed, will retry |
| `.ConnectionTest` | Special | Connection test report |

---

## State Management

### Service States

**Lifecycle**:
```
Stopped
   │
   ├─► OnStart()
   │   └─► StartPending → Running
   │
Running
   │
   ├─► OnPause()
   │   └─► PausePending → Paused
   │
Paused
   │
   ├─► OnContinue()
   │   └─► ContinuePending → Running
   │
   └─► OnStop()
       └─► StopPending → Stopped
```

**State Actions**:

**Running**:
- All timers enabled
- Converters running
- PendingWatcher active
- Reports being processed

**Paused**:
- All timers disabled
- Converters stopped
- PendingWatcher paused
- No processing

**Stopped**:
- All components disposed
- No threads running
- Files remain queued

### API States

**State Machine**:
```
Unknown
   │
   ├─► InitializeAPI()
   │
   ├─► Online (Connected, authenticated)
   │
   ├─► Offline (Cannot reach server)
   │
   ├─► NotRegistered (Client not in database)
   │
   ├─► NotActivated (License/activation issue)
   │
   ├─► NotInstalled (Configuration missing)
   │
   └─► Error (Fatal error occurred)
```

**State Transitions**:
```
Online ←──────────► Offline
  │                    │
  │ (Ping timeout)     │ (Ping success)
  │                    │
  └────────────────────┘

Online ──► (Auth fail) ──► NotActivated

Online ──► (Not found) ──► NotRegistered

Any ──► (Exception) ──► Error
```

### Converter States

```
Created
   │
   ├─► Start()
   │   └─► Running
   │
Running
   │
   ├─► Stop()
   │   └─► Stopped
   │
   └─► Dispose()
       └─► Disposed
```

### PendingWatcher States

```
Created
   │
   ├─► Start(async)
   │   └─► Initializing → Running
   │
Running
   │
   ├─► Enabled = false
   │   └─► Paused
   │
   ├─► Enabled = true
   │   └─► Running
   │
   └─► Dispose()
       └─► Stopping → Disposed
```

### Conversion Item States

```
Pending
   │ (Worker picks up)
   │
Processing
   │ (Conversion complete)
   │
PostProcessing
   │ (Submission/archival)
   │
Done
   │ (Removed from queue)
   │
   └─► [Deleted]
```

---

## Summary

### Key Takeaways

1. **Asynchronous Architecture**: Most operations are non-blocking
2. **Fault Tolerant**: Automatic retries, timeout handling
3. **Scalable**: Dynamic worker thread allocation
4. **Monitored**: Multiple health checks and status reporting
5. **Configurable**: XML-based configuration, registry settings
6. **Resilient**: Offline queue, automatic reconnection

### Critical Intervals

- **1 minute**: Health check (watchdog)
- **5 minutes**: Ping + queue processing
- **1 hour**: Client update + log upload
- **5 minutes**: Converter item timeout check (in watchdog)
- **30 minutes**: Transfer timeout reset
- **5 minutes**: Error state reset

### Thread Count

**Minimum**: 7-10 threads
- 1 main service
- 3 timer threads
- 1 pending watcher
- 1-2 converter threads
- 1+ worker threads

**Maximum**: 60+ threads
- Up to 50 worker threads
- N converter FileSystemWatchers
- System timers
- Service infrastructure

---

**Document Version**: 1.0  
**Last Updated**: January 30, 2026  
**Target Platform**: Windows, .NET 8.0
