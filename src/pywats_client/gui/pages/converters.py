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
    QSplitter, QTextEdit, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt

from .base import BasePage
from ...core.config import ClientConfig

if TYPE_CHECKING:
    from ..main_window import MainWindow


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
        """Setup page UI"""
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
        
        # Splitter for converter list and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - converter list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        list_label = QLabel("Loaded Converters")
        list_label.setStyleSheet("font-weight: bold;")
        left_layout.addWidget(list_label)
        
        self._converter_list = QListWidget()
        self._converter_list.currentRowChanged.connect(self._on_converter_selected)
        left_layout.addWidget(self._converter_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self._refresh_btn = QPushButton("Refresh")
        self._refresh_btn.clicked.connect(self._on_refresh)
        btn_layout.addWidget(self._refresh_btn)
        
        self._create_btn = QPushButton("Create New")
        self._create_btn.clicked.connect(self._on_create_new)
        btn_layout.addWidget(self._create_btn)
        
        btn_layout.addStretch()
        left_layout.addLayout(btn_layout)
        
        splitter.addWidget(left_widget)
        
        # Right side - converter details
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        detail_label = QLabel("Converter Details")
        detail_label.setStyleSheet("font-weight: bold;")
        right_layout.addWidget(detail_label)
        
        self._detail_group = QGroupBox()
        detail_inner = QVBoxLayout(self._detail_group)
        
        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self._name_label = QLabel()
        self._name_label.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(self._name_label, 1)
        detail_inner.addLayout(name_layout)
        
        # Description
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self._desc_label = QLabel()
        self._desc_label.setWordWrap(True)
        desc_layout.addWidget(self._desc_label, 1)
        detail_inner.addLayout(desc_layout)
        
        # File path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("File:"))
        self._path_label = QLabel()
        self._path_label.setWordWrap(True)
        self._path_label.setStyleSheet("color: #808080;")
        path_layout.addWidget(self._path_label, 1)
        detail_inner.addLayout(path_layout)
        
        # Status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        self._status_label = QLabel()
        status_layout.addWidget(self._status_label, 1)
        detail_inner.addLayout(status_layout)
        
        # Extensions
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("Extensions:"))
        self._ext_label = QLabel()
        ext_layout.addWidget(self._ext_label, 1)
        detail_inner.addLayout(ext_layout)
        
        right_layout.addWidget(self._detail_group)
        
        # Log/output area
        log_label = QLabel("Converter Output")
        log_label.setStyleSheet("font-weight: bold;")
        right_layout.addWidget(log_label)
        
        self._log_text = QTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setMaximumHeight(150)
        self._log_text.setStyleSheet(
            "background-color: #1e1e1e; font-family: monospace; font-size: 11px;"
        )
        right_layout.addWidget(self._log_text)
        
        splitter.addWidget(right_widget)
        
        # Set splitter sizes
        splitter.setSizes([300, 400])
        
        self._layout.addWidget(splitter, 1)
    
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
            asyncio.create_task(self._main_window.refresh_converters())
    
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
        """Refresh the converter list"""
        self._converter_list.clear()
        self._clear_details()
        
        folder = self._folder_edit.text()
        if not folder:
            return
        
        folder_path = Path(folder)
        if not folder_path.exists():
            return
        
        # List Python files
        for py_file in folder_path.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            
            item = QListWidgetItem(py_file.stem)
            item.setData(Qt.ItemDataRole.UserRole, str(py_file))
            self._converter_list.addItem(item)
    
    def _on_converter_selected(self, row: int) -> None:
        """Handle converter selection"""
        if row < 0:
            self._clear_details()
            return
        
        item = self._converter_list.item(row)
        if not item:
            return
        
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self._show_converter_details(file_path)
    
    def _clear_details(self) -> None:
        """Clear detail display"""
        self._name_label.setText("")
        self._desc_label.setText("")
        self._path_label.setText("")
        self._status_label.setText("")
        self._ext_label.setText("")
        self._log_text.clear()
    
    def _show_converter_details(self, file_path: str) -> None:
        """Show details for a converter"""
        path = Path(file_path)
        
        self._name_label.setText(path.stem)
        self._path_label.setText(str(path))
        
        # Try to load and inspect the converter
        try:
            content = path.read_text()
            
            # Simple parsing for docstring and properties
            if '"""' in content:
                docstring_start = content.find('"""') + 3
                docstring_end = content.find('"""', docstring_start)
                if docstring_end > docstring_start:
                    desc = content[docstring_start:docstring_end].strip()
                    self._desc_label.setText(desc[:200])
            
            # Check if it contains ConverterBase
            if "ConverterBase" in content:
                self._status_label.setText("Valid converter")
                self._status_label.setStyleSheet("color: #4ec9b0;")
            else:
                self._status_label.setText("Missing ConverterBase")
                self._status_label.setStyleSheet("color: #dcdcaa;")
            
            # Try to find extensions
            import re
            ext_match = re.search(r'extensions.*?\[([^\]]+)\]', content, re.DOTALL)
            if ext_match:
                extensions = ext_match.group(1).strip()
                self._ext_label.setText(extensions)
            else:
                self._ext_label.setText("(not defined)")
                
        except Exception as e:
            self._status_label.setText(f"Error: {str(e)}")
            self._status_label.setStyleSheet("color: #f14c4c;")
    
    def append_log(self, message: str) -> None:
        """Append message to log output"""
        self._log_text.append(message)
        # Scroll to bottom
        scrollbar = self._log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
