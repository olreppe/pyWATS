"""
Tests for retry logic.

This module tests the automatic retry functionality for transient failures.
"""
import pytest
import time
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass
import httpx

from pywats import pyWATS, RetryConfig, RetryExhaustedError
from pywats.core.retry import (
    RETRYABLE_STATUS_CODES, 
    IDEMPOTENT_METHODS,
    should_retry,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@dataclass
class MockResponse:
    """Mock HTTP response for testing."""
    status_code: int
    headers: dict = None
    
    def __post_init__(self):
        self.headers = self.headers or {}


def mock_response(status_code: int, headers: dict = None) -> MockResponse:
    """Create a mock response with given status code."""
    return MockResponse(status_code=status_code, headers=headers or {})


# =============================================================================
# RetryConfig Unit Tests
# =============================================================================

class TestRetryConfig:
    """Tests for RetryConfig dataclass."""
    
    def test_default_values(self):
        """Test that default values are sensible."""
        config = RetryConfig()
        
        assert config.enabled is True
        assert config.max_attempts == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 30.0
        assert config.exponential_base == 2.0
        assert config.jitter is True
        assert config.retry_on_timeout is True
        assert config.retry_on_connection_error is True
    
    def test_disabled_config(self):
        """Test creating a disabled config."""
        config = RetryConfig(enabled=False)
        
        assert config.enabled is False
        # Other values should still be accessible
        assert config.max_attempts == 3
    
    def test_custom_values(self):
        """Test creating config with custom values."""
        config = RetryConfig(
            max_attempts=5,
            base_delay=2.0,
            max_delay=60.0,
        )
        
        assert config.max_attempts == 5
        assert config.base_delay == 2.0
        assert config.max_delay == 60.0
    
    def test_should_retry_method_get(self):
        """GET should be retryable by default."""
        config = RetryConfig()
        assert config.should_retry_method("GET") is True
        assert config.should_retry_method("get") is True  # Case insensitive
    
    def test_should_retry_method_put(self):
        """PUT should be retryable by default."""
        config = RetryConfig()
        assert config.should_retry_method("PUT") is True
    
    def test_should_retry_method_delete(self):
        """DELETE should be retryable by default."""
        config = RetryConfig()
        assert config.should_retry_method("DELETE") is True
    
    def test_should_retry_method_post(self):
        """POST should NOT be retryable by default (not idempotent)."""
        config = RetryConfig()
        assert config.should_retry_method("POST") is False
    
    def test_should_retry_method_head_options(self):
        """HEAD and OPTIONS should be retryable."""
        config = RetryConfig()
        assert config.should_retry_method("HEAD") is True
        assert config.should_retry_method("OPTIONS") is True
    
    def test_should_retry_status_500(self):
        """HTTP 500 should be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(500) is True
    
    def test_should_retry_status_502(self):
        """HTTP 502 (Bad Gateway) should be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(502) is True
    
    def test_should_retry_status_503(self):
        """HTTP 503 (Service Unavailable) should be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(503) is True
    
    def test_should_retry_status_504(self):
        """HTTP 504 (Gateway Timeout) should be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(504) is True
    
    def test_should_retry_status_429(self):
        """HTTP 429 (Too Many Requests) should be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(429) is True
    
    def test_should_not_retry_status_400(self):
        """HTTP 400 (Bad Request) should NOT be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(400) is False
    
    def test_should_not_retry_status_401(self):
        """HTTP 401 (Unauthorized) should NOT be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(401) is False
    
    def test_should_not_retry_status_403(self):
        """HTTP 403 (Forbidden) should NOT be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(403) is False
    
    def test_should_not_retry_status_404(self):
        """HTTP 404 (Not Found) should NOT be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(404) is False
    
    def test_should_not_retry_status_409(self):
        """HTTP 409 (Conflict) should NOT be retryable."""
        config = RetryConfig()
        assert config.should_retry_status(409) is False
    
    def test_calculate_delay_exponential_no_jitter(self):
        """Test exponential backoff without jitter."""
        config = RetryConfig(base_delay=1.0, jitter=False)
        
        assert config.calculate_delay(0) == 1.0   # 1.0 * 2^0 = 1.0
        assert config.calculate_delay(1) == 2.0   # 1.0 * 2^1 = 2.0
        assert config.calculate_delay(2) == 4.0   # 1.0 * 2^2 = 4.0
        assert config.calculate_delay(3) == 8.0   # 1.0 * 2^3 = 8.0
    
    def test_calculate_delay_max_cap(self):
        """Test that delay is capped at max_delay."""
        config = RetryConfig(base_delay=10.0, max_delay=30.0, jitter=False)
        
        # 10 * 2^5 = 320, should be capped to 30
        assert config.calculate_delay(5) == 30.0
    
    def test_calculate_delay_with_jitter(self):
        """Test that jitter adds randomness."""
        config = RetryConfig(base_delay=1.0, jitter=True)
        
        # Generate multiple delays and check they vary
        delays = [config.calculate_delay(0) for _ in range(50)]
        
        # All delays should be between 0 and base_delay (for attempt 0)
        assert all(0 <= d <= 1.0 for d in delays)
        
        # Should have some variation (not all the same)
        unique_delays = len(set(round(d, 3) for d in delays))
        assert unique_delays > 1, "Jitter should produce varied delays"
    
    def test_get_retry_after_from_header(self):
        """Test parsing Retry-After header (seconds)."""
        config = RetryConfig()
        response = mock_response(429, headers={"Retry-After": "5"})
        
        retry_after = config.get_retry_after(response)
        assert retry_after == 5.0
    
    def test_get_retry_after_none_when_missing(self):
        """Test None when Retry-After header is missing."""
        config = RetryConfig()
        response = mock_response(429)
        
        retry_after = config.get_retry_after(response)
        assert retry_after is None
    
    def test_stats_initialization(self):
        """Test that stats start at zero."""
        config = RetryConfig()
        
        stats = config.stats
        assert stats["total_retries"] == 0
        assert stats["total_retry_time"] == 0.0
    
    def test_stats_after_retry(self):
        """Test stats are updated after recording retry."""
        config = RetryConfig()
        
        config.record_retry(delay=1.5)
        config.record_retry(delay=2.5)
        
        stats = config.stats
        assert stats["total_retries"] == 2
        assert stats["total_retry_time"] == 4.0
    
    def test_reset_stats(self):
        """Test resetting stats."""
        config = RetryConfig()
        config.record_retry(delay=1.0)
        config.record_retry(delay=2.0)
        
        config.reset_stats()
        
        stats = config.stats
        assert stats["total_retries"] == 0
        assert stats["total_retry_time"] == 0.0


# =============================================================================
# should_retry Function Tests
# =============================================================================

class TestShouldRetry:
    """Tests for the should_retry helper function."""
    
    def test_disabled_config(self):
        """should_retry returns False when retry is disabled."""
        config = RetryConfig(enabled=False)
        should, delay = should_retry(config, "GET", 0, response=mock_response(500))
        
        assert should is False
    
    def test_max_attempts_exceeded(self):
        """should_retry returns False when max attempts reached."""
        config = RetryConfig(max_attempts=3)
        
        # Attempt 0, 1, 2 are allowed (3 total), attempt 2 is the last one
        should, delay = should_retry(config, "GET", 2, response=mock_response(500))
        assert should is False  # Can't retry after attempt 2 (which is the 3rd attempt)
    
    def test_non_idempotent_method(self):
        """POST should not be retried."""
        config = RetryConfig()
        should, delay = should_retry(config, "POST", 0, response=mock_response(500))
        
        assert should is False
    
    def test_retryable_status_codes(self):
        """Test all retryable status codes."""
        config = RetryConfig()
        
        for status in [429, 500, 502, 503, 504]:
            should, delay = should_retry(config, "GET", 0, response=mock_response(status))
            assert should is True, f"Status {status} should be retryable"
    
    def test_non_retryable_status_codes(self):
        """Test that non-retryable status codes don't retry."""
        config = RetryConfig()
        
        for status in [400, 401, 403, 404, 409]:
            should, delay = should_retry(config, "GET", 0, response=mock_response(status))
            assert should is False, f"Status {status} should NOT be retryable"
    
    def test_connection_error_retry(self):
        """ConnectionError should trigger retry."""
        config = RetryConfig()
        exc = ConnectionError("Connection refused")
        
        should, delay = should_retry(config, "GET", 0, exception=exc)
        assert should is True
    
    def test_timeout_error_retry(self):
        """TimeoutError should trigger retry."""
        config = RetryConfig()
        exc = TimeoutError("Request timed out")
        
        should, delay = should_retry(config, "GET", 0, exception=exc)
        assert should is True
    
    def test_connection_error_retry_disabled(self):
        """ConnectionError should not retry when disabled."""
        config = RetryConfig(retry_on_connection_error=False)
        exc = ConnectionError("Connection refused")
        
        should, delay = should_retry(config, "GET", 0, exception=exc)
        assert should is False
    
    def test_timeout_retry_disabled(self):
        """TimeoutError should not retry when disabled."""
        config = RetryConfig(retry_on_timeout=False)
        exc = TimeoutError("Request timed out")
        
        should, delay = should_retry(config, "GET", 0, exception=exc)
        assert should is False
    
    def test_delay_from_retry_after_header(self):
        """Delay should use Retry-After header when present."""
        config = RetryConfig()
        response = mock_response(429, headers={"Retry-After": "10"})
        
        should, delay = should_retry(config, "GET", 0, response=response)
        
        assert should is True
        assert delay == 10.0
    
    def test_delay_uses_calculated_when_no_retry_after(self):
        """Delay should use calculated value when no Retry-After header."""
        config = RetryConfig(jitter=False, base_delay=1.0)
        response = mock_response(500)
        
        should, delay = should_retry(config, "GET", 0, response=response)
        
        assert should is True
        assert delay == 1.0  # base_delay * 2^0


# =============================================================================
# Constants Tests
# =============================================================================

class TestRetryConstants:
    """Tests for retry module constants."""
    
    def test_retryable_status_codes(self):
        """Verify retryable status codes set."""
        assert 429 in RETRYABLE_STATUS_CODES
        assert 500 in RETRYABLE_STATUS_CODES
        assert 502 in RETRYABLE_STATUS_CODES
        assert 503 in RETRYABLE_STATUS_CODES
        assert 504 in RETRYABLE_STATUS_CODES
        
        # These should NOT be in the set
        assert 400 not in RETRYABLE_STATUS_CODES
        assert 401 not in RETRYABLE_STATUS_CODES
        assert 404 not in RETRYABLE_STATUS_CODES
    
    def test_idempotent_methods(self):
        """Verify idempotent methods set."""
        assert "GET" in IDEMPOTENT_METHODS
        assert "PUT" in IDEMPOTENT_METHODS
        assert "DELETE" in IDEMPOTENT_METHODS
        assert "HEAD" in IDEMPOTENT_METHODS
        assert "OPTIONS" in IDEMPOTENT_METHODS
        
        # POST should NOT be idempotent
        assert "POST" not in IDEMPOTENT_METHODS


# =============================================================================
# pyWATS Integration Tests
# =============================================================================

class TestPyWATSRetryIntegration:
    """Tests for retry integration with pyWATS class."""
    
    def test_default_retry_config(self):
        """pyWATS should have retry disabled by default (for HTTP client)."""
        api = pyWATS(base_url="https://test.example.com", token="dGVzdDp0ZXN0")
        
        # HTTP retry is disabled by default
        assert api.retry_config.enabled is False
        assert api.retry_config.max_attempts == 3
    
    def test_custom_retry_config(self):
        """pyWATS should accept custom retry config."""
        config = RetryConfig(max_attempts=5, base_delay=2.0)
        api = pyWATS(
            base_url="https://test.example.com",
            token="dGVzdDp0ZXN0",
            retry_config=config,
        )
        
        assert api.retry_config.max_attempts == 5
        assert api.retry_config.base_delay == 2.0
    
    def test_retry_disabled_via_flag(self):
        """retry_enabled=False should disable retry."""
        api = pyWATS(
            base_url="https://test.example.com",
            token="dGVzdDp0ZXN0",
            retry_enabled=False,
        )
        
        assert api.retry_config.enabled is False
    
    def test_retry_config_setter(self):
        """Should be able to update retry config at runtime."""
        api = pyWATS(base_url="https://test.example.com", token="dGVzdDp0ZXN0")
        
        new_config = RetryConfig(max_attempts=10)
        api.retry_config = new_config
        
        assert api.retry_config.max_attempts == 10


# =============================================================================
# Top-level Import Tests
# =============================================================================

class TestTopLevelImports:
    """Test that retry classes are importable from top level."""
    
    def test_import_retry_config(self):
        """RetryConfig should be importable from pywats."""
        from pywats import RetryConfig
        config = RetryConfig()
        assert config.enabled is True
    
    def test_import_retry_exhausted_error(self):
        """RetryExhaustedError should be importable from pywats."""
        from pywats import RetryExhaustedError
        err = RetryExhaustedError("Test message", attempts=3, last_error=None)
        assert err.attempts == 3
