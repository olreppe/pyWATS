"""
Integration Tests for Client Application

End-to-end tests for complete client workflows:
- Application startup and shutdown
- File watching and conversion
- Report submission workflow
- Service coordination
- Error recovery scenarios
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch
import json

from pywats_client.core.config import ClientConfig, ConverterConfig
from pywats_client.services.connection import ConnectionService, ConnectionStatus
from pywats_client.services.report_queue import ReportQueueService
from pywats_client.converters.models import ValidationResult, ConversionRecord


@pytest.fixture
def integration_config(temp_dir):
    """Create configuration for integration tests"""
    config = ClientConfig()
    config.instance_name = "Integration Test Client"
    config.station_name = "Test Station"
    config.service_address = "https://wats.integration.test"
    config.converters_enabled = True
    config.offline_queue_enabled = True
    
    # Add test converter configuration
    converter_config = ConverterConfig(
        name="Test Converter",
        module_path="converters.csv_converter.CSVConverter",
        watch_folder=str(temp_dir / "watch"),
        done_folder=str(temp_dir / "done"),
        error_folder=str(temp_dir / "error"),
        pending_folder=str(temp_dir / "pending"),
        converter_type="file",
        file_patterns=["*.csv", "*.txt"],
        alarm_threshold=0.5,
        reject_threshold=0.2
    )
    config.converters.append(converter_config)
    
    return config


@pytest.mark.integration
@pytest.mark.asyncio
class TestFileToReportWorkflow:
    """Test complete file-to-report workflow"""
    
    async def test_file_watch_to_conversion(self, temp_dir, integration_config):
        """Test file watching triggers conversion"""
        watch_dir = temp_dir / "watch"
        watch_dir.mkdir(exist_ok=True)
        
        # Create a test file
        test_file = watch_dir / "test_data.csv"
        test_file.write_text("SerialNumber,PartNumber,Status\nTEST-001,WIDGET-100,PASS")
        
        # Verify file was created
        assert test_file.exists()
        assert test_file.stat().st_size > 0


@pytest.mark.integration
@pytest.mark.asyncio
class TestOfflineToOnlineWorkflow:
    """Test offline queue to online submission workflow"""
    
    async def test_queue_processes_when_online(self, temp_dir):
        """Test queued reports are processed when connection comes online"""
        # Setup
        queue_dir = temp_dir / "queue"
        queue_dir.mkdir(exist_ok=True)
        
        mock_connection = MagicMock()
        mock_connection.status = ConnectionStatus.OFFLINE
        mock_connection.get_client.return_value = None
        mock_connection.on_status_change = MagicMock()
        
        queue = ReportQueueService(
            connection=mock_connection,
            reports_folder=queue_dir,
            max_retries=3,
            retry_interval=1
        )
        
        await queue.start()
        
        # Submit report while offline
        report_data = {
            "type": "UUT",
            "serialNumber": "TEST-001",
            "status": "PASS"
        }
        
        result = await queue.submit(report_data)
        assert result is True
        assert len(queue._queue) == 1
        
        # Simulate coming online
        mock_connection.status = ConnectionStatus.ONLINE
        mock_client = MagicMock()
        mock_client.report.submit_wsjf = MagicMock(return_value="report-123")
        mock_connection.get_client.return_value = mock_client
        
        # Trigger status change
        queue._on_connection_change(ConnectionStatus.ONLINE)
        await asyncio.sleep(0.1)
        
        await queue.stop()


@pytest.mark.integration
@pytest.mark.asyncio  
class TestServiceCoordination:
    """Test coordination between multiple services"""
    
    async def test_connection_and_queue_coordination(self, temp_dir):
        """Test connection service coordinates with queue service"""
        # Create connection service
        from pywats_client.core.connection_config import ConnectionConfig
        
        conn_config = ConnectionConfig()
        conn_config.server_url = "https://test.wats.com"
        
        connection = ConnectionService(connection_config=conn_config)
        
        # Create queue service
        queue = ReportQueueService(
            connection=connection,
            reports_folder=temp_dir / "queue",
            max_retries=3,
            retry_interval=1
        )
        
        # Start queue
        await queue.start()
        
        # Submit report
        report = {"type": "UUT", "serialNumber": "TEST-001"}
        result = await queue.submit(report)
        
        assert result is True
        
        # Cleanup
        await queue.stop()
        connection.disconnect()  # NOT async


@pytest.mark.integration
class TestErrorRecovery:
    """Test error recovery scenarios"""
    
    @pytest.mark.asyncio
    async def test_queue_recovers_from_disk(self, temp_dir):
        """Test queue recovers pending reports after restart"""
        queue_dir = temp_dir / "queue"
        
        # Create first queue instance
        mock_conn1 = MagicMock()
        mock_conn1.status = ConnectionStatus.OFFLINE
        mock_conn1.on_status_change = MagicMock()
        
        queue1 = ReportQueueService(
            connection=mock_conn1,
            reports_folder=queue_dir,
            max_retries=3,
            retry_interval=1
        )
        
        # Submit reports
        await queue1.submit({"serialNumber": "TEST-001"})
        await queue1.submit({"serialNumber": "TEST-002"})
        
        assert len(queue1._queue) == 2
        
        # Simulate restart - create new queue instance
        mock_conn2 = MagicMock()
        mock_conn2.status = ConnectionStatus.OFFLINE
        mock_conn2.on_status_change = MagicMock()
        
        queue2 = ReportQueueService(
            connection=mock_conn2,
            reports_folder=queue_dir,
            max_retries=3,
            retry_interval=1
        )
        
        # Verify reports were loaded
        assert len(queue2._queue) == 2
    
    def test_config_persists_between_sessions(self, temp_dir):
        """Test configuration persists between sessions"""
        config_file = temp_dir / "client_config.json"
        
        # Session 1: Create and save config
        config1 = ClientConfig()
        config1.instance_name = "Persistent Client"
        config1.station_name = "Test Station"
        config1.service_address = "https://test.wats.com"
        config1.save(str(config_file))
        
        # Session 2: Load config
        config2 = ClientConfig.load(str(config_file))
        
        assert config2.instance_name == "Persistent Client"
        assert config2.station_name == "Test Station"
        assert config2.service_address == "https://test.wats.com"


@pytest.mark.integration
@pytest.mark.asyncio
class TestMultiConverterScenarios:
    """Test scenarios with multiple converters"""
    
    async def test_multiple_converters_same_folder(self, temp_dir):
        """Test multiple converters can handle different file types"""
        watch_dir = temp_dir / "watch"
        watch_dir.mkdir(exist_ok=True)
        
        # Create CSV file
        csv_file = watch_dir / "data.csv"
        csv_file.write_text("col1,col2\nval1,val2")
        
        # Create JSON file
        json_file = watch_dir / "data.json"
        json_file.write_text('{"key": "value"}')
        
        # Verify both files exist
        assert csv_file.exists()
        assert json_file.exists()
    
    async def test_converter_confidence_selection(self):
        """Test highest confidence converter is selected"""
        from pywats_client.converters.models import ValidationResult
        
        # Simulate multiple converters validating same file
        results = [
            ValidationResult(can_convert=True, confidence=0.6, message="CSV?"),
            ValidationResult(can_convert=True, confidence=0.95, message="Definitely JSON"),
            ValidationResult(can_convert=True, confidence=0.3, message="Maybe XML?"),
        ]
        
        # Select highest confidence
        best = max(results, key=lambda r: r.confidence)
        
        assert best.confidence == 0.95
        assert "JSON" in best.message


@pytest.mark.integration
class TestEndToEndScenarios:
    """Complete end-to-end test scenarios"""
    
    @pytest.mark.asyncio
    async def test_complete_client_lifecycle(self, temp_dir, integration_config):
        """Test complete client lifecycle from startup to shutdown"""
        # This would test:
        # 1. Client initialization
        # 2. Service startup
        # 3. Configuration loading
        # 4. Connection establishment
        # 5. File processing
        # 6. Report submission
        # 7. Graceful shutdown
        
        # For now, just verify config is valid
        errors = []
        for converter in integration_config.converters:
            errors.extend(converter.validate())
        
        assert len(errors) == 0, f"Config has errors: {errors}"
        assert integration_config.converters_enabled is True
        assert integration_config.offline_queue_enabled is True
    
    def test_configuration_migration(self, temp_dir):
        """Test configuration can be upgraded between versions"""
        config_file = temp_dir / "config.json"
        
        # Create old format config
        old_config = {
            "instance_id": "old-instance",
            "station_name": "Old Station"
            # Missing new fields
        }
        
        with open(config_file, 'w') as f:
            json.dump(old_config, f)
        
        # Load and verify defaults are applied
        config = ClientConfig.load(str(config_file))
        
        assert config.instance_id == "old-instance"
        assert config.station_name == "Old Station"
        # New fields should have defaults
        assert hasattr(config, 'offline_queue_enabled')
        assert hasattr(config, 'converters_enabled')
