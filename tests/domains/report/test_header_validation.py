"""Tests for report header validation (serial number, part number).

Tests the "soft" validation that blocks problematic characters but
allows bypass via context manager or SUPPRESS: prefix.
"""
import pytest
import warnings
from datetime import datetime

from pywats.core.validation import (
    validate_serial_number,
    validate_part_number,
    validate_batch_serial_number,
    validate_report_header_field,
    find_problematic_characters,
    allow_problematic_characters,
    is_problematic_chars_allowed,
    ReportHeaderValidationError,
    ReportHeaderValidationWarning,
    PROBLEMATIC_CHARS,
    SUPPRESS_PREFIX,
)
from pywats.models import UUTReport


class TestFindProblematicCharacters:
    """Test the find_problematic_characters function."""
    
    def test_no_problematic_chars(self):
        """Normal values should return empty list."""
        assert find_problematic_characters("SN-001") == []
        assert find_problematic_characters("PART_123.rev") == []
        assert find_problematic_characters("ABCdef123") == []
    
    def test_single_problematic_char(self):
        """Single problematic character should be found."""
        assert find_problematic_characters("SN*001") == ['*']
        assert find_problematic_characters("PART/001") == ['/']
        assert find_problematic_characters("TEST?") == ['?']
    
    def test_multiple_problematic_chars(self):
        """Multiple problematic characters should all be found."""
        result = find_problematic_characters("*SN/001?")
        assert '*' in result
        assert '/' in result
        assert '?' in result
    
    def test_brackets(self):
        """Square brackets should be found."""
        result = find_problematic_characters("[A-Z]")
        assert '[' in result
        assert ']' in result
    
    def test_backslash(self):
        """Backslash should be found."""
        assert find_problematic_characters("path\\to") == ['\\']


class TestValidateReportHeaderField:
    """Test the generic field validation function."""
    
    def test_valid_values(self):
        """Valid values should pass through unchanged."""
        assert validate_report_header_field("SN-001", "sn") == "SN-001"
        assert validate_report_header_field("PART_123", "pn") == "PART_123"
        assert validate_report_header_field("v1.2.3", "rev") == "v1.2.3"
    
    def test_empty_value(self):
        """Empty values should pass through."""
        assert validate_report_header_field("", "sn") == ""
        assert validate_report_header_field(None, "sn") is None
    
    def test_problematic_char_raises_error(self):
        """Problematic characters should raise error by default."""
        with pytest.raises(ReportHeaderValidationError) as exc_info:
            validate_report_header_field("SN*001", "serial_number")
        
        assert exc_info.value.field == "serial_number"
        assert exc_info.value.value == "SN*001"
        assert '*' in exc_info.value.problematic
    
    def test_error_message_includes_bypass_options(self):
        """Error message should include bypass instructions."""
        with pytest.raises(ReportHeaderValidationError) as exc_info:
            validate_report_header_field("TEST/001", "part_number")
        
        error = exc_info.value
        assert "allow_problematic_characters()" in str(error)
        assert "SUPPRESS:" in str(error)


class TestSupressPrefixBypass:
    """Test bypassing validation with SUPPRESS: prefix."""
    
    def test_suppress_prefix_allows_problematic_chars(self):
        """SUPPRESS: prefix should allow problematic characters."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = validate_report_header_field("SUPPRESS:SN*001", "sn")
            
            # Should return value without prefix
            assert result == "SN*001"
            
            # Should issue warning
            assert len(w) == 1
            assert issubclass(w[0].category, ReportHeaderValidationWarning)
            assert "'*'" in str(w[0].message)
    
    def test_suppress_prefix_stripped(self):
        """SUPPRESS: prefix should be stripped from result."""
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            result = validate_report_header_field("SUPPRESS:PART/001", "pn")
            assert result == "PART/001"
    
    def test_suppress_prefix_no_warning_if_valid(self):
        """SUPPRESS: prefix with valid value should not warn."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = validate_report_header_field("SUPPRESS:SN-001", "sn")
            
            assert result == "SN-001"
            assert len(w) == 0  # No warning for valid chars


