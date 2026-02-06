"""Dual instance test fixture for Client A (master) and Client B (secondary).

Usage:
    python test_both_guis.py              # Launch both instances side-by-side
    python test_both_guis.py --only-a     # Launch only Client A
    python test_both_guis.py --only-b     # Launch only Client B

Features:
- Client A: Master instance (instance_id="default") - Primary testing instance
- Client B: Secondary instance (instance_id="client_b") - Multi-instance testing
- Token sharing: Client B inherits token from Client A if B's token is missing
- Separate configs to prevent conflicts
- Instance-isolated: queue, logs, reports, converters
- Easy multi-instance testing
"""

import sys
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Optional

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMessageBox

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


def get_client_a_token() -> Optional[str]:
    """
    Get token from Client A (master) configuration.
    
    Returns:
        Token string if found, None otherwise
    """
    try:
        # Load Client A config (instance_id="default")
        config_path = Path.home() / ".pywats" / "instances" / "default" / "client_config.json"
        if not config_path.exists():
            logger.info("Client A config not found")
            return None
            
        config_a = ClientConfig.load(config_path)
        token = getattr(config_a, 'api_token', None)
        
        if token:
            logger.info(f"Found token in Client A config (length: {len(token)})")
            return token
        else:
            logger.info("No token found in Client A config")
            return None
    except Exception as e:
        logger.warning(f"Could not read Client A config: {e}")
        return None


def share_token_to_client_b() -> bool:
    """
    Share token from Client A to Client B if B is missing one.
    
    Returns:
        True if token was shared, False otherwise
    """
    try:
        # Load Client B config
        config_path_b = Path.home() / ".pywats" / "instances" / "client_b" / "client_config.json"
        if not config_path_b.exists():
            logger.info("Client B config not found, will create on first launch")
            return False
            
        config_b = ClientConfig.load(config_path_b)
        
        # Check if B already has a token
        token_b = getattr(config_b, 'api_token', None)
        if token_b:
            logger.info("Client B already has a token")
            return False
        
        # Get token from A
        token_a = get_client_a_token()
        if not token_a:
            logger.info("No token to share from Client A")
            return False
        
        # Share token to B
        config_b.api_token = token_a
        config_b.save()
        
        logger.info("Token shared from Client A to Client B")
        return True
        
    except Exception as e:
        logger.error(f"Failed to share token: {e}")
        return False


def launch_client_a() -> bool:
    """
    Launch Client A (master instance) in a separate window.
    
    Returns:
        True if launched successfully
    """
    try:
        logger.info("Launching Client A (Master Instance)...")
        
        # Import new GUI main window
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        
        # Load or create config for Client A (instance_id="default")
        instance_id = "default"
        config_path = Path.home() / ".pywats" / "instances" / instance_id / "client_config.json"
        
        if config_path.exists():
            config_a = ClientConfig.load(config_path)
        else:
            config_a = ClientConfig(instance_id=instance_id)
            config_a.instance_name = "Client A (Master)"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_a._config_path = config_path
            config_a.save()
        
        # Create and show window
        window_a = ConfiguratorMainWindow(config=config_a)
        window_a.setWindowTitle(f"pyWATS Client A (Master) - {instance_id}")
        window_a.show()
        
        # Position on left side of screen
        window_a.move(50, 50)
        
        logger.info("Client A launched successfully")
        return True
        
    except Exception as e:
        logger.exception(f"Failed to launch Client A: {e}")
        QMessageBox.critical(
            None,
            "Launch Error",
            f"Failed to launch Client A:\n\n{e}"
        )
        return False


def launch_client_b() -> bool:
    """
    Launch Client B (secondary instance) in a separate window.
    
    Returns:
        True if launched successfully
    """
    try:
        logger.info("Launching Client B (Secondary Instance)...")
        
        # Import new GUI main window
        from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
        
        # Load or create config for Client B (instance_id="client_b")
        instance_id = "client_b"
        config_path = Path.home() / ".pywats" / "instances" / instance_id / "client_config.json"
        
        if config_path.exists():
            config_b = ClientConfig.load(config_path)
        else:
            config_b = ClientConfig(instance_id=instance_id)
            config_b.instance_name = "Client B (Secondary)"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_b._config_path = config_path
            
            # Token sharing: inherit from Client A if B has no token
            token_a = get_client_a_token()
            if token_a:
                config_b.api_token = token_a
                logger.info("Inherited API token from Client A")
            
            config_b.save()
        
        # Create and show window
        window_b = ConfiguratorMainWindow(config=config_b)
        window_b.setWindowTitle(f"pyWATS Client B (Secondary) - {instance_id}")
        window_b.show()
        
        # Position on right side of screen (offset from A)
        window_b.move(700, 50)
        
        logger.info("Client B launched successfully")
        return True
        
    except Exception as e:
        logger.exception(f"Failed to launch Client B: {e}")
        QMessageBox.critical(
            None,
            "Launch Error",
            f"Failed to launch Client B:\n\n{e}"
        )
        return False


def main():
    """Main entry point"""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Launch Client A (master) and Client B (secondary) side-by-side"
    )
    parser.add_argument(
        "--only-a",
        action="store_true",
        help="Launch only Client A (master instance)"
    )
    parser.add_argument(
        "--only-b",
        action="store_true",
        help="Launch only Client B (secondary instance)"
    )
    parser.add_argument(
        "--no-token-share",
        action="store_true",
        help="Skip automatic token sharing from A to B"
    )
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    logger.info("="*80)
    logger.info("pyWATS Dual Instance Test Fixture")
    logger.info("="*80)
    logger.info("Client A: Master instance (instance_id='default')")
    logger.info("Client B: Secondary instance (instance_id='client_b')")
    logger.info("="*80)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Share token from A to B if enabled
    if not args.no_token_share and not args.only_a:
        logger.info("\nChecking token sharing...")
        shared = share_token_to_client_b()
        if shared:
            logger.info("Token sharing complete\n")
        else:
            logger.info("Token sharing not needed\n")
    
    # Launch GUIs based on arguments
    success_a = True
    success_b = True
    
    if not args.only_b:
        success_a = launch_client_a()
    
    if not args.only_a:
        success_b = launch_client_b()
    
    if not success_a and not success_b:
        logger.error("Failed to launch any GUIs. Exiting.")
        return 1
    
    if not success_a and not args.only_b:
        logger.warning("Client A failed to launch, but Client B is running")
    
    if not success_b and not args.only_a:
        logger.warning("Client B failed to launch, but Client A is running")
    
    logger.info("\n" + "="*80)
    if args.only_a:
        logger.info("Client A launched successfully!")
    elif args.only_b:
        logger.info("Client B launched successfully!")
    else:
        logger.info("Both instances launched successfully!")
    logger.info("="*80 + "\n")
    
    # Run event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

    
    return 0


if __name__ == "__main__":
    sys.exit(main())
