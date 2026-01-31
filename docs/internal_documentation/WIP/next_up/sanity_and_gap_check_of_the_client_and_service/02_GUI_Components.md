# GUI Components - WATS Client

## Overview

The WATS Client includes multiple GUI applications that interact with the Windows Service through shared XML files and service controller APIs. These applications provide user interfaces for monitoring, configuration, and management.

---

## GUI Applications

### 1. WATS Client Tray Icon

**Technology**: Win32 C++ Application  
**File**: `WATSTray.cpp`  
**Purpose**: System tray notification icon with status display

#### Architecture

```
WATS Tray Icon (WATSTray.exe)
│
├─► Notification Icon (System Tray)
│   ├─► Icon changes based on status
│   ├─► Tooltip shows statistics
│   └─► Right-click context menu
│
├─► File Watchers (2)
│   ├─► ServiceStatus.xml
│   └─► Statistics.xml
│
└─► Thread Model
    ├─► Main UI Thread (message pump)
    └─► Background Worker (file watching)
```

#### Features

**Context Menu Options**:
```
┌─────────────────────────────────┐
│ Open Status Monitor             │
│ Open Yield Monitor               │
│ Open Package Manager             │
│ Open Configurator                │
├─────────────────────────────────┤
│ About                            │
│ Exit                             │
└─────────────────────────────────┘
```

**Icon States**:
| Status | Icon | Color |
|--------|------|-------|
| Online | Green checkmark | Green |
| Offline | Yellow warning | Yellow |
| Error | Red X | Red |
| Stopped | Gray | Gray |

**Tooltip Format**:
```
WATS Client
Status: Online
Pending: 5
Total: 1,234 (1,100 UUT, 134 UUR)
```

#### File Watching Implementation

**Watch Handles**:
```cpp
waitHandles[0]: exitEvent - Signal to terminate
waitHandles[1]: changeHandle1 - Directory change notification
```

**Watched Directory**:
```
%ProgramData%\Virinco\WATS\
```

**Monitored Files**:
1. **ServiceStatus.xml**
   - Client status (Online/Offline/Error)
   - Pending report count
   - Converter states

2. **Statistics.xml**
   - UUT reports since startup
   - UUR reports since startup
   - Total reports

**Update Mechanism**:
```cpp
void watchStatus() {
    while (!completed) {
        // Wait for file change or exit signal
        DWORD waitResult = WaitForMultipleObjects(2, waitHandles, FALSE, INFINITE);
        
        if (waitResult == WAIT_OBJECT_0) {
            // Exit signal
            break;
        }
        else if (waitResult == WAIT_OBJECT_0 + 1) {
            // File changed
            Sleep(100); // Allow file write to complete
            status_t status = GetStatus();
            setNotificationStatus(status);
            
            // Reset change notification
            FindNextChangeNotification(changeHandle1);
        }
    }
}
```

**Retry Logic**:
```cpp
// XML loading with retry (max 5 attempts)
int attempt = 0;
bool loaded = false;
while (!loaded) {
    attempt++;
    doc.LoadFile(fpath);
    loaded = !doc.Error();
    if (!loaded) {
        if (attempt > 5) break;
        Sleep(5); // Wait 5ms between retries
    }
}
```

#### Status Parsing

**ServiceStatus.xml Parsing**:
```cpp
// Read client status
text = doc->FirstChildElement("WATS")
          ->FirstChildElement("ClientStatus")
          ->GetText();
// "Online", "Offline", "Paused", etc.

// Read pending count
XMLElement *p = doc->FirstChildElement("WATS")
                   ->FirstChildElement("pending");
p->QueryIntAttribute("total", &total);
```

**Statistics.xml Parsing**:
```cpp
XMLElement* e = doc->FirstChildElement("Statistics")
                   ->FirstChildElement("overview");
XMLElement *i = e->FirstChildElement("Value");
while (i != NULL) {
    const char* key = i->Attribute("key");
    if (strcmp(key, "UURReportsSinceStartup") == 0) {
        i->QueryIntText(&uur_count);
    }
    else if (strcmp(key, "UUTReportsSinceStartup") == 0) {
        i->QueryIntText(&uut_count);
    }
    i = i->NextSiblingElement("Value");
}
```

#### Launch Applications

**Launched Executables**:
```cpp
wsExecClientMonitor   = "WATS.Client.StatusMonitor.exe"
wsExecYieldMonitor    = "WATS.Client.YieldMonitor.exe"
wsExecPackageManager  = "WATS.Client.PackageManager.exe"
wsExecConfigurator    = "WATS.Client.Configurator.exe"
```

