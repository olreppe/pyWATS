"""
Test actual server round-trip to see what time the server stores/returns
"""
from datetime import datetime
from pywats import pyWATS
from pywats.domains.report.report_models.uut.uut_report import UUTReport
from pywats.domains.report.report_models.uut.uut_info import UUTInfo
import json

print("=" * 80)
print("SERVER ROUND-TRIP TEST")
print("=" * 80)

# Create report with known time
test_time = datetime.now().astimezone()
print(f"\n1. LOCAL TIME WHEN CREATING REPORT:")
print(f"   {test_time.strftime('%Y-%m-%d %H:%M:%S %z (%Z)')}")
print(f"   ISO format: {test_time.isoformat()}")

# Create minimal report
report = UUTReport(
    pn="TZ-TEST-001",
    sn=f"SN-TZ-{test_time.strftime('%H%M%S')}",
    rev="A",
    process_code=10,
    station_name="TZ-Test-Station",
    location="Test-Lab",
    purpose="Timezone-Test",
    result="P",
    start=test_time
)

# Add minimal info
report.info = UUTInfo(
    operator="TZ-Tester",
    comment=f"Timezone test - sent at {test_time.strftime('%H:%M:%S')}"
)

# Show what's being sent
json_data = report.model_dump(mode='json', by_alias=True, exclude_none=True)
json_str = json.dumps(json_data)
print(f"\n2. JSON BEING SENT TO SERVER:")
print(f"   start field: {json_data.get('start')}")
print(f"   startUTC in JSON: {'startUTC' in json_str}")

# Initialize client with credentials
try:
    client = pyWATS(
        base_url="https://python.wats.com",
        token="cHlXQVRTX0FQSV9BVVRPVEVTVDo2cGhUUjg0ZTVIMHA1R3JUWGtQZlY0UTNvbmk2MiM="
    )
    print(f"\n3. SENDING REPORT TO SERVER...")
    
    # Send report
    report_id = client.report.submit_report(report)
    
    if report_id:
        print(f"   [OK] Report sent successfully")
        print(f"   Report ID: {report_id}")
        print(f"   Serial Number: {report.sn}")
        
        # Wait a moment for server to process
        import time
        time.sleep(3)
        
        # Try to retrieve it
        print(f"\n4. RETRIEVING REPORT FROM SERVER...")
        retrieved = client.report.get_report(report_id)
        
        if retrieved:
            print(f"   [OK] Report retrieved")
            print(f"\n5. TIME COMPARISON:")
            print(f"   Sent:     {test_time.strftime('%H:%M:%S %z')}")
            print(f"   Retrieved: {retrieved.start.strftime('%H:%M:%S %z')}")
            
            # Calculate difference
            if hasattr(retrieved, 'start') and retrieved.start:
                time_diff = (retrieved.start - test_time).total_seconds()
                if abs(time_diff) < 5:
                    print(f"   [OK] Times match (difference: {time_diff:.1f} seconds)")
                else:
                    print(f"   [ERROR] TIME MISMATCH!")
                    print(f"   Difference: {time_diff / 3600:.2f} hours")
                    
                    # Check if it's exactly 1 hour off
                    if abs(time_diff - 3600) < 60:
                        print(f"   → Server subtracted 1 hour (treating +01:00 as UTC)")
                    elif abs(time_diff + 3600) < 60:
                        print(f"   → Server added 1 hour (treating timestamp as naive)")
            else:
                print(f"   [WARN] Retrieved report has no start time")
                
        else:
            print(f"   [WARN] Could not retrieve report (may take longer to process)")
            print(f"   Check manually in WATS system:")
            print(f"   - Serial Number: {report.sn}")
            print(f"   - Expected time: {test_time.strftime('%H:%M:%S')}")
            
    else:
        print(f"   [ERROR] Failed to send report")
        
except Exception as e:
    print(f"\n[ERROR]: {e}")
    print(f"\nTo manually test:")
    print(f"1. This report would have been sent at: {test_time.strftime('%H:%M:%S %z')}")
    print(f"2. Check if it appears in WATS with the correct time")

print("\n" + "=" * 80)
