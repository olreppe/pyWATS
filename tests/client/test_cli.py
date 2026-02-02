"""Integration tests for CLI commands."""

import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
from click.testing import CliRunner

from pywats_client.cli import cli
from pywats_client.core.config_manager import ConfigManager
from pywats.core.config import APISettings


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


@pytest.fixture
def mock_service_manager():
    """Create a mocked ServiceManager."""
    with patch('pywats_client.cli.ServiceManager') as mock:
        manager = Mock()
        manager.is_running.return_value = False
        manager.get_status.return_value = {
            'running': False,
            'pid': None,
            'uptime': None,
            'platform': 'Windows',
            'instance_id': 'default',
            'log_file': None
        }
        mock.return_value = manager
        yield manager


@pytest.fixture
def mock_config_manager(tmp_path):
    """Create a mocked ConfigManager."""
    with patch('pywats_client.cli.ConfigManager') as mock:
        config_path = tmp_path / "test_config.json"
        manager = Mock()
        manager.config_path = config_path
        manager.instance_id = "default"
        manager.load.return_value = APISettings()
        manager.exists.return_value = True
        mock.return_value = manager
        yield manager


class TestCLIHelp:
    """Test CLI help text and command discovery."""
    
    def test_cli_help(self, runner):
        """Test main CLI help text."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'pyWATS Client Service Manager' in result.output
        assert 'start' in result.output
        assert 'stop' in result.output
        assert 'status' in result.output
        assert 'config' in result.output
    
    def test_config_help(self, runner):
        """Test config command help text."""
        result = runner.invoke(cli, ['config', '--help'])
        assert result.exit_code == 0
        assert 'Manage pyWATS Client configuration' in result.output
        assert 'show' in result.output
        assert 'get' in result.output
        assert 'set' in result.output


class TestServiceCommands:
    """Test service management commands."""
    
    def test_start_command(self, runner, mock_service_manager):
        """Test start command."""
        mock_service_manager.start.return_value = True
        mock_service_manager.get_status.return_value = {
            'running': True,
            'pid': 12345,
            'uptime': 0,
            'platform': 'Windows',
            'instance_id': 'default',
            'log_file': '/tmp/pywats.log'
        }
        
        result = runner.invoke(cli, ['start'])
        
        assert result.exit_code == 0
        assert 'Service started successfully' in result.output
        assert '12345' in result.output
    
    def test_start_when_already_running(self, runner, mock_service_manager):
        """Test start command when service is already running."""
        mock_service_manager.is_running.return_value = True
        mock_service_manager.get_status.return_value = {
            'running': True,
            'pid': 12345,
            'uptime': 120.5,
            'platform': 'Windows',
            'instance_id': 'default',
            'log_file': None
        }
        
        result = runner.invoke(cli, ['start'])
        
        assert result.exit_code == 0
        assert 'already running' in result.output
    
    def test_stop_command(self, runner, mock_service_manager):
        """Test stop command."""
        mock_service_manager.is_running.return_value = True
        mock_service_manager.get_pid.return_value = 12345
        mock_service_manager.stop.return_value = True
        
        result = runner.invoke(cli, ['stop'])
        
        assert result.exit_code == 0
        assert 'Service stopped successfully' in result.output
    
    def test_stop_when_not_running(self, runner, mock_service_manager):
        """Test stop command when service is not running."""
        mock_service_manager.is_running.return_value = False
        
        result = runner.invoke(cli, ['stop'])
        
        assert result.exit_code == 0
        assert 'not running' in result.output
    
    def test_restart_command(self, runner, mock_service_manager):
        """Test restart command."""
        mock_service_manager.is_running.return_value = True
        mock_service_manager.stop.return_value = True
        mock_service_manager.start.return_value = True
        mock_service_manager.get_status.return_value = {
            'running': True,
            'pid': 12345,
            'uptime': 0,
            'platform': 'Windows',
            'instance_id': 'default',
            'log_file': '/tmp/pywats.log'
        }
        
        result = runner.invoke(cli, ['restart'])
        
        assert result.exit_code == 0
        assert 'Service restarted successfully' in result.output
    
    def test_status_command_running(self, runner, mock_service_manager):
        """Test status command when service is running."""
        mock_service_manager.get_status.return_value = {
            'running': True,
            'pid': 12345,
            'uptime': 3665.5,  # 1h 1m 5s
            'platform': 'Windows',
            'instance_id': 'default',
            'log_file': '/tmp/pywats.log'
        }
        
        result = runner.invoke(cli, ['status'])
        
        assert result.exit_code == 0
        assert 'Running' in result.output
        assert '12345' in result.output
        assert '1h' in result.output
    
    def test_status_command_stopped(self, runner, mock_service_manager):
        """Test status command when service is stopped."""
        result = runner.invoke(cli, ['status'])
        
        assert result.exit_code == 0
        assert 'Stopped' in result.output


class TestConfigCommands:
    """Test configuration management commands."""
    
    def test_config_show_text(self, runner, mock_service_manager, mock_config_manager):
        """Test config show command with text format."""
        result = runner.invoke(cli, ['config', 'show'])
        
        assert result.exit_code == 0
        assert 'pyWATS Client Configuration' in result.output
        assert 'Connection:' in result.output
        assert 'Caching:' in result.output
        assert 'Metrics:' in result.output
    
    def test_config_show_json(self, runner, mock_service_manager, mock_config_manager):
        """Test config show command with JSON format."""
        result = runner.invoke(cli, ['config', 'show', '--format', 'json'])
        
        assert result.exit_code == 0
        # Should be valid JSON
        data = json.loads(result.output)
        assert 'server_url' in data
    
    def test_config_get_valid_key(self, runner, mock_service_manager, mock_config_manager):
        """Test config get with valid key."""
        result = runner.invoke(cli, ['config', 'get', 'server_url'])
        
        assert result.exit_code == 0
        assert 'http' in result.output.lower()
    
    def test_config_get_invalid_key(self, runner, mock_service_manager, mock_config_manager):
        """Test config get with invalid key."""
        result = runner.invoke(cli, ['config', 'get', 'nonexistent_key'])
        
        assert result.exit_code == 1
        assert 'not found' in result.output.lower()
    
    def test_config_set_string(self, runner, mock_service_manager, mock_config_manager):
        """Test config set with string value."""
        result = runner.invoke(cli, [
            'config', 'set',
            'server_url', 'https://new.example.com'
        ])
        
        assert result.exit_code == 0
        assert 'Configuration updated' in result.output
        mock_config_manager.save.assert_called_once()
    
    def test_config_set_int(self, runner, mock_service_manager, mock_config_manager):
        """Test config set with integer value."""
        result = runner.invoke(cli, [
            'config', 'set',
            'timeout_seconds', '60',
            '--type', 'int'
        ])
        
        assert result.exit_code == 0
        assert 'Configuration updated' in result.output
    
    def test_config_set_bool(self, runner, mock_service_manager, mock_config_manager):
        """Test config set with boolean value."""
        result = runner.invoke(cli, [
            'config', 'set',
            'enable_cache', 'true',
            '--type', 'bool'
        ])
        
        assert result.exit_code == 0
        assert 'Configuration updated' in result.output
    
    def test_config_set_nested_key_fails(self, runner, mock_service_manager, mock_config_manager):
        """Test config set with nested key fails."""
        result = runner.invoke(cli, [
            'config', 'set',
            'domains.report.timeout', '60'
        ])
        
        assert result.exit_code == 1
        assert 'Nested keys not supported' in result.output
    
    def test_config_reset(self, runner, mock_service_manager, mock_config_manager):
        """Test config reset command."""
        result = runner.invoke(cli, ['config', 'reset'], input='y\n')
        
        assert result.exit_code == 0
        assert 'reset to defaults' in result.output.lower()
        mock_config_manager.reset_to_defaults.assert_called_once()
    
    def test_config_reset_cancel(self, runner, mock_service_manager, mock_config_manager):
        """Test config reset cancellation."""
        result = runner.invoke(cli, ['config', 'reset'], input='n\n')
        
        assert result.exit_code == 1  # Aborted
        mock_config_manager.reset_to_defaults.assert_not_called()
    
    def test_config_path(self, runner, mock_service_manager, mock_config_manager):
        """Test config path command."""
        result = runner.invoke(cli, ['config', 'path'])
        
        assert result.exit_code == 0
        assert 'Config File:' in result.output
        assert 'test_config.json' in result.output
    
    @patch('os.startfile')
    @patch('platform.system', return_value='Windows')
    def test_config_edit_windows(self, mock_platform, mock_startfile, runner, mock_service_manager, mock_config_manager):
        """Test config edit command on Windows."""
        result = runner.invoke(cli, ['config', 'edit'])
        
        assert result.exit_code == 0
        assert 'Opened:' in result.output
        mock_startfile.assert_called_once()
    
    @patch('subprocess.call')
    @patch('platform.system', return_value='Darwin')
    def test_config_edit_macos(self, mock_platform, mock_subprocess, runner, mock_service_manager, mock_config_manager):
        """Test config edit command on macOS."""
        result = runner.invoke(cli, ['config', 'edit'])
        
        assert result.exit_code == 0
        assert 'Opened:' in result.output
        mock_subprocess.assert_called_once()


class TestCLIOptions:
    """Test CLI options and flags."""
    
    def test_instance_id_option(self, runner, mock_service_manager):
        """Test --instance-id option."""
        with patch('pywats_client.cli.ServiceManager') as mock:
            manager = Mock()
            mock.return_value = manager
            
            result = runner.invoke(cli, ['--instance-id', 'custom', 'status'])
            
            mock.assert_called_with('custom')
    
    def test_verbose_option(self, runner, mock_service_manager):
        """Test --verbose option."""
        result = runner.invoke(cli, ['--verbose', 'status'])
        
        # Should not error
        assert result.exit_code == 0


class TestGUICommand:
    """Test GUI command."""
    
    @patch('pywats_client.cli.QApplication', side_effect=ImportError)
    def test_gui_without_qt(self, mock_qt, runner, mock_service_manager):
        """Test gui command fails gracefully without Qt."""
        result = runner.invoke(cli, ['gui'])
        
        assert result.exit_code == 1
        assert 'GUI not available' in result.output
        assert 'pip install pywats-api[client]' in result.output
