# WATS Client & Service Architecture Documentation

## 📚 Documentation Index

This folder contains comprehensive documentation of the WATS (Web-based Automated Test System) Client and Service architecture. The documentation explains how the system works **without including source code**, focusing on architecture, threading, timers, communication patterns, and automatic processes.

---

## 📖 Documents

### [01_Architecture_Overview.md](01_Architecture_Overview.md)
**Complete system architecture documentation**

**Contents**:
- System architecture diagram and component overview
- Detailed startup sequence (11-step process)
- Main components (ClientSvc, TDM API, Conversion, PendingWatcher)
- Threading model (7+ thread types)
- Timers and intervals (4 timers with specific intervals)
- Communication patterns (HTTP, file-based, events)
- Data flow diagrams
- State management (service, API, converter, pending watcher)

**Key Information**:
- **Startup time**: 7-15 seconds typical
- **Threads**: 7-60+ threads (depending on load)
- **Timers**: 
  - Watchdog: 1 minute
  - Ping: 5 minutes
  - Update Client: 1 hour
  - Pending Watcher: 5 minutes

---

### [02_GUI_Components.md](02_GUI_Components.md)
**GUI applications and communication with service**

**Contents**:
- Tray Icon (Win32 C++ application)
- Status Monitor (WPF MVVM application)
- Configurator (WPF settings editor)
- Yield Monitor (statistics viewer)
- Package Manager (offline package management)
- GUI ↔ Service communication (file-based IPC)
- ServiceStatus.xml and Statistics.xml specifications
- Update frequencies and polling intervals
- Threading in GUI applications

**Key Information**:
- **Communication method**: XML files (ServiceStatus.xml, Statistics.xml)
- **Update frequency**: 
  - Service writes: Every 1 minute + on-demand
  - GUI reads: FileSystemWatcher (real-time) + 30s timer polling
- **Service control**: Windows ServiceController API

---

### [03_Converters_And_Processing.md](03_Converters_And_Processing.md)
**File conversion system and processing pipeline**

**Contents**:
- Converter architecture and lifecycle
- Configuration (converters.xml)
- File detection and queuing
- Worker thread allocation (dynamic scaling 1-50)
- Conversion processing steps
- IReportConverter interface
- Standard converters (TestStand, ATML, JSON)
- Error handling and logging
- Performance characteristics
- Best practices

**Key Information**:
- **Worker scaling**: 1 worker per 10 pending files (max 50)
- **Timeout**: 600 seconds (10 minutes) per file
- **Throttling**: Max 10,000 files per scan, 10 pending threshold
- **Supported formats**: TestStand XML, ATML, JSON, custom

---

### [04_TDM_API_And_Integration.md](04_TDM_API_And_Integration.md)
**TDM API architecture and integration guide**

**Contents**:
- API class hierarchy and architecture
- Initialization modes (Synchronous, Asynchronous, NoConnection)
- API status states and transitions
- Report creation methods (UUT, UUR)
- Report submission flow and SubmitResult
- Server communication (Ping, UpdateClientInfo, PostClientLog)
- PendingWatcher integration methods
- Metadata download and caching
- Configuration (registry and XML)
- Statistics tracking
- Error handling and thread safety
- Best practices

**Key Information**:
- **Initialization**: Sync (blocks), Async (background), NoConnection (offline)
- **Status states**: Online, Offline, NotRegistered, NotActivated, Error
- **Submit methods**: Automatic (queue if offline), Queue (force queue), Immediate (fail if offline)
- **Server endpoints**: /api/ping (5min), /api/client/update (1hr), /api/report/submit (on-demand)

---

## 🎯 Quick Reference

### System Overview

