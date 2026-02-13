"""
Extended Unit Tests for ConverterConfig

Comprehensive tests for ConverterConfig covering areas not in test_config.py:
- Dict-like interface (get/set methods)
- Folder converter specific settings
- Post-processing configuration
- Priority validation
- Pattern handling (file_patterns, folder_patterns)
- Arguments dictionary handling
- Forward compatibility (unknown fields)
- Edge cases (empty strings, None values, boundaries)
- Metadata fields (version, description, author)

Author: Auto-generated for Task 1.6
Coverage Target: 90%+
"""

import pytest
from typing import Dict, Any
from pywats_client.core.config import ConverterConfig
from pywats_client.core.constants import ConverterType


class TestConverterConfigDictInterface:
    """Test dict-like get/set interface"""
    
    def test_get_existing_attribute(self):
        """Test get() returns existing attribute value"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            watch_folder="/test",
            priority=7
        )
        
        assert config.get("priority") == 7
        assert config.get("name") == "Test"
        assert config.get("watch_folder") == "/test"
    
    def test_get_with_default(self):
        """Test get() returns default for non-existent attribute"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.get("non_existent", "default_value") == "default_value"
        assert config.get("missing", 42) == 42
    
    def test_get_without_default_returns_none(self):
        """Test get() returns None when no default provided"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.get("non_existent") is None
    
    def test_set_existing_attribute(self):
        """Test set() updates existing attribute"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            priority=5
        )
        
        config.set("priority", 8)
        assert config.priority == 8
        
        config.set("name", "Updated Name")
        assert config.name == "Updated Name"
    
    def test_set_creates_new_attribute(self):
        """Test set() can create new attribute"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        config.set("custom_field", "custom_value")
        assert hasattr(config, "custom_field")
        assert config.custom_field == "custom_value"


class TestConverterConfigFolderSettings:
    """Test folder converter specific settings"""
    
    def test_default_readiness_marker(self):
        """Test default readiness_marker value"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.readiness_marker == "COMPLETE.marker"
    
    def test_custom_readiness_marker(self):
        """Test custom readiness_marker"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            readiness_marker="_READY"
        )
        
        assert config.readiness_marker == "_READY"
    
    def test_default_min_file_count_is_none(self):
        """Test default min_file_count is None"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.min_file_count is None
    
    def test_custom_min_file_count(self):
        """Test custom min_file_count"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            min_file_count=5
        )
        
        assert config.min_file_count == 5
    
    def test_folder_patterns_default(self):
        """Test default folder_patterns is ['*']"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.folder_patterns == ["*"]
    
    def test_custom_folder_patterns(self):
        """Test custom folder_patterns"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            folder_patterns=["TEST_*", "RESULT_*"]
        )
        
        assert config.folder_patterns == ["TEST_*", "RESULT_*"]


class TestConverterConfigPostProcessing:
    """Test post-processing configuration"""
    
    def test_default_post_action(self):
        """Test default post_action is 'move'"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.post_action == "move"
    
    def test_custom_post_action(self):
        """Test custom post_action values"""
        for action in ["move", "delete", "archive", "keep"]:
            config = ConverterConfig(
                name="Test",
                module_path="test.module",
                post_action=action
            )
            assert config.post_action == action
    
    def test_archive_folder_default(self):
        """Test default archive_folder is empty string"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.archive_folder == ""
    
    def test_custom_archive_folder(self):
        """Test custom archive_folder"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            post_action="archive",
            archive_folder="/archive/path"
        )
        
        assert config.archive_folder == "/archive/path"


