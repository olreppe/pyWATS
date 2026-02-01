# TDM API and Integration Guide

## Overview

The TDM (Test Data Management) API is the core interface for interacting with the WATS server. This document explains the API architecture, initialization, methods, and integration patterns.

---

## API Architecture

### Class Hierarchy

```
Interface.TDM (Base API - in Interface.TDM.dll)
    │
    ├─► Properties
    │   ├─► ServerAddress
    │   ├─► DataDir
    │   ├─► Status (Online/Offline/Error/etc.)
    │   └─► ClientInfo
    │
    ├─► Report Creation Methods
    │   ├─► CreateUUTReport()
    │   ├─► CreateUURReport()
    │   └─► CreateReport()
    │
    ├─► Submission Methods
    │   ├─► Submit()
    │   ├─► SubmitSync()
    │   └─► SubmitAsync()
    │
    └─► Server Communication
        ├─► Ping()
        ├─► ConnectServer()
        ├─► UpdateClientInfo()
        └─► DownloadMetadata()

TDM_ClientService (Service-specific extensions)
    │
    └─► Additional Methods
        ├─► CheckRemoteServer()
        ├─► CheckTransferingTimeout()
        ├─► PostClientLog()
        └─► SubmitFromFile()
```

---

## Initialization

### Initialization Modes

```csharp
public enum InitializationMode
{
    /// <summary>
    /// Initialize API, connect to server synchronously
    /// Blocks until connection established or timeout
    /// </summary>
    Synchronous,
    
    /// <summary>
    /// Initialize API, connect to server asynchronously
    /// Returns immediately, connection happens in background
    /// </summary>
    Asynchronous,
    
    /// <summary>
    /// Initialize API configuration only, do not connect
    /// </summary>
    NoConnection
}
```

### Service Initialization

**Service Startup**:
```csharp
// In ClientSvc.OnStart()
api = new TDM_ClientService();
api.InitializeAPI(
    InitializationMode.Synchronous,
    tryConnect: true
);
```

**Initialization Steps**:
```
1. Load configuration from:
   ├─► Registry: HKLM\SOFTWARE\Virinco\WATS
   └─► File: %ProgramData%\Virinco\WATS\WATS_WCF.config

2. IF tryConnect:
   ├─► Connect to server (HTTP/HTTPS)
   ├─► Authenticate with API key
   ├─► Download metadata:
   │   ├─► Test codes
   │   ├─► Operation types
   │   ├─► Failure codes
   │   └─► User-defined fields
   └─► Set Status: Online/Offline/Error

3. Initialize statistics tracking

4. Set up event handlers:
   └─► StatusChanged event

5. Return Status
```

### PendingWatcher Initialization

**Async Background**:
```csharp
// In PendingWatcher (separate thread)
api = new TDM_ClientService();
api.InitializeAPI(
    InitializationMode.Asynchronous,
    tryConnect: false
);
```

This allows the PendingWatcher to use API methods without blocking service startup.

---

## Status States

### APIStatusType Enumeration

```csharp
public enum APIStatusType
{
    Unknown = 0,
    
    /// <summary>
    /// Successfully connected and authenticated
    /// </summary>
    Online = 1,
    
    /// <summary>
    /// Cannot reach server (network/server down)
    /// </summary>
    Offline = 2,
    
    /// <summary>
    /// Client not registered in WATS
    /// </summary>
    NotRegistered = 3,
    
    /// <summary>
    /// License/activation issue
    /// </summary>
    NotActivated = 4,
    
    /// <summary>
    /// Configuration missing or invalid
    /// </summary>
    NotInstalled = 5,
    
    /// <summary>
    /// Paused by user
    /// </summary>
    Paused = 6,
    
    /// <summary>
    /// Service stopped
    /// </summary>
    Stopped = 7,
    
    /// <summary>
    /// Critical error occurred
    /// </summary>
    Error = 8
}
```

### Status Transitions

