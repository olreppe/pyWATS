"""Process service - public API business logic layer.

Uses the public WATS API for process operations.
"""
from typing import List, Optional

from .repository import ProcessRepository
from .models import ProcessInfo


class ProcessService:
    """
    Process business logic layer using public API.
    
    Provides operations for working with test operations and repair operations.
    """
    
    def __init__(self, repository: ProcessRepository):
        """
        Initialize service with repository.
        
        Args:
            repository: ProcessRepository instance
        """
        self._repository = repository
    
    def get_processes(self) -> List[ProcessInfo]:
        """
        Get all processes.
        
        Returns:
            List of ProcessInfo objects
        """
        return self._repository.get_processes()
    
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
    
    def get_process_by_code(self, code: int) -> Optional[ProcessInfo]:
        """
        Get a process by its code.
        
        Args:
            code: The process code (e.g., 100, 500)
            
        Returns:
            ProcessInfo or None if not found
        """
        for p in self.get_processes():
            if p.code == code:
                return p
        return None
    
    def is_valid_test_operation(self, code: int) -> bool:
        """
        Check if a process code is a valid test operation.
        
        Args:
            code: The process code to validate
            
        Returns:
            True if the code is a valid test operation
        """
        process = self.get_process_by_code(code)
        return process is not None and process.is_test_operation
    
    def is_valid_repair_operation(self, code: int) -> bool:
        """
        Check if a process code is a valid repair operation.
        
        Args:
            code: The process code to validate
            
        Returns:
            True if the code is a valid repair operation
        """
        process = self.get_process_by_code(code)
        return process is not None and process.is_repair_operation
    
    def get_default_repair_code(self) -> int:
        """
        Get the default repair process code.
        
        Returns:
            The first available repair process code, or 500 as fallback
        """
        repair_procs = self.get_repair_operations()
        if repair_procs:
            return repair_procs[0].code or 500
        return 500
