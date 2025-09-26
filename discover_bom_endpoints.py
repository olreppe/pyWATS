#!/usr/bin/env python3
"""
Discover and test BOM API endpoints for product 100200, revision 1
"""

from pyWATS import create_api
from pyWATS.mes import Product
import json

def test_bom_endpoints():
    """Test various BOM endpoint possibilities"""
    
    print("=== Initializing API ===")
    api = create_api()
    
    # Get the REST client directly
    client = api.tdm_client._connection._client
    
    part_number = "100200"
    revision = "1"
    
    print(f"\n=== Testing BOM endpoints for {part_number} rev {revision} ===")
    
    # Test various possible BOM GET endpoints
    endpoints_to_test = [
        f"/api/Product/{part_number}/BOM",
        f"/api/Product/{part_number}/{revision}/BOM",
        f"/api/Product/BOM/{part_number}",
        f"/api/Product/BOM/{part_number}/{revision}",
        f"/api/Product/BOM?partNumber={part_number}&revision={revision}",
        f"/api/Product/BOM?partNumber={part_number}",
    ]
    
    for endpoint in endpoints_to_test:
        try:
            print(f"\nTesting: GET {endpoint}")
            response = client.get(endpoint)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print("  ✅ SUCCESS! Found BOM endpoint")
                data = response.json()
                print(f"  Response type: {type(data)}")
                
                if isinstance(data, dict):
                    print(f"  Keys: {list(data.keys())[:10]}")
                    for key, value in list(data.items())[:5]:
                        print(f"    {key}: {type(value)} = {str(value)[:100]}")
                elif isinstance(data, list):
                    print(f"  List length: {len(data)}")
                    if data:
                        print(f"  First item type: {type(data[0])}")
                        print(f"  First item: {str(data[0])[:200]}")
                else:
                    print(f"  Raw response: {str(data)[:200]}")
                    
                return endpoint, data  # Found working endpoint
                
            elif response.status_code == 404:
                print("  ❌ Not Found")
            elif response.status_code == 401:
                print("  ❌ Unauthorized")
            elif response.status_code == 400:
                print("  ❌ Bad Request")
                try:
                    error_data = response.json()
                    print(f"    Error: {error_data}")
                except:
                    print(f"    Error text: {response.text[:100]}")
            else:
                print(f"  ❌ Status {response.status_code}")
                print(f"    Response: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ Exception: {e}")
    
    print("\n❌ No working BOM GET endpoint found")
    return None, None

if __name__ == "__main__":
    endpoint, data = test_bom_endpoints()
    
    if endpoint:
        print(f"\n🎉 SUCCESS: Working BOM endpoint found: {endpoint}")
        print(f"📋 Data sample: {str(data)[:300]}...")
    else:
        print("\n💡 BOM GET endpoint may not be implemented yet or requires different parameters")