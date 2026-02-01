"""
Tests for enhanced _run_sync() function with timeout and correlation ID support.

Tests Phase 1 Task 1.2: Enhance _run_sync() with Timeout
Tests Phase 1 Task 1.3: Add Correlation ID Support
"""
import pytest
import asyncio
import logging
from pywats.pywats import _run_sync, generate_correlation_id, correlation_id_var


# ============================================================================
# Timeout Tests (Task 1.2)
# ============================================================================

async def fast_operation():
    """Quick async operation."""
    await asyncio.sleep(0.1)
    return "done"


async def slow_operation():
    """Slow async operation that exceeds timeout."""
    await asyncio.sleep(5)
    return "done"


def test_run_sync_without_timeout():
    """Test _run_sync works without timeout."""
    result = _run_sync(fast_operation())
    assert result == "done"


def test_run_sync_with_timeout_succeeds():
    """Test _run_sync completes within timeout."""
    result = _run_sync(fast_operation(), timeout=2.0)
    assert result == "done"


def test_run_sync_with_timeout_fails():
    """Test _run_sync raises TimeoutError when exceeded."""
    with pytest.raises(TimeoutError, match="timed out after 1.0s"):
        _run_sync(slow_operation(), timeout=1.0)


def test_run_sync_timeout_none_disables():
    """Test timeout=None disables timeout."""
    # Should complete without timeout even if slow
    result = _run_sync(fast_operation(), timeout=None)
    assert result == "done"


# ============================================================================
# Correlation ID Tests (Task 1.3)
# ============================================================================

def test_generate_correlation_id():
    """Test correlation ID generation."""
    corr_id = generate_correlation_id()
    assert isinstance(corr_id, str)
    assert len(corr_id) == 8  # Short UUID


def test_generate_correlation_id_unique():
    """Test correlation IDs are unique."""
    id1 = generate_correlation_id()
    id2 = generate_correlation_id()
    assert id1 != id2


def test_run_sync_with_correlation_id():
    """Test _run_sync sets correlation ID in context."""
    async def check_correlation_id():
        # Correlation ID should be available in async context
        return correlation_id_var.get()
    
    corr_id = "test-123"
    result = _run_sync(check_correlation_id(), correlation_id=corr_id)
    assert result == corr_id


def test_run_sync_clears_correlation_id():
    """Test _run_sync clears correlation ID after completion."""
    async def dummy():
        return "done"
    
    # Set correlation ID
    _run_sync(dummy(), correlation_id="test-456")
    
    # Should be cleared after operation
    assert correlation_id_var.get() is None


def test_run_sync_clears_correlation_id_on_error():
    """Test _run_sync clears correlation ID even on error."""
    async def failing_operation():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        _run_sync(failing_operation(), correlation_id="test-789")
    
    # Should be cleared even after error
    assert correlation_id_var.get() is None


def test_correlation_id_in_logs(caplog):
    """Test correlation IDs appear in logs."""
    from pywats.core.logging import CorrelationFilter
    
    caplog.set_level(logging.INFO)
    
    # Add correlation filter to capture correlation IDs
    for handler in caplog.handler.handlers:
        handler.addFilter(CorrelationFilter())
    
    async def logged_operation():
        logger = logging.getLogger("pywats.test")
        logger.info("Test message")
        return "done"
    
    # Run with correlation ID
    token = correlation_id_var.set("abc12345")
    try:
        _run_sync(logged_operation())
    finally:
        correlation_id_var.reset(token)
    
    # Check that correlation ID appears in logs
    assert any("abc12345" in record.message or hasattr(record, 'correlation_id') 
               for record in caplog.records)


# ============================================================================
# Combined Tests
# ============================================================================

def test_run_sync_with_timeout_and_correlation():
    """Test _run_sync with both timeout and correlation ID."""
    async def operation():
        await asyncio.sleep(0.1)
        return correlation_id_var.get()
    
    corr_id = "combined-test"
    result = _run_sync(operation(), timeout=2.0, correlation_id=corr_id)
    assert result == corr_id


def test_run_sync_timeout_with_correlation_cleanup():
    """Test correlation ID cleaned up even on timeout."""
    async def slow_op():
        await asyncio.sleep(5)
        return "done"
    
    with pytest.raises(TimeoutError):
        _run_sync(slow_op(), timeout=0.5, correlation_id="timeout-test")
    
    # Correlation ID should be cleared
    assert correlation_id_var.get() is None
