# Performance Optimization - TODO

**Project:** Performance Optimization  
**Last Updated:** 2026-02-02

---

## Sprint 1: Caching Layer ✅ COMPLETE

### Core Implementation ✅
- ✅ `src/pywats/core/cache.py` (635 lines, pre-existing, validated)
  - ✅ TTLCache class with TTL
  - ✅ LRU eviction policy
  - ✅ Thread-safe operations
  - ✅ Cache statistics tracking
  - ✅ @cached decorator
  - ✅ AsyncTTLCache variant

### HTTP Client Integration ✅
- ✅ Modified `src/pywats/core/client.py` (sync)
  - ✅ Added TTLCache instance
  - ✅ Cache GET requests with key generation
  - ✅ Invalidate cache on POST/PUT/DELETE
  - ✅ Added enable_cache, cache_ttl, cache_max_size parameters
  - ✅ Added cache properties and methods

### Domain Service Caching ✅
- ✅ All domain services automatically benefit (via HttpClient)
- ✅ No code changes needed in repositories (separation of concerns)

### Testing ✅
- ✅ Created `examples/performance/http_caching.py` (456 lines, 6 examples)

---

## Sprint 2: Metrics & Health ✅ COMPLETE

- ✅ Metrics integration in HttpClient
- ✅ /metrics endpoint in health_server.py
- ✅ HTTP cache statistics exposed

---

## Sprint 3: Integration & Completion (CURRENT)

### AsyncHttpClient Caching (Critical Path) ✅ COMPLETE
- ✅ Add caching to `src/pywats/core/async_client.py`
  - ✅ Add enable_cache, cache_ttl, cache_max_size params
  - ✅ Create AsyncTTLCache instance
  - ✅ Add cache logic to get() method
  - ✅ Add invalidation to post/put/delete methods
  - ✅ Add cache properties (cache, cache_enabled, clear_cache, invalidate_cache)
  - ✅ Add metrics_collector parameter and tracking
  - ✅ Mirror all HttpClient caching functionality

### AsyncWATS Integration ✅ COMPLETE
- ✅ Wire caching params to `src/pywats/async_wats.py`
  - ✅ Add enable_cache, cache_ttl, cache_max_size constructor params
  - ✅ Pass to AsyncHttpClient initialization
- ✅ Wire caching params to `src/pywats/pywats.py` (sync wrapper)

### Configuration ✅ COMPLETE
- ✅ Add config options to `src/pywats_client/core/config.py`
  - ✅ enable_cache: bool = True
  - ✅ cache_ttl_seconds: float = 300.0
  - ✅ cache_max_size: int = 1000
  - ✅ Documented in config schema with inline comments

### Performance Benchmarks (Optional)
- [ ] Benchmark cache hit rates
- [ ] Benchmark response time improvements
- [ ] Memory usage profiling

---

## Sprint 2: Async/Await Patterns (DEFERRED)

### Async HTTP Client
- [ ] Create `src/pywats/core/async_http_client.py`
  - [ ] AsyncHTTPClient class
  - [ ] Async get/post/put/delete
  - [ ] get_many() for concurrent requests
  - [ ] Connection pooling
  - [ ] Context manager support

### Async Domain Services
- [ ] Create async service variants
  - [ ] AsyncAssetService
  - [ ] AsyncProductService
  - [ ] AsyncReportService
- [ ] Support batch operations
- [ ] Add async examples

### Async Queue
- [ ] Create `src/pywats_client/queue/async_processor.py`
  - [ ] Concurrent queue processing
  - [ ] Async converter support
  - [ ] Better throughput

### Testing
- [ ] Create `tests/async/test_async_client.py`
- [ ] Test concurrent operations
- [ ] Compare async vs sync performance

---

## Sprint 3: Benchmarking & Optimization

### Benchmark Suite
- [ ] Create `tests/performance/` directory
- [ ] Add pytest-benchmark fixtures
- [ ] Benchmark API operations
- [ ] Benchmark caching
- [ ] Benchmark async vs sync
- [ ] Memory profiling
- [ ] CPU profiling

### Query Optimization
- [ ] Identify N+1 patterns
- [ ] Implement batch fetching
- [ ] Add query profiling
- [ ] Optimize common operations
- [ ] Document optimizations

### CI Integration
- [ ] Create `.github/workflows/performance.yml`
- [ ] Run benchmarks on PR
- [ ] Detect regressions
- [ ] Report metrics

### Documentation
- [ ] Create `docs/guides/performance.md`
- [ ] Create `docs/development/performance.md`
- [ ] Add caching examples
- [ ] Add async examples
- [ ] Update README

---

## Dependencies
- [ ] Add aiohttp to pyproject.toml
- [ ] Add aiofiles to pyproject.toml
- [ ] Add pytest-benchmark to dev dependencies
- [ ] Add memory-profiler to dev dependencies

---

## Validation
- [ ] Cache hit rate >70%
- [ ] Response time -50% (cached)
- [ ] Throughput +200% (async)
- [ ] API calls -30%
- [ ] <5% regression tolerance
- [ ] Backward compatible

---

**Created:** 2026-02-02
