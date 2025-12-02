"""
pyWATS Main Example - API Explorer

This file initializes the pyWATS 2.0 API for exploration.
"""



from pyWATS.api import WATSApi


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
    
 
    # Product
    product = api.product.get_product("partNumer eq 'ABC123'",1,True, True)
    
       
    products = api.product.get_all()
    for product in products:
        print(f"Product: {product['partNumber']} (ID: {product['name']})")  
    
    
    
    
    
    
    return api

if __name__ == "__main__":
    main()  # Changed from api = main()