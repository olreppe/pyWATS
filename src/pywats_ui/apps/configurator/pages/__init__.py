"""Configurator pages package."""

from .connection import ConnectionPage
from .about import AboutPage
from .log import LogPage
from .sn_handler import SerialNumberHandlerPage
from .dashboard import DashboardPage
from .api_settings import APISettingsPage
from .setup import SetupPage
from .software import SoftwarePage
from .location import LocationPage
from .proxy_settings import ProxySettingsPage
from .converters import ConvertersPageV2

__all__ = [
    "ConnectionPage",
    "AboutPage",
    "LogPage",
    "SerialNumberHandlerPage",
    "DashboardPage",
    "APISettingsPage",
    "SetupPage",
    "SoftwarePage",
    "LocationPage",
    "ProxySettingsPage",
    "ConvertersPageV2",
]
