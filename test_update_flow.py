#!/usr/bin/env python3
"""
Test the product update flow step by step to identify where it fails
"""

from pyWATS import create_api
from pyWATS.rest_api.endpoints.product import get_product, create_product
from pyWATS.rest_api.models.product import Product as ProductRestModel
from datetime import datetime

def test_update_flow():
    """Test each step of the product update flow"""
    
    api = create_api()
    client = api.tdm_client._connection._client
    
    part_number = "010738-"
    timestamp = datetime.now().strftime("%H%M%S")
    
    print("=== Testing Product Update Flow Step by Step ===")
    
    print("\n--- Step 1: Get existing product ---")
    try:
        existing_product = get_product(part_number, client=client)
        print(f"✅ Got existing product: {type(existing_product)}")
        print(f"   Part Number: {existing_product.part_number}")
        print(f"   Current Name: {existing_product.name}")
        print(f"   Current Description: {existing_product.description}")
        
        # Convert to dict and show structure
        product_dict = existing_product.dict()
        print(f"   Dict keys: {list(product_dict.keys())}")
        
    except Exception as e:
        print(f"❌ Step 1 failed: {e}")
        return
    
    print("\n--- Step 2: Apply updates ---")
    try:
        updates = {
            "name": f"Updated Name {timestamp}",
            "description": f"Updated Description {timestamp}"
        }
        
        print(f"Applying updates: {updates}")
        product_dict.update(updates)
        print(f"✅ Updates applied")
        print(f"   New Name: {product_dict.get('name')}")
        print(f"   New Description: {product_dict.get('description')}")
        
    except Exception as e:
        print(f"❌ Step 2 failed: {e}")
        return
        
    print("\n--- Step 3: Create ProductRestModel ---")
    try:
        updated_product = ProductRestModel(**product_dict)
        print(f"✅ Created ProductRestModel")
        print(f"   Model Name: {updated_product.name}")
        print(f"   Model Description: {updated_product.description}")
        
    except Exception as e:
        print(f"❌ Step 3 failed: {e}")
        import traceback
        traceback.print_exc()
        return
        
    print("\n--- Step 4: Save via create_product ---")
    try:
        result = create_product(updated_product, client=client)
        print(f"✅ create_product returned: {type(result)}")
        print(f"   Result Name: {result.name}")
        print(f"   Result Description: {result.description}")
        
        print("\n🎉 Product update flow completed successfully!")
        
    except Exception as e:
        print(f"❌ Step 4 failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Let's also check what the actual request looks like
        print("\n--- Debugging create_product request ---")
        try:
            # Let's see what JSON would be sent
            json_data = updated_product.dict(exclude_none=True, by_alias=True)
            print(f"JSON that would be sent: {json_data}")
            
        except Exception as debug_e:
            print(f"Debug error: {debug_e}")

if __name__ == "__main__":
    test_update_flow()