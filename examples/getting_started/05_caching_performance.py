"""
Getting Started: HTTP Response Caching & Performance

This example demonstrates HTTP response caching for improved performance.
Learn when to enable/disable caching and how to tune cache settings.
"""
from pywats import pyWATS
from pywats.core import ErrorMode
import time

# =============================================================================
# Basic Caching
# =============================================================================

# Enable HTTP response caching (default: disabled)
# Caching speeds up repeated requests for the same data
api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=True,  # Enable caching
    cache_ttl=300,  # Cache responses for 5 minutes
    cache_max_size=1000  # Store up to 1000 cached responses
)

print("HTTP caching enabled:")
print("  - TTL: 300 seconds (5 minutes)")
print("  - Max size: 1000 entries")
print("  - GET requests are cached automatically")
print("  - POST/PUT/DELETE invalidate related cache entries")


# =============================================================================
# When to Use Caching
# =============================================================================

# ✅ ENABLE CACHING for read-heavy workloads:
# - Fetching product lists (rarely change)
# - Looking up process definitions
# - Repeated queries for the same data
# - Dashboard/reporting applications
# - Data exploration/analysis scripts

cached_api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=True,
    cache_ttl=600  # 10 minutes for slowly-changing data
)

# Example: Fetch products multiple times (only first call hits server)
start = time.time()
products1 = cached_api.product.get_products()  # Cache MISS - hits server
products2 = cached_api.product.get_products()  # Cache HIT - instant
products3 = cached_api.product.get_products()  # Cache HIT - instant
elapsed = time.time() - start
print(f"\nFetched products 3 times in {elapsed:.2f}s (with caching)")


# ❌ DISABLE CACHING for real-time data:
# - Live monitoring dashboards
# - Real-time test result ingestion
# - Time-sensitive queries
# - Data that changes frequently

realtime_api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=False  # Disable caching for fresh data
)

print("\nCaching disabled for real-time data")
print("  - Every request hits the server")
print("  - Always get the latest data")
print("  - Use for monitoring and real-time ingestion")


# =============================================================================
# Cache TTL Tuning
# =============================================================================

# Short TTL (30-120 seconds) for frequently-changing data
short_ttl_api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=True,
    cache_ttl=60  # 1 minute cache
)
print("\nShort TTL (60s) for recent reports/metrics")

# Medium TTL (5-15 minutes) for moderately-changing data
medium_ttl_api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=True,
    cache_ttl=600  # 10 minute cache
)
print("Medium TTL (600s) for product/process data")

# Long TTL (30-60 minutes) for rarely-changing data
long_ttl_api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=True,
    cache_ttl=3600  # 1 hour cache
)
print("Long TTL (3600s) for static configuration data")


# =============================================================================
# Cache Size Tuning
# =============================================================================

# Small cache (100-500) for single-purpose scripts
small_cache_api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=True,
    cache_ttl=300,
    cache_max_size=100  # Small cache
)
print("\nSmall cache (100 entries) for focused scripts")

# Medium cache (500-1000) for general applications
medium_cache_api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=True,
    cache_ttl=300,
    cache_max_size=1000  # Medium cache
)
print("Medium cache (1000 entries) for general use")

# Large cache (1000-5000) for complex dashboards
large_cache_api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    enable_cache=True,
    cache_ttl=300,
    cache_max_size=5000  # Large cache
)
print("Large cache (5000 entries) for dashboards/reporting")


# =============================================================================
# Cache Statistics & Monitoring
# =============================================================================

# Monitor cache performance (if your client supports it)
# Example usage:
# stats = api.get_cache_stats()
# print(f"Cache hits: {stats['hits']}")
# print(f"Cache misses: {stats['misses']}")
# print(f"Hit rate: {stats['hits'] / (stats['hits'] + stats['misses']):.1%}")
# print(f"Cache size: {stats['size']} / {stats['max_size']}")

print("\nCache Statistics (when available):")
print("  - hits: Number of requests served from cache")
print("  - misses: Number of requests that hit the server")
print("  - hit_rate: Percentage of cached requests (higher is better)")
print("  - size: Current number of cached entries")


# =============================================================================
# Automatic Cache Invalidation
# =============================================================================

print("\nAutomatic Cache Invalidation:")
print("  - GET requests are cached")
print("  - POST/PUT/DELETE requests invalidate related cache entries")
print("  - Example: Creating a product invalidates product list cache")
print("  - No manual cache management needed!")

# Example workflow:
# 1. api.product.get_products()  # Cache MISS - fetch from server
# 2. api.product.get_products()  # Cache HIT - instant response
# 3. api.product.create_product(...)  # POST request invalidates cache
# 4. api.product.get_products()  # Cache MISS - fresh data after create


# =============================================================================
# Performance Best Practices
# =============================================================================

print("\n" + "="*60)
print("Performance Best Practices")
print("="*60)
print("\n1. Enable caching for read-heavy workloads")
print("   cached_api = pyWATS(..., enable_cache=True, cache_ttl=300)")

print("\n2. Disable caching for real-time data")
print("   realtime_api = pyWATS(..., enable_cache=False)")

print("\n3. Tune TTL based on data change frequency:")
print("   - Real-time: enable_cache=False")
print("   - Frequent (reports): cache_ttl=60 (1 minute)")
print("   - Moderate (products): cache_ttl=600 (10 minutes)")
print("   - Rare (config): cache_ttl=3600 (1 hour)")

print("\n4. Tune cache size based on workload:")
print("   - Scripts: cache_max_size=100")
print("   - Applications: cache_max_size=1000")
print("   - Dashboards: cache_max_size=5000")

print("\n5. Monitor cache hit rate (aim for >70%)")
print("   stats = api.get_cache_stats()")
print("   hit_rate = stats['hits'] / (stats['hits'] + stats['misses'])")

print("\n6. Combine caching with other optimizations:")
print("   - Use async API for concurrent requests")
print("   - Batch operations when possible")
print("   - Use filters to reduce data transfer")

print("\n7. See benchmarks for performance data:")
print("   python examples/performance/benchmarks.py")

print("\n" + "="*60)
print("\nFor more details, see:")
print("  - docs/guides/performance.md (Performance tuning guide)")
print("  - docs/guides/observability.md (Cache metrics & monitoring)")
print("  - examples/performance/ (Benchmarking tools)")
print("="*60)
