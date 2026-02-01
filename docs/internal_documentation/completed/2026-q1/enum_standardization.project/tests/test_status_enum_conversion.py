"""
Comprehensive tests for flexible status enum conversion.

Tests the _missing_ hook implementation for StepStatus, ReportStatus, and StatusFilter.
Verifies that all three enums accept multiple input formats while maintaining correct
serialization for the WATS API.
"""
import pytest
from pywats.domains.report.report_models.common_types import StepStatus, ReportStatus
from pywats.shared.enums import StatusFilter


class TestStepStatusConversion:
    """Test StepStatus accepts multiple formats."""
    
    def test_exact_values(self):
        """Test exact enum values work (original format)."""
        assert StepStatus("P") == StepStatus.Passed
        assert StepStatus("F") == StepStatus.Failed
        assert StepStatus("S") == StepStatus.Skipped
        assert StepStatus("D") == StepStatus.Done
        assert StepStatus("E") == StepStatus.Error
        assert StepStatus("T") == StepStatus.Terminated
    
    def test_full_names_case_insensitive(self):
        """Test full names with any case."""
        # Passed variations
        assert StepStatus("Passed") == StepStatus.Passed
        assert StepStatus("PASSED") == StepStatus.Passed
        assert StepStatus("passed") == StepStatus.Passed
        assert StepStatus("Pass") == StepStatus.Passed
        assert StepStatus("PASS") == StepStatus.Passed
        assert StepStatus("pass") == StepStatus.Passed
        
        # Failed variations
        assert StepStatus("Failed") == StepStatus.Failed
        assert StepStatus("FAILED") == StepStatus.Failed
        assert StepStatus("failed") == StepStatus.Failed
        assert StepStatus("Fail") == StepStatus.Failed
        assert StepStatus("FAIL") == StepStatus.Failed
        
        # Other statuses
        assert StepStatus("Skipped") == StepStatus.Skipped
        assert StepStatus("skipped") == StepStatus.Skipped
        assert StepStatus("Done") == StepStatus.Done
        assert StepStatus("done") == StepStatus.Done
        assert StepStatus("Error") == StepStatus.Error
        assert StepStatus("error") == StepStatus.Error
        assert StepStatus("Terminated") == StepStatus.Terminated
        assert StepStatus("terminated") == StepStatus.Terminated
    
    def test_aliases(self):
        """Test common aliases."""
        # Passed aliases
        assert StepStatus("OK") == StepStatus.Passed
        assert StepStatus("ok") == StepStatus.Passed
        assert StepStatus("success") == StepStatus.Passed
        assert StepStatus("successful") == StepStatus.Passed
        
        # Failed aliases
        assert StepStatus("failure") == StepStatus.Failed
        assert StepStatus("NG") == StepStatus.Failed
        assert StepStatus("ng") == StepStatus.Failed
        
        # Other aliases
        assert StepStatus("skip") == StepStatus.Skipped
        assert StepStatus("complete") == StepStatus.Done
        assert StepStatus("completed") == StepStatus.Done
        assert StepStatus("err") == StepStatus.Error
        assert StepStatus("abort") == StepStatus.Terminated
        assert StepStatus("aborted") == StepStatus.Terminated
        assert StepStatus("term") == StepStatus.Terminated
    
    def test_enum_members_unchanged(self):
        """Test enum member access still works."""
        assert StepStatus.Passed.value == "P"
        assert StepStatus.Failed.value == "F"
        assert StepStatus.Skipped.value == "S"
        assert StepStatus.Done.value == "D"
        assert StepStatus.Error.value == "E"
        assert StepStatus.Terminated.value == "T"
        
        # Member names
        assert StepStatus.Passed.name == "Passed"
        assert StepStatus.Failed.name == "Failed"
        
        # Member comparison
        assert StepStatus.Passed == StepStatus.Passed
        assert StepStatus.Passed != StepStatus.Failed
    
    def test_invalid_values(self):
        """Test invalid values raise clear errors."""
        with pytest.raises(ValueError, match="Invalid step status"):
            StepStatus("INVALID")
        
        with pytest.raises(ValueError, match="Invalid step status"):
            StepStatus("X")
        
        with pytest.raises(ValueError, match="must be string"):
            StepStatus(123)
        
        with pytest.raises(ValueError, match="must be string"):
            StepStatus(None)
    
    def test_properties(self):
        """Test convenience properties work."""
        # full_name property
        assert StepStatus("P").full_name == "Passed"
        assert StepStatus("OK").full_name == "Passed"
        assert StepStatus("F").full_name == "Failed"
        
        # is_passing property
        assert StepStatus.Passed.is_passing is True
        assert StepStatus.Done.is_passing is True
        assert StepStatus.Failed.is_passing is False
        assert StepStatus.Error.is_passing is False
        assert StepStatus.Skipped.is_passing is False
        
        # is_failure property
        assert StepStatus.Failed.is_failure is True
        assert StepStatus.Error.is_failure is True
        assert StepStatus.Terminated.is_failure is True
        assert StepStatus.Passed.is_failure is False
        assert StepStatus.Done.is_failure is False
    
    def test_serialization_unchanged(self):
        """Test serialization still produces single letters."""
        # All input formats serialize to single letter
        assert StepStatus("Passed").value == "P"
        assert StepStatus("PASSED").value == "P"
        assert StepStatus("OK").value == "P"
        assert StepStatus("pass").value == "P"
        
        assert StepStatus("Failed").value == "F"
        assert StepStatus("fail").value == "F"
        assert StepStatus("NG").value == "F"


