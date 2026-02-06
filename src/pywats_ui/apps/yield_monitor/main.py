"""Main entry point for Yield Monitor application."""

import sys
from pywats_ui.framework import BaseApplication
from .main_window import YieldMonitorWindow


def main():
    """Entry point for Yield Monitor application."""
    app = BaseApplication("pyWATS Yield Monitor", "0.1.0")
    
    # Set up logging
    from pywats.core.logging import configure_logging
    configure_logging(
        level="INFO",
        file_path="pywats_yield_monitor.log"
    )
    
    window = YieldMonitorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
