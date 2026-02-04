"""pyWATS UI Widgets - Reusable Qt widgets for pyWATS applications."""

__version__ = "0.3.0"

from .script_editor import ScriptEditor, PythonSyntaxHighlighter
from .new_converter_dialog import NewConverterDialog

__all__ = [
    "ScriptEditor",
    "PythonSyntaxHighlighter",
    "NewConverterDialog",
]
