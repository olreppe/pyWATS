# pyWATS Test Suite

## Setup

1. Install pytest:
```bash
pip install pytest pytest-cov
```

2. Update test configuration in `conftest.py`:
   - Set your WATS server URL
   - Configure test credentials
   - Adjust test data as needed

## Running Tests

Run all tests:
```bash
pytest
```

Run specific module:
```bash
pytest tests/test_report.py
```

Run with coverage:
```bash
pytest --cov=pywats --cov-report=html
```

## Test Structure

### Core Module Tests

- `test_report.py` - Report creation, submission, querying
- `test_asset.py` - Asset management and state tracking
- `test_software.py` - Software package upload and management
- `test_production.py` - Unit management, tags, box build
- `test_product.py` - Product definitions and revisions
- `test_root_cause.py` - Ticket integration
- `test_app.py` - Statistics and data retrieval

### Critical Comprehensive Tests

- `test_advanced_uut_comprehensive.py` - **CRITICAL**: Advanced comprehensive UUT test with all step types
  - Tests ALL step types (Numeric, Boolean, String, Chart, Generic, Multi-*, etc.)
  - Extensive hierarchy testing (5+ levels deep)
  - All numeric comparison operators
  - Multiple chart types with complex data
  - API submission and retrieval validation
  - **This test MUST pass before deploying report module changes**

### Step Type Tests

- `test_step_discriminator.py` - Step type discrimination and serialization
- `test_step_types_server_integration.py` - Server round-trip for step types
- `test_uut_model_comprehensive.py` - Comprehensive UUT model construction

## Expected Behavior

Tests use `pytest.skip()` when:

- Server is not available
- Endpoints return errors
- Test data doesn't exist

This allows us to identify which features are working without breaking the test suite.

## Notes

- Product revision manipulation requires separate API calls
- Misc info on products needs separate functions
- Some endpoints may not work as expected - tests document actual behavior
