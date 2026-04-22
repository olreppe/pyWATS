"""Test execution tab.

Operator interface for executing Manual Inspection sequences.
Layout mirrors the WATS MI execution view:
- Top: Unit identification bar (serial, part number, revision, etc.)
- Left: Step list with status indicators
- Center: Step input area (Header/Step/Barcodes tabs)
- Right: Documentation panel (attached PDFs)
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..models import SequenceModel, StepNode, StepType, STEP_META

logger = logging.getLogger(__name__)

# Status badge styles
_BADGE_STYLES = {
    "none": "",
    "passed": (
        "background: #5cb85c; color: #fff; padding: 1px 6px;"
        " border-radius: 3px; font-size: 11px; font-weight: bold;"
    ),
    "failed": (
        "background: #d9534f; color: #fff; padding: 1px 6px;"
        " border-radius: 3px; font-size: 11px; font-weight: bold;"
    ),
}


class _UnitBar(QWidget):
    """Top bar with unit identification fields."""

    apply_clicked = Signal()
    clear_clicked = Signal()
    history_clicked = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "QWidget { background: #2d2d2d; }"
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; border-radius: 3px; }"
            "QLineEdit:read-only { background: #2a2a2a; color: #888; }"
        )
        self.setFixedHeight(44)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        self.serial_edit = QLineEdit()
        self.serial_edit.setPlaceholderText("Serial number")
        self.serial_edit.setMinimumWidth(120)
        layout.addWidget(self.serial_edit)

        self.part_edit = QLineEdit()
        self.part_edit.setPlaceholderText("Part number")
        self.part_edit.setMinimumWidth(120)
        layout.addWidget(self.part_edit)

        self.revision_edit = QLineEdit()
        self.revision_edit.setPlaceholderText("Revision")
        self.revision_edit.setReadOnly(True)
        layout.addWidget(self.revision_edit)

        self.product_edit = QLineEdit()
        self.product_edit.setPlaceholderText("Product name")
        self.product_edit.setReadOnly(True)
        layout.addWidget(self.product_edit)

        self.batch_edit = QLineEdit()
        self.batch_edit.setPlaceholderText("Batch number")
        self.batch_edit.setReadOnly(True)
        layout.addWidget(self.batch_edit)

        layout.addStretch()

        btn_style = (
            "QPushButton { color: #ddd; padding: 4px 12px; border-radius: 3px;"
            " background: #2d2d2d; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
        )

        btn_apply = QPushButton("✓ Apply")
        btn_apply.setStyleSheet(
            "QPushButton { color: #fff; padding: 4px 12px; border-radius: 3px;"
            " background: #094771; border: 1px solid #1177bb; }"
            "QPushButton:hover { background: #0a5a8a; }"
        )
        btn_apply.clicked.connect(self.apply_clicked.emit)
        layout.addWidget(btn_apply)

        btn_clear = QPushButton("✕ Clear")
        btn_clear.setStyleSheet(btn_style)
        btn_clear.clicked.connect(self.clear_clicked.emit)
        layout.addWidget(btn_clear)

        btn_history = QPushButton("⏱ History")
        btn_history.setStyleSheet(btn_style)
        btn_history.clicked.connect(self.history_clicked.emit)
        layout.addWidget(btn_history)

    def get_unit_info(self) -> Dict[str, str]:
        return {
            "serial_number": self.serial_edit.text().strip(),
            "part_number": self.part_edit.text().strip(),
            "revision": self.revision_edit.text().strip(),
            "batch_number": self.batch_edit.text().strip(),
        }

    def clear(self) -> None:
        self.serial_edit.clear()
        self.part_edit.clear()
        self.revision_edit.clear()
        self.product_edit.clear()
        self.batch_edit.clear()


class _StepList(QWidget):
    """Left panel showing sequence steps with status badges."""

    step_selected = Signal(int)  # step index
    pass_all_clicked = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.setMaximumWidth(260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header row: sequence name + Pass all
        header = QWidget()
        header.setStyleSheet("background: #2d2d2d;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(8, 6, 8, 6)
        header_layout.setSpacing(6)

        self._seq_icon = QLabel("🔧")
        header_layout.addWidget(self._seq_icon)

        self._seq_label = QLabel("Sequence")
        self._seq_label.setStyleSheet(
            "color: #ddd; font-weight: bold; font-size: 12px;"
        )
        header_layout.addWidget(self._seq_label, 1)

        self._status_badge = QLabel()
        self._status_badge.setVisible(False)
        header_layout.addWidget(self._status_badge)

        btn_pass_all = QPushButton("✓ Pass all")
        btn_pass_all.setStyleSheet(
            "QPushButton { color: #ddd; padding: 3px 10px; border-radius: 3px;"
            " background: #333; border: 1px solid #555; font-size: 11px; }"
            "QPushButton:hover { background: #3a3a3a; }"
        )
        btn_pass_all.clicked.connect(self.pass_all_clicked.emit)
        header_layout.addWidget(btn_pass_all)

        layout.addWidget(header)

        # Step list
        self._list = QListWidget()
        self._list.setStyleSheet(
            "QListWidget { background: #1e1e1e; color: #ddd; border: none;"
            " outline: none; }"
            "QListWidget::item { padding: 6px 8px; border-bottom: 1px solid #2a2a2a; }"
            "QListWidget::item:selected { background: #094771; }"
            "QListWidget::item:hover { background: #2a2d2e; }"
        )
        self._list.currentRowChanged.connect(self.step_selected.emit)
        layout.addWidget(self._list)

        self._steps: List[Dict[str, Any]] = []
        self._step_statuses: List[str] = []

    def set_sequence_name(self, name: str) -> None:
        self._seq_label.setText(name)

    def load_steps(self, steps: List[Dict[str, Any]]) -> None:
        """Load steps from step node dicts."""
        self._steps = steps
        self._step_statuses = ["none"] * len(steps)
        self._rebuild()

    def set_step_status(self, index: int, status: str) -> None:
        """Set status for a step ('none', 'passed', 'failed')."""
        if 0 <= index < len(self._step_statuses):
            self._step_statuses[index] = status
            self._rebuild()

    def pass_all(self) -> None:
        """Mark all steps as passed."""
        self._step_statuses = ["passed"] * len(self._steps)
        self._seq_status = "passed"
        self._status_badge.setText("✓ Passed")
        self._status_badge.setStyleSheet(_BADGE_STYLES["passed"])
        self._status_badge.setVisible(True)
        self._rebuild()

    def _rebuild(self) -> None:
        current = self._list.currentRow()
        self._list.clear()
        for i, step in enumerate(self._steps):
            step_type_str = step.get("type", "")
            name = step.get("name", step_type_str)
            meta = None
            for st in StepType:
                if st.value == step_type_str:
                    meta = STEP_META.get(st)
                    break

            # Build display text
            text = f"  {name}"
            item = QListWidgetItem(text)

            # Color icon based on step type
            if meta:
                color = meta.get("color", "#888")
                item.setForeground(QColor("#ddd"))
            else:
                color = "#888"

            # Status badge suffix
            status = self._step_statuses[i] if i < len(self._step_statuses) else "none"
            if status == "passed":
                item.setText(f"  {name}")
                item.setForeground(QColor("#ddd"))
            elif status == "failed":
                item.setText(f"  {name}")
                item.setForeground(QColor("#d9534f"))

            self._list.addItem(item)

        if 0 <= current < self._list.count():
            self._list.setCurrentRow(current)


class _HeaderPanel(QScrollArea):
    """Center panel for the 'Header' sub-tab — UUT/UUR general fields."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: #1e1e1e; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # -- UUT section --
        uut_label = QLabel("UUT")
        uut_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ddd;")
        layout.addWidget(uut_label)

        general_label = QLabel("General")
        general_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #ccc;")
        layout.addWidget(general_label)

        self.uut_comment = QTextEdit()
        self.uut_comment.setPlaceholderText("Comment")
        self.uut_comment.setMaximumHeight(80)
        self.uut_comment.setStyleSheet(
            "QTextEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; }"
        )
        layout.addWidget(self.uut_comment)

        # -- UUR section --
        uur_label = QLabel("UUR")
        uur_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ddd;")
        layout.addWidget(uur_label)

        process_label = QLabel("Process")
        process_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #ccc;")
        layout.addWidget(process_label)

        repair_row = QHBoxLayout()
        repair_lbl = QLabel("Repair operation:")
        repair_lbl.setStyleSheet("color: #ccc; font-weight: bold;")
        repair_row.addWidget(repair_lbl)
        self.repair_combo = QComboBox()
        self.repair_combo.setStyleSheet(
            "QComboBox { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; min-width: 200px; }"
        )
        repair_row.addWidget(self.repair_combo)
        repair_row.addStretch()
        layout.addLayout(repair_row)

        general2_label = QLabel("General")
        general2_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #ccc;")
        layout.addWidget(general2_label)

        self.uur_comment = QTextEdit()
        self.uur_comment.setPlaceholderText("UUR comment")
        self.uur_comment.setMaximumHeight(80)
        self.uur_comment.setStyleSheet(
            "QTextEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; }"
        )
        layout.addWidget(self.uur_comment)

        layout.addStretch()
        self.setWidget(content)


