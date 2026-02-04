"""Main window for pyWATS Client Configurator."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTabWidget, QLineEdit, QTextEdit,
    QFormLayout, QGroupBox, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt
from pywats_ui.framework import BaseMainWindow
from .config import ConfiguratorConfig


class ConfiguratorWindow(BaseMainWindow):
    """Main window for pyWATS Client Configurator."""
    
    def __init__(self):
        super().__init__("pyWATS Client Configurator")
        self.config = ConfiguratorConfig()
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
        self.load_settings()
    
    def setup_ui(self):
        """Set up the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("pyWATS Client Configurator")
        header.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        
        # Connection Tab
        self.tabs.addTab(self.create_connection_tab(), "Connection")
        
        # Station Tab
        self.tabs.addTab(self.create_station_tab(), "Station Setup")
        
        # Service Tab
        self.tabs.addTab(self.create_service_tab(), "Service Control")
        
        # Logs Tab
        self.tabs.addTab(self.create_logs_tab(), "Logs")
        
        layout.addWidget(self.tabs)
        
        # Button bar
        button_layout = QHBoxLayout()
        
        self.btn_save = QPushButton("Save Configuration")
        self.btn_save.clicked.connect(self.save_settings)
        button_layout.addWidget(self.btn_save)
        
        self.btn_test = QPushButton("Test Connection")
        self.btn_test.clicked.connect(self.test_connection)
        button_layout.addWidget(self.btn_test)
        
        button_layout.addStretch()
        
        self.btn_close = QPushButton("Close")
        self.btn_close.clicked.connect(self.close)
        button_layout.addWidget(self.btn_close)
        
        layout.addLayout(button_layout)
    
    def create_connection_tab(self) -> QWidget:
        """Create connection configuration tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Connection settings group
        conn_group = QGroupBox("pyWATS Server Connection")
        conn_layout = QFormLayout(conn_group)
        
        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText("https://your-wats-server.com")
        conn_layout.addRow("Server URL:", self.txt_url)
        
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("username")
        conn_layout.addRow("Username:", self.txt_username)
        
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setPlaceholderText("password")
        conn_layout.addRow("Password:", self.txt_password)
        
        layout.addWidget(conn_group)
        
        # Info label
        info = QLabel(
            "Configure your connection to the pyWATS server.\n"
            "Credentials are stored securely in your user directory."
        )
        info.setStyleSheet("color: gray; padding: 10px;")
        layout.addWidget(info)
        
        layout.addStretch()
        
        return tab
    
    def create_station_tab(self) -> QWidget:
        """Create station setup tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Station settings group
        station_group = QGroupBox("Test Station Configuration")
        station_layout = QFormLayout(station_group)
        
        self.txt_station_name = QLineEdit()
        self.txt_station_name.setPlaceholderText("Station-001")
        station_layout.addRow("Station Name:", self.txt_station_name)
        
        self.txt_station_id = QLineEdit()
        self.txt_station_id.setPlaceholderText("12345")
        station_layout.addRow("Station ID:", self.txt_station_id)
        
        layout.addWidget(station_group)
        
        # Converter settings group
        converter_group = QGroupBox("Converter Configuration")
        converter_layout = QVBoxLayout(converter_group)
        
        converter_info = QLabel(
            "Converter settings allow pyWATS to process test result files\n"
            "from various test equipment formats (Teradyne, Seica, etc.)"
        )
        converter_info.setStyleSheet("color: gray; padding: 5px;")
        converter_layout.addWidget(converter_info)
        
        # TODO: Add converter list/config when needed
        
        layout.addWidget(converter_group)
        
        layout.addStretch()
        
        return tab
    
    def create_service_tab(self) -> QWidget:
        """Create service control tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Service status group
        status_group = QGroupBox("pyWATS Client Service Status")
        status_layout = QVBoxLayout(status_group)
        
        self.lbl_service_status = QLabel("Status: Unknown")
        self.lbl_service_status.setStyleSheet("font-size: 14px; padding: 10px;")
        status_layout.addWidget(self.lbl_service_status)
        
        # Service control buttons
        control_layout = QHBoxLayout()
        
        self.btn_start_service = QPushButton("Start Service")
        self.btn_start_service.clicked.connect(self.start_service)
        control_layout.addWidget(self.btn_start_service)
        
        self.btn_stop_service = QPushButton("Stop Service")
        self.btn_stop_service.clicked.connect(self.stop_service)
        control_layout.addWidget(self.btn_stop_service)
        
        self.btn_restart_service = QPushButton("Restart Service")
        self.btn_restart_service.clicked.connect(self.restart_service)
        control_layout.addWidget(self.btn_restart_service)
        
        control_layout.addStretch()
        
        status_layout.addLayout(control_layout)
        
        layout.addWidget(status_group)
        
        layout.addStretch()
        
        return tab
    
    def create_logs_tab(self) -> QWidget:
        """Create logs viewer tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Log viewer
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setPlaceholderText("Service logs will appear here...")
        layout.addWidget(self.txt_logs)
        
        # Log controls
        log_controls = QHBoxLayout()
        
        btn_refresh_logs = QPushButton("Refresh")
        btn_refresh_logs.clicked.connect(self.refresh_logs)
        log_controls.addWidget(btn_refresh_logs)
        
        btn_clear_logs = QPushButton("Clear")
        btn_clear_logs.clicked.connect(lambda: self.txt_logs.clear())
        log_controls.addWidget(btn_clear_logs)
        
        log_controls.addStretch()
        
        layout.addLayout(log_controls)
        
        return tab
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        save_action = file_menu.addAction("&Save Configuration")
        save_action.triggered.connect(self.save_settings)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("E&xit")
        exit_action.triggered.connect(self.close)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        test_action = tools_menu.addAction("&Test Connection")
        test_action.triggered.connect(self.test_connection)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(self.show_about)
    
    def setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - pyWATS Client Configurator")
    
    def load_settings(self):
        """Load settings from configuration."""
        self.txt_url.setText(self.config.get("server_url", ""))
        self.txt_username.setText(self.config.get("username", ""))
        # Don't load password for security
        self.txt_station_name.setText(self.config.get("station_name", ""))
        self.txt_station_id.setText(self.config.get("station_id", ""))
    
    def save_settings(self):
        """Save settings to configuration."""
        self.config.set("server_url", self.txt_url.text())
        self.config.set("username", self.txt_username.text())
        # Password should be stored securely (TODO: use keyring)
        self.config.set("station_name", self.txt_station_name.text())
        self.config.set("station_id", self.txt_station_id.text())
        
        self.status_bar.showMessage("Configuration saved", 3000)
        QMessageBox.information(
            self,
            "Settings Saved",
            "pyWATS Client Configurator settings have been saved successfully."
        )
    
    def test_connection(self):
        """Test connection to pyWATS server."""
        self.status_bar.showMessage("Testing connection...", 0)
        
        # TODO: Actual connection test using pyWATS API
        # For now, just show placeholder
        url = self.txt_url.text()
        username = self.txt_username.text()
        
        if not url or not username:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter server URL and username before testing connection."
            )
            self.status_bar.showMessage("Connection test cancelled", 3000)
            return
        
        # Placeholder success message
        QMessageBox.information(
            self,
            "Connection Test",
            f"Connection test placeholder.\n\n"
            f"Server: {url}\n"
            f"Username: {username}\n\n"
            f"TODO: Implement actual pyWATS API connection test"
        )
        self.status_bar.showMessage("Connection test complete", 3000)
    
    def start_service(self):
        """Start pyWATS client service."""
        self.status_bar.showMessage("Starting service...", 3000)
        # TODO: Implement service start
        self.lbl_service_status.setText("Status: Starting...")
    
    def stop_service(self):
        """Stop pyWATS client service."""
        self.status_bar.showMessage("Stopping service...", 3000)
        # TODO: Implement service stop
        self.lbl_service_status.setText("Status: Stopping...")
    
    def restart_service(self):
        """Restart pyWATS client service."""
        self.status_bar.showMessage("Restarting service...", 3000)
        # TODO: Implement service restart
        self.lbl_service_status.setText("Status: Restarting...")
    
    def refresh_logs(self):
        """Refresh log viewer."""
        self.status_bar.showMessage("Refreshing logs...", 2000)
        # TODO: Load actual logs from file
        self.txt_logs.append("[INFO] Log refresh placeholder")
        self.txt_logs.append("[INFO] TODO: Implement actual log file reading")
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About pyWATS Client Configurator",
            "<h2>pyWATS Client Configurator</h2>"
            "<p>Version 0.3.0</p>"
            "<p>Configure and manage pyWATS client service.</p>"
            "<p>Part of the pyWATS GUI framework.</p>"
            "<p>© 2026 Virinco AS</p>"
        )
