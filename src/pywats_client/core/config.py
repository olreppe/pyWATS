"""
Client Configuration Management

Handles configuration for pyWATS Client instances including:
- Server connection settings
- Converter configurations
- Sync intervals
- Instance identification
"""

import json
import os
import uuid
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class ConverterConfig:
    """Configuration for a single converter"""
    name: str
    module_path: str
    watch_folder: str
    enabled: bool = True
    arguments: Dict[str, Any] = field(default_factory=dict)
    file_patterns: List[str] = field(default_factory=lambda: ["*.*"])
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConverterConfig":
        return cls(**data)


@dataclass
class ProxyConfig:
    """Proxy configuration"""
    enabled: bool = False
    host: str = ""
    port: int = 8080
    username: str = ""
    password: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProxyConfig":
        return cls(**data)


@dataclass
class ClientConfig:
    """
    Main configuration for pyWATS Client instance.
    
    Each instance has its own configuration file allowing
    multiple instances to run on the same machine.
    """
    # Instance identification
    instance_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    instance_name: str = "WATS Client"
    
    # Server connection
    service_address: str = ""
    api_token: str = ""
    username: str = ""
    
    # Station identification (from WATS server)
    station_name: str = ""
    location: str = ""
    purpose: str = ""
    station_description: str = ""
    auto_detect_location: bool = False
    include_station_in_reports: bool = True
    
    # Serial Number Handler settings
    sn_mode: str = "Manual Entry"  # "Manual Entry", "Auto-increment", "Barcode Scanner", "External Source"
    sn_prefix: str = ""
    sn_start: int = 1
    sn_padding: int = 6
    sn_com_port: str = "Auto-detect"
    sn_terminator: str = "Enter (CR)"
    sn_validate_format: bool = False
    sn_pattern: str = ""
    sn_check_duplicates: bool = True
    
    # Proxy settings (simplified fields for GUI binding)
    proxy_mode: str = "system"  # "none", "system", "manual"
    proxy_host: str = ""
    proxy_port: int = 8080
    proxy_auth: bool = False
    proxy_username: str = ""
    proxy_password: str = ""
    proxy_bypass: str = ""
    
    # Legacy proxy config (for backward compatibility)
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    
    # Sync settings
    sync_interval_seconds: int = 300  # 5 minutes
    process_sync_enabled: bool = True
    
    # Offline storage
    reports_folder: str = "reports"
    offline_queue_enabled: bool = True
    max_retry_attempts: int = 5
    retry_interval_seconds: int = 60
    
    # Converter settings
    converters_folder: str = "converters"
    converters: List[ConverterConfig] = field(default_factory=list)
    converters_enabled: bool = True
    
    # Yield monitor settings
    yield_monitor_enabled: bool = False
    yield_threshold: float = 95.0
    
    # Location services
    location_services_enabled: bool = False
    
    # Software Distribution settings
    software_auto_update: bool = False
    
    # GUI tab visibility settings - control which tabs are shown
    show_software_tab: bool = True
    show_sn_handler_tab: bool = True
    show_converters_tab: bool = True
    show_location_tab: bool = True
    show_proxy_tab: bool = True
    
    # Connection state - persist connected state
    auto_connect: bool = True  # Always try to connect on startup
    was_connected: bool = False  # Remember last connection state
    
    # Service settings
    service_auto_start: bool = True  # Start service on system startup
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "client.log"
    
    # GUI settings
    start_minimized: bool = False
    minimize_to_tray: bool = True
    
    # Internal state (not saved)
    _config_path: Optional[Path] = field(default=None, repr=False)
    
    def __post_init__(self):
        """Ensure nested objects are properly initialized"""
        if isinstance(self.proxy, dict):
            self.proxy = ProxyConfig.from_dict(self.proxy)
        if self.converters:
            converted = []
            for c in self.converters:
                if isinstance(c, dict):
                    converted.append(ConverterConfig.from_dict(c))
                else:
                    converted.append(c)
            self.converters = converted
    
    @property
    def identifier(self) -> str:
        """Get unique identifier for this instance"""
        # Similar to the MAC-based identifier shown in the WATS Client
        import hashlib
        return hashlib.md5(self.instance_id.encode()).hexdigest()[:16].upper()
    
    @property
    def formatted_identifier(self) -> str:
        """Get formatted identifier like 4C:5F:70:D6:2F:F4"""
        ident = self.identifier
        return ":".join(ident[i:i+2] for i in range(0, min(len(ident), 12), 2))
    
    @property
    def data_path(self) -> Path:
        """Get the base data path for this instance.
        
        This is the directory containing config, reports, logs, etc.
        """
        if self._config_path:
            return self._config_path.parent
        # Fallback to default location
        if os.name == 'nt':
            return Path(os.environ.get('APPDATA', '')) / 'pyWATS_Client'
        return Path.home() / '.config' / 'pywats_client'
    
    def get_reports_path(self) -> Path:
        """Get absolute path to reports folder"""
        if os.path.isabs(self.reports_folder):
            return Path(self.reports_folder)
        if self._config_path:
            return self._config_path.parent / self.reports_folder
        return Path(self.reports_folder)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = {
            "instance_id": self.instance_id,
            "instance_name": self.instance_name,
            "service_address": self.service_address,
            "api_token": self.api_token,
            # Station identification
            "station_name": self.station_name,
            "location": self.location,
            "purpose": self.purpose,
            "station_description": self.station_description,
            "auto_detect_location": self.auto_detect_location,
            "include_station_in_reports": self.include_station_in_reports,
            # Serial Number Handler
            "sn_mode": self.sn_mode,
            "sn_prefix": self.sn_prefix,
            "sn_start": self.sn_start,
            "sn_padding": self.sn_padding,
            "sn_com_port": self.sn_com_port,
            "sn_terminator": self.sn_terminator,
            "sn_validate_format": self.sn_validate_format,
            "sn_pattern": self.sn_pattern,
            "sn_check_duplicates": self.sn_check_duplicates,
            # Proxy settings
            "proxy_mode": self.proxy_mode,
            "proxy_host": self.proxy_host,
            "proxy_port": self.proxy_port,
            "proxy_auth": self.proxy_auth,
            "proxy_username": self.proxy_username,
            "proxy_password": self.proxy_password,
            "proxy_bypass": self.proxy_bypass,
            "proxy": self.proxy.to_dict(),
            "sync_interval_seconds": self.sync_interval_seconds,
            "process_sync_enabled": self.process_sync_enabled,
            "reports_folder": self.reports_folder,
            "offline_queue_enabled": self.offline_queue_enabled,
            "max_retry_attempts": self.max_retry_attempts,
            "retry_interval_seconds": self.retry_interval_seconds,
            "converters_folder": self.converters_folder,
            "converters": [c.to_dict() for c in self.converters],
            "converters_enabled": self.converters_enabled,
            "yield_monitor_enabled": self.yield_monitor_enabled,
            "yield_threshold": self.yield_threshold,
            "location_services_enabled": self.location_services_enabled,
            "software_auto_update": self.software_auto_update,
            # GUI tab visibility
            "show_software_tab": self.show_software_tab,
            "show_sn_handler_tab": self.show_sn_handler_tab,
            "show_converters_tab": self.show_converters_tab,
            "show_location_tab": self.show_location_tab,
            "show_proxy_tab": self.show_proxy_tab,
            "auto_connect": self.auto_connect,
            "was_connected": self.was_connected,
            "service_auto_start": self.service_auto_start,
            "log_level": self.log_level,
            "log_file": self.log_file,
            "start_minimized": self.start_minimized,
            "minimize_to_tray": self.minimize_to_tray,
        }
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientConfig":
        """Create from dictionary"""
        return cls(**data)
    
    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to file"""
        save_path = path or self._config_path
        if not save_path:
            raise ValueError("No configuration path specified")
        
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        self._config_path = save_path
    
    @classmethod
    def load(cls, path: Path) -> "ClientConfig":
        """Load configuration from file"""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        config = cls.from_dict(data)
        config._config_path = path
        return config
    
    @classmethod
    def load_or_create(cls, path: Path) -> "ClientConfig":
        """Load existing configuration or create new one"""
        path = Path(path)
        if path.exists():
            return cls.load(path)
        
        config = cls()
        config._config_path = path
        config.save()
        return config


def get_default_config_path(instance_id: Optional[str] = None) -> Path:
    """
    Get default configuration path for an instance.
    
    On Windows: %APPDATA%/pyWATS_Client/
    On Linux/Mac: ~/.config/pywats_client/
    """
    if os.name == 'nt':
        base = Path(os.environ.get('APPDATA', '')) / 'pyWATS_Client'
    else:
        base = Path.home() / '.config' / 'pywats_client'
    
    if instance_id:
        return base / f"config_{instance_id}.json"
    return base / "config.json"


def get_all_instance_configs() -> List[Path]:
    """Get all configuration files for all instances"""
    if os.name == 'nt':
        base = Path(os.environ.get('APPDATA', '')) / 'pyWATS_Client'
    else:
        base = Path.home() / '.config' / 'pywats_client'
    
    if not base.exists():
        return []
    
    return list(base.glob("config*.json"))
