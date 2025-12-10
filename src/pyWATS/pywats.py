"""pyWATS - Main API Class

The main entry point for the pyWATS library.
"""
from typing import Optional

from .core.client import HttpClient
from .core.exceptions import ErrorMode, ErrorHandler
from .domains.product import (
    ProductService, 
    ProductRepository,
    ProductServiceInternal,
    ProductRepositoryInternal,
)
from .domains.asset import AssetService, AssetRepository
from .domains.production import ProductionService, ProductionRepository
from .domains.report import ReportService, ReportRepository
from .domains.software import SoftwareService, SoftwareRepository
from .domains.app import AppService, AppRepository
from .domains.rootcause import RootCauseService, RootCauseRepository
from .domains.process import (
    ProcessService, 
    ProcessRepository,
    ProcessServiceInternal,
    ProcessRepositoryInternal,
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
    - rootcause: Ticketing system for issue collaboration
    
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
    
    # Default process cache refresh interval (5 minutes)
    DEFAULT_PROCESS_REFRESH_INTERVAL = 300
    
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: int = 30,
        process_refresh_interval: int = DEFAULT_PROCESS_REFRESH_INTERVAL,
        error_mode: ErrorMode = ErrorMode.STRICT
    ):
        """
        Initialize the pyWATS API.
        
        Args:
            base_url: Base URL of the WATS server (e.g., "https://your-wats.com")
            token: API token (Base64-encoded credentials)
            timeout: Request timeout in seconds (default: 30)
            process_refresh_interval: Process cache refresh interval in seconds (default: 300)
            error_mode: Error handling mode (STRICT or LENIENT). Default is STRICT.
                - STRICT: Raises exceptions for 404/empty responses
                - LENIENT: Returns None for 404/empty responses
        """
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout = timeout
        self._process_refresh_interval = process_refresh_interval
        self._error_mode = error_mode
        self._error_handler = ErrorHandler(error_mode)
        
        # Initialize HTTP client
        self._http_client = HttpClient(
            base_url=self._base_url,
            token=self._token,
            timeout=self._timeout
        )
        
        # Service instances (lazy initialization)
        self._product: Optional[ProductService] = None
        self._product_internal: Optional[ProductServiceInternal] = None
        self._asset: Optional[AssetService] = None
        self._production: Optional[ProductionService] = None
        self._report: Optional[ReportService] = None
        self._software: Optional[SoftwareService] = None
        self._app: Optional[AppService] = None
        self._rootcause: Optional[RootCauseService] = None
        self._process: Optional[ProcessService] = None
        self._process_internal: Optional[ProcessServiceInternal] = None
    
    # -------------------------------------------------------------------------
    # Module Properties
    # -------------------------------------------------------------------------
    
    @property
    def product(self) -> ProductService:
        """
        Access product management operations.
        
        Returns:
            ProductService instance
        """
        if self._product is None:
            repo = ProductRepository(self._http_client, self._error_handler)
            self._product = ProductService(repo)
        return self._product
    
    @property
    def product_internal(self) -> ProductServiceInternal:
        """
        Access internal product operations.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        This service uses internal WATS API endpoints that are not publicly
        documented. Methods may change or be removed without notice.
        
        Use this for:
        - Box build template management (subunit definitions)
        - BOM operations
        - Product categories
        
        Example:
            # Get a box build template
            with api.product_internal.get_box_build("MAIN-BOARD", "A") as bb:
                bb.add_subunit("PCBA-001", "A", quantity=2)
                bb.add_subunit("PSU-100", "B")
            # Changes saved automatically
        
        Returns:
            ProductServiceInternal instance
        """
        if self._product_internal is None:
            repo = ProductRepository(self._http_client)
            repo_internal = ProductRepositoryInternal(self._http_client, self._base_url)
            self._product_internal = ProductServiceInternal(repo, repo_internal)
        return self._product_internal
    
    @property
    def asset(self) -> AssetService:
        """
        Access asset management operations.
        
        Returns:
            AssetService instance
        """
        if self._asset is None:
            repo = AssetRepository(self._http_client, self._error_handler)
            self._asset = AssetService(repo)
        return self._asset
    
    @property
    def production(self) -> ProductionService:
        """
        Access production/unit management operations.
        
        Includes sub-modules:
        - serial_number: Serial number operations
        - verification: Unit verification operations
        
        Returns:
            ProductionService instance
        """
        if self._production is None:
            repo = ProductionRepository(self._http_client, self._error_handler)
            self._production = ProductionService(repo)
        return self._production
    
    @property
    def report(self) -> ReportService:
        """
        Access report operations.
        
        Returns:
            ReportService instance
        """
        if self._report is None:
            repo = ReportRepository(self._http_client, self._error_handler)
            self._report = ReportService(repo)
        return self._report
    
    @property
    def software(self) -> SoftwareService:
        """
        Access software distribution operations.
        
        Returns:
            SoftwareService instance
        """
        if self._software is None:
            repo = SoftwareRepository(self._http_client, self._error_handler)
            self._software = SoftwareService(repo)
        return self._software
    
    @property
    def app(self) -> AppService:
        """
        Access statistics and KPI operations.
        
        Returns:
            AppService instance
        """
        if self._app is None:
            repo = AppRepository(self._http_client, self._error_handler)
            self._app = AppService(repo)
        return self._app
    
    @property
    def rootcause(self) -> RootCauseService:
        """
        Access RootCause ticketing operations.
        
        The RootCause module provides a ticketing system for 
        collaboration on issue tracking and resolution.
        
        Returns:
            RootCauseService instance
        """
        if self._rootcause is None:
            repo = RootCauseRepository(self._http_client, self._error_handler)
            self._rootcause = RootCauseService(repo)
        return self._rootcause
    
    @property
    def process(self) -> ProcessService:
        """
        Access process/operation management (cached).
        
        Processes define the types of operations:
        - Test operations (e.g., End of line test, PCBA test)
        - Repair operations (e.g., Repair, RMA repair)
        - WIP operations (e.g., Assembly)
        
        The process list is cached in memory and refreshes at the configured
        interval (default: 5 minutes). Use api.process.refresh() to force refresh.
        
        Example:
            # Get by code
            test_op = api.process.get_test_operation(100)
            
            # Get by name
            repair_op = api.process.get_repair_operation("Repair")
            
            # Force refresh
            api.process.refresh()
        
        Returns:
            ProcessService instance
        """
        if self._process is None:
            repo = ProcessRepository(self._http_client, self._error_handler)
            self._process = ProcessService(repo, self._process_refresh_interval)
        return self._process
    
    @property
    def process_internal(self) -> ProcessServiceInternal:
        """
        Access internal process operations.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        This service uses internal WATS API endpoints that are not publicly
        documented. Methods may change or be removed without notice.
        
        Use this for:
        - Getting detailed process information with ProcessID
        - Getting repair categories and fail codes
        - Extended validation of process codes
        
        Returns:
            ProcessServiceInternal instance
        """
        if self._process_internal is None:
            repo = ProcessRepositoryInternal(self._http_client, self._base_url)
            self._process_internal = ProcessServiceInternal(repo)
        return self._process_internal
    
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
    
    @property
    def error_mode(self) -> ErrorMode:
        """Get the configured error handling mode."""
        return self._error_mode
    
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
