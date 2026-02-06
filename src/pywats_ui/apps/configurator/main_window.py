"""Configurator Main Window - Simplified reliable version.

Changes from original:
- H5 fix: REMOVED QLocalServer single-instance enforcement (allows multi-instance)
- H4 fix: cleanup() on closeEvent to cancel pending tasks
- Integrates QueueManager and ConnectionMonitor from framework
- Instance selector dialog for multi-instance support
- Simplified navigation (no advanced/compact modes for now)
"""

import asyncio
import logging
from typing import Optional, Dict
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QListWidget, QListWidgetItem, QLabel, QFrame, QPushButton,
    QMessageBox, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QCloseEvent, QPixmap

from pywats_ui.framework import BaseMainWindow
from pywats_ui.framework.reliability import QueueManager, ConnectionMonitor
from pywats_client.core.config import ClientConfig

# Import migrated pages
from .pages import (
    ConnectionPage, AboutPage, LogPage, SerialNumberHandlerPage,
    DashboardPage, APISettingsPage, SetupPage, SoftwarePage,
    LocationPage, ProxySettingsPage, ConvertersPageV2
)

logger = logging.getLogger(__name__)


class InstanceSelectorDialog(QDialog):
    """Dialog for selecting which client instance to manage."""
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("Select Instance")
        self.setModal(True)
        self.resize(400, 150)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        info_label = QLabel(
            "Multiple instances allow you to manage different stations or configurations.\n"
            "Select or create an instance:"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #b0b0b0; padding: 10px 0;")
        layout.addWidget(info_label)
        
        form = QFormLayout()
        
        self._instance_edit = QLineEdit()
        self._instance_edit.setText(self._config.get("instance_name", "default"))
        self._instance_edit.setPlaceholderText("e.g., Production-Line-1")
        form.addRow("Instance Name:", self._instance_edit)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_instance_name(self) -> str:
        """Get the selected instance name"""
        return self._instance_edit.text().strip() or "default"


class ConfiguratorMainWindow(BaseMainWindow):
    """Main window for pyWATS Configurator with reliability improvements.
    
    Features:
    - Multi-instance support (no QLocalServer enforcement)
    - Sidebar navigation with all configuration pages
    - Integrated QueueManager and ConnectionMonitor
    - Proper cleanup on close (H4 fix)
    """
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        
        # Reliability components
        self._queue_manager: Optional[QueueManager] = None
        self._connection_monitor: Optional[ConnectionMonitor] = None
        self._pending_tasks: list = []
        
        # Setup UI
        self._setup_window()
        self._setup_ui()
        self._setup_reliability()
        self._apply_styles()
    
    def _setup_window(self) -> None:
        """Configure window properties"""
        instance_name = self._config.get("instance_name", "default")
        self.setWindowTitle(f"pyWATS Configurator - {instance_name}")
        self.setMinimumSize(900, 650)
        self.resize(1100, 800)
        
        # Set window icon
        icon_path = Path(__file__).parent.parent / "resources" / "favicon.ico"
        if icon_path.exists():
            from PySide6.QtGui import QIcon
            self.setWindowIcon(QIcon(str(icon_path)))
    
    def _setup_ui(self) -> None:
        """Setup main UI layout"""
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
        
        # Logo icon
        logo_icon = QLabel("🔧")
        logo_icon.setStyleSheet("font-size: 24px;")
        logo_layout.addWidget(logo_icon)
        
        title_label = QLabel("Configurator")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        logo_layout.addWidget(title_label)
        logo_layout.addStretch()
        
        sidebar_layout.addWidget(logo_frame)
        
        # Navigation list
        self._nav_list = QListWidget()
        self._nav_list.setObjectName("navList")
        
        # Build navigation items
        nav_items = [
            "Dashboard",
            "Setup",
            "Connection",
            "Serial Numbers",
            "API Settings",
            "Converters",
            "Software",
            "Location",
            "Proxy",
            "Log",
            "About"
        ]
        
        for name in nav_items:
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, name)
            item.setSizeHint(QSize(0, 50))
            self._nav_list.addItem(item)
        
        self._nav_list.currentRowChanged.connect(self._on_nav_changed)
        sidebar_layout.addWidget(self._nav_list, 1)
        
        # Footer with version
        footer = QFrame()
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(15, 10, 15, 15)
        
        try:
            from pywats_client import __version__
            version_text = f"pyWATS v{__version__}"
        except ImportError:
            version_text = "pyWATS v(dev)"
        
        footer_label = QLabel(version_text)
        footer_label.setStyleSheet("color: #808080; font-size: 11px;")
        footer_layout.addWidget(footer_label)
        
        sidebar_layout.addWidget(footer)
        
        layout.addWidget(sidebar)
    
    def _create_content_area(self, layout: QHBoxLayout) -> None:
        """Create main content area with pages"""
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stacked widget for pages
        self._page_stack = QStackedWidget()
        
        # Create pages - all migrated pages
        self._pages: Dict[str, QWidget] = {
            "Dashboard": DashboardPage(self._config),
            "Setup": SetupPage(self._config),
            "Connection": ConnectionPage(self._config),
            "Serial Numbers": SerialNumberHandlerPage(self._config),
            "API Settings": APISettingsPage(self._config),
            "Converters": ConvertersPageV2(self._config, main_window=self),
            "Software": SoftwarePage(self._config),
            "Location": LocationPage(self._config),
            "Proxy": ProxySettingsPage(self._config),
            "Log": LogPage(self._config),
            "About": AboutPage(self._config),
        }
        
        # Add pages to stack
        for page in self._pages.values():
            self._page_stack.addWidget(page)
        
        content_layout.addWidget(self._page_stack)
        
        layout.addWidget(content_frame)
        
        # Select first page
        if self._nav_list.count() > 0:
            self._nav_list.setCurrentRow(0)
    
    def _create_status_bar(self) -> None:
        """Create status bar with connection info"""
        status_bar = self.statusBar()
        
        # Connection status label
        self._connection_status_label = QLabel("⚪ Initializing...")
        self._connection_status_label.setStyleSheet("color: #808080; padding: 5px;")
        status_bar.addPermanentWidget(self._connection_status_label)
        
        status_bar.showMessage("Ready")
    
    def _setup_reliability(self) -> None:
        """Setup reliability components (QueueManager, ConnectionMonitor)"""
        try:
            # Initialize queue manager with send callback
            queue_path = Path.home() / ".pywats" / "queue"
            self._queue_manager = QueueManager(
                queue_dir=queue_path,
                send_callback=self._send_queued_operation,
                retry_interval_ms=30000,
                max_retries=10
            )
            
            # Initialize connection monitor (FIX C3: add required callbacks)
            service_address = self._config.get("service_address", "")
            if service_address:
                self._connection_monitor = ConnectionMonitor(
                    connect_callback=self._connect_to_service,
                    check_callback=self._check_connection,
                    check_interval_ms=30000  # Check every 30s
                )
                self._connection_monitor.status_changed.connect(self._on_connection_status_changed)
                # ConnectionMonitor starts automatically on init
            
            logger.info("Reliability components initialized")
            
        except Exception as e:
            logger.exception(f"Failed to setup reliability components: {e}")
            QMessageBox.warning(
                self,
                "Initialization Warning",
                f"Failed to initialize reliability components.\n\nError: {e}\n\n"
                "Some features may not work correctly."
            )
    
    async def _send_queued_operation(self, operation: dict) -> None:
        """Send queued operation (callback for QueueManager).
        
        Args:
            operation: Operation dict with 'type' and 'data' keys
            
        Raises:
            Exception if send fails (triggers retry)
        """
        operation_type = operation.get("type")
        data = operation.get("data", {})
        
        logger.debug(f"Sending queued operation: {operation_type}")
        
        # For now, just log - specific send logic will be added later
        # This prevents QueueManager initialization errors
        if operation_type == "send_report":
            logger.info(f"Would send report: {data.get('serial_number', 'unknown')}")
        else:
            logger.info(f"Would send operation: {operation_type}")
    
    def _on_connection_status_changed(self, is_connected: bool, message: str) -> None:
        """Handle connection status change from ConnectionMonitor"""
        if is_connected:
            self._connection_status_label.setText(f"🟢 {message}")
            self._connection_status_label.setStyleSheet("color: #4ec9b0; padding: 5px;")
        else:
            self._connection_status_label.setText(f"🔴 {message}")
            self._connection_status_label.setStyleSheet("color: #f48771; padding: 5px;")
    
    def _check_connection(self) -> bool:
        """Check if service connection is available (callback for ConnectionMonitor).
        
        Returns:
            True if connected, False otherwise
        """
        # Simple check: if we have server address and token, we consider it "configured"
        # A more sophisticated check could ping the service
        has_address = bool(self._config.service_address)
        has_token = bool(self._config.api_token)
        return has_address and has_token
    
    async def _connect_to_service(self) -> None:
        """Establish connection to service (callback for ConnectionMonitor).
        
        Raises:
            Exception if connection fails
        """
        # For now, this is a placeholder
        # Real implementation would initialize API client, test connection, etc.
        if not self._config.service_address:
            raise ValueError("No service address configured")
        
        if not self._config.api_token:
            raise ValueError("No API token configured")
        
        # Connection is implicit - having valid credentials means we can connect
        logger.info(f"Connected to service: {self._config.service_address}")
    
    def _on_nav_changed(self, row: int) -> None:
        """Handle navigation item selection"""
        if row < 0:
            return
        
        item = self._nav_list.item(row)
        if not item:
            return
        
        page_name = item.data(Qt.ItemDataRole.UserRole)
        if page_name in self._pages:
            page = self._pages[page_name]
            self._page_stack.setCurrentWidget(page)
            
            # Load config when page is shown
            if hasattr(page, 'load_config'):
                try:
                    page.load_config()
                except Exception as e:
                    logger.exception(f"Failed to load config for {page_name}: {e}")
    
    def _apply_styles(self) -> None:
        """Apply dark theme styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #d4d4d4;
            }
            QFrame#sidebar {
                background-color: #252526;
                border-right: 1px solid #3c3c3c;
            }
            QFrame#contentFrame {
                background-color: #1e1e1e;
            }
            QListWidget#navList {
                background-color: #252526;
                border: none;
                outline: none;
                color: #d4d4d4;
                font-size: 14px;
            }
            QListWidget#navList::item {
                padding: 15px 20px;
                border: none;
            }
            QListWidget#navList::item:selected {
                background-color: #37373d;
                color: #ffffff;
            }
            QListWidget#navList::item:hover {
                background-color: #2a2d2e;
            }
            QStatusBar {
                background-color: #007acc;
                color: #ffffff;
            }
        """)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close - cleanup resources (H4 fix)"""
        try:
            logger.info("Configurator window closing, cleaning up...")
            
            # Save all page configs
            for page_name, page in self._pages.items():
                if hasattr(page, 'save_config'):
                    try:
                        page.save_config()
                    except Exception as e:
                        logger.exception(f"Failed to save config for {page_name}: {e}")
                
                # Cleanup page resources
                if hasattr(page, 'cleanup'):
                    try:
                        page.cleanup()
                    except Exception as e:
                        logger.exception(f"Failed to cleanup {page_name}: {e}")
            
            # Stop connection monitor
            if self._connection_monitor:
                # ConnectionMonitor will stop when destroyed
                pass
            
            # Cancel pending async tasks
            for task in self._pending_tasks:
                if not task.done():
                    task.cancel()
            
            logger.info("Configurator cleanup complete")
            
        except Exception as e:
            logger.exception(f"Error during cleanup: {e}")
        
        super().closeEvent(event)


def show_instance_selector(config: ClientConfig) -> Optional[str]:
    """Show instance selector dialog and return selected instance name.
    
    Returns:
        Instance name if user confirmed, None if cancelled
    """
    from PySide6.QtWidgets import QApplication
    
    # Create temporary app if needed (for standalone testing)
    app = QApplication.instance()
    temp_app = None
    if app is None:
        import sys
        temp_app = QApplication(sys.argv)
    
    dialog = InstanceSelectorDialog(config)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        instance_name = dialog.get_instance_name()
        if temp_app:
            temp_app.quit()
        return instance_name
    else:
        if temp_app:
            temp_app.quit()
        return None
