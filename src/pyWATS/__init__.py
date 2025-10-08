"""
pyWATS - Python SDK for WATS (Virinco Test Data Management System)

This package provides comprehensive access to WATS functionality through a modern
object-oriented API design:

- WATSApi: Main API class with module properties for organized access
- TDM: Test Data Management for creating and managing test reports
- Product: Product management and configuration
- Report: Analytics and reporting functionality  
- Unit: Unit/device management
- Workflow: Workflow and step management
- Production: Production tracking and control
- Asset: Asset management
- App: Application and system management

Report Models:
- UUTReport: Unit Under Test reports
- UURReport: Unit Under Repair reports  
- Report: Base report class

Example usage:
    from pyWATS import WATSApi, PyWATSConfig, TDM
    
    # Initialize with configuration
    config = PyWATSConfig()
    api = WATSApi(config=config)
    
    # Use TDM for test data management
    tdm = TDM(api.client)
    tdm.setup_api("./data", "Station1", "Development")
    
    # Create a UUT report
    report = tdm.create_uut_report(
        operator="John Doe",
        part_number="PCB-123",
        revision="A",
        serial_number="SN12345", 
        operation_type="Final Test",
        sequence_file="test.seq",
        version="1.0"
    )
    
    # Submit the report
    report_id = tdm.submit(report)
    
    # Access modules through properties
    products = api.product.get_all()
    report_stats = api.report.get_production_statistics()
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

# Import report models for direct access
from .models.report import UUTReport, UURReport, Report
from . import report_utils

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
    
    # Report Models
    "UUTReport",
    "UURReport", 
    "Report",
    "report_utils",
    
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