"""
Pytest configuration and fixtures for pyWATS tests
"""
from typing import Generator, Dict
import pytest
from pywats import pyWATS


@pytest.fixture(scope="session")
def wats_config() -> Dict[str, str]:
    """WATS configuration - update these with your test environment"""
    return {
        "base_url": "https://py.wats.com",
        "token": (
            "cHlXQVRTX1Rlc3RUb2tlbjo3NDRRNE9GWERtaGMmSjVWSUFpaTkzMGcwN0JncDU="
        )
    }


@pytest.fixture(scope="session")
def wats_client(wats_config: Dict[str, str]) -> Generator[pyWATS, None, None]:
    """Create a WATS client for the test session"""
    client = pyWATS(
        base_url=wats_config["base_url"],
        token=wats_config["token"]
    )
    yield client
    # Cleanup if needed


@pytest.fixture
def test_serial_number() -> str:
    """Generate a unique test serial number"""
    from datetime import datetime
    return f"TEST-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"


@pytest.fixture
def test_part_number() -> str:
    """Test part number"""
    return "TEST-PN-001"


@pytest.fixture
def test_revision() -> str:
    """Test revision"""
    return "A"
