"""
Tests for pywats_client exceptions.
"""
import pytest

from pywats_client.exceptions import (
    # Functions
    get_troubleshooting_hints,
    TROUBLESHOOTING_HINTS,
    # Base
    ClientError,
    # Converter exceptions
    ConverterError,
    FileFormatError,
    FileAccessError,
    ConverterConfigError,
    # Queue exceptions
    QueueError,
    QueueFullError,
    QueueCorruptedError,
    OfflineError,
    # Service exceptions
    ServiceInstallError,
    ServiceStartError,
    ServicePermissionError,
    # Config exceptions
    ConfigurationError,
    ConfigurationMissingError,
)


class TestTroubleshootingHints:
    """Tests for troubleshooting hints."""
    
    def test_hints_dict_has_categories(self):
        """Test that hints dict has expected categories."""
        expected = ["converter", "file_format", "file_access", "queue", 
                    "queue_full", "offline", "service_install"]
        for category in expected:
            assert category in TROUBLESHOOTING_HINTS
    
    def test_get_hints_returns_string(self):
        """Test get_troubleshooting_hints returns formatted string."""
        hints = get_troubleshooting_hints("converter")
        assert isinstance(hints, str)
        assert "Possible causes" in hints
    
    def test_get_hints_unknown_type(self):
        """Test unknown error type returns empty string."""
        hints = get_troubleshooting_hints("unknown_type_xyz")
        assert hints == ""
    
    def test_get_hints_with_context(self):
        """Test hints can include context values."""
        # Note: Most hints don't have placeholders, but the function supports them
        hints = get_troubleshooting_hints("converter", {"file": "/test/file.csv"})
        assert isinstance(hints, str)


class TestClientError:
    """Tests for base ClientError exception."""
    
    def test_basic_creation(self):
        """Test creating a basic error."""
        err = ClientError("Something went wrong")
        assert err.message == "Something went wrong"
        assert "Something went wrong" in str(err)
    
    def test_with_details(self):
        """Test error with details."""
        err = ClientError("Error occurred", details={"file": "test.csv", "line": 42})
        assert err.details["file"] == "test.csv"
        assert "file=test.csv" in str(err)
    
    def test_without_hints(self):
        """Test error without troubleshooting hints."""
        err = ClientError("Error", show_hints=False)
        assert err._hints is None
    
    def test_short_message_property(self):
        """Test short_message returns message without hints."""
        err = ClientError("Error message", show_hints=True)
        assert err.short_message == "Error message"


class TestConverterError:
    """Tests for ConverterError exception."""
    
    def test_basic_creation(self):
        """Test creating basic converter error."""
        err = ConverterError("Failed to convert file")
        assert err.message == "Failed to convert file"
        assert err.converter_name is None
    
    def test_with_converter_name(self):
        """Test error with converter name."""
        err = ConverterError(
            "Conversion failed",
            converter_name="CSVConverter",
        )
        assert err.converter_name == "CSVConverter"
        assert "converter=CSVConverter" in str(err)
    
    def test_with_file_path(self):
        """Test error with file path."""
        err = ConverterError(
            "Conversion failed",
            file_path="/path/to/file.csv",
        )
        assert err.file_path == "/path/to/file.csv"
        assert "file=/path/to/file.csv" in str(err)
    
    def test_with_cause(self):
        """Test error with underlying cause."""
        cause = ValueError("Invalid value")
        err = ConverterError(
            "Conversion failed",
            cause=cause,
        )
        assert err.cause is cause
        assert "Invalid value" in str(err)
    
    def test_has_converter_hints(self):
        """Test error includes converter troubleshooting hints."""
        err = ConverterError("Failed")
        assert "converter" in str(err).lower() or "Possible causes" in str(err)


class TestFileFormatError:
    """Tests for FileFormatError exception."""
    
    def test_basic_creation(self):
        """Test creating basic file format error."""
        err = FileFormatError("Invalid format")
        assert err.message == "Invalid format"
    
    def test_with_format_info(self):
        """Test error with format information."""
        err = FileFormatError(
            "Format mismatch",
            file_path="/test/file.txt",
            expected_format="CSV",
            actual_format="XML",
        )
        assert err.expected_format == "CSV"
        assert err.actual_format == "XML"
        assert "expected=CSV" in str(err)
        assert "actual=XML" in str(err)
    
    def test_with_line_number(self):
        """Test error with line number."""
        err = FileFormatError(
            "Parse error",
            line_number=42,
        )
        assert err.line_number == 42
        assert "line=42" in str(err)


class TestFileAccessError:
    """Tests for FileAccessError exception."""
    
    def test_basic_creation(self):
        """Test creating basic file access error."""
        err = FileAccessError("Cannot read file")
        assert err.message == "Cannot read file"
    
    def test_with_operation(self):
        """Test error with operation info."""
        err = FileAccessError(
            "Access denied",
            file_path="/etc/passwd",
            operation="read",
        )
        assert err.file_path == "/etc/passwd"
        assert err.operation == "read"


class TestConverterConfigError:
    """Tests for ConverterConfigError exception."""
    
    def test_basic_creation(self):
        """Test creating basic config error."""
        err = ConverterConfigError("Invalid setting")
        assert err.message == "Invalid setting"
    
    def test_with_setting_info(self):
        """Test error with setting information."""
        err = ConverterConfigError(
            "Invalid value for setting",
            converter_name="TestConverter",
            setting="timeout",
            value=-1,
        )
        assert err.converter_name == "TestConverter"
        assert err.setting == "timeout"
        assert err.value == -1


