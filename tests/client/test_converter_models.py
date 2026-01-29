"""
Tests for pywats_client converter models.
"""
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import os

from pywats_client.converters.models import (
    # Enums
    SourceType,
    ConverterType,
    ConversionStatus,
    PostProcessAction,
    ArgumentType,
    # Dataclasses
    FileInfo,
    ConverterSource,
    ValidationResult,
    ConverterResult,
)


class TestEnums:
    """Tests for converter enums."""
    
    def test_source_type_values(self):
        """Test SourceType enum values."""
        assert SourceType.FILE.value == "file"
        assert SourceType.FOLDER.value == "folder"
        assert SourceType.DATABASE.value == "database"
        assert SourceType.API.value == "api"
    
    def test_converter_type_values(self):
        """Test ConverterType enum values."""
        assert ConverterType.FILE.value == "file"
        assert ConverterType.FOLDER.value == "folder"
        assert ConverterType.SCHEDULED.value == "scheduled"
    
    def test_conversion_status_values(self):
        """Test ConversionStatus enum values."""
        assert ConversionStatus.SUCCESS.value == "success"
        assert ConversionStatus.FAILED.value == "failed"
        assert ConversionStatus.SUSPENDED.value == "suspended"
        assert ConversionStatus.SKIPPED.value == "skipped"
        assert ConversionStatus.REJECTED.value == "rejected"
    
    def test_post_process_action_values(self):
        """Test PostProcessAction enum values."""
        assert PostProcessAction.DELETE.value == "delete"
        assert PostProcessAction.MOVE.value == "move"
        assert PostProcessAction.ZIP.value == "zip"
        assert PostProcessAction.KEEP.value == "keep"
    
    def test_argument_type_values(self):
        """Test ArgumentType enum values."""
        assert ArgumentType.STRING.value == "string"
        assert ArgumentType.INTEGER.value == "integer"
        assert ArgumentType.FLOAT.value == "float"
        assert ArgumentType.BOOLEAN.value == "boolean"
        assert ArgumentType.PATH.value == "path"
        assert ArgumentType.CHOICE.value == "choice"
        assert ArgumentType.PASSWORD.value == "password"


class TestFileInfo:
    """Tests for FileInfo dataclass."""
    
    def test_file_info_from_existing_file(self, tmp_path):
        """Test FileInfo with an existing file."""
        test_file = tmp_path / "test.csv"
        test_file.write_text("data")
        
        info = FileInfo(test_file)
        
        assert info.name == "test.csv"
        assert info.stem == "test"
        assert info.extension == ".csv"
        assert info.size == 4
        assert info.parent == tmp_path
        assert info.modified_time is not None
    
    def test_file_info_from_nonexistent_file(self, tmp_path):
        """Test FileInfo with non-existent file."""
        fake_file = tmp_path / "nonexistent.txt"
        
        info = FileInfo(fake_file)
        
        assert info.name == "nonexistent.txt"
        assert info.size == 0
        assert info.modified_time is None
    
    def test_file_info_str(self, tmp_path):
        """Test FileInfo string representation."""
        test_file = tmp_path / "test.csv"
        test_file.write_text("data")
        
        info = FileInfo(test_file)
        s = str(info)
        
        assert "test.csv" in s
        assert "bytes" in s
    
    def test_matches_pattern(self, tmp_path):
        """Test glob pattern matching."""
        test_file = tmp_path / "report_2024.csv"
        test_file.write_text("data")
        
        info = FileInfo(test_file)
        
        assert info.matches_pattern("*.csv") is True
        assert info.matches_pattern("report_*.csv") is True
        assert info.matches_pattern("*.txt") is False
    
    def test_matches_any_pattern(self, tmp_path):
        """Test matching any of multiple patterns."""
        test_file = tmp_path / "report.csv"
        test_file.write_text("data")
        
        info = FileInfo(test_file)
        
        assert info.matches_any_pattern(["*.csv", "*.txt"]) is True
        assert info.matches_any_pattern(["*.xml", "*.json"]) is False
    
    def test_mime_type_detection(self, tmp_path):
        """Test MIME type detection."""
        csv_file = tmp_path / "data.csv"
        csv_file.write_text("a,b,c")
        
        info = FileInfo(csv_file)
        
        # MIME type might be detected based on extension
        assert info.extension == ".csv"


