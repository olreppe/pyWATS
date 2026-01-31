# Converter System - WATS Client

## Overview

The WATS Client Converter System is a pluggable architecture that automatically transforms test report files from various formats into the WATS Report Model (WRML). Converters monitor designated folders, detect new files, and process them through worker threads.

---

## Converter Architecture

### System Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                     Conversion Engine                         │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Converters List (cnvList)                             │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │  ┌─────────────────┐  ┌─────────────────┐             │  │
│  │  │  TestStand      │  │  ATML           │             │  │
│  │  │  Converter      │  │  Converter      │   ... N     │  │
│  │  └─────────────────┘  └─────────────────┘             │  │
│  │  Each converter:                                       │  │
│  │  • Has own FileSystemWatcher                           │  │
│  │  • Monitors specific file patterns                     │  │
│  │  • Queues files to shared pool                         │  │
│  └────────────────────────────────────────────────────────┘  │
│                           │                                   │
│                           ▼                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Pending Queue (shared)                                │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │  Dictionary<filepath, ConversionItem>                  │  │
│  │  Queue<ConversionItem> (FIFO)                          │  │
│  └────────────────────────────────────────────────────────┘  │
│                           │                                   │
│                           ▼                                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Worker Pool (dynamic: 1-50 threads)                   │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │  [Worker 1] [Worker 2] ... [Worker N]                  │  │
│  │  • Pull items from queue                               │  │
│  │  • Process conversions                                 │  │
│  │  • Submit reports                                      │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Key Classes

| Class | Purpose |
|-------|---------|
| **Conversion** | Main conversion engine coordinator |
| **Converter** | Individual converter instance with file watcher |
| **ConversionItem** | Represents one file to be converted |
| **ConverterWorkerClass** | Thread pool worker for processing |
| **IReportConverter** | Interface implemented by converter plugins |
| **IReportConverter_v2** | Extended interface with parameters |

---

## Converter Configuration

### converters.xml

**Location**: `%ProgramData%\Virinco\WATS\converters.xml`

**Structure**:
```xml
<?xml version="1.0" encoding="utf-8"?>
<converters>
  <converter name="TestStandConverter" 
             assembly="WATSStandardConverters" 
             class="Virinco.WATS.Converters.TestStandConverter">
    
    <!-- Source: Where to find files -->
    <Source>
      <Parameter name="Path">C:\WATS\TestStandReports</Parameter>
      <Parameter name="Filter">*.xml</Parameter>
      <Parameter name="PostProcessAction">Archive</Parameter>
    </Source>
    
    <!-- Destination: Converter-specific parameters -->
    <Destination>
      <Parameter name="EnableXYZ">true</Parameter>
      <Parameter name="CustomOption">value</Parameter>
    </Destination>
  </converter>
  
  <converter name="ATMLConverter" 
             assembly="WATSStandardConverters" 
             class="Virinco.WATS.Converters.ATML.ATMLConverter">
    <Source>
      <Parameter name="Path">C:\WATS\ATMLReports</Parameter>
      <Parameter name="Filter">*.atml</Parameter>
      <Parameter name="PostProcessAction">Move</Parameter>
    </Source>
    <Destination>
      <!-- ATML-specific parameters -->
    </Destination>
  </converter>
</converters>
```

### Configuration Parameters

#### Source Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| **Path** | Yes | Directory to monitor | `C:\WATS\Reports` |
| **Filter** | Yes | File pattern to match | `*.xml`, `*.atml`, `Report*.csv` |
| **PostProcessAction** | No | Action after conversion | `Archive`, `Move`, `Delete`, `Error` |

#### PostProcessAction Values

| Value | Behavior |
|-------|----------|
| **Delete** | Delete source file after successful conversion (default) |
| **Archive** | Create ZIP archive and delete source |
| **Move** | Move to "Processed" subdirectory |
| **Error** | Move to "Error" subdirectory on failure |

#### Destination Parameters

