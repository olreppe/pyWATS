"""pyWATS - Main API Class

The main entry point for the pyWATS library.
"""
from typing import Optional

from .http_client import HttpClient
from .rest_api import WATSEndpoints
from .modules import (
    ProductModule,
    AssetModule,
    ProductionModule,
    ReportModule,
    SoftwareModule,
    AppModule
)


class pyWATS:
    """
    Main pyWATS API class.
    
    Provides access to all WATS functionality through module properties:
    - product: Product management
    - asset: Asset management
    - production: Production/unit management
    - report: Report querying and submission
    - software: Software distribution
    - app: Statistics and KPIs
    
    Usage:
        from pywats import pyWATS
        
        # Initialize the API
        api = pyWATS(
            base_url="https://your-wats-server.com",
            token="your-api-token"
        )
        
        # Access product operations
        products = api.product.get_products()
        product = api.product.get_product("PART-001")
        
        # Access report operations
        headers = api.report.query_uut_headers()
        report = api.report.get_report("report-uuid")
        
        # Access statistics
        yield_data = api.app.get_dynamic_yield(filter)
    
    Authentication:
        The API uses Basic authentication. The token should be a Base64-encoded
        string in the format "username:password". The Authorization header will
        be sent as: "Basic <token>"
    """
    
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: int = 30
    ):
        """
        Initialize the pyWATS API.
        
        Args:
            base_url: Base URL of the WATS server (e.g., "https://your-wats.com")
            token: API token (Base64-encoded credentials)
            timeout: Request timeout in seconds (default: 30)
        """
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout = timeout
        
        # Initialize HTTP client
        self._http_client = HttpClient(
            base_url=self._base_url,
            token=self._token,
            timeout=self._timeout
        )
        
        # Initialize REST API endpoints
        self._endpoints = WATSEndpoints(self._http_client)
        
        # Module instances (lazy initialization)
        self._product: Optional[ProductModule] = None
        self._asset: Optional[AssetModule] = None
        self._production: Optional[ProductionModule] = None
        self._report: Optional[ReportModule] = None
        self._software: Optional[SoftwareModule] = None
        self._app: Optional[AppModule] = None
    
    # -------------------------------------------------------------------------
    # Module Properties
    # -------------------------------------------------------------------------
    
    @property
    def product(self) -> ProductModule:
        """
        Access product management operations.
        
        Returns:
            ProductModule instance
        """
        if self._product is None:
            self._product = ProductModule(self._endpoints.product)
        return self._product
    
    @property
    def asset(self) -> AssetModule:
        """
        Access asset management operations.
        
        Returns:
            AssetModule instance
        """
        if self._asset is None:
            self._asset = AssetModule(self._endpoints.asset)
        return self._asset
    
    @property
    def production(self) -> ProductionModule:
        """
        Access production/unit management operations.
        
        Includes sub-modules:
        - serial_number: Serial number operations
        - verification: Unit verification operations
        
        Returns:
            ProductionModule instance
        """
        if self._production is None:
            self._production = ProductionModule(self._endpoints.production)
        return self._production
    
    @property
    def report(self) -> ReportModule:
        """
        Access report operations.
        
        Returns:
            ReportModule instance
        """
        if self._report is None:
            self._report = ReportModule(self._endpoints.report)
        return self._report
    
    @property
    def software(self) -> SoftwareModule:
        """
        Access software distribution operations.
        
        Returns:
            SoftwareModule instance
        """
        if self._software is None:
            self._software = SoftwareModule(self._endpoints.software)
        return self._software
    
    @property
    def app(self) -> AppModule:
        """
        Access statistics and KPI operations.
        
        Returns:
            AppModule instance
        """
        if self._app is None:
            self._app = AppModule(self._endpoints.app)
        return self._app
    
    # -------------------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------------------
    
    @property
    def base_url(self) -> str:
        """Get the configured base URL."""
        return self._base_url
    
    @property
    def timeout(self) -> int:
        """Get the configured request timeout."""
        return self._timeout
    
    @timeout.setter
    def timeout(self, value: int):
        """Set the request timeout."""
        self._timeout = value
        self._http_client.timeout = value
    
    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------
    
    def test_connection(self) -> bool:
        """
        Test the connection to the WATS server.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            version = self.app.get_version()
            return version is not None
        except Exception:
            return False
    
    def get_version(self) -> dict:
        """
        Get WATS server version information.
        
        Returns:
            Version information dictionary
        """
        return self.app.get_version()
    
    def __repr__(self) -> str:
        """String representation of the pyWATS instance."""
        return f"pyWATS(base_url='{self._base_url}')"
