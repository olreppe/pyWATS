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
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


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
        
        return app.exec()
        
    except Exception as e:
        logger.error(f"Failed to launch Client B: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
