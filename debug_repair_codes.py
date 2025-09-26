#!/usr/bin/env python3
"""
Debug script to examine what repair operation process codes are available on the server
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pyWATS.tdm_client import TDMClient
import json

def main():
    """Debug what repair process codes are available"""
    
    # Initialize TDM client
    client = TDMClient()
    
    # Configure API settings
    client.setup_api(
        data_dir="./debug_data",
        location="Debug Lab",
        purpose="Debug Testing"
    )
    client.station_name = "Debug_Station"
    
    # Register with server and initialize
    BASE_URL = "http://wats-dw2.eltest.no"
    AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
    
    client.register_client(base_url=BASE_URL, token=AUTH_TOKEN)
    client.initialize_api()
    
    print("=" * 80)
    print("DEBUGGING REPAIR OPERATION PROCESS CODES")
    print("=" * 80)
    
    try:
        # Get all processes
        print("[1] Getting all processes...")
        processes = client.get_all_processes()
        print(f"    ✓ Found {len(processes)} processes")
        
        # Filter for repair operations
        repair_operations = [p for p in processes if p.get('isRepairOperation', False)]
        print(f"    ✓ Found {len(repair_operations)} repair operations")
        
        print("\n[2] Repair operation details:")
        for i, repair_op in enumerate(repair_operations, 1):
            process_code = repair_op.get('processCode')
            name = repair_op.get('name')
            is_repair = repair_op.get('isRepairOperation', False)
            is_test = repair_op.get('isTestOperation', False)
            
            print(f"    {i}. {name}")
            print(f"       Process Code: {process_code}")
            print(f"       isRepairOperation: {is_repair}")
            print(f"       isTestOperation: {is_test}")
            
            # Check if it has repair categories
            if 'repairOperation' in repair_op:
                repair_cats = repair_op['repairOperation'].get('repairCategories', [])
                print(f"       Repair Categories: {len(repair_cats)}")
                for cat in repair_cats[:2]:  # Show first 2 categories
                    print(f"         - {cat.get('description', 'No description')}")
            print()
        
        # Check if 500 exists and what its properties are
        print("[3] Checking process code 500 specifically:")
        process_500 = next((p for p in processes if p.get('processCode') == 500), None)
        if process_500:
            print("    ✓ Process code 500 exists!")
            print(f"    Name: {process_500.get('name')}")
            print(f"    isRepairOperation: {process_500.get('isRepairOperation', False)}")
            print(f"    isTestOperation: {process_500.get('isTestOperation', False)}")
            print(f"    Raw data: {json.dumps(process_500, indent=2)}")
        else:
            print("    ✗ Process code 500 NOT found in server response!")
            
        # Show some test operations for comparison
        print("\n[4] Some test operations for comparison:")
        test_operations = [p for p in processes if p.get('isTestOperation', False)]
        for i, test_op in enumerate(test_operations[:5], 1):
            process_code = test_op.get('processCode')
            name = test_op.get('name')
            print(f"    {i}. {name} (Code: {process_code})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()