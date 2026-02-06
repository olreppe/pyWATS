#!/usr/bin/env python
"""
Start pyWATS GUI (New Configurator) with Client A credentials.

This launcher uses the new GUI (pywats_ui) for Client A testing.
The old GUI has been removed as part of the migration.

For dual instance testing, use:
- run_client_a.py - Client A (master instance)
- run_client_b.py - Client B (secondary instance)  
- test_both_guis.py - Both instances side-by-side
"""
import sys
from pathlib import Path

# Add src to path so we can import pywats modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication
from pywats_client.core.config import ClientConfig
from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow

if __name__ == "__main__":
    # Load Client A test config
    config_path = Path(__file__).parent / "tests" / "fixtures" / "instances" / "client_a_config.json"
    
    if config_path.exists():
        print(f"Loading test config: {config_path.name}")
        try:
            config = ClientConfig.load(config_path)
            print(f"Config loaded")
            print(f"  - Service: {config.service_address}")
            print(f"  - Station: {config.station_name}")
            print(f"  - Instance: {config.instance_id}")
            print()
            print("Starting GUI with Client A credentials...")
        except Exception as e:
            print(f"Error loading config: {e}")
            import traceback
            traceback.print_exc()
            config = None
    else:
        print(f"Config not found at {config_path}, using default")
        config = ClientConfig(instance_id="default")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("pyWATS")
    app.setOrganizationName("pyWATS")
    
    # Create main window with config
    window = ConfiguratorMainWindow(config=config)
    window.setWindowTitle("pyWATS Configurator (Client A)")
    window.show()
    
    # Start event loop
    exit_code = app.exec()
    sys.exit(exit_code)
