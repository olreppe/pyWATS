"""
Tests for pywats_client connection configuration.
"""
import pytest
from datetime import datetime

from pywats_client.core.connection_config import (
    ConnectionState,
    ConnectionConfig,
    InstanceConfig,
    migrate_legacy_config,
)


class TestConnectionState:
    """Tests for ConnectionState enum."""
    
    def test_not_connected_value(self):
        """Test NOT_CONNECTED has correct value."""
        assert ConnectionState.NOT_CONNECTED.value == "Not Connected"
    
    def test_connected_value(self):
        """Test CONNECTED has correct value."""
        assert ConnectionState.CONNECTED.value == "Connected"
    
    def test_offline_value(self):
        """Test OFFLINE has correct value."""
        assert ConnectionState.OFFLINE.value == "Offline"
    
    def test_all_states_have_values(self):
        """Test all states have string values."""
        for state in ConnectionState:
            assert isinstance(state.value, str)
            assert len(state.value) > 0


class TestConnectionConfig:
    """Tests for ConnectionConfig dataclass."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = ConnectionConfig()
        assert config.server_url == ""
        assert config.username == ""
        assert config.token_encrypted == ""
        assert config.token_version == 1
        assert config.connection_state == "Not Connected"
        assert config.health_check_interval == 30
        assert config.health_check_timeout == 10
        assert config.auto_reconnect is True
        assert config.max_reconnect_attempts == 0
        assert config.reconnect_delay == 10
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = ConnectionConfig(
            server_url="https://wats.example.com",
            username="admin",
            health_check_interval=60,
        )
        assert config.server_url == "https://wats.example.com"
        assert config.username == "admin"
        assert config.health_check_interval == 60
    
    def test_get_state_connected(self):
        """Test get_state returns CONNECTED."""
        config = ConnectionConfig(connection_state="Connected")
        assert config.get_state() == ConnectionState.CONNECTED
    
    def test_get_state_offline(self):
        """Test get_state returns OFFLINE."""
        config = ConnectionConfig(connection_state="Offline")
        assert config.get_state() == ConnectionState.OFFLINE
    
    def test_get_state_not_connected(self):
        """Test get_state returns NOT_CONNECTED."""
        config = ConnectionConfig(connection_state="Not Connected")
        assert config.get_state() == ConnectionState.NOT_CONNECTED
    
    def test_get_state_invalid_fallback(self):
        """Test get_state falls back to NOT_CONNECTED for invalid state."""
        config = ConnectionConfig(connection_state="InvalidState")
        assert config.get_state() == ConnectionState.NOT_CONNECTED
    
    def test_set_state(self):
        """Test set_state updates connection_state."""
        config = ConnectionConfig()
        config.set_state(ConnectionState.CONNECTED)
        assert config.connection_state == "Connected"
    
    def test_is_authenticated_true(self):
        """Test is_authenticated returns True when credentials exist."""
        config = ConnectionConfig(
            server_url="https://example.com",
            token_encrypted="encrypted_token",
        )
        assert config.is_authenticated() is True
    
    def test_is_authenticated_false_no_token(self):
        """Test is_authenticated returns False without token."""
        config = ConnectionConfig(server_url="https://example.com")
        assert config.is_authenticated() is False
    
    def test_is_authenticated_false_no_url(self):
        """Test is_authenticated returns False without URL."""
        config = ConnectionConfig(token_encrypted="encrypted_token")
        assert config.is_authenticated() is False
    
    def test_is_connected(self):
        """Test is_connected returns True when state is CONNECTED."""
        config = ConnectionConfig(connection_state="Connected")
        assert config.is_connected() is True
        
        config.connection_state = "Offline"
        assert config.is_connected() is False
    
    def test_is_offline(self):
        """Test is_offline returns True when state is OFFLINE."""
        config = ConnectionConfig(connection_state="Offline")
        assert config.is_offline() is True
        
        config.connection_state = "Connected"
        assert config.is_offline() is False
    
    def test_mark_connected(self):
        """Test mark_connected updates state and stats."""
        config = ConnectionConfig()
        initial_connections = config.total_connections
        
        config.mark_connected()
        
        assert config.get_state() == ConnectionState.CONNECTED
        assert config.total_connections == initial_connections + 1
        assert config.last_connected is not None
    
    def test_mark_disconnected(self):
        """Test mark_disconnected clears credentials."""
        config = ConnectionConfig(
            server_url="https://example.com",
            username="admin",
            token_encrypted="token",
            connection_state="Connected",
        )
        initial_disconnections = config.total_disconnections
        
        config.mark_disconnected()
        
        assert config.get_state() == ConnectionState.NOT_CONNECTED
        assert config.total_disconnections == initial_disconnections + 1
        assert config.token_encrypted == ""
        assert config.username == ""
        assert config.last_disconnected is not None
    
    def test_mark_offline(self):
        """Test mark_offline sets OFFLINE state."""
        config = ConnectionConfig(connection_state="Connected")
        config.mark_offline()
        assert config.get_state() == ConnectionState.OFFLINE
    
    def test_record_health_check_success(self):
        """Test recording successful health check."""
        config = ConnectionConfig()
        initial_total = config.total_health_checks
        initial_failed = config.failed_health_checks
        
        config.record_health_check(success=True)
        
        assert config.total_health_checks == initial_total + 1
        assert config.failed_health_checks == initial_failed
    
    def test_record_health_check_failure(self):
        """Test recording failed health check."""
        config = ConnectionConfig()
        initial_total = config.total_health_checks
        initial_failed = config.failed_health_checks
        
        config.record_health_check(success=False)
        
        assert config.total_health_checks == initial_total + 1
        assert config.failed_health_checks == initial_failed + 1
    
    def test_get_health_check_success_rate_no_checks(self):
        """Test success rate is 100% when no checks performed."""
        config = ConnectionConfig()
        assert config.get_health_check_success_rate() == 100.0
    
    def test_get_health_check_success_rate_all_success(self):
        """Test success rate with all successful checks."""
        config = ConnectionConfig(total_health_checks=10, failed_health_checks=0)
        assert config.get_health_check_success_rate() == 100.0
    
    def test_get_health_check_success_rate_partial(self):
        """Test success rate with some failures."""
        config = ConnectionConfig(total_health_checks=10, failed_health_checks=2)
        assert config.get_health_check_success_rate() == 80.0
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = ConnectionConfig(
            server_url="https://example.com",
            username="admin",
        )
        d = config.to_dict()
        
        assert d["server_url"] == "https://example.com"
        assert d["username"] == "admin"
        assert "connection_state" in d
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "server_url": "https://example.com",
            "username": "admin",
            "token_encrypted": "",
            "token_version": 1,
            "connection_state": "Connected",
            "last_connected": None,
            "last_disconnected": None,
            "health_check_interval": 30,
            "health_check_timeout": 10,
            "auto_reconnect": True,
            "max_reconnect_attempts": 0,
            "reconnect_delay": 10,
            "total_connections": 0,
            "total_disconnections": 0,
            "total_health_checks": 0,
            "failed_health_checks": 0,
        }
        config = ConnectionConfig.from_dict(data)
        
        assert config.server_url == "https://example.com"
        assert config.username == "admin"
        assert config.get_state() == ConnectionState.CONNECTED


class TestInstanceConfig:
    """Tests for InstanceConfig dataclass."""
    
    def test_creation(self):
        """Test creating instance config."""
        config = InstanceConfig(
            instance_id="test-001",
            instance_name="Test Instance",
        )
        assert config.instance_id == "test-001"
        assert config.instance_name == "Test Instance"
        assert config.instance_type == "configurator"
        assert config.created_at is not None
    
    def test_connection_dict_conversion(self):
        """Test that connection dict is converted to ConnectionConfig."""
        config = InstanceConfig(
            instance_id="test-001",
            instance_name="Test",
            connection={"server_url": "https://example.com"},
        )
        assert isinstance(config.connection, ConnectionConfig)
        assert config.connection.server_url == "https://example.com"
    
    def test_mark_used(self):
        """Test mark_used updates last_used."""
        config = InstanceConfig(
            instance_id="test-001",
            instance_name="Test",
        )
        assert config.last_used is None
        
        config.mark_used()
        
        assert config.last_used is not None
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = InstanceConfig(
            instance_id="test-001",
            instance_name="Test Instance",
            instance_type="yield_monitor",
        )
        d = config.to_dict()
        
        assert d["instance_id"] == "test-001"
        assert d["instance_name"] == "Test Instance"
        assert d["instance_type"] == "yield_monitor"
        assert "connection" in d
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "instance_id": "test-001",
            "instance_name": "Test",
            "instance_type": "configurator",
            "storage_path": "/path/to/storage",
            "connection": {
                "server_url": "https://example.com",
            },
            "created_at": "2024-01-01T00:00:00",
            "last_used": None,
        }
        config = InstanceConfig.from_dict(data)
        
        assert config.instance_id == "test-001"
        assert config.storage_path == "/path/to/storage"
