"""
Performance Benchmarking Examples for PyWATS

Demonstrates how to benchmark and measure:
- HTTP cache performance (hit rates, response times)
- Memory usage with different cache configurations
- Concurrent request performance
- Cache vs no-cache comparisons

Run with: python examples/performance/benchmarks.py
"""

import asyncio
import time
import tracemalloc
from typing import List, Dict, Any
from dataclasses import dataclass
from statistics import mean, median, stdev

from pywats import AsyncWATS


@dataclass
class BenchmarkResult:
    """Results from a benchmark run"""
    name: str
    total_requests: int
    duration_seconds: float
    requests_per_second: float
    avg_response_time_ms: float
    median_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    cache_hit_rate: float = 0.0
    memory_mb: float = 0.0
    
    def __str__(self) -> str:
        return f"""
Benchmark: {self.name}
─────────────────────────────────────────
Total Requests:     {self.total_requests}
Duration:           {self.duration_seconds:.2f}s
Requests/sec:       {self.requests_per_second:.2f}
Avg Response Time:  {self.avg_response_time_ms:.2f}ms
Median Response:    {self.median_response_time_ms:.2f}ms
P95 Response:       {self.p95_response_time_ms:.2f}ms
P99 Response:       {self.p99_response_time_ms:.2f}ms
Cache Hit Rate:     {self.cache_hit_rate:.1%}
Memory Usage:       {self.memory_mb:.2f}MB
"""


async def benchmark_cache_performance(
    base_url: str,
    token: str,
    num_requests: int = 100,
    cache_enabled: bool = True
) -> BenchmarkResult:
    """
    Benchmark cache performance by making repeated requests.
    
    Args:
        base_url: WATS server URL
        token: API token
        num_requests: Number of requests to make
        cache_enabled: Whether to enable caching
        
    Returns:
        BenchmarkResult with performance metrics
    """
    response_times: List[float] = []
    
    # Start memory tracking
    tracemalloc.start()
    
    async with AsyncWATS(
        base_url=base_url,
        token=token,
        enable_cache=cache_enabled,
        cache_ttl=300.0,
        cache_max_size=1000
    ) as api:
        
        start_time = time.time()
        
        # Make repeated requests (should hit cache if enabled)
        for i in range(num_requests):
            request_start = time.time()
            
            # Alternate between endpoints to test cache
            if i % 3 == 0:
                await api.product.get_products(max_results=10)
            elif i % 3 == 1:
                await api.process.get_processes()
            else:
                await api.product.get_products(max_results=20)
            
            request_duration = (time.time() - request_start) * 1000  # ms
            response_times.append(request_duration)
        
        duration = time.time() - start_time
        
        # Get cache statistics
        cache_hit_rate = 0.0
        if cache_enabled and api._http_client.cache:
            stats = api._http_client.cache.stats()
            total = stats.get('total_requests', 0)
            hits = stats.get('hits', 0)
            cache_hit_rate = hits / total if total > 0 else 0.0
        
        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_mb = peak / 1024 / 1024
    
    # Calculate statistics
    response_times.sort()
    p95_index = int(len(response_times) * 0.95)
    p99_index = int(len(response_times) * 0.99)
    
    return BenchmarkResult(
        name=f"Cache {'Enabled' if cache_enabled else 'Disabled'}",
        total_requests=num_requests,
        duration_seconds=duration,
        requests_per_second=num_requests / duration,
        avg_response_time_ms=mean(response_times),
        median_response_time_ms=median(response_times),
        p95_response_time_ms=response_times[p95_index],
        p99_response_time_ms=response_times[p99_index],
        cache_hit_rate=cache_hit_rate,
        memory_mb=memory_mb
    )


