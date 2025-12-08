"""
GUI Pages module

Contains all page widgets for the main window.
"""

from .base import BasePage
from .setup import SetupPage
from .general import GeneralPage
from .connection import ConnectionPage
from .proxy_settings import ProxySettingsPage
from .converters import ConvertersPage
from .location import LocationPage
from .sn_handler import SNHandlerPage
from .software import SoftwarePage
from .about import AboutPage

__all__ = [
    "BasePage",
    "SetupPage",
    "GeneralPage",
    "ConnectionPage",
    "ProxySettingsPage",
    "ConvertersPage",
    "LocationPage",
    "SNHandlerPage",
    "SoftwarePage",
    "AboutPage",
]
