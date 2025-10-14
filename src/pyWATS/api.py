"""
Main WATSApi class providing object-oriented access to all WATS functionality.

This module provides the primary interface for interacting with the WATS system,
organizing all functionality into logical modules accessible as properties.
"""

from typing import Optional, TYPE_CHECKING, List, Dict, Any, Union
from datetime import datetime, timedelta
from threading import Lock, Thread
import time

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


class OperationCache:
    """Cache for operation metadata with automatic refresh."""
    
    def __init__(self, refresh_interval_minutes: int = 5):
        self._operations: List[Dict[str, Any]] = []
        self._last_refresh: Optional[datetime] = None
        self._refresh_interval = timedelta(minutes=refresh_interval_minutes)
        self._lock = Lock()
        self._auto_refresh_thread: Optional[Thread] = None
        self._auto_refresh_enabled = False
    
    def is_stale(self) -> bool:
        """Check if cache needs refreshing."""
        if self._last_refresh is None:
            return True
        return datetime.now() - self._last_refresh > self._refresh_interval
    
    def update(self, operations: List[Dict[str, Any]]) -> None:
        """Update cache with new operation data."""
        with self._lock:
            self._operations = operations
            self._last_refresh = datetime.now()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all cached operations."""
        with self._lock:
            return self._operations.copy()
    
    def find_by_code(self, code: int) -> Optional[Dict[str, Any]]:
        """Find operation by code."""
        with self._lock:
            return next((op for op in self._operations if op.get('code') == code), None)
    
    def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find operation by name (case-insensitive)."""
        with self._lock:
            name_lower = name.lower()
            return next((op for op in self._operations if op.get('name', '').lower() == name_lower), None)


