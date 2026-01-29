"""Tests for discovery utilities.

Tests the LLM/Agent-friendly API discovery functions.
"""
import pytest
from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

from pywats.shared.discovery import (
    get_model_fields,
    get_required_fields,
    get_optional_fields,
    get_enum_values,
    get_enum_names,
    get_method_signature,
    list_service_methods,
    get_filter_field_categories,
    get_valid_status_values,
    get_valid_date_groupings,
    get_valid_dimensions,
    _format_type,
)


# Test fixtures - sample models and enums for testing
class SampleEnum(Enum):
    """Sample enum for testing."""
    ACTIVE = 1
    INACTIVE = 0
    PENDING = 2


class SampleModel(BaseModel):
    """Sample Pydantic model for testing."""
    required_field: str
    optional_field: Optional[str] = None
    field_with_default: str = "default"
    field_with_alias: str = Field(default="aliased", serialization_alias="fieldAlias")
    field_with_description: str = Field(default="", description="A helpful description")


class NestedModel(BaseModel):
    """Model with nested types."""
    items: List[str] = []
    metadata: Dict[str, int] = {}
    nested: Optional[SampleModel] = None


class SampleService:
    """Sample service class for method testing."""
    
    def __init__(self):
        """Initialize the service."""
        pass
    
    def get_item(self, item_id: str) -> SampleModel:
        """Get an item by ID."""
        pass
    
    def create_item(self, name: str, value: int = 0, tags: Optional[List[str]] = None) -> SampleModel:
        """Create a new item with the given name."""
        pass
    
    def _private_method(self):
        """This should not appear in listings."""
        pass
    
    def method_without_doc(self):
        pass


class TestGetModelFields:
    """Tests for get_model_fields function."""
    
    def test_returns_all_fields(self):
        """Test that all fields are returned."""
        fields = get_model_fields(SampleModel)
        
        assert "required_field" in fields
        assert "optional_field" in fields
        assert "field_with_default" in fields
        assert "field_with_alias" in fields
        assert "field_with_description" in fields
    
    def test_identifies_required_fields(self):
        """Test that required flag is set correctly."""
        fields = get_model_fields(SampleModel)
        
        assert fields["required_field"]["required"] is True
        assert fields["optional_field"]["required"] is False
        assert fields["field_with_default"]["required"] is False
    
    def test_captures_default_values(self):
        """Test that default values are captured."""
        fields = get_model_fields(SampleModel)
        
        assert fields["optional_field"]["default"] is None
        assert fields["field_with_default"]["default"] == "default"
    
    def test_captures_aliases(self):
        """Test that serialization aliases are captured."""
        fields = get_model_fields(SampleModel)
        
        assert fields["field_with_alias"]["alias"] == "fieldAlias"
    
    def test_captures_descriptions(self):
        """Test that field descriptions are captured."""
        fields = get_model_fields(SampleModel)
        
        assert fields["field_with_description"]["description"] == "A helpful description"
    
    def test_formats_types(self):
        """Test that types are formatted as strings."""
        fields = get_model_fields(SampleModel)
        
        assert fields["required_field"]["type"] == "str"
        assert "Optional" in fields["optional_field"]["type"]
    
    def test_nested_model_types(self):
        """Test handling of nested/generic types."""
        fields = get_model_fields(NestedModel)
        
        assert "List" in fields["items"]["type"]
        assert "Dict" in fields["metadata"]["type"]


class TestGetRequiredFields:
    """Tests for get_required_fields function."""
    
    def test_returns_only_required(self):
        """Test that only required fields are returned."""
        required = get_required_fields(SampleModel)
        
        assert "required_field" in required
        assert "optional_field" not in required
        assert "field_with_default" not in required
    
    def test_returns_list(self):
        """Test that result is a list."""
        required = get_required_fields(SampleModel)
        assert isinstance(required, list)


class TestGetOptionalFields:
    """Tests for get_optional_fields function."""
    
    def test_returns_only_optional(self):
        """Test that only optional fields are returned."""
        optional = get_optional_fields(SampleModel)
        
        assert "required_field" not in optional
        assert "optional_field" in optional
        assert "field_with_default" in optional
    
    def test_returns_list(self):
        """Test that result is a list."""
        optional = get_optional_fields(SampleModel)
        assert isinstance(optional, list)


class TestGetEnumValues:
    """Tests for get_enum_values function."""
    
    def test_returns_all_values(self):
        """Test that all enum values are returned."""
        values = get_enum_values(SampleEnum)
        
        assert values["ACTIVE"] == 1
        assert values["INACTIVE"] == 0
        assert values["PENDING"] == 2
    
    def test_returns_dict(self):
        """Test that result is a dictionary."""
        values = get_enum_values(SampleEnum)
        assert isinstance(values, dict)


class TestGetEnumNames:
    """Tests for get_enum_names function."""
    
    def test_returns_all_names(self):
        """Test that all enum names are returned."""
        names = get_enum_names(SampleEnum)
        
        assert "ACTIVE" in names
        assert "INACTIVE" in names
        assert "PENDING" in names
    
    def test_returns_list(self):
        """Test that result is a list."""
        names = get_enum_names(SampleEnum)
        assert isinstance(names, list)


