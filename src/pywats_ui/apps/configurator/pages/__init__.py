"""Configurator pages package."""

from .connection import ConnectionPage
from .about import AboutPage
from .log import LogPage
from .sn_handler import SerialNumberHandlerPage
from .dashboard import DashboardPage
from .setup import SetupPage
from .converters import ConvertersPageV2

# Removed pages (Phase 1: GUI Cleanup):
# - APISettingsPage (moved to Connection → Advanced)
# - SoftwarePage (not needed for beta)
# - LocationPage (GPS toggle moved to Dashboard)
# - ProxySettingsPage (moved to Connection → Advanced)

__all__ = [
    "ConnectionPage",
    "AboutPage",
    "LogPage",
    "SerialNumberHandlerPage",
    "DashboardPage",
    "SetupPage",
    "ConvertersPageV2",
]
