"""
Tests for AsyncPendingQueue

Tests concurrent report uploads with asyncio.
"""

import asyncio
import json
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import tempfile
import shutil

from pywats_client.service.async_pending_queue import (
    AsyncPendingQueue,
    AsyncPendingQueueState,
)


@pytest.fixture
def temp_reports_dir():
    """Create a temporary reports directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_api():
    """Create a mock AsyncWATS client"""
    api = AsyncMock()
    api.report.submit_raw = AsyncMock()
    return api


@pytest.fixture
def queue(mock_api, temp_reports_dir):
    """Create a test queue instance"""
    return AsyncPendingQueue(
        api=mock_api,
        reports_dir=temp_reports_dir,
        max_concurrent=3
    )


class TestAsyncPendingQueueState:
    """Test queue state enum"""
    
    def test_state_values(self):
        assert AsyncPendingQueueState.CREATED.value == "Created"
        assert AsyncPendingQueueState.RUNNING.value == "Running"
        assert AsyncPendingQueueState.STOPPING.value == "Stopping"
        assert AsyncPendingQueueState.STOPPED.value == "Stopped"


class TestAsyncPendingQueueInit:
    """Test queue initialization"""
    
    def test_init_creates_directory(self, mock_api, temp_reports_dir):
        """Test that queue creates reports directory"""
        new_dir = temp_reports_dir / "subdir"
        queue = AsyncPendingQueue(mock_api, new_dir)
        
        assert new_dir.exists()
    
    def test_init_defaults(self, mock_api, temp_reports_dir):
        """Test default initialization values"""
        queue = AsyncPendingQueue(mock_api, temp_reports_dir)
        
        assert queue.state == AsyncPendingQueueState.CREATED
        assert queue._max_concurrent == 5
    
    def test_init_custom_concurrent(self, mock_api, temp_reports_dir):
        """Test custom max_concurrent"""
        queue = AsyncPendingQueue(mock_api, temp_reports_dir, max_concurrent=10)
        
        assert queue._max_concurrent == 10


class TestAsyncPendingQueueStats:
    """Test queue statistics"""
    
    def test_initial_stats(self, queue):
        """Test initial statistics values"""
        stats = queue.stats
        
        assert stats["total_submitted"] == 0
        assert stats["successful"] == 0
        assert stats["errors"] == 0
        assert stats["active_uploads"] == 0
    
    def test_stats_update_after_submit(self, queue, temp_reports_dir, mock_api):
        """Test stats are updated after submission"""
        # Create a queued file
        report_data = {"test": "data"}
        report_file = temp_reports_dir / "report1.queued"
        report_file.write_text(json.dumps(report_data))
        
        # Run submission
        asyncio.run(queue._submit_report(report_file))
        
        stats = queue.stats
        assert stats["total_submitted"] == 1
        assert stats["successful"] == 1


class TestAsyncPendingQueueSubmission:
    """Test report submission"""
    
    @pytest.mark.asyncio
    async def test_submit_single_report(self, queue, temp_reports_dir, mock_api):
        """Test submitting a single report"""
        # Create a queued file
        report_data = {"reportId": "test123", "data": "value"}
        report_file = temp_reports_dir / "report.queued"
        report_file.write_text(json.dumps(report_data))
        
        # Submit
        await queue._submit_report(report_file)
        
        # Check API was called
        mock_api.report.submit_raw.assert_called_once_with(report_data)
        
        # Check file was renamed to .completed
        assert not report_file.exists()
        assert (temp_reports_dir / "report.completed").exists()
    
    @pytest.mark.asyncio
    async def test_submit_invalid_json(self, queue, temp_reports_dir, mock_api):
        """Test submitting invalid JSON file"""
        # Create invalid file
        report_file = temp_reports_dir / "invalid.queued"
        report_file.write_text("not valid json")
        
        # Submit (should not raise)
        await queue._submit_report(report_file)
        
        # Should be marked as error
        assert (temp_reports_dir / "invalid.error").exists()
        
        # API should not be called
        mock_api.report.submit_raw.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_submit_api_error(self, queue, temp_reports_dir, mock_api):
        """Test handling API error"""
        mock_api.report.submit_raw.side_effect = Exception("API Error")
        
        report_file = temp_reports_dir / "report.queued"
        report_file.write_text(json.dumps({"test": "data"}))
        
        await queue._submit_report(report_file)
        
        # Should be marked as error
        assert (temp_reports_dir / "report.error").exists()
    
    @pytest.mark.asyncio
    async def test_submit_all_pending(self, queue, temp_reports_dir, mock_api):
        """Test submitting multiple pending reports"""
        # Create multiple queued files
        for i in range(5):
            report_file = temp_reports_dir / f"report{i}.queued"
            report_file.write_text(json.dumps({"id": i}))
        
        # Submit all
        await queue.submit_all_pending()
        
        # All should be submitted
        assert mock_api.report.submit_raw.call_count == 5
        
        # All should be completed
        completed = list(temp_reports_dir.glob("*.completed"))
        assert len(completed) == 5


class TestAsyncPendingQueueConcurrency:
    """Test concurrent upload behavior"""
    
    @pytest.mark.asyncio
    async def test_respects_max_concurrent(self, temp_reports_dir, mock_api):
        """Test that max_concurrent is respected"""
        # Create queue with low concurrency
        queue = AsyncPendingQueue(mock_api, temp_reports_dir, max_concurrent=2)
        
        # Track concurrent calls
        max_concurrent_seen = 0
        current_concurrent = 0
        
        async def slow_submit(data):
            nonlocal max_concurrent_seen, current_concurrent
            current_concurrent += 1
            max_concurrent_seen = max(max_concurrent_seen, current_concurrent)
            await asyncio.sleep(0.1)
            current_concurrent -= 1
        
        mock_api.report.submit_raw = slow_submit
        
        # Create many files
        for i in range(10):
            report_file = temp_reports_dir / f"report{i}.queued"
            report_file.write_text(json.dumps({"id": i}))
        
        # Submit all
        await queue.submit_all_pending()
        
        # Max concurrent should be <= 2
        assert max_concurrent_seen <= 2


class TestAsyncPendingQueueRecovery:
    """Test file recovery mechanisms"""
    
    @pytest.mark.asyncio
    async def test_recover_stuck_files(self, queue, temp_reports_dir):
        """Test recovery of stuck .processing files"""
        # Create a stuck file (old .processing)
        stuck_file = temp_reports_dir / "stuck.processing"
        stuck_file.write_text(json.dumps({"test": "data"}))
        
        # Set old modification time
        import os
        old_time = (datetime.now() - timedelta(hours=1)).timestamp()
        os.utime(stuck_file, (old_time, old_time))
        
        # Recover
        await queue._recover_stuck_files()
        
        # Should be moved back to .queued
        assert not stuck_file.exists()
        assert (temp_reports_dir / "stuck.queued").exists()
    
    @pytest.mark.asyncio
    async def test_retry_error_files(self, queue, temp_reports_dir):
        """Test retry of error files after delay"""
        # Create error file with old timestamp
        error_file = temp_reports_dir / "error.error"
        error_file.write_text(json.dumps({"test": "data"}))
        
        error_info = temp_reports_dir / "error.error.info"
        old_time = (datetime.now() - timedelta(minutes=10)).isoformat()
        error_info.write_text(json.dumps({
            "error": "Test error",
            "timestamp": old_time,
            "attempts": 1
        }))
        
        # Retry
        await queue._retry_error_files()
        
        # Should be moved back to .queued
        assert not error_file.exists()
        assert (temp_reports_dir / "error.queued").exists()


class TestAsyncPendingQueueLifecycle:
    """Test queue lifecycle"""
    
    @pytest.mark.asyncio
    async def test_start_stop(self, queue):
        """Test basic start and stop"""
        # Start queue in background
        task = asyncio.create_task(queue.run())
        
        # Wait a bit for it to start
        await asyncio.sleep(0.1)
        
        assert queue.state == AsyncPendingQueueState.RUNNING
        assert queue.is_running
        
        # Stop
        await queue.stop()
        
        assert queue.state == AsyncPendingQueueState.STOPPED
        assert not queue.is_running
        
        # Cancel the task
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
