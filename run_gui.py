#!/usr/bin/env python
"""
Start pyWATS GUI with test Client A credentials.
"""
import sys
from pathlib import Path

# Add src to path so we can import pywats_client
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pywats_client.core.config import ClientConfig
from pywats_client.core.connection_config import ConnectionConfig, ConnectionState
from pywats_client.gui.app import run_gui

if __name__ == "__main__":
    # Load Client A test config
    config_path = Path(__file__).parent / "tests" / "fixtures" / "instances" / "client_a_config.json"
    
    if config_path.exists():
        print(f"Loading test config: {config_path.name}")
        try:
            config = ClientConfig.load(config_path)
            print(f"✓ Config loaded")
            print(f"  - Service: {config.service_address}")
            print(f"  - Station: {config.station_name}")
            print(f"  - Instance: {config.instance_id}")
            
            # Set up connection config with credentials
            connection = ConnectionConfig(
                server_url=config.service_address,
                username="test_user",
                token_encrypted=config.api_token,  # Store token directly
                connection_state=ConnectionState.CONNECTED.value
            )
            config.connection = connection
            
            print(f"✓ Connection config prepared (authenticated)")
            print()
            print("Starting GUI with Client A credentials...")
        except Exception as e:
            print(f"Error loading config: {e}")
            import traceback
            traceback.print_exc()
            config = None
    else:
        print(f"Config not found at {config_path}")
        config = None
    
    # Start GUI with loaded config
    exit_code = run_gui(config=config) if config else run_gui()
    sys.exit(exit_code)
