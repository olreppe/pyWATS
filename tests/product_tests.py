"""
pyWATS Main Example - API Explorer

This file initializes the pyWATS 2.0 API for exploration.
"""



from pyWATS.api import WATSApi
from pyWATS.rest_api.public.models.virinco_wats_web_dashboard_models_mes_product_public_product import (
    VirincoWATSWebDashboardModelsMesProductPublicProduct as Product
)
from pyWATS.rest_api.public.models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import (
    VirincoWATSWebDashboardModelsMesProductPublicProductRevision as Revision
)


def main():
    """
    Initialize the pyWATS API for exploration.
    """
    print("Initializing pyWATS API...")
    
    # Initialize API with example configuration
    api = WATSApi(
        base_url="https://ola.wats.com",
        token="cHlXQVRTVGVzdDpNSDBENTQ0c2YzYlVpR1NFdXdmVjlxNEs0RFVPITc="
    )

    # api.refresh_operations(force=True)
    
 
 
    # Get Product (without revision) - Returns Product model
    print("\n=== Testing Product ===")
    try:
        result = api.product.get_product("ABC123")
        if result and isinstance(result, Product):
            print(f"Product retrieved: {result.part_number} - {result.name}")
            print(f"Type: {type(result).__name__}")
            print(f"Product has {len(result.revisions) if result.revisions else 0} revisions")
            
            # Update product
            # Note: Clear read-only fields before updating
            from pyWATS.rest_api.public.types import UNSET
            import json
            
            result.name = "Updated Product Name"
            result.revisions = UNSET  # Clear revisions - it's read-only
            result.product_category_name = UNSET  # Clear category name - it's read-only
            
            # Print the JSON that will be sent to the server
            json_data = result.to_dict()
            print("\n=== JSON being sent to PUT /api/Product ===")
            print(json.dumps(json_data, indent=2))
            print("=" * 50)
            
            print(f"\nSending update with product_id: {result.product_id}")
            updated_product = api.product.update_product(result)
            if updated_product:
                print(f"Product updated successfully: {updated_product.name}")
    except Exception as e:
        print(f"Error with product: {e}")
    
    # Get Product with Revision - Returns ProductRevision model
    print("\n=== Testing Product Revision ===")
    try:
        revision = api.product.get_product_revision("ABC123", "1")
        if revision:
            print(f"Revision retrieved: {revision.part_number} Rev {revision.revision}")
            print(f"Type: {type(revision).__name__}")
            
            # Update product revision
            revision.description = "Updated revision description"
            updated_revision = api.product.update_product_revision(revision)
            if updated_revision:
                print(f"Revision updated successfully: {updated_revision.description}")
    except Exception as e:
        print(f"Error with revision: {e}")
    
    # Alternative: get_product with revision parameter also returns ProductRevision
    print("\n=== Testing get_product with revision parameter ===")
    try:
        result = api.product.get_product("ABC123", revision="1")
        if result and isinstance(result, Revision):
            print(f"Retrieved via get_product: {result.part_number} Rev {result.revision}")
            print(f"Type: {type(result).__name__}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Get all products (returns objects)
    products = api.product.get_products()
    
    for product in products:
        print(f"Product: {product.part_number} (Name: {product.name})")  
    
    
    
    
    
    
    return api

if __name__ == "__main__":
    main()  # Changed from api = main()