"""Unified WATS HTTP client for all REST APIs."""

import httpx
from typing import Optional
from pyWATS.rest_api.public.client import Client as BaseClient  # generated base client


class WatsHttpClient(BaseClient):
    """Unified WATS HTTP client for all REST APIs."""

    def __init__(self, base_url: str, base64_token: str, timeout: float = 30.0, **kwargs):
        """
        Initialize the WATS HTTP client.
        
        Args:
            base_url: The base URL for the WATS API (e.g., "https://live.wats.com")
            base64_token: Base64-encoded authentication token
            timeout: Request timeout in seconds (default: 30.0)
            **kwargs: Additional arguments passed to the base client
        """
        super().__init__(base_url=base_url, timeout=httpx.Timeout(timeout), **kwargs)
        self._http = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Basic {base64_token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def get_httpx_client(self) -> httpx.Client:
        """Override to return the persistent shared httpx.Client."""
        return self._http

    def close(self):
        """Close the HTTP client connection."""
        if hasattr(self, '_http'):
            self._http.close()

    def __enter__(self):
        """Support for use as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for use as a context manager."""
        self.close()