"""
Pytest configuration and providers for PyWATS tests

This module provides pytest providers for testing the PyWATS library and client.

Test Instance Architecture:
--------------------------
Two persistent test instances are available (ClientA and ClientB) that:
- Store configs in tests/instances/ (version controlled)
- Store data in tests/instances/data/ (gitignored)
- Can be customized independently for different test scenarios

Provider Usage:
--------------
API-level testing (PyWATS client only):
    def test_api_call(wats_client):
        # Uses the default wats_client provider (Client A)
        products = wats_client.product.get_products()
    
    def test_with_client_b(wats_client_b):
        # Explicitly use Client B
        products = wats_client_b.product.get_products()

Client application testing (full pyWATSApplication):
    def test_client_app(client_app_a):
        # Full application with services
        await client_app_a.start()
        
    def test_client_config(client_config_a):
        # Just the ClientConfig for unit tests
        assert client_config_a.instance_name == "Test Client A"

Running GUI with test instances:
    python -m tests.test_instances --client A --gui
    python -m tests.test_instances --client B --gui
"""
from typing import Generator, Dict, TYPE_CHECKING
import pytest

from pywats import pyWATS

if TYPE_CHECKING:
    from pywats_client.core.config import ClientConfig
    from pywats_client.app import pyWATSApplication


# =============================================================================
# Test Instance Providers
# =============================================================================

@pytest.fixture(scope="session")
def test_instance_manager():
    """Get the test instance manager for managing test configurations."""
    from tests.test_instances import get_test_instance_manager
    return get_test_instance_manager()


# =============================================================================
# Client A Providers
# =============================================================================

@pytest.fixture(scope="session")
def wats_config() -> Dict[str, str]:
    """
    WATS configuration for Client A.
    
    This is the primary test configuration used by most tests.
    Configuration is stored in tests/instances/client_a_config.json
    """
    from tests.test_instances import get_test_instance_manager
    manager = get_test_instance_manager()
    config = manager.get_test_instance_config("A")
    return {
        "base_url": config.base_url,
        "token": config.token
    }


@pytest.fixture(scope="session")
def wats_client(wats_config: Dict[str, str]) -> Generator[pyWATS, None, None]:
    """
    Create a WATS API client for the test session (Client A).
    
    This is the primary API client fixture used by most tests.
    For client application tests, use client_app_a instead.
    """
    client = pyWATS(
        base_url=wats_config["base_url"],
        token=wats_config["token"]
    )
    yield client
    # Cleanup if needed


@pytest.fixture(scope="session")
def wats_client_a(wats_client: pyWATS) -> pyWATS:
    """Alias for wats_client - explicitly named for Client A."""
    return wats_client


@pytest.fixture(scope="session")
def client_config_a(test_instance_manager) -> "ClientConfig":
    """
    Get ClientConfig for Test Instance A.
    
    Use this for unit testing client configuration or 
    when you need the config without starting the application.
    """
    return test_instance_manager.get_client_config("A")


@pytest.fixture(scope="function")
def client_app_a(test_instance_manager) -> Generator["pyWATSApplication", None, None]:
    """
    Get full pyWATSApplication for Test Instance A.
    
    Use this for integration tests that need the full client
    application with all services (connection, sync, converters).
    
    Note: This is function-scoped to ensure clean state between tests.
    """
    app = test_instance_manager.get_application("A")
    yield app
    # Cleanup: stop services if running
    if hasattr(app, '_running') and app._running:
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(app.stop())
            else:
                loop.run_until_complete(app.stop())
        except Exception:
            pass


# =============================================================================
# Client B Providers
# =============================================================================

@pytest.fixture(scope="session")
def wats_config_b() -> Dict[str, str]:
    """
    WATS configuration for Client B.
    
    This is the secondary test configuration for comparison testing.
    Configuration is stored in tests/instances/client_b_config.json
    """
    from tests.test_instances import get_test_instance_manager
    manager = get_test_instance_manager()
    config = manager.get_test_instance_config("B")
    return {
        "base_url": config.base_url,
        "token": config.token
    }


@pytest.fixture(scope="session")
def wats_client_b(wats_config_b: Dict[str, str]) -> Generator[pyWATS, None, None]:
    """
    Create a WATS API client for Test Instance B.
    
    Use this when you need a second client for comparison testing
    or to test different configurations.
    """
    client = pyWATS(
        base_url=wats_config_b["base_url"],
        token=wats_config_b["token"]
    )
    yield client


@pytest.fixture(scope="session")
def client_config_b(test_instance_manager) -> "ClientConfig":
    """
    Get ClientConfig for Test Instance B.
    
    Use this for unit testing client configuration with
    alternative settings.
    """
    return test_instance_manager.get_client_config("B")


@pytest.fixture(scope="function")
def client_app_b(test_instance_manager) -> Generator["pyWATSApplication", None, None]:
    """
    Get full pyWATSApplication for Test Instance B.
    
    Use this for integration tests that need a second client
    with different configuration.
    """
    app = test_instance_manager.get_application("B")
    yield app
    # Cleanup
    if hasattr(app, '_running') and app._running:
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(app.stop())
            else:
                loop.run_until_complete(app.stop())
        except Exception:
            pass


# =============================================================================
# Utility Providers
# =============================================================================

@pytest.fixture
def test_serial_number() -> str:
    """Generate a unique test serial number."""
    from datetime import datetime
    return f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"


@pytest.fixture
def test_part_number() -> str:
    """Test part number for use in tests."""
    return "TEST-PN-001"


@pytest.fixture
def test_revision() -> str:
    """Test revision for use in tests."""
    return "A"


@pytest.fixture
def unique_test_id() -> str:
    """Generate a unique ID for test isolation."""
    import uuid
    return str(uuid.uuid4())[:8]


# =============================================================================
# Async Providers
# =============================================================================

@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# =============================================================================
# Markers
# =============================================================================

def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "client_a: mark test as using Client A instance"
    )
    config.addinivalue_line(
        "markers", "client_b: mark test as using Client B instance"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
