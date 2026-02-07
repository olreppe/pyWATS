"""
Tests for IPC Authentication & Rate Limiting

Tests the authentication handshake and rate limiting
added to AsyncIPCServer and AsyncIPCClient.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

from pywats_client.service.async_ipc_server import AsyncIPCServer
from pywats_client.service.async_ipc_client import AsyncIPCClient
from pywats_client.core.security import (
    generate_secret,
    save_secret,
    load_secret,
    delete_secret,
    RateLimiter,
)


class TestIPCAuthentication:
    """Test IPC authentication flow"""
    
    @pytest.fixture
    def temp_secret_dir(self, tmp_path, monkeypatch):
        """Set up a temporary directory for secrets"""
        secret_dir = tmp_path / "secrets"
        secret_dir.mkdir()
        
        # Patch get_secret_directory in both security module AND the server's import
        import pywats_client.core.security as security_module
        import pywats_client.service.async_ipc_server as server_module
        import pywats_client.service.async_ipc_client as client_module
        
        monkeypatch.setattr(security_module, 'get_secret_directory', lambda: secret_dir)
        
        # Also patch load_secret directly in server and client modules
        def patched_load_secret(instance_id: str):
            """Load from temp dir using .key extension"""
            secret_file = secret_dir / f"{instance_id}.key"
            if secret_file.exists():
                return secret_file.read_text().strip()
            return None
        
        monkeypatch.setattr(server_module, 'load_secret', patched_load_secret)
        monkeypatch.setattr(client_module, 'load_secret', patched_load_secret)
        
        yield secret_dir
    
    @pytest.fixture
    def mock_service(self):
        """Create a mock service with async get_status"""
        service = MagicMock()
        service.get_status_async = AsyncMock(return_value={
            'status': 'running',
            'uptime': 100.0
        })
        return service
    
    @pytest.mark.asyncio
    async def test_auth_disabled_when_no_secret(self, mock_service, temp_secret_dir):
        """Test that commands work without auth when no secret exists"""
        # No secret saved - auth should be disabled
        server = AsyncIPCServer(instance_id="no_auth_test", service=mock_service)
        
        await server.start()
        try:
            client = AsyncIPCClient(instance_id="no_auth_test")
            connected = await client.connect()
            
            assert connected, "Should connect to server"
            
            # Should be able to ping without auth
            response = await client.send_command("ping")
            assert response is not None
            assert response.get("success") is True
            assert response.get("data", {}).get("pong") is True
            
            await client.disconnect()
        finally:
            await server.stop()
    
    @pytest.mark.asyncio
    async def test_auth_required_when_secret_exists(self, mock_service, temp_secret_dir):
        """Test that server requires auth when secret is configured, and client auto-authenticates"""
        instance_id = "auth_required_test"
        
        # Save a secret directly to temp dir (bypassing possibly unpatched save_secret)
        secret = generate_secret()
        secret_file = temp_secret_dir / f"{instance_id}.key"
        secret_file.write_text(secret)
        
        server = AsyncIPCServer(instance_id=instance_id, service=mock_service)
        
        await server.start()
        try:
            # Server should have auth capability now
            assert 'auth' in server._capabilities
            assert server._secret is not None
            
            # Client with matching secret should auto-authenticate
            client = AsyncIPCClient(instance_id=instance_id)
            connected = await client.connect()
            
            assert connected, "Should connect to server"
            
            # Client should be auto-authenticated
            assert client._authenticated is True
            
            # get_status should work since we're authenticated
            response = await client.send_command("get_status")
            assert response is not None
            assert response.get("success") is True
            
            await client.disconnect()
        finally:
            await server.stop()
    
    @pytest.mark.asyncio
    async def test_auth_succeeds_with_valid_token(self, mock_service, temp_secret_dir):
        """Test that authentication succeeds with correct token"""
        instance_id = "auth_success_test"
        
        # Save a secret directly to temp dir
        secret = generate_secret()
        secret_file = temp_secret_dir / f"{instance_id}.key"
        secret_file.write_text(secret)
        
        server = AsyncIPCServer(instance_id=instance_id, service=mock_service)
        
        await server.start()
        try:
            client = AsyncIPCClient(instance_id=instance_id)
            connected = await client.connect()
            
            assert connected, "Should connect to server"
            
            # Authenticate with correct token
            auth_response = await client.send_command("auth", {"token": secret})
            
            assert auth_response is not None
            assert auth_response.get("success") is True
            assert auth_response.get("data", {}).get("authenticated") is True
            
            # Now get_status should work
            status_response = await client.send_command("get_status")
            assert status_response is not None
            assert status_response.get("success") is True
            
            await client.disconnect()
        finally:
            await server.stop()
    
    @pytest.mark.asyncio
    async def test_auth_fails_with_invalid_token(self, mock_service, temp_secret_dir):
        """Test that authentication fails with wrong token"""
        instance_id = "auth_fail_test"
        
        # Save a secret directly to temp dir
        server_secret = generate_secret()
        secret_file = temp_secret_dir / f"{instance_id}.key"
        secret_file.write_text(server_secret)
        
        server = AsyncIPCServer(instance_id=instance_id, service=mock_service)
        
        await server.start()
        try:
            # Delete secret file so client can't auto-auth
            secret_file.unlink()
            
            client = AsyncIPCClient(instance_id=instance_id)
            connected = await client.connect()
            
            assert connected, "Should connect to server"
            
            # Client should NOT be authenticated (no secret file to load)
            assert client._authenticated is False
            
            # Try to auth with wrong token
            auth_response = await client.send_command("auth", {"token": "wrong_token"})
            
            assert auth_response is not None
            assert auth_response.get("success") is False
            assert "Invalid token" in auth_response.get("error", "")
            
            # get_status should still fail (not authenticated)
            status_response = await client.send_command("get_status")
            assert status_response is not None
            assert status_response.get("success") is False
            assert "Invalid token" in status_response.get("error", "")  # Error message changed
            
            await client.disconnect()
        finally:
            await server.stop()
    
    @pytest.mark.asyncio
    async def test_ping_shows_auth_status(self, mock_service, temp_secret_dir):
        """Test that ping response includes authentication status"""
        instance_id = "ping_auth_test"
        
        # Save secret directly to temp dir
        secret = generate_secret()
        secret_file = temp_secret_dir / f"{instance_id}.key"
        secret_file.write_text(secret)
        
        server = AsyncIPCServer(instance_id=instance_id, service=mock_service)
        
        await server.start()
        try:
            # Delete secret so client can't auto-auth
            secret_file.unlink()
            
            client = AsyncIPCClient(instance_id=instance_id)
            await client.connect()
            
            # Client shouldn't be authenticated
            assert client._authenticated is False
            
            # Ping before auth - should show not authenticated
            ping1 = await client.send_command("ping")
            assert ping1.get("success") is True
            assert ping1.get("data", {}).get("authenticated") is False
            
            # Restore secret and authenticate manually
            secret_file.write_text(secret)
            
            # Authenticate
            await client.send_command("auth", {"token": secret})
            
            # Ping after auth - should show authenticated
            ping2 = await client.send_command("ping")
            assert ping2.get("success") is True
            assert ping2.get("data", {}).get("authenticated") is True
            
            await client.disconnect()
        finally:
            await server.stop()


class TestIPCRateLimiting:
    """Test IPC rate limiting"""
    
    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        service = MagicMock()
        service.get_status_async = AsyncMock(return_value={'status': 'running'})
        return service
    
    def test_rate_limiter_instance_on_server(self, mock_service):
        """Test that server has rate limiter instance"""
        server = AsyncIPCServer(instance_id="rate_test", service=mock_service)
        
        assert hasattr(server, '_rate_limiter')
        assert isinstance(server._rate_limiter, RateLimiter)
    
    def test_rate_limiter_allows_normal_usage(self):
        """Test rate limiter allows normal request rates"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=10)
        
        # Should allow burst of requests
        for _ in range(10):
            assert limiter.check_rate_limit("client1") is True
    
    def test_rate_limiter_blocks_excessive_requests(self):
        """Test rate limiter blocks after burst exhausted"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=5)
        
        # Exhaust burst
        for _ in range(5):
            limiter.check_rate_limit("client1")
        
        # Next request should be blocked
        assert limiter.check_rate_limit("client1") is False
    
    def test_rate_limiter_per_client_isolation(self):
        """Test that different clients have separate limits"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=3)
        
        # Client 1 exhausts burst
        for _ in range(3):
            limiter.check_rate_limit("client1")
        
        # Client 1 should be blocked
        assert limiter.check_rate_limit("client1") is False
        
        # Client 2 should still be allowed
        assert limiter.check_rate_limit("client2") is True


