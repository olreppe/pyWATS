"""
Unit Tests for Client Configuration

Tests for pywats_client.core.config module covering:
- ConverterConfig dataclass
- ClientConfig dataclass
- Configuration loading and saving
- Validation logic
"""

import pytest
import json
from pathlib import Path
from pywats_client.core.config import ConverterConfig, ClientConfig


class TestConverterConfig:
    """Tests for ConverterConfig dataclass"""
    
    def test_create_converter_config(self, sample_converter_config):
        """Test creating a converter config from dict"""
        config = ConverterConfig.from_dict(sample_converter_config)
        
        assert config.name == "Test CSV Converter"
        assert config.module_path == "converters.csv_converter.CSVConverter"
        assert config.converter_type == "file"
        assert config.enabled is True
        assert config.alarm_threshold == 0.5
        assert config.reject_threshold == 0.2
    
    def test_converter_type_properties(self):
        """Test converter type detection properties"""
        file_conv = ConverterConfig(
            name="File", 
            module_path="test",
            converter_type="file",
            watch_folder="/test"
        )
        assert file_conv.is_file_converter is True
        assert file_conv.is_folder_converter is False
        assert file_conv.is_scheduled_converter is False
        
        folder_conv = ConverterConfig(
            name="Folder",
            module_path="test",
            converter_type="folder",
            watch_folder="/test"
        )
        assert folder_conv.is_file_converter is False
        assert folder_conv.is_folder_converter is True
        assert folder_conv.is_scheduled_converter is False
        
        scheduled_conv = ConverterConfig(
            name="Scheduled",
            module_path="test",
            converter_type="scheduled",
            schedule_interval_seconds=60
        )
        assert scheduled_conv.is_file_converter is False
        assert scheduled_conv.is_folder_converter is False
        assert scheduled_conv.is_scheduled_converter is True
    
    def test_validation_missing_required_fields(self):
        """Test validation catches missing required fields"""
        config = ConverterConfig(name="", module_path="")
        errors = config.validate()
        
        assert len(errors) > 0
        assert any("name is required" in e for e in errors)
        assert any("module_path is required" in e for e in errors)
    
    def test_validation_invalid_converter_type(self):
        """Test validation catches invalid converter type"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            converter_type="invalid_type"
        )
        errors = config.validate()
        
        assert any("Invalid converter_type" in e for e in errors)
    
    def test_validation_threshold_range(self):
        """Test threshold values are within valid range"""
        config = ConverterConfig(
            name="Test",
            module_path="test",
            converter_type="file",
            watch_folder="/test",
            alarm_threshold=1.5,  # Invalid: > 1.0
            reject_threshold=-0.1  # Invalid: < 0.0
        )
        errors = config.validate()
        
        assert any("alarm_threshold" in e for e in errors)
        assert any("reject_threshold" in e for e in errors)
    
    def test_validation_threshold_order(self):
        """Test reject_threshold must be <= alarm_threshold"""
        config = ConverterConfig(
            name="Test",
            module_path="test",
            converter_type="file",
            watch_folder="/test",
            alarm_threshold=0.3,
            reject_threshold=0.5  # Invalid: > alarm_threshold
        )
        errors = config.validate()
        
        assert any("reject_threshold must be <=" in e for e in errors)
    
    def test_validation_file_converter_needs_watch_folder(self):
        """Test file converter requires watch_folder"""
        config = ConverterConfig(
            name="Test",
            module_path="test",
            converter_type="file",
            watch_folder=""  # Missing
        )
        errors = config.validate()
        
        assert any("watch_folder is required" in e for e in errors)
    
    def test_validation_scheduled_converter_needs_schedule(self):
        """Test scheduled converter requires schedule config"""
        config = ConverterConfig(
            name="Test",
            module_path="test",
            converter_type="scheduled"
            # Missing schedule_interval_seconds and cron_expression
        )
        errors = config.validate()
        
        assert any("schedule" in e.lower() for e in errors)
    
    def test_to_dict_round_trip(self, sample_converter_config):
        """Test config can be serialized and deserialized"""
        config1 = ConverterConfig.from_dict(sample_converter_config)
        config_dict = config1.to_dict()
        config2 = ConverterConfig.from_dict(config_dict)
        
        assert config1.name == config2.name
        assert config1.module_path == config2.module_path
        assert config1.alarm_threshold == config2.alarm_threshold
    
    def test_default_values(self):
        """Test default values are set correctly"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            watch_folder="/test"
        )
        
        assert config.converter_type == "file"
        assert config.enabled is True
        assert config.max_retries == 3
        assert config.retry_delay_seconds == 60
        assert config.alarm_threshold == 0.5
        assert config.reject_threshold == 0.2
        assert config.post_action == "move"


