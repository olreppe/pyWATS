"""
Unit Tests for FolderConverter Base Class

Tests all FolderConverter functionality:
- Property configuration (patterns, marker, min files, expected files)
- Folder readiness checking (marker, file count, expected files, patterns)
- Readiness pattern matching
- Helper methods (list_files, read_marker_data, delete_marker)
- Validation (default pattern match)
- Lifecycle callbacks (on_load, on_unload, on_success, on_failure)

Author: Auto-generated for Task 1.5
Coverage Target: 80%+
"""

import pytest
from pathlib import Path
from typing import List, Optional, Dict, Any
from unittest.mock import Mock

from pywats_client.converters.folder_converter import FolderConverter
from pywats_client.converters.models import (
    ConverterType,
    ConverterSource,
    ValidationResult,
    ConverterResult,
    PostProcessAction,
    ArgumentDefinition,
)


# =============================================================================
# Test Converter Implementations
# =============================================================================

class BasicFolderConverter(FolderConverter):
    """Minimal folder converter for testing"""
    
    @property
    def name(self) -> str:
        return "Basic Folder Converter"
    
    def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
        """Simple conversion that succeeds"""
        return ConverterResult.success_result(
            report={"type": "UUT", "serialNumber": "TEST-001"},
            post_action=PostProcessAction.MOVE
        )


class CustomPatternConverter(FolderConverter):
    """Converter with custom folder patterns"""
    
    @property
    def name(self) -> str:
        return "Custom Pattern Converter"
    
    @property
    def folder_patterns(self) -> List[str]:
        return ["TEST_*", "RESULT_*"]
    
    def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
        return ConverterResult.success_result(report={"type": "UUT"})


class NoMarkerConverter(FolderConverter):
    """Converter without a readiness marker"""
    
    @property
    def name(self) -> str:
        return "No Marker Converter"
    
    @property
    def readiness_marker(self) -> Optional[str]:
        return None
    
    def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
        return ConverterResult.success_result(report={"type": "UUT"})


class MinFileCountConverter(FolderConverter):
    """Converter with minimum file count requirement"""
    
    @property
    def name(self) -> str:
        return "Min File Count Converter"
    
    @property
    def min_file_count(self) -> Optional[int]:
        return 3
    
    def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
        return ConverterResult.success_result(report={"type": "UUT"})


class ExpectedFilesConverter(FolderConverter):
    """Converter with expected file patterns"""
    
    @property
    def name(self) -> str:
        return "Expected Files Converter"
    
    @property
    def expected_files(self) -> Optional[List[str]]:
        return ["data.csv", "config.xml", "*.log"]
    
    def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
        return ConverterResult.success_result(report={"type": "UUT"})


class LifecycleTrackingConverter(FolderConverter):
    """Converter that tracks lifecycle callbacks"""
    
    def __init__(self):
        super().__init__()
        self.lifecycle_calls = []
    
    @property
    def name(self) -> str:
        return "Lifecycle Tracking Converter"
    
    def on_load(self, context: Any) -> None:
        self.lifecycle_calls.append("on_load")
    
    def on_unload(self) -> None:
        self.lifecycle_calls.append("on_unload")
    
    def on_success(self, source: ConverterSource, result: ConverterResult, context: Any) -> None:
        self.lifecycle_calls.append("on_success")
    
    def on_failure(self, source: ConverterSource, result: ConverterResult, context: Any) -> None:
        self.lifecycle_calls.append("on_failure")
    
    def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
        return ConverterResult.success_result(report={"type": "UUT"})


# =============================================================================
# Test Classes
# =============================================================================

