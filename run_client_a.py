"""
Client A Launcher (Master Instance)

Launches the primary pyWATS client instance with instance_id="default".
This is the master instance for testing single-instance and multi-instance scenarios.

Instance Configuration (System-wide):
- Instance ID: "default"
- Config: C:/ProgramData/pyWATS/instances/default/client_config.json
- Queue: C:/ProgramData/pyWATS/instances/default/queue/
- Logs: C:/ProgramData/pyWATS/instances/default/logs/
- API Port: 8080 (if enabled)

Note: Uses system-wide paths so client can run as Windows Service
      accessible by all users on the machine.

Usage:
    python run_client_a.py
"""

import sys
import os
import logging
import json
import asyncio
from pathlib import Path

try:
    import qasync  # FIX C4: Add qasync for async event loop
except ImportError:
    qasync = None
    logging.warning("qasync not installed - async operations may not work correctly")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


def migrate_old_config(old_config_path: Path, new_config, instance_id: str):
    """Migrate settings from old GUI config to new instance config if empty."""
    if not old_config_path.exists():
        return False
    
    # Check if new config is empty (no server/token configured)
    if new_config.service_address or new_config.api_token:
        logger.info("Config already has settings, skipping migration")
        return False
    
    try:
        with open(old_config_path, 'r') as f:
            old_config = json.load(f)
        
        logger.info(f"Migrating settings from old config: {old_config_path}")
        
        # Migrate core connection settings
        if old_config.get('service_address'):
            new_config.service_address = old_config['service_address']
            logger.info(f"  ✓ Migrated service_address: {new_config.service_address}")
        
        if old_config.get('api_token'):
            new_config.api_token = old_config['api_token']
            logger.info(f"  ✓ Migrated api_token: {'*' * 20}...")
        
        # Migrate station settings
        if old_config.get('station_name'):
            new_config.station_name = old_config['station_name']
            logger.info(f"  ✓ Migrated station_name: {new_config.station_name}")
        
        if old_config.get('location'):
            new_config.location = old_config['location']
            logger.info(f"  ✓ Migrated location: {new_config.location}")
        
        if old_config.get('purpose'):
            new_config.purpose = old_config['purpose']
        
        # Migrate converter settings (use old configs if present)
        if old_config.get('converters') and len(old_config['converters']) > 0:
            # Convert dicts to ConverterConfig objects (FIX C1: was assigning raw dicts)
            from pywats_client.core.config import ConverterConfig
            new_config.converters = [
                ConverterConfig.from_dict(c) if isinstance(c, dict) else c
                for c in old_config['converters']
            ]
            logger.info(f"  ✓ Migrated {len(new_config.converters)} converters")
        
        # Migrate other useful settings
        for key in ['proxy_mode', 'proxy_host', 'proxy_port', 'log_level', 
                    'auto_connect', 'converters_enabled']:
            if key in old_config:
                setattr(new_config, key, old_config[key])
        
        logger.info("Migration complete!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to migrate old config: {e}")
        return False


def main():
    """Launch Client A (master instance)"""
    logger.info("=" * 80)
    logger.info("pyWATS Client A (Master Instance)")
    logger.info("=" * 80)
    logger.info("Instance ID: default")
    logger.info("=" * 80)
    
    try:
        from PySide6.QtWidgets import QApplication
        from pywats_client.core.config import ClientConfig, ConverterConfig
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("pyWATS Client A")
        app.setOrganizationName("pyWATS")
        
        # Load or create config for instance "default"
        # Use system-wide path: C:\ProgramData\pyWATS\instances\default\
        instance_id = "default"
        if os.name == 'nt':
            base_path = Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / 'pyWATS' / 'instances'
        else:
            base_path = Path('/var/lib/pywats/instances')
        
        config_path = base_path / instance_id / "client_config.json"
        old_config_path = Path.home() / ".pywats" / "config.json"  # Legacy user-level config for migration
        
        if config_path.exists():
            config = ClientConfig.load(config_path)
            logger.info(f"Loaded config from: {config_path}")
            
            # Try migration from old config if current config is empty
            migrate_old_config(old_config_path, config, instance_id)
        else:
            logger.info("Creating new config for Client A")
            config = ClientConfig(instance_id=instance_id)
            config.instance_name = "Client A (Master)"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config._config_path = config_path
            
            # Try migration from old config
            migrate_old_config(old_config_path, config, instance_id)
            
            config.save()
            logger.info(f"Config saved to: {config_path}")
        
        # Ensure instance-specific directories
        instance_dir = config_path.parent
        (instance_dir / "queue").mkdir(exist_ok=True)
        (instance_dir / "logs").mkdir(exist_ok=True)
        (instance_dir / "reports").mkdir(exist_ok=True)
        (instance_dir / "converters").mkdir(exist_ok=True)
        
        # Create main window
        window = ConfiguratorMainWindow(config=config)
        window.setWindowTitle(f"pyWATS Client A - {instance_id}")
        window.show()
        
        logger.info("Client A launched successfully")
        logger.info("=" * 80)
        
        # FIX C4: Integrate qasync event loop for async operations
        if qasync:
            logger.info("Using qasync event loop for async operations")
            loop = qasync.QEventLoop(app)
            asyncio.set_event_loop(loop)
            with loop:
                return loop.run_forever()
        else:
            logger.warning("Running without qasync - async operations may fail")
            return app.exec()
        
    except Exception as e:
        logger.error(f"Failed to launch Client A: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