**Launch Mechanism**:
```cpp
ShellExecute(NULL, _T("open"), path, NULL, NULL, SW_SHOWNORMAL);
```

---

### 2. WATS Client Status Monitor

**Technology**: WPF (.NET Framework 4.8)  
**Pattern**: MVVM (Model-View-ViewModel)  
**Project**: `WATS Client Status Monitor`

#### Architecture

```
StatusMonitor.exe
│
├─► Views (XAML)
│   ├─► ClientMonitor.xaml (Main Window)
│   ├─► About.xaml
│   └─► UserControls/
│       └─► Log.xaml
│
├─► ViewModels
│   ├─► ClientMonitorViewModel.cs
│   ├─► LogViewModel.cs
│   └─► ViewModelLocator.cs
│
└─► Model
    └─► TDMAPI (Interface.TDM)
```

#### ClientMonitorViewModel

**Responsibilities**:
- Monitor service status
- Display real-time statistics
- Show pending reports
- Display converter states
- Service control (start/stop/restart)

**File Watching**:
```csharp
FileSystemWatcher fsw = new FileSystemWatcher(
    api.DataDir, 
    "ServiceStatus.xml"
);
fsw.Changed += ServiceStatusFile_Changed;
fsw.EnableRaisingEvents = true;
```

**Timer-Based Updates**:
```csharp
Timer tmrUpdateStatus = new Timer(30000); // 30 seconds
tmrUpdateStatus.Elapsed += tmrUpdateStatus_Elapsed;

void tmrUpdateStatus_Elapsed() {
    UpdateServiceStatus();
    UpdateNotifyIcon();
    PendingReports = api.GetPendingReportCount() 
                   + api.GetPendingTSConversions();
}
```

**Properties (Data Binding)**:
```csharp
public int PendingReports { get; set; }
public string ClientStatus { get; set; }
public string APIStatus { get; set; }
public string ServiceStatus { get; set; }
public string LicensedToCompany { get; }
public string LicenseKey { get; }
```

#### Service Control

**ServiceController Integration**:
```csharp
ServiceController sc = new ServiceController("WATSClient");

// Check status
ServiceControllerStatus status = sc.Status;
// Running, Stopped, Paused, etc.

// Control operations
sc.Start();
sc.Stop();
sc.Pause();
sc.Continue();
sc.Refresh();
```

**Custom Commands**:
```csharp
// Service supports custom commands:
sc.ExecuteCommand(128); // ReloadConfig
sc.ExecuteCommand(129); // CheckConnection
sc.ExecuteCommand(130); // SubmitConnectionTestReport
```

---

### 3. WATS Client Configurator

**Technology**: WPF (.NET Framework 4.8)  
**Purpose**: Configure client settings, server connection

#### Features

1. **Server Configuration**
   - Server URL
   - Authentication settings
   - SSL/TLS options

2. **Client Settings**
   - Client name/identifier
   - Location settings
   - GPS coordinates

3. **Converter Management**
   - Enable/disable converters
   - Configure input directories
   - Set file patterns

4. **Advanced Settings**
   - Worker thread count
   - Timeout settings
   - Logging levels

#### Configuration Storage

**Registry Keys**:
```
HKLM\SOFTWARE\Virinco\WATS\
├─► Company (string)
├─► LicenseKey (string)
├─► MaxConversionWorkers (DWORD)
└─► DataDir (string)
```

**XML Configuration**:
```
%ProgramData%\Virinco\WATS\
├─► WATS_WCF.config (Main configuration)
├─► converters.xml (Converter definitions)
├─► ServiceStatus.xml (Read-only, generated)
└─► Statistics.xml (Read-only, generated)
```

---

### 4. WATS Client Yield Monitor

**Technology**: WPF (.NET Framework 4.8)  
**Purpose**: Display yield statistics and trends

#### Features

- Real-time yield calculations
- Test pass/fail statistics
- Graphical trend displays
- Date range filtering
- Export to Excel/PDF

---

### 5. WATS Client Package Manager

**Technology**: WPF (.NET Framework 4.8)  
**Purpose**: Manage package downloads for offline testing

#### Features

- Browse available packages
- Download package files
- Manage local cache
- Package versioning

---

