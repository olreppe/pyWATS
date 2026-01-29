"""Tests for the Result types (Success, Failure).

Tests the structured result types used for LLM/Agent-friendly error handling.
"""
import pytest
from pywats.shared.result import (
    Success,
    Failure,
    ErrorCode,
    failure_from_exception,
)


class TestErrorCode:
    """Tests for the ErrorCode enum."""
    
    def test_validation_errors_exist(self):
        """Test that validation error codes exist."""
        assert ErrorCode.INVALID_INPUT == "INVALID_INPUT"
        assert ErrorCode.MISSING_REQUIRED_FIELD == "MISSING_REQUIRED_FIELD"
        assert ErrorCode.INVALID_FORMAT == "INVALID_FORMAT"
        assert ErrorCode.VALUE_OUT_OF_RANGE == "VALUE_OUT_OF_RANGE"
    
    def test_resource_errors_exist(self):
        """Test that resource error codes exist."""
        assert ErrorCode.NOT_FOUND == "NOT_FOUND"
        assert ErrorCode.ALREADY_EXISTS == "ALREADY_EXISTS"
        assert ErrorCode.CONFLICT == "CONFLICT"
    
    def test_operation_errors_exist(self):
        """Test that operation error codes exist."""
        assert ErrorCode.OPERATION_FAILED == "OPERATION_FAILED"
        assert ErrorCode.SAVE_FAILED == "SAVE_FAILED"
        assert ErrorCode.DELETE_FAILED == "DELETE_FAILED"
    
    def test_auth_errors_exist(self):
        """Test that auth error codes exist."""
        assert ErrorCode.UNAUTHORIZED == "UNAUTHORIZED"
        assert ErrorCode.FORBIDDEN == "FORBIDDEN"
    
    def test_network_errors_exist(self):
        """Test that network error codes exist."""
        assert ErrorCode.CONNECTION_ERROR == "CONNECTION_ERROR"
        assert ErrorCode.TIMEOUT == "TIMEOUT"
        assert ErrorCode.API_ERROR == "API_ERROR"


class TestFailure:
    """Tests for the Failure class."""
    
    def test_basic_failure(self):
        """Test creating a basic failure."""
        failure = Failure(
            error_code="INVALID_INPUT",
            message="The input was invalid"
        )
        
        assert failure.error_code == "INVALID_INPUT"
        assert failure.message == "The input was invalid"
        assert failure.details == {}
        assert failure.suggestions == []
    
    def test_failure_with_details(self):
        """Test failure with details dictionary."""
        failure = Failure(
            error_code="MISSING_REQUIRED_FIELD",
            message="Field is required",
            details={"field": "serial_number", "value": None}
        )
        
        assert failure.details["field"] == "serial_number"
        assert failure.details["value"] is None
    
    def test_failure_with_suggestions(self):
        """Test failure with suggestions list."""
        failure = Failure(
            error_code="NOT_FOUND",
            message="Product not found",
            suggestions=["Check the part number", "Verify the product exists"]
        )
        
        assert len(failure.suggestions) == 2
        assert "Check the part number" in failure.suggestions
    
    def test_failure_is_success_false(self):
        """Test that is_success is always False for Failure."""
        failure = Failure(error_code="ERROR", message="Error")
        assert failure.is_success is False
    
    def test_failure_is_failure_true(self):
        """Test that is_failure is always True for Failure."""
        failure = Failure(error_code="ERROR", message="Error")
        assert failure.is_failure is True
    
    def test_failure_value_is_none(self):
        """Test that value is always None for Failure."""
        failure = Failure(error_code="ERROR", message="Error")
        assert failure.value is None
    
    def test_failure_str_basic(self):
        """Test string representation of failure."""
        failure = Failure(
            error_code="INVALID_INPUT",
            message="Input validation failed"
        )
        
        result = str(failure)
        assert "[INVALID_INPUT]" in result
        assert "Input validation failed" in result
    
    def test_failure_str_with_suggestions(self):
        """Test string representation includes suggestions."""
        failure = Failure(
            error_code="ERROR",
            message="Error occurred",
            suggestions=["Try again", "Check logs"]
        )
        
        result = str(failure)
        assert "Suggestions:" in result
        assert "Try again" in result
    
    def test_failure_with_error_code_enum(self):
        """Test creating failure with ErrorCode enum."""
        failure = Failure(
            error_code=ErrorCode.NOT_FOUND,
            message="Resource not found"
        )
        
        # Due to use_enum_values=True, it should store the string value
        assert failure.error_code == "NOT_FOUND"


