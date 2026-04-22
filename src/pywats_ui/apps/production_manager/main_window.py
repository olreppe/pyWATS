"""Main window for the pyWATS Production Manager.

Layout mirrors the WATS Production Manager:
- Header: App title + entity count
- Left: Definition tree (server-loaded folder/definition list)
- Right: Tabbed detail panel
  - Sequence overview: metadata + options form
  - Sequence designer: embedded flow editor with hideable panels
  - Relations: relation table with CRUD
  - Instructions (PDF): attached documents list
"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent, QKeySequence
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from .models import SequenceModel, parse_xaml
from .server_bridge import ServerBridge
from .widgets.definition_tree import DefinitionTree
from .widgets.designer_tab import DesignerTab
from .widgets.instructions_tab import InstructionsTab
from .widgets.overview_tab import OverviewTab
from .widgets.relations_tab import RelationsTab
from .widgets.test_tab import TestTab

logger = logging.getLogger(__name__)


class ConnectDialog(QDialog):
    """Simple dialog to enter server URL and auth token."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Connect to WATS Server")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://your-instance.wats.com")
        form.addRow("Server URL:", self.url_edit)

        self.token_edit = QLineEdit()
        self.token_edit.setPlaceholderText("Base64 auth token")
        self.token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Token:", self.token_edit)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        connect_btn = QPushButton("Connect")
        connect_btn.setDefault(True)
        connect_btn.clicked.connect(self.accept)
        btn_layout.addWidget(connect_btn)
        layout.addLayout(btn_layout)

        self.setStyleSheet(
            "QDialog { background: #2d2d2d; }"
            "QLabel { color: #ddd; }"
            "QLineEdit { background: #333; color: #ddd; border: 1px solid #555;"
            " padding: 6px; border-radius: 3px; }"
            "QPushButton { color: #ddd; padding: 6px 16px; border-radius: 3px;"
            " background: #094771; border: 1px solid #1177bb; }"
            "QPushButton:hover { background: #0a5a8a; }"
        )


