#!/usr/bin/env python3
"""Setup test configuration with server connection.

Creates a test instance with server URL and API token configured.
"""
import sys
from pathlib import Path

def main():
    """Create test configuration"""
    from pywats_client.core.config import ClientConfig
    
    print("=" * 60)
    print("pyWATS Test Configuration Setup")
    print("=" * 60)
    
    # Create test instance
    instance_id = "default"
    config = ClientConfig.load_for_instance(instance_id)
    
    # Configure for testing
    config.instance_name = "Test Instance"
    config.service_address = "https://wats.virinco.com"  # Default test server
    config.api_token = "your-api-token-here"  # User should replace this
    config.station_name = "Test-Station-1"
    config.location = "Test Lab"
    config.purpose = "Development & Testing"
    
    # Save configuration
    config.save()
    
    print(f"\n✓ Test configuration created!")
    print(f"  Instance: {config.instance_name}")
    print(f"  Server: {config.service_address}")
    print(f"  Station: {config.station_name}")
    print(f"  Config file: {config._config_path}")
    print("\n⚠️  IMPORTANT: Edit the API token in the Configurator")
    print(f"  Go to Connection tab and set your API token")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