Converter-specific parameters passed to the converter constructor. Each converter defines its own parameters through `IReportConverter_v2.ConverterParameters`.

---

## Converter Lifecycle

### Initialization Sequence

```
1. SERVICE STARTS
   │
2. Conversion.InitializeConverters() (async)
   ├─► Load converters.xml
   ├─► Deserialize configuration
   │
3. FOR EACH converter in config:
   ├─► new Converter(config, conversionEngine)
   │   ├─► Parse source/destination parameters
   │   ├─► Load converter assembly
   │   ├─► Verify implements IReportConverter
   │   ├─► Extract version from assembly
   │   ├─► State = Created
   │   └─► pendingitems = new List<>()
   │
   └─► Add to cnvList

4. Wait 5 seconds (allow file system to settle)

5. StartAllConverters()
   FOR EACH converter:
   ├─► converter.Start()
   │   ├─► Test folder access (write test file)
   │   ├─► Create Error subfolder
   │   ├─► State = Running
   │   ├─► CheckFolder() - Initial scan
   │   └─► Attach FileSystemWatcher
   │       ├─► Watch Path with Filter
   │       ├─► Events: Changed, Renamed
   │       └─► EnableRaisingEvents = true
   │
   └─► Log: "Converter started: {name}"

6. READY FOR FILES
```

### States

```
Created
   │
   ├─► Start()
   │   └─► Running
   │       ├─► (folder inaccessible)
   │       └─► FailedToStart
   │
Running
   │
   ├─► (error occurs)
   │   └─► Failed
   │
   ├─► Stop()
   │   └─► Stopped
   │
   └─► Dispose()
       └─► Disposing
```

---

## File Detection and Queuing

### FileSystemWatcher Events

**Monitored Events**:
```csharp
fsw.Changed += fsw_Changed;
fsw.Renamed += fsw_Renamed;
```

**Both events trigger**:
```csharp
CheckFolderSingleThread(null);
```

### CheckFolder Process

```
1. ENTRY
   ├─► Monitor.TryEnter(lock)
   │   └─► IF already running: Skip (exit)
   │
2. RECOVER FROM FAILED STATE
   ├─► IF State == FailedToStart
   │   └─► Retry Start()
   │
3. CHECK ORPHANED ITEMS
   ├─► Lock pendingitems
   ├─► FOR EACH item in pendingitems:
   │   └─► IF not in global pending queue:
   │       └─► Remove (orphaned)
   │
4. EARLY EXIT IF QUEUE FULL
   ├─► IF pendingitems.Count >= 10:
   │   └─► Skip (avoid filesystem query)
   │
5. ENUMERATE FILES
   ├─► DirectoryInfo.EnumerateFiles(Filter)
   ├─► OrderBy CreationTime
   ├─► Take 10,000 max
   │
6. QUEUE FILES
   ├─► FOR EACH file:
   │   ├─► conversion.AddFile(file, converter)
   │   │   ├─► Creates ConversionItem
   │   │   ├─► Adds to global pending dictionary
   │   │   └─► Adds to global pending_queue
   │   │
   │   └─► IF not in this.pendingitems:
   │       └─► Add to this.pendingitems
   │
7. EXIT
   ├─► Log: "Pending count: {count}, New files: {added}"
   ├─► Sleep 5 seconds
   └─► Monitor.Exit(lock)
```

### Throttling and Limits

| Limit | Value | Purpose |
|-------|-------|---------|
| **Max files per scan** | 10,000 | Prevent memory exhaustion |
| **Skip threshold** | 10 pending | Avoid redundant filesystem queries |
| **Scan cooldown** | 5 seconds | Rate limiting between scans |
| **Retry attempts (XML)** | 5 | Handle file locks during conversion |

---

## Conversion Processing

### Worker Thread Allocation

