#!/usr/bin/env python3
"""
Example usage of the regenerated pyWATS REST API

This script demonstrates how to use the newly generated REST API clients
with the unified WatsHttpClient.
"""

from pyWATS.rest_api import WatsHttpClient
from pyWATS.rest_api.public.api.app import app_dynamic_yield
from pyWATS.rest_api.public.api.product import product_public_get_products
from pyWATS.rest_api.public.api.asset import asset_get_assets


def main():
    """Example usage of the new REST API."""
    
    # Create the unified HTTP client
    client = WatsHttpClient(
        base_url="https://live.wats.com",
        base64_token="your_base64_encoded_token_here"
    )
    
    print("🚀 pyWATS REST API Usage Examples")
    print("=" * 50)
    
    # Example 1: Using the client with context manager
    print("\n📊 Example 1: Get products")
    try:
        with client:
            # Note: In real usage, you would call the actual API endpoint
            # This is just showing the import structure
            print(f"✅ product_public_get_products function available: {product_public_get_products}")
            print("   Call: product_public_get_products.sync(client=client)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Get dynamic yield data
    print("\n📈 Example 2: Get dynamic yield analytics")
    try:
        print(f"✅ app_dynamic_yield function available: {app_dynamic_yield}")
        print("   Call: app_dynamic_yield.sync(client=client, body={...})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Get assets
    print("\n🏭 Example 3: Get assets")
    try:
        print(f"✅ asset_get_assets function available: {asset_get_assets}")
        print("   Call: asset_get_assets.sync(client=client)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✨ REST API regeneration complete!")
    print("\n📚 Available API endpoints:")
    print("  Public API:")
    print("    • src/pyWATS/rest_api/public/api/app/ - Analytics endpoints")
    print("    • src/pyWATS/rest_api/public/api/product/ - Product management")
    print("    • src/pyWATS/rest_api/public/api/production/ - Production data")
    print("    • src/pyWATS/rest_api/public/api/asset/ - Asset management")
    print("    • src/pyWATS/rest_api/public/api/report/ - Reporting")
    print("    • And many more...")
    print("\n  Internal API:")
    print("    • src/pyWATS/rest_api/internal/api/ - Internal endpoints")
    print("    • (Same structure as public API)")
    
    print("\n🔧 Usage pattern:")
    print("""
    from pyWATS.rest_api import WatsHttpClient
    from pyWATS.rest_api.public.api.app import app_dynamic_yield
    
    client = WatsHttpClient(base_url="https://your-server.com", base64_token="token")
    
    with client:
        result = app_dynamic_yield.sync(
            client=client,
            body={
                "partNumber": "PART001",
                "testOperation": "Final Test"
            }
        )
        print(result)
    """)


if __name__ == "__main__":
    main()