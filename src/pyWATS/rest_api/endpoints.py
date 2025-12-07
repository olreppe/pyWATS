"""REST API Endpoints

This module provides organized access to all WATS API endpoints.
Each endpoint category is a property that returns an endpoint handler class.
"""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..http_client import HttpClient
    from .report_api import ReportApi
    from .product_api import ProductApi
    from .asset_api import AssetApi
    from .production_api import ProductionApi
    from .software_api import SoftwareApi
    from .app_api import AppApi
    from .rootcause_api import RootCauseApi


class WATSEndpoints:
    """
    Container for all REST API endpoints.
    
    Organizes API calls by category, making it easy to find and use
    the appropriate endpoint for any operation.
    
    Usage:
        endpoints = WATSEndpoints(http_client)
        product = endpoints.product.get_product("ABC123")
        endpoints.report.post_report_wsjf(report_data)
    """
    
    def __init__(self, http_client: 'HttpClient'):
        """
        Initialize the REST API with an HTTP client.
        
        Args:
            http_client: The HTTP client for making requests
        """
        self._http = http_client
        
        # Lazy-loaded API handlers
        self._report: Optional['ReportApi'] = None
        self._product: Optional['ProductApi'] = None
        self._asset: Optional['AssetApi'] = None
        self._production: Optional['ProductionApi'] = None
        self._software: Optional['SoftwareApi'] = None
        self._app: Optional['AppApi'] = None
        self._rootcause: Optional['RootCauseApi'] = None
    
    @property
    def report(self) -> 'ReportApi':
        """Report API endpoints."""
        if self._report is None:
            from .report_api import ReportApi
            self._report = ReportApi(self._http)
        return self._report
    
    @property
    def product(self) -> 'ProductApi':
        """Product API endpoints."""
        if self._product is None:
            from .product_api import ProductApi
            self._product = ProductApi(self._http)
        return self._product
    
    @property
    def asset(self) -> 'AssetApi':
        """Asset API endpoints."""
        if self._asset is None:
            from .asset_api import AssetApi
            self._asset = AssetApi(self._http)
        return self._asset
    
    @property
    def production(self) -> 'ProductionApi':
        """Production API endpoints."""
        if self._production is None:
            from .production_api import ProductionApi
            self._production = ProductionApi(self._http)
        return self._production
    
    @property
    def software(self) -> 'SoftwareApi':
        """Software distribution API endpoints."""
        if self._software is None:
            from .software_api import SoftwareApi
            self._software = SoftwareApi(self._http)
        return self._software
    
    @property
    def app(self) -> 'AppApi':
        """App/Statistics API endpoints."""
        if self._app is None:
            from .app_api import AppApi
            self._app = AppApi(self._http)
        return self._app
    
    @property
    def rootcause(self) -> 'RootCauseApi':
        """RootCause (Ticketing) API endpoints."""
        if self._rootcause is None:
            from .rootcause_api import RootCauseApi
            self._rootcause = RootCauseApi(self._http)
        return self._rootcause
