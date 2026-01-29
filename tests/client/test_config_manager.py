"""
Tests for pywats_client.core.config_manager module

Tests file-based configuration persistence for pyWATS Client.
"""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from pywats_client.core.config_manager import (
    ConfigManager,
    load_client_settings,
)
from pywats.core.config import APISettings


class TestConfigManagerInit:
    """Tests for ConfigManager initialization."""
    
    def test_init_with_default_path(self, tmp_path):
        """Test initialization with default path."""
        with patch.object(ConfigManager, '_get_default_config_path') as mock_path:
            mock_path.return_value = tmp_path / "config.json"
            manager = ConfigManager()
            
            assert manager.config_path == tmp_path / "config.json"
    
    def test_init_with_custom_path(self, tmp_path):
        """Test initialization with custom config path."""
        custom_path = tmp_path / "custom_config.json"
        manager = ConfigManager(config_path=custom_path)
        
        assert manager.config_path == custom_path
    
    def test_init_with_instance_id(self, tmp_path):
        """Test initialization with instance ID."""
        with patch.object(ConfigManager, '_get_default_config_path') as mock_path:
            mock_path.return_value = tmp_path / "instances" / "test" / "config.json"
            manager = ConfigManager(instance_id="test")
            
            mock_path.assert_called_with("test")
    
    def test_instance_id_property(self, tmp_path):
        """Test instance_id property."""
        manager = ConfigManager(config_path=tmp_path / "config.json", instance_id="my_instance")
        
        assert manager.instance_id == "my_instance"
    
    def test_default_instance_id(self, tmp_path):
        """Test default instance ID."""
        manager = ConfigManager(config_path=tmp_path / "config.json")
        
        assert manager.instance_id == "default"


class TestGetDefaultConfigPath:
    """Tests for _get_default_config_path() method."""
    
    def test_default_instance_windows(self):
        """Test default path on Windows."""
        with patch('pywats_client.core.config_manager.os.name', 'nt'):
            with patch.dict(os.environ, {'APPDATA': 'C:\\Users\\Test\\AppData\\Roaming'}):
                path = ConfigManager._get_default_config_path()
                
                assert 'pyWATS' in str(path)
                assert path.name == ConfigManager.DEFAULT_CONFIG_FILENAME
    
    def test_default_instance_unix(self):
        """Test default path on Unix - uses home directory."""
        # Just test that we get a path with the right filename
        path = ConfigManager._get_default_config_path()
        assert path.name == ConfigManager.DEFAULT_CONFIG_FILENAME
    
    def test_custom_instance_path(self):
        """Test path for custom instance."""
        with patch('os.name', 'nt'):
            with patch.dict(os.environ, {'APPDATA': 'C:\\AppData'}):
                path = ConfigManager._get_default_config_path("test_instance")
                
                assert "instances" in str(path)
                assert "test_instance" in str(path)
    
    def test_default_config_filename(self):
        """Test that default config filename is defined."""
        assert ConfigManager.DEFAULT_CONFIG_FILENAME == "pywats_api.json"


class TestGetConfigDirectory:
    """Tests for get_config_directory() method."""
    
    def test_get_config_directory_default(self):
        """Test getting config directory for default instance."""
        with patch.object(ConfigManager, '_get_default_config_path') as mock_path:
            mock_path.return_value = Path("/config/dir/config.json")
            
            directory = ConfigManager.get_config_directory()
            
            assert directory == Path("/config/dir")
    
    def test_get_config_directory_custom_instance(self):
        """Test getting config directory for custom instance."""
        with patch.object(ConfigManager, '_get_default_config_path') as mock_path:
            mock_path.return_value = Path("/config/instances/my_inst/config.json")
            
            directory = ConfigManager.get_config_directory("my_inst")
            
            mock_path.assert_called_with("my_inst")
            assert directory == Path("/config/instances/my_inst")


