"""AI Chat Application - Hello World Version."""

import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QLabel
)
from PySide6.QtCore import Qt, QThread, Signal
from pywats_ui.framework import BaseApplication, BaseMainWindow


class LLMWorker(QThread):
    """Background worker for LLM API calls."""
    response_ready = Signal(str)
    
    def __init__(self, prompt: str):
        super().__init__()
        self.prompt = prompt
    
    def run(self):
        """Call OpenAI API (placeholder for now)."""
        # TODO: Actual OpenAI integration
        # For hello world, just echo back
        response = f"🤖 AI Response:\n\nYou asked: '{self.prompt}'\n\n"
        response += "Six Sigma Analysis:\n"
        response += "• Cp: 1.33 (capable)\n"
        response += "• Cpk: 1.25 (capable)\n"
        response += "• Process is within specification limits.\n\n"
        response += "(This is a placeholder - OpenAI integration coming next!)"
        
        self.response_ready.emit(response)


class AIChatWindow(BaseMainWindow):
    """Main window for AI Chat application."""
    
    def __init__(self):
        super().__init__("pyWATS AI Chat - Hello World")
        self.setup_ui()
        self.worker = None
    
    def setup_ui(self):
        """Set up the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🤖 AI-Powered Test Data Analysis (Hello World)")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Chat history
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setPlaceholderText("Chat history will appear here...")
        layout.addWidget(self.chat_history, stretch=1)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask about test data (e.g., 'What is the Cpk for ICT?')")
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field, stretch=1)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # Quick actions
        quick_layout = QHBoxLayout()
        quick_label = QLabel("Quick Actions:")
        quick_layout.addWidget(quick_label)
        
        btn_cpk = QPushButton("Calculate Cpk")
        btn_cpk.clicked.connect(lambda: self.quick_query("Calculate Cpk for last 100 units"))
        quick_layout.addWidget(btn_cpk)
        
        btn_spc = QPushButton("SPC Check")
        btn_spc.clicked.connect(lambda: self.quick_query("Check for SPC violations"))
        quick_layout.addWidget(btn_spc)
        
        btn_rca = QPushButton("Root Cause")
        btn_rca.clicked.connect(lambda: self.quick_query("Analyze root causes for failures"))
        quick_layout.addWidget(btn_rca)
        
        quick_layout.addStretch()
        layout.addLayout(quick_layout)
        
        # Initial greeting
        self.chat_history.append("🤖 Welcome to pyWATS AI Chat!\n")
        self.chat_history.append("Ask me anything about your test data:\n")
        self.chat_history.append("• Process capability (Cp, Cpk, Pp, Ppk)\n")
        self.chat_history.append("• SPC violations and trends\n")
        self.chat_history.append("• Root cause analysis\n")
        self.chat_history.append("• Statistical insights\n\n")
        self.chat_history.append("=" * 60 + "\n\n")
    
    def quick_query(self, query: str):
        """Send a quick query."""
        self.input_field.setText(query)
        self.send_message()
    
    def send_message(self):
        """Send user message to LLM."""
        user_input = self.input_field.text().strip()
        if not user_input:
            return
        
        # Display user message
        self.chat_history.append(f"👤 You: {user_input}\n")
        self.input_field.clear()
        self.send_button.setEnabled(False)
        self.send_button.setText("Thinking...")
        
        # Call LLM in background
        self.worker = LLMWorker(user_input)
        self.worker.response_ready.connect(self.handle_response)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.start()
    
    def handle_response(self, response: str):
        """Handle LLM response."""
        self.chat_history.append(response + "\n\n")
        self.chat_history.append("=" * 60 + "\n\n")
        self.send_button.setEnabled(True)
        self.send_button.setText("Send")
        self.worker = None


def main():
    """Entry point for AI Chat application."""
    app = BaseApplication("pyWATS AI Chat", "0.1.0")
    window = AIChatWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
