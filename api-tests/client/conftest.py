"""
Test Configuration for Client Tests

This module contains pytest fixtures and configuration for testing the pyWATS Client.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any
import json


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def test_folders(temp_dir):
    """Create standard test folder structure"""
    folders = {
        'watch': temp_dir / 'watch',
        'done': temp_dir / 'done',
        'error': temp_dir / 'error',
        'pending': temp_dir / 'pending',
        'config': temp_dir / 'config',
        'data': temp_dir / 'data',
        'logs': temp_dir / 'logs',
    }
    
    for folder in folders.values():
        folder.mkdir(parents=True, exist_ok=True)
    
    return folders


@pytest.fixture
def sample_config_dict() -> Dict[str, Any]:
    """Sample configuration dictionary"""
    return {
        "instance_id": "test-instance-001",
        "instance_name": "Test Client",
        "station_name": "Test Station",
        "service_address": "https://wats.test.com",
        "api_token": "dGVzdDp0ZXN0",  # Base64 "test:test"
        "converters": [],
        "sync_interval_seconds": 60,
        "offline_queue_enabled": True,
    }


@pytest.fixture
def sample_converter_config() -> Dict[str, Any]:
    """Sample converter configuration"""
    return {
        "name": "Test CSV Converter",
        "module_path": "converters.csv_converter.CSVConverter",
        "watch_folder": "/test/watch",
        "done_folder": "/test/done",
        "error_folder": "/test/error",
        "pending_folder": "/test/pending",
        "converter_type": "file",
        "enabled": True,
        "file_patterns": ["*.csv"],
        "alarm_threshold": 0.5,
        "reject_threshold": 0.2,
        "max_retries": 3,
        "retry_delay_seconds": 60,
    }


@pytest.fixture
def config_file(temp_dir, sample_config_dict):
    """Create a configuration file"""
    config_path = temp_dir / 'config.json'
    with open(config_path, 'w') as f:
        json.dump(sample_config_dict, f, indent=2)
    return config_path


@pytest.fixture
def mock_wats_api():
    """Mock pyWATS API client"""
    from unittest.mock import MagicMock
    
    api = MagicMock()
    api.test_connection.return_value = True
    api.product.get_products.return_value = []
    api.report.submit_report.return_value = {"success": True}
    
    return api


@pytest.fixture
def sample_test_data():
    """Sample test data for reports"""
    return {
        "serial_number": "TEST-001",
        "part_number": "WIDGET-100",
        "status": "PASS",
        "start_time": "2024-01-01T10:00:00Z",
        "end_time": "2024-01-01T10:05:00Z",
        "measurements": [
            {"name": "Voltage", "value": 3.3, "unit": "V"},
            {"name": "Current", "value": 0.5, "unit": "A"},
        ]
    }


@pytest.fixture
def sample_report():
    """Sample report dictionary for queue testing"""
    return {
        "serial_number": "SN-12345",
        "part_number": "PN-WIDGET-100",
        "part_revision": "A",
        "status": "Passed",
        "start_time": "2024-01-15T10:00:00Z",
        "end_time": "2024-01-15T10:05:00Z",
        "station_name": "Test Station 1",
        "operator": "TestOperator",
        "measurements": [
            {"step_name": "Voltage Test", "measurement_name": "VCC", "value": 3.3, "unit": "V", "status": "Passed"},
            {"step_name": "Current Test", "measurement_name": "ICC", "value": 0.5, "unit": "A", "status": "Passed"},
        ]
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests that don't require external dependencies"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that may require services"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take a long time to run"
    )
