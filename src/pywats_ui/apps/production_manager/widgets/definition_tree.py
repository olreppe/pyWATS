"""Server definition tree panel.

Displays test sequence definitions in a folder tree mirroring
the WATS Production Manager left-side panel. Definitions are
loaded from the WATS server via the ServerBridge.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..server_bridge import ServerBridge

logger = logging.getLogger(__name__)

_STATUS_LABELS = {0: "Draft", 1: "Pending", 2: "Released", 3: "Revoked"}
_STATUS_COLORS = {
    0: "#888",      # Draft — gray
    1: "#f0ad4e",   # Pending — amber
    2: "#5cb85c",   # Released — green
    3: "#d9534f",   # Revoked — red
}


class DefinitionTree(QWidget):
    """Folder tree of server-side test sequence definitions.

    Emits ``definition_selected`` when a definition row is clicked.
    """

    definition_selected = Signal(dict)  # full definition dict

    def __init__(
        self,
        bridge: ServerBridge,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._definitions: List[Dict[str, Any]] = []

        self._setup_ui()
        self._connect_signals()

    # ----------------------------------------------------------------
    # UI
    # ----------------------------------------------------------------

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Search bar
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search and navigate")
        self._search.setClearButtonEnabled(True)
        self._search.setStyleSheet(
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " border-radius: 3px; padding: 4px 8px; }"
        )
        layout.addWidget(self._search)

        # Tree
        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Name", "Version"])
        self._tree.setColumnCount(2)
        self._tree.setRootIsDecorated(True)
        self._tree.setAlternatingRowColors(False)
        self._tree.setIndentation(20)
        header = self._tree.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._tree.setStyleSheet(
            "QTreeWidget { background: #1e1e1e; color: #ddd; border: none; }"
            "QTreeWidget::item { padding: 3px 0; }"
            "QTreeWidget::item:selected { background: #094771; }"
            "QTreeWidget::item:hover { background: #2a2d2e; }"
        )
        layout.addWidget(self._tree)

        # Status label
        self._status_label = QLabel("Not connected")
        self._status_label.setStyleSheet("color: #888; font-size: 11px; padding: 2px 4px;")
        layout.addWidget(self._status_label)

    def _connect_signals(self) -> None:
        self._search.textChanged.connect(self._filter_tree)
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._bridge.definitions_loaded.connect(self._on_definitions_loaded)
        self._bridge.error_occurred.connect(self._on_error)

    # ----------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------

    def refresh(self) -> None:
        """Request definitions from the server."""
        self._status_label.setText("Loading...")
        self._bridge.load_definitions(is_global=False)

    # ----------------------------------------------------------------
    # Signal handlers
    # ----------------------------------------------------------------

    def _on_definitions_loaded(self, definitions: list) -> None:
        self._definitions = definitions
        self._rebuild_tree()
        count = len(definitions)
        self._status_label.setText(f"{count} definition{'s' if count != 1 else ''}")

    def _on_error(self, message: str) -> None:
        self._status_label.setText(f"Error: {message}")
        logger.error("Definition tree error: %s", message)

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        defn = item.data(0, Qt.ItemDataRole.UserRole)
        if defn is not None:
            self.definition_selected.emit(defn)

    # ----------------------------------------------------------------
    # Tree building
    # ----------------------------------------------------------------

    def _rebuild_tree(self) -> None:
        self._tree.clear()

        # Group by VirtualFolderId
        folders: Dict[str, List[Dict[str, Any]]] = {}
        no_folder: List[Dict[str, Any]] = []

        for defn in self._definitions:
            folder_id = defn.get("VirtualFolderId")
            if folder_id:
                folders.setdefault(str(folder_id), []).append(defn)
            else:
                no_folder.append(defn)

        # For now, create a flat folder per folder_id (no folder name from API)
        # and show definitions as children
        if len(folders) <= 1 and not no_folder:
            # All in same folder — display flat
            for defn in self._definitions:
                self._add_definition_item(self._tree.invisibleRootItem(), defn)
        else:
            folder_idx = 0
            for folder_id, defs in sorted(folders.items()):
                folder_idx += 1
                folder_item = QTreeWidgetItem(["Folder", ""])
                folder_item.setFlags(
                    folder_item.flags() & ~Qt.ItemFlag.ItemIsSelectable
                )
                self._tree.addTopLevelItem(folder_item)
                folder_item.setExpanded(True)
                for defn in defs:
                    self._add_definition_item(folder_item, defn)

            for defn in no_folder:
                self._add_definition_item(self._tree.invisibleRootItem(), defn)

        self._tree.expandAll()

    def _add_definition_item(
        self, parent: QTreeWidgetItem, defn: Dict[str, Any]
    ) -> QTreeWidgetItem:
        name = defn.get("Name", "Untitled")
        version = str(defn.get("Version", ""))
        status = defn.get("Status", 0)

        item = QTreeWidgetItem([name, version])
        item.setData(0, Qt.ItemDataRole.UserRole, defn)

        # Color-code by status
        color = _STATUS_COLORS.get(status, "#888")
        item.setForeground(0, QColor(color))

        parent.addChild(item)
        return item

    # ----------------------------------------------------------------
    # Filtering
    # ----------------------------------------------------------------

    def _filter_tree(self, text: str) -> None:
        text_lower = text.lower()
        for i in range(self._tree.topLevelItemCount()):
            top = self._tree.topLevelItem(i)
            self._filter_item(top, text_lower)

    def _filter_item(self, item: QTreeWidgetItem, text: str) -> bool:
        """Recursively show/hide items matching the filter. Returns True if visible."""
        if item.childCount() == 0:
            # Leaf — match against name
            name = item.text(0).lower()
            visible = text == "" or text in name
            item.setHidden(not visible)
            return visible

        # Branch — show if any child matches
        any_visible = False
        for i in range(item.childCount()):
            child_visible = self._filter_item(item.child(i), text)
            any_visible = any_visible or child_visible

        item.setHidden(not any_visible)
        item.setExpanded(any_visible and text != "")
        return any_visible
