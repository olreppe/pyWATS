"""Software Distribution Settings Page - Migrated with reliability improvements.

Improvements:
- H1: Error handling for save_config() with validation
- H4: cleanup() method
- Better folder validation
"""

import logging
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QSpinBox, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = logging.getLogger(__name__)


class SoftwarePage(BasePage):
    """Software Distribution settings page.
    
    Configures where software packages from WATS will be installed.
    The actual downloading and installation is handled by the service.
    
    Settings include:
    - Root folder for software installation
    - File transfer chunk size (advanced)
    """
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Software Distribution"
    
    def _setup_ui(self) -> None:
        """Setup page UI for software distribution settings"""
        
        # Root Folder Setting
        root_group = QGroupBox("Software Distribution")
        root_layout = QVBoxLayout(root_group)
        
        # Root folder row
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Root folder:"))
        
        self._root_folder_edit = QLineEdit()
        self._root_folder_edit.setPlaceholderText("Select folder for software installations...")
        self._root_folder_edit.setToolTip(
            "Root directory where software packages will be installed.\n"
            "The folder must exist and be empty."
        )
        folder_layout.addWidget(self._root_folder_edit, 1)
        
        self._browse_btn = QPushButton("Browse")
        self._browse_btn.setFixedWidth(80)
        self._browse_btn.clicked.connect(self._on_browse)
        folder_layout.addWidget(self._browse_btn)
        
        root_layout.addLayout(folder_layout)
        
        # Description
        desc_label = QLabel(
            "The root folder is where software packages from WATS will be installed.\n"
            "Each package will be placed in a subdirectory under this folder.\n"
            "The folder must exist and be empty when first configured."
        )
        desc_label.setStyleSheet("color: #808080; font-size: 11px;")
        desc_label.setWordWrap(True)
        root_layout.addWidget(desc_label)
        
        self._layout.addWidget(root_group)
        
        # Advanced Options (collapsed by default)
        advanced_group = QGroupBox("Advanced Options")
        advanced_group.setCheckable(True)
        advanced_group.setChecked(False)
        advanced_layout = QVBoxLayout(advanced_group)
        
        # Chunk size
        chunk_layout = QHBoxLayout()
        chunk_layout.addWidget(QLabel("File transfer chunk size:"))
        
        self._chunk_size_spin = QSpinBox()
        self._chunk_size_spin.setRange(1024, 10485760)  # 1KB to 10MB
        self._chunk_size_spin.setValue(65536)  # 64KB default
        self._chunk_size_spin.setSingleStep(1024)
        self._chunk_size_spin.setSuffix(" bytes")
        self._chunk_size_spin.setToolTip(
            "Size of each chunk when transferring files.\n"
            "Larger chunks may be faster but use more memory."
        )
        chunk_layout.addWidget(self._chunk_size_spin)
        
        chunk_layout.addStretch()
        advanced_layout.addLayout(chunk_layout)
        
        # Chunk size description
        chunk_desc = QLabel(
            "The chunk size controls how large each piece of a file transfer is.\n"
            "Default: 65536 bytes (64 KB). Increase for faster transfers on reliable connections."
        )
        chunk_desc.setStyleSheet("color: #808080; font-size: 11px;")
        chunk_desc.setWordWrap(True)
        advanced_layout.addWidget(chunk_desc)
        
        self._layout.addWidget(advanced_group)
        
        # Add stretch to push everything to top
        self._layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_config)
        self._layout.addWidget(save_btn)
    
    def _on_browse(self) -> None:
        """Browse for root folder with validation"""
        try:
            current = self._root_folder_edit.text() or str(Path.home())
            
            folder = QFileDialog.getExistingDirectory(
                self,
                "Select Software Distribution Root Folder",
                current
            )
            
            if folder:
                folder_path = Path(folder)
                
                # Validate folder exists
                if not folder_path.exists():
                    QMessageBox.warning(
                        self,
                        "Invalid Folder",
                        "The selected folder does not exist."
                    )
                    return
                
                # Check if empty (only for new configuration)
                if self._root_folder_edit.text() != folder:
                    contents = list(folder_path.iterdir())
                    if contents:
                        reply = QMessageBox.question(
                            self,
                            "Folder Not Empty",
                            "The selected folder is not empty.\n\n"
                            "For new configurations, an empty folder is recommended.\n"
                            "Use this folder anyway?",
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )
                        if reply != QMessageBox.StandardButton.Yes:
                            return
                
                self._root_folder_edit.setText(folder)
                logger.info(f"Software distribution root folder set to: {folder}")
                
        except Exception as e:
            logger.exception(f"Failed to browse for folder: {e}")
            QMessageBox.warning(
                self,
                "Browse Failed",
                f"Failed to select folder.\n\nError: {e}"
            )
    
    def save_config(self) -> None:
        """Save software distribution settings (H1 fix - error handling)"""
        try:
            root_folder = self._root_folder_edit.text().strip()
            
            # Validate folder if specified
            if root_folder:
                folder_path = Path(root_folder)
                if not folder_path.exists():
                    QMessageBox.warning(
                        self,
                        "Invalid Folder",
                        f"The specified folder does not exist:\n\n{root_folder}\n\n"
                        "Please select a valid folder."
                    )
                    return
            
            # Update config
            self._config["sw_dist_root"] = root_folder
            self._config["sw_dist_chunk_size"] = self._chunk_size_spin.value()
            
            # Save to disk
            self._config.save()
            
            logger.info(
                f"Software distribution settings saved: root={root_folder}, "
                f"chunk_size={self._chunk_size_spin.value()}"
            )
            
            QMessageBox.information(
                self,
                "Configuration Saved",
                "Software distribution settings have been saved successfully."
            )
            
        except Exception as e:
            logger.exception(f"Failed to save software distribution settings: {e}")
            QMessageBox.critical(
                self,
                "Save Failed",
                f"Failed to save software distribution settings.\n\n"
                f"Error: {e}\n\n"
                "Please check the logs for details and try again."
            )
    
    def load_config(self) -> None:
        """Load software distribution settings from config"""
        try:
            root = self._config.get("sw_dist_root", "")
            self._root_folder_edit.setText(root)
            
            chunk_size = self._config.get("sw_dist_chunk_size", 65536)
            self._chunk_size_spin.setValue(chunk_size)
            
            logger.debug("Software distribution settings loaded")
            
        except Exception as e:
            logger.exception(f"Failed to load software distribution settings: {e}")
            QMessageBox.warning(
                self,
                "Load Failed",
                f"Failed to load software distribution settings.\n\nError: {e}\n\n"
                "Using default values."
            )
    
    def cleanup(self) -> None:
        """Clean up resources (H4 fix - consistency)"""
        pass  # No resources to clean
