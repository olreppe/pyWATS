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
        """Test loading invalid JSON raises error when no backup available"""
        invalid_file = temp_dir / "invalid.json"
        invalid_file.write_text("{ invalid json ")
        
        # With safe file handling, corrupted files raise IOError 
        # (after trying backup recovery)
        with pytest.raises((IOError, OSError)):
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


class TestConfigValidation:
    """Tests for ClientConfig validation and repair methods"""
    
    def test_validate_default_config_valid(self):
        """Default config should be valid"""
        config = ClientConfig()
        errors = config.validate()
        assert len(errors) == 0, f"Default config has errors: {errors}"
    
    def test_validate_negative_sync_interval(self):
        """Negative sync_interval_seconds should fail validation"""
        config = ClientConfig()
        config.sync_interval_seconds = -1
        errors = config.validate()
        assert "sync_interval_seconds must be non-negative" in errors
    
    def test_validate_negative_retry_attempts(self):
        """Negative max_retry_attempts should fail validation"""
        config = ClientConfig()
        config.max_retry_attempts = -5
        errors = config.validate()
        assert "max_retry_attempts must be non-negative" in errors
    
    def test_validate_invalid_proxy_port(self):
        """Invalid proxy_port should fail validation"""
        config = ClientConfig()
        config.proxy_port = 99999
        errors = config.validate()
        assert "proxy_port must be between 0 and 65535" in errors
    
    def test_validate_invalid_yield_threshold_high(self):
        """yield_threshold > 100 should fail validation"""
        config = ClientConfig()
        config.yield_threshold = 150.0
        errors = config.validate()
        assert "yield_threshold must be between 0.0 and 100.0" in errors
    
    def test_validate_invalid_yield_threshold_low(self):
        """yield_threshold < 0 should fail validation"""
        config = ClientConfig()
        config.yield_threshold = -10.0
        errors = config.validate()
        assert "yield_threshold must be between 0.0 and 100.0" in errors
    
    def test_validate_invalid_log_level(self):
        """Invalid log_level should fail validation"""
        config = ClientConfig()
        config.log_level = "INVALID"
        errors = config.validate()
        assert any("log_level" in e for e in errors)
    
    def test_validate_invalid_station_name_source(self):
        """Invalid station_name_source should fail validation"""
        config = ClientConfig()
        config.station_name_source = "invalid_source"
        errors = config.validate()
        assert any("station_name_source" in e for e in errors)
    
    def test_validate_invalid_proxy_mode(self):
        """Invalid proxy_mode should fail validation"""
        config = ClientConfig()
        config.proxy_mode = "invalid_mode"
        errors = config.validate()
        assert any("proxy_mode" in e for e in errors)
    
    def test_is_valid_returns_boolean(self):
        """is_valid should return True/False"""
        config = ClientConfig()
        assert config.is_valid() is True
        
        config.sync_interval_seconds = -1
        assert config.is_valid() is False
    
    def test_repair_negative_sync_interval(self):
        """repair() should fix negative sync_interval_seconds"""
        config = ClientConfig()
        config.sync_interval_seconds = -100
        
        repairs = config.repair()
        
        assert config.sync_interval_seconds == 300
        assert any("sync_interval_seconds" in r for r in repairs)
    
    def test_repair_invalid_proxy_port(self):
        """repair() should fix invalid proxy_port"""
        config = ClientConfig()
        config.proxy_port = 100000
        
        repairs = config.repair()
        
        assert config.proxy_port == 8080
        assert any("proxy_port" in r for r in repairs)
    
    def test_repair_yield_threshold_too_high(self):
        """repair() should clamp yield_threshold > 100"""
        config = ClientConfig()
        config.yield_threshold = 200.0
        
        repairs = config.repair()
        
        assert config.yield_threshold == 100.0
        assert any("yield_threshold" in r for r in repairs)
    
    def test_repair_yield_threshold_too_low(self):
        """repair() should fix yield_threshold < 0"""
        config = ClientConfig()
        config.yield_threshold = -50.0
        
        repairs = config.repair()
        
        assert config.yield_threshold == 0.0
        assert any("yield_threshold" in r for r in repairs)
    
    def test_repair_invalid_log_level(self):
        """repair() should fix invalid log_level"""
        config = ClientConfig()
        config.log_level = "GARBAGE"
        
        repairs = config.repair()
        
        assert config.log_level == "INFO"
        assert any("log_level" in r for r in repairs)
    
    def test_repair_multiple_issues(self):
        """repair() should fix multiple issues"""
        config = ClientConfig()
        config.sync_interval_seconds = -1
        config.proxy_port = -5
        config.log_level = "INVALID"
        
        repairs = config.repair()
        
        assert len(repairs) == 3
        assert config.sync_interval_seconds == 300
        assert config.proxy_port == 8080
        assert config.log_level == "INFO"
    
    def test_repair_valid_config_no_changes(self):
        """repair() on valid config should make no changes"""
        config = ClientConfig()
        repairs = config.repair()
        assert len(repairs) == 0
    
    def test_load_and_repair_corrupt_config(self, temp_dir):
        """load_and_repair should create default config if load fails"""
        bad_file = temp_dir / "corrupt.json"
        bad_file.write_text("this is not json")
        
        config, repairs = ClientConfig.load_and_repair(bad_file)
        
        # Should get a default config
        assert config is not None
        assert config.is_valid()
    
    def test_load_and_repair_valid_config(self, temp_dir):
        """load_and_repair should load and not repair valid config"""
        config_path = temp_dir / "valid.json"
        
        # Create and save a valid config
        original = ClientConfig()
        original.station_name = "Test Station"
        original.save(str(config_path))
        
        # Load and repair
        loaded, repairs = ClientConfig.load_and_repair(config_path)
        
        assert loaded.station_name == "Test Station"
        assert len(repairs) == 0