async def benchmark_concurrent_requests(
    base_url: str,
    token: str,
    num_concurrent: int = 10,
    cache_enabled: bool = True
) -> BenchmarkResult:
    """
    Benchmark concurrent request performance.
    
    Args:
        base_url: WATS server URL
        token: API token
        num_concurrent: Number of concurrent requests
        cache_enabled: Whether to enable caching
        
    Returns:
        BenchmarkResult with performance metrics
    """
    response_times: List[float] = []
    
    tracemalloc.start()
    
    async with AsyncWATS(
        base_url=base_url,
        token=token,
        enable_cache=cache_enabled,
        cache_ttl=300.0,
        cache_max_size=1000
    ) as api:
        
        async def make_request(request_id: int) -> None:
            """Single request task"""
            request_start = time.time()
            
            # Mix of different endpoints
            if request_id % 3 == 0:
                await api.product.get_products(max_results=10)
            elif request_id % 3 == 1:
                await api.process.get_processes()
            else:
                await api.report.get_reports(max_results=20)
            
            duration = (time.time() - request_start) * 1000
            response_times.append(duration)
        
        start_time = time.time()
        
        # Create concurrent tasks
        tasks = [make_request(i) for i in range(num_concurrent)]
        await asyncio.gather(*tasks)
        
        duration = time.time() - start_time
        
        # Get cache statistics
        cache_hit_rate = 0.0
        if cache_enabled and api._http_client.cache:
            stats = api._http_client.cache.stats()
            total = stats.get('total_requests', 0)
            hits = stats.get('hits', 0)
            cache_hit_rate = hits / total if total > 0 else 0.0
        
        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_mb = peak / 1024 / 1024
    
    # Calculate statistics
    response_times.sort()
    p95_index = int(len(response_times) * 0.95)
    p99_index = int(len(response_times) * 0.99)
    
    return BenchmarkResult(
        name=f"Concurrent ({num_concurrent} requests)",
        total_requests=num_concurrent,
        duration_seconds=duration,
        requests_per_second=num_concurrent / duration,
        avg_response_time_ms=mean(response_times),
        median_response_time_ms=median(response_times),
        p95_response_time_ms=response_times[p95_index],
        p99_response_time_ms=response_times[p99_index],
        cache_hit_rate=cache_hit_rate,
        memory_mb=memory_mb
    )


async def benchmark_cache_sizes(
    base_url: str,
    token: str,
    num_requests: int = 50
) -> List[BenchmarkResult]:
    """
    Benchmark different cache size configurations.
    
    Args:
        base_url: WATS server URL
        token: API token
        num_requests: Number of requests per test
        
    Returns:
        List of BenchmarkResults for each cache size
    """
    results = []
    cache_sizes = [100, 500, 1000, 2000]
    
    for cache_size in cache_sizes:
        response_times: List[float] = []
        
        tracemalloc.start()
        
        async with AsyncWATS(
            base_url=base_url,
            token=token,
            enable_cache=True,
            cache_ttl=300.0,
            cache_max_size=cache_size
        ) as api:
            
            start_time = time.time()
            
            # Make requests with some variation
            for i in range(num_requests):
                request_start = time.time()
                
                # Request different products to test cache size limits
                product_id = f"PROD-{i % (cache_size // 2)}"
                await api.product.get_products(max_results=10)
                
                duration = (time.time() - request_start) * 1000
                response_times.append(duration)
            
            duration = time.time() - start_time
            
            # Get cache statistics
            cache_hit_rate = 0.0
            if api._http_client.cache:
                stats = api._http_client.cache.stats()
                total = stats.get('total_requests', 0)
                hits = stats.get('hits', 0)
                cache_hit_rate = hits / total if total > 0 else 0.0
            
            # Get memory usage
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_mb = peak / 1024 / 1024
        
        # Calculate statistics
        response_times.sort()
        p95_index = int(len(response_times) * 0.95)
        p99_index = int(len(response_times) * 0.99)
        
        result = BenchmarkResult(
            name=f"Cache Size {cache_size}",
            total_requests=num_requests,
            duration_seconds=duration,
            requests_per_second=num_requests / duration,
            avg_response_time_ms=mean(response_times),
            median_response_time_ms=median(response_times),
            p95_response_time_ms=response_times[p95_index],
            p99_response_time_ms=response_times[p99_index],
            cache_hit_rate=cache_hit_rate,
            memory_mb=memory_mb
        )
        results.append(result)
    
    return results


