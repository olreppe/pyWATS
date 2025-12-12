"""
Main Window for WATS Client GUI

Implements the main application window with navigation sidebar
and content pages matching the WATS Client design.
"""

import asyncio
from typing import Optional, Dict, Any, TYPE_CHECKING, cast
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
    BasePage, SetupPage, GeneralPage, ConnectionPage, ProxySettingsPage, 
    ConvertersPage, LocationPage, SNHandlerPage, SoftwarePage, AboutPage
)
from ..core.config import ClientConfig
from ..app import pyWATSApplication, ApplicationStatus


class MainWindow(QMainWindow):
    """
    Main application window for WATS Client.
    
    Features:
    - Navigation sidebar with page selection
    - Stacked widget for page content
    - System tray integration
    - Status bar with connection info
    - Integration with pyWATSApplication service layer
    """
    
    # Signals for async updates
    connection_status_changed = Signal(str)
    application_status_changed = Signal(str)
    
    def __init__(
        self, 
        config: ClientConfig, 
        app: Optional[pyWATSApplication] = None, 
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        
        self.config = config
        self.app = app if app else pyWATSApplication(config)  # pyWATSApplication instance
        self._tray_icon: Optional[QSystemTrayIcon] = None
        self._is_connected = False
        
        # Setup UI
        self._setup_window()
        self._setup_tray_icon()
        self._setup_ui()
        self._apply_styles()
        self._connect_signals()
        
        # Connect application status callbacks
        self.app.on_status_changed(self._on_app_status_changed)
        
        # Update timer for status refresh
        self._status_timer = QTimer()
        self._status_timer.timeout.connect(self._update_status)
        self._status_timer.start(5000)  # Update every 5 seconds
        
        # Auto-start application if previously connected or auto_connect is enabled
        QTimer.singleShot(500, self._auto_start_on_startup)
    
    def _auto_start_on_startup(self) -> None:
        """Auto-start application on startup if configured"""
        # Check if we should auto-start
        if self.config.auto_connect and self.config.was_connected:
            # Only auto-start if we have valid credentials
            if self.config.service_address and self.config.api_token:
                asyncio.create_task(self._do_auto_start())
    
    async def _do_auto_start(self) -> None:
        """Perform auto-start of application services"""
        try:
            self.application_status_changed.emit("Starting")
            await self.app.start()
            self._is_connected = True
            
            # Update UI based on connection status
            if self.app.is_online():
                self.connection_status_changed.emit("Online")
            else:
                self.connection_status_changed.emit("Offline (Queuing)")
            
            # Update setup page state
            if "Setup" in self._pages:
                setup_page = cast(SetupPage, self._pages["Setup"])
                setup_page.set_connected(True)
        except Exception as e:
            self.connection_status_changed.emit(f"Error: {str(e)[:20]}")
            self.application_status_changed.emit("Error")
    
    def _on_app_status_changed(self, status: ApplicationStatus) -> None:
        """Handle application status changes"""
        self.application_status_changed.emit(status.value)
    
    def _setup_window(self) -> None:
        """Configure window properties"""
        self.setWindowTitle(f"WATS Client - {self.config.instance_name}")
        self.setMinimumSize(800, 600)
        self.resize(900, 650)
        
        # Set window icon for taskbar
        from PySide6.QtGui import QIcon
        icon_path = Path(__file__).parent / "resources" / "favicon2.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
    
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
        
        # Add navigation items matching reference design (from screenshots)
        nav_items = [
            ("Setup", "⚙️"),
            ("Connection", "🔗"),
            ("Location", "📍"),
            ("Converters", "🔄"),
            ("SN Handler", "🔢"),
            ("Proxy Settings", "🌐"),
            ("Software", "💻"),
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
        
        # Create pages matching reference design (from screenshots)
        self._pages: Dict[str, BasePage] = {
            "Setup": SetupPage(self.config, self),
            "Connection": ConnectionPage(self.config, self),
            "Location": LocationPage(self.config, self),
            "Converters": ConvertersPage(self.config, self),
            "SN Handler": SNHandlerPage(self.config, self),
            "Proxy Settings": ProxySettingsPage(self.config),
            "Software": SoftwarePage(self.config, self),
        }
        
        for page in self._pages.values():
            self._page_stack.addWidget(page)
            # Connect config change signal to enable Apply button
            if hasattr(page, 'config_changed'):
                page.config_changed.connect(self._on_config_changed)
        
        content_layout.addWidget(self._page_stack, 1)
        
        # Add stretch to push buttons to bottom
        content_layout.addStretch()
        
        # Apply/Cancel buttons at bottom
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 5, 0, 5)
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
        self.application_status_changed.connect(self._on_application_status_ui)
        
        # Connect page change signals
        for page in self._pages.values():
            if hasattr(page, 'config_changed'):
                page.config_changed.connect(self._on_config_changed)
        
        # Connect setup page connection signal
        if "Setup" in self._pages:
            setup_page = cast(SetupPage, self._pages["Setup"])
            setup_page.connection_changed.connect(self._on_connection_request)
    
    @Slot(bool)
    def _on_connection_request(self, should_connect: bool) -> None:
        """Handle connection request from setup page"""
        if should_connect:
            asyncio.create_task(self._perform_start())
        else:
            asyncio.create_task(self._perform_stop())
    
    async def _perform_start(self) -> None:
        """Start application services"""
        self.application_status_changed.emit("Starting")
        try:
            await self.app.start()
            self._is_connected = True
            
            # Update connection status based on actual connection
            if self.app.is_online():
                self.connection_status_changed.emit("Online")
            else:
                self.connection_status_changed.emit("Offline (Queuing)")
            
            self.application_status_changed.emit("Running")
        except Exception as e:
            self.connection_status_changed.emit(f"Error: {str(e)[:20]}")
            self.application_status_changed.emit("Error")
            # Revert setup page state
            if "Setup" in self._pages:
                setup_page = cast(SetupPage, self._pages["Setup"])
                setup_page.set_connected(False)
    
    async def _perform_stop(self) -> None:
        """Stop application services"""
        self.application_status_changed.emit("Stopping")
        await self.app.stop()
        self._is_connected = False
        self.connection_status_changed.emit("Disconnected")
        self.application_status_changed.emit("Stopped")
    
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
        """Handle Apply button click - save changes and disable button"""
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
    def _on_application_status_ui(self, status: str) -> None:
        """Update UI for application status change"""
        # Update window title with status
        title = f"WATS Client - {self.config.instance_name}"
        if status not in ["Stopped", "Running"]:
            title += f" [{status}]"
        self.setWindowTitle(title)
    
    def _update_status(self) -> None:
        """Periodic status update"""
        # Update connection status
        if self.app.is_online():
            self.connection_status_changed.emit("Online")
        elif self.app.status == ApplicationStatus.RUNNING:
            self.connection_status_changed.emit("Offline (Queuing)")
        
        # Update queue status
        queue_status = self.app.get_queue_status()
        if queue_status.get("pending_reports", 0) > 0:
            pending = queue_status["pending_reports"]
            self._status_label.setToolTip(f"{pending} reports queued")
    
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
        # Stop application services
        asyncio.create_task(self.app.stop())
        
        # Hide tray icon
        if self._tray_icon:
            self._tray_icon.hide()
        
        QApplication.quit()
    
    # Public methods for pages
    
    async def test_connection(self) -> bool:
        """Test connection to WATS server"""
        if self.app.wats_client:
            # Test connection by refreshing process cache
            try:
                self.app.wats_client.process.refresh()
                return True
            except Exception:
                return False
        return False
    
    async def start_services(self) -> bool:
        """Start application services"""
        try:
            await self.app.start()
            self._is_connected = True
            # Persist connection state
            self.config.was_connected = True
            self._save_config()
            return True
        except Exception:
            return False
    
    async def stop_services(self) -> None:
        """Stop application services"""
        self._is_connected = False
        # Persist disconnected state
        self.config.was_connected = False
        self._save_config()
        await self.app.stop()
    
    async def refresh_converters(self) -> None:
        """Refresh converters from converter manager"""
        if self.app.converter_manager:
            # Converter manager handles converter discovery
            pass

    async def send_test_uut(self) -> dict:
        """
        Send a test UUT report to verify full connectivity.
        
        Creates a comprehensive test report with various test types
        and submits it to the WATS server.
        
        Returns:
            dict with keys:
                - success: bool indicating if submission was successful
                - report_id: UUID of submitted report (if successful)
                - serial_number: Serial number of test report
                - part_number: Part number of test report
                - error: Error message (if failed)
        """
        from pywats.tools.test_uut import create_test_uut_report
        
        try:
            # Create test report with station name from config
            report = create_test_uut_report(
                station_name=self.config.station_name or "pyWATS-Client",
                location=self.config.location or "TestLocation",
                operator_name=getattr(self.config, 'operator', 'pyWATS-User')
            )
            
            result = {
                "success": False,
                "serial_number": report.sn,
                "part_number": report.pn,
                "report_id": str(report.id)
            }
            
            if self.app.wats_client:
                # Convert to dictionary for submission
                report_data = report.model_dump(mode="json", by_alias=True, exclude_none=True)
                
                # Submit the report via API client
                submit_result = await self.app.wats_client.report.create(report_data)
                if submit_result:
                    result["success"] = True
                else:
                    result["error"] = "Report submission returned false"
            else:
                result["error"] = "Client not initialized"
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "serial_number": "N/A",
                "part_number": "N/A"
            }

    async def test_send_uut(self) -> bool:
        """
        Create and submit a test UUT report.
        
        Uses the test_uut module to create a comprehensive test report
        demonstrating all pyWATS features.
        """
        if not self.app.wats_client:
            return False
        
        try:
            from pywats.tools import create_test_uut_report
            
            # Create test report using configured location and station
            report = create_test_uut_report(
                station_name=self.config.station_name or "pyWATS-Client",
                location=self.config.location or "TestLocation",
            )
            
            # Convert to dictionary for submission (Pydantic model_dump with by_alias for serialization)
            report_data = report.model_dump(mode="json", by_alias=True, exclude_none=True)
            
            # Submit via API client
            result = await self.app.wats_client.report.create(report_data)
            return bool(result)
        except Exception as e:
            print(f"Error creating/submitting test UUT: {e}")
            return False