class TestConfigManagerLoad:
    """Tests for ConfigManager.load() method."""
    
    def test_load_existing_config(self, tmp_path):
        """Test loading existing config file."""
        config_path = tmp_path / "config.json"
        config_data = {
            "timeout_seconds": 120,
            "max_retries": 5,
        }
        config_path.write_text(json.dumps(config_data))
        
        manager = ConfigManager(config_path=config_path)
        settings = manager.load()
        
        assert settings.timeout_seconds == 120
        assert settings.max_retries == 5
    
    def test_load_nonexistent_config_returns_defaults(self, tmp_path):
        """Test loading when config doesn't exist returns defaults."""
        config_path = tmp_path / "nonexistent.json"
        
        manager = ConfigManager(config_path=config_path)
        settings = manager.load()
        
        assert isinstance(settings, APISettings)
    
    def test_load_empty_config_returns_defaults(self, tmp_path):
        """Test loading empty config file returns defaults."""
        config_path = tmp_path / "empty.json"
        config_path.write_text("")
        
        manager = ConfigManager(config_path=config_path)
        
        with patch('pywats_client.core.config_manager.SafeFileReader') as mock_reader:
            mock_reader.read_json_safe.return_value = None
            settings = manager.load()
        
        assert isinstance(settings, APISettings)
    
    def test_load_corrupted_config_returns_defaults(self, tmp_path):
        """Test loading corrupted config returns defaults."""
        config_path = tmp_path / "corrupted.json"
        config_path.write_text("{invalid json")
        
        manager = ConfigManager(config_path=config_path)
        
        with patch('pywats_client.core.config_manager.SafeFileReader') as mock_reader:
            mock_reader.read_json_safe.side_effect = Exception("Parse error")
            settings = manager.load()
        
        assert isinstance(settings, APISettings)
    
    def test_load_caches_settings(self, tmp_path):
        """Test that load caches settings."""
        config_path = tmp_path / "config.json"
        config_data = {"base_url": "https://cached.wats.com"}
        config_path.write_text(json.dumps(config_data))
        
        manager = ConfigManager(config_path=config_path)
        settings1 = manager.load()
        
        assert manager._settings is not None


class TestConfigManagerSave:
    """Tests for ConfigManager.save() method."""
    
    def test_save_settings(self, tmp_path):
        """Test saving settings to file."""
        config_path = tmp_path / "output.json"
        
        manager = ConfigManager(config_path=config_path)
        settings = APISettings(base_url="https://saved.wats.com")
        
        with patch('pywats_client.core.config_manager.SafeFileWriter') as mock_writer:
            mock_result = Mock()
            mock_result.success = True
            mock_writer.write_json_atomic.return_value = mock_result
            
            manager.save(settings)
            
            mock_writer.write_json_atomic.assert_called_once()
    
    def test_save_creates_parent_directory(self, tmp_path):
        """Test save creates parent directories."""
        config_path = tmp_path / "subdir" / "deep" / "config.json"
        
        manager = ConfigManager(config_path=config_path)
        settings = APISettings()
        
        with patch('pywats_client.core.config_manager.SafeFileWriter') as mock_writer:
            mock_result = Mock()
            mock_result.success = True
            mock_writer.write_json_atomic.return_value = mock_result
            
            manager.save(settings)
            
            assert config_path.parent.exists()
    
    def test_save_without_settings_uses_defaults(self, tmp_path):
        """Test save without settings argument uses defaults."""
        config_path = tmp_path / "config.json"
        
        manager = ConfigManager(config_path=config_path)
        
        with patch('pywats_client.core.config_manager.SafeFileWriter') as mock_writer:
            mock_result = Mock()
            mock_result.success = True
            mock_writer.write_json_atomic.return_value = mock_result
            
            manager.save()
            
            mock_writer.write_json_atomic.assert_called_once()
    
    def test_save_uses_cached_settings(self, tmp_path):
        """Test save uses previously loaded settings if none provided."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"timeout_seconds": 99}))
        
        manager = ConfigManager(config_path=config_path)
        manager.load()  # Cache settings
        
        with patch('pywats_client.core.config_manager.SafeFileWriter') as mock_writer:
            mock_result = Mock()
            mock_result.success = True
            mock_writer.write_json_atomic.return_value = mock_result
            
            manager.save()  # Should use cached settings
            
            call_args = mock_writer.write_json_atomic.call_args
            saved_data = call_args[0][1]
            assert saved_data.get("timeout_seconds") == 99
    
    def test_save_failure_raises_error(self, tmp_path):
        """Test save failure raises IOError."""
        config_path = tmp_path / "config.json"
        
        manager = ConfigManager(config_path=config_path)
        settings = APISettings()
        
        with patch('pywats_client.core.config_manager.SafeFileWriter') as mock_writer:
            mock_result = Mock()
            mock_result.success = False
            mock_result.error = "Write failed"
            mock_writer.write_json_atomic.return_value = mock_result
            
            with pytest.raises(IOError):
                manager.save(settings)


class TestConfigManagerSettings:
    """Tests for settings property."""
    
    def test_settings_property_loads_if_needed(self, tmp_path):
        """Test settings property loads if not cached."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"timeout_seconds": 77}))
        
        manager = ConfigManager(config_path=config_path)
        
        # Access settings property without calling load()
        settings = manager.settings
        
        assert settings.timeout_seconds == 77
    
    def test_settings_property_returns_cached(self, tmp_path):
        """Test settings property returns cached value."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"timeout_seconds": 55}))
        
        manager = ConfigManager(config_path=config_path)
        manager.load()
        
        # Modify file (shouldn't affect cached settings)
        config_path.write_text(json.dumps({"timeout_seconds": 99}))
        
        settings = manager.settings
        
        assert settings.timeout_seconds == 55


class TestConfigManagerResetToDefaults:
    """Tests for reset_to_defaults() method."""
    
    def test_reset_to_defaults(self, tmp_path):
        """Test resetting settings to defaults."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"base_url": "https://custom.com"}))
        
        manager = ConfigManager(config_path=config_path)
        manager.load()
        
        with patch('pywats_client.core.config_manager.SafeFileWriter') as mock_writer:
            mock_result = Mock()
            mock_result.success = True
            mock_writer.write_json_atomic.return_value = mock_result
            
            settings = manager.reset_to_defaults()
            
            # Should return default APISettings
            assert isinstance(settings, APISettings)
            # Should have saved
            mock_writer.write_json_atomic.assert_called_once()