```
Unknown (Initial)
    │
    ├─► InitializeAPI()
    │
    ├──► Online (Success)
    │    │
    │    ├──► Offline (Network lost, server down)
    │    │    └──► Online (Network restored)
    │    │
    │    ├──► NotActivated (License expired)
    │    │
    │    └──► NotRegistered (Client removed from server)
    │
    ├──► Offline (Cannot connect)
    │    └──► Online (Server available)
    │
    ├──► NotInstalled (Config missing)
    │
    └──► Error (Fatal error)
```

### StatusChanged Event

**Event Signature**:
```csharp
public event EventHandler<StatusChangedEventArgs> StatusChanged;
```

**Service Subscription**:
```csharp
// In ClientSvc.OnStart()
api.StatusChanged += api_StatusChanged;

void api_StatusChanged(object sender, StatusChangedEventArgs e)
{
    // Update service status file
    SaveStatus();
    
    // IF transition to Online:
    if (e.NewStatus == APIStatusType.Online)
    {
        // Trigger pending report submission
        tw?.CheckState();
    }
}
```

---

## Report Creation

### CreateUUTReport

**Purpose**: Create a Unit Under Test (UUT) report

**Signature**:
```csharp
public UUTReport CreateUUTReport(
    string serialNumber,
    string partNumber,
    string partRevision,
    TestResultType testResult = TestResultType.Passed
)
```

**Example**:
```csharp
var report = api.CreateUUTReport(
    serialNumber: "SN123456789",
    partNumber: "PN-9876",
    partRevision: "A.1",
    testResult: TestResultType.Passed
);

report.UUT.Batch = "Batch-2025-01";
report.StartDateTime = DateTime.Now.AddMinutes(-10);
report.ExecutionTime = 600; // 10 minutes

var root = report.GetRootSequenceCall();
root.SequenceName = "MainSequence";

var step = root.AddNumericLimitStep("Voltage");
step.StepType = StepType.NI_TestStand;
step.Status = StepStatusType.Passed;
step.Measurement = 5.0;
step.CompOperator = CompOperatorType.GELE;
step.LowLimit = 4.5;
step.HighLimit = 5.5;
```

### CreateUURReport

**Purpose**: Create a Unit Under Repair (UUR) report

**Signature**:
```csharp
public UURReport CreateUURReport(
    string serialNumber,
    string partNumber,
    string partRevision,
    int defectCode
)
```

**Example**:
```csharp
var report = api.CreateUURReport(
    serialNumber: "SN987654321",
    partNumber: "PN-1234",
    partRevision: "B.2",
    defectCode: 12345 // WATS defect code
);

report.UUR.Location = "Station-5";
report.StartDateTime = DateTime.Now.AddHours(-1);
report.Purpose = "Repair";

// Add repair actions
report.UUR.AddRepairAction(
    symptomCode: 100,
    actionCode: 200,
    result: "Success"
);
```

---

## Report Submission

### Submit Method

**Signature**:
```csharp
public SubmitResult Submit(
    Report report,
    SubmitMethod method = SubmitMethod.Automatic
)
```

**SubmitMethod Enumeration**:
```csharp
public enum SubmitMethod
{
    /// <summary>
    /// Submit immediately if online, queue if offline
    /// </summary>
    Automatic,
    
    /// <summary>
    /// Always queue to disk (*.queued)
    /// </summary>
    Queue,
    
    /// <summary>
    /// Force immediate submission, fail if offline
    /// </summary>
    Immediate
}
```

### Submission Flow

```
1. api.Submit(report, SubmitMethod.Automatic)
   │
2. Check API Status
   │
   ├─► IF Online:
   │   ├─► Serialize report to XML (WRML)
   │   ├─► HTTP POST to /api/report/submit
   │   ├─► Server validates and stores
   │   ├─► Return SubmitResult
   │   │   └─► Success: ReportId assigned
   │   └─► Update statistics
   │
   └─► IF Offline (or method = Queue):
       ├─► Serialize report to XML
       ├─► Generate GUID filename
       ├─► Save as {GUID}.queued
       │   └─► Location: %ProgramData%\Virinco\WATS\Reports\
       ├─► Return SubmitResult
       │   └─► Queued: No ReportId yet
       └─► Update statistics

3. PendingWatcher will submit queued reports when Online
```

