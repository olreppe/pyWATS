"""
Product Examples - Products, Revisions, and BOMs

This example demonstrates how to work with products in pyWATS.

DOMAIN KNOWLEDGE: Product Hierarchy
====================================

Products in WATS represent the things you manufacture and test:

1. PRODUCT (Top Level)
   - The base product definition
   - Example: "Widget-2000 Controller"
   - Properties: Name, description, part number, state
   - Think of it as: The product family

2. PRODUCT REVISION
   - Specific version of a product
   - Example: "Widget-2000 Rev A", "Widget-2000 Rev B"
   - Properties: Revision name, changes from previous revision
   - Think of it as: The version/variant

3. BILL OF MATERIALS (BOM)
   - List of components required to build the product
   - Example: "Widget-2000 Rev A needs: 1x CPU, 2x RAM, 1x PCB"
   - Properties: Component part number, quantity, reference designators
   - Think of it as: The recipe/parts list

PRODUCT STATES:
===============

Products transition through these states:

1. Development
   - Product is being designed, not ready for production
   - Can be modified freely

2. Active
   - Product is in production
   - Standard state for manufactured products

3. Obsolete
   - Product is no longer manufactured
   - Historical data still accessible

4. Discontinued
   - Product manufacturing stopped but may still be supported

COMPLETE WORKFLOW:
==================
1. Create product with basic info
2. Add revisions as design evolves
3. Define BOM for each revision
4. Set product state (Development → Active)
5. Create production units referencing product + revision
6. Query product hierarchy and BOMs
7. Archive obsolete products
"""

from pywats import pyWATS
from pywats.domains.product.enums import ProductState
from datetime import datetime
import os


def example_1_create_simple_product(api: pyWATS):
    """
    Step 1: Create a basic product with one revision.
    
    This is the minimum needed to start production testing.
    """
    print("=" * 60)
    print("EXAMPLE 1: Simple Product Creation")
    print("=" * 60)
    
    product_name = "CTRL-1000"
    
    # Create product
    product = api.product.create_product(
        name=product_name,
        description="Industrial Controller Module",
        part_number="PN-CTRL-1000-001",
        state=ProductState.Development  # Start in development
    )
    
    print(f"Created product: {product.name}")
    print(f"  Product ID: {product.id}")
    print(f"  Part Number: {product.part_number}")
    print(f"  State: {product.state}")
    
    # Create first revision
    revision = api.product.create_product_revision(
        product_id=product.id,
        name="Rev A",
        description="Initial production revision"
    )
    
    print(f"\nCreated revision: {revision.name}")
    print(f"  Revision ID: {revision.id}")
    print(f"  Description: {revision.description}")
    
    print("=" * 60)
    
    return product.id, revision.id