class _StepPanel(QScrollArea):
    """Center panel for the 'Step' sub-tab — step-specific input form."""

    # Emits (status_str, result_dict) — status is "passed"/"failed"/"skipped"
    step_result = Signal(str, dict)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setStyleSheet("QScrollArea { border: none; background: #1e1e1e; }")

        self._content = QWidget()
        self._layout = QVBoxLayout(self._content)
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(12)
        self._layout.addStretch()
        self.setWidget(self._content)

        self._current_step: Optional[Dict[str, Any]] = None
        # Tracked input widgets — set by each builder
        self._value_edit: Optional[QLineEdit] = None
        self._string_edit: Optional[QLineEdit] = None
        self._comment_edit: Optional[QTextEdit] = None
        self._subunit_pn: Optional[QLineEdit] = None
        self._subunit_sn: Optional[QLineEdit] = None
        self._attach_path: Optional[str] = None

    def _collect_result(self, status: str) -> Dict[str, Any]:
        """Gather current input values into a result dict."""
        result: Dict[str, Any] = {"status": status}
        if self._value_edit is not None:
            result["value"] = self._value_edit.text().strip()
        if self._string_edit is not None:
            result["value"] = self._string_edit.text().strip()
        if self._comment_edit is not None:
            result["comment"] = self._comment_edit.toPlainText().strip()
        if self._subunit_pn is not None:
            result["part_number"] = self._subunit_pn.text().strip()
        if self._subunit_sn is not None:
            result["serial_number"] = self._subunit_sn.text().strip()
        if self._attach_path:
            result["attach_path"] = self._attach_path
        return result

    def _emit_result(self, status: str) -> None:
        result = self._collect_result(status)
        self.step_result.emit(status, result)

    def load_step(self, step: Dict[str, Any]) -> None:
        """Build the input form for the given step."""
        self._current_step = step
        self._clear_layout()
        # Reset tracked widgets
        self._value_edit = None
        self._string_edit = None
        self._comment_edit = None
        self._subunit_pn = None
        self._subunit_sn = None
        self._attach_path = None

        step_type = step.get("type", "")
        name = step.get("name", step_type)
        props = step.get("properties", {})

        # Step header with icon
        header = QLabel(f"  {name}")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #ddd;")
        self._layout.addWidget(header)

        if step_type == "NumericLimit":
            self._build_numeric_limit(props)
        elif step_type == "PassFail":
            self._build_pass_fail(props)
        elif step_type == "StringValue":
            self._build_string_value(props)
        elif step_type == "MessageBox":
            self._build_message_box(props)
        elif step_type == "AddSubunit":
            self._build_add_subunit(props)
        elif step_type == "Wait":
            self._build_wait(props)
        elif step_type == "SetUnitProcess":
            self._build_set_unit_process(props)
        elif step_type == "AttachFile":
            self._build_attach_file(props)
        else:
            info = QLabel(f"Step type: {step_type}")
            info.setStyleSheet("color: #888;")
            self._layout.addWidget(info)

        self._layout.addStretch()

    def _build_numeric_limit(self, props: Dict[str, Any]) -> None:
        # Value input
        val_label = QLabel("Value")
        val_label.setStyleSheet("color: #ccc; font-weight: bold;")
        self._layout.addWidget(val_label)

        self._value_edit = QLineEdit()
        self._value_edit.setStyleSheet(
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 6px 8px; border-top: 2px solid #e8a218; }"
        )
        self._layout.addWidget(self._value_edit)

        # Limits info row
        low = props.get("low_limit", 0)
        high = props.get("high_limit", 0)
        comp = props.get("comp_operator", "GELE")
        units = props.get("units", "")
        limits_text = f"↓ Low limit: {low}  ↑ High limit: {high}  🔄 Comparison type: {comp}"
        if units:
            limits_text += f"  ({units})"

        limits_label = QLabel(limits_text)
        limits_label.setStyleSheet("color: #5cb85c; font-size: 12px;")
        self._layout.addWidget(limits_label)

        # Comment
        self._add_comment_field()
        # Images
        self._add_image_upload()

        # Confirm button
        self._layout.addStretch()
        self._add_confirm_button()

    def _build_pass_fail(self, props: Dict[str, Any]) -> None:
        # Comment
        self._add_comment_field()
        # Images
        self._add_image_upload()

        # Pass / Fail / Skip buttons
        self._layout.addStretch()
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        btn_pass = QPushButton("✓ Pass")
        btn_pass.setStyleSheet(
            "QPushButton { color: #fff; padding: 8px 24px; border-radius: 3px;"
            " background: #5cb85c; border: 1px solid #4cae4c; font-weight: bold;"
            " font-size: 13px; }"
            "QPushButton:hover { background: #449d44; }"
        )
        btn_pass.clicked.connect(lambda: self._emit_result("passed"))
        btn_row.addWidget(btn_pass)

        btn_fail = QPushButton("✕ Fail")
        btn_fail.setStyleSheet(
            "QPushButton { color: #fff; padding: 8px 24px; border-radius: 3px;"
            " background: #d9534f; border: 1px solid #d43f3a; font-weight: bold;"
            " font-size: 13px; }"
            "QPushButton:hover { background: #c9302c; }"
        )
        btn_fail.clicked.connect(lambda: self._emit_result("failed"))
        btn_row.addWidget(btn_fail)

        btn_skip = QPushButton("↷ Skip")
        btn_skip.setStyleSheet(
            "QPushButton { color: #ddd; padding: 8px 24px; border-radius: 3px;"
            " background: #555; border: 1px solid #666; font-weight: bold;"
            " font-size: 13px; }"
            "QPushButton:hover { background: #666; }"
        )
        btn_skip.clicked.connect(lambda: self._emit_result("skipped"))
        btn_row.addWidget(btn_skip)

        btn_row.addStretch()
        self._layout.addLayout(btn_row)

    def _build_string_value(self, props: Dict[str, Any]) -> None:
        val_label = QLabel("Value")
        val_label.setStyleSheet("color: #ccc; font-weight: bold;")
        self._layout.addWidget(val_label)

        self._string_edit = QLineEdit()
        self._string_edit.setStyleSheet(
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 6px 8px; }"
        )
        self._layout.addWidget(self._string_edit)

        comp = props.get("comp_operator", "EQ")
        limit = props.get("string_limit", "")
        if limit:
            info = QLabel(f"String limit: {limit}  Operator: {comp}")
            info.setStyleSheet("color: #888; font-size: 12px;")
            self._layout.addWidget(info)

        self._add_comment_field()
        self._add_image_upload()
        self._layout.addStretch()
        self._add_confirm_button()

    def _build_message_box(self, props: Dict[str, Any]) -> None:
        title = props.get("title", "")
        message = props.get("message", "")

        if title:
            title_lbl = QLabel(title)
            title_lbl.setStyleSheet("color: #ddd; font-size: 14px; font-weight: bold;")
            self._layout.addWidget(title_lbl)

        if message:
            msg_lbl = QLabel(message)
            msg_lbl.setStyleSheet("color: #ccc; font-size: 13px;")
            msg_lbl.setWordWrap(True)
            self._layout.addWidget(msg_lbl)

        self._layout.addStretch()
        self._add_confirm_button()

    def _build_add_subunit(self, props: Dict[str, Any]) -> None:
        pn_label = QLabel("Part number")
        pn_label.setStyleSheet("color: #ccc; font-weight: bold;")
        self._layout.addWidget(pn_label)

        self._subunit_pn = QLineEdit()
        self._subunit_pn.setText(props.get("part_number", ""))
        self._subunit_pn.setStyleSheet(
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 6px 8px; }"
        )
        self._layout.addWidget(self._subunit_pn)

        sn_label = QLabel("Serial number")
        sn_label.setStyleSheet("color: #ccc; font-weight: bold;")
        self._layout.addWidget(sn_label)

        self._subunit_sn = QLineEdit()
        self._subunit_sn.setPlaceholderText("Scan or enter serial number")
        self._subunit_sn.setStyleSheet(
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 6px 8px; }"
        )
        self._layout.addWidget(self._subunit_sn)

        self._add_comment_field()
        self._layout.addStretch()
        self._add_confirm_button()

    def _build_wait(self, props: Dict[str, Any]) -> None:
        duration = props.get("duration_seconds", 0)
        info = QLabel(f"Wait duration: {duration} seconds")
        info.setStyleSheet("color: #ccc; font-size: 13px;")
        self._layout.addWidget(info)

        self._layout.addStretch()
        self._add_confirm_button()

    def _build_set_unit_process(self, props: Dict[str, Any]) -> None:
        code = props.get("process_code", "")
        info = QLabel(f"Process code: {code}")
        info.setStyleSheet("color: #ccc; font-size: 13px;")
        self._layout.addWidget(info)

        self._layout.addStretch()
        self._add_confirm_button()

    def _build_attach_file(self, props: Dict[str, Any]) -> None:
        desc = props.get("description", "")
        if desc:
            info = QLabel(desc)
            info.setStyleSheet("color: #ccc;")
            self._layout.addWidget(info)

        path_label = QLabel("No file selected")
        path_label.setStyleSheet("color: #888; font-style: italic;")
        path_label.setWordWrap(True)

        btn = QPushButton("📎 Select file…")
        btn.setStyleSheet(
            "QPushButton { color: #ddd; padding: 6px 16px; border-radius: 3px;"
            " background: #333; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
        )

        def _pick_file() -> None:
            path, _ = QFileDialog.getOpenFileName(
                btn, "Select File to Attach", "", "All Files (*)"
            )
            if path:
                path_label.setText(path)
                path_label.setStyleSheet("color: #5cb85c;")
                # Store the path in a dynamic attribute for collect_result
                self._attach_path = path

        btn.clicked.connect(_pick_file)
        self._layout.addWidget(btn)
        self._layout.addWidget(path_label)

        self._add_comment_field()
        self._layout.addStretch()
        self._add_confirm_button()

    # -- Shared form elements --

    def _add_comment_field(self) -> None:
        lbl = QLabel("Comment")
        lbl.setStyleSheet("color: #ccc; font-weight: bold;")
        self._layout.addWidget(lbl)

        self._comment_edit = QTextEdit()
        self._comment_edit.setMaximumHeight(80)
        self._comment_edit.setStyleSheet(
            "QTextEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; }"
        )
        self._layout.addWidget(self._comment_edit)

    def _add_image_upload(self) -> None:
        lbl = QLabel("Images")
        lbl.setStyleSheet("color: #ccc; font-weight: bold;")
        self._layout.addWidget(lbl)

        btn = QPushButton("📷 Upload image")
        btn.setStyleSheet(
            "QPushButton { color: #ddd; padding: 6px 16px; border-radius: 3px;"
            " background: #333; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
        )
        self._layout.addWidget(btn)

    def _add_confirm_button(self) -> None:
        btn = QPushButton("✓ Confirm")
        btn.setStyleSheet(
            "QPushButton { color: #ddd; padding: 8px 24px; border-radius: 3px;"
            " background: #555; border: 1px solid #666; font-weight: bold;"
            " font-size: 13px; }"
            "QPushButton:hover { background: #666; }"
        )
        btn.clicked.connect(lambda: self._emit_result("passed"))
        self._layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignLeft)

    def _clear_layout(self) -> None:
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_sub_layout(item.layout())

    def _clear_sub_layout(self, layout: Any) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_sub_layout(item.layout())

    def clear(self) -> None:
        self._clear_layout()
        self._layout.addStretch()


