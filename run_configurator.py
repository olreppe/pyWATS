#!/usr/bin/env python3
"""Entry point for pyWATS Configurator application.

Usage:
    python run_configurator.py [--instance NAME]

Example:
    python run_configurator.py --instance Production-Line-1
"""

import sys
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
            # Show instance selector (pass a temporary config for reading existing instances)
            temp_config = ClientConfig()
            instance_name = show_instance_selector(temp_config)
            if not instance_name:
                logger.info("Instance selection cancelled, exiting")
                return 0
        
        # Load or create config for the selected instance
        instance_id = instance_name if instance_name else "default"
        config = ClientConfig.load_for_instance(instance_id)
        
        # Ensure instance_name is set in config
        if instance_name and config.get('instance_name') != instance_name:
            config["instance_name"] = instance_name
            config.save()
        
        logger.info(f"Starting configurator for instance: {config.get('instance_name', 'default')}")
        
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
