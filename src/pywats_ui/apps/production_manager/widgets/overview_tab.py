"""Sequence Overview tab.

Displays definition metadata and options in a form layout
mirroring the WATS Production Manager 'Sequence overview' tab.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)

_STATUS_LABELS = {0: "Draft", 1: "Pending", 2: "Released", 3: "Revoked"}
_STATUS_STYLES = {
    0: "background: #555; color: #ddd; padding: 2px 10px; border-radius: 3px;",
    1: "background: #f0ad4e; color: #000; padding: 2px 10px; border-radius: 3px;",
    2: "background: #5cb85c; color: #fff; padding: 2px 10px; border-radius: 3px;",
    3: "background: #d9534f; color: #fff; padding: 2px 10px; border-radius: 3px;",
}
_REPAIR_LABELS = {0: "Disabled", 1: "Optional", 2: "Required"}
_TOGGLE_ON = (
    "QLabel { background: #e8a218; color: #000; padding: 2px 8px;"
    " border-radius: 8px; font-weight: bold; }"
)
_TOGGLE_OFF = (
    "QLabel { background: #555; color: #aaa; padding: 2px 8px;"
    " border-radius: 8px; }"
)


def _toggle_label(on: bool) -> QLabel:
    """Create a styled on/off toggle indicator."""
    lbl = QLabel("ON" if on else "OFF")
    lbl.setStyleSheet(_TOGGLE_ON if on else _TOGGLE_OFF)
    lbl.setFixedWidth(40)
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return lbl


def _format_datetime(value: Any) -> str:
    """Format a datetime value for display."""
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return str(value)


class OverviewTab(QWidget):
    """Sequence overview form tab.

    Shows definition metadata (name, description, status, timestamps)
    and options (repair on failed, toggles, etc.) in a read-only form
    matching the WATS Production Manager layout.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._definition: Dict[str, Any] = {}
        self._setup_ui()

    # ----------------------------------------------------------------
    # UI setup
    # ----------------------------------------------------------------

    def _setup_ui(self) -> None:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: #1e1e1e; }"
        )

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # --- Header: "Manual inspection sequence" ---
        header = QLabel("Manual inspection sequence")
        header.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #ddd; padding: 4px 0;"
        )
        layout.addWidget(header)

        # --- Metadata form ---
        meta_group = QWidget()
        meta_layout = QFormLayout(meta_group)
        meta_layout.setSpacing(10)
        meta_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._name_edit = QLineEdit()
        self._name_edit.setReadOnly(True)
        self._name_edit.setStyleSheet(
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; }"
        )
        meta_layout.addRow(self._make_label("Name"), self._name_edit)

        self._desc_edit = QTextEdit()
        self._desc_edit.setReadOnly(True)
        self._desc_edit.setMaximumHeight(60)
        self._desc_edit.setStyleSheet(
            "QTextEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; }"
        )
        meta_layout.addRow(self._make_label("Description"), self._desc_edit)

        self._status_label = QLabel()
        meta_layout.addRow(self._make_label("Status"), self._status_label)

        self._created_label = QLabel()
        self._created_label.setStyleSheet("color: #ccc;")
        meta_layout.addRow(self._make_label("Created by (UTC)"), self._created_label)

        self._modified_label = QLabel()
        self._modified_label.setStyleSheet("color: #ccc;")
        meta_layout.addRow(self._make_label("Modified by (UTC)"), self._modified_label)

        self._released_label = QLabel()
        self._released_label.setStyleSheet("color: #ccc;")
        meta_layout.addRow(self._make_label("Released by (UTC)"), self._released_label)

        self._version_label = QLabel()
        self._version_label.setStyleSheet("color: #ccc;")
        meta_layout.addRow(self._make_label("Version"), self._version_label)

        self._global_label = QLabel()
        meta_layout.addRow(self._make_label("Global"), self._global_label)

        # Conflict warning
        self._conflict_label = QLabel()
        self._conflict_label.setStyleSheet("color: #f0ad4e; padding: 4px;")
        self._conflict_label.setWordWrap(True)
        self._conflict_label.hide()
        meta_layout.addRow("", self._conflict_label)

        layout.addWidget(meta_group)

        # --- Options group ---
        options_group = QGroupBox("Options")
        options_group.setStyleSheet(
            "QGroupBox { color: #ddd; font-weight: bold; border: 1px solid #444;"
            " border-radius: 4px; margin-top: 8px; padding-top: 16px; }"
            "QGroupBox::title { subcontrol-origin: margin;"
            " subcontrol-position: top left; padding: 0 6px; }"
        )
        options_layout = QFormLayout(options_group)
        options_layout.setSpacing(10)
        options_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._repair_combo = QComboBox()
        self._repair_combo.addItems(["Disabled", "Optional", "Required"])
        self._repair_combo.setEnabled(False)
        self._repair_combo.setStyleSheet(
            "QComboBox { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 4px 8px; }"
        )
        options_layout.addRow(self._make_label("Repair on failed"), self._repair_combo)

        # Toggle indicators
        self._toggle_display_sub = QLabel()
        options_layout.addRow(self._make_label("Display sub units grid"), self._toggle_display_sub)

        self._toggle_submit_fail = QLabel()
        options_layout.addRow(
            self._make_label("Submit UUT/UUR report on first failed test step"),
            self._toggle_submit_fail,
        )

        self._toggle_auto_create = QLabel()
        options_layout.addRow(
            self._make_label("Auto-create new manual inspection on UUT failed"),
            self._toggle_auto_create,
        )

        self._toggle_load_misc = QLabel()
        options_layout.addRow(
            self._make_label("Load UUT misc info from previous report (product)"),
            self._toggle_load_misc,
        )

        self._toggle_uur_misc = QLabel()
        options_layout.addRow(
            self._make_label("Include UUR misc info in UUT report"),
            self._toggle_uur_misc,
        )

        self._toggle_log_operator = QLabel()
        options_layout.addRow(
            self._make_label("Log operator in UUT report"),
            self._toggle_log_operator,
        )

        self._toggle_log_desc = QLabel()
        options_layout.addRow(
            self._make_label("Log step description in UUT report"),
            self._toggle_log_desc,
        )

        layout.addWidget(options_group)
        layout.addStretch()

        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    @staticmethod
    def _make_label(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #aaa; min-width: 200px;")
        return lbl

    # ----------------------------------------------------------------
    # Data binding
    # ----------------------------------------------------------------

    def load_definition(self, defn: Dict[str, Any]) -> None:
        """Populate the form from a definition dict (PascalCase keys)."""
        self._definition = defn

        self._name_edit.setText(defn.get("Name", ""))
        self._desc_edit.setPlainText(defn.get("Description") or "")

        # Status badge
        status = defn.get("Status", 0)
        self._status_label.setText(_STATUS_LABELS.get(status, str(status)))
        self._status_label.setStyleSheet(
            _STATUS_STYLES.get(status, _STATUS_STYLES[0])
        )

        # Timestamps
        created_by = defn.get("CreatedBy", "")
        created = _format_datetime(defn.get("Created"))
        self._created_label.setText(f"{created_by}, {created}" if created_by else created)

        modified_by = defn.get("ModifiedBy", "")
        modified = _format_datetime(defn.get("Modified"))
        self._modified_label.setText(f"{modified_by}, {modified}" if modified_by else modified)

        released_by = defn.get("ReleasedBy", "")
        released = _format_datetime(defn.get("Released"))
        self._released_label.setText(f"{released_by}, {released}" if released_by else released)

        self._version_label.setText(str(defn.get("Version", "")))

        is_global = defn.get("IsGlobal", False)
        self._global_label.setText("Yes" if is_global else "No")
        self._global_label.setStyleSheet(
            f"color: {'#5cb85c' if is_global else '#ccc'};"
        )

        # Options
        repair = defn.get("OnFailRequireRepair", 0)
        self._repair_combo.setCurrentIndex(min(repair, 2))

        self._set_toggle(self._toggle_display_sub, defn.get("AddChildUnits", False))
        self._set_toggle(self._toggle_submit_fail, defn.get("OnFailRequireSubmit", False))
        self._set_toggle(
            self._toggle_auto_create,
            defn.get("CreateUnsubmittedReportOnFailedStep", False),
        )
        self._set_toggle(self._toggle_load_misc, defn.get("LoadPreviousMiscInfo", False))
        self._set_toggle(self._toggle_uur_misc, defn.get("IncludeUURMiscInfoInUUT", False))
        self._set_toggle(self._toggle_log_operator, defn.get("LogOperator", False))
        self._set_toggle(self._toggle_log_desc, defn.get("LogDescription", False))

    @staticmethod
    def _set_toggle(label: QLabel, on: bool) -> None:
        label.setText("ON" if on else "OFF")
        label.setStyleSheet(_TOGGLE_ON if on else _TOGGLE_OFF)
        label.setFixedWidth(40)

    def clear(self) -> None:
        """Reset the form to empty state."""
        self._definition = {}
        self._name_edit.clear()
        self._desc_edit.clear()
        self._status_label.clear()
        self._status_label.setStyleSheet("")
        self._created_label.clear()
        self._modified_label.clear()
        self._released_label.clear()
        self._version_label.clear()
        self._global_label.clear()
        self._conflict_label.hide()
