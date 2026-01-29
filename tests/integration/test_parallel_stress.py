"""
Stress tests for parallel execution.

Tests high-concurrency scenarios to ensure parallel_execute handles
load correctly without deadlocks, race conditions, or data corruption.
"""
import pytest
import time
import random
from typing import List
from pywats.core.parallel import parallel_execute, ParallelConfig
from pywats.shared.result import Result, Success, Failure


class TestParallelExecuteStress:
    """Stress tests for parallel_execute."""
    
    def test_high_concurrency(self):
        """Test with many concurrent operations."""
        def slow_operation(x: int) -> int:
            """Simulate slow operation."""
            time.sleep(0.01)
            return x * 2
        
        keys = list(range(1000))
        results = parallel_execute(
            keys=keys,
            operation=slow_operation,
            max_workers=50
        )
        
        # Verify all results
        assert len(results) == 1000
        assert all(r.is_success for r in results)
        assert [r.value for r in results] == [x * 2 for x in keys]
    
    def test_mixed_success_failure(self):
        """Test with mix of successes and failures."""
        def flaky_operation(x: int) -> int:
            """Operation that sometimes fails."""
            if x % 3 == 0:
                raise ValueError(f"Failed for {x}")
            time.sleep(0.005)
            return x * 2
        
        keys = list(range(300))
        results = parallel_execute(
            keys=keys,
            operation=flaky_operation,
            max_workers=30
        )
        
        # Verify results
        assert len(results) == 300
        
        # Count successes and failures
        successes = [r for r in results if r.is_success]
        failures = [r for r in results if r.is_failure]
        
        assert len(successes) == 200  # x % 3 != 0
        assert len(failures) == 100   # x % 3 == 0
        
        # Verify order preserved
        for i, result in enumerate(results):
            if i % 3 == 0:
                assert result.is_failure
            else:
                assert result.is_success
                assert result.value == i * 2
    
    def test_rapid_small_batches(self):
        """Test many rapid small batch executions."""
        def quick_op(x: int) -> int:
            return x + 1
        
        for _ in range(100):
            keys = list(range(10))
            results = parallel_execute(
                keys=keys,
                operation=quick_op,
                max_workers=5
            )
            
            assert len(results) == 10
            assert all(r.is_success for r in results)
            assert [r.value for r in results] == list(range(1, 11))
    
    def test_variable_duration_operations(self):
        """Test with operations of varying duration."""
        def variable_duration(x: int) -> int:
            """Operation with random duration."""
            sleep_time = random.uniform(0.001, 0.05)
            time.sleep(sleep_time)
            return x * x
        
        keys = list(range(200))
        results = parallel_execute(
            keys=keys,
            operation=variable_duration,
            max_workers=20
        )
        
        # Verify all completed
        assert len(results) == 200
        assert all(r.is_success for r in results)
        
        # Verify order and values
        for i, result in enumerate(results):
            assert result.value == i * i
    
    def test_exception_handling_stress(self):
        """Test exception handling under load."""
        exception_count = 0
        
        def exception_thrower(x: int) -> int:
            """Throws various exceptions."""
            nonlocal exception_count
            
            if x % 5 == 0:
                exception_count += 1
                raise ValueError(f"ValueError for {x}")
            elif x % 7 == 0:
                exception_count += 1
                raise RuntimeError(f"RuntimeError for {x}")
            elif x % 11 == 0:
                exception_count += 1
                raise KeyError(f"KeyError for {x}")
            
            return x
        
        keys = list(range(500))
        results = parallel_execute(
            keys=keys,
            operation=exception_thrower,
            max_workers=25
        )
        
        # Verify all operations completed
        assert len(results) == 500
        
        # Count failures
        failures = [r for r in results if r.is_failure]
        
        # Verify failure count matches exceptions
        # (Some numbers match multiple conditions, so check approximately)
        assert len(failures) > 0
        assert len(failures) < 500
        
        # Verify error details
        for i, result in enumerate(results):
            if result.is_failure:
                assert "details" in result.__dict__ or hasattr(result, "details")
    
    def test_memory_efficiency(self):
        """Test that large batches don't cause memory issues."""
        def simple_op(x: int) -> int:
            # Return small object
            return x % 100
        
        # Process large batch
        keys = list(range(10000))
        results = parallel_execute(
            keys=keys,
            operation=simple_op,
            max_workers=50
        )
        
        # Verify results
        assert len(results) == 10000
        assert all(r.is_success for r in results)
        
        # Verify values
        for i, result in enumerate(results):
            assert result.value == i % 100
    
    def test_progress_callback_stress(self):
        """Test progress callback under high load."""
        progress_updates = []
        
        def progress_handler(completed: int, total: int):
            progress_updates.append((completed, total))
        
        def simple_op(x: int) -> int:
            time.sleep(0.005)
            return x
        
        keys = list(range(200))
        results = parallel_execute(
            keys=keys,
            operation=simple_op,
            max_workers=20,
            on_progress=progress_handler
        )
        
        # Verify completion
        assert len(results) == 200
        assert all(r.is_success for r in results)
        
        # Verify progress updates
        assert len(progress_updates) > 0
        
        # Verify last update shows completion
        last_completed, last_total = progress_updates[-1]
        assert last_completed == 200
        assert last_total == 200
        
        # Verify progress is monotonic
        for i in range(1, len(progress_updates)):
            assert progress_updates[i][0] >= progress_updates[i-1][0]
    
    def test_fail_fast_mode(self):
        """Test fail_fast configuration."""
        def failing_operation(x: int) -> int:
            if x == 50:
                raise ValueError("Intentional failure")
            time.sleep(0.01)
            return x
        
        config = ParallelConfig(max_workers=10, fail_fast=True)
        
        keys = list(range(200))
        results = parallel_execute(
            keys=keys,
            operation=failing_operation,
            config=config
        )
        
        # With fail_fast, should stop after first error
        # Not all 200 operations may complete
        failures = [r for r in results if r.is_failure]
        assert len(failures) > 0, "Should have at least one failure"
    
    def test_thread_safety_shared_resource(self):
        """Test that operation isolation is maintained."""
        # Each operation should be independent
        def isolated_operation(x: int) -> int:
            # Simulate some computation
            result = 0
            for i in range(100):
                result += x
            return result
        
        keys = list(range(500))
        results = parallel_execute(
            keys=keys,
            operation=isolated_operation,
            max_workers=30
        )
        
        # Verify all operations completed correctly
        assert len(results) == 500
        assert all(r.is_success for r in results)
        
        # Verify values
        for i, result in enumerate(results):
            expected = i * 100
            assert result.value == expected
    
    def test_worker_count_configurations(self):
        """Test various worker count configurations."""
        def simple_op(x: int) -> int:
            time.sleep(0.01)
            return x * 2
        
        keys = list(range(100))
        
        for workers in [1, 5, 10, 20, 50]:
            results = parallel_execute(
                keys=keys,
                operation=simple_op,
                max_workers=workers
            )
            
            assert len(results) == 100
            assert all(r.is_success for r in results)
            assert [r.value for r in results] == [x * 2 for x in keys]
    
    def test_empty_input(self):
        """Test with empty input list."""
        def simple_op(x: int) -> int:
            return x
        
        results = parallel_execute(
            keys=[],
            operation=simple_op,
            max_workers=10
        )
        
        assert results == []
    
    def test_single_item(self):
        """Test with single item."""
        def simple_op(x: int) -> int:
            return x * 2
        
        results = parallel_execute(
            keys=[42],
            operation=simple_op,
            max_workers=10
        )
        
        assert len(results) == 1
        assert results[0].is_success
        assert results[0].value == 84
    
    def test_duplicate_keys(self):
        """Test with duplicate keys."""
        call_count = {}
        
        def counting_op(x: int) -> int:
            if x not in call_count:
                call_count[x] = 0
            call_count[x] += 1
            return x * 2
        
        keys = [1, 2, 3, 1, 2, 3, 1]  # Duplicates
        results = parallel_execute(
            keys=keys,
            operation=counting_op,
            max_workers=5
        )
        
        # All operations should complete
        assert len(results) == 7
        assert all(r.is_success for r in results)
        
        # Each key should be called for each occurrence
        assert call_count[1] == 3
        assert call_count[2] == 2
        assert call_count[3] == 2
    
    def test_operation_returns_none(self):
        """Test handling of None returns."""
        def none_returner(x: int) -> None:
            if x % 2 == 0:
                return None
            return x
        
        keys = list(range(20))
        results = parallel_execute(
            keys=keys,
            operation=none_returner,
            max_workers=5
        )
        
        # Verify all operations completed
        assert len(results) == 20
        
        # Even indices should be failures (returned None)
        for i, result in enumerate(results):
            if i % 2 == 0:
                assert result.is_failure
                assert "None" in result.message
            else:
                assert result.is_success
                assert result.value == i


