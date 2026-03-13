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
from pywats.core.logging import get_logger
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
    DashboardPage, SetupPage, ConvertersPageV2
)

logger = get_logger(__name__)


class InstanceSelectorDialog(QDialog):
    """Dialog for selecting which client instance to manage."""
    
    def __init__(self, config: ClientConfig, available_configs: list = None, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._config = config
        self._available_configs = available_configs or []
        self.setWindowTitle("Select Instance")
        self.setModal(True)
        self.resize(400, 200)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup dialog UI"""
        from PySide6.QtWidgets import QComboBox
        
        layout = QVBoxLayout(self)
        
        info_label = QLabel(
            "Multiple instances allow you to manage different stations or configurations.\n"
            "Select an existing instance or enter a new name:"
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #b0b0b0; padding: 10px 0;")
        layout.addWidget(info_label)
        
        form = QFormLayout()
        
        # If available configs, show dropdown
        if self._available_configs:
            self._instance_combo = QComboBox()
            self._instance_combo.setEditable(True)  # Allow custom entry
            
            # Load unique instance names from config files
            from pywats_client.core.config import ClientConfig
            seen_names = set()  # Track unique names
            
            for config_path in self._available_configs:
                try:
                    cfg = ClientConfig.load(config_path)
                    # Use instance_name if set, otherwise use instance_id
                    instance_name = cfg.instance_name if hasattr(cfg, 'instance_name') and cfg.instance_name else cfg.instance_id
                    if not instance_name:
                        instance_name = config_path.parent.name  # Use folder name as fallback
                    
                    # Only add if we haven't seen this name before
                    if instance_name not in seen_names:
                        seen_names.add(instance_name)
                        self._instance_combo.addItem(instance_name)
                        logger.debug(f"Added instance: {instance_name}")
                except Exception as e:
                    logger.debug(f"Failed to load config {config_path}: {e}")
            
            # Sort alphabetically for easier selection
            items = [self._instance_combo.itemText(i) for i in range(self._instance_combo.count())]
            self._instance_combo.clear()
            for item in sorted(items):
                self._instance_combo.addItem(item)
            
            # Set current or default
            current_instance = self._config.get("instance_name", "default")
            idx = self._instance_combo.findText(current_instance)
            if idx >= 0:
                self._instance_combo.setCurrentIndex(idx)
            
            form.addRow("Instance:", self._instance_combo)
        else:
            # No existing instances - text input only
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
        if hasattr(self, '_instance_combo'):
            return self._instance_combo.currentText().strip() or "default"
        else:
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
        self._tray_icon: Optional[QWidget] = None  # SystemTrayIcon (set via set_tray_icon)
        self._is_quitting: bool = False  # Track if actually quitting vs minimizing
        
        # Connection check state (background thread)
        self._connection_ok: bool = False
        self._bg_check_running: bool = False
        
        # Setup UI
        self._setup_window()
        self._setup_ui()
        self._setup_reliability()
        self._apply_styles()
        
        # Schedule delayed startup refresh (gives service time to auto-start)
        QTimer.singleShot(3000, self._delayed_startup_refresh)
    
    def set_tray_icon(self, tray_icon) -> None:
        """Set the system tray icon for minimize-to-tray support.
        
        Args:
            tray_icon: A SystemTrayIcon instance (from framework.system_tray)
        """
        self._tray_icon = tray_icon
    
    def _setup_window(self) -> None:
        """Configure window properties"""
        from . import __version__
        instance_name = self._config.get("instance_name", "default")
        self.setWindowTitle(f"pyWATS Client Configurator ({__version__}) - {instance_name}")
        # Phase 2: GUI Cleanup - Reduce minimum size for better scaling
        self.setMinimumSize(800, 600)  # Industry standard minimum
        self.resize(1000, 700)          # Comfortable default
        
        # Set window icon
        icon_path = Path(__file__).parent.parent / "resources" / "favicon.ico"
        if icon_path.exists():
            from PySide6.QtGui import QIcon
            self.setWindowIcon(QIcon(str(icon_path)))
    
    def _setup_menu_bar(self) -> None:
        """Setup menu bar with File menu (Phase 1: GUI Cleanup)"""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&File")
        
        # Disconnect action
        disconnect_action = file_menu.addAction("&Disconnect")
        disconnect_action.setStatusTip("Disconnect from WATS server")
        disconnect_action.setToolTip("Reset connection and clear credentials")
        disconnect_action.triggered.connect(self._on_disconnect)
        
        # Restart service action
        restart_action = file_menu.addAction("&Restart Service")
        restart_action.setStatusTip("Restart the pyWATS Client service")
        restart_action.setToolTip("Stop and restart the service (temporarily pauses file monitoring)")
        restart_action.triggered.connect(self._on_restart_service)
        
        # Minimize to tray action
        minimize_action = file_menu.addAction("&Minimize to Tray")
        minimize_action.setStatusTip("Minimize window to system tray")
        minimize_action.setToolTip("Hide window to system tray notification area")
        minimize_action.triggered.connect(self._on_minimize_to_tray)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = file_menu.addAction("E&xit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit application")
        exit_action.setToolTip("Close configurator and stop background tasks")
        exit_action.triggered.connect(self.close)
    
    def _setup_ui(self) -> None:
        """Setup main UI layout"""
        # Add menu bar first
        self._setup_menu_bar()
        
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
        # Phase 2: GUI Cleanup - Allow slight resize instead of fixed width
        sidebar.setMinimumWidth(180)
        sidebar.setMaximumWidth(220)
        sidebar.setStyleSheet("background-color: #252526;")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # No logo/title area (removed wrench icon and 'Configurator' label)
        
        # Navigation list
        self._nav_list = QListWidget()
        self._nav_list.setObjectName("navList")
        
        # Build navigation items (Phase 1: GUI Cleanup)
        nav_items = [
            ("Dashboard", "Service status, station info, and health overview"),
            ("Connection", "Server address, credentials, and connection testing"),
            ("Converters", "File converter configuration and monitoring"),
            ("Setup", "Station name, location, and general settings"),
            ("Serial Numbers", "Serial number handler configuration"),
            ("Log", "View application and converter logs"),
            ("About", "Version, system info, and license"),
        ]
        
        for name, tooltip in nav_items:
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, name)
            item.setToolTip(tooltip)
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
        
        # Create pages (Phase 1: GUI Cleanup - 7 essential tabs only)
        self._pages: Dict[str, QWidget] = {
            "Dashboard": DashboardPage(self._config),
            "Connection": ConnectionPage(self._config),
            "Converters": ConvertersPageV2(self._config, main_window=self),
            "Setup": SetupPage(self._config),
            "Serial Numbers": SerialNumberHandlerPage(self._config),
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
        self._connection_status_label.setToolTip("Current connection status to the WATS server")
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
            
            # Inject queue manager into ConnectionPage (created before reliability init)
            connection_page = self._pages.get("Connection")
            if connection_page and hasattr(connection_page, 'queue_manager'):
                connection_page.queue_manager = self._queue_manager
            
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
    
    async def _send_queued_operation(self, operation_data: dict) -> None:
        """Send queued operation via HTTP (callback for QueueManager).
        
        The QueueManager calls this with operation.data which contains:
          - url: Full API endpoint URL
          - report: The report payload dict
          - headers: HTTP headers dict
            
        Raises:
            Exception if send fails (triggers retry in QueueManager)
        """
        import httpx
        
        url = operation_data.get("url", "")
        report = operation_data.get("report")
        headers = operation_data.get("headers", {})
        
        if not url or not report:
            raise ValueError(f"Invalid queued operation: missing url or report data")
        
        logger.info(f"Sending queued report to {url} (SN: {report.get('sn', '?')})")
        
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.post(url, json=report, headers=headers)
            response.raise_for_status()
        
        logger.info(f"Queued report sent successfully: {response.status_code}")
    
    def _on_connection_status_changed(self, status: 'ConnectionStatus') -> None:
        """Handle connection status change from ConnectionMonitor.
        
        Propagates status to status bar, Dashboard, and Connection pages
        so all status labels stay consistent.
        
        Args:
            status: ConnectionStatus enum value (CONNECTED, DISCONNECTED, CONNECTING, RECONNECTING)
        """
        from pywats_ui.framework.reliability.connection_monitor import ConnectionStatus
        
        is_connected = (status == ConnectionStatus.CONNECTED)
        message = f"Connection {status.value}"
        
        # Update status bar
        if is_connected:
            self._connection_status_label.setText(f"🟢 {message}")
            self._connection_status_label.setStyleSheet("color: #4ec9b0; padding: 5px;")
        else:
            self._connection_status_label.setText(f"🔴 {message}")
            self._connection_status_label.setStyleSheet("color: #f48771; padding: 5px;")
        
        # Propagate to Dashboard page (server connection section)
        dashboard = self._pages.get("Dashboard")
        if dashboard and hasattr(dashboard, '_conn_indicator'):
            if is_connected:
                dashboard._conn_indicator.set_status("running")
                dashboard._conn_label.setText(f"Connected: {self._config.service_address}")
                dashboard._conn_label.setStyleSheet("color: #4ec9b0;")
            elif status == ConnectionStatus.RECONNECTING:
                dashboard._conn_indicator.set_status("unknown")
                dashboard._conn_label.setText("Reconnecting...")
                dashboard._conn_label.setStyleSheet("color: #dcdcaa;")
            else:
                dashboard._conn_indicator.set_status("stopped")
                dashboard._conn_label.setText(f"Disconnected ({self._config.service_address})")
                dashboard._conn_label.setStyleSheet("color: #808080;")
        
        # Propagate to Connection page
        connection_page = self._pages.get("Connection")
        if connection_page and hasattr(connection_page, 'update_status'):
            if is_connected:
                connection_page.update_status("Online")
            elif status == ConnectionStatus.RECONNECTING:
                connection_page.update_status("Connecting")
            else:
                connection_page.update_status("Offline")
    
    def _check_connection(self) -> bool:
        """Non-blocking connection check (callback for ConnectionMonitor).
        
        Returns cached result instantly. Actual HTTP check runs in a
        background thread to avoid blocking the Qt event loop.
        
        Returns:
            True if last check succeeded, False otherwise
        """
        url = self._config.service_address
        token = self._config.api_token
        
        if not url or not token:
            self._connection_ok = False
            return False
        
        # Start background HTTP check if not already running
        if not self._bg_check_running:
            self._bg_check_running = True
            import threading
            threading.Thread(
                target=self._bg_connection_check,
                daemon=True,
                name="ConnectionCheck"
            ).start()
        
        return self._connection_ok
    
    def _bg_connection_check(self) -> None:
        """Background thread: performs actual HTTP check and updates cached result."""
        try:
            import httpx
            url = self._config.service_address
            token = self._config.api_token
            test_url = f"{url.rstrip('/')}/api/Report/wats/info"
            headers = {"Authorization": f"Bearer {token}"}
            with httpx.Client(timeout=5.0, follow_redirects=True) as client:
                response = client.get(test_url, headers=headers)
                self._connection_ok = (response.status_code == 200)
        except Exception:
            self._connection_ok = False
        finally:
            self._bg_check_running = False
    
    def _delayed_startup_refresh(self) -> None:
        """Refresh Dashboard after startup delay (gives service time to auto-start)."""
        try:
            dashboard = self._pages.get("Dashboard")
            if dashboard and hasattr(dashboard, '_refresh_status'):
                dashboard._refresh_status()
                logger.debug("Delayed startup refresh completed")
        except Exception as e:
            logger.debug(f"Delayed startup refresh failed: {e}")
    
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
    
    def navigate_to_page(self, page_name: str) -> None:
        """Navigate to specific page by name (Phase 3: GUI Cleanup)
        
        Args:
            page_name: Name of the page to navigate to (e.g., "Setup", "Connection")
        """
        for i in range(self._nav_list.count()):
            item = self._nav_list.item(i)
            if item and item.data(Qt.ItemDataRole.UserRole) == page_name:
                self._nav_list.setCurrentRow(i)
                logger.debug(f"Navigated to page: {page_name}")
                return
        
        logger.warning(f"Page not found: {page_name}")
    
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
    
    def _on_disconnect(self) -> None:
        """Disconnect from server (File → Disconnect) - Phase 1: GUI Cleanup"""
        reply = QMessageBox.question(
            self,
            "Disconnect",
            "Disconnect from WATS server?\n\n"
            "This will stop the client service and clear the connection.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # TODO: Implement service stop logic
                # For now, just update status
                self.statusBar().showMessage("Disconnected")
                logger.info("Disconnected from server")
                
                # Update connection status label if it exists
                if hasattr(self, '_connection_status_label'):
                    self._connection_status_label.setText("⚪ Disconnected")
                
            except Exception as e:
                logger.exception(f"Failed to disconnect: {e}")
                QMessageBox.warning(self, "Disconnect Error", f"Failed to disconnect:\n{e}")
    
    def _on_restart_service(self) -> None:
        """Restart the pyWATS Client service (File → Restart Service)"""
        reply = QMessageBox.question(
            self,
            "Restart Service",
            "Restart the pyWATS Client service?\n\n"
            "This will temporarily pause file monitoring and uploads.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Run async restart in background
            asyncio.create_task(self._async_restart_service())
    
    async def _async_restart_service(self) -> None:
        """Async restart service using ServiceManager"""
        from pywats_client.service_manager import ServiceManager
        
        try:
            # Show progress
            self.statusBar().showMessage("Restarting service...")
            
            # Get instance ID from config
            instance_id = self._config.get("instance_id", "default")
            
            # Run restart in thread pool to avoid blocking UI
            loop = asyncio.get_event_loop()
            service_manager = ServiceManager(instance_id)
            success = await loop.run_in_executor(None, service_manager.restart)
            
            if success:
                self.statusBar().showMessage("Service restarted successfully", 5000)
                QMessageBox.information(
                    self,
                    "Service Restarted",
                    "Service restarted successfully.\n\n"
                    "File monitoring and uploads will resume shortly."
                )
                logger.info("Service restarted successfully")
                
                # Give service time to start, then refresh status
                await asyncio.sleep(2)
                if hasattr(self, '_delayed_startup_refresh'):
                    self._delayed_startup_refresh()
            else:
                self.statusBar().showMessage("Service restart failed", 5000)
                QMessageBox.critical(
                    self,
                    "Restart Failed",
                    "Failed to restart service. Check logs for details."
                )
                logger.error("Service restart failed")
                
        except Exception as e:
            logger.error(f"Error restarting service: {e}", exc_info=True)
            self.statusBar().showMessage("Service restart error", 5000)
            QMessageBox.critical(
                self,
                "Restart Error",
                f"Error restarting service:\n{e}"
            )
    
    def _on_minimize_to_tray(self) -> None:
        """Minimize to system tray (File -> Minimize to Tray)"""
        from PySide6.QtWidgets import QSystemTrayIcon
        
        if self._tray_icon is not None and QSystemTrayIcon.isSystemTrayAvailable():
            self.hide()
            self._tray_icon.showMessage(
                "pyWATS Client",
                "Minimized to tray. Click the tray icon to restore.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
            logger.debug("Minimized to system tray")
        elif QSystemTrayIcon.isSystemTrayAvailable():
            # No tray icon set - just hide (basic mode)
            self.hide()
            logger.debug("Minimized to system tray (no tray icon configured)")
        else:
            # Fallback to regular minimize
            self.showMinimized()
            logger.debug("System tray not available, minimized to taskbar")
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close - minimize to tray unless quitting."""
        # If not really quitting, minimize to tray instead
        if not self._is_quitting and self._tray_icon:
            event.ignore()
            self.hide()
            logger.info("Configurator minimized to system tray")
            return
        
        # Really quitting - do full cleanup
        try:
            logger.info("Configurator window closing, cleaning up...")
            
            # Track if any config changed (for consolidated message)
            config_saved = False
            save_errors = []
            
            # Save all page configs
            for page_name, page in self._pages.items():
                if hasattr(page, 'save_config'):
                    try:
                        page.save_config()
                        config_saved = True
                    except Exception as e:
                        logger.exception(f"Failed to save config for {page_name}: {e}")
                        save_errors.append(f"{page_name}: {str(e)}")
                
                # Cleanup page resources
                if hasattr(page, 'cleanup'):
                    try:
                        page.cleanup()
                    except Exception as e:
                        logger.exception(f"Failed to cleanup {page_name}: {e}")
            
            # Show consolidated message if configs were saved
            if config_saved and not save_errors:
                QMessageBox.information(
                    self,
                    "Configuration Saved",
                    "All configuration changes have been saved.\n\n"
                    "⚠️ Note: Some changes require a service restart to take effect."
                )
            elif save_errors:
                QMessageBox.warning(
                    self,
                    "Save Errors",
                    f"Some configurations failed to save:\n\n" + "\n".join(save_errors[:3])
                )
            
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
    
    def quit_application(self) -> None:
        """Quit the application (actually close, not minimize to tray)."""
        self._is_quitting = True
        self.close()


def show_instance_selector(config: ClientConfig, available_configs: list = None) -> Optional[str]:
    """Show instance selector dialog and return selected instance name.
    
    Args:
        config: ClientConfig instance for defaults
        available_configs: List of Path objects to existing config files
    
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
    
    dialog = InstanceSelectorDialog(config, available_configs)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        instance_name = dialog.get_instance_name()
        if temp_app:
            temp_app.quit()
        return instance_name
    else:
        if temp_app:
            temp_app.quit()
        return None
