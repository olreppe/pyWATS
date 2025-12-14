"""
Product Management Page

Manage products - part numbers, revisions, BOMs, and product state.
View and create products and their revisions.

Based on the WATS Product API:
- GET /api/Products - List all products
- GET /api/Product/{partNumber} - Get product details
- POST /api/Product - Create/update product
- GET /api/Product/{partNumber}/Revisions - Get revisions
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, 
    QHeaderView, QComboBox, QMessageBox, QDialog,
    QFormLayout, QTextEdit, QDialogButtonBox, QSplitter,
    QCheckBox, QTreeWidget, QTreeWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from .base import BasePage
from ...core.config import ClientConfig

if TYPE_CHECKING:
    from ..main_window import MainWindow


class ProductDialog(QDialog):
    """Dialog for creating/editing products"""
    
    def __init__(
        self,
        product: Optional[Dict[str, Any]] = None,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.product = product
        self._setup_ui()
        if product:
            self._populate_data(product)
    
    def _setup_ui(self) -> None:
        """Setup dialog UI"""
        self.setWindowTitle("New Product" if not self.product else "Edit Product")
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        
        # Form
        form = QFormLayout()
        form.setSpacing(10)
        
        self.part_edit = QLineEdit()
        self.part_edit.setPlaceholderText("Unique part number (required)")
        form.addRow("Part Number:", self.part_edit)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Product name")
        form.addRow("Name:", self.name_edit)
        
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(80)
        self.desc_edit.setPlaceholderText("Product description")
        form.addRow("Description:", self.desc_edit)
        
        # State
        self.state_combo = QComboBox()
        self.state_combo.addItems(["Active", "New", "Engineering", "Deprecated", "Obsolete"])
        form.addRow("State:", self.state_combo)
        
        # Non-serial checkbox
        self.non_serial_cb = QCheckBox("Non-serialized product")
        self.non_serial_cb.setToolTip("Check if this product cannot have individual units (e.g., bulk materials)")
        form.addRow("", self.non_serial_cb)
        
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def _populate_data(self, product: Dict[str, Any]) -> None:
        """Populate with existing product data"""
        self.part_edit.setText(product.get('partNumber', ''))
        self.part_edit.setEnabled(False)  # Can't change part number
        self.name_edit.setText(product.get('name', ''))
        self.desc_edit.setPlainText(product.get('description', ''))
        
        # State
        state = product.get('state', 'Active')
        index = self.state_combo.findText(state)
        if index >= 0:
            self.state_combo.setCurrentIndex(index)
        
        self.non_serial_cb.setChecked(product.get('nonSerial', False))
    
    def _validate_and_accept(self) -> None:
        """Validate input"""
        if not self.part_edit.text().strip():
            QMessageBox.warning(self, "Validation", "Part number is required")
            return
        self.accept()
    
    def get_data(self) -> Dict[str, Any]:
        """Get product data"""
        return {
            'partNumber': self.part_edit.text().strip(),
            'name': self.name_edit.text().strip() or None,
            'description': self.desc_edit.toPlainText().strip() or None,
            'state': self.state_combo.currentText(),
            'nonSerial': self.non_serial_cb.isChecked(),
        }


class ProductPage(BasePage):
    """Product Management page - manage products and revisions"""
    
    def __init__(
        self, 
        config: ClientConfig, 
        main_window: Optional['MainWindow'] = None,
        parent: Optional[QWidget] = None
    ):
        self._main_window = main_window
        self._products: List[Dict[str, Any]] = []
        self._selected_product: Optional[Dict[str, Any]] = None
        super().__init__(config, parent)
        self._setup_ui()
        self.load_config()
    
    @property
    def page_title(self) -> str:
        return "Products"
    
    def _setup_ui(self) -> None:
        """Setup page UI for Product Management"""
        # Toolbar
        toolbar_layout = QHBoxLayout()
        
        self._refresh_btn = QPushButton("⟳ Refresh")
        self._refresh_btn.setToolTip("Refresh products from server")
        self._refresh_btn.clicked.connect(self._on_refresh)
        toolbar_layout.addWidget(self._refresh_btn)
        
        self._add_btn = QPushButton("+ Add Product")
        self._add_btn.clicked.connect(self._on_add_product)
        toolbar_layout.addWidget(self._add_btn)
        
        toolbar_layout.addStretch()
        
        # Search
        toolbar_layout.addWidget(QLabel("Search:"))
        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText("Filter by part number or name...")
        self._search_edit.setMaximumWidth(250)
        self._search_edit.textChanged.connect(self._on_filter_changed)
        toolbar_layout.addWidget(self._search_edit)
        
        # State filter
        toolbar_layout.addWidget(QLabel("State:"))
        self._state_filter = QComboBox()
        self._state_filter.addItems(["All", "Active", "New", "Engineering", "Deprecated", "Obsolete"])
        self._state_filter.currentIndexChanged.connect(self._on_filter_changed)
        toolbar_layout.addWidget(self._state_filter)
        
        self._layout.addLayout(toolbar_layout)
        
        # Main content - splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - products table
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        table_group = QGroupBox("Products")
        table_layout = QVBoxLayout(table_group)
        
        self._products_table = QTableWidget()
        self._products_table.setColumnCount(4)
        self._products_table.setHorizontalHeaderLabels([
            "Part Number", "Name", "State", "Non-Serial"
        ])
        self._products_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self._products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._products_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._products_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self._products_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._products_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._products_table.setAlternatingRowColors(True)
        self._products_table.itemSelectionChanged.connect(self._on_selection_changed)
        self._products_table.doubleClicked.connect(self._on_edit_product)
        
        # Apply dark theme styling
        self._products_table.setStyleSheet("""
            QTableWidget {
                font-size: 11pt;
                background-color: #1e1e1e;
                alternate-background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                padding: 4px;
                border: 1px solid #3c3c3c;
                font-weight: bold;
            }
        """)
        table_layout.addWidget(self._products_table)
        
        left_layout.addWidget(table_group)
        splitter.addWidget(left_widget)
        
        # Right side - details and revisions
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Details group
        details_group = QGroupBox("Product Details")
        details_layout = QVBoxLayout(details_group)
        
        self._details_label = QLabel("Select a product to view details")
        self._details_label.setStyleSheet("color: #808080; font-style: italic;")
        self._details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._details_label.setWordWrap(True)
        details_layout.addWidget(self._details_label)
        
        # Action buttons
        action_layout = QHBoxLayout()
        
        self._edit_btn = QPushButton("Edit")
        self._edit_btn.setEnabled(False)
        self._edit_btn.clicked.connect(self._on_edit_product)
        action_layout.addWidget(self._edit_btn)
        
        action_layout.addStretch()
        details_layout.addLayout(action_layout)
        
        right_layout.addWidget(details_group)
        
        # Revisions group
        revisions_group = QGroupBox("Revisions")
        revisions_layout = QVBoxLayout(revisions_group)
        
        self._revisions_tree = QTreeWidget()
        self._revisions_tree.setColumnCount(3)
        self._revisions_tree.setHeaderLabels(["Revision", "State", "Modified"])
        self._revisions_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self._revisions_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._revisions_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._revisions_tree.setStyleSheet("""
            QTreeWidget {
                font-size: 11pt;
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                padding: 4px;
                border: 1px solid #3c3c3c;
                font-weight: bold;
            }
        """)
        revisions_layout.addWidget(self._revisions_tree)
        
        # Add revision button
        self._add_rev_btn = QPushButton("+ Add Revision")
        self._add_rev_btn.setEnabled(False)
        self._add_rev_btn.clicked.connect(self._on_add_revision)
        revisions_layout.addWidget(self._add_rev_btn)
        
        right_layout.addWidget(revisions_group)
        
        # BOM preview group
        bom_group = QGroupBox("Bill of Materials")
        bom_layout = QVBoxLayout(bom_group)
        
        self._bom_tree = QTreeWidget()
        self._bom_tree.setColumnCount(3)
        self._bom_tree.setHeaderLabels(["Part Number", "Name", "Quantity"])
        self._bom_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self._bom_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._bom_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self._bom_tree.setMaximumHeight(150)
        self._bom_tree.setStyleSheet("""
            QTreeWidget {
                font-size: 10pt;
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
            }
            QTreeWidget::item {
                padding: 2px;
            }
            QTreeWidget::item:selected {
                background-color: #0078d4;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                padding: 4px;
                border: 1px solid #3c3c3c;
                font-weight: bold;
            }
        """)
        bom_layout.addWidget(self._bom_tree)
        
        right_layout.addWidget(bom_group)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 400])
        
        self._layout.addWidget(splitter, 1)
        
        # Status label
        self._status_label = QLabel("Connect to WATS server to view products")
        self._status_label.setStyleSheet("color: #808080; font-style: italic;")
        self._layout.addWidget(self._status_label)
        
        # Auto-load if connected
        if self._main_window and self._main_window.app.wats_client:
            self._load_products()
    
    def _on_selection_changed(self) -> None:
        """Handle product selection change"""
        selected = len(self._products_table.selectedItems()) > 0
        self._edit_btn.setEnabled(selected)
        self._add_rev_btn.setEnabled(selected)
        
        if selected:
            row = self._products_table.currentRow()
            if 0 <= row < len(self._products):
                product = self._products[row]
                self._selected_product = product
                self._show_product_details(product)
        else:
            self._selected_product = None
            self._clear_details()
    
    def _show_product_details(self, product: Dict[str, Any]) -> None:
        """Display product details"""
        details = f"""
