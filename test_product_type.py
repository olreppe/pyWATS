"""Quick test to check what type get_product returns"""
from pyWATS.pyWATS import pyWATS

# Initialize API
api = pyWATS()

# Test get_product without revision
print("Testing get_product without revision...")
product = api.product.get_product("ABC123")
print(f"Type returned: {type(product)}")
print(f"Type name: {type(product).__name__}")
print(f"Has revisions attribute: {hasattr(product, 'revisions')}")

if product:
    print(f"Product ID: {product.product_id}")
    print(f"Part Number: {product.part_number}")
    if hasattr(product, 'revisions'):
        print(f"Number of revisions: {len(product.revisions) if product.revisions else 0}")

# Test get_product_revision with revision
print("\n\nTesting get_product_revision with revision...")
revision = api.product.get_product_revision("ABC123", "1")
print(f"Type returned: {type(revision)}")
print(f"Type name: {type(revision).__name__}")
print(f"Has revisions attribute: {hasattr(revision, 'revisions')}")

if revision:
    print(f"Product ID: {revision.product_id}")
    print(f"Part Number: {revision.part_number}")
    print(f"Revision: {revision.revision}")
