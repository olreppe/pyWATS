"""Main entry point for {{AppTitle}} application."""

import sys
from pywats_ui.framework import BaseApplication, BaseMainWindow
from .main_window import {{AppTitle}}Window


def main():
    """Entry point for {{AppTitle}} application."""
    app = BaseApplication("pyWATS {{AppTitle}}", "0.1.0")
    
    # Optional: Set up logging, config, API connection here
    # from pywats.core.logging import configure_logging
    # configure_logging(level="INFO")
    
    window = {{AppTitle}}Window()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