class _DocPanel(QWidget):
    """Right panel showing attached documentation (PDFs)."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(200)
        self.setMaximumWidth(350)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        header = QLabel("Documentation")
        header.setStyleSheet(
            "font-size: 13px; font-weight: bold; color: #ddd;"
        )
        layout.addWidget(header)

        self._list = QListWidget()
        self._list.setStyleSheet(
            "QListWidget { background: #1e1e1e; color: #ddd; border: none; }"
            "QListWidget::item { padding: 4px 8px; }"
            "QListWidget::item:selected { background: #094771; }"
        )
        layout.addWidget(self._list)

        self._placeholder = QLabel("No documents attached")
        self._placeholder.setStyleSheet("color: #666; font-size: 12px;")
        self._placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._placeholder)

    def load_documents(self, documents: List[Dict[str, Any]]) -> None:
        self._list.clear()
        for doc in documents:
            name = doc.get("FileName", doc.get("Name", "Document"))
            item = QListWidgetItem(f"📄 {name}")
            self._list.addItem(item)

        has_docs = len(documents) > 0
        self._list.setVisible(has_docs)
        self._placeholder.setVisible(not has_docs)

    def clear(self) -> None:
        self._list.clear()
        self._list.setVisible(False)
        self._placeholder.setVisible(True)


class TestTab(QWidget):
    """Test execution tab for running Manual Inspection sequences.

    Layout:
    - Top: Unit identification bar
    - Below: MI title + action buttons (Submit, Save draft, Delete)
    - Main area:
      - Left: Step list with status indicators
      - Center: Step input (Header/Step/Barcodes tabs)
      - Right: Documentation panel
    """

    def __init__(self, bridge: Any = None, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._bridge = bridge
        self._model: Optional[SequenceModel] = None
        self._definition: Optional[Dict[str, Any]] = None
        self._steps: List[Dict[str, Any]] = []
        self._results: Dict[int, Dict[str, Any]] = {}  # step index → result
        self._current_step_index: int = -1
        self._setup_ui()
        self._connect_signals()

    # ----------------------------------------------------------------
    # UI setup
    # ----------------------------------------------------------------

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Unit identification bar ---
        self._unit_bar = _UnitBar()
        layout.addWidget(self._unit_bar)

        # --- MI title + action buttons ---
        title_bar = QWidget()
        title_bar.setStyleSheet("background: #1e1e1e; border-bottom: 1px solid #333;")
        title_bar.setFixedHeight(56)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(16, 8, 16, 8)
        title_layout.setSpacing(12)

        self._mi_icon = QLabel("🔒")
        self._mi_icon.setStyleSheet("font-size: 20px;")
        title_layout.addWidget(self._mi_icon)

        title_text = QVBoxLayout()
        title_text.setSpacing(0)
        self._mi_title = QLabel("Manual inspection")
        self._mi_title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #ddd;"
        )
        title_text.addWidget(self._mi_title)

        self._mi_process = QLabel("Process:")
        self._mi_process.setStyleSheet("font-size: 11px; color: #888;")
        title_text.addWidget(self._mi_process)

        title_layout.addLayout(title_text)
        title_layout.addSpacing(24)

        btn_style = (
            "QPushButton { color: #ddd; padding: 4px 14px; border-radius: 3px;"
            " background: #2d2d2d; border: 1px solid #555; }"
            "QPushButton:hover { background: #3a3a3a; }"
            "QPushButton:disabled { color: #666; }"
        )

        self._btn_submit = QPushButton("☁ Submit")
        self._btn_submit.setStyleSheet(btn_style)
        title_layout.addWidget(self._btn_submit)

        self._btn_save_draft = QPushButton("📋 Save draft")
        self._btn_save_draft.setStyleSheet(btn_style)
        title_layout.addWidget(self._btn_save_draft)

        self._last_saved = QLabel()
        self._last_saved.setStyleSheet("color: #888; font-size: 11px;")
        title_layout.addWidget(self._last_saved)

        self._btn_delete = QPushButton("🗑 Delete")
        self._btn_delete.setStyleSheet(btn_style)
        title_layout.addWidget(self._btn_delete)

        title_layout.addStretch()
        layout.addWidget(title_bar)

        # --- Main 3-column area ---
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: Step list
        self._step_list = _StepList()
        splitter.addWidget(self._step_list)

        # Center: Header/Step/Barcodes tabs
        self._center_tabs = QTabWidget()
        self._center_tabs.setStyleSheet(
            "QTabWidget::pane { border: none; background: #1e1e1e; }"
            "QTabBar::tab { background: #2d2d2d; color: #aaa;"
            " padding: 6px 16px; border: none;"
            " border-bottom: 2px solid transparent; }"
            "QTabBar::tab:selected { color: #ddd;"
            " border-bottom: 2px solid #1177bb; }"
            "QTabBar::tab:hover { color: #ddd; background: #333; }"
        )

        self._header_panel = _HeaderPanel()
        self._step_panel = _StepPanel()
        self._barcodes_panel = QWidget()  # Placeholder
        barcodes_layout = QVBoxLayout(self._barcodes_panel)
        barcodes_layout.addWidget(QLabel("Barcode scanning"))
        barcodes_layout.addStretch()

        self._center_tabs.addTab(self._header_panel, "📋 Header")
        self._center_tabs.addTab(self._step_panel, "📝 Step")
        self._center_tabs.addTab(self._barcodes_panel, "⊞ Barcodes")

        splitter.addWidget(self._center_tabs)

        # Right: Documentation panel
        self._doc_panel = _DocPanel()
        splitter.addWidget(self._doc_panel)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)
        splitter.setSizes([220, 700, 250])

        layout.addWidget(splitter)

        # --- Start Test button (shown on header, hidden once running) ---
        self._start_bar = QWidget()
        self._start_bar.setFixedHeight(52)
        self._start_bar.setStyleSheet("background: #1e1e1e; border-top: 1px solid #333;")
        start_layout = QHBoxLayout(self._start_bar)
        start_layout.setContentsMargins(16, 8, 16, 8)

        self._btn_start = QPushButton("► Start Test")
        self._btn_start.setStyleSheet(
            "QPushButton { color: #000; padding: 8px 24px; border-radius: 3px;"
            " background: #e8a218; border: 1px solid #d4940f; font-weight: bold;"
            " font-size: 14px; }"
            "QPushButton:hover { background: #d4940f; }"
        )
        self._btn_start.clicked.connect(self._on_start_test)
        start_layout.addWidget(self._btn_start)
        start_layout.addStretch()

        layout.addWidget(self._start_bar)

    def _connect_signals(self) -> None:
        self._step_list.step_selected.connect(self._on_step_selected)
        self._step_list.pass_all_clicked.connect(self._on_pass_all)
        self._unit_bar.clear_clicked.connect(self._on_clear)
        self._step_panel.step_result.connect(self._on_step_result)
        self._btn_submit.clicked.connect(self._on_submit)
        self._btn_save_draft.clicked.connect(self._on_save_draft)

    # ----------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------

    def load_sequence(self, model: SequenceModel, definition: Dict[str, Any]) -> None:
        """Load a sequence for testing."""
        self._model = model
        self._definition = definition
        self._current_step_index = -1
        self._results = {}

        # Set title info
        name = definition.get("Name", "Manual inspection")
        self._mi_title.setText(name)
        self._step_list.set_sequence_name(name)

        # Flatten step tree into a list, recursing into sub-sequences
        self._steps = []
        if model and model.root:
            self._flatten_steps(model.root)

        self._step_list.load_steps(self._steps)

        # Show header tab initially
        self._center_tabs.setCurrentIndex(0)
        self._start_bar.setVisible(True)

    def _flatten_steps(self, node: Any) -> None:
        """Recursively flatten step tree into self._steps."""
        from ..models import StepType
        for child in node.children:
            d = child.to_dict()
            if child.step_type == StepType.SEQUENCE:
                # Add a group header, then recurse into children
                d["_is_group"] = True
                self._steps.append(d)
                self._flatten_steps(child)
            else:
                self._steps.append(d)

    def clear(self) -> None:
        """Reset the test tab."""
        self._model = None
        self._definition = None
        self._steps = []
        self._results = {}
        self._step_list.load_steps([])
        self._step_panel.clear()
        self._doc_panel.clear()
        self._unit_bar.clear()
        self._start_bar.setVisible(True)

    # ----------------------------------------------------------------
    # Actions
    # ----------------------------------------------------------------

    def _on_start_test(self) -> None:
        """Start the test execution — switch to Step tab."""
        if not self._steps:
            return
        self._results = {}
        self._start_bar.setVisible(False)
        self._center_tabs.setCurrentIndex(1)  # Switch to Step tab
        self._step_list._list.setCurrentRow(0)

    def _on_step_selected(self, index: int) -> None:
        """User selected a step in the list."""
        if 0 <= index < len(self._steps):
            self._current_step_index = index
            self._step_panel.load_step(self._steps[index])
            # Restore previously entered values if revisiting
            prev = self._results.get(index)
            if prev:
                self._restore_values(prev)
            self._center_tabs.setCurrentIndex(1)

    def _restore_values(self, result: Dict[str, Any]) -> None:
        """Restore previously entered values into the step panel."""
        if self._step_panel._value_edit and "value" in result:
            self._step_panel._value_edit.setText(str(result["value"]))
        if self._step_panel._string_edit and "value" in result:
            self._step_panel._string_edit.setText(str(result["value"]))
        if self._step_panel._comment_edit and "comment" in result:
            self._step_panel._comment_edit.setPlainText(result["comment"])
        if self._step_panel._subunit_pn and "part_number" in result:
            self._step_panel._subunit_pn.setText(result["part_number"])
        if self._step_panel._subunit_sn and "serial_number" in result:
            self._step_panel._subunit_sn.setText(result["serial_number"])
        if "attach_path" in result:
            self._step_panel._attach_path = result["attach_path"]

    def _on_step_result(self, status: str, result: Dict[str, Any]) -> None:
        """A step was completed with a status and collected values."""
        if self._current_step_index < 0:
            return
        # Store result
        self._results[self._current_step_index] = result
        # Update step list badge
        self._step_list.set_step_status(self._current_step_index, status)
        self._advance_to_next()

    def _on_pass_all(self) -> None:
        """Mark all steps as passed (with confirmation)."""
        from PySide6.QtWidgets import QMessageBox

        if not self._steps:
            return

        # Count actual test steps (not group headers)
        step_count = sum(1 for s in self._steps if not s.get("_is_group"))
        reply = QMessageBox.question(
            self,
            "Pass All Steps",
            f"Mark all {step_count} steps as passed?\n\n"
            "This will skip manual verification of each step.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        for i, step in enumerate(self._steps):
            if not step.get("_is_group"):
                self._results[i] = {"status": "passed"}
        self._step_list.pass_all()

    def _on_clear(self) -> None:
        """Clear unit fields."""
        self._unit_bar.clear()

    def _advance_to_next(self) -> None:
        """Move to the next step, or show completion."""
        next_idx = self._current_step_index + 1
        # Skip group headers
        while next_idx < len(self._steps) and self._steps[next_idx].get("_is_group"):
            self._results[next_idx] = {"status": "passed"}
            self._step_list.set_step_status(next_idx, "passed")
            next_idx += 1

        if next_idx < len(self._steps):
            self._step_list._list.setCurrentRow(next_idx)
        else:
            # All steps complete
            self._step_panel.clear()
            done = QLabel("✓ All steps completed — click Submit to send the report")
            done.setStyleSheet(
                "font-size: 16px; font-weight: bold; color: #5cb85c;"
            )
            self._step_panel._layout.insertWidget(0, done,
                                                   alignment=Qt.AlignmentFlag.AlignCenter)

    # ----------------------------------------------------------------
    # Report building and submission
    # ----------------------------------------------------------------

    def _build_report(self) -> Any:
        """Build a UUTReport from collected step results."""
        from datetime import datetime
        from pywats.models import UUTReport
        from pywats.domains.report.report_models.uut.uut_info import UUTInfo
        from pywats.shared.enums import CompOp

        unit = self._unit_bar.get_unit_info()
        sn = unit.get("serial_number", "")
        pn = unit.get("part_number", "")
        rev = unit.get("revision", "A")

        if not sn:
            sn = "MANUAL-" + datetime.now().strftime("%Y%m%d%H%M%S")
        if not pn and self._definition:
            pn = self._definition.get("Name", "MI")

        # Determine overall result
        has_failure = any(
            r.get("status") == "failed" for r in self._results.values()
        )
        overall = "Failed" if has_failure else "Passed"

        report = UUTReport(
            pn=pn,
            sn=sn,
            rev=rev or "A",
            result=overall,
            start=datetime.now(),
            process_code=10,
            station_name="pyWATS Production Manager",
            location="pyWATS",
            purpose="Production",
        )

        # Set operator info (required "uut" field in WSJF JSON)
        report.info = UUTInfo(operator="pyWATS")

        # Use the factory method to get the root sequence (sets name correctly)
        root = report.get_root_sequence_call()

        # Add comment from header panel
        uut_comment = self._header_panel.uut_comment.toPlainText().strip()
        if uut_comment:
            root.report_text = uut_comment

        # Map CompOp strings
        _COMP_MAP = {
            "GELE": CompOp.GELE,
            "GELT": CompOp.GELT,
            "GTLE": CompOp.GTLE,
            "GTLT": CompOp.GTLT,
            "EQ": CompOp.EQ,
            "NE": CompOp.NE,
            "LOG": CompOp.LOG,
        }

        # Add steps to the report
        for i, step in enumerate(self._steps):
            result = self._results.get(i, {})
            status_str = result.get("status", "skipped")
            step_type = step.get("type", "")
            step_name = step.get("name", step_type)
            props = step.get("properties", {})

            if step.get("_is_group"):
                continue  # sub-sequence headers are structural only

            # Map status string to WATS StepStatus
            status_map = {"passed": "P", "failed": "F", "skipped": "S"}
            wats_status = status_map.get(status_str, "S")
            comment = result.get("comment", "").strip() or None

            if step_type == "NumericLimit":
                value_str = result.get("value", "0")
                try:
                    value = float(value_str)
                except (ValueError, TypeError):
                    value = 0.0
                comp_str = props.get("comp_operator", "GELE")
                root.add_numeric_step(
                    name=step_name,
                    value=value,
                    unit=props.get("units", "") or "NA",
                    comp_op=_COMP_MAP.get(comp_str, CompOp.GELE),
                    low_limit=props.get("low_limit"),
                    high_limit=props.get("high_limit"),
                    status=wats_status,
                    report_text=comment,
                )
            elif step_type == "PassFail":
                root.add_boolean_step(
                    name=step_name,
                    status=wats_status,
                    report_text=comment,
                )
            elif step_type == "StringValue":
                value = result.get("value", "")
                root.add_string_step(
                    name=step_name,
                    value=value,
                    limit=props.get("string_limit") or None,
                    status=wats_status,
                    report_text=comment,
                )
            elif step_type == "AddSubunit":
                sub_pn = result.get("part_number", props.get("part_number", ""))
                sub_sn = result.get("serial_number", "")
                if sub_pn and sub_sn:
                    report.add_sub_unit(
                        part_type="Component",
                        sn=sub_sn,
                        pn=sub_pn,
                        rev="",
                    )
                root.add_action_step(
                    name=step_name,
                    status=wats_status,
                    report_text=comment,
                )
            else:
                # MessageBox, Wait, AttachFile → action step
                root.add_action_step(
                    name=step_name,
                    status=wats_status,
                    report_text=comment,
                )

        return report

    def _on_submit(self) -> None:
        """Build a UUT report and submit to the server."""
        from PySide6.QtWidgets import QMessageBox

        if not self._results:
            QMessageBox.warning(
                self, "No Results",
                "No test results to submit.\n\n"
                "Run the test first by clicking 'Start Test' and completing the steps."
            )
            return

        # Validate required fields
        unit_info = self._unit_bar.get_unit_info()
        if not unit_info.get("serial_number") and not unit_info.get("part_number"):
            QMessageBox.warning(
                self, "Missing Unit Info",
                "Please enter at least a Serial Number or Part Number "
                "before submitting the report."
            )
            return

        # Check for incomplete steps
        incomplete = [
            i for i, step in enumerate(self._steps)
            if not step.get("_is_group") and i not in self._results
        ]
        if incomplete:
            reply = QMessageBox.question(
                self, "Incomplete Test",
                f"{len(incomplete)} step(s) have not been completed.\n\n"
                "Submit anyway? Incomplete steps will be marked as skipped.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            # Mark incomplete steps as skipped
            for i in incomplete:
                self._results[i] = {"status": "skipped"}
                self._step_list.set_step_status(i, "skipped")

        try:
            report = self._build_report()
        except ValueError as e:
            logger.warning("Validation error building report: %s", e)
            QMessageBox.warning(
                self, "Validation Error",
                f"Invalid input data:\n{e}\n\n"
                "Please check your entered values and try again."
            )
            return
        except Exception as e:
            logger.error("Failed to build report: %s", e, exc_info=True)
            QMessageBox.critical(
                self, "Report Error",
                f"Failed to build report:\n{e}\n\n"
                "Check the logs for more details."
            )
            return

        if self._bridge:
            self._last_saved.setText("Submitting…")
            self._btn_submit.setEnabled(False)
            self._bridge.submit_report(report)
        else:
            QMessageBox.information(
                self, "Report Built",
                f"Report built ({len(self._results)} steps) "
                "but no server connection available.\n\n"
                "Connect to a WATS server to submit the report."
            )

    def _on_save_draft(self) -> None:
        """Save results locally (placeholder)."""
        self._last_saved.setText(f"Draft saved ({len(self._results)} steps)")
