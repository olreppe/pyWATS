"""
Converters Page

Displays and manages converter modules.
"""

import asyncio
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QListWidgetItem, QGroupBox,
    QSplitter, QTextEdit, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog, QPlainTextEdit
)
from PySide6.QtCore import Qt

from .base import BasePage
from ...core.config import ClientConfig

if TYPE_CHECKING:
    from ..main_window import MainWindow


class ConverterEditorDialog(QDialog):
    """Dialog for viewing/editing converter details"""
    
    def __init__(self, file_path: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.file_path = Path(file_path)
        self.setWindowTitle(f"Converter: {self.file_path.stem}")
        self.resize(800, 600)
        
        self._setup_ui()
        self._load_converter()
    
    def _setup_ui(self) -> None:
        """Setup UI components"""
        layout = QVBoxLayout(self)
        
        # File info
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel("File:"))
        self._path_label = QLabel(str(self.file_path))
        self._path_label.setStyleSheet("color: #4ec9b0;")
        info_layout.addWidget(self._path_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        self._status_label = QLabel()
        status_layout.addWidget(self._status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Code editor
        layout.addWidget(QLabel("Converter Code:"))
        self._code_editor = QPlainTextEdit()
        self._code_editor.setReadOnly(False)
        self._code_editor.setStyleSheet("""
            QPlainTextEdit {
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10pt;
                background-color: #1e1e1e;
                color: #d4d4d4;
            }
        """)
        layout.addWidget(self._code_editor)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self._save_btn = QPushButton("Save")
        self._save_btn.clicked.connect(self._save_converter)
        button_layout.addWidget(self._save_btn)
        
        self._close_btn = QPushButton("Close")
        self._close_btn.clicked.connect(self.reject)
        button_layout.addWidget(self._close_btn)
        
        layout.addLayout(button_layout)
    
    def _load_converter(self) -> None:
        """Load converter from file"""
        try:
            content = self.file_path.read_text()
            self._code_editor.setPlainText(content)
            
            # Check validity
            if "ConverterBase" in content:
                self._status_label.setText("Valid converter")
                self._status_label.setStyleSheet("color: #4ec9b0;")
            else:
                self._status_label.setText("Missing ConverterBase - not a valid converter")
                self._status_label.setStyleSheet("color: #dcdcaa;")
                
        except Exception as e:
            self._status_label.setText(f"Error loading: {str(e)}")
            self._status_label.setStyleSheet("color: #f14c4c;")
    
    def _save_converter(self) -> None:
        """Save converter to file"""
        try:
            content = self._code_editor.toPlainText()
            self.file_path.write_text(content)
            
            QMessageBox.information(
                self,
                "Saved",
                f"Converter saved to:\n{self.file_path}"
            )
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save converter:\n{str(e)}"
            )


class ConvertersPage(BasePage):
    """Converters management page"""
    
    def __init__(
        self, 
        config: ClientConfig, 
        main_window: Optional['MainWindow'] = None,
        parent: Optional[QWidget] = None
    ):
        self._main_window = main_window
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Converters"
    
    def _setup_ui(self) -> None:
        """Setup page UI with grid layout"""
        # Converters folder
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Converters folder:"))
        
        self._folder_edit = QLineEdit()
        self._folder_edit.setReadOnly(True)
        folder_layout.addWidget(self._folder_edit, 1)
        
        self._browse_btn = QPushButton("Browse...")
        self._browse_btn.clicked.connect(self._on_browse)
        folder_layout.addWidget(self._browse_btn)
        
        self._layout.addLayout(folder_layout)
        
        help_label = QLabel(
            "Place Python modules (.py files) implementing the ConverterBase interface\n"
            "in this folder. They will be automatically loaded and monitored for changes."
        )
        help_label.setStyleSheet("color: #808080; font-size: 11px;")
        self._layout.addWidget(help_label)
        
        self._layout.addSpacing(10)
        
        # Converters grid/table
        from PySide6.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
        
        self._converter_table = QTableWidget()
        self._converter_table.setColumnCount(5)
        self._converter_table.setHorizontalHeaderLabels([
            "Name", "Extensions", "Status", "Description", "File Path"
        ])
        self._converter_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self._converter_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._converter_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._converter_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self._converter_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
        self._converter_table.verticalHeader().setVisible(False)
        self._converter_table.setAlternatingRowColors(True)
        self._converter_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._converter_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._converter_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._converter_table.setColumnWidth(0, 200)
        self._converter_table.setColumnWidth(4, 300)
        self._converter_table.doubleClicked.connect(self._on_edit_converter)
        self._layout.addWidget(self._converter_table, 1)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self._refresh_btn = QPushButton("Refresh")
        self._refresh_btn.clicked.connect(self._on_refresh)
        btn_layout.addWidget(self._refresh_btn)
        
        self._create_btn = QPushButton("Create New")
        self._create_btn.clicked.connect(self._on_create_new)
        btn_layout.addWidget(self._create_btn)
        
        self._edit_btn = QPushButton("Edit/View...")
        self._edit_btn.setEnabled(False)
        self._edit_btn.clicked.connect(self._on_edit_converter)
        btn_layout.addWidget(self._edit_btn)
        
        btn_layout.addStretch()
        self._layout.addLayout(btn_layout)
        
        # Connect selection changed
        self._converter_table.itemSelectionChanged.connect(self._on_selection_changed)
    
    def save_config(self) -> None:
        """Save configuration"""
        self.config.converters_folder = self._folder_edit.text()
    
    def load_config(self) -> None:
        """Load configuration"""
        self._folder_edit.setText(self.config.converters_folder)
        self._refresh_converter_list()
    
    def _on_browse(self) -> None:
        """Browse for converters folder"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Converters Folder",
            self._folder_edit.text() or str(Path.home())
        )
        if folder:
            self._folder_edit.setText(folder)
            self._emit_changed()
            self._refresh_converter_list()
    
    def _on_refresh(self) -> None:
        """Refresh converter list"""
        self._refresh_converter_list()
        if self._main_window:
            self._main_window.refresh_converters()
    
    def _on_create_new(self) -> None:
        """Create a new converter template"""
        folder = self._folder_edit.text()
        if not folder:
            QMessageBox.warning(
                self,
                "No Folder Selected",
                "Please select a converters folder first."
            )
            return
        
        # Create template
        template = '''"""
Custom Converter Template

Implement your converter logic here.
"""

from pywats_client.converters import ConverterBase


class MyConverter(ConverterBase):
    """Example converter implementation"""
    
    @property
    def name(self) -> str:
        return "My Converter"
    
    @property
    def description(self) -> str:
        return "Converts custom log files to WATS reports"
    
    @property
    def extensions(self) -> list[str]:
        return [".log", ".txt"]
    
    async def convert(self, source_path: str) -> dict:
        """
        Convert source file to WATS report format.
        
        Args:
            source_path: Path to the source file
            
        Returns:
            Dictionary in WATS report format
        """
        # Read source file
        with open(source_path, 'r') as f:
            content = f.read()
        
        # Parse and convert to WATS format
        report = {
            "type": "Test",
            "pn": "PART-001",
            "sn": "SN-001",
            "result": "P",
            # Add your conversion logic here
        }
        
        return report
'''
        
        # Find unique filename
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        base_name = "my_converter"
        counter = 1
        while (folder_path / f"{base_name}.py").exists():
            base_name = f"my_converter_{counter}"
            counter += 1
        
        file_path = folder_path / f"{base_name}.py"
        file_path.write_text(template)
        
        QMessageBox.information(
            self,
            "Converter Created",
            f"New converter template created:\n{file_path}"
        )
        
        self._refresh_converter_list()
    
    def _refresh_converter_list(self) -> None:
        """Refresh the converter table"""
        self._converter_table.setRowCount(0)
        
        folder = self._folder_edit.text()
        if not folder:
            return
        
        folder_path = Path(folder)
        if not folder_path.exists():
            return
        
        # List Python files and populate table
        row = 0
        for py_file in folder_path.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            
            # Parse converter details
            name = py_file.stem
            extensions = ""
            status = ""
            description = ""
            
            try:
                content = py_file.read_text()
                
                # Extract description from docstring
                if '"""' in content:
                    docstring_start = content.find('"""') + 3
                    docstring_end = content.find('"""', docstring_start)
                    if docstring_end > docstring_start:
                        description = content[docstring_start:docstring_end].strip()
                        # Truncate to first line or 100 chars
                        description = description.split('\n')[0][:100]
                
                # Check validity
                if "ConverterBase" in content:
                    status = "Valid"
                else:
                    status = "Missing ConverterBase"
                
                # Extract extensions
                import re
                ext_match = re.search(r'extensions.*?\[([^\]]+)\]', content, re.DOTALL)
                if ext_match:
                    extensions = ext_match.group(1).strip().replace('"', '').replace("'", "")
                    
            except Exception as e:
                status = f"Error: {str(e)}"
            
            # Add row to table
            self._converter_table.insertRow(row)
            self._converter_table.setItem(row, 0, QTableWidgetItem(name))
            self._converter_table.setItem(row, 1, QTableWidgetItem(extensions))
            self._converter_table.setItem(row, 2, QTableWidgetItem(status))
            self._converter_table.setItem(row, 3, QTableWidgetItem(description))
            self._converter_table.setItem(row, 4, QTableWidgetItem(str(py_file)))
            
            # Store file path in row 0 data
            self._converter_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, str(py_file))
            
            row += 1
    
    def _on_selection_changed(self) -> None:
        """Handle table selection change"""
        has_selection = len(self._converter_table.selectedItems()) > 0
        self._edit_btn.setEnabled(has_selection)
    
    def _on_edit_converter(self) -> None:
        """Open editor for selected converter"""
        selected_rows = set(item.row() for item in self._converter_table.selectedItems())
        if not selected_rows:
            return
        
        row = min(selected_rows)
        name_item = self._converter_table.item(row, 0)
        if not name_item:
            return
        
        file_path = name_item.data(Qt.ItemDataRole.UserRole)
        
        # Show editor dialog
        dialog = ConverterEditorDialog(file_path, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._refresh_converter_list()
