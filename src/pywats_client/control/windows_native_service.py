"""
Native Windows Service using pywin32

This module provides a proper Windows Service that appears in:
- services.msc (Windows Services manager)
- Task Manager → Services tab
- sc.exe queries

This is the recommended approach for production Windows deployments.
For development or cross-platform, use the NSSM wrapper instead.

Installation:
    python -m pywats_client install-service --native
    
Control:
    net start pyWATS_Service
    net stop pyWATS_Service
    
Removal:
    python -m pywats_client uninstall-service --native
"""

import sys
import os
import logging
import time
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Check for pywin32 availability
try:
    import win32serviceutil
    import win32service
    import win32event
    import servicemanager
    import socket
    HAS_PYWIN32 = True
except ImportError:
    HAS_PYWIN32 = False
    # Create stub classes for type hints when pywin32 not available
    class win32serviceutil:
        class ServiceFramework:
            pass
    

class PyWATSService(win32serviceutil.ServiceFramework if HAS_PYWIN32 else object):
    """
    Native Windows Service for pyWATS Client.
    
    This service:
    - Registers with Windows Service Control Manager (SCM)
    - Appears in Task Manager and services.msc
    - Supports standard service commands (start, stop, pause, continue)
    - Auto-starts on system boot (if configured)
    - Runs under SYSTEM or specified user account
    
    The service wraps the ClientService class which handles:
    - API connection
    - File monitoring (PendingWatcher)
    - Converter processing
    - Report queue management
    """
    
    # Service configuration
    _svc_name_ = "pyWATS_Service"
    _svc_display_name_ = "pyWATS Client Service"
    _svc_description_ = (
        "WATS Test Report Management - Background service for monitoring "
        "test result files, converting reports, and uploading to WATS server."
    )
    
    # Instance ID for multi-station support (default is single station)
    _instance_id = "default"
    
    def __init__(self, args):
        """Initialize the Windows Service"""
        if not HAS_PYWIN32:
            raise RuntimeError("pywin32 is required for native Windows service")
        
        win32serviceutil.ServiceFramework.__init__(self, args)
        
        # Create stop event
        self._stop_event = win32event.CreateEvent(None, 0, 0, None)
        
        # Service components (initialized on start)
        self._service = None
        self._running = False
        
        # Get instance ID from environment or registry
        self._instance_id = os.environ.get('PYWATS_INSTANCE_ID', 'default')
        
        socket.setdefaulttimeout(60)
    
    def SvcStop(self):
        """
        Called when the service receives a stop command.
        
        Windows expects this to return quickly, so we:
        1. Report STOP_PENDING status
        2. Signal the stop event
        3. Let SvcDoRun handle graceful shutdown
        """
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self._stop_event)
        self._running = False
        
        # Log to Windows Event Log
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STOPPED,
            (self._svc_name_, '')
        )
    
    def SvcDoRun(self):
        """
        Main service entry point - called when service starts.
        
        This method must not return until the service should stop.
        """
        # Log startup to Windows Event Log
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )
        
        try:
            self._running = True
            self._main()
        except Exception as e:
            servicemanager.LogErrorMsg(f"Service failed: {e}")
            logger.exception("Service crashed")
            raise
    
    def _main(self):
        """
        Main service loop.
        
        Initializes and runs the pyWATS ClientService.
        """
        try:
            # Import here to avoid loading heavy modules at service registration
            from pywats_client.service.client_service import ClientService
            
            logger.info(f"Starting pyWATS Service (instance: {self._instance_id})")
            
            # Create client service
            self._service = ClientService(instance_id=self._instance_id)
            
            # Start service in a thread (ClientService.start() blocks)
            import threading
            service_thread = threading.Thread(
                target=self._service.start,
                daemon=True,
                name="ClientService"
            )
            service_thread.start()
            
            # Wait for stop signal
            while self._running:
                # Check stop event every 1 second
                result = win32event.WaitForSingleObject(self._stop_event, 1000)
                if result == win32event.WAIT_OBJECT_0:
                    # Stop event signaled
                    break
            
            # Graceful shutdown
            logger.info("Stopping pyWATS Service...")
            if self._service:
                self._service.stop()
            
            # Wait for service thread to finish
            service_thread.join(timeout=10)
            
            logger.info("pyWATS Service stopped")
            
        except Exception as e:
            logger.exception(f"Service error: {e}")
            servicemanager.LogErrorMsg(f"Service error: {e}")
            raise


def is_pywin32_available() -> bool:
    """Check if pywin32 is installed and functional"""
    return HAS_PYWIN32


def get_service_name(instance_id: str = "default") -> str:
    """Get service name for an instance"""
    if instance_id == "default":
        return "pyWATS_Service"
    return f"pyWATS_Service_{instance_id}"


def is_admin() -> bool:
    """Check if running with administrator privileges"""
    if not HAS_PYWIN32:
        return False
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False


