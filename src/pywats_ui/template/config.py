"""Configuration management for {{AppTitle}} application."""

import json
from pathlib import Path
from typing import Any, Dict


class AppConfig:
    """Application configuration manager."""
    
    def __init__(self, app_name: str):
        """Initialize configuration.
        
        Args:
            app_name: Application name (used for config file path)
        """
        self.app_name = app_name
        self.config_dir = Path.home() / ".pywats" / app_name
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
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
        self.save()
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get default configuration values.
        
        Returns:
            Dictionary of default configuration values
        """
        return {
            "window_width": 800,
            "window_height": 600,
            "theme": "default",
            # Add your default config values here
        }