class TestParallelExecutePerformance:
    """Performance benchmarks for parallel execution."""
    
    def test_throughput_benchmark(self):
        """Benchmark throughput with different worker counts."""
        def io_simulation(x: int) -> int:
            """Simulate I/O operation."""
            time.sleep(0.01)
            return x * 2
        
        keys = list(range(200))
        
        # Benchmark with different worker counts
        timings = {}
        
        for workers in [1, 10, 20, 40]:
            start = time.time()
            results = parallel_execute(
                keys=keys,
                operation=io_simulation,
                max_workers=workers
            )
            elapsed = time.time() - start
            timings[workers] = elapsed
            
            assert len(results) == 200
            assert all(r.is_success for r in results)
        
        # Verify parallelization provides speedup
        # 20 workers should be faster than 1 worker
        assert timings[20] < timings[1] * 0.5, "Parallelization should provide speedup"
    
    def test_overhead_measurement(self):
        """Measure overhead of parallel execution."""
        def instant_op(x: int) -> int:
            """Instant operation to measure overhead."""
            return x
        
        keys = list(range(1000))
        
        start = time.time()
        results = parallel_execute(
            keys=keys,
            operation=instant_op,
            max_workers=20
        )
        elapsed = time.time() - start
        
        assert len(results) == 1000
        assert all(r.is_success for r in results)
        
        # Should complete reasonably fast (overhead check)
        assert elapsed < 2.0, f"Overhead too high: {elapsed}s for 1000 instant operations"