class TestFolderConverterProperties:
    """Test FolderConverter property defaults and overrides"""
    
    def test_name_is_abstract(self):
        """Test that name property must be implemented"""
        with pytest.raises(TypeError):
            # Can't instantiate without implementing abstract methods
            class IncompleteConverter(FolderConverter):
                pass
            IncompleteConverter()
    
    def test_converter_type_is_always_folder(self):
        """Test that converter_type is always FOLDER"""
        converter = BasicFolderConverter()
        assert converter.converter_type == ConverterType.FOLDER
    
    def test_default_version(self):
        """Test default version is 1.0.0"""
        converter = BasicFolderConverter()
        assert converter.version == "1.0.0"
    
    def test_default_description(self):
        """Test default description is empty"""
        converter = BasicFolderConverter()
        assert converter.description == ""
    
    def test_default_author(self):
        """Test default author is empty"""
        converter = BasicFolderConverter()
        assert converter.author == ""
    
    def test_default_folder_patterns(self):
        """Test default folder_patterns is ['*'] (match all)"""
        converter = BasicFolderConverter()
        assert converter.folder_patterns == ["*"]
    
    def test_custom_folder_patterns(self):
        """Test custom folder_patterns override"""
        converter = CustomPatternConverter()
        assert converter.folder_patterns == ["TEST_*", "RESULT_*"]
    
    def test_default_readiness_marker(self):
        """Test default readiness_marker is 'COMPLETE.marker'"""
        converter = BasicFolderConverter()
        assert converter.readiness_marker == "COMPLETE.marker"
    
    def test_readiness_marker_can_be_none(self):
        """Test readiness_marker can be set to None"""
        converter = NoMarkerConverter()
        assert converter.readiness_marker is None
    
    def test_default_min_file_count(self):
        """Test default min_file_count is None"""
        converter = BasicFolderConverter()
        assert converter.min_file_count is None
    
    def test_custom_min_file_count(self):
        """Test custom min_file_count override"""
        converter = MinFileCountConverter()
        assert converter.min_file_count == 3
    
    def test_default_expected_files(self):
        """Test default expected_files is None"""
        converter = BasicFolderConverter()
        assert converter.expected_files is None
    
    def test_custom_expected_files(self):
        """Test custom expected_files override"""
        converter = ExpectedFilesConverter()
        assert converter.expected_files == ["data.csv", "config.xml", "*.log"]
    
    def test_default_arguments_schema(self):
        """Test default arguments_schema is empty dict"""
        converter = BasicFolderConverter()
        assert converter.arguments_schema == {}
    
    def test_default_post_action(self):
        """Test default_post_action is MOVE"""
        converter = BasicFolderConverter()
        assert converter.default_post_action == PostProcessAction.MOVE
    
    def test_default_preserve_folder_structure(self):
        """Test default preserve_folder_structure is True"""
        converter = BasicFolderConverter()
        assert converter.preserve_folder_structure is True


class TestFolderConverterReadinessMarker:
    """Test folder readiness checking with marker files"""
    
    def test_folder_ready_with_marker_file(self, tmp_path):
        """Test folder is ready when marker file exists"""
        converter = BasicFolderConverter()
        context = Mock()
        
        # Create marker file
        marker_file = tmp_path / "COMPLETE.marker"
        marker_file.touch()
        
        assert converter.is_folder_ready(tmp_path, context) is True
    
    def test_folder_not_ready_without_marker_file(self, tmp_path):
        """Test folder is not ready when marker file missing"""
        converter = BasicFolderConverter()
        context = Mock()
        
        # No marker file created
        assert converter.is_folder_ready(tmp_path, context) is False
    
    def test_folder_ready_when_no_marker_configured(self, tmp_path):
        """Test folder is ready when readiness_marker is None"""
        converter = NoMarkerConverter()
        context = Mock()
        
        # No marker file needed
        assert converter.is_folder_ready(tmp_path, context) is True
    
    def test_custom_marker_file_name(self, tmp_path):
        """Test custom marker file name"""
        class CustomMarkerConverter(FolderConverter):
            @property
            def name(self) -> str:
                return "Custom Marker"
            
            @property
            def readiness_marker(self) -> Optional[str]:
                return "_READY"
            
            def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
                return ConverterResult.success_result(report={"type": "UUT"})
        
        converter = CustomMarkerConverter()
        context = Mock()
        
        # Create custom marker
        marker_file = tmp_path / "_READY"
        marker_file.touch()
        
        assert converter.is_folder_ready(tmp_path, context) is True


