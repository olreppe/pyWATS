"""Main window for {{AppTitle}} application."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QTabWidget, QStatusBar
)
from PySide6.QtCore import Qt
from pywats_ui.framework import BaseMainWindow


class {{AppTitle}}Window(BaseMainWindow):
    """Main window for {{AppTitle}} application."""
    
    def __init__(self):
        super().__init__("pyWATS {{AppTitle}}")
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_status_bar()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("pyWATS {{AppTitle}}")
        header.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(header)
        
        # Tab widget (customize with your tabs)
        self.tabs = QTabWidget()
        
        # Example Tab 1
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        tab1_layout.addWidget(QLabel("Welcome to pyWATS {{AppTitle}}!"))
        tab1_layout.addWidget(QLabel("Customize this tab in main_window.py"))
        tab1_layout.addStretch()
        self.tabs.addTab(tab1, "Overview")
        
        # Example Tab 2
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        tab2_layout.addWidget(QLabel("Add your custom content here"))
        tab2_layout.addStretch()
        self.tabs.addTab(tab2, "Settings")
        
        layout.addWidget(self.tabs)
        
        # Button bar (example actions)
        button_layout = QHBoxLayout()
        
        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.on_refresh)
        button_layout.addWidget(btn_refresh)
        
        btn_settings = QPushButton("Settings")
        btn_settings.clicked.connect(self.on_settings)
        button_layout.addWidget(btn_settings)
        
        button_layout.addStretch()
        
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.close)
        button_layout.addWidget(btn_close)
        
        layout.addLayout(button_layout)
    
    def setup_menu_bar(self):
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # TODO: Add file menu actions
        # exit_action = file_menu.addAction("E&xit")
        # exit_action.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(self.on_about)
    
    def setup_status_bar(self):
        """Set up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    # Action handlers
    def on_refresh(self):
        """Handle refresh button click."""
        self.status_bar.showMessage("Refreshing...", 2000)
        # TODO: Add your refresh logic here
    
    def on_settings(self):
        """Handle settings button click."""
        self.status_bar.showMessage("Opening settings...", 2000)
        # TODO: Open settings dialog
    
    def on_about(self):
        """Handle about menu action."""
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(
            self,
            "About pyWATS {{AppTitle}}",
            "pyWATS {{AppTitle}} v0.1.0\n\n"
            "Part of the pyWATS GUI framework.\n\n"
            "© 2026 Your Organization"
        )
