"""
Threading tests for TTLCache.

Tests concurrent access patterns to ensure thread safety.
"""
import pytest
import threading
import time
import random
from pywats.core.cache import TTLCache, CacheStats


class TestTTLCacheThreadSafety:
    """Test TTLCache under concurrent access."""
    
    def test_concurrent_set_get(self):
        """Test concurrent reads and writes."""
        cache = TTLCache[str](default_ttl=60)
        errors = []
        
        def worker(thread_id: int):
            """Worker that sets and gets values."""
            try:
                for i in range(100):
                    key = f"key_{i % 10}"
                    value = f"value_{thread_id}_{i}"
                    
                    # Set value
                    cache.set(key, value)
                    
                    # Get value (may get value from other thread)
                    result = cache.get(key)
                    assert result is not None, f"Key {key} should exist"
                    
                    # Brief pause to increase interleaving
                    time.sleep(0.001)
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")
        
        # Start 10 threads
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(10)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Verify no errors occurred
        assert not errors, f"Threading errors: {errors}"
        
        # Verify cache integrity
        assert cache.size <= 10, "Should have at most 10 unique keys"
        
        # Verify stats are consistent
        stats = cache.stats
        assert stats.hits >= 0
        assert stats.misses >= 0
    
    def test_concurrent_expiration(self):
        """Test expiration cleanup with concurrent access."""
        cache = TTLCache[str](default_ttl=0.1)  # Fast expiration
        errors = []
        
        # Add items
        for i in range(50):
            cache.set(f"key_{i}", f"value_{i}")
        
        def reader(thread_id: int):
            """Reader that accesses potentially expired items."""
            try:
                for _ in range(100):
                    key = f"key_{random.randint(0, 49)}"
                    value = cache.get(key)
                    # Value may be None if expired
                    time.sleep(0.01)
            except Exception as e:
                errors.append(f"Reader {thread_id}: {e}")
        
        # Start readers
        readers = [
            threading.Thread(target=reader, args=(i,))
            for i in range(5)
        ]
        for t in readers:
            t.start()
        
        # Wait for expiration
        time.sleep(0.15)
        
        # Run cleanup concurrently with readers
        removed = cache.cleanup_expired()
        
        # Wait for readers to finish
        for t in readers:
            t.join()
        
        # Verify no errors
        assert not errors, f"Threading errors: {errors}"
        
        # Verify cleanup worked
        assert removed > 0, "Should have removed some expired items"
    
    def test_concurrent_eviction(self):
        """Test LRU eviction with concurrent access."""
        cache = TTLCache[int](default_ttl=60, max_size=20)
        errors = []
        
        def writer(thread_id: int):
            """Writer that adds items triggering evictions."""
            try:
                for i in range(50):
                    key = f"thread_{thread_id}_key_{i}"
                    cache.set(key, i)
                    time.sleep(0.001)
            except Exception as e:
                errors.append(f"Writer {thread_id}: {e}")
        
        # Start multiple writers
        writers = [
            threading.Thread(target=writer, args=(i,))
            for i in range(5)
        ]
        
        for t in writers:
            t.start()
        for t in writers:
            t.join()
        
        # Verify no errors
        assert not errors, f"Threading errors: {errors}"
        
        # Verify size constraint respected
        assert cache.size <= 20, f"Cache size {cache.size} exceeds max_size 20"
        
        # Verify evictions occurred
        stats = cache.stats
        assert stats.evictions > 0, "Evictions should have occurred"
    
    def test_concurrent_delete(self):
        """Test concurrent delete operations."""
        cache = TTLCache[str](default_ttl=60)
        errors = []
        
        # Pre-populate cache
        for i in range(50):
            cache.set(f"key_{i}", f"value_{i}")
        
        def deleter(thread_id: int):
            """Deleter that removes items."""
            try:
                for i in range(50):
                    key = f"key_{i}"
                    cache.delete(key)
                    time.sleep(0.001)
            except Exception as e:
                errors.append(f"Deleter {thread_id}: {e}")
        
        # Start multiple deleters
        deleters = [
            threading.Thread(target=deleter, args=(i,))
            for i in range(3)
        ]
        
        for t in deleters:
            t.start()
        for t in deleters:
            t.join()
        
        # Verify no errors
        assert not errors, f"Threading errors: {errors}"
        
        # All items should be deleted
        assert cache.size == 0, "All items should be deleted"
    
    def test_concurrent_clear(self):
        """Test clear() with concurrent access."""
        cache = TTLCache[str](default_ttl=60)
        errors = []
        cleared_count = 0
        lock = threading.Lock()
        
        def mixed_worker(thread_id: int):
            """Worker that mixes operations."""
            nonlocal cleared_count
            try:
                for i in range(50):
                    # Mix of operations
                    if i % 10 == 0:
                        cache.clear()
                        with lock:
                            cleared_count += 1
                    else:
                        cache.set(f"key_{thread_id}_{i}", f"value_{i}")
                        cache.get(f"key_{thread_id}_{i}")
                    time.sleep(0.001)
            except Exception as e:
                errors.append(f"Worker {thread_id}: {e}")
        
        # Start workers
        workers = [
            threading.Thread(target=mixed_worker, args=(i,))
            for i in range(5)
        ]
        
        for t in workers:
            t.start()
        for t in workers:
            t.join()
        
        # Verify no errors
        assert not errors, f"Threading errors: {errors}"
        
        # Verify clear was called
        assert cleared_count > 0, "Clear should have been called"
    
    def test_concurrent_stats_access(self):
        """Test stats access with concurrent modifications."""
        cache = TTLCache[str](default_ttl=60)
        errors = []
        
        def worker(thread_id: int):
            """Worker that triggers hits and misses."""
            try:
                for i in range(100):
                    # Mix hits and misses
                    if i % 2 == 0:
                        cache.set(f"key_{i % 10}", f"value_{thread_id}_{i}")
                    
                    cache.get(f"key_{i % 10}")  # May hit or miss
                    
                    # Check stats periodically
                    if i % 10 == 0:
                        stats = cache.stats
                        assert stats.hits >= 0
                        assert stats.misses >= 0
                        assert stats.evictions >= 0
                    
                    time.sleep(0.001)
            except Exception as e:
                errors.append(f"Worker {thread_id}: {e}")
        
        # Start workers
        workers = [
            threading.Thread(target=worker, args=(i,))
            for i in range(5)
        ]
        
        for t in workers:
            t.start()
        for t in workers:
            t.join()
        
        # Verify no errors
        assert not errors, f"Threading errors: {errors}"
        
        # Final stats should be consistent
        stats = cache.stats
        total = stats.hits + stats.misses
        assert total > 0, "Should have some cache operations"
        assert 0 <= stats.hit_rate <= 1, "Hit rate should be between 0 and 1"
    
    def test_high_contention_stress(self):
        """Stress test with high thread contention."""
        cache = TTLCache[int](default_ttl=30, max_size=100)
        errors = []
        operation_counts = {"set": 0, "get": 0, "delete": 0}
        lock = threading.Lock()
        
        def stress_worker(thread_id: int):
            """Worker that performs random operations."""
            try:
                for i in range(200):
                    op = random.choice(["set", "get", "delete"])
                    key = f"key_{random.randint(0, 50)}"
                    
                    if op == "set":
                        cache.set(key, random.randint(0, 1000))
                        with lock:
                            operation_counts["set"] += 1
                    elif op == "get":
                        cache.get(key)
                        with lock:
                            operation_counts["get"] += 1
                    else:
                        cache.delete(key)
                        with lock:
                            operation_counts["delete"] += 1
                    
                    # Minimal sleep to maximize contention
                    if i % 20 == 0:
                        time.sleep(0.001)
            except Exception as e:
                errors.append(f"Worker {thread_id}: {e}")
        
        # Start many threads
        workers = [
            threading.Thread(target=stress_worker, args=(i,))
            for i in range(20)
        ]
        
        for t in workers:
            t.start()
        for t in workers:
            t.join()
        
        # Verify no errors
        assert not errors, f"Threading errors: {errors}"
        
        # Verify operations were performed
        total_ops = sum(operation_counts.values())
        assert total_ops == 20 * 200, "All operations should complete"
        
        # Verify cache integrity
        assert cache.size <= 100, "Cache size should respect max_size"
        
        # Verify stats consistency
        stats = cache.stats
        assert stats.hits + stats.misses == operation_counts["get"]


class TestTTLCachePerformance:
    """Performance tests for TTLCache."""
    
    def test_lock_contention_benchmark(self):
        """Benchmark to measure lock contention."""
        cache = TTLCache[int](default_ttl=60, max_size=1000)
        
        # Pre-populate
        for i in range(100):
            cache.set(f"key_{i}", i)
        
        def benchmark_worker(thread_id: int):
            """Worker that performs reads."""
            for _ in range(1000):
                key = f"key_{random.randint(0, 99)}"
                cache.get(key)
        
        start = time.time()
        
        # Run with different thread counts
        for num_threads in [1, 5, 10, 20]:
            threads = [
                threading.Thread(target=benchmark_worker, args=(i,))
                for i in range(num_threads)
            ]
            
            thread_start = time.time()
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            thread_time = time.time() - thread_start
            
            # Just verify it completes reasonably fast
            assert thread_time < 5.0, f"Took too long with {num_threads} threads"
        
        total_time = time.time() - start
        assert total_time < 20.0, "Benchmark took too long overall"
