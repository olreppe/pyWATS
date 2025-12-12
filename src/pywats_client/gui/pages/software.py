"""
Software Page

Software Distribution page for downloading and managing software packages
from the WATS server. This allows test stations to receive updates to
test sequences, configurations, and other software.

Based on the WATS Software Distribution API:
- GET /api/Software/Packages - List all packages
- GET /api/Software/Package/{id} - Get package details
- GET /api/Software/PackagesByTag - Filter packages by tag
"""

import asyncio
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, 
    QHeaderView, QComboBox, QProgressBar, QMessageBox,
    QCheckBox
)
from PySide6.QtCore import Qt

from .base import BasePage
from ...core.config import ClientConfig

if TYPE_CHECKING:
    from ..main_window import MainWindow


class SoftwarePage(BasePage):
    """Software Distribution page - manage packages from WATS server"""
    
    def __init__(
        self, 
        config: ClientConfig, 
        main_window: Optional['MainWindow'] = None,
        parent: Optional[QWidget] = None
    ):
        self._main_window = main_window
        self._packages: List[Dict[str, Any]] = []
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Software"
    
    def _setup_ui(self) -> None:
        """Setup page UI for Software Distribution"""
        # Software Distribution Settings
        settings_group = QGroupBox("Software Distribution Settings")
        settings_layout = QVBoxLayout(settings_group)
        
        # Enable auto-update
        self._auto_update_cb = QCheckBox("Enable automatic software updates")
        self._auto_update_cb.setToolTip(
            "Automatically check for and download software updates from WATS"
        )
        self._auto_update_cb.stateChanged.connect(self._emit_changed)
        settings_layout.addWidget(self._auto_update_cb)
        
        # Virtual folder selection
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Virtual Folder:")
        folder_label.setFixedWidth(100)
        folder_layout.addWidget(folder_label)
        
        self._folder_combo = QComboBox()
        self._folder_combo.addItem("(All Folders)", "")
        self._folder_combo.setToolTip("Filter packages by virtual folder")
        folder_layout.addWidget(self._folder_combo, 1)
        
        self._refresh_folders_btn = QPushButton("Refresh")
        self._refresh_folders_btn.setFixedWidth(80)
        self._refresh_folders_btn.clicked.connect(self._on_refresh_folders)
        folder_layout.addWidget(self._refresh_folders_btn)
        
        settings_layout.addLayout(folder_layout)
        
        self._layout.addWidget(settings_group)
        
        self._layout.addSpacing(15)
        
        # Available Packages
        packages_group = QGroupBox("Available Packages")
        packages_layout = QVBoxLayout(packages_group)
        
        # Filter row
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Status:"))
        
        self._status_combo = QComboBox()
        self._status_combo.addItems(["Released", "All", "Draft", "Pending", "Revoked"])
        self._status_combo.currentIndexChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self._status_combo)
        
        filter_layout.addSpacing(20)
        filter_layout.addWidget(QLabel("Search:"))
        
        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText("Search packages...")
        self._search_edit.textChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self._search_edit, 1)
        
        packages_layout.addLayout(filter_layout)
        
        # Packages table
        self._packages_table = QTableWidget()
        self._packages_table.setColumnCount(5)
        self._packages_table.setHorizontalHeaderLabels([
            "Name", "Version", "Status", "Description", "Updated"
        ])
        self._packages_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self._packages_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._packages_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._packages_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self._packages_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self._packages_table.verticalHeader().setVisible(False)
        self._packages_table.setAlternatingRowColors(True)
        self._packages_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._packages_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._packages_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._packages_table.setColumnWidth(0, 200)
        packages_layout.addWidget(self._packages_table)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        self._refresh_btn = QPushButton("Refresh List")
        self._refresh_btn.clicked.connect(self._on_refresh_packages)
        btn_layout.addWidget(self._refresh_btn)
        
        self._download_btn = QPushButton("Download Selected")
        self._download_btn.setEnabled(False)
        self._download_btn.clicked.connect(self._on_download_package)
        btn_layout.addWidget(self._download_btn)
        
        btn_layout.addStretch()
        
        # Progress indicator
        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        self._progress_bar.setMaximumWidth(200)
        btn_layout.addWidget(self._progress_bar)
        
        packages_layout.addLayout(btn_layout)
        
        self._layout.addWidget(packages_group, 1)
        
        # Status message
        self._status_label = QLabel("Connect to WATS server to view available packages")
        self._status_label.setStyleSheet("color: #808080; font-style: italic;")
        self._layout.addWidget(self._status_label)
        
        # Connect table selection
        self._packages_table.itemSelectionChanged.connect(self._on_selection_changed)
        
        # Auto-load packages if connected
        if self._main_window and self._main_window.app.wats_client:
            print("[Software] Auto-loading packages on initialization")
            self._load_packages()
    
    def _on_selection_changed(self) -> None:
        """Handle package selection change"""
        selected = self._packages_table.selectedItems()
        self._download_btn.setEnabled(len(selected) > 0)
    
    def _on_filter_changed(self) -> None:
        """Handle filter changes - refresh displayed packages"""
        self._populate_packages_table()
    
    def _on_refresh_folders(self) -> None:
        """Refresh virtual folders from server"""
        if self._main_window and self._main_window.app.wats_client:
            self._load_virtual_folders()
        else:
            QMessageBox.warning(
                self, "Not Connected",
                "Please connect to WATS server first."
            )
    
    def _on_refresh_packages(self) -> None:
        """Refresh packages from server"""
        if self._main_window and self._main_window.app.wats_client:
            self._load_packages()
        else:
            QMessageBox.warning(
                self, "Not Connected",
                "Please connect to WATS server first."
            )
    
    def _on_download_package(self) -> None:
        """Download selected package"""
        selected_row = self._packages_table.currentRow()
        if selected_row < 0:
            return
        
        # Get package name from table
        name_item = self._packages_table.item(selected_row, 0)
        if name_item:
            package_name = name_item.text()
            QMessageBox.information(
                self, "Download",
                f"Download functionality for '{package_name}' not yet implemented.\n"
                "This will download the package files to the local machine."
            )
    
    def _load_virtual_folders(self) -> None:
        """Load virtual folders from WATS server"""
        try:
            self._status_label.setText("Loading virtual folders...")
            # TODO: Implement when client has software module access
            # folders = self._main_window.app.wats_client.software.get_virtual_folders()
            self._status_label.setText("Virtual folders loaded")
        except Exception as e:
            self._status_label.setText(f"Error loading folders: {str(e)}")
    
    def _load_packages(self) -> None:
        """Load packages from WATS server"""
        try:
            self._status_label.setText("Loading packages...")
            self._progress_bar.setVisible(True)
            self._progress_bar.setRange(0, 0)  # Indeterminate
            print("[Software] Starting to load packages...")
            
            if self._main_window and self._main_window.app.wats_client:
                client = self._main_window.app.wats_client
                print(f"[Software] WATS client available: {client}")
                # Get software packages from API
                packages = client.software.get_packages()
                print(f"[Software] Received {len(packages) if packages else 0} packages from API")
                if packages:
                    self._packages = packages
                    print(f"[Software] First package: {packages[0].name if packages else 'N/A'}")
                else:
                    self._packages = []
            else:
                print(f"[Software] No client - main_window: {self._main_window}, wats_client: {self._main_window.app.wats_client if self._main_window else None}")
                self._packages = []
            
            print(f"[Software] Populating table with {len(self._packages)} packages")
            self._populate_packages_table()
            self._progress_bar.setVisible(False)
            self._status_label.setText(f"Found {len(self._packages)} packages")
            
        except Exception as e:
            print(f"[Software] Error: {e}")
            import traceback
            traceback.print_exc()
            self._progress_bar.setVisible(False)
            self._status_label.setText(f"Error loading packages: {str(e)}")
    
    def _populate_packages_table(self) -> None:
        """Populate packages table with filtered results"""
        search_text = self._search_edit.text().lower()
        status_filter = self._status_combo.currentText()
        
        # Filter packages
        filtered = []
        for pkg in self._packages:
            # Status filter
            if status_filter != "All":
                pkg_status = str(pkg.status.value) if pkg.status else ""
                if pkg_status.lower() != status_filter.lower():
                    continue
            
            # Search filter
            if search_text:
                name = (pkg.name or "").lower()
                desc = (pkg.description or "").lower()
                if search_text not in name and search_text not in desc:
                    continue
            
            filtered.append(pkg)
        
        # Populate table
        self._packages_table.setRowCount(len(filtered))
        for row, pkg in enumerate(filtered):
            self._packages_table.setItem(row, 0, QTableWidgetItem(pkg.name or ""))
            self._packages_table.setItem(row, 1, QTableWidgetItem(str(pkg.version) if pkg.version else ""))
            self._packages_table.setItem(row, 2, QTableWidgetItem(str(pkg.status.value) if pkg.status else ""))
            self._packages_table.setItem(row, 3, QTableWidgetItem(pkg.description or ""))
            modified = str(pkg.modified_utc)[:10] if pkg.modified_utc else ""
            self._packages_table.setItem(row, 4, QTableWidgetItem(modified))
    
    def save_config(self) -> None:
        """Save configuration"""
        self.config.software_auto_update = self._auto_update_cb.isChecked()
    
    def load_config(self) -> None:
        """Load configuration"""
        self._auto_update_cb.setChecked(
            getattr(self.config, 'software_auto_update', False)
        )