class TestSuccess:
    """Tests for the Success class."""
    
    def test_basic_success(self):
        """Test creating a basic success."""
        success = Success(value="result")
        
        assert success.value == "result"
        assert success.message == ""
    
    def test_success_with_message(self):
        """Test success with a message."""
        success = Success(value=42, message="Operation completed")
        
        assert success.value == 42
        assert success.message == "Operation completed"
    
    def test_success_with_complex_value(self):
        """Test success with complex value type."""
        data = {"key": "value", "items": [1, 2, 3]}
        success = Success(value=data)
        
        assert success.value == data
        assert success.value["key"] == "value"
    
    def test_success_is_success_true(self):
        """Test that is_success is always True for Success."""
        success = Success(value="test")
        assert success.is_success is True
    
    def test_success_is_failure_false(self):
        """Test that is_failure is always False for Success."""
        success = Success(value="test")
        assert success.is_failure is False
    
    def test_success_error_code_is_none(self):
        """Test that error_code is always None for Success."""
        success = Success(value="test")
        assert success.error_code is None
    
    def test_success_str_with_message(self):
        """Test string representation with message."""
        success = Success(value="data", message="All done")
        
        result = str(success)
        assert "Success:" in result
        assert "All done" in result
    
    def test_success_str_without_message(self):
        """Test string representation without message."""
        success = Success(value=123)
        
        result = str(success)
        assert "Success:" in result
        assert "int" in result  # Shows the type name
    
    def test_success_with_none_value(self):
        """Test success with None value."""
        success = Success(value=None)
        
        assert success.value is None
        assert success.is_success is True
    
    def test_success_with_list_value(self):
        """Test success with list value."""
        success = Success(value=[1, 2, 3])
        
        assert success.value == [1, 2, 3]
        assert len(success.value) == 3


class TestFailureFromException:
    """Tests for failure_from_exception helper."""
    
    def test_basic_exception(self):
        """Test converting a basic exception."""
        exc = ValueError("Invalid value")
        failure = failure_from_exception(exc)
        
        assert failure.error_code == "UNKNOWN_ERROR"
        assert failure.message == "Invalid value"
        assert failure.details["exception_type"] == "ValueError"
    
    def test_with_custom_error_code(self):
        """Test with custom error code."""
        exc = KeyError("missing_key")
        failure = failure_from_exception(exc, "NOT_FOUND")
        
        assert failure.error_code == "NOT_FOUND"
    
    def test_preserves_exception_message(self):
        """Test that exception message is preserved."""
        exc = RuntimeError("Something went wrong during processing")
        failure = failure_from_exception(exc)
        
        assert "Something went wrong" in failure.message
    
    def test_captures_exception_type(self):
        """Test that exception type is captured in details."""
        exc = TypeError("wrong type")
        failure = failure_from_exception(exc)
        
        assert failure.details["exception_type"] == "TypeError"


class TestResultUsagePatterns:
    """Tests for common Result usage patterns."""
    
    def test_success_failure_type_checking(self):
        """Test distinguishing between Success and Failure."""
        success = Success(value="data")
        failure = Failure(error_code="ERROR", message="Failed")
        
        # Using is_success
        assert success.is_success
        assert not failure.is_success
        
        # Using is_failure
        assert not success.is_failure
        assert failure.is_failure
    
    def test_chained_value_access(self):
        """Test safely accessing values from results."""
        success = Success(value={"name": "Test"})
        failure = Failure(error_code="ERROR", message="No data")
        
        # Success has value
        if success.is_success:
            assert success.value["name"] == "Test"
        
        # Failure has no value
        if failure.is_failure:
            assert failure.value is None
    
    def test_result_in_function_return(self):
        """Test using Result as function return type pattern."""
        def process_data(value: int):
            if value < 0:
                return Failure(
                    error_code=ErrorCode.VALUE_OUT_OF_RANGE,
                    message="Value must be positive",
                    details={"received": value, "expected": "positive int"}
                )
            return Success(value=value * 2)
        
        # Test success case
        result = process_data(5)
        assert result.is_success
        assert result.value == 10
        
        # Test failure case
        result = process_data(-1)
        assert result.is_failure
        assert result.error_code == "VALUE_OUT_OF_RANGE"
        assert result.details["received"] == -1
