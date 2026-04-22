"""Sequence Designer tab.

Embeds the visual flow-graph editor with hideable dock panels for
the step toolbox and property editor. Shows a read-only rendering
of the sequence when no editing is active, and switches to full
editor mode with toolbox + property panels on demand.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ..models import SequenceModel, StepType
from .flow_canvas import FlowCanvas
from .outline_tree import OutlineTree
from .property_editor import PropertyEditor
from .toolbox import StepToolbox

logger = logging.getLogger(__name__)


class DesignerTab(QWidget):
    """Sequence Designer tab with embedded editor.

    The tab always shows the flow canvas. The toolbox (right) and
    property editor (bottom) can be toggled visible/hidden.
    """

    # Emitted when step properties are requested (double-click on canvas)
    properties_requested = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._model: Optional[SequenceModel] = None
        self._editing = False
        self._setup_ui()

    # ----------------------------------------------------------------
    # UI
    # ----------------------------------------------------------------

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        self._toolbar = QToolBar()
        self._toolbar.setMovable(False)
        self._toolbar.setStyleSheet(
            "QToolBar { background: #2d2d2d; border-bottom: 1px solid #444;"
            " spacing: 4px; padding: 2px 8px; }"
            "QToolButton { color: #ddd; padding: 4px 10px; border-radius: 3px; }"
            "QToolButton:hover { background: #3a3a3a; }"
            "QPushButton { color: #ddd; padding: 4px 12px; border-radius: 3px;"
            " background: #094771; border: 1px solid #1177bb; }"
            "QPushButton:hover { background: #0a5a8a; }"
            "QPushButton:checked { background: #5cb85c; border-color: #4cae4c; }"
        )

        self._edit_btn = QPushButton("Edit")
        self._edit_btn.setCheckable(True)
        self._edit_btn.clicked.connect(self._toggle_editing)
        self._toolbar.addWidget(self._edit_btn)

        self._toolbar.addSeparator()

        self._toolbox_btn = QPushButton("Toolbox")
        self._toolbox_btn.setCheckable(True)
        self._toolbox_btn.setChecked(True)
        self._toolbox_btn.clicked.connect(self._toggle_toolbox)
        self._toolbar.addWidget(self._toolbox_btn)

        self._props_btn = QPushButton("Properties")
        self._props_btn.setCheckable(True)
        self._props_btn.setChecked(True)
        self._props_btn.clicked.connect(self._toggle_properties)
        self._toolbar.addWidget(self._props_btn)

        self._outline_btn = QPushButton("Outline")
        self._outline_btn.setCheckable(True)
        self._outline_btn.setChecked(False)
        self._outline_btn.clicked.connect(self._toggle_outline)
        self._toolbar.addWidget(self._outline_btn)

        self._toolbar.addSeparator()

        # Quick-add buttons (populated when model loaded)
        self._quick_add_actions: list = []

        layout.addWidget(self._toolbar)

        # Placeholder shown when no definition is loaded
        self._placeholder = QLabel("Select a definition to view its sequence")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._placeholder.setStyleSheet(
            "color: #666; font-size: 14px; padding: 40px;"
        )

        # Editor area
        self._editor_container = QWidget()
        editor_layout = QVBoxLayout(self._editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)

        # Horizontal splitter: outline | canvas | toolbox
        self._h_splitter = QSplitter(Qt.Orientation.Horizontal)

        self._outline: Optional[OutlineTree] = None
        self._canvas: Optional[FlowCanvas] = None
        self._toolbox: Optional[StepToolbox] = None
        self._properties: Optional[PropertyEditor] = None

        # Vertical splitter: top | property editor
        self._v_splitter = QSplitter(Qt.Orientation.Vertical)
        self._v_splitter.addWidget(self._h_splitter)

        editor_layout.addWidget(self._v_splitter)

        # Stack: placeholder vs editor
        self._editor_container.hide()
        layout.addWidget(self._placeholder)
        layout.addWidget(self._editor_container)

        # Start with editing panels hidden
        self._set_editing_panels_visible(False)

    # ----------------------------------------------------------------
    # Model binding
    # ----------------------------------------------------------------

    def load_model(self, model: SequenceModel) -> None:
        """Switch to displaying and editing the given model."""
        self._model = model

        # Rebuild editor widgets
        self._rebuild_editor()

        self._placeholder.hide()
        self._editor_container.show()

        # Default to view mode
        self._editing = False
        self._edit_btn.setChecked(False)
        self._set_editing_panels_visible(False)

    def _rebuild_editor(self) -> None:
        """Create or replace all editor widgets for the current model."""
        if self._model is None:
            return

        # Clear existing
        while self._h_splitter.count():
            w = self._h_splitter.widget(0)
            w.setParent(None)

        # Remove properties panel if present
        if self._v_splitter.count() > 1:
            w = self._v_splitter.widget(1)
            w.setParent(None)

        # Create new widgets
        self._outline = OutlineTree(self._model)
        self._canvas = FlowCanvas(self._model)
        self._toolbox = StepToolbox()

        self._h_splitter.addWidget(self._outline)
        self._h_splitter.addWidget(self._canvas)
        self._h_splitter.addWidget(self._toolbox)
        self._h_splitter.setStretchFactor(0, 0)
        self._h_splitter.setStretchFactor(1, 1)
        self._h_splitter.setStretchFactor(2, 0)
        self._h_splitter.setSizes([180, 600, 200])

        self._properties = PropertyEditor(self._model)
        self._properties.setMinimumHeight(80)
        self._properties.setMaximumHeight(300)
        self._v_splitter.addWidget(self._properties)
        self._v_splitter.setStretchFactor(0, 1)
        self._v_splitter.setStretchFactor(1, 0)
        self._v_splitter.setSizes([500, 180])

        # Connect canvas properties-requested signal
        self._canvas.properties_requested.connect(self._on_properties_requested)

        # Apply current visibility state
        self._outline.setVisible(self._outline_btn.isChecked())
        self._set_editing_panels_visible(self._editing)

        # Build quick-add buttons
        self._rebuild_quick_add()

    def _rebuild_quick_add(self) -> None:
        """Add quick-add step buttons to the toolbar."""
        from ..models import STEP_META

        # Remove old quick-add actions
        for act in self._quick_add_actions:
            self._toolbar.removeAction(act)
        self._quick_add_actions.clear()

        if self._model is None:
            return

        for st in [StepType.SEQUENCE, StepType.NUMERIC_LIMIT, StepType.PASS_FAIL,
                    StepType.STRING_VALUE, StepType.MESSAGE_BOX]:
            act = self._toolbar.addAction(f"+ {STEP_META[st]['label']}")
            act.triggered.connect(lambda checked, _st=st: self._quick_add(_st))
            act.setVisible(self._editing)
            self._quick_add_actions.append(act)

    def clear(self) -> None:
        """Reset to empty state."""
        self._model = None
        self._editor_container.hide()
        self._placeholder.show()

    # ----------------------------------------------------------------
    # Editing toggle
    # ----------------------------------------------------------------

    def _toggle_editing(self, checked: bool) -> None:
        self._editing = checked
        self._set_editing_panels_visible(checked)
        for act in self._quick_add_actions:
            act.setVisible(checked)

    def _set_editing_panels_visible(self, visible: bool) -> None:
        if self._toolbox is not None:
            self._toolbox.setVisible(visible and self._toolbox_btn.isChecked())
        if self._properties is not None:
            self._properties.setVisible(visible and self._props_btn.isChecked())

    def _toggle_toolbox(self, checked: bool) -> None:
        if self._toolbox is not None and self._editing:
            self._toolbox.setVisible(checked)

    def _toggle_properties(self, checked: bool) -> None:
        if self._properties is not None and self._editing:
            self._properties.setVisible(checked)

    def _toggle_outline(self, checked: bool) -> None:
        if self._outline is not None:
            self._outline.setVisible(checked)

    # ----------------------------------------------------------------
    # Actions
    # ----------------------------------------------------------------

    def _quick_add(self, step_type: StepType) -> None:
        if self._model is None:
            return
        parent_id = None
        selected = self._model.selected_node()
        if selected is not None:
            if selected.is_container:
                parent_id = selected.id
            elif selected.parent is not None:
                parent_id = selected.parent.id
        node = self._model.add_step(step_type, parent_id=parent_id)
        self._model.select(node.id)

    def _on_properties_requested(self, step_id: str) -> None:
        if self._model is not None:
            self._model.select(step_id)
            if self._properties is not None:
                self._properties.show_step(step_id)
