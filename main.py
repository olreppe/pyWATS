"""
pyWATS Main Example

This file demonstrates how to use the pyWATS library to connect to a WATS API
and perform basic operations on assets.
"""

import sys
import os

# Add src to path so we can import pyWATS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pyWATS.connection import create_connection
from pyWATS.rest_api.endpoints import asset
from pyWATS.rest_api.exceptions import WATSAPIException
import json


def main():
    """
    Main function demonstrating pyWATS usage.
    """
    # Example configuration - replace with your actual WATS server details
    BASE_URL = "https://ola.wats.com"
    AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
    
    print("[START] pyWATS API Example")
    print("=" * 50)
    
    try:
        # Create connection to WATS API
        print("[CONNECT] Connecting to WATS API...")
        connection = create_connection(
            base_url=BASE_URL,
            token=AUTH_TOKEN
        )
        
        # Test connection
        print("[TEST] Testing connection...")
        if connection.test_connection():
            print("[SUCCESS] Connection successful!")
        else:
            print("[ERROR] Connection failed!")
            return
        
        # Example 1: Get assets
        print("\n[EXAMPLE 1] Getting assets (top 5)...")
        assets = []  # Initialize to avoid unbound variable issues
        try:
            assets = asset.get_assets(odata_top=5)
            print(f"[SUCCESS] Retrieved {len(assets)} assets")
            
            if assets:
                print("   First asset:")
                first_asset = assets[0]
                print(f"   - ID: {first_asset.get('id', 'N/A')}")
                print(f"   - Serial Number: {first_asset.get('serialNumber', 'N/A')}")
                print(f"   - Name: {first_asset.get('name', 'N/A')}")
                print(f"   - State: {first_asset.get('state', 'N/A')}")
            else:
                print("   No assets found")
                
        except WATSAPIException as e:
            print(f"[ERROR] Error getting assets: {e}")
            print(f"   Status Code: {e.status_code}")
            print(f"   Response: {e.response}")
        
        # Example 2: Get asset types
        print("\n[EXAMPLE 2] Getting asset types (top 3)...")
        try:
            asset_types = asset.get_asset_types(odata_top=3)
            print(f"[SUCCESS] Retrieved {len(asset_types)} asset types")
            
            for i, asset_type in enumerate(asset_types, 1):
                print(f"   {i}. {asset_type.get('name', 'N/A')} (ID: {asset_type.get('id', 'N/A')})")
                
        except WATSAPIException as e:
            print(f"[ERROR] Error getting asset types: {e}")
            print(f"   Status Code: {e.status_code}")
            
        # Example 3: Get asset by serial number (if assets exist)
        if assets:
            first_asset_serial = assets[0].get('serialNumber')
            if first_asset_serial:
                print(f"\n[EXAMPLE 3] Getting asset by serial number '{first_asset_serial}'...")
                try:
                    specific_asset = asset.get_asset_by_serial_number(first_asset_serial)
                    print("[SUCCESS] Asset retrieved successfully!")
                    print(f"   Name: {specific_asset.get('name', 'N/A')}")
                    print(f"   Type: {specific_asset.get('assetTypeName', 'N/A')}")
                    print(f"   Total Count: {specific_asset.get('totalCount', 'N/A')}")
                    print(f"   Running Count: {specific_asset.get('runningCount', 'N/A')}")
                    
                except WATSAPIException as e:
                    print(f"[ERROR] Error getting asset by serial number: {e}")
                    print(f"   Status Code: {e.status_code}")
        
        # Example 4: Get asset log (recent entries)
        print("\n[EXAMPLE 4] Getting recent asset log entries...")
        try:
            log_entries = asset.get_asset_log(
                odata_top=3,
                odata_orderby="dateTime desc"
            )
            print(f"[SUCCESS] Retrieved {len(log_entries)} log entries")
            
            for i, log_entry in enumerate(log_entries, 1):
                print(f"   {i}. {log_entry.get('dateTime', 'N/A')} - {log_entry.get('message', 'N/A')}")
                print(f"      Asset: {log_entry.get('assetSerialNumber', 'N/A')}")
                
        except WATSAPIException as e:
            print(f"[ERROR] Error getting asset log: {e}")
            print(f"   Status Code: {e.status_code}")
        
        # Close connection
        connection.close()
        print("\n[SUCCESS] Connection closed successfully")
        
    except Exception as e:
        print(f"[FATAL ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()


def demo_error_handling():
    """
    Demonstrate error handling with invalid credentials.
    """
    print("\n[ERROR DEMO] Error Handling Demo")
    print("=" * 30)
    
    # Try with invalid token
    print("[TEST] Testing with invalid token...")
    try:
        invalid_connection = create_connection(
            base_url="https://ola.wats.com",
            token="invalid_token"
        )
        
        # This should fail
        assets = asset.get_assets(odata_top=1)
        print("[ERROR] This should not print - authentication should have failed!")
        
    except WATSAPIException as e:
        print(f"[SUCCESS] Caught expected authentication error: {e}")
        print(f"   Status Code: {e.status_code}")
    except Exception as e:
        print(f"[SUCCESS] Caught error: {e}")


def show_connection_info():
    """
    Show connection configuration information.
    """
    print("\n[CONFIG] Connection Configuration")
    print("=" * 35)
    print("Base URL: https://ola.wats.com")
    print("Authentication: Basic Auth with encoded token")
    print("Token: cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ==")
    print("Timeout: 30 seconds")
    print("Referrer: Set automatically for internal API access")


if __name__ == "__main__":
    show_connection_info()
    main()
    demo_error_handling()
    
    print("\n[COMPLETE] Example completed!")
    print("=" * 50)
    print("[TIPS] Tips:")
    print("   - Replace BASE_URL and AUTH_TOKEN with your actual values")
    print("   - Check the connection.py module for environment variable support")
    print("   - Explore other endpoint modules (production, report, etc.)")
    print("   - Use OData filters for more specific queries")