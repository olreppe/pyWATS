"""System tray icon and menu for pyWATS applications."""

import sys
from typing import Callable, Optional, List, Tuple
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt


def create_default_icon() -> QIcon:
    """Create a default pyWATS icon if no icon file is provided.
    
    Returns:
        QIcon with pyWATS branding (blue circle with 'W')
    """
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Background circle (pyWATS blue)
    painter.setBrush(QColor(78, 201, 176))  # #4ec9b0
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(2, 2, 60, 60)
    
    # Letter 'W' in white
    painter.setPen(QColor(255, 255, 255))
    font = painter.font()
    font.setPointSize(32)
    font.setBold(True)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "W")
    
    painter.end()
    
    return QIcon(pixmap)


class SystemTrayIcon(QSystemTrayIcon):
    """System tray icon with menu for pyWATS applications.
    
    Provides a centralized way to launch different pyWATS GUI applications
    from the system tray.
    
    Example:
        >>> app = QApplication(sys.argv)
        >>> tray = SystemTrayIcon()
        >>> tray.add_application("Configurator", launch_configurator)
        >>> tray.add_application("Yield Monitor", launch_yield)
        >>> tray.show()
        >>> sys.exit(app.exec())
    """
    
    def __init__(self, icon: Optional[QIcon] = None, parent=None):
        """Initialize system tray icon.
        
        Args:
            icon: Custom icon (defaults to pyWATS branding)
            parent: Parent widget
        """
        if icon is None:
            icon = create_default_icon()
        
        super().__init__(icon, parent)
        
        self._menu = QMenu()
        self._app_items: List[Tuple[str, Callable, Optional[QIcon]]] = []
        
        self.setContextMenu(self._menu)
        self.setToolTip("pyWATS Applications")
        
        # Enable click to show menu
        self.activated.connect(self._on_activated)
    
    def add_application(self, name: str, callback: Callable, icon: Optional[QIcon] = None):
        """Add an application to the tray menu.
        
        Args:
            name: Display name for the application
            callback: Function to call when menu item is clicked
            icon: Optional icon for the menu item
        """
        self._app_items.append((name, callback, icon))
        self._rebuild_menu()
    
    def add_separator(self):
        """Add a separator line to the menu."""
        self._app_items.append(("__separator__", None, None))
        self._rebuild_menu()
    
    def add_quit_action(self, callback: Optional[Callable] = None):
        """Add a 'Quit' action to exit all applications.
        
        Args:
            callback: Optional callback before quitting (defaults to QApplication.quit)
        """
        if callback is None:
            from PySide6.QtWidgets import QApplication
            callback = QApplication.quit
        
        self.add_separator()
        self.add_application("Quit", callback)
    
    def _rebuild_menu(self):
        """Rebuild the context menu from current items."""
        self._menu.clear()
        
        for item in self._app_items:
            name = item[0]
            if name == "__separator__":
                self._menu.addSeparator()
            else:
                callback = item[1]
                icon = item[2]
                action = QAction(name, self._menu)
                if icon:
                    action.setIcon(icon)
                action.triggered.connect(callback)
                self._menu.addAction(action)
    
    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason):
        """Handle tray icon activation (click).
        
        Args:
            reason: Activation reason (click, double-click, etc.)
        """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # Left mouse click - show menu
            self._menu.popup(self.geometry().bottomLeft())
        elif reason == QSystemTrayIcon.ActivationReason.Context:
            # Right mouse click - context menu (handled automatically)
            pass
