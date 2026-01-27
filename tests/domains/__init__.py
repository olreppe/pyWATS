"""
Domain Test Suite

This package contains tests for the pyWATS API domain modules.

Test Organization:
- analytics/: Analytics API tests
- asset/: Asset management tests
- process/: Process management tests
- product/: Product management tests
- production/: Production tracking tests
- report/: Report submission and retrieval tests
- rootcause/: Root cause analysis tests
- software/: Software management tests

Run all domain tests:
    pytest tests/domains/

Run specific domain:
    pytest tests/domains/report/

Run with coverage:
    pytest tests/domains/ --cov=pywats --cov-report=html
"""
