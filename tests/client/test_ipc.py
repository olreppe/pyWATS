"""
Tests for IPC Communication

Tests service discovery and command/response communication.
Uses minimal mocking to test actual functionality.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import MagicMock
import sys

# Mock PySide6 only at module level
sys.modules['PySide6'] = MagicMock()
sys.modules['PySide6.QtCore'] = MagicMock()
sys.modules['PySide6.QtNetwork'] = MagicMock()

from pywats_client.service.ipc_server import IPCServer


class TestIPCCommunication:
    """Test inter-process communication between service and GUI"""
    
    def test_ipc_server_initialization(self):
        """Test IPC server creation"""
        mock_service = MagicMock()
        
        server = IPCServer(instance_id="test", service=mock_service)
        
        assert server.instance_id == "test"
        assert server.service == mock_service
        assert server.socket_name == "pyWATS_Service_test"
    
    def test_ipc_server_socket_naming(self):
        """Test socket naming convention"""
        mock_service = MagicMock()
        
        server1 = IPCServer(instance_id="default", service=mock_service)
        server2 = IPCServer(instance_id="production", service=mock_service)
        
        assert server1.socket_name == "pyWATS_Service_default"
        assert server2.socket_name == "pyWATS_Service_production"
        # Each instance should have unique socket
        assert server1.socket_name != server2.socket_name
    
    def test_ipc_socket_name_format(self):
        """Test socket name follows consistent format"""
        mock_service = MagicMock()
        
        instances = ["dev", "test", "staging", "prod"]
        for instance_id in instances:
            server = IPCServer(instance_id=instance_id, service=mock_service)
            expected = f"pyWATS_Service_{instance_id}"
            assert server.socket_name == expected
    
    def test_ipc_server_client_list(self):
        """Test server client tracking"""
        mock_service = MagicMock()
        server = IPCServer(instance_id="test", service=mock_service)
        
        # Should track connected clients
        assert isinstance(server._clients, list)
        assert len(server._clients) == 0
    
    def test_ipc_server_stop_cleanup(self):
        """Test server cleanup on stop"""
        mock_service = MagicMock()
        server = IPCServer(instance_id="test", service=mock_service)
        
        # Add mock clients
        mock_client1 = MagicMock()
        mock_client2 = MagicMock()
        server._clients = [mock_client1, mock_client2]
        
        # Mock server
        server._server = MagicMock()
        
        # Stop server
        server.stop()
        
        # Should close server
        server._server.close.assert_called_once()
        
        # Should disconnect all clients
        mock_client1.disconnectFromServer.assert_called_once()
        mock_client2.disconnectFromServer.assert_called_once()
        
        # Should clear client list
        assert len(server._clients) == 0
    
    def test_ipc_command_structure(self):
        """Test command/request structure"""
        # Commands should be JSON with 'command' field
        command = {
            'command': 'get_status',
            'instance_id': 'test'
        }
        
        # Should be serializable
        serialized = json.dumps(command)
        deserialized = json.loads(serialized)
        
        assert deserialized['command'] == 'get_status'
        assert deserialized['instance_id'] == 'test'
    
    def test_ipc_response_structure(self):
        """Test response structure"""
        # Responses should be JSON dicts
        response = {
            'status': 'ok',
            'data': {
                'service_status': 'Running',
                'api_status': 'Online'
            }
        }
        
        # Should be serializable
        serialized = json.dumps(response)
        deserialized = json.loads(serialized)
        
        assert deserialized['status'] == 'ok'
        assert 'data' in deserialized
    
    def test_ipc_error_response_structure(self):
        """Test error response structure"""
        error_response = {
            'error': 'Unknown command: invalid_cmd'
        }
        
        serialized = json.dumps(error_response)
        deserialized = json.loads(serialized)
        
        assert 'error' in deserialized
        assert 'Unknown command' in deserialized['error']
    
    def test_ipc_multiple_commands(self):
        """Test different command types"""
        commands = ['get_status', 'get_config', 'ping', 'stop', 'restart']
        
        for cmd in commands:
            command = {'command': cmd}
            serialized = json.dumps(command)
            deserialized = json.loads(serialized)
            assert deserialized['command'] == cmd
    
    def test_ipc_server_service_reference(self):
        """Test server maintains reference to service"""
        mock_service = MagicMock()
        mock_service.get_status_dict.return_value = {'status': 'Running'}
        
        server = IPCServer(instance_id="test", service=mock_service)
        
        # Server should have service reference
        assert server.service is mock_service
        
        # Should be able to call service methods
        status = server.service.get_status_dict()
        assert status['status'] == 'Running'

