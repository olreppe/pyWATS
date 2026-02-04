"""Proxy Settings Page - Migrated with reliability improvements.

Improvements:
- H1: Error handling for save_config()
- H4: cleanup() method
- Input validation for host/port
"""

import logging
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QCheckBox, QRadioButton, QButtonGroup, QSpinBox, QGroupBox,
    QMessageBox, QPushButton
)
from PySide6.QtCore import Qt

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = logging.getLogger(__name__)


class ProxySettingsPage(BasePage):
    """Proxy settings page"""
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Proxy Settings"
    
    def _setup_ui(self) -> None:
        """Setup page UI matching WATS Client design"""
        # Proxy mode selection
        self._proxy_mode_group = QButtonGroup(self)
        
        self._no_proxy_radio = QRadioButton("No proxy")
        self._system_proxy_radio = QRadioButton("Use system proxy settings")
        self._manual_proxy_radio = QRadioButton("Manual proxy configuration")
        
        self._proxy_mode_group.addButton(self._no_proxy_radio, 0)
        self._proxy_mode_group.addButton(self._system_proxy_radio, 1)
        self._proxy_mode_group.addButton(self._manual_proxy_radio, 2)
        
        self._layout.addWidget(self._no_proxy_radio)
        self._layout.addWidget(self._system_proxy_radio)
        self._layout.addWidget(self._manual_proxy_radio)
        
        self._proxy_mode_group.buttonToggled.connect(self._on_proxy_mode_changed)
        
        self._layout.addSpacing(20)
        
        # Manual proxy settings group
        self._manual_group = QGroupBox("Manual proxy settings")
        manual_layout = QVBoxLayout(self._manual_group)
        
        # Proxy host
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Proxy host:"))
        self._host_edit = QLineEdit()
        self._host_edit.setPlaceholderText("proxy.example.com")
        host_layout.addWidget(self._host_edit, 1)
        manual_layout.addLayout(host_layout)
        
        # Proxy port
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Proxy port:"))
        self._port_spin = QSpinBox()
        self._port_spin.setRange(1, 65535)
        self._port_spin.setValue(8080)
        self._port_spin.setFixedWidth(100)
        port_layout.addWidget(self._port_spin)
        port_layout.addStretch()
        manual_layout.addLayout(port_layout)
        
        # Authentication
        self._auth_check = QCheckBox("Proxy requires authentication")
        self._auth_check.toggled.connect(self._on_auth_toggled)
        manual_layout.addWidget(self._auth_check)
        
        # Username
        user_layout = QHBoxLayout()
        self._user_label = QLabel("Username:")
        user_layout.addWidget(self._user_label)
        self._user_edit = QLineEdit()
        user_layout.addWidget(self._user_edit, 1)
        manual_layout.addLayout(user_layout)
        
        # Password
        pass_layout = QHBoxLayout()
        self._pass_label = QLabel("Password:")
        pass_layout.addWidget(self._pass_label)
        self._pass_edit = QLineEdit()
        self._pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        pass_layout.addWidget(self._pass_edit, 1)
        manual_layout.addLayout(pass_layout)
        
        self._layout.addWidget(self._manual_group)
        
        # Bypass list
        self._bypass_group = QGroupBox("Bypass proxy for")
        bypass_layout = QVBoxLayout(self._bypass_group)
        
        self._bypass_edit = QLineEdit()
        self._bypass_edit.setPlaceholderText("localhost, 127.0.0.1, *.local")
        bypass_layout.addWidget(self._bypass_edit)
        
        bypass_help = QLabel("Comma-separated list of hosts that should bypass the proxy.")
        bypass_help.setStyleSheet("color: #808080; font-size: 11px;")
        bypass_layout.addWidget(bypass_help)
        
        self._layout.addWidget(self._bypass_group)
        
        # Add stretch to push content to top
        self._layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config)
        self._layout.addWidget(save_btn)
        
        # Set initial state
        self._update_manual_group_state()
        self._on_auth_toggled(False)
    
    def _on_proxy_mode_changed(self) -> None:
        """Handle proxy mode selection change"""
        self._update_manual_group_state()
    
    def _update_manual_group_state(self) -> None:
        """Enable/disable manual proxy settings based on mode"""
        is_manual = self._manual_proxy_radio.isChecked()
        self._manual_group.setEnabled(is_manual)
        self._bypass_group.setEnabled(is_manual)
    
    def _on_auth_toggled(self, checked: bool) -> None:
        """Enable/disable authentication fields"""
        self._user_label.setEnabled(checked)
        self._user_edit.setEnabled(checked)
        self._pass_label.setEnabled(checked)
        self._pass_edit.setEnabled(checked)
    
    def save_config(self) -> None:
        """Save configuration (H1 fix - error handling)"""
        try:
            # Determine proxy mode
            if self._no_proxy_radio.isChecked():
                proxy_mode = "none"
            elif self._system_proxy_radio.isChecked():
                proxy_mode = "system"
            else:
                proxy_mode = "manual"
                
                # Validate manual proxy settings
                host = self._host_edit.text().strip()
                if not host:
                    QMessageBox.warning(
                        self,
                        "Invalid Configuration",
                        "Proxy host is required when using manual proxy configuration.\n\n"
                        "Please enter a proxy host or select a different proxy mode."
                    )
                    return
            
            # Update config
            self._config["proxy_mode"] = proxy_mode
            self._config["proxy_host"] = self._host_edit.text()
            self._config["proxy_port"] = self._port_spin.value()
            self._config["proxy_auth"] = self._auth_check.isChecked()
            self._config["proxy_username"] = self._user_edit.text()
            self._config["proxy_password"] = self._pass_edit.text()
            self._config["proxy_bypass"] = self._bypass_edit.text()
            
            # Save to disk
            self._config.save()
            
            logger.info(f"Proxy settings saved: mode={proxy_mode}")
            
            QMessageBox.information(
                self,
                "Configuration Saved",
                "Proxy settings have been saved successfully.\n\n"
                "Restart the application for changes to take effect."
            )
            
        except Exception as e:
            logger.exception(f"Failed to save proxy settings: {e}")
            QMessageBox.critical(
                self,
                "Save Failed",
                f"Failed to save proxy settings.\n\n"
                f"Error: {e}\n\n"
                "Please check the logs for details and try again."
            )
    
    def load_config(self) -> None:
        """Load configuration"""
        try:
            mode = self._config.get("proxy_mode", "system")
            if mode == "none":
                self._no_proxy_radio.setChecked(True)
            elif mode == "system":
                self._system_proxy_radio.setChecked(True)
            else:
                self._manual_proxy_radio.setChecked(True)
            
            self._host_edit.setText(self._config.get("proxy_host", ""))
            self._port_spin.setValue(self._config.get("proxy_port", 8080))
            self._auth_check.setChecked(self._config.get("proxy_auth", False))
            self._user_edit.setText(self._config.get("proxy_username", ""))
            self._pass_edit.setText(self._config.get("proxy_password", ""))
            self._bypass_edit.setText(self._config.get("proxy_bypass", ""))
            
            self._update_manual_group_state()
            self._on_auth_toggled(self._auth_check.isChecked())
            
            logger.debug("Proxy settings loaded")
            
        except Exception as e:
            logger.exception(f"Failed to load proxy settings: {e}")
            QMessageBox.warning(
                self,
                "Load Failed",
                f"Failed to load proxy settings.\n\nError: {e}\n\n"
                "Using default values."
            )
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix - consistency)"""
        pass  # No resources to clean
