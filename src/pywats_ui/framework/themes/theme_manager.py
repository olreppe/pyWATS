"""
Centralized theme manager for pyWATS GUI applications.

Resolves ThemeTokens into a QSS stylesheet from base.qss, applies it to
QApplication, and provides color accessors for paint events and syntax
highlighting that cannot use QSS.

Usage:
    from pywats_ui.framework.themes import ThemeManager, DARK, LIGHT

    app = QApplication([])
    theme = ThemeManager()
    theme.apply(app, DARK)       # apply at startup
    theme.switch(LIGHT)          # swap at runtime

    # In widgets / highlighters:
    color = theme.color("syntax_keyword")   # -> QColor
    hexval = theme.hex("accent_primary")    # -> "#f0a30a"
"""

from __future__ import annotations

import warnings
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from .dark_tokens import DARK
from .tokens import ThemeTokens

# Load the QSS template once at import time
_QSS_TEMPLATE_PATH = Path(__file__).parent / "base.qss"
_QSS_TEMPLATE: Optional[str] = None


def _load_qss_template() -> str:
    """Load and cache the QSS template from disk."""
    global _QSS_TEMPLATE
    if _QSS_TEMPLATE is None:
        _QSS_TEMPLATE = _QSS_TEMPLATE_PATH.read_text(encoding="utf-8")
    return _QSS_TEMPLATE


# Module-level singleton for convenient access from widgets
_instance: Optional["ThemeManager"] = None


class ThemeManager:
    """Centralized theme management for all pyWATS GUI applications.

    Typical lifecycle:
        1. Instantiate in BaseApplication.__init__()
        2. Call apply(app, tokens) once
        3. Widgets call ThemeManager.instance() to look up colors
    """

    def __init__(self) -> None:
        self._current: ThemeTokens = DARK
        self._app: Optional[QApplication] = None
        self._token_dict: dict[str, str] = asdict(DARK)
        # Register as the module-level singleton
        global _instance
        _instance = self

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def apply(self, app: QApplication, tokens: ThemeTokens) -> None:
        """Apply a theme to the application.

        This sets the application-wide stylesheet so all widgets inherit
        the theme automatically. Also sets QPalette for native dialogs.
        """
        self._app = app
        self._current = tokens
        self._token_dict = asdict(tokens)
        self._apply_stylesheet(app)
        self._apply_palette(app)

    def switch(self, tokens: ThemeTokens) -> None:
        """Switch to a different theme at runtime.

        All existing widgets are immediately re-styled.
        """
        if self._app is None:
            warnings.warn(
                "ThemeManager.switch() called before apply(). "
                "Call apply(app, tokens) first.",
                stacklevel=2,
            )
            return
        self.apply(self._app, tokens)

    def color(self, token_name: str) -> QColor:
        """Get a QColor for use in paint events or QTextCharFormat.

        Args:
            token_name: A field name from ThemeTokens (e.g. 'syntax_keyword').

        Returns:
            QColor instance.

        Raises:
            KeyError: If token_name is not a valid token.
        """
        return QColor(self._token_dict[token_name])

    def hex(self, token_name: str) -> str:
        """Get the hex color string for a token.

        Args:
            token_name: A field name from ThemeTokens.

        Returns:
            Hex string like '#f0a30a'.

        Raises:
            KeyError: If token_name is not a valid token.
        """
        return self._token_dict[token_name]

    @property
    def current(self) -> ThemeTokens:
        """The currently active theme tokens."""
        return self._current

    @property
    def tokens(self) -> dict[str, str]:
        """All current token values as a dict (read-only copy)."""
        return dict(self._token_dict)

    @staticmethod
    def instance() -> "ThemeManager":
        """Get the module-level ThemeManager singleton.

        Raises:
            RuntimeError: If no ThemeManager has been created yet.
        """
        if _instance is None:
            raise RuntimeError(
                "ThemeManager has not been initialized. "
                "Create a ThemeManager instance in your application startup."
            )
        return _instance

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _apply_stylesheet(self, app: QApplication) -> None:
        """Render the QSS template with current tokens and apply."""
        template = _load_qss_template()
        stylesheet = template.format_map(self._token_dict)
        app.setStyleSheet(stylesheet)

    def _apply_palette(self, app: QApplication) -> None:
        """Set QPalette for native dialog consistency."""
        t = self._current
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(t.bg_base))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(t.text_primary))
        palette.setColor(QPalette.ColorRole.Base, QColor(t.bg_elevated))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(t.bg_surface))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(t.bg_elevated))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(t.text_primary))
        palette.setColor(QPalette.ColorRole.Text, QColor(t.text_primary))
        palette.setColor(QPalette.ColorRole.Button, QColor(t.bg_elevated))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(t.text_primary))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(t.status_error))
        palette.setColor(QPalette.ColorRole.Link, QColor(t.accent_link))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(t.accent_primary))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(t.text_on_accent))
        # Disabled group
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.WindowText,
            QColor(t.text_disabled),
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Text,
            QColor(t.text_disabled),
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            QColor(t.text_disabled),
        )
        app.setPalette(palette)
