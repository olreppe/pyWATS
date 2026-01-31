# .NET 8 Core - UUT and UUR Report Classes

This folder contains all classes related to UUT (Unit Under Test) and UUR (Unit Under Repair) report creation for .NET 8 Core.

## Source Projects
These files are copied from the following projects that target .NET 8:
- **Interface.TDM** - Targets: net48;net8.0-windows10.0.18362.0
- **Core (WATS-Core)** - Targets: net8.0-windows10.0.18362.0

## Directory Structure

### Root Files
- **TDM.cs** - Main TDM API class for creating and managing reports
- **Report.cs** - Base class for both UUT and UUR reports
- **Enums.cs** - All enumerations including UUTStatusType, StepStatusType, etc.
- **OperationType.cs** - Operation type definitions
- **RepairType.cs** - Repair type definitions for UUR reports
- **AdditionalData.cs** - Additional data handling
- **IReportConverter.cs** - Interface for report converters
- **Processes.cs** - Process-related classes

### UUTClasses/
Contains all classes for UUT (Unit Under Test) report creation:
- **UUTReport.cs** - Main UUT report class
- **UUTPartInfo.cs** - Part information for UUT
- **Step.cs** - Base step class
- **SequenceCall.cs** - Sequence call steps
- **NumericLimitStep.cs** / **NumericLimitTest.cs** - Numeric limit testing
- **PassFailStep.cs** / **PassFailTest.cs** - Pass/fail testing
- **StringValueStep.cs** / **StringValueTest.cs** - String value testing
- **CallExeStep.cs** - Executable call steps
- **GenericStep.cs** - Generic step implementation
- **MessagePopupStep.cs** - Message popup steps
- **PropertyLoader.cs** - Property loader functionality
- **Asset.cs** - Asset management
- **AssetStatistics.cs** - Asset statistics
- **Attachment.cs** - File attachments
- **Chart.cs** - Chart data
- **MiscUUTInfo.cs** - Miscellaneous UUT information
- **AdditionalResult.cs** - Additional result data

### UURClasses/
Contains all classes for UUR (Unit Under Repair) report creation:
- **UURReport.cs** - Main UUR report class
- **UURPartInfo.cs** - Part information for UUR
- **UURAttachment.cs** - Attachments for repair reports
- **Failure.cs** - Failure information
- **FailCodes.cs** - Failure code management
- **MiscUURInfo.cs** - Miscellaneous UUR information

### Schemas/
XML schema-related classes:
- **WATS Report.designer.cs** - WRML (WATS Report Markup Language) schema classes
- **WATS WSXF Report.cs** - WSXF (WATS Standard eXchange Format) schema classes
- **Converters.cs** - Schema converters

### Core/
Core utilities and infrastructure:
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

### Statistics/
Statistics and monitoring classes:
- **Statistics.cs** - Statistics tracking
- **StatisticsReader.cs** - Statistics reading
- **ServiceStatus.cs** - Service status monitoring
- **TestYield.cs** - Test yield calculations
- **YieldMonitor.cs** - Yield monitoring

## Key Classes for Report Creation

### Creating UUT Reports
```csharp
// Main class: TDM
// Method: CreateUUTReport()
// Returns: UUTReport instance
```

The `UUTReport` class allows you to:
- Set header information (part number, serial number, operator, etc.)
- Add test steps (NumericLimit, PassFail, StringValue, etc.)
- Add sequence calls and nested steps
- Attach files and additional data
- Submit reports to WATS server

### Creating UUR Reports
```csharp
// Main class: TDM
// Method: CreateUURReport()
// Returns: UURReport instance
```

The `UURReport` class allows you to:
- Reference a UUT report or create standalone repair report
- Define repair type and operation
- Add failure information and failure codes
- Add part information for repaired units
- Add attachments and comments

## Important Enumerations

### UUTStatusType
- Passed
- Failed
- Error
- Terminated

### StepStatusType
- Passed
- Done
- Skipped
- Failed
- Error
- Terminated

### ReportType
- UUT (Unit Under Test)
- UUR (Unit Under Repair)

## Dependencies
These classes require:
- .NET 8.0 or later
- Windows 10.0.18362.0 or later
- WATS Server connection for report submission

## Usage Notes
1. All classes use the `Virinco.WATS.Interface` namespace
2. Schema classes use `Virinco.WATS.Schemas.WRML` namespace
3. Report creation follows a builder pattern with method chaining
4. Validation is performed based on ValidationModeType setting
5. Reports can be submitted online or saved to offline queue

## Total Files: 52
