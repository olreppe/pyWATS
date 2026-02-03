"""
Tests for pyWATS logging utilities.

Tests the core logging configuration API including:
- configure_logging() function
- FileRotatingHandler class
- LoggingContext context manager
"""

import json
import logging
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest

from pywats.core.logging import (
    configure_logging,
    FileRotatingHandler,
    LoggingContext,
    get_logger,
    set_logging_context,
    clear_logging_context,
    get_logging_context,
)


class TestConfigureLogging:
    """Tests for configure_logging() function."""
    
    def setup_method(self):
        """Reset logging configuration before each test."""
        # Clear all handlers from root logger
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.setLevel(logging.WARNING)
        
        # Clear pyWATS logger
        pywats_logger = logging.getLogger('pywats')
        pywats_logger.handlers.clear()
        pywats_logger.setLevel(logging.WARNING)
        
        # Clear logging context
        clear_logging_context()
    
    def teardown_method(self):
        """Clean up after each test."""
        # Reset logging configuration
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.setLevel(logging.WARNING)
        
        pywats_logger = logging.getLogger('pywats')
        pywats_logger.handlers.clear()
        pywats_logger.setLevel(logging.WARNING)
        
        clear_logging_context()
    
    def test_configure_logging_default_console(self):
        """Test default configuration creates console handler with INFO level."""
        configure_logging()
        
        root_logger = logging.getLogger()
        
        # Should have one handler
        assert len(root_logger.handlers) == 1
        
        # Should be StreamHandler
        handler = root_logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        
        # Should be INFO level
        assert root_logger.level == logging.INFO
        
        # pyWATS logger should also be INFO
        pywats_logger = logging.getLogger('pywats')
        assert pywats_logger.level == logging.INFO
    
    def test_configure_logging_with_level_string(self):
        """Test setting log level using string."""
        configure_logging(level="DEBUG")
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG
        
        pywats_logger = logging.getLogger('pywats')
        assert pywats_logger.level == logging.DEBUG
    
    def test_configure_logging_with_level_int(self):
        """Test setting log level using integer."""
        configure_logging(level=logging.WARNING)
        
        root_logger = logging.getLogger()
        assert root_logger.level == logging.WARNING
        
        pywats_logger = logging.getLogger('pywats')
        assert pywats_logger.level == logging.WARNING
    
    def test_configure_logging_text_format(self):
        """Test text format creates Formatter."""
        configure_logging(format="text")
        
        root_logger = logging.getLogger()
        handler = root_logger.handlers[0]
        
        # Should have a formatter
        assert handler.formatter is not None
        assert isinstance(handler.formatter, logging.Formatter)
    
    def test_configure_logging_json_format(self):
        """Test JSON format creates StructuredFormatter."""
        configure_logging(format="json")
        
        root_logger = logging.getLogger()
        handler = root_logger.handlers[0]
        
        # Should have a formatter
        assert handler.formatter is not None
        # StructuredFormatter is a subclass of logging.Formatter
        assert isinstance(handler.formatter, logging.Formatter)
        # Check formatter class name
        assert handler.formatter.__class__.__name__ == 'StructuredFormatter'
    
    def test_configure_logging_with_file_path(self):
        """Test file logging creates rotating file handler."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            configure_logging(file_path=log_path)
            
            root_logger = logging.getLogger()
            
            # Should have one handler
            assert len(root_logger.handlers) == 1
            
            # Should be FileRotatingHandler
            handler = root_logger.handlers[0]
            assert isinstance(handler, FileRotatingHandler)
            
            # Log file should exist
            logger = get_logger(__name__)
            logger.info("Test message")
            
            # Close handler before cleanup
            handler.close()
            root_logger.handlers.clear()
            
            assert log_path.exists()
            content = log_path.read_text()
            assert "Test message" in content
    
    def test_configure_logging_with_custom_rotation(self):
        """Test custom rotation size and backup count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            configure_logging(
                file_path=log_path,
                rotate_size_mb=5,
                rotate_backups=3
            )
            
            root_logger = logging.getLogger()
            handler = root_logger.handlers[0]
            
            assert isinstance(handler, FileRotatingHandler)
            # Check rotation settings (5MB in bytes)
            assert handler.maxBytes == 5 * 1024 * 1024
            assert handler.backupCount == 3
            
            # Close handler before cleanup
            handler.close()
            root_logger.handlers.clear()
    
    def test_configure_logging_with_custom_handlers(self):
        """Test providing custom handlers."""
        # Create a custom handler
        import io
        stream = io.StringIO()
        custom_handler = logging.StreamHandler(stream)
        
        configure_logging(handlers=[custom_handler])
        
        root_logger = logging.getLogger()
        
        # Should use custom handler
        assert len(root_logger.handlers) == 1
        assert root_logger.handlers[0] is custom_handler
        
        # Test logging works
        logger = get_logger(__name__)
        logger.info("Test message")
        
        output = stream.getvalue()
        assert "Test message" in output
    
    def test_configure_logging_correlation_ids_enabled(self):
        """Test correlation IDs are added when enabled."""
        configure_logging(enable_correlation_ids=True, format="text")
        
        root_logger = logging.getLogger()
        handler = root_logger.handlers[0]
        
        # Should have CorrelationFilter
        assert len(handler.filters) > 0
        # Filter should be CorrelationFilter
        assert any(f.__class__.__name__ == 'CorrelationFilter' for f in handler.filters)
    
    def test_configure_logging_correlation_ids_disabled(self):
        """Test correlation IDs are not added when disabled."""
        configure_logging(enable_correlation_ids=False, format="text")
        
        root_logger = logging.getLogger()
        handler = root_logger.handlers[0]
        
        # Should not have CorrelationFilter
        assert all(f.__class__.__name__ != 'CorrelationFilter' for f in handler.filters)
    
    def test_configure_logging_clears_existing_handlers(self):
        """Test that calling configure_logging() clears existing handlers."""
        # Add a handler manually
        root_logger = logging.getLogger()
        old_handler = logging.StreamHandler()
        root_logger.addHandler(old_handler)
        
        initial_count = len(root_logger.handlers)
        assert initial_count >= 1  # At least our handler (pytest may add more)
        
        # Configure logging should clear old handlers
        configure_logging()
        
        # Should only have the new handler (pytest may add LogCaptureHandler)
        # Just verify old handler is gone
        assert old_handler not in root_logger.handlers
    
    def test_configure_logging_multiple_calls(self):
        """Test calling configure_logging() multiple times is safe."""
        configure_logging(level="DEBUG")
        configure_logging(level="INFO")
        configure_logging(level="WARNING")
        
        root_logger = logging.getLogger()
        
        # Should only have one handler
        assert len(root_logger.handlers) == 1
        
        # Should have latest level
        assert root_logger.level == logging.WARNING


