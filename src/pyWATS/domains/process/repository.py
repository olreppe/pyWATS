"""Process repository - public API data access layer.

Uses the public WATS API endpoints for process operations.
"""
from typing import List

from ...core import HttpClient
from .models import ProcessInfo


class ProcessRepository:
    """
    Process data access layer using public API.
    
    Uses:
    - GET /api/App/Processes (public endpoint)
    """
    
    def __init__(self, http_client: HttpClient):
        """
        Initialize repository with HTTP client.
        
        Args:
            http_client: The HTTP client for API calls
        """
        self._http = http_client
    
    def get_processes(self) -> List[ProcessInfo]:
        """
        Get all processes from the public API.
        
        GET /api/App/Processes
        
        Note: The public API returns processes with limited fields.
        Use ProcessRepositoryInternal for full details.
        
        Returns:
            List of ProcessInfo objects
        """
        response = self._http.get("/api/App/Processes")
        if response.is_success and response.data:
            return [ProcessInfo.model_validate(p) for p in response.data]
        return []
