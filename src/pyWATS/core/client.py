"""
HTTP Client for WATS API.

This module provides a clean HTTP client with Basic authentication
for communicating with the WATS server.
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass
import httpx
import json

from .exceptions import (
    AuthenticationError,
    NotFoundError,
    ServerError,
    ConnectionError,
    TimeoutError,
    PyWATSError
)


@dataclass
class Response:
    """HTTP Response wrapper."""
    status_code: int
    data: Any
    headers: Dict[str, str]
    raw: bytes

    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300

    @property
    def is_error(self) -> bool:
        return self.status_code >= 400


class HttpClient:
    """
    HTTP client with Basic authentication for WATS API.

    This client handles all HTTP communication with the WATS server,
    including authentication, request/response handling, and error management.
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 30.0,
        verify_ssl: bool = True
    ):
        """
        Initialize the HTTP client.

        Args:
            base_url: Base URL of the WATS server
            token: Base64 encoded authentication token for Basic auth
            timeout: Request timeout in seconds (default: 30)
            verify_ssl: Whether to verify SSL certificates (default: True)
        """
        # Clean up base URL - remove trailing slashes and /api suffixes
        self.base_url = base_url.rstrip("/")
        if self.base_url.endswith("/api"):
            self.base_url = self.base_url[:-4]

        self.token = token
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        # Default headers
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Create httpx client
        self._client: Optional[httpx.Client] = None

    @property
    def client(self) -> httpx.Client:
        """Get or create the httpx client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=self._headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
                follow_redirects=True
            )
        return self._client

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def _handle_response(self, response: httpx.Response) -> Response:
        """
        Handle HTTP response and convert to Response object.

        Args:
            response: The httpx response

        Returns:
            Response object with parsed data

        Raises:
            AuthenticationError: If authentication fails (401/403)
            NotFoundError: If resource not found (404)
            ServerError: If server returns an error (5xx)
        """
        # Try to parse JSON response
        data = None
        try:
            if response.content:
                data = response.json()
        except (json.JSONDecodeError, ValueError):
            data = response.text if response.text else None

        # Create response object
        result = Response(
            status_code=response.status_code,
            data=data,
            headers=dict(response.headers),
            raw=response.content
        )

        # Handle error status codes
        if response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed - invalid or expired token"
            )

        if response.status_code == 403:
            raise AuthenticationError(
                "Access forbidden - insufficient permissions"
            )

        if response.status_code == 404:
            msg = "Resource not found"
            if isinstance(data, dict):
                msg = data.get("message", msg)
            raise NotFoundError("Resource", "unknown", msg)

        if response.status_code >= 500:
            msg = "Server error"
            if isinstance(data, dict):
                msg = data.get("message", msg)
            raise ServerError(response.status_code, msg, response.text)

        return result

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Response:
        """
        Make an HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/api/Product/ABC123")
            params: Query parameters
            data: Request body data (will be JSON encoded)
            headers: Additional headers to merge with defaults

        Returns:
            Response object
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        # Merge headers
        request_headers = self._headers.copy()
        if headers:
            request_headers.update(headers)

        # Prepare request kwargs
        kwargs: Dict[str, Any] = {
            "method": method,
            "url": endpoint,
            "headers": request_headers
        }

        if params:
            # Filter out None values
            kwargs["params"] = {
                k: v for k, v in params.items() if v is not None
            }

        if data is not None:
            if isinstance(data, (dict, list)):
                kwargs["json"] = data
            else:
                kwargs["content"] = data

        try:
            response = self.client.request(**kwargs)
            return self._handle_response(response)
        except httpx.ConnectError as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {e}")
        except (AuthenticationError, NotFoundError, ServerError):
            raise
        except Exception as e:
            raise PyWATSError(f"HTTP request failed: {e}")

    # Convenience methods
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Response:
        """Make a GET request."""
        return self._make_request("GET", endpoint, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        data: Any = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Response:
        """Make a POST request."""
        return self._make_request(
            "POST", endpoint, data=data, params=params, **kwargs
        )

    def put(
        self,
        endpoint: str,
        data: Any = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Response:
        """Make a PUT request."""
        return self._make_request(
            "PUT", endpoint, data=data, params=params, **kwargs
        )

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Response:
        """Make a DELETE request."""
        return self._make_request("DELETE", endpoint, params=params, **kwargs)

    def patch(
        self,
        endpoint: str,
        data: Any = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Response:
        """Make a PATCH request."""
        return self._make_request(
            "PATCH", endpoint, data=data, params=params, **kwargs
        )