class TestConverterConfigPriority:
    """Test priority configuration"""
    
    def test_default_priority(self):
        """Test default priority is 5"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.priority == 5
    
    def test_high_priority(self):
        """Test high priority (1 = highest)"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            priority=1
        )
        
        assert config.priority == 1
    
    def test_low_priority(self):
        """Test low priority (10 = lowest)"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            priority=10
        )
        
        assert config.priority == 10
    
    def test_mid_range_priority(self):
        """Test mid-range priority values"""
        for priority in [3, 5, 7]:
            config = ConverterConfig(
                name="Test",
                module_path="test.module",
                priority=priority
            )
            assert config.priority == priority


class TestConverterConfigFilePatterns:
    """Test file_patterns configuration"""
    
    def test_default_file_patterns(self):
        """Test default file_patterns is ['*.*']"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.file_patterns == ["*.*"]
    
    def test_single_file_pattern(self):
        """Test single file pattern"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            file_patterns=["*.csv"]
        )
        
        assert config.file_patterns == ["*.csv"]
    
    def test_multiple_file_patterns(self):
        """Test multiple file patterns"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            file_patterns=["*.csv", "*.txt", "*.log"]
        )
        
        assert config.file_patterns == ["*.csv", "*.txt", "*.log"]
    
    def test_empty_file_patterns_list(self):
        """Test empty file_patterns list"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            file_patterns=[]
        )
        
        assert config.file_patterns == []


class TestConverterConfigArguments:
    """Test arguments dictionary handling"""
    
    def test_default_arguments_is_empty_dict(self):
        """Test default arguments is empty dict"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.arguments == {}
    
    def test_custom_arguments(self):
        """Test custom arguments dict"""
        args = {
            "delimiter": ",",
            "encoding": "utf-8",
            "skip_header": True
        }
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            arguments=args
        )
        
        assert config.arguments == args
        assert config.arguments["delimiter"] == ","
        assert config.arguments["encoding"] == "utf-8"
        assert config.arguments["skip_header"] is True
    
    def test_arguments_with_nested_dict(self):
        """Test arguments with nested dictionary"""
        args = {
            "settings": {
                "timeout": 30,
                "retry": True
            }
        }
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            arguments=args
        )
        
        assert config.arguments["settings"]["timeout"] == 30
        assert config.arguments["settings"]["retry"] is True


class TestConverterConfigRetrySettings:
    """Test retry configuration"""
    
    def test_default_max_retries(self):
        """Test default max_retries is 3"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.max_retries == 3
    
    def test_custom_max_retries(self):
        """Test custom max_retries"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            max_retries=5
        )
        
        assert config.max_retries == 5
    
    def test_default_retry_delay_seconds(self):
        """Test default retry_delay_seconds is 60"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.retry_delay_seconds == 60
    
    def test_custom_retry_delay_seconds(self):
        """Test custom retry_delay_seconds"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            retry_delay_seconds=120
        )
        
        assert config.retry_delay_seconds == 120


class TestConverterConfigScheduledSettings:
    """Test scheduled converter settings"""
    
    def test_default_schedule_interval_is_none(self):
        """Test default schedule_interval_seconds is None"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.schedule_interval_seconds is None
    
    def test_custom_schedule_interval(self):
        """Test custom schedule_interval_seconds"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            converter_type="scheduled",
            schedule_interval_seconds=300
        )
        
        assert config.schedule_interval_seconds == 300
    
    def test_default_cron_expression_is_none(self):
        """Test default cron_expression is None"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.cron_expression is None
    
    def test_custom_cron_expression(self):
        """Test custom cron_expression"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            converter_type="scheduled",
            cron_expression="0 0 * * *"  # Daily at midnight
        )
        
        assert config.cron_expression == "0 0 * * *"
    
    def test_default_run_on_startup(self):
        """Test default run_on_startup is False"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.run_on_startup is False
    
    def test_run_on_startup_enabled(self):
        """Test run_on_startup enabled"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            converter_type="scheduled",
            schedule_interval_seconds=60,
            run_on_startup=True
        )
        
        assert config.run_on_startup is True


class TestConverterConfigMetadata:
    """Test metadata fields"""
    
    def test_default_version(self):
        """Test default version is '1.0.0'"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.version == "1.0.0"
    
    def test_custom_version(self):
        """Test custom version"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            version="2.5.3"
        )
        
        assert config.version == "2.5.3"
    
    def test_default_description(self):
        """Test default description is empty string"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.description == ""
    
    def test_custom_description(self):
        """Test custom description"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            description="This is a test converter"
        )
        
        assert config.description == "This is a test converter"
    
    def test_default_author(self):
        """Test default author is empty string"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.author == ""
    
    def test_custom_author(self):
        """Test custom author"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            author="John Doe"
        )
        
        assert config.author == "John Doe"


