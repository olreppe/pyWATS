"""
Logging utilities for pyWATS.

The library uses Python's standard logging module but never configures
handlers or output. This allows applications to control logging behavior.

Usage in library code:
    >>> from pywats.core.logging import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.debug("Debug message")
    >>> logger.info("Info message")

Usage for quick debugging:
    >>> from pywats import enable_debug_logging
    >>> enable_debug_logging()
"""

import logging
from typing import Optional


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


def enable_debug_logging(format_string: Optional[str] = None, use_correlation_ids: bool = True) -> None:
    """
    Convenience function to enable debug logging for pyWATS.
    
    This is a helper for quick debugging but applications should
    configure logging properly for production use.
    
    Args:
        format_string: Custom format string for log messages.
                      Defaults to format with correlation IDs if use_correlation_ids=True,
                      otherwise: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        use_correlation_ids: Whether to include correlation IDs in log format
    
    Example:
        >>> from pywats import enable_debug_logging
        >>> enable_debug_logging()
        >>> # Now all pyWATS debug messages will be visible with correlation IDs
    """
    if format_string is None:
        format_string = DEFAULT_FORMAT_DETAILED if use_correlation_ids else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure basic logging
    logging.basicConfig(
        level=logging.DEBUG,
        format=format_string
    )
    
    # Set pyWATS logger level
    pywats_logger = logging.getLogger('pywats')
    pywats_logger.setLevel(logging.DEBUG)
    
    # Add correlation filter if enabled
    if use_correlation_ids:
        for handler in logging.getLogger().handlers:
            handler.addFilter(CorrelationFilter())


# Suppress warnings about unconfigured logging
# This prevents "No handlers found" warnings when the library is used
# without explicit logging configuration
logging.getLogger('pywats').addHandler(logging.NullHandler())