def example_2_product_revisions(api: pyWATS):
    """
    Step 2: Create multiple revisions to track design changes.
    
    Demonstrates revision evolution with design changes.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Multiple Product Revisions")
    print("=" * 60)
    
    product_name = "SENSOR-500"
    
    # Create product
    product = api.product.create_product(
        name=product_name,
        description="Temperature Sensor Module",
        part_number="PN-SENS-500"
    )
    
    print(f"Product: {product.name}")
    
    # Create revision history
    rev_a = api.product.create_product_revision(
        product_id=product.id,
        name="Rev A",
        description="Initial release - prototype PCB"
    )
    print(f"\n  Rev A (Prototype):")
    print(f"    ID: {rev_a.id}")
    print(f"    Initial design with prototype components")
    
    rev_b = api.product.create_product_revision(
        product_id=product.id,
        name="Rev B",
        description="Production release - Updated sensor IC, improved calibration"
    )
    print(f"\n  Rev B (Production):")
    print(f"    ID: {rev_b.id}")
    print(f"    Changed sensor IC from TMP100 to TMP117")
    print(f"    Added calibration EEPROM")
    
    rev_c = api.product.create_product_revision(
        product_id=product.id,
        name="Rev C",
        description="Cost reduction - Alternative connector, RoHS compliance"
    )
    print(f"\n  Rev C (Cost Reduced):")
    print(f"    ID: {rev_c.id}")
    print(f"    Replaced Molex connector with cheaper alternative")
    print(f"    Updated to RoHS-compliant components")
    
    # List all revisions
    revisions = api.product.get_product_revisions(product_id=product.id)
    print(f"\nTotal revisions for {product_name}: {len(revisions)}")
    
    print("=" * 60)
    
    return product.id


def example_3_bill_of_materials(api: pyWATS):
    """
    Step 3: Define a Bill of Materials (BOM) for a product revision.
    
    The BOM lists all components needed to build the product.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Bill of Materials (BOM)")
    print("=" * 60)
    
    product_name = "PSU-250"
    
    # Create product and revision
    product = api.product.create_product(
        name=product_name,
        description="250W Power Supply Module"
    )
    
    revision = api.product.create_product_revision(
        product_id=product.id,
        name="Rev A"
    )
    
    print(f"Product: {product_name} {revision.name}")
    print(f"\nBill of Materials:")
    
    # Add BOM items
    bom_items = [
        {
            "part_number": "PCB-PSU-250-A",
            "description": "Main PCB",
            "quantity": 1,
            "reference_designators": "PCB1"
        },
        {
            "part_number": "IC-REG-LM7805",
            "description": "5V Linear Regulator",
            "quantity": 1,
            "reference_designators": "U1"
        },
        {
            "part_number": "IC-REG-LM7812",
            "description": "12V Linear Regulator",
            "quantity": 1,
            "reference_designators": "U2"
        },
        {
            "part_number": "CAP-100uF-25V",
            "description": "Electrolytic Capacitor 100uF 25V",
            "quantity": 4,
            "reference_designators": "C1,C2,C3,C4"
        },
        {
            "part_number": "RES-10K-1%",
            "description": "Resistor 10K 1/4W 1%",
            "quantity": 6,
            "reference_designators": "R1,R2,R3,R4,R5,R6"
        },
        {
            "part_number": "XFMR-250W",
            "description": "Power Transformer 250W",
            "quantity": 1,
            "reference_designators": "T1"
        }
    ]
    
    for item in bom_items:
        bom_entry = api.product.add_bom_item(
            revision_id=revision.id,
            part_number=item["part_number"],
            description=item["description"],
            quantity=item["quantity"],
            reference_designators=item["reference_designators"]
        )
        print(f"  [{item['quantity']}x] {item['part_number']}")
        print(f"       {item['description']}")
        print(f"       Ref: {item['reference_designators']}")
    
    # Retrieve complete BOM
    bom = api.product.get_bom(revision_id=revision.id)
    print(f"\nTotal BOM items: {len(bom)}")
    print(f"Total unique components: {len(bom)}")
    print(f"Total parts required: {sum(item.quantity for item in bom)}")
    
    print("=" * 60)
    
    return product.id, revision.id


def example_4_product_states(api: pyWATS):
    """
    Step 4: Manage product lifecycle states.
    
    Move products through Development → Active → Obsolete.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Product Lifecycle States")
    print("=" * 60)
    
    product_name = "WIDGET-OLD"
    
    # Create product in Development
    product = api.product.create_product(
        name=product_name,
        description="Legacy widget being phased out",
        state=ProductState.Development
    )
    
    print(f"Product: {product.name}")
    print(f"Initial state: {product.state}")
    
    # Create revision
    revision = api.product.create_product_revision(
        product_id=product.id,
        name="Rev A"
    )
    
    # Move to Active (ready for production)
    print(f"\n1. Moving to Active (production ready)...")
    api.product.update_product(
        product_id=product.id,
        state=ProductState.Active
    )
    product = api.product.get_product_by_id(product.id)
    print(f"   State: {product.state}")
    print(f"   → Product can now be manufactured and tested")
    
    # Later: Move to Discontinued (stop manufacturing but keep support)
    print(f"\n2. Moving to Discontinued (end of manufacturing)...")
    api.product.update_product(
        product_id=product.id,
        state=ProductState.Discontinued
    )
    product = api.product.get_product_by_id(product.id)
    print(f"   State: {product.state}")
    print(f"   → No new units, but existing units still supported")
    
    # Finally: Move to Obsolete (archived)
    print(f"\n3. Moving to Obsolete (archived)...")
    api.product.update_product(
        product_id=product.id,
        state=ProductState.Obsolete
    )
    product = api.product.get_product_by_id(product.id)
    print(f"   State: {product.state}")
    print(f"   → Product archived, historical data retained")
    
    print("\nProduct lifecycle complete")
    print("=" * 60)
    
    return product.id


def example_5_product_families(api: pyWATS):
    """
    Step 5: Create a product family with variants.
    
    Example: Base product with different memory configurations.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Product Families")
    print("=" * 60)
    
    print("Creating CTRL-2000 family (different memory variants):\n")
    
    # Base product with different revisions for variants
    variants = [
        {
            "name": "CTRL-2000-8G",
            "description": "Controller with 8GB RAM",
            "part_number": "PN-CTRL-2000-8G",
            "memory": "8GB"
        },
        {
            "name": "CTRL-2000-16G",
            "description": "Controller with 16GB RAM",
            "part_number": "PN-CTRL-2000-16G",
            "memory": "16GB"
        },
        {
            "name": "CTRL-2000-32G",
            "description": "Controller with 32GB RAM",
            "part_number": "PN-CTRL-2000-32G",
            "memory": "32GB"
        }
    ]
    
    for variant in variants:
        product = api.product.create_product(
            name=variant["name"],
            description=variant["description"],
            part_number=variant["part_number"],
            state=ProductState.Active
        )
        
        revision = api.product.create_product_revision(
            product_id=product.id,
            name="Rev A"
        )
        
        print(f"  {variant['name']}")
        print(f"    Memory: {variant['memory']}")
        print(f"    Part Number: {variant['part_number']}")
        print(f"    Product ID: {product.id}")
        print()
    
    print("Product family created (3 variants)")
    print("=" * 60)


