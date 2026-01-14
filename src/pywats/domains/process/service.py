"""Process service - public API business logic layer.

Uses the public WATS API for process operations with in-memory caching.

Internal API methods (marked with ⚠️ INTERNAL) use undocumented endpoints
that may change without notice. Use with caution.
"""
from typing import List, Optional, Union, Dict, Any, TYPE_CHECKING
from datetime import datetime, timedelta
from uuid import UUID
import threading

if TYPE_CHECKING:
    from .service_internal import ProcessServiceInternal

from .repository import ProcessRepository
from .models import ProcessInfo, RepairOperationConfig, RepairCategory


class ProcessService:
    """
    Process business logic layer using public API with caching.
    
    Maintains an in-memory cache of processes that refreshes at a 
    configurable interval. Provides read-only access to processes
    with lookup methods by name or code.
    
    Example:
        # Get a test operation by code
        process = api.process.get_test_operation(100)
        
        # Get a test operation by name
        process = api.process.get_test_operation("End of line test")
        
        # Get a repair operation
        repair = api.process.get_repair_operation(500)
        
        # Force cache refresh
        api.process.refresh()
    """
    
    # Default cache refresh interval (5 minutes)
    DEFAULT_REFRESH_INTERVAL = 300
    
    # Default process codes (WATS convention)
    DEFAULT_TEST_PROCESS_CODE = 100
    DEFAULT_REPAIR_PROCESS_CODE = 500
    
    def __init__(
        self, 
        repository: ProcessRepository,
        refresh_interval: int = DEFAULT_REFRESH_INTERVAL,
        internal_service: Optional["ProcessServiceInternal"] = None
    ):
        """
        Initialize service with repository and caching.
        
        Args:
            repository: ProcessRepository instance
            refresh_interval: Cache refresh interval in seconds (default: 300)
            internal_service: Optional internal service for internal API methods
        """
        self._repository = repository
        self._refresh_interval = refresh_interval
        self._internal = internal_service
        
        # Cache state
        self._cache: List[ProcessInfo] = []
        self._last_refresh: Optional[datetime] = None
        self._lock = threading.Lock()
    
    # =========================================================================
    # Cache Management
    # =========================================================================
    
    @property
    def refresh_interval(self) -> int:
        """Get the cache refresh interval in seconds."""
        return self._refresh_interval
    
    @refresh_interval.setter
    def refresh_interval(self, value: int) -> None:
        """Set the cache refresh interval in seconds."""
        if value < 0:
            raise ValueError("Refresh interval must be non-negative")
        self._refresh_interval = value
    
    def refresh(self) -> None:
        """
        Force refresh the process cache from the server.
        
        Thread-safe operation that fetches fresh data from the API.
        """
        with self._lock:
            self._cache = self._repository.get_processes()
            self._last_refresh = datetime.now()
    
    def _ensure_cache(self) -> None:
        """Ensure cache is populated and not stale."""
        needs_refresh = False
        
        with self._lock:
            if not self._cache or self._last_refresh is None:
                needs_refresh = True
            elif self._refresh_interval > 0:
                age = datetime.now() - self._last_refresh
                if age > timedelta(seconds=self._refresh_interval):
                    needs_refresh = True
        
        if needs_refresh:
            self.refresh()
    
    @property
    def last_refresh(self) -> Optional[datetime]:
        """Get the timestamp of the last cache refresh."""
        return self._last_refresh
    
    # =========================================================================
    # Process Listing (Read-Only)
    # =========================================================================
    
    def get_processes(self) -> List[ProcessInfo]:
        """
        Get all processes (cached).
        
        Returns:
            List of ProcessInfo objects
        """
        self._ensure_cache()
        return list(self._cache)  # Return copy to prevent modification
    
    def get_test_operations(self) -> List[ProcessInfo]:
        """
        Get all test operations (isTestOperation=true).
        
        Returns:
            List of test operation ProcessInfo objects
        """
        return [p for p in self.get_processes() if p.is_test_operation]
    
    def get_repair_operations(self) -> List[ProcessInfo]:
        """
        Get all repair operations (isRepairOperation=true).
        
        Returns:
            List of repair operation ProcessInfo objects
        """
        return [p for p in self.get_processes() if p.is_repair_operation]
    
    def get_wip_operations(self) -> List[ProcessInfo]:
        """
        Get all WIP operations (isWipOperation=true).
        
        Returns:
            List of WIP operation ProcessInfo objects
        """
        return [p for p in self.get_processes() if p.is_wip_operation]
    
    # =========================================================================
    # Process Lookup (Read-Only)
    # =========================================================================
    
    def get_process(self, identifier: Union[int, str]) -> Optional[ProcessInfo]:
        """
        Get a process by code or name.
        
        Args:
            identifier: Process code (int) or name (str)
            
        Returns:
            ProcessInfo or None if not found
        """
        for p in self.get_processes():
            if isinstance(identifier, int) and p.code == identifier:
                return p
            if isinstance(identifier, str) and p.name and p.name.lower() == identifier.lower():
                return p
        return None
    
    def get_test_operation(self, identifier: Union[int, str]) -> Optional[ProcessInfo]:
        """
        Get a test operation by code or name.
        
        Args:
            identifier: Process code (int) or name (str)
            
        Returns:
            ProcessInfo or None if not found or not a test operation
            
        Example:
            # By code
            process = api.process.get_test_operation(100)
            
            # By name
            process = api.process.get_test_operation("End of line test")
        """
        process = self.get_process(identifier)
        if process and process.is_test_operation:
            return process
        return None
    
    def get_repair_operation(self, identifier: Union[int, str]) -> Optional[ProcessInfo]:
        """
        Get a repair operation by code or name.
        
        Args:
            identifier: Process code (int) or name (str)
            
        Returns:
            ProcessInfo or None if not found or not a repair operation
            
        Example:
            # By code
            process = api.process.get_repair_operation(500)
            
            # By name
            process = api.process.get_repair_operation("Repair")
        """
        process = self.get_process(identifier)
        if process and process.is_repair_operation:
            return process
        return None
    
    def get_wip_operation(self, identifier: Union[int, str]) -> Optional[ProcessInfo]:
        """
        Get a WIP operation by code or name.
        
        Args:
            identifier: Process code (int) or name (str)
            
        Returns:
            ProcessInfo or None if not found or not a WIP operation
            
        Example:
            # By code
            process = api.process.get_wip_operation(200)
            
            # By name
            process = api.process.get_wip_operation("Assembly")
        """
        process = self.get_process(identifier)
        if process and process.is_wip_operation:
            return process
        return None
    
    # =========================================================================
    # Validation Helpers
    # =========================================================================
    
    def is_valid_test_operation(self, code: int) -> bool:
        """
        Check if a process code is a valid test operation.
        
        Args:
            code: The process code to validate
            
        Returns:
            True if the code is a valid test operation
        """
        return self.get_test_operation(code) is not None
    
    def is_valid_repair_operation(self, code: int) -> bool:
        """
        Check if a process code is a valid repair operation.
        
        Args:
            code: The process code to validate
            
        Returns:
            True if the code is a valid repair operation
        """
        return self.get_repair_operation(code) is not None
    
    def is_valid_wip_operation(self, code: int) -> bool:
        """
        Check if a process code is a valid WIP operation.
        
        Args:
            code: The process code to validate
            
        Returns:
            True if the code is a valid WIP operation
        """
        return self.get_wip_operation(code) is not None
    
    def get_default_test_code(self) -> int:
        """
        Get the default test process code.
        
        Returns:
            The first available test process code, or DEFAULT_TEST_PROCESS_CODE as fallback
        """
        test_ops = self.get_test_operations()
        if test_ops and test_ops[0].code is not None:
            return test_ops[0].code
        return self.DEFAULT_TEST_PROCESS_CODE
    
    def get_default_repair_code(self) -> int:
        """
        Get the default repair process code.
        
        Returns:
            The first available repair process code, or DEFAULT_REPAIR_PROCESS_CODE as fallback
        """
        repair_ops = self.get_repair_operations()
        if repair_ops and repair_ops[0].code is not None:
            return repair_ops[0].code
        return self.DEFAULT_REPAIR_PROCESS_CODE

    # =========================================================================
    # Extended Methods (from internal service)
    # =========================================================================
    # ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
    # These methods use undocumented WATS API endpoints.
    # =========================================================================

    def _ensure_internal(self) -> "ProcessServiceInternal":
        """Ensure internal service is available."""
        if self._internal is None:
            raise RuntimeError(
                "Internal process methods are not available. "
                "This pyWATS client was not configured with internal API support."
            )
        return self._internal

    # -------------------------------------------------------------------------
    # Process Operations (Internal)
    # -------------------------------------------------------------------------

    def get_all_processes(self) -> List[ProcessInfo]:
        """
        Get all processes with full details.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Returns:
            List of ProcessInfo objects with full details
        """
        return self._ensure_internal().get_processes()

    def get_process_by_id(self, process_id: UUID) -> Optional[ProcessInfo]:
        """
        Get a specific process by ID.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Args:
            process_id: The process GUID
            
        Returns:
            ProcessInfo or None if not found
        """
        return self._ensure_internal().get_process(process_id)

    def get_all_test_operations(self) -> List[ProcessInfo]:
        """
        Get all test operations with full details.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Returns:
            List of test operation ProcessInfo objects
        """
        return self._ensure_internal().get_test_operations()

    def get_all_repair_processes(self) -> List[ProcessInfo]:
        """
        Get all repair processes with full details.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Returns:
            List of repair ProcessInfo objects
        """
        return self._ensure_internal().get_repair_processes()

    def get_process_by_code(self, code: int) -> Optional[ProcessInfo]:
        """
        Get a process by its code.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Args:
            code: The process code (e.g., 100, 500)
            
        Returns:
            ProcessInfo or None if not found
        """
        return self._ensure_internal().get_process_by_code(code)

    # -------------------------------------------------------------------------
    # Repair Operations (Internal)
    # -------------------------------------------------------------------------

    def get_repair_operation_configs(self) -> Dict[int, RepairOperationConfig]:
        """
        Get all repair operation configurations.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Returns a dictionary keyed by process code (e.g., 500, 510)
        containing repair categories and fail codes.
        
        Returns:
            Dict mapping process code to RepairOperationConfig
        """
        return self._ensure_internal().get_repair_operation_configs()

    def get_repair_categories(self, repair_code: int = 500) -> List[RepairCategory]:
        """
        Get repair categories (fail code categories) for a repair process.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Args:
            repair_code: The repair process code (default 500)
            
        Returns:
            List of RepairCategory objects
        """
        return self._ensure_internal().get_repair_categories(repair_code)

    def get_fail_codes(self, repair_code: int = 500) -> List[Dict[str, Any]]:
        """
        Get flattened fail codes for a repair process.
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Args:
            repair_code: The repair process code (default 500)
            
        Returns:
            List of fail code dicts with category info
        """
        return self._ensure_internal().get_fail_codes(repair_code)

    # -------------------------------------------------------------------------
    # Validation Helpers (Internal)
    # -------------------------------------------------------------------------



