"""Tests for pyWATS exceptions.

Tests all exception classes and their functionality.
Note: This test file previously tested the old pywats.exceptions module.
It now tests pywats.core.exceptions which is the canonical location.
"""
import pytest

from pywats.core.exceptions import (
    PyWATSError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ServerError,
    ConnectionError,
    TimeoutError,
    WatsApiError,
    ErrorMode,
)


@pytest.mark.skip(reason="Troubleshooting hints were part of deprecated pywats.exceptions module. Core exceptions use different pattern.")
class TestTroubleshootingHints:
    """Tests for troubleshooting hints functionality (DEPRECATED - old module only)."""
    
    def test_get_hints_for_connection(self):
        """Test getting connection error hints."""
        hints = get_troubleshooting_hints("connection")
        assert "Verify the server URL is correct" in hints
        assert "firewall" in hints.lower()
    
    def test_get_hints_for_authentication(self):
        """Test getting authentication error hints."""
        hints = get_troubleshooting_hints("authentication")
        assert "API token" in hints
        assert "base64-encoded" in hints
    
    def test_get_hints_for_timeout(self):
        """Test getting timeout error hints."""
        hints = get_troubleshooting_hints("timeout")
        assert "timeout" in hints.lower()
        assert "pyWATS(timeout=60.0)" in hints
    
    def test_get_hints_with_context_placeholder(self):
        """Test that context placeholders are replaced."""
        hints = get_troubleshooting_hints("connection", {"url": "https://example.com"})
        assert "https://example.com" in hints
    
    def test_get_hints_unknown_type(self):
        """Test getting hints for unknown error type returns empty."""
        hints = get_troubleshooting_hints("unknown_error_type")
        assert hints == ""
    
    def test_troubleshooting_hints_dict_has_expected_keys(self):
        """Test that all expected hint categories exist."""
        expected_keys = [
            "connection",
            "authentication",
            "timeout",
            "server_error",
            "not_found",
            "validation",
            "configuration",
            "service",
        ]
        for key in expected_keys:
            assert key in TROUBLESHOOTING_HINTS


class TestPyWATSError:
    """Tests for the base PyWATSError class."""
    
    def test_basic_error(self):
        """Test creating a basic error."""
        error = PyWATSError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert error.message == "Something went wrong"
    
    def test_error_with_details(self):
        """Test error with details dictionary."""
        error = PyWATSError("Error occurred", details={"key": "value"})
        assert error.details == {"key": "value"}
        assert "key" in str(error)
        assert "value" in str(error)
    
    def test_error_without_hints(self):
        """Test error with hints disabled."""
        error = PyWATSError("Error", show_hints=False)
        assert error._hints is None
        assert str(error) == "Error"
    
    def test_short_message(self):
        """Test the short_message property."""
        error = PyWATSError("Short message", details={"extra": "data"})
        assert error.short_message == "Short message"


class TestAuthenticationError:
    """Tests for AuthenticationError."""
    
    def test_default_message(self):
        """Test default authentication error message."""
        error = AuthenticationError()
        assert "Authentication failed" in str(error)
    
    def test_custom_message(self):
        """Test custom authentication error message."""
        error = AuthenticationError("Invalid token format")
        assert "Invalid token format" in str(error)
    
    def test_authentication_hints_included(self):
        """Test that authentication hints are included."""
        error = AuthenticationError()
        error_str = str(error)
        assert "API token" in error_str or "base64" in error_str
    
    def test_error_type(self):
        """Test that error_type is set correctly."""
        error = AuthenticationError()
        assert error.error_type == "authentication"


class TestNotFoundError:
    """Tests for NotFoundError."""
    
    def test_basic_not_found(self):
        """Test basic not found error."""
        error = NotFoundError("Product", "PN-001")
        assert "Product" in str(error)
        assert "PN-001" in str(error)
    
    def test_not_found_attributes(self):
        """Test that resource_type and identifier are stored."""
        error = NotFoundError("Asset", "SN-123")
        assert error.resource_type == "Asset"
        assert error.identifier == "SN-123"
    
    def test_custom_message(self):
        """Test custom message override."""
        error = NotFoundError("Report", "R-001", message="Custom not found message")
        assert "Custom not found message" in str(error)
    
    def test_details_populated(self):
        """Test that details dict is populated."""
        error = NotFoundError("Unit", "U-001")
        assert error.details["resource_type"] == "Unit"
        assert error.details["identifier"] == "U-001"


class TestValidationError:
    """Tests for ValidationError."""
    
    def test_basic_validation_error(self):
        """Test basic validation error."""
        error = ValidationError("Field is required")
        assert "Field is required" in str(error)
    
    def test_validation_with_field(self):
        """Test validation error with field name."""
        error = ValidationError("Invalid format", field="email")
        assert error.field == "email"
        assert error.details.get("field") == "email"
    
    def test_validation_with_value(self):
        """Test validation error with invalid value."""
        error = ValidationError("Out of range", field="count", value=-5)
        assert error.value == -5
        assert "-5" in str(error.details.get("value", ""))
    
    def test_long_value_truncated(self):
        """Test that long values are truncated."""
        long_value = "x" * 200
        error = ValidationError("Too long", value=long_value)
        # Value should be truncated to 100 chars
        assert len(error.details.get("value", "")) <= 100


