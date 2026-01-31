# WATS Client & Service - Quick Reference Guide

This is a condensed reference guide for the WATS Client and Service architecture. For detailed information, see the full documentation files.

---

## System Components

| Component | Type | Purpose |
|-----------|------|---------|
| **WATS Client Service** | Windows Service | Main orchestrator, runs converters and manages queues |
| **TDM API** | .NET Library | Interface for WATS operations and server communication |
| **Conversion Engine** | Service Component | Manages file converters and worker threads |
| **PendingWatcher** | Service Component | Monitors and submits queued reports |
| **Tray Icon** | C++ Application | System tray status indicator |
| **Status Monitor** | WPF Application | Detailed status and control interface |
| **Configurator** | WPF Application | Settings and configuration editor |

---

## Startup Sequence (Summary)

```
1. Service Starts → Set StartPending
2. Initialize TDM API (sync, 2-10 sec)
3. Set Service Status: Running
4. Start 3 Timers (watchdog 1min, ping 5min, update 1hr)
5. Start PendingWatcher (async, background)
6. Initialize Converters (async, 5+ sec)
7. Start FileSystemWatchers (per converter)
8. Ready (total 7-15 sec)
```

---

## Threading Model

| Thread Type | Count | Purpose | Created When |
|-------------|-------|---------|--------------|
| Main Service | 1 | Windows service dispatcher | Service start |
| Watchdog Timer | 1 | Health check every 1 min | Service start |
| Ping Timer | 1 | Server ping every 5 min | Service start |
| Update Timer | 1 | Client update every 1 hr | Service start |
| PendingWatcher | 1 | Queue monitor | Service start |
| FileSystemWatchers | N | File detection (per converter) | Converter start |
| Worker Pool | 1-50 | File conversion (dynamic) | On-demand |

**Total Threads**: Minimum 7-10, Maximum 60+

---

## Critical Timers

| Timer | Interval | Handler | Actions |
|-------|----------|---------|---------|
| **Watchdog** | 60 seconds | wdt_Elapsed | Check converter/watcher state, SaveStatus() |
| **Ping** | 300 seconds (5 min) | tmr5m_Elapsed | Ping server, SaveStatus() |
| **Update Client** | 3600 seconds (1 hr) | tmr1hr_Elapsed | UpdateClientInfo(), PostClientLog() |
| **Pending Watcher** | 300 seconds (5 min) | tmr_Elapsed | SubmitPendingReports() |

---

## File States

```
Source File (*.xml, *.atml, etc.)
  ↓
InMemory (created in API)
  ↓
queued (offline, waiting to submit)
  ↓
transferring (sending to server)
  ↓
transferred (successfully sent) → Deleted
  
  OR
  
error (failed submission) → Reset to queued after 5 min
```

---

## Communication Patterns

### Service → Server (HTTP/HTTPS)

| Endpoint | Method | Frequency | Purpose |
|----------|--------|-----------|---------|
| /api/ping | GET | Every 5 minutes | Keep-alive, connectivity check |
| /api/client/update | POST | Every 1 hour | Update client metadata |
| /api/client/log | POST | Every 1 hour | Upload diagnostic logs |
| /api/report/submit | POST | On-demand | Submit test reports |
| /api/codes | GET | Startup + on-demand | Download metadata (test codes, etc.) |

### GUI ↔ Service (File-Based)

| File | Writer | Reader | Update Frequency |
|------|--------|--------|------------------|
| ServiceStatus.xml | Service | GUI apps | Every 1 min + on state change |
| Statistics.xml | Service | GUI apps | On report submission |
| WATS_WCF.config | GUI apps | Service | On settings save |
| converters.xml | GUI apps | Service | On converter config save |

**GUI Polling**: FileSystemWatcher (real-time) + 30-second timer (backup)

---

## API Status States

```
Unknown → InitializeAPI()
   ↓
   ├─ Online (success)
   │    ├─ Offline (network lost)
   │    ├─ NotActivated (license issue)
   │    └─ NotRegistered (client removed)
   │
   ├─ Offline (cannot connect)
   ├─ NotInstalled (config missing)
   └─ Error (fatal error)
```