### SubmitResult

**Structure**:
```csharp
public class SubmitResult
{
    /// <summary>
    /// True if successfully submitted to server or queued
    /// </summary>
    public bool Success { get; set; }
    
    /// <summary>
    /// Server-assigned report ID (0 if queued)
    /// </summary>
    public long ReportId { get; set; }
    
    /// <summary>
    /// Error message if Success = false
    /// </summary>
    public string ErrorMessage { get; set; }
    
    /// <summary>
    /// Indicates if report was queued for later submission
    /// </summary>
    public bool Queued { get; set; }
}
```

**Examples**:
```csharp
// Successful immediate submission
SubmitResult {
    Success = true,
    ReportId = 123456,
    Queued = false
}

// Queued for later (offline)
SubmitResult {
    Success = true,
    ReportId = 0,
    Queued = true
}

// Failed
SubmitResult {
    Success = false,
    ErrorMessage = "Invalid API key",
    Queued = false
}
```

---

## Server Communication

### Ping

**Purpose**: Check server connectivity and keep connection alive

**Signature**:
```csharp
public bool Ping()
```

**Behavior**:
```csharp
// Called every 5 minutes by service
bool isOnline = api.Ping();

// Internally:
// 1. HTTP GET to /api/ping
// 2. IF successful: Return true, Status = Online
// 3. IF failed: Return false, Status = Offline
```

### ConnectServer

**Purpose**: Force connection to server

**Signature**:
```csharp
public bool ConnectServer(
    bool forceReconnect = false,
    int timeoutSeconds = 30
)
```

**Usage**:
```csharp
// Force reconnect (every 1 hour)
api.ConnectServer(
    forceReconnect: true,
    timeoutSeconds: 5
);
```

### UpdateClientInfo

**Purpose**: Send client metadata to server

**Signature**:
```csharp
public void UpdateClientInfo()
```

**Data Sent**:
```xml
<ClientInfo>
  <ClientId>12345</ClientId>
  <ClientName>TestStation-001</ClientName>
  <MachineName>STATION-PC-001</MachineName>
  <IPAddress>192.168.1.100</IPAddress>
  <MACAddress>00-11-22-33-44-55</MACAddress>
  <OSVersion>Windows 10 Pro 21H2</OSVersion>
  <ServiceVersion>4.0.0.0</ServiceVersion>
  <Location>
    <Latitude>37.7749</Latitude>
    <Longitude>-122.4194</Longitude>
  </Location>
  <PendingReports>
    <Total>150</Total>
    <Queued>100</Queued>
    <Unprocessed>50</Unprocessed>
  </PendingReports>
</ClientInfo>
```

**Frequency**: Every 1 hour (tmr1hr_Elapsed)

### PostClientLog

**Purpose**: Upload diagnostic logs to server

**Signature**:
```csharp
public void PostClientLog()
```

**Behavior**:
- Compresses recent log entries
- HTTP POST to /api/client/log
- Server stores for troubleshooting

**Frequency**: Every 1 hour (tmr1hr_Elapsed)

---

## PendingWatcher Integration

### CheckTransferingTimeout

**Purpose**: Reset stuck transfer states

**Signature** (TDM_ClientService extension):
```csharp
public void CheckTransferingTimeout()
```

**Behavior**:
```
1. Find *.transferring files
   └─► Modified > 30 minutes ago

2. Find *.error files
   └─► Modified > 5 minutes ago

3. FOR EACH timed-out file:
   └─► Rename to *.queued
       └─► Will be retried on next submission
```

**Called By**: PendingWatcher (every 5 minutes)

### SubmitPendingReports

**Purpose**: Submit all queued reports

**Signature**:
```csharp
public int SubmitPendingReports()
```

