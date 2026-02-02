"""Unit tests for ServiceManager.

Tests cross-platform service management functionality including:
- Platform detection
- Process detection using psutil
- Lock file management
- Status reporting
"""

import platform
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import psutil
import pytest

from pywats_client.service_manager import ServiceManager


class TestServiceManagerInit:
    """Test ServiceManager initialization."""
    
    def test_init_default_instance(self):
        """Test initialization with default instance ID."""
        manager = ServiceManager()
        
        assert manager.instance_id == "default"
        assert manager.platform == platform.system()
        assert manager.lock_dir == Path(tempfile.gettempdir()) / "pyWATS_Client"
    
    def test_init_custom_instance(self):
        """Test initialization with custom instance ID."""
        manager = ServiceManager("test-instance")
        
        assert manager.instance_id == "test-instance"
        assert "test-instance" in manager.service_name
    
    def test_lock_dir_created(self):
        """Test that lock directory is created on init."""
        manager = ServiceManager("test-dir-creation")
        
        assert manager.lock_dir.exists()
        assert manager.lock_dir.is_dir()
    
    def test_lock_file_property(self):
        """Test lock file path property."""
        manager = ServiceManager("test-lock")
        
        expected_path = manager.lock_dir / "instance_test-lock.lock"
        assert manager.lock_file == expected_path
    
    def test_service_name_windows(self):
        """Test Windows service name format."""
        with patch('platform.system', return_value='Windows'):
            manager = ServiceManager("test-win")
            assert manager.service_name == "pyWATS-Client-test-win"
    
    def test_service_name_linux(self):
        """Test Linux service name format."""
        with patch('platform.system', return_value='Linux'):
            manager = ServiceManager("test-linux")
            assert manager.service_name == "pywats-client@test-linux"
    
    def test_service_name_macos(self):
        """Test macOS service name format."""
        with patch('platform.system', return_value='Darwin'):
            manager = ServiceManager("test-mac")
            assert manager.service_name == "com.wats.pywats-client.test-mac"


class TestIsRunning:
    """Test service running detection."""
    
    def test_is_running_no_processes(self):
        """Test is_running when no matching processes exist."""
        manager = ServiceManager("test-not-running")
        
        # Mock process_iter to return no matching processes
        mock_processes = [
            Mock(info={'pid': 1234, 'name': 'python', 'cmdline': ['python', 'other_script.py']}),
            Mock(info={'pid': 5678, 'name': 'notepad', 'cmdline': ['notepad.exe']}),
        ]
        
        with patch('psutil.process_iter', return_value=mock_processes):
            assert not manager.is_running()
    
    def test_is_running_matching_process(self):
        """Test is_running when matching process exists."""
        manager = ServiceManager("test-running")
        
        # Mock process_iter with matching process
        mock_processes = [
            Mock(info={'pid': 1234, 'name': 'python', 'cmdline': ['python', '-m', 'pywats_client', '--instance-id', 'test-running']}),
        ]
        
        with patch('psutil.process_iter', return_value=mock_processes):
            assert manager.is_running()
    
    def test_is_running_default_instance(self):
        """Test is_running for default instance matches any pywats_client."""
        manager = ServiceManager("default")
        
        # Mock process with pywats_client but no instance-id
        mock_processes = [
            Mock(info={'pid': 1234, 'name': 'python', 'cmdline': ['python', '-m', 'pywats_client']}),
        ]
        
        with patch('psutil.process_iter', return_value=mock_processes):
            assert manager.is_running()
    
    def test_is_running_handles_access_denied(self):
        """Test is_running handles AccessDenied exception."""
        manager = ServiceManager("test-access-denied")
        
        # Mock process that raises AccessDenied
        mock_proc = Mock()
        mock_proc.info.get.side_effect = psutil.AccessDenied()
        
        with patch('psutil.process_iter', return_value=[mock_proc]):
            # Should not crash, should return False
            assert not manager.is_running()
    
    def test_is_running_handles_no_such_process(self):
        """Test is_running handles NoSuchProcess exception."""
        manager = ServiceManager("test-no-such")
        
        # Mock process that raises NoSuchProcess
        mock_proc = Mock()
        mock_proc.info.get.side_effect = psutil.NoSuchProcess(1234)
        
        with patch('psutil.process_iter', return_value=[mock_proc]):
            # Should not crash, should return False
            assert not manager.is_running()


