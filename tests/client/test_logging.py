"""
Tests for client logging infrastructure.

Tests the pyWATS client logging utilities including:
- setup_client_logging() function
- get_client_log_path() function
- get_conversion_log_dir() function  
- cleanup_old_conversion_logs() function
"""

import logging
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pywats_client.core.logging import (
    setup_client_logging,
    get_client_log_path,
    get_conversion_log_dir,
    cleanup_old_conversion_logs,
)


class TestSetupClientLogging:
    """Tests for setup_client_logging() function."""
    
    def setup_method(self):
        """Reset logging configuration before each test."""
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.setLevel(logging.WARNING)
    
    def teardown_method(self):
        """Clean up after each test."""
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.setLevel(logging.WARNING)
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_setup_creates_log_file(self, mock_get_path):
        """Test setup_client_logging creates log file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pywats.log"
            mock_get_path.return_value = log_path
            
            result = setup_client_logging(instance_id="test", log_level="INFO")
            
            assert result == log_path
            assert log_path.exists()
            
            # Clean up handlers
            for handler in logging.getLogger().handlers[:]:
                handler.close()
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_setup_with_console_enabled(self, mock_get_path):
        """Test setup with console output enabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pywats.log"
            mock_get_path.return_value = log_path
            
            setup_client_logging(instance_id="test", enable_console=True)
            
            root_logger = logging.getLogger()
            
            # Should have 2 handlers (file + console)
            assert len(root_logger.handlers) >= 2
            
            # Clean up
            for handler in root_logger.handlers[:]:
                handler.close()
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_setup_with_console_disabled(self, mock_get_path):
        """Test setup with console output disabled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pywats.log"
            mock_get_path.return_value = log_path
            
            setup_client_logging(instance_id="test", enable_console=False)
            
            root_logger = logging.getLogger()
            
            # Should have 1 handler (file only)
            # Note: May have pytest handlers too
            file_handlers = [h for h in root_logger.handlers if hasattr(h, 'baseFilename')]
            assert len(file_handlers) >= 1
            
            # Clean up
            for handler in root_logger.handlers[:]:
                handler.close()
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_setup_with_different_log_levels(self, mock_get_path):
        """Test setup with different log levels."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pywats.log"
            mock_get_path.return_value = log_path
            
            for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
                setup_client_logging(instance_id="test", log_level=level)
                
                root_logger = logging.getLogger()
                assert root_logger.level == getattr(logging, level)
                
                # Clean up
                for handler in root_logger.handlers[:]:
                    handler.close()
                root_logger.handlers.clear()
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_setup_with_json_format(self, mock_get_path):
        """Test setup with JSON format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pywats.log"
            mock_get_path.return_value = log_path
            
            setup_client_logging(instance_id="test", log_format="json")
            
            root_logger = logging.getLogger()
            
            # Check that handler has StructuredFormatter
            file_handlers = [h for h in root_logger.handlers if hasattr(h, 'baseFilename')]
            assert len(file_handlers) >= 1
            
            formatter = file_handlers[0].formatter
            assert formatter is not None
            assert formatter.__class__.__name__ == 'StructuredFormatter'
            
            # Clean up
            for handler in root_logger.handlers[:]:
                handler.close()
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_setup_logs_startup_message(self, mock_get_path):
        """Test setup logs startup message."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pywats.log"
            mock_get_path.return_value = log_path
            
            setup_client_logging(instance_id="test", log_level="INFO")
            
            # Flush handlers
            for handler in logging.getLogger().handlers:
                handler.flush()
                handler.close()
            
            # Check log file contains startup message
            content = log_path.read_text()
            assert "Client logging configured" in content
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_setup_with_custom_rotation(self, mock_get_path):
        """Test setup with custom rotation settings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pywats.log"
            mock_get_path.return_value = log_path
            
            setup_client_logging(
                instance_id="test",
                rotate_size_mb=5,
                rotate_backups=3
            )
            
            root_logger = logging.getLogger()
            file_handlers = [h for h in root_logger.handlers if hasattr(h, 'baseFilename')]
            
            assert len(file_handlers) >= 1
            handler = file_handlers[0]
            
            # Check rotation settings
            assert handler.maxBytes == 5 * 1024 * 1024
            assert handler.backupCount == 3
            
            # Clean up
            for h in root_logger.handlers[:]:
                h.close()


class TestGetClientLogPath:
    """Tests for get_client_log_path() function."""
    
    @patch('pywats_client.core.config.ClientConfig')
    def test_uses_client_config_when_available(self, mock_config_class):
        """Test uses ClientConfig to determine path."""
        # Mock config
        mock_config = Mock()
        mock_reports_path = Path("/test/reports")
        mock_config.get_reports_path.return_value = mock_reports_path
        mock_config_class.load_for_instance.return_value = mock_config
        
        result = get_client_log_path("test_instance")
        
        # Should use parent of reports path
        expected = mock_reports_path.parent / "pywats.log"
        assert result == expected
        
        mock_config_class.load_for_instance.assert_called_once_with("test_instance")
    
    @patch('pywats_client.core.config.ClientConfig')
    def test_fallback_when_config_unavailable(self, mock_config_class):
        """Test falls back when config unavailable."""
        # Mock config to raise exception
        mock_config_class.load_for_instance.side_effect = Exception("Config not found")
        
        # Should not crash and should return a valid path
        result = get_client_log_path("test")
        
        assert result is not None
        assert isinstance(result, Path)
        assert result.name == "pywats.log"
        assert "test" in str(result)  # Should include instance_id


class TestGetConversionLogDir:
    """Tests for get_conversion_log_dir() function."""
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_returns_conversions_subdirectory(self, mock_get_path):
        """Test returns logs/conversions subdirectory."""
        mock_get_path.return_value = Path("/test/install/pywats.log")
        
        result = get_conversion_log_dir("test")
        
        expected = Path("/test/install/logs/conversions")
        assert result == expected
    
    @patch('pywats_client.core.logging.get_client_log_path')
    def test_creates_directory_if_not_exists(self, mock_get_path):
        """Test creates directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "pywats.log"
            mock_get_path.return_value = log_path
            
            result = get_conversion_log_dir("test")
            
            # Directory should exist
            assert result.exists()
            assert result.is_dir()
            
            # Should be logs/conversions
            assert result.name == "conversions"
            assert result.parent.name == "logs"


