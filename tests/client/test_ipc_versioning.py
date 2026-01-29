"""
Tests for IPC Protocol Versioning

Tests the protocol version negotiation, hello messages,
and version compatibility checking.
"""

import pytest
import asyncio
import json
from unittest.mock import MagicMock, AsyncMock

from pywats_client.service.ipc_protocol import (
    PROTOCOL_VERSION,
    PROTOCOL_VERSION_MAJOR,
    PROTOCOL_VERSION_MINOR,
    MIN_CLIENT_VERSION,
    MIN_SERVER_VERSION,
    parse_version,
    is_version_compatible,
    check_version_compatibility,
    MessageType,
    IPCMessage,
    IPCResponse,
    HelloMessage,
    ConnectMessage,
    ServerCapability,
    VersionMismatchError,
    MAX_MESSAGE_SIZE,
    create_request,
    create_hello,
)
from pywats_client.service.async_ipc_server import AsyncIPCServer
from pywats_client.service.async_ipc_client import AsyncIPCClient


class TestProtocolVersion:
    """Test protocol version constants and parsing"""
    
    def test_protocol_version_format(self):
        """Protocol version should be in major.minor format"""
        assert "." in PROTOCOL_VERSION
        major, minor = PROTOCOL_VERSION.split(".")
        assert major.isdigit()
        assert minor.isdigit()
    
    def test_protocol_version_constants_match(self):
        """Version constants should be consistent"""
        assert PROTOCOL_VERSION == f"{PROTOCOL_VERSION_MAJOR}.{PROTOCOL_VERSION_MINOR}"
    
    def test_parse_version_valid(self):
        """Test parsing valid version strings"""
        assert parse_version("2.0") == (2, 0)
        assert parse_version("1.5") == (1, 5)
        assert parse_version("10.20") == (10, 20)
        assert parse_version("3") == (3, 0)  # Minor defaults to 0
    
    def test_parse_version_invalid(self):
        """Test parsing invalid version strings"""
        assert parse_version("") == (0, 0)
        assert parse_version("invalid") == (0, 0)
        assert parse_version("a.b") == (0, 0)


class TestVersionCompatibility:
    """Test version compatibility checking"""
    
    def test_same_version_compatible(self):
        """Same versions should be compatible"""
        assert is_version_compatible("2.0", "2.0") is True
        assert is_version_compatible("1.5", "1.5") is True
    
    def test_newer_version_compatible(self):
        """Newer versions should be compatible with older minimum"""
        assert is_version_compatible("3.0", "2.0") is True
        assert is_version_compatible("2.5", "2.0") is True
        assert is_version_compatible("2.1", "2.0") is True
    
    def test_older_version_incompatible(self):
        """Older versions should not be compatible with newer minimum"""
        assert is_version_compatible("1.0", "2.0") is False
        assert is_version_compatible("1.9", "2.0") is False
    
    def test_check_version_compatibility_both_valid(self):
        """Both versions should pass compatibility check"""
        compatible, error = check_version_compatibility("2.0", "2.0")
        assert compatible is True
        assert error == ""
    
    def test_check_version_compatibility_client_too_old(self):
        """Should detect client version too old"""
        # This will fail if client is older than MIN_CLIENT_VERSION
        # Simulate by checking against "3.0" min
        compatible, error = check_version_compatibility("1.0", "2.0")
        assert compatible is False
        assert "Client version" in error or "too old" in error.lower()


class TestMessageTypes:
    """Test message type enum"""
    
    def test_message_types_are_strings(self):
        """Message types should be string values"""
        assert MessageType.HELLO.value == "hello"
        assert MessageType.AUTH.value == "auth"
        assert MessageType.PING.value == "ping"
        assert MessageType.GET_STATUS.value == "get_status"
    
    def test_all_message_types_unique(self):
        """All message type values should be unique"""
        values = [mt.value for mt in MessageType]
        assert len(values) == len(set(values))


