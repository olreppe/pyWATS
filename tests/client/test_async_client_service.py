"""
Tests for AsyncClientService

Tests the async service lifecycle, timers, and component integration.
"""

import asyncio
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock

# Test module
from pywats_client.service.async_client_service import (
    AsyncClientService,
    AsyncServiceStatus,
)


@pytest.fixture
def mock_config():
    """Create a mock ClientConfig"""
    config = MagicMock()
    config.get_runtime_credentials.return_value = (
        "https://test.wats.com",
        "test-token"
    )
    config.get_reports_path.return_value = Path("/tmp/reports")
    config.get_converters.return_value = []
    # Use MagicMock for config_path to avoid WindowsPath attribute issues
    mock_path = MagicMock()
    mock_path.exists.return_value = False
    config.config_path = mock_path
    return config


@pytest.fixture
def mock_async_wats():
    """Create a mock AsyncWATS client"""
    api = AsyncMock()
    api.get_version = AsyncMock(return_value="1.0.0")
    api.__aenter__ = AsyncMock(return_value=api)
    api.__aexit__ = AsyncMock()
    api.close = AsyncMock()
    return api


class TestAsyncServiceStatus:
    """Test service status enum"""
    
    def test_status_values(self):
        assert AsyncServiceStatus.STOPPED.value == "Stopped"
        assert AsyncServiceStatus.RUNNING.value == "Running"
        assert AsyncServiceStatus.START_PENDING.value == "StartPending"
        assert AsyncServiceStatus.STOP_PENDING.value == "StopPending"


class TestAsyncClientServiceInit:
    """Test service initialization"""
    
    @patch('pywats_client.service.async_client_service.ClientConfig')
    def test_init_default_instance(self, mock_config_cls, mock_config):
        """Test initialization with default instance ID"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        
        assert service.instance_id == "default"
        assert service.status == AsyncServiceStatus.STOPPED
        assert service.api is None
        mock_config_cls.load_for_instance.assert_called_once_with("default")
    
    @patch('pywats_client.service.async_client_service.ClientConfig')
    def test_init_custom_instance(self, mock_config_cls, mock_config):
        """Test initialization with custom instance ID"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService(instance_id="custom")
        
        assert service.instance_id == "custom"
        mock_config_cls.load_for_instance.assert_called_once_with("custom")
    
    @patch('pywats_client.service.async_client_service.ClientConfig')
    def test_initial_stats(self, mock_config_cls, mock_config):
        """Test initial statistics"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        
        stats = service.stats
        assert stats["start_time"] is None
        assert stats["reports_submitted"] == 0
        assert stats["api_status"] == "Offline"


class TestAsyncClientServiceLifecycle:
    """Test service lifecycle (start/stop)"""
    
    @pytest.mark.asyncio
    @patch('pywats_client.service.async_pending_queue.AsyncPendingQueue')
    @patch('pywats_client.service.async_converter_pool.AsyncConverterPool')
    @patch('pywats_client.service.async_client_service.ClientConfig')
    @patch('pywats_client.service.async_client_service.AsyncWATS')
    async def test_start_stop(self, mock_wats_cls, mock_config_cls, mock_pool_cls, mock_queue_cls, mock_config, mock_async_wats):
        """Test basic start and stop"""
        mock_config_cls.load_for_instance.return_value = mock_config
        mock_wats_cls.return_value = mock_async_wats
        
        # Set up mock queue
        mock_queue_instance = MagicMock()
        mock_queue_instance.run = AsyncMock()
        mock_queue_instance.stop = AsyncMock()
        mock_queue_instance.stats = {}
        mock_queue_cls.return_value = mock_queue_instance
        
        # Set up mock pool
        mock_pool_instance = MagicMock()
        mock_pool_instance.run = AsyncMock()
        mock_pool_instance.stop = AsyncMock()
        mock_pool_instance.stats = {}
        mock_pool_cls.return_value = mock_pool_instance
        
        service = AsyncClientService()
        
        # Mock the IPC/health servers
        with patch.object(service, '_setup_ipc_server', new_callable=AsyncMock):
            with patch.object(service, '_start_health_server', new_callable=AsyncMock):
                # Start service
                await service.start()
                
                assert service.status == AsyncServiceStatus.RUNNING
                assert service.is_running
                
                # Stop service
                await service.stop()
                
                assert service.status == AsyncServiceStatus.STOPPED
                assert not service.is_running
    
    @pytest.mark.asyncio
    @patch('pywats_client.service.async_client_service.ClientConfig')
    async def test_request_shutdown(self, mock_config_cls, mock_config):
        """Test shutdown request"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        
        # Request shutdown
        service.request_shutdown()
        
        # Shutdown event should be set
        assert service._shutdown_event.is_set()