class TestFileRotatingHandler:
    """Tests for FileRotatingHandler class."""
    
    def test_creates_log_file(self):
        """Test handler creates log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            handler = FileRotatingHandler(log_path)
            handler.setFormatter(logging.Formatter('%(message)s'))
            
            logger = logging.getLogger('test_handler')
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            
            logger.info("Test message")
            handler.close()
            
            assert log_path.exists()
            content = log_path.read_text()
            assert "Test message" in content
    
    def test_creates_parent_directories(self):
        """Test handler creates parent directories automatically."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "logs" / "app" / "test.log"
            
            # Directory should not exist yet
            assert not log_path.parent.exists()
            
            handler = FileRotatingHandler(log_path)
            
            # Directory should be created
            assert log_path.parent.exists()
            
            handler.close()
    
    def test_rotation_on_size(self):
        """Test file rotates when size limit is reached."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            # Create handler with tiny size limit (1KB)
            handler = FileRotatingHandler(
                log_path,
                max_bytes=1024,  # 1KB
                backup_count=2
            )
            handler.setFormatter(logging.Formatter('%(message)s'))
            
            logger = logging.getLogger('test_rotation')
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            
            # Write enough messages to trigger rotation
            for i in range(100):
                logger.info(f"Test message {i:04d} with some padding text to reach size limit")
            
            handler.close()
            
            # Should have created backup file(s)
            backup1 = Path(str(log_path) + ".1")
            assert backup1.exists() or log_path.stat().st_size < 1024
    
    def test_backup_count(self):
        """Test backup count limits number of backup files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            handler = FileRotatingHandler(
                log_path,
                max_bytes=100,  # Very small
                backup_count=2
            )
            handler.setFormatter(logging.Formatter('%(message)s'))
            
            logger = logging.getLogger('test_backups')
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            
            # Write many messages to create multiple backups
            for i in range(200):
                logger.info(f"Message {i:04d} padding padding padding")
            
            handler.close()
            
            # Should have at most backup_count backup files
            backup_files = list(Path(tmpdir).glob("test.log.*"))
            assert len(backup_files) <= 2
    
    def test_utf8_encoding(self):
        """Test handler uses UTF-8 encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            handler = FileRotatingHandler(log_path)
            handler.setFormatter(logging.Formatter('%(message)s'))
            
            logger = logging.getLogger('test_encoding')
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            
            # Log message with non-ASCII characters
            logger.info("Test message with Unicode: 日本語 中文 한글 🎉")
            handler.close()
            
            # Should read correctly as UTF-8
            content = log_path.read_text(encoding='utf-8')
            assert "日本語" in content
            assert "中文" in content
            assert "한글" in content
            assert "🎉" in content
    
    def test_accepts_path_object(self):
        """Test handler accepts Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            # Should accept Path object
            handler = FileRotatingHandler(log_path)
            assert handler is not None
            handler.close()
    
    def test_accepts_string_path(self):
        """Test handler accepts string path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = str(Path(tmpdir) / "test.log")
            
            # Should accept string path
            handler = FileRotatingHandler(log_path)
            assert handler is not None
            handler.close()
    
    def test_default_rotation_settings(self):
        """Test default rotation is 10MB and 5 backups."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            handler = FileRotatingHandler(log_path)
            
            # Check defaults
            assert handler.maxBytes == 10 * 1024 * 1024  # 10MB
            assert handler.backupCount == 5
            
            handler.close()


