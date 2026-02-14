"""GUI compatibility module.

This module provides compatibility with the old GUI module structure.
The actual GUI implementation has been migrated to pywats_ui.apps.configurator.

This module only provides the entry point function required by the CLI.
"""

from .app import run_gui

__all__ = ["run_gui"]
