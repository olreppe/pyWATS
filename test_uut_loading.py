#!/usr/bin/env python3
"""
Test loading and deserializing a submitted UUT report from the server
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pyWATS.tdm_client import TDMClient
from pyWATS.rest_api.models.wsjf_reports import UUTReport
from pyWATS.tdm_client import APIStatusType
import json

def main():
    """Test loading a UUT report from server and deserializing it"""
    
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
        print("=== TESTING UUT REPORT LOADING & DESERIALIZATION ===")
        print("\n[1] Connecting to server...")
        tdm.register_client(base_url=BASE_URL, token=AUTH_TOKEN)
        tdm.initialize_api(try_connect_to_server=True, download_metadata=True)
        
        if tdm.status != APIStatusType.Online:
            print("❌ Not online")
            return
            
        print("✅ Connected successfully!")
        
        # The last successful UUT report ID from our previous run
        # From the output: "Report successfully submitted with ID: 537a358f-5776-400e-b33e-da99d22eea6a"
        last_uut_id = "537a358f-5776-400e-b33e-da99d22eea6a"
        
        print(f"\n[2] Attempting to load UUT report: {last_uut_id}")
        
        # Try to get the report using the REST API directly
        if tdm._connection:
            try:
                # Use internal REST API to fetch the report
                url = f"/api/Internal/Report/WRML/{last_uut_id}"
                print(f"    Making request to: {url}")
                
                response = tdm._connection._client.get(url)
                print(f"    Response status: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Successfully retrieved report from server!")
                    
                    # Parse the JSON response
                    report_data = response.json()
                    print(f"\n[3] Raw report data structure:")
                    print(f"    Keys: {list(report_data.keys())}")
                    print(f"    Type field: {report_data.get('type')}")
                    print(f"    ID field: {report_data.get('id')}")
                    print(f"    Process code: {report_data.get('processCode')}")
                    
                    # Show first 500 chars of raw JSON
                    raw_json = json.dumps(report_data, indent=2)
                    print(f"\n[4] Raw JSON (first 500 chars):")
                    print(raw_json[:500] + "..." if len(raw_json) > 500 else raw_json)
                    
                    print(f"\n[5] Attempting to deserialize into UUTReport...")
                    try:
                        # Try to create UUTReport from the server data
                        uut_report = UUTReport.model_validate(report_data)
                        print("✅ Successfully deserialized into UUTReport!")
                        
                        # Verify the key fields
                        print(f"\n[6] Deserialized UUTReport verification:")
                        print(f"    ID: {uut_report.id}")
                        print(f"    Type: {uut_report.type}")
                        print(f"    Serial Number: {uut_report.sn}")
                        print(f"    Part Number: {uut_report.pn}")
                        print(f"    Process Code: {uut_report.process_code}")
                        print(f"    Result: {uut_report.result}")
                        print(f"    Station: {uut_report.station_name}")
                        print(f"    Misc Infos: {len(uut_report.misc_infos) if uut_report.misc_infos else 0}")
                        
                        # Test round-trip serialization
                        print(f"\n[7] Testing round-trip serialization...")
                        serialized = uut_report.model_dump(by_alias=True)
                        print(f"    Serialized keys: {list(serialized.keys())}")
                        print("✅ Round-trip serialization successful!")
                        
                        return uut_report
                        
                    except Exception as deserialize_error:
                        print(f"❌ Deserialization failed: {deserialize_error}")
                        print(f"    Error type: {type(deserialize_error)}")
                        
                        # Try to identify the specific field causing issues
                        try:
                            print(f"\n    Analyzing field compatibility...")
                            expected_fields = UUTReport.model_fields.keys()
                            actual_fields = report_data.keys()
                            
                            print(f"    Expected fields: {sorted(expected_fields)}")
                            print(f"    Server fields: {sorted(actual_fields)}")
                            
                            missing_in_server = set(expected_fields) - set(actual_fields)
                            extra_in_server = set(actual_fields) - set(expected_fields)
                            
                            if missing_in_server:
                                print(f"    Missing in server: {missing_in_server}")
                            if extra_in_server:
                                print(f"    Extra in server: {extra_in_server}")
                                
                        except Exception as analysis_error:
                            print(f"    Field analysis failed: {analysis_error}")
                        
                        return None
                        
                else:
                    print(f"❌ Failed to retrieve report: {response.status_code}")
                    print(f"    Response: {response.text[:200]}...")
                    return None
                    
            except Exception as api_error:
                print(f"❌ API call failed: {api_error}")
                return None
        else:
            print("❌ No connection available")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n🎉 SUCCESS: Retrieved and deserialized UUT report!")
    else:
        print(f"\n💥 FAILED: Could not load/deserialize UUT report")