class TestGetMethodSignature:
    """Tests for get_method_signature function."""
    
    def test_captures_parameters(self):
        """Test that method parameters are captured."""
        sig = get_method_signature(SampleService.create_item)
        
        assert "name" in sig["parameters"]
        assert "value" in sig["parameters"]
        assert "tags" in sig["parameters"]
    
    def test_excludes_self(self):
        """Test that 'self' parameter is excluded."""
        sig = get_method_signature(SampleService.get_item)
        
        assert "self" not in sig["parameters"]
    
    def test_identifies_required_params(self):
        """Test that required parameters are identified."""
        sig = get_method_signature(SampleService.create_item)
        
        assert sig["parameters"]["name"]["required"] is True
        assert sig["parameters"]["value"]["required"] is False
    
    def test_captures_default_values(self):
        """Test that default values are captured."""
        sig = get_method_signature(SampleService.create_item)
        
        assert sig["parameters"]["value"]["default"] == 0
    
    def test_captures_return_type(self):
        """Test that return type is captured."""
        sig = get_method_signature(SampleService.get_item)
        
        assert sig["return_type"] == "SampleModel"
    
    def test_captures_docstring(self):
        """Test that docstring is captured."""
        sig = get_method_signature(SampleService.create_item)
        
        assert "Create a new item" in sig["docstring"]


class TestListServiceMethods:
    """Tests for list_service_methods function."""
    
    def test_lists_public_methods(self):
        """Test that public methods are listed."""
        methods = list_service_methods(SampleService)
        
        assert "get_item" in methods
        assert "create_item" in methods
    
    def test_excludes_private_methods(self):
        """Test that private methods are excluded."""
        methods = list_service_methods(SampleService)
        
        assert "_private_method" not in methods
        assert "__init__" not in methods
    
    def test_returns_docstring_first_line(self):
        """Test that first line of docstring is returned."""
        methods = list_service_methods(SampleService)
        
        assert methods["get_item"] == "Get an item by ID."
        assert methods["create_item"] == "Create a new item with the given name."
    
    def test_handles_missing_docstring(self):
        """Test handling of methods without docstring."""
        methods = list_service_methods(SampleService)
        
        assert methods["method_without_doc"] == ""


class TestGetFilterFieldCategories:
    """Tests for get_filter_field_categories function."""
    
    def test_returns_expected_categories(self):
        """Test that expected categories are returned."""
        categories = get_filter_field_categories()
        
        assert "identity" in categories
        assert "location" in categories
        assert "status" in categories
        assert "date_range" in categories
    
    def test_identity_fields(self):
        """Test identity category contains expected fields."""
        categories = get_filter_field_categories()
        
        assert "serial_number" in categories["identity"]
        assert "part_number" in categories["identity"]
    
    def test_date_range_fields(self):
        """Test date_range category contains expected fields."""
        categories = get_filter_field_categories()
        
        assert "date_from" in categories["date_range"]
        assert "date_to" in categories["date_range"]


class TestGetValidStatusValues:
    """Tests for get_valid_status_values function."""
    
    def test_returns_all_statuses(self):
        """Test that all status values are returned."""
        statuses = get_valid_status_values()
        
        assert "Passed" in statuses
        assert "Failed" in statuses
        assert "Error" in statuses
    
    def test_returns_list(self):
        """Test that result is a list."""
        statuses = get_valid_status_values()
        assert isinstance(statuses, list)


class TestGetValidDateGroupings:
    """Tests for get_valid_date_groupings function."""
    
    def test_returns_all_groupings(self):
        """Test that all date groupings are returned."""
        groupings = get_valid_date_groupings()
        
        assert "HOUR" in groupings
        assert "DAY" in groupings
        assert "WEEK" in groupings
        assert "MONTH" in groupings
        assert "QUARTER" in groupings
        assert "YEAR" in groupings
    
    def test_returns_list(self):
        """Test that result is a list."""
        groupings = get_valid_date_groupings()
        assert isinstance(groupings, list)


class TestGetValidDimensions:
    """Tests for get_valid_dimensions function."""
    
    def test_returns_common_dimensions(self):
        """Test that common dimensions are returned."""
        dimensions = get_valid_dimensions()
        
        assert "partNumber" in dimensions
        assert "revision" in dimensions
        assert "stationName" in dimensions
    
    def test_returns_misc_dimensions(self):
        """Test that misc info dimensions are returned."""
        dimensions = get_valid_dimensions()
        
        assert "miscInfoDescription" in dimensions
        assert "miscInfoString" in dimensions
    
    def test_returns_repair_dimensions(self):
        """Test that repair-specific dimensions are returned."""
        dimensions = get_valid_dimensions()
        
        assert "repairOperation" in dimensions
        assert "repairCode" in dimensions
    
    def test_returns_list(self):
        """Test that result is a list."""
        dimensions = get_valid_dimensions()
        assert isinstance(dimensions, list)


class TestFormatType:
    """Tests for _format_type helper function."""
    
    def test_format_none(self):
        """Test formatting None type."""
        result = _format_type(None)
        assert result == "None"
    
    def test_format_string_annotation(self):
        """Test formatting string type annotation."""
        result = _format_type("CustomType")
        assert result == "CustomType"
    
    def test_format_simple_type(self):
        """Test formatting simple types."""
        assert _format_type(str) == "str"
        assert _format_type(int) == "int"
        assert _format_type(float) == "float"
        assert _format_type(bool) == "bool"
    
    def test_format_optional(self):
        """Test formatting Optional type."""
        result = _format_type(Optional[str])
        assert result == "Optional[str]"
    
    def test_format_list(self):
        """Test formatting List type."""
        result = _format_type(List[str])
        assert result == "List[str]"
    
    def test_format_dict(self):
        """Test formatting Dict type."""
        result = _format_type(Dict[str, int])
        assert result == "Dict[str, int]"
    
    def test_format_nested_generic(self):
        """Test formatting nested generic types."""
        result = _format_type(List[Optional[str]])
        assert "List" in result
        assert "Optional" in result
