# Performance Guide

## Table of Contents
- [HTTP Response Caching](#http-response-caching)
- [Configuration](#configuration)
- [Cache Tuning](#cache-tuning)
- [Monitoring Cache Performance](#monitoring-cache-performance)
- [Best Practices](#best-practices)
- [Benchmarking](#benchmarking)
- [Async API Performance](#async-api-performance)
- [Troubleshooting](#troubleshooting)

---

## HTTP Response Caching

pyWATS includes built-in HTTP response caching to improve performance for read-heavy workloads. The cache:

- **Automatically caches GET requests** - No manual cache management needed
- **Respects cache TTL** - Entries expire after configured time
- **Auto-invalidates on writes** - POST/PUT/DELETE requests invalidate related cache
- **LRU eviction** - Least recently used entries removed when cache is full
- **Thread-safe** - Safe for concurrent use
- **Zero breaking changes** - Disabled by default, opt-in feature

### When to Use Caching

✅ **Enable caching for:**
- Product/process lookups (rarely change)
- Configuration data queries
- Reporting/analytics dashboards
- Data exploration scripts
- Repeated queries for the same data

❌ **Disable caching for:**
- Real-time monitoring dashboards
- Live test result ingestion
- Time-sensitive queries
- Data that changes frequently

---

## Configuration

### Basic Setup

```python
from pywats import pyWATS

# Enable caching with defaults
api = pyWATS(
    base_url="https://your-server.com",
    token="your-api-token",
    enable_cache=True  # Enable HTTP response caching
)
```

### Full Configuration

```python
api = pyWATS(
    base_url="https://your-server.com",
    token="your-api-token",
    enable_cache=True,      # Enable caching
    cache_ttl=300,          # Time-to-live: 5 minutes (seconds)
    cache_max_size=1000     # Maximum cached responses
)
```

### Parameter Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enable_cache` | `bool` | `False` | Enable/disable HTTP response caching |
| `cache_ttl` | `int` | `300` | Time-to-live in seconds (how long to cache) |
| `cache_max_size` | `int` | `1000` | Maximum number of cached responses |

---

## Cache Tuning

### TTL (Time-to-Live) Tuning

Choose cache TTL based on how frequently your data changes:

```python
# Real-time data - DISABLE caching
realtime_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=False  # Always fetch fresh data
)

# Frequently-changing data - SHORT TTL (1-5 minutes)
report_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=True,
    cache_ttl=60  # 1 minute
)

# Moderately-changing data - MEDIUM TTL (5-15 minutes)
product_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=True,
    cache_ttl=600  # 10 minutes
)

# Rarely-changing data - LONG TTL (30-60 minutes)
config_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=True,
    cache_ttl=3600  # 1 hour
)
```

**TTL Guidelines:**

| Data Type | Change Frequency | Recommended TTL |
|-----------|------------------|-----------------|
| Real-time metrics | Seconds | `enable_cache=False` |
| Test reports | Minutes | `60-300` (1-5 min) |
| Products/processes | Hours | `600-3600` (10-60 min) |
| Configuration | Days/weeks | `3600-7200` (1-2 hours) |

### Cache Size Tuning

Choose cache size based on your application's workload:

```python
# Small scripts - SMALL CACHE (100-500 entries)
script_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=True,
    cache_max_size=100  # Small focused cache
)

# General applications - MEDIUM CACHE (500-1000 entries)
app_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=True,
    cache_max_size=1000  # Default size
)

# Dashboards/reporting - LARGE CACHE (1000-5000 entries)
dashboard_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=True,
    cache_max_size=5000  # Large cache for many queries
)
```

**Cache Size Guidelines:**

| Application Type | Concurrent Queries | Recommended Size |
|------------------|--------------------|------------------|
| Single-purpose scripts | 10-50 | `100` |
| CLI tools | 50-200 | `500` |
| Web applications | 200-1000 | `1000` |
| Dashboards | 1000-5000 | `2000-5000` |

**Cache Size Too Small:** Frequent evictions (thrashing), low hit rate  
**Cache Size Too Large:** Higher memory usage, slower lookups

---

## Monitoring Cache Performance

### Cache Statistics

Monitor cache performance to optimize your configuration:

```python
# Get cache statistics
stats = api.http_client.get_cache_stats()

print(f"Cache hits: {stats['hits']}")
print(f"Cache misses: {stats['misses']}")
print(f"Current size: {stats['size']} / {stats['max_size']}")
print(f"Hit rate: {stats['hits'] / (stats['hits'] + stats['misses']):.1%}")
```

**Example Output:**
```
Cache hits: 450
Cache misses: 150
Current size: 200 / 1000
Hit rate: 75.0%
```

### Metrics

Cache metrics available in Prometheus format (see [Observability Guide](observability.md)):

```promql
# HTTP cache hit rate
rate(pywats_http_cache_hits_total[5m]) / 
rate(pywats_http_cache_total[5m])

# Cache size utilization
pywats_http_cache_size / pywats_http_cache_max_size

# Cache eviction rate (sign of cache thrashing)
rate(pywats_http_cache_evictions_total[5m])
```

### Target Metrics

| Metric | Target | Interpretation |
|--------|--------|----------------|
| **Hit Rate** | >70% | Good caching effectiveness |
| **Cache Utilization** | 50-90% | Appropriately sized cache |
| **Eviction Rate** | <10/min | Minimal thrashing |
| **TTL Expiry Rate** | Variable | Depends on data freshness needs |

---

## Best Practices

### 1. Enable Caching for Read-Heavy Workloads

```python
# Dashboard fetching product data repeatedly
dashboard_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=True,
    cache_ttl=600,  # 10 minutes
    cache_max_size=2000
)

# Fetch products multiple times (only first hits server)
products = dashboard_api.product.get_products()  # Cache MISS
products = dashboard_api.product.get_products()  # Cache HIT (instant)
products = dashboard_api.product.get_products()  # Cache HIT (instant)
```

### 2. Disable Caching for Real-Time Data

```python
# Real-time monitoring - always fetch fresh data
monitor_api = pyWATS(
    base_url="https://server.com",
    token="token",
    enable_cache=False  # Never cache
)

# Always get latest report data
latest_reports = monitor_api.report.get_recent_reports()
```

### 3. Tune TTL Based on Data Change Frequency

```python
# Products change occasionally - longer TTL
product_api = pyWATS(..., cache_ttl=3600)  # 1 hour

# Reports created frequently - shorter TTL
report_api = pyWATS(..., cache_ttl=60)  # 1 minute
```

### 4. Monitor and Adjust

```python
# Check cache effectiveness periodically
stats = api.http_client.get_cache_stats()
hit_rate = stats['hits'] / (stats['hits'] + stats['misses'])

if hit_rate < 0.5:  # Less than 50% hit rate
    print("Consider increasing cache_ttl or cache_max_size")

if stats['size'] >= stats['max_size'] * 0.95:  # Cache >95% full
    print("Consider increasing cache_max_size")
```

### 5. Use Environment-Specific Configuration

```python
import os

environment = os.getenv("ENVIRONMENT", "development")

if environment == "production":
    # Production: Conservative caching
    api = pyWATS(
        base_url=os.getenv("WATS_URL"),
        token=os.getenv("WATS_TOKEN"),
        enable_cache=True,
        cache_ttl=300,  # 5 minutes
        cache_max_size=1000
    )
elif environment == "development":
    # Development: Aggressive caching for fast iteration
    api = pyWATS(
        base_url="https://dev.server.com",
        token="dev-token",
        enable_cache=True,
        cache_ttl=3600,  # 1 hour
        cache_max_size=5000
    )
```

### 6. Combine Caching with Async API

```python
from pywats import AsyncWATS
import asyncio

async def fetch_data():
    # Async + caching = best performance
    async with AsyncWATS(
        base_url="https://server.com",
        token="token",
        enable_cache=True,
        cache_ttl=300
    ) as api:
        # Concurrent requests with caching
        products, processes = await asyncio.gather(
            api.product.get_products(),
            api.process.get_processes()
        )
        return products, processes
```

---

## Benchmarking

Use the included benchmark suite to measure cache performance:

```bash
# Run complete benchmark suite
python examples/performance/benchmarks.py

# Set credentials
export WATS_BASE_URL="https://your-server.com"
export WATS_TOKEN="your-token"
```

### Benchmark Results Example

```
=== Cache vs No-Cache Performance ===
Cached:    150 requests in 2.3s (65.2 req/s)
No Cache:   150 requests in 45.7s (3.3 req/s)
Improvement: 19.8x faster with caching

=== Concurrent Requests (Async) ===
5 concurrent:  500 requests in 8.2s (61.0 req/s)
10 concurrent: 500 requests in 8.5s (58.8 req/s)
20 concurrent: 500 requests in 9.1s (54.9 req/s)

=== Cache Size Testing ===
Size 100:   Hit rate 68%, Avg 45ms
Size 500:   Hit rate 82%, Avg 28ms
Size 1000:  Hit rate 88%, Avg 22ms
Size 2000:  Hit rate 91%, Avg 20ms
```

See [examples/performance/benchmarks.py](../../examples/performance/benchmarks.py) for complete benchmarking code.

---

## Async API Performance

The `AsyncWATS` API provides significant performance improvements for concurrent workloads:

### Concurrent Requests

```python
import asyncio
from pywats import AsyncWATS

async def fetch_multiple():
    async with AsyncWATS(
        base_url="https://server.com",
        token="token",
        enable_cache=True
    ) as api:
        # Fetch 10 products concurrently
        tasks = [
            api.product.get_product(product_id)
            for product_id in range(1, 11)
        ]
        products = await asyncio.gather(*tasks)
        return products

# 10x faster than sequential sync calls
products = asyncio.run(fetch_multiple())
```

### Performance Comparison

| Approach | 100 Requests | Throughput |
|----------|--------------|------------|
| Sync (no cache) | 180s | 0.6 req/s |
| Sync (with cache) | 15s | 6.7 req/s |
| Async (no cache) | 25s | 4.0 req/s |
| **Async + cache** | **3s** | **33.3 req/s** |

---

## Troubleshooting

### Low Cache Hit Rate (<50%)

**Symptoms:** Cache hits < cache misses, poor performance improvement

**Causes:**
- Cache TTL too short
- Cache size too small (frequent evictions)
- Queries with many unique parameters
- Real-time data being cached

**Solutions:**
```python
# Increase TTL
api = pyWATS(..., cache_ttl=600)  # Increase from 300 to 600

# Increase cache size
api = pyWATS(..., cache_max_size=2000)  # Increase from 1000 to 2000

# Check if data should be cached at all
if realtime_workload:
    api = pyWATS(..., enable_cache=False)
```

### Cache Memory Usage Too High

**Symptoms:** High memory consumption, slow application

**Causes:**
- Cache size too large
- Caching large response payloads

**Solutions:**
```python
# Reduce cache size
api = pyWATS(..., cache_max_size=500)  # Reduce from 1000 to 500

# Reduce TTL (entries expire sooner)
api = pyWATS(..., cache_ttl=180)  # Reduce from 300 to 180

# Disable caching if not beneficial
api = pyWATS(..., enable_cache=False)
```

### Stale Data Being Returned

**Symptoms:** Old data shown after updates, cache not invalidating

**Causes:**
- Cache TTL too long
- Write operations not invalidating cache properly

**Solutions:**
```python
# Reduce TTL for frequently-changing data
api = pyWATS(..., cache_ttl=60)  # Short TTL for fresh data

# Disable caching for real-time needs
api = pyWATS(..., enable_cache=False)

# Verify write operations are using POST/PUT/DELETE
# (these automatically invalidate cache)
```

### Cache Not Working

**Symptoms:** No performance improvement, hit rate always 0%

**Causes:**
- Caching not enabled
- All requests are writes (POST/PUT/DELETE)
- Requests have unique URLs (query parameters)

**Solutions:**
```python
# Verify caching is enabled
api = pyWATS(..., enable_cache=True)  # Must be True

# Check cache stats
stats = api.http_client.get_cache_stats()
print(f"Hits: {stats['hits']}, Misses: {stats['misses']}")

# Ensure you're making repeated GET requests
# (POST/PUT/DELETE are not cached)
```

---

## Additional Resources

- **[Observability Guide](observability.md)** - Monitoring cache metrics
- **[Configuration Guide](configuration.md)** - Complete configuration reference
- **[Getting Started: Caching](../../examples/getting_started/05_caching_performance.py)** - Basic caching examples
- **[Benchmarks](../../examples/performance/benchmarks.py)** - Performance testing suite
- **[Client Configuration Example](../../examples/client/configuration.py)** - Real-world configuration patterns

---

**Last Updated:** 2026-02-02
