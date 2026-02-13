"""
Unit Tests for FileConverter Base Class

Tests the FileConverter abstract base class and all its methods.
Uses concrete test converter implementations to test abstract functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
from typing import Dict, List

from pywats_client.converters.file_converter import FileConverter
from pywats_client.converters.models import (
    ConverterSource,
    ConverterResult,
    ValidationResult,
    ConverterType,
    PostProcessAction,
    ArgumentDefinition,
    ArgumentType,
    SourceType,
)
from pywats_client.converters.context import ConverterContext

from tests.fixtures.test_file_generators import TestFileGenerator


# ============================================================================
# Test Converter Implementations (Concrete Classes for Testing)
# ============================================================================

class SimpleCSVConverter(FileConverter):
    """Simple CSV converter for testing"""
    
    @property
    def name(self) -> str:
        return "Simple CSV Converter"
    
    @property
    def file_patterns(self) -> List[str]:
        return ["*.csv"]
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        """Simple conversion that reads CSV and returns success"""
        try:
            lines = self.read_file_lines(source.path)
            return ConverterResult.success_result(
                report={"type": "T", "pn": "TEST001", "sn": "SN001", "result": "P"},
                post_action=PostProcessAction.MOVE,
            )
        except Exception as e:
            return ConverterResult.failed_result(error=str(e))


class ValidatingXMLConverter(FileConverter):
    """XML converter with content validation"""
    
    @property
    def name(self) -> str:
        return "Validating XML Converter"
    
    @property
    def file_patterns(self) -> List[str]:
        return ["*.xml"]
    
    @property
    def arguments_schema(self) -> Dict[str, ArgumentDefinition]:
        return {
            "encoding": ArgumentDefinition(
                arg_type=ArgumentType.STRING,
                default="utf-8",
                description="File encoding",
            ),
            "validate_schema": ArgumentDefinition(
                arg_type=ArgumentType.BOOLEAN,
                default=True,
                description="Validate XML schema",
            ),
        }
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        """Check XML content for expected structure"""
        try:
            content = self.read_file_text(source.path)
            
            if "<?xml" in content and "<UUTReport" in content:
                # Perfect match - has XML declaration and UUTReport element
                return ValidationResult(
                    can_convert=True,
                    confidence=0.98,
                    message="Valid UUTReport XML",
                    detected_serial_number=self._extract_sn(content),
                )
            elif "<?xml" in content:
                # Has XML declaration but not our format
                return ValidationResult(
                    can_convert=True,
                    confidence=0.5,
                    message="XML file but not UUTReport format",
                )
            else:
                return ValidationResult.no_match("Not an XML file")
        except Exception as e:
            return ValidationResult.no_match(f"Validation error: {e}")
    
    def _extract_sn(self, content: str) -> str:
        """Extract serial number from XML content"""
        import re
        match = re.search(r'SerialNumber="([^"]+)"', content)
        return match.group(1) if match else ""
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        """Convert XML to report"""
        encoding = context.get_argument("encoding", "utf-8")
        validate_schema = context.get_argument("validate_schema", True)
        
        try:
            content = self.read_file_text(source.path, encoding=encoding)
            
            if validate_schema and "<UUTReport" not in content:
                return ConverterResult.failed_result(error="Invalid XML schema")
            
            # Simulated successful conversion
            return ConverterResult.success_result(
                report={"type": "T", "pn": "XML001", "sn": self._extract_sn(content), "result": "P"},
                post_action=PostProcessAction.DELETE,
                metadata={"encoding": encoding, "validated": validate_schema},
            )
        except Exception as e:
            return ConverterResult.failed_result(error=str(e))


class CallbackTrackerConverter(FileConverter):
    """Converter that tracks lifecycle callback invocations"""
    
    def __init__(self):
        super().__init__()
        self.load_called = False
        self.unload_called = False
        self.success_calls = []
        self.failure_calls = []
    
    @property
    def name(self) -> str:
        return "Callback Tracker"
    
    @property
    def file_patterns(self) -> List[str]:
        return ["*.txt"]
    
    def on_load(self, context: ConverterContext) -> None:
        self.load_called = True
    
    def on_unload(self) -> None:
        self.unload_called = True
    
    def on_success(self, source: ConverterSource, result: ConverterResult, context: ConverterContext) -> None:
        self.success_calls.append((source, result))
    
    def on_failure(self, source: ConverterSource, result: ConverterResult, context: ConverterContext) -> None:
        self.failure_calls.append((source, result))
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        return ConverterResult.success_result(
            report={"type": "T", "pn": "TXT001", "sn": "SN001", "result": "P"},
            post_action=PostProcessAction.KEEP,
        )


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_context():
    """Mock ConverterContext for testing"""
    context = Mock(spec=ConverterContext)
    context.get_argument = Mock(side_effect=lambda name, default=None: default)
    context.api_client = Mock()
    context.station_name = "TestStation"
    context.drop_folder = Path("/watch")
    context.done_folder = Path("/done")
    context.error_folder = Path("/error")
    return context


@pytest.fixture
def simple_csv_converter():
    """Simple CSV converter instance"""
    return SimpleCSVConverter()


@pytest.fixture
def validating_xml_converter():
    """Validating XML converter instance"""
    return ValidatingXMLConverter()


@pytest.fixture
def callback_tracker_converter():
    """Callback tracking converter instance"""
    return CallbackTrackerConverter()


# ============================================================================
# Test Pattern Matching
# ============================================================================

class TestPatternMatching:
    """Test file pattern matching functionality"""
    
    def test_matches_single_pattern(self, simple_csv_converter, temp_dir):
        """Test matching a single file pattern"""
        csv_file = temp_dir / "test.csv"
        csv_file.touch()
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=csv_file,
            files=[csv_file],
        )
        
        assert simple_csv_converter._matches_file_patterns(source)
    
    def test_no_match_wrong_extension(self, simple_csv_converter, temp_dir):
        """Test no match for wrong file extension"""
        txt_file = temp_dir / "test.txt"
        txt_file.touch()
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=txt_file,
            files=[txt_file],
        )
        
        assert not simple_csv_converter._matches_file_patterns(source)
    
    def test_matches_multiple_patterns(self, validating_xml_converter, temp_dir):
        """Test matching when multiple patterns configured"""
        xml_file = temp_dir / "report.xml"
        xml_file.touch()
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=xml_file,
            files=[xml_file],
        )
        
        assert validating_xml_converter._matches_file_patterns(source)
    
    def test_wildcard_pattern_matches_all(self, temp_dir):
        """Test wildcard pattern matches all files"""
        # Create converter with wildcard pattern
        class WildcardConverter(FileConverter):
            @property
            def name(self) -> str:
                return "Wildcard"
            
            @property
            def file_patterns(self) -> List[str]:
                return ["*"]
            
            def convert(self, source, context):
                return ConverterResult.success_result(report={"type": "T", "pn": "TEST", "sn": "SN001", "result": "P"})
        
        converter = WildcardConverter()
        csv_file = temp_dir / "test.csv"
        csv_file.touch()
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=csv_file,
            files=[csv_file],
        )
        
        assert converter._matches_file_patterns(source)
    
    def test_case_insensitive_matching(self, simple_csv_converter, temp_dir):
        """Test pattern matching is case-insensitive"""
        csv_file = temp_dir / "TEST.CSV"
        csv_file.touch()
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=csv_file,
            files=[csv_file],
        )
        
        assert simple_csv_converter._matches_file_patterns(source)


# ============================================================================
# Test Validation
# ============================================================================

class TestValidation:
    """Test validation functionality"""
    
    def test_default_validation_pattern_match(self, simple_csv_converter, mock_context, temp_dir):
        """Test default validation returns pattern match for matching files"""
        csv_file = temp_dir / "test.csv"
        csv_file.touch()
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=csv_file,
            files=[csv_file],
        )
        
        result = simple_csv_converter.validate(source, mock_context)
        
        assert result.can_convert
        assert 0.3 <= result.confidence <= 0.6  # Pattern match range
        assert "pattern" in result.message.lower()
    
    def test_default_validation_no_match(self, simple_csv_converter, mock_context, temp_dir):
        """Test default validation returns no match for non-matching files"""
        txt_file = temp_dir / "test.txt"
        txt_file.touch()
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=txt_file,
            files=[txt_file],
        )
        
        result = simple_csv_converter.validate(source, mock_context)
        
        assert not result.can_convert
        assert result.confidence == 0.0
    
    def test_content_validation_perfect_match(self, validating_xml_converter, mock_context, temp_dir):
        """Test content-based validation returns perfect match"""
        # Generate XML file with proper structure
        xml_file = TestFileGenerator.generate_xml_file(
            output_path=temp_dir / "report.xml",
            serial_number="SN123456",
        )
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=xml_file,
            files=[xml_file],
        )
        
        result = validating_xml_converter.validate(source, mock_context)
        
        assert result.can_convert
        assert result.confidence >= 0.9  # High confidence
        assert result.detected_serial_number == "SN123456"
    
    def test_content_validation_partial_match(self, validating_xml_converter, mock_context, temp_dir):
        """Test content validation with partial match (XML but wrong format)"""
        # Create XML file without UUTReport element
        xml_file = temp_dir / "other.xml"
        xml_file.write_text('<?xml version="1.0"?><OtherReport></OtherReport>')
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=xml_file,
            files=[xml_file],
        )
        
        result = validating_xml_converter.validate(source, mock_context)
        
        assert result.can_convert
        assert 0.4 <= result.confidence <= 0.6  # Medium confidence
    
    def test_validation_handles_unreadable_file(self, validating_xml_converter, mock_context, temp_dir):
        """Test validation handles unreadable files gracefully"""
        missing_file = temp_dir / "missing.xml"
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=missing_file,
            files=[missing_file],
        )
        
        result = validating_xml_converter.validate(source, mock_context)
        
        assert not result.can_convert
        assert result.confidence == 0.0
        assert "error" in result.message.lower()


# ============================================================================
# Test Conversion
# ============================================================================

class TestConversion:
    """Test conversion functionality"""
    
    def test_successful_conversion(self, simple_csv_converter, mock_context, temp_dir):
        """Test successful file conversion"""
        # Generate CSV file
        csv_file = TestFileGenerator.generate_csv_file(
            output_path=temp_dir / "test.csv",
            rows=10,
        )
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=csv_file,
            files=[csv_file],
        )
        
        result = simple_csv_converter.convert(source, mock_context)
        
        assert result.success
        assert result.report is not None
        assert result.post_action == PostProcessAction.MOVE
    
    def test_conversion_with_arguments(self, validating_xml_converter, mock_context, temp_dir):
        """Test conversion uses context arguments"""
        # Set up mock context to return specific arguments
        mock_context.get_argument = Mock(side_effect=lambda name, default: {
            "encoding": "utf-8",
            "validate_schema": True,
        }.get(name, default))
        
        # Generate XML file
        xml_file = TestFileGenerator.generate_xml_file(
            output_path=temp_dir / "report.xml",
        )
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=xml_file,
            files=[xml_file],
        )
        
        result = validating_xml_converter.convert(source, mock_context)
        
        assert result.success
        assert result.metadata["encoding"] == "utf-8"
        assert result.metadata["validated"] is True
        
        # Verify arguments were requested
        assert mock_context.get_argument.called
    
    def test_failed_conversion(self, validating_xml_converter, mock_context, temp_dir):
        """Test failed conversion returns failure result"""
        # Create invalid XML content (no UUTReport element)
        xml_file = temp_dir / "invalid.xml"
        xml_file.write_text('<?xml version="1.0"?><Invalid></Invalid>')
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=xml_file,
            files=[xml_file],
        )
        
        result = validating_xml_converter.convert(source, mock_context)
        
        assert not result.success
        assert "schema" in result.error.lower()
    
    def test_conversion_missing_file(self, simple_csv_converter, mock_context, temp_dir):
        """Test conversion handles missing files"""
        missing_file = temp_dir / "missing.csv"
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=missing_file,
            files=[missing_file],
        )
        
        result = simple_csv_converter.convert(source, mock_context)
        
        assert not result.success
        assert result.error is not None


# ============================================================================
# Test Helper Methods
# ============================================================================

class TestHelperMethods:
    """Test file reading helper methods"""
    
    def test_read_file_text(self, simple_csv_converter, temp_dir):
        """Test read_file_text helper"""
        test_file = temp_dir / "test.txt"
        test_content = "Hello\nWorld\n"
        test_file.write_text(test_content, encoding="utf-8")
        
        content = simple_csv_converter.read_file_text(test_file)
        
        assert content == test_content
    
    def test_read_file_text_with_encoding(self, simple_csv_converter, temp_dir):
        """Test read_file_text with custom encoding"""
        test_file = temp_dir / "test.txt"
        test_content = "Special characters: ñ é ü"
        test_file.write_text(test_content, encoding="utf-8")
        
        content = simple_csv_converter.read_file_text(test_file, encoding="utf-8")
        
        assert content == test_content
    
    def test_read_file_lines(self, simple_csv_converter, temp_dir):
        """Test read_file_lines helper"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3\n")
        
        lines = simple_csv_converter.read_file_lines(test_file)
        
        assert len(lines) == 3
        assert lines[0] == "Line 1"
        assert lines[1] == "Line 2"
        assert lines[2] == "Line 3"
    
    def test_read_file_lines_no_strip(self, simple_csv_converter, temp_dir):
        """Test read_file_lines without stripping"""
        test_file = temp_dir / "test.txt"
        test_file.write_text("  Line 1  \n  Line 2  \n")
        
        lines = simple_csv_converter.read_file_lines(test_file, strip=False)
        
        assert lines[0] == "  Line 1  \n"
        assert lines[1] == "  Line 2  \n"
    
    def test_read_file_bytes(self, simple_csv_converter, temp_dir):
        """Test read_file_bytes helper"""
        test_file = temp_dir / "test.bin"
        test_bytes = b'\x00\x01\x02\x03\xFF'
        test_file.write_bytes(test_bytes)
        
        content = simple_csv_converter.read_file_bytes(test_file)
        
        assert content == test_bytes


