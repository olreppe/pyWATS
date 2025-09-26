# Test Organization

This document describes the reorganized test structure for pyWATS.

## Directory Structure

```
tests/
├── __init__.py                 # Test suite documentation
├── tdm/                        # Test Data Management (TDM) tests
│   ├── __init__.py            # TDM test documentation
│   ├── run_uut_tests.py       # Main TDM test runner
│   ├── test_uut_reports.py    # Alternative UUT test structure
│   ├── test_config.py         # TDM test configuration
│   ├── test_utils.py          # TDM test utilities
│   └── test_data/             # Test data files
│       └── processes_cache.json
└── mes/                        # Manufacturing Execution System (MES) tests
    ├── __init__.py            # MES test documentation
    ├── asset/                 # Asset management tests
    │   └── __init__.py
    ├── base/                  # Base MES functionality tests
    │   └── __init__.py
    ├── configuration/         # Configuration and setup tests
    │   └── __init__.py
    ├── product/               # Product-related tests
    │   └── __init__.py
    ├── production/            # Production workflow tests
    │   └── __init__.py
    ├── software/              # Software component tests
    │   └── __init__.py
    └── workflow/              # Workflow management tests
        └── __init__.py
```

## Running Tests

### TDM Tests
```bash
# From project root
cd tests/tdm
python run_uut_tests.py

# Alternative test runner
python test_uut_reports.py
```

### MES Tests
```bash
# Future MES test files will be organized by module
cd tests/mes/[module]
python [test_file].py
```

## Test Organization Principles

1. **Module Separation**: TDM and MES tests are clearly separated
2. **Logical Grouping**: MES tests are organized by functional modules matching the C# project structure
3. **Package Structure**: All directories have `__init__.py` files for proper Python package imports
4. **Path Independence**: Test files use relative imports that work from any directory level

## Migration Notes

- All import paths have been updated to account for the new directory structure
- Tests maintain the same functionality and 100% success rate
- The test runner commands remain simple and intuitive
- Future test development follows the established module organization