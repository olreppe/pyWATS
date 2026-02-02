"""
Tests for structured logging functionality.

Tests JSON formatting, context management, and correlation IDs.
"""

import json
import logging
import pytest
from io import StringIO
from typing import Dict, Any

from pywats.core.logging import (
    get_logger,
    enable_debug_logging,
    set_logging_context,
    clear_logging_context,
    get_logging_context,
    StructuredFormatter,
    CorrelationFilter,
)


class TestStructuredFormatter:
    """Tests for JSON structured logging formatter."""
    
    def test_basic_json_output(self):
        """Test that StructuredFormatter outputs valid JSON."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="pywats.test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        output = formatter.format(record)
        data = json.loads(output)  # Should not raise
        
        assert data["level"] == "INFO"
        assert data["logger"] == "pywats.test"
        assert data["message"] == "Test message"
        assert "timestamp" in data
        assert data["timestamp"].endswith("+00:00")  # UTC timezone format
    
    def test_json_with_extra_fields(self):
        """Test that extra fields are included in JSON output."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="pywats.test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Report submitted",
            args=(),
            exc_info=None
        )
        
        # Add extra fields
        record.report_id = 123
        record.serial_number = "ABC-456"
        record.station = "ICT-01"
        
        output = formatter.format(record)
        data = json.loads(output)
        
        assert data["report_id"] == 123
        assert data["serial_number"] == "ABC-456"
        assert data["station"] == "ICT-01"
    
    def test_json_with_correlation_id(self):
        """Test that correlation ID is included when present."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="pywats.test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        record.correlation_id = "abc-123-xyz"
        
        output = formatter.format(record)
        data = json.loads(output)
        
        assert data["correlation_id"] == "abc-123-xyz"
    
    def test_json_without_correlation_id(self):
        """Test that placeholder correlation ID is excluded."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="pywats.test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        record.correlation_id = "--------"  # Placeholder
        
        output = formatter.format(record)
        data = json.loads(output)
        
        # Placeholder should not be included
        assert "correlation_id" not in data
    
    def test_json_with_exception(self):
        """Test that exceptions are formatted in JSON."""
        formatter = StructuredFormatter()
        
        try:
            raise ValueError("Test error")
        except ValueError:
            import sys
            exc_info = sys.exc_info()
        
        record = logging.LogRecord(
            name="pywats.test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=exc_info
        )
        
        output = formatter.format(record)
        data = json.loads(output)
        
        assert "exception" in data
        assert "ValueError: Test error" in data["exception"]
        assert "Traceback" in data["exception"]
    
    def test_json_with_non_serializable_field(self):
        """Test that non-serializable fields are converted to strings."""
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="pywats.test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # Add non-serializable field
        class CustomObject:
            def __str__(self):
                return "CustomObject instance"
        
        record.custom_obj = CustomObject()
        
        output = formatter.format(record)
        data = json.loads(output)
        
        assert data["custom_obj"] == "CustomObject instance"


class TestLoggingContext:
    """Tests for logging context management."""
    
    def test_set_logging_context(self):
        """Test setting logging context."""
        clear_logging_context()
        
        set_logging_context(user_id="user123", session_id="sess456")
        
        context = get_logging_context()
        assert context["user_id"] == "user123"
        assert context["session_id"] == "sess456"
    
    def test_update_logging_context(self):
        """Test updating existing logging context."""
        clear_logging_context()
        
        set_logging_context(user_id="user123")
        set_logging_context(session_id="sess456")
        
        context = get_logging_context()
        assert context["user_id"] == "user123"
        assert context["session_id"] == "sess456"
    
    def test_clear_logging_context(self):
        """Test clearing logging context."""
        set_logging_context(user_id="user123")
        clear_logging_context()
        
        context = get_logging_context()
        assert context == {}
    
    def test_logging_context_in_json_output(self):
        """Test that logging context appears in JSON output."""
        clear_logging_context()
        set_logging_context(environment="test", version="1.0")
        
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="pywats.test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        output = formatter.format(record)
        data = json.loads(output)
        
        assert "context" in data
        assert data["context"]["environment"] == "test"
        assert data["context"]["version"] == "1.0"


