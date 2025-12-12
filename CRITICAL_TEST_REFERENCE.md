# Report Module Critical Test Reference

## Overview

The `test_advanced_uut_comprehensive.py` test is a **CRITICAL** test that must pass before deploying any changes to the report module. This test validates the entire report creation, submission, and retrieval pipeline.

## What This Test Validates

### 1. All Step Types
- **NumericStep**: Single numeric measurements with all comparison operators (GELE, GT, LT, EQ, NE, GE, LE, LOG)
- **MultiNumericStep**: Multiple numeric measurements in a single step
- **BooleanStep**: Single boolean/pass-fail tests
- **MultiBooleanStep**: Multiple boolean tests
- **StringStep**: Single string value tests
- **MultiStringStep**: Multiple string values
- **ChartStep**: Chart/graph data with various chart types
- **SequenceCall**: Nested test sequences (containers)
- **GenericStep**: Flow control steps (If, For, While, Action, Statement, etc.)
- **ActionStep**: Procedure/action steps

### 2. Deep Hierarchy
- 5+ levels of nested SequenceCall structures
- Parent-child relationships maintained throughout
- Proper step ordering preserved

### 3. Extensive Numeric Testing
- All comparison operators: GELE, GT, LT, EQ, NE, GE, LE, LOG
- Pass/fail status variations
- Multiple units (V, A, Ω, °C, Hz, dB, %, etc.)
- High precision values
- Multi-measurement steps with mixed operators

### 4. Chart Step Validation
- Multiple chart types:
  - LINE: Standard line charts
  - LINE_LOG_X: Log-scale X axis
  - LINE_LOG_Y: Log-scale Y axis
  - LINE_LOG_XY: Log-scale both axes
- Complex data series:
  - Frequency response (Bode plots)
  - Step response
  - Harmonic analysis
  - Noise spectrum
  - Power profiles
  - Temperature cycling
- Multiple series per chart
- Reference lines and limits

### 5. API Validation
- Report submission via `send_uut_report()`
- Server processing wait loop
- Report retrieval via `get_uut_reports()` and `get_uut_report()`
- Data integrity verification
- Hierarchy preservation validation

### 6. Real-World Test Scenarios
- Power supply initialization
- Temperature monitoring
- Digital I/O testing
- Analog signal tests (ADC/DAC)
- Communication interfaces (I2C, SPI, UART)
- Performance testing (frequency response, step response, harmonics)
- Stress testing (temperature cycling, voltage stress)
- Flow control logic
- Cleanup and finalization

## Running the Test

### Run only the critical test:
```bash
pytest tests/test_advanced_uut_comprehensive.py -v
```

### Run all critical tests:
```bash
pytest -m critical -v
```

### Run with detailed output:
```bash
pytest tests/test_advanced_uut_comprehensive.py -v -s
```

## Test Output

The test provides detailed progress information:
- Report creation progress with section names
- Total step count
- Hierarchy depth
- Submission timing
- Processing wait status
- Verification results
- Performance metrics

Example output:
```
================================================================================
Creating Advanced Comprehensive UUT Report
Serial Number: ADVANCED-UUT-20251212-143022-123456
================================================================================

Building Initialization Sequence...
Building Functional Tests...
Building Performance Tests with Charts...
Building Stress Tests...
Building Flow Control Tests...
Building Cleanup Sequence...

================================================================================
Report Structure Complete!
Total Steps Created: 150
Hierarchy Depth: 5 levels
================================================================================

Submitting report to server...
✓ Report submitted successfully (2.35s)

Waiting for report processing...
✓ Report found (ID: b0612e7a-ea2f-423f-bfd8-505ca52ab042)
✓ Full report loaded

================================================================================
Report Verification
================================================================================

✓ Serial number verified: ADVANCED-UUT-20251212-143022-123456
✓ Part number verified: ADVANCED-UUT-TEST
✓ Result verified: PASSED
✓ Root sequence exists
✓ Main sequences verified: 6 sequences
✓ Sequence found: System Initialization
✓ Sequence found: Functional Tests
✓ Sequence found: Performance Tests
✓ Sequence found: Stress Tests
✓ Nested hierarchy verified (depth >= 3)
✓ Numeric steps verified: 15 steps
✓ Chart steps verified: 8 charts
✓ Total steps in loaded report: 150

================================================================================
✓ ALL VERIFICATIONS PASSED!
================================================================================

Performance Summary:
  - Steps Created: 150
  - Steps Loaded: 150
  - Submit Time: 2.35s
  - Load Time: 5.12s
  - Total Time: 7.47s
================================================================================
```

## When to Run This Test

### MANDATORY - Before:
1. Committing changes to any file in `src/pywats/domains/report/`
2. Modifying step types or step hierarchy
3. Changing serialization/deserialization logic
4. Updating the UUTReport model
5. Modifying chart handling
6. Changing numeric measurement logic
7. Updating API endpoints for report submission/retrieval

### RECOMMENDED - Before:
1. Major refactoring of any core modules
2. Updating dependencies (Pydantic, etc.)
3. Changing validation logic
4. Adding new step types
5. Modifying the step discriminator

## Troubleshooting

### Test Fails on Submission
- Check server connectivity
- Verify credentials in `conftest.py`
- Check server logs for errors
- Validate report structure before submission

### Test Fails on Retrieval
- Increase timeout (default: 60 seconds)
- Check server processing queue
- Verify report was actually created
- Check for server-side validation errors

### Step Count Mismatch
- Some steps may be filtered by server
- Check for validation failures on specific steps
- Verify step type discrimination is working
- Look for serialization issues

### Chart Steps Missing
- Verify chart series data format (semicolon-separated)
- Check chart type enums are correct
- Validate x_data and y_data are present
- Ensure chart is attached to step correctly

## Updating This Test

When adding new features to the report module:

1. Add test cases for new step types
2. Include new chart types or features
3. Test new comparison operators
4. Add hierarchy variations
5. Update expected counts and validations
6. Document new test scenarios

## Integration with CI/CD

This test should be:
- Run on every pull request
- Required to pass before merging
- Part of the deployment gate
- Included in nightly regression tests

## Related Tests

- `test_step_discriminator.py` - Step type discrimination
- `test_step_types_server_integration.py` - Server round-trip
- `test_uut_model_comprehensive.py` - Model construction
- `tests/acceptance/test_scenario_step_hierarchy.py` - Hierarchy scenarios

## Contact

For questions about this test or report module changes, contact the pyWATS maintainers.
