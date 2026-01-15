# Async API Implementation Plan

> **Status**: 📋 PLANNED  
> **Priority**: HIGH  
> **Estimated Effort**: 2-3 weeks  
> **Target Version**: 0.2.0

---

## Overview

Modern Python applications increasingly use `async/await` for concurrent I/O operations. This plan outlines adding async support to pyWATS while maintaining full backward compatibility with the synchronous API.

---

## Current State

| Component | Current | Target |
|-----------|---------|--------|
| HTTP Client | `httpx.Client` (sync) | `httpx.AsyncClient` (async) |
| API Methods | Synchronous only | Sync + Async |
| Connection | New per request | Connection pooling |
| Batch Operations | Sequential | Concurrent with `asyncio.gather()` |

---

## Goals

### Must Have
- [ ] Async versions of all public API methods
- [ ] Full feature parity with sync API
- [ ] Connection pooling for better performance
- [ ] Backward compatible (sync API unchanged)
- [ ] Concurrent batch operations

### Nice to Have
- [ ] Async context managers
- [ ] Async iterators for pagination
- [ ] WebSocket support for real-time events
- [ ] Streaming responses for large data

### Out of Scope (This Phase)
- Reactive streams (RxPy)
- Trio/anyio support (asyncio only)
- Automatic sync→async migration tool

---

## Design Decisions

### Decision 1: API Surface Design

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A. Separate AsyncPyWATS class** | `AsyncPyWATS` with async methods | Clear separation | Code duplication |
| **B. Dual methods** | `get_product()` + `get_product_async()` | Single class | Cluttered API |
| **C. Mode flag** | `pyWATS(async_mode=True)` | Flexible | Confusing types |
| **D. Async-first with sync wrapper** ✅ | Internal async, sync methods wrap | DRY, modern | Complexity |

**Decision**: Option D - Async-first with sync wrapper

**Rationale**:
- httpx already supports both sync and async
- Avoids code duplication
- Modern pattern used by major libraries (httpx, aiohttp wrappers)
- Internal implementation is async; sync methods use `asyncio.run()` or similar

### Decision 2: Import Structure

```python
# Option A: Submodule
from pywats.async_api import AsyncPyWATS

# Option B: Top-level with prefix ✅
from pywats import AsyncPyWATS

# Option C: Same class, different methods
from pywats import pyWATS
api = pyWATS(...)
await api.product.get_product_async("X")
```

**Decision**: Option B - Top-level export of `AsyncPyWATS`

### Decision 3: Concurrent Execution Strategy

```python
# For batch operations
async def get_products_batch(self, part_numbers: list[str]) -> list[Product]:
    tasks = [self.get_product(pn) for pn in part_numbers]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

**Decision**: Use `asyncio.gather()` with `return_exceptions=True` for resilient batch operations.

---

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1)

**Scope**: Async HTTP client and base classes

**Files to create/modify**:
- `src/pywats/core/async_client.py` (NEW)
- `src/pywats/async_api.py` (NEW)
- `src/pywats/__init__.py` (export AsyncPyWATS)

**Deliverables**:
1. `AsyncHttpClient` class using `httpx.AsyncClient`
2. `AsyncPyWATS` base class with lifecycle management
3. Async context manager support
4. Connection pooling configuration

**Code Structure**:
```python
# src/pywats/core/async_client.py
class AsyncHttpClient:
    def __init__(self, base_url: str, token: str, ...):
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self) -> "AsyncHttpClient":
        self._client = httpx.AsyncClient(...)
        return self
    
    async def __aexit__(self, *args) -> None:
        await self._client.aclose()
    
    async def get(self, endpoint: str, **kwargs) -> Response:
        ...
    
    async def post(self, endpoint: str, data: Any, **kwargs) -> Response:
        ...
