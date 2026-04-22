"""Relations tab.

Displays the test sequence relations in a table matching the
WATS Production Manager 'Relations' tab layout, with Add/Delete/Edit support.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..server_bridge import ServerBridge

logger = logging.getLogger(__name__)

# Mapping from UI display label to (EntitySchema, EntityKey)
_RELATION_TYPES: List[Dict[str, str]] = [
    {"label": "Part number", "schema": "Product", "key": "PartNumber"},
    {"label": "Product revision", "schema": "Product", "key": "Revision"},
    {"label": "Serial number", "schema": "Unit", "key": "SerialNumber"},
    {"label": "Batch number", "schema": "Unit", "key": "BatchNumber"},
]


class RelationsTab(QWidget):
    """Relations tab showing product/process relations.

    Displays a table of relations for the currently selected definition,
    with columns matching the Production Manager: Active, Relation type,
    Value, Product name, Test operations.

    Supports Add, Delete, and Edit operations.
    """

    def __init__(
        self,
        bridge: ServerBridge,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._definition_id: Optional[str] = None
        self._relations: List[Dict[str, Any]] = []
        self._editing: bool = False
        self._setup_ui()
        self._connect_signals()

    # ----------------------------------------------------------------
    # UI
    # ----------------------------------------------------------------

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # --- Header with count + toolbar ---
        header_row = QHBoxLayout()
        header_row.setSpacing(12)

        self._count_label = QLabel()
        self._count_label.setStyleSheet(
            "font-size: 13px; color: #ddd;"
        )
        header_row.addWidget(self._count_label)

        header_row.addStretch()

        self._btn_add = QPushButton("+ Add")
        self._btn_add.setStyleSheet(
            "QPushButton { color: #ddd; padding: 4px 12px; border-radius: 3px;"
            " background: #2d2d2d; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
            "QPushButton:disabled { color: #666; }"
        )
        self._btn_add.clicked.connect(self._start_add)
        header_row.addWidget(self._btn_add)

        self._btn_delete = QPushButton("✕ Delete")
        self._btn_delete.setStyleSheet(
            "QPushButton { color: #ddd; padding: 4px 12px; border-radius: 3px;"
            " background: #2d2d2d; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
            "QPushButton:disabled { color: #666; }"
        )
        self._btn_delete.setEnabled(False)
        self._btn_delete.clicked.connect(self._on_delete)
        header_row.addWidget(self._btn_delete)

        self._btn_edit = QPushButton("✏ Edit")
        self._btn_edit.setStyleSheet(
            "QPushButton { color: #ddd; padding: 4px 12px; border-radius: 3px;"
            " background: #2d2d2d; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
            "QPushButton:disabled { color: #666; }"
        )
        self._btn_edit.setEnabled(False)
        self._btn_edit.clicked.connect(self._start_edit)
        header_row.addWidget(self._btn_edit)

        layout.addLayout(header_row)

        # --- Table ---
        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels([
            "Active", "Relation type", "Value", "Product name", "Test operations"
        ])
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)

        header_view = self._table.horizontalHeader()
        header_view.setStretchLastSection(True)
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        self._table.setStyleSheet(
            "QTableWidget { background: #1e1e1e; color: #ddd; border: none;"
            " gridline-color: #333; }"
            "QTableWidget::item { padding: 4px 8px; }"
            "QTableWidget::item:selected { background: #094771; }"
            "QHeaderView::section { background: #2d2d2d; color: #ccc;"
            " padding: 4px 8px; border: none; border-bottom: 1px solid #444; }"
        )
        self._table.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self._table)

        # --- Inline edit row (hidden by default) ---
        self._edit_row = QWidget()
        self._edit_row.setVisible(False)
        edit_layout = QHBoxLayout(self._edit_row)
        edit_layout.setContentsMargins(0, 4, 0, 4)
        edit_layout.setSpacing(8)

        self._edit_type_combo = QComboBox()
        for rt in _RELATION_TYPES:
            self._edit_type_combo.addItem(rt["label"])
        self._edit_type_combo.setStyleSheet(
            "QComboBox { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; min-width: 140px; }"
            "QComboBox QAbstractItemView { background: #2d2d2d; color: #ddd;"
            " selection-background-color: #094771; }"
        )
        edit_layout.addWidget(self._edit_type_combo)

        self._edit_value = QLineEdit()
        self._edit_value.setPlaceholderText("Value (e.g. ABC123 or ABC%)")
        self._edit_value.setStyleSheet(
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; }"
        )
        edit_layout.addWidget(self._edit_value, 1)

        self._btn_ok = QPushButton("✓ OK")
        self._btn_ok.setStyleSheet(
            "QPushButton { color: #fff; padding: 4px 16px; border-radius: 3px;"
            " background: #5cb85c; border: 1px solid #4cae4c; font-weight: bold; }"
            "QPushButton:hover { background: #449d44; }"
        )
        self._btn_ok.clicked.connect(self._on_save)
        edit_layout.addWidget(self._btn_ok)

        self._btn_cancel = QPushButton("✕ Cancel")
        self._btn_cancel.setStyleSheet(
            "QPushButton { color: #ddd; padding: 4px 12px; border-radius: 3px;"
            " background: #2d2d2d; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
        )
        self._btn_cancel.clicked.connect(self._on_cancel)
        edit_layout.addWidget(self._btn_cancel)

        layout.addWidget(self._edit_row)

        # --- Status label ---
        self._status_label = QLabel()
        self._status_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self._status_label)

    def _connect_signals(self) -> None:
        self._bridge.relations_loaded.connect(self._on_relations_loaded)
        self._bridge.operation_complete.connect(self._on_operation_complete)

    # ----------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------

    def load_relations(self, definition_id: str) -> None:
        """Request relations for the given definition from the server."""
        self._definition_id = definition_id
        self._status_label.setText("Loading relations...")
        self._bridge.load_relations(definition_id)

    def clear(self) -> None:
        """Clear the table."""
        self._table.setRowCount(0)
        self._relations = []
        self._definition_id = None
        self._count_label.clear()
        self._status_label.clear()
        self._on_cancel()

    # ----------------------------------------------------------------
    # Selection
    # ----------------------------------------------------------------

    def _on_selection_changed(self) -> None:
        has_selection = len(self._table.selectedItems()) > 0
        self._btn_delete.setEnabled(has_selection and not self._editing)
        self._btn_edit.setEnabled(has_selection and not self._editing)

    # ----------------------------------------------------------------
    # Add / Edit / Delete
    # ----------------------------------------------------------------

    def _start_add(self) -> None:
        """Show the inline edit row for adding a new relation."""
        if not self._definition_id:
            QMessageBox.information(self, "No Definition",
                                   "Select a definition first.")
            return
        self._editing = True
        self._edit_mode = "add"
        self._edit_type_combo.setCurrentIndex(0)
        self._edit_value.clear()
        self._edit_row.setVisible(True)
        self._edit_value.setFocus()
        self._btn_add.setEnabled(False)
        self._btn_delete.setEnabled(False)
        self._btn_edit.setEnabled(False)

    def _start_edit(self) -> None:
        """Populate the inline edit row from the selected relation."""
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            return
        row_idx = rows[0].row()
        if row_idx >= len(self._relations):
            return

        rel = self._relations[row_idx]
        self._editing = True
        self._edit_mode = "edit"
        self._edit_row_index = row_idx

        # Find matching relation type
        schema = rel.get("EntitySchema", "")
        key = rel.get("EntityKey", "")
        for i, rt in enumerate(_RELATION_TYPES):
            if rt["schema"] == schema and rt["key"] == key:
                self._edit_type_combo.setCurrentIndex(i)
                break

        self._edit_value.setText(rel.get("EntityValue", ""))
        self._edit_row.setVisible(True)
        self._edit_value.setFocus()
        self._btn_add.setEnabled(False)
        self._btn_delete.setEnabled(False)
        self._btn_edit.setEnabled(False)

    def _on_save(self) -> None:
        """Save the new or edited relation."""
        if not self._definition_id:
            return

        idx = self._edit_type_combo.currentIndex()
        rt = _RELATION_TYPES[idx]
        value = self._edit_value.text().strip()

        if not value:
            QMessageBox.warning(self, "Missing Value",
                                "Please enter a value for the relation.")
            return

        self._bridge.create_relation(
            self._definition_id, rt["schema"], rt["key"], value,
        )
        self._on_cancel()

    def _on_delete(self) -> None:
        """Delete the selected relation."""
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            return
        row_idx = rows[0].row()
        if row_idx >= len(self._relations):
            return

        rel = self._relations[row_idx]
        rel_type = self._table.item(row_idx, 1).text() if self._table.item(row_idx, 1) else ""
        value = rel.get("EntityValue", "")

        reply = QMessageBox.question(
            self, "Delete Relation",
            f'Delete relation "{rel_type} = {value}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._bridge.delete_relation(rel)

    def _on_cancel(self) -> None:
        """Hide the inline edit row."""
        self._editing = False
        self._edit_row.setVisible(False)
        self._btn_add.setEnabled(True)
        self._on_selection_changed()

    # ----------------------------------------------------------------
    # Signal handlers
    # ----------------------------------------------------------------

    def _on_relations_loaded(self, relations: list) -> None:
        self._relations = relations
        self._rebuild_table()
        count = len(relations)
        self._count_label.setText(
            f"{count} relation{'s' if count != 1 else ''}"
        )
        self._status_label.clear()

    def _on_operation_complete(self, message: str) -> None:
        """After a create/delete, refresh relations from server."""
        if self._definition_id:
            self._status_label.setText(message)
            self._bridge.load_relations(self._definition_id)

    def _rebuild_table(self) -> None:
        self._table.setRowCount(0)

        for rel in self._relations:
            row = self._table.rowCount()
            self._table.insertRow(row)

            # Active
            status = rel.get("Status", 0)
            active = status == 1
            active_item = QTableWidgetItem("Active" if active else "Inactive")
            active_item.setForeground(
                QColor("#5cb85c") if active else QColor("#888")
            )
            self._table.setItem(row, 0, active_item)

            # Relation type — show friendly label
            schema = rel.get("EntitySchema", "")
            key = rel.get("EntityKey", "")
            friendly = f"{schema}.{key}"
            for rt in _RELATION_TYPES:
                if rt["schema"] == schema and rt["key"] == key:
                    friendly = rt["label"]
                    break
            self._table.setItem(row, 1, QTableWidgetItem(friendly))

            # Value
            value = rel.get("EntityValue", "")
            self._table.setItem(row, 2, QTableWidgetItem(value))

            # Product name
            product = rel.get("ProductName") or ""
            self._table.setItem(row, 3, QTableWidgetItem(product))

            # Test operations
            process_rels = rel.get("TestSequenceProcessRelations", [])
            if process_rels:
                ops_text = f"{len(process_rels)} operation{'s' if len(process_rels) != 1 else ''}"
            else:
                ops_text = ""
            self._table.setItem(row, 4, QTableWidgetItem(ops_text))