class TestServerError:
    """Tests for ServerError."""
    
    def test_server_error_500(self):
        """Test 500 internal server error."""
        error = ServerError(500, "Internal error")
        assert "500" in str(error)
        assert "Internal error" in str(error)
    
    def test_server_error_502(self):
        """Test 502 bad gateway error."""
        error = ServerError(502, "Bad gateway")
        assert "502" in str(error)
        assert "gateway" in str(error).lower()
    
    def test_server_error_503(self):
        """Test 503 service unavailable error."""
        error = ServerError(503, "Service unavailable")
        assert "503" in str(error)
    
    def test_server_error_504(self):
        """Test 504 gateway timeout error."""
        error = ServerError(504, "Gateway timeout")
        assert "504" in str(error)
    
    def test_server_error_with_response_body(self):
        """Test server error with response body."""
        error = ServerError(500, "Error", response_body='{"error": "details"}')
        assert error.response_body == '{"error": "details"}'
        assert error.status_code == 500
    
    def test_response_body_truncated(self):
        """Test that long response bodies are truncated in details."""
        long_body = "x" * 1000
        error = ServerError(500, "Error", response_body=long_body)
        # Details should have truncated body
        assert len(error.details.get("response_body", "")) <= 500


class TestConnectionError:
    """Tests for ConnectionError."""
    
    def test_basic_connection_error(self):
        """Test basic connection error."""
        error = ConnectionError("Failed to connect")
        assert "Failed to connect" in str(error)
    
    def test_connection_error_with_url(self):
        """Test connection error with URL context."""
        error = ConnectionError("Connection refused", url="https://wats.example.com")
        assert error.details.get("url") == "https://wats.example.com"


class TestTimeoutError:
    """Tests for TimeoutError."""
    
    def test_default_timeout_error(self):
        """Test default timeout error message."""
        error = TimeoutError()
        assert "timed out" in str(error).lower()
    
    def test_timeout_with_duration(self):
        """Test timeout error with duration."""
        error = TimeoutError("Operation timed out", timeout=30.0)
        assert error.details.get("timeout_seconds") == 30.0
    
    def test_timeout_with_endpoint(self):
        """Test timeout error with endpoint info."""
        error = TimeoutError("Request timed out", endpoint="/api/reports")
        assert error.details.get("endpoint") == "/api/reports"


class TestConfigurationError:
    """Tests for ConfigurationError."""
    
    def test_basic_config_error(self):
        """Test basic configuration error."""
        error = ConfigurationError("Invalid configuration")
        assert "Invalid configuration" in str(error)
    
    def test_config_error_with_file(self):
        """Test configuration error with file path."""
        error = ConfigurationError("Parse error", config_file="/home/user/.pywats/config.json")
        assert error.details.get("config_file") == "/home/user/.pywats/config.json"
    
    def test_config_error_with_missing_field(self):
        """Test configuration error with missing field."""
        error = ConfigurationError("Missing required field", missing_field="base_url")
        assert error.details.get("missing_field") == "base_url"


class TestServiceError:
    """Tests for ServiceError."""
    
    def test_basic_service_error(self):
        """Test basic service error."""
        error = ServiceError("Service failed")
        assert "Service failed" in str(error)
    
    def test_service_error_with_name(self):
        """Test service error with service name."""
        error = ServiceError("Failed to start", service_name="pywats-client")
        assert error.details.get("service_name") == "pywats-client"
    
    def test_service_error_with_operation(self):
        """Test service error with operation context."""
        error = ServiceError("Operation failed", operation="submit_report")
        assert error.details.get("operation") == "submit_report"


class TestExceptionHierarchy:
    """Tests for exception class hierarchy."""
    
    def test_all_errors_inherit_from_base(self):
        """Test that all errors inherit from PyWATSError."""
        error_classes = [
            AuthenticationError,
            NotFoundError,
            ValidationError,
            ServerError,
            ConnectionError,
            TimeoutError,
            ConfigurationError,
            ServiceError,
        ]
        
        for error_class in error_classes:
            assert issubclass(error_class, PyWATSError)
    
    def test_base_error_inherits_from_exception(self):
        """Test that base error inherits from Exception."""
        assert issubclass(PyWATSError, Exception)
    
    def test_can_catch_by_base_class(self):
        """Test that derived errors can be caught by base class."""
        with pytest.raises(PyWATSError):
            raise AuthenticationError()
        
        with pytest.raises(PyWATSError):
            raise NotFoundError("Test", "ID")
        
        with pytest.raises(PyWATSError):
            raise ServerError(500, "Error")