**Scaling Algorithm**:
```csharp
int pendingCount = pending_queue.Count;
int desiredWorkers = (pendingCount + 9) / 10;

// Respect registry setting
if (desiredWorkers > MaxConversionWorkers)
    desiredWorkers = MaxConversionWorkers;

// Absolute maximum
if (desiredWorkers > 50)
    desiredWorkers = 50;

// Minimum
if (desiredWorkers < 1)
    desiredWorkers = 1;

// Spawn or shutdown workers to match desired
while (workers.Count < desiredWorkers)
    SpawnWorker();
```

**Examples**:
```
Pending: 0-10    → 1 worker
Pending: 11-20   → 2 workers
Pending: 21-30   → 3 workers
Pending: 100-110 → 11 workers (if MaxConversionWorkers >= 11)
Pending: 500+    → 50 workers (absolute max)
```

### Worker Lifecycle

```
1. SPAWN WORKER
   └─► ThreadPool.QueueUserWorkItem(DoWork)

2. DoWork() LOOP
   WHILE !ShutDownInProgress:
   ├─► GetNextFileToConvert(out item)
   │   └─► Returns next item from pending_queue
   │
   ├─► IF item != null:
   │   ├─► Process item
   │   └─► Continue immediately
   │
   └─► ELSE (no work):
       └─► Sleep briefly, retry

3. SHUTDOWN
   ├─► ShutDownInProgress = true
   ├─► Complete current item
   └─► Exit loop
```

### Conversion Steps

```
1. GET CONVERTER INSTANCE
   ├─► Load assembly
   ├─► Create instance with destination parameters
   └─► Cast to IReportConverter

2. OPEN FILE (EXCLUSIVE)
   ├─► FileStream(path, FileMode.Open, FileAccess.Read, FileShare.None)
   └─► Prevents concurrent access

3. CALL ImportReport()
   ├─► IReportConverter.ImportReport(api, fileStream)
   ├─► Converter parses file
   ├─► Creates UUTReport or UURReport
   └─► Returns Report instance

4. SUBMIT REPORT
   ├─► IF report != null:
   │   └─► api.Submit(report, SubmitMethod.Automatic)
   │       ├─► IF Online: HTTP POST to server
   │       └─► ELSE: Save as *.queued
   │
   └─► ELSE (converter handles submission):
       └─► Converter already called api.Submit()

5. CLEANUP
   ├─► converter.CleanUp()
   └─► Converter deletes temp files, etc.

6. POST-PROCESS SOURCE FILE
   ├─► SWITCH PostProcessAction:
   │   ├─► Delete: File.Delete()
   │   ├─► Archive: Create ZIP, delete source
   │   ├─► Move: Move to "Processed" folder
   │   └─► Error: Move to "Error" folder
   │
   └─► Remove from pending queue

7. TIMEOUT DETECTION (600 seconds)
   ├─► Watchdog checks item.processstart
   └─► IF (Now - processstart) > 600 seconds:
       ├─► Reset item state
       └─► Re-queue for retry
```

---

## IReportConverter Interface

### Interface Definition

```csharp
public interface IReportConverter
{
    /// <summary>
    /// Import and convert a file to WATS Report
    /// </summary>
    /// <param name="api">TDM API instance</param>
    /// <param name="file">File stream (exclusive lock)</param>
    /// <returns>Report instance or null if converter handles submission</returns>
    Interface.Report ImportReport(TDM api, Stream file);
    
    /// <summary>
    /// Clean up after conversion (delete temp files, etc.)
    /// </summary>
    void CleanUp();
}

public interface IReportConverter_v2 : IReportConverter
{
    /// <summary>
    /// Default parameters exposed to configurator
    /// </summary>
    Dictionary<string, string> ConverterParameters { get; }
}
```

### Implementation Example

