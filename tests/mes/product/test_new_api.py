"""
Test the new PyWATS API with proper configuration-driven setup
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from pyWATS import PyWATSAPI, create_api


def test_new_api():
    """Test the new PyWATS API setup"""
    print("🚀 Testing new PyWATS API...")
    print()
    
    # Method 1: Use the create_api convenience function
    print("=" * 50)
    print("Method 1: Using create_api() convenience function")
    print("=" * 50)
    
    api = create_api()
    print()
    print("API Info:")
    server_info = api.get_server_info()
    for key, value in server_info.items():
        print(f"  {key}: {value}")
    
    print()
    print("=" * 50)
    print("Method 2: Manual PyWATSAPI creation")
    print("=" * 50)
    
    # Method 2: Create manually and test connection
    api2 = PyWATSAPI()
    connection_success = api2.test_connection()
    
    print(f"Connection test result: {connection_success}")
    print(f"API representation: {api2}")
    
    # Method 3: Show that we have access to the TDM client
    print()
    print("=" * 50)
    print("Method 3: Accessing TDM client for operations")
    print("=" * 50)
    
    if api2.tdm_client:
        print("✅ TDM client is available!")
        print(f"   Status: {api2.tdm_client.status}")
        print(f"   Station: {api2.tdm_client.station_name}")
        print(f"   Location: {api2.tdm_client.location}")
        print(f"   Purpose: {api2.tdm_client.purpose}")
        
        # Test a simple TDM operation
        try:
            print("\nTesting metadata operations...")
            operation_types = api2.tdm_client.get_operation_types()
            print(f"✅ Retrieved {len(operation_types)} operation types")
        except Exception as e:
            print(f"⚠️ Operation types failed: {e}")
            
    else:
        print("❌ TDM client not available")
    
    print()
    print("🏁 API test complete!")


if __name__ == "__main__":
    test_new_api()