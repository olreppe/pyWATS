"""
Main Window for WATS Client GUI

Implements the main application window with navigation sidebar
and content pages matching the WATS Client design.
"""

import asyncio
from typing import Optional, Dict, Any
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QListWidget, QListWidgetItem, QLabel, QFrame, QSizePolicy,
    QSystemTrayIcon, QMenu, QMessageBox, QApplication, QPushButton
)
from PySide6.QtCore import Qt, QSize, Signal, Slot, QTimer
from PySide6.QtGui import QAction, QCloseEvent

from .styles import DARK_STYLESHEET
from .pages import (
    BasePage, GeneralPage, ConnectionPage, ProxySettingsPage, 
    ConvertersPage, AboutPage
)
from ..core.config import ClientConfig
from ..core.client import WATSClient


class MainWindow(QMainWindow):
    """
    Main application window for WATS Client.
    
    Features:
    - Navigation sidebar with page selection
    - Stacked widget for page content
    - System tray integration
    - Status bar with connection info
    """
    
    # Signals for async updates
    connection_status_changed = Signal(str)
    client_status_changed = Signal(str)
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        self.config = config
        self.client: Optional[WATSClient] = None
        self._tray_icon: Optional[QSystemTrayIcon] = None
        
        # Setup UI
        self._setup_window()
        self._setup_tray_icon()
        self._setup_ui()
        self._apply_styles()
        self._connect_signals()
        
        # Initialize client
        self._init_client()
        
        # Update timer for status refresh
        self._status_timer = QTimer()
        self._status_timer.timeout.connect(self._update_status)
        self._status_timer.start(5000)  # Update every 5 seconds
    
    def _setup_window(self) -> None:
        """Configure window properties"""
        self.setWindowTitle(f"WATS Client - {self.config.instance_name}")
        self.setMinimumSize(800, 600)
        self.resize(900, 650)
    
    def _setup_tray_icon(self) -> None:
        """Setup system tray icon"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        tray_icon = QSystemTrayIcon(self)
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self._quit_application)
        tray_menu.addAction(quit_action)
        
        tray_icon.setContextMenu(tray_menu)
        tray_icon.activated.connect(self._on_tray_activated)
        
        if self.config.minimize_to_tray:
            tray_icon.show()
        
        self._tray_icon = tray_icon
    
    def _setup_ui(self) -> None:
        """Setup the main UI layout"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self._create_sidebar(main_layout)
        
        # Create content area
        self._create_content_area(main_layout)
        
        # Create status bar
        self._create_status_bar()
    
    def _create_sidebar(self, layout: QHBoxLayout) -> None:
        """Create navigation sidebar"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #252526;")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Logo/Title area
        logo_frame = QFrame()
        logo_layout = QHBoxLayout(logo_frame)
        logo_layout.setContentsMargins(15, 15, 15, 15)
        
        # Logo icon placeholder
        logo_icon = QLabel("🔧")  # Placeholder - use actual icon
        logo_icon.setStyleSheet("font-size: 24px;")
        logo_layout.addWidget(logo_icon)
        
        title_label = QLabel("WATS Client")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        logo_layout.addWidget(title_label)
        logo_layout.addStretch()
        
        sidebar_layout.addWidget(logo_frame)
        
        # Navigation list
        self._nav_list = QListWidget()
        self._nav_list.setObjectName("navList")
        
        # Add navigation items - only the pages we have implemented
        nav_items = [
            ("General", "⚙️"),
            ("Connection", "🔗"),
            ("Proxy Settings", "🌐"),
            ("Converters", "🔄"),
            ("", ""),  # Separator
            ("About", "ℹ️"),
        ]
        
        for name, icon in nav_items:
            if not name:  # Separator
                item = QListWidgetItem()
                item.setFlags(Qt.ItemFlag.NoItemFlags)
                item.setSizeHint(QSize(0, 20))
                self._nav_list.addItem(item)
            else:
                item = QListWidgetItem(f"  {name}")
                item.setData(Qt.ItemDataRole.UserRole, name)
                item.setSizeHint(QSize(0, 45))
                self._nav_list.addItem(item)
        
        self._nav_list.currentRowChanged.connect(self._on_nav_changed)
        sidebar_layout.addWidget(self._nav_list, 1)
        
        # Footer
        footer_frame = QFrame()
        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(15, 10, 15, 15)
        
        from .. import __version__
        footer_label = QLabel(f"pyWATS Client | v{__version__}")
        footer_label.setObjectName("footerLabel")
        footer_layout.addWidget(footer_label)
        
        sidebar_layout.addWidget(footer_frame)
        
        layout.addWidget(sidebar)
    
    def _create_content_area(self, layout: QHBoxLayout) -> None:
        """Create main content area"""
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stacked widget for pages
        self._page_stack = QStackedWidget()
        
        # Create pages - only the ones we have implemented
        self._pages: Dict[str, BasePage] = {
            "General": GeneralPage(self.config),
            "Connection": ConnectionPage(self.config, self),
            "Proxy Settings": ProxySettingsPage(self.config),
            "Converters": ConvertersPage(self.config, self),
            "About": AboutPage(self.config),
        }
        
        for page in self._pages.values():
            self._page_stack.addWidget(page)
        
        content_layout.addWidget(self._page_stack)
        
        # Apply/Cancel buttons at bottom
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.addStretch()
        
        self._apply_btn = QPushButton("Apply")
        self._apply_btn.setObjectName("primaryButton")
        self._apply_btn.setEnabled(False)
        self._apply_btn.clicked.connect(self._on_apply)
        button_layout.addWidget(self._apply_btn)
        
        self._ok_btn = QPushButton("Ok")
        self._ok_btn.clicked.connect(self._on_ok)
        button_layout.addWidget(self._ok_btn)
        
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.clicked.connect(self._on_cancel)
        button_layout.addWidget(self._cancel_btn)
        
        content_layout.addWidget(button_frame)
        
        layout.addWidget(content_frame, 1)
        
        # Select first page
        self._nav_list.setCurrentRow(0)
    
    def _create_status_bar(self) -> None:
        """Create status bar"""
        status_bar = self.statusBar()
        
        # Connection status
        self._status_label = QLabel("Disconnected")
        status_bar.addWidget(self._status_label)
        
        status_bar.addWidget(QLabel(" | "))
        
        # Instance info
        self._instance_label = QLabel(f"Instance: {self.config.instance_id}")
        status_bar.addWidget(self._instance_label)
    
    def _apply_styles(self) -> None:
        """Apply dark theme stylesheet"""
        self.setStyleSheet(DARK_STYLESHEET)
    
    def _connect_signals(self) -> None:
        """Connect signals and slots"""
        self.connection_status_changed.connect(self._on_connection_status_ui)
        self.client_status_changed.connect(self._on_client_status_ui)
        
        # Connect page change signals
        for page in self._pages.values():
            if hasattr(page, 'config_changed'):
                page.config_changed.connect(self._on_config_changed)
    
    def _init_client(self) -> None:
        """Initialize the WATS client"""
        self.client = WATSClient(self.config)
    
    # Navigation handling
    
    @Slot(int)
    def _on_nav_changed(self, index: int) -> None:
        """Handle navigation item selection"""
        item = self._nav_list.item(index)
        if not item:
            return
        
        page_name = item.data(Qt.ItemDataRole.UserRole)
        if page_name and page_name in self._pages:
            page_index = list(self._pages.keys()).index(page_name)
            self._page_stack.setCurrentIndex(page_index)
    
    # Button handlers
    
    def _on_apply(self) -> None:
        """Handle Apply button click"""
        self._save_config()
        self._apply_btn.setEnabled(False)
    
    def _on_ok(self) -> None:
        """Handle Ok button click"""
        self._save_config()
        self.close()
    
    def _on_cancel(self) -> None:
        """Handle Cancel button click"""
        self.close()
    
    def _on_config_changed(self) -> None:
        """Handle configuration changes"""
        self._apply_btn.setEnabled(True)
    
    def _save_config(self) -> None:
        """Save configuration from all pages"""
        for page in self._pages.values():
            if hasattr(page, 'save_config'):
                page.save_config()
        
        self.config.save()
    
    # Status handling
    
    @Slot(str)
    def _on_connection_status_ui(self, status: str) -> None:
        """Update UI for connection status change"""
        self._status_label.setText(status)
        
        # Update connection page
        if "Connection" in self._pages:
            connection_page = self._pages["Connection"]
            if isinstance(connection_page, ConnectionPage):
                connection_page.update_status(status)
    
    @Slot(str)
    def _on_client_status_ui(self, status: str) -> None:
        """Update UI for client status change"""
        pass  # Can be used for additional status indicators
    
    def _update_status(self) -> None:
        """Periodic status update"""
        if self.client:
            # Get current connection status from client
            pass
    
    # Window events
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close event"""
        if self.config.minimize_to_tray and self._tray_icon:
            event.ignore()
            self.hide()
            self._tray_icon.showMessage(
                "WATS Client",
                "Application minimized to tray",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            self._quit_application()
            event.accept()
    
    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()
            self.activateWindow()
    
    def _quit_application(self) -> None:
        """Quit the application"""
        # Stop client
        if self.client:
            asyncio.create_task(self.client.stop())
        
        # Hide tray icon
        if self._tray_icon:
            self._tray_icon.hide()
        
        QApplication.quit()
    
    # Public methods for pages
    
    async def test_connection(self) -> bool:
        """Test connection to WATS server"""
        if self.client:
            return await self.client.test_connection()
        return False
    
    async def connect(self) -> bool:
        """Connect to WATS server"""
        if self.client:
            return await self.client.start()
        return False
    
    async def disconnect(self) -> None:
        """Disconnect from WATS server"""
        if self.client:
            await self.client.stop()
    
    async def refresh_converters(self) -> None:
        """Refresh converters"""
        if self.client:
            await self.client.refresh_converters()