---

## Worker Scaling

```
Pending Files    Workers
    0-10         1
   11-20         2
   21-30         3
   ...
  100-110        11 (if MaxConversionWorkers >= 11)
   500+          50 (absolute max)
```

**Formula**: `desiredWorkers = min((pending + 9) / 10, MaxConversionWorkers, 50)`

**Registry**: `HKLM\SOFTWARE\Virinco\WATS\MaxConversionWorkers`

---

## Converter Configuration

### converters.xml Structure

```xml
<converter name="TestStandConverter" 
           assembly="WATSStandardConverters" 
           class="Virinco.WATS.Converters.TestStandConverter">
  <Source>
    <Parameter name="Path">C:\WATS\Reports</Parameter>
    <Parameter name="Filter">*.xml</Parameter>
    <Parameter name="PostProcessAction">Archive</Parameter>
  </Source>
  <Destination>
    <Parameter name="Option1">value1</Parameter>
  </Destination>
</converter>
```

### PostProcessAction Values

| Value | Behavior |
|-------|----------|
| Delete | Delete source file after conversion (default) |
| Archive | Create ZIP and delete source |
| Move | Move to "Processed" subfolder |
| Error | Move to "Error" subfolder on failure |

---

## Report Creation Quick Start

### UUT Report

```csharp
var report = api.CreateUUTReport(
    serialNumber: "SN123456",
    partNumber: "PN-9876",
    partRevision: "A.1"
);

var root = report.GetRootSequenceCall();
var step = root.AddNumericLimitStep("Voltage");
step.StepType = StepType.NI_TestStand;
step.Status = StepStatusType.Passed;
step.Measurement = 5.0;
step.CompOperator = CompOperatorType.GELE;
step.LowLimit = 4.5;
step.HighLimit = 5.5;

var result = api.Submit(report, SubmitMethod.Automatic);
```

### UUR Report

```csharp
var report = api.CreateUURReport(
    serialNumber: "SN987654",
    partNumber: "PN-1234",
    partRevision: "B.2",
    defectCode: 12345
);

report.UUR.AddRepairAction(
    symptomCode: 100,
    actionCode: 200,
    result: "Success"
);

api.Submit(report);
```

---

## Submit Methods

| Method | Behavior |
|--------|----------|
| **Automatic** | Submit if online, queue if offline (default) |
| **Queue** | Always queue to disk (*.queued) |
| **Immediate** | Force immediate submission, fail if offline |

---

## Configuration Locations

| Item | Location |
|------|----------|
| **Registry** | `HKLM\SOFTWARE\Virinco\WATS\` |
| **Main Config** | `%ProgramData%\Virinco\WATS\WATS_WCF.config` |
| **Converters** | `%ProgramData%\Virinco\WATS\converters.xml` |
| **Service Status** | `%ProgramData%\Virinco\WATS\ServiceStatus.xml` (generated) |
| **Statistics** | `%ProgramData%\Virinco\WATS\Statistics.xml` (generated) |
| **Reports Queue** | `%ProgramData%\Virinco\WATS\Reports\` |

---

## Common Registry Settings

| Key | Type | Description | Default |
|-----|------|-------------|---------|
| ServerAddress | String | WATS server URL | (none) |
| APIKey | String | Authentication key | (none) |
| ClientId | DWORD | Client ID | 0 |
| Company | String | Licensed company | (none) |
| MaxConversionWorkers | DWORD | Max worker threads | 1 |

---

## Performance Characteristics

### Throughput

**Small Files (< 100 KB)**:
- 1 worker: 30-60 files/min
- 10 workers: 300-600 files/min

**Large Files (> 1 MB)**:
- 1 worker: 5-10 files/min
- 10 workers: 50-100 files/min

### Resource Usage

**Memory**:
- Base: ~50 MB
- Per worker: ~10 MB
- Per pending file: ~5 KB

**CPU**:
- Idle: < 1%
- Active (10 workers): 10-30%
- Peak (50 workers): 80-100%

---

## ServiceStatus.xml Structure

```xml
<WATS>
  <ServiceStatus>Running|Stopped|Paused</ServiceStatus>
  <APIStatus>Online|Offline|Error|...</APIStatus>
  <ClientStatus>Online|Offline|Paused|...</ClientStatus>
  <ClientError>Error description</ClientError>
  <pending total="150" current="100" future="0" 
           unprocessed="50" senderror="0" loaderror="0">
    <converter name="TestStandConverter" state="Running" 
               version="1.0" total="80" error="0"/>
  </pending>
