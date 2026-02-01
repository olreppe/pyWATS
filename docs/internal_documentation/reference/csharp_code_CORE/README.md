# .NET 8 Core - Report Headers and Listing Classes

This folder contains all classes related to retrieving and listing report headers from WATS, including the base Report concept and report querying functionality.

## Purpose

While the `NET8_UUT_UUR_Classes` folder contains classes for **creating** UUT and UUR reports, this folder contains classes for **querying and retrieving** existing reports from the WATS system.

## Source Projects
These files are copied from the following projects that target .NET 8:
- **Interface.TDM** - Targets: net48;net8.0-windows10.0.18362.0
- **WATS-Core** - Targets: net8.0-windows10.0.18362.0

## Directory Structure

### Root Files
- **TDM.cs** - Main TDM API class with FindReportHeaders() and FindReports() methods
- **Report.cs** - Base class for both UUT and UUR reports
- **Enums.cs** - All enumerations
- **OperationType.cs** - Operation type definitions
- **RepairType.cs** - Repair type definitions
- **Processes.cs** - Process-related classes

### Models/
Contains data models for report headers and query results:
- **ReportHeader.cs** - Modern report header model (used by FindReportHeaders)
- **Client.cs** - Client/station information model
- **ClientVersion.cs** - Client version information
- **ProcessConverter.cs** - JSON converter for process types

#### Models/da-import/
Legacy and data-access models:
- **WatsReportHeader.cs** - Legacy report header model (deprecated, used by FindReports)
- **ReportsWrmlUpsertResult.cs** - Result model for report submission
- **Member.cs** - Member/client data model
- **Codes.cs** - Status and result codes

### Core/
Core utilities and infrastructure (shared with NET8_UUT_UUR_Classes):
- **Enum.cs** - Core enumerations
- **Env.cs** - Environment settings
- **Extensions.cs** - Extension methods
- **GlobalUtilities.cs** - Global utility functions
- **Settings.cs** - Settings management
- **Registry.cs** - Registry access
- **WATSException.cs** - Exception classes

#### Core/Security/
- **Cryptography.cs** - Cryptographic functions
- **Licensing.cs** - License management
- **SimpleAes.cs** - AES encryption

### Schemas/
XML schema-related classes (shared with NET8_UUT_UUR_Classes):
- **WATS Report.designer.cs** - WRML schema classes
- **WATS WSXF Report.cs** - WSXF schema classes
- **Converters.cs** - Schema converters

## Key Classes for Report Querying

### ReportHeader (Modern API)
**File:** `Models/ReportHeader.cs`

The modern model for report headers returned by `FindReportHeaders()`.

**Properties:**
- `UUID` - Report unique ID
- `SerialNumber` - Unit serial number
- `PartNumber` - Part number
- `ReportType` - "T" (UUT) or "R" (UUR)
- `Start` - Report start timestamp
- `Revision` - Part revision
- `Result` - Test result (Passed, Failed, Error, Terminated)
- `BatchNumber` - Batch number
- `UserName` - Operator name
- `StationName` - Test station name
- `Location` - Station location
- `Purpose` - Station purpose
- `TimeStamp` - Processing order timestamp
- `OperationCode` - Operation type code
- `OperationName` - Operation type name
- And more...

### WatsReportHeader (Legacy API)
**File:** `Models/da-import/WatsReportHeader.cs`

**[Obsolete]** Legacy model for report headers returned by `FindReports()`.

**Properties:**
- `Guid` - Report unique ID
- `SN` - Serial number
- `PN` - Part number
- `ReportType` - Report type
- `Start_UTC` - Start time UTC
- `Rev` - Revision
- `Result` - Test result
- `OpCode` - Operation code
- `OpName` - Operation name
- `BatchNo` - Batch number
- `Operator` - Operator name
- `MachineName` - Station name
- `Location` - Location
- `Purpose` - Purpose
- `MeasuresDeleted` - Measures deleted flag

## TDM API Methods for Report Querying

### FindReportHeaders (Modern API - Recommended)
```csharp
ReportHeader[] FindReportHeaders(
    string filter,      // OData-style filter
    int top,            // Max number of results
    int skip = 0,       // Skip N results (pagination)
    string orderby = "start desc",  // Sort order
    string select = "", // Select specific fields
    string expand = ""  // Expand related entities
)
```

