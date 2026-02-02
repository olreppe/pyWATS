# Detailed Code Quality Findings

## Date: 2026-02-02

## Executive Summary
Comprehensive review of 72 example files and 12+ documentation files reveals widespread issues with:
- String literals instead of type-safe enums
- Missing or incorrect imports  
- Missing type hints
- Inconsistent usage patterns

## Critical Issues Found

### 1. Non-Existent Import: UUTStepType
**Severity:** HIGH - Code won't run  
**Affected Files:**
- `examples/domains/report_examples.py` line 62
- Multiple other report examples

**Issue:** Code imports `from pywats.domains.report.enums import UUTStepType` but this enum doesn't exist.

**Fix:** Should use `from pywats.shared.enums import StepType` instead, OR the actual string literals defined in the models like "NumericLimitTest", "PassFailTest", etc.

### 2. String Literals for Status Values
**Severity:** MEDIUM - Works but not type-safe  
**Pattern:** Using "Passed", "Failed", "Error" strings instead of StepStatus enum

**Examples:**
- `examples/domains/report_examples.py` line 550: `s.status == "Failed"` 
- `examples/converters/csv_converter.py`: Multiple instances of `"Failed"` string
- `examples/report/step_types.py` line 73: `report.result = "Passed"`

**Available Enum:** `StepStatus.Passed`, `StepStatus.Failed` from `pywats.domains.report.report_models.common_types`

**Issue:** Not using the enum for status comparisons and assignments.

### 3. OData Filter String Literals  
**Severity:** LOW - OData requires strings, but could use constants
**Pattern:** Using hardcoded strings in OData filters

**Examples:**
- `examples/report/query_reports.py` line 83: `odata_filter="result eq 'Failed'"`
- `examples/report/query_reports.py` line 126: `odata_filter="partNumber eq 'WIDGET-001' and result eq 'Failed'"`

**Note:** OData filters inherently use strings, but we could define constants for field names and values to prevent typos.

### 4. Missing Type Hints
**Severity:** MEDIUM - Reduces code clarity
**Pattern:** Function parameters and return types without type annotations

**Examples:**
- Many example functions don't specify parameter types
- Return types not specified (should be `-> None` or actual return type)

### 5. Inconsistent Enum Usage in Analytics
**Severity:** MEDIUM  
**Pattern:** Examples don't use available Dimension, KPI, SortDirection enums

**Available Enums:**
- `Dimension` - for dimension fields  
- `KPI` - for KPI metrics
- `DimensionBuilder` - fluent builder for dimension strings
- `SortDirection` - ASC/DESC

**Examples:**
- `examples/analytics/yield_analysis.py` - Creates WATSFilter but doesn't use DimensionBuilder or enums for dimensions

### 6. Direct Result String Comparison
**Severity:** MEDIUM  
**Pattern:** Comparing unit/report `result` field with strings

**Examples:**
- `examples/production/phase_management.py` line 95: `if unit.status == "Failed":`

**Issue:** Should use proper status enum if available

### 7. Converter Examples with Mixed Status Types
**Severity:** MEDIUM
**Pattern:** Mixing StepStatus enum with string literals

**Examples:**
- `examples/converters/csv_converter.py`: Uses `StepStatus.Passed` in some places and `"Failed"` string in others

**Fix:** Be consistent - use StepStatus enum everywhere

## Files Requiring Updates

### High Priority (Broken Code)
1. ✗ examples/domains/report_examples.py - Invalid import  
2. ✗ examples/report/create_uur_report.py - Check imports
3. ✗ examples/report/create_uut_report.py - Check imports
4. ✗ examples/report/step_types.py - Check imports

### Medium Priority (Type Safety)
5. examples/analytics/yield_analysis.py - Add dimension enums
6. examples/analytics/*.py (7 files) - Review all analytics examples
7. examples/production/phase_management.py - Status comparison
8. examples/converters/*.py (6 files) - Consistent enum usage
9. examples/process/operations.py - Result strings
10. examples/report/query_reports.py - OData filter constants

### Lower Priority (Type Hints & Polish)
- All 72 example files need type hint review
- Documentation code snippets need review

## Enums Available for Use

### From pywats.shared.enums:
- `StatusFilter` - Passed, Failed, Error, Terminated, Done, Skipped
- `RunFilter` - FIRST, SECOND, THIRD, LAST, ALL  
- `StepType` - NumericLimit, PassFail, StringValue, etc.
- `CompOp` - Comparison operators (GELE, GT, LT, etc.)
- `SortDirection` - ASC, DESC
- `QueueItemStatus` - pending, processing, completed, failed, suspended

### From pywats.domains.report.report_models.common_types:
- `StepStatus` - Passed, Failed, Error, Terminated, Done, Skipped, Running, Waiting
- `ReportStatus` - (same values as StepStatus)
- `StepGroup` - Parallel, Sequential, Conditional
- `ReportType` - UUT, UUR, Unknown  
- `ChartType` - Line, Bar, Scatter, etc.
- `FlowType` - PassFail, Sequence, etc.

### From pywats.domains.report.enums:
- `DateGrouping` - YEAR, QUARTER, MONTH, WEEK, DAY, HOUR
- `ReportType` - UUT ("U"), UUR ("R")
- `ImportMode` - Import, Active

### From pywats.domains.analytics.enums:
- `YieldDataType` - FIRST_PASS, FINAL, ROLLED
- `AlarmType` - REPORT, YIELD_VOLUME, SERIAL_NUMBER, MEASUREMENT, ASSET
- `ProcessType` - TEST, REPAIR, CALIBRATION
- `Dimension` - 30+ dimension fields (partNumber, stationName, period, etc.)
- `RepairDimension` - Repair-specific dimensions
- `KPI` - unitCount, fpy, spy, etc.
- `RepairKPI` - repairCount, etc.
- `DimensionBuilder` - Builder class for constructing dimension queries

### From other domains:
- `ProductState`, `SerialNumberIdentifier`, `TicketPriority`, `PackageStatus`, `AssetState`, etc.

## Next Steps
1. Fix high-priority broken imports immediately
2. Systematically update all examples to use proper enums
3. Add type hints to all function signatures
4. Update documentation to match corrected examples
5. Run sample of examples to verify they work
6. Update CHANGELOG.md

## Estimated Scope
- ~72 Python example files to review/fix
- ~12 documentation files to review
- Estimate 2-5 issues per file average = 100-400 individual fixes
