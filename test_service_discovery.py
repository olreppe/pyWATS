"""
Test service discovery - start service then check if GUI can find it
"""
import asyncio
import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pywats_client.app import pyWATSApplication
from pywats_client.core.config import ClientConfig
from pywats_client.services.ipc import ServiceIPCClient


async def test_discovery():
    """Test that a running service can be discovered"""
    print("=" * 80)
    print("TESTING SERVICE DISCOVERY")
    print("=" * 80)
    
    # Load config
    config_path = Path.home() / ".pywats" / "client_config.json"
    if not config_path.exists():
        config = ClientConfig()
    else:
        config = ClientConfig.load(config_path)
    
    # Start service
    print("\n1. Starting service...")
    app = pyWATSApplication(config)
    await app.start()
    print(f"   Service running with IPC name: pyWATS_Service_{config.instance_id}")
    
    # Wait a moment for IPC server to be ready
    await asyncio.sleep(1)
    
    # Try to discover it
    print("\n2. Attempting to discover service...")
    from pywats_client.services.ipc import ServiceDiscovery
    instances = ServiceDiscovery.discover_instances()
    
    print(f"   Found {len(instances)} service instance(s)")
    for inst in instances:
        print(f"   - Instance: {inst['instance_id']}")
        print(f"     Status: {inst['status']}")
        print(f"     IPC Name: {inst['ipc_name']}")
    
    # Stop service
    print("\n3. Stopping service...")
    await app.stop()
    
    print("\n" + "=" * 80)
    if len(instances) > 0:
        print("SUCCESS: Service was discoverable!")
    else:
        print("FAILED: Service was NOT discoverable")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_discovery())
