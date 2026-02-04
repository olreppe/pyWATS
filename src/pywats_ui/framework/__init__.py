"""Shared UI framework for pyWATS applications."""

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

__all__ = ["BaseApplication", "BaseMainWindow"]


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
