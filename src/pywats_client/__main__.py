"""
pyWATS Client Entry Point

Run the client with:
    python -m pywats_client

Or use the installed command:
    pywats-client
"""

import sys
import asyncio
import argparse
from pathlib import Path


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="pyWATS Client - WATS Test Report Management"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to configuration file"
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Run in headless mode without GUI"
    )
    parser.add_argument(
        "--instance-name",
        type=str,
        help="Instance name for this client"
    )
    parser.add_argument(
        "--service-address",
        type=str,
        help="WATS service address"
    )
    parser.add_argument(
        "--api-token",
        type=str,
        help="API token for authentication"
    )
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version and exit"
    )
    
    args = parser.parse_args()
    
    # Show version
    if args.version:
        from . import __version__
        print(f"pyWATS Client v{__version__}")
        sys.exit(0)
    
    # Load or create configuration
    from .core.config import ClientConfig
    
    if args.config:
        config_path = Path(args.config)
        config = ClientConfig.load_or_create(config_path)
    else:
        # Use default config location
        config_dir = Path.home() / ".pywats_client"
        config_path = config_dir / "config.json"
        config = ClientConfig.load_or_create(config_path)
    
    # Apply command line overrides
    if args.instance_name:
        config.instance_name = args.instance_name
    if args.service_address:
        config.service_address = args.service_address
    if args.api_token:
        config.api_token = args.api_token
    
    # Run client
    if args.no_gui:
        # Headless mode - run client without GUI
        from .core.client import WATSClient
        
        async def run_headless():
            client = WATSClient(config)
            try:
                await client.start()
                # Keep running until interrupted
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down...")
            finally:
                await client.stop()
        
        asyncio.run(run_headless())
    else:
        # GUI mode
        from .gui.app import run_gui
        run_gui(config)


if __name__ == "__main__":
    main()
