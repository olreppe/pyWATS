#!/usr/bin/env python3
"""
Debug script to inspect process structure for repair operations
"""

import json
from src.pyWATS.tdm_client import TDMClient


def main():
    # Create client
    client = TDMClient()
    client.station_name = "Debug_Station"
    client.data_directory = "./debug_data"
    client.location = "Debug Lab"
    
    # Initialize connection
    client.register_client(
        base_url="https://wats.watsolution.com",
        token="wats_demo_token_12345"
    )
    
    # Get all processes
    processes = client._processes or {}
    
    print("=== ALL PROCESSES ===")
    print(f"Total processes: {len(processes.get('processes', []))}")
    
    repair_processes = []
    for process in processes.get('processes', []):
        is_repair_op = process.get('isRepairOperation', process.get('IsRepairOperation', False))
        if is_repair_op:
            repair_processes.append(process)
            
    print(f"\n=== REPAIR OPERATIONS ({len(repair_processes)}) ===")
    
    for i, process in enumerate(repair_processes[:3]):  # Show first 3
        print(f"\n--- Repair Process {i+1} ---")
        print(f"Name: {process.get('name', process.get('Name'))}")
        print(f"Code: {process.get('code', process.get('Code'))}")
        print(f"Description: {process.get('description', process.get('Description'))}")
        print(f"Is Repair Operation: {process.get('isRepairOperation', process.get('IsRepairOperation'))}")
        
        # Look for all possible failure-related fields
        failure_fields = [key for key in process.keys() if 'fail' in key.lower()]
        category_fields = [key for key in process.keys() if 'categor' in key.lower()]
        code_fields = [key for key in process.keys() if 'code' in key.lower()]
        
        print(f"Failure-related fields: {failure_fields}")
        print(f"Category-related fields: {category_fields}")
        print(f"Code-related fields: {code_fields}")
        
        # Show all keys for structure analysis
        print(f"All keys: {list(process.keys())}")
        
        # Show full structure for first process
        if i == 0:
            print(f"\n=== FULL STRUCTURE ===")
            print(json.dumps(process, indent=2, default=str))
    
    client.unregister_client()


if __name__ == "__main__":
    main()