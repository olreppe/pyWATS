"""Service Dashboard Page - Migrated with reliability improvements.

Improvements:
- H4: cleanup() method to stop refresh timer
- Better error handling for status queries
- No automatic refresh (prevents event loop blocking)
- Manual refresh button added
"""

import logging
from typing import Optional, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = logging.getLogger(__name__)


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
        status_row.addWidget(self._service_indicator)
        
        self._service_status_label = QLabel("Checking...")
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
            
            # Update service status (standalone mode)
            self._service_indicator.set_status("unknown")
            self._service_status_label.setText("Standalone Mode")
            self._service_status_label.setStyleSheet("color: #dcdcaa;")
            self._uptime_label.setText("Service mode not active")
            
            logger.info("Dashboard status refreshed")
            
        except Exception as e:
            logger.exception(f"Failed to refresh dashboard status: {e}")
            QMessageBox.warning(
                self,
                "Refresh Failed",
                f"Failed to refresh dashboard status.\n\nError: {e}\n\n"
                "Check logs for details."
            )
    
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
        """No config to save on dashboard (read-only display)"""
        pass
    
    def load_config(self) -> None:
        """Load initial dashboard state"""
        self._refresh_status()
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix)."""
        if self._refresh_timer:
            self._refresh_timer.stop()
            self._refresh_timer = None
        logger.debug("Dashboard cleanup complete")
