"""Tests for path utilities.

Tests StepPath, MeasurementPath, and path normalization functions.
"""
import pytest

from pywats.shared.paths import (
    PILCROW,
    SLASH,
    normalize_path,
    display_path,
    StepPath,
    MeasurementPath,
    normalize_paths,
)


class TestConstants:
    """Tests for path constants."""
    
    def test_pilcrow_constant(self):
        """Test the pilcrow constant value."""
        assert PILCROW == "¶"
    
    def test_slash_constant(self):
        """Test the slash constant value."""
        assert SLASH == "/"


class TestNormalizePath:
    """Tests for normalize_path function."""
    
    def test_normalize_slash_path(self):
        """Test normalizing slash-separated path."""
        result = normalize_path("Main/Setup/Test")
        assert result == "Main¶Setup¶Test"
    
    def test_normalize_already_normalized(self):
        """Test that already normalized path is unchanged."""
        result = normalize_path("Main¶Setup¶Test")
        assert result == "Main¶Setup¶Test"
    
    def test_normalize_single_component(self):
        """Test normalizing single component path."""
        result = normalize_path("Main")
        assert result == "Main"
    
    def test_normalize_empty_string(self):
        """Test normalizing empty string."""
        result = normalize_path("")
        assert result == ""
    
    def test_normalize_multiple_slashes(self):
        """Test path with multiple consecutive slashes."""
        result = normalize_path("Main//Test")
        assert result == "Main¶¶Test"


class TestDisplayPath:
    """Tests for display_path function."""
    
    def test_display_pilcrow_path(self):
        """Test converting pilcrow path to display format."""
        result = display_path("Main¶Setup¶Test")
        assert result == "Main/Setup/Test"
    
    def test_display_already_display(self):
        """Test that display format path is unchanged."""
        result = display_path("Main/Setup/Test")
        assert result == "Main/Setup/Test"
    
    def test_display_empty_string(self):
        """Test displaying empty string."""
        result = display_path("")
        assert result == ""


class TestStepPath:
    """Tests for StepPath class."""
    
    def test_create_from_slash_path(self):
        """Test creating StepPath from slash path."""
        path = StepPath("Main/Setup/Initialize")
        assert str(path) == "Main¶Setup¶Initialize"
    
    def test_create_from_pilcrow_path(self):
        """Test creating StepPath from pilcrow path."""
        path = StepPath("Main¶Setup¶Initialize")
        assert str(path) == "Main¶Setup¶Initialize"
    
    def test_api_format_property(self):
        """Test api_format property returns pilcrow format."""
        path = StepPath("Main/Setup/Test")
        assert path.api_format == "Main¶Setup¶Test"
    
    def test_display_property(self):
        """Test display property returns slash format."""
        path = StepPath("Main¶Setup¶Test")
        assert path.display == "Main/Setup/Test"
    
    def test_parts_property(self):
        """Test parts property returns list of components."""
        path = StepPath("Main/Setup/Test")
        assert path.parts == ["Main", "Setup", "Test"]
    
    def test_name_property(self):
        """Test name property returns last component."""
        path = StepPath("Main/Setup/Initialize")
        assert path.name == "Initialize"
    
    def test_name_property_single(self):
        """Test name property with single component."""
        path = StepPath("Main")
        assert path.name == "Main"
    
    def test_name_property_empty(self):
        """Test name property with empty path."""
        path = StepPath("")
        assert path.name == ""
    
    def test_parent_property(self):
        """Test parent property returns parent path."""
        path = StepPath("Main/Setup/Test")
        parent = path.parent
        
        assert parent is not None
        assert parent.display == "Main/Setup"
    
    def test_parent_property_root(self):
        """Test parent property at root returns None."""
        path = StepPath("Main")
        assert path.parent is None
    
    def test_repr(self):
        """Test __repr__ method."""
        path = StepPath("Main/Setup")
        assert repr(path) == "StepPath('Main/Setup')"
    
    def test_equality_with_step_path(self):
        """Test equality comparison between StepPaths."""
        path1 = StepPath("Main/Setup")
        path2 = StepPath("Main/Setup")
        path3 = StepPath("Main/Other")
        
        assert path1 == path2
        assert path1 != path3
    
    def test_equality_with_string(self):
        """Test equality comparison with string."""
        path = StepPath("Main/Setup")
        
        # Should match both formats
        assert path == "Main¶Setup"
        assert path == "Main/Setup"
    
    def test_equality_with_other_type(self):
        """Test equality with non-comparable type."""
        path = StepPath("Main/Setup")
        assert path != 123
        assert path != None
        assert path != ["Main", "Setup"]
    
    def test_hash(self):
        """Test that StepPath is hashable."""
        path1 = StepPath("Main/Setup")
        path2 = StepPath("Main/Setup")
        
        assert hash(path1) == hash(path2)
        
        # Can be used in sets
        paths = {path1, path2}
        assert len(paths) == 1
    
    def test_truediv_operator(self):
        """Test / operator for path concatenation."""
        path = StepPath("Main") / "Setup" / "Test"
        assert path.display == "Main/Setup/Test"
    
    def test_from_parts_classmethod(self):
        """Test from_parts class method."""
        path = StepPath.from_parts("Main", "Setup", "Test")
        assert path.display == "Main/Setup/Test"
    
    def test_from_parts_single(self):
        """Test from_parts with single part."""
        path = StepPath.from_parts("Main")
        assert path.display == "Main"