# ============================================================================
# Test Lifecycle Callbacks
# ============================================================================

class TestLifecycleCallbacks:
    """Test converter lifecycle callbacks"""
    
    def test_on_load_called(self, callback_tracker_converter, mock_context):
        """Test on_load callback is invoked"""
        callback_tracker_converter.on_load(mock_context)
        
        assert callback_tracker_converter.load_called
    
    def test_on_unload_called(self, callback_tracker_converter):
        """Test on_unload callback is invoked"""
        callback_tracker_converter.on_unload()
        
        assert callback_tracker_converter.unload_called
    
    def test_on_success_called(self, callback_tracker_converter, mock_context, temp_dir):
        """Test on_success callback is invoked"""
        txt_file = temp_dir / "test.txt"
        txt_file.write_text("test")
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=txt_file,
            files=[txt_file],
        )
        
        result = ConverterResult.success_result(
            report={"type": "T", "pn": "TEST", "sn": "SN001", "result": "P"},
        )
        
        callback_tracker_converter.on_success(source, result, mock_context)
        
        assert len(callback_tracker_converter.success_calls) == 1
        assert callback_tracker_converter.success_calls[0][0] == source
        assert callback_tracker_converter.success_calls[0][1] == result
    
    def test_on_failure_called(self, callback_tracker_converter, mock_context, temp_dir):
        """Test on_failure callback is invoked"""
        txt_file = temp_dir / "test.txt"
        txt_file.write_text("test")
        
        source = ConverterSource(
            source_type=SourceType.FILE,
            path=txt_file,
            files=[txt_file],
        )
        
        result = ConverterResult.failed_result(error="Test error")
        
        callback_tracker_converter.on_failure(source, result, mock_context)
        
        assert len(callback_tracker_converter.failure_calls) == 1
        assert callback_tracker_converter.failure_calls[0][0] == source
        assert callback_tracker_converter.failure_calls[0][1] == result


