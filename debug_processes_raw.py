#!/usr/bin/env python3
"""
Debug script to see raw server response for processes
"""

import json
from src.pyWATS.tdm_client import TDMClient


def main():
    # Create client and connect
    client = TDMClient()
    client.station_name = "Debug_Station"
    
    # Initialize connection
    client.register_client(
        base_url="https://ola.wats.com",
        token="cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
    )
    
    # Get raw connection to make direct API calls
    connection = client.connection
    
    print("=== Testing /api/App/Processes endpoint ===")
    try:
        response = connection.client.get("/api/App/Processes", params={
            "includeTestOperations": True,
            "includeRepairOperations": True,
            "includeWipOperations": False,
            "includeInactiveProcesses": False
        })
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response Type: {type(data)}")
            print(f"Total processes: {len(data) if isinstance(data, list) else 'Not a list'}")
            
            # Look for repair operations (code 500)
            repair_500 = None
            if isinstance(data, list):
                for process in data:
                    if process.get('code') == 500:
                        repair_500 = process
                        break
            
            if repair_500:
                print(f"\n=== Process Code 500 Raw Data ===")
                print(json.dumps(repair_500, indent=2))
                
                # Check all field names that might contain failure data
                failure_fields = []
                for key in repair_500.keys():
                    if any(word in key.lower() for word in ['failure', 'categor', 'code', 'repair']):
                        failure_fields.append(key)
                
                print(f"\nPossible failure-related fields: {failure_fields}")
                
                for field in failure_fields:
                    print(f"{field}: {repair_500.get(field)}")
            else:
                print("No process with code 500 found")
        else:
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"Error calling /api/App/Processes: {e}")
    
    print("\n=== Testing /api/internal/process/GetProcesses endpoint ===")
    try:
        response = connection.client.get("/api/internal/process/GetProcesses")
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response Type: {type(data)}")
            
            processes = data if isinstance(data, list) else data.get("processes", [])
            print(f"Total processes: {len(processes)}")
            
            # Look for repair operations (code 500)
            repair_500 = None
            for process in processes:
                if process.get('code') == 500:
                    repair_500 = process
                    break
            
            if repair_500:
                print(f"\n=== Internal API - Process Code 500 Raw Data ===")
                print(json.dumps(repair_500, indent=2))
            else:
                print("No process with code 500 found in internal API")
        else:
            print(f"Error: {response.text}")
    
    except Exception as e:
        print(f"Error calling internal API: {e}")
    
    client.unregister_client()


if __name__ == "__main__":
    main()