## Communication Flow: GUI ↔ Service

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   GUI Applications                           │
└──────────┬──────────────────────────────────────────────────┘
           │
           ├─► READ: ServiceStatus.xml (every 30 seconds or on change)
           │   ├─► ClientStatus
           │   ├─► APIStatus
           │   ├─► PendingCount
           │   └─► ConverterStates
           │
           ├─► READ: Statistics.xml (every 30 seconds or on change)
           │   ├─► UUTReportsSinceStartup
           │   ├─► UURReportsSinceStartup
           │   └─► OtherStatistics
           │
           ├─► WRITE: WATS_WCF.config (on settings change)
           │   └─► Triggers service reload
           │
           └─► CONTROL: ServiceController API
               ├─► Start()
               ├─► Stop()
               ├─► Pause()
               ├─► Continue()
               └─► ExecuteCommand(code)
                   ├─► 128: ReloadConfig
                   ├─► 129: CheckConnection
                   └─► 130: SubmitConnectionTestReport

┌─────────────────────────────────────────────────────────────┐
│              WATS Client Service                             │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │ Every 1 minute (watchdog):                         │     │
│  │   WRITE: ServiceStatus.xml                         │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │ On statistics change:                              │     │
│  │   WRITE: Statistics.xml                            │     │
│  └────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │ FileSystemWatcher on WATS_WCF.config:              │     │
│  │   OnChanged → Reload configuration                 │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### XML File Specifications

#### ServiceStatus.xml

**Location**: `%ProgramData%\Virinco\WATS\ServiceStatus.xml`  
**Updated**: Every 1 minute (watchdog), on state changes  
**Readers**: Tray Icon, Status Monitor, Configurator

**Complete Structure**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<WATS>
  <!-- Service state: Running, Stopped, Paused -->
  <ServiceStatus>Running</ServiceStatus>
  
  <!-- API connection state: Online, Offline, Error, etc. -->
  <APIStatus>Online</APIStatus>
  
  <!-- Overall client status -->
  <ClientStatus>Online</ClientStatus>
  
  <!-- Error message if ClientStatus = Error -->
  <ClientError></ClientError>
  
  <!-- Pending reports summary -->
  <pending total="150" current="100" future="0" 
           unprocessed="50" senderror="0" loaderror="0">
    
    <!-- Individual converter states -->
    <converter name="TestStandConverter" state="Running" 
               version="1.0.0.0" total="80" error="0"/>
    <converter name="ATMLConverter" state="Running" 
               version="1.0.0.0" total="20" error="0"/>
  </pending>
</WATS>
```

**Attributes Explained**:
- `total`: Total pending (current + unprocessed)
- `current`: Currently queued for submission
- `future`: Reserved for future use
- `unprocessed`: Not yet converted
- `senderror`: Failed to send
- `loaderror`: Failed to load/convert

#### Statistics.xml

**Location**: `%ProgramData%\Virinco\WATS\Statistics.xml`  
**Updated**: On report submission  
**Readers**: Tray Icon, Yield Monitor

**Structure**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<Statistics>
  <overview>
    <Value key="UUTReportsSinceStartup">1100</Value>
    <Value key="UURReportsSinceStartup">134</Value>
    <Value key="UUTReportsToday">50</Value>
    <Value key="UURReportsToday">5</Value>
    <Value key="TotalReportsSent">12567</Value>
    <Value key="ServiceStartTime">2025-01-30T08:00:00</Value>
  </overview>
  
  <converters>
    <converter name="TestStandConverter">
      <Value key="Converted">1000</Value>
      <Value key="Failed">5</Value>
    </converter>
  </converters>
</Statistics>
```

---

## Update Frequencies

### File Update Intervals

| File | Writer | Update Trigger | Typical Frequency |
|------|--------|----------------|-------------------|
| **ServiceStatus.xml** | Service | Watchdog timer, state changes | Every 1 minute + on-demand |
| **Statistics.xml** | Service | Report submission | Variable (per report) |
| **WATS_WCF.config** | GUI apps | User saves settings | On-demand |
| **converters.xml** | GUI apps | User saves converter config | On-demand |

### GUI Polling Intervals

| Application | Method | Interval | What's Monitored |
|-------------|--------|----------|------------------|
| **Tray Icon** | FileSystemWatcher | Real-time | Directory changes |
| **Status Monitor** | FileSystemWatcher + Timer | Real-time + 30s | ServiceStatus.xml |
| **Configurator** | FileSystemWatcher + Timer | Real-time + 30s | ServiceStatus.xml |

---

## User Interaction Flows

### Flow 1: Check Service Status

