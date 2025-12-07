"""
REST API Module

This module provides a clean interface to all WATS API endpoints,
organized by category (report, product, asset, production, software, app).
"""

from .endpoints import WATSEndpoints
from .product_api import ProductApi
from .report_api import ReportApi
from .asset_api import AssetApi
from .production_api import ProductionApi
from .software_api import SoftwareApi
from .app_api import AppApi

# Aliases for backward compatibility
ProductAPI = ProductApi
ReportAPI = ReportApi
AssetAPI = AssetApi
ProductionAPI = ProductionApi
SoftwareDistributionAPI = SoftwareApi
AppAPI = AppApi

__all__ = [
    "WATSEndpoints",
    "ProductApi",
    "ReportApi",
    "AssetApi",
    "ProductionApi",
    "SoftwareApi",
    "AppApi",
    # Aliases
    "ProductAPI",
    "ReportAPI",
    "AssetAPI",
    "ProductionAPI",
    "SoftwareDistributionAPI",
    "AppAPI",
]
