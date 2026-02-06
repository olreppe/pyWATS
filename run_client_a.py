"""
Client A Launcher (Master Instance)

Launches the primary pyWATS client instance with instance_id="default".
This is the master instance for testing single-instance and multi-instance scenarios.

Instance Configuration:
- Instance ID: "default"
- Config: ~/.pywats/instances/default/client_config.json
- Queue: ~/.pywats/instances/default/queue/
- Logs: ~/.pywats/instances/default/logs/
- API Port: 8080 (if enabled)

Usage:
    python run_client_a.py
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
    """Launch Client A (master instance)"""
    logger.info("=" * 80)
    logger.info("pyWATS Client A (Master Instance)")
    logger.info("=" * 80)
    logger.info("Instance ID: default")
    logger.info("=" * 80)
    
    try:
        from PySide6.QtWidgets import QApplication
        from pywats_client.core.config import ClientConfig
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("pyWATS Client A")
        app.setOrganizationName("pyWATS")
        
        # Load or create config for instance "default"
        instance_id = "default"
        config_path = Path.home() / ".pywats" / "instances" / instance_id / "client_config.json"
        
        if config_path.exists():
            config = ClientConfig.load(config_path)
            logger.info(f"Loaded config from: {config_path}")
        else:
            logger.info("Creating new config for Client A")
            config = ClientConfig(instance_id=instance_id)
            config.instance_name = "Client A (Master)"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config._config_path = config_path
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
        
        return app.exec()
        
    except Exception as e:
        logger.error(f"Failed to launch Client A: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
