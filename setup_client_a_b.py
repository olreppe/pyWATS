#!/usr/bin/env python3
"""Setup Client A and Client B test instances.

Creates two separate instances for multi-instance testing.
"""
import sys
from pathlib import Path

def main():
    """Create Client A and B test configurations"""
    from pywats_client.core.config import ClientConfig
    
    print("=" * 60)
    print("Setting up Client A and Client B Test Instances")
    print("=" * 60)
    
    # Client A
    print("\n[1/2] Creating Client A...")
    config_a = ClientConfig.load_for_instance("client_a")
    config_a.instance_name = "Client A"
    config_a.instance_id = "client_a"
    config_a.service_address = "https://wats.virinco.com"
    config_a.api_token = "your-token-for-client-a"
    config_a.station_name = "Station-A"
    config_a.location = "Production Line 1"
    config_a.purpose = "ICT Testing"
    config_a.save()
    print(f"  ✓ Client A created: {config_a._config_path}")
    
    # Client B
    print("\n[2/2] Creating Client B...")
    config_b = ClientConfig.load_for_instance("client_b")
    config_b.instance_name = "Client B"
    config_b.instance_id = "client_b"
    config_b.service_address = "https://wats.virinco.com"
    config_b.api_token = "your-token-for-client-b"
    config_b.station_name = "Station-B"
    config_b.location = "Production Line 2"
    config_b.purpose = "FCT Testing"
    config_b.save()
    print(f"  ✓ Client B created: {config_b._config_path}")
    
    print("\n" + "=" * 60)
    print("✓ Setup complete!")
    print("\nYou now have two test instances:")
    print("  • Client A - Production Line 1 (ICT)")
    print("  • Client B - Production Line 2 (FCT)")
    print("\nNext steps:")
    print("  1. Run: python run_configurator.py")
    print("  2. Select instance from dropdown")
    print("  3. Set API tokens in Connection tab")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