class TestQueueError:
    """Tests for QueueError exception."""
    
    def test_basic_creation(self):
        """Test creating basic queue error."""
        err = QueueError("Queue operation failed")
        assert err.message == "Queue operation failed"
    
    def test_with_queue_info(self):
        """Test error with queue information."""
        err = QueueError(
            "Failed to enqueue",
            queue_path="/var/queue",
            item_id="item-001",
            operation="enqueue",
        )
        assert err.queue_path == "/var/queue"
        assert err.item_id == "item-001"
        assert err.operation == "enqueue"


class TestQueueFullError:
    """Tests for QueueFullError exception."""
    
    def test_default_message(self):
        """Test default error message."""
        err = QueueFullError()
        assert "full" in err.message.lower()
    
    def test_custom_message(self):
        """Test custom error message."""
        err = QueueFullError("Cannot add more items")
        assert err.message == "Cannot add more items"
    
    def test_with_size_info(self):
        """Test error with size information."""
        err = QueueFullError(
            current_size=100,
            max_size=100,
        )
        assert err.current_size == 100
        assert err.max_size == 100
        assert "current_size=100" in str(err)
        assert "max_size=100" in str(err)


class TestQueueCorruptedError:
    """Tests for QueueCorruptedError exception."""
    
    def test_basic_creation(self):
        """Test creating basic corruption error."""
        err = QueueCorruptedError("Queue data corrupted")
        assert err.message == "Queue data corrupted"
    
    def test_with_file_info(self):
        """Test error with corrupted file info."""
        err = QueueCorruptedError(
            "Data corruption detected",
            queue_path="/var/queue",
            corrupted_file="item-001.wsjf",
        )
        assert err.queue_path == "/var/queue"
        assert err.corrupted_file == "item-001.wsjf"


class TestOfflineError:
    """Tests for OfflineError exception."""
    
    def test_default_message(self):
        """Test default error message."""
        err = OfflineError()
        assert "connectivity" in err.message.lower() or "offline" in err.message.lower()
    
    def test_with_server_url(self):
        """Test error with server URL."""
        err = OfflineError(
            server_url="https://wats.example.com",
        )
        assert err.server_url == "https://wats.example.com"
    
    def test_queued_indicator(self):
        """Test error indicates if request was queued."""
        err = OfflineError(queued=True)
        assert err.queued is True
        assert "queued" in str(err).lower()


class TestServiceInstallError:
    """Tests for ServiceInstallError exception."""
    
    def test_basic_creation(self):
        """Test creating basic install error."""
        err = ServiceInstallError("Installation failed")
        assert err.message == "Installation failed"
    
    def test_with_service_info(self):
        """Test error with service information."""
        err = ServiceInstallError(
            "Failed to install service",
            service_name="pywats-client",
            platform="windows",
        )
        assert err.service_name == "pywats-client"
        assert err.platform == "windows"
    
    def test_with_cause(self):
        """Test error with underlying cause."""
        cause = PermissionError("Access denied")
        err = ServiceInstallError(
            "Install failed",
            cause=cause,
        )
        assert err.cause is cause


class TestServiceStartError:
    """Tests for ServiceStartError exception."""
    
    def test_basic_creation(self):
        """Test creating basic start error."""
        err = ServiceStartError("Service failed to start")
        assert err.message == "Service failed to start"
    
    def test_with_service_info(self):
        """Test error with service information."""
        err = ServiceStartError(
            "Failed to start",
            service_name="pywats-client",
            reason="Port in use",
        )
        assert err.service_name == "pywats-client"
        assert err.reason == "Port in use"


class TestServicePermissionError:
    """Tests for ServicePermissionError exception."""
    
    def test_default_message(self):
        """Test default error message."""
        err = ServicePermissionError()
        assert "administrator" in err.message.lower() or "privileges" in err.message.lower()
    
    def test_custom_message(self):
        """Test custom error message."""
        err = ServicePermissionError("Insufficient privileges")
        assert err.message == "Insufficient privileges"
    
    def test_with_operation(self):
        """Test error with operation info."""
        err = ServicePermissionError(operation="install")
        assert err.operation == "install"


class TestConfigurationError:
    """Tests for ConfigurationError exception."""
    
    def test_basic_creation(self):
        """Test creating basic config error."""
        err = ConfigurationError("Configuration error")
        assert err.message == "Configuration error"
    
    def test_with_config_info(self):
        """Test error with config information."""
        err = ConfigurationError(
            "Invalid value",
            config_file="/etc/pywats/config.json",
            key="timeout",
            value=-1,
        )
        assert err.config_file == "/etc/pywats/config.json"
        assert err.key == "timeout"
        assert err.value == -1


class TestConfigurationMissingError:
    """Tests for ConfigurationMissingError exception."""
    
    def test_default_message(self):
        """Test default error message."""
        err = ConfigurationMissingError()
        assert "not found" in err.message.lower() or "missing" in err.message.lower()
    
    def test_with_location_info(self):
        """Test error with location information."""
        err = ConfigurationMissingError(
            config_file="config.json",
            expected_location="~/.pywats_client/config.json",
        )
        assert err.config_file == "config.json"
        assert err.expected_location == "~/.pywats_client/config.json"