# ============================================================================
# Test Properties and Configuration
# ============================================================================

class TestPropertiesAndConfiguration:
    """Test converter properties and configuration"""
    
    def test_converter_type_is_file(self, simple_csv_converter):
        """Test converter_type property returns FILE"""
        assert simple_csv_converter.converter_type == ConverterType.FILE
    
    def test_default_version(self, simple_csv_converter):
        """Test default version property"""
        assert simple_csv_converter.version == "1.0.0"
    
    def test_arguments_schema(self, validating_xml_converter):
        """Test arguments_schema property"""
        schema = validating_xml_converter.arguments_schema
        
        assert "encoding" in schema
        assert "validate_schema" in schema
        assert schema["encoding"].arg_type == ArgumentType.STRING
        assert schema["validate_schema"].arg_type == ArgumentType.BOOLEAN
    
    def test_default_post_action(self, simple_csv_converter):
        """Test default_post_action property"""
        assert simple_csv_converter.default_post_action == PostProcessAction.MOVE
    
    def test_file_patterns_property(self, simple_csv_converter):
        """Test file_patterns property"""
        patterns = simple_csv_converter.file_patterns
        
        assert isinstance(patterns, list)
        assert "*.csv" in patterns
    
    def test_sandbox_properties(self, simple_csv_converter):
        """Test sandbox configuration properties"""
        # Default values
        assert simple_csv_converter.source_path is None
        assert simple_csv_converter.trusted_mode is False
        
        # Set values
        test_path = Path("/test/converter.py")
        simple_csv_converter.source_path = test_path
        simple_csv_converter.trusted_mode = True
        
        assert simple_csv_converter.source_path == test_path
        assert simple_csv_converter.trusted_mode is True


