"""pyWATS - Main API Class

The main entry point for the pyWATS library.
"""
import logging
from typing import Optional, Union

from .core.client import HttpClient
from .core.station import Station, StationRegistry
from .core.retry import RetryConfig

logger = logging.getLogger(__name__)
from .core.exceptions import ErrorMode, ErrorHandler
from .domains.product import (
    ProductService, 
    ProductRepository,
    ProductServiceInternal,
    ProductRepositoryInternal,
)
from .domains.asset import (
    AssetService,
    AssetRepository,
    AssetServiceInternal,
    AssetRepositoryInternal,
)
from .domains.production import (
    ProductionService,
    ProductionRepository,
    ProductionServiceInternal,
    ProductionRepositoryInternal,
)
from .domains.report import ReportService, ReportRepository
from .domains.software import SoftwareService, SoftwareRepository
from .domains.analytics import (
    AnalyticsService, 
    AnalyticsRepository,
    AnalyticsServiceInternal,
    AnalyticsRepositoryInternal,
)
from .domains.rootcause import RootCauseService, RootCauseRepository
from .domains.scim import ScimService, ScimRepository
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
    - analytics: Yield statistics, KPIs, and failure analysis (also available as 'app')
    - rootcause: Ticketing system for issue collaboration
    
    Station Configuration:
        pyWATS supports a Station concept for managing test station identity.
        A Station encapsulates: name (machineName), location, and purpose.
        
        Single station mode (most common):
            api = pyWATS(
                base_url="https://your-wats-server.com",
                token="your-api-token",
                station=Station("TEST-STATION-01", "Lab A", "Production")
            )
        
        Multi-station mode (hub):
            api = pyWATS(base_url="...", token="...")
            api.stations.add("line-1", Station("PROD-LINE-1", "Building A", "Production"))
            api.stations.add("line-2", Station("PROD-LINE-2", "Building A", "Production"))
            api.stations.set_active("line-1")
    
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
        yield_data = api.analytics.get_dynamic_yield(filter)
    
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
        station: Optional[Station] = None,
        timeout: int = 30,
        process_refresh_interval: int = DEFAULT_PROCESS_REFRESH_INTERVAL,
        error_mode: ErrorMode = ErrorMode.STRICT,
        retry_config: Optional[RetryConfig] = None,
        retry_enabled: bool = True,
    ):
        """
        Initialize the pyWATS API.
        
        Args:
            base_url: Base URL of the WATS server (e.g., "https://your-wats.com")
            token: API token (Base64-encoded credentials)
            station: Default station configuration for reports. If provided,
                     this station's name, location, and purpose will be used
                     when creating reports (unless overridden).
            timeout: Request timeout in seconds (default: 30)
            process_refresh_interval: Process cache refresh interval in seconds (default: 300)
            error_mode: Error handling mode (STRICT or LENIENT). Default is STRICT.
                - STRICT: Raises exceptions for 404/empty responses
                - LENIENT: Returns None for 404/empty responses
            retry_config: Custom retry configuration. If None, uses defaults.
            retry_enabled: Enable/disable retry (default: True). 
                Shorthand for RetryConfig(enabled=False).
        """
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout = timeout
        self._process_refresh_interval = process_refresh_interval
        self._error_mode = error_mode
        self._error_handler = ErrorHandler(error_mode)
        
        # Retry configuration
        if retry_config is not None:
            self._retry_config = retry_config
        elif not retry_enabled:
            self._retry_config = RetryConfig(enabled=False)
        else:
            self._retry_config = RetryConfig()
        
        # Station configuration
        self._station: Optional[Station] = station
        self._station_registry = StationRegistry()
        if station:
            self._station_registry.set_default(station)
        
        # Initialize HTTP client
        self._http_client = HttpClient(
            base_url=self._base_url,
            token=self._token,
            timeout=self._timeout,
            retry_config=self._retry_config,
        )
        
        # Service instances (lazy initialization)
        self._product: Optional[ProductService] = None
        self._asset: Optional[AssetService] = None
        self._production: Optional[ProductionService] = None
        self._report: Optional[ReportService] = None
        self._software: Optional[SoftwareService] = None
        self._analytics: Optional[AnalyticsService] = None
        self._rootcause: Optional[RootCauseService] = None
        self._scim: Optional[ScimService] = None
        self._process: Optional[ProcessService] = None
    
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
            # Also create internal service for extended methods
            repo_internal = ProductRepositoryInternal(self._http_client, self._base_url)
            internal_service = ProductServiceInternal(repo, repo_internal)
            self._product = ProductService(repo, internal_service)
        return self._product
    
    @property
    def asset(self) -> AssetService:
        """
        Access asset management operations.
        
        Returns:
            AssetService instance
        """
        if self._asset is None:
            repo = AssetRepository(self._http_client, self._error_handler)
            # Also create internal service for extended methods
            repo_internal = AssetRepositoryInternal(self._http_client, self._base_url)
            internal_service = AssetServiceInternal(repo_internal)
            self._asset = AssetService(repo, self._base_url, internal_service)
        return self._asset
    
    @property
    def production(self) -> ProductionService:
        """
        Access production/unit management operations.
        
        Includes sub-modules:
        - serial_number: Serial number operations
        - verification: Unit verification operations
        
        Unit phases are cached and accessible via:
        - get_phases(): Get all available phases
        - get_phase(id_or_name): Get a specific phase
        
        Returns:
            ProductionService instance
        """
        if self._production is None:
            repo = ProductionRepository(self._http_client, self._error_handler)
            # Also create internal service for extended methods
            repo_internal = ProductionRepositoryInternal(self._http_client, self._base_url)
            internal_service = ProductionServiceInternal(repo_internal)
            self._production = ProductionService(repo, base_url=self._base_url, internal_service=internal_service)
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
            self._report = ReportService(repo, station_provider=self._get_station)
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
    def analytics(self) -> AnalyticsService:
        """
        Access yield statistics, KPIs, and failure analysis.
        
        Provides high-level operations for:
        - Yield statistics (dynamic yield, volume yield, worst yield)
        - Failure analysis (top failed steps, test step analysis)
        - Production metrics (OEE, measurements)
        - Report queries (serial number history, UUT/UUR reports)
        - Unit flow analysis (⚠️ internal API)
        - Measurement/step drill-down (⚠️ internal API)
        
        Example:
            >>> # Get yield for a product
            >>> yield_data = api.analytics.get_dynamic_yield(
            ...     WATSFilter(part_number="WIDGET-001", period_count=30)
            ... )
            >>> # Get top failures
            >>> failures = api.analytics.get_top_failed(part_number="WIDGET-001")
        
        Returns:
            AnalyticsService instance
        """
        if self._analytics is None:
            repo = AnalyticsRepository(self._http_client, self._error_handler)
            # Also create internal service for internal API methods
            repo_internal = AnalyticsRepositoryInternal(self._http_client, self._base_url)
            internal_service = AnalyticsServiceInternal(repo_internal)
            self._analytics = AnalyticsService(repo, internal_service)
        return self._analytics
    
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
    def scim(self) -> ScimService:
        """
        Access SCIM user provisioning operations.
        
        SCIM (System for Cross-domain Identity Management) provides
        automatic user provisioning from Azure Active Directory to WATS.
        
        Use this for:
        - Generating provisioning tokens for Azure AD configuration
        - Managing SCIM users (create, read, update, delete)
        - Querying users by ID or username
        
        Example:
            >>> # Get a provisioning token for Azure AD
            >>> token = api.scim.get_token(duration_days=90)
            >>> print(f"Configure Azure with token: {token.token[:50]}...")
            
            >>> # List all SCIM users
            >>> users = api.scim.get_users()
            >>> for user in users.resources:
            ...     print(f"{user.user_name}: {user.display_name}")
            
            >>> # Deactivate a user
            >>> api.scim.deactivate_user("user-guid")
        
        Returns:
            ScimService instance
        """
        if self._scim is None:
            repo = ScimRepository(self._http_client, self._error_handler)
            self._scim = ScimService(repo)
        return self._scim
    
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
            # Also create internal service for extended methods
            repo_internal = ProcessRepositoryInternal(self._http_client, self._base_url)
            internal_service = ProcessServiceInternal(repo_internal)
            self._process = ProcessService(repo, self._process_refresh_interval, internal_service)
        return self._process
    
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
    
    @property
    def retry_config(self) -> RetryConfig:
        """Get the retry configuration."""
        return self._retry_config
    
    @retry_config.setter
    def retry_config(self, value: RetryConfig) -> None:
        """Set the retry configuration."""
        self._retry_config = value
        self._http_client.retry_config = value
    
    # -------------------------------------------------------------------------
    # Station Configuration
    # -------------------------------------------------------------------------
    
    @property
    def station(self) -> Optional[Station]:
        """
        Get the currently active station.
        
        Returns the active station from the registry, or the default station
        if no active station is set.
        
        Returns:
            Active Station or None
        """
        return self._station_registry.active or self._station
    
    @station.setter
    def station(self, station: Optional[Station]) -> None:
        """
        Set the default station.
        
        This station will be used for reports when no station is explicitly
        specified.
        
        Args:
            station: Station to set as default
        """
        self._station = station
        if station:
            self._station_registry.set_default(station)
    
    @property
    def stations(self) -> StationRegistry:
        """
        Access the station registry for multi-station support.
        
        Use this for scenarios where a single client handles reports
        from multiple stations (hub mode).
        
        Example:
            # Add stations
            api.stations.add("line-1", Station("PROD-LINE-1", "Building A", "Production"))
            api.stations.add("line-2", Station("PROD-LINE-2", "Building A", "Production"))
            
            # Set active station
            api.stations.set_active("line-1")
            
            # Get active station
            station = api.stations.active
        
        Returns:
            StationRegistry instance
        """
        return self._station_registry
    
    def _get_station(self) -> Optional[Station]:
        """
        Internal method to get the current station.
        
        Used by services that need station information.
        
        Returns:
            Current station or None
        """
        return self.station
    
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
            version = self.analytics.get_version()
            return version is not None
        except Exception as e:
            logger.debug(f"Connection test failed: {e}")
            return False
    
    def get_version(self) -> dict:
        """
        Get WATS server version information.
        
        Returns:
            Version information dictionary
        """
        return self.analytics.get_version()
    
    def __repr__(self) -> str:
        """String representation of the pyWATS instance."""
        return f"pyWATS(base_url='{self._base_url}')"
