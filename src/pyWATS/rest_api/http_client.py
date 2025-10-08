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
            base_url: The base URL for the WATS API (e.g., "https://py.wats.com")
            base64_token: Base64-encoded authentication token
            timeout: Request timeout in seconds (default: 30.0)
            **kwargs: Additional arguments passed to the base client
        """
        # Set up headers with authentication
        headers = kwargs.get('headers', {})
        headers.update({
            "Authorization": f"Basic {base64_token}",
            "Content-Type": "application/json",
        })
        kwargs['headers'] = headers
        
        super().__init__(base_url=base_url, timeout=httpx.Timeout(timeout), **kwargs)
        self._base64_token = base64_token

    def get_httpx_client(self) -> httpx.Client:
        """Override to return the configured httpx.Client with authentication."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                headers=self._headers,
                cookies=self._cookies,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._client

    def close(self):
        """Close the HTTP client connection."""
        if self._client is not None:
            self._client.close()
        if self._async_client is not None:
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self._async_client.aclose())
                else:
                    asyncio.run(self._async_client.aclose())
            except:
                pass  # Best effort cleanup

    def __enter__(self):
        """Support for use as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support for use as a context manager."""
        self.close()