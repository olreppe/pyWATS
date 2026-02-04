"""
Standalone launcher for the new Configurator GUI (Client B only)

This runs ONLY the new pywats_ui configurator without loading
any old GUI code, avoiding potential conflicts.
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)

logger = logging.getLogger(__name__)


def main():
    """Launch the new configurator GUI standalone"""
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        from pywats_client.core.config import ClientConfig
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        
        logger.info("=" * 60)
        logger.info("pyWATS New Configurator GUI (Standalone)")
        logger.info("=" * 60)
        logger.info(f"Instance: default")
        logger.info("=" * 60)
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("pyWATS Configurator")
        app.setOrganizationName("pyWATS")
        
        # High DPI settings (ignore deprecation warnings for now)
        try:
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        except:
            pass  # These might not be available on all Qt versions
        
        # Load or create config
        logger.info("Loading configuration...")
        
        try:
            from pywats_client.core.config_manager import ConfigManager
            config_manager = ConfigManager(instance_id="default")
            config = config_manager.load_config()
            logger.info(f"✓ Loaded existing config for instance 'default'")
        except Exception as e:
            logger.info(f"ℹ Creating new config (no existing config found)")
            config = ClientConfig(instance_id="default")
        
        # Create and show main window
        logger.info("Creating main window...")
        window = ConfiguratorMainWindow(config=config)
        window.show()
        
        logger.info("✓ New Configurator GUI launched successfully!")
        logger.info("=" * 60)
        
        # Run event loop
        sys.exit(app.exec())
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("Make sure pywats_ui is installed and all dependencies are available")
        return 1
    except Exception as e:
        logger.error(f"❌ Failed to launch: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
