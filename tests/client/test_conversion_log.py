"""
Tests for ConversionLog - Per-conversion detailed logging.

Tests the pyWATS conversion logging utilities including:
- ConversionLog class
- ConversionLogEntry dataclass
- JSON line format output
- Context manager usage
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from pywats_client.converters.conversion_log import (
    ConversionLog,
    ConversionLogEntry,
)


class TestConversionLogEntry:
    """Tests for ConversionLogEntry dataclass."""
    
    def test_create_entry(self):
        """Test creating a log entry."""
        entry = ConversionLogEntry(
            timestamp="2026-02-03T12:00:00Z",
            level="INFO",
            step="Reading file",
            message="Started"
        )
        
        assert entry.timestamp == "2026-02-03T12:00:00Z"
        assert entry.level == "INFO"
        assert entry.step == "Reading file"
        assert entry.message == "Started"
        assert entry.metadata is None
    
    def test_entry_with_metadata(self):
        """Test entry with metadata."""
        entry = ConversionLogEntry(
            timestamp="2026-02-03T12:00:00Z",
            level="INFO",
            step="Parsing",
            message="Found rows",
            metadata={"rows": 10, "columns": 5}
        )
        
        assert entry.metadata == {"rows": 10, "columns": 5}
    
    def test_to_dict(self):
        """Test converting entry to dictionary."""
        entry = ConversionLogEntry(
            timestamp="2026-02-03T12:00:00Z",
            level="WARNING",
            step="Validation",
            message="Missing field",
            metadata={"field": "temperature"}
        )
        
        result = entry.to_dict()
        
        assert result == {
            "timestamp": "2026-02-03T12:00:00Z",
            "level": "WARNING",
            "step": "Validation",
            "message": "Missing field",
            "metadata": {"field": "temperature"}
        }
    
    def test_to_dict_without_metadata(self):
        """Test to_dict without metadata."""
        entry = ConversionLogEntry(
            timestamp="2026-02-03T12:00:00Z",
            level="INFO",
            step="Test",
            message="Test message"
        )
        
        result = entry.to_dict()
        
        assert "metadata" not in result


class TestConversionLog:
    """Tests for ConversionLog class."""
    
    def test_create_log(self):
        """Test creating a conversion log."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test_file.csv", "test_instance")
            log.finalize(success=True)
            
            assert log.log_file_path == log_path
            assert log.file_name == "test_file.csv"
            assert log.instance_id == "test_instance"
            assert log_path.exists()
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_create_for_file(self, mock_get_dir):
        """Test create_for_file class method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            conversion_dir = Path(tmpdir) / "conversions"
            conversion_dir.mkdir()
            mock_get_dir.return_value = conversion_dir
            
            log = ConversionLog.create_for_file("test_data.csv", "test")
            log.finalize(success=True)
            
            # Check log file was created
            log_files = list(conversion_dir.glob("test_data_*.log"))
            assert len(log_files) == 1
            assert log_files[0].stem.startswith("test_data_")
    
    def test_step_logging(self):
        """Test step() method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            log.step("Reading file", metadata={"size": 1024})
            log.step("Parsing data", message="Found rows", metadata={"rows": 10})
            log.finalize(success=True)
            
            # Read log file
            lines = log_path.read_text().strip().split('\n')
            assert len(lines) >= 3  # START + 2 steps + COMPLETED
            
            # Check second line (first step)
            entry = json.loads(lines[1])
            assert entry["level"] == "INFO"
            assert entry["step"] == "Reading file"
            assert entry["metadata"]["size"] == 1024
    
    def test_warning_logging(self):
        """Test warning() method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            log.warning("Missing optional field", metadata={"field": "temp"})
            log.finalize(success=True)
            
            # Read log file
            lines = log_path.read_text().strip().split('\n')
            
            # Find warning line
            warning_line = next(line for line in lines if '"WARNING"' in line)
            entry = json.loads(warning_line)
            
            assert entry["level"] == "WARNING"
            assert entry["message"] == "Missing optional field"
            assert entry["metadata"]["field"] == "temp"
    
    def test_error_logging(self):
        """Test error() method."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            log.error("Parse failed", step="Parsing", metadata={"line": 5})
            log.finalize(success=False, error="Parse error")
            
            # Read log file
            lines = log_path.read_text().strip().split('\n')
            
            # Find error line (not the FAILED line)
            error_lines = [line for line in lines if '"ERROR"' in line]
            assert len(error_lines) == 2  # One explicit error + FAILED
            
            entry = json.loads(error_lines[0])
            assert entry["level"] == "ERROR"
            assert entry["step"] == "Parsing"
            assert entry["message"] == "Parse failed"
    
    def test_error_with_exception(self):
        """Test error() with exception object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            
            try:
                raise ValueError("Invalid value")
            except ValueError as e:
                log.error("Validation error", exception=e)
            
            log.finalize(success=False, error="Validation failed")
            
            # Read log file
            lines = log_path.read_text().strip().split('\n')
            error_line = next(line for line in lines if '"ERROR"' in line and 'Validation error' in line)
            entry = json.loads(error_line)
            
            assert entry["metadata"]["exception_type"] == "ValueError"
            assert entry["metadata"]["exception_message"] == "Invalid value"
    
    def test_finalize_success(self):
        """Test finalize() with success."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            log.step("Converting")
            log.finalize(success=True, report_id=456, metadata={"rows": 10})
            
            # Read log file
            lines = log_path.read_text().strip().split('\n')
            final_line = lines[-1]
            entry = json.loads(final_line)
            
            assert entry["level"] == "INFO"
            assert entry["step"] == "COMPLETED"
            assert entry["message"] == "Conversion successful"
            assert entry["metadata"]["success"] is True
            assert entry["metadata"]["report_id"] == 456
            assert entry["metadata"]["rows"] == 10
    
    def test_finalize_failure(self):
        """Test finalize() with failure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            log.error("Parse error")
            log.finalize(success=False, error="Invalid format")
            
            # Read log file
            lines = log_path.read_text().strip().split('\n')
            final_line = lines[-1]
            entry = json.loads(final_line)
            
            assert entry["level"] == "ERROR"
            assert entry["step"] == "FAILED"
            assert "Conversion failed" in entry["message"]
            assert entry["metadata"]["success"] is False
            assert entry["metadata"]["error"] == "Invalid format"
    
    def test_context_manager_success(self):
        """Test using ConversionLog as context manager (success)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            with ConversionLog(log_path, "test.csv") as log:
                log.step("Processing")
                log.finalize(success=True)
            
            # Log should be finalized and closed
            assert log_path.exists()
            assert log._finalized
    
    def test_context_manager_exception(self):
        """Test context manager with exception."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            try:
                with ConversionLog(log_path, "test.csv") as log:
                    log.step("Processing")
                    raise ValueError("Test error")
            except ValueError:
                pass  # Expected
            
            # Log should be finalized with error
            lines = log_path.read_text().strip().split('\n')
            final_line = lines[-1]
            entry = json.loads(final_line)
            
            assert entry["level"] == "ERROR"
            assert entry["step"] == "FAILED"
            assert "Test error" in str(entry)
    
    def test_prevents_logging_after_finalize(self):
        """Test that logging after finalize is prevented."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            log.finalize(success=True)
            
            # These should be no-ops (with warnings)
            initial_count = len(log.entries)
            log.step("Late step")
            log.warning("Late warning")
            log.error("Late error")
            
            # No new entries should be added
            assert len(log.entries) == initial_count
    
    def test_auto_flush(self):
        """Test that log entries are auto-flushed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            log.step("Step 1")
            
            # File should have content even before finalize
            # (due to auto-flush for crash safety)
            content = log_path.read_text()
            assert "Step 1" in content
            
            log.finalize(success=True)
    
    def test_json_line_format(self):
        """Test that log file uses JSON line format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "test.log"
            
            log = ConversionLog(log_path, "test.csv")
            log.step("Step 1")
            log.step("Step 2")
            log.finalize(success=True)
            
            # Each line should be valid JSON
            lines = log_path.read_text().strip().split('\n')
            for line in lines:
                entry = json.loads(line)  # Should not raise
                assert "timestamp" in entry
                assert "level" in entry
                assert "step" in entry
                assert "message" in entry
    
    def test_creates_directory_if_not_exists(self):
        """Test that log directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "logs" / "conversions" / "test.log"
            
            # Directory doesn't exist yet
            assert not log_path.parent.exists()
            
            log = ConversionLog(log_path, "test.csv")
            log.finalize(success=True)
            
            # Directory should be created
            assert log_path.parent.exists()
            assert log_path.exists()


class TestConversionLogIntegration:
    """Integration tests for ConversionLog."""
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_full_conversion_workflow(self, mock_get_dir):
        """Test complete conversion workflow with logging."""
        with tempfile.TemporaryDirectory() as tmpdir:
            conversion_dir = Path(tmpdir) / "conversions"
            conversion_dir.mkdir()
            mock_get_dir.return_value = conversion_dir
            
            # Create log for conversion
            log = ConversionLog.create_for_file("production_data.csv", "station_a")
            
            # Simulate conversion steps
            log.step("Reading file", metadata={"size_bytes": 2048})
            log.step("Parsing CSV", metadata={"rows": 25, "columns": 8})
            log.warning("Missing optional column: operator_notes")
            log.step("Validating data", metadata={"valid_rows": 24, "invalid_rows": 1})
            log.step("Creating WATS report", metadata={"serial": "SN12345"})
            log.finalize(success=True, report_id=789, metadata={"upload_time_ms": 123})
            
            # Verify log file
            log_files = list(conversion_dir.glob("production_data_*.log"))
            assert len(log_files) == 1
            
            # Verify content
            content = log_files[0].read_text()
            lines = content.strip().split('\n')
            assert len(lines) == 7  # START + 4 steps + warning + COMPLETED
            
            # Parse all entries
            entries = [json.loads(line) for line in lines]
            
            # Check START
            assert entries[0]["step"] == "START"
            assert entries[0]["message"] == "Starting conversion of production_data.csv"
            
            # Check steps
            assert entries[1]["step"] == "Reading file"
            assert entries[2]["step"] == "Parsing CSV"
            
            # Check warning
            warning_entry = next(e for e in entries if e["level"] == "WARNING")
            assert "operator_notes" in warning_entry["message"]
            
            # Check completion
            assert entries[-1]["step"] == "COMPLETED"
            assert entries[-1]["metadata"]["success"] is True
            assert entries[-1]["metadata"]["report_id"] == 789
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_failed_conversion_workflow(self, mock_get_dir):
        """Test failed conversion with error logging."""
        with tempfile.TemporaryDirectory() as tmpdir:
            conversion_dir = Path(tmpdir) / "conversions"
            conversion_dir.mkdir()
            mock_get_dir.return_value = conversion_dir
            
            log = ConversionLog.create_for_file("bad_data.csv", "station_b")
            
            log.step("Reading file")
            log.step("Parsing CSV")
            log.error("Invalid CSV format at line 5", metadata={"line": 5})
            log.finalize(success=False, error="Parse error at line 5")
            
            # Verify log file
            log_files = list(conversion_dir.glob("bad_data_*.log"))
            assert len(log_files) == 1
            
            content = log_files[0].read_text()
            lines = content.strip().split('\n')
            entries = [json.loads(line) for line in lines]
            
            # Check error entry
            error_entries = [e for e in entries if e["level"] == "ERROR"]
            assert len(error_entries) == 2  # Explicit error + FAILED
            
            # Check final entry
            assert entries[-1]["step"] == "FAILED"
            assert entries[-1]["metadata"]["success"] is False
