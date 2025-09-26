#!/usr/bin/env python3
"""
Test direct REST endpoints for update and BOM operations
"""

from pyWATS import create_api
from datetime import datetime

def test_direct_operations():
    """Test direct REST API calls"""
    
    api = create_api()
    client = api.tdm_client._connection._client

    print("=== Direct Product Update Test ===")
    # Try direct PUT to update product
    timestamp = datetime.now().strftime("%H%M%S")
    product_data = {
        "partNumber": "010738-",
        "name": "Test Updated Direct", 
        "description": f"Direct update test {timestamp}"
    }

    response = client.put("/api/Product", json=product_data)
    print(f"Direct update status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    if response.status_code == 200:
        print("✅ Direct product update SUCCESS!")
    else:
        print("❌ Direct product update failed")

    print("\n=== BOM Upload Test (Simple Format) ===")
    # Try BOM without XML declaration, matching server format
    simple_bom = '<Root><TestTag Value="TestUpload" /></Root>'
    response = client.put(
        "/api/Product/BOM", 
        data=simple_bom, 
        headers={"Content-Type": "application/xml"}
    )
    print(f"BOM status: {response.status_code}")
    print(f"BOM response: {response.text[:300]}")
    
    if response.status_code == 200:
        print("✅ BOM upload SUCCESS!")
    else:
        print("❌ BOM upload failed")

if __name__ == "__main__":
    test_direct_operations()