**Process**:
```
1. Get all *.queued files in Reports directory

2. FOR EACH file:
   ├─► Rename: *.queued → *.transferring
   ├─► Load report from XML
   ├─► HTTP POST to server
   │
   ├─► IF success:
   │   ├─► Rename: *.transferring → *.transferred
   │   └─► Update statistics
   │
   └─► IF failure:
       └─► Rename: *.transferring → *.error
           └─► Will retry after 5 minutes

3. Delete *.transferred files

4. Return: Number of reports submitted
```

**Called By**: PendingWatcher (every 5 minutes when Online)

---

## Metadata Download

### Purpose

Download reference data from server for validation and UI display.

### Metadata Types

| Metadata | Endpoint | Frequency | Cached |
|----------|----------|-----------|--------|
| **Test Codes** | /api/codes/test | Startup + daily | Yes |
| **Failure Codes** | /api/codes/failure | Startup + daily | Yes |
| **Operation Types** | /api/codes/operations | Startup + daily | Yes |
| **User-Defined Fields** | /api/udf | Startup + on-demand | Yes |
| **Product Info** | /api/products/{pn} | On-demand | Yes |

### Cache Location

```
%ProgramData%\Virinco\WATS\Cache\
├─► TestCodes.xml
├─► FailureCodes.xml
├─► OperationTypes.xml
└─► UDF.xml
```

### Usage Example

```csharp
// Get test code by name
TestCode code = api.GetTestCode("Voltage_Check");
if (code != null)
{
    // Use code in report
    step.TestCodeId = code.Id;
}
```

---

## Configuration

### Registry Settings

**Location**: `HKLM\SOFTWARE\Virinco\WATS`

| Key | Type | Description | Default |
|-----|------|-------------|---------|
| **ServerAddress** | String | WATS server URL | (none) |
| **APIKey** | String | Authentication key | (none) |
| **ClientId** | DWORD | Numeric client ID | 0 |
| **Company** | String | Licensed company name | (none) |
| **DataDir** | String | Data directory path | `%ProgramData%\Virinco\WATS` |
| **MaxConversionWorkers** | DWORD | Max worker threads | 1 |

### Configuration File

**Location**: `%ProgramData%\Virinco\WATS\WATS_WCF.config`

**Structure**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <appSettings>
    <add key="ServerAddress" value="https://wats.example.com" />
    <add key="APIKey" value="ABC123..." />
    <add key="ClientName" value="TestStation-001" />
    <add key="Location" value="Building A, Floor 2" />
    <add key="EnableGPS" value="false" />
    <add key="LogLevel" value="Information" />
  </appSettings>
</configuration>
```

### Priority

```
1. Registry (highest priority)
2. WATS_WCF.config
3. Hardcoded defaults (lowest priority)
```

---

## Statistics Tracking

### Tracked Metrics

**Per Session (since startup)**:
- UUT reports submitted
- UUR reports submitted
- Total reports submitted
- Reports queued
- Conversion errors

**All Time**:
- Total UUT reports
- Total UUR reports
- Total reports

### Statistics.xml

**Structure**:
```xml
<Statistics>
  <overview>
    <Value key="UUTReportsSinceStartup">1100</Value>
    <Value key="UURReportsSinceStartup">134</Value>
    <Value key="UUTReportsToday">50</Value>
    <Value key="UURReportsToday">5</Value>
    <Value key="TotalReportsSent">12567</Value>
    <Value key="ServiceStartTime">2025-01-30T08:00:00</Value>
    <Value key="LastSubmissionTime">2025-01-30T14:32:15</Value>
  </overview>
  
  <converters>
    <converter name="TestStandConverter">
      <Value key="Converted">1000</Value>
      <Value key="Failed">5</Value>
      <Value key="AverageTimeMs">250</Value>
    </converter>
  </converters>
