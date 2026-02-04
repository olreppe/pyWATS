"""Main entry point for pyWATS Client Configurator."""

import sys
from pywats_ui.framework import BaseApplication, BaseMainWindow
from .main_window import ConfiguratorWindow


def main():
    """Entry point for pyWATS Client Configurator application."""
    app = BaseApplication("pyWATS Client Configurator", "0.3.0")
    
    # Set up logging
    from pywats.core.logging import configure_logging
    configure_logging(
        level="INFO",
        file_path="pywats_configurator.log"
    )
    
    window = ConfiguratorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