class TestConfigManagerExists:
    """Tests for exists() method."""
    
    def test_exists_true(self, tmp_path):
        """Test exists returns True when file exists."""
        config_path = tmp_path / "config.json"
        config_path.write_text("{}")
        
        manager = ConfigManager(config_path=config_path)
        
        assert manager.exists() is True
    
    def test_exists_false(self, tmp_path):
        """Test exists returns False when file doesn't exist."""
        config_path = tmp_path / "nonexistent.json"
        
        manager = ConfigManager(config_path=config_path)
        
        assert manager.exists() is False


class TestLoadClientSettings:
    """Tests for load_client_settings convenience function."""
    
    def test_load_client_settings_default(self):
        """Test load_client_settings with default instance."""
        with patch.object(ConfigManager, 'load') as mock_load:
            mock_settings = APISettings()
            mock_load.return_value = mock_settings
            
            with patch.object(ConfigManager, '_get_default_config_path') as mock_path:
                mock_path.return_value = Path("/tmp/config.json")
                
                settings = load_client_settings()
                
                assert settings == mock_settings
    
    def test_load_client_settings_custom_instance(self):
        """Test load_client_settings with custom instance ID."""
        with patch.object(ConfigManager, 'load') as mock_load:
            mock_settings = APISettings()
            mock_load.return_value = mock_settings
            
            with patch.object(ConfigManager, '_get_default_config_path') as mock_path:
                mock_path.return_value = Path("/tmp/instances/custom/config.json")
                
                settings = load_client_settings(instance_id="custom")
                
                mock_path.assert_called_with("custom")


class TestConfigManagerRoundTrip:
    """Integration tests for save/load round trips."""
    
    def test_save_and_load_round_trip(self, tmp_path):
        """Test saving and loading settings preserves data."""
        config_path = tmp_path / "roundtrip.json"
        
        # Create settings with custom values
        original = APISettings(
            timeout_seconds=120,
            max_retries=5,
        )
        
        # Save
        manager1 = ConfigManager(config_path=config_path)
        manager1.save(original)
        
        # Load with new manager instance
        manager2 = ConfigManager(config_path=config_path)
        loaded = manager2.load()
        
        assert loaded.timeout_seconds == original.timeout_seconds
        assert loaded.max_retries == original.max_retries
    
    def test_modify_and_save(self, tmp_path):
        """Test modifying and saving settings."""
        config_path = tmp_path / "modify.json"
        config_path.write_text(json.dumps({"timeout_seconds": 30}))
        
        manager = ConfigManager(config_path=config_path)
        settings = manager.load()
        
        # Create new settings with modified value (Pydantic models are immutable by default)
        modified = APISettings(timeout_seconds=90)
        manager.save(modified)
        
        # Verify
        manager2 = ConfigManager(config_path=config_path)
        loaded = manager2.load()
        
        assert loaded.timeout_seconds == 90