class TestConverterConfigStateManagement:
    """Test enabled state configuration"""
    
    def test_default_enabled_state(self):
        """Test default enabled state is True"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.enabled is True
    
    def test_disabled_state(self):
        """Test disabled state"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            enabled=False
        )
        
        assert config.enabled is False
    
    def test_toggle_enabled_state(self):
        """Test toggling enabled state"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.enabled is True
        config.enabled = False
        assert config.enabled is False
        config.enabled = True
        assert config.enabled is True


class TestConverterConfigFolderPaths:
    """Test folder path configuration"""
    
    def test_default_folders_are_empty(self):
        """Test default folder paths are empty strings"""
        config = ConverterConfig(name="Test", module_path="test.module")
        
        assert config.watch_folder == ""
        assert config.done_folder == ""
        assert config.error_folder == ""
        assert config.pending_folder == ""
    
    def test_custom_folder_paths(self):
        """Test custom folder paths"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            watch_folder="/watch",
            done_folder="/done",
            error_folder="/error",
            pending_folder="/pending"
        )
        
        assert config.watch_folder == "/watch"
        assert config.done_folder == "/done"
        assert config.error_folder == "/error"
        assert config.pending_folder == "/pending"


class TestConverterConfigForwardCompatibility:
    """Test forward compatibility with unknown fields"""
    
    def test_from_dict_ignores_unknown_fields(self):
        """Test from_dict ignores unknown fields for forward compatibility"""
        data = {
            "name": "Test",
            "module_path": "test.module",
            "watch_folder": "/test",
            "unknown_field_1": "value1",
            "future_feature": 42
        }
        
        config = ConverterConfig.from_dict(data)
        
        # Known fields should be set
        assert config.name == "Test"
        assert config.module_path == "test.module"
        assert config.watch_folder == "/test"
        
        # Unknown fields should be ignored (not raise error)
        assert not hasattr(config, "unknown_field_1")
        assert not hasattr(config, "future_feature")
    
    def test_to_dict_includes_all_fields(self):
        """Test to_dict includes all dataclass fields"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            watch_folder="/test"
        )
        
        result = config.to_dict()
        
        # Should include all dataclass fields
        assert "name" in result
        assert "module_path" in result
        assert "watch_folder" in result
        assert "enabled" in result
        assert "priority" in result
        assert "file_patterns" in result
        assert "arguments" in result


class TestConverterConfigEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_empty_name_string(self):
        """Test empty name string"""
        config = ConverterConfig(name="", module_path="test.module")
        
        errors = config.validate()
        assert any("name is required" in e for e in errors)
    
    def test_empty_module_path(self):
        """Test empty module_path string"""
        config = ConverterConfig(name="Test", module_path="")
        
        errors = config.validate()
        assert any("module_path is required" in e for e in errors)
    
    def test_very_long_name(self):
        """Test very long name (500+ characters)"""
        long_name = "A" * 500
        config = ConverterConfig(
            name=long_name,
            module_path="test.module"
        )
        
        assert config.name == long_name
    
    def test_very_long_module_path(self):
        """Test very long module_path"""
        long_path = "module." * 100 + "Converter"
        config = ConverterConfig(
            name="Test",
            module_path=long_path
        )
        
        assert config.module_path == long_path
    
    def test_threshold_exact_boundaries(self):
        """Test thresholds at exact boundaries"""
        # Test 0.0 (min)
        config1 = ConverterConfig(
            name="Test",
            module_path="test.module",
            watch_folder="/test",
            alarm_threshold=0.0,
            reject_threshold=0.0
        )
        assert config1.validate() == []
        
        # Test 1.0 (max)
        config2 = ConverterConfig(
            name="Test",
            module_path="test.module",
            watch_folder="/test",
            alarm_threshold=1.0,
            reject_threshold=1.0
        )
        assert config2.validate() == []
    
    def test_priority_boundaries(self):
        """Test priority at boundaries"""
        # Minimum priority (highest)
        config1 = ConverterConfig(
            name="Test",
            module_path="test.module",
            priority=1
        )
        assert config1.priority == 1
        
        # Maximum priority (lowest)
        config2 = ConverterConfig(
            name="Test",
            module_path="test.module",
            priority=10
        )
        assert config2.priority == 10
    
    def test_zero_retry_settings(self):
        """Test retry settings with zero values"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            max_retries=0,
            retry_delay_seconds=0
        )
        
        assert config.max_retries == 0
        assert config.retry_delay_seconds == 0
    
    def test_negative_retry_values(self):
        """Test negative retry values (allowed but unusual)"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            max_retries=-1,
            retry_delay_seconds=-10
        )
        
        assert config.max_retries == -1
        assert config.retry_delay_seconds == -10
    
    def test_special_characters_in_name(self):
        """Test special characters in name"""
        special_names = [
            "Test (Copy)",
            "Test [Version 2]",
            "Test & More",
            "Test @ Location",
            "Test #1"
        ]
        
        for name in special_names:
            config = ConverterConfig(
                name=name,
                module_path="test.module"
            )
            assert config.name == name
    
    def test_unicode_in_name(self):
        """Test unicode characters in name"""
        config = ConverterConfig(
            name="Tëst Çõnvérter 测试",
            module_path="test.module"
        )
        
        assert "Tëst" in config.name
        assert "测试" in config.name
    
    def test_whitespace_in_paths(self):
        """Test paths with whitespace"""
        config = ConverterConfig(
            name="Test",
            module_path="test.module",
            watch_folder="/path with spaces/folder",
            done_folder="/done folder/path",
            error_folder="/error  folder"
        )
        
        assert config.watch_folder == "/path with spaces/folder"
        assert config.done_folder == "/done folder/path"
        assert "  " in config.error_folder


class TestConverterConfigValidationIntegration:
    """Integration tests for combined validation scenarios"""
    
    def test_valid_file_converter_complete(self):
        """Test completely valid file converter config"""
        config = ConverterConfig(
            name="Production CSV Converter",
            module_path="converters.csv_converter.CSVConverter",
            converter_type="file",
            watch_folder="/data/csv",
            done_folder="/data/csv/done",
            error_folder="/data/csv/error",
            pending_folder="/data/csv/pending",
            enabled=True,
            priority=3,
            file_patterns=["*.csv", "*.txt"],
            alarm_threshold=0.6,
            reject_threshold=0.3,
            max_retries=5,
            retry_delay_seconds=120,
            post_action="move",
            description="Processes CSV test data files",
            author="Test Team",
            version="1.2.3"
        )
        
        errors = config.validate()
        assert len(errors) == 0
    
    def test_valid_folder_converter_complete(self):
        """Test completely valid folder converter config"""
        config = ConverterConfig(
            name="Batch Folder Converter",
            module_path="converters.folder_converter.FolderConverter",
            converter_type="folder",
            watch_folder="/data/batches",
            done_folder="/data/batches/done",
            error_folder="/data/batches/error",
            pending_folder="/data/batches/pending",
            folder_patterns=["BATCH_*", "TEST_*"],
            readiness_marker="complete.flag",
            min_file_count=3,
            post_action="archive",
            archive_folder="/archive",
            priority=5
        )
        
        errors = config.validate()
        assert len(errors) == 0
    
    def test_valid_scheduled_converter_with_interval(self):
        """Test valid scheduled converter with interval"""
        config = ConverterConfig(
            name="Hourly Report Converter",
            module_path="converters.scheduled.ReportConverter",
            converter_type="scheduled",
            schedule_interval_seconds=3600,
            run_on_startup=True,
            priority=7
        )
        
        errors = config.validate()
        assert len(errors) == 0
    
    def test_valid_scheduled_converter_with_cron(self):
        """Test valid scheduled converter with cron expression"""
        config = ConverterConfig(
            name="Daily Backup Converter",
            module_path="converters.scheduled.BackupConverter",
            converter_type="scheduled",
            cron_expression="0 2 * * *",  # 2 AM daily
            run_on_startup=False
        )
        
        errors = config.validate()
        assert len(errors) == 0
    
    def test_multiple_validation_errors(self):
        """Test config with multiple validation errors"""
        config = ConverterConfig(
            name="",  # Error: empty name
            module_path="",  # Error: empty module_path
            converter_type="file",
            watch_folder="",  # Error: missing for file converter
            alarm_threshold=1.5,  # Error: > 1.0
            reject_threshold=0.6,  # Error: > alarm_threshold (when fixed)
        )
        
        errors = config.validate()
        
        # Should have multiple errors
        assert len(errors) >= 3
        assert any("name" in e for e in errors)
        assert any("module_path" in e for e in errors)
        assert any("watch_folder" in e or "alarm_threshold" in e for e in errors)
