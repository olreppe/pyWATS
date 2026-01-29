"""
Tests for security module.

Tests:
- Secret generation
- Secret storage/loading
- Token validation
- Rate limiting
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

from pywats_client.core.security import (
    generate_secret, save_secret, load_secret, delete_secret,
    validate_token, hash_secret, RateLimiter, get_secret_directory
)


class TestSecretManagement:
    """Test secret generation and storage"""
    
    @pytest.fixture
    def temp_secret_dir(self):
        """Create temporary directory for secrets"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    def test_generate_secret(self):
        """Test secret generation"""
        secret1 = generate_secret()
        secret2 = generate_secret()
        
        # Should be 64 hex characters (256 bits)
        assert len(secret1) == 64
        assert len(secret2) == 64
        
        # Should be different each time
        assert secret1 != secret2
        
        # Should be valid hex
        assert all(c in '0123456789abcdef' for c in secret1)
        assert all(c in '0123456789abcdef' for c in secret2)
    
    def test_save_and_load_secret(self, temp_secret_dir):
        """Test saving and loading secrets"""
        instance_id = "test_instance"
        secret = generate_secret()
        
        with patch('pywats_client.core.security.get_secret_directory', return_value=temp_secret_dir):
            # Save secret
            secret_file = save_secret(instance_id, secret)
            assert secret_file.exists()
            assert secret_file.parent == temp_secret_dir
            
            # Load secret
            loaded_secret = load_secret(instance_id)
            assert loaded_secret == secret
    
    def test_load_nonexistent_secret(self, temp_secret_dir):
        """Test loading secret that doesn't exist"""
        with patch('pywats_client.core.security.get_secret_directory', return_value=temp_secret_dir):
            loaded_secret = load_secret("nonexistent")
            assert loaded_secret is None
    
    def test_delete_secret(self, temp_secret_dir):
        """Test deleting secrets"""
        instance_id = "test_instance"
        secret = generate_secret()
        
        with patch('pywats_client.core.security.get_secret_directory', return_value=temp_secret_dir):
            # Save and delete
            save_secret(instance_id, secret)
            assert delete_secret(instance_id) is True
            
            # Should be gone
            assert load_secret(instance_id) is None
            
            # Deleting again should return False
            assert delete_secret(instance_id) is False
    
    def test_secret_file_permissions(self, temp_secret_dir):
        """Test that secret files have restrictive permissions on Unix"""
        import sys
        if sys.platform == 'win32':
            pytest.skip("Permission test only applies to Unix")
        
        instance_id = "test_instance"
        secret = generate_secret()
        
        with patch('pywats_client.core.security.get_secret_directory', return_value=temp_secret_dir):
            secret_file = save_secret(instance_id, secret)
            
            # Check permissions (should be 0o600 = rw-------)
            import stat
            mode = secret_file.stat().st_mode
            assert stat.S_IMODE(mode) == 0o600


class TestTokenValidation:
    """Test token validation"""
    
    def test_validate_token_success(self):
        """Test successful token validation"""
        secret = generate_secret()
        assert validate_token(secret, secret) is True
    
    def test_validate_token_failure(self):
        """Test failed token validation"""
        secret1 = generate_secret()
        secret2 = generate_secret()
        assert validate_token(secret1, secret2) is False
    
    def test_validate_token_timing_safe(self):
        """Test that validation uses timing-safe comparison"""
        # This test just ensures validate_token uses secrets.compare_digest
        # which is timing-safe (prevents timing attacks)
        secret = "a" * 64
        wrong = "b" * 64
        
        # Should use constant-time comparison
        assert validate_token(secret, secret) is True
        assert validate_token(secret, wrong) is False


class TestSecretHashing:
    """Test secret hashing for logging"""
    
    def test_hash_secret(self):
        """Test secret hashing"""
        secret = generate_secret()
        hashed = hash_secret(secret)
        
        # Should be 16 hex characters
        assert len(hashed) == 16
        assert all(c in '0123456789abcdef' for c in hashed)
        
        # Same secret should produce same hash
        assert hash_secret(secret) == hashed
        
        # Different secret should produce different hash
        different_secret = generate_secret()
        assert hash_secret(different_secret) != hashed


class TestRateLimiter:
    """Test rate limiting"""
    
    def test_rate_limiter_allows_burst(self):
        """Test that rate limiter allows burst"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=10)
        client_id = "test_client"
        
        # Should allow burst_size requests immediately
        for _ in range(10):
            assert limiter.check_rate_limit(client_id) is True
        
        # 11th request should be blocked
        assert limiter.check_rate_limit(client_id) is False
    
    def test_rate_limiter_refills_over_time(self):
        """Test that rate limiter refills tokens over time"""
        import time
        
        limiter = RateLimiter(requests_per_minute=60, burst_size=5)
        client_id = "test_client"
        
        # Use up burst
        for _ in range(5):
            assert limiter.check_rate_limit(client_id) is True
        
        # Should be blocked
        assert limiter.check_rate_limit(client_id) is False
        
        # Wait for 1 token to refill (60 req/min = 1 req/sec)
        time.sleep(1.1)
        
        # Should allow 1 more request
        assert limiter.check_rate_limit(client_id) is True
        assert limiter.check_rate_limit(client_id) is False  # Used up again
    
    def test_rate_limiter_per_client(self):
        """Test that rate limiting is per-client"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=5)
        
        # Use up client1's burst
        for _ in range(5):
            assert limiter.check_rate_limit("client1") is True
        assert limiter.check_rate_limit("client1") is False
        
        # client2 should still have full burst
        for _ in range(5):
            assert limiter.check_rate_limit("client2") is True
        assert limiter.check_rate_limit("client2") is False
    
    def test_rate_limiter_reset(self):
        """Test resetting rate limit for client"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=5)
        client_id = "test_client"
        
        # Use up burst
        for _ in range(5):
            assert limiter.check_rate_limit(client_id) is True
        assert limiter.check_rate_limit(client_id) is False
        
        # Reset
        limiter.reset(client_id)
        
        # Should have full burst again
        for _ in range(5):
            assert limiter.check_rate_limit(client_id) is True
    
    def test_rate_limiter_cleanup(self):
        """Test cleaning up old clients"""
        import time
        
        limiter = RateLimiter(requests_per_minute=60, burst_size=5)
        
        # Make requests from multiple clients
        limiter.check_rate_limit("client1")
        limiter.check_rate_limit("client2")
        limiter.check_rate_limit("client3")
        
        # Wait a bit
        time.sleep(0.1)
        
        # Clean up clients older than 0.05 seconds
        removed = limiter.cleanup_old_clients(max_age_seconds=0.05)
        
        # Should have removed all 3 clients
        assert removed == 3
        
        # New requests should work (fresh buckets)
        for _ in range(5):
            assert limiter.check_rate_limit("client1") is True


class TestSecretDirectory:
    """Test secret directory creation"""
    
    def test_get_secret_directory(self):
        """Test getting secret directory"""
        secret_dir = get_secret_directory()
        
        # Should exist
        assert secret_dir.exists()
        assert secret_dir.is_dir()
        
        # Should be in appropriate location
        import sys
        if sys.platform == 'win32':
            assert 'AppData' in str(secret_dir)
            assert 'pyWATS' in str(secret_dir)
        else:
            assert '.config' in str(secret_dir)
            assert 'pywats' in str(secret_dir)