</Statistics>
```

---

## Error Handling

### Connection Errors

**Timeout**:
```csharp
try {
    api.Submit(report);
}
catch (TimeoutException ex) {
    // Server not responding
    // Report automatically queued
}
```

**Authentication Error**:
```csharp
// InitializeAPI returns status
if (api.Status == APIStatusType.NotActivated) {
    // Invalid API key or license
    // Check configuration
}
```

### Submission Errors

**Validation Error**:
```csharp
var result = api.Submit(report);
if (!result.Success) {
    // Server rejected report
    // ErrorMessage contains details
    Log.Error($"Submit failed: {result.ErrorMessage}");
}
```

**Network Error**:
```csharp
// Automatic retry:
// 1. Report saved as *.queued
// 2. PendingWatcher retries every 5 minutes
// 3. Up to 30-minute timeout, then reset
```

---

## Thread Safety

### API Instance Thread Safety

**TDM API**: Thread-safe for read operations, lock required for writes

**Locking Pattern**:
```csharp
lock (api)
{
    api.Submit(report);
    api.Ping();
    api.UpdateClientInfo();
}
```

**Service Implementation**:
```csharp
// Main service
TDM_ClientService api; // Shared instance

// PendingWatcher
TDM_ClientService api; // Separate instance (thread-safe)

// Converters
// Use shared api instance with locking
lock (api)
{
    api.Submit(report, SubmitMethod.Automatic);
}
```

---

## Best Practices

### 1. Use Appropriate InitializationMode

```csharp
// Service startup: Block until connected
api.InitializeAPI(InitializationMode.Synchronous, true);

// Background threads: Don't block
api.InitializeAPI(InitializationMode.Asynchronous, false);

// Offline scenarios: No connection
api.InitializeAPI(InitializationMode.NoConnection, false);
```

### 2. Handle All Status States

```csharp
switch (api.Status)
{
    case APIStatusType.Online:
        // Normal operations
        break;
    case APIStatusType.Offline:
        // Reports will queue automatically
        break;
    case APIStatusType.NotRegistered:
        // Contact administrator
        break;
    case APIStatusType.NotActivated:
        // Check license
        break;
    default:
        // Log error
        break;
}
```

### 3. Use SubmitMethod Appropriately

```csharp
// Normal use: Automatic
api.Submit(report, SubmitMethod.Automatic);

// Ensure immediate submission (e.g., critical data)
try {
    api.Submit(report, SubmitMethod.Immediate);
}
catch (Exception ex) {
    // Handle failure (report not queued)
}

// Force queuing (e.g., batch processing)
api.Submit(report, SubmitMethod.Queue);
```

### 4. Subscribe to StatusChanged

```csharp
api.StatusChanged += (sender, e) => {
    Log.Info($"Status changed: {e.OldStatus} → {e.NewStatus}");
    
    if (e.NewStatus == APIStatusType.Online) {
        // Trigger queued report submission
    }
};
```

---

## Summary

### Key Concepts

1. **InitializationMode**: Controls blocking vs. async initialization
2. **Status States**: Online/Offline/Error/etc. drive behavior
3. **Automatic Queuing**: Reports queue when offline, submit when online
4. **StatusChanged Event**: React to connection state changes
5. **Thread Safety**: Lock API for concurrent access
6. **Metadata Caching**: Codes and reference data cached locally
7. **Statistics Tracking**: Comprehensive metrics for monitoring

### API Usage Pattern

```csharp
// 1. Initialize
var api = new TDM_ClientService();
api.InitializeAPI(InitializationMode.Synchronous, true);

// 2. Subscribe to events
api.StatusChanged += HandleStatusChanged;

// 3. Create report
var report = api.CreateUUTReport("SN123", "PN456", "1.0");
// ... populate report ...

// 4. Submit
var result = api.Submit(report, SubmitMethod.Automatic);
if (result.Success) {
    if (result.Queued) {
        Log.Info("Report queued (offline)");
    } else {
        Log.Info($"Report submitted: ID {result.ReportId}");
    }
}
```

---

**Document Version**: 1.0  
**Last Updated**: January 30, 2025
