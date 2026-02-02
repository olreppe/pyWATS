# HTTP Caching & Metrics Integration Plan

**Status:** Infrastructure complete, wiring needed  
**Created:** February 2, 2026

---

## Current State Summary

We've built the infrastructure for HTTP caching and metrics, but it's not fully integrated into the service layers yet. Here's what exists and where:

### ✅ What's Implemented

1. **HTTP Response Caching** - [src/pywats/core/client.py](../../../src/pywats/core/client.py)
   - `HttpClient` / `AsyncHttpClient` enhanced with TTLCache
   - Constructor params: `enable_cache`, `cache_ttl`, `cache_max_size`
   - Automatic caching of GET 2xx responses
   - Auto-invalidation on POST/PUT/DELETE
   - **Scope:** Low-level HTTP client (core infrastructure)

2. **Metrics Collection** - [src/pywats/core/metrics.py](../../../src/pywats/core/metrics.py)
   - `MetricsCollector` class with Prometheus integration
   - HTTP request tracking (method, endpoint, status, duration)
   - System metrics (CPU, memory, threads)
   - **Scope:** Low-level metrics infrastructure

3. **Health & Metrics Endpoints** - [src/pywats_client/service/health_server.py](../../../src/pywats_client/service/health_server.py)
   - GET `/health`, `/health/live`, `/health/ready`, `/health/details`
   - GET `/metrics` - Prometheus or JSON summary
   - **Scope:** Service-level health monitoring

---

## Where Code Belongs

### **Core Infrastructure** (src/pywats/core/)
✅ **Already in the right place:**
- `client.py` - HTTP client with caching
- `async_client.py` - Async HTTP client (needs caching - see below)
- `metrics.py` - Prometheus metrics collector
- `cache.py` - TTLCache, AsyncTTLCache

**Purpose:** Low-level building blocks used by all domain services

---

### **Domain Services** (src/pywats/domains/*/async_repository.py)
⚠️ **Indirectly uses caching (via HttpClient):**
- `AsyncProductRepository` receives `AsyncHttpClient` instance
- `AsyncReportRepository` receives `AsyncHttpClient` instance
- All 9 domain repositories receive HTTP client as dependency

**Current behavior:**
- Caching **IS** active if the HTTP client passed in has caching enabled
- Repositories don't control caching (that's correct - separation of concerns)

**What's working:**
- When `AsyncWATS` creates HttpClient with `enable_cache=True`, all domain services automatically benefit
- No code changes needed in repositories

---

### **Main API Entry Points** (src/pywats/)
⚠️ **Needs integration:**

**[src/pywats/async_wats.py](../../../src/pywats/async_wats.py)** - Line ~175
```python
# Current code:
self._http_client = AsyncHttpClient(
    base_url=self._base_url,
    token=self._token,
    timeout=self._timeout,
    verify_ssl=self._verify_ssl,
    rate_limiter=rate_limiter,
    enable_throttling=enable_throttling,
    retry_config=self._retry_config,
)
```

**Missing:** `enable_cache`, `cache_ttl`, `cache_max_size`, `metrics_collector` parameters

**[src/pywats/pywats.py](../../../src/pywats/pywats.py)** - Similar location
- Sync wrapper - same issue

---

### **Client Service** (src/pywats_client/service/)
⚠️ **Needs integration:**

**[src/pywats_client/service/async_client_service.py](../../../src/pywats_client/service/async_client_service.py)**

**Current state (Line ~100-150):**
```python
self.api: Optional[AsyncWATS] = None  # Created later in _connect_to_api()
self._converter_pool: Optional['AsyncConverterPool'] = None
self._pending_queue: Optional['AsyncPendingQueue'] = None
self._health_server = None  # Created in _start_health_server()
```

**Missing:**
1. `MetricsCollector` instance not created
2. Health server doesn't receive references to:
   - `_metrics_collector`
   - `_http_client` (for cache stats)
   - `_converter_pool` (for queue stats)

---

## Integration Tasks

### Task 1: Add Caching to AsyncHttpClient
**File:** [src/pywats/core/async_client.py](../../../src/pywats/core/async_client.py)  
**Status:** ⏳ Not started  
**Effort:** Medium (mirror HttpClient changes)

**Changes needed:**
- Add `enable_cache`, `cache_ttl`, `cache_max_size` constructor params
- Add `AsyncTTLCache` instance for response caching
- Add cache logic to `get()` method
- Add invalidation to `post()`, `put()`, `delete()`
- Add `cache`, `cache_enabled`, `clear_cache()`, `invalidate_cache()` properties

**Impact:** All async domain services automatically get caching

---

### Task 2: Wire Caching Parameters to AsyncWATS
**File:** [src/pywats/async_wats.py](../../../src/pywats/async_wats.py)  
**Status:** ⏳ Not started  
**Effort:** Small

**Changes needed:**
```python
def __init__(
    self,
    # ... existing params ...
    enable_cache: bool = True,
    cache_ttl: float = 300.0,
    cache_max_size: int = 1000,
):
    # ... existing code ...
    
    self._http_client = AsyncHttpClient(
        base_url=self._base_url,
        token=self._token,
        timeout=self._timeout,
        verify_ssl=self._verify_ssl,
        rate_limiter=rate_limiter,
        enable_throttling=enable_throttling,
        retry_config=self._retry_config,
        enable_cache=enable_cache,  # NEW
        cache_ttl=cache_ttl,  # NEW
        cache_max_size=cache_max_size,  # NEW
    )
```

**Also update:** `src/pywats/pywats.py` (sync wrapper)

**Impact:** Users can configure caching via `AsyncWATS()` constructor

---

