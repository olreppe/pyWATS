"""
Main WATSApi class providing object-oriented access to all WATS functionality.

This module provides the primary interface for interacting with the WATS system,
organizing all functionality into logical modules accessible as properties.
"""

from typing import Optional
from .rest_api._http_client import WatsHttpClient
from .config import PyWATSConfig


class WATSApi:
    """
    Main API class for WATS system interaction.
    
    Provides access to all WATS modules through properties:
    - product: Product management and configuration
    - report: Analytics and reporting functionality  
    - workflow: Workflow and step management
    - production: Production tracking and control
    - asset: Asset management
    - software: Software package management
    - app: Application and system management
    
    Example:
        ```python
        # Initialize API with configuration
        api = WATSApi(config=config)
        
        # Access modules through properties
        products = api.product.get_all()
        report = api.report.generate_statistics()
        ```
    """
    
    def __init__(self, 
                 config: Optional[PyWATSConfig] = None,
                 base_url: Optional[str] = None,
                 token: Optional[str] = None):
        """
        Initialize WATSApi with configuration.
        
        Args:
            config: PyWATSConfig instance with connection settings
            base_url: Direct base URL for WATS API (alternative to config)
            token: Authentication token (alternative to config)
        """
        if config is not None:
            self._config = config
            self._http_client = WatsHttpClient(
                base_url=config.BASE_URL,
                base64_token=config.AUTH_TOKEN
            )
        elif base_url is not None:
            self._config = None
            self._http_client = WatsHttpClient(
                base_url=base_url,
                base64_token=token or ""
            )
        else:
            raise ValueError("Either config or base_url must be provided")
        
        # Initialize modules lazily
        self._product_module = None
        self._report_module = None
        self._workflow_module = None
        self._production_module = None
        self._asset_module = None
        self._software_module = None
        self._app_module = None
    
    @property
    def config(self) -> Optional[PyWATSConfig]:
        """Get the current configuration."""
        return self._config
    
    @property
    def http_client(self) -> WatsHttpClient:
        """Get the HTTP client for direct API access."""
        return self._http_client
    
    @property
    def product(self):
        """Access product management functionality."""
        if self._product_module is None:
            from .modules.product import ProductModule
            self._product_module = ProductModule(self._http_client)
        return self._product_module
    
    @property
    def report(self):
        """Access analytics and reporting functionality."""
        if self._report_module is None:
            from .modules.report import ReportModule
            self._report_module = ReportModule(self._http_client)
        return self._report_module
    
    @property
    def workflow(self):
        """Access workflow and step management functionality."""
        if self._workflow_module is None:
            from .modules.workflow import WorkflowModule
            self._workflow_module = WorkflowModule(self._http_client)
        return self._workflow_module
    
    @property
    def production(self):
        """Access production tracking and control functionality."""
        if self._production_module is None:
            from .modules.production import ProductionModule
            self._production_module = ProductionModule(self._http_client)
        return self._production_module
    
    @property
    def asset(self):
        """Access asset management functionality."""
        if self._asset_module is None:
            from .modules.asset import AssetModule
            self._asset_module = AssetModule(self._http_client)
        return self._asset_module
    
    @property
    def software(self):
        """Access software package management functionality."""
        if self._software_module is None:
            from .modules.software import SoftwareModule
            self._software_module = SoftwareModule(self._http_client)
        return self._software_module
    
    @property
    def app(self):
        """Access application and system management functionality."""
        if self._app_module is None:
            from .modules.app import AppModule
            self._app_module = AppModule(self._http_client)
        return self._app_module
    
    def __repr__(self) -> str:
        """String representation of the API instance."""
        base_url = getattr(self._http_client, 'base_url', "Unknown") if self._http_client else "Unknown"
        return f"WATSApi(base_url='{base_url}')"