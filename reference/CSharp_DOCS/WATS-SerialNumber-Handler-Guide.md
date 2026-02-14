# WATS Serial Number Handler Guide

## Complete Reference for Managing Serial Numbers in Production

---

## Table of Contents

1. [Overview](#1-overview)
2. [Serial Number Types](#2-serial-number-types)
3. [Request Types - Take vs Reserve](#3-request-types---take-vs-reserve)
4. [Initialization](#4-initialization)
5. [Getting Serial Numbers](#5-getting-serial-numbers)
6. [Offline Storage](#6-offline-storage)
7. [Synchronization](#7-synchronization)
8. [Advanced Features](#8-advanced-features)
9. [Data Models](#9-data-models)
10. [Administration](#10-administration)
11. [Complete Examples](#11-complete-examples)

---

## 1. Overview

### What is the Serial Number Handler?

The **Serial Number Handler** is a WATS MES component that manages serial number allocation in production environments. It provides:

- **Centralized Management**: Serial numbers stored on WATS server
- **Offline Support**: Local pools for production lines without constant connectivity
- **Traceability**: Links serial numbers to products and parts
- **Sequence Control**: Contiguous serial number allocation (e.g., MAC addresses)
- **Multi-Station**: Prevents duplicate serial number usage across stations

### Architecture

```
???????????????????????????????????????????????????????????????
? WATS Server                                                  ?
?  - Serial Number Types (MAC, Device ID, etc.)               ?
?  - Serial Number Ranges (pools)                              ?
?  - Allocation tracking                                       ?
?  - Reference database                                        ?
???????????????????????????????????????????????????????????????
                 ?
                 ? Initialize / Reserve / Take
                 ?
???????????????????????????????????????????????????????????????
? Production Station (Client)                                  ?
?  - SerialNumberHandler instance                              ?
?  - Local pool (XML file) - OFFLINE MODE ONLY                ?
?  - Auto-refill when threshold reached                        ?
?  - Reference tracking (UUT SN, Part Number)                  ?
???????????????????????????????????????????????????????????????
```

### When to Use

| Scenario | Recommended Mode |
|----------|------------------|
| Online station, real-time allocation | **Take** mode |
| Production line, intermittent network | **Reserve** mode |
| MAC address programming (contiguous) | **Reserve** + Sequence |
| Multi-station, shared pool | **Take** or **Reserve** |
| Audit trail required | Both (automatic) |
| Testing/development | **Take** mode |

---

## 2. Serial Number Types

### 2.1 What is a Serial Number Type?

A **Serial Number Type** defines a category of serial numbers with:
- **Name**: Identifier (e.g., "MACAddress", "DeviceID")
- **Description**: Human-readable description
- **Format**: Display format (e.g., "XX-XX-XX-XX-XX-XX")
- **Regex**: Validation pattern
- **Ranges**: Available serial number pools

### 2.2 Getting Serial Number Types

```csharp
using Virinco.WATS.Interface.MES.Production;

// Get all available types
IEnumerable<SerialNumberType> types = SerialNumberHandler.GetSerialNumberTypes();

foreach (var type in types)
{
    Console.WriteLine($"Type: {type.Name}");
    Console.WriteLine($"  Description: {type.Description}");
    Console.WriteLine($"  Format: {type.Format}");
    Console.WriteLine($"  Regex: {type.Regex}");
}
```

**Example Types:**
```
Type: MACAddress
  Description: Network MAC Address
  Format: XX-XX-XX-XX-XX-XX
  Regex: ^([0-9A-F]{2}-){5}[0-9A-F]{2}$

Type: DeviceID
  Description: Unique Device Identifier
  Format: XXXXXXXX
  Regex: ^[0-9]{8}$
```

### 2.3 Serial Number Ranges

Ranges define the pool of available serial numbers for a type.

**Server Configuration:**
- Created via WATS web interface
- Can have multiple ranges per type
- Ranges tracked independently
- Each range has start/end or list of values

**Example Ranges for MACAddress:**
```
Range 1: 00-11-22-00-00-00 to 00-11-22-00-FF-FF (65,536 addresses)
Range 2: 00-11-33-00-00-00 to 00-11-33-00-FF-FF (65,536 addresses)
```

---

## 3. Request Types - Take vs Reserve

### 3.1 Comparison

| Aspect | Take Mode | Reserve Mode |
|--------|-----------|--------------|
| **Connection** | Must be online | Can work offline |
| **Allocation** | Immediate (on request) | Pre-reserved in batches |
| **Local Storage** | None | XML file maintained |
| **Use Case** | Online stations | Production lines |
| **Performance** | Network call per request | Local retrieval |
| **Complexity** | Simple | Manages local pool |
| **Recovery** | N/A | Uncommitted files |

### 3.2 Take Mode Workflow

```
Request Serial Number
    ?
[Client] ? Server: "Take 1 serial number"
    ?
[Server] Finds next available
    ?
[Server] Marks as Taken
    ?
[Server] ? Client: Returns serial number
    ?
[Client] Uses serial number immediately
```

**Characteristics:**
- ? No local state
- ? Simple to use
- ? Requires network connectivity
- ? Higher latency
- ? No cleanup needed

### 3.3 Reserve Mode Workflow

```
Initialization
    ?
[Client] ? Server: "Reserve batch of 100"
    ?
[Server] Marks 100 as Reserved
    ?
[Server] ? Client: Returns 100 serial numbers
    ?
[Client] Saves to local XML file
    ?
Production Loop:
    [Client] Retrieves from local pool
    [Client] Marks as taken in local file
    [Client] Links to UUT SN / Part Number
    ?
    When pool < threshold (e.g., 10 left)
        ?
        [Client] ? Server: "Reserve next batch"
        [Server] Updates reservation status
        [Client] Updates local pool
```

**Characteristics:**
- ? Works offline
- ? Low latency (local)
- ? Auto-refills
- ? Requires cleanup on shutdown
- ? Maintains state

---

## 4. Initialization

### 4.1 Basic Initialization (Take Mode)

```csharp
using Virinco.WATS.Interface.MES.Production;

// Create handler for a type
SerialNumberHandler handler = new SerialNumberHandler("MACAddress");

// Initialize in Take mode
handler.Initialize(
    tokenID: null,                              // Uses client token from settings
    serviceUrl: null,                           // Uses client URL from settings
    requestType: SerialNumberHandler.RequestType.Take,
    onlyInSequence: false,                      // Not applicable for Take
    batchSize: 0,                               // Not applicable for Take
    fetchWhenLessThan: 0,                       // Not applicable for Take
    startFromSerialNumber: null,                // Optional: start from specific number
    siteName: null,                             // Deprecated
    token: Guid.Empty                           // Deprecated
);

// Check status
var status = handler.GetStatus();
Console.WriteLine($"Status: {status}");  // Ready
```

### 4.2 Reserve Mode Initialization

```csharp
SerialNumberHandler handler = new SerialNumberHandler("MACAddress");

// Initialize in Reserve mode
handler.Initialize(
    tokenID: null,                              // Auto from settings
    serviceUrl: null,                           // Auto from settings
    requestType: SerialNumberHandler.RequestType.Reserve,
    onlyInSequence: false,                      // Allow non-contiguous
    batchSize: 100,                             // Reserve 100 at a time
    fetchWhenLessThan: 10,                      // Refill when < 10 left
    startFromSerialNumber: null,                // Start from beginning
    siteName: null,                             // Deprecated
    token: Guid.Empty                           // Deprecated
);
```

### 4.3 Reserve Mode with Sequence

```csharp
// For MAC addresses - ensures contiguous allocation
handler.Initialize(
    tokenID: null,
    serviceUrl: null,
    requestType: SerialNumberHandler.RequestType.Reserve,
    onlyInSequence: true,                       // ? Contiguous only
    batchSize: 1000,                            // Large batch
    fetchWhenLessThan: 100,                     // Refill threshold
    startFromSerialNumber: "00-11-22-00-00-00", // ? Start position
    siteName: null,
    token: Guid.Empty
);
```

### 4.4 Initialization Parameters

| Parameter | Type | Purpose |
|-----------|------|---------|
| `tokenID` | `string` | Client authentication (null = use settings) |
| `serviceUrl` | `string` | Server URL (null = use settings) |
| `requestType` | `RequestType` | Take or Reserve |
| `onlyInSequence` | `bool` | Allocate contiguous numbers only |
| `batchSize` | `int` | Number to reserve per batch |
| `fetchWhenLessThan` | `int` | Threshold to trigger refill |
| `startFromSerialNumber` | `string` | Optional starting position |
| `siteName` | `string` | Deprecated |
| `token` | `Guid` | Deprecated |

---

## 5. Getting Serial Numbers

### 5.1 Single Serial Number

```csharp
SerialNumberHandler handler = new SerialNumberHandler("DeviceID");
handler.Initialize(/* ... */);

// Get one serial number
string serialNumber = handler.GetSerialNumber(
    serialnumberRef: "UUT-SN-12345",    // Link to UUT serial number
    partnumberRef: "PCB-001"             // Link to part number
);

Console.WriteLine($"Allocated: {serialNumber}");
// Output: Allocated: 12345678
```

### 5.2 Multiple Serial Numbers

```csharp
// Get multiple (e.g., for multi-port device)
string[] serialNumbers = handler.GetSerialNumbers(
    numToGet: 4,                        // Need 4 serial numbers
    serialnumberRef: "UUT-SN-12345",
    partnumberRef: "PCB-QUAD-PORT"
);

foreach (var sn in serialNumbers)
{
    Console.WriteLine($"Port SN: {sn}");
}
/* Output:
Port SN: 00-11-22-00-00-10
Port SN: 00-11-22-00-00-11
Port SN: 00-11-22-00-00-12
Port SN: 00-11-22-00-00-13
*/
```

### 5.3 Sequence Mode (Contiguous)

```csharp
SerialNumberHandler handler = new SerialNumberHandler("MACAddress");

// Initialize with sequence
handler.Initialize(
    tokenID: null,
    serviceUrl: null,
    requestType: SerialNumberHandler.RequestType.Reserve,
    onlyInSequence: true,               // ? Contiguous
    batchSize: 1000,
    fetchWhenLessThan: 100,
    startFromSerialNumber: null,
    siteName: null,
    token: Guid.Empty
);

// Get 8 contiguous MAC addresses
string[] macs = handler.GetSerialNumbers(8, "UUT-001", "DEVICE-8PORT");

// Guaranteed contiguous:
// 00-11-22-00-10-00
// 00-11-22-00-10-01
// 00-11-22-00-10-02
// ...
// 00-11-22-00-10-07
```

### 5.4 Without References

```csharp
// No linking to UUT/Part
string sn = handler.GetSerialNumber(
    serialnumberRef: null,
    partnumberRef: null
);
```

### 5.5 Checking Pool Status

```csharp
// Get number of local serial numbers available
int available = handler.GetFreeLocalSerialNumbers();
Console.WriteLine($"Available locally: {available}");

// Get pool configuration
handler.GetPoolInfo(
    out bool onlyInSequence,
    out int batchSize,
    out int fetchWhenLessThan,
    out string startFromSerialNumber,
    out string siteName
);

Console.WriteLine($"Batch size: {batchSize}");
Console.WriteLine($"Refill threshold: {fetchWhenLessThan}");
Console.WriteLine($"Available: {available}");
```

---

## 6. Offline Storage

### 6.1 File Location

Reserve mode stores serial numbers locally in XML files:

```
Location: C:\ProgramData\Virinco\WATS\AddressStore\
Format:   {SerialNumberType}.xml
Example:  MACAddress.xml, DeviceID.xml
```

### 6.2 File Structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<SerialNumbers 
    requestType="Reserve" 
    serialNumberType="MACAddress" 
    batchSize="100" 
    fetchWhenLessThan="10" 
    onlyInSequence="true"
    fromSerialNumber="00-11-22-00-00-00"
    stationName="PROD-STATION-01"
    tokenId="eyJhbGciOiJIUzI1..."
    url="https://wats.example.com/api/Internal/Production/">
    
    <!-- Reserved but not yet taken -->
    <SN id="00-11-22-00-00-10" seq="5"/>
    <SN id="00-11-22-00-00-11" seq="4"/>
    <SN id="00-11-22-00-00-12" seq="3"/>
    
    <!-- Taken serial numbers -->
    <SN id="00-11-22-00-00-00" 
        taken="2024-01-15T10:30:25Z" 
        refSN="UUT-SN-12345" 
        refPN="PCB-001"/>
    <SN id="00-11-22-00-00-01" 
        taken="2024-01-15T10:31:10Z" 
        refSN="UUT-SN-12346" 
        refPN="PCB-001"/>
</SerialNumbers>
```

### 6.3 SerialNumbers Root Attributes

| Attribute | Type | Purpose |
|-----------|------|---------|
| `requestType` | `string` | "Take" or "Reserve" |
| `serialNumberType` | `string` | Type name |
| `batchSize` | `int` | Number per batch reservation |
| `fetchWhenLessThan` | `int` | Refill threshold |
| `onlyInSequence` | `bool` | Contiguous allocation |
| `fromSerialNumber` | `string` | Starting position |
| `stationName` | `string` | Machine name |
| `tokenId` | `string` | Client authentication token |
| `url` | `string` | Server API endpoint |

### 6.4 SN Element Attributes

| Attribute | Type | Purpose |
|-----------|------|---------|
| `id` | `string` | The serial number itself |
| `taken` | `DateTime` | When it was allocated (UTC) |
| `seq` | `int` | Sequence count (contiguous mode) |
| `refSN` | `string` | Reference UUT serial number |
| `refPN` | `string` | Reference part number |
| `refStn` | `string` | Reference station name |

**Status Interpretation:**
- **Reserved (not taken)**: Element exists with `id` only
- **Taken**: Has `taken` attribute set
- **Sequence**: `seq` indicates how many contiguous SNs follow

### 6.5 Uncommitted Files

When `Initialize()` is called, existing pool is moved to uncommitted:

```
Location: C:\ProgramData\Virinco\WATS\AddressStore\
Format:   {SerialNumberType}.{RandomGuid}.uncommitted
Example:  MACAddress.a1b2c3d4.uncommitted
```

**Purpose:**
- Server cancellation of old reservations
- Recovery on next initialization
- Prevents lost reservations

**Lifecycle:**
```
1. User calls Initialize()
   ?
2. MACAddress.xml ? MACAddress.a1b2c3d4.uncommitted
   ?
3. New pool reserved ? MACAddress.xml created
   ?
4. Server notified to cancel old reservation
   ?
5. Uncommitted file deleted
```

If step 4/5 fails, next `Initialize()` retries cancellation.

---

## 7. Synchronization

### 7.1 Auto-Refill Mechanism

In Reserve mode, the handler automatically refills the local pool:

```
????????????????????????????????????????????????????????????
? Local Pool Status                                         ?
? ???????????????????????????????????????????????          ?
? ? Available: 100  ???????????????             ?          ?
? ?                 ? Threshold   ?             ?          ?
? ? Available: 50   ? = 10        ?             ?          ?
? ?                 ???????????????             ?          ?
? ? Available: 11   ???? Still OK               ?          ?
? ?                                              ?          ?
? ? Available: 10   ???? At threshold           ?          ?
? ?      ?                                       ?          ?
? ?      ? GetSerialNumber() allocates 1        ?          ?
? ?      ?                                       ?          ?
? ? Available: 9    ???? TRIGGER REFILL         ?          ?
? ?      ?                                       ?          ?
? ?      ? Contact server for new batch         ?          ?
? ?      ?                                       ?          ?
? ? Available: 109  ???? Refilled (+100)        ?          ?
? ???????????????????????????????????????????????          ?
????????????????????????????????????????????????????????????
```

### 7.2 Refill Process

```csharp
// Internal process (automatic)
private string[] GetSerialNumbersLocal(SerialNumbers sn, int numToGet, 
    string connectToSerial, string connectToPartNumber)
{
    // 1. Check available
    int leftCount = sn.SN.Count(s => !s.takenSpecified);
    
    // 2. If exhausted, fetch immediately
    if (leftCount == 0)
    {
        sn = GetFromServer(sn);
    }
    
    // 3. Allocate requested serial numbers
    // ... (mark as taken, add references) ...
    
    // 4. Check if refill needed
    leftCount = sn.SN.Count(s => !s.takenSpecified);
    if (leftCount <= sn.fetchWhenLessThan)
    {
        try
        {
            sn = GetFromServer(sn);  // Async refill
        }
        catch (Exception)
        {
            // Allow offline operation - continue with remaining pool
        }
    }
    
    // 5. Save updated pool
    SaveFile(sn);
    
    return allocatedSerialNumbers;
}
```

### 7.3 Offline/Online Transition

**Going Offline:**
```csharp
// Production continues using local pool
// No errors until pool exhausted
// If pool runs out while offline ? Exception
```

**Coming Back Online:**
```csharp
// Next allocation attempt triggers refill
// Pool automatically synchronized
// Reserved serial numbers updated on server
```

### 7.4 Sync Failure Handling

```csharp
try
{
    // Try to get serial number
    string sn = handler.GetSerialNumber("UUT-001", "PCB-001");
}
catch (ApplicationException ex) when (ex.Message.Contains("No more serial numbers"))
{
    // Pool exhausted and can't refill
    // Options:
    // 1. Wait for connection
    // 2. Use different serial number type
    // 3. Manual intervention
}
```

---

## 8. Advanced Features

### 8.1 Starting from Specific Position

```csharp
// Reserve from specific MAC address onwards
handler.Initialize(
    tokenID: null,
    serviceUrl: null,
    requestType: SerialNumberHandler.RequestType.Reserve,
    onlyInSequence: true,
    batchSize: 100,
    fetchWhenLessThan: 10,
    startFromSerialNumber: "00-11-22-00-50-00",  // ? Start here
    siteName: null,
    token: Guid.Empty
);

// First serial number will be >= 00-11-22-00-50-00
string sn = handler.GetSerialNumber("UUT-001", "PCB-001");
// Result: 00-11-22-00-50-00 (or next available after this)
```

### 8.2 Duplicate Request Handling

Enable reuse of serial numbers on duplicate requests:

```csharp
// Enable duplicate request reuse
handler.SetReuseOnDuplicateRequest(true);

// First request
string[] sn1 = handler.GetSerialNumbers(3, "UUT-12345", "PCB-001");
// Returns: ["SN-001", "SN-002", "SN-003"]

// Duplicate request (same refSN and refPN, same count)
string[] sn2 = handler.GetSerialNumbers(3, "UUT-12345", "PCB-001");
// Returns: ["SN-001", "SN-002", "SN-003"] (SAME serial numbers)

// Different count - new serial numbers allocated
string[] sn3 = handler.GetSerialNumbers(2, "UUT-12345", "PCB-001");
// Returns: ["SN-004", "SN-005"] (NEW serial numbers)
```

**Use Case:**
- Test sequence re-runs
- Programming retries
- Development/debugging

### 8.3 Retrieving Taken Serial Numbers

```csharp
// Find all serial numbers for a UUT
string[] snForUUT = handler.GetTakenSerialNumbers(
    serialnumberRef: "UUT-SN-12345",
    partnumberRef: null
);

// Find all serial numbers for a part
string[] snForPart = handler.GetTakenSerialNumbers(
    serialnumberRef: null,
    partnumberRef: "PCB-001"
);

// Find serial numbers for UUT + Part combination
string[] snForBoth = handler.GetTakenSerialNumbers(
    serialnumberRef: "UUT-SN-12345",
    partnumberRef: "PCB-001"
);

foreach (var sn in snForUUT)
{
    Console.WriteLine($"UUT SN used: {sn}");
}
```

### 8.4 MAC Address Utilities

```csharp
SerialNumberHandler handler = new SerialNumberHandler("MACAddress");

// Convert MAC string to integer
Int64 macInt = handler.MACToInt("00-11-22-33-44-55");
// Result: 73596058965 (0x00112233445)

// Convert integer to MAC string
string mac = handler.FormatAsMAC(73596058965, separator: '-');
// Result: "00-11-22-33-44-55"

// Different separator
string macColon = handler.FormatAsMAC(73596058965, separator: ':');
// Result: "00:11:22:33:44:55"
```

### 8.5 Inspecting Local Pool

```csharp
// Get all local serial numbers
IEnumerable<SerialNumbersSN> localSNs = handler.GetLocalSerialNumbers();

foreach (var sn in localSNs)
{
    Console.WriteLine($"SN: {sn.id}");
    
    if (sn.takenSpecified)
    {
        Console.WriteLine($"  Taken: {sn.taken}");
        Console.WriteLine($"  Ref UUT SN: {sn.refSN}");
        Console.WriteLine($"  Ref PN: {sn.refPN}");
    }
    else
    {
        Console.WriteLine($"  Status: Available");
        if (sn.seqSpecified)
            Console.WriteLine($"  Sequence: {sn.seq} contiguous");
    }
}
```

---

## 9. Data Models

### 9.1 SerialNumberType

```csharp
public class SerialNumberType
{
    public string Name { get; set; }            // Type identifier
    public string Description { get; set; }     // Human-readable name
    public string Format { get; set; }          // Display format
    public string Regex { get; set; }           // Validation pattern
}
```

### 9.2 SerialNumbers (Pool)

```csharp
public class SerialNumbers
{
    public SerialNumbersSN[] SN { get; set; }           // Array of serial numbers
    public string requestType { get; set; }             // "Take" or "Reserve"
    public string serialNumberType { get; set; }        // Type name
    public DateTime reservedUTC { get; set; }           // When reserved
    public string stationName { get; set; }             // Machine name
    public int batchSize { get; set; }                  // Reservation batch size
    public int fetchWhenLessThan { get; set; }          // Refill threshold
    public string tokenId { get; set; }                 // Auth token
    public string url { get; set; }                     // Server URL
    public bool onlyInSequence { get; set; }            // Contiguous mode
    public string fromSerialNumber { get; set; }        // Start position
    public string refSN { get; set; }                   // Reference UUT SN
    public string refPN { get; set; }                   // Reference Part Number
}
```

### 9.3 SerialNumbersSN (Individual)

```csharp
public class SerialNumbersSN
{
    public string id { get; set; }              // The serial number
    public DateTime taken { get; set; }         // When allocated (UTC)
    public bool takenSpecified { get; set; }    // True if taken
    public int seq { get; set; }                // Sequence count
    public bool seqSpecified { get; set; }      // True if in sequence
    public string refSN { get; set; }           // Reference UUT Serial Number
    public string refPN { get; set; }           // Reference Part Number
    public string refStn { get; set; }          // Reference Station
}
```

### 9.4 Status Enum

```csharp
public enum Status
{
    Ready,              // Initialized and ready
    NotInitialized      // Needs initialization
}
```

### 9.5 RequestType Enum

```csharp
public enum RequestType
{
    Reserve,    // Offline mode with local pool
    Take        // Online mode, immediate allocation
}
```

---

## 10. Administration

### 10.1 Uploading Serial Numbers from File

```csharp
SerialNumberHandler handler = new SerialNumberHandler("DeviceID");

// Upload from text file (one SN per line)
List<string> rejected = handler.UploadSerialNumbersFromFile(
    tokenID: "your-token-id",
    serviceUrl: "https://wats.example.com/api/Internal/Production/",
    fileName: @"C:\SerialNumbers\device_ids.txt",
    uploaded: out int uploadedCount,
    rejected: out int rejectedCount,
    token: new Guid("{1C3CFC7C-1386-4219-94F4-06D2B7FD8E18}")  // Admin token
);

Console.WriteLine($"Uploaded: {uploadedCount}");
Console.WriteLine($"Rejected (duplicates): {rejectedCount}");

foreach (var dup in rejected)
{
    Console.WriteLine($"  Already exists: {dup}");
}
```

**File Format (device_ids.txt):**
```
12345678
12345679
12345680
12345681
```

### 10.2 Generating and Uploading MAC Addresses

```csharp
SerialNumberHandler handler = new SerialNumberHandler("MACAddress");

// Generate range and upload
Int64 startMAC = handler.MACToInt("00-11-22-00-00-00");
Int64 endMAC = handler.MACToInt("00-11-22-00-FF-FF");

List<string> rejected = handler.GenerateAndUploadSerialNumbers(
    tokenID: "your-token-id",
    serviceUrl: "https://wats.example.com/api/Internal/Production/",
    fromSN: startMAC,
    toSN: endMAC,
    separator: '-',
    uploaded: out int uploadedCount,
    rejected: out int rejectedCount,
    token: new Guid("{1C3CFC7C-1386-4219-94F4-06D2B7FD8E18}")
);

Console.WriteLine($"Uploaded: {uploadedCount} MAC addresses");
Console.WriteLine($"Range: 00-11-22-00-00-00 to 00-11-22-00-FF-FF");
```

### 10.3 Canceling Reservations

```csharp
// Cancel all reservations for this type
handler.CancelReservations();

// Or cancel all types (before disconnecting client)
SerialNumberHandler.CancelAllReservations();
```

**When to Cancel:**
- Before client shutdown
- When changing configuration
- On error recovery
- Before re-initialization

**What Happens:**
1. Unreserved SNs marked as available on server
2. Local pool cleared
3. Next `GetSerialNumber()` fetches new batch

---

## 11. Complete Examples

### 11.1 Simple Online Mode (Take)

```csharp
using Virinco.WATS.Interface.MES.Production;
using System;

class OnlineExample
{
    static void Main()
    {
        // Create handler
        SerialNumberHandler handler = new SerialNumberHandler("DeviceID");
        
        // Initialize in Take mode (online)
        handler.Initialize(
            tokenID: null,
            serviceUrl: null,
            requestType: SerialNumberHandler.RequestType.Take,
            onlyInSequence: false,
            batchSize: 0,
            fetchWhenLessThan: 0,
            startFromSerialNumber: null,
            siteName: null,
            token: Guid.Empty
        );
        
        // Get serial number for production
        string deviceID = handler.GetSerialNumber(
            serialnumberRef: "UUT-SN-001",
            partnumberRef: "DEVICE-X1"
        );
        
        Console.WriteLine($"Device ID assigned: {deviceID}");
        // Output: Device ID assigned: 12345678
        
        // Program device with this ID
        // ...
    }
}
```

### 11.2 Offline Production Line (Reserve)

```csharp
using Virinco.WATS.Interface.MES.Production;
using System;

class ProductionLineExample
{
    static void Main()
    {
        // Initialize handler for production
        SerialNumberHandler handler = new SerialNumberHandler("DeviceID");
        
        // Reserve mode with offline support
        handler.Initialize(
            tokenID: null,
            serviceUrl: null,
            requestType: SerialNumberHandler.RequestType.Reserve,
            onlyInSequence: false,
            batchSize: 500,             // Reserve 500 at a time
            fetchWhenLessThan: 50,      // Refill when < 50 left
            startFromSerialNumber: null,
            siteName: null,
            token: Guid.Empty
        );
        
        Console.WriteLine($"Pool initialized");
        
        // Production loop
        for (int i = 1; i <= 1000; i++)
        {
            string uutSN = $"UUT-{i:D6}";
            
            try
            {
                // Get serial number
                string deviceID = handler.GetSerialNumber(
                    serialnumberRef: uutSN,
                    partnumberRef: "PRODUCT-X"
                );
                
                Console.WriteLine($"UUT {uutSN}: Device ID {deviceID}");
                
                // Check pool status every 100 units
                if (i % 100 == 0)
                {
                    int available = handler.GetFreeLocalSerialNumbers();
                    Console.WriteLine($"  Pool: {available} available");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"ERROR: {ex.Message}");
                break;
            }
        }
        
        // Cleanup - cancel unused reservations
        handler.CancelReservations();
    }
}
```

### 11.3 MAC Address Programming (Sequence)

```csharp
using Virinco.WATS.Interface.MES.Production;
using System;

class MACProgrammingExample
{
    static void Main()
    {
        SerialNumberHandler handler = new SerialNumberHandler("MACAddress");
        
        // Initialize for contiguous MAC addresses
        handler.Initialize(
            tokenID: null,
            serviceUrl: null,
            requestType: SerialNumberHandler.RequestType.Reserve,
            onlyInSequence: true,                       // ? Contiguous
            batchSize: 1000,
            fetchWhenLessThan: 100,
            startFromSerialNumber: "00-11-22-00-00-00", // Start position
            siteName: null,
            token: Guid.Empty
        );
        
        // Program device with 4 MAC addresses (must be contiguous)
        string uutSN = "UUT-QUAD-001";
        string[] macs = handler.GetSerialNumbers(
            numToGet: 4,
            serialnumberRef: uutSN,
            partnumberRef: "ROUTER-4PORT"
        );
        
        Console.WriteLine($"Assigned contiguous MACs for {uutSN}:");
        for (int i = 0; i < macs.Length; i++)
        {
            Console.WriteLine($"  Port {i}: {macs[i]}");
            
            // Verify contiguous
            if (i > 0)
            {
                Int64 prev = handler.MACToInt(macs[i - 1]);
                Int64 curr = handler.MACToInt(macs[i]);
                
                if (curr - prev != 1)
                {
                    Console.WriteLine($"  WARNING: Not contiguous!");
                }
            }
        }
        
        /* Output:
        Assigned contiguous MACs for UUT-QUAD-001:
          Port 0: 00-11-22-00-00-10
          Port 1: 00-11-22-00-00-11
          Port 2: 00-11-22-00-00-12
          Port 3: 00-11-22-00-00-13
        */
    }
}
```

### 11.4 Multi-Station Production

```csharp
using Virinco.WATS.Interface.MES.Production;
using System;
using System.Threading.Tasks;

class MultiStationExample
{
    static void Main()
    {
        // Simulate 3 stations
        Task.Run(() => Station("Station-1"));
        Task.Run(() => Station("Station-2"));
        Task.Run(() => Station("Station-3"));
        
        Console.ReadLine();
    }
    
    static void Station(string stationName)
    {
        SerialNumberHandler handler = new SerialNumberHandler("DeviceID");
        
        // Each station has its own pool
        handler.Initialize(
            tokenID: null,
            serviceUrl: null,
            requestType: SerialNumberHandler.RequestType.Reserve,
            onlyInSequence: false,
            batchSize: 100,
            fetchWhenLessThan: 10,
            startFromSerialNumber: null,
            siteName: null,
            token: Guid.Empty
        );
        
        // Production on this station
        for (int i = 1; i <= 50; i++)
        {
            string uutSN = $"{stationName}-UUT-{i:D4}";
            string deviceID = handler.GetSerialNumber(uutSN, "PRODUCT-X");
            
            Console.WriteLine($"[{stationName}] {uutSN}: {deviceID}");
            System.Threading.Thread.Sleep(100);  // Simulate production time
        }
        
        handler.CancelReservations();
    }
}
```

### 11.5 Traceability Example

```csharp
using Virinco.WATS.Interface.MES.Production;
using System;

class TraceabilityExample
{
    static void Main()
    {
        SerialNumberHandler handler = new SerialNumberHandler("ModuleID");
        handler.Initialize(/* ... */);
        
        // Production: Assign module IDs to UUT
        string uutSN = "UUT-MAIN-12345";
        string partNumber = "SYSTEM-X";
        
        // System has 3 modules
        string[] moduleIDs = handler.GetSerialNumbers(
            numToGet: 3,
            serialnumberRef: uutSN,
            partnumberRef: partNumber
        );
        
        Console.WriteLine($"System {uutSN} ({partNumber}):");
        Console.WriteLine($"  Module 1: {moduleIDs[0]}");
        Console.WriteLine($"  Module 2: {moduleIDs[1]}");
        Console.WriteLine($"  Module 3: {moduleIDs[2]}");
        
        // Later: Retrieve modules for this UUT
        Console.WriteLine("\nRetrieving modules for UUT...");
        string[] retrievedModules = handler.GetTakenSerialNumbers(
            serialnumberRef: uutSN,
            partnumberRef: null
        );
        
        Console.WriteLine($"Found {retrievedModules.Length} modules:");
        foreach (var module in retrievedModules)
        {
            Console.WriteLine($"  - {module}");
        }
        
        // Or retrieve all UUTs using a specific part
        Console.WriteLine($"\nAll systems using part {partNumber}:");
        string[] allForPart = handler.GetTakenSerialNumbers(
            serialnumberRef: null,
            partnumberRef: partNumber
        );
        
        Console.WriteLine($"Found {allForPart.Length} systems");
    }
}
```

---

## 12. Quick Reference

### 12.1 Common Workflows

| Task | Mode | Commands |
|------|------|----------|
| Simple online | Take | `Initialize()` ? `GetSerialNumber()` |
| Offline production | Reserve | `Initialize()` ? Loop: `GetSerialNumber()` ? `CancelReservations()` |
| MAC programming | Reserve+Seq | `Initialize(onlyInSequence=true)` ? `GetSerialNumbers(n)` |
| Traceability | Either | `GetSerialNumber(refSN, refPN)` ? `GetTakenSerialNumbers()` |

### 12.2 File Locations

| File | Location | Purpose |
|------|----------|---------|
| Pool (active) | `C:\ProgramData\Virinco\WATS\AddressStore\{Type}.xml` | Current pool |
| Uncommitted | `C:\ProgramData\Virinco\WATS\AddressStore\{Type}.{guid}.uncommitted` | Recovery |
| Settings | `C:\ProgramData\Virinco\WATS\Client\settings.json` | Client config |

### 12.3 Common Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Not calling `CancelReservations()` | Unused SNs remain reserved | Always cancel on shutdown |
| Using Take mode offline | Network errors | Use Reserve mode |
| Requesting more than `batchSize` | Exception | Increase `batchSize` or request fewer |
| Not checking pool status | Unexpected exhaustion | Monitor `GetFreeLocalSerialNumbers()` |
| Mixing sequence/non-sequence | Inconsistent allocation | Decide mode at initialization |

### 12.4 Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Status = NotInitialized | `Initialize()` not called | Call `Initialize()` |
| "No more serial numbers" | Pool exhausted | Check network, increase `batchSize` |
| Duplicate serial numbers | Multiple clients not synced | Check server, verify unique reservations |
| Sequence broken | Not using `onlyInSequence=true` | Re-initialize with sequence mode |
| File access error | Permissions | Check `C:\ProgramData\Virinco\WATS\` access |

---

## Appendix: API Reference

### Key Methods

#### SerialNumberHandler

- `SerialNumberHandler(string typeName)` - Constructor
- `Initialize(...)` - Setup handler
- `GetSerialNumber(refSN, refPN)` - Get one SN
- `GetSerialNumbers(count, refSN, refPN)` - Get multiple SNs
- `GetTakenSerialNumbers(refSN, refPN)` - Query taken SNs
- `GetStatus()` - Check readiness
- `GetFreeLocalSerialNumbers()` - Count available
- `GetPoolInfo(...)` - Get configuration
- `CancelReservations()` - Release unreserved SNs
- `SetReuseOnDuplicateRequest(bool)` - Enable duplicate handling

#### Static Methods

- `GetSerialNumberTypes()` - List all types
- `CancelAllReservations()` - Release all types

#### Utilities

- `MACToInt(string)` - Convert MAC to integer
- `FormatAsMAC(Int64, char)` - Convert integer to MAC
- `GenerateAndUploadSerialNumbers(...)` - Upload range
- `UploadSerialNumbersFromFile(...)` - Upload from file

### Key Classes

- `SerialNumberHandler` - Main handler class
- `SerialNumberType` - Type definition
- `SerialNumbers` - Pool container
- `SerialNumbersSN` - Individual serial number
- `RequestType` - Take/Reserve enum
- `Status` - Ready/NotInitialized enum

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**For WATS Client API Version:** 5.0+