class TestFolderConverterMinFileCount:
    """Test folder readiness checking with minimum file count"""
    
    def test_folder_ready_with_sufficient_files(self, tmp_path):
        """Test folder is ready when file count >= min_file_count"""
        converter = MinFileCountConverter()
        context = Mock()
        
        # Create 3 files (meets minimum)
        for i in range(3):
            (tmp_path / f"file{i}.txt").touch()
        
        # Create marker
        (tmp_path / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is True
    
    def test_folder_not_ready_with_insufficient_files(self, tmp_path):
        """Test folder is not ready when file count < min_file_count"""
        converter = MinFileCountConverter()
        context = Mock()
        
        # Create only 1 file (below minimum of 3)
        # Note: marker file counts as a file, so 1 + marker = 2 < 3
        (tmp_path / "file1.txt").touch()
        
        # With marker, we have 2 files total (still below minimum of 3)
        (tmp_path / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is False
    
    def test_folder_ready_with_extra_files(self, tmp_path):
        """Test folder is ready when file count > min_file_count"""
        converter = MinFileCountConverter()
        context = Mock()
        
        # Create 5 files (exceeds minimum of 3)
        for i in range(5):
            (tmp_path / f"file{i}.txt").touch()
        
        # Create marker
        (tmp_path / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is True
    
    def test_subdirectories_not_counted_as_files(self, tmp_path):
        """Test that subdirectories don't count toward min_file_count"""
        converter = MinFileCountConverter()
        context = Mock()
        
        # Create 1 file and 2 directories
        (tmp_path / "file1.txt").touch()
        (tmp_path / "subdir1").mkdir()
        (tmp_path / "subdir2").mkdir()
        
        # Create marker (now we have 2 files total)
        (tmp_path / "COMPLETE.marker").touch()
        
        # Only 2 files (file1.txt + marker), need 3
        assert converter.is_folder_ready(tmp_path, context) is False


class TestFolderConverterExpectedFiles:
    """Test folder readiness checking with expected file patterns"""
    
    def test_folder_ready_with_all_expected_files(self, tmp_path):
        """Test folder is ready when all expected files exist"""
        converter = ExpectedFilesConverter()
        context = Mock()
        
        # Create all expected files
        (tmp_path / "data.csv").touch()
        (tmp_path / "config.xml").touch()
        (tmp_path / "test.log").touch()  # Matches *.log
        
        # Create marker
        (tmp_path / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is True
    
    def test_folder_not_ready_with_missing_expected_file(self, tmp_path):
        """Test folder is not ready when expected file is missing"""
        converter = ExpectedFilesConverter()
        context = Mock()
        
        # Create only some expected files (missing config.xml)
        (tmp_path / "data.csv").touch()
        (tmp_path / "test.log").touch()
        
        # Create marker
        (tmp_path / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is False
    
    def test_folder_ready_with_pattern_match(self, tmp_path):
        """Test folder is ready when file matches wildcard pattern"""
        converter = ExpectedFilesConverter()
        context = Mock()
        
        # Create files including pattern match
        (tmp_path / "data.csv").touch()
        (tmp_path / "config.xml").touch()
        (tmp_path / "debug.log").touch()  # Matches *.log pattern
        
        # Create marker
        (tmp_path / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is True
    
    def test_folder_not_ready_without_pattern_match(self, tmp_path):
        """Test folder is not ready when no file matches wildcard pattern"""
        converter = ExpectedFilesConverter()
        context = Mock()
        
        # Create files but no .log file
        (tmp_path / "data.csv").touch()
        (tmp_path / "config.xml").touch()
        (tmp_path / "notes.txt").touch()  # Doesn't match *.log
        
        # Create marker
        (tmp_path / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is False


class TestFolderConverterPatternMatching:
    """Test folder pattern matching logic"""
    
    def test_wildcard_pattern_matches_all_folders(self, tmp_path):
        """Test that '*' pattern matches any folder name"""
        converter = BasicFolderConverter()
        context = Mock()
        
        # Any folder name should match
        test_folder = tmp_path / "random_folder_name"
        test_folder.mkdir()
        (test_folder / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(test_folder, context) is True
    
    def test_prefix_pattern_matches_correctly(self, tmp_path):
        """Test prefix pattern (TEST_*) matching"""
        converter = CustomPatternConverter()
        context = Mock()
        
        # Should match TEST_ prefix
        test_folder = tmp_path / "TEST_123"
        test_folder.mkdir()
        (test_folder / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(test_folder, context) is True
    
    def test_prefix_pattern_rejects_non_matching(self, tmp_path):
        """Test prefix pattern rejects non-matching folder names"""
        converter = CustomPatternConverter()
        context = Mock()
        
        # Should not match (doesn't start with TEST_ or RESULT_)
        test_folder = tmp_path / "DATA_123"
        test_folder.mkdir()
        (test_folder / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(test_folder, context) is False
    
    def test_suffix_pattern_matches_correctly(self, tmp_path):
        """Test suffix pattern (RESULT_*) matching"""
        converter = CustomPatternConverter()
        context = Mock()
        
        # Should match RESULT_ prefix
        test_folder = tmp_path / "RESULT_456"
        test_folder.mkdir()
        (test_folder / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(test_folder, context) is True
    
    def test_pattern_matching_is_case_insensitive(self, tmp_path):
        """Test pattern matching is case-insensitive"""
        converter = CustomPatternConverter()
        context = Mock()
        
        # Should match even with different case
        test_folder = tmp_path / "test_abc"
        test_folder.mkdir()
        (test_folder / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(test_folder, context) is True


class TestFolderConverterHelperMethods:
    """Test FolderConverter helper methods"""
    
    def test_list_files_non_recursive(self, tmp_path):
        """Test list_files without recursion"""
        converter = BasicFolderConverter()
        
        # Create files in root
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.csv").touch()
        
        # Create subdirectory with files
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.txt").touch()
        
        # Non-recursive should only find root files
        files = converter.list_files(tmp_path, "*.txt", recursive=False)
        assert len(files) == 1
        assert files[0].name == "file1.txt"
    
    def test_list_files_recursive(self, tmp_path):
        """Test list_files with recursion"""
        converter = BasicFolderConverter()
        
        # Create files in root
        (tmp_path / "file1.txt").touch()
        
        # Create nested subdirectories with files
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.txt").touch()
        
        nested = subdir / "nested"
        nested.mkdir()
        (nested / "file3.txt").touch()
        
        # Recursive should find all .txt files
        files = converter.list_files(tmp_path, "*.txt", recursive=True)
        assert len(files) == 3
    
    def test_list_files_with_pattern_filter(self, tmp_path):
        """Test list_files with pattern filtering"""
        converter = BasicFolderConverter()
        
        # Create various file types
        (tmp_path / "data.csv").touch()
        (tmp_path / "config.xml").touch()
        (tmp_path / "notes.txt").touch()
        (tmp_path / "debug.log").touch()
        
        # List only .csv files
        csv_files = converter.list_files(tmp_path, "*.csv", recursive=False)
        assert len(csv_files) == 1
        assert csv_files[0].name == "data.csv"
    
    def test_list_files_default_wildcard(self, tmp_path):
        """Test list_files with default wildcard pattern"""
        converter = BasicFolderConverter()
        
        # Create various files
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.csv").touch()
        (tmp_path / "file3.xml").touch()
        
        # Default pattern "*" should list all files
        files = converter.list_files(tmp_path)
        assert len(files) == 3
    
    def test_read_marker_data_returns_content(self, tmp_path):
        """Test read_marker_data returns marker file contents"""
        converter = BasicFolderConverter()
        
        # Create marker with data
        marker_file = tmp_path / "COMPLETE.marker"
        marker_file.write_text("metadata:value\ntimestamp:2026-02-13")
        
        content = converter.read_marker_data(tmp_path)
        assert content == "metadata:value\ntimestamp:2026-02-13"
    
    def test_read_marker_data_returns_none_when_missing(self, tmp_path):
        """Test read_marker_data returns None when marker doesn't exist"""
        converter = BasicFolderConverter()
        
        # No marker file created
        content = converter.read_marker_data(tmp_path)
        assert content is None
    
    def test_read_marker_data_returns_none_when_no_marker_configured(self, tmp_path):
        """Test read_marker_data returns None when readiness_marker is None"""
        converter = NoMarkerConverter()
        
        content = converter.read_marker_data(tmp_path)
        assert content is None
    
    def test_delete_marker_removes_file(self, tmp_path):
        """Test delete_marker removes the marker file"""
        converter = BasicFolderConverter()
        
        # Create marker
        marker_file = tmp_path / "COMPLETE.marker"
        marker_file.touch()
        assert marker_file.exists()
        
        # Delete marker
        result = converter.delete_marker(tmp_path)
        assert result is True
        assert not marker_file.exists()
    
    def test_delete_marker_returns_false_when_missing(self, tmp_path):
        """Test delete_marker returns False when marker doesn't exist"""
        converter = BasicFolderConverter()
        
        # No marker file
        result = converter.delete_marker(tmp_path)
        assert result is False
    
    def test_delete_marker_returns_false_when_no_marker_configured(self, tmp_path):
        """Test delete_marker returns False when readiness_marker is None"""
        converter = NoMarkerConverter()
        
        result = converter.delete_marker(tmp_path)
        assert result is False


class TestFolderConverterValidation:
    """Test FolderConverter validation logic"""
    
    def test_default_validation_returns_pattern_match(self):
        """Test default validate() returns pattern match result"""
        converter = BasicFolderConverter()
        context = Mock()
        source = Mock(spec=ConverterSource)
        
        result = converter.validate(source, context)
        
        # Default implementation returns pattern_match
        assert result.can_convert is True
        assert "pattern" in result.message.lower() or "matched" in result.message.lower()
    
    def test_validation_message_includes_converter_name(self):
        """Test validation message includes converter name"""
        converter = BasicFolderConverter()
        context = Mock()
        source = Mock(spec=ConverterSource)
        
        result = converter.validate(source, context)
        
        assert "Basic Folder Converter" in result.message


class TestFolderConverterLifecycle:
    """Test FolderConverter lifecycle callbacks"""
    
    def test_on_load_callback(self):
        """Test on_load callback is called"""
        converter = LifecycleTrackingConverter()
        context = Mock()
        
        converter.on_load(context)
        
        assert "on_load" in converter.lifecycle_calls
    
    def test_on_unload_callback(self):
        """Test on_unload callback is called"""
        converter = LifecycleTrackingConverter()
        
        converter.on_unload()
        
        assert "on_unload" in converter.lifecycle_calls
    
    def test_on_success_callback(self):
        """Test on_success callback is called"""
        converter = LifecycleTrackingConverter()
        context = Mock()
        source = Mock(spec=ConverterSource)
        result = Mock(spec=ConverterResult)
        
        converter.on_success(source, result, context)
        
        assert "on_success" in converter.lifecycle_calls
    
    def test_on_failure_callback(self):
        """Test on_failure callback is called"""
        converter = LifecycleTrackingConverter()
        context = Mock()
        source = Mock(spec=ConverterSource)
        result = Mock(spec=ConverterResult)
        
        converter.on_failure(source, result, context)
        
        assert "on_failure" in converter.lifecycle_calls
    
    def test_lifecycle_callback_order(self):
        """Test lifecycle callbacks are called in order"""
        converter = LifecycleTrackingConverter()
        context = Mock()
        source = Mock(spec=ConverterSource)
        result = Mock(spec=ConverterResult)
        
        converter.on_load(context)
        converter.on_success(source, result, context)
        converter.on_unload()
        
        assert converter.lifecycle_calls == ["on_load", "on_success", "on_unload"]


class TestFolderConverterComplexScenarios:
    """Test complex folder readiness scenarios"""
    
    def test_all_readiness_conditions_required(self, tmp_path):
        """Test folder must meet ALL readiness conditions"""
        class ComplexConverter(FolderConverter):
            @property
            def name(self) -> str:
                return "Complex Converter"
            
            @property
            def folder_patterns(self) -> List[str]:
                return ["TEST_*"]
            
            @property
            def min_file_count(self) -> Optional[int]:
                return 2
            
            @property
            def expected_files(self) -> Optional[List[str]]:
                return ["data.csv"]
            
            def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
                return ConverterResult.success_result(report={"type": "UUT"})
        
        converter = ComplexConverter()
        context = Mock()
        
        # Create folder matching pattern
        test_folder = tmp_path / "TEST_001"
        test_folder.mkdir()
        
        # Missing files - not ready
        assert converter.is_folder_ready(test_folder, context) is False
        
        # Add one file - still not enough
        (test_folder / "file1.txt").touch()
        assert converter.is_folder_ready(test_folder, context) is False
        
        # Add second file but not expected file - still not ready
        (test_folder / "file2.txt").touch()
        assert converter.is_folder_ready(test_folder, context) is False
        
        # Add expected file - still missing marker
        (test_folder / "data.csv").touch()
        assert converter.is_folder_ready(test_folder, context) is False
        
        # Add marker - now ready!
        (test_folder / "COMPLETE.marker").touch()
        assert converter.is_folder_ready(test_folder, context) is True
    
    def test_readiness_with_multiple_pattern_matches(self, tmp_path):
        """Test folder can match multiple patterns"""
        class MultiPatternConverter(FolderConverter):
            @property
            def name(self) -> str:
                return "Multi Pattern"
            
            @property
            def folder_patterns(self) -> List[str]:
                return ["TEST_*", "PROD_*", "*_RESULTS"]
            
            def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
                return ConverterResult.success_result(report={"type": "UUT"})
        
        converter = MultiPatternConverter()
        context = Mock()
        
        # Test first pattern
        folder1 = tmp_path / "TEST_123"
        folder1.mkdir()
        (folder1 / "COMPLETE.marker").touch()
        assert converter.is_folder_ready(folder1, context) is True
        
        # Test second pattern
        folder2 = tmp_path / "PROD_456"
        folder2.mkdir()
        (folder2 / "COMPLETE.marker").touch()
        assert converter.is_folder_ready(folder2, context) is True
        
        # Test third pattern
        folder3 = tmp_path / "BATCH_RESULTS"
        folder3.mkdir()
        (folder3 / "COMPLETE.marker").touch()
        assert converter.is_folder_ready(folder3, context) is True
    
    def test_empty_folder_with_only_marker(self, tmp_path):
        """Test folder with only marker file (no other files)"""
        converter = BasicFolderConverter()
        context = Mock()
        
        # Only marker file, no data files
        (tmp_path / "COMPLETE.marker").touch()
        
        # Should be ready (no min_file_count requirement)
        assert converter.is_folder_ready(tmp_path, context) is True
    
    def test_nested_folders_not_counted_in_readiness(self, tmp_path):
        """Test that nested subdirectories don't affect readiness"""
        converter = MinFileCountConverter()  # Requires 3 files
        context = Mock()
        
        # Create 3 files
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()
        (tmp_path / "file3.txt").touch()
        
        # Create nested directories (should be ignored)
        (tmp_path / "subdir1").mkdir()
        (tmp_path / "subdir2").mkdir()
        (tmp_path / "subdir1" / "subdir3").mkdir()
        
        # Create marker
        (tmp_path / "COMPLETE.marker").touch()
        
        # Should be ready (3 files, subdirs ignored)
        assert converter.is_folder_ready(tmp_path, context) is True


class TestFolderConverterEdgeCases:
    """Test FolderConverter edge cases"""
    
    def test_marker_file_in_subdirectory_not_detected(self, tmp_path):
        """Test marker file must be in root folder, not subdirectory"""
        converter = BasicFolderConverter()
        context = Mock()
        
        # Create marker in subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "COMPLETE.marker").touch()
        
        # Should not be ready (marker must be in root)
        assert converter.is_folder_ready(tmp_path, context) is False
    
    def test_expected_file_in_subdirectory_not_detected(self, tmp_path):
        """Test expected files must be in root folder"""
        converter = ExpectedFilesConverter()
        context = Mock()
        
        # Create expected files in subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "data.csv").touch()
        (subdir / "config.xml").touch()
        (subdir / "test.log").touch()
        
        # Create marker in root
        (tmp_path / "COMPLETE.marker").touch()
        
        # Should not be ready (expected files must be in root)
        assert converter.is_folder_ready(tmp_path, context) is False
    
    def test_special_characters_in_folder_name(self, tmp_path):
        """Test folder names with special characters"""
        converter = BasicFolderConverter()
        context = Mock()
        
        # Create folder with special characters
        special_folder = tmp_path / "TEST (Copy) [2024]"
        special_folder.mkdir()
        (special_folder / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(special_folder, context) is True
    
    def test_unicode_in_folder_name(self, tmp_path):
        """Test folder names with unicode characters"""
        converter = BasicFolderConverter()
        context = Mock()
        
        # Create folder with unicode
        unicode_folder = tmp_path / "TEST_Données_测试"
        unicode_folder.mkdir()
        (unicode_folder / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(unicode_folder, context) is True
    
    def test_very_long_folder_name(self, tmp_path):
        """Test folder with very long name"""
        converter = BasicFolderConverter()
        context = Mock()
        
        # Create folder with long name (200 chars)
        long_name = "TEST_" + "A" * 195
        long_folder = tmp_path / long_name
        long_folder.mkdir()
        (long_folder / "COMPLETE.marker").touch()
        
        assert converter.is_folder_ready(long_folder, context) is True
    
    def test_marker_file_with_no_extension(self, tmp_path):
        """Test marker file without extension"""
        class NoExtensionMarkerConverter(FolderConverter):
            @property
            def name(self) -> str:
                return "No Extension Marker"
            
            @property
            def readiness_marker(self) -> Optional[str]:
                return "READY"
            
            def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
                return ConverterResult.success_result(report={"type": "UUT"})
        
        converter = NoExtensionMarkerConverter()
        context = Mock()
        
        (tmp_path / "READY").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is True
    
    def test_hidden_marker_file(self, tmp_path):
        """Test hidden marker file (starts with dot)"""
        class HiddenMarkerConverter(FolderConverter):
            @property
            def name(self) -> str:
                return "Hidden Marker"
            
            @property
            def readiness_marker(self) -> Optional[str]:
                return ".ready"
            
            def convert(self, source: ConverterSource, context: Any) -> ConverterResult:
                return ConverterResult.success_result(report={"type": "UUT"})
        
        converter = HiddenMarkerConverter()
        context = Mock()
        
        (tmp_path / ".ready").touch()
        
        assert converter.is_folder_ready(tmp_path, context) is True
