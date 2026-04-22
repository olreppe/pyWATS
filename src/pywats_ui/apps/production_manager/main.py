"""Entry point for the Production Manager application."""

import sys

from PySide6.QtWidgets import QApplication

from .main_window import ProductionManagerWindow
from pywats_ui.framework.themes import ThemeManager, DARK


def main() -> None:
    """Launch the Production Manager."""
    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("pyWATS Production Manager")
    app.setApplicationVersion("0.2.0")

    # Apply centralized theme (if not already applied by parent app)
    try:
        ThemeManager.instance()
    except RuntimeError:
        theme = ThemeManager()
        theme.apply(app, DARK)

    window = ProductionManagerWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
