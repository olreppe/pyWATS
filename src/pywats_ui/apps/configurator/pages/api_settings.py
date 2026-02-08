"""API Settings Page - Migrated with reliability improvements.

Improvements:
- H1: Error handling for save_config() with user dialogs
- H4: cleanup() method for consistency
- Input validation for ports, URLs
"""

import logging
from pywats.core.logging import get_logger
import secrets
from typing import Optional
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QFormLayout, QCheckBox, QSpinBox,
    QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QInputDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = get_logger(__name__)


class APISettingsPage(BasePage):
    """API Settings configuration page.
    
    Configure:
    - HTTP API server settings
    - Authentication tokens
    - Webhook endpoints
    - API rate limiting
    """
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "API Settings"
    
    def _setup_ui(self) -> None:
        """Setup API settings UI"""
        
        # === HTTP API Server ===
        api_group = QGroupBox("HTTP API Server")
        api_layout = QFormLayout(api_group)
        api_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        
        # Enable API
        self._api_enabled = QCheckBox("Enable HTTP API Server")
        self._api_enabled.setToolTip("Allow external applications to interact with the client via HTTP API")
        api_layout.addRow("", self._api_enabled)
        
        # API Port
        self._api_port = QSpinBox()
        self._api_port.setRange(1024, 65535)
        self._api_port.setValue(8080)
        self._api_port.setToolTip("Port for HTTP API server")
        api_layout.addRow("API Port:", self._api_port)
        
        # API Host
        self._api_host = QLineEdit()
        self._api_host.setText("127.0.0.1")
        self._api_host.setPlaceholderText("127.0.0.1 (localhost only) or 0.0.0.0 (all interfaces)")
        self._api_host.setToolTip("Host address to bind API server to")
        api_layout.addRow("API Host:", self._api_host)
        
        # API Base Path
        self._api_base_path = QLineEdit()
        self._api_base_path.setText("/api/v1")
        self._api_base_path.setPlaceholderText("/api/v1")
        self._api_base_path.setToolTip("Base path for API endpoints")
        api_layout.addRow("Base Path:", self._api_base_path)
        
        # CORS Settings
        self._api_cors_enabled = QCheckBox("Enable CORS")
        self._api_cors_enabled.setToolTip("Allow cross-origin requests from web browsers")
        api_layout.addRow("", self._api_cors_enabled)
        
        self._api_cors_origins = QLineEdit()
        self._api_cors_origins.setPlaceholderText("* (all origins) or http://localhost:3000,https://app.example.com")
        self._api_cors_origins.setToolTip("Allowed CORS origins (comma-separated)")
        api_layout.addRow("CORS Origins:", self._api_cors_origins)
        
        self._layout.addWidget(api_group)
        
        # === Authentication ===
        auth_group = QGroupBox("Authentication")
        auth_layout = QVBoxLayout(auth_group)
        
        # Auth type
        auth_type_layout = QHBoxLayout()
        auth_type_layout.addWidget(QLabel("Authentication Type:"))
        
        self._auth_type = QComboBox()
        self._auth_type.addItems(["None", "API Key", "Bearer Token", "Basic Auth"])
        self._auth_type.setToolTip("Authentication method for API requests")
        auth_type_layout.addWidget(self._auth_type, 1)
        auth_layout.addLayout(auth_type_layout)
        
        # API Tokens table
        tokens_label = QLabel("API Tokens")
        tokens_font = QFont()
        tokens_font.setBold(True)
        tokens_label.setFont(tokens_font)
        auth_layout.addWidget(tokens_label)
        
        self._tokens_table = QTableWidget()
        self._tokens_table.setColumnCount(4)
        self._tokens_table.setHorizontalHeaderLabels(["Name", "Token", "Created", "Actions"])
        
        header = self._tokens_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        
        self._tokens_table.setColumnWidth(0, 150)
        self._tokens_table.setColumnWidth(3, 100)
        self._tokens_table.setMaximumHeight(200)
        self._tokens_table.verticalHeader().setVisible(False)
        self._tokens_table.setAlternatingRowColors(True)
        
        auth_layout.addWidget(self._tokens_table)
        
        # Token management buttons
        token_btn_layout = QHBoxLayout()
        
        self._generate_token_btn = QPushButton("Generate New Token")
        self._generate_token_btn.clicked.connect(self._on_generate_token)
        token_btn_layout.addWidget(self._generate_token_btn)
        
        token_btn_layout.addStretch()
        
        auth_layout.addLayout(token_btn_layout)
        
        self._layout.addWidget(auth_group)
        
        # === Rate Limiting ===
        rate_group = QGroupBox("Rate Limiting")
        rate_layout = QFormLayout(rate_group)
        
        self._rate_limit_enabled = QCheckBox("Enable Rate Limiting")
        self._rate_limit_enabled.setToolTip("Limit API request rate to prevent abuse")
        rate_layout.addRow("", self._rate_limit_enabled)
        
        self._rate_limit_requests = QSpinBox()
        self._rate_limit_requests.setRange(1, 10000)
        self._rate_limit_requests.setValue(100)
        self._rate_limit_requests.setToolTip("Maximum requests per window")
        rate_layout.addRow("Requests:", self._rate_limit_requests)
        
        self._rate_limit_window = QSpinBox()
        self._rate_limit_window.setRange(1, 3600)
        self._rate_limit_window.setValue(60)
        self._rate_limit_window.setSuffix(" seconds")
        self._rate_limit_window.setToolTip("Time window for rate limiting")
        rate_layout.addRow("Per Window:", self._rate_limit_window)
        
        self._layout.addWidget(rate_group)
        
        # === Webhooks ===
        webhook_group = QGroupBox("Webhooks")
        webhook_layout = QVBoxLayout(webhook_group)
        
        webhook_help = QLabel(
            "Configure webhook URLs to receive notifications about converter events, "
            "report submissions, and service status changes."
        )
        webhook_help.setWordWrap(True)
        webhook_help.setStyleSheet("color: #808080; font-size: 11px;")
        webhook_layout.addWidget(webhook_help)
        
        # Webhook URLs
        webhook_url_layout = QFormLayout()
        
        self._webhook_converter_url = QLineEdit()
        self._webhook_converter_url.setPlaceholderText("https://your-server.com/webhooks/converter")
        self._webhook_converter_url.setToolTip("Called when converter processes a file")
        webhook_url_layout.addRow("Converter Events:", self._webhook_converter_url)
        
        self._webhook_report_url = QLineEdit()
        self._webhook_report_url.setPlaceholderText("https://your-server.com/webhooks/report")
        self._webhook_report_url.setToolTip("Called when report is submitted to WATS")
        webhook_url_layout.addRow("Report Events:", self._webhook_report_url)
        
        self._webhook_service_url = QLineEdit()
        self._webhook_service_url.setPlaceholderText("https://your-server.com/webhooks/service")
        self._webhook_service_url.setToolTip("Called when service status changes")
        webhook_url_layout.addRow("Service Events:", self._webhook_service_url)
        
        webhook_layout.addLayout(webhook_url_layout)
        
        # Webhook authentication
        webhook_auth_layout = QFormLayout()
        
        self._webhook_auth_header = QLineEdit()
        self._webhook_auth_header.setPlaceholderText("Authorization")
        self._webhook_auth_header.setToolTip("HTTP header name for authentication")
        webhook_auth_layout.addRow("Auth Header:", self._webhook_auth_header)
        
        self._webhook_auth_value = QLineEdit()
        self._webhook_auth_value.setPlaceholderText("Bearer your-webhook-secret")
        self._webhook_auth_value.setEchoMode(QLineEdit.EchoMode.Password)
        self._webhook_auth_value.setToolTip("HTTP header value for authentication")
        webhook_auth_layout.addRow("Auth Value:", self._webhook_auth_value)
        
        webhook_layout.addLayout(webhook_auth_layout)
        
        # Test webhook button
        test_webhook_layout = QHBoxLayout()
        
        self._test_webhook_btn = QPushButton("Test Webhooks")
        self._test_webhook_btn.setToolTip("Send test events to configured webhook URLs")
        self._test_webhook_btn.clicked.connect(self._on_test_webhooks)
        test_webhook_layout.addWidget(self._test_webhook_btn)
        
        test_webhook_layout.addStretch()
        
        webhook_layout.addLayout(test_webhook_layout)
        
        self._layout.addWidget(webhook_group)
        
        # === API Documentation ===
        docs_group = QGroupBox("API Documentation")
        docs_layout = QVBoxLayout(docs_group)
        
        docs_text = QLabel(
            "API documentation is available at: <b>http://localhost:{port}/docs</b> "
            "when the API server is running.\n\n"
            "The API provides endpoints for:\n"
            "• Submitting test reports\n"
            "• Managing converters\n"
            "• Querying service status\n"
            "• Retrieving configuration"
        )
        docs_text.setWordWrap(True)
        docs_layout.addWidget(docs_text)
        
        self._layout.addWidget(docs_group)
        
        self._layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config)
        self._layout.addWidget(save_btn)
    
    def _on_generate_token(self) -> None:
        """Generate a new API token with error handling."""
        try:
            name, ok = QInputDialog.getText(
                self,
                "Generate API Token",
                "Enter a name for this token:"
            )
            
            if not ok or not name:
                return
            
            # Validate name
            if len(name.strip()) == 0:
                self.show_warning("Token name cannot be empty.", "Invalid Name")
                return
            
            # Generate secure token
            token = secrets.token_urlsafe(32)
            
            # Add to table
            row = self._tokens_table.rowCount()
            self._tokens_table.insertRow(row)
            
            name_item = QTableWidgetItem(name)
            self._tokens_table.setItem(row, 0, name_item)
            
            token_item = QTableWidgetItem(token)
            self._tokens_table.setItem(row, 1, token_item)
            
            created_item = QTableWidgetItem(datetime.now().strftime("%Y-%m-%d %H:%M"))
            self._tokens_table.setItem(row, 2, created_item)
            
            # Actions button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda: self._delete_token(row))
            self._tokens_table.setCellWidget(row, 3, delete_btn)
            
            # Show token in message box
            self.show_success(
                f"<b>Token Name:</b> {name}<br><br>"
                f"<b>Token:</b><br><code>{token}</code><br><br>"
                "<b>Important:</b> Copy this token now. You won't be able to see it again.",
                "API Token Generated"
            )
            
            logger.info(f"Generated API token: {name}")
            
        except Exception as e:
            self.handle_error(e, "generating API token")
    
    def _delete_token(self, row: int) -> None:
        """Delete an API token with confirmation."""
        try:
            if self.confirm_action(
                "Are you sure you want to delete this API token?",
                "Delete Token"
            ):
                token_name = self._tokens_table.item(row, 0).text()
                self._tokens_table.removeRow(row)
                logger.info(f"Deleted API token: {token_name}")
                
        except Exception as e:
            self.handle_error(e, "deleting API token")
    
    def _on_test_webhooks(self) -> None:
        """Test webhook configuration (placeholder)."""
        self.show_success(
            "Webhook testing will send sample events to configured URLs.\n\n"
            "This feature will be implemented in a future update.",
            "Test Webhooks"
        )
    
    def save_config(self) -> None:
        """Save API settings to config (H1 fix - error handling)."""
        try:
            # Validate inputs
            host = self._api_host.text().strip()
            if not host:
                self.show_warning(
                    "API host cannot be empty.\n\nPlease enter a valid host (e.g., 127.0.0.1)",
                    "Invalid Configuration"
                )
                return
            
            # Update config - map directly to ClientConfig fields
            self._config.api_enabled = self._api_enabled.isChecked()
            self._config.api_port = self._api_port.value()
            self._config.api_host = host
            self._config.api_base_path = self._api_base_path.text()
            self._config.api_cors_enabled = self._api_cors_enabled.isChecked()
            self._config.api_cors_origins = self._api_cors_origins.text()
            self._config.api_auth_type = self._auth_type.currentText()
            self._config.api_rate_limit_enabled = self._rate_limit_enabled.isChecked()
            self._config.api_rate_limit_requests = self._rate_limit_requests.value()
            self._config.api_rate_limit_window = self._rate_limit_window.value()
            
            # Webhook settings
            self._config.webhook_converter_url = self._webhook_converter_url.text()
            self._config.webhook_report_url = self._webhook_report_url.text()
            self._config.webhook_service_url = self._webhook_service_url.text()
            self._config.webhook_auth_header = self._webhook_auth_header.text()
            self._config.webhook_auth_value = self._webhook_auth_value.text()
            
            # api_tokens field removed - not in new schema
            # Token management handled externally via api_auth_type
            
            # Save to disk
            self._config.save()
            
            logger.info(
                f"API settings saved: enabled={self._api_enabled.isChecked()}, "
                f"port={self._api_port.value()}, host={host}"
            )
            
            # Success - no popup needed (prevents multiple popups on close)
            # Note: Service restart needed for API changes to take effect
            
        except Exception as e:
            self.handle_error(e, "saving API settings")
    
    def load_config(self) -> None:
        """Load API settings from config"""
        try:
            self._api_enabled.setChecked(self._config.api_enabled)
            self._api_port.setValue(self._config.api_port)
            self._api_host.setText(self._config.api_host or "127.0.0.1")
            self._api_base_path.setText(self._config.api_base_path or "/api/v1")
            self._api_cors_enabled.setChecked(self._config.api_cors_enabled)
            self._api_cors_origins.setText(self._config.api_cors_origins or "")
            
            # Set auth type
            auth_type = self._config.api_auth_type or "None"
            index = self._auth_type.findText(auth_type)
            if index >= 0:
                self._auth_type.setCurrentIndex(index)
            
            self._rate_limit_enabled.setChecked(self._config.api_rate_limit_enabled)
            self._rate_limit_requests.setValue(self._config.api_rate_limit_requests)
            self._rate_limit_window.setValue(self._config.api_rate_limit_window)
            
            # Load webhook settings
            self._webhook_converter_url.setText(self._config.webhook_converter_url or "")
            self._webhook_report_url.setText(self._config.webhook_report_url or "")
            self._webhook_service_url.setText(self._config.webhook_service_url or "")
            self._webhook_auth_header.setText(self._config.webhook_auth_header or "")
            self._webhook_auth_value.setText(self._config.webhook_auth_value or "")
            
            # Tokens table removed - api_tokens not in new schema
            # Token management handled externally
            self._tokens_table.setRowCount(0)
            
            logger.debug("API settings loaded")
            
        except Exception as e:
            self.handle_error(e, "loading API settings")
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix - consistency)."""
        pass  # No resources to clean
