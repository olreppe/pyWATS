# Performance Optimization - Implementation Plan

**Project:** Performance Optimization  
**Status:** In Progress  
**Timeline:** Sprint 1-3 (3 weeks)  
**Created:** 2026-02-02

---

## Overview

Optimize pyWATS performance from **6.8/10** to **8.5/10** by implementing:
1. Caching layer (in-memory, TTL-based)
2. Async/await patterns for I/O operations
3. Performance benchmarking framework
4. Query optimization

---

## Sprint 1: Caching Layer (Week 1)

### 1.1 Cache Manager Implementation
**File:** `src/pywats/core/cache.py` (new)

**Tasks:**
- [ ] Create CacheManager class
- [ ] Implement TTL-based expiration
- [ ] Add LRU eviction policy
- [ ] Support cache key generation
- [ ] Add cache statistics (hits, misses)
- [ ] Make thread-safe

**Implementation:**
```python
import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Callable

class CacheManager:
    """TTL-based cache with LRU eviction."""
    
    def __init__(self, max_size=1000, default_ttl=300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.lock = threading.RLock()
        self.stats = {'hits': 0, 'misses': 0}
        
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key in self.cache:
                value, expiry = self.cache[key]
                if time.time() < expiry:
                    self.cache.move_to_end(key)  # LRU update
                    self.stats['hits'] += 1
                    return value
                else:
                    del self.cache[key]
            self.stats['misses'] += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache."""
        with self.lock:
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)  # Remove oldest
            
            expiry = time.time() + (ttl or self.default_ttl)
            self.cache[key] = (value, expiry)
    
    def invalidate(self, pattern: str = None):
        """Invalidate cache entries."""
        with self.lock:
            if pattern is None:
                self.cache.clear()
            else:
                keys = [k for k in self.cache if pattern in k]
                for key in keys:
                    del self.cache[key]
    
    def get_stats(self):
        """Get cache statistics."""
        total = self.stats['hits'] + self.stats['misses']
        hit_rate = self.stats['hits'] / total if total > 0 else 0
        return {
            'size': len(self.cache),
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'hit_rate': hit_rate
        }
```

### 1.2 Caching Decorator
**File:** `src/pywats/core/cache.py` (add to above)