</WATS>
```

---

## Error Handling

### Timeouts

| State | Timeout | Action |
|-------|---------|--------|
| .transferring | 30 minutes | Reset to .queued |
| .error | 5 minutes | Reset to .queued |
| Processing | 600 seconds | Reset and retry |

### Retry Logic

**File Lock**:
- Retry up to 5 times
- 5ms delay between retries

**Network Error**:
- Automatic queue to disk
- Retry every 5 minutes when online

---

## Service Control

### ServiceController Operations

```csharp
ServiceController sc = new ServiceController("WATSClient");

// Status
ServiceControllerStatus status = sc.Status;

// Control
sc.Start();
sc.Stop();
sc.Pause();
sc.Continue();

// Custom commands
sc.ExecuteCommand(128); // ReloadConfig
sc.ExecuteCommand(129); // CheckConnection
sc.ExecuteCommand(130); // SubmitConnectionTestReport
```

---

## Logging Levels

```csharp
TraceEventType.Critical      // Fatal errors, service stops
TraceEventType.Error         // Conversion failures
TraceEventType.Warning       // Recoverable issues
TraceEventType.Information   // State changes
TraceEventType.Verbose       // Debug info
```

---

## Common Troubleshooting

### Service won't start
- Check registry configuration
- Verify ServerAddress and APIKey
- Check DataDir permissions
- Review Windows Event Log

### Files not converting
- Check converter State (in ServiceStatus.xml)
- Verify Path exists and is accessible
- Check Filter pattern matches files
- Review converter logs

### Reports not submitting
- Check APIStatus (in ServiceStatus.xml)
- Verify network connectivity
- Check server accessibility (ping endpoint)
- Review queued reports count

### High CPU usage
- Check MaxConversionWorkers (reduce if too high)
- Review pending queue depth
- Check for large/complex files
- Monitor worker count

---

## Best Practices

### Worker Configuration

```
Low volume (< 100/day):      1-2 workers
Medium volume (100-1000):    5-10 workers
High volume (> 1000/day):    10-20 workers
Burst traffic:               20-50 workers
```

### Folder Structure

```
C:\WATS\
├─ TestStandReports\
│  ├─ Error\
│  └─ Archive\
├─ ATMLReports\
│  ├─ Error\
│  └─ Processed\
└─ CustomReports\
   ├─ Error\
   └─ Archive\
```

### API Usage

```csharp
// Always handle status
if (api.Status == APIStatusType.Online)
{
    // Safe to submit
}

// Use appropriate SubmitMethod
api.Submit(report, SubmitMethod.Automatic); // Normal use

// Lock for concurrent access
lock (api)
{
    api.Submit(report);
}
```

---

## Key Architectural Decisions

1. **File-Based IPC**: Simple, reliable GUI communication
2. **Dynamic Worker Scaling**: Efficient resource usage
3. **Queue-on-Offline**: No data loss when server unavailable
4. **FileSystemWatcher**: Real-time detection without polling
5. **Pluggable Converters**: Support any test system format

---

## Related Documents

- **[01_Architecture_Overview.md](01_Architecture_Overview.md)**: Complete architecture
- **[02_GUI_Components.md](02_GUI_Components.md)**: GUI applications
- **[03_Converters_And_Processing.md](03_Converters_And_Processing.md)**: Conversion system
- **[04_TDM_API_And_Integration.md](04_TDM_API_And_Integration.md)**: API reference

---

**Document Version**: 1.0  
**Last Updated**: January 30, 2025  
**Platform**: Windows, .NET 8.0 / .NET Framework 4.8