**Example:**
```csharp
TDM api = new TDM();

// Find last 10 UUT reports
var headers = api.FindReportHeaders(
    filter: "reportType eq 'T'",
    top: 10,
    orderby: "start desc"
);

// Find reports by serial number
var headers = api.FindReportHeaders(
    filter: "serialNumber eq 'SN-12345'",
    top: 100
);

// Find failed reports today
var today = DateTime.Today.ToString("yyyy-MM-dd");
var headers = api.FindReportHeaders(
    filter: $"start ge {today} and result eq 'Failed'",
    top: 100
);
```

### FindReports (Legacy API - Deprecated)
```csharp
[Obsolete("Deprecated, use FindReportHeaders instead.")]
WatsReportHeader[] FindReports(
    string filter,      // Custom filter syntax
    int top,            // Max number of results
    string orderby = "Start_UTC desc"  // Sort order
)
```

**Example:**
```csharp
// Legacy syntax - still works but deprecated
var headers = api.FindReports(
    filter: "(SN eq 'SN-12345') and (ReportType eq 'UUT')",
    top: 10
);
```

## Common Query Scenarios

### 1. Find Reports by Serial Number
```csharp
var headers = api.FindReportHeaders(
    filter: "serialNumber eq 'SN-67890'",
    top: 100,
    orderby: "start desc"
);
```

### 2. Find Reports by Part Number and Operation
```csharp
var headers = api.FindReportHeaders(
    filter: "partNumber eq 'PN-001' and operationCode eq '10'",
    top: 50
);
```

### 3. Find Failed Reports in Date Range
```csharp
var headers = api.FindReportHeaders(
    filter: "start ge 2026-01-01 and start lt 2026-02-01 and result eq 'Failed'",
    top: 1000
);
```

### 4. Find Reports by Station
```csharp
var headers = api.FindReportHeaders(
    filter: "stationName eq 'TestStation-01'",
    top: 100,
    orderby: "start desc"
);
```

### 5. Pagination
```csharp
// Get first page
var page1 = api.FindReportHeaders(
    filter: "reportType eq 'T'",
    top: 50,
    skip: 0
);

// Get second page
var page2 = api.FindReportHeaders(
    filter: "reportType eq 'T'",
    top: 50,
    skip: 50
);
```

## Filter Syntax (OData)

The modern `FindReportHeaders` uses OData query syntax:

### Comparison Operators
- `eq` - Equals
- `ne` - Not equals
- `gt` - Greater than
- `ge` - Greater than or equal
- `lt` - Less than
- `le` - Less than or equal

### Logical Operators
- `and` - Logical AND
- `or` - Logical OR
- `not` - Logical NOT

### String Functions
- `contains(field, 'value')` - Contains substring
- `startswith(field, 'value')` - Starts with
- `endswith(field, 'value')` - Ends with

### Examples
```csharp
// Multiple conditions
"partNumber eq 'PN-001' and result eq 'Passed' and start ge 2026-01-01"

// OR condition
"result eq 'Failed' or result eq 'Error'"

// String contains
"contains(serialNumber, '12345')"

// Date range
"start ge 2026-01-01 and start lt 2026-02-01"
```

## Report Base Concept

The `Report` class (Report.cs) serves as the base class for both UUTReport and UURReport. It provides common functionality:

- Report identification (ReportId GUID)
- Part information (PartNumber, SerialNumber, Revision)
- Timestamps and status
- File management
- Validation
- Statistics tracking

Both UUT and UUR reports inherit from this base class, providing a unified interface for report handling.

## Important Notes

1. **Use FindReportHeaders** - The modern API with OData filtering
2. **FindReports is deprecated** - Still works but use FindReportHeaders for new code
3. **Pagination support** - Use skip parameter for large result sets
4. **Filter validation** - Invalid filters will throw exceptions
5. **Date formats** - Use ISO 8601 format (yyyy-MM-dd or yyyy-MM-ddTHH:mm:ss)
6. **Case sensitivity** - Filters are generally case-sensitive
7. **Performance** - Use specific filters and limit top parameter for best performance

## Dependencies
These classes require:
- .NET 8.0 or later
- Windows 10.0.18362.0 or later
- WATS Server connection
- Newtonsoft.Json for JSON serialization

## Related Folders

- **NET8_UUT_UUR_Classes/** - Classes for creating UUT/UUR reports
- This folder focuses on querying and retrieving existing reports

## Total Files: 30
- C# Source Files: 30
- Main API: TDM.cs with FindReportHeaders() method
- Modern Model: ReportHeader.cs
- Legacy Model: WatsReportHeader.cs (deprecated)