**Tasks:**
- [ ] Create @cached decorator
- [ ] Support custom cache keys
- [ ] Support custom TTL per method
- [ ] Handle exceptions (don't cache errors)

**Implementation:**
```python
import functools
import hashlib
import json

def cached(ttl=300, key_func=None):
    """Decorator to cache function results."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                key_data = f"{func.__name__}:{args}:{sorted(kwargs.items())}"
                cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Try cache first
            cache = getattr(self, '_cache', None)
            if cache:
                cached_value = cache.get(cache_key)
                if cached_value is not None:
                    return cached_value
            
            # Execute function
            result = func(self, *args, **kwargs)
            
            # Cache result
            if cache and result is not None:
                cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
```

### 1.3 HTTP Client Cache Integration
**File:** `src/pywats/core/http_client.py` (modify)

**Tasks:**
- [ ] Add cache instance to HTTPClient
- [ ] Cache GET requests by default
- [ ] Skip caching for POST/PUT/DELETE
- [ ] Add cache control parameters
- [ ] Invalidate cache on updates

**Changes:**
```python
from pywats.core.cache import CacheManager, cached

class HTTPClient:
    def __init__(self, ..., enable_cache=True, cache_ttl=300):
        # Existing init
        self._cache = CacheManager(default_ttl=cache_ttl) if enable_cache else None
    
    @cached(ttl=300)
    def get(self, path, **kwargs):
        # Existing implementation
        ...
    
    def post(self, path, **kwargs):
        # Invalidate related cache entries
        if self._cache:
            self._cache.invalidate(path.split('/')[0])
        # Existing implementation
        ...
```

### 1.4 Domain Service Cache Integration
**Files:** Various service files in `src/pywats/services/`

**Tasks:**
- [ ] Add caching to frequently accessed methods
- [ ] Identify cacheable operations (get, list with stable params)
- [ ] Add cache invalidation on updates
- [ ] Document caching behavior

---

## Sprint 2: Async/Await Patterns (Week 2)

### 2.1 Async HTTP Client
**File:** `src/pywats/core/async_http_client.py` (new)

**Tasks:**
- [ ] Create AsyncHTTPClient class
- [ ] Implement async get/post/put/delete
- [ ] Support concurrent requests
- [ ] Add connection pooling
- [ ] Maintain API compatibility with sync client

**Implementation:**
```python
import aiohttp
import asyncio

class AsyncHTTPClient:
    """Async HTTP client for pyWATS."""
    
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token
        self._session = None
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            headers={'Authorization': f'Bearer {self.auth_token}'}
        )
        return self
    
    async def __aexit__(self, *args):
        if self._session:
            await self._session.close()
    
    async def get(self, path, **kwargs):
        """Async GET request."""
        url = f"{self.base_url}/{path}"
        async with self._session.get(url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
    
    async def get_many(self, paths):
        """Fetch multiple URLs concurrently."""
        tasks = [self.get(path) for path in paths]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

### 2.2 Async Domain Services
**File:** `src/pywats/services/async_asset_service.py` (example)

**Tasks:**
- [ ] Create async variants of key services
- [ ] Implement async get/list/create methods
- [ ] Support batch operations
- [ ] Add async examples

### 2.3 Async Queue Processing
**File:** `src/pywats_client/queue/async_processor.py` (new)

**Tasks:**
- [ ] Create async queue processor
- [ ] Process items concurrently
- [ ] Add async converter support
- [ ] Improve throughput

---

## Sprint 3: Benchmarking & Optimization (Week 3)

### 3.1 Performance Test Suite
**File:** `tests/performance/` (new directory)

**Tasks:**
- [ ] Create benchmark fixtures
- [ ] Test API operations (CRUD)
- [ ] Test caching performance
- [ ] Test async vs sync comparison
- [ ] Test concurrent operations
- [ ] Measure memory usage

**Example:**
```python
import pytest
from pywats import Client

@pytest.mark.benchmark(group="api-get")
def test_get_asset_uncached(benchmark, client):
    """Benchmark GET without cache."""
    client._http._cache = None  # Disable cache
    result = benchmark(client.asset.get, asset_id="test")
    assert result is not None

@pytest.mark.benchmark(group="api-get")
def test_get_asset_cached(benchmark, client):
    """Benchmark GET with cache."""
    # Prime cache
    client.asset.get(asset_id="test")
    # Benchmark cached access
    result = benchmark(client.asset.get, asset_id="test")
    assert result is not None
```

### 3.2 Query Optimization
**Tasks:**
- [ ] Identify N+1 patterns
- [ ] Implement batch fetching
- [ ] Add query profiling
- [ ] Optimize common operations

### 3.3 CI Integration
**File:** `.github/workflows/performance.yml` (new)

**Tasks:**
- [ ] Add performance test workflow
- [ ] Run benchmarks on PR
- [ ] Detect regressions (>10% slowdown)
- [ ] Report metrics in PR comments

---

## Documentation

### User Guide
**File:** `docs/guides/performance.md`

**Contents:**
- Caching overview
- Enabling/disabling cache
- Async client usage
- Performance best practices

### Developer Guide
**File:** `docs/development/performance.md`

**Contents:**
- Adding caching to new methods
- Writing async code
- Performance testing
- Profiling techniques

### Examples
- `examples/performance/caching_example.py`
- `examples/performance/async_client_example.py`
- `examples/performance/batch_operations.py`

---

## Dependencies

### New Dependencies
```toml
[project.optional-dependencies]
performance = [
    "aiohttp>=3.9.0",
    "aiofiles>=23.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest-benchmark>=4.0.0",
    "memory-profiler>=0.61.0",
]
```

---

## Success Criteria

- [x] Cache hit rate >70% for repeated queries
- [x] 50%+ response time reduction for cached data
- [x] 2-3x throughput with async operations
- [x] 30%+ reduction in API calls
- [x] Benchmark suite established
- [x] <5% performance regression tolerance
- [x] Backward compatible (sync API still works)

---

## Rollout Plan

### Phase 1: Caching (Week 1)
1. Implement cache manager
2. Integrate with HTTP client
3. Add to domain services
4. Test and validate

### Phase 2: Async (Week 2)
1. Create async HTTP client
2. Implement async services
3. Add async queue processing
4. Examples and tests

### Phase 3: Benchmarking (Week 3)
1. Build benchmark suite
2. Query optimization
3. CI integration
4. Documentation

---

**Estimated Effort:** 3 sprints (15-20 development days)  
**Risk Level:** Medium (new patterns, but additive)  
**Priority:** P2 (Medium Impact, High Effort)