```csharp
public class MyConverter : IReportConverter_v2
{
    private Dictionary<string, string> args;
    
    // Constructor receives Destination parameters
    public MyConverter(IDictionary<string, string> args)
    {
        this.args = new Dictionary<string, string>(args);
    }
    
    // Default parameters for configurator
    public Dictionary<string, string> ConverterParameters
    {
        get
        {
            return new Dictionary<string, string>
            {
                { "Option1", "default_value" },
                { "Option2", "true" }
            };
        }
    }
    
    public Interface.Report ImportReport(TDM api, Stream file)
    {
        // 1. Parse file
        XDocument doc = XDocument.Load(file);
        
        // 2. Create report
        var report = api.CreateUUTReport(
            "SerialNumber123",
            "PartNumber456",
            "1.0"
        );
        
        // 3. Add steps
        var root = report.GetRootSequenceCall();
        var step = root.AddNumericLimitStep("Voltage");
        step.StepType = StepType.NI_TestStand;
        step.Status = StepStatusType.Passed;
        step.ReportText = "Voltage check";
        step.Measurement = 5.0;
        step.CompOperator = CompOperatorType.GELE;
        step.LowLimit = 4.5;
        step.HighLimit = 5.5;
        
        // 4. Return report
        // Service will automatically submit
        return report;
    }
    
    public void CleanUp()
    {
        // Delete any temporary files created during import
    }
}
```

### Return Value Behavior

**Return Report Instance**:
```csharp
public Report ImportReport(TDM api, Stream file)
{
    var report = api.CreateUUTReport(...);
    // ... populate report ...
    return report; // Service will call api.Submit(report)
}
```

**Return Null (Manual Submission)**:
```csharp
public Report ImportReport(TDM api, Stream file)
{
    var report = api.CreateUUTReport(...);
    // ... populate report ...
    api.Submit(report, SubmitMethod.Automatic);
    return null; // Converter handled submission
}
```

---

## Standard Converters

### Included Converters

| Converter | Assembly | Formats |
|-----------|----------|---------|
| **TestStandConverter** | WATSStandardConverters | NI TestStand XML |
| **ATMLConverter** | WATSStandardConverters | ATML 5.2/6.0 XML |
| **WATSStandardJsonConverter** | WATSStandardConverters | WATS JSON format |
| **WSXFApiTestConverter** | WATSStandardConverters | WSXF test format |
| **TextConverterBase** | WATSStandardConverters | Text-based (abstract) |

### TestStand Converter

**Source Parameters**:
```xml
<Parameter name="Path">C:\WATS\TestStandReports</Parameter>
<Parameter name="Filter">*.xml</Parameter>
<Parameter name="PostProcessAction">Archive</Parameter>
```

**Destination Parameters**:
```xml
<Parameter name="IncludeArrayMeasurements">true</Parameter>
<Parameter name="IncludePassSteps">true</Parameter>
<Parameter name="IncludeAllProperties">false</Parameter>
```

**Features**:
- Parses TestStand XML reports
- Supports all step types (Numeric, String, MultipleNumeric, etc.)
- Handles station globals
- Preserves step hierarchy
- Configurable detail level

### ATML Converter

**Source Parameters**:
```xml
<Parameter name="Path">C:\WATS\ATMLReports</Parameter>
<Parameter name="Filter">*.atml</Parameter>
```

**Destination Parameters**:
```xml
<Parameter name="ATMLVersion">6.0</Parameter>
```

**Features**:
- Supports ATML 5.2 and 6.0
- Converts TestResults to steps
- Maps limits and outcomes
- Handles test equipment data

---

## Error Handling

### Conversion Errors

**Error Folder**:
```
{ConverterPath}\Error\
```

**Error Scenarios**:

1. **File Parse Error**
   ```
   Exception during ImportReport()
   ├─► Log error with stack trace
   ├─► Move file to Error folder
   └─► Remove from pending queue
   ```

2. **Assembly Load Error**
   ```
   Cannot load converter assembly
   ├─► Log error
   ├─► Converter State = Failed
   └─► All files for this converter skip processing
   ```

3. **File Lock Error**
   ```
   Cannot open file (locked by another process)
   ├─► Retry up to 5 times
   ├─► 5ms delay between retries
   └─► IF still locked: Skip, retry on next scan
   ```

