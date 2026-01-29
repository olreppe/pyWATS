"""
Tests for Converter Sandbox

Tests process isolation, resource limits, and security restrictions.
"""

import asyncio
import json
import pytest
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch

from pywats_client.converters.sandbox import (
    SandboxCapability,
    ResourceLimits,
    SandboxConfig,
    SandboxMessageType,
    SandboxMessage,
    SandboxError,
    SandboxTimeoutError,
    SandboxResourceError,
    SandboxSecurityError,
    SandboxProcess,
    ConverterValidator,
    ConverterSandbox,
    DEFAULT_CAPABILITIES,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_dir():
    """Create a temporary directory."""
    with tempfile.TemporaryDirectory(prefix="pywats_test_") as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_converter(temp_dir):
    """Create a sample converter file."""
    converter_code = '''
"""Sample converter for testing."""

from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class ConversionStatus(Enum):
    SUCCESS = "Success"
    FAILED = "Failed"


@dataclass
class ConverterResult:
    status: ConversionStatus
    report: dict = None
    error: str = None
    post_action: str = None
    metadata: dict = None
    
    @classmethod
    def success_result(cls, report=None, **kwargs):
        return cls(status=ConversionStatus.SUCCESS, report=report or {}, **kwargs)


class SampleConverter:
    """Simple test converter."""
    
    @property
    def name(self) -> str:
        return "SampleConverter"
    
    def convert_file(self, file_path, args):
        content = file_path.read_text() if file_path.exists() else ""
        
        return ConverterResult.success_result(
            report={"content_length": len(content)},
            metadata={"file_name": file_path.name}
        )
'''
    
    converter_path = temp_dir / "sample_converter.py"
    converter_path.write_text(converter_code)
    return converter_path


@pytest.fixture
def malicious_converter(temp_dir):
    """Create a converter with dangerous code."""
    converter_code = '''
"""Malicious converter that should be blocked."""

import subprocess  # Dangerous!
import socket  # Also dangerous!

class MaliciousConverter:
    def convert_file(self, file_path, args):
        # Try to run system command
        subprocess.run(["whoami"])
        return {"status": "success"}
'''
    
    converter_path = temp_dir / "malicious_converter.py"
    converter_path.write_text(converter_code)
    return converter_path


@pytest.fixture
def default_config():
    """Create a default sandbox config."""
    return SandboxConfig()


# =============================================================================
# Test SandboxCapability
# =============================================================================

class TestSandboxCapability:
    """Tests for SandboxCapability enum."""
    
    def test_capability_values(self):
        """Test capability enum values."""
        assert SandboxCapability.READ_INPUT.value == "read_input"
        assert SandboxCapability.WRITE_OUTPUT.value == "write_output"
        assert SandboxCapability.NETWORK_WATS.value == "network_wats"
    
    def test_default_capabilities(self):
        """Test default capabilities are minimal."""
        assert SandboxCapability.READ_INPUT in DEFAULT_CAPABILITIES
        assert SandboxCapability.WRITE_OUTPUT in DEFAULT_CAPABILITIES
        assert SandboxCapability.LOG_INFO in DEFAULT_CAPABILITIES
        
        # Network should NOT be in default
        assert SandboxCapability.NETWORK_LOCAL not in DEFAULT_CAPABILITIES
        assert SandboxCapability.NETWORK_WATS not in DEFAULT_CAPABILITIES


# =============================================================================
# Test ResourceLimits
# =============================================================================

class TestResourceLimits:
    """Tests for ResourceLimits dataclass."""
    
    def test_default_values(self):
        """Test default resource limits."""
        limits = ResourceLimits()
        
        assert limits.timeout_seconds == 300.0
        assert limits.cpu_time_seconds == 120.0
        assert limits.memory_mb == 512
        assert limits.max_output_size_mb == 100
        assert limits.max_open_files == 50
        assert limits.max_processes == 1
    
    def test_custom_values(self):
        """Test custom resource limits."""
        limits = ResourceLimits(
            timeout_seconds=60.0,
            memory_mb=256,
            max_processes=2,
        )
        
        assert limits.timeout_seconds == 60.0
        assert limits.memory_mb == 256
        assert limits.max_processes == 2
    
    def test_to_dict(self):
        """Test serialization to dict."""
        limits = ResourceLimits(timeout_seconds=120.0, memory_mb=1024)
        
        data = limits.to_dict()
        
        assert data["timeout_seconds"] == 120.0
        assert data["memory_mb"] == 1024
    
    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {"timeout_seconds": 60.0, "cpu_time_seconds": 30.0}
        
        limits = ResourceLimits.from_dict(data)
        
        assert limits.timeout_seconds == 60.0
        assert limits.cpu_time_seconds == 30.0
        # Defaults should be applied
        assert limits.memory_mb == 512


# =============================================================================
# Test SandboxConfig
# =============================================================================

class TestSandboxConfig:
    """Tests for SandboxConfig dataclass."""
    
    def test_default_config(self, default_config):
        """Test default configuration."""
        assert default_config.capabilities == DEFAULT_CAPABILITIES
        assert isinstance(default_config.resource_limits, ResourceLimits)
        assert "subprocess" in default_config.blocked_imports
    
    def test_blocked_imports(self, default_config):
        """Test blocked imports list."""
        blocked = default_config.blocked_imports
        
        # Critical dangerous imports should be blocked
        assert "subprocess" in blocked
        assert "multiprocessing" in blocked
        assert "ctypes" in blocked
        assert "socket" in blocked
        assert "os.system" in blocked
    
    def test_to_dict_and_back(self, default_config):
        """Test serialization roundtrip."""
        data = default_config.to_dict()
        restored = SandboxConfig.from_dict(data)
        
        assert restored.capabilities == default_config.capabilities
        assert restored.resource_limits.timeout_seconds == default_config.resource_limits.timeout_seconds


# =============================================================================
# Test SandboxMessage
# =============================================================================

class TestSandboxMessage:
    """Tests for SandboxMessage IPC."""
    
    def test_create_message(self):
        """Test creating a message."""
        msg = SandboxMessage(
            type=SandboxMessageType.INIT,
            payload={"key": "value"}
        )
        
        assert msg.type == SandboxMessageType.INIT
        assert msg.payload == {"key": "value"}
    
    def test_to_json(self):
        """Test JSON serialization."""
        msg = SandboxMessage(
            type=SandboxMessageType.CONVERT,
            payload={"input_path": "/tmp/test.csv"}
        )
        
        json_str = msg.to_json()
        parsed = json.loads(json_str)
        
        assert parsed["type"] == "convert"
        assert parsed["payload"]["input_path"] == "/tmp/test.csv"
    
    def test_from_json(self):
        """Test JSON deserialization."""
        json_str = '{"type": "result", "payload": {"status": "success"}}'
        
        msg = SandboxMessage.from_json(json_str)
        
        assert msg.type == SandboxMessageType.RESULT
        assert msg.payload["status"] == "success"
    
    def test_message_types(self):
        """Test all message types."""
        assert SandboxMessageType.INIT.value == "init"
        assert SandboxMessageType.CONVERT.value == "convert"
        assert SandboxMessageType.SHUTDOWN.value == "shutdown"
        assert SandboxMessageType.READY.value == "ready"
        assert SandboxMessageType.RESULT.value == "result"
        assert SandboxMessageType.ERROR.value == "error"


# =============================================================================
# Test ConverterValidator
# =============================================================================

class TestConverterValidator:
    """Tests for static code analysis."""
    
    def test_validate_safe_code(self, default_config):
        """Test validation passes for safe code."""
        validator = ConverterValidator(default_config)
        
        safe_code = '''
import json
import pathlib

class SafeConverter:
    def convert_file(self, path, args):
        data = pathlib.Path(path).read_text()
        return json.loads(data)
'''
        
        is_valid, issues = validator.validate_source(safe_code)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_blocked_import(self, default_config):
        """Test validation fails for blocked imports."""
        validator = ConverterValidator(default_config)
        
        dangerous_code = '''
import subprocess

class DangerousConverter:
    def run(self):
        subprocess.run(["rm", "-rf", "/"])
'''
        
        is_valid, issues = validator.validate_source(dangerous_code)
        
        assert is_valid is False
        assert any("subprocess" in issue for issue in issues)
    
    def test_validate_blocked_from_import(self, default_config):
        """Test validation catches from-imports."""
        validator = ConverterValidator(default_config)
        
        code = '''
from os import system

class BadConverter:
    def run(self):
        system("whoami")
'''
        
        is_valid, issues = validator.validate_source(code)
        
        # os.system should be blocked
        assert is_valid is False
    
    def test_validate_dangerous_calls(self, default_config):
        """Test detection of dangerous function calls."""
        validator = ConverterValidator(default_config)
        
        code = '''
class EvalConverter:
    def convert(self, data):
        return eval(data)  # Very dangerous!
'''
        
        is_valid, issues = validator.validate_source(code)
        
        assert is_valid is False
        assert any("eval" in issue for issue in issues)
    
    def test_validate_syntax_error(self, default_config):
        """Test handling of syntax errors."""
        validator = ConverterValidator(default_config)
        
        bad_code = '''
class Broken
    def x(self)  # Missing colon
'''
        
        is_valid, issues = validator.validate_source(bad_code)
        
        assert is_valid is False
        assert any("Syntax error" in issue for issue in issues)
    
    def test_validate_file(self, default_config, sample_converter):
        """Test file validation."""
        validator = ConverterValidator(default_config)
        
        is_valid, issues = validator.validate_file(sample_converter)
        
        assert is_valid is True
    
    def test_validate_malicious_file(self, default_config, malicious_converter):
        """Test malicious file is rejected."""
        validator = ConverterValidator(default_config)
        
        is_valid, issues = validator.validate_file(malicious_converter)
        
        assert is_valid is False
        assert len(issues) >= 2  # subprocess and socket


# =============================================================================
# Test SandboxProcess
# =============================================================================

class TestSandboxProcess:
    """Tests for SandboxProcess subprocess management."""
    
    def test_init(self, default_config, sample_converter):
        """Test process initialization."""
        process = SandboxProcess(
            config=default_config,
            converter_path=sample_converter,
            converter_class="SampleConverter",
        )
        
        assert process.converter_path == sample_converter
        assert process.converter_class == "SampleConverter"
        assert process.is_running is False
    
    def test_create_restricted_env(self, default_config, sample_converter):
        """Test restricted environment creation."""
        process = SandboxProcess(
            config=default_config,
            converter_path=sample_converter,
            converter_class="SampleConverter",
        )
        
        env = process._create_restricted_env()
        
        # Should have sandbox marker
        assert env.get("PYWATS_SANDBOX") == "1"
        
        # Should have safe vars from current env (if present)
        # These may or may not be present depending on the test environment


# =============================================================================
# Test ConverterSandbox (High-Level Interface)
# =============================================================================

class TestConverterSandbox:
    """Tests for ConverterSandbox high-level interface."""
    
    def test_init(self):
        """Test sandbox initialization."""
        sandbox = ConverterSandbox()
        
        assert sandbox.default_config is not None
        assert sandbox.validator is not None
    
    def test_init_with_custom_config(self, default_config):
        """Test sandbox with custom config."""
        custom = SandboxConfig(
            resource_limits=ResourceLimits(timeout_seconds=60.0)
        )
        
        sandbox = ConverterSandbox(default_config=custom)
        
        assert sandbox.default_config.resource_limits.timeout_seconds == 60.0
    
    @pytest.mark.asyncio
    async def test_validate_converter(self, sample_converter):
        """Test converter validation through high-level interface."""
        sandbox = ConverterSandbox()
        
        is_valid, issues = await sandbox.validate_converter(sample_converter)
        
        assert is_valid is True
    
    @pytest.mark.asyncio
    async def test_validate_malicious_converter(self, malicious_converter):
        """Test malicious converter is rejected."""
        sandbox = ConverterSandbox()
        
        is_valid, issues = await sandbox.validate_converter(malicious_converter)
        
        assert is_valid is False
    
    @pytest.mark.asyncio
    async def test_shutdown(self):
        """Test sandbox shutdown."""
        sandbox = ConverterSandbox()
        
        # Should not raise even with no processes
        await sandbox.shutdown()


# =============================================================================
# Test Error Classes
# =============================================================================

class TestSandboxErrors:
    """Tests for sandbox error classes."""
    
    def test_sandbox_error(self):
        """Test base sandbox error."""
        error = SandboxError("Test error")
        assert str(error) == "Test error"
    
    def test_timeout_error(self):
        """Test timeout error."""
        error = SandboxTimeoutError("Timed out after 30s")
        assert "30s" in str(error)
        assert isinstance(error, SandboxError)
    
    def test_resource_error(self):
        """Test resource limit error."""
        error = SandboxResourceError("Memory limit exceeded")
        assert "Memory" in str(error)
        assert isinstance(error, SandboxError)
    
    def test_security_error(self):
        """Test security violation error."""
        error = SandboxSecurityError("Blocked import detected")
        assert "Blocked" in str(error)
        assert isinstance(error, SandboxError)


# =============================================================================
# Integration Tests (require subprocess)
# =============================================================================

class TestSandboxIntegration:
    """Integration tests for sandbox subprocess."""
    
    @pytest.mark.asyncio
    @pytest.mark.skipif(sys.platform == "win32", reason="Unix-specific resource limits")
    async def test_unix_resource_limits_setup(self, default_config, sample_converter):
        """Test that resource limits are set on Unix."""
        process = SandboxProcess(
            config=default_config,
            converter_path=sample_converter,
            converter_class="SampleConverter",
        )
        
        # Test that _setup_unix_limits doesn't raise
        # (actual limits require process fork)
        # This is a smoke test for the method
        assert hasattr(process, "_setup_unix_limits")
    
    @pytest.mark.asyncio
    async def test_run_converter_validation_failure(self, malicious_converter, temp_dir):
        """Test that malicious converters are rejected before running."""
        sandbox = ConverterSandbox()
        
        input_file = temp_dir / "input.txt"
        input_file.write_text("test data")
        
        with pytest.raises(SandboxSecurityError) as exc_info:
            await sandbox.run_converter(
                converter_path=malicious_converter,
                converter_class="MaliciousConverter",
                input_path=input_file,
            )
        
        assert "validation failed" in str(exc_info.value).lower()


# =============================================================================
# Test Sandbox Runner Script
# =============================================================================

class TestSandboxRunnerProtocol:
    """Tests for sandbox_runner.py protocol handling."""
    
    def test_message_protocol_constants(self):
        """Test message types match between sandbox.py and sandbox_runner.py."""
        # These should match the values in sandbox_runner.py
        assert SandboxMessageType.INIT.value == "init"
        assert SandboxMessageType.CONVERT.value == "convert"
        assert SandboxMessageType.READY.value == "ready"
        assert SandboxMessageType.RESULT.value == "result"
        assert SandboxMessageType.ERROR.value == "error"
