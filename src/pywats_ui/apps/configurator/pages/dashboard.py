"""Service Dashboard Page - Migrated with reliability improvements.

Improvements:
- H4: cleanup() method to stop refresh timer
- Better error handling for status queries
- No automatic refresh (prevents event loop blocking)
- Manual refresh button added
- Subprocess-based service management (services survive GUI crashes)
"""

import logging
from pywats.core.logging import get_logger
from typing import Optional, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QCheckBox, QFormLayout
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig
from pywats_client.core import service_manager

logger = get_logger(__name__)


class StatusIndicator(QFrame):
    """Visual status indicator widget"""
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedSize(16, 16)
        self._status = "unknown"
        self._update_style()
    
    def set_status(self, status: str) -> None:
        """Set status: 'running', 'stopped', 'error', 'unknown'"""
        self._status = status
        self._update_style()
    
    def _update_style(self) -> None:
        colors = {
            "running": "#4ec9b0",  # Green
            "stopped": "#808080",  # Gray
            "error": "#f48771",    # Red
            "unknown": "#dcdcaa",  # Yellow
        }
        color = colors.get(self._status, "#808080")
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                border: 1px solid #3c3c3c;
            }}
        """)


class DashboardPage(BasePage):
    """Service Dashboard - Main monitoring page with converter health overview.
    
    Displays:
    - Service status and controls
    - Converter health overview
    - Quick statistics
    - Connection status
    """
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        self._refresh_timer: Optional[QTimer] = None
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Dashboard"
    
    def _setup_ui(self) -> None:
        """Setup dashboard UI"""
        
        # === Service Status Section ===
        service_group = QGroupBox("Service Status")
        service_layout = QVBoxLayout(service_group)
        
        # Status row
        status_row = QHBoxLayout()
        
        self._service_indicator = StatusIndicator()
        self._service_indicator.set_status("stopped")  # Initially stopped
        status_row.addWidget(self._service_indicator)
        
        self._service_status_label = QLabel("Stopped")
        self._service_status_label.setStyleSheet("color: #808080;")  # Gray for stopped
        status_font = QFont()
        status_font.setPointSize(12)
        status_font.setBold(True)
        self._service_status_label.setFont(status_font)
        status_row.addWidget(self._service_status_label)
        
        status_row.addStretch()
        
        # Refresh button (manual - no auto-refresh to prevent event loop blocking)
        self._refresh_btn = QPushButton("Refresh")
        self._refresh_btn.setToolTip("Manually refresh service status")
        self._refresh_btn.clicked.connect(self._refresh_status)
        status_row.addWidget(self._refresh_btn)
        
        service_layout.addLayout(status_row)
        
        # Service control buttons
        control_row = QHBoxLayout()
        control_row.addStretch()
        
        self._start_btn = QPushButton("Start Service")
        self._start_btn.setToolTip("Start the pyWATS client service")
        self._start_btn.clicked.connect(self._on_start_service)
        control_row.addWidget(self._start_btn)
        
        self._stop_btn = QPushButton("Stop Service")
        self._stop_btn.setToolTip("Stop the pyWATS client service")
        self._stop_btn.clicked.connect(self._on_stop_service)
        self._stop_btn.setEnabled(False)  # Disabled until service starts
        control_row.addWidget(self._stop_btn)
        
        service_layout.addLayout(control_row)
        
        # Service info
        info_layout = QHBoxLayout()
        
        self._uptime_label = QLabel("Uptime: --")
        self._uptime_label.setStyleSheet("color: #808080;")
        info_layout.addWidget(self._uptime_label)
        
        info_layout.addStretch()
        
        self._instance_label = QLabel(f"Instance: {self._config.instance_name}")
        self._instance_label.setStyleSheet("color: #808080;")
        info_layout.addWidget(self._instance_label)
        
        service_layout.addLayout(info_layout)
        
        self._layout.addWidget(service_group)
        
        # === Station Information Section === (Phase 3: GUI Cleanup)
        station_group = QGroupBox("Station Information")
        station_layout = QVBoxLayout(station_group)
        
        # Info display (read-only labels)
        from PySide6.QtWidgets import QFormLayout
        info_form = QFormLayout()
        info_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        
        self._client_name_label = QLabel("--")
        self._client_name_label.setStyleSheet("color: #dcdcaa; font-weight: bold;")
        info_form.addRow("Client Name:", self._client_name_label)
        
        self._station_name_label = QLabel("--")
        self._station_name_label.setStyleSheet("color: #dcdcaa; font-weight: bold;")
        info_form.addRow("Station Name:", self._station_name_label)
        
        self._station_location_label = QLabel("--")
        self._station_location_label.setStyleSheet("color: #dcdcaa;")
        info_form.addRow("Location:", self._station_location_label)
        
        self._station_purpose_label = QLabel("--")
        self._station_purpose_label.setStyleSheet("color: #dcdcaa;")
        info_form.addRow("Purpose:", self._station_purpose_label)
        
        station_layout.addLayout(info_form)
        
        # GPS toggle
        from PySide6.QtWidgets import QCheckBox
        self._gps_enabled_cb = QCheckBox("Allow GPS location services")
        self._gps_enabled_cb.setToolTip(
            "When enabled, the client includes geographical coordinates with test reports"
        )
        self._gps_enabled_cb.stateChanged.connect(self._on_gps_changed)
        station_layout.addWidget(self._gps_enabled_cb)
        
        # Edit button
        edit_layout = QHBoxLayout()
        self._edit_station_btn = QPushButton("Edit Station Settings")
        self._edit_station_btn.setMinimumWidth(150)
        self._edit_station_btn.setToolTip("Open Setup page to edit station information")
        self._edit_station_btn.clicked.connect(self._on_edit_station)
        edit_layout.addWidget(self._edit_station_btn)
        edit_layout.addStretch()
        station_layout.addLayout(edit_layout)
        
        self._layout.addWidget(station_group)
        
        # === Statistics Row ===
        stats_layout = QHBoxLayout()
        
        # Converters card
        converters_card = self._create_stat_card("Converters", "0 Active", "#4ec9b0")
        self._converters_value = converters_card.findChild(QLabel, "value")
        stats_layout.addWidget(converters_card)
        
        # Queue card
        queue_card = self._create_stat_card("Queue", "0 Pending", "#dcdcaa")
        self._queue_value = queue_card.findChild(QLabel, "value")
        stats_layout.addWidget(queue_card)
        
        # Reports card
        reports_card = self._create_stat_card("Reports", "0 Today", "#569cd6")
        self._reports_value = reports_card.findChild(QLabel, "value")
        stats_layout.addWidget(reports_card)
        
        # Success rate card
        success_card = self._create_stat_card("Success Rate", "--%", "#4ec9b0")
        self._success_value = success_card.findChild(QLabel, "value")
        stats_layout.addWidget(success_card)
        
        self._layout.addLayout(stats_layout)
        
        # === Converter Health Table ===
        health_group = QGroupBox("Converter Health")
        health_layout = QVBoxLayout(health_group)
        
        self._health_table = QTableWidget()
        self._health_table.setColumnCount(6)
        self._health_table.setHorizontalHeaderLabels([
            "Status", "Converter", "Watch Folder", "Processed", "Success", "Last Run"
        ])
        
        header = self._health_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self._health_table.setColumnWidth(1, 200)
        self._health_table.verticalHeader().setVisible(False)
        self._health_table.setAlternatingRowColors(True)
        self._health_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._health_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        health_layout.addWidget(self._health_table)
        
        self._layout.addWidget(health_group, 1)
        
        # === Connection Status ===
        conn_group = QGroupBox("Server Connection")
        conn_layout = QHBoxLayout(conn_group)
        
        self._conn_indicator = StatusIndicator()
        conn_layout.addWidget(self._conn_indicator)
        
        self._conn_label = QLabel("Not connected")
        conn_layout.addWidget(self._conn_label)
        
        conn_layout.addStretch()
        
        self._sync_label = QLabel("Last sync: Never")
        self._sync_label.setStyleSheet("color: #808080;")
        conn_layout.addWidget(self._sync_label)
        
        self._layout.addWidget(conn_group)
    
    def _create_stat_card(self, title: str, value: str, color: str) -> QGroupBox:
        """Create a statistics card widget"""
        card = QGroupBox()
        card.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                margin-top: 0px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #808080; font-size: 11px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_font = QFont()
        value_font.setPointSize(16)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        return card
    
    def _refresh_status(self) -> None:
        """Refresh all status indicators with error handling."""
        try:
            # Update converter health from config
            self._update_converter_health()
            
            # Update connection status from config
            self._update_connection_status()
            
            # Update service status from lock file (subprocess mode)
            instance_id = self._config.get("instance_id", "default")
            service_status = service_manager.get_service_status(instance_id)
            
            if service_status.is_running:
                self._update_service_status("running", "Running")
                self._start_btn.setEnabled(False)
                self._stop_btn.setEnabled(True)
                
                # Update uptime
                if service_status.started_at:
                    uptime = service_manager.get_uptime(service_status.started_at)
                    self._uptime_label.setText(f"Uptime: {uptime} (PID: {service_status.pid})")
                else:
                    self._uptime_label.setText(f"Uptime: Unknown (PID: {service_status.pid})")
            else:
                self._update_service_status("stopped", "Stopped")
                self._start_btn.setEnabled(True)
                self._stop_btn.setEnabled(False)
                self._uptime_label.setText("Uptime: --")
            
            logger.debug("Dashboard status refreshed")
            
        except Exception as e:
            self.handle_error(e, "refreshing dashboard status")
    
    def _update_converter_health(self) -> None:
        """Update converter health table from local config."""
        try:
            self._health_table.setRowCount(0)
            
            active_count = 0
            converters = self._config.get("converters", [])
            
            for conv in converters:
                if not conv.get("enabled", False):
                    continue
                
                active_count += 1
                row = self._health_table.rowCount()
                self._health_table.insertRow(row)
                
                # Status indicator
                status_item = QTableWidgetItem("●")
                status_item.setForeground(QColor("#dcdcaa"))  # Yellow - unknown
                self._health_table.setItem(row, 0, status_item)
                
                # Name
                name_item = QTableWidgetItem(conv.get("name", "Unknown"))
                self._health_table.setItem(row, 1, name_item)
                
                # Watch folder
                watch_item = QTableWidgetItem(conv.get("watch_folder", "--"))
                watch_item.setForeground(QColor("#808080"))
                self._health_table.setItem(row, 2, watch_item)
                
                # No live stats available without service integration
                processed_item = QTableWidgetItem("--")
                self._health_table.setItem(row, 3, processed_item)
                
                success_item = QTableWidgetItem("--%")
                self._health_table.setItem(row, 4, success_item)
                
                last_run_item = QTableWidgetItem("--")
                last_run_item.setForeground(QColor("#808080"))
                self._health_table.setItem(row, 5, last_run_item)
            
            # Update stat cards
            self._converters_value.setText(f"{active_count} Configured")
            self._queue_value.setText("-- Pending")
            self._reports_value.setText("-- Today")
            self._success_value.setText("--%")
            
        except Exception as e:
            logger.exception(f"Failed to update converter health: {e}")
            self._converters_value.setText("Error")
    
    def _update_connection_status(self) -> None:
        """Update server connection status from config."""
        try:
            service_address = self._config.get("service_address", "")
            if service_address:
                self._conn_indicator.set_status("unknown")
                self._conn_label.setText(f"Configured: {service_address}")
                self._sync_label.setText("Last sync: Unknown")
            else:
                self._conn_indicator.set_status("stopped")
                self._conn_label.setText("Not configured")
                self._sync_label.setText("No service configured")
                
        except Exception as e:
            logger.exception(f"Failed to update connection status: {e}")
            self._conn_indicator.set_status("error")
            self._conn_label.setText("Error reading status")
    
    def save_config(self) -> None:
        """Save GPS setting (Phase 3: GUI Cleanup)"""
        try:
            # Save GPS setting to config
            self._config["location_services_enabled"] = self._gps_enabled_cb.isChecked()
            self._config.save()
            logger.debug("GPS setting saved from Dashboard")
        except Exception as e:
            self.handle_error(e, "saving GPS setting")
    
    def load_config(self) -> None:
        """Load initial dashboard state and station information (Phase 3: GUI Cleanup)"""
        try:
            # Refresh service/converter status
            self._refresh_status()
            
            # Load station information
            self._client_name_label.setText(
                self._config.get("client_name", "Not configured")
            )
            self._station_name_label.setText(
                self._config.get("station_name", "Not configured")
            )
            self._station_location_label.setText(
                self._config.get("location", "Not configured")
            )
            self._station_purpose_label.setText(
                self._config.get("purpose", "Not configured")
            )
            self._gps_enabled_cb.setChecked(
                self._config.get("location_services_enabled", False)
            )
            
            logger.debug("Dashboard configuration loaded")
            
        except Exception as e:
            self.handle_error(e, "loading dashboard configuration")
    
    def _on_gps_changed(self, state: int) -> None:
        """Handle GPS checkbox change (Phase 3: GUI Cleanup)"""
        try:
            enabled = state == Qt.CheckState.Checked.value
            self._config["location_services_enabled"] = enabled
            self._config.save()
            logger.info(f"GPS location services: {enabled}")
        except Exception as e:
            self.handle_error(e, "saving GPS setting")
    
    def _on_edit_station(self) -> None:
        """Navigate to Setup page for editing station info (Phase 3: GUI Cleanup)"""
        # Try to navigate via main window
        main_window = self.window()
        if hasattr(main_window, 'navigate_to_page'):
            main_window.navigate_to_page("Setup")
            logger.debug("Navigated to Setup page from Dashboard")
        else:
            # Fallback: Show info message
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Edit Station Settings",
                "Navigate to the 'Setup' page to edit station information."
            )
    
    def _on_start_service(self) -> None:
        """Start the client service as independent process (decoupled from GUI)"""
        try:
            instance_id = self._config.get("instance_id", "default")
            logger.info(f"Starting service '{instance_id}' as subprocess...")
            
            # Launch service as independent process (survives GUI crashes)
            if service_manager.start_service(instance_id, wait=False):
                logger.info(f"Service '{instance_id}' started successfully")
                self._update_service_status("running", "Running")
                self._start_btn.setEnabled(False)
                self._stop_btn.setEnabled(True)
                # Refresh to get PID and uptime
                self._refresh_status()
            else:
                logger.error(f"Failed to start service '{instance_id}'")
                self._update_service_status("error", "Failed to start")
            
        except Exception as e:
            self.handle_error(e, "starting service")
            self._update_service_status("error", f"Failed to start: {str(e)}")
    
    def _on_stop_service(self) -> None:
        """Stop the client service (independent process)"""
        try:
            instance_id = self._config.get("instance_id", "default")
            logger.info(f"Stopping service '{instance_id}'...")
            
            # Stop service process (graceful SIGTERM/taskkill)
            if service_manager.stop_service(instance_id, force=False):
                logger.info(f"Service '{instance_id}' stopped successfully")
                self._update_service_status("stopped", "Stopped")
                self._start_btn.setEnabled(True)
                self._stop_btn.setEnabled(False)
                # Refresh to clear PID and uptime
                self._refresh_status()
            else:
                logger.warning(f"Service '{instance_id}' was not running")
                # Update UI anyway (in case of stale state)
                self._update_service_status("stopped", "Stopped")
                self._start_btn.setEnabled(True)
                self._stop_btn.setEnabled(False)
            
        except Exception as e:
            self.handle_error(e, "stopping service")
    
    def _update_service_status(self, status: str, text: str) -> None:
        """Update service status indicator and label"""
        self._service_indicator.set_status(status)
        self._service_status_label.setText(text)
        
        # Update label color based on status
        colors = {
            "running": "color: #4ec9b0;",  # Green
            "stopped": "color: #808080;",  # Gray
            "error": "color: #f48771;",    # Red
            "unknown": "color: #dcdcaa;",  # Yellow
        }
        self._service_status_label.setStyleSheet(colors.get(status, ""))
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix)."""
        # NOTE: Do NOT stop service on cleanup - service should survive GUI exit
        # Users can manually stop service via Stop button if needed
        
        if self._refresh_timer:
            self._refresh_timer.stop()
            self._refresh_timer = None
        logger.debug("Dashboard cleanup complete (service left running)")
