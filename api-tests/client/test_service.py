"""
Tests for Client Service Components

Tests ClientService, PendingWatcher, and ConverterPool.
"""

import pytest
import time
import threading
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, Mock
from pywats_client.service.client_service import ClientService, ServiceStatus
from pywats_client.service.pending_watcher import PendingWatcher, PendingWatcherState
from pywats_client.service.converter_pool import ConverterPool

# Mock PySide6 before importing modules that use it
sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtCore'] = MagicMock()


class TestClientService:
    """Test main service controller"""
    
    def test_service_initialization(self, tmp_path, monkeypatch):
        """Test service creation and initial state"""
        # Mock config loading
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.converters = []
        
        with patch('pywats_client.service.client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            
            assert service.instance_id == "test"
            assert service.status == ServiceStatus.STOPPED
            assert service.api is None
            assert service.converter_pool is None
            assert service.pending_watcher is None
    
    def test_service_status_property(self, tmp_path):
        """Test service status tracking"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.converters = []
        
        with patch('pywats_client.service.client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            
            assert service.status == ServiceStatus.STOPPED
            # Status should update during lifecycle
            assert service._status == ServiceStatus.STOPPED
    
    def test_api_status_offline(self, tmp_path):
        """Test API status when not connected"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        
        with patch('pywats_client.service.client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            
            assert service.api_status == "Offline"
    
    def test_api_status_online(self, tmp_path):
        """Test API status when connected"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        
        with patch('pywats_client.service.client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            service.api = MagicMock()
            
            assert service.api_status == "Online"
    
    def test_service_double_start_protection(self, tmp_path):
        """Test that service prevents double start"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.converters = []
        
        with patch('pywats_client.service.client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            service._running = True
            
            # Should not start if already running
            service.start()  # Should log warning and return
            
            # Verify it didn't change state
            assert service._running == True
    
    def test_service_stop_when_not_running(self, tmp_path):
        """Test stopping service when not running"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        
        with patch('pywats_client.service.client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            
            # Should handle gracefully
            service.stop()
            
            assert service.status == ServiceStatus.STOPPED


class TestPendingWatcher:
    """Test report queue manager"""
    
    def test_pending_watcher_creation(self, tmp_path):
        """Test PendingWatcher initialization"""
        reports_dir = tmp_path / "reports"
        mock_api = MagicMock()
        
        watcher = PendingWatcher(
            api_client=mock_api,
            reports_directory=reports_dir,
            initialize_async=False
        )
        
        assert watcher.reports_directory == reports_dir
        assert reports_dir.exists()
        assert watcher.api_client == mock_api
        assert watcher.state in [PendingWatcherState.CREATED, PendingWatcherState.RUNNING]
    
    def test_pending_watcher_async_initialization(self, tmp_path):
        """Test async initialization mode"""
        reports_dir = tmp_path / "reports"
        mock_api = MagicMock()
        
        watcher = PendingWatcher(
            api_client=mock_api,
            reports_directory=reports_dir,
            initialize_async=True
        )
        
        # Give async thread time to start
        time.sleep(0.5)
        
        assert watcher.state == PendingWatcherState.RUNNING
        assert watcher._running
        
        # Cleanup
        watcher.dispose()
    
    def test_pending_watcher_file_monitoring(self, tmp_path):
        """Test file system watcher for .queued files"""
        reports_dir = tmp_path / "reports"
        mock_api = MagicMock()
        
        watcher = PendingWatcher(
            api_client=mock_api,
            reports_directory=reports_dir,
            initialize_async=False
        )
        
        # Verify observer is set up
        assert watcher._observer is not None
        
        # Cleanup
        watcher.dispose()
    
    def test_pending_watcher_dispose(self, tmp_path):
        """Test cleanup on dispose"""
        reports_dir = tmp_path / "reports"
        mock_api = MagicMock()
        
        watcher = PendingWatcher(
            api_client=mock_api,
            reports_directory=reports_dir,
            initialize_async=False
        )
        
        watcher.dispose()
        
        assert watcher.state == PendingWatcherState.DISPOSED
        assert not watcher._running
    
    def test_pending_watcher_submission_lock(self, tmp_path):
        """Test thread-safe submission with lock"""
        reports_dir = tmp_path / "reports"
        mock_api = MagicMock()
        
        watcher = PendingWatcher(
            api_client=mock_api,
            reports_directory=reports_dir,
            initialize_async=False
        )
        
        # Lock should exist for thread safety
        assert watcher._submission_lock is not None
        
        # Should be able to acquire lock
        acquired = watcher._submission_lock.acquire(timeout=1)
        assert acquired
        watcher._submission_lock.release()
        
        # Cleanup
        watcher.dispose()


class TestConverterPool:
    """Test converter pool and worker management"""
    
    def test_converter_pool_initialization(self, tmp_path):
        """Test pool creation"""
        mock_config = MagicMock()
        mock_config.converters = []
        mock_config.max_converter_workers = 5
        mock_api = MagicMock()
        
        pool = ConverterPool(config=mock_config, api_client=mock_api)
        
        assert pool.config == mock_config
        assert pool.api_client == mock_api
        assert pool._max_workers == 5
        assert len(pool.converter_list) == 0
    
    def test_converter_pool_default_max_workers(self, tmp_path):
        """Test default worker limit"""
        mock_config = MagicMock()
        mock_config.converters = []
        # No max_converter_workers attribute
        del mock_config.max_converter_workers
        mock_api = MagicMock()
        
        pool = ConverterPool(config=mock_config, api_client=mock_api)
        
        # Should default to 10
        assert pool._max_workers == 10
    
    def test_converter_pool_worker_limit_bounds(self, tmp_path):
        """Test worker limit enforcement"""
        mock_config = MagicMock()
        mock_config.converters = []
        mock_api = MagicMock()
        
        # Test zero workers defaults to 1
        mock_config.max_converter_workers = 0
        pool1 = ConverterPool(config=mock_config, api_client=mock_api)
        assert pool1._max_workers == 1
        
        # Test > 50 capped to 50
        mock_config.max_converter_workers = 100
        pool2 = ConverterPool(config=mock_config, api_client=mock_api)
        assert pool2._max_workers == 50
    
    def test_converter_pool_converter_list(self, tmp_path):
        """Test converter list management"""
        mock_config = MagicMock()
        mock_config.converters = []
        mock_config.max_converter_workers = 5
        mock_api = MagicMock()
        
        pool = ConverterPool(config=mock_config, api_client=mock_api)
        
        assert isinstance(pool.converter_list, list)
        assert len(pool.converter_list) == 0
    
    def test_converter_pool_dispose_flag(self, tmp_path):
        """Test disposal flag"""
        mock_config = MagicMock()
        mock_config.converters = []
        mock_config.max_converter_workers = 5
        mock_api = MagicMock()
        
        pool = ConverterPool(config=mock_config, api_client=mock_api)
        
        assert not pool._disposing
        
        # After disposal
        pool.dispose()
        assert pool._disposing
    
    def test_converter_pool_pending_queue(self, tmp_path):
        """Test pending conversion queue"""
        mock_config = MagicMock()
        mock_config.converters = []
        mock_config.max_converter_workers = 5
        mock_api = MagicMock()
        
        pool = ConverterPool(config=mock_config, api_client=mock_api)
        
        # Verify queue structures exist
        assert pool._pending is not None
        assert pool._pending_queue is not None
        assert pool._pending_lock is not None
