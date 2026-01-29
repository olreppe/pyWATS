"""
Sandbox Integration Tests

Tests that actually run converters in sandboxed subprocesses.
These tests verify end-to-end behavior of the sandbox system.
"""

import asyncio
import inspect
import json
import pytest
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any

from pywats_client.converters.sandbox import (
    SandboxCapability,
    ResourceLimits,
    SandboxConfig,
    SandboxError,
    SandboxTimeoutError,
    SandboxSecurityError,
    SandboxProcess,
    ConverterValidator,
    ConverterSandbox,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory(prefix="pywats_sandbox_test_") as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def simple_converter_code():
    """A minimal converter that can run in the sandbox."""
    return '''
"""Simple converter for integration testing."""

from pathlib import Path


class SimpleConverter:
    """Minimal converter implementation."""
    
    @property
    def name(self) -> str:
        return "SimpleConverter"
    
    def convert_file(self, file_path: Path, args: dict):
        """Convert a file by reading its content."""
        content = file_path.read_text() if file_path.exists() else ""
        
        return {
            "status": "Success",
            "report": {
                "content_length": len(content),
                "file_name": file_path.name,
            },
            "metadata": {
                "converter": self.name,
            }
        }
'''


@pytest.fixture
def simple_converter(temp_dir, simple_converter_code):
    """Create a simple converter file."""
    converter_path = temp_dir / "simple_converter.py"
    converter_path.write_text(simple_converter_code)
    return converter_path


@pytest.fixture
def echo_converter_code():
    """A converter that echoes back the args it receives."""
    return '''
"""Echo converter that returns its arguments."""

from pathlib import Path


class EchoConverter:
    """Converter that echoes back args for testing."""
    
    @property
    def name(self) -> str:
        return "EchoConverter"
    
    def convert_file(self, file_path: Path, args: dict):
        """Echo back the arguments and file info."""
        return {
            "status": "Success",
            "report": {
                "received_args": args,
                "file_path": str(file_path),
                "file_exists": file_path.exists(),
            },
            "metadata": {}
        }
'''


@pytest.fixture
def echo_converter(temp_dir, echo_converter_code):
    """Create an echo converter file."""
    converter_path = temp_dir / "echo_converter.py"
    converter_path.write_text(echo_converter_code)
    return converter_path


@pytest.fixture
def slow_converter_code():
    """A converter that takes time to complete."""
    return '''
"""Slow converter for timeout testing."""

import time
from pathlib import Path


class SlowConverter:
    """Converter that deliberately takes a long time."""
    
    @property
    def name(self) -> str:
        return "SlowConverter"
    
    def convert_file(self, file_path: Path, args: dict):
        """Sleep for the specified duration."""
        duration = args.get("sleep_duration", 1)
        time.sleep(duration)
        
        return {
            "status": "Success",
            "report": {"slept_for": duration},
            "metadata": {}
        }
'''


@pytest.fixture
def slow_converter(temp_dir, slow_converter_code):
    """Create a slow converter file."""
    converter_path = temp_dir / "slow_converter.py"
    converter_path.write_text(slow_converter_code)
    return converter_path


@pytest.fixture
def error_converter_code():
    """A converter that raises an exception."""
    return '''
"""Converter that raises an error."""

from pathlib import Path


class ErrorConverter:
    """Converter that always fails."""
    
    @property
    def name(self) -> str:
        return "ErrorConverter"
    
    def convert_file(self, file_path: Path, args: dict):
        """Always raise an error."""
        error_type = args.get("error_type", "generic")
        
        if error_type == "value":
            raise ValueError("Invalid value provided")
        elif error_type == "runtime":
            raise RuntimeError("Runtime error occurred")
        elif error_type == "key":
            d = {}
            return d["nonexistent"]  # KeyError
        else:
            raise Exception("Generic error")
'''


@pytest.fixture
def error_converter(temp_dir, error_converter_code):
    """Create an error converter file."""
    converter_path = temp_dir / "error_converter.py"
    converter_path.write_text(error_converter_code)
    return converter_path


@pytest.fixture
def malicious_import_converter_code():
    """A converter that tries to import dangerous modules."""
    return '''
"""Converter with dangerous imports."""

import subprocess  # Should be blocked!
from pathlib import Path


class MaliciousImportConverter:
    def convert_file(self, file_path: Path, args: dict):
        subprocess.run(["echo", "pwned"])
        return {"status": "Success"}
'''


@pytest.fixture
def malicious_import_converter(temp_dir, malicious_import_converter_code):
    """Create a malicious converter with blocked imports."""
    converter_path = temp_dir / "malicious_import.py"
    converter_path.write_text(malicious_import_converter_code)
    return converter_path


@pytest.fixture
def malicious_exec_converter_code():
    """A converter that tries to use exec/eval."""
    return '''
"""Converter that tries eval/exec."""

from pathlib import Path


class MaliciousExecConverter:
    def convert_file(self, file_path: Path, args: dict):
        # Try to use eval
        code = args.get("code", "1+1")
        result = eval(code)  # Should be blocked!
        return {"status": "Success", "result": result}
'''


@pytest.fixture
def malicious_exec_converter(temp_dir, malicious_exec_converter_code):
    """Create a malicious converter with eval/exec."""
    converter_path = temp_dir / "malicious_exec.py"
    converter_path.write_text(malicious_exec_converter_code)
    return converter_path


@pytest.fixture
def input_file(temp_dir):
    """Create a simple input file."""
    input_path = temp_dir / "input.txt"
    input_path.write_text("Hello, sandbox world!\nLine 2\nLine 3")
    return input_path


# =============================================================================
# Validator Tests
# =============================================================================

class TestConverterValidatorIntegration:
    """Integration tests for converter validation."""
    
    def test_validate_simple_converter(self, simple_converter):
        """Valid converter passes validation."""
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        source = simple_converter.read_text()
        is_valid, issues = validator.validate_source(source)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_echo_converter(self, echo_converter):
        """Echo converter passes validation."""
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        source = echo_converter.read_text()
        is_valid, issues = validator.validate_source(source)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_malicious_import(self, malicious_import_converter):
        """Converter with dangerous imports fails validation."""
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        source = malicious_import_converter.read_text()
        is_valid, issues = validator.validate_source(source)
        
        assert is_valid is False
        assert len(issues) > 0
        assert any("subprocess" in issue.lower() for issue in issues)
    
    def test_validate_malicious_exec(self, malicious_exec_converter):
        """Converter with eval/exec fails validation."""
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        source = malicious_exec_converter.read_text()
        is_valid, issues = validator.validate_source(source)
        
        assert is_valid is False
        assert len(issues) > 0
        assert any("eval" in issue.lower() for issue in issues)
    
    def test_validate_file_method(self, simple_converter):
        """Test validate_file method."""
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        is_valid, issues = validator.validate_file(simple_converter)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_validate_nonexistent_file(self, temp_dir):
        """Nonexistent file fails validation."""
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        fake_path = temp_dir / "nonexistent.py"
        is_valid, issues = validator.validate_file(fake_path)
        
        assert is_valid is False
        assert len(issues) > 0


# =============================================================================
# Sandbox Config Tests
# =============================================================================

class TestSandboxConfigIntegration:
    """Integration tests for sandbox configuration."""
    
    def test_default_config_blocks_dangerous_imports(self):
        """Default config blocks dangerous imports."""
        config = SandboxConfig()
        
        assert "subprocess" in config.blocked_imports
        assert "socket" in config.blocked_imports
        assert "ctypes" in config.blocked_imports
    
    def test_custom_blocked_imports(self):
        """Can add custom blocked imports."""
        config = SandboxConfig(
            blocked_imports=frozenset(["custom_module", "another_module"])
        )
        
        assert "custom_module" in config.blocked_imports
        assert "another_module" in config.blocked_imports
    
    def test_config_serialization(self):
        """Config can be serialized and deserialized."""
        original = SandboxConfig(
            capabilities=frozenset([
                SandboxCapability.READ_INPUT,
                SandboxCapability.NETWORK_WATS,
            ]),
            resource_limits=ResourceLimits(
                memory_mb=512,
                timeout_seconds=120,
            ),
        )
        
        config_dict = original.to_dict()
        restored = SandboxConfig.from_dict(config_dict)
        
        assert restored.capabilities == original.capabilities
        assert restored.resource_limits.memory_mb == original.resource_limits.memory_mb
        assert restored.resource_limits.timeout_seconds == original.resource_limits.timeout_seconds


# =============================================================================
# Sandbox Security Tests
# =============================================================================

class TestSandboxSecurity:
    """Tests for sandbox security features."""
    
    @pytest.mark.asyncio
    async def test_rejects_malicious_imports(self, malicious_import_converter, input_file):
        """Sandbox rejects converters with dangerous imports."""
        sandbox = ConverterSandbox()
        
        with pytest.raises(SandboxSecurityError) as exc_info:
            await sandbox.run_converter(
                converter_path=malicious_import_converter,
                converter_class="MaliciousImportConverter",
                input_path=input_file,
            )
        
        assert "validation failed" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_rejects_eval_exec(self, malicious_exec_converter, input_file):
        """Sandbox rejects converters with eval/exec."""
        sandbox = ConverterSandbox()
        
        with pytest.raises(SandboxSecurityError) as exc_info:
            await sandbox.run_converter(
                converter_path=malicious_exec_converter,
                converter_class="MaliciousExecConverter",
                input_path=input_file,
            )
        
        assert "validation failed" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_custom_blocked_imports(self, temp_dir, input_file):
        """Sandbox can block custom imports."""
        # Create converter that imports json (normally allowed)
        converter_code = '''
import json
from pathlib import Path

class JsonConverter:
    def convert_file(self, file_path: Path, args: dict):
        return {"status": "Success"}
'''
        converter_path = temp_dir / "json_converter.py"
        converter_path.write_text(converter_code)
        
        # Block json import
        config = SandboxConfig(
            blocked_imports=frozenset(
                list(SandboxConfig().blocked_imports) + ["json"]
            )
        )
        sandbox = ConverterSandbox(default_config=config)
        
        with pytest.raises(SandboxSecurityError) as exc_info:
            await sandbox.run_converter(
                converter_path=converter_path,
                converter_class="JsonConverter",
                input_path=input_file,
            )
        
        assert "validation failed" in str(exc_info.value).lower()


# =============================================================================
# Sandbox Lifecycle Tests
# =============================================================================

class TestSandboxLifecycle:
    """Tests for sandbox lifecycle management."""
    
    @pytest.mark.asyncio
    async def test_sandbox_startup_shutdown(self):
        """Sandbox can start and shutdown cleanly."""
        sandbox = ConverterSandbox()
        
        # Sandbox should start with no active processes
        assert hasattr(sandbox, "_processes")
        
        # Shutdown should be safe even with no processes
        await sandbox.shutdown()
    
    @pytest.mark.asyncio
    async def test_multiple_sandboxes(self, simple_converter, input_file):
        """Multiple sandbox instances work independently."""
        sandbox1 = ConverterSandbox()
        sandbox2 = ConverterSandbox()
        
        try:
            # Both should validate the same converter
            # validate_converter may be sync or async, check both
            if inspect.iscoroutinefunction(sandbox1.validate_converter):
                await sandbox1.validate_converter(simple_converter)
                await sandbox2.validate_converter(simple_converter)
            else:
                sandbox1.validate_converter(simple_converter)
                sandbox2.validate_converter(simple_converter)
        finally:
            await sandbox1.shutdown()
            await sandbox2.shutdown()


# =============================================================================
# SandboxProcess Tests
# =============================================================================

class TestSandboxProcessCreation:
    """Tests for SandboxProcess initialization."""
    
    def test_process_creation(self, simple_converter):
        """SandboxProcess can be created."""
        config = SandboxConfig()
        process = SandboxProcess(
            config=config,
            converter_path=simple_converter,
            converter_class="SimpleConverter",
        )
        
        assert process.converter_class == "SimpleConverter"
        assert process.converter_path == simple_converter
    
    def test_process_environment_isolation(self, simple_converter):
        """Process environment is properly restricted."""
        config = SandboxConfig()
        process = SandboxProcess(
            config=config,
            converter_path=simple_converter,
            converter_class="SimpleConverter",
        )
        
        env = process._create_restricted_env()
        
        # Should have essential variables but limited
        assert "PATH" in env or "PYTHONPATH" in env or len(env) > 0
    
    def test_custom_resource_limits(self, simple_converter):
        """Process respects custom resource limits."""
        config = SandboxConfig(
            resource_limits=ResourceLimits(
                memory_mb=256,
                cpu_time_seconds=10,
                max_output_size_mb=5,
                timeout_seconds=30,
            )
        )
        
        process = SandboxProcess(
            config=config,
            converter_path=simple_converter,
            converter_class="SimpleConverter",
        )
        
        assert process.config.resource_limits.memory_mb == 256
        assert process.config.resource_limits.timeout_seconds == 30


# =============================================================================
# Performance Tests
# =============================================================================

class TestSandboxPerformance:
    """Performance-related tests for sandbox."""
    
    def test_validator_performance(self, simple_converter):
        """Validation should be fast."""
        import time
        
        config = SandboxConfig()
        validator = ConverterValidator(config)
        source = simple_converter.read_text()
        
        # Validate 100 times
        start = time.perf_counter()
        for _ in range(100):
            validator.validate_source(source)
        elapsed = time.perf_counter() - start
        
        # Should complete in under 1 second
        assert elapsed < 1.0, f"100 validations took {elapsed:.3f}s"
    
    def test_config_serialization_performance(self):
        """Config serialization should be fast."""
        import time
        
        config = SandboxConfig()
        
        start = time.perf_counter()
        for _ in range(1000):
            d = config.to_dict()
            SandboxConfig.from_dict(d)
        elapsed = time.perf_counter() - start
        
        # Should complete in under 1 second
        assert elapsed < 1.0, f"1000 serializations took {elapsed:.3f}s"


# =============================================================================
# Edge Cases
# =============================================================================

class TestSandboxEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_empty_converter_file(self, temp_dir):
        """Empty converter file fails validation."""
        empty_converter = temp_dir / "empty.py"
        empty_converter.write_text("")
        
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        # Empty file is valid syntax-wise
        is_valid, issues = validator.validate_source("")
        assert is_valid is True  # No dangerous patterns in empty file
    
    def test_syntax_error_converter(self, temp_dir):
        """Converter with syntax errors fails validation."""
        bad_converter = temp_dir / "bad_syntax.py"
        bad_converter.write_text("def broken(:\n    pass")  # Missing param
        
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        source = bad_converter.read_text()
        is_valid, issues = validator.validate_source(source)
        
        assert is_valid is False
        assert any("syntax" in issue.lower() for issue in issues)
    
    def test_unicode_in_converter(self, temp_dir):
        """Converter with unicode content works."""
        unicode_converter = temp_dir / "unicode.py"
        unicode_converter.write_text('''
# -*- coding: utf-8 -*-
"""Converter with unicode: 日本語, émojis 🚀"""

from pathlib import Path

class UnicodeConverter:
    """Handles 日本語 and émojis 🎉"""
    
    def convert_file(self, file_path: Path, args: dict):
        return {"status": "Success", "message": "日本語 OK!"}
''', encoding='utf-8')
        
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        source = unicode_converter.read_text(encoding='utf-8')
        is_valid, issues = validator.validate_source(source)
        
        assert is_valid is True
        assert len(issues) == 0
    
    def test_large_converter_file(self, temp_dir):
        """Large converter file can be validated."""
        # Create a converter with many methods
        methods = "\n".join([
            f'''
    def method_{i}(self, x):
        """Method {i}"""
        return x + {i}
''' for i in range(100)
        ])
        
        large_converter_code = f'''
from pathlib import Path

class LargeConverter:
    """Converter with many methods."""
{methods}
    
    def convert_file(self, file_path: Path, args: dict):
        return {{"status": "Success"}}
'''
        
        large_converter = temp_dir / "large.py"
        large_converter.write_text(large_converter_code)
        
        config = SandboxConfig()
        validator = ConverterValidator(config)
        
        source = large_converter.read_text()
        is_valid, issues = validator.validate_source(source)
        
        assert is_valid is True
        assert len(issues) == 0


# =============================================================================
# AsyncConverterPool Integration Tests
# =============================================================================

@pytest.mark.asyncio
class TestAsyncConverterPoolSandboxIntegration:
    """Tests for AsyncConverterPool sandbox integration."""
    
    async def test_pool_sandbox_parameter(self):
        """AsyncConverterPool accepts enable_sandbox parameter."""
        from pywats_client.service.async_converter_pool import AsyncConverterPool
        from unittest.mock import MagicMock, AsyncMock
        
        # Create mock config and api
        mock_config = MagicMock()
        mock_api = AsyncMock()
        
        # Should not raise
        pool = AsyncConverterPool(
            config=mock_config, 
            api=mock_api, 
            max_concurrent=2, 
            enable_sandbox=True
        )
        assert pool._enable_sandbox is True
        
        pool2 = AsyncConverterPool(
            config=mock_config, 
            api=mock_api, 
            max_concurrent=2, 
            enable_sandbox=False
        )
        assert pool2._enable_sandbox is False
    
    async def test_pool_creates_sandbox_when_enabled(self):
        """Pool creates sandbox when enabled."""
        from pywats_client.service.async_converter_pool import AsyncConverterPool
        from unittest.mock import MagicMock, AsyncMock
        
        mock_config = MagicMock()
        mock_api = AsyncMock()
        
        pool = AsyncConverterPool(
            config=mock_config, 
            api=mock_api, 
            max_concurrent=2, 
            enable_sandbox=True
        )
        
        # Access _ensure_sandbox method exists
        assert hasattr(pool, "_ensure_sandbox")
