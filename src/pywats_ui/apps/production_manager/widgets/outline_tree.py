"""Outline tree panel for the Sequence Designer.

Shows the hierarchical structure of the sequence as a tree view.
Clicking a tree item selects the corresponding step on the canvas.
"""
from __future__ import annotations

from typing import Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHeaderView,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)

from ..models import STEP_META, SequenceModel, StepNode


class OutlineTree(QFrame):
    """Left-side tree view showing the sequence hierarchy."""

    def __init__(
        self,
        model: SequenceModel,
        parent: Optional[QFrame] = None,
    ) -> None:
        super().__init__(parent)
        self._model = model
        self._item_map: Dict[str, QTreeWidgetItem] = {}
        self._updating = False

        self.setMinimumWidth(180)
        self.setMaximumWidth(260)
        self.setStyleSheet(
            "OutlineTree { background: #252526; border-right: 1px solid #333; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QLabel("  Outline")
        header.setFixedHeight(32)
        header.setStyleSheet(
            "background: #333; color: #ccc; font-weight: bold; "
            "font-size: 12px; padding-left: 8px; border: none;"
        )
        layout.addWidget(header)

        # Tree widget
        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        self._tree.setIndentation(16)
        self._tree.setStyleSheet(
            "QTreeWidget { background: #252526; color: #ddd; border: none; "
            "font-size: 11px; }"
            "QTreeWidget::item { padding: 3px 4px; }"
            "QTreeWidget::item:selected { background: #094771; }"
            "QTreeWidget::item:hover { background: #2a2d2e; }"
        )
        self._tree.currentItemChanged.connect(self._on_item_selected)
        layout.addWidget(self._tree)

        # Connect model signals
        model.structure_changed.connect(self._rebuild)
        model.selection_changed.connect(self._on_model_selection)
        model.step_changed.connect(self._on_step_changed)

        self._rebuild()

    def _rebuild(self) -> None:
        """Rebuild the tree from the model."""
        self._updating = True
        self._tree.clear()
        self._item_map.clear()

        root_item = self._build_item(self._model.root)
        self._tree.addTopLevelItem(root_item)
        root_item.setExpanded(True)
        self._expand_all(root_item)

        # Restore selection
        if self._model.selected_id and self._model.selected_id in self._item_map:
            self._tree.setCurrentItem(self._item_map[self._model.selected_id])

        self._updating = False

    def _build_item(self, node: StepNode) -> QTreeWidgetItem:
        """Recursively build tree items."""
        meta = STEP_META[node.step_type]
        item = QTreeWidgetItem([node.name])
        item.setData(0, Qt.ItemDataRole.UserRole, node.id)
        self._item_map[node.id] = item

        for child in node.children:
            child_item = self._build_item(child)
            item.addChild(child_item)

        return item

    def _expand_all(self, item: QTreeWidgetItem) -> None:
        item.setExpanded(True)
        for i in range(item.childCount()):
            self._expand_all(item.child(i))

    def _on_item_selected(
        self,
        current: Optional[QTreeWidgetItem],
        previous: Optional[QTreeWidgetItem],
    ) -> None:
        if self._updating or current is None:
            return
        step_id = current.data(0, Qt.ItemDataRole.UserRole)
        if step_id:
            self._model.select(step_id)

    def _on_model_selection(self, step_id: str) -> None:
        """Sync tree selection when model selection changes externally."""
        if step_id in self._item_map:
            self._updating = True
            self._tree.setCurrentItem(self._item_map[step_id])
            self._updating = False

    def _on_step_changed(self, step_id: str) -> None:
        """Update item label when a step is renamed."""
        if step_id in self._item_map:
            node = self._model.find_node(step_id)
            if node:
                self._item_map[step_id].setText(0, node.name)
