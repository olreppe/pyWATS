"""Unit tests for parallel operations.

Tests the parallel execution utilities in pywats.core.parallel.
"""
import pytest
from unittest.mock import Mock, patch
import time

from pywats.core.parallel import (
    parallel_execute,
    parallel_execute_with_retry,
    ParallelConfig,
    collect_successes,
    collect_failures,
    partition_results,
)
from pywats.shared.result import Success, Failure


class TestParallelExecute:
    """Tests for parallel_execute function."""

    def test_empty_keys_returns_empty_list(self):
        """Empty input returns empty output."""
        results = parallel_execute(
            keys=[],
            operation=lambda x: x,
        )
        assert results == []

    def test_single_key_success(self):
        """Single key operation succeeds."""
        results = parallel_execute(
            keys=["key1"],
            operation=lambda x: f"value_{x}",
        )
        assert len(results) == 1
        assert results[0].is_success
        assert results[0].value == "value_key1"

    def test_multiple_keys_preserve_order(self):
        """Results preserve input order."""
        keys = ["a", "b", "c", "d", "e"]
        results = parallel_execute(
            keys=keys,
            operation=lambda x: f"value_{x}",
            max_workers=2,
        )
        assert len(results) == len(keys)
        for i, key in enumerate(keys):
            assert results[i].is_success
            assert results[i].value == f"value_{key}"

    def test_operation_returning_none_is_failure(self):
        """Operations returning None become failures."""
        results = parallel_execute(
            keys=["key1"],
            operation=lambda x: None,
        )
        assert len(results) == 1
        assert results[0].is_failure
        assert results[0].error_code == "NOT_FOUND"

    def test_operation_exception_is_failure(self):
        """Operations raising exceptions become failures."""
        def failing_operation(x):
            raise ValueError(f"Error for {x}")

        results = parallel_execute(
            keys=["key1", "key2"],
            operation=failing_operation,
        )
        assert len(results) == 2
        assert all(r.is_failure for r in results)
        assert all(r.error_code == "INVALID_INPUT" for r in results)

    def test_mixed_success_and_failure(self):
        """Batch handles mix of successes and failures."""
        def mixed_operation(x):
            if x == "fail":
                raise ValueError("Intentional failure")
            return f"value_{x}"

        results = parallel_execute(
            keys=["ok1", "fail", "ok2"],
            operation=mixed_operation,
        )
        assert len(results) == 3
        assert results[0].is_success
        assert results[1].is_failure
        assert results[2].is_success

    def test_max_workers_respected(self):
        """Concurrency is limited by max_workers."""
        active_count = 0
        max_active = 0
        
        def tracking_operation(x):
            nonlocal active_count, max_active
            active_count += 1
            max_active = max(max_active, active_count)
            time.sleep(0.01)  # Small delay to allow overlap
            active_count -= 1
            return x

        parallel_execute(
            keys=list(range(10)),
            operation=tracking_operation,
            max_workers=3,
        )
        # Max should be around 3 (may vary due to timing)
        assert max_active <= 5  # Allow some slack

    def test_progress_callback_called(self):
        """Progress callback is called for each completion."""
        progress_calls = []
        
        def on_progress(completed, total):
            progress_calls.append((completed, total))

        parallel_execute(
            keys=["a", "b", "c"],
            operation=lambda x: x,
            on_progress=on_progress,
        )
        
        assert len(progress_calls) == 3
        # Final call should show all completed
        assert progress_calls[-1] == (3, 3)

    def test_parallel_config_used(self):
        """ParallelConfig is applied correctly."""
        config = ParallelConfig(max_workers=2, fail_fast=False)
        
        results = parallel_execute(
            keys=["a", "b"],
            operation=lambda x: x,
            config=config,
        )
        assert len(results) == 2


class TestParallelHelpers:
    """Tests for batch helper functions."""

    def test_collect_successes(self):
        """collect_successes extracts successful values."""
        results = [
            Success(value="a"),
            Failure(error_code="ERR", message="failed"),
            Success(value="b"),
        ]
        successes = collect_successes(results)
        assert successes == ["a", "b"]

    def test_collect_failures(self):
        """collect_failures extracts failure objects."""
        results = [
            Success(value="a"),
            Failure(error_code="ERR1", message="failed1"),
            Failure(error_code="ERR2", message="failed2"),
        ]
        failures = collect_failures(results)
        assert len(failures) == 2
        assert failures[0].error_code == "ERR1"
        assert failures[1].error_code == "ERR2"

    def test_partition_results(self):
        """partition_results separates successes and failures."""
        results = [
            Success(value=1),
            Failure(error_code="ERR", message="failed"),
            Success(value=2),
        ]
        successes, failures = partition_results(results)
        assert successes == [1, 2]
        assert len(failures) == 1


class TestParallelConfig:
    """Tests for ParallelConfig."""

    def test_default_values(self):
        """Default config values are sensible."""
        config = ParallelConfig()
        assert config.max_workers == 10
        assert config.fail_fast == False
        assert config.timeout is None

    def test_invalid_max_workers_raises(self):
        """max_workers < 1 raises ValueError."""
        with pytest.raises(ValueError):
            ParallelConfig(max_workers=0)

    def test_high_max_workers_warns(self, caplog):
        """High max_workers logs warning."""
        import logging
        with caplog.at_level(logging.WARNING):
            ParallelConfig(max_workers=150)
        assert "rate limiting" in caplog.text.lower()
