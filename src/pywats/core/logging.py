"""
Logging utilities for pyWATS.

The library uses Python's standard logging module but never configures
handlers or output. This allows applications to control logging behavior.

Supports both traditional text logging and structured JSON logging:

Text logging usage:
    >>> from pywats.core.logging import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.debug("Debug message")
    >>> logger.info("Info message")

JSON structured logging usage:
    >>> from pywats import enable_debug_logging
    >>> enable_debug_logging(use_json=True)
    >>> logger = get_logger(__name__)
    >>> logger.info("Report submitted", extra={"report_id": 123, "serial": "ABC123"})

Quick debugging:
    >>> from pywats import enable_debug_logging
    >>> enable_debug_logging()
"""

import json
import logging
import sys
from contextvars import ContextVar, copy_context
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union


# Context variable for structured logging metadata
_logging_context: ContextVar[Dict[str, Any]] = ContextVar('_logging_context', default={})


class CorrelationFilter(logging.Filter):
    """
    Logging filter that adds correlation ID to log records.
    
    The correlation ID is retrieved from the correlation_id_var context variable.
    If no correlation ID is set, uses "--------" as placeholder.
    """
    
    def filter(self, record):
        """Add correlation_id attribute to log record."""
        # Import here to avoid circular dependency
        try:
            from ..pywats import correlation_id_var
            corr_id = correlation_id_var.get()
            record.correlation_id = corr_id if corr_id else "--------"
        except (ImportError, LookupError):
            record.correlation_id = "--------"
        return True


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    Outputs log records as JSON objects with standard fields plus any
    extra fields provided via LogRecord.extra.
    
    Standard fields:
        - timestamp: ISO 8601 timestamp
        - level: Log level name (DEBUG, INFO, etc.)
        - logger: Logger name
        - message: Log message
        - correlation_id: Correlation ID from context (if available)
        - context: Additional structured context from ContextVar
        
    Example output:
        {"timestamp": "2024-02-02T10:30:45.123Z", "level": "INFO",
         "logger": "pywats.domains.report", "message": "Report submitted",
         "correlation_id": "abc-123", "report_id": 456, "serial": "XYZ"}
    
    Important: Avoid using reserved LogRecord field names in extra dict:
        Reserved: process, processName, thread, threadName, name, msg, args, 
                  created, filename, funcName, levelname, levelno, lineno, 
                  module, msecs, message, pathname, exc_info, exc_text, stack_info
        
        Use alternatives like: process_type, process_name, thread_id, etc.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        # Base fields
        log_data: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add correlation ID if available
        if hasattr(record, 'correlation_id') and record.correlation_id != "--------":
            log_data["correlation_id"] = record.correlation_id
        
        # Add context from ContextVar
        try:
            context = _logging_context.get()
            if context:
                log_data["context"] = context
        except LookupError:
            pass
        
        # Add extra fields from record.__dict__
        # Exclude standard logging fields and private attributes
        reserved_fields = {
            'name', 'msg', 'args', 'created', 'filename', 'funcName', 'levelname',
            'levelno', 'lineno', 'module', 'msecs', 'message', 'pathname', 'process',
            'processName', 'relativeCreated', 'thread', 'threadName', 'exc_info',
            'exc_text', 'stack_info', 'correlation_id'
        }
        
        for key, value in record.__dict__.items():
            if key not in reserved_fields and not key.startswith('_'):
                # Handle non-serializable types
                try:
                    json.dumps(value)  # Test serializability
                    log_data[key] = value
                except (TypeError, ValueError):
                    log_data[key] = str(value)
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


# Default format with correlation ID
DEFAULT_FORMAT = "[%(levelname)s] [%(correlation_id)s] %(name)s: %(message)s"
DEFAULT_FORMAT_DETAILED = "%(asctime)s [%(levelname)s] [%(correlation_id)s] %(name)s: %(message)s"


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the given name.
    
    All pyWATS loggers are children of 'pywats' root logger,
    allowing users to control library logging with:
    
        >>> import logging
        >>> logging.getLogger('pywats').setLevel(logging.WARNING)
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def set_logging_context(**kwargs: Any) -> None:
    """
    Set structured logging context that will be included in all log messages.
    
    The context is stored in a ContextVar and is automatically included
    in JSON-formatted log output.
    
    Args:
        **kwargs: Key-value pairs to add to logging context
        
    Example:
        >>> from pywats.core.logging import set_logging_context, get_logger
        >>> set_logging_context(user_id="user123", session_id="sess456")
        >>> logger = get_logger(__name__)
        >>> logger.info("User action")  # Will include user_id and session_id in JSON output
    """
    current = _logging_context.get({})
    current.update(kwargs)
    _logging_context.set(current)