```
WATS Client Ecosystem
│
├─► WATS Client Service (Windows Service)
│   ├─► TDM API (server communication)
│   ├─► Conversion Engine (file processing)
│   │   ├─► Converters (N instances)
│   │   └─► Workers (1-50 threads)
│   └─► PendingWatcher (queue monitor)
│
├─► GUI Applications
│   ├─► Tray Icon (status display)
│   ├─► Status Monitor (detailed view)
│   ├─► Configurator (settings)
│   ├─► Yield Monitor (statistics)
│   └─► Package Manager (packages)
│
└─► File System
    ├─► Reports Directory (queued reports)
    ├─► Converter Directories (source files)
    └─► Status Files (ServiceStatus.xml, Statistics.xml)
```

### Critical Intervals

| Timer | Interval | Purpose |
|-------|----------|---------|
| **Watchdog** | 1 minute | Health check, status update |
| **Ping** | 5 minutes | Server connectivity check |
| **Update Client** | 1 hour | Registration, log upload |
| **Pending Watcher** | 5 minutes | Submit queued reports |
| **GUI Polling** | 30 seconds | Read status files |

### Threading Summary

| Thread Type | Count | Purpose |
|-------------|-------|---------|
| **Main Service** | 1 | Service message pump |
| **Watchdog Timer** | 1 | Health monitoring |
| **Ping Timer** | 1 | Server ping |
| **Update Timer** | 1 | Client registration |
| **Pending Watcher** | 1 | Queue processing |
| **FileSystemWatchers** | N | File detection (per converter) |
| **Worker Pool** | 1-50 | File conversion (dynamic) |

**Total**: Minimum 7-10 threads, maximum 60+ threads

### Communication Patterns

#### Service → Server (HTTP/HTTPS)
```
/api/ping               - Every 5 minutes
/api/client/update      - Every 1 hour
/api/client/log         - Every 1 hour
/api/report/submit      - On-demand (queued reports)
/api/codes              - Startup + on-demand
```

#### GUI ↔ Service (File-Based)
```
Service writes:
  ServiceStatus.xml     - Every 1 minute + on state change
  Statistics.xml        - On report submission

GUI reads:
  ServiceStatus.xml     - FileSystemWatcher + 30s timer
  Statistics.xml        - FileSystemWatcher + 30s timer

GUI writes:
  WATS_WCF.config       - On settings save
  converters.xml        - On converter config save
```

### File States

```
Source File (*.xml, *.atml, etc.)
  → .InMemory (created in API)
  → .queued (offline, waiting)
  → .transferring (sending to server)
  → .transferred (successfully sent)
  → .error (failed, will retry after 5 min)
```

### Worker Scaling

```
Pending files:    Workers:
  0-10            1
  11-20           2
  21-30           3
  ...
  100-110         11 (if MaxConversionWorkers >= 11)
  500+            50 (absolute maximum)
```

**Registry Setting**:
```
HKLM\SOFTWARE\Virinco\WATS\MaxConversionWorkers
```

---

## 🔍 Finding Information

