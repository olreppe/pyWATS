"""Side-by-side GUI test fixture for comparing old (A) and new (B) GUIs.

Usage:
    python test_both_guis.py                  # Launch both GUIs with default instance
    python test_both_guis.py --instance dev   # Launch with specific instance name

Features:
- Client A: Old GUI (pywats_client/gui) - Production stable version
- Client B: New GUI (pywats_ui/apps/configurator) - Improved reliability version
- Token sharing: Client B reads token from Client A if B's token is missing
- Separate config instances to prevent conflicts
- Easy comparison of features and reliability
"""

import sys
import asyncio
import logging
import argparse
from pathlib import Path
from typing import Optional

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

# qasync for async support
try:
    import qasync
except ImportError:
    print("Error: qasync is required but not installed.")
    print("Install with: pip install qasync")
    sys.exit(1)

# pyWATS imports
from pywats_client.core.config import ClientConfig

logger = logging.getLogger(__name__)


def setup_logging():
    """Configure logging for test fixture"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )


def get_old_gui_token(instance_name: str) -> Optional[str]:
    """
    Get token from old GUI (Client A) configuration.
    
    Args:
        instance_name: Instance name for the config
        
    Returns:
        Token string if found, None otherwise
    """
    try:
        # Load old GUI config
        config_a = ClientConfig(instance=instance_name)
        token = config_a.get("api_token")
        
        if token:
            logger.info(f"✓ Found token in Client A config (length: {len(token)})")
            return token
        else:
            logger.info("ℹ No token found in Client A config")
            return None
    except Exception as e:
        logger.warning(f"Could not read Client A config: {e}")
        return None


def share_token_to_new_gui(instance_name: str) -> bool:
    """
    Share token from old GUI (A) to new GUI (B) if B is missing one.
    
    Args:
        instance_name: Instance name for configs
        
    Returns:
        True if token was shared, False otherwise
    """
    try:
        # Load new GUI config
        config_b = ClientConfig(instance=f"{instance_name}_new")
        
        # Check if B already has a token
        token_b = config_b.get("api_token")
        if token_b:
            logger.info("✓ Client B already has a token")
            return False
        
        # Get token from A
        token_a = get_old_gui_token(instance_name)
        if not token_a:
            logger.info("ℹ No token to share from Client A")
            return False
        
        # Share token to B
        config_b.set("api_token", token_a)
        config_b.save()
        
        logger.info("✓ Token shared from Client A to Client B")
        return True
        
    except Exception as e:
        logger.error(f"Failed to share token: {e}")
        return False


def launch_old_gui(instance_name: str, event_loop) -> bool:
    """
    Launch old GUI (Client A) in a separate window.
    
    Args:
        instance_name: Instance name for the config
        event_loop: qasync event loop
        
    Returns:
        True if launched successfully
    """
    try:
        logger.info("Launching Client A (Old GUI)...")
        
        # Import old GUI main window
        from pywats_client.gui.main_window import MainWindow
        
        # Load config for Client A
        config_a = ClientConfig(instance=instance_name)
        
        # Create and show window
        window_a = MainWindow(config=config_a)
        window_a.setWindowTitle(f"pyWATS Client A (Original) - {instance_name}")
        window_a.show()
        
        # Position on left side of screen
        window_a.move(50, 50)
        
        logger.info("✓ Client A launched successfully")
        return True
        
    except Exception as e:
        logger.exception(f"Failed to launch Client A: {e}")
        QMessageBox.critical(
            None,
            "Launch Error",
            f"Failed to launch old GUI (Client A):\n\n{e}"
        )
        return False


def launch_new_gui(instance_name: str, event_loop) -> bool:
    """
    Launch new GUI (Client B) in a separate window.
    
    Args:
        instance_name: Instance name for the config
        event_loop: qasync event loop
        
    Returns:
        True if launched successfully
    """
    try:
        logger.info("Launching Client B (New GUI)...")
        
        # Import new GUI main window
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        
        # Load config for Client B (separate instance to avoid conflicts)
        config_b = ClientConfig(instance=f"{instance_name}_new")
        config_b.set("instance_name", f"{instance_name} (New)")
        
        # Create and show window
        window_b = ConfiguratorMainWindow(config=config_b)
        window_b.setWindowTitle(f"pyWATS Client B (Improved) - {instance_name}")
        window_b.show()
        
        # Position on right side of screen (offset from A)
        window_b.move(700, 50)
        
        logger.info("✓ Client B launched successfully")
        return True
        
    except Exception as e:
        logger.exception(f"Failed to launch Client B: {e}")
        QMessageBox.critical(
            None,
            "Launch Error",
            f"Failed to launch new GUI (Client B):\n\n{e}"
        )
        return False


def main():
    """Main entry point"""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Launch old (A) and new (B) GUIs side-by-side for comparison"
    )
    parser.add_argument(
        "--instance",
        default="default",
        help="Instance name for configurations (default: 'default')"
    )
    parser.add_argument(
        "--no-token-share",
        action="store_true",
        help="Skip automatic token sharing from A to B"
    )
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    logger.info("="*60)
    logger.info("pyWATS Side-by-Side GUI Test Fixture")
    logger.info("="*60)
    logger.info(f"Instance: {args.instance}")
    logger.info(f"Client A: Old GUI (pywats_client.gui)")
    logger.info(f"Client B: New GUI (pywats_ui.apps.configurator)")
    logger.info("="*60)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Enable high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Setup async event loop
    event_loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    
    # Share token from A to B if enabled
    if not args.no_token_share:
        logger.info("\nChecking token sharing...")
        shared = share_token_to_new_gui(args.instance)
        if shared:
            logger.info("✓ Token sharing complete\n")
        else:
            logger.info("ℹ Token sharing not needed\n")
    
    # Launch both GUIs
    success_a = launch_old_gui(args.instance, event_loop)
    success_b = launch_new_gui(args.instance, event_loop)
    
    if not success_a and not success_b:
        logger.error("Failed to launch both GUIs. Exiting.")
        return 1
    
    if not success_a:
        logger.warning("Client A failed to launch, but Client B is running")
    
    if not success_b:
        logger.warning("Client B failed to launch, but Client A is running")
    
    logger.info("\n" + "="*60)
    logger.info("Both GUIs launched successfully!")
    logger.info("Compare features, reliability, and UI improvements.")
    logger.info("="*60 + "\n")
    
    # Run event loop
    try:
        with event_loop:
            event_loop.run_forever()
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
