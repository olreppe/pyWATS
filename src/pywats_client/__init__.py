"""
pyWATS Client - Cross-platform client application for WATS

Features:
- Process data synchronization from WATS server
- Offline report storage and automatic upload when online
- Converter framework for file-to-report conversion
- Qt-based GUI (optional - can run headless)
- Multi-instance support
- Persistent settings and serial number management
- File monitoring and auto-conversion
- Service/daemon mode support
"""

__version__ = "1.0.0"

# Core components
from .core.config import ClientConfig
from .core.client import WATSClient
from .converters.base import ConverterBase, ConverterResult

# Application layer (no GUI)
from .app import pyWATSApplication, ApplicationStatus, ApplicationError, ServiceError

# Services
from .services.settings_manager import (
    SettingsManager,
    ApplicationSettings,
    MonitorFolder,
    ConverterConfig,
)
from .services.serial_manager import SerialNumberManager, ReservedSerial
from .services.file_monitor import FileMonitor, MonitorRule, FileEventType
from .services.connection import ConnectionService, ConnectionStatus
from .services.process_sync import ProcessSyncService
from .services.report_queue import ReportQueueService
from .services.converter_manager import ConverterManager
from .services.converter_processor import ConverterProcessor, ConversionRecord

# Converters
from .converters.base import (
    ConverterBase,
    ConverterResult,
    ConverterArguments,
    ConversionStatus,
    PostProcessAction,
    FileInfo,
    CSVConverter,
)

__all__ = [
    # Core
    "ClientConfig",
    "WATSClient",
    
    # Application
    "pyWATSApplication",
    "ApplicationStatus",
    "ApplicationError",
    "ServiceError",
    
    # Settings
    "SettingsManager",
    "ApplicationSettings",
    "MonitorFolder",
    "ConverterConfig",
    
    # Serial management
    "SerialNumberManager",
    "ReservedSerial",
    
    # File monitoring
    "FileMonitor",
    "MonitorRule",
    "FileEventType",
    
    # Services
    "ConnectionService",
    "ConnectionStatus",
    "ProcessSyncService",
    "ReportQueueService",
    "ConverterManager",
    "ConverterProcessor",
    "ConversionRecord",
    
    # Converters
    "ConverterBase",
    "ConverterResult",
    "ConverterArguments",
    "ConversionStatus",
    "PostProcessAction",
    "FileInfo",
    "CSVConverter",
]
