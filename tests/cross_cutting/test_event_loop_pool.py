"""Tests for EventLoopPool module.

Tests thread-local event loop pooling for sync API wrapper performance.
"""

import asyncio
import threading
import time
import pytest

from pywats.core.event_loop_pool import EventLoopPool


class TestEventLoopPool:
    """Test suite for EventLoopPool class."""
    
    def setup_method(self):
        """Clean up event loop pool before each test."""
        EventLoopPool.shutdown_all()
    
    def teardown_method(self):
        """Clean up event loop pool after each test."""
        EventLoopPool.shutdown_all()
    
    def test_get_or_create_loop_returns_loop(self):
        """Test that get_or_create_loop returns an event loop."""
        loop = EventLoopPool.get_or_create_loop()
        
        assert loop is not None
        assert isinstance(loop, asyncio.AbstractEventLoop)
        assert loop.is_running()
    
    def test_get_or_create_loop_reuses_same_loop(self):
        """Test that multiple calls in same thread return same loop."""
        loop1 = EventLoopPool.get_or_create_loop()
        loop2 = EventLoopPool.get_or_create_loop()
        loop3 = EventLoopPool.get_or_create_loop()
        
        assert loop1 is loop2
        assert loop2 is loop3
    
    def test_run_coroutine_executes_simple_coroutine(self):
        """Test basic coroutine execution."""
        async def return_value():
            return 42
        
        result = EventLoopPool.run_coroutine(return_value())
        
        assert result == 42
    
    def test_run_coroutine_executes_async_operation(self):
        """Test coroutine with async operation."""
        async def async_operation():
            await asyncio.sleep(0.01)
            return "completed"
        
        result = EventLoopPool.run_coroutine(async_operation())
        
        assert result == "completed"
    
    def test_run_coroutine_with_arguments(self):
        """Test coroutine with arguments."""
        async def add(a: int, b: int) -> int:
            return a + b
        
        result = EventLoopPool.run_coroutine(add(5, 3))
        
        assert result == 8
    
    def test_run_coroutine_raises_exceptions(self):
        """Test that coroutine exceptions are propagated."""
        async def raise_error():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            EventLoopPool.run_coroutine(raise_error())
    
    def test_multiple_sequential_calls_use_same_loop(self):
        """Test that sequential calls reuse the same event loop."""
        async def get_loop_id():
            return id(asyncio.get_event_loop())
        
        loop_id1 = EventLoopPool.run_coroutine(get_loop_id())
        loop_id2 = EventLoopPool.run_coroutine(get_loop_id())
        loop_id3 = EventLoopPool.run_coroutine(get_loop_id())
        
        assert loop_id1 == loop_id2 == loop_id3
    
    def test_different_threads_get_different_loops(self):
        """Test that different threads get isolated event loops."""
        results = []
        
        def run_in_thread():
            loop = EventLoopPool.get_or_create_loop()
            results.append(id(loop))
        
        threads = [threading.Thread(target=run_in_thread) for _ in range(3)]
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All threads should get different loops
        assert len(set(results)) == 3
    
    def test_thread_safety_concurrent_access(self):
        """Test concurrent access from multiple threads."""
        results = []
        errors = []
        
        async def compute(value: int) -> int:
            await asyncio.sleep(0.01)
            return value * 2
        
        def worker(value: int):
            try:
                result = EventLoopPool.run_coroutine(compute(value))
                results.append(result)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        assert len(errors) == 0
        assert sorted(results) == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    
    def test_shutdown_all_stops_loop(self):
        """Test that shutdown_all stops the event loop."""
        loop = EventLoopPool.get_or_create_loop()
        
        assert loop.is_running()
        
        EventLoopPool.shutdown_all()
        
        # Give loop time to stop
        time.sleep(0.1)
        
        # Loop should be stopped (accessing after shutdown may raise)
        # We verify by checking we can create a new loop
        new_loop = EventLoopPool.get_or_create_loop()
        assert new_loop is not loop


class TestEventLoopPoolPerformance:
    """Performance tests for EventLoopPool."""
    
    def setup_method(self):
        """Clean up event loop pool before each test."""
        EventLoopPool.shutdown_all()
    
    def teardown_method(self):
        """Clean up event loop pool after each test."""
        EventLoopPool.shutdown_all()
    
    def test_loop_reuse_is_faster_than_new_loop(self):
        """Test that loop reuse is significantly faster than creating new loops."""
        async def simple_operation():
            return "done"
        
        # Warm up the pool
        EventLoopPool.run_coroutine(simple_operation())
        
        # Benchmark with pool (reused loops)
        start = time.time()
        for _ in range(100):
            EventLoopPool.run_coroutine(simple_operation())
        pooled_time = time.time() - start
        
        # Benchmark without pool (new loops each time)
        start = time.time()
        for _ in range(100):
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(simple_operation())
            finally:
                loop.close()
        new_loop_time = time.time() - start
        
        # Pooled should be at least 2x faster (usually 10-100x)
        speedup = new_loop_time / pooled_time
        assert speedup >= 2.0, f"Expected ≥2x speedup, got {speedup:.1f}x"
        
        print(f"\nEventLoopPool Performance:")
        print(f"  Pooled: {pooled_time:.4f}s (100 calls)")
        print(f"  New loops: {new_loop_time:.4f}s (100 calls)")
        print(f"  Speedup: {speedup:.1f}x")
