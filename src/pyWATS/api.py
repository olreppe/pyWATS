"""
Main WATSApi class providing object-oriented access to all WATS functionality.

This module provides the primary interface for interacting with the WATS system,
organizing all functionality into logical modules accessible as properties.
"""

from typing import Optional, TYPE_CHECKING, List, Dict, Any, Union
from datetime import datetime, timedelta

from .rest_api._http_client import WatsHttpClient
from .config import PyWATSConfig
from .exceptions import WATSNotFoundError
from .cache import OperationCache
from .models import Process, ProcessType

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
        self._operation_cache.set_refresh_callback(self._fetch_operations_from_server)
        
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
    
    # Process Cache Properties
    
    @property
    def processes(self) -> List[Process]:
        """Get all cached processes."""
        self._ensure_cache_fresh()
        return self._operation_cache.get_all_processes()
    
    @property
    def test_operations(self) -> List[Process]:
        """Get all test operations."""
        self._ensure_cache_fresh()
        return self._operation_cache.get_test_operations()
    
    @property
    def repair_operations(self) -> List[Process]:
        """Get all repair operations."""
        self._ensure_cache_fresh()
        return self._operation_cache.get_repair_operations()
    
    @property
    def wip_operations(self) -> List[Process]:
        """Get all WIP operations."""
        self._ensure_cache_fresh()
        return self._operation_cache.get_wip_operations()
    
    # Process Cache Management Methods
    
    def _ensure_cache_fresh(self, force: bool = False) -> None:
        """Ensure cache is fresh, refresh if needed."""
        if force or self._operation_cache.is_stale():
            self.refresh_operations()
    
    def _fetch_operations_from_server(self) -> None:
        """Fetch operations from server and update cache using REST API."""
        try:
            from .rest_api.public.api.app import app_processes
            
            print(f"Refreshing operations from {self._http_client._base_url}...")
            
            # Use the dedicated REST API endpoint which now handles parsing gracefully
            response = app_processes.sync_detailed(
                client=self._http_client,
                include_test_operations=True,
                include_repair_operations=True,
                include_wip_operations=True,
                include_inactive_processes=False
            )
            
            if response and response.status_code == 200:
                # The response.parsed now handles both model parsing and raw JSON fallback
                json_data = response.parsed
                
                print(f"Raw response type: {type(json_data)}")
                if isinstance(json_data, list):
                    if len(json_data) > 0:
                        print(f"Response is a list with {len(json_data)} items")
                        print(f"First item sample: {json_data[0]}")
                    else:
                        print("Response is an empty list")
                elif isinstance(json_data, dict):
                    print(f"Response is dict with keys: {list(json_data.keys())}")
                elif hasattr(json_data, '__dict__'):
                    print(f"Response is object with attributes: {list(json_data.__dict__.keys())}")
                
                # Extract operation list from response
                operation_list = self._extract_operation_list(json_data)
                
                print(f"Extracted {len(operation_list)} operations from response")
                
                # Parse operations into Process objects
                processes = []
                for i, op_data in enumerate(operation_list):
                    try:
                        if i < 3:  # Only log first 3 for brevity
                            print(f"Processing operation {i}: {op_data}")
                        process = Process.from_api_response(op_data)
                        processes.append(process)
                        if i < 3:
                            print(f"Successfully created process: {process}")
                    except Exception as e:
                        print(f"Error parsing operation {i} ({op_data}): {e}")
                        continue
                
                self._operation_cache.update(processes)
                
                # Print summary
                stats = self._operation_cache.get_cache_stats()
                print(f"Successfully cached {stats['total_processes']} operations: "
                      f"{stats['test_operations']} test, {stats['repair_operations']} repair, "
                      f"{stats['wip_operations']} WIP operations")
            else:
                print(f"HTTP request failed with status: {response.status_code if response else 'No response'}")
                if response and hasattr(response, 'content'):
                    print(f"Response content: {response.content}")
            
        except Exception as e:
            error_msg = f"Failed to refresh operations: {e}"
            print(f"ERROR: {error_msg}")
            print(f"Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(error_msg) from e
    
    def _extract_operation_list(self, response) -> List[Dict[str, Any]]:
        """Extract operation list from API response."""
        print(f"Extracting from response type: {type(response)}")
        
        # If response is already a list, return it directly
        if isinstance(response, list):
            print("Response is already a list")
            return response
        
        # If response is a dict, try to find the operation list
        if isinstance(response, dict):
            print(f"Response is dict with keys: {list(response.keys())}")
            # Try to get the operation list from different possible attributes
            for attr_name in ['items', 'data', 'result', 'processes', 'operations', 'value']:
                if attr_name in response:
                    operation_list = response[attr_name]
                    if operation_list is not None:
                        print(f"Found operations in key '{attr_name}': {len(operation_list) if isinstance(operation_list, list) else 'Not a list'}")
                        return operation_list if isinstance(operation_list, list) else []
        
        # Try to get from object attributes if it's not a dict/list
        if hasattr(response, '__dict__'):
            print(f"Response has attributes: {list(response.__dict__.keys())}")
            for attr_name in ['items', 'data', 'result', 'processes', 'operations', 'value']:
                if hasattr(response, attr_name):
                    operation_list = getattr(response, attr_name)
                    if operation_list is not None:
                        print(f"Found operations in attribute '{attr_name}': {len(operation_list) if isinstance(operation_list, list) else 'Not a list'}")
                        return operation_list if isinstance(operation_list, list) else []
        
        # If no known attribute found, try to use response directly if it's iterable
        if hasattr(response, '__iter__') and not isinstance(response, str):
            try:
                result = list(response)
                print(f"Converted iterable response to list with {len(result)} items")
                return result
            except Exception as e:
                print(f"Error converting to list: {e}")
        
        print("No operation list found, returning empty list")
        return []

    def refresh_operations(self, force: bool = False) -> None:
        """
        Refresh operation metadata from server.
        
        Args:
            force: Force refresh even if cache is not stale
        """
        if not force and not self._operation_cache.is_stale():
            return
        
        self._fetch_operations_from_server()
    
    def get_process(self, 
                   identifier: Union[int, str], 
                   process_type: Optional[ProcessType] = None,
                   auto_refresh: bool = True,
                   strict: bool = False) -> Optional[Process]:
        """
        Get process by code or name, optionally filtered by type.
        
        Args:
            identifier: Process code (int) or name (str)
            process_type: Filter by type
            auto_refresh: Automatically refresh cache if stale
            strict: Raise WATSNotFoundError if not found
            
        Returns:
            Process or None if not found
        """
        if auto_refresh:
            self._ensure_cache_fresh()
        
        # Find process
        if isinstance(identifier, int):
            if process_type:
                process = self._operation_cache.find_by_code_and_type(identifier, process_type)
            else:
                process = self._operation_cache.find_by_code(identifier)
        else:
            if process_type:
                process = self._operation_cache.find_by_name_and_type(identifier, process_type)
            else:
                process = self._operation_cache.find_by_name(identifier)
        
        if strict and process is None:
            type_str = f" of type '{process_type.value}'" if process_type else ""
            raise WATSNotFoundError(f"Process '{identifier}'{type_str} not found")
        
        return process
    
    def get_process_code(self, 
                        identifier: Union[int, str],
                        process_type: Optional[ProcessType] = None,
                        auto_refresh: bool = True,
                        strict: bool = True) -> Optional[int]:
        """Get process code by name or validate code exists."""
        process = self.get_process(identifier, process_type, auto_refresh, strict)
        return process.code if process else None
    
    def get_processes_by_type(self, process_type: ProcessType, auto_refresh: bool = True) -> List[Process]:
        """Get all processes of a specific type."""
        if auto_refresh:
            self._ensure_cache_fresh()
        return self._operation_cache.get_processes_by_type(process_type)
    
    def start_operation_auto_refresh(self) -> None:
        """Start automatic background refresh of operation cache."""
        self._operation_cache.start_auto_refresh()
    
    def stop_operation_auto_refresh(self) -> None:
        """Stop automatic background refresh of operation cache."""
        self._operation_cache.stop_auto_refresh()
    
    def get_operation_cache_stats(self) -> Dict[str, Any]:
        """Get operation cache statistics."""
        return self._operation_cache.get_cache_stats()
    
    def get_operation_cache_age(self) -> Optional[timedelta]:
        """Get age of operation cache."""
        stats = self.get_operation_cache_stats()
        last_refresh = stats.get('last_refresh')
        if last_refresh:
            return datetime.now() - last_refresh
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