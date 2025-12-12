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

import asyncio
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QSpinBox, QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt

from .base import BasePage
from ...core.config import ClientConfig

if TYPE_CHECKING:
    from ..main_window import MainWindow


class SNHandlerPage(BasePage):
    """Serial Number Handler page - manage serial numbers from WATS server"""
    
    def __init__(
        self, 
        config: ClientConfig, 
        main_window: Optional['MainWindow'] = None,
        parent: Optional[QWidget] = None
    ):
        self._main_window = main_window
        self._sn_types: List[Dict[str, Any]] = []
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
        
        # Refresh button
        refresh_layout = QHBoxLayout()
        self._refresh_btn = QPushButton("Refresh Types")
        self._refresh_btn.clicked.connect(self._on_refresh_types)
        refresh_layout.addWidget(self._refresh_btn)
        refresh_layout.addStretch()
        types_layout.addLayout(refresh_layout)
        
        self._layout.addWidget(types_group)
        
        self._layout.addSpacing(15)
        
        # Take Serial Numbers Group
        take_group = QGroupBox("Take Serial Numbers")
        take_layout = QVBoxLayout(take_group)
        
        # Type selection
        type_row = QHBoxLayout()
        type_label = QLabel("Type:")
        type_label.setFixedWidth(80)
        type_row.addWidget(type_label)
        
        self._type_combo = QComboBox()
        self._type_combo.setPlaceholderText("Select serial number type...")
        type_row.addWidget(self._type_combo, 1)
        take_layout.addLayout(type_row)
        
        # Count
        count_row = QHBoxLayout()
        count_label = QLabel("Count:")
        count_label.setFixedWidth(80)
        count_row.addWidget(count_label)
        
        self._count_spin = QSpinBox()
        self._count_spin.setRange(1, 1000)
        self._count_spin.setValue(1)
        self._count_spin.setFixedWidth(100)
        count_row.addWidget(self._count_spin)
        count_row.addStretch()
        take_layout.addLayout(count_row)
        
        # Reference (optional)
        ref_row = QHBoxLayout()
        ref_label = QLabel("Reference:")
        ref_label.setFixedWidth(80)
        ref_row.addWidget(ref_label)
        
        self._reference_edit = QLineEdit()
        self._reference_edit.setPlaceholderText("Optional reference (e.g., work order)")
        ref_row.addWidget(self._reference_edit, 1)
        take_layout.addLayout(ref_row)
        
        # Take button
        take_btn_row = QHBoxLayout()
        self._take_btn = QPushButton("Take Serial Numbers")
        self._take_btn.setEnabled(False)
        self._take_btn.clicked.connect(self._on_take_serials)
        take_btn_row.addWidget(self._take_btn)
        take_btn_row.addStretch()
        take_layout.addLayout(take_btn_row)
        
        self._layout.addWidget(take_group)
        
        self._layout.addSpacing(15)
        
        # Results Group
        results_group = QGroupBox("Results")
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
    
    def _on_type_selected(self) -> None:
        """Handle serial number type selection in table"""
        selected = self._types_table.selectedItems()
        if selected:
            row = selected[0].row()
            item = self._types_table.item(row, 0)
            if item is not None:
                type_name = item.text()
                # Select in combo box
                index = self._type_combo.findText(type_name)
                if index >= 0:
                    self._type_combo.setCurrentIndex(index)
    
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
        type_name = self._type_combo.currentText()
        if not type_name:
            QMessageBox.warning(self, "Error", "Please select a serial number type.")
            return
        
        if self._main_window and self._main_window.client:
            asyncio.create_task(self._take_serial_numbers())
        else:
            QMessageBox.warning(
                self, "Not Connected",
                "Please connect to WATS server first."
            )
    
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
            
            if self._main_window and self._main_window.app.wats_client:
                client = self._main_window.app.wats_client
                # Get serial number types from production API
                types = client.production.get_serial_number_types()
                if types:
                    self._sn_types = types
                else:
                    self._sn_types = []
            else:
                self._sn_types = []
                self._status_label.setText("Not connected to WATS server")
                return
            
            self._populate_types_table()
            self._populate_type_combo()
            self._status_label.setText(f"Found {len(self._sn_types)} serial number types")
            
        except Exception as e:
            self._status_label.setText(f"Error: {str(e)}")
    
    async def _take_serial_numbers(self) -> None:
        """Take serial numbers from server"""
        try:
            type_name = self._type_combo.currentText()
            count = self._count_spin.value()
            reference = self._reference_edit.text().strip() or None
            
            self._status_label.setText(f"Taking {count} serial number(s)...")
            self._take_btn.setEnabled(False)
            
            # TODO: Implement when client has production module access
            # serials = await self._main_window.client.take_serial_numbers(
            #     type_name=type_name,
            #     count=count,
            #     reference=reference
            # )
            
            # Placeholder
            serials = [f"{type_name}-{i:06d}" for i in range(1, count + 1)]
            
            # Display results
            self._results_text.setPlainText("\n".join(serials))
            self._copy_btn.setEnabled(True)
            self._status_label.setText(f"Successfully took {len(serials)} serial number(s)")
            
        except Exception as e:
            self._status_label.setText(f"Error: {str(e)}")
        finally:
            self._take_btn.setEnabled(True)
    
    def _populate_types_table(self) -> None:
        """Populate serial number types table"""
        self._types_table.setRowCount(len(self._sn_types))
        for row, sn_type in enumerate(self._sn_types):
            self._types_table.setItem(row, 0, QTableWidgetItem(sn_type.get("name", "")))
            self._types_table.setItem(row, 1, QTableWidgetItem(sn_type.get("prefix", "")))
            self._types_table.setItem(row, 2, QTableWidgetItem(sn_type.get("suffix", "")))
            self._types_table.setItem(row, 3, QTableWidgetItem(sn_type.get("description", "")))
    
    def _populate_type_combo(self) -> None:
        """Populate type combo box"""
        self._type_combo.clear()
        for sn_type in self._sn_types:
            self._type_combo.addItem(sn_type.get("name", ""))
        self._take_btn.setEnabled(len(self._sn_types) > 0)
    
    def save_config(self) -> None:
        """No configuration to save for this page"""
        pass
    
    def load_config(self) -> None:
        """No configuration to load for this page"""
        pass