class TestConfigSchemaVersioning:
    """Tests for config schema versioning"""
    
    def test_default_schema_version(self):
        """New configs should have current schema version"""
        config = ClientConfig()
        assert config.schema_version == "2.0"
        assert config.schema_version == ClientConfig.CURRENT_SCHEMA_VERSION
    
    def test_schema_version_in_saved_config(self, temp_dir):
        """Saved config should include schema_version"""
        config_path = temp_dir / "schema_test.json"
        
        config = ClientConfig()
        config.save(str(config_path))
        
        # Read the raw JSON
        import json
        with open(config_path) as f:
            data = json.load(f)
        
        assert "schema_version" in data
        assert data["schema_version"] == "2.0"
    
    def test_schema_version_constants(self):
        """Schema version constants should be defined"""
        assert ClientConfig.CURRENT_SCHEMA_VERSION == "2.0"
        assert ClientConfig.MIN_SCHEMA_VERSION == "1.0"
    
    def test_parse_version(self):
        """Version parsing should work correctly"""
        assert ClientConfig._parse_version("2.0") == (2, 0)
        assert ClientConfig._parse_version("1.5") == (1, 5)
        assert ClientConfig._parse_version("10.20") == (10, 20)
        assert ClientConfig._parse_version("invalid") == (0, 0)
    
    def test_schema_version_compatibility_same(self):
        """Same version should be compatible"""
        config = ClientConfig()
        assert config._is_schema_version_compatible("2.0") is True
    
    def test_schema_version_compatibility_older_supported(self):
        """Older supported versions should be compatible"""
        config = ClientConfig()
        assert config._is_schema_version_compatible("1.0") is True
        assert config._is_schema_version_compatible("1.5") is True
    
    def test_schema_version_compatibility_too_old(self):
        """Versions below minimum should not be compatible"""
        config = ClientConfig()
        assert config._is_schema_version_compatible("0.5") is False
        assert config._is_schema_version_compatible("0.0") is False
    
    def test_schema_version_compatibility_future(self):
        """Future major versions should not be compatible"""
        config = ClientConfig()
        assert config._is_schema_version_compatible("3.0") is False
        assert config._is_schema_version_compatible("10.0") is False
    
    def test_validate_schema_version_invalid(self):
        """Validation should fail for unsupported schema versions"""
        config = ClientConfig()
        config.schema_version = "0.5"  # Below minimum
        
        errors = config.validate()
        assert any("schema_version" in e for e in errors)
    
    def test_repair_upgrades_old_schema_version(self):
        """repair() should upgrade old schema versions"""
        config = ClientConfig()
        config.schema_version = "1.0"
        
        repairs = config.repair()
        
        assert config.schema_version == "2.0"
        assert any("schema_version" in r for r in repairs)
    
    def test_load_old_config_without_schema_version(self, temp_dir):
        """Loading config without schema_version should work and set default"""
        import json
        
        config_path = temp_dir / "old_config.json"
        
        # Create config file without schema_version (simulating old format)
        old_data = {
            "instance_id": "test",
            "instance_name": "Old Config",
            "station_name": "Test Station"
        }
        with open(config_path, 'w') as f:
            json.dump(old_data, f)
        
        # Load - should work and get default schema_version
        config = ClientConfig.load(str(config_path))
        
        # Schema version should be default (2.0 in dataclass)
        assert config.schema_version == "2.0"
        assert config.instance_name == "Old Config"
    
    def test_load_and_repair_upgrades_schema(self, temp_dir):
        """load_and_repair should upgrade schema version of old configs"""
        import json
        
        config_path = temp_dir / "upgrade_test.json"
        
        # Create config file with old schema_version
        old_data = {
            "schema_version": "1.0",
            "instance_id": "test",
            "station_name": "Old Station"
        }
        with open(config_path, 'w') as f:
            json.dump(old_data, f)
        
        # Load and repair
        config, repairs = ClientConfig.load_and_repair(config_path)
        
        assert config.schema_version == "2.0"
        assert any("schema_version" in r for r in repairs)


class TestQueueConfigFields:
    """Tests for queue configuration fields"""
    
    def test_default_max_queue_size(self):
        """Test default max_queue_size value"""
        config = ClientConfig()
        assert config.max_queue_size == 10000
    
    def test_default_max_concurrent_uploads(self):
        """Test default max_concurrent_uploads value"""
        config = ClientConfig()
        assert config.max_concurrent_uploads == 5
    
    def test_custom_queue_settings(self):
        """Test custom queue settings"""
        config = ClientConfig(
            max_queue_size=5000,
            max_concurrent_uploads=10
        )
        assert config.max_queue_size == 5000
        assert config.max_concurrent_uploads == 10
    
    def test_queue_settings_in_to_dict(self):
        """Test that queue settings are included in to_dict"""
        config = ClientConfig(
            max_queue_size=1000,
            max_concurrent_uploads=3
        )
        data = config.to_dict()
        
        assert data["max_queue_size"] == 1000
        assert data["max_concurrent_uploads"] == 3
    
    def test_queue_settings_round_trip(self, temp_dir):
        """Test queue settings survive save/load cycle"""
        config = ClientConfig(
            instance_id="queue_test",
            max_queue_size=2000,
            max_concurrent_uploads=8
        )
        
        # Save
        config_path = temp_dir / "queue_config.json"
        config.save(str(config_path))
        
        # Load
        loaded = ClientConfig.load(str(config_path))
        
        assert loaded.max_queue_size == 2000
        assert loaded.max_concurrent_uploads == 8
    
    def test_unlimited_queue_size(self):
        """Test that 0 means unlimited queue"""
        config = ClientConfig(max_queue_size=0)
        assert config.max_queue_size == 0
