"""Pytest configuration and fixtures for PyWATS tests

This module provides pytest fixtures for testing the PyWATS library and client.

Test Instance Architecture:
--------------------------
Two persistent test instances are available (ClientA and ClientB) that:
- Store configs in tests/fixtures/instances/ (version controlled)
- Store data in tests/fixtures/instances/data/ (gitignored)
- Can be customized independently for different test scenarios
- Have separate API tokens for load distribution (reduces rate limiting)

Fixture Usage:
--------------
API-level testing (PyWATS client only):
    def test_api_call(wats_client):
        # Uses the default wats_client fixture (Client A)
        products = wats_client.product.get_products()

    def test_with_client_b(wats_client_b):
        # Explicitly use Client B
        products = wats_client_b.product.get_products()

    def test_with_load_balance(wats_client_balanced):
        # Automatically alternates between Client A and B tokens
        # Reduces rate limiting during large test runs
        products = wats_client_balanced.product.get_products()

Client configuration testing:
    def test_client_config(client_config_a):
        # Just the ClientConfig for unit tests
        assert client_config_a.instance_name == "Test Client A"

Running GUI with test instances:
    python -m tests.cross_cutting.test_instances --client A --gui
    python -m tests.cross_cutting.test_instances --client B --gui
"""
from typing import Generator, Dict, TYPE_CHECKING
from pathlib import Path
import sys
import pytest

# Add tests directory to path for imports
_tests_dir = Path(__file__).parent
if str(_tests_dir) not in sys.path:
    sys.path.insert(0, str(_tests_dir))

from pywats import pyWATS

if TYPE_CHECKING:
    from pywats_client.core.config import ClientConfig


# =============================================================================
# Test Instance Providers
# =============================================================================

@pytest.fixture(scope="session")
def test_instance_manager():
    """Get the test instance manager for managing test configurations."""
    from cross_cutting.test_instances import get_test_instance_manager
    return get_test_instance_manager()


# =============================================================================
# Client A Providers
# =============================================================================

@pytest.fixture(scope="session")
def wats_config() -> Dict[str, str]:
    """
    WATS configuration for Client A.
    
    This is the primary test configuration used by most tests.
    Configuration is stored in tests/fixtures/instances/client_a_config.json
    """
    from cross_cutting.test_instances import get_test_instance_manager
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


# =============================================================================
# Client B Providers
# =============================================================================

@pytest.fixture(scope="session")
def wats_config_b() -> Dict[str, str]:
    """
    WATS configuration for Client B.
    
    This is the secondary test configuration for comparison testing.
    Configuration is stored in tests/fixtures/instances/client_b_config.json
    """
    from cross_cutting.test_instances import get_test_instance_manager
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
        "markers", "integration: mark test as integration test (require external services)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "stress: mark test as stress test (high load, long duration)"
    )
    config.addinivalue_line(
        "markers", "benchmark: mark test as performance benchmark"
    )


# =============================================================================
# Load-Balanced Client (Reduces Rate Limiting)
# =============================================================================

class LoadBalancedClientPool:
    """
    A pool that alternates between Client A and B tokens to distribute API load.
    
    This helps avoid rate limiting (HTTP 429) during large test runs by spreading
    requests across two separate API tokens with independent rate limit counters.
    """
    
    def __init__(self, client_a: pyWATS, client_b: pyWATS):
        self._clients = [client_a, client_b]
        self._index = 0
    
    def get_client(self) -> pyWATS:
        """Get the next client in round-robin fashion."""
        client = self._clients[self._index]
        self._index = (self._index + 1) % len(self._clients)
        return client
    
    @property
    def current(self) -> pyWATS:
        """Get current client without advancing."""
        return self._clients[self._index]
    
    @property
    def client_a(self) -> pyWATS:
        """Direct access to Client A."""
        return self._clients[0]
    
    @property
    def client_b(self) -> pyWATS:
        """Direct access to Client B."""
        return self._clients[1]


