"""
Client logging infrastructure for pyWATS.

Provides centralized logging setup for client-side operations including:
- Top-level pywats.log in installation directory
- Conversion logs directory management
- Rotating file handlers
- Integration with core logging framework

Usage:
    >>> from pywats_client.core.logging import setup_client_logging
    >>> setup_client_logging(instance_id="test_station", log_level="INFO")
    >>> # Now all logs go to {install_dir}/pywats.log with rotation
"""

import logging
from pywats.core.logging import get_logger
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal, Optional

from pywats.core.logging import configure_logging, FileRotatingHandler


def get_client_log_path(instance_id: str = "default") -> Path:
    """
    Get the path to the main client log file.
    
    Returns the top-level pywats.log file path in the client installation
    directory. Creates parent directories if they don't exist.
    
    Args:
        instance_id: Client instance identifier (default: "default")
        
    Returns:
        Path to pywats.log file
        
    Example:
        >>> from pywats_client.core.logging import get_client_log_path
        >>> log_path = get_client_log_path("station_a")
        >>> print(log_path)
        C:/ProgramData/pyWATS/station_a/pywats.log
    """
    from .config import ClientConfig
    
    try:
        config = ClientConfig.load_for_instance(instance_id)
        # Use reports path parent as installation directory
        install_dir = config.get_reports_path().parent
    except Exception:
        # Fallback to ProgramData if config unavailable
        if Path("C:/ProgramData").exists():
            install_dir = Path("C:/ProgramData") / "pyWATS" / instance_id
        else:
            # Linux/Mac fallback
            install_dir = Path.home() / ".pywats" / instance_id
    
    # Ensure directory exists
    install_dir.mkdir(parents=True, exist_ok=True)
    
    return install_dir / "pywats.log"


def get_conversion_log_dir(instance_id: str = "default") -> Path:
    """
    Get the directory for conversion logs.
    
    Returns the path to the conversion logs directory. Each conversion
    creates a separate log file in this directory.
    
    Args:
        instance_id: Client instance identifier (default: "default")
        
    Returns:
        Path to conversion logs directory
        
    Example:
        >>> from pywats_client.core.logging import get_conversion_log_dir
        >>> log_dir = get_conversion_log_dir("station_a")
        >>> print(log_dir)
        C:/ProgramData/pyWATS/station_a/logs/conversions
    """
    log_path = get_client_log_path(instance_id)
    conversion_dir = log_path.parent / "logs" / "conversions"
    
    # Create directory if it doesn't exist
    conversion_dir.mkdir(parents=True, exist_ok=True)
    
    return conversion_dir


def setup_client_logging(
    instance_id: str = "default",
    log_level: str = "INFO",
    log_format: Literal["text", "json"] = "text",
    enable_console: bool = True,
    rotate_size_mb: int = 10,
    rotate_backups: int = 5
) -> Path:
    """
    Configure unified logging for pyWATS client.
    
    Sets up logging with:
    - Top-level pywats.log in installation directory
    - Automatic file rotation (default: 10MB, 5 backups)
    - Optional console output
    - Text or JSON format
    - Correlation ID support
    
    This is the recommended way to configure logging for client applications,
    services, and GUI components.
    
    Args:
        instance_id: Client instance identifier (default: "default")
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Output format - "text" or "json"
        enable_console: Also log to console (default: True)
        rotate_size_mb: Max file size in MB before rotation (default: 10)
        rotate_backups: Number of backup files to keep (default: 5)
        
    Returns:
        Path to the log file
        
    Example (headless service):
        >>> from pywats_client.core.logging import setup_client_logging
        >>> log_path = setup_client_logging(
        ...     instance_id="test_station",
        ...     log_level="INFO",
        ...     enable_console=False
        ... )
        
    Example (GUI with JSON logging):
        >>> from pywats_client.core.logging import setup_client_logging
        >>> log_path = setup_client_logging(
        ...     instance_id="production",
        ...     log_level="DEBUG",
        ...     log_format="json",
        ...     enable_console=True
        ... )
    """
    # Get log file path
    log_path = get_client_log_path(instance_id)
    
    # Create handlers list
    handlers = []
    
    # Add file handler with rotation
    file_handler = FileRotatingHandler(
        log_path,
        max_bytes=rotate_size_mb * 1024 * 1024,
        backup_count=rotate_backups
    )
    handlers.append(file_handler)
    
    # Add console handler if enabled
    if enable_console:
        console_handler = logging.StreamHandler()
        handlers.append(console_handler)
    
    # Configure logging using core framework
    configure_logging(
        level=log_level,
        format=log_format,
        handlers=handlers,
        enable_correlation_ids=True,
        enable_context=True
    )
    
    # Log startup message
    logger = get_logger(__name__)
    logger.info(
        f"Client logging configured",
        extra={
            "instance_id": instance_id,
            "log_path": str(log_path),
            "log_level": log_level,
            "log_format": log_format,
            "enable_console": enable_console
        }
    )
    
    return log_path


def cleanup_old_conversion_logs(
    instance_id: str = "default",
    max_age_days: int = 30,
    dry_run: bool = False
) -> int:
    """
    Clean up old conversion log files.
    
    Removes conversion logs older than the specified age. This helps
    manage disk space usage for systems with many conversions.
    
    Args:
        instance_id: Client instance identifier (default: "default")
        max_age_days: Maximum age in days before deletion (default: 30)
        dry_run: If True, only report what would be deleted (default: False)
        
    Returns:
        Number of files deleted (or would be deleted if dry_run=True)
        
    Example:
        >>> from pywats_client.core.logging import cleanup_old_conversion_logs
        >>> # See what would be deleted
        >>> count = cleanup_old_conversion_logs(max_age_days=30, dry_run=True)
        >>> print(f"Would delete {count} files")
        >>> 
        >>> # Actually delete old logs
        >>> count = cleanup_old_conversion_logs(max_age_days=30)
        >>> print(f"Deleted {count} old conversion logs")
    """
    conversion_dir = get_conversion_log_dir(instance_id)
    
    if not conversion_dir.exists():
        return 0
    
    # Calculate cutoff date
    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    cutoff_timestamp = cutoff_date.timestamp()
    
    deleted_count = 0
    logger = get_logger(__name__)
    
    # Find and delete old log files
    for log_file in conversion_dir.glob("*.log"):
        try:
            # Check file modification time
            if log_file.stat().st_mtime < cutoff_timestamp:
                if dry_run:
                    logger.info(f"Would delete: {log_file.name}")
                    deleted_count += 1
                else:
                    log_file.unlink()
                    logger.debug(f"Deleted old conversion log: {log_file.name}")
                    deleted_count += 1
        except Exception as e:
            logger.warning(f"Failed to process {log_file.name}: {e}", exc_info=True)
    
    if deleted_count > 0:
        logger.info(
            f"Cleanup complete: {'would delete' if dry_run else 'deleted'} {deleted_count} files",
            extra={
                "instance_id": instance_id,
                "max_age_days": max_age_days,
                "dry_run": dry_run,
                "deleted_count": deleted_count
            }
        )
    
    return deleted_count


__all__ = [
    'setup_client_logging',
    'get_client_log_path',
    'get_conversion_log_dir',
    'cleanup_old_conversion_logs',
]
