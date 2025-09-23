"""
pyWATS REST API Client Module

This module provides a REST client for the WATS API with session management,
authentication, and referrer header support for internal endpoints.
"""

import httpx
from typing import Optional, Dict, Any, Union
import os


class WATSClient:
    """
    REST client for WATS API with session management and authentication.
    
    Supports both public and internal API endpoints with proper referrer handling
    for internal endpoints as specified in the REST API strategy.
    """
    
    def __init__(
        self,
        base_url: str = "https://ola.wats.com",  # Updated to use example URL instead of OpenAPI spec URL
        auth_token: Optional[str] = None,
        timeout: float = 30.0,
        referrer: Optional[str] = None
    ):
        """
        Initialize WATS REST client.
        
        Args:
            base_url: Base URL for the WATS API (e.g., "https://ola.wats.com")
            auth_token: Authentication token for API access (Basic auth encoded)
            timeout: Request timeout in seconds
            referrer: Referrer header for internal API access
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.referrer = referrer or f"{base_url}/dashboard"
        
        # Default headers
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        
        # Add authentication if provided
        if auth_token:
            self.headers["Authorization"] = f"Basic {auth_token}"
            
        # Add referrer for internal API support
        if self.referrer:
            self.headers["Referer"] = self.referrer
            
        # Initialize HTTP client
        self.client = httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout
        )
    
    def set_auth_token(self, token: str) -> None:
        """Set or update the authentication token."""
        self.headers["Authorization"] = f"Basic {token}"
        self.client.headers.update(self.headers)
    
    def set_referrer(self, referrer: str) -> None:
        """Set or update the referrer header for internal API access."""
        self.referrer = referrer
        self.headers["Referer"] = referrer
        self.client.headers.update(self.headers)
    
    def get(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> httpx.Response:
        """Make GET request."""
        return self.client.get(url, params=params, **kwargs)
    
    def post(
        self, 
        url: str, 
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> httpx.Response:
        """Make POST request."""
        return self.client.post(url, json=json, data=data, params=params, **kwargs)
    
    def put(
        self, 
        url: str, 
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> httpx.Response:
        """Make PUT request."""
        return self.client.put(url, json=json, data=data, params=params, **kwargs)
    
    def delete(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> httpx.Response:
        """Make DELETE request."""
        return self.client.delete(url, params=params, **kwargs)
    
    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Default client instance - can be configured globally
default_client = None


def get_default_client() -> WATSClient:
    """
    Get or create the default WATS client instance.
    
    The client can be configured using environment variables:
    - WATS_BASE_URL: Base URL for the WATS API (defaults to "https://ola.wats.com")
    - WATS_AUTH_TOKEN: Authentication token
    - WATS_REFERRER: Referrer header for internal API access
    """
    global default_client
    
    if default_client is None:
        base_url = os.getenv("WATS_BASE_URL", "https://ola.wats.com")
        auth_token = os.getenv("WATS_AUTH_TOKEN")
        referrer = os.getenv("WATS_REFERRER")
        
        default_client = WATSClient(
            base_url=base_url,
            auth_token=auth_token,
            referrer=referrer
        )
    
    return default_client


def set_default_client(client: WATSClient) -> None:
    """Set the default client instance."""
    global default_client
    default_client = client