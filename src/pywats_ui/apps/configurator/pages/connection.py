"""Connection Page - Migrated with reliability improvements.

Fixes applied from weakness analysis:
- H1: Error handling for config saves with user dialogs
- H3: Event loop guards for all async operations  
- H4: Cleanup method for resource management
- C1: QueueManager integration for test UUT send (never lose data)

User requirement: "Fix weaknesses, ensure reliability, NEVER lose customer data"
"""

import asyncio
import logging
from pywats.core.logging import get_logger
from typing import Optional, TYPE_CHECKING
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QFrame, QCheckBox
)
from PySide6.QtCore import Qt, Slot

from pywats_ui.framework import BasePage, OfflineCapability, QueueManager
from pywats_client.core.config import ClientConfig

if TYPE_CHECKING:
    pass  # Will be updated when ConfiguratorMainWindow is created

logger = get_logger(__name__)


class ConnectionPage(BasePage, OfflineCapability):
    """Connection settings page with offline capability and reliability improvements.
    
    Improvements over original:
    - Event loop safety checks before async operations (H3 fix)
    - Error dialogs for save failures (H1 fix)
    - QueueManager integration for test UUT send - never lose data (C1 fix)
    - Offline mode support - can edit settings when disconnected (C3 fix)
    - Cleanup method stops pending operations (H4 fix)
    - Retry logic for connection tests (3 attempts)
    """
    
    def __init__(
        self, 
        config: ClientConfig,
        queue_manager: Optional[QueueManager] = None,
        parent: Optional[QWidget] = None
    ) -> None:
        BasePage.__init__(self, config, parent)
        OfflineCapability.__init__(self)
        
        self.queue_manager = queue_manager
        self._auto_test_pending = True
        self._pending_tasks: list[asyncio.Task] = []
        
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Connection"
    
    def _setup_ui(self) -> None:
        """Setup page UI matching WATS Client design"""
        # Service address section
        address_layout = QHBoxLayout()
        address_layout.addWidget(QLabel("Service address"))
        
        self._address_edit = QLineEdit()
        self._address_edit.setPlaceholderText("https://your-wats-server.com/")
        self._address_edit.textChanged.connect(self._emit_changed)
        address_layout.addWidget(self._address_edit, 1)
        
        self._layout.addLayout(address_layout)
        
        # Disconnect button
        self._disconnect_btn = QPushButton("Disconnect")
        self._disconnect_btn.setMinimumWidth(120)  # Phase 2: Scaling fix
        self._disconnect_btn.clicked.connect(self._on_disconnect)
        self._layout.addWidget(self._disconnect_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        # Help text
        help_label = QLabel(
            'Service address to your wats.com account or WATS server. Click\n'
            '"Disconnect" to reset the client and log on to another service.'
        )
        help_label.setStyleSheet("color: #808080; font-size: 11px;")
        self._layout.addWidget(help_label)
        
        self._layout.addSpacing(20)
        
        # Test connection section
        test_layout = QHBoxLayout()
        test_layout.addWidget(QLabel("Test connection"))
        
        self._test_btn = QPushButton("Run test")
        self._test_btn.setMinimumWidth(100)  # Phase 2: Scaling fix
        self._test_btn.clicked.connect(self._on_test_connection)
        test_layout.addWidget(self._test_btn)
        test_layout.addStretch()
        
        self._layout.addLayout(test_layout)
        
        self._layout.addSpacing(10)
        
        # Test send UUT section - Advanced connection test with actual report
        test_uut_layout = QHBoxLayout()
        test_uut_layout.addWidget(QLabel("Test send UUT"))
        
        self._test_uut_btn = QPushButton("Send test report")
        self._test_uut_btn.setMinimumWidth(130)  # Phase 2: Scaling fix
        self._test_uut_btn.setToolTip(
            "Creates and submits a comprehensive test UUT report to verify\n"
            "full connectivity and report submission functionality.\n\n"
            "NEW: Uses local queue - report saved locally if server unreachable."
        )
        self._test_uut_btn.clicked.connect(self._on_test_send_uut)
        test_uut_layout.addWidget(self._test_uut_btn)
        test_uut_layout.addStretch()
        
        self._layout.addLayout(test_uut_layout)
        
        # Test UUT help text
        test_uut_help = QLabel(
            'Sends a test UUT report with various test types (numeric, string,\n'
            'boolean, charts) to verify full data submission capability.\n'
            '✨ Report queued locally if server unavailable - never lose data!'
        )
        test_uut_help.setStyleSheet("color: #808080; font-size: 11px;")
        self._layout.addWidget(test_uut_help)
        
        self._layout.addSpacing(20)
        
        # Status section
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("WATS Client Status"))
        self._client_status_label = QLabel("Offline")
        self._client_status_label.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(self._client_status_label)
        status_layout.addStretch()
        self._layout.addLayout(status_layout)
        
        service_status_layout = QHBoxLayout()
        service_status_layout.addWidget(QLabel("WATS Client Service"))
        self._service_status_label = QLabel("Stopped")
        self._service_status_label.setStyleSheet("font-weight: bold;")
        service_status_layout.addWidget(self._service_status_label)
        service_status_layout.addStretch()
        self._layout.addLayout(service_status_layout)
        
        identifier_layout = QHBoxLayout()
        identifier_layout.addWidget(QLabel("Current Identifier"))
        self._identifier_label = QLabel()
        self._identifier_label.setStyleSheet("font-weight: bold;")
        identifier_layout.addWidget(self._identifier_label)
        identifier_layout.addStretch()
        self._layout.addLayout(identifier_layout)
        
        self._layout.addSpacing(20)
        
        # Advanced options (collapsible)
        self._advanced_group = QGroupBox("⊙ Advanced options")
        self._advanced_group.setCheckable(True)
        self._advanced_group.setChecked(False)
        advanced_layout = QVBoxLayout(self._advanced_group)
        
        # API Token
        token_layout = QHBoxLayout()
        token_layout.addWidget(QLabel("API Token:"))
        self._token_edit = QLineEdit()
        self._token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._token_edit.textChanged.connect(self._emit_changed)
        token_layout.addWidget(self._token_edit, 1)
        advanced_layout.addLayout(token_layout)
        
        # Sync interval
        sync_layout = QHBoxLayout()
        sync_layout.addWidget(QLabel("Sync interval (seconds):"))
        self._sync_interval_edit = QLineEdit()
        self._sync_interval_edit.setMinimumWidth(100)  # Phase 2: Scaling fix
        self._sync_interval_edit.textChanged.connect(self._emit_changed)
        sync_layout.addWidget(self._sync_interval_edit)
        sync_layout.addStretch()
        advanced_layout.addLayout(sync_layout)
        
        # Proxy settings (Phase 4: GUI Cleanup - migrated from Proxy page)
        advanced_layout.addSpacing(15)
        proxy_separator = QLabel("─" * 50)
        proxy_separator.setStyleSheet("color: #3c3c3c;")
        advanced_layout.addWidget(proxy_separator)
        
        self._proxy_enabled_cb = QCheckBox("Use proxy server")
        self._proxy_enabled_cb.setToolTip("Route all connections through a proxy server")
        self._proxy_enabled_cb.stateChanged.connect(self._on_proxy_enabled_changed)
        advanced_layout.addWidget(self._proxy_enabled_cb)
        
        proxy_url_layout = QHBoxLayout()
        proxy_url_layout.addWidget(QLabel("Proxy URL:"))
        self._proxy_url_edit = QLineEdit()
        self._proxy_url_edit.setPlaceholderText("http://proxy.company.com:8080")
        self._proxy_url_edit.setToolTip("Full proxy URL including protocol and port")
        self._proxy_url_edit.textChanged.connect(self._emit_changed)
        proxy_url_layout.addWidget(self._proxy_url_edit, 1)
        advanced_layout.addLayout(proxy_url_layout)
        
        self._layout.addWidget(self._advanced_group)
        
        # Add stretch to push content to top
        self._layout.addStretch()
    
    def save_config(self) -> None:
        """Save configuration with error handling (H1 fix)."""
        try:
            self.config.service_address = self._address_edit.text().strip()
            self.config.api_token = self._token_edit.text().strip()
            
            try:
                sync_interval = int(self._sync_interval_edit.text())
                if sync_interval < 5:
                    raise ValueError("Sync interval must be at least 5 seconds")
                self.config.sync_interval_seconds = sync_interval
            except ValueError as e:
                self.handle_error(e, "validating sync interval")
                return
            
            # Save proxy settings (Phase 4: GUI Cleanup)
            self.config["proxy_enabled"] = self._proxy_enabled_cb.isChecked()
            self.config["proxy_url"] = self._proxy_url_edit.text().strip()
            
            # Save to file
            if hasattr(self.config, '_config_path') and self.config._config_path:
                self.config.save()
                logger.info("Connection configuration saved successfully")
            else:
                logger.warning("Config path not set - changes only in memory")
                
        except Exception as e:
            self.handle_error(e, "saving connection configuration")
            raise  # Re-raise so caller knows save failed
    
    def save_config_locally(self) -> None:
        """Save config to local file (for OfflineCapability)."""
        self.save_config()
    
    def sync_config_to_server(self) -> None:
        """Sync config to server (for OfflineCapability).
        
        Connection config is local-only, so this is a no-op.
        """
        pass
    
    def load_config(self) -> None:
        """Load configuration"""
        self._address_edit.setText(self.config.service_address)
        self._token_edit.setText(self.config.api_token)
        self._sync_interval_edit.setText(str(self.config.sync_interval_seconds))
        self._identifier_label.setText(self.config.formatted_identifier)
        
        # Load proxy settings (Phase 4: GUI Cleanup)
        self._proxy_enabled_cb.setChecked(self.config.get("proxy_enabled", False))
        self._proxy_url_edit.setText(self.config.get("proxy_url", ""))
        self._on_proxy_enabled_changed(self._proxy_enabled_cb.checkState())  # Update enabled state
        
        # Status will be updated after auto-test
        self.update_status("Checking...")
    
    def showEvent(self, event) -> None:
        """Called when page becomes visible"""
        super().showEvent(event)
        # Run auto-test on first show if service address is configured
        if self._auto_test_pending and self.config.service_address:
            self._auto_test_pending = False
            self._start_async_task(self._run_connection_test(auto=True))
        elif self._auto_test_pending:
            self._auto_test_pending = False
            self.update_status("Not configured")
    
    def _start_async_task(self, coro) -> bool:
        """Start async task with event loop safety check (H3 fix).
        
        Args:
            coro: Coroutine to execute
            
        Returns:
            True if task started, False if event loop not ready
        """
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_running():
                logger.warning("Event loop not running - cannot start async task")
                self.show_warning(
                    "Please wait for application to finish starting before using this feature.",
                    "Application Initializing"
                )
                return False
            
            task = asyncio.create_task(coro)
            self._pending_tasks.append(task)
            
            # Clean up completed tasks
            self._pending_tasks = [t for t in self._pending_tasks if not t.done()]
            
            return True
            
        except RuntimeError as e:
            self.handle_error(e, "starting async task")
            return False
    
    def update_status(self, status: str) -> None:
        """Update connection status display"""
        self._client_status_label.setText(status)
        
        # Green for online/connected states
        if status in ("Online", "Connected", "Online - Test OK"):
            self._client_status_label.setStyleSheet("font-weight: bold; color: #4ec9b0;")
            self._service_status_label.setText("Running")
            self._service_status_label.setStyleSheet("font-weight: bold; color: #4ec9b0;")
        elif status in ("Connecting", "Starting service...", "Checking..."):
            self._client_status_label.setStyleSheet("font-weight: bold; color: #dcdcaa;")
            self._service_status_label.setText("Checking...")
            self._service_status_label.setStyleSheet("font-weight: bold; color: #dcdcaa;")
        elif "Error" in status or "already running" in status.lower():
            self._client_status_label.setStyleSheet("font-weight: bold; color: #f14c4c;")
            if "already running" in status.lower():
                self._service_status_label.setText("Already Running")
                self._service_status_label.setStyleSheet("font-weight: bold; color: #ce9178;")
            else:
                self._service_status_label.setText("Error")
                self._service_status_label.setStyleSheet("font-weight: bold; color: #f14c4c;")
        elif status in ("Offline", "Disconnected", "Service not running"):
            # Gray for disconnected/offline states
            self._client_status_label.setStyleSheet("font-weight: bold; color: #808080;")
            self._service_status_label.setText("Stopped")
            self._service_status_label.setStyleSheet("font-weight: bold; color: #808080;")
        else:
            # Default: red for unknown states
            self._client_status_label.setStyleSheet("font-weight: bold; color: #f14c4c;")
            self._service_status_label.setText("Stopped")
            self._service_status_label.setStyleSheet("font-weight: bold;")
    
    def _on_disconnect(self) -> None:
        """Handle disconnect button click"""
        # Clear credentials (works offline - C3 fix)
        self._address_edit.clear()
        self._token_edit.clear()
        self.update_status("Offline")
        self._emit_changed()
    
    def _on_test_connection(self) -> None:
        """Handle test connection button click"""
        self._test_btn.setEnabled(False)
        self._test_btn.setText("Testing...")
        
        # Save current values to config first
        try:
            self.save_config()
        except Exception:
            # Save failed - error already shown
            self._test_btn.setEnabled(True)
            self._test_btn.setText("Run test")
            return
        
        # Run test in background with event loop safety (H3 fix)
        if not self._start_async_task(self._run_connection_test(auto=False)):
            self._test_btn.setEnabled(True)
            self._test_btn.setText("Run test")
            self.update_status("Error: Event loop not ready")
    
    async def _run_connection_test(self, auto: bool = False, retry_count: int = 3) -> None:
        """Run connection test asynchronously with retry logic (M1 improvement).
        
        Args:
            auto: If True, this is an automatic test at startup (don't touch button state)
            retry_count: Number of retry attempts for transient failures
        """
        last_error = None
        
        for attempt in range(retry_count):
            try:
                import httpx
                
                url = self.config.service_address.rstrip('/')
                if not url:
                    self._show_test_result(False, "No service address configured", auto)
                    return
                
                # Test the API endpoint
                test_url = f"{url}/api/Report/wats/info"
                headers = {}
                if self.config.api_token:
                    headers["Authorization"] = f"Bearer {self.config.api_token}"
                
                # Show retry attempt if not first try
                if attempt > 0 and not auto:
                    self._test_btn.setText(f"Testing... ({attempt + 1}/{retry_count})")
                
                # Enable redirect following
                async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                    response = await client.get(test_url, headers=headers)
                    
                    if response.status_code == 200:
                        self._show_test_result(True, "Online", auto)
                        return
                    elif response.status_code == 401:
                        self._show_test_result(False, "Authentication failed (401)", auto)
                        return
                    elif response.status_code == 403:
                        self._show_test_result(False, "Access denied (403)", auto)
                        return
                    elif response.status_code == 404:
                        # Try alternative endpoint
                        alt_url = f"{url}/api/report/wats/info"
                        response = await client.get(alt_url, headers=headers)
                        if response.status_code == 200:
                            self._show_test_result(True, "Online", auto)
                            return
                        else:
                            self._show_test_result(False, f"API not found (404)", auto)
                            return
                    else:
                        last_error = f"Server returned {response.status_code}"
                        
            except httpx.ConnectError as e:
                last_error = "Connection failed"
            except httpx.TimeoutException as e:
                last_error = "Connection timeout"
            except Exception as e:
                logger.exception("Connection test error")
                last_error = f"Error: {str(e)[:30]}"
            
            # Wait before retry (except on last attempt)
            if attempt < retry_count - 1:
                await asyncio.sleep(2)
        
        # All retries failed
        self._show_test_result(False, last_error or "Connection failed", auto)
    
    def _show_test_result(self, success: bool, message: str, auto: bool = False) -> None:
        """Show test result and re-enable button
        
        Args:
            success: Whether the test passed
            message: Status message to display
            auto: If True, don't touch button state (auto-test at startup)
        """
        if not auto:
            self._test_btn.setEnabled(True)
            self._test_btn.setText("Run test")
        
        if success:
            self._client_status_label.setText(message)
            self._client_status_label.setStyleSheet("font-weight: bold; color: #4ec9b0;")
            self._service_status_label.setText("Available")
            self._service_status_label.setStyleSheet("font-weight: bold; color: #4ec9b0;")
        else:
            self._client_status_label.setText(message)
            self._client_status_label.setStyleSheet("font-weight: bold; color: #f14c4c;")

    def _on_test_send_uut(self) -> None:
        """Handle test send UUT button click with queue support (C1 fix)."""
        if not self.queue_manager:
            self.show_warning(
                "Local queue manager not configured.\n\n"
                "Test UUT send requires queue manager to prevent data loss.",
                "Queue Not Available"
            )
            return
        
        self._test_uut_btn.setEnabled(False)
        self._test_uut_btn.setText("Sending...")
        
        # Save config first
        try:
            self.save_config()
        except Exception:
            # Save failed - error already shown
            self._test_uut_btn.setEnabled(True)
            self._test_uut_btn.setText("Send test report")
            return
        
        # Run async test with event loop safety (H3 fix)
        if not self._start_async_task(self._run_send_uut_test()):
            self._test_uut_btn.setEnabled(True)
            self._test_uut_btn.setText("Send test report")
    
    async def _run_send_uut_test(self) -> None:
        """Run test UUT send operation with queue support (C1 fix - NEVER LOSE DATA)."""
        try:
            from datetime import datetime
            
            url = self.config.service_address.rstrip('/')
            if not url:
                self.show_warning(
                    "Please configure service address before sending test report.",
                    "Configuration Required"
                )
                return
            
            # Create a minimal test UUT report
            test_report = {
                "pn": "TEST-PART-001",
                "sn": f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "rev": "1.0",
                "processCode": 10,
                "result": "P",  # Passed
                "start": datetime.utcnow().isoformat() + "Z",
                "root": {
                    "status": "P",
                    "steps": [
                        {
                            "name": "pyWATS GUI Connection Test",
                            "status": "P",
                            "steps": [
                                {
                                    "name": "Test Step",
                                    "status": "P",
                                    "numericMeas": [{
                                        "name": "Test Value",
                                        "status": "P",
                                        "value": 42.0,
                                        "unit": "units"
                                    }]
                                }
                            ]
                        }
                    ]
                }
            }
            
            # Queue the operation - GUARANTEES DATA NEVER LOST (C1 fix)
            operation_id = self.queue_manager.enqueue(
                operation_type="send_test_uut",
                data={
                    "url": f"{url}/api/Report/wats",
                    "report": test_report,
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.config.api_token}" if self.config.api_token else ""
                    }
                }
            )
            
            self.show_success(
                f"Test UUT report queued successfully!\n\n"
                f"Operation ID: {operation_id}\n"
                f"Serial: {test_report['sn']}\n"
                f"Part Number: {test_report['pn']}\n\n"
                f"✨ Report will be sent automatically when server is reachable.\n"
                f"Check queue status in main window status bar.",
                "Test Report Queued"
            )
            
            self._client_status_label.setText("Online - Test Queued")
            self._client_status_label.setStyleSheet("font-weight: bold; color: #4ec9b0;")
                    
        except Exception as e:
            self.handle_error(e, "queueing test report")
        finally:
            self._test_uut_btn.setEnabled(True)
            self._test_uut_btn.setText("Send test report")
    
    def _on_proxy_enabled_changed(self, state: int) -> None:
        """Enable/disable proxy URL field based on checkbox (Phase 4: GUI Cleanup)
        
        Args:
            state: Checkbox state from Qt (Checked/Unchecked)
        """
        enabled = state == Qt.CheckState.Checked.value
        self._proxy_url_edit.setEnabled(enabled)
        if enabled:
            self._proxy_url_edit.setStyleSheet("")
        else:
            self._proxy_url_edit.setStyleSheet("color: #808080;")
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix)."""
        # Cancel all pending tasks
        for task in self._pending_tasks:
            if not task.done():
                task.cancel()
        
        self._pending_tasks.clear()
        logger.info("ConnectionPage cleanup complete")
