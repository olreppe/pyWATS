"""
Tests for QueueManager - Local queue with auto-retry.

Tests the queue manager's ability to handle operations, retries,
and especially double-failure scenarios (queue + fallback fail).
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
import pytest

from pywats_ui.framework.reliability.queue_manager import (
    QueueManager,
    QueuedOperation,
    QueueStatus
)
from pywats_client.exceptions import QueueCriticalError


class TestQueueManagerDoubleFailure:
    """Tests for critical double-failure scenarios."""
    
    def test_double_failure_raises_critical_error(self):
        """Test that double failure (send + save) raises QueueCriticalError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            queue_dir = Path(tmpdir)
            
            # Create a send callback that always fails
            def failing_send(data):
                raise IOError("Network unavailable")
            
            manager = QueueManager(
                queue_dir=queue_dir,
                send_callback=failing_send,
                retry_interval_ms=10000,
                max_retries=3
            )
            
            # Enqueue an operation successfully
            operation_id = manager.enqueue(
                operation_type="test_operation",
                data={"test": "data"}
            )
            
            # Now simulate disk full by making pending directory read-only
            # This will cause the save operation to fail
            pending_file = queue_dir / "pending" / f"{operation_id}.json"
            assert pending_file.exists()
            
            # Mock the file write to simulate disk full
            with patch('builtins.open') as mock_open:
                # Make reads work but writes fail
                original_open = open
                
                def selective_open(file_path, mode='r', **kwargs):
                    if 'w' in mode and 'pending' in str(file_path):
                        raise OSError("No space left on device")
                    elif 'r' in mode:
                        return original_open(file_path, mode, **kwargs)
                    else:
                        return original_open(file_path, mode, **kwargs)
                
                mock_open.side_effect = selective_open
                
                # Trigger send attempt - should raise QueueCriticalError
                with pytest.raises(QueueCriticalError) as exc_info:
                    import asyncio
                    asyncio.run(manager._send_operation(operation_id))
                
                # Verify exception details
                error = exc_info.value
                assert "primary" in error.primary_error.lower() or "network" in error.primary_error.lower()
                assert "space" in error.fallback_error.lower() or "oserror" in error.fallback_error.lower()
                assert error.operation_id == operation_id
                assert error.operation_type == "test_operation"
    
    def test_single_send_failure_does_not_raise(self):
        """Test that single send failure (without save failure) doesn't raise critical error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            queue_dir = Path(tmpdir)
            
            # Create a send callback that always fails
            def failing_send(data):
                raise IOError("Network unavailable")
            
            manager = QueueManager(
                queue_dir=queue_dir,
                send_callback=failing_send,
                retry_interval_ms=10000,
                max_retries=3
            )
            
            # Enqueue an operation
            operation_id = manager.enqueue(
                operation_type="test_operation",
                data={"test": "data"}
            )
            
            # Send should fail but NOT raise QueueCriticalError
            # (because saving the error state succeeds)
            import asyncio
            result = asyncio.run(manager._send_operation(operation_id))
            
            assert result is False  # Send failed
            
            # Operation should still be in pending (for retry)
            pending_file = queue_dir / "pending" / f"{operation_id}.json"
            assert pending_file.exists()
            
            # Check that error was recorded
            with open(pending_file, 'r') as f:
                operation_data = json.load(f)
                assert operation_data['error'] == "Network unavailable"
                assert operation_data['attempts'] == 1
    
    def test_successful_send_after_retry(self):
        """Test that operations retry and eventually succeed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            queue_dir = Path(tmpdir)
            
            # Create a send callback that fails then succeeds
            call_count = 0
            
            def flaky_send(data):
                nonlocal call_count
                call_count += 1
                if call_count < 2:
                    raise IOError("Temporary network issue")
                return {"status": "success"}
            
            manager = QueueManager(
                queue_dir=queue_dir,
                send_callback=flaky_send,
                retry_interval_ms=10000,
                max_retries=5
            )
            
            # Enqueue operation
            operation_id = manager.enqueue(
                operation_type="test_operation",
                data={"test": "data"}
            )
            
            import asyncio
            
            # First attempt - should fail
            result1 = asyncio.run(manager._send_operation(operation_id))
            assert result1 is False
            
            # Second attempt - should succeed
            result2 = asyncio.run(manager._send_operation(operation_id))
            assert result2 is True
            
            # Should be moved to sent folder
            sent_file = queue_dir / "sent" / f"{operation_id}.json"
            assert sent_file.exists()
            
            # Should not be in pending anymore
            pending_file = queue_dir / "pending" / f"{operation_id}.json"
            assert not pending_file.exists()


