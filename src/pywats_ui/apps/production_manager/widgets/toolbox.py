"""Step toolbox panel for the Sequence Designer.

Lists all available step types that can be dragged onto the canvas.
Mirrors the Toolbox panel in the WATS Sequence Designer.
"""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QByteArray, QMimeData, Qt
from PySide6.QtGui import QDrag, QFont, QMouseEvent, QPixmap, QPainter, QColor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..models import STEP_META, StepType


class ToolboxItem(QFrame):
    """A single draggable step type in the toolbox."""

    def __init__(self, step_type: StepType, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.step_type = step_type
        meta = STEP_META[step_type]

        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setStyleSheet(
            "ToolboxItem { background: #2d2d2d; border: 1px solid #444; "
            "border-radius: 3px; padding: 4px; }"
            "ToolboxItem:hover { background: #3a3a3a; border-color: #666; }"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        # Color swatch
        swatch = QFrame()
        swatch.setFixedSize(14, 14)
        swatch.setStyleSheet(
            f"background: {meta['color']}; border: 1px solid #888; border-radius: 2px;"
        )
        layout.addWidget(swatch)

        # Label
        label = QLabel(meta["label"])
        label.setStyleSheet("color: #ddd; font-size: 11px; border: none;")
        layout.addWidget(label)
        layout.addStretch()

        self.setFixedHeight(32)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return

        drag = QDrag(self)
        mime = QMimeData()
        mime.setData(
            "application/x-pywats-step-type",
            QByteArray(self.step_type.value.encode()),
        )
        drag.setMimeData(mime)

        # Create a small drag pixmap
        pixmap = QPixmap(120, 28)
        pixmap.fill(QColor(STEP_META[self.step_type]["color"]))
        painter = QPainter(pixmap)
        painter.setPen(QColor("#333"))
        painter.setFont(QFont("Segoe UI", 9))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, STEP_META[self.step_type]["label"])
        painter.end()
        drag.setPixmap(pixmap)

        drag.exec(Qt.DropAction.CopyAction)


class StepToolbox(QFrame):
    """Right-side toolbox listing available step types.

    Steps can be dragged from here onto the FlowCanvas, or
    double-clicked to append to the current selection.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(180)
        self.setMaximumWidth(220)
        self.setStyleSheet(
            "StepToolbox { background: #252526; border-left: 1px solid #333; }"
        )

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Header
        header = QLabel("  Toolbox")
        header.setFixedHeight(32)
        header.setStyleSheet(
            "background: #333; color: #ccc; font-weight: bold; "
            "font-size: 12px; padding-left: 8px; border: none;"
        )
        outer.addWidget(header)

        # Search filter
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search…")
        self._search.setStyleSheet(
            "QLineEdit { background: #3c3c3c; color: #ddd; border: 1px solid #555; "
            "border-radius: 3px; padding: 4px 8px; margin: 6px; }"
        )
        self._search.textChanged.connect(self._filter_items)
        outer.addWidget(self._search)

        # Category label
        cat_label = QLabel("  Step")
        cat_label.setStyleSheet(
            "color: #aaa; font-size: 10px; font-weight: bold; "
            "padding: 4px 8px; border: none;"
        )
        outer.addWidget(cat_label)

        # Scrollable item list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self._item_container = QWidget()
        self._item_layout = QVBoxLayout(self._item_container)
        self._item_layout.setContentsMargins(6, 0, 6, 6)
        self._item_layout.setSpacing(2)

        # Add all step types
        self._items: list[ToolboxItem] = []
        for st in StepType:
            item = ToolboxItem(st)
            self._items.append(item)
            self._item_layout.addWidget(item)

        self._item_layout.addStretch()
        scroll.setWidget(self._item_container)
        outer.addWidget(scroll)

    def _filter_items(self, text: str) -> None:
        """Show/hide toolbox items based on search text."""
        needle = text.lower()
        for item in self._items:
            label = STEP_META[item.step_type]["label"].lower()
            item.setVisible(needle in label)