class TestGetPid:
    """Test PID retrieval."""
    
    def test_get_pid_no_process(self):
        """Test get_pid when no process running."""
        manager = ServiceManager("test-no-pid")
        
        with patch('psutil.process_iter', return_value=[]):
            assert manager.get_pid() is None
    
    def test_get_pid_with_process(self):
        """Test get_pid when process is running."""
        manager = ServiceManager("test-with-pid")
        
        mock_processes = [
            Mock(info={'pid': 9876, 'name': 'python', 'cmdline': ['python', '-m', 'pywats_client', '--instance-id', 'test-with-pid']}),
        ]
        
        with patch('psutil.process_iter', return_value=mock_processes):
            assert manager.get_pid() == 9876


class TestGetStatus:
    """Test status reporting."""
    
    def test_get_status_not_running(self):
        """Test get_status when service not running."""
        manager = ServiceManager("test-status-stopped")
        
        with patch('psutil.process_iter', return_value=[]):
            status = manager.get_status()
            
            assert status['running'] is False
            assert status['pid'] is None
            assert status['uptime'] is None
            assert status['instance_id'] == "test-status-stopped"
            assert status['platform'] == platform.system()
            assert 'log_file' in status
    
    def test_get_status_running(self):
        """Test get_status when service is running."""
        manager = ServiceManager("test-status-running")
        
        # Mock running process
        mock_process = Mock(spec=psutil.Process)
        mock_process.create_time.return_value = time.time() - 120  # 2 minutes ago
        
        mock_processes = [
            Mock(info={'pid': 1111, 'name': 'python', 'cmdline': ['python', '-m', 'pywats_client', '--instance-id', 'test-status-running']}),
        ]
        
        with patch('psutil.process_iter', return_value=mock_processes):
            with patch('psutil.Process', return_value=mock_process):
                status = manager.get_status()
                
                assert status['running'] is True
                assert status['pid'] == 1111
                assert status['uptime'] is not None
                assert 115 < status['uptime'] < 125  # ~120 seconds with tolerance
    
    def test_get_status_includes_platform(self):
        """Test that status includes platform information."""
        manager = ServiceManager("test-platform")
        
        with patch('psutil.process_iter', return_value=[]):
            status = manager.get_status()
            
            assert status['platform'] in ['Windows', 'Linux', 'Darwin']