<b>Part Number:</b> {product.get('partNumber', 'N/A')}<br>
<b>Name:</b> {product.get('name', 'N/A')}<br>
<b>Description:</b> {product.get('description', 'N/A')}<br>
<b>State:</b> {product.get('state', 'N/A')}<br>
<b>Non-Serial:</b> {'Yes' if product.get('nonSerial') else 'No'}<br>
<b>Created:</b> {product.get('created', 'N/A')}<br>
"""
        self._details_label.setText(details)
        self._details_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Load revisions
        self._load_revisions(product.get('partNumber'))
        
        # Load BOM if available
        self._load_bom(product)
    
    def _clear_details(self) -> None:
        """Clear details panel"""
        self._details_label.setText("Select a product to view details")
        self._details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._revisions_tree.clear()
        self._bom_tree.clear()
    
    def _load_revisions(self, part_number: str) -> None:
        """Load revisions for a product"""
        self._revisions_tree.clear()
        
        try:
            if self._main_window and self._main_window.app.wats_client:
                client = self._main_window.app.wats_client
                product = client.product.get_product(part_number)
                
                if product and hasattr(product, 'revisions') and product.revisions:
                    for rev in product.revisions:
                        item = QTreeWidgetItem([
                            getattr(rev, 'revision', '') or 'Default',
                            getattr(rev, 'state', '') or 'Active',
                            str(getattr(rev, 'modified', ''))[:19] if hasattr(rev, 'modified') else ''
                        ])
                        self._revisions_tree.addTopLevelItem(item)
                else:
                    # No revisions
                    item = QTreeWidgetItem(["(No revisions)", "", ""])
                    self._revisions_tree.addTopLevelItem(item)
        except Exception as e:
            print(f"[Product] Failed to load revisions: {e}")
    
    def _load_bom(self, product: Dict[str, Any]) -> None:
        """Load BOM for a product"""
        self._bom_tree.clear()
        
        try:
            if self._main_window and self._main_window.app.wats_client:
                client = self._main_window.app.wats_client
                full_product = client.product.get_product(product.get('partNumber'))
                
                if full_product and hasattr(full_product, 'bom') and full_product.bom:
                    for bom_item in full_product.bom:
                        item = QTreeWidgetItem([
                            getattr(bom_item, 'part_number', ''),
                            getattr(bom_item, 'name', ''),
                            str(getattr(bom_item, 'quantity', 1))
                        ])
                        self._bom_tree.addTopLevelItem(item)
                else:
                    item = QTreeWidgetItem(["(No BOM items)", "", ""])
                    self._bom_tree.addTopLevelItem(item)
        except Exception as e:
            print(f"[Product] Failed to load BOM: {e}")
    
    def _on_filter_changed(self) -> None:
        """Handle filter changes"""
        self._populate_table()
    
    def _on_refresh(self) -> None:
        """Refresh products from server"""
        if self._main_window and self._main_window.app.wats_client:
            self._load_products()
        else:
            QMessageBox.warning(self, "Not Connected", "Please connect to WATS server first.")
    
    def _load_products(self) -> None:
        """Load products from WATS server"""
        try:
            self._status_label.setText("Loading products...")
            
            if self._main_window and self._main_window.app.wats_client:
                client = self._main_window.app.wats_client
                
                # Get products
                products = client.product.get_products()
                self._products = [self._product_to_dict(p) for p in products] if products else []
                
                self._populate_table()
                self._status_label.setText(f"Loaded {len(self._products)} products")
            else:
                self._status_label.setText("Not connected to WATS server")
        except Exception as e:
            self._status_label.setText(f"Error: {str(e)[:50]}")
            QMessageBox.warning(self, "Error", f"Failed to load products: {e}")
    
    def _product_to_dict(self, product: Any) -> Dict[str, Any]:
        """Convert Product model to dictionary"""
        if hasattr(product, '__dict__'):
            return {
                'partNumber': getattr(product, 'part_number', ''),
                'name': getattr(product, 'name', ''),
                'description': getattr(product, 'description', ''),
                'state': str(getattr(product, 'state', 'Active')),
                'nonSerial': getattr(product, 'non_serial', False),
                'created': str(getattr(product, 'created', ''))[:19],
            }
        return dict(product) if isinstance(product, dict) else {}
    
    def _populate_table(self) -> None:
        """Populate the products table with filtered data"""
        self._products_table.setRowCount(0)
        
        search_text = self._search_edit.text().lower()
        state_filter = self._state_filter.currentText()
        
        for product in self._products:
            # Apply search filter
            if search_text:
                part = product.get('partNumber', '').lower()
                name = product.get('name', '').lower()
                if search_text not in part and search_text not in name:
                    continue
            
            # Apply state filter
            if state_filter != "All":
                if product.get('state', '') != state_filter:
                    continue
            
            row = self._products_table.rowCount()
            self._products_table.insertRow(row)
            
            self._products_table.setItem(row, 0, QTableWidgetItem(product.get('partNumber', '')))
            self._products_table.setItem(row, 1, QTableWidgetItem(product.get('name', '')))
            
            # State with color coding
            state = product.get('state', 'Active')
            state_item = QTableWidgetItem(state)
            if state == "Active":
                state_item.setForeground(QColor("#4CAF50"))  # Green
            elif state == "Deprecated":
                state_item.setForeground(QColor("#FF9800"))  # Orange
            elif state == "Obsolete":
                state_item.setForeground(QColor("#f44336"))  # Red
            self._products_table.setItem(row, 2, state_item)
            
            # Non-serial
            non_serial = "Yes" if product.get('nonSerial') else "No"
            self._products_table.setItem(row, 3, QTableWidgetItem(non_serial))
    
    def _on_add_product(self) -> None:
        """Show dialog to add new product"""
        if not self._main_window or not self._main_window.app.wats_client:
            QMessageBox.warning(self, "Not Connected", "Please connect to WATS server first.")
            return
        
        dialog = ProductDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                client = self._main_window.app.wats_client
                
                # Map state string to enum
                state_map = {
                    "Active": 1,
                    "New": 0,
                    "Engineering": 2,
                    "Deprecated": 3,
                    "Obsolete": 4
                }
                
                result = client.product.create_product(
                    part_number=data['partNumber'],
                    name=data.get('name'),
                    description=data.get('description'),
                    non_serial=data.get('nonSerial', False),
                    state=state_map.get(data.get('state', 'Active'), 1),
                )
                
                if result:
                    QMessageBox.information(self, "Success", "Product created successfully")
                    self._load_products()
                else:
                    QMessageBox.warning(self, "Error", "Failed to create product")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create product: {e}")
    
    def _on_edit_product(self) -> None:
        """Edit selected product"""
        if not self._selected_product:
            return
        
        dialog = ProductDialog(product=self._selected_product, parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                client = self._main_window.app.wats_client
                
                # Update product
                result = client.product.update_product(
                    part_number=data['partNumber'],
                    name=data.get('name'),
                    description=data.get('description'),
                    non_serial=data.get('nonSerial', False),
                )
                
                if result:
                    QMessageBox.information(self, "Success", "Product updated successfully")
                    self._load_products()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update product: {e}")
    
    def _on_add_revision(self) -> None:
        """Add revision to selected product"""
        if not self._selected_product:
            return
        
        part_number = self._selected_product.get('partNumber')
        
        # Simple dialog for revision name
        from PySide6.QtWidgets import QInputDialog
        revision, ok = QInputDialog.getText(
            self, "Add Revision",
            f"Enter revision name for {part_number}:",
            QLineEdit.EchoMode.Normal, "A"
        )
        
        if ok and revision:
            try:
                client = self._main_window.app.wats_client
                result = client.product.create_revision(
                    part_number=part_number,
                    revision=revision,
                )
                
                if result:
                    QMessageBox.information(self, "Success", f"Revision '{revision}' created")
                    self._load_revisions(part_number)
                else:
                    QMessageBox.warning(self, "Error", "Failed to create revision")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create revision: {e}")
    
    def save_config(self) -> None:
        """Save configuration"""
        pass
    
    def load_config(self) -> None:
        """Load configuration"""
        pass
