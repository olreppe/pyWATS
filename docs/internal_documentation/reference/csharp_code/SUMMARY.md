# Summary - Report Headers and Listing Classes (.NET 8)

## ✅ New Folder Created

**Location:** `NET8_Report_Headers_And_Listing/`

## 📊 Statistics

- **Total Files:** 31
  - C# Source Files: 30
  - Documentation Files: 1
- **Directories:** 4 subdirectories

## 🎯 Purpose

This folder contains classes for **querying and retrieving** existing report headers from WATS.

### Key Difference from NET8_UUT_UUR_Classes
- **NET8_UUT_UUR_Classes** → Create new reports
- **NET8_Report_Headers_And_Listing** → Query existing reports

## 📁 Contents

### Main API
- **TDM.cs** - Contains FindReportHeaders() and FindReports() methods

### Report Header Models
- **Models/ReportHeader.cs** - Modern report header model (recommended)
- **Models/da-import/WatsReportHeader.cs** - Legacy model (deprecated)

### Base Concept
- **Report.cs** - Base class for all reports (UUT and UUR)

### Supporting Classes
- Client information models
- Process converters
- Type definitions (OperationType, RepairType, Processes)
- Core utilities and infrastructure
- Schema definitions

## 🔍 Key Functionality

### FindReportHeaders (Modern API)
```csharp
TDM api = new TDM();

// Find reports by serial number
var headers = api.FindReportHeaders(
    filter: "serialNumber eq 'SN-12345'",
    top: 100,
    orderby: "start desc"
);

// Find failed reports today
var headers = api.FindReportHeaders(
    filter: "start ge 2026-01-30 and result eq 'Failed'",
    top: 50
);

// Pagination
var page1 = api.FindReportHeaders("reportType eq 'T'", top: 50, skip: 0);
var page2 = api.FindReportHeaders("reportType eq 'T'", top: 50, skip: 50);
```

### FindReports (Legacy API - Deprecated)
```csharp
// Still works but deprecated - use FindReportHeaders instead
var headers = api.FindReports(
    filter: "(SN eq 'SN-12345') and (ReportType eq 'UUT')",
    top: 10
);
```

## 📋 Report Header Properties

### ReportHeader (Modern)
- UUID - Report unique ID
- SerialNumber - Unit serial number
- PartNumber - Part number
- ReportType - "T" (UUT) or "R" (UUR)
- Start - Report start timestamp
- Result - Passed, Failed, Error, Terminated
- UserName - Operator
- StationName - Test station
- OperationCode/Name - Operation type
- And many more...

## 🔧 Common Use Cases

1. **Find by Serial Number** - Query all reports for a unit
2. **Date Range Queries** - Get reports within time period
3. **Status Filtering** - Find passed/failed reports
4. **Station Queries** - Reports from specific station
5. **Pagination** - Retrieve large result sets
6. **Report Lookup** - Find specific report by UUID

## 📚 Filter Syntax (OData)

### Comparison Operators
- `eq` - Equals
- `ne` - Not equals
- `gt`, `ge` - Greater than (or equal)
- `lt`, `le` - Less than (or equal)

### Logical Operators
- `and`, `or`, `not`

### String Functions
- `contains(field, 'value')`
- `startswith(field, 'value')`
- `endswith(field, 'value')`

### Examples
```
serialNumber eq 'SN-001'
partNumber eq 'PN-001' and result eq 'Passed'
start ge 2026-01-01 and start lt 2026-02-01
reportType eq 'T' and operationCode eq '10'
contains(serialNumber, '1234')
result eq 'Failed' or result eq 'Error'
```

## 📖 Documentation Files

- **README.md** - Comprehensive guide with examples
- **FILE_INVENTORY.md** - Complete file listing

## 🔗 Relationship with Other Folders

### NET8_UUT_UUR_Classes (Report Creation)
- Contains: UUTReport, UURReport, Step classes
- Purpose: Create new test reports
- Methods: CreateUUTReport(), CreateUURReport()

### NET8_Report_Headers_And_Listing (Report Querying)
- Contains: ReportHeader, WatsReportHeader
- Purpose: Query existing reports
- Methods: FindReportHeaders(), FindReports()

### Shared Components
Both folders share:
- Base Report class
- TDM API class
- Core utilities
- Schemas
- Enumerations

## ✨ What's Included

✅ Modern report header querying (FindReportHeaders)  
✅ Legacy report querying support (FindReports)  
✅ OData-style filtering  
✅ Pagination support  
✅ Base Report class concept  
✅ Client/station information models  
✅ Process type converters  
✅ Result and status models  
✅ Complete documentation  

## 💡 Key Points

- **Use FindReportHeaders** for new code (modern OData API)
- **FindReports is deprecated** but still functional
- **Pagination** supported via skip parameter
- **Filters** use OData syntax (modern) or custom syntax (legacy)
- **ReportHeader** is the modern model to use
- **WatsReportHeader** is legacy (marked obsolete)

## 🚀 Quick Start

1. **Initialize API**
```csharp
TDM api = new TDM();
```

2. **Query Reports**
```csharp
var headers = api.FindReportHeaders(
    filter: "serialNumber eq 'SN-12345'",
    top: 10
);
```

3. **Process Results**
```csharp
foreach (var header in headers)
{
    Console.WriteLine($"{header.SerialNumber}: {header.Result}");
}
```

---

**Created:** January 30, 2026  
**Total Files:** 31  
**Status:** ✅ Complete