class TestClientConfig:
    """Tests for ClientConfig dataclass"""
    
    def test_create_client_config(self, sample_config_dict):
        """Test creating client config from dict"""
        config = ClientConfig.from_dict(sample_config_dict)
        
        assert config.instance_id == "test-instance-001"
        assert config.instance_name == "Test Client"
        assert config.station_name == "Test Station"
        assert config.service_address == "https://wats.test.com"
        assert config.sync_interval_seconds == 60
        assert config.offline_queue_enabled is True
    
    def test_save_and_load_config(self, temp_dir, sample_config_dict):
        """Test saving and loading configuration file"""
        config_path = temp_dir / "test_config.json"
        
        # Create and save
        config1 = ClientConfig.from_dict(sample_config_dict)
        config1.save(str(config_path))
        
        # Load
        config2 = ClientConfig.load(str(config_path))
        
        assert config1.instance_id == config2.instance_id
        assert config1.station_name == config2.station_name
        assert config1.service_address == config2.service_address
    
    def test_load_or_create_existing(self, config_file):
        """Test load_or_create with existing file"""
        config = ClientConfig.load_or_create(str(config_file))
        
        assert config.instance_id == "test-instance-001"
        assert config.station_name == "Test Station"
    
    def test_load_or_create_new(self, temp_dir):
        """Test load_or_create creates new config if file doesn't exist"""
        config_path = temp_dir / "new_config.json"
        
        config = ClientConfig.load_or_create(str(config_path))
        
        # Should have default values
        assert config is not None
        assert isinstance(config.instance_id, str)
        assert len(config.converters) == 0
    
    def test_add_converter(self, sample_config_dict, sample_converter_config):
        """Test adding a converter to config"""
        config = ClientConfig.from_dict(sample_config_dict)
        converter = ConverterConfig.from_dict(sample_converter_config)
        
        config.converters.append(converter)
        
        assert len(config.converters) == 1
        assert config.converters[0].name == "Test CSV Converter"
    
    def test_invalid_json_raises_error(self, temp_dir):
        """Test loading invalid JSON raises error"""
        invalid_file = temp_dir / "invalid.json"
        invalid_file.write_text("{ invalid json ")
        
        with pytest.raises(json.JSONDecodeError):
            ClientConfig.load(str(invalid_file))
    
    def test_missing_file_raises_error(self, temp_dir):
        """Test loading non-existent file raises error"""
        missing_file = temp_dir / "missing.json"
        
        with pytest.raises(FileNotFoundError):
            ClientConfig.load(str(missing_file))


@pytest.mark.integration
class TestConfigIntegration:
    """Integration tests for configuration system"""
    
    def test_full_config_workflow(self, temp_dir, sample_converter_config):
        """Test complete config creation, modification, and save workflow"""
        config_path = temp_dir / "workflow_test.json"
        
        # 1. Create new config
        config = ClientConfig.load_or_create(str(config_path))
        config.station_name = "Integration Test Station"
        
        # 2. Add converter
        converter = ConverterConfig.from_dict(sample_converter_config)
        config.converters.append(converter)
        
        # 3. Save
        config.save(str(config_path))
        
        # 4. Load fresh instance
        loaded = ClientConfig.load(str(config_path))
        
        # 5. Verify
        assert loaded.station_name == "Integration Test Station"
        assert len(loaded.converters) == 1
        assert loaded.converters[0].name == "Test CSV Converter"
        
        # 6. Validate converter
        errors = loaded.converters[0].validate()
        assert len(errors) == 0, f"Converter has errors: {errors}"
