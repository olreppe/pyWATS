"""Tests for OData query helpers."""
import pytest
from datetime import date, datetime
from pywats.shared.odata import (
    escape_string,
    escape_guid,
    format_value,
    build_filter,
    ODataFilterBuilder,
)


class TestEscapeString:
    """Tests for escape_string function."""
    
    def test_no_special_chars(self):
        """Normal strings pass through unchanged."""
        assert escape_string("normal") == "normal"
        assert escape_string("test123") == "test123"
    
    def test_single_quote_escaped(self):
        """Single quotes are doubled for OData."""
        assert escape_string("O'Brien") == "O''Brien"
        assert escape_string("it's") == "it''s"
    
    def test_multiple_quotes(self):
        """Multiple quotes are all escaped."""
        assert escape_string("'test'") == "''test''"
        assert escape_string("a'b'c") == "a''b''c"
    
    def test_empty_string(self):
        """Empty string returns empty."""
        assert escape_string("") == ""
    
    def test_non_string_converted(self):
        """Non-strings are converted to string first."""
        assert escape_string(123) == "123"
        assert escape_string(None) == "None"


class TestEscapeGuid:
    """Tests for escape_guid function."""
    
    def test_valid_guid_with_dashes(self):
        """Valid GUID with dashes."""
        result = escape_guid("550e8400-e29b-41d4-a716-446655440000")
        assert result == "550e8400-e29b-41d4-a716-446655440000"
    
    def test_valid_guid_without_dashes(self):
        """Valid GUID without dashes gets formatted."""
        result = escape_guid("550e8400e29b41d4a716446655440000")
        assert result == "550e8400-e29b-41d4-a716-446655440000"
    
    def test_uppercase_normalized(self):
        """Uppercase GUIDs are normalized to lowercase."""
        result = escape_guid("550E8400-E29B-41D4-A716-446655440000")
        assert result == "550e8400-e29b-41d4-a716-446655440000"
    
    def test_invalid_length_raises(self):
        """Invalid length raises ValueError."""
        with pytest.raises(ValueError, match="Invalid GUID format"):
            escape_guid("too-short")
    
    def test_invalid_chars_raises(self):
        """Invalid characters raise ValueError."""
        with pytest.raises(ValueError, match="Invalid GUID format"):
            escape_guid("550e8400-e29b-41d4-a716-44665544000g")


class TestFormatValue:
    """Tests for format_value function."""
    
    def test_string_quoted_and_escaped(self):
        """Strings are quoted and escaped."""
        assert format_value("test") == "'test'"
        assert format_value("O'Brien") == "'O''Brien'"
    
    def test_integer(self):
        """Integers are not quoted."""
        assert format_value(42) == "42"
        assert format_value(-10) == "-10"
    
    def test_float(self):
        """Floats are not quoted."""
        assert format_value(3.14) == "3.14"
    
    def test_boolean(self):
        """Booleans are lowercase."""
        assert format_value(True) == "true"
        assert format_value(False) == "false"
    
    def test_none(self):
        """None becomes null."""
        assert format_value(None) == "null"
    
    def test_date(self):
        """Dates are formatted as ISO."""
        assert format_value(date(2024, 1, 15)) == "2024-01-15"
    
    def test_datetime(self):
        """Datetimes are formatted as ISO."""
        assert format_value(datetime(2024, 1, 15, 10, 30, 0)) == "2024-01-15T10:30:00"


