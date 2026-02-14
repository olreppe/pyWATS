"""
Test: Service Survives GUI Crashes

This script demonstrates that services run independently and survive GUI crashes.

Test Steps:
1. Start service via command line (no GUI)
2. Check service is running
3. "Crash" by exiting this script
4. Service should still be running
5. Stop service manually

Expected Result:
- Service keeps running even after script exits
- Service can be stopped from another process
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pywats_client.core import service_manager


def test_service_independence():
    """Test that service runs independently of launcher process."""
    
    instance_id = "default"
    
    print("=" * 80)
    print("TEST: Service Independence (Survives GUI Crashes)")
    print("=" * 80)
    print()
    
    # Step 1: Check current status
    print("Step 1: Check current service status...")
    status = service_manager.get_service_status(instance_id)
    print(f"  Status: {status}")
    
    if status.is_running:
        print(f"  ⚠ Service is already running (PID: {status.pid})")
        print(f"  Stopping existing service first...")
        service_manager.stop_service(instance_id)
        time.sleep(2)
    
    # Step 2: Start service
    print()
    print("Step 2: Starting service as independent process...")
    if service_manager.start_service(instance_id, wait=False):
        print("  ✓ Service started successfully")
    else:
        print("  ✗ Failed to start service")
        return False
    
    time.sleep(2)  # Wait for service to initialize
    
    # Step 3: Verify service is running
    print()
    print("Step 3: Verify service is running...")
    status = service_manager.get_service_status(instance_id)
    if status.is_running:
        print(f"  ✓ Service is running (PID: {status.pid})")
        print(f"  Instance: {status.instance_name}")
        print(f"  Started: {status.started_at}")
        if status.started_at:
            uptime = service_manager.get_uptime(status.started_at)
            print(f"  Uptime: {uptime}")
    else:
        print("  ✗ Service failed to start")
        return False
    
    # Step 4: Simulate crash (exit script)
    print()
    print("Step 4: Simulating GUI crash (exiting this script)...")
    print("  The service should continue running in the background")
    print()
    print("=" * 80)
    print("VERIFY:")
    print("  1. This script will exit in 5 seconds")
    print("  2. Check service status with:")
    print(f"     python -c \"from pywats_client.core import service_manager; print(service_manager.get_service_status('{instance_id}'))\"")
    print("  3. Stop service with:")
    print(f"     python -c \"from pywats_client.core import service_manager; service_manager.stop_service('{instance_id}')\"")
    print("=" * 80)
    
    for i in range(5, 0, -1):
        print(f"  Exiting in {i}...", end="\r")
        time.sleep(1)
    
    print()
    print("  ✓ Script exited - Service should still be running!")
    print()
    return True


if __name__ == "__main__":
    try:
        success = test_service_independence()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Test interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
