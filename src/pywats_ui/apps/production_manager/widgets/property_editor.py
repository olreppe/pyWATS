"""Step property editor for the Sequence Designer.

When a step is selected and the properties button (…) is clicked,
this panel shows editable fields for the step's name and type-specific
properties.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ..models import STEP_META, SequenceModel, StepNode, StepType

# Comparison operators available for numeric/string limits
COMP_OPERATORS = [
    ("EQ", "Equal (==)"),
    ("NE", "Not Equal (!=)"),
    ("GT", "Greater Than (>)"),
    ("GE", "Greater or Equal (>=)"),
    ("LT", "Less Than (<)"),
    ("LE", "Less or Equal (<=)"),
    ("GELE", "Between Inclusive (>= and <=)"),
    ("GTLT", "Between Exclusive (> and <)"),
    ("GELT", "Between (>= and <)"),
    ("GTLE", "Between (> and <=)"),
]


class PropertyEditor(QFrame):
    """Bottom-docked or right-side panel for editing step properties."""

    def __init__(
        self,
        model: SequenceModel,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._model = model
        self._current_node: Optional[StepNode] = None
        self._suppress_updates = False

        self.setStyleSheet(
            "PropertyEditor { background: #1e1e1e; border-top: 1px solid #333; }"
        )

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Header
        self._header = QLabel("  Properties")
        self._header.setFixedHeight(28)
        self._header.setStyleSheet(
            "background: #333; color: #ccc; font-weight: bold; "
            "font-size: 11px; padding-left: 8px; border: none;"
        )
        outer.addWidget(self._header)

        # Scroll area for properties
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self._content = QWidget()
        self._form_layout = QFormLayout(self._content)
        self._form_layout.setContentsMargins(12, 8, 12, 8)
        self._form_layout.setSpacing(6)
        self._form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        scroll.setWidget(self._content)
        outer.addWidget(scroll)

        # Placeholder
        self._placeholder = QLabel("Select a step to edit properties")
        self._placeholder.setStyleSheet("color: #666; padding: 16px; border: none;")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._form_layout.addRow(self._placeholder)

        # Connect model signals
        model.selection_changed.connect(self._on_selection_changed)

    def show_step(self, step_id: str) -> None:
        """Populate the editor for the given step."""
        node = self._model.find_node(step_id)
        if node is None:
            self._show_placeholder()
            return

        self._current_node = node
        self._rebuild_form(node)

    def _on_selection_changed(self, step_id: str) -> None:
        if step_id:
            self.show_step(step_id)
        else:
            self._show_placeholder()

    def _show_placeholder(self) -> None:
        self._current_node = None
        self._clear_form()
        self._placeholder = QLabel("Select a step to edit properties")
        self._placeholder.setStyleSheet("color: #666; padding: 16px; border: none;")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._form_layout.addRow(self._placeholder)

    def _clear_form(self) -> None:
        while self._form_layout.count() > 0:
            item = self._form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _rebuild_form(self, node: StepNode) -> None:
        self._suppress_updates = True
        self._clear_form()

        meta = STEP_META[node.step_type]

        # Type (read-only)
        type_label = QLabel(meta["label"])
        type_label.setStyleSheet("color: #ddd; border: none;")
        self._add_row("Type", type_label)

        # Name
        name_edit = QLineEdit(node.name)
        name_edit.setStyleSheet(self._input_style())
        name_edit.textChanged.connect(
            lambda text: self._update_prop("__name__", text)
        )
        self._add_row("Name", name_edit)

        # Type-specific properties
        if node.step_type == StepType.NUMERIC_LIMIT:
            self._build_numeric_limit_props(node)
        elif node.step_type == StepType.PASS_FAIL:
            pass  # No extra properties
        elif node.step_type == StepType.STRING_VALUE:
            self._build_string_value_props(node)
        elif node.step_type == StepType.WAIT:
            self._build_wait_props(node)
        elif node.step_type == StepType.MESSAGE_BOX:
            self._build_message_box_props(node)
        elif node.step_type == StepType.SET_UNIT_PROCESS:
            self._build_set_unit_process_props(node)
        elif node.step_type == StepType.ATTACH_FILE:
            self._build_attach_file_props(node)
        elif node.step_type == StepType.GLOBAL_SEQUENCE:
            self._build_global_sequence_props(node)
        elif node.step_type == StepType.ADD_SUBUNIT:
            self._build_add_subunit_props(node)

        self._suppress_updates = False

    # -- Type-specific property builders --

    def _build_numeric_limit_props(self, node: StepNode) -> None:
        props = node.properties

        units = QLineEdit(str(props.get("units", "")))
        units.setStyleSheet(self._input_style())
        units.textChanged.connect(lambda t: self._update_prop("units", t))
        self._add_row("Units", units)

        comp = self._comp_operator_combo(props.get("comp_operator", "GELE"))
        comp.currentTextChanged.connect(
            lambda _: self._update_prop("comp_operator", comp.currentData())
        )
        self._add_row("Operator", comp)

        low = QDoubleSpinBox()
        low.setRange(-1e9, 1e9)
        low.setDecimals(6)
        low.setValue(float(props.get("low_limit", 0)))
        low.setStyleSheet(self._input_style())
        low.valueChanged.connect(lambda v: self._update_prop("low_limit", v))
        self._add_row("Low Limit", low)

        high = QDoubleSpinBox()
        high.setRange(-1e9, 1e9)
        high.setDecimals(6)
        high.setValue(float(props.get("high_limit", 0)))
        high.setStyleSheet(self._input_style())
        high.valueChanged.connect(lambda v: self._update_prop("high_limit", v))
        self._add_row("High Limit", high)

    def _build_string_value_props(self, node: StepNode) -> None:
        props = node.properties

        comp = self._comp_operator_combo(props.get("comp_operator", "EQ"))
        comp.currentTextChanged.connect(
            lambda _: self._update_prop("comp_operator", comp.currentData())
        )
        self._add_row("Operator", comp)

        limit = QLineEdit(str(props.get("string_limit", "")))
        limit.setStyleSheet(self._input_style())
        limit.textChanged.connect(lambda t: self._update_prop("string_limit", t))
        self._add_row("String Limit", limit)

    def _build_wait_props(self, node: StepNode) -> None:
        dur = QDoubleSpinBox()
        dur.setRange(0, 86400)
        dur.setDecimals(1)
        dur.setSuffix(" s")
        dur.setValue(float(node.properties.get("duration_seconds", 1.0)))
        dur.setStyleSheet(self._input_style())
        dur.valueChanged.connect(lambda v: self._update_prop("duration_seconds", v))
        self._add_row("Duration", dur)

    def _build_message_box_props(self, node: StepNode) -> None:
        props = node.properties

        title = QLineEdit(str(props.get("title", "")))
        title.setStyleSheet(self._input_style())
        title.textChanged.connect(lambda t: self._update_prop("title", t))
        self._add_row("Title", title)

        msg = QLineEdit(str(props.get("message", "")))
        msg.setStyleSheet(self._input_style())
        msg.textChanged.connect(lambda t: self._update_prop("message", t))
        self._add_row("Message", msg)

    def _build_set_unit_process_props(self, node: StepNode) -> None:
        code = QLineEdit(str(node.properties.get("process_code", "")))
        code.setStyleSheet(self._input_style())
        code.textChanged.connect(lambda t: self._update_prop("process_code", t))
        self._add_row("Process Code", code)

    def _build_attach_file_props(self, node: StepNode) -> None:
        props = node.properties

        path = QLineEdit(str(props.get("file_path", "")))
        path.setStyleSheet(self._input_style())
        path.textChanged.connect(lambda t: self._update_prop("file_path", t))
        self._add_row("File Path", path)

        desc = QLineEdit(str(props.get("description", "")))
        desc.setStyleSheet(self._input_style())
        desc.textChanged.connect(lambda t: self._update_prop("description", t))
        self._add_row("Description", desc)

    def _build_global_sequence_props(self, node: StepNode) -> None:
        props = node.properties

        name = QLineEdit(str(props.get("sequence_name", "")))
        name.setStyleSheet(self._input_style())
        name.textChanged.connect(lambda t: self._update_prop("sequence_name", t))
        self._add_row("Sequence Name", name)

        ver = QLineEdit(str(props.get("sequence_version", "")))
        ver.setStyleSheet(self._input_style())
        ver.textChanged.connect(lambda t: self._update_prop("sequence_version", t))
        self._add_row("Version", ver)

    def _build_add_subunit_props(self, node: StepNode) -> None:
        props = node.properties

        pn = QLineEdit(str(props.get("part_number", "")))
        pn.setStyleSheet(self._input_style())
        pn.textChanged.connect(lambda t: self._update_prop("part_number", t))
        self._add_row("Part Number", pn)

        src = QLineEdit(str(props.get("serial_number_source", "")))
        src.setStyleSheet(self._input_style())
        src.textChanged.connect(lambda t: self._update_prop("serial_number_source", t))
        self._add_row("S/N Source", src)

    # -- Helpers --

    def _add_row(self, label: str, widget: QWidget) -> None:
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #aaa; font-size: 11px; border: none;")
        self._form_layout.addRow(lbl, widget)

    def _comp_operator_combo(self, current: str) -> QComboBox:
        combo = QComboBox()
        combo.setStyleSheet(
            "QComboBox { background: #3c3c3c; color: #ddd; border: 1px solid #555; "
            "border-radius: 3px; padding: 3px 6px; }"
        )
        selected_index = 0
        for i, (value, display) in enumerate(COMP_OPERATORS):
            combo.addItem(display, userData=value)
            if value == current:
                selected_index = i
        combo.setCurrentIndex(selected_index)
        return combo

    def _update_prop(self, key: str, value: Any) -> None:
        if self._suppress_updates or self._current_node is None:
            return
        if key == "__name__":
            self._model.rename_step(self._current_node.id, str(value))
        else:
            self._model.update_step_properties(self._current_node.id, **{key: value})

    @staticmethod
    def _input_style() -> str:
        return (
            "QLineEdit, QDoubleSpinBox { background: #3c3c3c; color: #ddd; "
            "border: 1px solid #555; border-radius: 3px; padding: 3px 6px; }"
        )
