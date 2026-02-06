"""Main window for Yield Monitor application."""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class YieldMonitorWindow(QMainWindow):
    """Main window for Yield Monitor application."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pyWATS Yield Monitor")
        self.resize(900, 600)
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title = QLabel("📊 Yield Monitor")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Real-time yield analytics and dashboards")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #888; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Hello message
        message = QLabel("Hello WATS! 👋")
        message_font = QFont()
        message_font.setPointSize(18)
        message.setFont(message_font)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("margin: 40px; color: #4ec9b0;")
        layout.addWidget(message)
        
        # Info
        info = QLabel(
            "This application will provide:\n\n"
            "• Real-time yield dashboards\n"
            "• Process analytics (ICT, FCT, EOL)\n"
            "• Trend charts and visualizations\n"
            "• Configurable time ranges\n"
            "• Alert thresholds\n"
            "• Export reports"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("color: #ccc; line-height: 1.6;")
        layout.addWidget(info)
        
        # Close button
        close_btn = QPushButton("Close Window")
        close_btn.clicked.connect(self.close)
        close_btn.setFixedWidth(150)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
