# pyWATS Test Suite

> **⚠️ CRITICAL WARNING - DO NOT RUN ON PRODUCTION SERVERS**
>
> **This test suite creates extensive test data on the WATS server and should ONLY be run against dedicated sandbox/development environments.**
>
> - ❌ **NEVER** run these tests against production WATS servers
> - ❌ **NEVER** use production credentials in test configuration
> - ✅ **ALWAYS** use a dedicated sandbox server for testing
> - ✅ **ALWAYS** verify you're connected to the correct environment before running tests
>
> **Test data created includes:** UUT reports, products, parts, serial numbers, stations, processes, and various domain-specific entities. Cleaning up this data from a production environment is extremely time-consuming and error-prone.
>
> **Designed by:** Ola Lund Reppe, Integration Architect, The WATS Company AS

This directory contains the comprehensive test suite for pyWATS, organized by functional area for better discoverability and maintenance.

## Directory Structure

```
tests/
├── domains/           # Domain-specific API tests
│   ├── analytics/     # Analytics domain tests
│   ├── asset/         # Asset management tests
│   ├── process/       # Process domain tests
│   ├── product/       # Product domain tests
│   ├── production/    # Production tracking tests
│   ├── report/        # Test report submission tests
│   ├── rootcause/     # Root cause analysis tests
│   └── software/      # Software distribution tests
├── client/            # Client-specific tests
│   ├── test_config.py
│   ├── test_converters.py
│   ├── test_integration.py
│   ├── test_ipc.py
│   ├── test_queue.py
│   └── test_service.py
├── infrastructure/    # Infrastructure and core library tests
│   ├── test_pywats_cfx.py
│   └── test_pywats_events.py
├── integration/       # Cross-domain integration tests
│   ├── test_batch.py
│   ├── test_boxbuild.py
│   ├── test_client_instances.py
│   ├── test_instances.py
│   ├── test_pagination.py
│   ├── test_retry.py
│   └── test_throttle.py
└── fixtures/          # Shared test fixtures and data
    ├── acceptance_conftest.py
    ├── data/
    ├── instances/
    └── scenarios/
```

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Tests by Category

**Domain Tests:**
```bash
pytest tests/domains/           # All domain tests
pytest tests/domains/report/    # Specific domain
```

**Client Tests:**
```bash
pytest tests/client/
```

**Infrastructure Tests:**
```bash
pytest tests/infrastructure/
```

**Integration Tests:**
```bash
pytest tests/integration/
```

### Run Specific Test Files
```bash
pytest tests/domains/report/test_integration.py
pytest tests/client/test_service.py
```

### Run with Coverage
```bash
pytest tests/domains/report/ --cov=src/pywats/domains/report
```

## Test Categories

### Domain Tests (`tests/domains/`)
Tests for individual WATS domains (previously in `api-tests/analytics/`, `api-tests/report/`, etc.). Each domain folder contains:
- `test_integration.py` - End-to-end domain functionality
- `test_service.py` - Service layer tests
- `test_models.py` - Data model tests (where applicable)
- `test_workflow.py` - Multi-step workflows (where applicable)

**Key domains:**
- **analytics**: Dynamic repair, unit flow, measurement API
- **asset**: Station management, calibration tracking
- **product**: BOM management, product definitions
- **production**: Serial number tracking, unit verification
- **report**: UUT/UUR submission, step types, timezone handling
- **rootcause**: 8D workflows, defect tracking
- **software**: Package distribution

### Client Tests (`tests/client/`)
Tests for the pyWATS client service and converter framework (previously in `api-tests/client/`):
- Configuration management
- Converter loading and execution
- IPC communication
- Queue handling
- Service lifecycle

### Infrastructure Tests (`tests/infrastructure/`)
Core library and infrastructure tests (previously in `tests/`):
- CFX integration (`test_pywats_cfx.py`)
- Event system (`test_pywats_events.py`)

### Integration Tests (`tests/integration/`)
Cross-cutting concerns and multi-domain workflows (previously in `api-tests/cross_cutting/`):
- Batch operations
- Box build workflows
- Client instance management
- Pagination patterns
- Retry logic
- Throttling

### Fixtures (`tests/fixtures/`)
Shared test data and configuration:
- **data/**: Test data files
- **instances/**: Multi-client test configurations
- **scenarios/**: Complex test scenarios and data generators

## Configuration

Tests use `conftest.py` at the root level (`tests/conftest.py`) for shared fixtures and configuration.

### Environment Setup

Tests require:
- WATS server connection (configured via environment variables)
- Test client instances (see `fixtures/instances/`)

See `.env.example` in the project root for required environment variables.

## Best Practices

1. **Test Naming**: Follow `test_*.py` convention
2. **Organization**: Place tests in the appropriate category folder
3. **Fixtures**: Use shared fixtures from `tests/fixtures/` or `conftest.py`
4. **Independence**: Tests should be independent and not rely on execution order
5. **Cleanup**: Use fixtures with proper teardown to clean up test data
6. **Documentation**: Document complex test scenarios and prerequisites

## Migration Notes

This test structure replaces the previous `api-tests/` organization (January 2025):
- `api-tests/analytics/` → `tests/domains/analytics/`
- `api-tests/client/` → `tests/client/`
- `api-tests/cross_cutting/` → `tests/integration/`
- `tests/test_pywats_*.py` → `tests/infrastructure/test_pywats_*.py`
- `api-tests/fixtures/` → `tests/fixtures/`

For historical context, see `tests/api-tests-readme.md` (previous API tests documentation).

## Contributing

When adding new tests:
1. Determine the correct category (domain, client, infrastructure, integration)
2. Follow existing naming conventions and structure
3. Add shared fixtures to `conftest.py` if needed across multiple test files
4. Update this README if adding a new test category or significant test suite