class TestIPCMessage:
    """Test IPC message dataclass"""
    
    def test_create_message(self):
        """Create a basic IPC message"""
        msg = IPCMessage(command="ping", request_id="123")
        assert msg.command == "ping"
        assert msg.request_id == "123"
        assert msg.protocol_version == PROTOCOL_VERSION
        assert msg.args == {}
    
    def test_message_to_dict(self):
        """Message should serialize to dict"""
        msg = IPCMessage(command="get_status", request_id="abc", args={"foo": "bar"})
        d = msg.to_dict()
        assert d["command"] == "get_status"
        assert d["request_id"] == "abc"
        assert d["protocol_version"] == PROTOCOL_VERSION
        assert d["args"] == {"foo": "bar"}
    
    def test_message_to_json(self):
        """Message should serialize to JSON"""
        msg = IPCMessage(command="ping")
        j = msg.to_json()
        parsed = json.loads(j)
        assert parsed["command"] == "ping"
    
    def test_message_from_dict(self):
        """Message should deserialize from dict"""
        d = {"command": "auth", "request_id": "xyz", "protocol_version": "1.0", "args": {"token": "secret"}}
        msg = IPCMessage.from_dict(d)
        assert msg.command == "auth"
        assert msg.request_id == "xyz"
        assert msg.protocol_version == "1.0"
        assert msg.args == {"token": "secret"}
    
    def test_message_from_json(self):
        """Message should deserialize from JSON"""
        j = '{"command": "ping", "request_id": "test"}'
        msg = IPCMessage.from_json(j)
        assert msg.command == "ping"
        assert msg.request_id == "test"


class TestIPCResponse:
    """Test IPC response dataclass"""
    
    def test_success_response(self):
        """Create a success response"""
        resp = IPCResponse.success_response(data={"status": "ok"}, request_id="123")
        assert resp.success is True
        assert resp.data == {"status": "ok"}
        assert resp.error is None
        assert resp.request_id == "123"
    
    def test_error_response(self):
        """Create an error response"""
        resp = IPCResponse.error_response(error="Something went wrong", request_id="456")
        assert resp.success is False
        assert resp.error == "Something went wrong"
        assert resp.data is None
        assert resp.request_id == "456"
    
    def test_response_includes_protocol_version(self):
        """Responses should include protocol version"""
        resp = IPCResponse.success_response()
        assert resp.protocol_version == PROTOCOL_VERSION


class TestHelloMessage:
    """Test hello message structure"""
    
    def test_create_hello(self):
        """Create a hello message"""
        hello = HelloMessage(
            protocol_version="2.0",
            server_version="0.1.0",
            instance_id="test",
            requires_auth=True,
            capabilities=["auth", "queue"]
        )
        assert hello.protocol_version == "2.0"
        assert hello.server_version == "0.1.0"
        assert hello.instance_id == "test"
        assert hello.requires_auth is True
        assert "auth" in hello.capabilities
    
    def test_hello_defaults(self):
        """Hello message should have sensible defaults"""
        hello = HelloMessage()
        assert hello.protocol_version == PROTOCOL_VERSION
        assert hello.requires_auth is False
        assert hello.capabilities == []
    
    def test_hello_to_dict(self):
        """Hello should serialize to dict"""
        hello = HelloMessage(instance_id="default")
        d = hello.to_dict()
        assert "protocol_version" in d
        assert "instance_id" in d
        assert "requires_auth" in d
        assert "capabilities" in d
    
    def test_hello_from_dict(self):
        """Hello should deserialize from dict"""
        d = {"protocol_version": "1.0", "server_version": "test", "requires_auth": True}
        hello = HelloMessage.from_dict(d)
        assert hello.protocol_version == "1.0"
        assert hello.requires_auth is True


class TestServerCapability:
    """Test server capability enum"""
    
    def test_capability_values(self):
        """Capabilities should have string values"""
        assert ServerCapability.AUTH.value == "auth"
        assert ServerCapability.RATE_LIMIT.value == "rate_limit"
        assert ServerCapability.CONVERTERS.value == "converters"
        assert ServerCapability.QUEUE.value == "queue"
        assert ServerCapability.CONFIG.value == "config"


