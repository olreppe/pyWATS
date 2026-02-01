"""
Tests for SyncConfig and RetryConfig dataclasses.

Tests Phase 1 Task 1.1: SyncConfig Dataclass
"""
import pytest
from pywats.core.config import SyncConfig, RetryConfig


def test_sync_config_defaults():
    """Test that SyncConfig has correct default values."""
    config = SyncConfig()
    assert config.timeout == 30.0
    assert config.retry_enabled is False
    assert config.correlation_id_enabled is True
    assert isinstance(config.retry, RetryConfig)


def test_sync_config_custom_values():
    """Test SyncConfig with custom values."""
    config = SyncConfig(
        timeout=60.0,
        retry_enabled=True,
        correlation_id_enabled=False
    )
    assert config.timeout == 60.0
    assert config.retry_enabled is True
    assert config.correlation_id_enabled is False


def test_sync_config_no_timeout():
    """Test SyncConfig with timeout disabled."""
    config = SyncConfig(timeout=None)
    assert config.timeout is None


def test_retry_config_defaults():
    """Test that RetryConfig has correct default values."""
    config = RetryConfig()
    assert config.max_retries == 3
    assert config.backoff == 2.0
    assert ConnectionError in config.retry_on_errors
    assert TimeoutError in config.retry_on_errors


def test_retry_config_custom_values():
    """Test RetryConfig with custom values."""
    config = RetryConfig(
        max_retries=5,
        backoff=1.5,
        retry_on_errors=(ValueError, RuntimeError)
    )
    assert config.max_retries == 5
    assert config.backoff == 1.5
    assert ValueError in config.retry_on_errors
    assert RuntimeError in config.retry_on_errors


def test_sync_config_with_custom_retry():
    """Test SyncConfig with custom RetryConfig."""
    retry = RetryConfig(max_retries=5, backoff=1.5)
    config = SyncConfig(retry_enabled=True, retry=retry)
    
    assert config.retry_enabled is True
    assert config.retry.max_retries == 5
    assert config.retry.backoff == 1.5