class WATSApi:
    """
    Main API class for WATS system interaction.
    
    Provides access to all WATS modules through properties and maintains
    cached metadata for operations (test, repair, and WIP operations).
    """
    
    def __init__(self, 
                 config: Optional[PyWATSConfig] = None,
                 base_url: Optional[str] = None,
                 token: Optional[str] = None,
                 operation_refresh_interval_minutes: int = 5,
                 auto_refresh_operations: bool = False):
        """
        Initialize WATSApi with configuration.
        
        Args:
            config: PyWATSConfig instance with connection settings
            base_url: Direct base URL for WATS API (alternative to config)
            token: Authentication token (alternative to config)
            operation_refresh_interval_minutes: How often to refresh operation cache (default: 5)
            auto_refresh_operations: Enable automatic background refresh (default: False)
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
        
        # Initialize operation cache
        self._operation_cache = OperationCache(refresh_interval_minutes=operation_refresh_interval_minutes)
        
        # Auto-refresh setup
        if auto_refresh_operations:
            self.start_operation_auto_refresh()
    
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
    
    # Operation Cache Management Methods
    
    def refresh_operations(self, force: bool = False) -> None:
        """
        Refresh operation metadata from server.
        
        This fetches all test operations, repair operations, and WIP operations
        from the WATS server and updates the local cache.
        
        Args:
            force: Force refresh even if cache is not stale
            
        Example:
            >>> api = WATSApi(base_url="https://api.example.com", token="token")
            >>> api.refresh_operations(force=True)
        """
        if not force and not self._operation_cache.is_stale():
            return
        
        try:
            from .rest_api.public.api.app import app_processes
            
            # Fetch all operation types
            response = app_processes.sync(
                client=self._http_client,
                include_test_operations=True,
                include_repair_operations=True,
                include_wip_operations=True,
                include_inactive_processes=False
            )
            
            # Try to access the correct attribute for the list of operations
            operation_list = None
            if response:
                if hasattr(response, 'items'):
                    operation_list = getattr(response, 'items')
                elif hasattr(response, 'data'):
                    operation_list = getattr(response, 'data')
                elif hasattr(response, 'result'):
                    operation_list = getattr(response, 'result')
                elif isinstance(response, list):
                    operation_list = response

            if operation_list:
                operations = []
                for op in operation_list:
                    operations.append({
                        'code': getattr(op, 'code', None),
                        'process_id': str(getattr(op, 'process_id', None)) if getattr(op, 'process_id', None) is not None else None,
                        'name': getattr(op, 'name', None),
                        'description': getattr(op, 'description', None),
                        'is_test_operation': getattr(op, 'is_test_operation', False),
                        'is_repair_operation': getattr(op, 'is_repair_operation', False),
                        'is_wip_operation': getattr(op, 'is_wip_operation', False),
                        'process_index': getattr(op, 'process_index', None),
                        'state': getattr(op, 'state', None),
                    })
                self._operation_cache.update(operations)
        except Exception as e:
            print(f"Warning: Failed to refresh operations: {e}")
    
    def get_operation(self, 
                     identifier: Union[int, str], 
                     operation_type: Optional[str] = None,
                     auto_refresh: bool = True,
                     strict: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get operation by code or name, optionally filtered by type.
        
        Args:
            identifier: Operation code (int) or name (str)
            operation_type: Filter by type: 'test', 'repair', 'wip', or None for any
            auto_refresh: Automatically refresh cache if stale (default: True)
            strict: Raise WATSNotFoundError if not found (default: False)
            
        Returns:
            Operation dictionary or None if not found
            
        Raises:
            WATSNotFoundError: If operation not found and strict=True
            
        Example:
            >>> api = WATSApi(base_url="https://api.example.com", token="token")
            >>> # Get any operation
            >>> op = api.get_operation("Final Test")
            >>> # Get specifically a test operation
            >>> test_op = api.get_operation("Final Test", operation_type="test")
            >>> # Get by code
            >>> op = api.get_operation(10)
        """
        if auto_refresh:
            self.refresh_operations()
        
        # Find operation
        if isinstance(identifier, int):
            operation = self._operation_cache.find_by_code(identifier)
        else:
            operation = self._operation_cache.find_by_name(identifier)
        
        # Apply type filter if specified
        if operation and operation_type:
            type_key = f'is_{operation_type}_operation'
            if not operation.get(type_key, False):
                operation = None
        
        if strict and operation is None:
            raise WATSNotFoundError(
                f"Operation '{identifier}'" + 
                (f" of type '{operation_type}'" if operation_type else "") + 
                " not found"
            )
        
        return operation
    
    def get_operation_code(self, 
                          identifier: Union[int, str],
                          operation_type: Optional[str] = None,
                          auto_refresh: bool = True,
                          strict: bool = True) -> Optional[int]:
        """
        Get operation code by name or validate code exists.
        
        This is a convenience method for when you need just the code value,
        useful for API calls that require operation codes.
        
        Args:
            identifier: Operation code (int) or name (str)
            operation_type: Filter by type: 'test', 'repair', 'wip', or None for any
            auto_refresh: Automatically refresh cache if stale (default: True)
            strict: Raise WATSNotFoundError if not found (default: True)
            
        Returns:
            Operation code (int) or None if not found and strict=False
            
        Raises:
            WATSNotFoundError: If operation not found and strict=True
            
        Example:
            >>> api = WATSApi(base_url="https://api.example.com", token="token")
            >>> # Get code by name
            >>> code = api.get_operation_code("Final Test")
            >>> # Validate code exists
            >>> code = api.get_operation_code(10)
            >>> # Get test operation code
            >>> code = api.get_operation_code("Final Test", operation_type="test")
        """
        operation = self.get_operation(identifier, operation_type, auto_refresh, strict)
        return operation.get('code') if operation else None
    
    def get_all_operations(self, 
                          operation_type: Optional[str] = None,
                          auto_refresh: bool = True) -> List[Dict[str, Any]]:
        """
        Get all operations, optionally filtered by type.
        
        Args:
            operation_type: Filter by type: 'test', 'repair', 'wip', or None for all
            auto_refresh: Automatically refresh cache if stale (default: True)
            
        Returns:
            List of operation dictionaries
            
        Example:
            >>> api = WATSApi(base_url="https://api.example.com", token="token")
            >>> # Get all operations
            >>> all_ops = api.get_all_operations()
            >>> # Get only test operations
            >>> test_ops = api.get_all_operations(operation_type="test")
            >>> # Get only repair operations
            >>> repair_ops = api.get_all_operations(operation_type="repair")
        """
        if auto_refresh:
            self.refresh_operations()
        
        operations = self._operation_cache.get_all()
        
        if operation_type:
            type_key = f'is_{operation_type}_operation'
            operations = [op for op in operations if op.get(type_key, False)]
        
        return operations
    
    def start_operation_auto_refresh(self) -> None:
        """
        Start automatic background refresh of operation cache.
        
        The cache will be refreshed in the background at the interval specified
        during initialization (default: 5 minutes).
        
        Example:
            >>> api = WATSApi(base_url="https://api.example.com", token="token")
            >>> api.start_operation_auto_refresh()
        """
        if self._operation_cache._auto_refresh_enabled:
            return
        
        self._operation_cache._auto_refresh_enabled = True
        
        def refresh_loop():
            while self._operation_cache._auto_refresh_enabled:
                try:
                    self.refresh_operations()
                except Exception as e:
                    print(f"Auto-refresh error: {e}")
                
                time.sleep(self._operation_cache._refresh_interval.total_seconds())
        
        self._operation_cache._auto_refresh_thread = Thread(target=refresh_loop, daemon=True)
        self._operation_cache._auto_refresh_thread.start()
    
    def stop_operation_auto_refresh(self) -> None:
        """
        Stop automatic background refresh of operation cache.
        
        Example:
            >>> api = WATSApi(base_url="https://api.example.com", token="token")
            >>> api.stop_operation_auto_refresh()
        """
        self._operation_cache._auto_refresh_enabled = False
        if self._operation_cache._auto_refresh_thread:
            self._operation_cache._auto_refresh_thread.join(timeout=5)
    
    def get_operation_cache_age(self) -> Optional[timedelta]:
        """
        Get age of operation cache.
        
        Returns:
            Time since last refresh or None if never refreshed
            
        Example:
            >>> api = WATSApi(base_url="https://api.example.com", token="token")
            >>> age = api.get_operation_cache_age()
            >>> if age and age.total_seconds() > 300:
            ...     print("Cache is older than 5 minutes")
        """
        if self._operation_cache._last_refresh:
            return datetime.now() - self._operation_cache._last_refresh
        return None
    
    # Legacy/Utility Methods for Other Metadata
    
    def get_repair_types(self) -> List[Dict[str, Any]]:
        """
        Get all available repair types.
        
        Note: This is different from repair operations. Repair types are categories
        of repairs (e.g., "Component Replacement", "Calibration").
        
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