"""
pyWATS Usage Examples

This file demonstrates the clean, object-oriented usage of the refactored pyWATS library.
"""

# Add the src_refactored folder to path for testing
import sys
sys.path.insert(0, "src_refactored")

from pywats import pyWATS, WATSFilter, Product, ProductState

# For report creation, import the models
from pywats.models.report import UUTReport, UURReport


def main():
    # =========================================================================
    # Initialize the API
    # =========================================================================
    
    # Create API instance with your WATS server URL and token
    api = pyWATS(
        base_url="https://ola.wats.com",
        token="cHlXQVRTVGVzdDpNSDBENTQ0c2YzYlVpR1NFdXdmVjlxNEs0RFVPITc="
    )
    
    print("pyWATS Refactored Example")
    print("=" * 50)
    
    # =========================================================================
    # Test Connection
    # =========================================================================
    
    print("\n1. Testing Connection...")
    if api.test_connection():
        print("   ✓ Connection successful!")
        version = api.get_version()
        print(f"   Server version: {version}")
    else:
        print("   ✗ Connection failed!")
        return
    
    # =========================================================================
    # Product Operations
    # =========================================================================
    
    print("\n2. Product Operations")
    print("-" * 50)
    
    # Get all products
    print("   Getting all products...")
    products = api.product.get_products()
    print(f"   Found {len(products)} products")
    
    if products:
        # Display first few products
        for p in products[:3]:
            print(f"   - {p.part_number}: {p.name} (State: {p.state.name})")
    
    # Get a specific product
    if products:
        part_number = products[0].part_number
        print(f"\n   Getting product '{part_number}'...")
        product = api.product.get_product(part_number)
        if product:
            print(f"   ✓ Found: {product.name}")
            print(f"     Part Number: {product.part_number}")
            print(f"     Description: {product.description}")
            print(f"     Revisions: {len(product.revisions)}")
            
            # Get a specific revision
            if product.revisions:
                rev = product.revisions[0]
                print(f"\n   Getting revision '{rev.revision}'...")
                revision = api.product.get_product_revision(part_number, rev.revision)
                if revision:
                    print(f"   ✓ Revision: {revision.revision}")
                    print(f"     Name: {revision.name}")
    
    # =========================================================================
    # Asset Operations
    # =========================================================================
    
    print("\n3. Asset Operations")
    print("-" * 50)
    
    # Get asset types
    print("   Getting asset types...")
    asset_types = api.asset.get_asset_types()
    print(f"   Found {len(asset_types)} asset types")
    
    for at in asset_types[:3]:
        print(f"   - {at.type_name}")
    
    # Get all assets
    print("\n   Getting all assets...")
    assets = api.asset.get_assets()
    print(f"   Found {len(assets)} assets")
    
    if assets:
        for a in assets[:3]:
            print(f"   - {a.serial_number}: {a.asset_name} (State: {a.state.name})")
    
    # =========================================================================
    # Report Operations
    # =========================================================================
    
    print("\n4. Report Operations")
    print("-" * 50)
    
    # Query UUT report headers
    print("   Querying UUT reports...")
    filter = WATSFilter(top_count=10)
    headers = api.report.query_uut_headers(filter)
    print(f"   Found {len(headers)} report headers")
    
    if headers:
        for h in headers[:3]:
            print(f"   - {h.serial_number} | {h.part_number} | {h.status}")
    
    # =========================================================================
    # Production Operations
    # =========================================================================
    
    print("\n5. Production Operations")
    print("-" * 50)
    
    # Get serial number types
    print("   Getting serial number types...")
    sn_types = api.production.serial_number.get_types()
    print(f"   Found {len(sn_types)} serial number types")
    
    for snt in sn_types[:3]:
        print(f"   - {snt.name}: {snt.format}")
    
    # =========================================================================
    # Statistics (App Module)
    # =========================================================================
    
    print("\n6. Statistics Operations")
    print("-" * 50)
    
    # Get processes
    print("   Getting processes...")
    processes = api.app.get_processes()
    print(f"   Found {len(processes)} processes")
    
    for p in processes[:5]:
        print(f"   - [{p.process_code}] {p.process_name}")
    
    # Get levels
    print("\n   Getting levels...")
    levels = api.app.get_levels()
    print(f"   Found {len(levels)} levels")
    
    for l in levels[:5]:
        print(f"   - {l.level_name}")
    
    # Get product groups
    print("\n   Getting product groups...")
    groups = api.app.get_product_groups()
    print(f"   Found {len(groups)} product groups")
    
    for g in groups[:5]:
        print(f"   - {g.product_group_name}")
    
    # =========================================================================
    # Summary
    # =========================================================================
    
    print("\n" + "=" * 50)
    print("Example completed successfully!")
    print("\nThe refactored pyWATS provides:")
    print("  • Clean, object-oriented API: api.product.get_product(...)")
    print("  • Type-safe models with from_dict()/to_dict() methods")
    print("  • Organized modules: product, asset, production, report, app")
    print("  • Sub-modules: api.production.serial_number, api.production.verification")
    print("  • Built-in Basic authentication")
    print("=" * 50)


if __name__ == "__main__":
    main()
