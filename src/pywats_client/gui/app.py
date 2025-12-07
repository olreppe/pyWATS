"""
Qt Application Entry Point

Provides the main GUI application runner.
"""

import sys
import asyncio
from typing import Optional
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication

from .main_window import MainWindow
from ..core.config import ClientConfig, get_default_config_path


def run_gui(config: Optional[ClientConfig] = None, config_path: Optional[Path] = None, instance_id: Optional[str] = None) -> int:
    """
    Run the pyWATS Client GUI application.
    
    Args:
        config: ClientConfig instance (optional)
        config_path: Path to configuration file (optional)
        instance_id: Instance ID for multi-instance support (optional)
    
    Returns:
        Exit code
    """
    # Set application metadata
    QCoreApplication.setOrganizationName("WATS")
    QCoreApplication.setApplicationName("WATS Client")
    QCoreApplication.setApplicationVersion("1.0.0")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Apply dark theme
    app.setStyle("Fusion")
    
    # Load or create configuration
    if config:
        pass  # Use provided config
    elif config_path:
        config = ClientConfig.load_or_create(Path(config_path))
    else:
        config = ClientConfig.load_or_create(get_default_config_path(instance_id))
    
    # Create and show main window
    window = MainWindow(config)
    window.show()
    
    # Run event loop
    return app.exec()


def run_headless(config_path: Optional[Path] = None) -> int:
    """
    Run the pyWATS Client in headless mode (no GUI).
    
    Args:
        config_path: Path to configuration file (optional)
    
    Returns:
        Exit code
    """
    from ..core.client import WATSClient
    
    # Load configuration
    if config_path:
        config = ClientConfig.load(Path(config_path))
    else:
        config = ClientConfig.load(get_default_config_path())
    
    # Create and run client
    client = WATSClient(config)
    
    try:
        client.run()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1
