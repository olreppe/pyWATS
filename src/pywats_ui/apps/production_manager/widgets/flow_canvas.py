"""Flow-graph canvas widget for the Sequence Designer.

Renders the sequence as a vertical flow graph where each step is a
rectangular block connected by downward arrows. Container steps
(Sequence) expand to show their children indented inside a group box.

Supports:
- Drag-and-drop from the toolbox to add steps
- Click to select
- Right-click context menu (delete, properties)
- Visual drop indicators between steps
"""
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, QMimeData, QRectF, QPointF, Signal
from PySide6.QtGui import (
    QColor,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QFont,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
    QResizeEvent,
    QWheelEvent,
)
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..models import STEP_META, SequenceModel, StepNode, StepType


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
STEP_WIDTH = 280
STEP_HEIGHT = 56
STEP_SPACING = 12
CONTAINER_PADDING = 16
ARROW_SIZE = 8
CONNECTOR_LENGTH = 24
BORDER_RADIUS = 4


class StepWidget(QFrame):
    """Visual representation of a single step node."""

    clicked = Signal(str)           # step id
    properties_requested = Signal(str)  # step id

    def __init__(self, node: StepNode, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.node = node
        self._selected = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        meta = STEP_META[self.node.step_type]
        self.setFixedWidth(STEP_WIDTH)

        # Styling
        bg = meta["color"]
        self.setStyleSheet(
            f"StepWidget {{ background: {bg}; border: 1px solid #999; "
            f"border-radius: {BORDER_RADIUS}px; }}"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 4, 4)
        layout.setSpacing(2)

        # Top row: icon label + name + properties button
        top_row = QHBoxLayout()
        top_row.setSpacing(6)

        type_label = QLabel(meta["label"])
        type_label.setStyleSheet("font-weight: bold; font-size: 11px; color: #333; border: none;")
        top_row.addWidget(type_label)

        top_row.addStretch()

        props_btn = QPushButton("…")
        props_btn.setFixedSize(22, 22)
        props_btn.setStyleSheet(
            "QPushButton { background: rgba(255,255,255,0.6); border: 1px solid #aaa; "
            "border-radius: 3px; font-weight: bold; color: #555; }"
            "QPushButton:hover { background: rgba(255,255,255,0.9); }"
        )
        props_btn.clicked.connect(lambda: self.properties_requested.emit(self.node.id))
        top_row.addWidget(props_btn)

        layout.addLayout(top_row)

        # Name row
        self._name_label = QLabel(self.node.name)
        self._name_label.setStyleSheet("font-size: 10px; color: #555; border: none;")
        layout.addWidget(self._name_label)

        self.setMinimumHeight(STEP_HEIGHT)

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        border_color = "#0078d7" if selected else "#999"
        border_width = 2 if selected else 1
        meta = STEP_META[self.node.step_type]
        bg = meta["color"]
        self.setStyleSheet(
            f"StepWidget {{ background: {bg}; border: {border_width}px solid {border_color}; "
            f"border-radius: {BORDER_RADIUS}px; }}"
        )

    def refresh_name(self) -> None:
        self._name_label.setText(self.node.name)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.node.id)
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):  # type: ignore[override]
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        props_action = menu.addAction("Properties…")
        action = menu.exec(event.globalPos())
        if action == delete_action:
            # Handled by the canvas via model
            if self.node.parent is not None:
                model = self._find_model()
                if model:
                    model.remove_step(self.node.id)
        elif action == props_action:
            self.properties_requested.emit(self.node.id)

    def _find_model(self) -> Optional[SequenceModel]:
        """Walk up widget tree to find the FlowCanvas and its model."""
        widget = self.parent()
        while widget is not None:
            if isinstance(widget, FlowCanvas):
                return widget.model
            widget = widget.parent()  # type: ignore[assignment]
        return None


class ConnectorWidget(QWidget):
    """Draws a downward arrow between two steps."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedSize(STEP_WIDTH, CONNECTOR_LENGTH)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, event):  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor("#aaa"), 1.5)
        painter.setPen(pen)

        cx = self.width() // 2
        top_y = 0
        bot_y = self.height()

        # Vertical line
        painter.drawLine(cx, top_y, cx, bot_y - ARROW_SIZE)

        # Arrowhead
        path = QPainterPath()
        path.moveTo(cx, bot_y)
        path.lineTo(cx - ARROW_SIZE // 2, bot_y - ARROW_SIZE)
        path.lineTo(cx + ARROW_SIZE // 2, bot_y - ARROW_SIZE)
        path.closeSubpath()
        painter.fillPath(path, QColor("#aaa"))

        painter.end()


class DropIndicator(QWidget):
    """Thin horizontal indicator shown during drag-and-drop."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(4)
        self.setStyleSheet("background: #0078d7; border-radius: 2px;")
        self.hide()


