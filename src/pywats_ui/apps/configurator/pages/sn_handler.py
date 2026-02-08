"""Serial Number Handler Configuration Page - Migrated with reliability improvements.

Improvements:
- H1: Error handling for save_config() with user dialogs
- H4: cleanup() method for consistency
- Better input validation
"""

import logging
from pywats.core.logging import get_logger
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QComboBox,
    QCheckBox, QSpinBox, QPushButton, QLabel, QGroupBox
)
from PySide6.QtCore import Qt

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = get_logger(__name__)


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
            # No batch size validation - removed in new schema (async handles batching)
            
            # Update config - map to flat fields (no nested dict)
            # Map old type selector to new sn_mode field
            type_mapping = {
                "WATS Sequential": "Auto-increment",
                "Station Generated": "Auto-increment",
                "External System": "External Source",
                "Manual Entry": "Manual Entry"
            }
            current_type = self._type_combo.currentText()
            self._config.sn_mode = type_mapping.get(current_type, "Manual Entry")
            
            # Map reuse checkbox to duplicate checking (opposite logic)
            self._config.sn_check_duplicates = not self._reuse_cb.isChecked()
            
            # Offline reservations handled by offline_queue_enabled (global setting)
            self._config.offline_queue_enabled = self._reserve_offline_cb.isChecked()
            
            # Batch settings removed from schema (async framework handles this)
            # In-sequence enforcement removed (not in new schema)
            
            # Save to disk
            self._config.save()
            
            logger.info(
                f"Serial number handler config saved: mode={self._config.sn_mode}, "
                f"check_duplicates={self._config.sn_check_duplicates}"
            )
            
            # Success - no popup needed (prevents multiple popups on close)
            self._update_status()
            
        except Exception as e:
            self.handle_error(e, "saving serial number handler configuration")
    
    def load_config(self) -> None:
        """Load serial number handler configuration from config"""
        try:
            # Map new sn_mode field to old UI type selector
            mode_mapping = {
                "Manual Entry": "Manual Entry",
                "Auto-increment": "WATS Sequential",
                "Barcode Scanner": "External System",
                "External Source": "External System"
            }
            current_mode = self._config.sn_mode or "Manual Entry"
            ui_type = mode_mapping.get(current_mode, "Manual Entry")
            index = self._type_combo.findText(ui_type)
            if index >= 0:
                self._type_combo.setCurrentIndex(index)
            
            # Map duplicate checking to reuse checkbox (opposite logic)
            self._reuse_cb.setChecked(not self._config.sn_check_duplicates)
            
            # Map offline queue enabled to reserve offline checkbox
            self._reserve_offline_cb.setChecked(self._config.offline_queue_enabled)
            
            # In-sequence checkbox - not in new schema, default to True
            self._in_sequence_cb.setChecked(True)
            
            # Batch settings - not in new schema, use defaults
            self._batch_size_spin.setValue(10)
            self._fetch_threshold_spin.setValue(5)
            
            # Start-from display - not in new schema
            self._start_from_label.setText("(Not configured)")
            
            self._update_status()
            
            logger.debug("Serial number handler config loaded")
            
        except Exception as e:
            self.handle_error(e, "loading serial number handler configuration")
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix - consistency)."""
        pass  # No resources to clean
