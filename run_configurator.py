#!/usr/bin/env python3
"""Entry point for pyWATS Configurator application.

Usage:
    python run_configurator.py [--instance NAME]

Example:
    python run_configurator.py --instance Production-Line-1
"""

import sys
import os
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for configurator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="pyWATS Configurator")
    parser.add_argument(
        "--instance",
        default=None,
        help="Instance name (e.g., Production-Line-1)"
    )
    parser.add_argument(
        "--select-instance",
        action="store_true",
        help="Show instance selector dialog on startup"
    )
    
    args = parser.parse_args()
    
    try:
        # Import Qt
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        import qasync
        
        # Import configurator components
        from pywats_client.core.config import ClientConfig
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow, show_instance_selector
        
        # Enable high DPI scaling
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("pyWATS Configurator")
        app.setOrganizationName("Virinco")
        app.setOrganizationDomain("wats.com")
        
        # Setup async event loop
        loop = qasync.QEventLoop(app)
        import asyncio
        asyncio.set_event_loop(loop)
        
        # Determine instance name
        instance_name = args.instance
        
        if args.select_instance or not instance_name:
            # Get list of instances from C:\ProgramData\pyWATS\instances\ (system-wide)
            if os.name == 'nt':
                instances_dir = Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / 'pyWATS' / 'instances'
            else:
                instances_dir = Path('/var/lib/pywats/instances')
            
            available_configs = []
            if instances_dir.exists():
                available_configs = list(instances_dir.glob("*/client_config.json"))
            
            if not available_configs:
                # No existing instances - use default
                instance_name = "default"
                logger.info("No existing instances found, using default")
            elif len(available_configs) == 1:
                # Only one instance - auto-select it
                config_path = available_configs[0]
                temp_config = ClientConfig.load(config_path)
                instance_name = temp_config.instance_name or temp_config.instance_id or "default"
                logger.info(f"Auto-selected only instance: {instance_name}")
            else:
                # Multiple instances - show selector
                temp_config = ClientConfig()
                instance_name = show_instance_selector(temp_config, available_configs)
                if not instance_name:
                    logger.info("Instance selection cancelled, exiting")
                    return 0
        
        # Load config from C:\ProgramData\pyWATS\instances\{instance_id}\ (system-wide)
        # Map display name to instance_id
        instance_id_map = {
            "Client A (Master)": "default",
            "Client B (Secondary)": "client_b",
            "Test Instance": "default",
        }
        instance_id = instance_id_map.get(instance_name, instance_name.lower().replace(" ", "_"))
        
        if os.name == 'nt':
            base_path = Path(os.environ.get('PROGRAMDATA', 'C:\\ProgramData')) / 'pyWATS' / 'instances'
        else:
            base_path = Path('/var/lib/pywats/instances')
        
        config_path = base_path / instance_id / "client_config.json"
        
        if config_path.exists():
            config = ClientConfig.load(config_path)
            logger.info(f"Loaded config from: {config_path}")
        else:
            logger.info(f"Creating new instance: {instance_id}")
            config = ClientConfig(instance_id=instance_id)
            config.instance_name = instance_name
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config._config_path = config_path
            config.save()
            logger.info(f"Config saved to: {config_path}")
        
        logger.info(f"Starting configurator for instance: {config.instance_name} ({instance_id})")
        
        # Create and show main window
        window = ConfiguratorMainWindow(config)
        window.show()
        
        # Run event loop
        with loop:
            exit_code = loop.run_forever()
        
        return exit_code
        
    except ImportError as e:
        logger.error(f"Missing required dependencies: {e}")
        logger.error("Install with: pip install PySide6 qasync")
        return 1
        
    except Exception as e:
        logger.exception(f"Failed to start configurator: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
