"""
Common test fixtures for pyWATS modules.
"""

import pytest
from pyWATS.rest_api._http_client import WatsHttpClient
from pyWATS.config import PyWATSConfig


@pytest.fixture
def http_client():
    """Create HTTP client for testing."""
    config = PyWATSConfig()
    return WatsHttpClient(
        base_url=config.BASE_URL,
        base64_token=config.AUTH_TOKEN
    )


@pytest.fixture
def config():
    """Create config for testing."""
    return PyWATSConfig()