async def compare_cache_vs_no_cache(
    base_url: str,
    token: str,
    num_requests: int = 50
) -> None:
    """
    Compare performance with and without caching.
    
    Args:
        base_url: WATS server URL
        token: API token
        num_requests: Number of requests to make
    """
    print("=" * 60)
    print("CACHE VS NO-CACHE COMPARISON")
    print("=" * 60)
    
    # Benchmark with cache disabled
    print("\n🔴 Running benchmark WITHOUT cache...")
    no_cache_result = await benchmark_cache_performance(
        base_url, token, num_requests, cache_enabled=False
    )
    print(no_cache_result)
    
    # Benchmark with cache enabled
    print("\n🟢 Running benchmark WITH cache...")
    cache_result = await benchmark_cache_performance(
        base_url, token, num_requests, cache_enabled=True
    )
    print(cache_result)
    
    # Calculate improvements
    print("\n📊 PERFORMANCE IMPROVEMENTS:")
    print("─────────────────────────────────────────")
    
    speedup = cache_result.requests_per_second / no_cache_result.requests_per_second
    print(f"Throughput Improvement:  {speedup:.2f}x faster")
    
    response_improvement = (
        (no_cache_result.avg_response_time_ms - cache_result.avg_response_time_ms) 
        / no_cache_result.avg_response_time_ms * 100
    )
    print(f"Response Time Reduction: {response_improvement:.1f}% faster")
    
    print(f"Cache Hit Rate:          {cache_result.cache_hit_rate:.1%}")
    print(f"Memory Overhead:         {cache_result.memory_mb - no_cache_result.memory_mb:.2f}MB")


async def run_all_benchmarks(base_url: str, token: str) -> None:
    """
    Run complete benchmark suite.
    
    Args:
        base_url: WATS server URL
        token: API token
    """
    print("\n" + "=" * 60)
    print("PYWATS PERFORMANCE BENCHMARK SUITE")
    print("=" * 60)
    print(f"\nServer: {base_url}")
    print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Test 1: Cache vs No Cache
    await compare_cache_vs_no_cache(base_url, token, num_requests=100)
    
    # Test 2: Concurrent Requests
    print("\n" + "=" * 60)
    print("CONCURRENT REQUEST BENCHMARK")
    print("=" * 60)
    
    for concurrency in [5, 10, 20]:
        print(f"\n🔀 Running {concurrency} concurrent requests...")
        result = await benchmark_concurrent_requests(
            base_url, token, num_concurrent=concurrency, cache_enabled=True
        )
        print(result)
    
    # Test 3: Cache Size Comparison
    print("\n" + "=" * 60)
    print("CACHE SIZE BENCHMARK")
    print("=" * 60)
    print("\nTesting different cache sizes...")
    
    cache_size_results = await benchmark_cache_sizes(base_url, token, num_requests=100)
    
    print("\n📊 CACHE SIZE COMPARISON:")
    print("─────────────────────────────────────────")
    print(f"{'Size':<12} {'Hit Rate':<12} {'Avg Time':<12} {'Memory':<12}")
    print("─────────────────────────────────────────")
    
    for result in cache_size_results:
        cache_size = result.name.split()[-1]
        print(
            f"{cache_size:<12} "
            f"{result.cache_hit_rate:.1%}{'':6} "
            f"{result.avg_response_time_ms:.2f}ms{'':6} "
            f"{result.memory_mb:.2f}MB"
        )
    
    print("\n" + "=" * 60)
    print("BENCHMARK SUITE COMPLETE")
    print("=" * 60)
    print(f"\nFinished: {time.strftime('%Y-%m-%d %H:%M:%S')}")


async def main():
    """Main entry point"""
    
    # Configuration
    BASE_URL = "https://your-wats-server.com"
    API_TOKEN = "your-api-token-here"
    
    # Check for credentials
    import os
    base_url = os.environ.get("PYWATS_SERVER_URL", BASE_URL)
    token = os.environ.get("PYWATS_API_TOKEN", API_TOKEN)
    
    if base_url == BASE_URL or token == API_TOKEN:
        print("⚠️  Please configure credentials:")
        print("   export PYWATS_SERVER_URL='https://your-server.com'")
        print("   export PYWATS_API_TOKEN='your-token'")
        print("\nOr edit this file to set BASE_URL and API_TOKEN")
        return
    
    try:
        await run_all_benchmarks(base_url, token)
    except KeyboardInterrupt:
        print("\n\n⚠️  Benchmark interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
