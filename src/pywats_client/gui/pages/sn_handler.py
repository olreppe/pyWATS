"""
SN Handler Page

Serial Number Handler page for managing serial numbers through the WATS server.
This page allows users to:
- View available serial number types configured on the server
- Take/reserve serial numbers for testing
- View serial number usage statistics

Based on the WATS Production API:
- GET /api/Production/SerialNumberTypes - List available types
- POST /api/Production/TakeSerialNumber - Reserve serial numbers
- GET /api/Production/SerialNumbers - Query serial numbers
"""

from typing import Optional, List, TYPE_CHECKING
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpinBox, QMessageBox, QTextEdit,
    QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt

from .base import BasePage
from ...core.config import ClientConfig

if TYPE_CHECKING:
    from ..main_window import MainWindow


class TakeSerialNumbersDialog(QDialog):
    """Dialog for taking serial numbers"""
    
    def __init__(self, type_name: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.type_name = type_name
        self.setWindowTitle(f"Take Serial Numbers - {type_name}")
        self.setMinimumWidth(450)
        
        self.count = 1
        self.ref_sn = ""
        self.ref_pn = ""
        self.ref_station = ""
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        
        # Type (read-only)
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Type:"))
        type_label = QLabel(self.type_name)
        type_label.setStyleSheet("color: #4ec9b0; font-weight: bold;")
        type_layout.addWidget(type_label)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        layout.addSpacing(10)
        
        # Count
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Count:"))
        self._count_spin = QSpinBox()
        self._count_spin.setRange(1, 1000)
        self._count_spin.setValue(1)
        self._count_spin.setFixedWidth(100)
        count_layout.addWidget(self._count_spin)
        count_layout.addStretch()
        layout.addLayout(count_layout)
        
        layout.addSpacing(10)
        
        # Reference section
        ref_group = QGroupBox("Reference (Optional)")
        ref_layout = QVBoxLayout(ref_group)
        
        # Reference Serial Number
        ref_sn_layout = QHBoxLayout()
        ref_sn_label = QLabel("Serial Number:")
        ref_sn_label.setFixedWidth(100)
        ref_sn_layout.addWidget(ref_sn_label)
        self._ref_sn_edit = QLineEdit()
        self._ref_sn_edit.setPlaceholderText("Reference serial number")
        ref_sn_layout.addWidget(self._ref_sn_edit)
        ref_layout.addLayout(ref_sn_layout)
        
        # Reference Part Number
        ref_pn_layout = QHBoxLayout()
        ref_pn_label = QLabel("Part Number:")
        ref_pn_label.setFixedWidth(100)
        ref_pn_layout.addWidget(ref_pn_label)
        self._ref_pn_edit = QLineEdit()
        self._ref_pn_edit.setPlaceholderText("Reference part number")
        ref_pn_layout.addWidget(self._ref_pn_edit)
        ref_layout.addLayout(ref_pn_layout)
        
        # Reference Station
        ref_station_layout = QHBoxLayout()
        ref_station_label = QLabel("Station:")
        ref_station_label.setFixedWidth(100)
        ref_station_layout.addWidget(ref_station_label)
        self._ref_station_edit = QLineEdit()
        self._ref_station_edit.setPlaceholderText("Station name")
        ref_station_layout.addWidget(self._ref_station_edit)
        ref_layout.addLayout(ref_station_layout)
        
        layout.addWidget(ref_group)
        
        layout.addSpacing(10)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_values(self) -> dict:
        """Get the values from the dialog"""
        return {
            'count': self._count_spin.value(),
            'ref_sn': self._ref_sn_edit.text().strip(),
            'ref_pn': self._ref_pn_edit.text().strip(),
            'ref_station': self._ref_station_edit.text().strip()
        }


class SNHandlerPage(BasePage):
    """Serial Number Handler page - manage serial numbers from WATS server"""
    
    def __init__(
        self, 
        config: ClientConfig, 
        main_window: Optional['MainWindow'] = None,
        parent: Optional[QWidget] = None
    ):
        self._main_window = main_window
        self._sn_types: List = []
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "SN Handler"
    
    def _setup_ui(self) -> None:
        """Setup page UI for Serial Number handling"""
        # Serial Number Types Group
        types_group = QGroupBox("Serial Number Types")
        types_layout = QVBoxLayout(types_group)
        
        # Types table
        self._types_table = QTableWidget()
        self._types_table.setColumnCount(4)
        self._types_table.setHorizontalHeaderLabels([
            "Type Name", "Prefix", "Suffix", "Description"
        ])
        self._types_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self._types_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._types_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._types_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self._types_table.verticalHeader().setVisible(False)
        self._types_table.setAlternatingRowColors(True)
        self._types_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._types_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._types_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._types_table.setMaximumHeight(150)
        self._types_table.setColumnWidth(0, 150)
        self._types_table.itemSelectionChanged.connect(self._on_type_selected)
        types_layout.addWidget(self._types_table)
        
        # Action buttons in header
        action_layout = QHBoxLayout()
        self._refresh_btn = QPushButton("Refresh")
        self._refresh_btn.clicked.connect(self._on_refresh_types)
        action_layout.addWidget(self._refresh_btn)
        
        self._take_btn = QPushButton("Take")
        self._take_btn.setEnabled(False)
        self._take_btn.clicked.connect(self._on_take_serials)
        action_layout.addWidget(self._take_btn)
        
        action_layout.addStretch()
        types_layout.addLayout(action_layout)
        
        self._layout.addWidget(types_group)
        
        self._layout.addSpacing(15)
        
        # Results Group
        results_group = QGroupBox("Taken Serial Numbers")
        results_layout = QVBoxLayout(results_group)
        
        self._results_text = QTextEdit()
        self._results_text.setReadOnly(True)
        self._results_text.setMaximumHeight(120)
        self._results_text.setStyleSheet(
            "background-color: #1e1e1e; font-family: monospace; font-size: 11px;"
        )
        self._results_text.setPlaceholderText(
            "Serial numbers will appear here after taking..."
        )
        results_layout.addWidget(self._results_text)
        
        # Copy button
        copy_layout = QHBoxLayout()
        self._copy_btn = QPushButton("Copy to Clipboard")
        self._copy_btn.setEnabled(False)
        self._copy_btn.clicked.connect(self._on_copy_results)
        copy_layout.addWidget(self._copy_btn)
        copy_layout.addStretch()
        results_layout.addLayout(copy_layout)
        
        self._layout.addWidget(results_group)
        
        # Status
        self._status_label = QLabel("Connect to WATS server to manage serial numbers")
        self._status_label.setStyleSheet("color: #808080; font-style: italic;")
        self._layout.addWidget(self._status_label)
        
        # Add stretch
        self._layout.addStretch()
        
        # Auto-load types if connected
        if self._main_window and self._main_window.app.wats_client:
            print("[SN Handler] Auto-loading types on initialization")
            self._load_sn_types()
    
    def _on_type_selected(self) -> None:
        """Handle serial number type selection in table"""
        selected = self._types_table.selectedItems()
        # Enable Take button only when a type is selected
        self._take_btn.setEnabled(len(selected) > 0)
    
    def _on_refresh_types(self) -> None:
        """Refresh serial number types from server"""
        if self._main_window and self._main_window.app.wats_client:
            self._load_sn_types()
        else:
            QMessageBox.warning(
                self, "Not Connected",
                "Please connect to WATS server first."
            )
    
    def _on_take_serials(self) -> None:
        """Take serial numbers from server"""
        # Get selected type from table
        selected = self._types_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Please select a serial number type.")
            return
        
        row = selected[0].row()
        type_item = self._types_table.item(row, 0)
        if not type_item:
            return
        
        type_name = type_item.text()
        
        # Show dialog
        dialog = TakeSerialNumbersDialog(type_name, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            # TODO: Implement actual API call to take serial numbers
            self._results_text.append(f"Taking {values['count']} serial number(s) of type '{type_name}'...")
            if values['ref_sn']:
                self._results_text.append(f"  Reference SN: {values['ref_sn']}")
            if values['ref_pn']:
                self._results_text.append(f"  Reference PN: {values['ref_pn']}")
            if values['ref_station']:
                self._results_text.append(f"  Station: {values['ref_station']}")
            self._results_text.append("\n[Not yet implemented - API call needed]\n")
            self._copy_btn.setEnabled(True)
    
    def _on_copy_results(self) -> None:
        """Copy results to clipboard"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self._results_text.toPlainText())
        self._status_label.setText("Copied to clipboard")
    
    def _load_sn_types(self) -> None:
        """Load serial number types from WATS server"""
        try:
            self._status_label.setText("Loading serial number types...")
            print("[SN Handler] Starting to load serial number types...")
            
            if self._main_window and self._main_window.app.wats_client:
                client = self._main_window.app.wats_client
                print(f"[SN Handler] WATS client available: {client}")
                # Get serial number types from production API
                types = client.production.get_serial_number_types()
                print(f"[SN Handler] Received {len(types) if types else 0} types from API")
                if types:
                    self._sn_types = types
                    print(f"[SN Handler] First type: {types[0].name if types else 'N/A'}")
                else:
                    self._sn_types = []
            else:
                print(f"[SN Handler] No client - main_window: {self._main_window}, wats_client: {self._main_window.app.wats_client if self._main_window else None}")
                self._sn_types = []
                self._status_label.setText("Not connected to WATS server")
                return
            
            print(f"[SN Handler] Populating table with {len(self._sn_types)} types")
            self._populate_types_table()
            self._status_label.setText(f"Found {len(self._sn_types)} serial number types")
            
        except Exception as e:
            print(f"[SN Handler] Error: {e}")
            import traceback
            traceback.print_exc()
            self._status_label.setText(f"Error: {str(e)}")
    

    
    def _populate_types_table(self) -> None:
        """Populate serial number types table"""
        self._types_table.setRowCount(len(self._sn_types))
        for row, sn_type in enumerate(self._sn_types):
            self._types_table.setItem(row, 0, QTableWidgetItem(sn_type.name or ""))
            self._types_table.setItem(row, 1, QTableWidgetItem(getattr(sn_type, 'prefix', '') or ""))
            self._types_table.setItem(row, 2, QTableWidgetItem(getattr(sn_type, 'suffix', '') or ""))
            self._types_table.setItem(row, 3, QTableWidgetItem(sn_type.description or ""))
    

    
    def save_config(self) -> None:
        """No configuration to save for this page"""
        pass
    
    def load_config(self) -> None:
        """No configuration to load for this page"""
        pass
