"""
Setup Page

Main setup page with:
- Computer name (read-only)
- Location
- Purpose
- Account/Server URL
- Token authentication
- Connect/Disconnect button
- Advanced options
"""

import socket
from typing import Optional, TYPE_CHECKING
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl

from .base import BasePage
from ...core.config import ClientConfig

if TYPE_CHECKING:
    from ..main_window import MainWindow


class SetupPage(BasePage):
    """Setup/Connection settings page"""
    
    # Signal emitted when connection state changes
    connection_changed = Signal(bool)  # True = connected, False = disconnected
    
    def __init__(
        self, 
        config: ClientConfig, 
        main_window: Optional['MainWindow'] = None,
        parent: Optional[QWidget] = None
    ):
        self._main_window = main_window
        self._is_connected = False
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Setup"
    
    def _setup_ui(self) -> None:
        """Setup page UI matching WATS Client design"""
        # Computer name (read-only)
        computer_layout = QHBoxLayout()
        computer_label = QLabel("Computer name")
        computer_label.setFixedWidth(120)
        computer_layout.addWidget(computer_label)
        
        self._computer_name_edit = QLineEdit()
        self._computer_name_edit.setReadOnly(True)
        self._computer_name_edit.setText(socket.gethostname().upper())
        self._computer_name_edit.setStyleSheet("background-color: #3c3c3c;")
        computer_layout.addWidget(self._computer_name_edit, 1)
        
        self._layout.addLayout(computer_layout)
        self._computer_name_edit.setToolTip("Used as station name in reports. Edit in Windows settings.")
        
        self._layout.addSpacing(10)
        
        # Location
        location_layout = QHBoxLayout()
        location_label = QLabel("Location")
        location_label.setFixedWidth(120)
        location_layout.addWidget(location_label)
        
        self._location_edit = QLineEdit()
        self._location_edit.setPlaceholderText("e.g., Building A, Floor 2")
        self._location_edit.textChanged.connect(self._emit_changed)
        location_layout.addWidget(self._location_edit, 1)
        
        self._layout.addLayout(location_layout)
        
        # Purpose
        purpose_layout = QHBoxLayout()
        purpose_label = QLabel("Purpose")
        purpose_label.setFixedWidth(120)
        purpose_layout.addWidget(purpose_label)
        
        self._purpose_edit = QLineEdit()
        self._purpose_edit.setPlaceholderText("e.g., Production Testing")
        self._purpose_edit.textChanged.connect(self._emit_changed)
        purpose_layout.addWidget(self._purpose_edit, 1)
        
        self._layout.addLayout(purpose_layout)
        self._location_edit.setToolTip("Station location shown in reports and dashboards")
        self._purpose_edit.setToolTip("Station purpose shown in reports and dashboards")
        
        self._layout.addSpacing(10)
        
        # Account / Server
        server_layout = QHBoxLayout()
        server_label = QLabel("Account / Server")
        server_label.setFixedWidth(120)
        server_layout.addWidget(server_label)
        
        self._server_edit = QLineEdit()
        self._server_edit.setPlaceholderText("https://your-account.wats.com/")
        self._server_edit.textChanged.connect(self._emit_changed)
        server_layout.addWidget(self._server_edit, 1)
        
        self._layout.addLayout(server_layout)
        self._server_edit.setToolTip("e.g. virinco.wats.com")
        
        self._layout.addSpacing(10)
        
        # Token
        token_layout = QHBoxLayout()
        token_label = QLabel("Token")
        token_label.setFixedWidth(120)
        token_layout.addWidget(token_label)
        
        self._token_edit = QLineEdit()
        self._token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._token_edit.setPlaceholderText("API access token")
        self._token_edit.setToolTip("Base64 encoded API token")
        self._token_edit.textChanged.connect(self._emit_changed)
        token_layout.addWidget(self._token_edit, 1)
        
        self._layout.addLayout(token_layout)
        
        self._layout.addSpacing(15)
        
        # Connect / New customer buttons
        button_layout = QHBoxLayout()
        button_layout.addSpacing(125)  # Align with fields
        
        self._connect_btn = QPushButton("Connect")
        self._connect_btn.setObjectName("primaryButton")
        self._connect_btn.setFixedWidth(100)
        self._connect_btn.clicked.connect(self._on_connect_clicked)
        button_layout.addWidget(self._connect_btn)
        
        button_layout.addSpacing(20)
        
        self._new_customer_btn = QPushButton("New customer")
        self._new_customer_btn.setFixedWidth(120)
        self._new_customer_btn.clicked.connect(self._on_new_customer_clicked)
        button_layout.addWidget(self._new_customer_btn)
        
        button_layout.addStretch()
        
        self._layout.addLayout(button_layout)
        
        self._layout.addSpacing(20)
        
        # Advanced options (collapsible)
        self._create_advanced_section()
        
        # Add stretch to push content to top
        self._layout.addStretch()
    
    def _create_advanced_section(self) -> None:
        """Create advanced options section"""
        # Advanced options header (clickable)
        self._advanced_expanded = False
        
        advanced_header = QHBoxLayout()
        self._advanced_toggle = QLabel("▶ Advanced options")
        self._advanced_toggle.setStyleSheet("color: #cccccc; font-weight: bold;")
        self._advanced_toggle.mousePressEvent = lambda e: self._toggle_advanced()
        advanced_header.addWidget(self._advanced_toggle)
        advanced_header.addStretch()
        self._layout.addLayout(advanced_header)
        
        # Advanced options content
        self._advanced_frame = QFrame()
        self._advanced_frame.setVisible(False)
        advanced_layout = QVBoxLayout(self._advanced_frame)
        advanced_layout.setContentsMargins(20, 10, 0, 0)
        
        # Sync interval
        sync_layout = QHBoxLayout()
        sync_label = QLabel("Sync interval")
        sync_label.setFixedWidth(100)
        sync_layout.addWidget(sync_label)
        
        self._sync_edit = QLineEdit()
        self._sync_edit.setFixedWidth(80)
        self._sync_edit.textChanged.connect(self._emit_changed)
        sync_layout.addWidget(self._sync_edit)
        sync_layout.addWidget(QLabel("seconds"))
        sync_layout.addStretch()
        advanced_layout.addLayout(sync_layout)
        
        # Auto-start service
        self._auto_start_cb = QCheckBox("Start service automatically on login")
        self._auto_start_cb.stateChanged.connect(self._on_auto_start_changed)
        advanced_layout.addWidget(self._auto_start_cb)
        
        self._layout.addWidget(self._advanced_frame)
    
    def _on_auto_start_changed(self, state: int) -> None:
        """Handle auto-start checkbox change"""
        enabled = state == Qt.CheckState.Checked.value
        try:
            # Only available on Windows
            import sys
            if sys.platform == 'win32':
                from ...services.windows_service import set_auto_start
                success = set_auto_start(enabled)
                if not success:
                    # Revert checkbox if failed
                    self._auto_start_cb.blockSignals(True)
                    self._auto_start_cb.setChecked(not enabled)
                    self._auto_start_cb.blockSignals(False)
                    QMessageBox.warning(
                        self, "Error",
                        "Failed to update auto-start setting.\n"
                        "You may need to run as administrator."
                    )
        except ImportError:
            pass
        self._emit_changed()
    
    def _toggle_advanced(self) -> None:
        """Toggle advanced options visibility"""
        self._advanced_expanded = not self._advanced_expanded
        self._advanced_frame.setVisible(self._advanced_expanded)
        if self._advanced_expanded:
            self._advanced_toggle.setText("▼ Advanced options")
        else:
            self._advanced_toggle.setText("▶ Advanced options")
    
    def _set_fields_enabled(self, enabled: bool) -> None:
        """Enable or disable input fields"""
        self._location_edit.setEnabled(enabled)
        self._purpose_edit.setEnabled(enabled)
        self._server_edit.setEnabled(enabled)
        self._token_edit.setEnabled(enabled)
        self._sync_edit.setEnabled(enabled)
        self._auto_start_cb.setEnabled(enabled)
        self._new_customer_btn.setEnabled(enabled)
    
    def set_connected(self, connected: bool) -> None:
        """Update UI for connected/disconnected state"""
        self._is_connected = connected
        if connected:
            self._connect_btn.setText("Disconnect")
            self._set_fields_enabled(False)
        else:
            self._connect_btn.setText("Connect")
            self._set_fields_enabled(True)
    
    @Slot()
    def _on_connect_clicked(self) -> None:
        """Handle connect/disconnect button click"""
        if self._is_connected:
            # Disconnect
            self.set_connected(False)
            self.connection_changed.emit(False)
        else:
            # Validate fields before connecting
            if not self._server_edit.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter a server address.")
                self._server_edit.setFocus()
                return
            
            if not self._token_edit.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter an API token.")
                self._token_edit.setFocus()
                return
            
            # Save configuration before connecting
            self.save_config()
            
            # Connect
            self.set_connected(True)
            self.connection_changed.emit(True)
    
    @Slot()
    def _on_new_customer_clicked(self) -> None:
        """Open new customer registration page"""
        QDesktopServices.openUrl(QUrl("https://www.wats.com/register"))
    
    def save_config(self) -> None:
        """Save configuration"""
        self.config.service_address = self._server_edit.text().strip()
        self.config.location = self._location_edit.text().strip()
        self.config.purpose = self._purpose_edit.text().strip()
        self.config.api_token = self._token_edit.text().strip()
        self.config.service_auto_start = self._auto_start_cb.isChecked()
        
        try:
            self.config.sync_interval_seconds = int(self._sync_edit.text())
        except (ValueError, TypeError):
            pass
        
        # Save to file
        if self.config._config_path:
            try:
                self.config.save()
            except Exception as e:
                print(f"Failed to save config: {e}")
    
    def load_config(self) -> None:
        """Load configuration"""
        self._server_edit.setText(self.config.service_address)
        self._location_edit.setText(self.config.location)
        self._purpose_edit.setText(self.config.purpose)
        self._token_edit.setText(self.config.api_token)
        self._sync_edit.setText(str(self.config.sync_interval_seconds))
        
        # Check actual auto-start state from system (Windows only)
        auto_start_enabled = False
        try:
            import sys
            if sys.platform == 'win32':
                from ...services.windows_service import is_auto_start_enabled
                auto_start_enabled = is_auto_start_enabled()
        except ImportError:
            auto_start_enabled = getattr(self.config, 'service_auto_start', False)
        
        self._auto_start_cb.blockSignals(True)
        self._auto_start_cb.setChecked(auto_start_enabled)
        self._auto_start_cb.blockSignals(False)
        
        # Check if we should be connected (auto-connect on startup)
        if self.config.auto_connect and self.config.was_connected:
            if self.config.service_address and self.config.api_token:
                # Will be connected by main window
                pass