class ProductionManagerWindow(QMainWindow):
    """Main Production Manager window.

    Left: server definition tree. Right: tabbed detail panels
    (overview, designer, relations, instructions).
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("pyWATS — Production Manager")
        self.resize(1400, 900)

        self._bridge = ServerBridge(self)
        self._current_definition: Optional[Dict[str, Any]] = None
        self._current_model: Optional[SequenceModel] = None

        self._setup_ui()
        self._setup_toolbar()
        self._setup_menu_bar()
        self._setup_status_bar()
        self._connect_signals()

        # Auto-connect on startup
        self._try_auto_connect()

    # -----------------------------------------------------------------
    # UI setup
    # -----------------------------------------------------------------

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Header bar (app title + entity count) ---
        header = QWidget()
        header.setFixedHeight(40)
        header.setStyleSheet("background: #1e1e1e; border-bottom: 1px solid #333;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 8, 16, 8)
        header_layout.setSpacing(8)

        title_label = QLabel("Production manager")
        title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #ddd;"
        )
        header_layout.addWidget(title_label)

        self._entity_count_label = QLabel()
        self._entity_count_label.setStyleSheet(
            "font-size: 12px; color: #888;"
        )
        header_layout.addWidget(self._entity_count_label)
        header_layout.addStretch()

        main_layout.addWidget(header)

        # --- Splitter (left tree + right tabs) ---
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left: Definition tree
        self._def_tree = DefinitionTree(self._bridge)
        self._def_tree.setMinimumWidth(250)

        # Right: Tab widget
        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(
            "QTabWidget::pane { border: none; background: #1e1e1e; }"
            "QTabBar::tab { background: #2d2d2d; color: #aaa;"
            " padding: 8px 20px; border: none;"
            " border-bottom: 2px solid transparent; }"
            "QTabBar::tab:selected { color: #ddd;"
            " border-bottom: 2px solid #1177bb; }"
            "QTabBar::tab:hover { color: #ddd; background: #333; }"
        )

        self._overview_tab = OverviewTab()
        self._designer_tab = DesignerTab()
        self._relations_tab = RelationsTab(self._bridge)
        self._instructions_tab = InstructionsTab(self._bridge)
        self._test_tab = TestTab(bridge=self._bridge)

        self._tabs.addTab(self._overview_tab, "Sequence overview")
        self._tabs.addTab(self._designer_tab, "Sequence designer")
        self._tabs.addTab(self._relations_tab, "Relations")
        self._tabs.addTab(self._instructions_tab, "Instructions (PDF)")
        self._tabs.addTab(self._test_tab, "Test")

        splitter.addWidget(self._def_tree)
        splitter.addWidget(self._tabs)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([300, 1100])

        main_layout.addWidget(splitter)

    def _setup_toolbar(self) -> None:
        toolbar = QToolBar("Production Manager")
        toolbar.setMovable(False)
        toolbar.setStyleSheet(
            "QToolBar { background: #2d2d2d; border-bottom: 1px solid #444;"
            " spacing: 4px; padding: 2px 8px; }"
            "QToolButton { color: #ddd; padding: 4px 10px; border-radius: 3px; }"
            "QToolButton:hover { background: #3a3a3a; }"
            "QToolButton:disabled { color: #666; }"
        )

        # --- Connection actions ---
        self._act_connect = QAction("Connect…", self)
        self._act_connect.triggered.connect(self._on_connect)
        toolbar.addAction(self._act_connect)

        self._act_refresh = QAction("Refresh", self)
        self._act_refresh.setShortcut(QKeySequence("F5"))
        self._act_refresh.triggered.connect(self._on_refresh)
        toolbar.addAction(self._act_refresh)

        toolbar.addSeparator()

        # --- Definition actions (match WATS Production Manager) ---
        self._act_new = QAction("+ New…", self)
        self._act_new.setShortcut(QKeySequence.StandardKey.New)
        self._act_new.triggered.connect(self._on_new)
        toolbar.addAction(self._act_new)

        self._act_copy = QAction("Copy", self)
        self._act_copy.triggered.connect(self._on_copy)
        self._act_copy.setEnabled(False)
        toolbar.addAction(self._act_copy)

        toolbar.addSeparator()

        self._act_move_draft = QAction("Move to draft", self)
        self._act_move_draft.triggered.connect(self._on_move_to_draft)
        self._act_move_draft.setEnabled(False)
        toolbar.addAction(self._act_move_draft)

        self._act_move_pending = QAction("Move to pending", self)
        self._act_move_pending.triggered.connect(self._on_move_to_pending)
        self._act_move_pending.setEnabled(False)
        toolbar.addAction(self._act_move_pending)

        self._act_release = QAction("Release", self)
        self._act_release.triggered.connect(self._on_release)
        self._act_release.setEnabled(False)
        toolbar.addAction(self._act_release)

        toolbar.addSeparator()

        self._act_delete = QAction("Delete", self)
        self._act_delete.setShortcut(QKeySequence("Delete"))
        self._act_delete.triggered.connect(self._on_delete)
        self._act_delete.setEnabled(False)
        toolbar.addAction(self._act_delete)

        self._act_revoke = QAction("Revoke", self)
        self._act_revoke.triggered.connect(self._on_revoke)
        self._act_revoke.setEnabled(False)
        toolbar.addAction(self._act_revoke)

        self.addToolBar(toolbar)

    def _setup_menu_bar(self) -> None:
        menubar = self.menuBar()

        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self._act_connect)
        file_menu.addAction(self._act_refresh)
        file_menu.addSeparator()
        file_menu.addAction(self._act_new)
        file_menu.addAction(self._act_copy)
        file_menu.addSeparator()
        file_menu.addAction(self._act_delete)
        file_menu.addSeparator()

        exit_action = file_menu.addAction("E&xit")
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)

        definition_menu = menubar.addMenu("&Definition")
        definition_menu.addAction(self._act_move_draft)
        definition_menu.addAction(self._act_move_pending)
        definition_menu.addAction(self._act_release)
        definition_menu.addSeparator()
        definition_menu.addAction(self._act_revoke)

        help_menu = menubar.addMenu("&Help")
        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(self._on_about)

    def _setup_status_bar(self) -> None:
        self._status = QStatusBar()
        self._status.setStyleSheet(
            "QStatusBar { background: #1e1e1e; color: #888; font-size: 11px; }"
        )
        self.setStatusBar(self._status)
        self._status.showMessage("Connecting...")

    # -----------------------------------------------------------------
    # Signal wiring
    # -----------------------------------------------------------------

    def _connect_signals(self) -> None:
        self._def_tree.definition_selected.connect(self._on_definition_selected)
        self._bridge.definitions_loaded.connect(self._on_definitions_count)
        self._bridge.definition_loaded.connect(self._on_definition_detail_loaded)
        self._bridge.xaml_loaded.connect(self._on_xaml_loaded)
        self._bridge.error_occurred.connect(self._on_error)
        self._bridge.connected.connect(self._on_connected)
        self._bridge.definition_copied.connect(self._on_definition_copied)
        self._bridge.definition_updated.connect(self._on_definition_updated)

    # -----------------------------------------------------------------
    # Auto-connect
    # -----------------------------------------------------------------

    def _try_auto_connect(self) -> None:
        """Attempt auto-discovery from installed pyWATS API."""
        if self._bridge.auto_connect():
            # auto_connect fires connected signal, which triggers _on_connected
            pass
        else:
            self._status.showMessage(
                "Not connected — use Connect to enter server details"
            )

    def _on_connected(self, base_url: str) -> None:
        """Called when the bridge successfully connects (auto or manual)."""
        self._status.showMessage(f"Connected to {base_url}")
        self._def_tree.refresh()

    def _on_definitions_count(self, definitions: list) -> None:
        """Update entity count in header when definitions are loaded."""
        count = len(definitions)
        self._entity_count_label.setText(f"{count} entities")

    # -----------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------

    def _on_connect(self) -> None:
        dlg = ConnectDialog(self)
        # Pre-fill with current values if available
        if self._bridge.base_url:
            dlg.url_edit.setText(self._bridge.base_url)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            url = dlg.url_edit.text().strip()
            token = dlg.token_edit.text().strip()
            if not url or not token:
                QMessageBox.warning(self, "Invalid", "URL and token are required.")
                return
            self._bridge.configure(url, token)
            self._def_tree.refresh()

    def _on_refresh(self) -> None:
        if not self._bridge.is_configured:
            QMessageBox.information(
                self, "Not Connected",
                "Connect to a WATS server first.",
            )
            return
        self._def_tree.refresh()

    def _on_new(self) -> None:
        """Create a new empty sequence for editing."""
        model = SequenceModel(name="New Sequence")
        self._current_model = model
        self._current_definition = {
            "Name": "New Sequence",
            "Status": 0,
            "Version": 1,
        }
        self._overview_tab.load_definition(self._current_definition)
        self._designer_tab.load_model(model)
        self._relations_tab.clear()
        self._instructions_tab.clear()
        self._tabs.setCurrentWidget(self._designer_tab)
        self._update_toolbar_state()

    def _on_copy(self) -> None:
        """Copy the currently selected definition."""
        if not self._current_definition:
            return
        def_id = str(self._current_definition.get("TestSequenceDefinitionId", ""))
        if not def_id:
            return
        name = self._current_definition.get("Name", "")
        reply = QMessageBox.question(
            self, "Copy Definition",
            f'Create a copy of "{name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._bridge.copy_definition(def_id)

    def _on_move_to_draft(self) -> None:
        """Move the selected definition back to Draft status."""
        self._change_status(0, "Move to Draft",
                            "Move this definition back to Draft?")

    def _on_move_to_pending(self) -> None:
        """Move the selected definition to Pending status."""
        self._change_status(1, "Move to Pending",
                            "Move this definition to Pending (test mode)?")

    def _on_release(self) -> None:
        """Release the selected definition."""
        name = self._current_definition.get("Name", "") if self._current_definition else ""
        reply = QMessageBox.warning(
            self, "Release Definition",
            f'Release "{name}"?\n\n'
            "Released definitions are immutable. Any previously released\n"
            "version with the same name will be automatically revoked.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._change_status_impl(2)

    def _on_delete(self) -> None:
        """Delete (revoke) a Draft or Pending definition."""
        name = self._current_definition.get("Name", "") if self._current_definition else ""
        reply = QMessageBox.warning(
            self, "Delete Definition",
            f'Delete "{name}"?\n\nThis will revoke the definition.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._change_status_impl(3)

    def _on_revoke(self) -> None:
        """Revoke a Released definition."""
        name = self._current_definition.get("Name", "") if self._current_definition else ""
        reply = QMessageBox.warning(
            self, "Revoke Definition",
            f'Revoke "{name}"?\n\nThis cannot be undone.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._change_status_impl(3)

    def _change_status(self, new_status: int, title: str, message: str) -> None:
        """Show confirmation and change definition status."""
        if not self._current_definition:
            return
        reply = QMessageBox.question(
            self, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._change_status_impl(new_status)

    def _change_status_impl(self, new_status: int) -> None:
        """Execute a status change on the current definition."""
        if not self._current_definition:
            return
        def_id = str(self._current_definition.get("TestSequenceDefinitionId", ""))
        if def_id:
            self._bridge.update_definition_status(
                def_id, new_status, self._current_definition)

    # -----------------------------------------------------------------
    # Toolbar state management
    # -----------------------------------------------------------------

    def _update_toolbar_state(self) -> None:
        """Enable/disable toolbar actions based on current definition status."""
        if not self._current_definition:
            self._act_copy.setEnabled(False)
            self._act_move_draft.setEnabled(False)
            self._act_move_pending.setEnabled(False)
            self._act_release.setEnabled(False)
            self._act_delete.setEnabled(False)
            self._act_revoke.setEnabled(False)
            return

        status = self._current_definition.get("Status", -1)

        # Copy is always available when a definition is selected
        self._act_copy.setEnabled(True)

        # State transitions per the lifecycle
        self._act_move_draft.setEnabled(status == 1)     # Pending → Draft
        self._act_move_pending.setEnabled(status == 0)    # Draft → Pending
        self._act_release.setEnabled(status == 1)         # Pending → Released
        self._act_delete.setEnabled(status in (0, 1))     # Draft/Pending → Revoked
        self._act_revoke.setEnabled(status == 2)          # Released → Revoked

    def _on_definition_selected(self, defn: Dict[str, Any]) -> None:
        """User clicked a definition in the tree."""
        self._current_definition = defn
        def_id = str(defn.get("TestSequenceDefinitionId", ""))

        # Load overview immediately from tree data
        self._overview_tab.load_definition(defn)

        # Request full detail + XAML + relations + documents from server
        if def_id:
            self._bridge.load_definition(def_id)
            self._bridge.load_xaml(def_id)
            self._relations_tab.load_relations(def_id)
            self._instructions_tab.load_documents(def_id)

        name = defn.get("Name", "")
        status_code = defn.get("Status", 0)
        status_text = {0: "Draft", 1: "Pending", 2: "Released", 3: "Revoked"}.get(
            status_code, str(status_code)
        )
        self._status.showMessage(f"{name}  |  v{defn.get('Version', '?')}  |  {status_text}")
        self._update_toolbar_state()

    def _on_definition_detail_loaded(self, defn: Dict[str, Any]) -> None:
        """Full definition detail arrived from server."""
        if defn:
            self._current_definition = defn
            self._overview_tab.load_definition(defn)
            self._update_toolbar_state()

    def _on_definition_copied(self, defn: Dict[str, Any]) -> None:
        """A definition was successfully copied — refresh the tree."""
        name = defn.get("Name", "Copy")
        self._status.showMessage(f"Copied: {name}")
        self._def_tree.refresh()

    def _on_definition_updated(self, defn: Dict[str, Any]) -> None:
        """A definition status was changed — refresh the tree."""
        status_code = defn.get("Status", 0)
        status_text = {0: "Draft", 1: "Pending", 2: "Released", 3: "Revoked"}.get(
            status_code, str(status_code)
        )
        name = defn.get("Name", "")
        self._status.showMessage(f"{name} → {status_text}")
        self._current_definition = defn
        self._overview_tab.load_definition(defn)
        self._update_toolbar_state()
        self._def_tree.refresh()

    def _on_xaml_loaded(self, xaml_data: Dict[str, Any]) -> None:
        """XAML content arrived — build a SequenceModel from it."""
        xaml_string = xaml_data.get("Definition", "")
        def_id = xaml_data.get("TestSequenceDefinitionId", "")

        if not xaml_string:
            self._designer_tab.clear()
            return

        # Parse XAML into a StepNode tree
        name = "Sequence"
        if self._current_definition:
            name = self._current_definition.get("Name", "Sequence")

        root_node = parse_xaml(xaml_string)

        # Handle parse failure with user feedback
        if root_node is None:
            self._designer_tab.clear()
            self._status.showMessage(
                f"Failed to parse sequence XAML for '{name}'", 5000
            )
            logger.error(
                "XAML parse failed for definition %s (%s)", def_id, name
            )
            QMessageBox.warning(
                self,
                "Parse Error",
                f"Failed to parse the sequence definition '{name}'.\n\n"
                "The XAML content may be malformed or use unsupported elements."
            )
            return

        model = SequenceModel(name=name)
        model._root = root_node
        model.definition_id = str(def_id)
        self._current_model = model

        # Connect dirty tracking to window title
        model.dirty_changed.connect(self._on_model_dirty_changed)

        self._designer_tab.load_model(model)
        if self._current_definition:
            self._test_tab.load_sequence(model, self._current_definition)

    def _on_error(self, message: str) -> None:
        self._status.showMessage(f"Error: {message}", 5000)
        logger.error("Server error: %s", message)

    def _on_model_dirty_changed(self, is_dirty: bool) -> None:
        """Update window title to show modified indicator."""
        base_title = "pyWATS — Production Manager"
        if self._current_definition:
            name = self._current_definition.get("Name", "")
            if name:
                base_title = f"{name} — pyWATS Production Manager"
        if is_dirty:
            self.setWindowTitle(f"• {base_title}")
        else:
            self.setWindowTitle(base_title)

    def _on_about(self) -> None:
        QMessageBox.about(
            self,
            "About pyWATS Production Manager",
            "pyWATS Production Manager v0.2.0\n\n"
            "Browse and edit WATS Manual Inspection sequences.\n\n"
            "Part of the pyWATS GUI framework.",
        )

    # -----------------------------------------------------------------
    # Window events
    # -----------------------------------------------------------------

    def closeEvent(self, event: QCloseEvent) -> None:
        self._bridge.shutdown()
        event.accept()
