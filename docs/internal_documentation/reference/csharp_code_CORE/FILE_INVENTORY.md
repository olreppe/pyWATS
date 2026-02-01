# File Inventory - NET8_Report_Headers_And_Listing

Generated: January 30, 2026
Total Files: 31 (30 .cs files + 1 README.md)

## Purpose
Classes for querying and retrieving existing report headers from WATS, including the base Report concept and report listing functionality.

## Root Level (7 files)
1. Enums.cs
2. OperationType.cs
3. Processes.cs
4. README.md
5. RepairType.cs
6. Report.cs
7. TDM.cs

## Core/ (7 files)
1. Core/Enum.cs
2. Core/Env.cs
3. Core/Extensions.cs
4. Core/GlobalUtilities.cs
5. Core/Registry.cs
6. Core/Settings.cs
7. Core/WATSException.cs

## Core/Security/ (3 files)
1. Core/Security/Cryptography.cs
2. Core/Security/Licensing.cs
3. Core/Security/SimpleAes.cs

## Models/ (4 files)
1. Models/Client.cs - Client/station information
2. Models/ClientVersion.cs - Client version info
3. Models/ProcessConverter.cs - JSON converter for processes
4. Models/ReportHeader.cs - **Modern report header model**

## Models/da-import/ (4 files)
1. Models/da-import/Codes.cs - Status/result codes
2. Models/da-import/Member.cs - Member data model
3. Models/da-import/ReportsWrmlUpsertResult.cs - Report submission results
4. Models/da-import/WatsReportHeader.cs - **Legacy report header model (deprecated)**

## Schemas/ (6 files)
1. Schemas/Converters.cs
2. Schemas/WATS Report.designer.cs
3. Schemas/WATS WSXF Report.cs
4. Schemas/Schemas/Converters.cs
5. Schemas/Schemas/WATS Report.designer.cs
6. Schemas/Schemas/WATS WSXF Report.cs

## File Categories

### Report Querying API (2 key files)
- **TDM.cs** - Main API with FindReportHeaders() and FindReports() methods
- **Report.cs** - Base class for all reports (UUT and UUR)

### Report Header Models (2 files)
- **Models/ReportHeader.cs** - Modern model (recommended)
- **Models/da-import/WatsReportHeader.cs** - Legacy model (deprecated)

### Supporting Models (6 files)
- Client information models
- Process converters
- Result models
- Member data

### Type Definitions (3 files)
- Enums.cs - All enumerations
- OperationType.cs - Operation type definitions
- RepairType.cs - Repair type definitions
- Processes.cs - Process definitions

### Core Infrastructure (10 files in Core/)
Utility classes, extensions, settings, security, and exception handling

### Schema Definitions (6 files in Schemas/)
XML schema classes for WRML and WSXF formats

## Key Methods in TDM.cs

### FindReportHeaders (Modern - Recommended)
```csharp
ReportHeader[] FindReportHeaders(
    string filter,
    int top,
    int skip = 0,
    string orderby = "start desc",
    string select = "",
    string expand = ""
)
```

### FindReports (Legacy - Deprecated)
```csharp
[Obsolete("Deprecated, use FindReportHeaders instead.")]
WatsReportHeader[] FindReports(
    string filter,
    int top,
    string orderby = "Start_UTC desc"
)
```

## Comparison with NET8_UUT_UUR_Classes

| Aspect | NET8_UUT_UUR_Classes | NET8_Report_Headers_And_Listing |
|--------|---------------------|--------------------------------|
| Purpose | **Create** new reports | **Query** existing reports |
| Main Classes | UUTReport, UURReport | ReportHeader, WatsReportHeader |
| Key Methods | CreateUUTReport(), CreateUURReport() | FindReportHeaders(), FindReports() |
| Focus | Building test data | Retrieving report summaries |
| Use Case | During testing | Reporting, analysis, lookup |

## Common Use Cases

### 1. Find Reports by Serial Number
Query all reports for a specific unit

### 2. Find Reports in Date Range
Get reports within specific time period

### 3. Find Failed Reports
Query reports by result status

### 4. Find Reports by Station
Get reports from specific test station

### 5. Pagination
Retrieve large result sets in pages

### 6. Report Lookup
Find specific report by UUID

## Filter Examples

### OData-style (FindReportHeaders)
```
serialNumber eq 'SN-12345'
partNumber eq 'PN-001' and result eq 'Failed'
start ge 2026-01-01 and start lt 2026-02-01
reportType eq 'T' and operationCode eq '10'
contains(serialNumber, '1234')
```

### Legacy-style (FindReports - Deprecated)
```
(SN eq 'SN-12345')
(PN eq 'PN-001') and (Result eq 'Failed')
(Start_UTC ge 2026-01-01) and (ReportType eq 'UUT')
```

## Source Information
All files are from projects targeting .NET 8:
- Source: Interface.TDM project (net48;net8.0-windows10.0.18362.0)
- Source: WATS-Core project (net8.0-windows10.0.18362.0)
- Location: c:\Users\ola.lund.reppe\Source\repos\WATS Client\

## Relationship to Report Creation

This folder complements NET8_UUT_UUR_Classes:
- **Create reports** → Use NET8_UUT_UUR_Classes
- **Query reports** → Use NET8_Report_Headers_And_Listing
- **Base Report class** → Shared between both folders
