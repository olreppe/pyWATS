"""Tests for CircuitBreaker pattern."""

import time
import pytest
from unittest.mock import Mock

from pywats.core.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    CircuitState
)


class TestCircuitBreakerBasics:
    """Basic circuit breaker functionality tests."""
    
    def test_initial_state_is_closed(self):
        """Test circuit breaker starts in CLOSED state."""
        breaker = CircuitBreaker("test")
        
        assert breaker.state == CircuitState.CLOSED
        assert breaker.is_closed
        assert not breaker.is_open
        assert not breaker.is_half_open
    
    def test_successful_call_returns_result(self):
        """Test successful calls pass through."""
        breaker = CircuitBreaker("test")
        
        result = breaker.call(lambda: "success")
        
        assert result == "success"
        assert breaker.is_closed
    
    def test_multiple_successes_keep_circuit_closed(self):
        """Test multiple successes maintain CLOSED state."""
        breaker = CircuitBreaker("test")
        
        for i in range(10):
            result = breaker.call(lambda: i)
            assert result == i
        
        assert breaker.is_closed
    
    def test_exception_propagates_to_caller(self):
        """Test exceptions are raised to caller."""
        breaker = CircuitBreaker("test")
        
        with pytest.raises(ValueError, match="test error"):
            breaker.call(lambda: (_ for _ in ()).throw(ValueError("test error")))


class TestCircuitBreakerStateTransitions:
    """Test state transitions: CLOSED → OPEN → HALF_OPEN → CLOSED."""
    
    def test_opens_after_failure_threshold(self):
        """Test circuit opens after consecutive failures."""
        config = CircuitBreakerConfig(failure_threshold=3)
        breaker = CircuitBreaker("test", config)
        
        # Cause 3 failures
        for _ in range(3):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        assert breaker.is_open
    
    def test_fails_fast_when_open(self):
        """Test circuit breaker fails fast when OPEN."""
        config = CircuitBreakerConfig(failure_threshold=2)
        breaker = CircuitBreaker("test", config)
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        # Next call should fail immediately with CircuitBreakerOpenError
        with pytest.raises(CircuitBreakerOpenError, match="is OPEN"):
            breaker.call(lambda: "should not execute")
    
    def test_transitions_to_half_open_after_timeout(self):
        """Test OPEN → HALF_OPEN transition after timeout."""
        config = CircuitBreakerConfig(
            failure_threshold=2,
            timeout_seconds=0.1  # Short timeout for test
        )
        breaker = CircuitBreaker("test", config)
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        assert breaker.is_open
        
        # Wait for timeout
        time.sleep(0.15)
        
        # Next call should transition to HALF_OPEN and execute
        result = breaker.call(lambda: "recovery")
        
        assert result == "recovery"
        assert breaker.is_half_open
    
    def test_closes_from_half_open_after_successes(self):
        """Test HALF_OPEN → CLOSED after success threshold."""
        config = CircuitBreakerConfig(
            failure_threshold=2,
            success_threshold=2,
            timeout_seconds=0.1
        )
        breaker = CircuitBreaker("test", config)
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        # Wait for timeout
        time.sleep(0.15)
        
        # Make 2 successful calls (success threshold)
        breaker.call(lambda: "success1")
        assert breaker.is_half_open
        
        breaker.call(lambda: "success2")
        assert breaker.is_closed  # Should be closed now
    
    def test_reopens_from_half_open_on_failure(self):
        """Test HALF_OPEN → OPEN on any failure."""
        config = CircuitBreakerConfig(
            failure_threshold=2,
            timeout_seconds=0.1
        )
        breaker = CircuitBreaker("test", config)
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        # Wait for timeout
        time.sleep(0.15)
        
        # First call succeeds (HALF_OPEN)
        breaker.call(lambda: "success")
        assert breaker.is_half_open
        
        # Second call fails (should reopen)
        with pytest.raises(RuntimeError):
            breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail again")))
        
        assert breaker.is_open


