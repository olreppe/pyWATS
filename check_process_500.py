#!/usr/bin/env python3
"""
Simple check of available repair operation process codes using existing client setup
"""
import sys
import os

# Add src to path so we can import pyWATS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pyWATS import TDMClient
from pyWATS.tdm_client import APIStatusType
import json

def main():
    """Check repair operation codes"""
    # Initialize TDM client exactly like tdm_example.py
    tdm = TDMClient()

    # Configure API settings  
    tdm.setup_api(
        data_dir="./wats_tdm_data",
        location="TDM Demo Lab",
        purpose="Development Testing",
        persist=False
    )
    tdm.station_name = "TDM_Demo_Station"

    # Connection
    BASE_URL = "http://wats-dw2.eltest.no"
    AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
    
    try:
        print("Connecting to server...")
        tdm.register_client(base_url=BASE_URL, token=AUTH_TOKEN)
        tdm.initialize_api(try_connect_to_server=True, download_metadata=True)
        
        if tdm.status != APIStatusType.Online:
            print("❌ Not online")
            return
            
        print("✅ Connected successfully!")
        
        # Get repair operations using the same method as tdm_example.py
        print("\n=== REPAIR OPERATIONS DEBUG ===")
        repair_operations = tdm.get_repair_operations()
        
        print(f"Found {len(repair_operations)} repair operations:")
        for i, repair_op in enumerate(repair_operations, 1):
            process_code = repair_op.get('processCode')
            name = repair_op.get('name')
            print(f"  {i}. {name} (Code: {process_code})")
            
        # Also check all processes to see what repair operations exist
        print(f"\n=== ALL PROCESSES WITH isRepairOperation=true ===")
        all_processes = tdm.get_all_processes()
        
        repair_processes = [p for p in all_processes if p.get('isRepairOperation', False)]
        print(f"Found {len(repair_processes)} processes with isRepairOperation=true:")
        
        for i, process in enumerate(repair_processes, 1):
            process_code = process.get('processCode')
            name = process.get('name', 'Unknown')
            is_test = process.get('isTestOperation', False)
            is_repair = process.get('isRepairOperation', False)
            print(f"  {i}. {name}")
            print(f"      Code: {process_code}")
            print(f"      isTestOperation: {is_test}")
            print(f"      isRepairOperation: {is_repair}")
            
            # Check if process 500 specifically
            if process_code == 500:
                print(f"      *** THIS IS PROCESS 500! ***")
                print(f"      Full data: {json.dumps(process, indent=6)}")
        
        # Check specifically for 500
        process_500 = next((p for p in all_processes if p.get('processCode') == 500), None)
        print(f"\n=== PROCESS 500 SPECIFIC CHECK ===")
        if process_500:
            print("✅ Process 500 exists in server data!")
            print(f"Name: {process_500.get('name')}")
            print(f"isRepairOperation: {process_500.get('isRepairOperation')}")
            print(f"isTestOperation: {process_500.get('isTestOperation')}")
        else:
            print("❌ Process 500 NOT found in server!")
            
        # Show some working test operation codes for comparison
        print(f"\n=== SOME WORKING TEST OPERATIONS ===")
        test_processes = [p for p in all_processes if p.get('isTestOperation', False)]
        print(f"Found {len(test_processes)} test operations, showing first 5:")
        for i, process in enumerate(test_processes[:5], 1):
            process_code = process.get('processCode')
            name = process.get('name', 'Unknown')
            print(f"  {i}. {name} (Code: {process_code})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()