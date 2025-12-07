"""
pyWATS Client - Cross-platform client application for WATS

Features:
- Process data synchronization from WATS server
- Offline report storage and automatic upload when online
- Converter framework for file-to-report conversion
- Qt-based GUI (optional - can run headless)
- Multi-instance support
"""

__version__ = "1.0.0"

from .core.config import ClientConfig
from .core.client import WATSClient
from .converters.base import ConverterBase, ConverterResult

__all__ = [
    "ClientConfig",
    "WATSClient",
    "ConverterBase",
    "ConverterResult",
]