### Task 3: Create MetricsCollector in AsyncClientService
**File:** [src/pywats_client/service/async_client_service.py](../../../src/pywats_client/service/async_client_service.py)  
**Status:** ⏳ Not started  
**Effort:** Small

**Changes needed in `__init__`:**
```python
def __init__(self, instance_id: str = "default"):
    # ... existing code ...
    
    # Metrics collection
    self._metrics_collector = None
    if self.config.enable_metrics:  # Add config flag
        from pywats.core.metrics import MetricsCollector
        self._metrics_collector = MetricsCollector(enabled=True)
```

**Changes needed in API creation:**
```python
async def _connect_to_api(self):
    # ... existing code ...
    
    self.api = AsyncWATS(
        base_url=base_url,
        token=token,
        # ... other params ...
        metrics_collector=self._metrics_collector,  # NEW
    )
```

**Impact:** HTTP requests automatically tracked in Prometheus metrics

---

### Task 4: Wire Components to HealthServer
**File:** [src/pywats_client/service/async_client_service.py](../../../src/pywats_client/service/async_client_service.py)  
**Status:** ⏳ Not started  
**Effort:** Small

**Changes needed in `_start_health_server()`:**
```python
async def _start_health_server(self):
    from .health_server import HealthServer
    self._health_server = HealthServer(port=self._health_port)
    self._health_server.set_health_check(self._get_health_status)
    
    # NEW: Wire up component references for /metrics endpoint
    self._health_server._metrics_collector = self._metrics_collector
    self._health_server._http_client = self.api._http_client if self.api else None
    self._health_server._converter_pool = self._converter_pool
    
    self._health_server.start()
```

**Impact:** `/metrics` endpoint exposes real cache/queue stats

---

### Task 5: Add Configuration Options
**File:** [src/pywats_client/core/config.py](../../../src/pywats_client/core/config.py)  
**Status:** ⏳ Not started  
**Effort:** Small

**Add to ClientConfig:**
```python
class ClientConfig:
    # ... existing fields ...
    
    # Performance & Observability
    enable_cache: bool = True
    cache_ttl_seconds: int = 300
    cache_max_size: int = 1000
    enable_metrics: bool = True
    metrics_port: int = 9090  # Prometheus scrape port
```

**Impact:** Users can configure via JSON config files

---

### Task 6: Update Examples
**Files:** [examples/getting_started/](../../../examples/getting_started/)  
**Status:** ⏳ Not started  
**Effort:** Small

**Add caching examples:**
```python
# Example: Disable caching for specific use case
api = AsyncWATS(
    base_url="http://localhost/WATS",
    token="...",
    enable_cache=False  # Disable if always need fresh data
)

# Example: Custom cache TTL
api = AsyncWATS(
    base_url="http://localhost/WATS",
    token="...",
    cache_ttl=60.0  # 1-minute TTL for fast-changing data
)
```

---

## Migration Path

### Phase 1: Core Integration (Week 1)
1. ✅ Add caching to AsyncHttpClient (mirror HttpClient)
2. ✅ Wire caching params to AsyncWATS/pyWATS constructors
3. ✅ Test: Verify caching works end-to-end

### Phase 2: Service Integration (Week 1)
4. ✅ Create MetricsCollector in AsyncClientService
5. ✅ Wire components to HealthServer
6. ✅ Add configuration options to ClientConfig
7. ✅ Test: Verify /metrics endpoint returns real data

### Phase 3: Documentation & Examples (Week 2)
8. ✅ Update examples with caching configuration
9. ✅ Update user guides (docs/guides/)
10. ✅ Add performance benchmarks showing cache benefits

---

## Testing Strategy

### Unit Tests
- ✅ HttpClient caching already working (examples/performance/http_caching.py)
- ⏳ AsyncHttpClient caching (mirror HttpClient tests)
- ⏳ MetricsCollector integration (verify metrics tracked)

### Integration Tests
- ⏳ AsyncWATS with caching enabled (verify domain services benefit)
- ⏳ HealthServer /metrics endpoint (verify stats exposed)
- ⏳ Config file caching settings (verify user control)

### Performance Tests
- ⏳ Before/after benchmarks for repeated queries
- ⏳ Cache hit rate measurement
- ⏳ Memory usage with large caches

---

## Backward Compatibility

✅ **All changes are backward compatible:**
- Caching defaults to **enabled** (opt-out if not wanted)
- Metrics defaults to **disabled** (opt-in)
- No breaking changes to existing APIs
- Existing code continues working without changes

**User control:**
```python
# Disable caching if needed
api = AsyncWATS(base_url="...", token="...", enable_cache=False)

# Keep existing code - caching silently improves performance
api = AsyncWATS(base_url="...", token="...")  # Caching enabled by default
```

---

## Success Criteria

### Performance Improvements
- ✅ 50%+ reduction in repeated query response times
- ✅ Cache hit rate >70% for typical workloads
- ✅ Zero performance degradation for uncached paths

### Observability
- ✅ /metrics endpoint exposes cache statistics
- ✅ /metrics endpoint exposes HTTP request metrics
- ✅ Prometheus can scrape metrics

### User Experience
- ✅ Zero code changes required for existing users
- ✅ Simple opt-in for advanced features
- ✅ Clear documentation and examples

---

## Next Actions

**Recommended order:**
1. Task 1: Add caching to AsyncHttpClient (enables everything else)
2. Task 2: Wire params to AsyncWATS (makes caching configurable)
3. Task 3: Create MetricsCollector (enables observability)
4. Task 4: Wire to HealthServer (exposes metrics)
5. Task 5: Add config options (user control)
6. Task 6: Update examples (user education)

**Estimated effort:** 3-4 days for full integration