```

**Acceptance Criteria**:
- [ ] `AsyncHttpClient` connects to WATS server
- [ ] Basic GET/POST/PUT/DELETE async methods work
- [ ] Context manager properly opens/closes connections
- [ ] Rate limiting works with async (thread-safe)
- [ ] Retry logic works with async

### Phase 2: Domain Services (Week 1-2)

**Scope**: Async versions of all domain services

**Files to create**:
- `src/pywats/domains/product/async_service.py`
- `src/pywats/domains/asset/async_service.py`
- `src/pywats/domains/production/async_service.py`
- `src/pywats/domains/report/async_service.py`
- `src/pywats/domains/analytics/async_service.py`
- `src/pywats/domains/rootcause/async_service.py`
- `src/pywats/domains/software/async_service.py`
- `src/pywats/domains/scim/async_service.py`
- `src/pywats/domains/process/async_service.py`

**Pattern**:
```python
# src/pywats/domains/product/async_service.py
class AsyncProductService:
    def __init__(self, client: AsyncHttpClient, error_handler: ErrorHandler):
        self._client = client
        self._error_handler = error_handler
    
    async def get_product(self, part_number: str) -> Optional[Product]:
        response = await self._client.get(f"/api/Product/{part_number}")
        return self._handle_response(response, Product)
    
    async def get_products(self) -> list[Product]:
        response = await self._client.get("/api/Product")
        return self._handle_list_response(response, Product)
```

**Acceptance Criteria**:
- [ ] All domain services have async equivalents
- [ ] Feature parity with sync services
- [ ] Proper error handling
- [ ] Type hints complete

### Phase 3: Concurrent Operations (Week 2)

**Scope**: Batch operations using `asyncio.gather()`

**New Methods**:
```python
class AsyncProductService:
    async def get_products_batch(
        self, 
        part_numbers: list[str],
        max_concurrent: int = 10
    ) -> list[Result[Product]]:
        """Fetch multiple products concurrently."""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def fetch_one(pn: str) -> Result[Product]:
            async with semaphore:
                try:
                    product = await self.get_product(pn)
                    return Success(product)
                except Exception as e:
                    return Failure(e)
        
        tasks = [fetch_one(pn) for pn in part_numbers]
        return await asyncio.gather(*tasks)
```

**Acceptance Criteria**:
- [ ] Concurrent fetch with semaphore limiting
- [ ] Results preserve order
- [ ] Individual failures don't break batch
- [ ] Configurable concurrency limit

### Phase 4: Async Iterators (Week 2-3)

**Scope**: Async iteration for paginated results

**New Pattern**:
```python
class AsyncReportService:
    async def iter_uut_headers(
        self, 
        filter: WATSFilter,
        page_size: int = 100
    ) -> AsyncIterator[ReportHeader]:
        """Async iterate over all matching headers."""
        offset = 0
        while True:
            page = await self.query_uut_headers(
                filter, 
                start=offset, 
                count=page_size
            )
            if not page:
                break
            for header in page:
                yield header
            offset += len(page)
            if len(page) < page_size:
                break
```

**Usage**:
```python
async for header in api.report.iter_uut_headers(filter):
    await process(header)
```

**Acceptance Criteria**:
- [ ] Async generators for all paginated endpoints
- [ ] Memory-efficient (doesn't load all pages at once)
- [ ] Early termination support (break works)
- [ ] Proper cleanup on exception

### Phase 5: Testing & Documentation (Week 3)

**Scope**: Comprehensive async tests and documentation

**Test Files**:
- `api-tests/async/test_async_client.py`
- `api-tests/async/test_async_product.py`
- `api-tests/async/test_async_batch.py`
- `api-tests/async/test_async_pagination.py`

**Documentation Updates**:
- `docs/ASYNC.md` (NEW)
- `docs/GETTING_STARTED.md` (add async section)
- `README.md` (add async examples)

**Acceptance Criteria**:
- [ ] All async methods have tests
- [ ] Integration tests pass
- [ ] Documentation complete
- [ ] Examples work

---

## Technical Specification

### AsyncPyWATS Class

```python
# src/pywats/async_api.py
from typing import Optional
from .core.async_client import AsyncHttpClient
from .core.retry import RetryConfig
from .core.station import Station
from .domains.product.async_service import AsyncProductService
# ... other imports

