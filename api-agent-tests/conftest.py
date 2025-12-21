"""
Pytest configuration for agent tests.

Imports fixtures from api-tests for real API integration tests.
"""
import sys
from pathlib import Path
from typing import Generator, Dict
import pytest

# Add api-tests directory to path
_api_tests_dir = Path(__file__).parent.parent / "api-tests"
if str(_api_tests_dir) not in sys.path:
    sys.path.insert(0, str(_api_tests_dir))

# Import the required modules
from pywats import pyWATS


@pytest.fixture(scope="session")
def wats_config() -> Dict[str, str]:
    """
    WATS configuration for testing.
    
    Loads configuration from api-tests test instance manager.
    """
    from test_instances import get_test_instance_manager
    manager = get_test_instance_manager()
    config = manager.get_test_instance_config("A")
    return {
        "base_url": config.base_url,
        "token": config.token
    }


@pytest.fixture(scope="session")
def wats_client(wats_config: Dict[str, str]) -> Generator[pyWATS, None, None]:
    """
    Create a WATS API client for agent integration tests.
    
    Uses the same test instance configuration as api-tests.
    """
    client = pyWATS(
        base_url=wats_config["base_url"],
        token=wats_config["token"]
    )
    yield client

