"""
Main WATSApi class providing object-oriented access to all WATS functionality.

This module provides the primary interface for interacting with the WATS system,
organizing all functionality into logical modules accessible as properties.
"""

from typing import Optional, TYPE_CHECKING, List, Dict, Any, Union
from datetime import datetime
from .rest_api._http_client import WatsHttpClient
from .config import PyWATSConfig
from .exceptions import WATSNotFoundError

# Import module types for type hints without circular imports
if TYPE_CHECKING:
    from .modules.product import ProductModule
    from .modules.report import ReportModule
    from .modules.workflow import WorkflowModule
    from .modules.production import ProductionModule
    from .modules.asset import AssetModule
    from .modules.software import SoftwareModule
    from .modules.app import AppModule


class WATSApi:
    def is_connected(self) -> bool:
        """
        Check if the API is connected to the WATS service.
        Returns:
            bool: True if connected, False otherwise.
        """
        raise NotImplementedError("WATSApi.is_connected not implemented")
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
        # Prioritize direct parameters over config
        if base_url is not None:
            self._config = None
            self._http_client = WatsHttpClient(
                base_url=base_url,
                token=token or ""
            )
        elif config is not None:
            self._config = config
            self._http_client = WatsHttpClient(
                base_url=config.BASE_URL,
                token=config.AUTH_TOKEN
            )
        else:
            raise ValueError("Either config or base_url must be provided")
        
        # Initialize modules lazily
        self._product_module: Optional['ProductModule'] = None
        self._report_module: Optional['ReportModule'] = None
        self._workflow_module: Optional['WorkflowModule'] = None
        self._production_module: Optional['ProductionModule'] = None
        self._asset_module: Optional['AssetModule'] = None
        self._software_module: Optional['SoftwareModule'] = None
        self._app_module: Optional['AppModule'] = None
    
    @property
    def config(self) -> Optional[PyWATSConfig]:
        """Get the current configuration."""
        return self._config
    
    @property
    def http_client(self) -> WatsHttpClient:
        """Get the HTTP client for direct API access."""
        return self._http_client
    
    @property
    def product(self) -> 'ProductModule':
        """Access product management functionality."""
        if self._product_module is None:
            from .modules.product import ProductModule
            self._product_module = ProductModule(self._http_client)
        return self._product_module
    
    @property
    def report(self) -> 'ReportModule':
        """Access analytics and reporting functionality."""
        if self._report_module is None:
            from .modules.report import ReportModule
            self._report_module = ReportModule(self._http_client)
        return self._report_module
    
    @property
    def workflow(self) -> 'WorkflowModule':
        """Access workflow and step management functionality."""
        if self._workflow_module is None:
            from .modules.workflow import WorkflowModule
            self._workflow_module = WorkflowModule(self._http_client)
        return self._workflow_module
    
    @property
    def production(self) -> 'ProductionModule':
        """Access production tracking and control functionality."""
        if self._production_module is None:
            from .modules.production import ProductionModule
            self._production_module = ProductionModule(self._http_client)
        return self._production_module
    
    @property
    def asset(self) -> 'AssetModule':
        """Access asset management functionality."""
        if self._asset_module is None:
            from .modules.asset import AssetModule
            self._asset_module = AssetModule(self._http_client)
        return self._asset_module
    
    @property
    def software(self) -> 'SoftwareModule':
        """Access software package management functionality."""
        if self._software_module is None:
            from .modules.software import SoftwareModule
            self._software_module = SoftwareModule(self._http_client)
        return self._software_module
    
    @property
    def app(self) -> 'AppModule':
        """Access application and system management functionality."""
        if self._app_module is None:
            from .modules.app import AppModule
            self._app_module = AppModule(self._http_client)
        return self._app_module
    
    # Utility methods for metadata and reference data
    
    def get_operation_types(self) -> List[Dict[str, Any]]:
        """
        Get all available operation types.
        
        Returns:
            List[Dict[str, Any]]: List of operation type dictionaries with id, name, and description
        
        Example:
            >>> api = WATSApi("https://api.example.com", "token")
            >>> types = api.get_operation_types()
            >>> print(types[0]["name"])
        """
        # TODO: Replace with actual API endpoint when available
        return [
            {"id": 1, "name": "Test", "description": "Testing operation"},
            {"id": 2, "name": "Repair", "description": "Repair operation"}
        ]
    
    def get_operation_type(self, identifier: Union[int, str]) -> Dict[str, Any]:
        """
        Get a specific operation type by ID or name.
        
        Args:
            identifier: The operation type ID (int) or name (str)
            
        Returns:
            Dict[str, Any]: Operation type information
            
        Raises:
            WATSNotFoundError: If the operation type is not found
            
        Example:
            >>> api = WATSApi("https://api.example.com", "token")
            >>> op_type = api.get_operation_type("Test")
            >>> print(op_type["description"])
        """
        # TODO: Replace with actual API endpoint when available
        operation_types = self.get_operation_types()
        
        for op_type in operation_types:
            if isinstance(identifier, int) and op_type["id"] == identifier:
                return op_type
            elif isinstance(identifier, str) and op_type["name"].lower() == identifier.lower():
                return op_type
        
        raise WATSNotFoundError(f"Operation type '{identifier}' not found")
    
    def get_repair_types(self) -> List[Dict[str, Any]]:
        """
        Get all available repair types.
        
        Returns:
            List[Dict[str, Any]]: List of repair type dictionaries with id, name, and description
            
        Example:
            >>> api = WATSApi("https://api.example.com", "token")
            >>> types = api.get_repair_types()
            >>> for t in types:
            ...     print(f"{t['name']}: {t['description']}")
        """
        # TODO: Replace with actual API endpoint when available
        return [
            {"id": 1, "name": "Component", "description": "Component replacement"},
            {"id": 2, "name": "Adjustment", "description": "Calibration or adjustment"}
        ]
    
    def get_root_fail_codes(self, repair_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get root failure codes, optionally filtered by repair type.
        
        Args:
            repair_type: Optional repair type to filter by
            
        Returns:
            List[Dict[str, Any]]: List of failure code dictionaries
            
        Example:
            >>> api = WATSApi("https://api.example.com", "token")
            >>> codes = api.get_root_fail_codes("Component")
            >>> print(codes[0]["description"])
        """
        # TODO: Replace with actual API endpoint when available
        all_codes = [
            {"id": 1, "code": "ELEC-001", "description": "Electrical failure", "repair_type": "Component"},
            {"id": 2, "code": "MECH-001", "description": "Mechanical failure", "repair_type": "Component"}
        ]
        
        if repair_type:
            return [code for code in all_codes if code.get("repair_type") == repair_type]
        return all_codes
    
    def get_yield_monitor_statistics(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get yield monitoring statistics for a date range.
        
        Args:
            start_date: Start of the date range (defaults to 30 days ago)
            end_date: End of the date range (defaults to now)
            
        Returns:
            Dict[str, Any]: Statistics including total_units, passed_units, failed_units, 
                          yield_percentage, and date_range
                          
        Example:
            >>> api = WATSApi("https://api.example.com", "token")
            >>> from datetime import datetime, timedelta
            >>> stats = api.get_yield_monitor_statistics(
            ...     start_date=datetime.now() - timedelta(days=7),
            ...     end_date=datetime.now()
            ... )
            >>> print(f"Yield: {stats['yield_percentage']}%")
        """
        # TODO: Replace with actual API endpoint when available
        if not end_date:
            end_date = datetime.now().astimezone()
        if not start_date:
            from datetime import timedelta
            start_date = end_date - timedelta(days=30)
        
        return {
            "total_units": 1000,
            "passed_units": 950,
            "failed_units": 50,
            "yield_percentage": 95.0,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            }
        }
    
    def __repr__(self) -> str:
        """String representation of the API instance."""
        base_url = getattr(self._http_client, 'base_url', "Unknown") if self._http_client else "Unknown"
        return f"WATSApi(base_url='{base_url}')"