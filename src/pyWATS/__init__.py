"""
pyWATS - Python SDK for WATS (Virinco Test Data Management System)

This package provides comprehensive access to WATS functionality including:
- REST API client for HTTP-based operations
- Connection management with authentication
- MES (Manufacturing Execution System) modules
- TDM (Test Data Management) modules
- WATS client library for direct database access (legacy)
- Data models and utilities

For most use cases, start with the REST API:
    from pyWATS.connection import create_connection
    from pyWATS.rest_api import endpoints, models

For MES operations:
    from pyWATS.mes import Production, Product, Asset, Software, Workflow

For TDM operations:
    from pyWATS.tdm import Statistics, Analytics, Reports

Example usage:
    # Create connection
    connection = create_connection(
        base_url="https://your-wats-server.com",
        token="your_base64_token"
    )
    
    # Use REST API endpoints
    from pyWATS.rest_api.endpoints.asset import get_assets
    assets = get_assets(odata_top=10)
    
    # Use MES modules
    from pyWATS.mes import Production
    production = Production(connection)
    unit_info = production.get_unit_info("12345", "PART001")
    
    # Use TDM modules
    from pyWATS.tdm import Statistics
    statistics = Statistics(connection)
    trend_data = statistics.get_trend("PART001", "OP001")
"""

# Import connection management for easy access
from .connection import create_connection, create_connection_from_env, WATSConnection

# Import REST API components for easy access
from . import rest_api

# Import MES modules
from . import mes

# Import TDM modules
from . import tdm
from .tdm_client import TDMClient

# Import legacy WATS client if available
try:
    from . import wats_client
except ImportError:
    wats_client = None

__version__ = "1.0.0"

__all__ = [
    "create_connection",
    "create_connection_from_env", 
    "WATSConnection",
    "rest_api",
    "mes",
    "tdm",
    "TDMClient",
    "wats_client",  # May be None if not available
]