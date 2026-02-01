"""
Tests for retry wrapper functionality.

Tests Phase 2 Task 2.1: Implement Retry Wrapper
"""
import pytest
import time
from pywats.pywats import _with_retry
from pywats.core.config import RetryConfig


# ============================================================================
# Retry Logic Tests
# ============================================================================

def test_retry_success_on_first_attempt():
    """Test that successful calls don't trigger retry."""
    call_count = 0
    
    def successful_func():
        nonlocal call_count
        call_count += 1
        return "success"
    
    config = RetryConfig(max_retries=3, backoff=0.1)
    wrapped = _with_retry(successful_func, config, "test-123")
    
    result = wrapped()
    assert result == "success"
    assert call_count == 1  # Called only once


def test_retry_success_after_failures():
    """Test that retry succeeds after transient failures."""
    call_count = 0
    
    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Transient error")
        return "success"
    
    config = RetryConfig(max_retries=3, backoff=0.1)
    wrapped = _with_retry(flaky_func, config, "test-123")
    
    result = wrapped()
    assert result == "success"
    assert call_count == 3  # Failed twice, succeeded on third


def test_retry_exhausted():
    """Test that retry gives up after max attempts."""
    call_count = 0
    
    def always_fails():
        nonlocal call_count
        call_count += 1
        raise ConnectionError("Permanent error")
    
    config = RetryConfig(max_retries=2, backoff=0.1)
    wrapped = _with_retry(always_fails, config, "test-456")
    
    with pytest.raises(ConnectionError, match="Permanent error"):
        wrapped()
    
    assert call_count == 3  # Initial + 2 retries


def test_retry_backoff_timing():
    """Test that backoff delays are correct."""
    call_times = []
    
    def failing_func():
        call_times.append(time.time())
        raise TimeoutError("Always timeout")
    
    config = RetryConfig(max_retries=2, backoff=0.2)
    wrapped = _with_retry(failing_func, config, "test-789")
    
    with pytest.raises(TimeoutError):
        wrapped()
    
    # Check timing between calls
    assert len(call_times) == 3  # Initial + 2 retries
    
    # First retry should wait backoff^1 = 0.2s
    delay1 = call_times[1] - call_times[0]
    assert 0.15 < delay1 < 0.35
    
    # Second retry should wait backoff^2 = 0.04s
    delay2 = call_times[2] - call_times[1]
    assert 0.02 < delay2 < 0.08


def test_retry_on_specific_errors_only():
    """Test that retry only happens on specified error types."""
    call_count = 0
    
    def specific_error_func():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ValueError("Should not retry this")
        return "success"
    
    # Only retry on ConnectionError and TimeoutError
    config = RetryConfig(
        max_retries=3,
        backoff=0.1,
        retry_on_errors=(ConnectionError, TimeoutError)
    )
    wrapped = _with_retry(specific_error_func, config, "test-abc")
    
    # ValueError should not trigger retry
    with pytest.raises(ValueError, match="Should not retry this"):
        wrapped()
    
    assert call_count == 1  # No retry


def test_retry_with_arguments():
    """Test retry wrapper preserves function arguments."""
    call_count = 0
    
    def func_with_args(x, y, z=10):
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ConnectionError("Transient")
        return x + y + z
    
    config = RetryConfig(max_retries=2, backoff=0.1)
    wrapped = _with_retry(func_with_args, config, "test-def")
    
    result = wrapped(5, 3, z=7)
    assert result == 15
    assert call_count == 2


def test_retry_preserves_function_metadata():
    """Test that wrapper preserves function name and docstring."""
    def original_func():
        """Original docstring."""
        return "result"
    
    config = RetryConfig(max_retries=1, backoff=0.1)
    wrapped = _with_retry(original_func, config, "test-ghi")
    
    assert wrapped.__name__ == "original_func"
    assert wrapped.__doc__ == "Original docstring."


def test_retry_zero_backoff():
    """Test retry with zero backoff (immediate retry)."""
    call_count = 0
    
    def func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Transient")
        return "success"
    
    config = RetryConfig(max_retries=3, backoff=0.0)
    wrapped = _with_retry(func, config, "test-jkl")
    
    start = time.time()
    result = wrapped()
    duration = time.time() - start
    
    assert result == "success"
    assert call_count == 3
    # Should complete quickly with 0^n = 0 backoff
    assert duration < 0.2


def test_retry_exponential_backoff():
    """Test that backoff is exponential."""
    call_times = []
    
    def func():
        call_times.append(time.time())
        raise ConnectionError("Always fail")
    
    config = RetryConfig(max_retries=3, backoff=2.0)
    wrapped = _with_retry(func, config, "test-mno")
    
    with pytest.raises(ConnectionError):
        wrapped()
    
    # Should have 4 calls total (initial + 3 retries)
    assert len(call_times) == 4
    
    # Delays should be: 2s (2^1), 4s (2^2), 8s (2^3)
    # Allow some tolerance for timing
    delay1 = call_times[1] - call_times[0]
    assert 1.8 < delay1 < 2.4
    
    delay2 = call_times[2] - call_times[1]
    assert 3.6 < delay2 < 4.6
    
    delay3 = call_times[3] - call_times[2]
    assert 7.0 < delay3 < 9.0


def test_retry_max_retries_zero():
    """Test that max_retries=0 means no retries."""
    call_count = 0
    
    def func():
        nonlocal call_count
        call_count += 1
        raise ConnectionError("Fail")
    
    config = RetryConfig(max_retries=0, backoff=0.1)
    wrapped = _with_retry(func, config, "test-pqr")
    
    with pytest.raises(ConnectionError):
        wrapped()
    
    assert call_count == 1  # Only initial attempt, no retries
