"""Instructions (PDF) tab.

Displays attached PDF documents for a Manual Inspection definition.
Supports Add (upload), Delete, and Download via the WATS Blob/mi endpoints.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..server_bridge import ServerBridge

logger = logging.getLogger(__name__)


class InstructionsTab(QWidget):
    """Instructions (PDF) tab.

    Shows a list of PDF documents attached to the currently selected
    MI definition. Supports Add (upload), Delete, and Download.
    """

    def __init__(
        self,
        bridge: ServerBridge,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._definition_id: Optional[str] = None
        self._documents: List[Dict[str, Any]] = []
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
        self._count_label.setStyleSheet("font-size: 13px; color: #ddd;")
        header_row.addWidget(self._count_label)

        header_row.addStretch()

        self._btn_add = QPushButton("+ Add")
        self._btn_add.setStyleSheet(
            "QPushButton { color: #ddd; padding: 4px 12px; border-radius: 3px;"
            " background: #2d2d2d; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
            "QPushButton:disabled { color: #666; }"
        )
        self._btn_add.clicked.connect(self._on_add)
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

        self._btn_download = QPushButton("📥 Download")
        self._btn_download.setStyleSheet(
            "QPushButton { color: #ddd; padding: 4px 12px; border-radius: 3px;"
            " background: #2d2d2d; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
            "QPushButton:disabled { color: #666; }"
        )
        self._btn_download.setEnabled(False)
        self._btn_download.clicked.connect(self._on_download)
        header_row.addWidget(self._btn_download)

        layout.addLayout(header_row)

        # --- Table ---
        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels([
            "Filename", "Size", "Uploaded"
        ])
        self._table.setAlternatingRowColors(True)
        self._table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)

        header_view = self._table.horizontalHeader()
        header_view.setStretchLastSection(True)
        header_view.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header_view.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header_view.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

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

        # --- Status label ---
        self._status_label = QLabel()
        self._status_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self._status_label)

    def _connect_signals(self) -> None:
        self._bridge.media_loaded.connect(self._on_media_loaded)
        self._bridge.operation_complete.connect(self._on_operation_complete)

    # ----------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------

    def load_documents(self, definition_id: str) -> None:
        """Request documents for the given definition from the server."""
        self._definition_id = definition_id
        self._status_label.setText("Loading documents...")
        self._bridge.load_media(definition_id)

    def clear(self) -> None:
        """Clear the table."""
        self._table.setRowCount(0)
        self._documents = []
        self._definition_id = None
        self._count_label.clear()
        self._status_label.clear()

    # ----------------------------------------------------------------
    # Selection
    # ----------------------------------------------------------------

    def _on_selection_changed(self) -> None:
        has_selection = len(self._table.selectedItems()) > 0
        self._btn_delete.setEnabled(has_selection)
        self._btn_download.setEnabled(has_selection)

    # ----------------------------------------------------------------
    # Add / Delete / Download
    # ----------------------------------------------------------------

    def _on_add(self) -> None:
        """Open file picker to select a PDF for upload."""
        if not self._definition_id:
            QMessageBox.information(self, "No Definition",
                                   "Select a definition first.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PDF Document", "",
            "PDF Files (*.pdf);;All Files (*)",
        )
        if file_path:
            self._status_label.setText(f"Uploading {os.path.basename(file_path)}...")
            self._bridge.upload_media(self._definition_id, file_path)

    def _on_delete(self) -> None:
        """Delete the selected document."""
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            return
        row_idx = rows[0].row()
        if row_idx >= len(self._documents):
            return

        doc = self._documents[row_idx]
        filename = doc.get("FileName", doc.get("Name", "document"))

        reply = QMessageBox.question(
            self, "Delete Document",
            f'Delete "{filename}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._bridge.delete_media(self._definition_id or "", doc)

    def _on_download(self) -> None:
        """Download the selected document."""
        rows = self._table.selectionModel().selectedRows()
        if not rows:
            return
        row_idx = rows[0].row()
        if row_idx >= len(self._documents):
            return

        doc = self._documents[row_idx]
        filename = doc.get("FileName", doc.get("Name", "document.pdf"))

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Document", filename,
            "PDF Files (*.pdf);;All Files (*)",
        )
        if save_path:
            self._status_label.setText(f"Downloading {filename}...")
            self._bridge.download_media(self._definition_id or "", doc, save_path)

    # ----------------------------------------------------------------
    # Signal handlers
    # ----------------------------------------------------------------

    def _on_media_loaded(self, documents: list) -> None:
        self._documents = documents
        self._rebuild_table()
        count = len(documents)
        self._count_label.setText(
            f"{count} document{'s' if count != 1 else ''}"
        )
        self._status_label.clear()

    def _on_operation_complete(self, message: str) -> None:
        """After upload/delete, refresh documents from server."""
        if self._definition_id and "media" in message.lower():
            self._status_label.setText(message)
            self._bridge.load_media(self._definition_id)

    def _rebuild_table(self) -> None:
        self._table.setRowCount(0)

        for doc in self._documents:
            row = self._table.rowCount()
            self._table.insertRow(row)

            # Filename
            filename = doc.get("FileName", doc.get("Name", ""))
            self._table.setItem(row, 0, QTableWidgetItem(filename))

            # Size
            size_bytes = doc.get("Size", doc.get("ContentLength", 0))
            size_text = self._format_size(size_bytes)
            size_item = QTableWidgetItem(size_text)
            size_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self._table.setItem(row, 1, size_item)

            # Uploaded date
            uploaded = doc.get("Created", doc.get("UploadDate", ""))
            if uploaded and hasattr(uploaded, "strftime"):
                uploaded = uploaded.strftime("%Y-%m-%d %H:%M")
            self._table.setItem(row, 2, QTableWidgetItem(str(uploaded)))

    @staticmethod
    def _format_size(size_bytes: Any) -> str:
        """Format bytes into a human-readable string."""
        try:
            size = int(size_bytes)
        except (TypeError, ValueError):
            return ""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
