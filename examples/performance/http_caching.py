"""
HTTP Response Caching Example
==============================

Demonstrates HTTP client caching capabilities for improved performance.

Key Concepts:
    - Automatic GET request caching with TTL (Time To Live)
    - Cache hit/miss tracking
    - Cache invalidation on mutations
    - Performance benefits measurement
    - Cache statistics

Performance Impact:
    - Cache hits return responses instantly (no network latency)
    - Reduces server load
    - Improves application responsiveness
    - Configurable TTL balances freshness vs performance
"""

import asyncio
import time
from typing import Optional

from pywats import AsyncProductService, AsyncProductRepository
from pywats.core.client import HttpClient


async def example_basic_caching():
    """Basic caching example - repeated GET requests."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic HTTP Response Caching")
    print("=" * 70)
    
    # Create HTTP client with caching enabled (default: 5-minute TTL)
    http_client = HttpClient(
        base_url="http://localhost/WATS",
        enable_cache=True,
        cache_ttl=300.0,  # 5 minutes (default)
        cache_max_size=1000
    )
    
    repository = AsyncProductRepository(http_client=http_client)
    service = AsyncProductService(repository=repository)
    
    # First request - cache miss (fetches from server)
    print("\n1. First request (cache miss):")
    start = time.perf_counter()
    product1 = await service.get_product("PN12345")
    elapsed1 = time.perf_counter() - start
    print(f"   Product: {product1.name if product1 else 'Not found'}")
    print(f"   Time: {elapsed1 * 1000:.2f} ms")
    
    # Second request - cache hit (returns instantly)
    print("\n2. Second request (cache hit):")
    start = time.perf_counter()
    product2 = await service.get_product("PN12345")
    elapsed2 = time.perf_counter() - start
    print(f"   Product: {product2.name if product2 else 'Not found'}")
    print(f"   Time: {elapsed2 * 1000:.2f} ms")
    
    # Performance improvement
    speedup = elapsed1 / elapsed2 if elapsed2 > 0 else float('inf')
    print(f"\n   Performance: {speedup:.1f}x faster (cache hit)")
    print(f"   Time saved: {(elapsed1 - elapsed2) * 1000:.2f} ms")
    
    await http_client.close()


async def example_cache_statistics():
    """Track cache performance with statistics."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Cache Statistics")
    print("=" * 70)
    
    http_client = HttpClient(
        base_url="http://localhost/WATS",
        enable_cache=True,
        cache_ttl=300.0
    )
    
    repository = AsyncProductRepository(http_client=http_client)
    service = AsyncProductService(repository=repository)
    
    # Make several requests (mix of cache hits and misses)
    products = ["PN12345", "PN67890", "PN12345", "PN11111", "PN67890"]
    
    print("\nRequests:")
    for i, pn in enumerate(products, 1):
        product = await service.get_product(pn)
        status = "found" if product else "not found"
        print(f"   {i}. {pn}: {status}")
    
    # Get cache statistics
    if http_client.cache:
        stats = http_client.cache.stats()
        hit_rate = (stats.hits / stats.requests * 100) if stats.requests > 0 else 0
        
        print(f"\nCache Statistics:")
        print(f"   Total requests: {stats.requests}")
        print(f"   Cache hits: {stats.hits}")
        print(f"   Cache misses: {stats.misses}")
        print(f"   Hit rate: {hit_rate:.1f}%")
        print(f"   Current size: {stats.size} entries")
        print(f"   Evictions: {stats.evictions}")
        
        # Expected: 2 unique products cached, 3 hits, 2 misses from first access
        # Pattern: PN12345 (miss), PN67890 (miss), PN12345 (hit), PN11111 (miss), PN67890 (hit)
        # If PN11111 doesn't exist, still counts as miss then cached as None
    
    await http_client.close()


async def example_cache_invalidation():
    """Demonstrate cache invalidation on mutations."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Cache Invalidation on Mutations")
    print("=" * 70)
    
    http_client = HttpClient(
        base_url="http://localhost/WATS",
        enable_cache=True,
        cache_ttl=300.0
    )
    
    repository = AsyncProductRepository(http_client=http_client)
    service = AsyncProductService(repository=repository)
    
    # Get product (cache miss)
    print("\n1. Initial GET (cache miss):")
    product = await service.get_product("PN12345")
    if product:
        print(f"   Product: {product.name}")
    
    # Get again (cache hit)
    print("\n2. Second GET (cache hit):")
    product = await service.get_product("PN12345")
    if product:
        print(f"   Product: {product.name} (from cache)")
    
    # Update product (invalidates cache)
    print("\n3. Update product (invalidates cache):")
    if product:
        product.description = "Updated description"
        updated = await service.update_product(product)
        print(f"   Updated: {updated.name if updated else 'Failed'}")
    
    # Get again (cache miss - cache was invalidated)
    print("\n4. GET after update (cache miss):")
    print("   Cache was invalidated by PUT request")
    product = await service.get_product("PN12345")
    if product:
        print(f"   Product: {product.name} (fresh from server)")
        print(f"   Description: {product.description}")
    
    await http_client.close()


async def example_manual_cache_control():
    """Manual cache control - bypass, clear, invalidate."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Manual Cache Control")
    print("=" * 70)
    
    http_client = HttpClient(
        base_url="http://localhost/WATS",
        enable_cache=True,
        cache_ttl=300.0
    )
    
    repository = AsyncProductRepository(http_client=http_client)
    service = AsyncProductService(repository=repository)
    
    # Cache a product
    print("\n1. Cache product:")
    product = await service.get_product("PN12345")
    print(f"   Cached: {product.name if product else 'Not found'}")
    
    # Bypass cache for single request
    print("\n2. Bypass cache (force fresh request):")
    # Note: This requires modifying repository to support cache kwarg
    # For now, demonstration only
    print("   Use: http_client.get(endpoint, cache=False)")
    
    # Clear specific entries
    print("\n3. Invalidate specific pattern:")
    http_client.invalidate_cache("/api/Product")
    print("   Invalidated all /api/Product/* entries")
    
    # Clear entire cache
    print("\n4. Clear entire cache:")
    http_client.clear_cache()
    print("   Entire cache cleared")
    
    if http_client.cache:
        stats = http_client.cache.stats()
        print(f"\n   Cache size after clear: {stats.size} entries")
    
    await http_client.close()


