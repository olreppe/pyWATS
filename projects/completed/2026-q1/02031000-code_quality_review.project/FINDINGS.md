# Findings Tracker

## Summary Statistics
- **Files Reviewed:** 10/72 examples + 0/12 docs  
- **Issues Found:** 25+
- **Issues Fixed:** 14

## Fixed Issues

### Converter Examples
1. ✅ `examples/converters/csv_converter.py` - Fixed 6 instances of "Failed" string → StepStatus.Failed
2. ✅ `examples/converters/json_converter.py` - Added StepStatus/ReportStatus imports, improved result mapping
3. ✅ `examples/converters/xml_converter.py` - Added StepStatus/ReportStatus imports
4. ✅ `examples/converters/converter_template.py` - Fixed incorrect StepStatus import path

### Process Examples
5. ✅ `examples/process/operations.py` - Fixed "Passed" string → ReportStatus.Passed, fixed imports

## Remaining High Priority Issues

### Report Examples (API Mismatch - Major Issue)
**CRITICAL:** Report examples in `examples/domains/report_examples.py`, `examples/report/*.py` use a fictional API that doesn't exist:
- They call `api.report.add_uut_step()`, `api.report.start_uut_report()`, etc.
- These methods don't exist in the actual pyWATS API
- The real API uses direct model construction: `UUTReport()`, `root.add_numeric_step()`, etc.

**Files affected:**
- examples/domains/report_examples.py  
- examples/report/create_uur_report.py
- examples/report/create_uut_report.py
- examples/report/step_types.py

**These need complete rewrite, not just enum fixes.**

## Issue Categories

### 1. String Literals Instead of Enums ⚠️
**Status:** Partially fixed (converters done, others remain)

Remaining files with issues:
- examples/production/phase_management.py - line 95: `if unit.status == "Failed"`
- examples/domains/report_examples.py - line 550: `s.status == "Failed"`  
- examples/report/*.py - Multiple instances (but API is broken anyway)

### 2. Missing/Incorrect Imports ✅
**Status:** Fixed in reviewed files

Fixed:
- json_converter.py - Added StepStatus, ReportStatus
- xml_converter.py - Added StepStatus, ReportStatus
- converter_template.py - Fixed import path
- process/operations.py - Fixed import path

### 3. API Mismatch (Report Examples) 🚨
**Status:** Identified, requires major refactoring

The report examples use methods that don't exist. Should use:
- Direct model construction: `UUTReport(pn="...", sn="...", ...)`
- Factory methods: `root = report.get_root_sequence_call()`
- Step addition: `root.add_numeric_step(...)`

See `src/pywats/tools/test_uut.py` for correct usage pattern.

## Next Steps
1. ✅ Fix converter enum usage (COMPLETED)
2. ✅ Fix process enum usage (COMPLETED)
3. ⏭️ Fix production examples enum usage
4. ⏭️ Fix analytics examples to use Dimension/KPI enums
5. ⏭️ Fix product/asset examples if issues found
6. ⏭️ Add type hints to all examples
7. ⏭️ Document report API mismatch issue
8. ⏭️ Fix documentation code snippets
