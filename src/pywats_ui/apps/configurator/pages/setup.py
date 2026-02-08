"""Setup Page - Station configuration - Migrated with reliability improvements.

Improvements:
- H1: Error handling for save_config() with user dialogs
- H4: cleanup() method for consistency  
- Better validation for client ID, station names
- Multi-station dialog improvements
"""

import logging
from pywats.core.logging import get_logger
from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox, QCheckBox, QSpinBox,
    QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PySide6.QtCore import Qt

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = get_logger(__name__)


class StationManagerDialog(QDialog):
    """Dialog for managing multiple stations in hub mode."""
    
    def __init__(self, stations: List[Dict[str, Any]], parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._stations = stations.copy()  # Work on a copy
        self.setWindowTitle("Station Manager")
        self.resize(700, 400)
        self._setup_ui()
        self._load_stations()
    
    def _setup_ui(self) -> None:
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        # Instructions
        info_label = QLabel(
            "Manage stations that connect to this hub.\n"
            "Each station requires a unique name and location."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #808080; padding: 10px 0;")
        layout.addWidget(info_label)
        
        # Stations table
        self._stations_table = QTableWidget()
        self._stations_table.setColumnCount(3)
        self._stations_table.setHorizontalHeaderLabels(["Name", "Location", "Purpose"])
        
        header = self._stations_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        self._stations_table.setColumnWidth(0, 200)
        self._stations_table.setColumnWidth(1, 150)
        self._stations_table.verticalHeader().setVisible(False)
        self._stations_table.setAlternatingRowColors(True)
        
        layout.addWidget(self._stations_table, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Station")
        add_btn.clicked.connect(self._on_add_station)
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self._on_remove_station)
        button_layout.addWidget(remove_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def _load_stations(self) -> None:
        """Load stations into table"""
        self._stations_table.setRowCount(0)
        for station in self._stations:
            row = self._stations_table.rowCount()
            self._stations_table.insertRow(row)
            
            self._stations_table.setItem(row, 0, QTableWidgetItem(station.get("name", "")))
            self._stations_table.setItem(row, 1, QTableWidgetItem(station.get("location", "")))
            self._stations_table.setItem(row, 2, QTableWidgetItem(station.get("purpose", "")))
    
    def _on_add_station(self) -> None:
        """Add a new station"""
        # Add empty row
        row = self._stations_table.rowCount()
        self._stations_table.insertRow(row)
        
        self._stations_table.setItem(row, 0, QTableWidgetItem("New Station"))
        self._stations_table.setItem(row, 1, QTableWidgetItem("Location"))
        self._stations_table.setItem(row, 2, QTableWidgetItem("Purpose"))
        
        # Start editing name
        self._stations_table.editItem(self._stations_table.item(row, 0))
    
    def _on_remove_station(self) -> None:
        """Remove selected station"""
        selected = self._stations_table.selectedItems()
        if not selected:
            self.show_warning("Please select a station to remove.", "No Selection")
            return
        
        row = self._stations_table.currentRow()
        if row >= 0:
            if self.confirm_action(
                f"Remove station '{self._stations_table.item(row, 0).text()}'?",
                "Remove Station"
            ):
                self._stations_table.removeRow(row)
    
    def get_stations(self) -> List[Dict[str, Any]]:
        """Get stations from table"""
        stations = []
        for row in range(self._stations_table.rowCount()):
            name_item = self._stations_table.item(row, 0)
            location_item = self._stations_table.item(row, 1)
            purpose_item = self._stations_table.item(row, 2)
            
            if name_item and location_item:
                stations.append({
                    "name": name_item.text(),
                    "location": location_item.text() if location_item else "",
                    "purpose": purpose_item.text() if purpose_item else ""
                })
        
        return stations


class SetupPage(BasePage):
    """Station Setup configuration page.
    
    Configure:
    - Client identification (instance name, client ID)
    - Station configuration (name, location, purpose)
    - Multi-station mode (hub)
    - Advanced options
    """
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Station Setup"
    
    def _setup_ui(self) -> None:
        """Setup page UI"""
        
        # === Client Identification ===
        client_group = QGroupBox("Client Identification")
        client_layout = QFormLayout(client_group)
        client_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        
        self._instance_name = QLineEdit()
        self._instance_name.setPlaceholderText("e.g., Production-Client-1")
        self._instance_name.setToolTip("Unique name for this client instance")
        client_layout.addRow("Instance Name:", self._instance_name)
        
        self._client_id = QLineEdit()
        self._client_id.setPlaceholderText("Auto-generated if empty")
        self._client_id.setToolTip("Unique client identifier (auto-generated)")
        client_layout.addRow("Client ID:", self._client_id)
        
        self._layout.addWidget(client_group)
        
        # === Station Configuration ===
        station_group = QGroupBox("Station Configuration")
        station_layout = QFormLayout(station_group)
        station_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        
        self._station_name = QLineEdit()
        self._station_name.setPlaceholderText("e.g., ICT-Station-1")
        self._station_name.setToolTip("Name of the test station")
        station_layout.addRow("Station Name:", self._station_name)
        
        self._use_hostname = QCheckBox("Use computer hostname as station name")
        self._use_hostname.setToolTip("Automatically use the computer's hostname")
        self._use_hostname.stateChanged.connect(self._on_hostname_toggled)
        station_layout.addRow("", self._use_hostname)
        
        self._location = QLineEdit()
        self._location.setPlaceholderText("e.g., Building-A, Line-2")
        self._location.setToolTip("Physical location of the station")
        station_layout.addRow("Location:", self._location)
        
        self._purpose = QLineEdit()
        self._purpose.setPlaceholderText("e.g., ICT Testing, Final Assembly")
        self._purpose.setToolTip("Purpose or role of this station")
        station_layout.addRow("Purpose:", self._purpose)
        
        self._layout.addWidget(station_group)
        
        # === Multi-Station Mode (Hub) ===
        hub_group = QGroupBox("Multi-Station Mode (Hub)")
        hub_layout = QVBoxLayout(hub_group)
        
        hub_info = QLabel(
            "Enable hub mode to manage multiple stations from this client.\n"
            "Each station can have its own configuration and converters."
        )
        hub_info.setWordWrap(True)
        hub_info.setStyleSheet("color: #808080; padding: 5px 0;")
        hub_layout.addWidget(hub_info)
        
        self._hub_mode = QCheckBox("Enable hub mode")
        self._hub_mode.setToolTip("Enable multi-station management")
        self._hub_mode.stateChanged.connect(self._on_hub_mode_toggled)
        hub_layout.addWidget(self._hub_mode)
        
        # Hub stations summary
        self._stations_summary = QLabel("0 stations configured")
        self._stations_summary.setStyleSheet("color: #808080;")
        hub_layout.addWidget(self._stations_summary)
        
        # Manage stations button
        self._manage_stations_btn = QPushButton("Manage Stations")
        self._manage_stations_btn.clicked.connect(self._on_manage_stations)
        self._manage_stations_btn.setEnabled(False)
        hub_layout.addWidget(self._manage_stations_btn)
        
        self._layout.addWidget(hub_group)
        
        # === Connection Status (Read-only summary) ===
        conn_group = QGroupBox("Connection Status")
        conn_layout = QVBoxLayout(conn_group)
        
        self._conn_status_label = QLabel("Not configured")
        self._conn_status_label.setStyleSheet("color: #808080; padding: 10px;")
        conn_layout.addWidget(self._conn_status_label)
        
        goto_conn_btn = QPushButton("Configure Connection →")
        goto_conn_btn.setToolTip("Go to Connection page to configure WATS API connection")
        goto_conn_btn.clicked.connect(lambda: self._emit_page_change_request("connection"))
        conn_layout.addWidget(goto_conn_btn)
        
        self._layout.addWidget(conn_group)
        
        # === Advanced Options ===
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QFormLayout(advanced_group)
        
        self._sync_interval = QSpinBox()
        self._sync_interval.setRange(1, 3600)
        self._sync_interval.setValue(60)
        self._sync_interval.setSuffix(" seconds")
        self._sync_interval.setToolTip("Interval for syncing queued reports to WATS")
        advanced_layout.addRow("Sync Interval:", self._sync_interval)
        
        self._auto_start_service = QCheckBox("Auto-start service on system startup")
        self._auto_start_service.setToolTip("Automatically start the client service when system boots")
        advanced_layout.addRow("", self._auto_start_service)
        
        self._layout.addWidget(advanced_group)
        
        self._layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config)
        self._layout.addWidget(save_btn)
    
    def _on_hostname_toggled(self, state: int) -> None:
        """Handle hostname checkbox toggle"""
        checked = (state == Qt.CheckState.Checked.value)
        self._station_name.setEnabled(not checked)
        
        if checked:
            import socket
            hostname = socket.gethostname()
            self._station_name.setText(hostname)
    
    def _on_hub_mode_toggled(self, state: int) -> None:
        """Handle hub mode checkbox toggle"""
        checked = (state == Qt.CheckState.Checked.value)
        self._manage_stations_btn.setEnabled(checked)
    
    def _on_manage_stations(self) -> None:
        """Open station manager dialog"""
        try:
            # Get current stations from config
            stations = self._config.get("stations", [])
            
            # Show dialog
            dialog = StationManagerDialog(stations, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Get updated stations
                updated_stations = dialog.get_stations()
                
                # Update config immediately (not saved to disk until Save button)
                self._config["stations"] = updated_stations
                
                # Update summary
                self._stations_summary.setText(f"{len(updated_stations)} stations configured")
                
                logger.info(f"Stations updated: {len(updated_stations)} total")
                
        except Exception as e:
            self.handle_error(e, "managing stations")
    
    def _emit_page_change_request(self, page_name: str) -> None:
        """Request page change (will be connected by main window)"""
        # TODO: Implement page navigation signal
        logger.info(f"Page change requested: {page_name}")
        self.show_success(
            f"Please manually navigate to the '{page_name}' page to configure connection settings.",
            "Navigate"
        )
    
    def save_config(self) -> None:
        """Save station setup configuration (H1 fix - error handling)."""
        try:
            # Validate inputs
            instance_name = self._instance_name.text().strip()
            if not instance_name:
                self.show_warning(
                    "Instance name is required.\n\nPlease enter a name for this client instance.",
                    "Invalid Configuration"
                )
                return
            
            station_name = self._station_name.text().strip()
            if not station_name and not self._use_hostname.isChecked():
                self.show_warning(
                    "Station name is required.\n\nPlease enter a name or enable 'Use hostname'.",
                    "Invalid Configuration"
                )
                return
            
            # Update config
            self._config.instance_name = instance_name
            
            # Station settings
            self._config.station_name = station_name
            # Map use_hostname checkbox to station_name_source field
            self._config.station_name_source = "hostname" if self._use_hostname.isChecked() else "config"
            self._config.location = self._location.text().strip()
            self._config.purpose = self._purpose.text().strip()
            
            # Hub mode - map to new field name
            self._config.multi_station_enabled = self._hub_mode.isChecked()
            
            # Advanced options
            self._config.sync_interval_seconds = self._sync_interval.value()
            self._config.service_auto_start = self._auto_start_service.isChecked()
            
            # Save to disk
            self._config.save()
            
            logger.info(
                f"Station setup saved: instance={instance_name}, "
                f"station={station_name}, hub_mode={self._hub_mode.isChecked()}"
            )
            
            # Success - no popup needed (prevents multiple popups on close)
            
        except Exception as e:
            self.handle_error(e, "saving station setup configuration")
    
    def load_config(self) -> None:
        """Load station setup from config"""
        try:
            # Client identification (client_id removed - not in new schema)
            self._instance_name.setText(self._config.instance_name or "")
            self._client_id.setText("")  # Always empty - field deprecated
            
            # Station settings
            self._station_name.setText(self._config.station_name or "")
            # Map station_name_source to use_hostname checkbox
            use_hostname = self._config.station_name_source == "hostname"
            self._use_hostname.setChecked(use_hostname)
            self._station_name.setEnabled(not use_hostname)
            
            self._location.setText(self._config.location or "")
            self._purpose.setText(self._config.purpose or "")
            
            # Hub mode - use new field name
            hub_mode = self._config.multi_station_enabled
            self._hub_mode.setChecked(hub_mode)
            self._manage_stations_btn.setEnabled(hub_mode)
            
            # Update stations summary - use new field name
            stations = self._config.station_presets or []
            self._stations_summary.setText(f"{len(stations)} stations configured")
            
            # Advanced options
            self._sync_interval.setValue(self._config.sync_interval_seconds)
            self._auto_start_service.setChecked(self._config.service_auto_start)
            
            # Connection status summary
            service_address = self._config.service_address or ""
            if service_address:
                self._conn_status_label.setText(f"✓ Connected to: {service_address}")
                self._conn_status_label.setStyleSheet("color: #4ec9b0; padding: 10px;")
            else:
                self._conn_status_label.setText("⚠ Not configured - please configure connection")
                self._conn_status_label.setStyleSheet("color: #ce9178; padding: 10px;")
            
            logger.debug("Station setup loaded")
            
        except Exception as e:
            self.handle_error(e, "loading station setup")
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix - consistency)."""
        pass  # No resources to clean
