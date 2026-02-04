"""Configuration management for pyWATS Client Configurator."""

import json
from pathlib import Path
from typing import Any, Dict


class ConfiguratorConfig:
    """Configuration manager for pyWATS Client Configurator."""
    
    def __init__(self):
        """Initialize configuration."""
        self.config_dir = Path.home() / ".pywats" / "configurator"
        self.config_file = self.config_dir / "config.json"
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self._config = json.load(f)
            except Exception as e:
                print(f"Failed to load config: {e}")
                self._config = {}
        else:
            self._config = self.get_defaults()
            self.save()
    
    def save(self):
        """Save configuration to file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self._config[key] = value
        self.save()
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "window_width": 900,
            "window_height": 700,
            "server_url": "",
            "username": "",
            "station_name": "",
            "station_id": "",
            "theme": "default",
        }