4. **Timeout (600 seconds)**
   ```
   Watchdog detects stalled conversion
   ├─► Log warning
   ├─► Reset item state
   └─► Re-queue for retry
   ```

### Logging

**Trace Levels**:
```csharp
TraceEventType.Critical  - Fatal errors, service stops
TraceEventType.Error     - Conversion failures
TraceEventType.Warning   - Recoverable issues (folder unavailable)
TraceEventType.Information - State changes
TraceEventType.Verbose   - Debug info (file counts, timings)
```

**Example Log Entry**:
```
Th[0x0A],Cnv[TestStandConverter],Check[],Checkfolder result: 
  pending count: 15, new files: 5
```

---

## Performance Characteristics

### Throughput

**Variables Affecting Throughput**:
- Number of workers (1-50)
- File size
- Converter complexity
- Server response time
- Network latency

**Typical Performance**:
```
Small files (< 100 KB):
  1 worker:  30-60 files/minute
  10 workers: 300-600 files/minute

Large files (> 1 MB):
  1 worker:  5-10 files/minute
  10 workers: 50-100 files/minute
```

### Resource Usage

**Memory**:
```
Base service: ~50 MB
+ Per worker: ~10 MB
+ Per pending file: ~5 KB (metadata only)

Example (10 workers, 100 pending):
  50 + (10 * 10) + (100 * 0.005) = 150.5 MB
```

**CPU**:
```
Idle: < 1%
Active conversion: 5-50% (scales with workers)
Peak (50 workers): 80-100%
```

**Disk I/O**:
```
Read: File size
Write (if queued): File size + overhead
Archive (ZIP): ~50-70% of original size
```

---

## Configuration Best Practices

### Worker Count

**Recommendations**:
```
Low volume (< 100/day):    1-2 workers
Medium volume (100-1000):  5-10 workers
High volume (> 1000/day):  10-20 workers
Burst traffic:             20-50 workers
```

**Registry Setting**:
```
HKLM\SOFTWARE\Virinco\WATS\MaxConversionWorkers = 10
```

### Folder Structure

**Recommended**:
```
C:\WATS\
├─► TestStandReports\      (Converter 1 monitors)
│   ├─► Error\
│   └─► Archive\
│
├─► ATMLReports\           (Converter 2 monitors)
│   ├─► Error\
│   └─► Processed\
│
└─► CustomReports\         (Converter 3 monitors)
    ├─► Error\
    └─► Archive\
```

### File Patterns

**Good Patterns**:
```xml
<Parameter name="Filter">*.xml</Parameter>
<Parameter name="Filter">Report_*.csv</Parameter>
<Parameter name="Filter">Test_[0-9][0-9][0-9][0-9].atml</Parameter>
```

**Avoid**:
```xml
<!-- Too broad, may match temp files -->
<Parameter name="Filter">*.*</Parameter>

<!-- Wildcards in middle can be slow -->
<Parameter name="Filter">*Report*.xml</Parameter>
```

---

## Summary

### Key Concepts

1. **Pluggable Architecture**: Any assembly implementing IReportConverter can be used
2. **File-Based Triggering**: FileSystemWatcher for real-time detection
3. **Dynamic Scaling**: Worker threads scale 1-50 based on queue depth
4. **Fault Tolerance**: Timeouts, retries, error folders
5. **Configurable**: XML-based configuration for all converters

### Data Flow Summary

```
External File → FileSystemWatcher Event
                → CheckFolder()
                → AddFile (pending queue)
                → Worker pulls from queue
                → ImportReport (conversion)
                → Submit (to server or queue)
                → PostProcess (archive/delete)
                → Cleanup
```

### Thread Model

```
Main Service Thread
  └─► Watchdog Timer (1 min)
      └─► CheckState() for all converters

Per-Converter FileSystemWatcher Threads (N converters)
  └─► Triggers CheckFolder()

Worker Thread Pool (1-50 dynamic)
  └─► Process conversions in parallel
```

---

**Document Version**: 1.0  
**Last Updated**: January 30, 2025
