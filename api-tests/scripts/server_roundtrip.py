"""
Test actual server round-trip to see what time the server stores/returns

This test requires a real WATS server connection.
Configure via tests/instances/client_a_config.json or environment variables:
  WATS_BASE_URL - Your WATS server URL
  WATS_AUTH_TOKEN - Your base64-encoded token

USAGE: Run this file directly, not via pytest:
    python -m api-tests.test_server_roundtrip
"""
import os
from datetime import datetime
from pywats import pyWATS
from pywats.domains.report.report_models.uut.uut_report import UUTReport
from pywats.domains.report.report_models.uut.uut_info import UUTInfo
import json


def run_roundtrip_test():
    """Execute the server round-trip timezone test."""
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

    # Initialize client with credentials from environment or config
    base_url = os.environ.get("WATS_BASE_URL", "")
    token = os.environ.get("WATS_AUTH_TOKEN", "")

    if not base_url or not token:
        # Try loading from config file
        import json as json_module
        config_path = os.path.join(os.path.dirname(__file__), "instances", "client_a_config.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json_module.load(f)
                base_url = config.get("base_url", "")
                token = config.get("token", "")

    if not base_url or not token:
        print("ERROR: No WATS server configured. Set WATS_BASE_URL and WATS_AUTH_TOKEN or configure tests/instances/client_a_config.json")
        return 1

    try:
        client = pyWATS(base_url=base_url, token=token)
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
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(run_roundtrip_test())