# ============================================================================
# Test Post-Processing Actions
# ============================================================================

class TestPostProcessingActions:
    """Test different post-processing action returns"""
    
    def test_returns_move_action(self, simple_csv_converter, mock_context, temp_dir):
        """Test converter can return MOVE post-action"""
        csv_file = TestFileGenerator.generate_csv_file(temp_dir / "test.csv", rows=5)
        
        source = ConverterSource(source_type=SourceType.FILE, path=csv_file, files=[csv_file])
        result = simple_csv_converter.convert(source, mock_context)
        
        assert result.post_action == PostProcessAction.MOVE
    
    def test_returns_delete_action(self, validating_xml_converter, mock_context, temp_dir):
        """Test converter can return DELETE post-action"""
        xml_file = TestFileGenerator.generate_xml_file(temp_dir / "report.xml")
        
        source = ConverterSource(source_type=SourceType.FILE, path=xml_file, files=[xml_file])
        result = validating_xml_converter.convert(source, mock_context)
        
        assert result.post_action == PostProcessAction.DELETE
    
    def test_returns_keep_action(self, callback_tracker_converter, mock_context, temp_dir):
        """Test converter can return KEEP post-action"""
        txt_file = temp_dir / "test.txt"
        txt_file.write_text("test content")
        
        source = ConverterSource(source_type=SourceType.FILE, path=txt_file, files=[txt_file])
        result = callback_tracker_converter.convert(source, mock_context)
        
        assert result.post_action == PostProcessAction.KEEP