def example_6_query_products(api: pyWATS):
    """
    Step 6: Query and filter products.
    
    Find products by various criteria.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Query Products")
    print("=" * 60)
    
    # Get all products
    all_products = api.product.get_products()
    print(f"\nTotal products in database: {len(all_products)}")
    
    # Filter by state
    active_products = [p for p in all_products if p.state == ProductState.Active]
    print(f"Active products: {len(active_products)}")
    
    dev_products = [p for p in all_products if p.state == ProductState.Development]
    print(f"Development products: {len(dev_products)}")
    
    # Search by name pattern
    controllers = [p for p in all_products if "CTRL" in p.name]
    print(f"\nController products (CTRL-*)): {len(controllers)}")
    for ctrl in controllers[:5]:  # Show first 5
        print(f"  - {ctrl.name}: {ctrl.description}")
    
    # Get specific product by name
    print(f"\nSearching for specific product...")
    product = api.product.get_product_by_name("CTRL-1000")
    if product:
        print(f"  Found: {product.name}")
        print(f"  ID: {product.id}")
        print(f"  State: {product.state}")
        
        # Get its revisions
        revisions = api.product.get_product_revisions(product_id=product.id)
        print(f"  Revisions: {len(revisions)}")
        for rev in revisions:
            print(f"    - {rev.name}: {rev.description}")
    
    print("\n" + "=" * 60)


def example_7_product_with_attachments(api: pyWATS):
    """
    Step 7: Add documentation and files to products.
    
    Attach datasheets, schematics, etc.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Product Documentation")
    print("=" * 60)
    
    product_name = "MODULE-300"
    
    # Create product
    product = api.product.create_product(
        name=product_name,
        description="Multi-function I/O Module with documentation"
    )
    
    revision = api.product.create_product_revision(
        product_id=product.id,
        name="Rev A"
    )
    
    print(f"Product: {product_name} Rev A")
    print(f"\nDocumentation:")
    
    # In a real scenario, you would attach actual files
    # This example shows the metadata structure
    documentation = [
        {
            "type": "Datasheet",
            "filename": "MODULE-300_Datasheet_RevA.pdf",
            "description": "Product specifications and characteristics"
        },
        {
            "type": "Schematic",
            "filename": "MODULE-300_Schematic_RevA.pdf",
            "description": "Circuit diagram"
        },
        {
            "type": "Assembly",
            "filename": "MODULE-300_Assembly_RevA.pdf",
            "description": "Assembly drawing and BOM"
        },
        {
            "type": "Test Procedure",
            "filename": "MODULE-300_Test_RevA.pdf",
            "description": "Manufacturing test procedure"
        }
    ]
    
    for doc in documentation:
        print(f"  [{doc['type']}] {doc['filename']}")
        print(f"    {doc['description']}")
        # In actual code:
        # api.product.add_attachment(
        #     revision_id=revision.id,
        #     file_path=doc['filename'],
        #     description=doc['description']
        # )
    
    print(f"\nTotal documentation files: {len(documentation)}")
    print("=" * 60)


def main():
    """Run all product examples."""
    # Connect to WATS API
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")
    
    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)
    
    print("=" * 60)
    print("PRODUCT DOMAIN EXAMPLES")
    print("Demonstrates products, revisions, and BOMs")
    print("=" * 60)
    
    # Run examples
    example_1_create_simple_product(api)
    example_2_product_revisions(api)
    example_3_bill_of_materials(api)
    example_4_product_states(api)
    example_5_product_families(api)
    example_6_query_products(api)
    example_7_product_with_attachments(api)
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