class TestLoggingContext:
    """Tests for LoggingContext context manager."""
    
    def setup_method(self):
        """Clear logging context before each test."""
        clear_logging_context()
    
    def teardown_method(self):
        """Clear logging context after each test."""
        clear_logging_context()
    
    def test_context_sets_values(self):
        """Test context manager sets context values."""
        assert get_logging_context() == {}
        
        with LoggingContext(request_id="req123", user="alice"):
            context = get_logging_context()
            assert context["request_id"] == "req123"
            assert context["user"] == "alice"
    
    def test_context_restores_on_exit(self):
        """Test context manager restores previous context on exit."""
        with LoggingContext(request_id="req123"):
            assert get_logging_context()["request_id"] == "req123"
        
        # Context should be cleared after exit
        assert get_logging_context() == {}
    
    def test_nested_contexts(self):
        """Test nested context managers work correctly."""
        with LoggingContext(request_id="req123"):
            assert get_logging_context()["request_id"] == "req123"
            
            with LoggingContext(user="alice"):
                context = get_logging_context()
                # Should have both values
                assert context["request_id"] == "req123"
                assert context["user"] == "alice"
            
            # Inner context should be removed
            context = get_logging_context()
            assert context["request_id"] == "req123"
            assert "user" not in context
        
        # All context should be cleared
        assert get_logging_context() == {}
    
    def test_context_with_exception(self):
        """Test context is restored even when exception occurs."""
        try:
            with LoggingContext(request_id="req123"):
                assert get_logging_context()["request_id"] == "req123"
                raise ValueError("Test error")
        except ValueError:
            pass
        
        # Context should be restored despite exception
        assert get_logging_context() == {}
    
    def test_context_updates_existing(self):
        """Test context manager updates existing context."""
        set_logging_context(session_id="sess456")
        
        with LoggingContext(request_id="req123"):
            context = get_logging_context()
            # Should have both values
            assert context["session_id"] == "sess456"
            assert context["request_id"] == "req123"
        
        # Should restore to just session_id
        context = get_logging_context()
        assert context["session_id"] == "sess456"
        assert "request_id" not in context
    
    def test_context_overwrites_keys(self):
        """Test context manager overwrites existing keys."""
        set_logging_context(user="bob")
        
        with LoggingContext(user="alice"):
            assert get_logging_context()["user"] == "alice"
        
        # Should restore original value
        assert get_logging_context()["user"] == "bob"
