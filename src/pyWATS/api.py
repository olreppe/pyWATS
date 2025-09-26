"""
pyWATS API - High-level interface for WATS operations

This module provides a simple, configuration-driven interface to pyWATS functionality.
It automatically handles initialization based on configuration settings.
"""

import os
from typing import Optional, Dict, Any, Union
from .config import PyWATSConfig, DEFAULT_CONFIG, ENV_CONFIG
from .tdm_client import TDMClient, APIStatusType, ValidationModeType, TestModeType


class PyWATSAPI:
    """
    High-level pyWATS API interface.
    
    This class provides a simple way to access pyWATS functionality with automatic
    initialization based on configuration. It encapsulates the TDM client setup
    and connection management.
    
    Usage:
        # Use default configuration
        api = PyWATSAPI()
        
        # Use custom configuration
        config = PyWATSConfig()
        config.BASE_URL = "https://my-wats-server.com"
        api = PyWATSAPI(config)
        
        # Use environment-based configuration
        api = PyWATSAPI.from_environment()
    """
    
    def __init__(self, config: Optional[PyWATSConfig] = None):
        """
        Initialize pyWATS API with configuration.
        
        Args:
            config: Configuration object. If None, uses default configuration.
        """
        self.config = config or DEFAULT_CONFIG
        self._tdm_client: Optional[TDMClient] = None
        self._is_initialized = False
        self._connection_status = APIStatusType.Unknown
        
    @classmethod
    def from_environment(cls) -> 'PyWATSAPI':
        """Create pyWATS API using environment-based configuration."""
        return cls(ENV_CONFIG)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'PyWATSAPI':
        """Create pyWATS API from configuration dictionary."""
        config = PyWATSConfig()
        for key, value in config_dict.items():
            if hasattr(config, key.upper()):
                setattr(config, key.upper(), value)
        return cls(config)
    
    def initialize(self, force_reinit: bool = False) -> bool:
        """
        Initialize the pyWATS API connection and client.
        
        Args:
            force_reinit: Force re-initialization even if already initialized
            
        Returns:
            True if initialization successful, False otherwise
        """
        if self._is_initialized and not force_reinit:
            return self._connection_status == APIStatusType.Online
        
        try:
            print(f"[PyWATS] Initializing pyWATS API...")
            print(f"[PyWATS] Server: {self.config.BASE_URL}")
            print(f"[PyWATS] Location: {self.config.LOCATION}")
            
            # Create TDM client
            self._tdm_client = TDMClient()
            
            # Configure API settings (following tdm_example pattern)
            self._tdm_client.setup_api(
                data_dir=self.config.DATA_DIR,
                location=self.config.LOCATION,
                purpose=self.config.PURPOSE,
                persist=self.config.PERSIST_DATA
            )
            
            # Set additional properties
            self._tdm_client.station_name = self.config.STATION_NAME
            
            # Set validation mode
            if self.config.VALIDATION_MODE == "ThrowExceptions":
                self._tdm_client.validation_mode = ValidationModeType.ThrowExceptions
            else:
                self._tdm_client.validation_mode = ValidationModeType.LogErrors
            
            # Set test mode
            if self.config.TEST_MODE == "Import":
                self._tdm_client.test_mode = TestModeType.Import
            else:
                self._tdm_client.test_mode = TestModeType.Active
            
            self._tdm_client.root_step_name = self.config.ROOT_STEP_NAME
            
            print(f"[PyWATS] ✓ TDM client configured")
            
            # Register with server
            print(f"[PyWATS] Registering with WATS server...")
            self._tdm_client.register_client(
                base_url=self.config.BASE_URL, 
                token=self.config.AUTH_TOKEN
            )
            print(f"[PyWATS] ✓ Client registered")
            
            # Initialize API
            print(f"[PyWATS] Initializing API connection...")
            self._tdm_client.initialize_api(
                try_connect_to_server=self.config.TRY_CONNECT_TO_SERVER,
                download_metadata=self.config.DOWNLOAD_METADATA
            )
            
            self._connection_status = self._tdm_client.status
            self._is_initialized = True
            
            print(f"[PyWATS] ✓ API Status: {self._connection_status}")
            print(f"[PyWATS] ✓ Client State: {self._tdm_client.client_state}")
            
            if self._connection_status == APIStatusType.Online:
                print(f"[PyWATS] 🎉 Successfully connected to WATS server!")
                return True
            else:
                print(f"[PyWATS] ⚠️ Connected but status is {self._connection_status}")
                return False
                
        except Exception as e:
            print(f"[PyWATS] ❌ Initialization failed: {e}")
            self._connection_status = APIStatusType.Error
            self._is_initialized = False
            return False
    
    @property
    def tdm_client(self) -> Optional[TDMClient]:
        """Get the underlying TDM client. Initializes if needed."""
        if not self._is_initialized:
            self.initialize()
        return self._tdm_client
    
    @property
    def is_online(self) -> bool:
        """Check if the API is online and ready."""
        return self._connection_status == APIStatusType.Online
    
    @property
    def connection_status(self) -> APIStatusType:
        """Get current connection status."""
        return self._connection_status
    
    def test_connection(self) -> bool:
        """Test the connection to the WATS server."""
        if not self._is_initialized:
            return self.initialize()
        return self.is_online
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about the configured server."""
        return {
            'base_url': self.config.BASE_URL,
            'location': self.config.LOCATION,
            'purpose': self.config.PURPOSE,
            'station_name': self.config.STATION_NAME,
            'is_initialized': self._is_initialized,
            'connection_status': str(self._connection_status),
            'is_online': self.is_online
        }
    
    def __repr__(self) -> str:
        """String representation of the API object."""
        return (f"PyWATSAPI(server='{self.config.BASE_URL}', "
                f"location='{self.config.LOCATION}', "
                f"status='{self._connection_status}')")


# Convenience function to create a ready-to-use API instance
def create_api(config: Optional[Union[PyWATSConfig, Dict[str, Any]]] = None, 
               auto_init: bool = True) -> PyWATSAPI:
    """
    Create and optionally initialize a pyWATS API instance.
    
    Args:
        config: Configuration object or dictionary. If None, uses default config.
        auto_init: Automatically initialize the API on creation.
        
    Returns:
        PyWATSAPI instance
    """
    if isinstance(config, dict):
        api = PyWATSAPI.from_dict(config)
    else:
        api = PyWATSAPI(config)
    
    if auto_init:
        api.initialize()
    
    return api