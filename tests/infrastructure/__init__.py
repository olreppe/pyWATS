"""
Infrastructure Test Suite

This package contains tests for pyWATS infrastructure components.

Test Organization:
- test_pywats_cfx.py: CFX (Connected Factory Exchange) message tests
- test_pywats_events.py: Event system and dead letter queue tests

Run all infrastructure tests:
    pytest tests/infrastructure/

Run with coverage:
    pytest tests/infrastructure/ --cov=pywats_cfx --cov=pywats_events --cov-report=html
"""
