"""
Tests for Client Service Components

Tests AsyncClientService and ClientService (sync entry point).
Architecture: Async-first.
"""

import pytest
import asyncio
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock

# Mock PySide6 before importing modules that use it
sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtCore'] = MagicMock()
sys.modules['PySide6.QtNetwork'] = MagicMock()

from pywats_client.service.client_service import ClientService, ServiceStatus
from pywats_client.service.async_client_service import AsyncClientService, AsyncServiceStatus
from pywats_client.service.async_pending_queue import AsyncPendingQueue, AsyncPendingQueueState
from pywats_client.service.async_converter_pool import AsyncConverterPool


class TestClientService:
    """Test sync entry point for AsyncClientService"""
    
    def test_service_initialization(self, tmp_path, monkeypatch):
        """Test sync service creation and initial state"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.config_path = tmp_path / "config.json"
        mock_config.converters = []
        
        with patch('pywats_client.service.async_client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            
            assert service.instance_id == "test"
            assert service.status == ServiceStatus.STOPPED
            assert service._async is not None
    
    def test_service_status_mapping(self, tmp_path):
        """Test status mapping from async to sync"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.config_path = tmp_path / "config.json"
        
        with patch('pywats_client.service.async_client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            
            # Initial state
            assert service.status == ServiceStatus.STOPPED
            
            # Simulate async status change
            service._async._status = AsyncServiceStatus.RUNNING
            assert service.status == ServiceStatus.RUNNING
    
    def test_api_status_offline(self, tmp_path):
        """Test API status when not connected"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.config_path = tmp_path / "config.json"
        
        with patch('pywats_client.service.async_client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            
            assert service.api_status == "Offline"
    
    def test_stop_signals_shutdown(self, tmp_path):
        """Test that stop() signals the async service to shutdown"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.config_path = tmp_path / "config.json"
        
        with patch('pywats_client.service.async_client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = ClientService(instance_id="test")
            
            # Verify shutdown event is not set
            assert not service._async._shutdown_event.is_set()
            
            # Call stop
            service.stop()
            
            # Verify shutdown was requested
            assert service._async._shutdown_event.is_set()


class TestAsyncClientService:
    """Test async client service"""
    
    @pytest.mark.asyncio
    async def test_async_service_initialization(self, tmp_path):
        """Test async service creation and initial state"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.config_path = tmp_path / "config.json"
        mock_config.converters = []
        mock_config.get_converters = MagicMock(return_value=[])
        
        with patch('pywats_client.service.async_client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = AsyncClientService(instance_id="test")
            
            assert service.instance_id == "test"
            assert service.status == AsyncServiceStatus.STOPPED
            assert service.api is None
    
    @pytest.mark.asyncio
    async def test_async_service_request_shutdown(self, tmp_path):
        """Test shutdown request mechanism"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.config_path = tmp_path / "config.json"
        
        with patch('pywats_client.service.async_client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = AsyncClientService(instance_id="test")
            
            assert not service._shutdown_event.is_set()
            service.request_shutdown()
            assert service._shutdown_event.is_set()
    
    @pytest.mark.asyncio
    async def test_async_service_stats(self, tmp_path):
        """Test service statistics"""
        mock_config = MagicMock()
        mock_config.get_reports_path.return_value = tmp_path / "reports"
        mock_config.config_path = tmp_path / "config.json"
        
        with patch('pywats_client.service.async_client_service.ClientConfig') as mock_config_class:
            mock_config_class.load_for_instance.return_value = mock_config
            service = AsyncClientService(instance_id="test")
            
            stats = service.stats
            assert "start_time" in stats
            assert "reports_submitted" in stats
            assert "errors" in stats


class TestAsyncPendingQueue:
    """Test async pending queue"""
    
    @pytest.mark.asyncio
    async def test_queue_initialization(self, tmp_path):
        """Test AsyncPendingQueue initialization"""
        reports_dir = tmp_path / "reports"
        mock_api = AsyncMock()
        
        queue = AsyncPendingQueue(
            api=mock_api,
            reports_dir=reports_dir,
            max_concurrent=5
        )
        
        assert queue.reports_dir == reports_dir
        assert reports_dir.exists()
        assert queue._max_concurrent == 5
        assert queue.state == AsyncPendingQueueState.CREATED
    
    @pytest.mark.asyncio
    async def test_queue_stats(self, tmp_path):
        """Test queue statistics"""
        reports_dir = tmp_path / "reports"
        mock_api = AsyncMock()
        
        queue = AsyncPendingQueue(
            api=mock_api,
            reports_dir=reports_dir,
            max_concurrent=5
        )
        
        stats = queue.stats
        assert "total_submitted" in stats
        assert "successful" in stats
        assert "errors" in stats
        assert "queued_files" in stats
    
    @pytest.mark.asyncio
    async def test_queue_stop_when_not_running(self, tmp_path):
        """Test stopping queue when not running"""
        reports_dir = tmp_path / "reports"
        mock_api = AsyncMock()
        
        queue = AsyncPendingQueue(
            api=mock_api,
            reports_dir=reports_dir,
            max_concurrent=5
        )
        
        # Should handle gracefully when not running
        await queue.stop()
        # State transitions to STOPPED after stop() regardless of initial state
        assert queue.state == AsyncPendingQueueState.STOPPED


class TestAsyncConverterPool:
    """Test async converter pool"""
    
    @pytest.mark.asyncio
    async def test_pool_initialization(self, tmp_path):
        """Test AsyncConverterPool initialization"""
        mock_config = MagicMock()
        mock_config.converters = []
        mock_config.get_converters = MagicMock(return_value=[])
        mock_api = AsyncMock()
        
        pool = AsyncConverterPool(
            config=mock_config,
            api=mock_api,
            max_concurrent=10
        )
        
        assert pool.config == mock_config
        assert pool._max_concurrent == 10
        assert not pool.is_running
    
    @pytest.mark.asyncio
    async def test_pool_stats(self, tmp_path):
        """Test pool statistics"""
        mock_config = MagicMock()
        mock_config.converters = []
        mock_api = AsyncMock()
        
        pool = AsyncConverterPool(
            config=mock_config,
            api=mock_api,
            max_concurrent=10
        )
        
        stats = pool.stats
        assert "total_processed" in stats
        assert "successful" in stats
        assert "errors" in stats
        assert "queue_size" in stats
    
    @pytest.mark.asyncio
    async def test_pool_stop_when_not_running(self, tmp_path):
        """Test stopping pool when not running"""
        mock_config = MagicMock()
        mock_config.converters = []
        mock_api = AsyncMock()
        
        pool = AsyncConverterPool(
            config=mock_config,
            api=mock_api,
            max_concurrent=10
        )
        
        # Should handle gracefully when not running
        await pool.stop()
        assert not pool.is_running
