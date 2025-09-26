#!/usr/bin/env python3
"""
Add-on test for loading UUT report - to be run after tdm_example.py connection is established
"""

from pyWATS.rest_api.models.wsjf_reports import UUTReport
import json

def test_load_uut_report(tdm, last_uut_id="537a358f-5776-400e-b33e-da99d22eea6a"):
    """Test loading and deserializing a UUT report from server"""
    
    print("\n" + "="*60)
    print(" TESTING UUT REPORT LOADING & DESERIALIZATION")
    print("="*60)
    
    try:
        print(f"\n[1] Attempting to load UUT report: {last_uut_id}")
        
        if not tdm._connection or not tdm._connection._client:
            print("❌ No connection available")
            return None
            
        # Try to get the report using the REST API
        url = f"/api/Internal/Report/WRML/{last_uut_id}"
        print(f"    Making request to: {url}")
        
        response = tdm._connection._client.get(url)
        print(f"    Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully retrieved report from server!")
            
            # Parse the JSON response
            report_data = response.json()
            print(f"\n[2] Raw report data structure:")
            print(f"    Keys: {list(report_data.keys())}")
            print(f"    Type field: {report_data.get('type')}")
            print(f"    ID field: {report_data.get('id')}")
            print(f"    Process code: {report_data.get('processCode')}")
            
            print(f"\n[3] Attempting to deserialize into UUTReport...")
            try:
                # Try to create UUTReport from the server data
                uut_report = UUTReport.model_validate(report_data)
                print("✅ Successfully deserialized into UUTReport!")
                
                # Verify the key fields
                print(f"\n[4] Deserialized UUTReport verification:")
                print(f"    ID: {uut_report.id}")
                print(f"    Type: {uut_report.type}")
                print(f"    Serial Number: {uut_report.sn}")
                print(f"    Part Number: {uut_report.pn}")
                print(f"    Process Code: {uut_report.process_code}")
                print(f"    Result: {uut_report.result}")
                print(f"    Station: {uut_report.station_name}")
                print(f"    Misc Infos: {len(uut_report.misc_infos) if uut_report.misc_infos else 0}")
                
                # Test round-trip serialization
                print(f"\n[5] Testing round-trip serialization...")
                serialized = uut_report.model_dump(by_alias=True)
                print(f"    Serialized keys: {list(serialized.keys())}")
                print("✅ Round-trip serialization successful!")
                
                print(f"\n🎉 SUCCESS: UUT report loading and deserialization works!")
                return uut_report
                
            except Exception as deserialize_error:
                print(f"❌ Deserialization failed: {deserialize_error}")
                print(f"    Error type: {type(deserialize_error)}")
                
                # Show some raw data for debugging
                print(f"\n    Raw data sample (first 300 chars):")
                raw_json = json.dumps(report_data, indent=2)
                print(raw_json[:300] + "..." if len(raw_json) > 300 else raw_json)
                
                return None
                
        else:
            print(f"❌ Failed to retrieve report: {response.status_code}")
            try:
                error_text = response.text
                print(f"    Response: {error_text[:200]}...")
            except:
                print("    Could not get response text")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

# Instructions for use:
print("To use this test:")
print("1. Run tdm_example.py normally to establish connection")
print("2. In the Python debug console, import this module")  
print("3. Call: test_load_uut_report(tdm)")
print("   where 'tdm' is the TDMClient instance from tdm_example.py")