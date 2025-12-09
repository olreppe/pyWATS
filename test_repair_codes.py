# Test script to check repair processes and fail codes
from pywats import pyWATS
import json

# Connect to WATS with correct token
wats = pyWATS(
    base_url='https://python.wats.com',
    token='cHlXQVRTX0FQSV9BVVRPVEVTVDo2cGhUUjg0ZTVIMHA1R3JUWGtQZlY0UTNvbmk2MiM='
)

# Get repair operations from internal API
response = wats._http_client.get('/api/internal/Process/GetRepairOperations')
if response.is_success:
    print("=== Repair Operations ===")
    if response.data:
        print(json.dumps(response.data[:2], indent=2, default=str)[:8000])
else:
    print(f"Error: {response.status_code}")
    if response.data:
        print(response.data)
