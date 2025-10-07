"""
Base module class for WATS API modules.

This module provides common functionality and structure for all WATS API modules.
"""

from typing import Any, Dict, List, Optional
from ..rest_api.http_client import WatsHttpClient
from ..exceptions import WATSException, WATSAPIError, WATSNotFoundError


class BaseModule:
    """
    Base class for all WATS API modules.
    
    Provides common functionality like error handling, response processing,
    and HTTP client access.
    """
    
    def __init__(self, http_client: WatsHttpClient):
        """
        Initialize the module with an HTTP client.
        
        Args:
            http_client: The WatsHttpClient instance for API communication
        """
        self._http_client = http_client
    
    @property
    def http_client(self) -> WatsHttpClient:
        """Get the HTTP client instance."""
        return self._http_client
    
    def _handle_api_error(self, response_data: Any, operation: str) -> None:
        """
        Handle API error responses and raise appropriate exceptions.
        
        Args:
            response_data: The response data from the API
            operation: Description of the operation that failed
            
        Raises:
            WATSAPIError: For general API errors
            WATSNotFoundError: For 404 errors
        """
        if hasattr(response_data, 'status_code'):
            if response_data.status_code == 404:
                raise WATSNotFoundError(f"{operation} failed: Resource not found")
            elif response_data.status_code >= 400:
                error_msg = f"{operation} failed with status {response_data.status_code}"
                if hasattr(response_data, 'text'):
                    error_msg += f": {response_data.text}"
                raise WATSAPIError(error_msg)
        
        # Handle other error scenarios
        if isinstance(response_data, dict) and 'error' in response_data:
            raise WATSAPIError(f"{operation} failed: {response_data['error']}")
    
    def _extract_data(self, response: Any) -> Any:
        """
        Extract data from API response.
        
        Args:
            response: The API response object
            
        Returns:
            The extracted data
        """
        # Handle different response types from the generated client
        if hasattr(response, 'content'):
            return response.content
        elif hasattr(response, 'data'):
            return response.data
        else:
            return response
    
    def _validate_id(self, item_id: Any, item_type: str = "item") -> None:
        """
        Validate that an ID is provided and not None.
        
        Args:
            item_id: The ID to validate
            item_type: The type of item for error messages
            
        Raises:
            WATSException: If the ID is None or empty
        """
        if item_id is None or item_id == "":
            raise WATSException(f"{item_type} ID cannot be None or empty")
    
    def _build_filter_params(self, **kwargs) -> Dict[str, Any]:
        """
        Build filter parameters for API queries, removing None values.
        
        Args:
            **kwargs: Filter parameters
            
        Returns:
            Dictionary of non-None filter parameters
        """
        return {k: v for k, v in kwargs.items() if v is not None}