```
User
  │
  └─► Look at Tray Icon
      ├─► Icon color indicates status
      └─► Hover for tooltip
          └─► Shows pending count & total
```

### Flow 2: View Detailed Status

```
User
  │
  └─► Right-click Tray Icon
      └─► Click "Open Status Monitor"
          └─► StatusMonitor.exe launches
              ├─► Loads ServiceStatus.xml
              ├─► Shows detailed converter states
              ├─► Displays pending counts
              └─► Auto-updates every 30s
```

### Flow 3: Change Configuration

```
User
  │
  └─► Right-click Tray Icon
      └─► Click "Open Configurator"
          └─► Configurator.exe launches
              ├─► Load current settings
              ├─► User modifies settings
              ├─► Click "Save"
              └─► WATS_WCF.config updated
                  └─► Service FileSystemWatcher triggered
                      └─► Service reloads config (500-1000ms delay)
```

### Flow 4: Control Service

```
User
  │
  └─► Open Status Monitor
      └─► Click "Stop Service" button
          └─► ServiceController.Stop()
              ├─► Service receives Stop command
              ├─► OnStop() executes
              │   ├─► Dispose timers
              │   ├─► Stop converters
              │   ├─► Stop PendingWatcher
              │   └─► Update ServiceStatus.xml
              └─► ServiceStatus: Stopped
                  └─► Tray icon updates to gray
```

---

## Threading in GUI Applications

### Tray Icon Threading

**Main Thread**:
- Windows message pump
- Context menu handling
- Notification icon updates

**Background Thread**:
- File watching loop (watchStatus)
- XML parsing
- Status updates

**Synchronization**:
```cpp
HANDLE exitEvent; // Signal to terminate watcher
```

### WPF Applications Threading

**UI Thread** (Dispatcher):
- Window rendering
- User input
- Data binding updates

**Background Threads**:
- FileSystemWatcher callbacks
- Timer callbacks
- ServiceController operations

**Thread Marshaling**:
```csharp
// Update UI from background thread
Application.Current.Dispatcher.Invoke(() => {
    // Update UI properties
    ClientStatus = newStatus;
});
```

---

## Security Considerations

### Permissions Required

**Tray Icon**:
- Read access to `%ProgramData%\Virinco\WATS\`
- Execute permissions for other GUI apps

**Status Monitor/Configurator**:
- Read/Write access to configuration files
- ServiceController access (requires elevation for some operations)
- Registry read/write access to `HKLM\SOFTWARE\Virinco\WATS`

### Elevation

**Operations Requiring Elevation**:
- Service start/stop/pause
- Modify registry under HKLM
- Modify configuration in ProgramData (depending on permissions)

**UAC Prompts**:
- Configurator may request elevation on launch
- Service control operations trigger UAC if not elevated

---

## Error Handling

### File Access Errors

**Retry Logic** (Tray Icon):
```cpp
// Retry up to 5 times with 5ms delay
// Handles file locks during write operations
```

**Exception Handling** (WPF):
```csharp
try {
    XDocument doc = XDocument.Load(filepath);
    // Parse...
}
catch (IOException) {
    // File locked, retry later
}
catch (XmlException) {
    // Malformed XML, use defaults
}
```

### Service Controller Errors

```csharp
try {
    sc.Start();
}
catch (InvalidOperationException) {
    // Service already running
}
catch (Win32Exception) {
    // Permission denied or service not found
}
```

---

## Summary

### Key Takeaways

1. **File-Based IPC**: XML files provide simple, reliable communication
2. **Real-Time Updates**: FileSystemWatcher for instant notifications
3. **Polling Backup**: 30-second timers ensure updates even if events missed
4. **Retry Logic**: Handles file locks during concurrent access
5. **Service Control**: Standard Windows ServiceController API
6. **Minimal Dependencies**: Each GUI app can run independently

### Communication Pattern

```
Service (Authority) ──► Writes status files
                        ├─► ServiceStatus.xml (every 1 min)
                        └─► Statistics.xml (on change)

GUI Apps (Observers) ──► Read status files
                        ├─► FileSystemWatcher (real-time)
                        └─► Timer polling (30s backup)
```

This architecture provides:
- **Decoupling**: GUIs don't need direct service communication
- **Reliability**: File system is the source of truth
- **Simplicity**: No complex IPC mechanisms
- **Debuggability**: Status visible in plain text XML files

---

**Document Version**: 1.0  
**Last Updated**: January 30, 2025
