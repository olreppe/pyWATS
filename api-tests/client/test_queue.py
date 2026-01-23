"""
Unit Tests for Report Queue Service

Tests for pywats_client.services.report_queue module covering:
- QueuedReport dataclass
- ReportQueueService lifecycle
- Queue operations (submit, process, retry)
- Persistence (save, load, recovery)
- Error handling and max retries
"""

import pytest
import asyncio
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch

from pywats_client.services.report_queue import (
    ReportQueueService,
    QueuedReport,
    ReportStatus
)
from pywats_client.services.connection import ConnectionStatus


@pytest.fixture
def mock_connection():
    """Mock ConnectionService"""
    conn = MagicMock()
    conn.status = ConnectionStatus.OFFLINE
    conn.get_client = MagicMock(return_value=None)
    conn.on_status_change = MagicMock()
    return conn


@pytest.fixture
def queue_folder(temp_dir):
    """Create queue folder structure"""
    queue_dir = temp_dir / "queue"
    queue_dir.mkdir(parents=True, exist_ok=True)
    return queue_dir


@pytest.fixture
def queue_service(mock_connection, queue_folder):
    """Create ReportQueueService instance"""
    return ReportQueueService(
        connection=mock_connection,
        reports_folder=queue_folder,
        max_retries=3,
        retry_interval=1  # Short interval for testing
    )


@pytest.fixture
def sample_report_data():
    """Sample WSJF report data"""
    return {
        "type": "UUT",
        "serialNumber": "TEST-001",
        "partNumber": "WIDGET-100",
        "status": "PASS",
        "startDateTime": "2024-01-01T10:00:00Z",
        "endDateTime": "2024-01-01T10:05:00Z"
    }


class TestQueuedReport:
    """Tests for QueuedReport dataclass"""
    
    def test_create_queued_report(self, sample_report_data):
        """Test creating a queued report"""
        report = QueuedReport(report_data=sample_report_data)
        
        assert report.report_id is not None
        assert len(report.report_id) > 0
        assert report.report_data == sample_report_data
        assert report.status == ReportStatus.PENDING
        assert report.attempts == 0
        assert report.created_at is not None
        assert report.last_attempt is None
        assert report.error is None
    
    def test_queued_report_with_custom_id(self, sample_report_data):
        """Test creating report with custom ID"""
        custom_id = "custom-report-123"
        report = QueuedReport(
            report_data=sample_report_data,
            report_id=custom_id
        )
        
        assert report.report_id == custom_id
    
    def test_to_dict_serialization(self, sample_report_data):
        """Test converting report to dictionary"""
        report = QueuedReport(
            report_data=sample_report_data,
            status=ReportStatus.FAILED,
            attempts=2,
            error="Connection timeout"
        )
        
        data = report.to_dict()
        
        assert data['report_id'] == report.report_id
        assert data['report_data'] == sample_report_data
        assert data['status'] == 'failed'
        assert data['attempts'] == 2
        assert data['error'] == "Connection timeout"
        assert 'created_at' in data
    
    def test_from_dict_deserialization(self, sample_report_data):
        """Test creating report from dictionary"""
        report_dict = {
            'report_id': 'test-123',
            'report_data': sample_report_data,
            'status': 'pending',
            'attempts': 1,
            'created_at': '2024-01-01T10:00:00',
            'last_attempt': '2024-01-01T10:05:00',
            'error': None
        }
        
        report = QueuedReport.from_dict(report_dict)
        
        assert report.report_id == 'test-123'
        assert report.report_data == sample_report_data
        assert report.status == ReportStatus.PENDING
        assert report.attempts == 1
        assert isinstance(report.created_at, datetime)
        assert isinstance(report.last_attempt, datetime)
    
    def test_round_trip_serialization(self, sample_report_data):
        """Test serialization round-trip"""
        report1 = QueuedReport(report_data=sample_report_data, attempts=3)
        data = report1.to_dict()
        report2 = QueuedReport.from_dict(data)
        
        assert report1.report_id == report2.report_id
        assert report1.report_data == report2.report_data
        assert report1.status == report2.status
        assert report1.attempts == report2.attempts


class TestReportQueueServiceInit:
    """Tests for ReportQueueService initialization"""
    
    def test_service_initialization(self, queue_service, queue_folder):
        """Test service initializes correctly"""
        assert queue_service.reports_folder == queue_folder
        assert queue_service.max_retries == 3
        assert queue_service.retry_interval == 1
        assert queue_service._running is False
        assert len(queue_service._queue) == 0
    
    def test_creates_folder_structure(self, queue_service, queue_folder):
        """Test service creates required folders"""
        assert (queue_folder / "pending").exists()
        assert (queue_folder / "failed").exists()
        assert (queue_folder / "completed").exists()
    
    def test_loads_existing_pending_reports(self, mock_connection, queue_folder, sample_report_data):
        """Test service loads existing pending reports on init"""
        # Create a pending report file
        pending_folder = queue_folder / "pending"
        pending_folder.mkdir(parents=True, exist_ok=True)
        
        report = QueuedReport(report_data=sample_report_data)
        report_file = pending_folder / f"{report.report_id}.json"
        with open(report_file, 'w') as f:
            json.dump(report.to_dict(), f)
        
        # Create service (should load the file)
        service = ReportQueueService(
            connection=mock_connection,
            reports_folder=queue_folder,
            max_retries=3,
            retry_interval=1
        )
        
        assert len(service._queue) == 1
        assert service._queue[0].report_id == report.report_id


