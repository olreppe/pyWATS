"""
Client Test Suite

This package contains comprehensive tests for the pyWATS Client application.

Test Organization:
- test_config.py: Configuration management tests
- test_queue.py: Queue manager tests
- test_converters.py: Converter functionality tests
- test_integration.py: End-to-end integration tests

Run all client tests:
    pytest tests/client/

Run specific test file:
    pytest tests/client/test_config.py

Run with coverage:
    pytest tests/client/ --cov=pywats_client --cov-report=html

Run only unit tests:
    pytest tests/client/ -m unit

Run only integration tests:
    pytest tests/client/ -m integration
"""

__version__ = "0.1.0b34"
