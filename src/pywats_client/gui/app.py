"""GUI entry point module.

This module provides the run_gui() function used by the pywats-client CLI.

Note: The old GUI (pywats_client.gui) has been migrated to the new configurator
(pywats_ui.apps.configurator). This module serves as a compatibility layer.
"""

import sys
import logging
from pywats.core.logging import get_logger
from pathlib import Path
from typing import Optional

logger = get_logger(__name__)


def run_gui(config: 'ClientConfig', instance_id: str = "default") -> None:
    """Launch Configurator GUI with qasync integration.
    
    This is the main entry point for the pyWATS Configurator GUI.
    It sets up the Qt application with async event loop support via qasync.
    
    Args:
        config: ClientConfig instance to use
        instance_id: Instance ID for multi-station mode (default: "default")
        
    Raises:
        ImportError: If PySide6 or qasync is not installed
        SystemExit: When GUI is closed
        
    Example:
        >>> from pywats_client.core.config import ClientConfig
        >>> from pywats_client.gui.app import run_gui
        >>> 
        >>> config = ClientConfig.load_or_create()
        >>> run_gui(config)  # Launches GUI
    """
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        import qasync
        import asyncio
    except ImportError as e:
        logger.exception(f"Failed to import GUI dependencies: {e}")
        print("Error: GUI mode requires PySide6 and qasync")
        print("Install with: pip install pywats-api[client]")
        sys.exit(1)
    
    try:
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
    except ImportError as e:
        logger.exception(f"Failed to import configurator: {e}")
        print("Error: Configurator GUI is not available")
        print("Please ensure pywats_ui package is installed")
        sys.exit(1)
    
    logger.info(f"Launching pyWATS Configurator [instance: {instance_id}]")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("pyWATS Configurator")
    app.setOrganizationName("pyWATS")
    
    # Enable high DPI support
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    except Exception:
        pass  # Ignore if not available
    
    # Setup async event loop with qasync
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    # Create and show main window
    window = ConfiguratorMainWindow(config=config)
    
    # Set window title with instance name
    if instance_id != "default":
        window.setWindowTitle(f"pyWATS Configurator - {instance_id}")
    else:
        window.setWindowTitle("pyWATS Configurator")
    
    window.show()
    
    logger.info("Configurator GUI launched successfully")
    
    # Run event loop
    with loop:
        loop.run_forever()


__all__ = ["run_gui"]
