"""
pyWATS Configuration

Centralized configuration for pyWATS API initialization.
This file contains all the settings needed to automatically initialize
the pyWATS client with proper connection and authentication.
"""

import os
from typing import Optional


class PyWATSConfig:
    """Configuration class for pyWATS API initialization"""
    
    # Server Configuration - Updated for debugging
    BASE_URL: str = "https://py.wats.com"
    AUTH_TOKEN: str = "cHlXQVRTX1Rlc3RpbmdfT2xhOmdHMVZMM0xvc3preDlOUTB3cDk0RjhHOFE5IWI0Vg=="
    
    # TDM Client Configuration
    DATA_DIR: str = "./wats_data"
    LOCATION: str = "Test Lab"
    PURPOSE: str = "Development Testing"
    STATION_NAME: str = "Python_Test_Station"
    PERSIST_DATA: bool = False
    
    # Connection Settings
    TRY_CONNECT_TO_SERVER: bool = True
    DOWNLOAD_METADATA: bool = True
    CONNECTION_TIMEOUT: float = 30.0
    
    # Test Configuration
    TEST_MODE: str = "Active"  # Active, Inactive, Simulation
    VALIDATION_MODE: str = "ThrowExceptions"  # ThrowExceptions, LogWarnings, Silent
    ROOT_STEP_NAME: str = "Main Sequence"
    
    # Optional Override from Environment Variables
    @classmethod
    def from_environment(cls) -> 'PyWATSConfig':
        """Create configuration from environment variables if available"""
        config = cls()
        
        # Override with environment variables if they exist
        config.BASE_URL = os.getenv("PYWATS_BASE_URL", cls.BASE_URL)
        config.AUTH_TOKEN = os.getenv("PYWATS_AUTH_TOKEN", cls.AUTH_TOKEN)
        config.DATA_DIR = os.getenv("PYWATS_DATA_DIR", cls.DATA_DIR)
        config.LOCATION = os.getenv("PYWATS_LOCATION", cls.LOCATION)
        config.PURPOSE = os.getenv("PYWATS_PURPOSE", cls.PURPOSE)
        config.STATION_NAME = os.getenv("PYWATS_STATION_NAME", cls.STATION_NAME)
        
        return config
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            'base_url': self.BASE_URL,
            'auth_token': self.AUTH_TOKEN,
            'data_dir': self.DATA_DIR,
            'location': self.LOCATION,
            'purpose': self.PURPOSE,
            'station_name': self.STATION_NAME,
            'persist_data': self.PERSIST_DATA,
            'try_connect_to_server': self.TRY_CONNECT_TO_SERVER,
            'download_metadata': self.DOWNLOAD_METADATA,
            'connection_timeout': self.CONNECTION_TIMEOUT,
            'test_mode': self.TEST_MODE,
            'validation_mode': self.VALIDATION_MODE,
            'root_step_name': self.ROOT_STEP_NAME
        }


# Default configuration instance
DEFAULT_CONFIG = PyWATSConfig()

# Environment-based configuration instance  
ENV_CONFIG = PyWATSConfig.from_environment()