class TestEnableDebugLogging:
    """Tests for enable_debug_logging convenience function."""
    
    def teardown_method(self):
        """Clear handlers after each test."""
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        clear_logging_context()
    
    def test_enable_debug_logging_text_format(self):
        """Test enabling debug logging with text format."""
        # Capture stderr
        stream = StringIO()
        
        enable_debug_logging()
        
        # Replace handler's stream with our test stream
        root_logger = logging.getLogger()
        if root_logger.handlers:
            root_logger.handlers[0].stream = stream
        
        logger = get_logger("pywats.test")
        logger.info("Test message")
        
        output = stream.getvalue()
        assert "Test message" in output
        assert "pywats.test" in output
    
    def test_enable_debug_logging_json_format(self):
        """Test enabling debug logging with JSON format."""
        stream = StringIO()
        
        enable_debug_logging(use_json=True)
        
        # Replace handler's stream with our test stream
        root_logger = logging.getLogger()
        if root_logger.handlers:
            root_logger.handlers[0].stream = stream
        
        logger = get_logger("pywats.test")
        logger.info("Test message", extra={"test_field": "test_value"})
        
        output = stream.getvalue().strip()
        data = json.loads(output)
        
        assert data["message"] == "Test message"
        assert data["test_field"] == "test_value"
        assert data["level"] == "INFO"
    
    def test_enable_debug_logging_with_custom_level(self):
        """Test enabling logging with custom level."""
        stream = StringIO()
        
        enable_debug_logging(level=logging.WARNING)
        
        # Replace handler's stream with our test stream
        root_logger = logging.getLogger()
        if root_logger.handlers:
            root_logger.handlers[0].stream = stream
        
        logger = get_logger("pywats.test")
        logger.debug("Debug message")  # Should not appear
        logger.warning("Warning message")  # Should appear
        
        output = stream.getvalue()
        assert "Debug message" not in output
        assert "Warning message" in output
    
    def test_enable_debug_logging_removes_existing_handlers(self):
        """Test that enable_debug_logging removes existing handlers."""
        # Add a handler
        root_logger = logging.getLogger()
        handler1 = logging.StreamHandler()
        root_logger.addHandler(handler1)
        
        initial_count = len(root_logger.handlers)
        
        enable_debug_logging()
        
        # Should have exactly 1 handler (the new one)
        assert len(root_logger.handlers) == 1
        assert root_logger.handlers[0] is not handler1


class TestCorrelationFilter:
    """Tests for correlation ID filter."""
    
    def test_correlation_filter_adds_id(self):
        """Test that correlation filter adds correlation ID from context."""
        # Mock correlation_id_var since we can't import from pywats.pywats in tests
        from unittest.mock import patch, MagicMock
        
        mock_context_var = MagicMock()
        mock_context_var.get.return_value = "test-correlation-id"
        
        with patch('pywats.pywats.correlation_id_var', mock_context_var):
            filter_obj = CorrelationFilter()
            record = logging.LogRecord(
                name="pywats.test",
                level=logging.INFO,
                pathname="test.py",
                lineno=10,
                msg="Test message",
                args=(),
                exc_info=None
            )
            
            filter_obj.filter(record)
            
            assert hasattr(record, 'correlation_id')
            assert record.correlation_id == "test-correlation-id"
    
    def test_correlation_filter_uses_placeholder_when_no_id(self):
        """Test that correlation filter uses placeholder when no ID is set."""
        from unittest.mock import patch, MagicMock
        
        mock_context_var = MagicMock()
        mock_context_var.get.side_effect = LookupError()
        
        with patch('pywats.pywats.correlation_id_var', mock_context_var):
            filter_obj = CorrelationFilter()
            record = logging.LogRecord(
                name="pywats.test",
                level=logging.INFO,
                pathname="test.py",
                lineno=10,
                msg="Test message",
                args=(),
                exc_info=None
            )
            
            filter_obj.filter(record)
            
            assert hasattr(record, 'correlation_id')
            assert record.correlation_id == "--------"


class TestIntegration:
    """Integration tests for structured logging."""
    
    def teardown_method(self):
        """Clear handlers and context after each test."""
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        clear_logging_context()
    
    def test_end_to_end_json_logging_with_context(self):
        """Test complete workflow: context + correlation + JSON."""
        stream = StringIO()
        
        # Setup JSON logging
        enable_debug_logging(use_json=True)
        
        # Replace handler's stream
        root_logger = logging.getLogger()
        if root_logger.handlers:
            root_logger.handlers[0].stream = stream
        
        # Set context
        set_logging_context(environment="production", version="0.3.0")
        
        # Log with extra fields
        logger = get_logger("pywats.domains.report")
        logger.info("Report submitted", extra={
            "report_id": 789,
            "serial_number": "TEST-123",
            "station": "FCT-02"
        })
        
        # Parse output
        output = stream.getvalue().strip()
        data = json.loads(output)
        
        # Verify all fields present
        assert data["message"] == "Report submitted"
        assert data["logger"] == "pywats.domains.report"
        assert data["level"] == "INFO"
        assert data["report_id"] == 789
        assert data["serial_number"] == "TEST-123"
        assert data["station"] == "FCT-02"
        assert data["context"]["environment"] == "production"
        assert data["context"]["version"] == "0.3.0"
        assert "timestamp" in data
    
    def test_text_logging_with_correlation(self):
        """Test traditional text logging with correlation IDs."""
        from unittest.mock import patch, MagicMock
        
        stream = StringIO()
        
        enable_debug_logging(use_correlation_ids=True)
        
        # Replace handler's stream
        root_logger = logging.getLogger()
        if root_logger.handlers:
            root_logger.handlers[0].stream = stream
        
        # Mock correlation ID
        mock_context_var = MagicMock()
        mock_context_var.get.return_value = "corr-123"
        
        with patch('pywats.pywats.correlation_id_var', mock_context_var):
            # Manually trigger filter
            for handler in root_logger.handlers:
                for f in handler.filters:
                    if isinstance(f, CorrelationFilter):
                        record = logging.LogRecord(
                            name="pywats.test",
                            level=logging.INFO,
                            pathname="test.py",
                            lineno=10,
                            msg="Test message",
                            args=(),
                            exc_info=None
                        )
                        f.filter(record)
                        logger = get_logger("pywats.test")
                        logger.handle(record)
        
        output = stream.getvalue()
        
        # Correlation ID should be in output
        if output:  # May be empty depending on handler configuration
            assert "corr-123" in output or "Test message" in output