class TestCircuitBreakerConfiguration:
    """Test circuit breaker configuration options."""
    
    def test_custom_failure_threshold(self):
        """Test custom failure threshold."""
        config = CircuitBreakerConfig(failure_threshold=5)
        breaker = CircuitBreaker("test", config)
        
        # 4 failures shouldn't open
        for _ in range(4):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        assert breaker.is_closed
        
        # 5th failure should open
        with pytest.raises(RuntimeError):
            breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        assert breaker.is_open
    
    def test_custom_success_threshold(self):
        """Test custom success threshold."""
        config = CircuitBreakerConfig(
            failure_threshold=1,
            success_threshold=3,
            timeout_seconds=0.1
        )
        breaker = CircuitBreaker("test", config)
        
        # Open circuit
        with pytest.raises(RuntimeError):
            breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        time.sleep(0.15)
        
        # Need 3 successes to close
        breaker.call(lambda: "s1")
        assert breaker.is_half_open
        
        breaker.call(lambda: "s2")
        assert breaker.is_half_open
        
        breaker.call(lambda: "s3")
        assert breaker.is_closed
    
    def test_excluded_exceptions_dont_count_as_failures(self):
        """Test that excluded exceptions don't trigger circuit."""
        config = CircuitBreakerConfig(
            failure_threshold=2,
            excluded_exceptions=(ValueError,)
        )
        breaker = CircuitBreaker("test", config)
        
        # ValueError shouldn't count
        for _ in range(5):
            with pytest.raises(ValueError):
                breaker.call(lambda: (_ for _ in ()).throw(ValueError("ignored")))
        
        assert breaker.is_closed
        
        # But RuntimeError should
        for _ in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        assert breaker.is_open


class TestCircuitBreakerManualControl:
    """Test manual circuit breaker control."""
    
    def test_manual_reset_closes_circuit(self):
        """Test manual reset to CLOSED state."""
        config = CircuitBreakerConfig(failure_threshold=1)
        breaker = CircuitBreaker("test", config)
        
        # Open circuit
        with pytest.raises(RuntimeError):
            breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        assert breaker.is_open
        
        # Manual reset
        breaker.reset()
        
        assert breaker.is_closed
        
        # Should work normally now
        result = breaker.call(lambda: "works")
        assert result == "works"
    
    def test_manual_reset_clears_counters(self):
        """Test manual reset clears failure/success counters."""
        config = CircuitBreakerConfig(failure_threshold=3)
        breaker = CircuitBreaker("test", config)
        
        # Cause 2 failures (not enough to open)
        for _ in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        # Reset
        breaker.reset()
        
        # Should need full threshold again
        for _ in range(2):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        assert breaker.is_closed  # Still closed (needs 3 total)


class TestCircuitBreakerMetrics:
    """Test circuit breaker metrics and monitoring."""
    
    def test_get_metrics_returns_current_state(self):
        """Test metrics include current state."""
        breaker = CircuitBreaker("test-service")
        
        metrics = breaker.get_metrics()
        
        assert metrics["name"] == "test-service"
        assert metrics["state"] == "closed"
        assert metrics["failure_count"] == 0
        assert metrics["success_count"] == 0
    
    def test_metrics_track_failures(self):
        """Test metrics track failure count."""
        config = CircuitBreakerConfig(failure_threshold=5)
        breaker = CircuitBreaker("test", config)
        
        # Cause 3 failures
        for _ in range(3):
            with pytest.raises(RuntimeError):
                breaker.call(lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        
        metrics = breaker.get_metrics()
        
        assert metrics["failure_count"] == 3
        assert metrics["state"] == "closed"  # Not open yet
    
    def test_metrics_include_config(self):
        """Test metrics include configuration."""
        config = CircuitBreakerConfig(
            failure_threshold=10,
            success_threshold=3,
            timeout_seconds=120
        )
        breaker = CircuitBreaker("test", config)
        
        metrics = breaker.get_metrics()
        
        assert metrics["config"]["failure_threshold"] == 10
        assert metrics["config"]["success_threshold"] == 3
        assert metrics["config"]["timeout_seconds"] == 120


class TestCircuitBreakerThreadSafety:
    """Test circuit breaker is thread-safe."""
    
    def test_concurrent_calls_dont_corrupt_state(self):
        """Test concurrent calls maintain consistent state."""
        import threading
        
        config = CircuitBreakerConfig(failure_threshold=10)
        breaker = CircuitBreaker("test", config)
        errors = []
        
        def make_calls():
            try:
                for _ in range(5):
                    breaker.call(lambda: "success")
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=make_calls) for _ in range(10)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
        assert breaker.is_closed
    
    def test_repr_shows_state(self):
        """Test __repr__ shows current state."""
        breaker = CircuitBreaker("my-service")
        
        repr_str = repr(breaker)
        
        assert "my-service" in repr_str
        assert "closed" in repr_str
