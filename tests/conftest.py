"""
Pytest configuration and fixtures for pyWATS tests
"""
import pytest
from pywats.client import WATSClient


@pytest.fixture(scope="session")
def wats_config():
    """WATS configuration - update these with your test environment"""
    return {
        "base_url": "http://localhost:8080",  # Update with your WATS server
        "username": "test_user",  # Update with test credentials
        "password": "test_password",
        "client_id": "pyWATS_tests"
    }


@pytest.fixture(scope="session")
def wats_client(wats_config):
    """Create a WATS client for the test session"""
    client = WATSClient(
        base_url=wats_config["base_url"],
        username=wats_config["username"],
        password=wats_config["password"],
        client_id=wats_config["client_id"]
    )
    yield client
    # Cleanup if needed


@pytest.fixture
def test_serial_number():
    """Generate a unique test serial number"""
    from datetime import datetime
    return f"TEST-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"


@pytest.fixture
def test_part_number():
    """Test part number"""
    return "TEST-PN-001"


@pytest.fixture
def test_revision():
    """Test revision"""
    return "A"