class AsyncPyWATS:
    """
    Async Python API for WATS.
    
    Example:
        >>> async with AsyncPyWATS(base_url="...", token="...") as api:
        ...     products = await api.product.get_products()
        ...     
        ...     # Concurrent batch fetch
        ...     results = await api.product.get_products_batch(
        ...         ["PART-1", "PART-2", "PART-3"]
        ...     )
    """
    
    def __init__(
        self,
        base_url: str,
        token: str,
        station: Optional[Station] = None,
        timeout: int = 30,
        retry_config: Optional[RetryConfig] = None,
        retry_enabled: bool = True,
        max_connections: int = 100,
        max_keepalive_connections: int = 20,
    ):
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout = timeout
        self._station = station
        self._max_connections = max_connections
        self._max_keepalive = max_keepalive_connections
        
        # Retry configuration
        if retry_config is not None:
            self._retry_config = retry_config
        elif not retry_enabled:
            self._retry_config = RetryConfig(enabled=False)
        else:
            self._retry_config = RetryConfig()
        
        # Client (created on __aenter__)
        self._client: Optional[AsyncHttpClient] = None
        
        # Services (lazy)
        self._product: Optional[AsyncProductService] = None
        # ... other services
    
    async def __aenter__(self) -> "AsyncPyWATS":
        """Enter async context - opens connection pool."""
        self._client = AsyncHttpClient(
            base_url=self._base_url,
            token=self._token,
            timeout=self._timeout,
            retry_config=self._retry_config,
            limits=httpx.Limits(
                max_connections=self._max_connections,
                max_keepalive_connections=self._max_keepalive,
            ),
        )
        await self._client.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context - closes connection pool."""
        if self._client:
            await self._client.close()
            self._client = None
    
    @property
    def product(self) -> AsyncProductService:
        """Access async product operations."""
        if self._product is None:
            self._product = AsyncProductService(self._client, self._error_handler)
        return self._product
    
    # ... other service properties
```

### AsyncHttpClient Class

```python
# src/pywats/core/async_client.py
import httpx
import asyncio
from typing import Any, Optional, Dict
from .retry import RetryConfig, should_retry
from .throttle import RateLimiter

class AsyncHttpClient:
    """Async HTTP client with retry, rate limiting, and connection pooling."""
    
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 30.0,
        retry_config: Optional[RetryConfig] = None,
        limits: Optional[httpx.Limits] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self._retry_config = retry_config or RetryConfig()
        self._limits = limits or httpx.Limits(
            max_connections=100,
            max_keepalive_connections=20,
        )
        self._client: Optional[httpx.AsyncClient] = None
        self._rate_limiter = RateLimiter()  # Thread-safe, works with async
    
    async def connect(self) -> None:
        """Open the connection pool."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Basic {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=self.timeout,
            limits=self._limits,
        )
    
    async def close(self) -> None:
        """Close the connection pool."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Any = None,
    ) -> Response:
        """Make async HTTP request with retry logic."""
        last_exception = None
        
        for attempt in range(self._retry_config.max_attempts):
            try:
                # Rate limiting (sync operation, but thread-safe)
                self._rate_limiter.acquire()
                
                # Make request
                response = await self._client.request(
                    method=method,
                    url=endpoint,
                    params=params,
                    json=data,
                )
                
                # Check for retryable status
                should_retry_flag, delay = should_retry(
                    self._retry_config, method, attempt, response=response
                )
                if should_retry_flag:
                    await asyncio.sleep(delay)
                    continue
                
                return self._handle_response(response)
                
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exception = e
                should_retry_flag, delay = should_retry(
                    self._retry_config, method, attempt, exception=e
                )
                if should_retry_flag:
                    await asyncio.sleep(delay)
                    continue
                raise
        
        if last_exception:
            raise last_exception
    
    async def get(self, endpoint: str, **kwargs) -> Response:
        return await self._make_request("GET", endpoint, **kwargs)
    
    async def post(self, endpoint: str, data: Any = None, **kwargs) -> Response:
        return await self._make_request("POST", endpoint, data=data, **kwargs)
    
    async def put(self, endpoint: str, data: Any = None, **kwargs) -> Response:
        return await self._make_request("PUT", endpoint, data=data, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> Response:
        return await self._make_request("DELETE", endpoint, **kwargs)
```

---

## Usage Examples

### Basic Async Usage

```python
import asyncio
from pywats import AsyncPyWATS

async def main():
    async with AsyncPyWATS(
        base_url="https://your-wats.com",
        token="your_token"
    ) as api:
        # Single operations
        product = await api.product.get_product("WIDGET-001")
        print(f"Product: {product.description}")
        
        # Concurrent batch
        part_numbers = ["PART-1", "PART-2", "PART-3", "PART-4"]
        products = await api.product.get_products_batch(part_numbers)
        for result in products:
            if result.is_success:
                print(f"Found: {result.value.part_number}")
            else:
                print(f"Failed: {result.error}")

asyncio.run(main())
```

### Async Iteration

```python
import asyncio
from pywats import AsyncPyWATS, WATSFilter

async def process_all_reports():
    async with AsyncPyWATS(base_url="...", token="...") as api:
        filter = WATSFilter(part_number="WIDGET-001", period_count=30)
        
        count = 0
        async for header in api.report.iter_uut_headers(filter):
            print(f"Processing: {header.serial_number}")
            count += 1
        
        print(f"Processed {count} reports")

asyncio.run(process_all_reports())
```

### Mixed Sync/Async

```python
from pywats import pyWATS, AsyncPyWATS

# Sync for simple scripts
def sync_example():
    api = pyWATS(base_url="...", token="...")
    product = api.product.get_product("WIDGET-001")
    return product

# Async for high-performance apps
async def async_example():
    async with AsyncPyWATS(base_url="...", token="...") as api:
        products = await api.product.get_products_batch(
            ["P1", "P2", "P3", "P4", "P5"],
            max_concurrent=5
        )
        return products
```

---

## Testing Strategy

### Unit Tests

```python
# api-tests/async/test_async_client.py
import pytest
import asyncio
from pywats import AsyncPyWATS

@pytest.mark.asyncio
async def test_async_context_manager():
    """Test async context manager opens/closes properly."""
    async with AsyncPyWATS(base_url="...", token="...") as api:
        assert api._client is not None
    assert api._client is None

@pytest.mark.asyncio
async def test_async_get_product():
    """Test async get_product."""
    async with AsyncPyWATS(base_url="...", token="...") as api:
        product = await api.product.get_product("TEST-001")
        assert product is not None

@pytest.mark.asyncio
async def test_batch_concurrent():
    """Test batch operations run concurrently."""
    async with AsyncPyWATS(base_url="...", token="...") as api:
        start = asyncio.get_event_loop().time()
        
        # 10 operations that each take ~100ms
        results = await api.product.get_products_batch(
            [f"PART-{i}" for i in range(10)],
            max_concurrent=10
        )
        
        elapsed = asyncio.get_event_loop().time() - start
        # Should complete in ~100ms, not 1000ms
        assert elapsed < 0.5
```

---

## Migration Guide

### From Sync to Async

```python
# Before (sync)
from pywats import pyWATS

api = pyWATS(base_url="...", token="...")
products = api.product.get_products()
api.close()

# After (async)
from pywats import AsyncPyWATS

async with AsyncPyWATS(base_url="...", token="...") as api:
    products = await api.product.get_products()
```

### Key Differences

| Aspect | Sync API | Async API |
|--------|----------|-----------|
| Import | `from pywats import pyWATS` | `from pywats import AsyncPyWATS` |
| Initialize | `api = pyWATS(...)` | `async with AsyncPyWATS(...) as api:` |
| Method calls | `api.product.get_product(pn)` | `await api.product.get_product(pn)` |
| Cleanup | `api.close()` (optional) | Automatic with context manager |
| Batch | Sequential loop | `await api.product.get_products_batch([...])` |
| Iteration | `for item in items:` | `async for item in api.iter_items():` |

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Code duplication between sync/async | Medium | High | Shared base classes, code generation |
| Rate limiter thread safety issues | Low | High | Use asyncio-compatible rate limiter |
| Connection pool exhaustion | Medium | Medium | Configurable limits, semaphores |
| Breaking sync API | Low | Critical | Extensive testing, separate classes |
| Learning curve for users | Medium | Low | Good docs, examples, migration guide |

---

## Success Metrics

- [ ] All 400+ existing tests pass
- [ ] Async tests achieve same coverage
- [ ] Batch operations 5-10x faster than sequential
- [ ] No memory leaks in long-running async operations
- [ ] Documentation complete and clear

---

## Timeline

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1 | Infrastructure | AsyncHttpClient, AsyncPyWATS base |
| 1-2 | Services | All async domain services |
| 2 | Batch | Concurrent batch operations |
| 2-3 | Iterators | Async generators for pagination |
| 3 | Polish | Tests, docs, examples |

---

## Appendix: httpx Async Example

```python
# httpx already supports async natively
import httpx

async def example():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

This makes our async implementation straightforward - httpx does the heavy lifting.
