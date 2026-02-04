"""Shared UI framework for pyWATS applications."""

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

# Import from pywats_client.core (shared infrastructure)
from pywats_client.core import AsyncTaskRunner, EventBus

# Import framework components
from .async_api_runner import AsyncAPIRunner
from .error_mixin import ErrorHandlingMixin
from .base_page import BasePage

# Import reliability components
from .reliability import (
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
    
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(800, 600)
