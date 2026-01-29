"""
Tests for pywats_client control exit codes.
"""
import pytest

from pywats_client.control.exit_codes import (
    # Success
    EXIT_SUCCESS,
    # General errors
    EXIT_ERROR,
    EXIT_MISSING_REQUIREMENTS,
    EXIT_INTERRUPTED,
    # Installation errors
    EXIT_ALREADY_INSTALLED,
    EXIT_NOT_INSTALLED,
    EXIT_INSTALL_FAILED,
    EXIT_UNINSTALL_FAILED,
    EXIT_PERMISSION_DENIED,
    # Configuration errors
    EXIT_CONFIG_ERROR,
    EXIT_CONFIG_NOT_FOUND,
    EXIT_CONFIG_INVALID,
    # Service operation errors
    EXIT_SERVICE_START_FAILED,
    EXIT_SERVICE_STOP_FAILED,
    EXIT_SERVICE_NOT_RUNNING,
    EXIT_SERVICE_TIMEOUT,
    # Network errors
    EXIT_NETWORK_ERROR,
    EXIT_SERVER_UNREACHABLE,
    EXIT_AUTH_FAILED,
    # Function
    get_exit_code_description,
)


class TestExitCodeValues:
    """Tests for exit code constant values."""
    
    def test_success_is_zero(self):
        """Test that success is 0."""
        assert EXIT_SUCCESS == 0
    
    def test_general_errors_range(self):
        """Test general errors are in 1-9 range."""
        assert 1 <= EXIT_ERROR <= 9
        assert 1 <= EXIT_MISSING_REQUIREMENTS <= 9
        assert 1 <= EXIT_INTERRUPTED <= 9
    
    def test_installation_errors_range(self):
        """Test installation errors are in 10-19 range."""
        assert 10 <= EXIT_ALREADY_INSTALLED <= 19
        assert 10 <= EXIT_NOT_INSTALLED <= 19
        assert 10 <= EXIT_INSTALL_FAILED <= 19
        assert 10 <= EXIT_UNINSTALL_FAILED <= 19
        assert 10 <= EXIT_PERMISSION_DENIED <= 19
    
    def test_configuration_errors_range(self):
        """Test configuration errors are in 20-29 range."""
        assert 20 <= EXIT_CONFIG_ERROR <= 29
        assert 20 <= EXIT_CONFIG_NOT_FOUND <= 29
        assert 20 <= EXIT_CONFIG_INVALID <= 29
    
    def test_service_errors_range(self):
        """Test service errors are in 30-39 range."""
        assert 30 <= EXIT_SERVICE_START_FAILED <= 39
        assert 30 <= EXIT_SERVICE_STOP_FAILED <= 39
        assert 30 <= EXIT_SERVICE_NOT_RUNNING <= 39
        assert 30 <= EXIT_SERVICE_TIMEOUT <= 39
    
    def test_network_errors_range(self):
        """Test network errors are in 40-49 range."""
        assert 40 <= EXIT_NETWORK_ERROR <= 49
        assert 40 <= EXIT_SERVER_UNREACHABLE <= 49
        assert 40 <= EXIT_AUTH_FAILED <= 49
    
    def test_all_codes_unique(self):
        """Test all exit codes are unique."""
        all_codes = [
            EXIT_SUCCESS,
            EXIT_ERROR,
            EXIT_MISSING_REQUIREMENTS,
            EXIT_INTERRUPTED,
            EXIT_ALREADY_INSTALLED,
            EXIT_NOT_INSTALLED,
            EXIT_INSTALL_FAILED,
            EXIT_UNINSTALL_FAILED,
            EXIT_PERMISSION_DENIED,
            EXIT_CONFIG_ERROR,
            EXIT_CONFIG_NOT_FOUND,
            EXIT_CONFIG_INVALID,
            EXIT_SERVICE_START_FAILED,
            EXIT_SERVICE_STOP_FAILED,
            EXIT_SERVICE_NOT_RUNNING,
            EXIT_SERVICE_TIMEOUT,
            EXIT_NETWORK_ERROR,
            EXIT_SERVER_UNREACHABLE,
            EXIT_AUTH_FAILED,
        ]
        assert len(all_codes) == len(set(all_codes))


class TestGetExitCodeDescription:
    """Tests for get_exit_code_description function."""
    
    def test_success_description(self):
        """Test success code description."""
        desc = get_exit_code_description(EXIT_SUCCESS)
        assert desc == "Success"
    
    def test_error_description(self):
        """Test general error description."""
        desc = get_exit_code_description(EXIT_ERROR)
        assert "error" in desc.lower()
    
    def test_missing_requirements_description(self):
        """Test missing requirements description."""
        desc = get_exit_code_description(EXIT_MISSING_REQUIREMENTS)
        assert "requirement" in desc.lower() or "python" in desc.lower()
    
    def test_permission_denied_description(self):
        """Test permission denied description."""
        desc = get_exit_code_description(EXIT_PERMISSION_DENIED)
        assert "permission" in desc.lower() or "administrator" in desc.lower()
    
    def test_config_not_found_description(self):
        """Test config not found description."""
        desc = get_exit_code_description(EXIT_CONFIG_NOT_FOUND)
        assert "config" in desc.lower() or "not found" in desc.lower()
    
    def test_service_start_failed_description(self):
        """Test service start failed description."""
        desc = get_exit_code_description(EXIT_SERVICE_START_FAILED)
        assert "service" in desc.lower() or "start" in desc.lower()
    
    def test_auth_failed_description(self):
        """Test auth failed description."""
        desc = get_exit_code_description(EXIT_AUTH_FAILED)
        assert "auth" in desc.lower() or "failed" in desc.lower()
    
    def test_unknown_code_description(self):
        """Test unknown code returns generic message."""
        desc = get_exit_code_description(999)
        assert "999" in desc or "unknown" in desc.lower()
    
    def test_all_known_codes_have_descriptions(self):
        """Test all known codes have non-empty descriptions."""
        known_codes = [
            EXIT_SUCCESS,
            EXIT_ERROR,
            EXIT_MISSING_REQUIREMENTS,
            EXIT_INTERRUPTED,
            EXIT_ALREADY_INSTALLED,
            EXIT_NOT_INSTALLED,
            EXIT_INSTALL_FAILED,
            EXIT_UNINSTALL_FAILED,
            EXIT_PERMISSION_DENIED,
            EXIT_CONFIG_ERROR,
            EXIT_CONFIG_NOT_FOUND,
            EXIT_CONFIG_INVALID,
            EXIT_SERVICE_START_FAILED,
            EXIT_SERVICE_STOP_FAILED,
            EXIT_SERVICE_NOT_RUNNING,
            EXIT_SERVICE_TIMEOUT,
            EXIT_NETWORK_ERROR,
            EXIT_SERVER_UNREACHABLE,
            EXIT_AUTH_FAILED,
        ]
        for code in known_codes:
            desc = get_exit_code_description(code)
            assert desc is not None
            assert len(desc) > 0
            # Known codes shouldn't have "unknown" in their description
            assert "unknown" not in desc.lower()
