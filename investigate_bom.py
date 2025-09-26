#!/usr/bin/env python3
"""
Investigate BOM for product 100200, revision 1
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from pyWATS import create_api
from pyWATS.mes import Product

def investigate_bom():
    """Investigate BOM structure for product 100200, revision 1"""
    
    print("=== Initializing API ===")
    api = create_api()
    
    # Create product service directly
    product_service = Product(api.tdm_client)
    
    print("\n=== Checking Product 100200 ===")
    try:
        # First check if the product exists
        product_info = product_service.get_product_info("100200", "1")
        print(f"✅ Product found!")
        print(f"   Part Number: {product_info.part_number}")
        print(f"   Revision: {product_info.revision}")
        print(f"   Name: {product_info.name}")
        print(f"   Description: {product_info.description}")
    except Exception as e:
        print(f"❌ Error getting product info: {e}")
        
    print("\n=== Getting Product Revisions ===")
    try:
        revisions = product_service.get_product_revisions("100200")
        print(f"✅ Found {len(revisions)} revision(s):")
        for i, rev in enumerate(revisions):
            print(f"   [{i+1}] Revision: {rev.revision}")
            if hasattr(rev, 'name') and rev.name:
                print(f"       Name: {rev.name}")
            if hasattr(rev, 'description') and rev.description:
                print(f"       Description: {rev.description}")
    except Exception as e:
        print(f"❌ Error getting revisions: {e}")
        
    print("\n=== Attempting to Get BOM ===")
    try:
        # Try to get BOM for the specific product revision
        bom_result = product_service.get_bom("100200", "1")
        print(f"✅ BOM retrieval result: {bom_result}")
        
        if bom_result and hasattr(bom_result, 'success') and bom_result.success:
            print("✅ BOM found! Analyzing structure...")
            if hasattr(bom_result, 'data') and bom_result.data:
                bom_data = bom_result.data
                print(f"   BOM Data Type: {type(bom_data)}")
                print(f"   BOM Data: {bom_data}")
                
                # Try to understand the structure
                if isinstance(bom_data, dict):
                    print(f"   BOM Keys: {list(bom_data.keys())}")
                    for key, value in bom_data.items():
                        print(f"   {key}: {type(value)} = {value}")
                elif isinstance(bom_data, list):
                    print(f"   BOM Items Count: {len(bom_data)}")
                    if bom_data:
                        print(f"   First Item Type: {type(bom_data[0])}")
                        print(f"   First Item: {bom_data[0]}")
        else:
            print("❌ BOM retrieval failed or returned no data")
            
    except Exception as e:
        print(f"❌ Error getting BOM: {e}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    investigate_bom()