class TestCleanStaleLocks:
    """Test stale lock file cleanup."""
    
    def test_clean_stale_locks_no_locks(self, tmp_path):
        """Test cleanup when no lock files exist."""
        manager = ServiceManager("test-no-locks")
        manager.lock_dir = tmp_path  # Use temp dir for testing
        
        removed = manager.clean_stale_locks()
        assert removed == 0
    
    def test_clean_stale_locks_running_process(self, tmp_path):
        """Test cleanup doesn't remove locks for running processes."""
        manager = ServiceManager("test-running-lock")
        manager.lock_dir = tmp_path
        
        # Create lock file with current process PID (should not be removed)
        import os
        lock_file = tmp_path / "instance_test.lock"
        lock_file.write_text(str(os.getpid()))
        
        removed = manager.clean_stale_locks()
        assert removed == 0
        assert lock_file.exists()
    
    def test_clean_stale_locks_dead_process(self, tmp_path):
        """Test cleanup removes locks for dead processes."""
        manager = ServiceManager("test-dead-lock")
        manager.lock_dir = tmp_path
        
        # Create lock file with impossible PID
        lock_file = tmp_path / "instance_test.lock"
        lock_file.write_text("999999")
        
        removed = manager.clean_stale_locks()
        assert removed == 1
        assert not lock_file.exists()
    
    def test_clean_stale_locks_multiple_files(self, tmp_path):
        """Test cleanup with multiple lock files."""
        manager = ServiceManager("test-multi-locks")
        manager.lock_dir = tmp_path
        
        # Create multiple lock files with dead PIDs
        for i in range(3):
            lock_file = tmp_path / f"instance_test{i}.lock"
            lock_file.write_text(str(999990 + i))
        
        removed = manager.clean_stale_locks()
        assert removed == 3
    
    def test_clean_stale_locks_invalid_content(self, tmp_path):
        """Test cleanup handles invalid lock file content."""
        manager = ServiceManager("test-invalid-lock")
        manager.lock_dir = tmp_path
        
        # Create lock file with non-numeric content
        lock_file = tmp_path / "instance_test.lock"
        lock_file.write_text("not-a-number")
        
        # Should not crash, should skip invalid files
        removed = manager.clean_stale_locks()
        assert removed == 0
        assert lock_file.exists()  # Invalid file not removed


class TestServiceControl:
    """Test service start/stop/restart methods."""
    
    def test_start_already_running(self):
        """Test start when service already running."""
        manager = ServiceManager("test-start-running")
        
        mock_processes = [
            Mock(info={'pid': 1234, 'name': 'python', 'cmdline': ['python', '-m', 'pywats_client', '--instance-id', 'test-start-running']}),
        ]
        
        with patch('psutil.process_iter', return_value=mock_processes):
            result = manager.start()
            assert result is False
    
    def test_stop_not_running(self):
        """Test stop when service not running."""
        manager = ServiceManager("test-stop-not-running")
        
        with patch('psutil.process_iter', return_value=[]):
            result = manager.stop()
            assert result is False
    
    def test_restart_calls_stop_then_start(self):
        """Test restart calls stop then start."""
        manager = ServiceManager("test-restart")
        
        with patch.object(manager, 'is_running', side_effect=[True, False, False]):
            with patch.object(manager, 'stop', return_value=True) as mock_stop:
                with patch.object(manager, 'start', return_value=True) as mock_start:
                    result = manager.restart()
                    
                    assert result is True
                    mock_stop.assert_called_once()
                    mock_start.assert_called_once()
    
    def test_restart_not_running_just_starts(self):
        """Test restart when not running just calls start."""
        manager = ServiceManager("test-restart-not-running")
        
        with patch.object(manager, 'is_running', return_value=False):
            with patch.object(manager, 'start', return_value=True) as mock_start:
                result = manager.restart()
                
                assert result is True
                mock_start.assert_called_once()


