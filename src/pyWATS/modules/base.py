"""
Base module class for all WATS modules.

Provides common functionality and validation methods for all modules.
"""
from typing import TYPE_CHECKING, Union
from ..exceptions import WATSException

if TYPE_CHECKING:
    from ..rest_api._http_client import WatsHttpClient
    from ..rest_api.public.client import AuthenticatedClient, Client


class BaseModule:
    """
    Base class for all WATS API modules.
    
    Provides common functionality like validation and error handling
    that is shared across all modules.
    """
    
    def __init__(self, client: Union['WatsHttpClient', 'AuthenticatedClient', 'Client']):
        """
        Initialize the base module.
        
        Args:
            client: HTTP client instance for making API requests
        """
        self.http_client = client
    
    def _validate_id(self, id_value: str, entity_name: str) -> None:
        """
        Validate that an ID is provided and not empty.
        
        Args:
            id_value: The ID to validate
            entity_name: Name of the entity type (for error messages)
            
        Raises:
            WATSException: If the ID is invalid
        """
        if not id_value:
            raise WATSException(f"{entity_name} ID must be provided")
    
    def _build_filter_params(self, **kwargs) -> dict:
        """
        Build a dictionary of filter parameters, excluding None values.
        
        Args:
            **kwargs: Filter parameters
            
        Returns:
            Dictionary with non-None parameters
        """
        return {k: v for k, v in kwargs.items() if v is not None}