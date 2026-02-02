"""
Async HTTP Client for WATS API.

This module provides an asynchronous HTTP client with Basic authentication
for communicating with the WATS server using httpx.AsyncClient.

Usage:
    async with AsyncHttpClient(base_url="...", token="...") as client:
        response = await client.get("/api/Product/ABC123")

For GUI applications using Qt/PySide6, use with qasync:
    from qasync import QEventLoop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
"""
from typing import Optional, Dict, Any, AsyncIterator, TYPE_CHECKING
from contextlib import asynccontextmanager
import asyncio
import time
import httpx
import json
import logging

from .exceptions import (
    ConnectionError,
    TimeoutError,
    PyWATSError,
    WatsApiError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ServerError,
)
from .throttle import RateLimiter, get_default_limiter
from .retry import RetryConfig, should_retry
from .client import Response  # Reuse the Response model
from .cache import AsyncTTLCache

if TYPE_CHECKING:
    from .metrics import MetricsCollector

logger = logging.getLogger(__name__)


class AsyncHttpClient:
    """
    Async HTTP client with Basic authentication for WATS API.

    This client handles all async HTTP communication with the WATS server,
    including authentication, request/response handling, and error management.
    
    Example:
        >>> async with AsyncHttpClient(base_url="https://wats.example.com", token="...") as client:
        ...     response = await client.get("/api/Product/ABC123")
        ...     print(response.data)
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 30.0,
        verify_ssl: bool = True,
        rate_limiter: Optional[RateLimiter] = None,
        enable_throttling: bool = True,
        retry_config: Optional[RetryConfig] = None,
        enable_cache: bool = True,
        cache_ttl: float = 300.0,
        cache_max_size: int = 1000,
        metrics_collector: Optional['MetricsCollector'] = None,
    ):
        """
        Initialize the async HTTP client.

        Args:
            base_url: Base URL of the WATS server
            token: Base64 encoded authentication token for Basic auth
            timeout: Request timeout in seconds (default: 30)
            verify_ssl: Whether to verify SSL certificates (default: True)
            rate_limiter: Custom RateLimiter instance (default: global limiter)
            enable_throttling: Enable/disable rate limiting (default: True)
            retry_config: Retry configuration (default: RetryConfig())
            enable_cache: Enable response caching for GET requests (default: True)
            cache_ttl: Cache TTL in seconds (default: 300 = 5 minutes)
            cache_max_size: Maximum cache entries (default: 1000)
            metrics_collector: Optional MetricsCollector for request tracking
        """
        # Clean up base URL
        self.base_url = base_url.rstrip("/")
        if self.base_url.endswith("/api"):
            self.base_url = self.base_url[:-4]

        self.token = token
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        
        # Rate limiter
        if rate_limiter is not None:
            self._rate_limiter = rate_limiter
        elif enable_throttling:
            self._rate_limiter = get_default_limiter()
        else:
            self._rate_limiter = RateLimiter(enabled=False)
        
        # Retry configuration
        self._retry_config = retry_config if retry_config is not None else RetryConfig()

        # Cache configuration
        self._cache_enabled = enable_cache
        self._cache: Optional[AsyncTTLCache[Response]] = None
        if enable_cache:
            self._cache = AsyncTTLCache[Response](
                default_ttl=cache_ttl,
                max_size=cache_max_size
            )
            logger.debug(f"Async HTTP cache enabled: TTL={cache_ttl}s, max_size={cache_max_size}")
        
        # Metrics collection
        self._metrics_collector = metrics_collector

        # Default headers
        self._headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Async httpx client (created on first use or via context manager)
        self._client: Optional[httpx.AsyncClient] = None

        # Trace capture stack
        self._trace_stack: list[list[dict[str, Any]]] = []

    @asynccontextmanager
    async def capture_traces(self) -> AsyncIterator[list[dict[str, Any]]]:
        """Capture HTTP request/response traces within this async context."""
        bucket: list[dict[str, Any]] = []
        self._trace_stack.append(bucket)
        try:
            yield bucket
        finally:
            if self._trace_stack and self._trace_stack[-1] is bucket:
                self._trace_stack.pop()

    def _emit_trace(self, trace: dict[str, Any]) -> None:
        """Append trace to all active capture buckets."""
        for bucket in self._trace_stack:
            bucket.append(trace)

    @staticmethod
    def _bounded_json(value: Any, *, max_chars: int = 10_000) -> Any:
        """Return a JSON-serializable structure, bounded for debug surfaces."""
        if value is None:
            return None
        if isinstance(value, (dict, list)):
            try:
                text = json.dumps(value, ensure_ascii=False, default=str)
            except Exception:
                return {"_unserializable": True, "type": type(value).__name__}
            if len(text) <= max_chars:
                return value
            return {"_truncated": True, "_original_chars": len(text), "_preview": text[:max_chars]}
        if isinstance(value, (bytes, bytearray)):
            size = len(value)
            if size <= max_chars:
                return value.decode("utf-8", errors="replace")
            return {"_truncated": True, "_original_bytes": size, "_preview": value[:max_chars].decode("utf-8", errors="replace")}
        if isinstance(value, str):
            if len(value) <= max_chars:
                return value
            return {"_truncated": True, "_original_chars": len(value), "_preview": value[:max_chars]}
        return value

    @property
    def rate_limiter(self) -> RateLimiter:
        """Get the rate limiter instance."""
        return self._rate_limiter

    @property
    def retry_config(self) -> RetryConfig:
        """Get the retry configuration instance."""
        return self._retry_config
    
    @retry_config.setter
    def retry_config(self, value: RetryConfig) -> None:
        """Set the retry configuration instance."""
        self._retry_config = value

    @property
    def cache(self) -> Optional[AsyncTTLCache[Response]]:
        """Get the async cache instance (if caching is enabled)."""
        return self._cache

    @property
    def cache_enabled(self) -> bool:
        """Check if caching is enabled."""
        return self._cache_enabled

    async def clear_cache(self) -> None:
        """Clear all cached responses."""
        if self._cache:
            await self._cache.clear()
            logger.debug("Async HTTP cache cleared")

    async def invalidate_cache(self, endpoint_pattern: Optional[str] = None) -> None:
        """
        Invalidate cached responses matching a pattern.
        
        Args:
            endpoint_pattern: Pattern to match (e.g., "/api/Product" invalidates all product endpoints)
                            If None, clears entire cache.
        """
        if not self._cache:
            return
            
        if endpoint_pattern is None:
            await self.clear_cache()
            return
            
        # Invalidate entries matching pattern
        keys_to_remove = [
            key for key in self._cache._cache.keys()
            if endpoint_pattern in key
        ]
        for key in keys_to_remove:
            await self._cache.delete(key)
        
        if keys_to_remove:
            logger.debug(f"Invalidated {len(keys_to_remove)} async cache entries matching '{endpoint_pattern}'")

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the async httpx client with connection pooling."""
        if self._client is None:
            # Configure connection pooling for better performance
            limits = httpx.Limits(
                max_connections=100,  # Total connection pool size
                max_keepalive_connections=20,  # Keep connections alive
                keepalive_expiry=30.0  # Keep-alive timeout in seconds
            )
            
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self._headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
                follow_redirects=True,
                limits=limits,  # Enable connection pooling
                http2=True  # Enable HTTP/2 for multiplexing
            )
        return self._client

    async def close(self) -> None:
        """Close the async HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> "AsyncHttpClient":
        await self._get_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    def _handle_response(self, response: httpx.Response) -> Response:
        """
        Handle HTTP response and convert to Response object.
        Does NOT raise exceptions - that's handled by the caller if needed.
        """
        data = None
        try:
            if response.content:
                data = response.json()
        except (json.JSONDecodeError, ValueError):
            data = response.text if response.text else None

        return Response(
            status_code=response.status_code,
            data=data,
            headers=dict(response.headers),
            raw=response.content
        )

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        retry: Optional[bool] = None
    ) -> Response:
        """
        Make an async HTTP request with automatic retry for transient failures.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/api/Product/ABC123")
            params: Query parameters
            data: Request body data (will be JSON encoded)
            headers: Additional headers to merge with defaults
            retry: Override retry behavior (True/False/None for default)

        Returns:
            Response object
        """
        retry_enabled = retry if retry is not None else self._retry_config.enabled
        max_attempts = self._retry_config.max_attempts if retry_enabled else 1
        
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        request_headers = self._headers.copy()
        if headers:
            request_headers.update(headers)

        kwargs: Dict[str, Any] = {
            "method": method,
            "url": endpoint,
            "headers": request_headers
        }

        if params:
            kwargs["params"] = {k: v for k, v in params.items() if v is not None}

        if data is not None:
            if isinstance(data, (dict, list)):
                kwargs["json"] = data
            else:
                kwargs["content"] = data

        full_url = f"{self.base_url}{endpoint}"
        
        last_exception: Optional[Exception] = None
        last_response: Optional[Response] = None
        
        # Track metrics if collector is available
        metrics_start_time = time.time() if self._metrics_collector else None
        final_status = 0
        
        client = await self._get_client()
        
        for attempt in range(max_attempts):
            # Rate limiting (sync for now - could be made async)
            self._rate_limiter.acquire()
            
            started = time.perf_counter()
            try:
                response = await client.request(**kwargs)
                duration_ms = (time.perf_counter() - started) * 1000.0
                final_status = response.status_code
                
                self._emit_trace({
                    "method": method,
                    "url": full_url,
                    "params": self._bounded_json(kwargs.get("params")),
                    "json": self._bounded_json(kwargs.get("json")),
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "response_bytes": len(response.content or b""),
                    "attempt": attempt + 1,
                })
                
                parsed_response = self._handle_response(response)
                
                # Check if we should retry this status code
                if retry_enabled and self._retry_config.should_retry_status(response.status_code):
                    should_retry_flag, delay = should_retry(
                        self._retry_config, method, attempt, response=parsed_response
                    )
                    if should_retry_flag:
                        self._retry_config._total_retries += 1
                        self._retry_config._total_retry_time += delay
                        logger.info(
                            f"Retry {attempt + 1}/{max_attempts} for {method} {endpoint} "
                            f"after {delay:.2f}s (HTTP {response.status_code})"
                        )
                        await asyncio.sleep(delay)
                        last_response = parsed_response
                        continue
                
                # Track successful completion
                if self._metrics_collector and metrics_start_time:
                    duration = time.time() - metrics_start_time
                    status_label = str(final_status)
                    self._metrics_collector.http_requests_total.labels(
                        method=method,
                        endpoint=endpoint,
                        status=status_label
                    ).inc()
                    self._metrics_collector.http_request_duration_seconds.labels(
                        method=method,
                        endpoint=endpoint
                    ).observe(duration)
                
                return parsed_response
                
            except httpx.ConnectError as e:
                last_exception = ConnectionError(
                    f"Failed to connect to {self.base_url}: {e}",
                    operation=f"{method} {endpoint}",
                    details={"url": self.base_url}
                )
                
                if retry_enabled:
                    should_retry_flag, delay = should_retry(
                        self._retry_config, method, attempt, exception=last_exception
                    )
                    if should_retry_flag:
                        self._retry_config._total_retries += 1
                        self._retry_config._total_retry_time += delay
                        logger.info(
                            f"Retry {attempt + 1}/{max_attempts} for {method} {endpoint} "
                            f"after {delay:.2f}s (ConnectionError)"
                        )
                        await asyncio.sleep(delay)
                        continue
                
                raise last_exception
                
            except httpx.TimeoutException as e:
                last_exception = TimeoutError(
                    f"Request timed out after {self.timeout}s: {e}",
                    operation=f"{method} {endpoint}",
                    details={"timeout": self.timeout, "endpoint": endpoint}
                )
                
                if retry_enabled:
                    should_retry_flag, delay = should_retry(
                        self._retry_config, method, attempt, exception=last_exception
                    )
                    if should_retry_flag:
                        self._retry_config._total_retries += 1
                        self._retry_config._total_retry_time += delay
                        logger.info(
                            f"Retry {attempt + 1}/{max_attempts} for {method} {endpoint} "
                            f"after {delay:.2f}s (TimeoutError)"
                        )
                        await asyncio.sleep(delay)
                        continue
                
                raise last_exception
                
            except Exception as e:
                raise PyWATSError(f"HTTP request failed: {e}")
        
        if last_exception:
            raise last_exception
        if last_response:
            return last_response
        
        raise PyWATSError("Unexpected state: no response or exception after retries")

    # Convenience methods
    def _make_cache_key(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a cache key for a request.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Cache key string
        """
        # Normalize endpoint
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        
        # Sort params for consistent keys
        params_str = ""
        if params:
            sorted_params = sorted(params.items())
            params_str = "&".join(f"{k}={v}" for k, v in sorted_params)
        
        return f"{method}:{endpoint}?{params_str}" if params_str else f"{method}:{endpoint}"

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Response:
        """
        Make an async GET request with automatic caching.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional arguments for _make_request
            
        Returns:
            Response object (from cache or fresh HTTP request)
            
        Note:
            Successful responses (2xx) are cached based on TTL configuration.
            Cache can be disabled per-request using cache=False in kwargs.
        """
        # Check if caching should be bypassed
        use_cache = kwargs.pop('cache', True) and self._cache_enabled
        
        if use_cache and self._cache:
            cache_key = self._make_cache_key("GET", endpoint, params)
            
            # Try cache hit
            cached_response = await self._cache.get(cache_key)
            if cached_response is not None:
                logger.debug(f"Async cache hit: {cache_key}")
                return cached_response
            
            # Cache miss - make request
            logger.debug(f"Async cache miss: {cache_key}")
            response = await self._make_request("GET", endpoint, params=params, **kwargs)
            
            # Cache successful responses
            if 200 <= response.status_code < 300:
                await self._cache.put(cache_key, response)
                logger.debug(f"Cached async response: {cache_key}")
            
            return response
        
        # Caching disabled - direct request
        return await self._make_request("GET", endpoint, params=params, **kwargs)

    async def post(
        self,
        endpoint: str,
        data: Any = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Response:
        """
        Make an async POST request with cache invalidation.
        
        Note:
            POST to an endpoint invalidates all cached entries for that endpoint prefix.
        """
        response = await self._make_request(
            "POST", endpoint, data=data, params=params, **kwargs
        )
        
        # Invalidate cache for this endpoint
        if self._cache:
            await self.invalidate_cache(endpoint)
        
        return response

    async def put(
        self,
        endpoint: str,
        data: Any = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Response:
        """
        Make an async PUT request with cache invalidation.
        
        Note:
            PUT to an endpoint invalidates all cached entries for that endpoint prefix.
        """
        response = await self._make_request(
            "PUT", endpoint, data=data, params=params, **kwargs
        )
        
        # Invalidate cache for this endpoint
        if self._cache:
            await self.invalidate_cache(endpoint)
        
        return response

    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Response:
        """
        Make an async DELETE request with cache invalidation.
        
        Note:
            DELETE to an endpoint invalidates all cached entries for that endpoint prefix.
        """
        response = await self._make_request("DELETE", endpoint, params=params, **kwargs)
        
        # Invalidate cache for this endpoint
        if self._cache:
            await self.invalidate_cache(endpoint)
        
        return response

    async def patch(
        self,
        endpoint: str,
        data: Any = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Response:
        """Make an async PATCH request."""
        return await self._make_request(
            "PATCH", endpoint, data=data, params=params, **kwargs
        )