class TestCleanupOldConversionLogs:
    """Tests for cleanup_old_conversion_logs() function."""
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_cleanup_dry_run(self, mock_get_dir):
        """Test cleanup in dry-run mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            conversion_dir = Path(tmpdir) / "conversions"
            conversion_dir.mkdir()
            mock_get_dir.return_value = conversion_dir
            
            # Create old log file
            old_log = conversion_dir / "old.log"
            old_log.write_text("old content")
            
            # Set modification time to 35 days ago
            old_time = (datetime.now() - timedelta(days=35)).timestamp()
            import os
            os.utime(old_log, (old_time, old_time))
            
            # Dry run should not delete
            count = cleanup_old_conversion_logs(instance_id="test", max_age_days=30, dry_run=True)
            
            assert count == 1
            assert old_log.exists()  # File still exists
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_cleanup_deletes_old_files(self, mock_get_dir):
        """Test cleanup deletes files older than max_age."""
        with tempfile.TemporaryDirectory() as tmpdir:
            conversion_dir = Path(tmpdir) / "conversions"
            conversion_dir.mkdir()
            mock_get_dir.return_value = conversion_dir
            
            # Create old log file
            old_log = conversion_dir / "old.log"
            old_log.write_text("old content")
            
            # Set modification time to 35 days ago
            old_time = (datetime.now() - timedelta(days=35)).timestamp()
            import os
            os.utime(old_log, (old_time, old_time))
            
            # Real cleanup should delete
            count = cleanup_old_conversion_logs(instance_id="test", max_age_days=30)
            
            assert count == 1
            assert not old_log.exists()  # File deleted
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_cleanup_keeps_recent_files(self, mock_get_dir):
        """Test cleanup keeps files newer than max_age."""
        with tempfile.TemporaryDirectory() as tmpdir:
            conversion_dir = Path(tmpdir) / "conversions"
            conversion_dir.mkdir()
            mock_get_dir.return_value = conversion_dir
            
            # Create recent log file
            recent_log = conversion_dir / "recent.log"
            recent_log.write_text("recent content")
            
            # Cleanup should not delete recent files
            count = cleanup_old_conversion_logs(instance_id="test", max_age_days=30)
            
            assert count == 0
            assert recent_log.exists()  # File still exists
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_cleanup_with_no_directory(self, mock_get_dir):
        """Test cleanup when directory doesn't exist."""
        mock_get_dir.return_value = Path("/nonexistent/dir")
        
        # Should not crash
        count = cleanup_old_conversion_logs(instance_id="test")
        
        assert count == 0
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_cleanup_handles_exceptions(self, mock_get_dir):
        """Test cleanup handles file access errors gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            conversion_dir = Path(tmpdir) / "conversions"
            conversion_dir.mkdir()
            mock_get_dir.return_value = conversion_dir
            
            # Create log file
            log_file = conversion_dir / "test.log"
            log_file.write_text("content")
            
            # Set old time
            old_time = (datetime.now() - timedelta(days=35)).timestamp()
            import os
            os.utime(log_file, (old_time, old_time))
            
            # Mock unlink to raise exception
            with patch.object(Path, 'unlink', side_effect=PermissionError("Access denied")):
                # Should not crash, just log warning
                count = cleanup_old_conversion_logs(instance_id="test", max_age_days=30)
                
                # No files deleted due to error
                assert count == 0
    
    @patch('pywats_client.core.logging.get_conversion_log_dir')
    def test_cleanup_only_processes_log_files(self, mock_get_dir):
        """Test cleanup only processes .log files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            conversion_dir = Path(tmpdir) / "conversions"
            conversion_dir.mkdir()
            mock_get_dir.return_value = conversion_dir
            
            # Create old files with different extensions
            old_log = conversion_dir / "old.log"
            old_log.write_text("log")
            
            old_txt = conversion_dir / "old.txt"
            old_txt.write_text("txt")
            
            # Set both to old time
            old_time = (datetime.now() - timedelta(days=35)).timestamp()
            import os
            os.utime(old_log, (old_time, old_time))
            os.utime(old_txt, (old_time, old_time))
            
            # Cleanup should only process .log files
            count = cleanup_old_conversion_logs(instance_id="test", max_age_days=30)
            
            assert count == 1
            assert not old_log.exists()  # .log deleted
            assert old_txt.exists()  # .txt kept