@pytest.mark.asyncio
class TestReportQueueServiceLifecycle:
    """Tests for service lifecycle (start/stop)"""
    
    async def test_start_service(self, queue_service):
        """Test starting the queue service"""
        await queue_service.start()
        
        assert queue_service._running is True
        assert queue_service._process_task is not None
    
    async def test_stop_service(self, queue_service):
        """Test stopping the queue service"""
        await queue_service.start()
        await queue_service.stop()
        
        assert queue_service._running is False
        assert queue_service._process_task is None
    
    async def test_start_idempotent(self, queue_service):
        """Test starting service multiple times is safe"""
        await queue_service.start()
        first_task = queue_service._process_task
        
        await queue_service.start()  # Start again
        
        assert queue_service._process_task == first_task  # Same task
    
    async def test_service_cleanup(self, queue_service):
        """Test service cleans up properly on stop"""
        await queue_service.start()
        task = queue_service._process_task
        
        await queue_service.stop()
        
        assert task.cancelled() or task.done()


@pytest.mark.asyncio
class TestQueueSubmit:
    """Tests for submitting reports to queue"""
    
    async def test_submit_while_offline(self, queue_service, sample_report_data):
        """Test submitting report while offline queues it"""
        result = await queue_service.submit(sample_report_data)
        
        assert result is True
        assert len(queue_service._queue) == 1
        
        queued_report = queue_service._queue[0]
        assert queued_report.status == ReportStatus.PENDING
        assert queued_report.report_data == sample_report_data
    
    async def test_submit_creates_file(self, queue_service, sample_report_data, queue_folder):
        """Test submitting report creates pending file"""
        await queue_service.submit(sample_report_data)
        
        pending_files = list((queue_folder / "pending").glob("*.json"))
        assert len(pending_files) == 1
        
        # Verify file contents
        with open(pending_files[0], 'r') as f:
            data = json.load(f)
        assert data['report_data'] == sample_report_data
    
    async def test_submit_multiple_reports(self, queue_service, sample_report_data):
        """Test submitting multiple reports"""
        await queue_service.submit(sample_report_data)
        await queue_service.submit({**sample_report_data, "serialNumber": "TEST-002"})
        await queue_service.submit({**sample_report_data, "serialNumber": "TEST-003"})
        
        assert len(queue_service._queue) == 3
        assert all(r.status == ReportStatus.PENDING for r in queue_service._queue)
    
    @patch('pywats_client.services.report_queue.logger')
    async def test_submit_handles_errors(self, mock_logger, queue_service):
        """Test submit handles errors gracefully"""
        # Submit invalid data that will cause serialization error
        invalid_data = {"circular_ref": None}
        invalid_data["circular_ref"] = invalid_data  # Can't serialize circular refs
        
        with patch.object(queue_service, '_save_report', side_effect=Exception("Disk full")):
            result = await queue_service.submit({"valid": "data"})
        
        assert result is False


@pytest.mark.asyncio
class TestQueuePersistence:
    """Tests for queue persistence operations"""
    
    async def test_save_report(self, queue_service, sample_report_data, queue_folder):
        """Test saving report to disk"""
        report = QueuedReport(report_data=sample_report_data)
        queue_service._save_report(report)
        
        report_file = queue_folder / "pending" / f"{report.report_id}.json"
        assert report_file.exists()
        
        with open(report_file, 'r') as f:
            data = json.load(f)
        assert data['report_id'] == report.report_id
    
    async def test_move_to_completed(self, queue_service, sample_report_data, queue_folder):
        """Test moving report to completed folder"""
        report = QueuedReport(report_data=sample_report_data)
        queue_service._queue.append(report)
        queue_service._save_report(report)
        
        queue_service._move_to_completed(report)
        
        # Check moved to completed
        completed_file = queue_folder / "completed" / f"{report.report_id}.json"
        assert completed_file.exists()
        
        # Check removed from pending
        pending_file = queue_folder / "pending" / f"{report.report_id}.json"
        assert not pending_file.exists()
        
        # Check removed from in-memory queue
        assert report not in queue_service._queue
    
    async def test_move_to_failed(self, queue_service, sample_report_data, queue_folder):
        """Test moving report to failed folder"""
        report = QueuedReport(report_data=sample_report_data)
        report.error = "Max retries exceeded"
        queue_service._queue.append(report)
        queue_service._save_report(report)
        
        queue_service._move_to_failed(report)
        
        # Check moved to failed
        failed_file = queue_folder / "failed" / f"{report.report_id}.json"
        assert failed_file.exists()
        
        # Verify error is saved
        with open(failed_file, 'r') as f:
            data = json.load(f)
        assert data['error'] == "Max retries exceeded"
        
        # Check removed from pending
        pending_file = queue_folder / "pending" / f"{report.report_id}.json"
        assert not pending_file.exists()