class TestAsyncClientServiceTimers:
    """Test async timer loops"""
    
    @pytest.mark.asyncio
    @patch('pywats_client.service.async_client_service.ClientConfig')
    async def test_watchdog_loop_checks_api(self, mock_config_cls, mock_config, mock_async_wats):
        """Test watchdog checks API health"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        service.api = mock_async_wats
        
        # Call watchdog handler directly
        await service._on_watchdog_elapsed()
        
        # Should have called get_version
        mock_async_wats.get_version.assert_called_once()
        assert service._stats["api_status"] == "Online"
    
    @pytest.mark.asyncio
    @patch('pywats_client.service.async_client_service.ClientConfig')
    async def test_watchdog_handles_api_error(self, mock_config_cls, mock_config, mock_async_wats):
        """Test watchdog handles API error"""
        mock_config_cls.load_for_instance.return_value = mock_config
        mock_async_wats.get_version.side_effect = Exception("Connection failed")
        
        service = AsyncClientService()
        service.api = mock_async_wats
        
        await service._on_watchdog_elapsed()
        
        assert service._stats["api_status"] == "Offline"
    
    @pytest.mark.asyncio
    @patch('pywats_client.service.async_client_service.ClientConfig')
    async def test_ping_updates_timestamp(self, mock_config_cls, mock_config, mock_async_wats):
        """Test ping updates last_ping timestamp"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        service.api = mock_async_wats
        
        await service._on_ping_elapsed()
        
        assert service._stats["last_ping"] is not None


class TestAsyncClientServiceIPC:
    """Test IPC command handlers"""
    
    @patch('pywats_client.service.async_client_service.ClientConfig')
    def test_get_service_status(self, mock_config_cls, mock_config):
        """Test get_service_status returns correct data"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        
        status = service.get_service_status()
        
        assert "status" in status
        assert "api_status" in status
        assert status["status"] == "Stopped"
    
    @patch('pywats_client.service.async_client_service.ClientConfig')
    def test_get_credentials(self, mock_config_cls, mock_config):
        """Test get_credentials returns credentials"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        
        creds = service.get_credentials()
        
        assert creds is not None
        assert creds["base_url"] == "https://test.wats.com"
        assert creds["token"] == "test-token"


class TestAsyncClientServiceHealth:
    """Test health status"""
    
    @patch('pywats_client.service.async_client_service.ClientConfig')
    def test_health_status_when_stopped(self, mock_config_cls, mock_config):
        """Test health status when stopped"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        
        health = service._get_health_status()
        
        assert health["status"] == "unhealthy"
        assert health["service_status"] == "Stopped"
    
    @patch('pywats_client.service.async_client_service.ClientConfig')
    def test_health_status_when_running(self, mock_config_cls, mock_config):
        """Test health status when running"""
        mock_config_cls.load_for_instance.return_value = mock_config
        
        service = AsyncClientService()
        service._status = AsyncServiceStatus.RUNNING
        
        health = service._get_health_status()
        
        assert health["status"] == "healthy"
        assert health["service_status"] == "Running"
