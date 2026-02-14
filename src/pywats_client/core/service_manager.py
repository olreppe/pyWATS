"""
Service Management Utilities

Cross-platform utilities for managing pyWATS client services.
Services run as independent processes and are tracked via lock files.

Features:
- Start/stop services (subprocess management)
- Check service status (via lock file + process check)
- List all running services
- Cross-platform (Windows, Linux, macOS)

Lock File Format:
{
    "pid": 12345,
    "instance_id": "default",
    "instance_name": "Client A (Master)",
    "started_at": "2026-02-14T10:30:00",
    "service_url": "https://python.wats.com",
    "config_path": "C:/ProgramData/pyWATS/instances/default/client_config.json"
}
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ServiceInfo:
    """Information about a service instance."""
    
    def __init__(self, instance_id: str, lock_data: Optional[Dict[str, Any]] = None):
        self.instance_id = instance_id
        self.instance_name = ""
        self.pid: Optional[int] = None
        self.started_at: Optional[str] = None
        self.service_url = ""
        self.config_path = ""
        self.is_running = False
        
        if lock_data:
            self.instance_name = lock_data.get("instance_name", instance_id)
            self.pid = lock_data.get("pid")
            self.started_at = lock_data.get("started_at")
            self.service_url = lock_data.get("service_url", "")
            self.config_path = lock_data.get("config_path", "")
            self.is_running = self.pid and is_process_running(self.pid)
    
    def __repr__(self) -> str:
        status = "Running" if self.is_running else "Stopped"
        return f"ServiceInfo(id={self.instance_id}, name={self.instance_name}, status={status}, pid={self.pid})"


def get_instances_base_path() -> Path:
    """Get the system-wide instances base directory (cross-platform)."""
    if os.name == 'nt':
        # Windows: C:\ProgramData\pyWATS\instances
        base = Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / 'pyWATS' / 'instances'
    else:
        # Linux/Mac: /var/lib/pywats/instances
        base = Path('/var/lib/pywats/instances')
    
    return base


def get_instance_dir(instance_id: str) -> Path:
    """Get the directory for a specific instance."""
    return get_instances_base_path() / instance_id


def get_lock_file_path(instance_id: str) -> Path:
    """Get the lock file path for an instance."""
    return get_instance_dir(instance_id) / "service.lock"


def read_lock_file(instance_id: str) -> Optional[Dict[str, Any]]:
    """Read lock file and return service metadata (None if not running)."""
    lock_path = get_lock_file_path(instance_id)
    if not lock_path.exists():
        return None
    
    try:
        with open(lock_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read lock file {lock_path}: {e}")
        return None


def is_process_running(pid: int) -> bool:
    """Check if process with given PID is running (cross-platform)."""
    try:
        if os.name == 'nt':
            # Windows: Use tasklist
            result = subprocess.run(
                ['tasklist', '/FI', f'PID eq {pid}'],
                capture_output=True,
                text=True
            )
            return str(pid) in result.stdout
        else:
            # Linux/Mac: Send signal 0 (doesn't kill, just checks)
            os.kill(pid, 0)
            return True
    except (OSError, ProcessLookupError):
        return False


def get_service_status(instance_id: str) -> ServiceInfo:
    """Get status of a service instance."""
    lock_data = read_lock_file(instance_id)
    return ServiceInfo(instance_id, lock_data)


def list_all_services() -> List[ServiceInfo]:
    """List all service instances (running and stopped)."""
    services = []
    base_path = get_instances_base_path()
    
    if not base_path.exists():
        logger.warning(f"Instances directory not found: {base_path}")
        return services
    
    for instance_dir in base_path.iterdir():
        if instance_dir.is_dir():
            instance_id = instance_dir.name
            lock_data = read_lock_file(instance_id)
            services.append(ServiceInfo(instance_id, lock_data))
    
    return services


def start_service(instance_id: str, wait: bool = False) -> bool:
    """
    Start a service instance.
    
    Args:
        instance_id: Instance identifier (e.g., "default", "client_b")
        wait: If True, wait for process to complete (blocking)
              If False, launch as background process (default)
    
    Returns:
        True if started successfully, False otherwise
    """
    try:
        # Check if already running
        status = get_service_status(instance_id)
        if status.is_running:
            logger.warning(f"Service '{instance_id}' is already running (PID: {status.pid})")
            return False
        
        # Clean up stale lock file
        lock_path = get_lock_file_path(instance_id)
        if lock_path.exists():
            logger.info(f"Removing stale lock file: {lock_path}")
            lock_path.unlink()
        
        # Get python executable and run_service.py path
        python_exe = sys.executable
        # Go up 4 levels: service_manager.py -> core -> pywats_client -> src -> repository root
        run_service_script = Path(__file__).parent.parent.parent.parent / "run_service.py"
        
        if not run_service_script.exists():
            logger.error(f"run_service.py not found: {run_service_script}")
            return False
        
        # Launch subprocess
        if wait:
            # Blocking mode (for testing)
            result = subprocess.run(
                [python_exe, str(run_service_script), instance_id],
                check=True
            )
            return result.returncode == 0
        else:
            # Background mode (normal operation)
            if os.name == 'nt':
                # Windows: Use CREATE_NEW_PROCESS_GROUP to detach
                subprocess.Popen(
                    [python_exe, str(run_service_script), instance_id],
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL
                )
            else:
                # Linux/Mac: Use nohup-style detachment
                subprocess.Popen(
                    [python_exe, str(run_service_script), instance_id],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True
                )
            
            logger.info(f"Service '{instance_id}' started as background process")
            return True
        
    except Exception as e:
        logger.error(f"Failed to start service '{instance_id}': {e}", exc_info=True)
        return False


def stop_service(instance_id: str, force: bool = False) -> bool:
    """
    Stop a running service instance.
    
    Args:
        instance_id: Instance identifier
        force: If True, forcefully kill process (SIGKILL/taskkill /F)
               If False, graceful shutdown (SIGTERM/taskkill)
    
    Returns:
        True if stopped successfully, False otherwise
    """
    try:
        status = get_service_status(instance_id)
        
        if not status.is_running:
            logger.warning(f"Service '{instance_id}' is not running")
            # Clean up stale lock file if exists
            lock_path = get_lock_file_path(instance_id)
            if lock_path.exists():
                lock_path.unlink()
                logger.info(f"Removed stale lock file: {lock_path}")
            return False
        
        pid = status.pid
        logger.info(f"Stopping service '{instance_id}' (PID: {pid})...")
        
        if os.name == 'nt':
            # Windows: Use taskkill
            if force:
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True)
            else:
                subprocess.run(['taskkill', '/PID', str(pid)], check=True)
        else:
            # Linux/Mac: Use kill
            import signal
            sig = signal.SIGKILL if force else signal.SIGTERM
            os.kill(pid, sig)
        
        logger.info(f"Service '{instance_id}' stopped successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to stop service '{instance_id}': {e}", exc_info=True)
        return False


def restart_service(instance_id: str) -> bool:
    """Restart a service instance (stop then start)."""
    logger.info(f"Restarting service '{instance_id}'...")
    
    # Stop if running
    status = get_service_status(instance_id)
    if status.is_running:
        if not stop_service(instance_id):
            logger.error("Failed to stop service")
            return False
        
        # Wait a moment for cleanup
        import time
        time.sleep(1)
    
    # Start
    return start_service(instance_id)


def get_uptime(started_at: str) -> str:
    """Calculate uptime from ISO timestamp."""
    try:
        start_time = datetime.fromisoformat(started_at)
        uptime = datetime.now() - start_time
        
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    except Exception:
        return "Unknown"