class TestReportStatusConversion:
    """Test ReportStatus accepts multiple formats."""
    
    def test_exact_values(self):
        """Test exact enum values work."""
        assert ReportStatus("P") == ReportStatus.Passed
        assert ReportStatus("F") == ReportStatus.Failed
        assert ReportStatus("D") == ReportStatus.Done
        assert ReportStatus("E") == ReportStatus.Error
        assert ReportStatus("T") == ReportStatus.Terminated
    
    def test_full_names_case_insensitive(self):
        """Test full names with any case."""
        assert ReportStatus("Passed") == ReportStatus.Passed
        assert ReportStatus("PASSED") == ReportStatus.Passed
        assert ReportStatus("passed") == ReportStatus.Passed
        assert ReportStatus("Failed") == ReportStatus.Failed
        assert ReportStatus("FAILED") == ReportStatus.Failed
    
    def test_aliases(self):
        """Test common aliases work."""
        assert ReportStatus("OK") == ReportStatus.Passed
        assert ReportStatus("ok") == ReportStatus.Passed
        assert ReportStatus("Fail") == ReportStatus.Failed
        assert ReportStatus("NG") == ReportStatus.Failed
        assert ReportStatus("complete") == ReportStatus.Done
        assert ReportStatus("err") == ReportStatus.Error
        assert ReportStatus("abort") == ReportStatus.Terminated
    
    def test_no_skipped_status(self):
        """Test ReportStatus does not have Skipped (only StepStatus has it)."""
        with pytest.raises(ValueError, match="Invalid report status"):
            ReportStatus("Skipped")
        
        with pytest.raises(ValueError, match="Invalid report status"):
            ReportStatus("S")
        
        # Verify StepStatus has it
        assert StepStatus("Skipped") == StepStatus.Skipped
        assert StepStatus("S") == StepStatus.Skipped
    
    def test_properties(self):
        """Test convenience properties work."""
        assert ReportStatus("P").full_name == "Passed"
        assert ReportStatus.Passed.is_passing is True
        assert ReportStatus.Done.is_passing is True
        assert ReportStatus.Failed.is_failure is True
        assert ReportStatus.Error.is_failure is True
    
    def test_serialization_unchanged(self):
        """Test serialization produces single letters."""
        assert ReportStatus("Passed").value == "P"
        assert ReportStatus("OK").value == "P"
        assert ReportStatus("Failed").value == "F"
        assert ReportStatus("NG").value == "F"


class TestStatusFilterConversion:
    """Test StatusFilter accepts multiple formats."""
    
    def test_exact_values(self):
        """Test StatusFilter uses full words."""
        assert StatusFilter("Passed") == StatusFilter.PASSED
        assert StatusFilter("Failed") == StatusFilter.FAILED
        assert StatusFilter("Error") == StatusFilter.ERROR
        assert StatusFilter("Terminated") == StatusFilter.TERMINATED
        assert StatusFilter("Done") == StatusFilter.DONE
        assert StatusFilter("Skipped") == StatusFilter.SKIPPED
    
    def test_case_insensitive(self):
        """Test StatusFilter accepts any case."""
        assert StatusFilter("PASSED") == StatusFilter.PASSED
        assert StatusFilter("passed") == StatusFilter.PASSED
        assert StatusFilter("Pass") == StatusFilter.PASSED
        assert StatusFilter("FAILED") == StatusFilter.FAILED
        assert StatusFilter("failed") == StatusFilter.FAILED
    
    def test_aliases(self):
        """Test StatusFilter supports aliases."""
        assert StatusFilter("OK") == StatusFilter.PASSED
        assert StatusFilter("ok") == StatusFilter.PASSED
        assert StatusFilter("fail") == StatusFilter.FAILED
        assert StatusFilter("p") == StatusFilter.PASSED
        assert StatusFilter("f") == StatusFilter.FAILED
        assert StatusFilter("success") == StatusFilter.PASSED
    
    def test_uppercase_member_names(self):
        """Test StatusFilter uses UPPERCASE member names."""
        assert StatusFilter.PASSED.name == "PASSED"
        assert StatusFilter.FAILED.name == "FAILED"
        assert StatusFilter.PASSED.value == "Passed"
        assert StatusFilter.FAILED.value == "Failed"
    
    def test_properties(self):
        """Test convenience properties work."""
        assert StatusFilter.PASSED.full_name == "Passed"
        assert StatusFilter.PASSED.is_passing is True
        assert StatusFilter.DONE.is_passing is True
        assert StatusFilter.FAILED.is_failure is True
        assert StatusFilter.ERROR.is_failure is True
    
    def test_serialization_unchanged(self):
        """Test StatusFilter serializes to full words for queries."""
        assert StatusFilter("OK").value == "Passed"
        assert StatusFilter("ok").value == "Passed"
        assert StatusFilter("fail").value == "Failed"
        assert StatusFilter("p").value == "Passed"


