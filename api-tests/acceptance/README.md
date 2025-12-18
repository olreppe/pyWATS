# Release Acceptance Testing

This directory contains scenario-based acceptance tests for release validation.

## Purpose

These tests are designed to:
- Validate complete workflows from start to finish
- Test real-world usage scenarios
- Automatically verify results after each operation
- Ensure API functionality works end-to-end
- Serve as release gate criteria

## Structure

- **conftest.py** - Shared fixtures and utilities for acceptance tests
- **test_scenario_*.py** - Individual scenario test files
- **scenarios/** - Reusable scenario definitions and data

## Test Scenarios

Each test scenario typically includes:
1. Setup phase (create required data)
2. Execution phase (perform operations)
3. Verification phase (load and validate results)
4. Cleanup phase (optional, based on test requirements)

## Running Tests

Run all acceptance tests:
```bash
pytest tests/acceptance/ -v
```

Run specific scenario:
```bash
pytest tests/acceptance/test_scenario_production_workflow.py -v
```

Run with detailed output:
```bash
pytest tests/acceptance/ -v -s
```

## Guidelines

- Each scenario should be independent and self-contained
- Use descriptive test names that explain the scenario
- Include comprehensive assertions to validate all aspects
- Load and verify data after each significant operation
- Use fixtures for common setup/teardown
- Document complex scenarios with docstrings