class TestVersionMismatchError:
    """Test version mismatch exception"""
    
    def test_exception_creation(self):
        """Create version mismatch error"""
        error = VersionMismatchError(
            client_version="1.0",
            server_version="2.0"
        )
        assert "1.0" in str(error)
        assert "2.0" in str(error)
    
    def test_exception_custom_message(self):
        """Exception with custom message"""
        error = VersionMismatchError(
            client_version="1.0",
            server_version="2.0",
            message="Custom error message"
        )
        assert str(error) == "Custom error message"


class TestHelperFunctions:
    """Test protocol helper functions"""
    
    def test_create_request(self):
        """create_request should build valid IPCMessage"""
        msg = create_request("ping", args={"test": True}, request_id="req123")
        assert msg.command == "ping"
        assert msg.args == {"test": True}
        assert msg.request_id == "req123"
        assert msg.protocol_version == PROTOCOL_VERSION
    
    def test_create_hello_function(self):
        """create_hello should build valid HelloMessage"""
        hello = create_hello(
            instance_id="test",
            server_version="1.0.0",
            requires_auth=True,
            capabilities=["auth"]
        )
        assert hello.instance_id == "test"
        assert hello.server_version == "1.0.0"
        assert hello.requires_auth is True
        assert "auth" in hello.capabilities


class TestProtocolConstants:
    """Test protocol constants"""
    
    def test_max_message_size(self):
        """Max message size should be reasonable"""
        assert MAX_MESSAGE_SIZE > 0
        assert MAX_MESSAGE_SIZE == 1024 * 1024  # 1MB


@pytest.mark.asyncio
class TestServerHelloIntegration:
    """Integration tests for server hello message"""
    
    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        service = MagicMock()
        service.get_status_async = AsyncMock(return_value={"status": "running"})
        return service
    
    async def test_server_sends_hello_on_connect(self, mock_service):
        """Server should send hello message when client connects"""
        server = AsyncIPCServer(instance_id="hello_test", service=mock_service)
        
        await server.start()
        try:
            client = AsyncIPCClient(instance_id="hello_test")
            connected = await client.connect()
            
            assert connected
            # Client should have received hello
            assert client._server_hello is not None
            assert client._server_hello.protocol_version == PROTOCOL_VERSION
            assert client._server_hello.instance_id == "hello_test"
            
            await client.disconnect()
        finally:
            await server.stop()
    
    async def test_server_hello_includes_capabilities(self, mock_service):
        """Server hello should list capabilities"""
        server = AsyncIPCServer(instance_id="cap_test", service=mock_service)
        
        await server.start()
        try:
            client = AsyncIPCClient(instance_id="cap_test")
            await client.connect()
            
            # Should have at least some capabilities
            assert client._server_hello is not None
            assert isinstance(client._server_hello.capabilities, list)
            # rate_limit and config are always present
            assert "rate_limit" in client._server_hello.capabilities
            assert "config" in client._server_hello.capabilities
            
            await client.disconnect()
        finally:
            await server.stop()
    
    async def test_client_sends_version_in_requests(self, mock_service):
        """Client requests should include protocol version"""
        server = AsyncIPCServer(instance_id="version_test", service=mock_service)
        
        await server.start()
        try:
            client = AsyncIPCClient(instance_id="version_test")
            await client.connect()
            
            # Response should include server's protocol version
            response = await client.send_command("ping")
            assert response is not None
            assert response.get("protocol_version") == PROTOCOL_VERSION
            
            await client.disconnect()
        finally:
            await server.stop()
    
    async def test_server_version_property(self, mock_service):
        """Client should expose server version property"""
        server = AsyncIPCServer(instance_id="prop_test", service=mock_service)
        
        await server.start()
        try:
            client = AsyncIPCClient(instance_id="prop_test")
            await client.connect()
            
            assert client.server_version == PROTOCOL_VERSION
            assert client.server_capabilities is not None
            
            await client.disconnect()
            
            # After disconnect, properties should reset
            assert client.server_version is None
            
        finally:
            await server.stop()
