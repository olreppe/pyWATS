"""
Operation cache manager for WATS processes.

This module provides caching functionality for WATS operations with automatic
refresh capabilities and type-based filtering.
"""

from typing import List, Optional, Union, Dict, Any, Callable
from datetime import datetime, timedelta
from threading import Lock, Thread
import time

from ..models.process import Process, ProcessType


class OperationCache:
    """
    Cache manager for WATS operations with automatic refresh.
    
    Maintains a cache of all available processes (TestOperations, RepairOperations,
    and WIP Operations) with configurable auto-refresh functionality.
    """
    
    def __init__(self, refresh_interval_minutes: int = 5):
        """
        Initialize operation cache.
        
        Args:
            refresh_interval_minutes: How often to refresh cache automatically
        """
        self._processes: List[Process] = []
        self._last_refresh: Optional[datetime] = None
        self._refresh_interval = timedelta(minutes=refresh_interval_minutes)
        self._lock = Lock()
        self._auto_refresh_thread: Optional[Thread] = None
        self._auto_refresh_enabled = False
        self._refresh_callback: Optional[Callable[[], None]] = None
    
    def set_refresh_callback(self, callback: Callable[[], None]) -> None:
        """Set callback function to fetch fresh data from server."""
        self._refresh_callback = callback
    
    def is_stale(self) -> bool:
        """Check if cache needs refreshing."""
        if self._last_refresh is None:
            return True
        return datetime.now() - self._last_refresh > self._refresh_interval
    
    def update(self, processes: List[Process]) -> None:
        """
        Update cache with new process data.
        
        Args:
            processes: List of Process objects to cache
        """
        with self._lock:
            self._processes = processes.copy()
            self._last_refresh = datetime.now()
    
    def get_all_processes(self) -> List[Process]:
        """Get all cached processes."""
        with self._lock:
            return self._processes.copy()
    
    def get_test_operations(self) -> List[Process]:
        """Get all test operations."""
        with self._lock:
            return [p for p in self._processes if p.is_test_operation]
    
    def get_repair_operations(self) -> List[Process]:
        """Get all repair operations."""
        with self._lock:
            return [p for p in self._processes if p.is_repair_operation]
    
    def get_wip_operations(self) -> List[Process]:
        """Get all WIP operations."""
        with self._lock:
            return [p for p in self._processes if p.is_wip_operation]
    
    def get_processes_by_type(self, process_type: ProcessType) -> List[Process]:
        """
        Get processes filtered by type.
        
        Args:
            process_type: Type of processes to return
            
        Returns:
            List of processes matching the specified type
        """
        with self._lock:
            if process_type == ProcessType.TEST:
                return [p for p in self._processes if p.is_test_operation]
            elif process_type == ProcessType.REPAIR:
                return [p for p in self._processes if p.is_repair_operation]
            elif process_type == ProcessType.WIP:
                return [p for p in self._processes if p.is_wip_operation]
            else:
                return self._processes.copy()
    
    def find_by_code(self, code: int) -> Optional[Process]:
        """Find process by code."""
        with self._lock:
            return next((p for p in self._processes if p.code == code), None)
    
    def find_by_name(self, name: str, case_sensitive: bool = False) -> Optional[Process]:
        """
        Find process by name.
        
        Args:
            name: Process name to search for
            case_sensitive: Whether to perform case-sensitive search
            
        Returns:
            First matching process or None
        """
        with self._lock:
            if case_sensitive:
                return next((p for p in self._processes if p.name == name), None)
            else:
                name_lower = name.lower()
                return next((p for p in self._processes if p.name.lower() == name_lower), None)
    
    def find_by_code_and_type(self, code: int, process_type: ProcessType) -> Optional[Process]:
        """
        Find process by code and type.
        
        Args:
            code: Process code
            process_type: Required process type
            
        Returns:
            Matching process or None
        """
        process = self.find_by_code(code)
        if process and process_type in process.process_types:
            return process
        return None
    
    def find_by_name_and_type(self, name: str, process_type: ProcessType, case_sensitive: bool = False) -> Optional[Process]:
        """
        Find process by name and type.
        
        Args:
            name: Process name
            process_type: Required process type
            case_sensitive: Whether to perform case-sensitive search
            
        Returns:
            Matching process or None
        """
        process = self.find_by_name(name, case_sensitive)
        if process and process_type in process.process_types:
            return process
        return None
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            total_count = len(self._processes)
            test_count = sum(1 for p in self._processes if p.is_test_operation)
            repair_count = sum(1 for p in self._processes if p.is_repair_operation)
            wip_count = sum(1 for p in self._processes if p.is_wip_operation)
            
            return {
                "total_processes": total_count,
                "test_operations": test_count,
                "repair_operations": repair_count,
                "wip_operations": wip_count,
                "last_refresh": self._last_refresh,
                "is_stale": self.is_stale(),
                "auto_refresh_enabled": self._auto_refresh_enabled
            }
    
    def start_auto_refresh(self) -> None:
        """Start automatic background refresh."""
        if self._auto_refresh_enabled or not self._refresh_callback:
            return
        
        self._auto_refresh_enabled = True
        
        def refresh_loop():
            while self._auto_refresh_enabled:
                try:
                    if self.is_stale():
                        self._refresh_callback()
                except Exception as e:
                    print(f"Auto-refresh error: {e}")
                
                time.sleep(60)  # Check every minute
        
        self._auto_refresh_thread = Thread(target=refresh_loop, daemon=True)
        self._auto_refresh_thread.start()
    
    def stop_auto_refresh(self) -> None:
        """Stop automatic background refresh."""
        self._auto_refresh_enabled = False
        if self._auto_refresh_thread:
            self._auto_refresh_thread.join(timeout=5)
    
    def __len__(self) -> int:
        """Get number of cached processes."""
        with self._lock:
            return len(self._processes)
