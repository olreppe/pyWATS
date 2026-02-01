"""
Tests for SyncServiceWrapper with retry integration.

Tests Phase 2 Task 2.2: Integrate Retry into SyncServiceWrapper
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from pywats.pywats import SyncServiceWrapper
from pywats.core.config import SyncConfig, RetryConfig


# ============================================================================
# Mock Async Service
# ============================================================================

class MockAsyncService:
    """Mock async service for testing."""
    
    def __init__(self):
        self.call_count = 0
        self.fail_count = 0
    
    async def successful_method(self, value: str) -> str:
        """Always succeeds."""
        self.call_count += 1
        await asyncio.sleep(0.01)
        return f"success: {value}"
    
    async def flaky_method(self, value: str) -> str:
        """Fails a few times then succeeds."""
        self.call_count += 1
        if self.call_count <= self.fail_count:
            await asyncio.sleep(0.01)
            raise ConnectionError(f"Transient error (attempt {self.call_count})")
        await asyncio.sleep(0.01)
        return f"success after {self.call_count} attempts: {value}"
    
    async def always_fails(self, value: str) -> str:
        """Always fails."""
        self.call_count += 1
        await asyncio.sleep(0.01)
        raise ConnectionError("Permanent failure")
    
    def sync_property(self) -> str:
        """Non-async property."""
        return "sync_value"


# ============================================================================
# Basic Wrapper Tests with Config
# ============================================================================

def test_sync_wrapper_with_default_config():
    """Test SyncServiceWrapper with default config."""
    service = MockAsyncService()
    wrapper = SyncServiceWrapper(service)
    
    result = wrapper.successful_method("test")
    assert result == "success: test"
    assert service.call_count == 1


def test_sync_wrapper_with_custom_config():
    """Test SyncServiceWrapper with custom config."""
    config = SyncConfig(
        timeout=60.0,
        retry_enabled=False,
        correlation_id_enabled=False
    )
    service = MockAsyncService()
    wrapper = SyncServiceWrapper(service, config=config)
    
    result = wrapper.successful_method("test")
    assert result == "success: test"


def test_sync_wrapper_timeout_from_config():
    """Test that wrapper uses timeout from config."""
    async def slow_method():
        await asyncio.sleep(5)
        return "done"
    
    service = Mock()
    service.slow_method = slow_method
    
    config = SyncConfig(timeout=0.5)
    wrapper = SyncServiceWrapper(service, config=config)
    
    with pytest.raises(TimeoutError, match="timed out after 0.5s"):
        wrapper.slow_method()


# ============================================================================
# Retry Integration Tests
# ============================================================================

def test_sync_wrapper_retry_disabled():
    """Test that retry is disabled by default."""
    service = MockAsyncService()
    service.fail_count = 2
    
    config = SyncConfig(retry_enabled=False)
    wrapper = SyncServiceWrapper(service, config=config)
    
    # Should fail immediately without retry
    with pytest.raises(ConnectionError, match="Transient error"):
        wrapper.flaky_method("test")
    
    assert service.call_count == 1  # No retry


def test_sync_wrapper_retry_enabled():
    """Test that retry works when enabled."""
    service = MockAsyncService()
    service.fail_count = 2  # Fail twice, succeed on third
    
    config = SyncConfig(
        retry_enabled=True,
        retry=RetryConfig(max_retries=3, backoff=0.1)
    )
    wrapper = SyncServiceWrapper(service, config=config)
    
    result = wrapper.flaky_method("test")
    assert "success after 3 attempts" in result
    assert service.call_count == 3


def test_sync_wrapper_retry_exhausted():
    """Test retry gives up after max attempts."""
    service = MockAsyncService()
    
    config = SyncConfig(
        retry_enabled=True,
        retry=RetryConfig(max_retries=2, backoff=0.1)
    )
    wrapper = SyncServiceWrapper(service, config=config)
    
    with pytest.raises(ConnectionError, match="Permanent failure"):
        wrapper.always_fails("test")
    
    assert service.call_count == 3  # Initial + 2 retries


def test_sync_wrapper_retry_with_timeout():
    """Test retry works together with timeout."""
    call_count = 0
    
    async def slow_then_fast():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            # First call times out
            await asyncio.sleep(5)
        else:
            # Retry succeeds quickly
            await asyncio.sleep(0.01)
        return "success"
    
    service = Mock()
    service.slow_then_fast = slow_then_fast
    
    config = SyncConfig(
        timeout=0.5,
        retry_enabled=True,
        retry=RetryConfig(
            max_retries=2,
            backoff=0.1,
            retry_on_errors=(TimeoutError, ConnectionError)
        )
    )
    wrapper = SyncServiceWrapper(service, config=config)
    
    result = wrapper.slow_then_fast()
    assert result == "success"
    assert call_count == 2  # Failed once on timeout, succeeded on retry


def test_sync_wrapper_custom_retry_errors():
    """Test retry with custom error types."""
    call_count = 0
    
    async def custom_error_method():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Custom transient error")
        return "success"
    
    service = Mock()
    service.custom_error_method = custom_error_method
    
    config = SyncConfig(
        retry_enabled=True,
        retry=RetryConfig(
            max_retries=3,
            backoff=0.1,
            retry_on_errors=(ValueError,)
        )
    )
    wrapper = SyncServiceWrapper(service, config=config)
    
    result = wrapper.custom_error_method()
    assert result == "success"
    assert call_count == 3


def test_sync_wrapper_non_async_methods_not_wrapped():
    """Test that non-async methods are not wrapped."""
    service = MockAsyncService()
    wrapper = SyncServiceWrapper(service)
    
    # sync_property is not async, should work directly
    result = wrapper.sync_property()
    assert result == "sync_value"


def test_sync_wrapper_correlation_id_enabled():
    """Test wrapper with correlation IDs enabled."""
    service = MockAsyncService()
    config = SyncConfig(correlation_id_enabled=True)
    wrapper = SyncServiceWrapper(service, config=config)
    
    result = wrapper.successful_method("test")
    assert result == "success: test"


def test_sync_wrapper_correlation_id_disabled():
    """Test wrapper with correlation IDs disabled."""
    service = MockAsyncService()
    config = SyncConfig(correlation_id_enabled=False)
    wrapper = SyncServiceWrapper(service, config=config)
    
    result = wrapper.successful_method("test")
    assert result == "success: test"


# ============================================================================
# Multiple Methods Test
# ============================================================================

def test_sync_wrapper_multiple_methods():
    """Test wrapper with multiple async methods."""
    service = MockAsyncService()
    config = SyncConfig(
        retry_enabled=True,
        retry=RetryConfig(max_retries=3, backoff=0.1)
    )
    wrapper = SyncServiceWrapper(service, config=config)
    
    # Successful method
    result1 = wrapper.successful_method("first")
    assert result1 == "success: first"
    
    # Reset for flaky method
    service.call_count = 0
    service.fail_count = 1
    
    # Flaky method with retry
    result2 = wrapper.flaky_method("second")
    assert "success after 2 attempts" in result2


# ============================================================================
# Config Precedence Tests
# ============================================================================

def test_sync_wrapper_no_config_uses_defaults():
    """Test wrapper without config uses defaults."""
    service = MockAsyncService()
    wrapper = SyncServiceWrapper(service)  # No config
    
    # Should work with default config
    result = wrapper.successful_method("test")
    assert result == "success: test"
    
    # Retry should be disabled by default
    assert wrapper._config.retry_enabled is False
    assert wrapper._config.timeout == 30.0
    assert wrapper._config.correlation_id_enabled is True
