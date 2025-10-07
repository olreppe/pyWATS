"""
pyWATS Connection Module

Manages connection settings and authentication for WATS API access.
This module provides a centralized way to configure the base URL and authentication
token for all REST API operations.
"""

import os
from typing import Optional
# TODO: Update to use new REST API structure
# from .rest_api.client import WATSClient, set_default_client


class WATSConnection:
    """
    WATS Connection configuration for API access.
    
    This class manages the base URL, authentication token, and other connection
    settings for the WATS API. It provides a centralized configuration point
    that can be used throughout the pyWATS library.
    """
    
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 30.0,
        referrer: Optional[str] = None
    ):
        """
        Initialize WATS connection.
        
        Args:
            base_url: Base URL for the WATS API (e.g., "https://your-wats-server.com")
            token: Authentication token (Basic auth encoded)
            timeout: Request timeout in seconds
            referrer: Referrer header for internal API access
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.timeout = timeout
        self.referrer = referrer or f"{self.base_url}/dashboard"
        
        # Create and set the default client
        self._client = WATSClient(
            base_url=self.base_url,
            auth_token=self.token,
            timeout=self.timeout,
            referrer=self.referrer
        )
        set_default_client(self._client)
    
    @property
    def client(self) -> WATSClient:
        """Get the underlying WATS client."""
        return self._client
    
    def update_token(self, token: str) -> None:
        """
        Update the authentication token.
        
        Args:
            token: New authentication token
        """
        self.token = token
        self._client.set_auth_token(token)
    
    def update_base_url(self, base_url: str) -> None:
        """
        Update the base URL and recreate the client.
        
        Args:
            base_url: New base URL
        """
        self.base_url = base_url.rstrip('/')
        self.referrer = f"{self.base_url}/dashboard"
        
        # Recreate client with new base URL
        self._client.close()
        self._client = WATSClient(
            base_url=self.base_url,
            auth_token=self.token,
            timeout=self.timeout,
            referrer=self.referrer
        )
        set_default_client(self._client)
    
    def test_connection(self) -> bool:
        """
        Test the connection to the WATS API.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try to access a simple endpoint (assets with top=1)
            response = self._client.get("/api/Asset", params={"$top": 1})
            return response.status_code == 200
        except Exception:
            return False
    
    def close(self) -> None:
        """Close the connection."""
        if self._client:
            self._client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def create_connection(
    base_url: str,
    token: str,
    timeout: float = 30.0,
    referrer: Optional[str] = None
) -> WATSConnection:
    """
    Create a WATS connection with the specified parameters.
    
    Args:
        base_url: Base URL for the WATS API
        token: Authentication token (Basic auth encoded)
        timeout: Request timeout in seconds
        referrer: Referrer header for internal API access
        
    Returns:
        Configured WATSConnection instance
    """
    return WATSConnection(
        base_url=base_url,
        token=token,
        timeout=timeout,
        referrer=referrer
    )


def create_connection_from_env() -> Optional[WATSConnection]:
    """
    Create a WATS connection from environment variables.
    
    Expected environment variables:
    - WATS_BASE_URL: Base URL for the WATS API
    - WATS_AUTH_TOKEN: Authentication token
    - WATS_TIMEOUT: Request timeout (optional, defaults to 30.0)
    - WATS_REFERRER: Referrer header (optional)
    
    Returns:
        WATSConnection instance if environment variables are set, None otherwise
    """
    base_url = os.getenv("WATS_BASE_URL")
    token = os.getenv("WATS_AUTH_TOKEN")
    
    if not base_url or not token:
        return None
    
    timeout = float(os.getenv("WATS_TIMEOUT", "30.0"))
    referrer = os.getenv("WATS_REFERRER")
    
    return WATSConnection(
        base_url=base_url,
        token=token,
        timeout=timeout,
        referrer=referrer
    )