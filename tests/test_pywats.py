"""
Top-level tests for pyWATS API.
"""
import pytest
from pyWATS import WATSApi
from pyWATS.config import PyWATSConfig


class TestConnection:
    """Test pyWATS API connection and initialization."""
    
    def test_api_initialization(self):
        """Test that the API can be initialized."""
        config = PyWATSConfig()
        api = WATSApi(config)
        assert api is not None
        assert api.config is not None
        assert api.http_client is not None