class TestQueueManagerBasics:
    """Basic queue manager functionality tests."""
    
    def test_enqueue_creates_pending_file(self):
        """Test that enqueuing creates a file in pending directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            queue_dir = Path(tmpdir)
            
            def dummy_send(data):
                return {"status": "success"}
            
            manager = QueueManager(
                queue_dir=queue_dir,
                send_callback=dummy_send,
                retry_interval_ms=10000
            )
            
            operation_id = manager.enqueue(
                operation_type="test_op",
                data={"key": "value"}
            )
            
            # Check pending file exists
            pending_file = queue_dir / "pending" / f"{operation_id}.json"
            assert pending_file.exists()
            
            # Check file content
            with open(pending_file, 'r') as f:
                data = json.load(f)
                assert data['operation_type'] == "test_op"
                assert data['data'] == {"key": "value"}
                assert data['status'] == 'pending'
    
    def test_get_pending_count(self):
        """Test getting count of pending operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            queue_dir = Path(tmpdir)
            
            # Create send callback that never completes (blocks sending)
            def blocking_send(data):
                raise IOError("Intentionally blocked")
            
            manager = QueueManager(
                queue_dir=queue_dir,
                send_callback=blocking_send,
                retry_interval_ms=10000
            )
            
            assert manager.get_pending_count() == 0
            
            # Enqueue some operations
            manager.enqueue("op1", {"data": 1})
            assert manager.get_pending_count() == 1
            
            manager.enqueue("op2", {"data": 2})
            assert manager.get_pending_count() == 2
    
    def test_max_retries_moves_to_failed(self):
        """Test that operations move to failed after max retries."""
        with tempfile.TemporaryDirectory() as tmpdir:
            queue_dir = Path(tmpdir)
            
            def always_fail(data):
                raise IOError("Permanent failure")
            
            manager = QueueManager(
                queue_dir=queue_dir,
                send_callback=always_fail,
                retry_interval_ms=10000,
                max_retries=3
            )
            
            operation_id = manager.enqueue(
                operation_type="test_op",
                data={"test": "data"}
            )
            
            import asyncio
            
            # Attempt send multiple times
            for i in range(3):
                result = asyncio.run(manager._send_operation(operation_id))
                assert result is False
            
            # Should be moved to failed folder
            failed_file = queue_dir / "failed" / f"{operation_id}.json"
            assert failed_file.exists()
            
            # Should not be in pending anymore
            pending_file = queue_dir / "pending" / f"{operation_id}.json"
            assert not pending_file.exists()
            
            # Check failed count
            assert manager.get_failed_count() == 1


class TestQueuedOperation:
    """Tests for QueuedOperation dataclass."""
    
    def test_to_dict(self):
        """Test converting operation to dictionary."""
        operation = QueuedOperation(
            id="test_123",
            operation_type="send_uut",
            data={"serial": "ABC123"},
            created="2026-02-07T12:00:00",
            attempts=2,
            last_attempt="2026-02-07T12:05:00",
            error="Network error",
            status=QueueStatus.PENDING
        )
        
        result = operation.to_dict()
        
        assert result['id'] == "test_123"
        assert result['operation_type'] == "send_uut"
        assert result['data'] == {"serial": "ABC123"}
        assert result['attempts'] == 2
        assert result['status'] == 'pending'  # Enum converted to value
    
    def test_from_dict(self):
        """Test creating operation from dictionary."""
        data = {
            'id': "test_456",
            'operation_type': "update_config",
            'data': {"key": "value"},
            'created': "2026-02-07T12:00:00",
            'attempts': 1,
            'last_attempt': None,
            'error': None,
            'status': 'sending'
        }
        
        operation = QueuedOperation.from_dict(data)
        
        assert operation.id == "test_456"
        assert operation.operation_type == "update_config"
        assert operation.data == {"key": "value"}
        assert operation.status == QueueStatus.SENDING  # String converted to enum