### "How does the service start?"
→ See [01_Architecture_Overview.md](01_Architecture_Overview.md#startup-sequence)

### "What threads are created?"
→ See [01_Architecture_Overview.md](01_Architecture_Overview.md#threading-model)

### "What timers are running and how often?"
→ See [01_Architecture_Overview.md](01_Architecture_Overview.md#timers-and-intervals)

### "How does the GUI connect to the service?"
→ See [02_GUI_Components.md](02_GUI_Components.md#communication-flow-gui--service)

### "What automatic processes run?"
→ See [01_Architecture_Overview.md](01_Architecture_Overview.md#timers-and-intervals)

### "How are files converted?"
→ See [03_Converters_And_Processing.md](03_Converters_And_Processing.md#conversion-processing)

### "How do I create a custom converter?"
→ See [03_Converters_And_Processing.md](03_Converters_And_Processing.md#ireportconverter-interface)

### "What happens when service is offline?"
→ See [01_Architecture_Overview.md](01_Architecture_Overview.md#data-flow)

### "How many threads can run simultaneously?"
→ See [01_Architecture_Overview.md](01_Architecture_Overview.md#summary) (Minimum 7-10, Maximum 60+)

### "How do I use the TDM API?"
→ See [04_TDM_API_And_Integration.md](04_TDM_API_And_Integration.md)

### "How do I create and submit reports?"
→ See [04_TDM_API_And_Integration.md](04_TDM_API_And_Integration.md#report-creation)

### "What happens to queued reports?"
→ See [04_TDM_API_And_Integration.md](04_TDM_API_And_Integration.md#pendingwatcher-integration)

---

## 💡 Key Architectural Decisions

### 1. File-Based GUI Communication
**Why**: Simple, reliable, no complex IPC needed  
**Trade-off**: Slight delay (up to 30s for polling updates)  
**Benefit**: GUI apps can run independently, easy debugging

### 2. Dynamic Worker Scaling
**Why**: Efficient resource usage  
**Trade-off**: Complexity in worker management  
**Benefit**: Handles both low and high volume efficiently

### 3. Queue-on-Offline
**Why**: No data loss when server unavailable  
**Trade-off**: Disk space for queued files  
**Benefit**: Reliable reporting, automatic retry

### 4. FileSystemWatcher for File Detection
**Why**: Real-time detection without polling  
**Trade-off**: OS-dependent, can miss rapid changes  
**Benefit**: Low CPU overhead, instant response

### 5. Pluggable Converter Architecture
**Why**: Extensibility without modifying service  
**Trade-off**: Learning curve for custom converters  
**Benefit**: Support any test system format

---

## 📊 Performance Characteristics

### Typical Performance

**Small Files (< 100 KB)**:
- 1 worker: 30-60 files/minute
- 10 workers: 300-600 files/minute

**Large Files (> 1 MB)**:
- 1 worker: 5-10 files/minute
- 10 workers: 50-100 files/minute

### Resource Usage

**Memory**:
- Base service: ~50 MB
- Per worker: ~10 MB
- Per pending file: ~5 KB

**CPU**:
- Idle: < 1%
- Active (10 workers): 10-30%
- Peak (50 workers): 80-100%

---

## 🛠️ Configuration Files

| File | Location | Purpose |
|------|----------|---------|
| **WATS_WCF.config** | `%ProgramData%\Virinco\WATS\` | Main configuration |
| **converters.xml** | `%ProgramData%\Virinco\WATS\` | Converter definitions |
| **ServiceStatus.xml** | `%ProgramData%\Virinco\WATS\` | Service status (generated) |
| **Statistics.xml** | `%ProgramData%\Virinco\WATS\` | Statistics (generated) |
| **Registry** | `HKLM\SOFTWARE\Virinco\WATS\` | System settings |

---

## 🔐 Security & Permissions

### Required Permissions

**Service**:
- Read/Write: `%ProgramData%\Virinco\WATS\`
- Read/Write: Converter input directories
- Network: HTTP/HTTPS to WATS server
- Registry: Read/Write `HKLM\SOFTWARE\Virinco\WATS\`

**GUI Applications**:
- Read: `%ProgramData%\Virinco\WATS\` (status files)
- Write: `%ProgramData%\Virinco\WATS\` (configuration)
- ServiceController: Requires elevation for start/stop/pause

---

## 📝 Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | January 30, 2025 | Initial documentation |

---

## 📞 Document Scope

This documentation covers:
- ✅ System architecture and design
- ✅ Threading model and concurrency
- ✅ Timers and automatic processes
- ✅ Communication patterns
- ✅ Data flow and state management
- ✅ Configuration and deployment
- ✅ Performance characteristics

This documentation does **NOT** include:
- ❌ Source code listings
- ❌ Complete API reference
- ❌ Deployment/installation procedures
- ❌ User manuals
- ❌ Troubleshooting guides

---

**Created for**: WATS Client project  
**Target audience**: Developers, architects, technical leads  
**Platform**: Windows, .NET 8.0 / .NET Framework 4.8  
**Document version**: 1.0
