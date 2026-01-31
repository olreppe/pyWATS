# File Inventory - NET8_UUT_UUR_Classes

Generated: January 30, 2026
Total Files: 53 (52 .cs files + 1 README.md)

## Root Level (8 files)
1. AdditionalData.cs
2. Enums.cs
3. IReportConverter.cs
4. OperationType.cs
5. Processes.cs
6. README.md
7. RepairType.cs
8. Report.cs
9. TDM.cs

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

## Schemas/ (3 files)
1. Schemas/Converters.cs
2. Schemas/WATS Report.designer.cs
3. Schemas/WATS WSXF Report.cs

## Statistics/ (5 files)
1. Statistics/ServiceStatus.cs
2. Statistics/Statistics.cs
3. Statistics/StatisticsReader.cs
4. Statistics/TestYield.cs
5. Statistics/YieldMonitor.cs

## UURClasses/ (6 files)
1. UURClasses/FailCodes.cs
2. UURClasses/Failure.cs
3. UURClasses/MiscUURInfo.cs
4. UURClasses/UURAttachment.cs
5. UURClasses/UURPartInfo.cs
6. UURClasses/UURReport.cs

## UUTClasses/ (20 files)
1. UUTClasses/AdditionalResult.cs
2. UUTClasses/Asset.cs
3. UUTClasses/AssetStatistics.cs
4. UUTClasses/Attachment.cs
5. UUTClasses/CallExeStep.cs
6. UUTClasses/Chart.cs
7. UUTClasses/GenericStep.cs
8. UUTClasses/MessagePopupStep.cs
9. UUTClasses/MiscUUTInfo.cs
10. UUTClasses/NumericLimitStep.cs
11. UUTClasses/NumericLimitTest.cs
12. UUTClasses/PassFailStep.cs
13. UUTClasses/PassFailTest.cs
14. UUTClasses/PropertyLoader.cs
15. UUTClasses/SequenceCall.cs
16. UUTClasses/Step.cs
17. UUTClasses/StringValueStep.cs
18. UUTClasses/StringValueTest.cs
19. UUTClasses/UUTPartInfo.cs
20. UUTClasses/UUTReport.cs

## File Categories

### Report Creation Core (3 files)
- TDM.cs - Main API for creating reports
- Report.cs - Base class for all reports
- IReportConverter.cs - Interface for custom converters

### UUT Report Classes (20 files in UUTClasses/)
All classes needed to create and populate UUT (Unit Under Test) reports

### UUR Report Classes (6 files in UURClasses/)
All classes needed to create and populate UUR (Unit Under Repair) reports

### Schema Definitions (3 files in Schemas/)
XML schema classes for WRML and WSXF formats

### Support Classes (8 files)
- Enums.cs - All enumerations
- OperationType.cs - Operation type definitions
- RepairType.cs - Repair type definitions
- AdditionalData.cs - Additional data handling
- Processes.cs - Process definitions

### Core Infrastructure (10 files in Core/)
Utility classes, extensions, settings, security, and exception handling

### Statistics (5 files in Statistics/)
Classes for tracking test statistics and yield monitoring

## Source Information
All files are from projects targeting .NET 8:
- Source: Interface.TDM project (net48;net8.0-windows10.0.18362.0)
- Source: WATS-Core project (net8.0-windows10.0.18362.0)
- Location: c:\Users\ola.lund.reppe\Source\repos\WATS Client\
