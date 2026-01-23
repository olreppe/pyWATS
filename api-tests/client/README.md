# Client Test Suite

Comprehensive test suite for pyWATS Client application.

## Coverage Goals

- **Overall Target:** 80%+ code coverage
- **Unit Tests:** Core business logic, data validation, configuration
- **Integration Tests:** Service lifecycle, file watching, converter execution
- **Functional Tests:** End-to-end workflows

## Test Structure

```
api-tests/client/
├── conftest.py              # Shared fixtures and configuration
├── __init__.py              # Package documentation
├── test_config.py           # Configuration tests (✅ COMPLETE)
├── test_queue.py            # Queue manager tests (TODO)
├── test_converters.py       # Converter tests (TODO)
├── test_service_manager.py  # Service manager tests (TODO)
├── test_integration.py      # End-to-end tests (TODO)
└── README.md                # This file
```

## Running Tests

### All Client Tests

```bash
pytest api-tests/client/
```

### Specific Test File

```bash
pytest api-tests/client/test_config.py
pytest api-tests/client/test_queue.py
```

### With Coverage

```bash
# HTML report
pytest api-tests/client/ --cov=pywats_client --cov-report=html

# Terminal report
pytest api-tests/client/ --cov=pywats_client --cov-report=term-missing

# View HTML report
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html  # Linux
```

### By Test Type

```bash
# Unit tests only (fast, no external dependencies)
pytest api-tests/client/ -m unit

# Integration tests only (may require services)
pytest api-tests/client/ -m integration

# Exclude slow tests
pytest api-tests/client/ -m "not slow"
```

### Verbose Output

```bash
# Show test names and results
pytest api-tests/client/ -v

# Show print statements
pytest api-tests/client/ -s

# Both
pytest api-tests/client/ -vs
```

## Test Markers

Tests use pytest markers for categorization:

- `@pytest.mark.unit` - Unit tests (isolated, fast)
- `@pytest.mark.integration` - Integration tests (multiple components)
- `@pytest.mark.slow` - Long-running tests

## Test Coverage by Module

### ✅ Configuration (`test_config.py`)

**Status:** COMPLETE (21 tests)

**Coverage:**
- ConverterConfig dataclass
- ClientConfig dataclass  
- Configuration loading/saving
- Validation logic
- Default values
- Round-trip serialization

**Tests:**
- `test_create_converter_config` - Create from dict
- `test_converter_type_properties` - Type detection
- `test_validation_missing_required_fields` - Required field validation
- `test_validation_invalid_converter_type` - Type validation
- `test_validation_threshold_range` - Threshold bounds
- `test_validation_threshold_order` - Threshold ordering
- `test_validation_file_converter_needs_watch_folder` - Folder requirement
- `test_validation_scheduled_converter_needs_schedule` - Schedule requirement
- `test_to_dict_round_trip` - Serialization
- `test_default_values` - Default initialization
- `test_create_client_config` - Client config creation
- `test_save_and_load_config` - Persistence
- `test_load_or_create_existing` - Load existing
- `test_load_or_create_new` - Create new
- `test_add_converter` - Converter management
- `test_invalid_json_raises_error` - Error handling
- `test_missing_file_raises_error` - File not found
- `test_full_config_workflow` - Integration workflow

### 🔨 Queue Manager (`test_queue.py`)

**Status:** TODO

**Planned Coverage:**
- Queue initialization
- Add/remove operations
- Persistence (save/load)
- Error handling
- Retry logic
- Queue size limits
- Priority handling

### 🔨 Converters (`test_converters.py`)

**Status:** TODO

**Planned Coverage:**
- File validation
- Confidence scoring
- Conversion execution
- Error handling
- Post-processing actions
- Converter registration
- Mock converter implementation

### 🔨 Service Manager (`test_service_manager.py`)

**Status:** TODO

**Planned Coverage:**
- Service lifecycle (start/stop)
- State management
- Graceful shutdown
- Error recovery
- Event bus integration
- Concurrent operations

### 🔨 Integration Tests (`test_integration.py`)

**Status:** TODO

**Planned Coverage:**
- File watching → conversion → upload
- Queue persistence and recovery
- Multi-converter scenarios
- Error scenarios and recovery
- Configuration reloading

## Fixtures

### Test Directories

- `temp_dir` - Temporary directory (auto-cleanup)
- `test_folders` - Standard folder structure (watch, done, error, pending, config, data, logs)

### Sample Data

- `sample_config_dict` - Basic client configuration
- `sample_converter_config` - Converter configuration
- `sample_test_data` - Test report data
- `config_file` - Pre-created config file

### Mocks

- `mock_wats_api` - Mocked pyWATS API client

## Writing New Tests

### Test Naming Convention

- Test files: `test_<module>.py`
- Test classes: `Test<Feature>`
- Test methods: `test_<what_it_tests>`

### Example Test

```python
import pytest
from pywats_client.core.config import ConverterConfig

@pytest.mark.unit
def test_converter_validation(sample_converter_config):
    """Test converter configuration validation"""
    config = ConverterConfig.from_dict(sample_converter_config)
    errors = config.validate()
    
    assert len(errors) == 0, f"Validation failed: {errors}"
```

### Using Fixtures

```python
def test_with_temp_directory(temp_dir, test_folders):
    """Test using temporary directories"""
    watch_dir = test_folders['watch']
    test_file = watch_dir / "test.csv"
    test_file.write_text("data")
    
    assert test_file.exists()
    # temp_dir and all contents auto-deleted after test
```

## Continuous Integration

Tests run automatically on:
- Push to main branch
- Pull requests
- Manual workflow trigger

See `.github/workflows/test.yml` for CI configuration.

## Target Metrics

- **Code Coverage:** 80%+ overall
  - Core modules: 90%+
  - Converters: 75%+
  - GUI: 60%+ (lower due to Qt complexity)

- **Test Count:** 100+ tests
  - Unit: ~70 tests
  - Integration: ~20 tests
  - Functional: ~10 tests

- **Performance:**
  - Unit tests: < 30 seconds total
  - All tests: < 5 minutes total

## Next Steps

1. ✅ Configuration tests (COMPLETE)
2. 🔨 Queue manager tests
3. 🔨 Converter tests
4. 🔨 Service manager tests
5. 🔨 Integration tests
6. 📊 Achieve 80%+ coverage
7. 🔄 Add to CI/CD pipeline

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Python testing best practices](https://docs.python-guide.org/writing/tests/)

---

**Last Updated:** January 23, 2026  
**Version:** 0.1.0b34
