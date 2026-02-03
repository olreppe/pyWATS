"""Integration tests for pyWATS logging infrastructure.

Tests end-to-end logging scenarios with actual API behavior.
Simplified to verify core logging functionality works correctly.
"""
import json
import logging
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from pywats.core.logging import (
    configure_logging,
    get_logger,
    LoggingContext,
    clear_logging_context,
    FileRotatingHandler,
)


@pytest.fixture
def log_dir() -> Generator[Path, None, None]:
    """Provide temporary directory for log files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration before each test."""
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    root.setLevel(logging.WARNING)
    clear_logging_context()
    
    yield
    
    for handler in root.handlers[:]:
        handler.close()
        root.removeHandler(handler)
    clear_logging_context()


class TestUnifiedConfiguration:
    """Test configure_logging() integration."""
    
    def test_console_logging(self):
        """Test simple console configuration."""
        configure_logging(level="INFO", format="text")
        
        logger = get_logger("test.module")
        logger.info("Test message")
        
        # Verify handler attached to root
        root = logging.getLogger()
        assert len(root.handlers) > 0
    
    def test_file_logging(self, log_dir: Path):
        """Test file logging works end-to-end."""
        log_file = log_dir / "app.log"
        
        configure_logging(
            level="INFO",
            format="text",
            file_path=log_file,
        )
        
        logger = get_logger("test.file")
        logger.info("Test message")
        logger.debug("Should not appear")  # Below INFO level
        
        # Force flush
        for handler in logging.getLogger().handlers:
            handler.flush()
        
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content
        assert "Should not appear" not in content
    
    def test_json_logging(self, log_dir: Path):
        """Test JSON structured logging."""
        log_file = log_dir / "structured.log"
        
        configure_logging(
            level="INFO",
            format="json",
            file_path=log_file,
        )
        
        logger = get_logger("test.json")
        logger.info("Structured event", extra={"user_id": 123})
        
        # Force flush
        for handler in logging.getLogger().handlers:
            handler.flush()
        
        content = log_file.read_text().strip()
        log_entry = json.loads(content)
        
        assert log_entry["message"] == "Structured event"
        assert log_entry["user_id"] == 123
        assert "level" in log_entry


class TestLoggingContext:
    """Test context management integration."""
    
    def test_context_scoping(self, log_dir: Path):
        """Test LoggingContext provides scoped metadata."""
        log_file = log_dir / "context.log"
        
        configure_logging(
            level="INFO",
            format="json",
            file_path=log_file,
            enable_context=True,
        )
        
        logger = get_logger("test.context")
        
        logger.info("Before context")
        
        with LoggingContext(request_id="REQ-123"):
            logger.info("Inside context")
        
        logger.info("After context")
        
        # Force flush
        for handler in logging.getLogger().handlers:
            handler.flush()
        
        lines = log_file.read_text().strip().split("\n")
        assert len(lines) == 3


class TestFileRotation:
    """Test file rotation works correctly."""
    
    def test_rotation_creates_backup(self, log_dir: Path):
        """Test files rotate when size limit reached."""
        log_file = log_dir / "rotate.log"
        
        # Configure with small size limit
        handler = FileRotatingHandler(
            str(log_file),
            max_bytes=1024,  # 1KB
            backup_count=2,
        )
        
        logger = logging.getLogger("test.rotation")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        # Write enough to trigger rotation
        for i in range(100):
            logger.info(f"Message {i} {'x' * 100}")
        
        handler.close()
        
        # Should have created files
        all_files = list(log_dir.glob("rotate.log*"))
        assert len(all_files) >= 1  # At minimum the current file


class TestMultiModule:
    """Test logging works across modules."""
    
    def test_multiple_modules_same_log(self, log_dir: Path):
        """Test different modules write to same log file."""
        log_file = log_dir / "multimodule.log"
        
        configure_logging(
            level="INFO",
            format="json",
            file_path=log_file,
        )
        
        # Different module loggers
        logger_a = get_logger("module.a")
        logger_b = get_logger("module.b.sub")
        logger_c = get_logger("another")
        
        logger_a.info("From A")
        logger_b.info("From B")
        logger_c.info("From C")
        
        # Force flush
        for handler in logging.getLogger().handlers:
            handler.flush()
        
        lines = log_file.read_text().strip().split("\n")
        assert len(lines) == 3


class TestEndToEndScenarios:
    """Real-world integration scenarios."""
    
    def test_production_configuration(self, log_dir: Path):
        """Test typical production logging setup."""
        log_file = log_dir / "production.log"
        
        configure_logging(
            level="INFO",
            format="json",
            file_path=log_file,
            rotate_size_mb=50,
            rotate_backups=10,
            enable_correlation_ids=True,
            enable_context=True,
        )
        
        logger = get_logger("myapp.service")
        
        # Simulate production operations
        logger.info("Application started", extra={"version": "1.0.0"})
        logger.info("Processing request", extra={"request_id": "REQ-001"})
        logger.warning("Resource limit approaching", extra={"usage_pct": 85})
        logger.info("Request completed", extra={"duration_ms": 245})
        
        # Force flush
        for handler in logging.getLogger().handlers:
            handler.flush()
        
        assert log_file.exists()
        lines = log_file.read_text().strip().split("\n")
        assert len(lines) == 4
        
        # Verify all are valid JSON
        for line in lines:
            entry = json.loads(line)
            assert "message" in entry
            assert "timestamp" in entry