def install_service(
    instance_id: str = "default",
    startup: str = "auto",
    username: Optional[str] = None,
    password: Optional[str] = None
) -> bool:
    """
    Install pyWATS as a native Windows Service.
    
    Args:
        instance_id: Instance identifier (default: "default")
        startup: Startup type - "auto", "manual", or "disabled"
        username: Service account username (None for LocalSystem)
        password: Service account password
        
    Returns:
        True if installation successful
    """
    if not HAS_PYWIN32:
        print("ERROR: pywin32 is required for native Windows service")
        print("Install with: pip install pywin32")
        return False
    
    if not is_admin():
        print("ERROR: Administrator privileges required")
        print("Please run as Administrator")
        return False
    
    try:
        # Configure service name for instance
        service_name = get_service_name(instance_id)
        display_name = f"pyWATS Client Service"
        if instance_id != "default":
            display_name = f"pyWATS Client Service ({instance_id})"
        
        # Get Python executable path
        python_exe = sys.executable
        
        # Get this module's path
        module_path = Path(__file__).resolve()
        
        # Build service command
        # We need to run this module directly for the service
        service_cmd = f'"{python_exe}" "{module_path}"'
        
        # Set instance ID via environment for multi-instance
        if instance_id != "default":
            os.environ['PYWATS_INSTANCE_ID'] = instance_id
        
        print(f"Installing service: {service_name}")
        print(f"  Display name: {display_name}")
        print(f"  Instance ID: {instance_id}")
        print(f"  Startup type: {startup}")
        
        # Map startup type
        startup_map = {
            "auto": win32service.SERVICE_AUTO_START,
            "manual": win32service.SERVICE_DEMAND_START,
            "disabled": win32service.SERVICE_DISABLED
        }
        startup_type = startup_map.get(startup, win32service.SERVICE_AUTO_START)
        
        # Temporarily modify class attributes for this instance
        PyWATSService._svc_name_ = service_name
        PyWATSService._svc_display_name_ = display_name
        PyWATSService._instance_id = instance_id
        
        # Install service
        win32serviceutil.InstallService(
            PyWATSService._svc_reg_class_,
            service_name,
            display_name,
            startType=startup_type,
            userName=username,
            password=password,
            description=PyWATSService._svc_description_
        )
        
        print(f"\n✓ Service '{service_name}' installed successfully")
        print(f"\nTo start the service:")
        print(f"  net start {service_name}")
        print(f"  or: sc start {service_name}")
        print(f"\nTo view in Services:")
        print(f"  services.msc")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to install service: {e}")
        logger.exception("Service installation failed")
        return False


def uninstall_service(instance_id: str = "default") -> bool:
    """
    Uninstall the Windows Service.
    
    Args:
        instance_id: Instance identifier
        
    Returns:
        True if uninstallation successful
    """
    if not HAS_PYWIN32:
        print("ERROR: pywin32 is required")
        return False
    
    if not is_admin():
        print("ERROR: Administrator privileges required")
        return False
    
    try:
        service_name = get_service_name(instance_id)
        
        print(f"Stopping service '{service_name}'...")
        try:
            win32serviceutil.StopService(service_name)
            time.sleep(2)  # Give it time to stop
        except Exception:
            pass  # Service might not be running
        
        print(f"Removing service '{service_name}'...")
        win32serviceutil.RemoveService(service_name)
        
        print(f"\n✓ Service '{service_name}' removed successfully")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to remove service: {e}")
        return False


def get_service_status(instance_id: str = "default") -> Optional[str]:
    """
    Get the current status of the Windows Service.
    
    Returns:
        Status string or None if service not found
    """
    if not HAS_PYWIN32:
        return None
    
    try:
        import win32serviceutil
        service_name = get_service_name(instance_id)
        
        status = win32serviceutil.QueryServiceStatus(service_name)
        state = status[1]
        
        state_map = {
            win32service.SERVICE_STOPPED: "Stopped",
            win32service.SERVICE_START_PENDING: "Starting",
            win32service.SERVICE_STOP_PENDING: "Stopping",
            win32service.SERVICE_RUNNING: "Running",
            win32service.SERVICE_CONTINUE_PENDING: "Continuing",
            win32service.SERVICE_PAUSE_PENDING: "Pausing",
            win32service.SERVICE_PAUSED: "Paused",
        }
        
        return state_map.get(state, "Unknown")
        
    except Exception:
        return None


def start_service(instance_id: str = "default") -> bool:
    """Start the Windows Service"""
    if not HAS_PYWIN32:
        return False
    
    try:
        service_name = get_service_name(instance_id)
        win32serviceutil.StartService(service_name)
        return True
    except Exception as e:
        print(f"ERROR: Failed to start service: {e}")
        return False


def stop_service(instance_id: str = "default") -> bool:
    """Stop the Windows Service"""
    if not HAS_PYWIN32:
        return False
    
    try:
        service_name = get_service_name(instance_id)
        win32serviceutil.StopService(service_name)
        return True
    except Exception as e:
        print(f"ERROR: Failed to stop service: {e}")
        return False


# Entry point for service execution
if __name__ == '__main__':
    if HAS_PYWIN32:
        if len(sys.argv) == 1:
            # Running as service
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(PyWATSService)
            servicemanager.StartServiceCtrlDispatcher()
        else:
            # Command line handling (install, remove, etc.)
            win32serviceutil.HandleCommandLine(PyWATSService)
    else:
        print("ERROR: pywin32 is required for Windows service functionality")
        print("Install with: pip install pywin32")
        sys.exit(1)
