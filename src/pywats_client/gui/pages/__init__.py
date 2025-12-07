"""
GUI Pages module

Contains all page widgets for the main window.
"""

from .base import BasePage
from .general import GeneralPage
from .connection import ConnectionPage
from .proxy_settings import ProxySettingsPage
from .converters import ConvertersPage
from .about import AboutPage

__all__ = [
    "BasePage",
    "GeneralPage",
    "ConnectionPage",
    "ProxySettingsPage",
    "ConvertersPage",
    "AboutPage",
]