class TestPlatformSpecificMethods:
    """Test platform-specific start/stop methods."""
    
    def test_start_windows_uses_sc(self):
        """Test Windows start tries sc command first."""
        with patch('platform.system', return_value='Windows'):
            manager = ServiceManager("test-win-start")
            
            # Mock sc command success
            mock_result = Mock(returncode=0)
            
            with patch('subprocess.run', return_value=mock_result) as mock_run:
                with patch.object(manager, 'is_running', return_value=False):
                    with patch.object(manager, 'clean_stale_locks', return_value=0):
                        result = manager._start_windows()
                        
                        # Should call sc start
                        mock_run.assert_called_once()
                        call_args = mock_run.call_args[0][0]
                        assert call_args[0] == "sc"
                        assert call_args[1] == "start"
    
    def test_start_linux_uses_systemctl(self):
        """Test Linux start tries systemctl command first."""
        with patch('platform.system', return_value='Linux'):
            manager = ServiceManager("test-linux-start")
            
            # Mock systemctl command success
            mock_result = Mock(returncode=0)
            
            with patch('subprocess.run', return_value=mock_result) as mock_run:
                result = manager._start_linux()
                
                # Should call systemctl start
                mock_run.assert_called_once()
                call_args = mock_run.call_args[0][0]
                assert call_args[0] == "systemctl"
                assert call_args[1] == "--user"
                assert call_args[2] == "start"
    
    def test_start_macos_uses_launchctl(self):
        """Test macOS start tries launchctl command first."""
        with patch('platform.system', return_value='Darwin'):
            manager = ServiceManager("test-mac-start")
            
            # Mock launchctl command success
            mock_result = Mock(returncode=0)
            
            with patch('subprocess.run', return_value=mock_result) as mock_run:
                result = manager._start_macos()
                
                # Should call launchctl start
                mock_run.assert_called_once()
                call_args = mock_run.call_args[0][0]
                assert call_args[0] == "launchctl"
                assert call_args[1] == "start"
    
    def test_start_subprocess_fallback(self):
        """Test subprocess fallback when platform commands fail."""
        manager = ServiceManager("test-subprocess")
        
        # Mock subprocess.Popen
        mock_popen = Mock()
        
        with patch('subprocess.Popen', return_value=mock_popen):
            with patch.object(manager, 'is_running', side_effect=[False, True]):
                with patch('time.sleep'):
                    result = manager._start_subprocess()
                    
                    assert result is True
    
    def test_stop_process_graceful_shutdown(self):
        """Test graceful shutdown with terminate."""
        manager = ServiceManager("test-stop-graceful")
        
        # Mock process that terminates gracefully
        mock_process = Mock(spec=psutil.Process)
        mock_process.wait.return_value = None  # Exits within timeout
        
        with patch.object(manager, 'get_pid', return_value=1234):
            with patch('psutil.Process', return_value=mock_process):
                result = manager._stop_process()
                
                assert result is True
                mock_process.terminate.assert_called_once()
                mock_process.wait.assert_called()
    
    def test_stop_process_force_kill(self):
        """Test force kill when graceful shutdown times out."""
        manager = ServiceManager("test-stop-force")
        
        # Mock process that doesn't terminate gracefully
        mock_process = Mock(spec=psutil.Process)
        mock_process.wait.side_effect = [psutil.TimeoutExpired(30), None]  # Timeout then exit
        
        with patch.object(manager, 'get_pid', return_value=1234):
            with patch('psutil.Process', return_value=mock_process):
                result = manager._stop_process()
                
                assert result is True
                mock_process.terminate.assert_called_once()
                mock_process.kill.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_unsupported_platform_start(self):
        """Test start on unsupported platform."""
        with patch('platform.system', return_value='UnknownOS'):
            manager = ServiceManager("test-unknown-os")
            
            with patch.object(manager, 'is_running', return_value=False):
                with patch.object(manager, 'clean_stale_locks', return_value=0):
                    result = manager.start()
                    
                    assert result is False
    
    def test_unsupported_platform_stop(self):
        """Test stop on unsupported platform."""
        with patch('platform.system', return_value='UnknownOS'):
            manager = ServiceManager("test-unknown-os-stop")
            
            with patch.object(manager, 'is_running', return_value=True):
                result = manager.stop()
                
                assert result is False
    
    def test_wait_for_stop_timeout(self):
        """Test wait_for_stop times out."""
        manager = ServiceManager("test-wait-timeout")
        
        with patch.object(manager, 'is_running', return_value=True):
            result = manager._wait_for_stop(timeout=1)
            
            assert result is False
    
    def test_wait_for_stop_success(self):
        """Test wait_for_stop succeeds."""
        manager = ServiceManager("test-wait-success")
        
        with patch.object(manager, 'is_running', side_effect=[True, True, False]):
            with patch('time.sleep'):
                result = manager._wait_for_stop(timeout=10)
                
                assert result is True
