"""Test to verify timezone handling during deserialization from server."""

import sys
from datetime import datetime, timezone
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pywats import pyWATS as WATS
import os

def main():
    print("=" * 80)
    print("Testing Deserialization Timezone Handling")
    print("=" * 80)
    
    # Get credentials from environment or config
    base_url = os.environ.get("WATS_BASE_URL", "")
    token = os.environ.get("WATS_AUTH_TOKEN", "")
    
    if not base_url or not token:
        # Try loading from config file
        import json
        config_path = os.path.join(os.path.dirname(__file__), "instances", "client_a_config.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)
                base_url = config.get("base_url", "")
                token = config.get("token", "")
    
    if not base_url or not token:
        print("ERROR: No WATS server configured. Set WATS_BASE_URL and WATS_AUTH_TOKEN")
        return
    
    # Connect to server
    wats = WATS(base_url=base_url, token=token)
    
    # Get current local time
    now_local = datetime.now().astimezone()
    print(f"\n1. LOCAL TIME WHEN CREATING REPORT:")
    print(f"   Time: {now_local}")
    print(f"   ISO: {now_local.isoformat()}")
    print(f"   Timezone: {now_local.tzinfo}")
    print(f"   UTC offset: {now_local.strftime('%z')}")
    
    # Create and submit report
    print(f"\n2. CREATING AND SUBMITTING REPORT...")
    report = wats.report.create_uut_report(
        operator="TestOperator",
        part_number="DESER_TEST",
        revision="A",
        serial_number=f"SN_{now_local.strftime('%H%M%S')}",
        operation_type=10,
        station_name="TestStation",
        location="TestLocation",
        purpose="DeserializationTest"
    )
    
    # Check what we're sending
    report_dict = report.model_dump(mode="json", by_alias=True, exclude_none=True)
    print(f"\n3. JSON BEING SENT TO SERVER:")
    print(f"   start: {report_dict.get('start')}")
    print(f"   startUTC: {report_dict.get('startUTC', 'NOT PRESENT')}")
    
    # Submit
    report_id = wats.report.submit(report)
    print(f"\n4. REPORT SUBMITTED:")
    print(f"   ID: {report_id}")
    
    if not report_id:
        print("\n✗ FAILED TO SUBMIT REPORT")
        return
    
    # Wait a moment for processing
    import time
    print("\n5. WAITING 3 SECONDS FOR SERVER PROCESSING...")
    time.sleep(3)
    
    # Query back the report
    print(f"\n6. QUERYING REPORT BACK FROM SERVER...")
    retrieved_report = wats.report.get_report(report_id)
    
    if retrieved_report:
        print(f"\n7. RETRIEVED REPORT DATA:")
        print(f"   Type: {type(retrieved_report)}")
        print(f"   start field: {retrieved_report.start}")
        print(f"   start ISO: {retrieved_report.start.isoformat()}")
        print(f"   start timezone: {retrieved_report.start.tzinfo}")
        print(f"   start UTC offset: {retrieved_report.start.strftime('%z')}")
        
        # Check if start_utc is present
        if hasattr(retrieved_report, 'start_utc') and retrieved_report.start_utc:
            print(f"   startUTC field: {retrieved_report.start_utc}")
            print(f"   startUTC ISO: {retrieved_report.start_utc.isoformat()}")
        else:
            print(f"   startUTC field: NOT PRESENT or None")
        
        # Compare times
        print(f"\n8. TIME COMPARISON:")
        print(f"   Original local time: {now_local.isoformat()}")
        print(f"   Retrieved start:     {retrieved_report.start.isoformat()}")
        
        # Calculate difference
        time_diff = retrieved_report.start - now_local
        print(f"   Difference: {time_diff.total_seconds()} seconds")
        
        if abs(time_diff.total_seconds()) < 5:
            print(f"   ✓ Times match (within 5 seconds)")
        else:
            print(f"   ✗ Times differ by {time_diff.total_seconds()} seconds")
            
        # Check if retrieved time is timezone-aware
        print(f"\n9. TIMEZONE AWARENESS CHECK:")
        if retrieved_report.start.tzinfo is None:
            print(f"   ✗ Retrieved datetime is NAIVE (no timezone info)")
            print(f"   This means server returned time without timezone offset")
            print(f"   Our code may be interpreting it as local time when it's actually UTC")
        else:
            print(f"   ✓ Retrieved datetime is AWARE")
            print(f"   Timezone: {retrieved_report.start.tzinfo}")
            print(f"   UTC offset: {retrieved_report.start.strftime('%z')}")
            
            # Check what the server thinks the timezone is
            if retrieved_report.start.strftime('%z') == '+00:00':
                print(f"   ⚠ Server returned UTC time (offset +00:00)")
                print(f"   This may indicate server stored as UTC but isn't returning original offset")
            elif retrieved_report.start.strftime('%z') == now_local.strftime('%z'):
                print(f"   ✓ Server preserved timezone offset: {retrieved_report.start.strftime('%z')}")
    else:
        print("\n✗ FAILED TO RETRIEVE REPORT")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
