"""
Test script to start the pyWATS service without GUI
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pywats_client.app import pyWATSApplication
from pywats_client.core.config import ClientConfig


async def test_service():
    """Test starting and checking the service"""
    print("=" * 80)
    print("TESTING PYWATS SERVICE START")
    print("=" * 80)
    
    # Load config
    print("\n1. Loading configuration...")
    config_path = Path.home() / ".pywats" / "client_config.json"
    if not config_path.exists():
        print(f"   Config not found at {config_path}")
        print(f"   Creating default config...")
        config = ClientConfig()
    else:
        config = ClientConfig.load(config_path)
    print(f"   Config loaded: {config.instance_name}")
    print(f"   Service address: {config.service_address}")
    
    # Create application
    print("\n2. Creating pyWATS application...")
    app = pyWATSApplication(config)
    print(f"   Initial status: {app.status.value}")
    
    # Start the service
    print("\n3. Starting service...")
    try:
        await app.start()
        print(f"   Service started successfully!")
        print(f"   Status: {app.status.value}")
        print(f"   Online: {app.is_online()}")
        
        # Check services
        if app.connection:
            print(f"   Connection status: {app.connection.status.value}")
        
        if app._ipc_server:
            print(f"   IPC server running: {app._ipc_server._server is not None}")
            
        # Wait a moment
        print("\n4. Waiting 5 seconds...")
        await asyncio.sleep(5)
        
        # Check again
        print(f"\n5. Status after 5 seconds:")
        print(f"   Status: {app.status.value}")
        print(f"   Online: {app.is_online()}")
        
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Stop the service
    print("\n6. Stopping service...")
    try:
        await app.stop()
        print(f"   Service stopped")
        print(f"   Final status: {app.status.value}")
    except Exception as e:
        print(f"   ERROR during stop: {e}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_service())