class TestMeasurementPath:
    """Tests for MeasurementPath class."""
    
    def test_inherits_from_step_path(self):
        """Test that MeasurementPath inherits from StepPath."""
        assert issubclass(MeasurementPath, StepPath)
    
    def test_measurement_name_property(self):
        """Test measurement_name property."""
        path = MeasurementPath("Main/Voltage Test/Output")
        assert path.measurement_name == "Output"
    
    def test_step_path_property(self):
        """Test step_path property returns parent as StepPath."""
        path = MeasurementPath("Main/Voltage Test/Output")
        step = path.step_path
        
        assert isinstance(step, StepPath)
        assert step.display == "Main/Voltage Test"
    
    def test_step_path_single_component(self):
        """Test step_path with single component returns empty path."""
        path = MeasurementPath("Output")
        step = path.step_path
        assert step._path == ""
    
    def test_measurement_path_str(self):
        """Test string representation."""
        path = MeasurementPath("Main/Test/Measurement")
        assert str(path) == "Main¶Test¶Measurement"
    
    def test_measurement_path_display(self):
        """Test display format."""
        path = MeasurementPath("Main¶Test¶Measurement")
        assert path.display == "Main/Test/Measurement"


class TestNormalizePaths:
    """Tests for normalize_paths function."""
    
    def test_normalize_single_string(self):
        """Test normalizing single string path."""
        result = normalize_paths("Main/Test")
        assert result == "Main¶Test"
    
    def test_normalize_single_step_path(self):
        """Test normalizing single StepPath."""
        path = StepPath("Main/Test")
        result = normalize_paths(path)
        assert result == "Main¶Test"
    
    def test_normalize_list_of_strings(self):
        """Test normalizing list of string paths."""
        result = normalize_paths(["Main/Test1", "Main/Test2"])
        assert result == "Main¶Test1;Main¶Test2"
    
    def test_normalize_list_of_step_paths(self):
        """Test normalizing list of StepPaths."""
        paths = [StepPath("Main/Test1"), StepPath("Main/Test2")]
        result = normalize_paths(paths)
        assert result == "Main¶Test1;Main¶Test2"
    
    def test_normalize_mixed_list(self):
        """Test normalizing mixed list of strings and StepPaths."""
        paths = [StepPath("Main/Test1"), "Main/Test2"]
        result = normalize_paths(paths)
        assert result == "Main¶Test1;Main¶Test2"
    
    def test_normalize_empty_list(self):
        """Test normalizing empty list."""
        result = normalize_paths([])
        assert result == ""
    
    def test_normalize_single_item_list(self):
        """Test normalizing single-item list."""
        result = normalize_paths(["Main/Test"])
        assert result == "Main¶Test"


class TestPathSpecialCases:
    """Tests for special cases and edge conditions."""
    
    def test_path_with_spaces(self):
        """Test path containing spaces."""
        path = StepPath("Main Group/Setup Step/Initialize Test")
        assert path.parts == ["Main Group", "Setup Step", "Initialize Test"]
        assert path.display == "Main Group/Setup Step/Initialize Test"
    
    def test_path_with_numbers(self):
        """Test path containing numbers."""
        path = StepPath("Step1/Test2/Measurement3")
        assert path.parts == ["Step1", "Test2", "Measurement3"]
    
    def test_path_with_special_characters(self):
        """Test path with special characters (excluding separators)."""
        path = StepPath("Main_Test/Setup-1/Init.2")
        assert path.name == "Init.2"
        assert path.parts == ["Main_Test", "Setup-1", "Init.2"]
    
    def test_path_with_unicode(self):
        """Test path with Unicode characters."""
        path = StepPath("Main/测试/テスト")
        assert path.parts == ["Main", "测试", "テスト"]
        assert path.name == "テスト"
    
    def test_path_preserves_case(self):
        """Test that path preserves character case."""
        path = StepPath("MAIN/Setup/test")
        assert path.parts == ["MAIN", "Setup", "test"]
    
    def test_path_chaining_multiple(self):
        """Test chaining multiple path components."""
        path = StepPath("Root")
        path = path / "Level1" / "Level2" / "Level3" / "Leaf"
        
        assert path.parts == ["Root", "Level1", "Level2", "Level3", "Leaf"]
        assert path.name == "Leaf"
    
    def test_parent_chain(self):
        """Test navigating up through parent chain."""
        path = StepPath("A/B/C/D")
        
        assert path.parent.display == "A/B/C"
        assert path.parent.parent.display == "A/B"
        assert path.parent.parent.parent.display == "A"
        assert path.parent.parent.parent.parent is None
