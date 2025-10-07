"""
pyWATS - Python SDK for WATS (Virinco Test Data Management System)

This package provides comprehensive access to WATS functionality through a modern
object-oriented API design:

- WATSApi: Main API class with module properties for organized access
- Product: Product management and configuration
- Report: Analytics and reporting functionality  
- Unit: Unit/device management
- Workflow: Workflow and step management
- Production: Production tracking and control
- Asset: Asset management
- App: Application and system management

Example usage:
    from pyWATS import WATSApi, PyWATSConfig
    
    # Initialize with configuration
    config = PyWATSConfig()
    api = WATSApi(config=config)
    
    # Or initialize directly
    api = WATSApi(base_url="https://your-wats-server.com", token="your_token")
    
    # Access modules through properties
    products = api.product.get_all()
    report = api.report.get_production_statistics()
    units = api.unit.get_all()
"""

# Import the main API class and configuration
from .api import WATSApi
from .config import PyWATSConfig
from .exceptions import (
    WATSException, 
    WATSAPIError, 
    WATSConnectionError, 
    WATSAuthenticationError,
    WATSValidationError,
    WATSNotFoundError,
    WATSConfigurationError,
    WATSTimeoutError
)

# Import REST API components for direct access if needed
from . import rest_api

# Import legacy components if available
try:
    from . import wats_client
except ImportError:
    wats_client = None

__version__ = "2.0.0"

__all__ = [
    # Main API
    "WATSApi",
    "PyWATSConfig",
    
    # Exceptions
    "WATSException",
    "WATSAPIError", 
    "WATSConnectionError",
    "WATSAuthenticationError",
    "WATSValidationError",
    "WATSNotFoundError", 
    "WATSConfigurationError",
    "WATSTimeoutError",
    
    # REST API components for advanced usage
    "rest_api",
    
    # Legacy components (may be None)
    "wats_client",
]