"""
Tests for pyWATS Client Converters (simplified for actual API)

Tests basic converter functionality with the real API structure.
"""

import pytest
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock

from pywats_client.converters.base import (
    ConverterBase, 
    ConverterResult, 
    ConverterArguments,
    ConversionStatus,
    PostProcessAction,
    FileInfo
)
from pywats_client.converters.models import ValidationResult, ConversionRecord


class TestValidationResult:
    """Tests for ValidationResult model"""
    
    def test_create_validation_result(self):
        """Test creating validation result with detected fields"""
        result = ValidationResult(
            can_convert=True,
            confidence=0.95,
            detected_part_number="PN-12345",
            detected_serial_number="SN-00001"
        )
        
        assert result.can_convert is True
        assert result.confidence == 0.95
        assert result.detected_part_number == "PN-12345"
    
    def test_validation_failed(self):
        """Test failed validation"""
        result = ValidationResult(
            can_convert=False,
            confidence=0.1
        )
        
        assert result.can_convert is False
        assert result.confidence < 0.3


class TestConversionRecord:
    """Tests for ConversionRecord model"""
    
    def test_create_conversion_record(self):
        """Test creating conversion record"""
        record = ConversionRecord(
            source_path=Path("test.csv"),
            converter_name="CSVConverter"
        )
        
        assert record.source_path == Path("test.csv")
        assert record.converter_name == "CSVConverter"
        assert record.attempts == 0
    
    def test_record_attempt(self):
        """Test recording conversion attempts"""
        record = ConversionRecord(
            source_path=Path("test.csv"),
            converter_name="CSVConverter"
        )
        
        record.record_attempt(
            status=ConversionStatus.SUCCESS,
            confidence=0.9
        )
        
        assert record.attempts == 1
        assert record.last_status == ConversionStatus.SUCCESS
        assert record.last_confidence == 0.9


class TestConverterBase:
    """Tests for ConverterBase abstract class"""
    
    def test_converter_initialization(self, temp_dir):
        """Test converter can be instantiated with required methods"""
        
        class MinimalConverter(ConverterBase):
            @property
            def name(self) -> str:
                return "Minimal"
            
            def convert_file(self, file_path: Path, args: ConverterArguments) -> ConverterResult:
                return ConverterResult.success_result(report={"type": "UUT"})
        
        converter = MinimalConverter()
        assert converter.name == "Minimal"
        assert converter.version == "1.0.0"  # default version
    
    def test_file_info_helper(self, temp_dir):
        """Test FileInfo helper class"""
        test_file = temp_dir / "test.csv"
        test_file.write_text("data")
        
        file_info = FileInfo(test_file)
        
        assert file_info.name == "test.csv"
        assert file_info.stem == "test"
        assert file_info.extension == ".csv"
        assert file_info.size > 0
    
    def test_converter_result_success(self):
        """Test creating successful converter result"""
        result = ConverterResult.success_result(
            report={"type": "UUT", "serialNumber": "TEST-001"},
            post_action=PostProcessAction.ZIP
        )
        
        assert result.status == ConversionStatus.SUCCESS
        assert result.report is not None
        assert result.post_action == PostProcessAction.ZIP
    
    def test_converter_result_failure(self):
        """Test creating failed converter result"""
        result = ConverterResult.failed_result(
            error="Parsing error"
        )
        
        assert result.status == ConversionStatus.FAILED
        assert "Parsing" in result.error
    
    def test_converter_result_suspended(self):
        """Test creating suspended converter result"""
        result = ConverterResult.suspended_result(
            reason="Waiting for dependencies"
        )
        
        assert result.status == ConversionStatus.SUSPENDED
        assert result.suspend_reason == "Waiting for dependencies"


class TestConverterWorkflow:
    """Tests for complete converter workflow"""
    
    def test_basic_conversion(self, temp_dir):
        """Test a complete file conversion workflow"""
        
        class SimpleConverter(ConverterBase):
            @property
            def name(self) -> str:
                return "Simple"
            
            def convert_file(self, file_path: Path, args: ConverterArguments) -> ConverterResult:
                content = file_path.read_text()
                
                report = {
                    "type": "UUT",
                    "serialNumber": args.file_info.stem,
                    "partNumber": "TEST-PART",
                    "result": "Passed"
                }
                
                return ConverterResult.success_result(report=report)
        
        # Create test file
        test_file = temp_dir / "UNIT-001.csv"
        test_file.write_text("test,data\n1,2")
        
        # Create converter
        converter = SimpleConverter()
        
        # Create arguments
        file_info = FileInfo(test_file)
        args = ConverterArguments(
            file_info=file_info,
            drop_folder=temp_dir,
            done_folder=temp_dir / "Done",
            error_folder=temp_dir / "Error",
            api_client=None
        )
        
        # Convert
        result = converter.convert_file(test_file, args)
        
        assert result.status == ConversionStatus.SUCCESS
        assert result.report["serialNumber"] == "UNIT-001"
