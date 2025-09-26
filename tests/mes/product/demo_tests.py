"""
MES Product Test Demo - Show Structure Even With Connection Issues

This version will run all tests to show the structure, even if connection fails.
"""

import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from test_product_operations import ProductTestRunner
from product_config import TEST_BASE_URL, TEST_AUTH_TOKEN


def main():
    """Run MES product tests - continue even if connection fails"""
    print("🚀 Starting MES Product Test Demo...")
    print(f"📡 Server: {TEST_BASE_URL}")
    print("📋 This will show all test structure even if connection fails")
    print()
    
    runner = ProductTestRunner(TEST_BASE_URL, TEST_AUTH_TOKEN)
    
    # Modified version that continues even if connection fails
    print("=" * 60)
    print(" MES PRODUCT TESTING SUITE - DEMO MODE")
    print("=" * 60)
    print(f"Started at: runner timestamp here")
    print()

    # Setup (but continue even if it fails)
    result = runner.setup_connection()
    print(f"[SETUP] Connection: {result}")
    
    # Continue with all tests regardless of connection
    print("\n" + "=" * 60)
    print(" TEST 1: Get Product Info")
    print("=" * 60)
    
    test_part_numbers = ["TEST_PART_001", "PCBA_PART_001"]
    for pn in test_part_numbers:
        try:
            result = runner.test_get_product_info(pn)
            print(f"[1] Product Info ({pn}): {result}")
        except Exception as e:
            print(f"[1] Product Info ({pn}): ❌ FAIL: {str(e)}")

    print("\n" + "=" * 60)
    print(" TEST 2: Get Products with Filter")
    print("=" * 60)
    
    filters = ["TEST", "PCBA", "*"]
    for filter_text in filters:
        try:
            result = runner.test_get_products(filter_text, top_count=5)
            print(f"[2] Products Filter ('{filter_text}'): {result}")
        except Exception as e:
            print(f"[2] Products Filter ('{filter_text}'): ❌ FAIL: {str(e)}")

    print("\n" + "=" * 60)
    print(" TEST 3: Update Product (Simulation)")
    print("=" * 60)
    
    try:
        updates = {
            "description": "Updated via automated test",
            "category": "Test Category"
        }
        result = runner.test_update_product("TEST_PART_001", updates)
        print(f"[3] Product Update: {result}")
    except Exception as e:
        print(f"[3] Product Update: ❌ FAIL: {str(e)}")

    print("\n" + "=" * 60)
    print(" TEST 4: Get BOM")
    print("=" * 60)
    
    for pn in test_part_numbers:
        try:
            result = runner.test_get_bom(pn)
            print(f"[4] Get BOM ({pn}): {result}")
        except Exception as e:
            print(f"[4] Get BOM ({pn}): ❌ FAIL: {str(e)}")

    print("\n" + "=" * 60)
    print(" TEST 5: Upload BOM")
    print("=" * 60)
    
    try:
        sample_bom = runner.create_sample_bom("TEST_BOM_PART_001")
        result = runner.test_upload_bom(sample_bom)
        print(f"[5] Upload BOM: {result}")
        
        if hasattr(result, 'success') and result.success:
            print("    📋 BOM Data Sample:")
            print(f"    📋 Part Number: {sample_bom['partNumber']}")
            print(f"    📋 Items: {len(sample_bom['bomItems'])}")
        else:
            print(f"    📋 Sample BOM created with {len(sample_bom['bomItems'])} items")
    except Exception as e:
        print(f"[5] Upload BOM: ❌ FAIL: {str(e)}")

    print("\n" + "=" * 60)
    print(" TEST STRUCTURE SUMMARY")
    print("=" * 60)
    print("✅ 5 test methods implemented:")
    print("  1. test_get_product_info() - Get product by part number/revision")
    print("  2. test_get_products() - Search products with filters")
    print("  3. test_update_product() - Update product information")
    print("  4. test_get_bom() - Get Bill of Materials")
    print("  5. test_upload_bom() - Upload BOM data")
    print()
    print("📁 Supporting files:")
    print("  - product_config.py (configuration)")
    print("  - product_utils.py (utilities)")
    print("  - test_data/sample_data.json (sample data)")
    print("  - README.md (documentation)")
    
    print()
    print("🏁 MES Product Test Demo Complete!")


if __name__ == "__main__":
    main()