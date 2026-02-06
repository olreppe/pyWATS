"""Main entry point for Package Manager application."""

import sys
from pywats_ui.framework import BaseApplication
from .main_window import PackageManagerWindow


def main():
    """Entry point for Package Manager application."""
    app = BaseApplication("pyWATS Package Manager", "0.1.0")
    
    # Set up logging
    from pywats.core.logging import configure_logging
    configure_logging(
        level="INFO",
        file_path="pywats_package_manager.log"
    )
    
    window = PackageManagerWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
