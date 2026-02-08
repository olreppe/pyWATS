"""Cross-platform service management for pyWATS Client.

This module provides a unified interface for managing the pyWATS Client service
across Windows, Linux, and macOS platforms. It uses psutil for process detection
and platform-specific commands for service control.

Example usage:
    >>> manager = ServiceManager("default")
    >>> manager.start()
    >>> manager.get_status()
    {'running': True, 'pid': 12345, 'uptime': 120.5}
    >>> manager.stop()
"""

import logging
from pywats.core.logging import get_logger
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional

import psutil

logger = get_logger(__name__)


class ServiceManager:
    """Manages pyWATS Client service lifecycle across platforms.
    
    Provides cross-platform methods for starting, stopping, and monitoring
    the pyWATS Client service. Uses psutil for reliable process detection
    and platform-specific commands when available.
    
    Attributes:
        instance_id: Unique identifier for this service instance
        platform: Current operating system (Windows, Linux, Darwin)
        lock_dir: Directory for lock files
    """
    
    def __init__(self, instance_id: str = "default"):
        """Initialize ServiceManager.
        
        Args:
            instance_id: Unique identifier for this service instance.
                Allows multiple independent instances to run simultaneously.
        """
        self.instance_id = instance_id
        self.platform = platform.system()
        self.lock_dir = Path(tempfile.gettempdir()) / "pyWATS_Client"
        self.lock_dir.mkdir(parents=True, exist_ok=True)
        
        # Platform-specific service names
        self._service_name_map = {
            "Windows": f"pyWATS-Client-{instance_id}",
            "Linux": f"pywats-client@{instance_id}",
            "Darwin": f"com.wats.pywats-client.{instance_id}"
        }
    
    @property
    def lock_file(self) -> Path:
        """Get the lock file path for this instance."""
        return self.lock_dir / f"instance_{self.instance_id}.lock"
    
    @property
    def service_name(self) -> str:
        """Get the platform-specific service name."""
        return self._service_name_map.get(self.platform, f"pywats-client-{self.instance_id}")
    
    def is_running(self) -> bool:
        """Check if the service is currently running.
        
        Uses psutil to find running pywats_client processes. More reliable
        than checking lock files alone, as it handles crash scenarios.
        
        Returns:
            True if service process is running, False otherwise.
        """
        try:
            # Look for pywats_client processes
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline') or []
                    cmdline_str = ' '.join(cmdline)
                    
                    # Check if this is a pywats_client process
                    if 'pywats_client' in cmdline_str or 'pywats-client' in cmdline_str:
                        # Check if it matches our instance_id
                        if self.instance_id in cmdline_str or self.instance_id == "default":
                            logger.debug(f"Found running service: PID {proc.info['pid']}")
                            return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return False
        except Exception as e:
            logger.exception(f"Error checking service status: {e}")
            return False
    
    def get_pid(self) -> Optional[int]:
        """Get the process ID of the running service.
        
        Returns:
            PID of running service, or None if not running.
        """
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = proc.info.get('cmdline') or []
                    cmdline_str = ' '.join(cmdline)
                    
                    if 'pywats_client' in cmdline_str or 'pywats-client' in cmdline_str:
                        if self.instance_id in cmdline_str or self.instance_id == "default":
                            return proc.info['pid']
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return None
        except Exception as e:
            logger.exception(f"Error getting PID: {e}")
            return None
    
    def get_status(self) -> Dict:
        """Get detailed service status information.
        
        Returns:
            Dictionary with keys:
                - running (bool): Whether service is running
                - pid (int|None): Process ID if running
                - uptime (float|None): Seconds since start if running
                - instance_id (str): Instance identifier
                - platform (str): Operating system
                - log_file (str|None): Path to log file if available
        """
        pid = self.get_pid()
        running = pid is not None
        uptime = None
        
        if running and pid:
            try:
                proc = psutil.Process(pid)
                uptime = time.time() - proc.create_time()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                running = False
                pid = None
        
        # Try to find log file
        log_file = None
        log_locations = [
            Path.home() / ".pywats" / "client" / f"{self.instance_id}.log",
            Path(tempfile.gettempdir()) / "pyWATS_Client" / f"{self.instance_id}.log",
        ]
        for log_path in log_locations:
            if log_path.exists():
                log_file = str(log_path)
                break
        
        return {
            "running": running,
            "pid": pid,
            "uptime": uptime,
            "instance_id": self.instance_id,
            "platform": self.platform,
            "log_file": log_file
        }
    
    def clean_stale_locks(self) -> int:
        """Remove lock files for processes that are no longer running.
        
        Scans all lock files in the lock directory and removes those
        belonging to dead processes. Useful for crash recovery.
        
        Returns:
            Number of stale lock files removed.
        """
        removed = 0
        
        try:
            for lock_file in self.lock_dir.glob("instance_*.lock"):
                try:
                    # Read PID from lock file
                    pid = int(lock_file.read_text().strip())
                    
                    # Check if process is still running
                    if not psutil.pid_exists(pid):
                        logger.info(f"Removing stale lock file: {lock_file} (PID {pid})")
                        lock_file.unlink()
                        removed += 1
                except (ValueError, FileNotFoundError, PermissionError) as e:
                    logger.warning(f"Error processing lock file {lock_file}: {e}", exc_info=True)
                    continue
        except Exception as e:
            logger.exception(f"Error cleaning stale locks: {e}")
        
        return removed
    
    def start(self) -> bool:
        """Start the pyWATS Client service.
        
        Platform-specific service start logic. Tries native service
        management first (sc, systemctl, launchctl), falls back to
        direct subprocess execution.
        
        Returns:
            True if service started successfully, False otherwise.
        """
        # Clean stale locks before starting
        cleaned = self.clean_stale_locks()
        if cleaned > 0:
            logger.info(f"Cleaned {cleaned} stale lock file(s)")
        
        # Check if already running
        if self.is_running():
            logger.warning(f"Service already running (instance: {self.instance_id})")
            return False
        
        # Platform-specific start
        if self.platform == "Windows":
            return self._start_windows()
        elif self.platform == "Linux":
            return self._start_linux()
        elif self.platform == "Darwin":
            return self._start_macos()
        else:
            logger.error(f"Unsupported platform: {self.platform}")
            return False
    
    def stop(self) -> bool:
        """Stop the pyWATS Client service.
        
        Attempts graceful shutdown first (30s timeout), then force kills
        if process doesn't exit. Platform-specific logic.
        
        Returns:
            True if service stopped successfully, False otherwise.
        """
        if not self.is_running():
            logger.warning(f"Service not running (instance: {self.instance_id})")
            return False
        
        # Platform-specific stop
        if self.platform == "Windows":
            return self._stop_windows()
        elif self.platform == "Linux":
            return self._stop_linux()
        elif self.platform == "Darwin":
            return self._stop_macos()
        else:
            logger.error(f"Unsupported platform: {self.platform}")
            return False
    
    def restart(self) -> bool:
        """Restart the pyWATS Client service.
        
        Stops the service (if running) then starts it again.
        
        Returns:
            True if restart successful, False otherwise.
        """
        if self.is_running():
            if not self.stop():
                logger.error("Failed to stop service during restart")
                return False
            
            # Wait for process to fully terminate
            for _ in range(10):
                if not self.is_running():
                    break
                time.sleep(0.5)
            else:
                logger.error("Service did not stop in time")
                return False
        
        return self.start()
    
    def _start_windows(self) -> bool:
        """Start service on Windows.
        
        Tries:
        1. Windows Service (sc start / net start)
        2. Direct subprocess execution
        
        Returns:
            True if started successfully.
        """
        # Try Windows Service first
        try:
            result = subprocess.run(
                ["sc", "start", self.service_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Started Windows service: {self.service_name}")
                return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug(f"sc command failed: {e}")
        
        # Fall back to direct execution
        return self._start_subprocess()
    
    def _start_linux(self) -> bool:
        """Start service on Linux.
        
        Tries:
        1. systemd user service (systemctl --user start)
        2. Direct subprocess execution
        
        Returns:
            True if started successfully.
        """
        # Try systemd user service
        try:
            result = subprocess.run(
                ["systemctl", "--user", "start", self.service_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Started systemd service: {self.service_name}")
                return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug(f"systemctl command failed: {e}")
        
        # Fall back to direct execution
        return self._start_subprocess()
    
    def _start_macos(self) -> bool:
        """Start service on macOS.
        
        Tries:
        1. launchd service (launchctl start)
        2. Direct subprocess execution
        
        Returns:
            True if started successfully.
        """
        # Try launchd
        try:
            result = subprocess.run(
                ["launchctl", "start", self.service_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Started launchd service: {self.service_name}")
                return True
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug(f"launchctl command failed: {e}")
        
        # Fall back to direct execution
        return self._start_subprocess()
    
    def _start_subprocess(self) -> bool:
        """Start service via direct subprocess execution.
        
        Uses python -m pywats_client --instance-id <id> in background.
        
        Returns:
            True if subprocess started successfully.
        """
        try:
            cmd = [
                sys.executable,
                "-m",
                "pywats_client",
                "--instance-id",
                self.instance_id
            ]
            
            # Start in background (detached process)
            if self.platform == "Windows":
                # Windows: use CREATE_NEW_PROCESS_GROUP and DETACHED_PROCESS
                subprocess.Popen(
                    cmd,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Unix: use start_new_session
                subprocess.Popen(
                    cmd,
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # Wait a moment and verify it started
            time.sleep(2)
            if self.is_running():
                logger.info(f"Started service via subprocess (instance: {self.instance_id})")
                return True
            else:
                logger.error("Service subprocess failed to start")
                return False
                
        except Exception as e:
            logger.exception(f"Error starting subprocess: {e}")
            return False
    
    def _stop_windows(self) -> bool:
        """Stop service on Windows.
        
        Tries:
        1. Windows Service (sc stop / net stop)
        2. Graceful process termination
        3. Force kill
        
        Returns:
            True if stopped successfully.
        """
        # Try Windows Service first
        try:
            result = subprocess.run(
                ["sc", "stop", self.service_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Stopped Windows service: {self.service_name}")
                return self._wait_for_stop()
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug(f"sc command failed: {e}")
        
        # Fall back to process termination
        return self._stop_process()
    
    def _stop_linux(self) -> bool:
        """Stop service on Linux.
        
        Tries:
        1. systemd user service (systemctl --user stop)
        2. Graceful process termination
        3. Force kill
        
        Returns:
            True if stopped successfully.
        """
        # Try systemd user service
        try:
            result = subprocess.run(
                ["systemctl", "--user", "stop", self.service_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Stopped systemd service: {self.service_name}")
                return self._wait_for_stop()
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug(f"systemctl command failed: {e}")
        
        # Fall back to process termination
        return self._stop_process()
    
    def _stop_macos(self) -> bool:
        """Stop service on macOS.
        
        Tries:
        1. launchd service (launchctl stop)
        2. Graceful process termination
        3. Force kill
        
        Returns:
            True if stopped successfully.
        """
        # Try launchd
        try:
            result = subprocess.run(
                ["launchctl", "stop", self.service_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.info(f"Stopped launchd service: {self.service_name}")
                return self._wait_for_stop()
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.debug(f"launchctl command failed: {e}")
        
        # Fall back to process termination
        return self._stop_process()
    
    def _stop_process(self) -> bool:
        """Stop service by terminating the process.
        
        Tries graceful termination (SIGTERM) first with 30s timeout,
        then force kills (SIGKILL) if needed.
        
        Returns:
            True if process stopped successfully.
        """
        pid = self.get_pid()
        if not pid:
            logger.warning("No process found to stop")
            return True  # Already stopped
        
        try:
            proc = psutil.Process(pid)
            
            # Try graceful termination first
            logger.info(f"Sending SIGTERM to PID {pid}")
            proc.terminate()
            
            # Wait up to 30 seconds for graceful shutdown
            try:
                proc.wait(timeout=30)
                logger.info(f"Process {pid} terminated gracefully")
                return True
            except psutil.TimeoutExpired:
                logger.warning(f"Process {pid} did not terminate gracefully, force killing", exc_info=True)
                proc.kill()
                proc.wait(timeout=5)
                logger.info(f"Process {pid} force killed")
                return True
                
        except psutil.NoSuchProcess:
            logger.info(f"Process {pid} already exited")
            return True
        except Exception as e:
            logger.exception(f"Error stopping process: {e}")
            return False
    
    def _wait_for_stop(self, timeout: int = 30) -> bool:
        """Wait for service to stop.
        
        Args:
            timeout: Maximum seconds to wait.
            
        Returns:
            True if service stopped within timeout.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.is_running():
                return True
            time.sleep(0.5)
        
        logger.error(f"Service did not stop within {timeout}s")
        return False
