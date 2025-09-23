"""
Authentication Endpoints

Authentication and authorization endpoints.
These endpoints are grouped by the "Auth" tag in the OpenAPI specification.
"""

from typing import Optional, Dict, Any
import httpx

from ..client import get_default_client, WATSClient
from ..exceptions import handle_response_error


def get_token(
    reset: Optional[bool] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Create and return a new access token (identified by the authenticated user).
    
    You will get access to the WATS API by specifying the Authorization header 
    together with the returned token. The token is visible only once, 
    please store it securely.
    
    Args:
        reset: Create a new token (the old one is no longer valid)
        client: Optional WATS client instance
        
    Returns:
        Access token data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if reset is not None:
        params["reset"] = reset
    
    response = client.get("/api/Auth/GetToken", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_token_with_identifier(
    identifier: str,
    reset: Optional[bool] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Create and return a new access token with a specific identifier.
    
    Args:
        identifier: Token identifier
        reset: Create a new token (the old one is no longer valid)
        client: Optional WATS client instance
        
    Returns:
        Access token data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if reset is not None:
        params["reset"] = reset
    
    response = client.get(f"/api/Auth/GetToken/{identifier}", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()