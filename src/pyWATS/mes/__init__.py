"""
pyWATS MES (Manufacturing Execution System) Module

This module provides comprehensive MES functionality for WATS including:
- Production management
- Product management  
- Asset management
- Software package management
- Workflow orchestration

The MES module is designed to mirror the Interface.MES C# API while leveraging
Python conventions and the pyWATS REST API infrastructure.

Example usage:
    from pyWATS.mes import Production, Product, AssetHandler, Software, Workflow
    from pyWATS.connection import create_connection
    
    # Create connection
    connection = create_connection(
        base_url="https://your-wats-server.com",
        token="your_token"
    )
    
    # Initialize MES modules
    production = Production(connection)
    product = Product(connection)
    asset_handler = AssetHandler(connection)
    
    # Use the modules
    unit_info = production.get_unit_info("12345", "PART001")
    product_info = product.get_product_info("PART001")
    asset_info = asset_handler.get_asset("FIXTURE001")
"""

from .production import Production
from .product import Product
from .asset import AssetHandler
from .software import Software
from .workflow import Workflow

__all__ = [
    "Production",
    "Product", 
    "AssetHandler",
    "Software",
    "Workflow"
]