@pytest.mark.asyncio
class TestQueueRetry:
    """Tests for retry logic"""
    
    async def test_retry_failed_report(self, queue_service, sample_report_data, queue_folder):
        """Test retrying a failed report"""
        # Create a failed report
        report = QueuedReport(
            report_data=sample_report_data,
            status=ReportStatus.FAILED,
            attempts=3,
            error="Connection failed"
        )
        
        # Save to failed folder
        failed_file = queue_folder / "failed" / f"{report.report_id}.json"
        with open(failed_file, 'w') as f:
            json.dump(report.to_dict(), f)
        
        # Retry the report
        result = await queue_service.retry_failed(report.report_id)
        
        assert result is True
        
        # Check moved back to pending
        assert len(queue_service._queue) == 1
        retried = queue_service._queue[0]
        assert retried.report_id == report.report_id
        assert retried.status == ReportStatus.PENDING
        assert retried.attempts == 0  # Reset attempts
        assert retried.error is None  # Clear error
        
        # Check removed from failed folder
        assert not failed_file.exists()
    
    async def test_retry_nonexistent_report(self, queue_service):
        """Test retrying a report that doesn't exist"""
        result = await queue_service.retry_failed("nonexistent-id")
        
        assert result is False


@pytest.mark.asyncio
class TestQueueStatus:
    """Tests for queue status reporting"""
    
    async def test_get_status_empty_queue(self, queue_service):
        """Test getting status of empty queue"""
        status = queue_service.get_status()
        
        assert status['pending'] == 0
        assert status['failed'] == 0
        assert 'folder' in status
    
    async def test_get_status_with_reports(self, queue_service, sample_report_data, queue_folder):
        """Test getting status with reports in queue"""
        # Add pending reports
        await queue_service.submit(sample_report_data)
        await queue_service.submit(sample_report_data)
        
        # Add failed report
        failed_file = queue_folder / "failed" / "failed-001.json"
        failed_data = QueuedReport(report_data=sample_report_data, status=ReportStatus.FAILED)
        with open(failed_file, 'w') as f:
            json.dump(failed_data.to_dict(), f)
        
        status = queue_service.get_status()
        
        assert status['pending'] == 2
        assert status['failed'] == 1
    
    async def test_get_pending_reports(self, queue_service, sample_report_data):
        """Test getting list of pending reports"""
        await queue_service.submit(sample_report_data)
        await queue_service.submit({**sample_report_data, "serialNumber": "TEST-002"})
        
        pending = queue_service.get_pending_reports()
        
        assert len(pending) == 2
        assert all(isinstance(r, dict) for r in pending)
        assert all(r['status'] == 'pending' for r in pending)


@pytest.mark.integration
@pytest.mark.asyncio
class TestQueueIntegration:
    """Integration tests for queue service"""
    
    async def test_full_queue_lifecycle(self, mock_connection, queue_folder, sample_report_data):
        """Test complete queue workflow"""
        service = ReportQueueService(
            connection=mock_connection,
            reports_folder=queue_folder,
            max_retries=3,
            retry_interval=1
        )
        
        # 1. Start service
        await service.start()
        assert service._running is True
        
        # 2. Submit report
        result = await service.submit(sample_report_data)
        assert result is True
        assert len(service._queue) == 1
        
        # 3. Check status
        status = service.get_status()
        assert status['pending'] == 1
        
        # 4. Stop service
        await service.stop()
        assert service._running is False
        
        # 5. Restart and verify persistence
        service2 = ReportQueueService(
            connection=mock_connection,
            reports_folder=queue_folder,
            max_retries=3,
            retry_interval=1
        )
        assert len(service2._queue) == 1  # Loaded from disk
    
    async def test_connection_status_change(self, queue_service, mock_connection, sample_report_data):
        """Test queue processes when connection comes online"""
        await queue_service.start()
        
        # Submit report while offline
        await queue_service.submit(sample_report_data)
        assert len(queue_service._queue) == 1
        
        # Simulate connection coming online
        mock_connection.status = ConnectionStatus.ONLINE
        mock_client = MagicMock()
        mock_client.report.submit_wsjf = MagicMock(return_value="report-id-123")
        mock_connection.get_client.return_value = mock_client
        
        # Trigger connection change handler
        queue_service._on_connection_change(ConnectionStatus.ONLINE)
        
        # Give async task time to run
        await asyncio.sleep(0.1)
        
        # Note: Full upload test would need proper async mocking