class TestExamplePatterns:
    """Test that example code patterns work."""
    
    # These tests require full API setup - tested manually via examples
    # Just verify the enum conversions work directly
    
    def test_numeric_step_status_formats(self):
        """Test that different status formats all work for numeric steps."""
        # All these should work
        assert StepStatus("Passed") == StepStatus.Passed
        assert StepStatus("P") == StepStatus.Passed
        assert StepStatus("OK") == StepStatus.Passed
        assert StepStatus("pass") == StepStatus.Passed
        
        # All serialize to "P"
        for input_val in ["Passed", "P", "OK", "pass"]:
            assert StepStatus(input_val).value == "P"
    
    def test_mixed_status_formats(self):
        """Test that mixed formats all resolve correctly."""
        # Different formats for same status
        statuses = [
            StepStatus("Passed"),
            StepStatus("P"),
            StepStatus("OK"),
            StepStatus("pass"),
        ]
        
        # All should be equal
        for status in statuses:
            assert status == StepStatus.Passed
            assert status.value == "P"


class TestBackwardCompatibility:
    """Test that all existing code patterns still work."""
    
    def test_exact_match_still_works(self):
        """Test all existing exact-match code unchanged."""
        # These always worked, still work
        assert StepStatus("P") == StepStatus.Passed
        assert ReportStatus("P") == ReportStatus.Passed
        assert StatusFilter("Passed") == StatusFilter.PASSED
    
    def test_enum_member_values_unchanged(self):
        """Test enum serialization format unchanged."""
        assert StepStatus.Passed.value == "P"
        assert StepStatus.Failed.value == "F"
        assert ReportStatus.Passed.value == "P"
        assert StatusFilter.PASSED.value == "Passed"
    
    def test_enum_member_access_unchanged(self):
        """Test enum member access patterns unchanged."""
        # Direct member access
        status = StepStatus.Passed
        assert status.value == "P"
        
        # Member in conditionals
        if status == StepStatus.Passed:
            assert True
        else:
            assert False
        
        # Member comparison
        assert StepStatus.Passed != StepStatus.Failed
        assert ReportStatus.Passed == ReportStatus.Passed


class TestSerializationIntegration:
    """Test that serialization produces correct WATS API format."""
    
    # Integration tests require full API - verify enum serialization directly
    
    def test_stepstatus_serialization_format(self):
        """Test StepStatus always serializes to single letters."""
        # All input formats serialize to "P"
        inputs = ["Passed", "PASSED", "OK", "pass", "P"]
        for input_val in inputs:
            status = StepStatus(input_val)
            assert status.value == "P", f"Input '{input_val}' should serialize to 'P'"
        
        # Test all statuses
        assert StepStatus("Failed").value == "F"
        assert StepStatus("NG").value == "F"
        assert StepStatus("Skipped").value == "S"
        assert StepStatus("Done").value == "D"
        assert StepStatus("Error").value == "E"
        assert StepStatus("Terminated").value == "T"
    
    def test_reportstatus_serialization_format(self):
        """Test ReportStatus always serializes to single letters."""
        assert ReportStatus("Passed").value == "P"
        assert ReportStatus("OK").value == "P"
        assert ReportStatus("Failed").value == "F"
        assert ReportStatus("NG").value == "F"
        assert ReportStatus("Done").value == "D"
        assert ReportStatus("Error").value == "E"
        assert ReportStatus("Terminated").value == "T"
    
    def test_statusfilter_serialization_format(self):
        """Test StatusFilter serializes to full words for queries."""
        assert StatusFilter("OK").value == "Passed"
        assert StatusFilter("pass").value == "Passed"
        assert StatusFilter("fail").value == "Failed"
        assert StatusFilter("p").value == "Passed"
        assert StatusFilter("f").value == "Failed"


class TestErrorMessages:
    """Test that error messages are helpful."""
    
    def test_invalid_status_error_message(self):
        """Test error message lists valid options."""
        with pytest.raises(ValueError) as exc_info:
            StepStatus("INVALID_STATUS")
        
        error_msg = str(exc_info.value)
        assert "Invalid step status" in error_msg
        assert "INVALID_STATUS" in error_msg
        assert "Passed" in error_msg or "case-insensitive" in error_msg
    
    def test_wrong_type_error_message(self):
        """Test error message for non-string input."""
        with pytest.raises(ValueError) as exc_info:
            StepStatus(123)
        
        error_msg = str(exc_info.value)
        assert "must be string" in error_msg
        assert "int" in error_msg