class ContainerWidget(QFrame):
    """Visual wrapper for a Sequence (container) step and its children."""

    def __init__(
        self,
        node: StepNode,
        canvas: FlowCanvas,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.node = node
        self._canvas = canvas
        self._setup_ui()

    def _setup_ui(self) -> None:
        meta = STEP_META[self.node.step_type]
        bg = meta["color"]
        self.setStyleSheet(
            f"ContainerWidget {{ background: {bg}; border: 2px solid #c0a050; "
            f"border-radius: 6px; }}"
        )

        outer = QVBoxLayout(self)
        outer.setContentsMargins(CONTAINER_PADDING, 8, CONTAINER_PADDING, CONTAINER_PADDING)
        outer.setSpacing(0)

        # Header: step label
        self._header = StepWidget(self.node)
        self._header.clicked.connect(lambda sid: self._canvas.model.select(sid))
        self._header.properties_requested.connect(self._canvas._on_properties_requested)
        outer.addWidget(self._header, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Children area
        self._children_layout = QVBoxLayout()
        self._children_layout.setContentsMargins(0, 0, 0, 0)
        self._children_layout.setSpacing(0)
        self._children_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        outer.addLayout(self._children_layout)

        self.setMinimumWidth(STEP_WIDTH + 2 * CONTAINER_PADDING + 4)

    def rebuild_children(self) -> None:
        """Rebuild the child widgets from the node's children list."""
        # Clear existing
        while self._children_layout.count() > 0:
            item = self._children_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for child in self.node.children:
            # Connector arrow
            conn = ConnectorWidget()
            self._children_layout.addWidget(conn, alignment=Qt.AlignmentFlag.AlignHCenter)

            if child.is_container:
                container = ContainerWidget(child, self._canvas)
                container.rebuild_children()
                self._children_layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignHCenter)
            else:
                step_w = StepWidget(child)
                step_w.clicked.connect(lambda sid: self._canvas.model.select(sid))
                step_w.properties_requested.connect(self._canvas._on_properties_requested)
                self._children_layout.addWidget(step_w, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Bottom connector drop zone
        conn = ConnectorWidget()
        self._children_layout.addWidget(conn, alignment=Qt.AlignmentFlag.AlignHCenter)


class FlowCanvas(QScrollArea):
    """Scrollable canvas that displays the sequence as a vertical flow graph.

    The canvas owns the SequenceModel and rebuilds its widget tree whenever
    the model emits ``structure_changed``.
    """

    properties_requested = Signal(str)  # step id

    def __init__(
        self,
        model: SequenceModel,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._model = model
        self.setWidgetResizable(True)
        self.setAcceptDrops(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setStyleSheet("QScrollArea { border: none; background: #fafaf0; }")

        # Inner container
        self._inner = QWidget()
        self._inner.setStyleSheet("background: #fafaf0;")
        self._layout = QVBoxLayout(self._inner)
        self._layout.setContentsMargins(40, 40, 40, 40)
        self._layout.setSpacing(0)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setWidget(self._inner)

        # Connect to model
        model.structure_changed.connect(self._rebuild)
        model.selection_changed.connect(self._on_selection_changed)
        model.step_changed.connect(self._on_step_changed)

        self._rebuild()

    @property
    def model(self) -> SequenceModel:
        return self._model

    # -- Rebuild --

    def _rebuild(self) -> None:
        """Recreate all widgets from the model."""
        # Clear
        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        root = self._model.root
        container = ContainerWidget(root, self)
        container.rebuild_children()
        self._layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignHCenter)
        self._layout.addStretch()

    def _on_selection_changed(self, step_id: str) -> None:
        """Highlight the selected step widget."""
        self._apply_selection_recursive(self._inner, step_id)

    def _apply_selection_recursive(self, widget: QWidget, step_id: str) -> None:
        if isinstance(widget, StepWidget):
            widget.set_selected(widget.node.id == step_id)
        for child in widget.findChildren(QWidget):
            if isinstance(child, StepWidget):
                child.set_selected(child.node.id == step_id)

    def _on_step_changed(self, step_id: str) -> None:
        """Refresh the label of a changed step."""
        for sw in self._inner.findChildren(StepWidget):
            if sw.node.id == step_id:
                sw.refresh_name()

    def _on_properties_requested(self, step_id: str) -> None:
        self.properties_requested.emit(step_id)

    # -- Drag & Drop --

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasFormat("application/x-pywats-step-type"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasFormat("application/x-pywats-step-type"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        mime = event.mimeData()
        if not mime.hasFormat("application/x-pywats-step-type"):
            event.ignore()
            return

        step_type_str = bytes(mime.data("application/x-pywats-step-type")).decode()
        try:
            step_type = StepType(step_type_str)
        except ValueError:
            event.ignore()
            return

        # Determine drop target: find the nearest container
        target_id: Optional[str] = None
        selected = self._model.selected_node()
        if selected is not None:
            if selected.is_container:
                target_id = selected.id
            elif selected.parent is not None:
                target_id = selected.parent.id

        self._model.add_step(step_type, parent_id=target_id)
        event.acceptProposedAction()
