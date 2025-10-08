"""
Top-level tests for pyWATS API.
"""

import pytest
from pyWATS import WATSApi
from pyWATS.config import PyWATSConfig


class TestConnection:
    """Test connection and API initialization."""
    
    def test_api_initialization(self):
        """Test that the API can be initialized."""
        config = PyWATSConfig()
        api = WATSApi(config)
        
        assert api is not None
        assert api.config is not None
        assert hasattr(api, 'app')
        assert hasattr(api, 'report')
        assert hasattr(api, 'product')
        assert hasattr(api, 'production')
        assert hasattr(api, 'asset')
        assert hasattr(api, 'workflow')
        assert hasattr(api, 'software')