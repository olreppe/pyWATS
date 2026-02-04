"""
Debug launcher for new Configurator GUI with maximum logging

Captures all errors to both console and log file for analysis.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Create logs directory
log_dir = Path("debug_logs")
log_dir.mkdir(exist_ok=True)

# Create timestamped log file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = log_dir / f"gui_debug_{timestamp}.log"

# Setup comprehensive logging with UTF-8 console output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
# Force UTF-8 encoding for console to handle Unicode symbols
console_handler.stream = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

logging.basicConfig(
    level=logging.DEBUG,  # Maximum verbosity
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        console_handler
    ]
)

logger = logging.getLogger(__name__)

# Enable asyncio debug mode
import os
os.environ['PYTHONASYNCIODEBUG'] = '1'

# Log uncaught exceptions
def exception_handler(exc_type, exc_value, exc_traceback):
    """Log uncaught exceptions"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = exception_handler


def main():
    """Launch the new configurator GUI with full debug logging"""
    logger.info("=" * 80)
    logger.info("pyWATS New Configurator GUI - DEBUG MODE")
    logger.info("=" * 80)
    logger.info(f"Log file: {log_file.absolute()}")
    logger.info(f"Python: {sys.version}")
    logger.info(f"Working directory: {Path.cwd()}")
    logger.info("=" * 80)
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt, qInstallMessageHandler, QtMsgType
        try:
            from PySide6.QtCore import QT_VERSION_STR
            logger.info(f"Qt version: {QT_VERSION_STR}")
        except ImportError:
            logger.info("Qt version: (version string not available)")
        
        # Qt message handler for Qt warnings/errors
        def qt_message_handler(mode, context, message):
            if mode == QtMsgType.QtDebugMsg:
                logger.debug(f"Qt: {message}")
            elif mode == QtMsgType.QtInfoMsg:
                logger.info(f"Qt: {message}")
            elif mode == QtMsgType.QtWarningMsg:
                logger.warning(f"Qt: {message}")
            elif mode == QtMsgType.QtCriticalMsg:
                logger.error(f"Qt: {message}")
            elif mode == QtMsgType.QtFatalMsg:
                logger.critical(f"Qt: {message}")
        
        qInstallMessageHandler(qt_message_handler)
        
        # Import and check components
        logger.info("Importing pywats_client components...")
        from pywats_client.core.config import ClientConfig
        from pywats_client.core.config_manager import ConfigManager
        logger.info("✓ pywats_client imports successful")
        
        logger.info("Importing pywats_ui components...")
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        logger.info("✓ pywats_ui imports successful")
        
        # Create Qt application
        logger.info("Creating Qt application...")
        app = QApplication(sys.argv)
        app.setApplicationName("pyWATS Configurator Debug")
        app.setOrganizationName("pyWATS")
        logger.info("✓ Qt application created")
        
        # Load configuration using ClientConfig directly
        logger.info("Loading configuration for instance 'default'...")
        try:
            # Try to load existing config
            config_path = Path.home() / ".pywats" / "instances" / "default" / "client_config.json"
            
            if config_path.exists():
                config = ClientConfig.load_from_file(config_path)
                logger.info(f"✓ Config loaded from: {config_path}")
            else:
                logger.info("No existing config found, creating new config")
                config = ClientConfig(instance_id="default")
                # Create config directory
                config_path.parent.mkdir(parents=True, exist_ok=True)
                # Save to establish config path
                config._config_path = config_path
                config.save()
                logger.info(f"✓ New config created at: {config_path}")
            
            logger.info(f"  - API URL: {config.service_address or '(not set)'}")
            logger.info(f"  - Token: {'SET' if config.api_token else 'NOT SET'}")
            logger.info(f"  - Station: {config.station_name or '(not set)'}")
            logger.info(f"  - Converters enabled: {config.converters_enabled}")
            logger.info(f"  - Number of converters: {len(config.converters)}")
            
        except Exception as e:
            logger.error(f"Failed to load config: {e}", exc_info=True)
            return 1
        
        # Create main window
        logger.info("Creating ConfiguratorMainWindow...")
        try:
            window = ConfiguratorMainWindow(config=config)
            logger.info("✓ Main window created")
        except Exception as e:
            logger.error(f"Failed to create main window: {e}", exc_info=True)
            return 1
        
        # Show window
        logger.info("Showing main window...")
        window.show()
        logger.info("✓ Window shown")
        
        logger.info("=" * 80)
        logger.info("GUI LAUNCHED SUCCESSFULLY - Entering event loop")
        logger.info(f"All output logged to: {log_file.absolute()}")
        logger.info("=" * 80)
        
        # Run event loop
        exit_code = app.exec()
        
        logger.info("=" * 80)
        logger.info(f"Application exited with code: {exit_code}")
        logger.info("=" * 80)
        
        return exit_code
        
    except ImportError as e:
        logger.error(f"Import error: {e}", exc_info=True)
        logger.error("Make sure all dependencies are installed:")
        logger.error("  pip install PySide6 qasync")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