# ============================================================================
# Test Error Handling
# ============================================================================

class TestErrorHandling:
    """Test error handling in various scenarios"""
    
    def test_handles_read_permission_error(self, simple_csv_converter, mock_context, temp_dir):
        """Test converter handles file permission errors"""
        csv_file = temp_dir / "readonly.csv"
        csv_file.touch()
        
        # Mock read_file_lines to raise PermissionError
        with patch.object(simple_csv_converter, 'read_file_lines', side_effect=PermissionError("Access denied")):
            source = ConverterSource(source_type=SourceType.FILE, path=csv_file, files=[csv_file])
            result = simple_csv_converter.convert(source, mock_context)
            
            assert not result.success
            assert "denied" in result.error.lower() or "permission" in result.error.lower()
    
    def test_handles_encoding_error(self, validating_xml_converter, mock_context, temp_dir):
        """Test converter handles encoding errors"""
        xml_file = temp_dir / "bad_encoding.xml"
        xml_file.write_bytes(b'\xFF\xFE Invalid UTF-8 \x80\x81')
        
        # Should handle gracefully with errors='replace' parameter
        result = validating_xml_converter.validate(ConverterSource(
            source_type=SourceType.FILE, path=xml_file, files=[xml_file]
        ), mock_context)
        
        # Should not crash, even if it doesn't match
        assert result is not None
    
    def test_validates_with_corrupted_file(self, validating_xml_converter, mock_context, temp_dir):
        """Test validation handles corrupted files"""
        # Create corrupted XML (missing closing tags)
        xml_file = TestFileGenerator.generate_xml_file(
            output_path=temp_dir / "corrupted.xml",
            malformed=True,
        )
        
        source = ConverterSource(source_type=SourceType.FILE, path=xml_file, files=[xml_file])
        result = validating_xml_converter.validate(source, mock_context)
        
        # Should return some result without crashing
        assert result is not None


# ============================================================================
# Test Integration with Test File Generators
# ============================================================================

class TestWithGeneratedFiles:
    """Test converter with files from test generators"""
    
    def test_converts_generated_csv_file(self, simple_csv_converter, mock_context, temp_dir):
        """Test conversion of generated CSV file"""
        csv_file = TestFileGenerator.generate_csv_file(
            output_path=temp_dir / "generated.csv",
            rows=100,
        )
        
        source = ConverterSource(source_type=SourceType.FILE, path=csv_file, files=[csv_file])
        result = simple_csv_converter.convert(source, mock_context)
        
        assert result.success
    
    def test_validates_generated_xml_file(self, validating_xml_converter, mock_context, temp_dir):
        """Test validation of generated XML file"""
        xml_file = TestFileGenerator.generate_xml_file(
            output_path=temp_dir / "generated.xml",
        )
        
        source = ConverterSource(source_type=SourceType.FILE, path=xml_file, files=[xml_file])
        result = validating_xml_converter.validate(source, mock_context)
        
        assert result.can_convert
        assert result.confidence > 0.9  # High confidence for valid XML
    
    def test_handles_batch_generated_files(self, simple_csv_converter, mock_context, temp_dir):
        """Test handling batch of generated files"""
        files = TestFileGenerator.generate_batch(
            output_dir=temp_dir,
            file_type='csv',
            count=10,
            rows=20,
        )
        
        success_count = 0
        for file in files:
            source = ConverterSource(source_type=SourceType.FILE, path=file, files=[file])
            result = simple_csv_converter.convert(source, mock_context)
            if result.success:
                success_count += 1
        
        assert success_count == 10  # All should succeed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
