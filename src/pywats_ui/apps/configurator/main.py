"""Main entry point for pyWATS Client Configurator."""

import sys
from pathlib import Path
from pywats_ui.framework import BaseApplication
from .main_window import ConfiguratorMainWindow


def main(instance_id: str = "default"):
    """Entry point for pyWATS Client Configurator application.
    
    Args:
        instance_id: Client instance ID to configure (default: "default")
    """
    app = BaseApplication("pyWATS Client Configurator", "0.3.0")
    
    # Set up logging
    from pywats.core.logging import configure_logging
    configure_logging(
        level="INFO",
        file_path="pywats_configurator.log"
    )
    
    # Load or create client configuration
    from pywats_client.core.config import ClientConfig
    
    # Get config path for instance
    config_dir = Path.home() / ".pywats" / "instances" / instance_id
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "client_config.json"
    
    # Load config or create new one
    if config_path.exists():
        config = ClientConfig.load(config_path)
    else:
        config = ClientConfig(instance_id=instance_id)
        config.instance_name = f"Instance: {instance_id}"
        config._config_path = config_path
        config.save()
        
        # Ensure instance-specific directories
        (config_dir / "queue").mkdir(exist_ok=True)
        (config_dir / "logs").mkdir(exist_ok=True)
        (config_dir / "reports").mkdir(exist_ok=True)
        (config_dir / "converters").mkdir(exist_ok=True)
    
    # Create and show window
    window = ConfiguratorMainWindow(config)
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
