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
    QCheckBox, QTreeWidget, QTreeWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

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
        
        # Add small refresh button inline with filters
        self._refresh_btn = QPushButton("⟳")
        self._refresh_btn.setFixedSize(28, 28)
        self._refresh_btn.setToolTip("Refresh packages from server")
        self._refresh_btn.clicked.connect(self._on_refresh_packages)
        filter_layout.addWidget(self._refresh_btn)
        
        packages_layout.addLayout(filter_layout)
        
        # Packages tree view (organized by virtual folders)
        self._packages_tree = QTreeWidget()
        self._packages_tree.setColumnCount(4)
        self._packages_tree.setHeaderLabels([
            "Package / Folder", "Version", "Status", "Updated"
        ])
        self._packages_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self._packages_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._packages_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._packages_tree.header().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self._packages_tree.setAlternatingRowColors(True)
        self._packages_tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self._packages_tree.setIndentation(20)
        self._packages_tree.setColumnWidth(0, 300)
        # Apply styling to match other grids in the app
        self._packages_tree.setStyleSheet("""
            QTreeWidget {
                font-size: 11pt;
                background-color: #1e1e1e;
                alternate-background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
            }
            QTreeWidget::item:hover {
                background-color: #2d2d2d;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                padding: 4px;
                border: 1px solid #3c3c3c;
                font-weight: bold;
            }
        """)
        packages_layout.addWidget(self._packages_tree)
        
        # Progress indicator
        progress_layout = QHBoxLayout()
        progress_layout.addStretch()
        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        self._progress_bar.setMaximumWidth(200)
        progress_layout.addWidget(self._progress_bar)
        packages_layout.addLayout(progress_layout)
        
        self._layout.addWidget(packages_group, 1)
        
        # Status message
        self._status_label = QLabel("Connect to WATS server to view available packages")
        self._status_label.setStyleSheet("color: #808080; font-style: italic;")
        self._layout.addWidget(self._status_label)
        
        # Connect tree selection
        self._packages_tree.itemSelectionChanged.connect(self._on_selection_changed)
        
        # Auto-load packages if connected
        if self._main_window and self._main_window.app.wats_client:
            print("[Software] Auto-loading packages on initialization")
            self._load_packages()
    
    def _on_selection_changed(self) -> None:
        """Handle package selection change"""
        # Selection tracking for future features
        pass
    
    def _on_filter_changed(self) -> None:
        """Handle filter changes - refresh displayed packages"""
        self._populate_packages_tree()
    

    
    def _on_refresh_packages(self) -> None:
        """Refresh packages from server"""
        if self._main_window and self._main_window.app.wats_client:
            self._load_packages()
        else:
            QMessageBox.warning(
                self, "Not Connected",
                "Please connect to WATS server first."
            )
    

    

    
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
            
            print(f"[Software] Populating tree with {len(self._packages)} packages")
            self._populate_packages_tree()
            self._progress_bar.setVisible(False)
            self._status_label.setText(f"Found {len(self._packages)} packages")
            
        except Exception as e:
            print(f"[Software] Error: {e}")
            import traceback
            traceback.print_exc()
            self._progress_bar.setVisible(False)
            self._status_label.setText(f"Error loading packages: {str(e)}")
    
    def _populate_packages_tree(self) -> None:
        """Populate packages tree with folders and filtered results"""
        search_text = self._search_edit.text().lower()
        status_filter = self._status_combo.currentText()
        
        self._packages_tree.clear()
        
        # Organize packages by virtual folder
        folders: Dict[str, List[Any]] = {}
        
        for pkg in self._packages:
            # Status filter
            if status_filter != "All":
                # Status might be enum or string
                if hasattr(pkg.status, 'value'):
                    pkg_status = str(pkg.status.value)
                else:
                    pkg_status = str(pkg.status) if pkg.status else ""
                if pkg_status.lower() != status_filter.lower():
                    continue
            
            # Search filter
            if search_text:
                name = (pkg.name or "").lower()
                desc = (pkg.description or "").lower()
                if search_text not in name and search_text not in desc:
                    continue
            
            # Get folder from tags or use "Uncategorized"
            folder_name = "Uncategorized"
            if pkg.tags:
                for tag in pkg.tags:
                    if hasattr(tag, 'key') and tag.key == "Folder":
                        folder_name = tag.value or "Uncategorized"
                        break
            
            if folder_name not in folders:
                folders[folder_name] = []
            folders[folder_name].append(pkg)
        
        # Create tree structure
        for folder_name in sorted(folders.keys()):
            # Create folder item
            folder_item = QTreeWidgetItem(self._packages_tree)
            folder_item.setText(0, f"📁 {folder_name}")
            folder_item.setExpanded(True)
            
            # Add packages to folder
            for pkg in folders[folder_name]:
                pkg_item = QTreeWidgetItem(folder_item)
                pkg_item.setText(0, pkg.name or "")
                pkg_item.setText(1, str(pkg.version) if pkg.version else "")
                
                # Status might be enum or string
                if hasattr(pkg.status, 'value'):
                    status_str = str(pkg.status.value)
                else:
                    status_str = str(pkg.status) if pkg.status else ""
                pkg_item.setText(2, status_str)
                
                modified = str(pkg.modified_utc)[:10] if pkg.modified_utc else ""
                pkg_item.setText(3, modified)
                
                # Store package data
                pkg_item.setData(0, Qt.ItemDataRole.UserRole, pkg)
    
    def save_config(self) -> None:
        """Save configuration"""
        self.config.software_auto_update = self._auto_update_cb.isChecked()
    
    def load_config(self) -> None:
        """Load configuration"""
        self._auto_update_cb.setChecked(
            getattr(self.config, 'software_auto_update', False)
        )