@pytest.fixture(scope="session")
def wats_client_pool(wats_client: pyWATS, wats_client_b: pyWATS) -> LoadBalancedClientPool:
    """
    Get a load-balanced pool of WATS clients.
    
    The pool alternates between Client A and B tokens to distribute
    API requests and reduce rate limiting during large test runs.
    
    Usage:
        def test_something(wats_client_pool):
            client = wats_client_pool.get_client()  # Alternates A/B
            result = client.product.get_products()
    """
    return LoadBalancedClientPool(wats_client, wats_client_b)


@pytest.fixture
def wats_client_balanced(wats_client_pool: LoadBalancedClientPool) -> pyWATS:
    """
    Get a WATS client from the load-balanced pool.
    
    Each test that uses this fixture gets a client from the pool,
    automatically alternating between Client A and B tokens.
    This distributes API calls across tokens, reducing rate limiting.
    
    Usage:
        def test_something(wats_client_balanced):
            # Automatically uses alternating tokens
            result = wats_client_balanced.product.get_products()
    """
    return wats_client_pool.get_client()


# =============================================================================
# Converter Test File Generators
# =============================================================================

# Import test file generator utilities
from tests.fixtures.test_file_generators import TestFileGenerator


@pytest.fixture
def temp_dir(tmp_path):
    """
    Temporary directory for test files.
    
    This is a wrapper around pytest's tmp_path that provides a consistent name.
    """
    return tmp_path


@pytest.fixture
def watch_dir(tmp_path):
    """Temporary watch folder for converter tests."""
    watch = tmp_path / "watch"
    watch.mkdir()
    return watch


@pytest.fixture
def done_dir(tmp_path):
    """Temporary Done folder for post-processing tests."""
    done = tmp_path / "Done"
    done.mkdir()
    return done


@pytest.fixture
def error_dir(tmp_path):
    """Temporary Error folder for failure tests."""
    error = tmp_path / "Error"
    error.mkdir()
    return error


@pytest.fixture
def pending_dir(tmp_path):
    """Temporary Pending folder for retry tests."""
    pending = tmp_path / "Pending"
    pending.mkdir()
    return pending


@pytest.fixture
def test_csv_file(temp_dir):
    """Generate single CSV test file."""
    return TestFileGenerator.generate_csv_file(
        temp_dir / "test.csv",
        rows=50
    )


@pytest.fixture
def test_csv_files(temp_dir):
    """Generate 10 CSV test files."""
    return TestFileGenerator.generate_batch(
        temp_dir,
        'csv',
        count=10,
        rows=50
    )


@pytest.fixture
def test_xml_file(temp_dir):
    """Generate single XML test file."""
    return TestFileGenerator.generate_xml_file(
        temp_dir / "test.xml",
        test_steps=10
    )


@pytest.fixture
def test_xml_files(temp_dir):
    """Generate 10 XML test files."""
    return TestFileGenerator.generate_batch(
        temp_dir,
        'xml',
        count=10,
        test_steps=10
    )


@pytest.fixture
def corrupted_csv_file(temp_dir):
    """Generate single corrupted CSV file."""
    return TestFileGenerator.generate_csv_file(
        temp_dir / "corrupt.csv",
        rows=100,
        corrupt=True
    )


@pytest.fixture
def malformed_xml_file(temp_dir):
    """Generate malformed XML file."""
    return TestFileGenerator.generate_xml_file(
        temp_dir / "malformed.xml",
        test_steps=5,
        malformed=True
    )


@pytest.fixture
def large_csv_file(temp_dir):
    """Generate large CSV file (10,000 rows)."""
    return TestFileGenerator.generate_csv_file(
        temp_dir / "large.csv",
        rows=10000
    )


@pytest.fixture
def large_file_set(temp_dir):
    """Generate large mixed file set for stress testing."""
    return TestFileGenerator.generate_mixed_batch(
        temp_dir,
        {'csv': 100, 'xml': 100, 'txt': 50}
    )


@pytest.fixture
def stress_file_set(temp_dir):
    """Generate 1000 files for stress testing."""
    return TestFileGenerator.generate_batch(
        temp_dir,
        'csv',
        count=1000,
        rows=10  # Small files for speed
    )