async def example_performance_comparison():
    """Compare performance with caching enabled vs disabled."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Performance Comparison (Cached vs Uncached)")
    print("=" * 70)
    
    # Test with caching enabled
    http_client_cached = HttpClient(
        base_url="http://localhost/WATS",
        enable_cache=True,
        cache_ttl=300.0
    )
    
    repository_cached = AsyncProductRepository(http_client=http_client_cached)
    service_cached = AsyncProductService(repository=repository_cached)
    
    # Warm up cache
    await service_cached.get_product("PN12345")
    
    # Measure 100 cached requests
    print("\n1. With caching (100 requests):")
    start = time.perf_counter()
    for _ in range(100):
        await service_cached.get_product("PN12345")
    elapsed_cached = time.perf_counter() - start
    print(f"   Total time: {elapsed_cached * 1000:.2f} ms")
    print(f"   Avg per request: {elapsed_cached / 100 * 1000:.2f} ms")
    
    await http_client_cached.close()
    
    # Test with caching disabled
    http_client_uncached = HttpClient(
        base_url="http://localhost/WATS",
        enable_cache=False
    )
    
    repository_uncached = AsyncProductRepository(http_client=http_client_uncached)
    service_uncached = AsyncProductService(repository=repository_uncached)
    
    # Measure 10 uncached requests (fewer to avoid rate limiting)
    print("\n2. Without caching (10 requests):")
    start = time.perf_counter()
    for _ in range(10):
        await service_uncached.get_product("PN12345")
    elapsed_uncached = time.perf_counter() - start
    avg_uncached = elapsed_uncached / 10
    print(f"   Total time: {elapsed_uncached * 1000:.2f} ms")
    print(f"   Avg per request: {avg_uncached * 1000:.2f} ms")
    
    # Compare
    estimated_uncached_100 = avg_uncached * 100
    speedup = estimated_uncached_100 / elapsed_cached
    print(f"\n3. Performance Comparison:")
    print(f"   Cached 100 requests: {elapsed_cached * 1000:.2f} ms")
    print(f"   Estimated uncached 100: {estimated_uncached_100 * 1000:.2f} ms")
    print(f"   Speedup: {speedup:.1f}x faster with caching")
    print(f"   Time saved: {(estimated_uncached_100 - elapsed_cached) * 1000:.2f} ms")
    
    await http_client_uncached.close()


async def example_ttl_expiration():
    """Demonstrate TTL-based cache expiration."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: TTL-Based Cache Expiration")
    print("=" * 70)
    
    # Create client with 5-second TTL for demonstration
    http_client = HttpClient(
        base_url="http://localhost/WATS",
        enable_cache=True,
        cache_ttl=5.0,  # 5 seconds (short for demo)
        cache_max_size=1000
    )
    
    repository = AsyncProductRepository(http_client=http_client)
    service = AsyncProductService(repository=repository)
    
    # Cache a product
    print("\n1. Initial request (cache miss):")
    start = time.perf_counter()
    product = await service.get_product("PN12345")
    elapsed1 = time.perf_counter() - start
    print(f"   Product: {product.name if product else 'Not found'}")
    print(f"   Time: {elapsed1 * 1000:.2f} ms")
    
    # Request within TTL (cache hit)
    print("\n2. Request within TTL (cache hit):")
    await asyncio.sleep(2)  # Wait 2 seconds (still within 5-second TTL)
    start = time.perf_counter()
    product = await service.get_product("PN12345")
    elapsed2 = time.perf_counter() - start
    print(f"   Product: {product.name if product else 'Not found'}")
    print(f"   Time: {elapsed2 * 1000:.2f} ms (from cache)")
    
    # Request after TTL expires (cache miss)
    print("\n3. Request after TTL expiration (cache miss):")
    await asyncio.sleep(4)  # Wait 4 more seconds (total 6 seconds > 5-second TTL)
    start = time.perf_counter()
    product = await service.get_product("PN12345")
    elapsed3 = time.perf_counter() - start
    print(f"   Product: {product.name if product else 'Not found'}")
    print(f"   Time: {elapsed3 * 1000:.2f} ms (cache expired, fresh from server)")
    
    print(f"\n   Cache lifecycle:")
    print(f"   - Request at t=0s: miss ({elapsed1 * 1000:.2f} ms)")
    print(f"   - Request at t=2s: hit ({elapsed2 * 1000:.2f} ms)")
    print(f"   - Request at t=6s: miss/expired ({elapsed3 * 1000:.2f} ms)")
    
    await http_client.close()


async def main():
    """Run all caching examples."""
    print("\n" + "=" * 70)
    print("HTTP Response Caching Examples")
    print("=" * 70)
    print("\nNote: These examples require a running WATS server")
    print("      Configure connection in examples/.env")
    
    try:
        await example_basic_caching()
        await example_cache_statistics()
        await example_cache_invalidation()
        await example_manual_cache_control()
        await example_performance_comparison()
        await example_ttl_expiration()
        
        print("\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Ensure WATS server is running and accessible")


if __name__ == "__main__":
    asyncio.run(main())