class TestContextManagerBypass:
    """Test bypassing validation with context manager."""
    
    def test_context_manager_allows_problematic_chars(self):
        """Context manager should allow problematic characters."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            with allow_problematic_characters():
                result = validate_serial_number("SN*001")
            
            assert result == "SN*001"
            assert len(w) == 1
            assert issubclass(w[0].category, ReportHeaderValidationWarning)
    
    def test_context_manager_scoped(self):
        """Context manager bypass should be scoped."""
        # Inside context - allowed
        with allow_problematic_characters():
            assert is_problematic_chars_allowed()
        
        # Outside context - not allowed
        assert not is_problematic_chars_allowed()
        
        # Error should be raised again
        with pytest.raises(ReportHeaderValidationError):
            validate_serial_number("SN*001")
    
    def test_nested_context_managers(self):
        """Nested context managers should work correctly."""
        with allow_problematic_characters():
            assert is_problematic_chars_allowed()
            
            with allow_problematic_characters():
                assert is_problematic_chars_allowed()
            
            # Still allowed after nested exits
            assert is_problematic_chars_allowed()
        
        # Not allowed after outer exits
        assert not is_problematic_chars_allowed()


class TestSpecificValidators:
    """Test specific field validators."""
    
    def test_validate_serial_number(self):
        """validate_serial_number should work correctly."""
        assert validate_serial_number("SN-001") == "SN-001"
        
        with pytest.raises(ReportHeaderValidationError) as exc_info:
            validate_serial_number("SN*001")
        assert exc_info.value.field == "serial_number"
    
    def test_validate_part_number(self):
        """validate_part_number should work correctly."""
        assert validate_part_number("PART-001") == "PART-001"
        
        with pytest.raises(ReportHeaderValidationError) as exc_info:
            validate_part_number("PART/001")
        assert exc_info.value.field == "part_number"
    
    def test_validate_batch_serial_number(self):
        """validate_batch_serial_number should work correctly."""
        assert validate_batch_serial_number("BATCH-001") == "BATCH-001"
        
        with pytest.raises(ReportHeaderValidationError) as exc_info:
            validate_batch_serial_number("BATCH?001")
        assert exc_info.value.field == "batch_serial_number"


class TestUUTReportIntegration:
    """Test that validation is integrated into UUTReport model."""
    
    def test_valid_report_creation(self):
        """Valid serial/part numbers should work."""
        report = UUTReport(
            pn="PART-001",
            sn="SN-12345",
            rev="A",
            process_code=10,
            station_name="TestStation",
            location="TestLab",
            purpose="Development",
        )
        assert report.pn == "PART-001"
        assert report.sn == "SN-12345"
    
    def test_problematic_serial_number_blocked(self):
        """Problematic serial number should be blocked."""
        with pytest.raises(Exception) as exc_info:  # pydantic wraps in ValidationError
            UUTReport(
                pn="PART-001",
                sn="SN*001",  # Problematic!
                rev="A",
                process_code=10,
                station_name="TestStation",
                location="TestLab",
                purpose="Development",
            )
        # Check that our validation error is in there
        assert "problematic" in str(exc_info.value).lower() or "SN*001" in str(exc_info.value)
    
    def test_problematic_part_number_blocked(self):
        """Problematic part number should be blocked."""
        with pytest.raises(Exception) as exc_info:
            UUTReport(
                pn="PART/001",  # Problematic!
                sn="SN-001",
                rev="A",
                process_code=10,
                station_name="TestStation",
                location="TestLab",
                purpose="Development",
            )
        assert "problematic" in str(exc_info.value).lower() or "PART/001" in str(exc_info.value)
    
    def test_bypass_with_context_manager(self):
        """Context manager should allow problematic chars in UUTReport."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            with allow_problematic_characters():
                report = UUTReport(
                    pn="PART/001",  # Would normally be blocked
                    sn="SN*001",    # Would normally be blocked
                    rev="A",
                    process_code=10,
                    station_name="TestStation",
                    location="TestLab",
                    purpose="Development",
                )
            
            assert report.pn == "PART/001"
            assert report.sn == "SN*001"
            # Should have warnings
            assert len(w) >= 2
    
    def test_bypass_with_suppress_prefix(self):
        """SUPPRESS: prefix should allow problematic chars in UUTReport."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            report = UUTReport(
                pn="SUPPRESS:PART/001",
                sn="SUPPRESS:SN*001",
                rev="A",
                process_code=10,
                station_name="TestStation",
                location="TestLab",
                purpose="Development",
            )
            
            # Prefix should be stripped
            assert report.pn == "PART/001"
            assert report.sn == "SN*001"
            # Should have warnings
            assert len(w) >= 2


class TestProblematicCharsConstant:
    """Test that PROBLEMATIC_CHARS covers expected characters."""
    
    def test_all_documented_chars_included(self):
        """All documented problematic characters should be in the constant."""
        documented = ['*', '%', '?', '[', ']', '^', '!', '/', '\\']
        for char in documented:
            assert char in PROBLEMATIC_CHARS, f"Missing documented char: {char}"
    
    def test_descriptions_present(self):
        """All problematic characters should have descriptions."""
        for char, desc in PROBLEMATIC_CHARS.items():
            assert desc, f"Missing description for: {char}"
            assert isinstance(desc, str)
