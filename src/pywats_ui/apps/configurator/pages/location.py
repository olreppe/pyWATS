"""Location Page - Migrated with minimal changes (simple settings).

Improvements:
- H1: Error handling for save_config()
- H4: cleanup() method
"""

import logging
from pywats.core.logging import get_logger
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QGroupBox, QCheckBox
)
from PySide6.QtCore import Qt

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = get_logger(__name__)


class LocationPage(BasePage):
    """Location services settings page.
    
    Manages location services settings for the WATS client.
    This is about enabling/disabling location services (GPS/network location sharing),
    NOT about station naming or physical location text.
    """
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Location"
    
    def _setup_ui(self) -> None:
        """Setup page UI matching WATS Client design"""
        # Location Services Group
        location_group = QGroupBox("Location Services")
        location_layout = QVBoxLayout(location_group)
        
        # Enable location services checkbox
        self._location_enabled_cb = QCheckBox("Allow this app to use location services")
        self._location_enabled_cb.setToolTip(
            "When enabled, the client can send location data with reports.\n"
            "This helps track where units are tested."
        )
        location_layout.addWidget(self._location_enabled_cb)
        
        # Info text
        info_label = QLabel(
            "Location services allow the WATS client to include geographical\n"
            "coordinates when submitting test reports. This can help with:\n\n"
            "  • Tracking where units are manufactured or tested\n"
            "  • Identifying location-specific yield issues\n"
            "  • Compliance and traceability requirements"
        )
        info_label.setStyleSheet("color: #808080; font-size: 11px; margin-top: 10px;")
        location_layout.addWidget(info_label)
        
        self._layout.addWidget(location_group)
        
        self._layout.addSpacing(15)
        
        # Privacy notice
        privacy_group = QGroupBox("Privacy")
        privacy_layout = QVBoxLayout(privacy_group)
        
        privacy_label = QLabel(
            "When location services are enabled:\n\n"
            "  • Location data is only sent with test reports\n"
            "  • No background location tracking occurs\n"
            "  • Location accuracy depends on your network/GPS settings\n"
            "  • You can disable this at any time"
        )
        privacy_label.setStyleSheet("color: #808080; font-size: 11px;")
        privacy_layout.addWidget(privacy_label)
        
        self._layout.addWidget(privacy_group)
        
        # Add stretch to push content to top
        self._layout.addStretch()
    
    def save_config(self) -> None:
        """Save configuration (H1 fix - error handling)"""
        try:
            self._config["location_services_enabled"] = self._location_enabled_cb.isChecked()
            self._config.save()
            
            logger.info(f"Location services: {self._location_enabled_cb.isChecked()}")
            
        except Exception as e:
            self.handle_error(e, "saving location settings")
    
    def load_config(self) -> None:
        """Load configuration"""
        try:
            enabled = self._config.get("location_services_enabled", False)
            self._location_enabled_cb.setChecked(enabled)
            
            logger.debug("Location settings loaded")
            
        except Exception as e:
            self.handle_error(e, "loading location settings")
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix - consistency)"""
        pass  # No resources to clean
