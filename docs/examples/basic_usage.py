"""
PyWATS Basic Usage Example

This example demonstrates basic usage of the PyWATS library for interacting 
with the WATS API.

Setup:
    1. Copy .env.template to .env
    2. Update WATS_BASE_URL and WATS_AUTH_TOKEN with your values
    3. Run: python -m docs.examples.basic_usage
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from pywats import pyWATS, WATSFilter


def main():
    # Initialize the API with credentials from environment variables
    api = pyWATS(
        base_url=os.getenv("WATS_BASE_URL"),
        token=os.getenv("WATS_AUTH_TOKEN"),
    )

    print("PyWATS Basic Usage Example")
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
        for p in products[:3]:
            print(f"   - {p.part_number}: {p.name}")

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

    # =========================================================================
    # Report Operations
    # =========================================================================

    print("\n4. Report Operations")
    print("-" * 50)

    # Query recent UUT report headers
    print("   Querying recent UUT reports...")
    filter = WATSFilter(top_count=10)
    headers = api.report.query_uut_headers(filter)
    print(f"   Found {len(headers)} report headers")

    if headers:
        for h in headers[:3]:
            print(f"   - {h.serial_number} | {h.part_number} | {h.status}")

    # =========================================================================
    # App Statistics
    # =========================================================================

    print("\n5. Statistics Operations")
    print("-" * 50)

    # Get processes
    print("   Getting processes...")
    processes = api.app.get_processes()
    print(f"   Found {len(processes)} processes")

    for p in processes[:5]:
        print(f"   - [{p.process_code}] {p.process_name}")

    print("\n" + "=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()
