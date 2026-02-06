"""Main entry point for Client Monitor application."""

import sys
from pywats_ui.framework import BaseApplication
from .main_window import ClientMonitorWindow


def main():
    """Entry point for Client Monitor application."""
    app = BaseApplication("pyWATS Client Monitor", "0.1.0")
    
    # Set up logging
    from pywats.core.logging import configure_logging
    configure_logging(
        level="INFO",
        file_path="pywats_client_monitor.log"
    )
    
    window = ClientMonitorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
