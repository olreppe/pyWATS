# Quick Start Guide - UUT and UUR Report Classes (.NET 8)

## Overview
This folder contains all .NET 8 Core classes needed for creating UUT (Unit Under Test) and UUR (Unit Under Repair) reports in the WATS system.

## What's Included
- ✅ 52 C# source files
- ✅ Complete UUT report creation classes
- ✅ Complete UUR report creation classes
- ✅ All enumerations and type definitions
- ✅ Schema definitions (WRML & WSXF)
- ✅ Core utilities and infrastructure
- ✅ Statistics tracking classes

## Main Components

### 1. UUT (Unit Under Test) Reports
**Location:** `UUTClasses/`

**Main Class:** `UUTReport.cs`

**Purpose:** Create test reports for units being tested

**Key Features:**
- Add various test step types (Numeric, PassFail, String)
- Create hierarchical step structures with SequenceCall
- Attach files and additional data
- Track test execution time and results
- Set part information and serial numbers

**Step Types Available:**
- `NumericLimitStep` - For numeric measurements with limits
- `PassFailStep` - For boolean pass/fail tests
- `StringValueStep` - For string-based tests
- `CallExeStep` - For external executable calls
- `GenericStep` - For custom test steps
- `MessagePopupStep` - For message/information steps

### 2. UUR (Unit Under Repair) Reports
**Location:** `UURClasses/`

**Main Class:** `UURReport.cs`

**Purpose:** Create repair reports for units undergoing repair

**Key Features:**
- Link to original UUT report
- Record failure information
- Track repair operations
- Add failure codes
- Document repair steps and outcomes
- Attach repair documentation

### 3. TDM API
**File:** `TDM.cs`

**Purpose:** Main API class for creating and submitting reports

**Key Methods:**
```csharp
// Create UUT Report
UUTReport CreateUUTReport(...)

// Create UUR Report  
UURReport CreateUURReport(...)

// Submit reports
void Submit(Report report)
```

### 4. Enumerations
**File:** `Enums.cs`

**Important Enums:**
- `UUTStatusType` - Overall test status (Passed, Failed, Error, Terminated)
- `StepStatusType` - Individual step status
- `APIStatusType` - API connection status
- `TestModeType` - Test mode (Active, Import, TestStand)
- `ValidationModeType` - Validation behavior
- `SubmitMethod` - Report submission method

### 5. Type Definitions
- `OperationType.cs` - Defines test operations
- `RepairType.cs` - Defines repair operations
- `Processes.cs` - Process definitions

## Typical Usage Flow

### Creating a UUT Report
```csharp
// 1. Initialize TDM API
TDM api = new TDM();

// 2. Create UUT Report
UUTReport uut = api.CreateUUTReport(
    partNumber: "PN-12345",
    operatorName: "John Doe",
    partRevision: "Rev A",
    serialNumber: "SN-67890",
    operationType: api.GetOperationType("10"),
    sequenceName: "MainSequence",
    sequenceVersion: "1.0"
);

// 3. Set additional properties
uut.StartDateTime = DateTime.Now;
uut.Status = UUTStatusType.Passed;

// 4. Add test steps
var step = uut.GetRootSequenceCall()
    .AddNumericLimitStep("VoltageTest")
    .AddTest(5.0, 4.5, 5.5, "Volts", StepStatusType.Passed);

// 5. Submit report
api.Submit(uut);
```

### Creating a UUR Report
```csharp
// 1. Create UUR linked to a UUT
UURReport uur = api.CreateUURReport(
    operatorName: "Jane Smith",
    repairType: api.GetRepairType("Repair"),
    uutReport: existingUUT
);

// 2. Add failure information
var failure = uur.AddFailure();
failure.DefectCode = "DEF-001";
failure.Comment = "Component X failed";

// 3. Submit repair report
api.Submit(uur);
```

## Directory Structure
```
NET8_UUT_UUR_Classes/
├── README.md                    (Detailed documentation)
├── FILE_INVENTORY.md           (Complete file list)
├── QUICK_START.md              (This file)
├── Core/                       (Infrastructure)
│   ├── Security/
│   └── *.cs
├── Schemas/                    (XML schemas)
├── Statistics/                 (Test statistics)
├── UUTClasses/                (UUT report classes)
└── UURClasses/                (UUR report classes)
```

## Dependencies
- .NET 8.0 or later
- Windows 10.0.18362.0 or later
- WATS Server (for report submission)

## Key Namespaces
```csharp
using Virinco.WATS.Interface;           // Main API classes
using Virinco.WATS.Schemas.WRML;        // XML schema classes
using Virinco.WATS;                     // Core utilities
```

## Important Notes

### Validation
- Properties are validated based on `ValidationModeType`
- `ThrowExceptions` - Strict validation with exceptions
- `AutoTruncate` - Automatically truncates oversized data

### Submission Methods
- `Automatic` - Online if connected, offline queue otherwise
- `Online` - Synchronous, requires connection
- `Offline` - Always queued for async processing

### Test Modes
- `Active` - Normal testing with timing and validation
- `Import` - For importing pre-compiled data
- `TestStand` - For TestStand integration

## Common Scenarios

### 1. Multi-Step Test Sequence
```csharp
var root = uut.GetRootSequenceCall();
var seq = root.AddSequenceCall("Calibration", "Cal.seq", "1.0");
seq.AddNumericLimitStep("Step1").AddTest(...);
seq.AddPassFailStep("Step2").AddTest(...);
seq.AddStringValueStep("Step3").AddTest(...);
```

### 2. Adding Attachments
```csharp
uut.AddAttachment("photo.jpg", "image/jpeg", fileBytes);
```

### 3. Adding Misc Info
```csharp
uut.AddMiscInfo("Temperature", "25°C");
```

### 4. Hierarchical Steps
```csharp
var mainSeq = root.AddSequenceCall("Main", "main.seq", "1.0");
var subSeq = mainSeq.AddSequenceCall("Sub", "sub.seq", "1.0");
subSeq.AddNumericLimitStep("Measurement");
```

## For More Information
- See `README.md` for detailed class descriptions
- See `FILE_INVENTORY.md` for complete file listing
- Check individual class files for XML documentation comments

## Source Projects
These files originate from:
- **Interface.TDM** - Multi-targeting: net48;net8.0-windows10.0.18362.0
- **WATS-Core** - Targeting: net8.0-windows10.0.18362.0

Both projects are part of the WATS Client solution and support .NET 8 Core.
