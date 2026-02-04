"""Log Viewer Page - Migrated with reliability improvements.

Improvements:
- H4: cleanup() method to properly remove log handler
- Better error handling for log handler setup
- Thread-safe logging via Qt signals (already in original)
"""

import logging
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QPushButton, QComboBox, QLabel, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QTextCursor, QFont

from pywats_ui.framework import BasePage
from pywats_client.core.config import ClientConfig

logger = logging.getLogger(__name__)


class QTextEditLogger(logging.Handler, QObject):
    """Custom logging handler that emits log messages to a Qt signal.
    
    Thread-safe logging to GUI via Qt's signal/slot mechanism.
    """
    log_signal = Signal(str)
    
    def __init__(self) -> None:
        logging.Handler.__init__(self)
        QObject.__init__(self)
        
        # Format for log display
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        self.setFormatter(formatter)
    
    def emit(self, record) -> None:
        """Emit log record to Qt signal"""
        try:
            msg = self.format(record)
            self.log_signal.emit(msg)
        except Exception:
            self.handleError(record)


class LogPage(BasePage):
    """Log viewer page with real-time log display"""
    
    def __init__(self, config: ClientConfig, parent: Optional[QWidget] = None) -> None:
        super().__init__(config, parent)
        self._log_handler: Optional[QTextEditLogger] = None
        self._auto_scroll = True
        self._max_lines = 1000
        self._setup_ui()
        self._setup_logging()
    
    @property
    def page_title(self) -> str:
        return "Log Viewer"
    
    def _setup_ui(self) -> None:
        """Setup page UI"""
        # Controls toolbar
        controls_layout = QHBoxLayout()
        
        # Log level filter
        controls_layout.addWidget(QLabel("Log Level:"))
        self._level_combo = QComboBox()
        self._level_combo.addItems(["ALL", "DEBUG", "INFO", "WARNING", "ERROR"])
        self._level_combo.setCurrentText("INFO")
        self._level_combo.currentTextChanged.connect(self._on_level_changed)
        controls_layout.addWidget(self._level_combo)
        
        controls_layout.addSpacing(20)
        
        # Auto-scroll checkbox
        self._auto_scroll_cb = QCheckBox("Auto-scroll")
        self._auto_scroll_cb.setChecked(True)
        self._auto_scroll_cb.stateChanged.connect(self._on_auto_scroll_changed)
        controls_layout.addWidget(self._auto_scroll_cb)
        
        controls_layout.addSpacing(20)
        
        # Clear button
        self._clear_btn = QPushButton("Clear")
        self._clear_btn.clicked.connect(self._on_clear_clicked)
        controls_layout.addWidget(self._clear_btn)
        
        # Copy button
        self._copy_btn = QPushButton("Copy All")
        self._copy_btn.clicked.connect(self._on_copy_clicked)
        controls_layout.addWidget(self._copy_btn)
        
        controls_layout.addStretch()
        
        self._layout.addLayout(controls_layout)
        
        # Log display area
        self._log_display = QPlainTextEdit()
        self._log_display.setReadOnly(True)
        self._log_display.setMaximumBlockCount(self._max_lines)
        
        # Use monospace font for better readability
        font = QFont("Consolas", 9)
        if not font.exactMatch():
            font = QFont("Courier New", 9)
        self._log_display.setFont(font)
        
        # Dark theme styling
        self._log_display.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                padding: 5px;
            }
        """)
        
        self._layout.addWidget(self._log_display, 1)
        
        # Info label
        info_label = QLabel(
            f"Displaying last {self._max_lines} log entries. "
            "Logs are also written to file for persistence."
        )
        info_label.setStyleSheet("color: #808080; font-style: italic;")
        self._layout.addWidget(info_label)
    
    def _setup_logging(self) -> None:
        """Setup logging handler to capture logs with error handling."""
        try:
            self._log_handler = QTextEditLogger()
            self._log_handler.log_signal.connect(self._append_log)
            
            # Add handler to root logger to capture all logs
            root_logger = logging.getLogger()
            root_logger.addHandler(self._log_handler)
            
            logger.info("Log viewer initialized")
            
        except Exception as e:
            logger.exception(f"Failed to setup log handler: {e}")
            QMessageBox.warning(
                self,
                "Log Setup Error",
                f"Failed to initialize log viewer.\n\nError: {e}\n\n"
                "Logs will not be displayed in this window."
            )
    
    def _append_log(self, message: str) -> None:
        """Append log message to display (thread-safe via Qt signal)."""
        try:
            # Filter by level if needed
            if self._level_combo.currentText() != "ALL":
                level_filter = self._level_combo.currentText()
                if level_filter not in message:
                    return
            
            # Append message
            self._log_display.appendPlainText(message)
            
            # Auto-scroll to bottom if enabled
            if self._auto_scroll:
                self._log_display.moveCursor(QTextCursor.MoveOperation.End)
                
        except Exception as e:
            # Silently fail to avoid logging recursion
            pass
    
    def _on_level_changed(self, level: str) -> None:
        """Handle log level filter change"""
        # When level changes, we just filter new messages
        # Existing messages remain visible
        logger.info(f"Log level filter changed to: {level}")
    
    def _on_auto_scroll_changed(self, state: int) -> None:
        """Handle auto-scroll checkbox change"""
        self._auto_scroll = (state == Qt.CheckState.Checked.value)
    
    def _on_clear_clicked(self) -> None:
        """Clear log display"""
        self._log_display.clear()
        logger.info("Log display cleared by user")
    
    def _on_copy_clicked(self) -> None:
        """Copy all log text to clipboard"""
        try:
            from PySide6.QtWidgets import QApplication
            text = self._log_display.toPlainText()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            
            logger.info(f"Copied {len(text)} characters to clipboard")
            
        except Exception as e:
            logger.exception(f"Failed to copy logs: {e}")
            QMessageBox.warning(
                self,
                "Copy Failed",
                f"Failed to copy logs to clipboard.\n\nError: {e}"
            )
    
    def save_config(self) -> None:
        """Save configuration (nothing to save for log viewer)"""
        pass
    
    def load_config(self) -> None:
        """Load configuration (nothing to load for log viewer)"""
        pass
    
    def cleanup(self) -> None:
        """Clean up resources - remove log handler (H4 fix)."""
        if self._log_handler:
            try:
                root_logger = logging.getLogger()
                root_logger.removeHandler(self._log_handler)
                logger.info("Log viewer cleanup complete")
            except Exception as e:
                logger.exception(f"Error during log viewer cleanup: {e}")