def clear_logging_context() -> None:
    """
    Clear all structured logging context.
    
    Example:
        >>> from pywats.core.logging import clear_logging_context
        >>> clear_logging_context()
    """
    _logging_context.set({})


def get_logging_context() -> Dict[str, Any]:
    """
    Get current structured logging context.
    
    Returns:
        Dictionary of current context values
        
    Example:
        >>> from pywats.core.logging import get_logging_context
        >>> context = get_logging_context()
        >>> print(context)
        {'user_id': 'user123', 'session_id': 'sess456'}
    """
    return _logging_context.get({}).copy()


class FileRotatingHandler(RotatingFileHandler):
    """
    File handler with automatic rotation based on size.
    
    Extends Python's RotatingFileHandler with pyWATS-specific defaults
    and UTF-8 encoding enforcement.
    
    Args:
        file_path: Path to log file
        max_bytes: Maximum file size before rotation (default: 10MB)
        backup_count: Number of backup files to keep (default: 5)
        
    Example:
        >>> from pywats.core.logging import FileRotatingHandler
        >>> handler = FileRotatingHandler("app.log", max_bytes=5*1024*1024, backup_count=3)
    """
    
    def __init__(
        self,
        file_path: Union[str, Path],
        max_bytes: int = 10 * 1024 * 1024,  # 10MB default
        backup_count: int = 5
    ):
        """Initialize rotating file handler with UTF-8 encoding."""
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        super().__init__(
            filename=str(file_path),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )


class LoggingContext:
    """
    Context manager for scoped logging context.
    
    Automatically adds context key-value pairs to all log messages
    within the context scope. Context is cleaned up on exit.
    
    Args:
        **kwargs: Key-value pairs to add to logging context
        
    Example:
        >>> from pywats.core.logging import LoggingContext, get_logger
        >>> logger = get_logger(__name__)
        >>> with LoggingContext(request_id="req123", user="alice"):
        ...     logger.info("Processing request")  # Includes request_id and user
        >>> logger.info("Outside context")  # No request_id or user
    """
    
    def __init__(self, **kwargs: Any):
        """Initialize context with key-value pairs."""
        self.context = kwargs
        self.previous_context: Optional[Dict[str, Any]] = None
    
    def __enter__(self):
        """Enter context: save previous and set new context."""
        self.previous_context = _logging_context.get({}).copy()
        current = self.previous_context.copy()
        current.update(self.context)
        _logging_context.set(current)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context: restore previous context."""
        if self.previous_context is not None:
            _logging_context.set(self.previous_context)
        return False


def configure_logging(
    level: Union[str, int] = "INFO",
    format: Literal["text", "json"] = "text",
    handlers: Optional[List[logging.Handler]] = None,
    file_path: Optional[Path] = None,
    rotate_size_mb: int = 10,
    rotate_backups: int = 5,
    enable_correlation_ids: bool = True,
    enable_context: bool = True
) -> None:
    """
    Configure unified logging for pyWATS with support for text/JSON formats and file rotation.
    
    This is the recommended way to configure logging in pyWATS applications.
    Replaces enable_debug_logging() and enable_json_logging() with a unified API.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) or numeric value
        format: Output format - "text" for human-readable or "json" for structured
        handlers: Optional list of custom handlers (if provided, file_path is ignored)
        file_path: Optional path to log file (enables file rotation if provided)
        rotate_size_mb: Maximum log file size in MB before rotation (default: 10)
        rotate_backups: Number of backup files to keep (default: 5)
        enable_correlation_ids: Include correlation IDs in log output (default: True)
        enable_context: Include logging context in log output (default: True)
        
    Example (text logging to console):
        >>> from pywats.core.logging import configure_logging
        >>> configure_logging(level="DEBUG", format="text")
        
    Example (JSON logging to file with rotation):
        >>> from pathlib import Path
        >>> from pywats.core.logging import configure_logging
        >>> configure_logging(
        ...     level="INFO",
        ...     format="json",
        ...     file_path=Path("logs/pywats.log"),
        ...     rotate_size_mb=20,
        ...     rotate_backups=10
        ... )
        
    Example (custom handlers):
        >>> import logging
        >>> from pywats.core.logging import configure_logging
        >>> custom_handler = logging.StreamHandler()
        >>> configure_logging(handlers=[custom_handler])
    """
    # Convert string level to numeric if needed
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    
    # Get root logger
    root_logger = logging.getLogger()
    
    # Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # Determine handlers to use
    if handlers is not None:
        # Use custom handlers
        handler_list = handlers
    elif file_path is not None:
        # Create rotating file handler
        max_bytes = rotate_size_mb * 1024 * 1024
        handler_list = [FileRotatingHandler(file_path, max_bytes, rotate_backups)]
    else:
        # Default to console handler
        handler_list = [logging.StreamHandler(sys.stdout)]
    
    # Configure each handler
    for handler in handler_list:
        # Set formatter based on format type
        if format == "json":
            formatter = StructuredFormatter()
        else:
            # Use detailed format with correlation IDs if enabled
            if enable_correlation_ids:
                format_string = DEFAULT_FORMAT_DETAILED
            else:
                format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(format_string)
        
        handler.setFormatter(formatter)
        
        # Add correlation filter if enabled (for both JSON and text)
        if enable_correlation_ids:
            handler.addFilter(CorrelationFilter())
        
        # Add handler to root logger
        root_logger.addHandler(handler)
    
    # Set root logger level
    root_logger.setLevel(level)
    
    # Set pyWATS logger level
    pywats_logger = logging.getLogger('pywats')
    pywats_logger.setLevel(level)


def enable_debug_logging(
    format_string: Optional[str] = None,
    use_correlation_ids: bool = True,
    use_json: bool = False,
    level: int = logging.DEBUG
) -> None:
    """
    Convenience function to enable debug logging for pyWATS.
    
    .. deprecated:: 0.5.0
        Use :func:`configure_logging` instead for a more flexible API.
    
    This is a helper for quick debugging but applications should
    configure logging properly for production use.
    
    Args:
        format_string: Custom format string for log messages.
                      Ignored if use_json=True.
                      Defaults to format with correlation IDs if use_correlation_ids=True,
                      otherwise: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        use_correlation_ids: Whether to include correlation IDs in log format
        use_json: Whether to use JSON structured logging format
        level: Logging level (default: logging.DEBUG)
    
    Example (traditional logging):
        >>> from pywats import enable_debug_logging
        >>> enable_debug_logging()
        >>> # Now all pyWATS debug messages will be visible with correlation IDs
        
    Example (JSON structured logging):
        >>> from pywats import enable_debug_logging
        >>> enable_debug_logging(use_json=True)
        >>> # All logs will be output as JSON with structured fields
    
    Note:
        This function is deprecated. Use configure_logging() instead:
        
        Instead of:
            enable_debug_logging(use_json=True, level=logging.INFO)
        
        Use:
            configure_logging(level="INFO", format="json")
    """
    import warnings
    warnings.warn(
        "enable_debug_logging() is deprecated and will be removed in v1.0.0. "
        "Use configure_logging() instead for a more flexible API.",
        DeprecationWarning,
        stacklevel=2
    )
    
    # If custom format_string provided, we need to create a custom handler
    if format_string is not None and not use_json:
        # Create custom handler with user's format
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(format_string))
        if use_correlation_ids:
            handler.addFilter(CorrelationFilter())
        configure_logging(level=level, handlers=[handler], enable_correlation_ids=use_correlation_ids)
    else:
        # Use configure_logging with appropriate settings
        configure_logging(
            level=level,
            format="json" if use_json else "text",
            enable_correlation_ids=use_correlation_ids
        )


# Suppress warnings about unconfigured logging
# This prevents "No handlers found" warnings when the library is used
# without explicit logging configuration
logging.getLogger('pywats').addHandler(logging.NullHandler())


__all__ = [
    'get_logger',
    'configure_logging',
    'enable_debug_logging',
    'set_logging_context',
    'clear_logging_context',
    'get_logging_context',
    'FileRotatingHandler',
    'LoggingContext',
    'CorrelationFilter',
    'StructuredFormatter',
    'DEFAULT_FORMAT',
    'DEFAULT_FORMAT_DETAILED',
]
