"""  Conversion Logging - Per-conversion detailed logging.

Provides ConversionLog class for tracking detailed conversion steps,
warnings, and errors in a structured JSON line format.
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any


@dataclass
class ConversionLogEntry:
    """
    Single log entry for a conversion step.
    
    Attributes:
        timestamp: ISO 8601 timestamp
        level: Log level (INFO, WARNING, ERROR)
        step: Step name or description
        message: Log message
        metadata: Optional additional data
    """
    timestamp: str
    level: str
    step: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "timestamp": self.timestamp,
            "level": self.level,
            "step": self.step,
            "message": self.message
        }
        if self.metadata:
            result["metadata"] = self.metadata
        return result


class ConversionLog:
    """
    Per-conversion detailed logging.
    
    Creates a dedicated log file for each conversion with:
    - JSON line format (one JSON object per line)
    - Step-by-step tracking
    - Warning and error capture
    - Auto-flush for crash safety
    - Structured metadata
    
    Usage:
        >>> from pywats_client.converters.conversion_log import ConversionLog
        >>> log = ConversionLog.create_for_file("test.csv", instance_id="station_a")
        >>> 
        >>> log.step("Reading file", metadata={"size_bytes": 1024})
        >>> log.step("Parsing CSV", metadata={"rows": 10})
        >>> log.warning("Missing column: temperature")
        >>> log.step("Creating report", metadata={"serial": "SN123"})
        >>> log.finalize(success=True, report_id=456)
        
    Log file format (JSON Lines):
        {"timestamp": "2026-02-03T...", "level": "INFO", "step": "Reading file", "message": "Started", "metadata": {"size_bytes": 1024}}
        {"timestamp": "2026-02-03T...", "level": "INFO", "step": "Parsing CSV", "message": "Started", "metadata": {"rows": 10}}
        {"timestamp": "2026-02-03T...", "level": "WARNING", "step": "Validation", "message": "Missing column: temperature"}
        {"timestamp": "2026-02-03T...", "level": "INFO", "step": "Creating report", "message": "Started", "metadata": {"serial": "SN123"}}
        {"timestamp": "2026-02-03T...", "level": "INFO", "step": "COMPLETED", "message": "Conversion successful", "metadata": {"success": true, "report_id": 456}}
    """
    
    def __init__(
        self,
        log_file_path: Path,
        file_name: str,
        instance_id: str = "default"
    ):
        """
        Initialize conversion log.
        
        Args:
            log_file_path: Path to the log file
            file_name: Name of file being converted
            instance_id: Client instance identifier
        """
        self.log_file_path = log_file_path
        self.file_name = file_name
        self.instance_id = instance_id
        self.entries: List[ConversionLogEntry] = []
        self._finalized = False
        self._file_handle: Optional[Any] = None
        
        # Ensure directory exists
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Open log file in append mode
        self._file_handle = open(self.log_file_path, 'a', encoding='utf-8')
        
        # Write header entry
        self._write_entry(ConversionLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            level="INFO",
            step="START",
            message=f"Starting conversion of {file_name}",
            metadata={"instance_id": instance_id}
        ))
    
    @classmethod
    def create_for_file(
        cls,
        file_name: str,
        instance_id: str = "default"
    ) -> "ConversionLog":
        """
        Create a ConversionLog for a specific file.
        
        Creates log file in the conversion logs directory with timestamp.
        
        Args:
            file_name: Name of file being converted
            instance_id: Client instance identifier
            
        Returns:
            ConversionLog instance
            
        Example:
            >>> log = ConversionLog.create_for_file("test_data.csv")
            >>> # Log file: {install_dir}/logs/conversions/test_data_20260203_143022.log
        """
        from pywats_client.core.logging import get_conversion_log_dir
        
        # Get conversion log directory
        conversion_dir = get_conversion_log_dir(instance_id)
        
        # Create timestamped log filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = Path(file_name).stem.replace(" ", "_")
        log_filename = f"{safe_name}_{timestamp}.log"
        log_path = conversion_dir / log_filename
        
        return cls(log_path, file_name, instance_id)
    
    def step(
        self,
        step_name: str,
        message: str = "Started",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log a conversion step (INFO level).
        
        Args:
            step_name: Name/description of the step
            message: Optional message (default: "Started")
            metadata: Optional additional data
            
        Example:
            >>> log.step("Reading file", metadata={"size_bytes": 1024})
            >>> log.step("Parsing data", message="Found 10 rows", metadata={"rows": 10})
        """
        if self._finalized:
            logging.warning("Attempted to log step after finalization")
            return
        
        entry = ConversionLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            level="INFO",
            step=step_name,
            message=message,
            metadata=metadata
        )
        self._write_entry(entry)
    
    def warning(
        self,
        message: str,
        step: str = "Validation",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log a warning (WARNING level).
        
        Args:
            message: Warning message
            step: Step name where warning occurred (default: "Validation")
            metadata: Optional additional data
            
        Example:
            >>> log.warning("Missing optional field: temperature")
            >>> log.warning("Serial number format unusual", metadata={"serial": "ABC-123"})
        """
        if self._finalized:
            logging.warning("Attempted to log warning after finalization")
            return
        
        entry = ConversionLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            level="WARNING",
            step=step,
            message=message,
            metadata=metadata
        )
        self._write_entry(entry)
    
    def error(
        self,
        message: str,
        step: str = "Conversion",
        metadata: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None,
        raise_after_log: bool = True
    ) -> None:
        """
        Log an error (ERROR level).
        
        Args:
            message: Error message
            step: Step name where error occurred (default: "Conversion")
            metadata: Optional additional data
            exception: Optional exception object (will extract type and message)
            raise_after_log: If True and exception is provided, re-raises the exception
                           after logging (default: True). Set to False for backward
                           compatibility or when exception handling is done elsewhere.
            
        Example:
            >>> log.error("Failed to parse CSV", metadata={"line": 5})
            >>> 
            >>> # Exception will be re-raised after logging (default behavior)
            >>> try:
            >>>     data = parse_file()
            >>> except ValueError as e:
            >>>     log.error("Parse error", exception=e)  # Logs and re-raises
            >>> 
            >>> # Suppress re-raise for backward compatibility
            >>> try:
            >>>     data = parse_file()
            >>> except ValueError as e:
            >>>     log.error("Parse error", exception=e, raise_after_log=False)
            >>>     # Handle error without raising
        
        Note:
            Starting in v0.5.1, exceptions are re-raised by default to prevent
            silent failures. Set raise_after_log=False to maintain v0.5.0 behavior.
        """
        if self._finalized:
            logging.warning("Attempted to log error after finalization")
            return
        
        # Add exception info to metadata if provided
        if exception and metadata is None:
            metadata = {}
        if exception:
            if metadata is None:
                metadata = {}
            metadata["exception_type"] = type(exception).__name__
            metadata["exception_message"] = str(exception)
        
        entry = ConversionLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            level="ERROR",
            step=step,
            message=message,
            metadata=metadata
        )
        self._write_entry(entry)
        
        # Re-raise exception if configured (default behavior)
        if exception and raise_after_log:
            raise exception
    
    def finalize(
        self,
        success: bool,
        report_id: Optional[int] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Finalize the conversion log.
        
        Writes final entry and closes log file. Should be called when
        conversion completes (success or failure).
        
        Args:
            success: Whether conversion succeeded
            report_id: WATS report ID if successful
            error: Error message if failed
            metadata: Optional additional data
            
        Example (success):
            >>> log.finalize(success=True, report_id=456, metadata={"rows_processed": 10})
            
        Example (failure):
            >>> log.finalize(success=False, error="Invalid format")
        """
        if self._finalized:
            logging.warning("ConversionLog already finalized")
            return
        
        # Build final metadata
        final_metadata = metadata or {}
        final_metadata["success"] = success
        if report_id is not None:
            final_metadata["report_id"] = report_id
        if error:
            final_metadata["error"] = error
        
        # Write final entry
        entry = ConversionLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            level="INFO" if success else "ERROR",
            step="COMPLETED" if success else "FAILED",
            message="Conversion successful" if success else f"Conversion failed: {error}",
            metadata=final_metadata
        )
        self._write_entry(entry)
        
        # Close file
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None
        
        self._finalized = True
    
    def _write_entry(self, entry: ConversionLogEntry) -> None:
        """
        Write log entry to file (JSON line format).
        
        Args:
            entry: Log entry to write
        """
        self.entries.append(entry)
        
        if self._file_handle:
            # Write as single-line JSON
            json_line = json.dumps(entry.to_dict(), ensure_ascii=False)
            self._file_handle.write(json_line + '\n')
            self._file_handle.flush()  # Auto-flush for crash safety
    
    def __enter__(self) -> "ConversionLog":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - finalize on exception."""
        if not self._finalized:
            if exc_val:
                # Exception occurred - log as failure
                # Don't re-raise here - let the context manager propagate the original exception
                self.error(
                    message=str(exc_val),
                    step="Conversion",
                    exception=exc_val,
                    raise_after_log=False  # Context manager handles propagation
                )
                self.finalize(success=False, error=str(exc_val))
            else:
                # Normal exit without explicit finalize - log warning
                self.warning("ConversionLog not explicitly finalized")
                self.finalize(success=False, error="Incomplete conversion (no finalize() call)")
    
    def __del__(self) -> None:
        """Cleanup - ensure file is closed."""
        if self._file_handle and not self._file_handle.closed:
            try:
                if not self._finalized:
                    self.finalize(success=False, error="Log not properly finalized")
            except:
                pass  # Avoid errors during cleanup


__all__ = [
    'ConversionLog',
    'ConversionLogEntry',
]
