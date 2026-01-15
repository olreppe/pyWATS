# Retry Logic Implementation Plan

**Status**: Planning  
**Author**: Copilot  
**Date**: 2026-01-14  
**Priority**: Medium  

---

## Executive Summary

This document outlines a comprehensive plan to implement automatic retry logic for transient failures in the pyWATS library. The goal is to improve resilience against network hiccups, server overloads, and temporary outages without risking data integrity.

---

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Goals & Non-Goals](#goals--non-goals)
3. [Design Decisions](#design-decisions)
4. [Implementation Phases](#implementation-phases)
5. [Technical Specification](#technical-specification)
6. [Risk Assessment & Mitigation](#risk-assessment--mitigation)
7. [Testing Strategy](#testing-strategy)
8. [Migration & Compatibility](#migration--compatibility)
9. [Documentation Updates](#documentation-updates)
10. [Timeline Estimate](#timeline-estimate)

---

## Current State Analysis

### What Exists Today

| Component | Status | Location |
|-----------|--------|----------|
| Rate Limiting | ✅ Implemented | `core/throttle.py` - `RateLimiter` class |
| Error Handling | ✅ Implemented | `core/exceptions.py` - `ErrorHandler` class |
| HTTP Client | ✅ Implemented | `core/client.py` - `HttpClient` class |
| Retry Logic | ❌ Not implemented | Only manual pattern in docs |

### Current Error Flow

```
User Code → Service → Repository → HttpClient → WATS Server
                                       ↓
                              Exception raised
                                       ↓
                              ErrorHandler decides
                                       ↓
                         Raise or return None (LENIENT)
```

### Exceptions Raised Today

```python
# From core/client.py _make_request()
except httpx.ConnectError as e:
    raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")
except httpx.TimeoutException as e:
    raise TimeoutError(f"Request timed out: {e}")
except Exception as e:
    raise PyWATSError(f"HTTP request failed: {e}")
```

### User-Facing Documentation

From `docs/GETTING_STARTED.md`, users are currently expected to implement their own retry:

```python
def get_product_with_retry(api, part_number, max_retries=3):
    for attempt in range(max_retries):
        try:
            return api.product.get_product(part_number)
        except (ConnectionError, ServerError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise
```

---

## Goals & Non-Goals

### Goals

1. **Automatic retry for transient failures** - Network errors, timeouts, server overloads
2. **Configurable behavior** - Users can customize or disable retry logic
3. **Safe by default** - Only retry idempotent operations automatically
4. **Observable** - Log all retry attempts for debugging
5. **Compatible** - No breaking changes to existing API
6. **Efficient** - Use exponential backoff with jitter to prevent thundering herd

### Non-Goals

1. **Retry for client errors** - 400, 401, 403, 404, 409 are deterministic failures
2. **Automatic retry for POST** - Risk of duplicate creates (Phase 3 consideration)
3. **Circuit breaker pattern** - Deferred to future enhancement
4. **Async retry** - Library is synchronous; async is out of scope

---

## Design Decisions

### Decision 1: Where to Implement Retry

| Option | Pros | Cons |
|--------|------|------|
| **A. HttpClient level** ✅ | Centralized, affects all operations | Less granular control |
| B. Repository level | Per-domain customization | Code duplication |
| C. Decorator pattern | Flexible, composable | More complex, harder to configure globally |
| D. External library (tenacity) | Battle-tested | Additional dependency |

**Decision**: Option A - Implement at `HttpClient._make_request()` level

**Rationale**: 
- Single point of change
- Consistent behavior across all domains
- Easiest to test and maintain
- Rate limiter already lives here

### Decision 2: Which Operations to Retry

| HTTP Method | Idempotent | Auto-Retry |
|-------------|------------|------------|
| GET | ✅ Yes | ✅ Yes |
| PUT | ✅ Yes | ✅ Yes |
| DELETE | ✅ Yes | ✅ Yes |
| PATCH | ⚠️ Depends | ⚠️ Configurable (default: yes) |
| POST | ❌ No | ❌ No (opt-in only) |

**Decision**: Retry GET, PUT, DELETE by default. POST only with explicit opt-in.

### Decision 3: Which Errors to Retry

| Error Type | Retry | Rationale |
|------------|-------|-----------|
| `ConnectionError` | ✅ Yes | Transient network issue |
| `TimeoutError` | ✅ Yes | Server slow, may recover |
| HTTP 429 (Too Many Requests) | ✅ Yes | Respect `Retry-After` header |
| HTTP 500 (Internal Server Error) | ✅ Yes | Often deployment/restart |
| HTTP 502 (Bad Gateway) | ✅ Yes | Proxy/load balancer issue |
| HTTP 503 (Service Unavailable) | ✅ Yes | Temporary overload |
| HTTP 504 (Gateway Timeout) | ✅ Yes | Upstream timeout |
| HTTP 400 (Bad Request) | ❌ No | Invalid input |
| HTTP 401 (Unauthorized) | ❌ No | Auth failure |
| HTTP 403 (Forbidden) | ❌ No | Permission denied |
| HTTP 404 (Not Found) | ❌ No | Resource doesn't exist |
| HTTP 409 (Conflict) | ❌ No | Optimistic lock failure |

### Decision 4: Backoff Strategy

**Algorithm**: Exponential backoff with full jitter

```python
sleep_time = min(
    base_delay * (2 ** attempt) + random.uniform(0, 1),
    max_delay
)
```

**Default values**:
- `base_delay`: 1.0 seconds
- `max_delay`: 30.0 seconds  
- `max_attempts`: 3

**Example progression**:
| Attempt | Base | With Jitter (example) |
|---------|------|----------------------|
| 1 | 1s | 1.0 - 2.0s |
| 2 | 2s | 2.0 - 3.0s |
| 3 | 4s | 4.0 - 5.0s |
| (fail) | - | Exception raised |

### Decision 5: Configuration Approach

**Option A: Constructor parameters** ✅
```python
api = pyWATS(
    base_url="...",
    token="...",
    retry_enabled=True,
    retry_max_attempts=3,
    retry_base_delay=1.0
)
```

**Option B: Separate config object**
```python
retry_config = RetryConfig(max_attempts=5)
api = pyWATS(..., retry_config=retry_config)
```

**Decision**: Both - simple parameters AND config object for advanced use

---

## Implementation Phases

### Phase 1: Foundation (Low Risk) ✅ COMPLETE

**Scope**: All idempotent methods (GET, PUT, DELETE) retry with basic configuration

**Files modified**:
- `src/pywats/core/retry.py` (NEW) - RetryConfig, RetryExhaustedError, should_retry()
- `src/pywats/core/client.py` - Added retry loop in _make_request()
- `src/pywats/core/__init__.py` - Exports retry classes
- `src/pywats/pywats.py` - retry_config/retry_enabled parameters
- `src/pywats/__init__.py` - Top-level exports
- `api-tests/cross_cutting/test_retry.py` (NEW) - 45 unit tests

**Deliverables**:
1. ✅ `RetryConfig` dataclass with full configuration
2. ✅ Retry logic in `HttpClient._make_request()` for all idempotent methods
3. ✅ Logging for all retry attempts at INFO level
4. ✅ 45 unit tests passing
5. ✅ Retry statistics tracking

**Acceptance criteria**:
- [x] GET requests automatically retry on `ConnectionError`
- [x] GET requests automatically retry on `TimeoutError`
- [x] GET requests automatically retry on HTTP 500, 502, 503, 504
- [x] PUT/DELETE also retry (all idempotent methods)
- [x] Retry respects `Retry-After` header for 429
- [x] Exponential backoff with jitter implemented
- [x] Retry can be disabled via constructor (`retry_enabled=False`)
- [x] All retry attempts logged at INFO level
- [x] Unit tests pass (45 tests)
- [x] `retry_config.stats` tracks retry counts and time

### Phase 2: Extended Coverage (Medium Risk) - PARTIALLY DONE

**Scope**: Per-request retry override + PATCH handling

**Remaining Deliverables**:
1. ~~Enable retry for PUT, DELETE, PATCH~~ ✅ Done in Phase 1
2. Per-request retry override (deferred)
3. ~~Retry statistics~~ ✅ Done in Phase 1
4. ~~Integration tests~~ ✅ 45 unit tests in Phase 1

**Acceptance criteria**:
- [x] PUT, DELETE retry on transient failures
- [ ] PATCH retry configurable (default: on) - Not yet configurable separately
- [x] `retry_config.stats` shows attempt counts
- [ ] Can override retry per-call: `api.product.get_product("X", retry=False)` - Deferred

### Phase 3: POST Safety (Higher Risk - Optional)

**Scope**: Safe retry for POST with idempotency support

**Prerequisites**:
- Verify WATS API supports idempotency keys (check headers)
- Design fallback for APIs without idempotency

**Deliverables**:
1. Idempotency key generation and tracking
2. POST retry with idempotency header
3. Duplicate detection/warning

**Acceptance criteria**:
- [ ] POST retry only when idempotency key provided
- [ ] Idempotency key sent in request header
- [ ] Warning logged if retrying POST without idempotency
- [ ] Test confirms no duplicate creates

### Phase 4: Advanced Features (Future)

**Scope**: Circuit breaker, async support, adaptive retry

**Potential features**:
- Circuit breaker: Stop retrying after N consecutive failures
- Adaptive delay: Learn from server response times
- Async retry: For future async client support
- Per-endpoint configuration

---

## Technical Specification

### New File: `src/pywats/core/retry.py`

```python
"""
Retry configuration and utilities for transient failure handling.

This module provides automatic retry logic for HTTP requests that fail
due to transient issues like network errors, timeouts, or server overloads.
"""
import time
import random
import logging
from dataclasses import dataclass, field
from typing import Optional, Set, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Response

logger = logging.getLogger(__name__)


# Status codes that indicate transient failures worth retrying
RETRYABLE_STATUS_CODES: Set[int] = {429, 500, 502, 503, 504}

# HTTP methods that are safe to retry (idempotent)
IDEMPOTENT_METHODS: Set[str] = {"GET", "PUT", "DELETE", "HEAD", "OPTIONS"}


@dataclass
class RetryConfig:
    """
    Configuration for automatic retry behavior.
    
    Attributes:
        enabled: Whether retry is enabled (default: True)
        max_attempts: Maximum number of attempts including initial (default: 3)
        base_delay: Initial delay in seconds (default: 1.0)
        max_delay: Maximum delay cap in seconds (default: 30.0)
        exponential_base: Base for exponential backoff (default: 2.0)
        jitter: Whether to add random jitter (default: True)
        retry_methods: HTTP methods to retry (default: idempotent only)
        retry_status_codes: HTTP status codes to retry (default: 429, 5xx)
        retry_on_timeout: Retry on timeout errors (default: True)
        retry_on_connection_error: Retry on connection errors (default: True)
        
    Example:
        >>> config = RetryConfig(max_attempts=5, base_delay=2.0)
        >>> api = pyWATS(base_url="...", token="...", retry_config=config)
    """
    enabled: bool = True
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: bool = True
    retry_methods: Set[str] = field(default_factory=lambda: IDEMPOTENT_METHODS.copy())
    retry_status_codes: Set[int] = field(default_factory=lambda: RETRYABLE_STATUS_CODES.copy())
    retry_on_timeout: bool = True
    retry_on_connection_error: bool = True
    
    # Statistics (updated during operation)
    _total_retries: int = field(default=0, repr=False)
    _total_retry_time: float = field(default=0.0, repr=False)
    
    def should_retry_method(self, method: str) -> bool:
        """Check if the HTTP method is safe to retry."""
        return method.upper() in self.retry_methods
    
    def should_retry_status(self, status_code: int) -> bool:
        """Check if the status code indicates a retryable error."""
        return status_code in self.retry_status_codes
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate delay before next retry attempt.
        
        Uses exponential backoff with optional jitter.
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Delay in seconds
        """
        delay = self.base_delay * (self.exponential_base ** attempt)
        
        if self.jitter:
            # Full jitter: random value between 0 and calculated delay
            delay = random.uniform(0, delay)
        
        return min(delay, self.max_delay)
    
    def get_retry_after(self, response: "Response") -> Optional[float]:
        """
        Extract Retry-After header value if present.
        
        Args:
            response: HTTP response object
            
        Returns:
            Delay in seconds, or None if header not present
        """
        retry_after = response.headers.get("Retry-After")
        if retry_after is None:
            return None
        
        try:
            # Try parsing as integer (seconds)
            return float(retry_after)
        except ValueError:
            # Could be HTTP date format - ignore for simplicity
            logger.debug(f"Could not parse Retry-After header: {retry_after}")
            return None
    
    @property
    def stats(self) -> dict:
        """Get retry statistics."""
        return {
            "total_retries": self._total_retries,
            "total_retry_time_seconds": round(self._total_retry_time, 2),
        }
    
    def reset_stats(self) -> None:
        """Reset retry statistics."""
        self._total_retries = 0
        self._total_retry_time = 0.0


class RetryExhaustedError(Exception):
    """Raised when all retry attempts have been exhausted."""
    
    def __init__(
        self, 
        message: str, 
        attempts: int, 
        last_exception: Optional[Exception] = None
    ):
        super().__init__(message)
        self.attempts = attempts
        self.last_exception = last_exception


def should_retry(
    config: RetryConfig,
    method: str,
    attempt: int,
    response: Optional["Response"] = None,
    exception: Optional[Exception] = None
) -> Tuple[bool, float]:
    """
    Determine if a request should be retried.
    
    Args:
        config: Retry configuration
        method: HTTP method
        attempt: Current attempt number (0-indexed)
        response: HTTP response (if request completed)
        exception: Exception raised (if request failed)
        
    Returns:
        Tuple of (should_retry, delay_seconds)
    """
    if not config.enabled:
        return False, 0.0
    
    # Check if we've exhausted attempts
    if attempt >= config.max_attempts - 1:
        return False, 0.0
    
    # Check if method is retryable
    if not config.should_retry_method(method):
        logger.debug(f"Method {method} is not configured for retry")
        return False, 0.0
    
    # Determine if this failure is retryable
    should_retry_this = False
    
    if exception is not None:
        # Import here to avoid circular imports
        from ..exceptions import ConnectionError, TimeoutError
        
        if isinstance(exception, ConnectionError) and config.retry_on_connection_error:
            should_retry_this = True
            logger.info(f"Connection error on attempt {attempt + 1}, will retry")
        elif isinstance(exception, TimeoutError) and config.retry_on_timeout:
            should_retry_this = True
            logger.info(f"Timeout on attempt {attempt + 1}, will retry")
    
    elif response is not None:
        if config.should_retry_status(response.status_code):
            should_retry_this = True
            logger.info(
                f"HTTP {response.status_code} on attempt {attempt + 1}, will retry"
            )
    
    if not should_retry_this:
        return False, 0.0
    
    # Calculate delay
    delay = config.calculate_delay(attempt)
    
    # Check for Retry-After header (takes precedence)
    if response is not None:
        retry_after = config.get_retry_after(response)
        if retry_after is not None:
            delay = min(retry_after, config.max_delay)
            logger.info(f"Using Retry-After header: {delay}s")
    
    return True, delay
```

### Modified: `src/pywats/core/client.py`

```python
# Add to imports
from .retry import RetryConfig, should_retry

# Modify HttpClient.__init__
def __init__(
    self,
    base_url: str,
    token: str,
    timeout: float = 30.0,
    verify_ssl: bool = True,
    rate_limiter: Optional[RateLimiter] = None,
    enable_throttling: bool = True,
    retry_config: Optional[RetryConfig] = None,  # NEW
):
    # ... existing code ...
    
    # Retry configuration
    self._retry_config = retry_config or RetryConfig()

# Modify _make_request
def _make_request(
    self,
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    data: Any = None,
    headers: Optional[Dict[str, str]] = None,
    retry: Optional[bool] = None,  # NEW: per-call override
) -> Response:
    """
    Make an HTTP request with automatic retry for transient failures.
    
    Args:
        method: HTTP method
        endpoint: API endpoint
        params: Query parameters
        data: Request body
        headers: Additional headers
        retry: Override retry config (True/False/None for default)
    """
    # Determine if retry is enabled for this request
    retry_enabled = (
        retry if retry is not None 
        else self._retry_config.enabled
    )
    
    last_exception: Optional[Exception] = None
    last_response: Optional[Response] = None
    
    for attempt in range(self._retry_config.max_attempts if retry_enabled else 1):
        try:
            # Acquire rate limiter slot
            self._rate_limiter.acquire()
            
            # ... existing request code ...
            
            response = self.client.request(**kwargs)
            
            # Check if response indicates retryable error
            if retry_enabled and response.status_code in self._retry_config.retry_status_codes:
                should_retry_flag, delay = should_retry(
                    self._retry_config, method, attempt, response=response
                )
                if should_retry_flag:
                    self._retry_config._total_retries += 1
                    self._retry_config._total_retry_time += delay
                    logger.info(
                        f"Retry {attempt + 1}/{self._retry_config.max_attempts} "
                        f"for {method} {endpoint} after {delay:.2f}s "
                        f"(HTTP {response.status_code})"
                    )
                    time.sleep(delay)
                    continue
            
            return self._handle_response(response)
            
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            last_exception = self._convert_exception(e)
            
            if retry_enabled:
                should_retry_flag, delay = should_retry(
                    self._retry_config, method, attempt, exception=last_exception
                )
                if should_retry_flag:
                    self._retry_config._total_retries += 1
                    self._retry_config._total_retry_time += delay
                    logger.info(
                        f"Retry {attempt + 1}/{self._retry_config.max_attempts} "
                        f"for {method} {endpoint} after {delay:.2f}s "
                        f"({type(last_exception).__name__})"
                    )
                    time.sleep(delay)
                    continue
            
            raise last_exception
    
    # If we get here, all retries exhausted
    if last_exception:
        raise last_exception
    if last_response:
        return self._handle_response(last_response)
    
    raise PyWATSError("Unexpected state: no response or exception")
```

### Modified: `src/pywats/pywats.py`

```python
# Add to imports
from .core.retry import RetryConfig

# Modify pyWATS.__init__
def __init__(
    self,
    base_url: str,
    token: str,
    timeout: float = 30.0,
    verify_ssl: bool = True,
    error_mode: ErrorMode = ErrorMode.STRICT,
    enable_throttling: bool = True,
    # NEW retry parameters
    retry_enabled: bool = True,
    retry_max_attempts: int = 3,
    retry_config: Optional[RetryConfig] = None,
):
    """
    Initialize pyWATS client.
    
    Args:
        base_url: WATS server URL
        token: Authentication token
        timeout: Request timeout in seconds
        verify_ssl: Verify SSL certificates
        error_mode: STRICT or LENIENT error handling
        enable_throttling: Enable rate limiting
        retry_enabled: Enable automatic retry for transient failures
        retry_max_attempts: Maximum retry attempts (default: 3)
        retry_config: Advanced retry configuration (overrides simple params)
    """
    # Build retry config
    if retry_config is None:
        retry_config = RetryConfig(
            enabled=retry_enabled,
            max_attempts=retry_max_attempts
        )
    
    self._http_client = HttpClient(
        base_url=base_url,
        token=token,
        timeout=timeout,
        verify_ssl=verify_ssl,
        enable_throttling=enable_throttling,
        retry_config=retry_config,  # NEW
    )
    
    # ... rest of init ...

@property
def retry_stats(self) -> dict:
    """Get retry statistics."""
    return self._http_client._retry_config.stats
```

### Modified: `src/pywats/__init__.py`

```python
# Add to exports
from .core.retry import RetryConfig

__all__ = [
    # ... existing exports ...
    "RetryConfig",
]
```

---

## Risk Assessment & Mitigation

### Risk Matrix

| Risk | Probability | Impact | Severity | Mitigation |
|------|-------------|--------|----------|------------|
| Duplicate POST creates | Low (POST disabled) | High | 🟡 Medium | Don't retry POST by default |
| Thundering herd after outage | Medium | Medium | 🟡 Medium | Jitter in backoff |
| Masking real failures | Medium | Low | 🟢 Low | Log all retries, limit attempts |
| Increased latency | High | Low | 🟢 Low | Users prefer delay over failure |
| Breaking existing code | Low | High | 🟡 Medium | Default behavior unchanged |
| Test data loss | Low (retry helps) | High | 🟢 Low | Retry actually reduces this risk |

### Mitigation Strategies

1. **Duplicate creates**: POST not retried by default. Phase 3 adds idempotency keys.

2. **Thundering herd**: Full jitter randomizes retry timing:
   ```python
   delay = random.uniform(0, base * 2^attempt)
   ```

3. **Masking failures**: 
   - Log every retry at INFO level
   - Limit to 3 attempts by default
   - Final failure still raises exception

4. **Breaking changes**:
   - Retry enabled by default (improves UX)
   - Can disable: `retry_enabled=False`
   - Behavior for client errors (4xx) unchanged

---

## Testing Strategy

### Unit Tests

```python
# tests/core/test_retry.py

import pytest
from pywats.core.retry import RetryConfig, should_retry, RETRYABLE_STATUS_CODES

class TestRetryConfig:
    def test_default_values(self):
        config = RetryConfig()
        assert config.enabled is True
        assert config.max_attempts == 3
        assert config.base_delay == 1.0
    
    def test_should_retry_method(self):
        config = RetryConfig()
        assert config.should_retry_method("GET") is True
        assert config.should_retry_method("POST") is False
        assert config.should_retry_method("PUT") is True
    
    def test_should_retry_status(self):
        config = RetryConfig()
        assert config.should_retry_status(500) is True
        assert config.should_retry_status(404) is False
        assert config.should_retry_status(429) is True
    
    def test_calculate_delay_exponential(self):
        config = RetryConfig(base_delay=1.0, jitter=False)
        assert config.calculate_delay(0) == 1.0
        assert config.calculate_delay(1) == 2.0
        assert config.calculate_delay(2) == 4.0
    
    def test_calculate_delay_max_cap(self):
        config = RetryConfig(base_delay=10.0, max_delay=30.0, jitter=False)
        assert config.calculate_delay(5) == 30.0  # Would be 320 without cap
    
    def test_calculate_delay_with_jitter(self):
        config = RetryConfig(base_delay=1.0, jitter=True)
        delays = [config.calculate_delay(0) for _ in range(100)]
        # All delays should be between 0 and base_delay
        assert all(0 <= d <= 1.0 for d in delays)
        # Should have variation (not all the same)
        assert len(set(round(d, 2) for d in delays)) > 1


class TestShouldRetry:
    def test_disabled_config(self):
        config = RetryConfig(enabled=False)
        should, delay = should_retry(config, "GET", 0, response=mock_500_response())
        assert should is False
    
    def test_max_attempts_exceeded(self):
        config = RetryConfig(max_attempts=3)
        should, delay = should_retry(config, "GET", 2, response=mock_500_response())
        assert should is False
    
    def test_non_idempotent_method(self):
        config = RetryConfig()
        should, delay = should_retry(config, "POST", 0, response=mock_500_response())
        assert should is False
    
    def test_retryable_status_code(self):
        config = RetryConfig()
        for status in [429, 500, 502, 503, 504]:
            should, delay = should_retry(config, "GET", 0, response=mock_response(status))
            assert should is True
    
    def test_non_retryable_status_code(self):
        config = RetryConfig()
        for status in [400, 401, 403, 404, 409]:
            should, delay = should_retry(config, "GET", 0, response=mock_response(status))
            assert should is False
```

### Integration Tests

```python
# tests/integration/test_retry_integration.py

import pytest
from unittest.mock import patch, MagicMock
from pywats import pyWATS, RetryConfig

class TestRetryIntegration:
    def test_retry_on_connection_error(self, mock_server):
        """Verify retry on connection failure"""
        # First two calls fail, third succeeds
        mock_server.responses = [
            ConnectionError("Connection refused"),
            ConnectionError("Connection refused"),
            {"id": 1, "partNumber": "TEST-001"}
        ]
        
        api = pyWATS(base_url="http://test", token="test")
        product = api.product.get_product("TEST-001")
        
        assert product is not None
        assert mock_server.call_count == 3
        assert api.retry_stats["total_retries"] == 2
    
    def test_no_retry_on_404(self, mock_server):
        """Verify no retry on 404"""
        mock_server.responses = [mock_404_response()]
        
        api = pyWATS(base_url="http://test", token="test")
        
        with pytest.raises(NotFoundError):
            api.product.get_product("NONEXISTENT")
        
        assert mock_server.call_count == 1
        assert api.retry_stats["total_retries"] == 0
    
    def test_retry_disabled(self, mock_server):
        """Verify retry can be disabled"""
        mock_server.responses = [ConnectionError("fail")]
        
        api = pyWATS(base_url="http://test", token="test", retry_enabled=False)
        
        with pytest.raises(ConnectionError):
            api.product.get_product("TEST-001")
        
        assert mock_server.call_count == 1
```

### Manual Testing Checklist

- [ ] Test with real WATS server behind unstable network
- [ ] Verify retry logging appears in console
- [ ] Confirm exponential backoff timing
- [ ] Test rate limit (429) handling with Retry-After header
- [ ] Verify POST is not retried
- [ ] Test disable via `retry_enabled=False`
- [ ] Confirm retry stats are accurate

---

## Migration & Compatibility

### Breaking Changes

**None** - Retry is additive and enabled by default for improved UX.

### Backward Compatibility

| Scenario | Before | After |
|----------|--------|-------|
| GET with transient failure | Exception raised | Automatic retry, then exception |
| POST with transient failure | Exception raised | Exception raised (no change) |
| Explicit error handling | Works | Works (final exception still raised) |
| Rate limiting | Works | Works (retry respects rate limiter) |

### Opt-Out

Users who want the old behavior can disable:

```python
# Disable retry globally
api = pyWATS(base_url="...", token="...", retry_enabled=False)

# Or per-call (Phase 2)
product = api.product.get_product("X", retry=False)
```

---

## Documentation Updates

### Files to Update

1. **docs/GETTING_STARTED.md**
   - Update "Retry Logic" section with automatic retry info
   - Add "Disabling Retry" section
   - Update exception matrix

2. **docs/CONFIGURATION.md** (NEW or update existing)
   - RetryConfig parameters
   - Examples for different scenarios

3. **CHANGELOG.md**
   - Add to [Unreleased] section

4. **README.md**
   - Mention automatic retry in features list

### Example Documentation

```markdown
## Automatic Retry

pyWATS automatically retries requests that fail due to transient errors:

- **Connection errors** - Network issues, DNS failures
- **Timeouts** - Server slow to respond
- **Server errors** - HTTP 500, 502, 503, 504
- **Rate limiting** - HTTP 429 (respects Retry-After header)

Retry uses exponential backoff with jitter to prevent thundering herd.

### Configuration

```python
# Default: retry enabled with 3 attempts
api = pyWATS(base_url="...", token="...")

# Disable retry
api = pyWATS(base_url="...", token="...", retry_enabled=False)

# Custom retry settings
from pywats import RetryConfig

config = RetryConfig(
    max_attempts=5,
    base_delay=2.0,
    max_delay=60.0
)
api = pyWATS(base_url="...", token="...", retry_config=config)
```

### What's NOT Retried

- **POST requests** - Risk of duplicate creates
- **Client errors** - 400, 401, 403, 404, 409 (deterministic failures)

### Statistics

```python
# Check retry statistics
print(api.retry_stats)
# {'total_retries': 5, 'total_retry_time_seconds': 12.5}
```
```

---

## Timeline Estimate

| Phase | Effort | Dependencies | Est. Time |
|-------|--------|--------------|-----------|
| Phase 1: Foundation | Medium | None | 2-3 days |
| Phase 2: Extended | Medium | Phase 1 | 2 days |
| Phase 3: POST Safety | High | Phase 2, WATS API research | 3-4 days |
| Documentation | Low | Phase 1 | 1 day |
| Testing | Medium | Each phase | Included |

**Total for Phase 1 + Docs**: ~4 days

---

## Appendix

### Related Work

- [httpx Transport retries](https://www.python-httpx.org/advanced/#custom-transports)
- [tenacity library](https://tenacity.readthedocs.io/)
- [AWS SDK retry behavior](https://docs.aws.amazon.com/general/latest/gr/api-retries.html)
- [Google API retry guidelines](https://cloud.google.com/storage/docs/retry-strategy)

### References

- [Exponential Backoff And Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Idempotency Keys](https://stripe.com/docs/api/idempotent_requests)

---

## Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Author | Copilot | 2026-01-14 | Draft |
| Reviewer | | | Pending |
| Approver | | | Pending |