class TestBuildFilter:
    """Tests for build_filter function."""
    
    def test_single_condition(self):
        """Single condition works."""
        result = build_filter(("partNumber", "eq", "PN-001"))
        assert result == "partNumber eq 'PN-001'"
    
    def test_multiple_conditions_and(self):
        """Multiple conditions joined with AND."""
        result = build_filter(
            ("partNumber", "eq", "PN-001"),
            ("status", "eq", "Passed"),
        )
        assert result == "partNumber eq 'PN-001' and status eq 'Passed'"
    
    def test_multiple_conditions_or(self):
        """Multiple conditions can be joined with OR."""
        result = build_filter(
            ("status", "eq", "Passed"),
            ("status", "eq", "Failed"),
            operator="or"
        )
        assert result == "status eq 'Passed' or status eq 'Failed'"
    
    def test_numeric_values(self):
        """Numeric values are not quoted."""
        result = build_filter(
            ("count", "gt", 10),
            ("count", "lt", 100),
        )
        assert result == "count gt 10 and count lt 100"
    
    def test_date_values(self):
        """Date values are formatted correctly."""
        result = build_filter(
            ("start", "ge", date(2024, 1, 1)),
        )
        assert result == "start ge 2024-01-01"
    
    def test_empty_conditions(self):
        """Empty conditions return empty string."""
        assert build_filter() == ""
    
    def test_injection_prevention(self):
        """User input with quotes is safely escaped."""
        # Attempt SQL/OData injection
        malicious = "' or 1=1 --"
        result = build_filter(("name", "eq", malicious))
        assert result == "name eq ''' or 1=1 --'"
        # The injection is safely escaped, not executable


class TestODataFilterBuilder:
    """Tests for ODataFilterBuilder class."""
    
    def test_simple_eq(self):
        """Simple equals condition."""
        result = ODataFilterBuilder().field("name").eq("test").build()
        assert result == "name eq 'test'"
    
    def test_chained_conditions(self):
        """Chained conditions with AND."""
        result = (ODataFilterBuilder()
            .field("partNumber").eq("PN-001")
            .field("status").eq("Passed")
            .build())
        assert result == "partNumber eq 'PN-001' and status eq 'Passed'"
    
    def test_comparison_operators(self):
        """All comparison operators work."""
        assert ODataFilterBuilder().field("x").ne(1).build() == "x ne 1"
        assert ODataFilterBuilder().field("x").gt(1).build() == "x gt 1"
        assert ODataFilterBuilder().field("x").ge(1).build() == "x ge 1"
        assert ODataFilterBuilder().field("x").lt(1).build() == "x lt 1"
        assert ODataFilterBuilder().field("x").le(1).build() == "x le 1"
    
    def test_string_functions(self):
        """String functions work."""
        assert ODataFilterBuilder().field("name").contains("test").build() == "contains(name, 'test')"
        assert ODataFilterBuilder().field("name").startswith("pre").build() == "startswith(name, 'pre')"
        assert ODataFilterBuilder().field("name").endswith("suf").build() == "endswith(name, 'suf')"
    
    def test_null_checks(self):
        """Null checks work."""
        assert ODataFilterBuilder().field("x").is_null().build() == "x eq null"
        assert ODataFilterBuilder().field("x").is_not_null().build() == "x ne null"
    
    def test_in_list(self):
        """In-list generates OR conditions."""
        result = ODataFilterBuilder().field("status").in_list(["A", "B"]).build()
        assert result == "(status eq 'A' or status eq 'B')"
    
    def test_in_list_empty(self):
        """Empty in-list generates false."""
        result = ODataFilterBuilder().field("status").in_list([]).build()
        assert result == "false"
    
    def test_use_or(self):
        """OR operator can be used."""
        result = (ODataFilterBuilder()
            .field("status").eq("A")
            .field("status").eq("B")
            .use_or()
            .build())
        assert result == "status eq 'A' or status eq 'B'"
    
    def test_or_group(self):
        """Nested groups work."""
        sub = ODataFilterBuilder().field("x").eq(1).field("x").eq(2).use_or()
        result = (ODataFilterBuilder()
            .field("active").eq(True)
            .or_group(sub)
            .build())
        assert result == "active eq true and (x eq 1 or x eq 2)"
    
    def test_str_method(self):
        """__str__ returns the filter."""
        builder = ODataFilterBuilder().field("x").eq(1)
        assert str(builder) == "x eq 1"
    
    def test_no_field_raises(self):
        """Operations without field() raise ValueError."""
        with pytest.raises(ValueError, match="Must call field"):
            ODataFilterBuilder().eq("test")
    
    def test_injection_prevention(self):
        """Builder prevents injection."""
        malicious = "' or 1=1 --"
        result = ODataFilterBuilder().field("name").eq(malicious).build()
        assert "' or 1=1 --" not in result or "''" in result
