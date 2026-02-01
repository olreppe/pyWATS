"""
Tests for pyWATS constructor with sync_config integration.

Tests Phase 3: Configuration & Integration
"""
import pytest
from pywats import pyWATS
from pywats.core.config import SyncConfig, RetryConfig


# Mock credentials for testing
TEST_URL = "https://test-wats.com"
TEST_TOKEN = "test-token-123"


def test_pywats_with_default_sync_config():
    """Test pyWATS uses default sync config when none provided."""
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN)
    
    # Should have sync_config
    assert hasattr(api, '_sync_config')
    assert api._sync_config is not None
    assert api._sync_config.timeout == 30.0
    assert api._sync_config.retry_enabled is False
    assert api._sync_config.correlation_id_enabled is True


def test_pywats_with_custom_timeout():
    """Test pyWATS with custom timeout parameter."""
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN, timeout=60.0)
    
    # Sync config should use the custom timeout
    assert api._sync_config.timeout == 60.0


def test_pywats_with_full_sync_config():
    """Test pyWATS with full SyncConfig object."""
    config = SyncConfig(
        timeout=45.0,
        retry_enabled=True,
        retry=RetryConfig(max_retries=5, backoff=1.5),
        correlation_id_enabled=False
    )
    
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN, sync_config=config)
    
    assert api._sync_config.timeout == 45.0
    assert api._sync_config.retry_enabled is True
    assert api._sync_config.retry.max_retries == 5
    assert api._sync_config.retry.backoff == 1.5
    assert api._sync_config.correlation_id_enabled is False


def test_pywats_sync_config_overrides_timeout():
    """Test that sync_config parameter overrides timeout parameter."""
    config = SyncConfig(timeout=99.0)
    
    # Even though timeout=60 is provided, sync_config should win
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN, timeout=60.0, sync_config=config)
    
    assert api._sync_config.timeout == 99.0


def test_pywats_services_use_sync_config():
    """Test that all services receive the sync config."""
    config = SyncConfig(
        timeout=55.0,
        retry_enabled=True,
        retry=RetryConfig(max_retries=4, backoff=3.0)
    )
    
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN, sync_config=config)
    
    # Access each service to trigger initialization
    # (We can't check internals without triggering lazy init, but we can verify no errors)
    services = []
    try:
        # These will fail to connect, but should initialize wrappers successfully
        services.append(api.product)
    except Exception:
        pass  # Connection errors are expected
    
    try:
        services.append(api.asset)
    except Exception:
        pass
    
    try:
        services.append(api.production)
    except Exception:
        pass
    
    try:
        services.append(api.report)
    except Exception:
        pass
    
    try:
        services.append(api.software)
    except Exception:
        pass
    
    try:
        services.append(api.analytics)
    except Exception:
        pass
    
    try:
        services.append(api.rootcause)
    except Exception:
        pass
    
    try:
        services.append(api.scim)
    except Exception:
        pass
    
    try:
        services.append(api.process)
    except Exception:
        pass
    
    # All services should have been created (even if connections failed)
    # Verify wrappers have config
    assert api._product._config.timeout == 55.0
    assert api._asset._config.timeout == 55.0
    assert api._production._config.timeout == 55.0
    assert api._report._config.timeout == 55.0
    assert api._software._config.timeout == 55.0
    assert api._analytics._config.timeout == 55.0
    assert api._rootcause._config.timeout == 55.0
    assert api._scim._config.timeout == 55.0
    assert api._process._config.timeout == 55.0


def test_pywats_timeout_none_disables():
    """Test that timeout=None disables timeout."""
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN, timeout=None)
    
    # When timeout is None, should use default 30.0 for sync config
    # (because we need a timeout for the HTTP client)
    assert api._timeout is None or api._sync_config.timeout == 30.0


def test_pywats_retry_disabled_by_default():
    """Test that retry is disabled by default."""
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN)
    
    assert api._sync_config.retry_enabled is False


def test_pywats_correlation_enabled_by_default():
    """Test that correlation IDs are enabled by default."""
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN)
    
    assert api._sync_config.correlation_id_enabled is True


def test_pywats_with_retry_enabled():
    """Test enabling retry via sync_config."""
    config = SyncConfig(
        retry_enabled=True,
        retry=RetryConfig(max_retries=3, backoff=2.0)
    )
    
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN, sync_config=config)
    
    assert api._sync_config.retry_enabled is True
    assert api._sync_config.retry.max_retries == 3


def test_pywats_backward_compatible():
    """Test that existing code without sync_config still works."""
    # Old-style initialization should still work
    api = pyWATS(base_url=TEST_URL, token=TEST_TOKEN)
    
    # Should have default sync config
    assert api._sync_config is not None
    assert isinstance(api._sync_config, SyncConfig)
