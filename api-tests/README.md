# pyWATS Test Suite

## Structure

Tests are organized by module, matching the `src/wats/domains/` structure:

```
api-tests/
├── conftest.py              # Shared fixtures
├── README.md
│
├── analytics/               # Analytics domain tests
│   ├── test_service.py      # Unit tests with mock repository
│   ├── test_integration.py  # Server integration tests
│   ├── test_dynamic_repair.py
│   ├── test_measurement_api.py
│   └── test_unit_flow.py
│
├── asset/                   # Asset domain tests
│   ├── test_service.py      # Unit tests with mock repository
│   ├── test_integration.py  # Server integration tests
│   └── test_workflow.py     # End-to-end workflows
│
├── process/                 # Process domain tests
│   ├── test_service.py
│   └── test_models.py
│
├── product/                 # Product domain tests
│   ├── test_service.py
│   └── test_integration.py
│
├── production/              # Production domain tests
│   ├── test_service.py
│   ├── test_integration.py
│   └── test_workflow.py
│
├── report/                  # Report domain tests
│   ├── test_service.py
│   ├── test_integration.py
│   ├── test_models.py       # UUT model validation
│   ├── test_import_mode.py  # ImportMode feature
│   ├── test_step_types.py
│   ├── test_step_discriminator.py
│   ├── test_timezone.py
│   ├── test_timezone_sync.py
│   ├── test_filter.py
│   ├── test_robustness.py
│   └── test_workflow.py     # End-to-end UUT submission
│
├── rootcause/               # RootCause domain tests
│   ├── test_service.py
│   ├── test_integration.py
│   ├── test_d8_workflow.py  # 8D problem-solving workflow
│   └── test_comprehensive.py
│
├── software/                # Software domain tests
│   ├── test_service.py
│   ├── test_integration.py
│   └── test_comprehensive.py
│
├── cross_cutting/           # Cross-cutting concerns
│   ├── test_client_instances.py
│   ├── test_instances.py
│   ├── test_throttle.py
│   └── test_boxbuild.py
│
├── fixtures/                # Test data and configs
│   ├── client_a_config.json
│   ├── client_b_config.json
│   └── scenarios/
│
└── scripts/                 # Debug utilities (not pytest)
    ├── debug_boxbuild_api.py
    └── server_roundtrip.py
```

## Naming Convention

| File Name | Purpose | Requires Server |
|-----------|---------|-----------------|
| `test_service.py` | Unit tests with mock repositories | No |
| `test_models.py` | Pydantic model validation | No |
| `test_integration.py` | Direct WATS API calls | Yes |
| `test_workflow.py` | End-to-end business scenarios | Yes |
| `test_comprehensive.py` | Full feature coverage | Yes |

## Setup

1. Install test dependencies:
```bash
pip install pytest pytest-cov pytest-mock pytest-asyncio
```

2. Configure test instances in `fixtures/`:
   - Copy `client_a_config.template.json` to `client_a_config.json`
   - Set your WATS server URL and token

## Running Tests

Run all tests:
```bash
pytest api-tests/
```

Run a specific module:
```bash
pytest api-tests/report/          # All report tests
pytest api-tests/report/test_service.py  # Only service tests
```

Run only unit tests (no server required):
```bash
pytest api-tests/*/test_service.py api-tests/*/test_models.py
```

Run with coverage:
```bash
pytest api-tests/ --cov=pywats --cov-report=html
```

## Test Categories

### Unit Tests (No Server Required)
- `test_service.py` - Tests service layer with mock repositories
- `test_models.py` - Tests Pydantic model validation
- `test_import_mode.py` - Tests ImportMode enum and auto-calculation
- `test_step_discriminator.py` - Tests step type serialization
- `test_throttle.py` - Tests RateLimiter class

### Integration Tests (Server Required)
- `test_integration.py` - Direct API endpoint tests
- `test_workflow.py` - Full business scenario tests
- `test_comprehensive.py` - Complete feature validation
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
