"""
Client B Launcher (Secondary Instance)

Launches the secondary pyWATS client instance with instance_id="client_b".
This is the secondary instance for multi-instance testing scenarios.

Instance Configuration:
- Instance ID: "client_b"
- Config: ~/.pywats/instances/client_b/client_config.json
- Queue: ~/.pywats/instances/client_b/queue/
- Logs: ~/.pywats/instances/client_b/logs/
- API Port: 8081 (if enabled)

Token Sharing:
- If Client B has no API token, it will attempt to use Client A's token
- This allows testing with a single WATS API connection

Usage:
    python run_client_b.py
"""

import sys
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
    """Launch Client B (secondary instance)"""
    logger.info("=" * 80)
    logger.info("pyWATS Client B (Secondary Instance)")
    logger.info("=" * 80)
    logger.info("Instance ID: client_b")
    logger.info("=" * 80)
    
    try:
        from PySide6.QtWidgets import QApplication
        from pywats_client.core.config import ClientConfig
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("pyWATS Client B")
        app.setOrganizationName("pyWATS")
        
        # Load or create config for instance "client_b"
        instance_id = "client_b"
        config_path = Path.home() / ".pywats" / "instances" / instance_id / "client_config.json"
        
        if config_path.exists():
            config = ClientConfig.load(config_path)
            logger.info(f"Loaded config from: {config_path}")
        else:
            logger.info("Creating new config for Client B")
            config = ClientConfig(instance_id=instance_id)
            config.instance_name = "Client B (Secondary)"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config._config_path = config_path
            
            # Token sharing: Use Client A's token if B has none
            client_a_config_path = Path.home() / ".pywats" / "instances" / "default" / "client_config.json"
            if client_a_config_path.exists():
                logger.info("Checking Client A for token sharing...")
                try:
                    client_a_config = ClientConfig.load(client_a_config_path)
                    if hasattr(client_a_config, 'api_token') and client_a_config.api_token:
                        config.api_token = client_a_config.api_token
                        config.api_base_url = client_a_config.api_base_url
                        logger.info("Inherited API token from Client A")
                except Exception as e:
                    logger.warning(f"Could not load Client A config: {e}")
            
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
        window.setWindowTitle(f"pyWATS Client B - {instance_id}")
        window.show()
        
        logger.info("Client B launched successfully")
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
        logger.error(f"Failed to launch Client B: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