class TestClientAuthentication:
    """Test AsyncIPCClient authentication helpers"""
    
    @pytest.fixture
    def temp_secret_dir(self, tmp_path, monkeypatch):
        """Set up temporary secrets directory"""
        secret_dir = tmp_path / "secrets"
        secret_dir.mkdir()
        
        from pywats_client.core import security
        monkeypatch.setattr(security, 'get_secret_directory', lambda: secret_dir)
        
        yield secret_dir
    
    def test_client_has_authenticate_method(self):
        """Test that client has _authenticate method"""
        client = AsyncIPCClient(instance_id="test")
        
        assert hasattr(client, '_authenticate')
        assert callable(client._authenticate)
    
    def test_client_tracks_auth_state(self):
        """Test that client has _authenticated flag"""
        client = AsyncIPCClient(instance_id="test")
        
        assert hasattr(client, '_authenticated')
        assert client._authenticated is False


class TestSecurityIntegration:
    """Integration tests for security module with IPC"""
    
    def test_secret_lifecycle(self, tmp_path, monkeypatch):
        """Test complete secret lifecycle for IPC"""
        secret_dir = tmp_path / "secrets"
        secret_dir.mkdir()
        
        # Import the module so we can use patched versions
        import pywats_client.core.security as security
        monkeypatch.setattr(security, 'get_secret_directory', lambda: secret_dir)
        
        instance_id = "lifecycle_test"
        
        # Generate and save (call through the module)
        # Note: signature is save_secret(instance_id, secret)
        secret = security.generate_secret()
        assert len(secret) == 64  # 32 bytes = 64 hex chars
        
        security.save_secret(instance_id, secret)
        
        # Verify file was created with .key extension
        assert (secret_dir / f"{instance_id}.key").exists()
        
        # Load (through module)
        loaded = security.load_secret(instance_id)
        assert loaded == secret
        
        # Delete (through module)
        security.delete_secret(instance_id)
        assert security.load_secret(instance_id) is None
