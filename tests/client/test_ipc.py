"""
Tests for Async IPC Communication

Tests service discovery and command/response communication
using pure asyncio IPC (no Qt dependency).
"""

import pytest
import json
import asyncio
from unittest.mock import MagicMock, AsyncMock

from pywats_client.service.async_ipc_server import AsyncIPCServer, get_socket_address
from pywats_client.service.async_ipc_client import AsyncIPCClient, ServiceStatus


class TestAsyncIPCServer:
    """Test AsyncIPCServer functionality"""
    
    def test_socket_address_format_windows(self):
        """Test socket address generation for Windows (TCP localhost)"""
        import sys
        if sys.platform == 'win32':
            addr = get_socket_address("test")
            host, port = addr
            assert host == "127.0.0.1"
            assert 50000 <= port <= 59999
    
    def test_socket_address_deterministic(self):
        """Test that same instance_id gives same address"""
        addr1 = get_socket_address("my_instance")
        addr2 = get_socket_address("my_instance")
        assert addr1 == addr2
    
    def test_socket_address_unique_per_instance(self):
        """Test that different instances get different addresses"""
        addr1 = get_socket_address("instance1")
        addr2 = get_socket_address("instance2")
        assert addr1 != addr2
    
    def test_server_initialization(self):
        """Test AsyncIPCServer creation"""
        mock_service = MagicMock()
        
        server = AsyncIPCServer(instance_id="test", service=mock_service)
        
        assert server.instance_id == "test"
        assert server._service == mock_service
        assert server._running is False
    
    @pytest.mark.asyncio
    async def test_server_start_stop(self):
        """Test server lifecycle"""
        mock_service = MagicMock()
        mock_service.get_status.return_value = {'status': 'Running'}
        
        server = AsyncIPCServer(instance_id="test_lifecycle", service=mock_service)
        
        # Start server
        await server.start()
        assert server._running is True
        assert server._server is not None
        
        # Stop server
        await server.stop()
        assert server._running is False
    
    @pytest.mark.asyncio
    async def test_server_client_communication(self):
        """Test server-client communication"""
        mock_service = MagicMock()
        mock_service.get_status.return_value = {
            'status': 'Running',
            'api_status': 'Online',
            'pending_count': 5
        }
        
        server = AsyncIPCServer(instance_id="test_comm", service=mock_service)
        await server.start()
        
        try:
            # Connect client
            client = AsyncIPCClient("test_comm")
            connected = await client.connect()
            assert connected is True
            
            # Get status
            status = await client.get_status()
            assert status.status == 'Running'
            assert status.api_status == 'Online'
            assert status.pending_count == 5
            
            # Ping
            pong = await client.ping()
            assert pong is True
            
            await client.disconnect()
        finally:
            await server.stop()


class TestAsyncIPCClient:
    """Test AsyncIPCClient functionality"""
    
    def test_client_initialization(self):
        """Test AsyncIPCClient creation"""
        client = AsyncIPCClient(instance_id="test")
        
        assert client.instance_id == "test"
        assert client.connected is False
    
    @pytest.mark.asyncio
    async def test_client_connect_no_server(self):
        """Test client connection when no server running"""
        client = AsyncIPCClient(instance_id="nonexistent_server_12345")
        
        # Should fail gracefully
        connected = await client.connect()
        assert connected is False
        assert client.connected is False


class TestIPCProtocol:
    """Test IPC command/response protocol"""
    
    def test_command_structure(self):
        """Test command/request structure"""
        command = {
            'command': 'get_status',
            'instance_id': 'test'
        }
        
        serialized = json.dumps(command)
        deserialized = json.loads(serialized)
        
        assert deserialized['command'] == 'get_status'
        assert deserialized['instance_id'] == 'test'
    
    def test_response_structure(self):
        """Test response structure"""
        response = {
            'success': True,
            'data': {
                'status': 'Running',
                'api_status': 'Online'
            }
        }
        
        serialized = json.dumps(response)
        deserialized = json.loads(serialized)
        
        assert deserialized['success'] is True
        assert 'data' in deserialized
    
    def test_error_response_structure(self):
        """Test error response structure"""
        error_response = {
            'success': False,
            'error': 'Unknown command: invalid_cmd'
        }
        
        serialized = json.dumps(error_response)
        deserialized = json.loads(serialized)
        
        assert deserialized['success'] is False
        assert 'Unknown command' in deserialized['error']
    
    def test_all_commands_serializable(self):
        """Test different command types"""
        commands = ['get_status', 'get_config', 'ping', 'stop', 'restart']
        
        for cmd in commands:
            command = {'command': cmd}
            serialized = json.dumps(command)
            deserialized = json.loads(serialized)
            assert deserialized['command'] == cmd


class TestServiceStatus:
    """Test ServiceStatus dataclass"""
    
    def test_service_status_creation(self):
        """Test ServiceStatus dataclass"""
        status = ServiceStatus(
            status='Running',
            api_status='Online',
            pending_count=10,
            instance_id='test'
        )
        
        assert status.status == 'Running'
        assert status.api_status == 'Online'
        assert status.pending_count == 10
        assert status.instance_id == 'test'
    
    def test_service_status_defaults(self):
        """Test ServiceStatus defaults"""
        status = ServiceStatus()
        
        assert status.status == 'Unknown'
        assert status.api_status == 'Unknown'
        assert status.pending_count == 0
        assert status.instance_id == ''

