"""Shared UI framework for pyWATS applications."""

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

# Import from pywats_client.core (shared infrastructure)
from pywats_client.core.async_runner import AsyncTaskRunner
from pywats_client.core.event_bus import event_bus as EventBus

# Import framework components
from pywats_ui.framework.async_api_runner import AsyncAPIRunner
from pywats_ui.framework.error_mixin import ErrorHandlingMixin
from pywats_ui.framework.base_page import BasePage
from pywats_ui.framework.system_tray import SystemTrayIcon, create_default_icon

# Import reliability components
from pywats_ui.framework.reliability import (
    QueueManager,
    QueuedOperation,
    QueueStatus,
    ConnectionMonitor,
    ConnectionStatus,
    OfflineCapability,
)

__all__ = [
    # Legacy base classes
    "BaseApplication",
    "BaseMainWindow",
    
    # Core infrastructure (from pywats_client.core)
    'AsyncTaskRunner',
    'EventBus',
    
    # Framework components
    'AsyncAPIRunner',
    'ErrorHandlingMixin',
    'BasePage',
    'SystemTrayIcon',
    'create_default_icon',
    
    # Reliability components (offline-capable apps)
    'QueueManager',
    'QueuedOperation',
    'QueueStatus',
    'ConnectionMonitor',
    'ConnectionStatus',
    'OfflineCapability',
]


class BaseApplication(QApplication):
    """Base class for all pyWATS GUI applications."""
    
    def __init__(self, app_name: str, app_version: str):
        super().__init__([])
        self.app_name = app_name
        self.app_version = app_version
        self.setApplicationName(app_name)
        self.setApplicationVersion(app_version)


class BaseMainWindow(QMainWindow):
    """Base class for main application windows."""
    
    def __init__(self, config, parent=None):
        """Initialize base main window.
        
        Args:
            config: ClientConfig instance
            parent: Optional parent widget
        """
        super().__init__(parent)
        self._config = config
        self.setWindowTitle(config.get("instance_name", "pyWATS Client"))
        self.resize(800, 600)
