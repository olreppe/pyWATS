"""Serial Number Handler Configuration Page - Migrated with reliability improvements.

Improvements:
- H1: Error handling for save_config() with user dialogs
- H4: cleanup() method for consistency
- Better input validation
"""

import logging
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QComboBox,
    QCheckBox, QSpinBox, QPushButton, QMessageBox, QLabel, QGroupBox
)
from PySide6.QtCore import Qt

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = logging.getLogger(__name__)


class SerialNumberHandlerPage(BasePage):
    """Serial number handler configuration page.
    
    Configures how serial numbers are requested, cached, and reserved for testing.
    """
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Serial Number Handler"
    
    def _setup_ui(self) -> None:
        """Setup page UI"""
        # Description
        desc_label = QLabel(
            "Configure how serial numbers are requested from WATS and reserved for testing.\n"
            "When offline, serial numbers can be reserved locally and synced when reconnected."
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #b0b0b0; padding: 10px 0;")
        self._layout.addWidget(desc_label)
        
        # Handler settings group
        handler_group = QGroupBox("Handler Configuration")
        handler_layout = QFormLayout()
        
        # Serial number type selector
        self._type_combo = QComboBox()
        self._type_combo.addItems([
            "WATS Sequential",
            "Station Generated",
            "External System",
            "Manual Entry"
        ])
        handler_layout.addRow("Serial Number Type:", self._type_combo)
        
        # Reuse serial numbers
        self._reuse_cb = QCheckBox("Allow serial number reuse")
        self._reuse_cb.setToolTip(
            "If enabled, serial numbers can be reused for different test runs.\n"
            "Typically disabled for production testing."
        )
        handler_layout.addRow("Reuse:", self._reuse_cb)
        
        handler_group.setLayout(handler_layout)
        self._layout.addWidget(handler_group)
        
        # Caching settings group
        cache_group = QGroupBox("Caching & Offline Behavior")
        cache_layout = QFormLayout()
        
        # Reserve offline
        self._reserve_offline_cb = QCheckBox("Reserve serial numbers when offline")
        self._reserve_offline_cb.setToolTip(
            "When enabled, serial numbers can be reserved locally when the WATS API is unreachable.\n"
            "Reserved numbers will be synced to WATS when connection is restored."
        )
        cache_layout.addRow("Offline Reservations:", self._reserve_offline_cb)
        
        # Batch size
        self._batch_size_spin = QSpinBox()
        self._batch_size_spin.setRange(1, 1000)
        self._batch_size_spin.setValue(10)
        self._batch_size_spin.setToolTip(
            "Number of serial numbers to fetch from WATS in a single batch.\n"
            "Larger batches reduce API calls but may reserve more than needed."
        )
        cache_layout.addRow("Batch Size:", self._batch_size_spin)
        
        # Fetch threshold
        self._fetch_threshold_spin = QSpinBox()
        self._fetch_threshold_spin.setRange(1, 100)
        self._fetch_threshold_spin.setValue(5)
        self._fetch_threshold_spin.setToolTip(
            "Trigger a new batch fetch when available serial numbers drop below this threshold.\n"
            "Should be less than batch size to maintain buffer."
        )
        cache_layout.addRow("Fetch Threshold:", self._fetch_threshold_spin)
        
        cache_group.setLayout(cache_layout)
        self._layout.addWidget(cache_group)
        
        # Advanced settings group
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QFormLayout()
        
        # In-sequence ordering
        self._in_sequence_cb = QCheckBox("Enforce sequential order")
        self._in_sequence_cb.setToolTip(
            "Require serial numbers to be used in the order they were fetched.\n"
            "Ensures sequential numbering for production traceability."
        )
        advanced_layout.addRow("Sequential Order:", self._in_sequence_cb)
        
        # Start-from serial number
        self._start_from_label = QLabel("(None)")
        self._start_from_label.setStyleSheet("color: #808080;")
        advanced_layout.addRow("Current Start:", self._start_from_label)
        
        advanced_group.setLayout(advanced_layout)
        self._layout.addWidget(advanced_group)
        
        # Status display
        self._status_label = QLabel()
        self._status_label.setStyleSheet("color: #808080; font-style: italic; padding: 10px 0;")
        self._layout.addWidget(self._status_label)
        
        self._layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config)
        self._layout.addWidget(save_btn)
        
        # Update status display
        self._update_status()
    
    def _update_status(self) -> None:
        """Update status label with current cache info"""
        sn_type = self._type_combo.currentText()
        batch = self._batch_size_spin.value()
        threshold = self._fetch_threshold_spin.value()
        
        if batch <= threshold:
            self._status_label.setText(
                "⚠️ Warning: Fetch threshold should be less than batch size to maintain buffer."
            )
            self._status_label.setStyleSheet("color: #ce9178; font-style: italic;")
        else:
            self._status_label.setText(
                f"Using {sn_type} handler with batch size {batch} (refetch at {threshold} remaining)"
            )
            self._status_label.setStyleSheet("color: #808080; font-style: italic;")
    
    def save_config(self) -> None:
        """Save serial number handler configuration (H1 fix - error handling)."""
        try:
            # Validate inputs
            if self._batch_size_spin.value() <= self._fetch_threshold_spin.value():
                QMessageBox.warning(
                    self,
                    "Invalid Configuration",
                    "Batch size must be greater than fetch threshold to maintain a serial number buffer.\n\n"
                    "Please adjust the values before saving."
                )
                return
            
            # Update config
            sn_config = self._config.get("serial_number_handler", {})
            sn_config["type"] = self._type_combo.currentText()
            sn_config["allow_reuse"] = self._reuse_cb.isChecked()
            sn_config["reserve_offline"] = self._reserve_offline_cb.isChecked()
            sn_config["batch_size"] = self._batch_size_spin.value()
            sn_config["fetch_threshold"] = self._fetch_threshold_spin.value()
            sn_config["enforce_sequential"] = self._in_sequence_cb.isChecked()
            
            self._config["serial_number_handler"] = sn_config
            
            # Save to disk
            self._config.save()
            
            logger.info(
                f"Serial number handler config saved: type={sn_config['type']}, "
                f"batch={sn_config['batch_size']}, threshold={sn_config['fetch_threshold']}"
            )
            
            QMessageBox.information(
                self,
                "Configuration Saved",
                "Serial number handler configuration has been saved successfully."
            )
            
            self._update_status()
            
        except Exception as e:
            logger.exception(f"Failed to save serial number handler config: {e}")
            QMessageBox.critical(
                self,
                "Save Failed",
                f"Failed to save serial number handler configuration.\n\n"
                f"Error: {e}\n\n"
                "Please check the logs for details and try again."
            )
    
    def load_config(self) -> None:
        """Load serial number handler configuration from config"""
        try:
            sn_config = self._config.get("serial_number_handler", {})
            
            # Load type
            sn_type = sn_config.get("type", "WATS Sequential")
            index = self._type_combo.findText(sn_type)
            if index >= 0:
                self._type_combo.setCurrentIndex(index)
            
            # Load checkboxes
            self._reuse_cb.setChecked(sn_config.get("allow_reuse", False))
            self._reserve_offline_cb.setChecked(sn_config.get("reserve_offline", True))
            self._in_sequence_cb.setChecked(sn_config.get("enforce_sequential", True))
            
            # Load numeric values
            self._batch_size_spin.setValue(sn_config.get("batch_size", 10))
            self._fetch_threshold_spin.setValue(sn_config.get("fetch_threshold", 5))
            
            # Update start-from display
            start_from = sn_config.get("start_from_serial")
            if start_from:
                self._start_from_label.setText(str(start_from))
            else:
                self._start_from_label.setText("(None)")
            
            self._update_status()
            
            logger.debug("Serial number handler config loaded")
            
        except Exception as e:
            logger.exception(f"Failed to load serial number handler config: {e}")
            QMessageBox.warning(
                self,
                "Load Failed",
                f"Failed to load serial number handler configuration.\n\n"
                f"Error: {e}\n\n"
                "Using default values."
            )
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix - consistency)."""
        pass  # No resources to clean
