"""
Custom HTTP client for WATS API with Basic authentication.

This module implements a workaround for authentication issues in the generated
OpenAPI client. The standard AuthenticatedClient uses Bearer token authentication,
but WATS API requires Basic authentication.

KNOWN ISSUES & WORKAROUNDS:
===========================

Issue #1: Empty Authorization Header
-------------------------------------
The generated OpenAPI client creates empty headers in endpoint functions
(e.g., report_post_wsjf.py line 19: `headers: dict[str, Any] = {}`).
These empty headers override the httpx client's default headers, resulting
in missing Authorization headers in HTTP requests.

Workaround: We monkey-patch the httpx.Client.request() method during
initialization to intercept all requests and inject authentication headers
before they are sent.

Issue #2: Parent Class Authorization Logic
-------------------------------------------
AuthenticatedClient.get_httpx_client() automatically sets:
    self._headers[self.auth_header_name] = f"{self.prefix} {self.token}"

When we pass token="" and prefix="", this results in Authorization: " "
(a space), which is then overridden by the empty headers from Issue #1.

Workaround: We bypass the parent's header logic entirely by:
1. Not passing headers to super().__init__()
2. Creating our own httpx.Client with correct headers
3. Never calling super().get_httpx_client()

FUTURE IMPROVEMENTS:
====================
1. Regenerate the OpenAPI client with correct authentication configuration
2. Update the OpenAPI spec to include proper security schemes
3. Patch the openapi-python-client generator template to merge headers
   instead of replacing them
4. Consider using a different OpenAPI client generator

Last Updated: 2025-10-13
"""

from typing import Dict, Any, Optional
import httpx
from ..rest_api.public.client import AuthenticatedClient


class WatsHttpClient(AuthenticatedClient):
    """
    Custom HTTP client that uses Basic authentication instead of Bearer.
    """
    
    def __init__(self, base_url: str, token: str, **kwargs):
        """
        Initialize the HTTP client with Basic authentication.
        
        Args:
            base_url: The base URL for the WATS API
            token: The Basic authentication token (already base64 encoded)
        """
        # Strip any /api, /api/v1, /api/v2, /api/internal suffixes
        import re
        base_url = re.sub(r'/api(/v\d+|/internal)?/?$', '', base_url)
        
        # Create headers dict with Basic auth
        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Store the token for later use
        self._auth_token = token
        
        # Initialize parent WITHOUT headers (we'll set them ourselves)
        # Pass empty token to prevent parent from setting Authorization header
        super().__init__(base_url=base_url, token="", **kwargs)
        
        # Override prefix to empty to prevent any "Bearer " additions
        self.prefix = ""
        
        # Create our own httpx client with correct headers
        # DON'T call parent's get_httpx_client() as it will set Authorization incorrectly
        self._custom_httpx_client = httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=getattr(self, '_timeout', 30.0),
            verify=getattr(self, '_verify_ssl', True),
            follow_redirects=getattr(self, '_follow_redirects', False),
        )
        
        # Apply monkey-patch to inject authentication headers
        # (See module docstring for detailed explanation of why this is necessary)
        
        # Store the original request method
        _original_request = self._custom_httpx_client.request
        
        # Create the custom headers dict
        _custom_headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        def _patched_request(*args, **kwargs):
            """
            Intercept all HTTP requests and inject authentication headers.
            
            This patches the httpx.Client.request() method to ensure that our
            custom authentication headers (especially Authorization) are present
            in every request, even when the generated endpoint code passes empty
            headers that would normally override the client's default headers.
            """
            request_headers = kwargs.get('headers', {})
            
            # Convert to plain dict if needed (in case it's a Headers object)
            try:
                if hasattr(request_headers, 'items'):
                    request_headers_dict = dict(request_headers.items())
                elif isinstance(request_headers, dict):
                    request_headers_dict = request_headers
                else:
                    request_headers_dict = dict(request_headers) if request_headers else {}
            except (TypeError, ValueError):
                # If conversion fails, just use empty dict
                request_headers_dict = {}
            
            # Merge headers: start with our authentication headers,
            # then overlay any headers from the request
            merged_headers = {}
            merged_headers.update(_custom_headers)
            merged_headers.update(request_headers_dict)
            
            kwargs['headers'] = merged_headers
            return _original_request(*args, **kwargs)
        
        # Replace the request method ONCE during initialization
        self._custom_httpx_client.request = _patched_request
    
    def get_httpx_client(self) -> httpx.Client:
        """Override to return our custom httpx client with patched request method"""
        # The request method was already patched in __init__
        return self._custom_httpx_client
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, *args):
        """Context manager exit - close the httpx client"""
        if hasattr(self, '_custom_httpx_client'):
            self._custom_httpx_client.close()