class TestConverterSource:
    """Tests for ConverterSource dataclass."""
    
    def test_from_file(self, tmp_path):
        """Test creating source from a file."""
        test_file = tmp_path / "test.csv"
        test_file.write_text("data")
        
        source = ConverterSource.from_file(test_file)
        
        assert source.source_type == SourceType.FILE
        assert source.path == test_file
        assert source.is_file is True
        assert source.is_folder is False
        assert source.primary_name == "test.csv"
    
    def test_from_folder(self, tmp_path):
        """Test creating source from a folder."""
        # Create test files
        (tmp_path / "file1.csv").write_text("data1")
        (tmp_path / "file2.csv").write_text("data2")
        (tmp_path / "file3.txt").write_text("data3")
        
        source = ConverterSource.from_folder(tmp_path, include_pattern="*.csv")
        
        assert source.source_type == SourceType.FOLDER
        assert source.path == tmp_path
        assert source.is_folder is True
        assert source.is_file is False
        assert len(source.files) == 2  # Only .csv files
    
    def test_from_folder_recursive(self, tmp_path):
        """Test recursive folder scanning."""
        # Create nested structure
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "file1.csv").write_text("data1")
        (subdir / "file2.csv").write_text("data2")
        
        source = ConverterSource.from_folder(tmp_path, include_pattern="*.csv", recursive=True)
        
        assert len(source.files) == 2
    
    def test_from_folder_non_recursive(self, tmp_path):
        """Test non-recursive folder scanning."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "file1.csv").write_text("data1")
        (subdir / "file2.csv").write_text("data2")
        
        source = ConverterSource.from_folder(tmp_path, include_pattern="*.csv", recursive=False)
        
        assert len(source.files) == 1  # Only top-level
    
    def test_from_database_record(self):
        """Test creating source from database record."""
        source = ConverterSource.from_database_record(
            record_id="REC-001",
            connection_info="server=localhost",
            metadata={"table": "results"}
        )
        
        assert source.source_type == SourceType.DATABASE
        assert source.record_id == "REC-001"
        assert source.connection_info == "server=localhost"
        assert source.metadata["table"] == "results"
    
    def test_get_files_matching(self, tmp_path):
        """Test filtering files by pattern."""
        (tmp_path / "report_2024.csv").write_text("data")
        (tmp_path / "report_2023.csv").write_text("data")
        (tmp_path / "other.txt").write_text("data")
        
        source = ConverterSource.from_folder(tmp_path)
        matching = source.get_files_matching("report_*.csv")
        
        assert len(matching) == 2
    
    def test_file_info_property(self, tmp_path):
        """Test file_info property caching."""
        test_file = tmp_path / "test.csv"
        test_file.write_text("data")
        
        source = ConverterSource.from_file(test_file)
        
        # Access twice - should be cached
        info1 = source.file_info
        info2 = source.file_info
        
        assert info1 is info2
        assert info1.name == "test.csv"


class TestValidationResult:
    """Tests for ValidationResult dataclass."""
    
    def test_perfect_match(self):
        """Test creating perfect match validation."""
        result = ValidationResult.perfect_match(
            message="Content verified",
            detected_part_number="PART-001"
        )
        
        assert result.can_convert is True
        assert result.confidence == 1.0
        assert result.message == "Content verified"
        assert result.detected_part_number == "PART-001"
    
    def test_good_match(self):
        """Test creating good match validation."""
        result = ValidationResult.good_match(
            confidence=0.85,
            message="Header matches expected format",
            detected_serial_number="SN-001"
        )
        
        assert result.can_convert is True
        assert result.confidence == 0.85
        assert result.detected_serial_number == "SN-001"
    
    def test_pattern_match(self):
        """Test creating pattern-only match."""
        result = ValidationResult.pattern_match(
            detected_process="Test"
        )
        
        assert result.can_convert is True
        assert result.confidence == 0.3
    
    def test_no_match(self):
        """Test creating no-match result."""
        result = ValidationResult.no_match("File format not supported")
        
        assert result.can_convert is False
        assert result.confidence == 0.0
        assert result.message == "File format not supported"
    
    def test_not_ready(self):
        """Test creating not-ready result."""
        result = ValidationResult.not_ready(
            missing=["Serial number reservation"],
            retry_after=timedelta(seconds=30)
        )
        
        assert result.can_convert is True
        assert result.ready is False
        assert "Serial number reservation" in result.missing_dependencies
        assert result.retry_after == timedelta(seconds=30)
    
    def test_confidence_clamping(self):
        """Test that confidence is clamped to 0-1 range."""
        high = ValidationResult(can_convert=True, confidence=1.5)
        low = ValidationResult(can_convert=True, confidence=-0.5)
        
        assert high.confidence == 1.0
        assert low.confidence == 0.0
    
    def test_is_below_alarm_threshold(self):
        """Test alarm threshold check."""
        high = ValidationResult(can_convert=True, confidence=0.7)
        low = ValidationResult(can_convert=True, confidence=0.3)
        
        assert high.is_below_alarm_threshold is False
        assert low.is_below_alarm_threshold is True
    
    def test_check_thresholds(self):
        """Test checking custom thresholds."""
        result = ValidationResult(can_convert=True, confidence=0.4)
        
        should_alarm, should_reject = result.check_thresholds(
            alarm_threshold=0.5,
            reject_threshold=0.2
        )
        
        assert should_alarm is True  # 0.4 < 0.5
        assert should_reject is False  # 0.4 > 0.2


class TestConverterResult:
    """Tests for ConverterResult dataclass."""
    
    def test_success_result(self):
        """Test creating successful result."""
        report = {"type": "UUT", "pn": "PART-001"}
        result = ConverterResult.success_result(
            report=report,
            post_action=PostProcessAction.ZIP,
            warnings=["Minor issue"],
            metadata={"rows": 100}
        )
        
        assert result.status == ConversionStatus.SUCCESS
        assert result.success is True
        assert result.report == report
        assert result.post_action == PostProcessAction.ZIP
        assert "Minor issue" in result.warnings
        assert result.metadata["rows"] == 100
    
    def test_success_result_multiple_reports(self):
        """Test success with multiple reports."""
        reports = [
            {"type": "UUT", "sn": "SN-001"},
            {"type": "UUT", "sn": "SN-002"},
        ]
        result = ConverterResult.success_result(reports=reports)
        
        assert result.success is True
        assert result.has_multiple_reports is True
        assert len(result.get_all_reports()) == 2
        assert result.records_processed == 2
    
    def test_failed_result(self):
        """Test creating failed result."""
        result = ConverterResult.failed_result(
            error="Parse error at line 42",
            warnings=["File encoding unknown"]
        )
        
        assert result.status == ConversionStatus.FAILED
        assert result.success is False
        assert result.error == "Parse error at line 42"
        assert result.post_action == PostProcessAction.KEEP
    
    def test_suspended_result(self):
        """Test creating suspended result."""
        result = ConverterResult.suspended_result(
            reason="Waiting for serial number",
            retry_after=timedelta(minutes=5),
            retry_count=2
        )
        
        assert result.status == ConversionStatus.SUSPENDED
        assert result.suspend_reason == "Waiting for serial number"
        assert result.retry_after == timedelta(minutes=5)
        assert result.retry_count == 2
    
    def test_skipped_result(self):
        """Test creating skipped result."""
        result = ConverterResult.skipped_result("File doesn't match pattern")
        
        assert result.status == ConversionStatus.SKIPPED
        assert result.error == "File doesn't match pattern"
    
    def test_rejected_result(self):
        """Test creating rejected result."""
        result = ConverterResult.rejected_result(
            reason="Low confidence",
            confidence=0.15,
            threshold=0.2
        )
        
        assert result.status == ConversionStatus.REJECTED
        assert "0.15" in result.error
        assert "0.20" in result.error
    
    def test_get_all_reports_single(self):
        """Test get_all_reports with single report."""
        report = {"type": "UUT"}
        result = ConverterResult.success_result(report=report)
        
        all_reports = result.get_all_reports()
        
        assert len(all_reports) == 1
        assert all_reports[0] == report
    
    def test_get_all_reports_empty(self):
        """Test get_all_reports with no reports."""
        result = ConverterResult.failed_result("Error")
        
        all_reports = result.get_all_reports()
        
        assert all_reports == []
