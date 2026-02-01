"""
Box Build Examples - Multi-Level Product Assemblies

This example demonstrates how to work with box build functionality in pyWATS.

DOMAIN KNOWLEDGE: Templates vs. Units
======================================

Understanding this distinction is CRITICAL:

1. BOX BUILD TEMPLATE (Product Domain)
   - DESIGN-TIME definition of what subunits are required
   - Lives in: Product domain (api.product)
   - Example: "Controller Module CTRL-100 requires 1x Power Supply and 2x Sensor Boards"
   - Think of it as: The blueprint/recipe

2. UNIT ASSEMBLY (Production Domain)
   - RUNTIME attachment of actual units (with serial numbers)
   - Lives in: Production domain (api.production)
   - Example: "Unit CTRL-SN-001 contains PSU-SN-456, SENSOR-SN-789, SENSOR-SN-790"
   - Think of it as: The actual built product

The template defines WHAT is needed; the assembly records WHAT was actually used.

COMPLETE WORKFLOW:
==================
1. Create parent and child products with revisions
2. Define box build template (what subunits are required)
3. Create production units with serial numbers
4. Test and finalize child units (REQUIRED before assembly)
5. Build the assembly (attach child units to parent)
6. Query assembly structure
7. Disassemble if needed (remove child units)
"""

from pywats import pyWATS
from pywats.domains.product.enums import ProductState
from pywats.domains.production import Unit
import os


def example_1_create_products_and_revisions(api: pyWATS):
    """
    Step 1: Create the parent and child products.
    
    In this example:
    - Parent: CTRL-100 (Controller Module)
    - Children: PSU-200 (Power Supply), SENSOR-300 (Sensor Board)
    """
    print("=" * 60)
    print("Step 1: Creating Products and Revisions")
    print("=" * 60)
    
    # Create child product: Power Supply
    print("\n✓ Creating Power Supply product...")
    api.product.create_product(
        part_number="PSU-200",
        name="Power Supply Unit",
        description="24V DC Power Supply",
        state=ProductState.ACTIVE
    )
    api.product.create_revision(
        part_number="PSU-200",
        revision="A",
        state=ProductState.ACTIVE
    )
    
    # Create child product: Sensor Board
    print("✓ Creating Sensor Board product...")
    api.product.create_product(
        part_number="SENSOR-300",
        name="Sensor Board",
        description="Temperature and Humidity Sensor",
        state=ProductState.ACTIVE
    )
    api.product.create_revision(
        part_number="SENSOR-300",
        revision="A",
        state=ProductState.ACTIVE
    )
    
    # Create parent product: Controller Module
    print("✓ Creating Controller Module product...")
    api.product.create_product(
        part_number="CTRL-100",
        name="Controller Module",
        description="Main Controller with Power Supply and Sensors",
        state=ProductState.ACTIVE
    )
    api.product.create_revision(
        part_number="CTRL-100",
        revision="A",
        state=ProductState.ACTIVE
    )
    
    print("\n✅ All products and revisions created successfully!")


def example_2_define_box_build_template(api: pyWATS):
    """
    Step 2: Define the box build template.
    
    This tells WATS: "To build CTRL-100 rev A, you need:
    - 1x PSU-200 rev A
    - 2x SENSOR-300 rev A"
    
    This is the DESIGN-TIME specification, not the actual assembly.
    """
    print("\n" + "=" * 60)
    print("Step 2: Defining Box Build Template")
    print("=" * 60)
    
    # Get the box build template (creates if doesn't exist)
    template = api.product.get_box_build_template("CTRL-100", "A")
    
    # Add required subunits
    print("\n✓ Adding Power Supply requirement (quantity: 1)...")
    template.add_subunit(
        part_number="PSU-200",
        revision="A",
        quantity=1
    )
    
    print("✓ Adding Sensor Board requirement (quantity: 2)...")
    template.add_subunit(
        part_number="SENSOR-300",
        revision="A",
        quantity=2
    )
    
    # Save the template to WATS
    template.save()
    
    print("\n✅ Box build template defined successfully!")
    print(f"   Template says: CTRL-100 rev A requires {len(template.subunits)} subunit types")
    
    # Alternative: Use context manager (auto-saves)
    print("\n💡 TIP: Use context manager for automatic saving:")
    print("   with api.product.get_box_build_template('CTRL-100', 'A') as bb:")
    print("       bb.add_subunit('PSU-200', 'A', quantity=1)")
    print("       # Automatically saved when exiting context")


def example_3_create_production_units(api: pyWATS):
    """
    Step 3: Create actual production units with serial numbers.
    
    These are the REAL units that will be built and tested.
    """
    print("\n" + "=" * 60)
    print("Step 3: Creating Production Units")
    print("=" * 60)
    
    # Create parent unit (Controller Module)
    print("\n✓ Creating parent unit: CTRL-SN-001...")
    parent_unit = Unit(
        serial_number="CTRL-SN-001",
        part_number="CTRL-100",
        revision="A"
    )
    
    # Create child units (Power Supply and 2 Sensor Boards)
    print("✓ Creating child unit 1: PSU-SN-456 (Power Supply)...")
    psu_unit = Unit(
        serial_number="PSU-SN-456",
        part_number="PSU-200",
        revision="A"
    )
    
    print("✓ Creating child unit 2: SENSOR-SN-789 (Sensor Board #1)...")
    sensor1_unit = Unit(
        serial_number="SENSOR-SN-789",
        part_number="SENSOR-300",
        revision="A"
    )
    
    print("✓ Creating child unit 3: SENSOR-SN-790 (Sensor Board #2)...")
    sensor2_unit = Unit(
        serial_number="SENSOR-SN-790",
        part_number="SENSOR-300",
        revision="A"
    )
    
    # Save all units to WATS
    api.production.create_units([parent_unit, psu_unit, sensor1_unit, sensor2_unit])
    
    print("\n✅ All production units created successfully!")
    print("   Units created: CTRL-SN-001, PSU-SN-456, SENSOR-SN-789, SENSOR-SN-790")


def example_4_test_and_finalize_child_units(api: pyWATS):
    """
    Step 4: Test and finalize child units.
    
    CRITICAL REQUIREMENT: Child units MUST be finalized before they can be
    added to an assembly. This ensures all child units have passed testing.
    
    In a real scenario, you would:
    1. Run tests on the child unit (submit UUT reports)
    2. Verify all tests passed
    3. Set unit phase to "Finalized"
    """
    print("\n" + "=" * 60)
    print("Step 4: Testing and Finalizing Child Units")
    print("=" * 60)
    
    child_units = [
        ("PSU-SN-456", "PSU-200"),
        ("SENSOR-SN-789", "SENSOR-300"),
        ("SENSOR-SN-790", "SENSOR-300"),
    ]
    
    for serial, part in child_units:
        print(f"\n✓ Testing {serial}...")
        # In real scenario: Submit test reports here
        # api.report.send_uut_report(test_report)
        
        print(f"✓ Setting {serial} to Finalized phase...")
        api.production.set_unit_phase(
            serial_number=serial,
            part_number=part,
            phase="Finalized"  # or phase=16 (the phase ID)
        )
    
    print("\n✅ All child units tested and finalized!")
    print("   ⚠️  Important: Child units are now locked and ready for assembly")


def example_5_build_assembly(api: pyWATS):
    """
    Step 5: Build the assembly by attaching child units to parent.
    
    This is the RUNTIME assembly - attaching actual serial numbered units
    to create the final product.
    
    IMPORTANT NOTES:
    - Child units must be in "Finalized" phase
    - Child units must match the box build template (correct part numbers)
    - Child units become locked (cannot be modified) once added to assembly
    - Assembly history is tracked (who built it, when, where)
    """
    print("\n" + "=" * 60)
    print("Step 5: Building the Assembly")
    print("=" * 60)
    
    parent_serial = "CTRL-SN-001"
    parent_part = "CTRL-100"
    
    # Add Power Supply to assembly
    print(f"\n✓ Adding Power Supply (PSU-SN-456) to {parent_serial}...")
    api.production.add_child_to_assembly(
        parent_serial=parent_serial,
        parent_part=parent_part,
        child_serial="PSU-SN-456",
        child_part="PSU-200"
    )
    
    # Add Sensor Board #1 to assembly
    print(f"✓ Adding Sensor Board #1 (SENSOR-SN-789) to {parent_serial}...")
    api.production.add_child_to_assembly(
        parent_serial=parent_serial,
        parent_part=parent_part,
        child_serial="SENSOR-SN-789",
        child_part="SENSOR-300"
    )
    
    # Add Sensor Board #2 to assembly
    print(f"✓ Adding Sensor Board #2 (SENSOR-SN-790) to {parent_serial}...")
    api.production.add_child_to_assembly(
        parent_serial=parent_serial,
        parent_part=parent_part,
        child_serial="SENSOR-SN-790",
        child_part="SENSOR-300"
    )
    
    print(f"\n✅ Assembly {parent_serial} built successfully!")
    print("   Contains: PSU-SN-456, SENSOR-SN-789, SENSOR-SN-790")


def example_6_query_assembly_structure(api: pyWATS):
    """
    Step 6: Query the assembly structure.
    
    Retrieve information about what child units are in an assembly,
    or what parent a child unit belongs to.
    """
    print("\n" + "=" * 60)
    print("Step 6: Querying Assembly Structure")
    print("=" * 60)
    
    parent_serial = "CTRL-SN-001"
    parent_part = "CTRL-100"
    
    # Get all child units in the assembly
    print(f"\n✓ Getting child units for assembly {parent_serial}...")
    children = api.production.get_assembly_children(
        parent_serial=parent_serial,
        parent_part=parent_part
    )
    
    print(f"\n📦 Assembly {parent_serial} contains {len(children)} child units:")
    for child in children:
        print(f"   - {child.serial_number} ({child.part_number} rev {child.revision})")
        print(f"     Added: {child.assembly_date}")
        print(f"     By: {child.assembled_by}")
    
    # Query parent of a child unit
    child_serial = "PSU-SN-456"
    print(f"\n✓ Getting parent assembly for child unit {child_serial}...")
    parent = api.production.get_unit_parent(
        serial_number=child_serial,
        part_number="PSU-200"
    )
    
    if parent:
        print(f"\n🔗 Child unit {child_serial} belongs to parent:")
        print(f"   Parent: {parent.serial_number} ({parent.part_number})")
    else:
        print(f"\n   Child unit {child_serial} is not in any assembly")
    
    print("\n✅ Assembly structure queried successfully!")


def example_7_disassemble_units(api: pyWATS):
    """
    Step 7: Disassemble units (remove child from parent).
    
    Use cases:
    - Child unit failed testing after assembly
    - Need to rework/repair a child unit
    - Assembly was incorrect
    
    IMPORTANT:
    - Disassembly is tracked (who, when, why)
    - Child unit returns to available state
    - History is preserved (can see it was previously assembled)
    """
    print("\n" + "=" * 60)
    print("Step 7: Disassembling Units")
    print("=" * 60)
    
    parent_serial = "CTRL-SN-001"
    parent_part = "CTRL-100"
    child_serial = "SENSOR-SN-790"  # Remove one sensor board
    child_part = "SENSOR-300"
    
    # Option 1: Remove individual child unit
    print(f"\n✓ Removing individual child: {child_serial} from {parent_serial}...")
    api.production.remove_child_from_assembly(
        parent_serial=parent_serial,
        parent_part=parent_part,
        child_serial=child_serial,
        child_part=child_part
    )
    
    print(f"\n✅ Child unit {child_serial} removed from assembly!")
    print(f"   Status: {child_serial} is now available for other assemblies")
    
    # Option 2: Remove ALL children at once (convenience method)
    print(f"\n✓ Removing ALL remaining children from {parent_serial}...")
    print("   This is a convenience method equivalent to C#'s RemoveAllChildUnits()")
    api.production.remove_all_children_from_assembly(
        parent_serial=parent_serial,
        parent_part=parent_part
    )
    
    print(f"\n✅ All child units removed from assembly {parent_serial}!")
    print(f"   Assembly is now empty and can be rebuilt")
    print(f"   All child units (PSU-SN-456, SENSOR-SN-789) are now available")
    print(f"   History: Disassembly timestamp recorded")


def example_8_validation_and_template_checking(api: pyWATS):
    """
    Step 8: Template validation and checking.
    
    WATS validates assemblies against templates:
    - Ensures correct child part numbers are used
    - Checks quantity requirements are met
    - Warns if assembly doesn't match template
    """
    print("\n" + "=" * 60)
    print("Step 8: Template Validation")
    print("=" * 60)
    
    parent_serial = "CTRL-SN-001"
    parent_part = "CTRL-100"
    
    # Get the template
    template = api.product.get_box_build_template("CTRL-100", "A")
    
    # Get actual assembly
    children = api.production.get_assembly_children(
        parent_serial=parent_serial,
        parent_part=parent_part
    )
    
    print(f"\n📋 Template Requirements:")
    for subunit in template.subunits:
        print(f"   - {subunit.quantity}x {subunit.part_number} rev {subunit.revision}")
    
    print(f"\n📦 Actual Assembly:")
    from collections import Counter
    actual_parts = Counter([f"{c.part_number} rev {c.revision}" for c in children])
    for part_rev, count in actual_parts.items():
        print(f"   - {count}x {part_rev}")
    
    # Validate
    print(f"\n✓ Checking if assembly matches template...")
    is_valid = True
    for subunit in template.subunits:
        key = f"{subunit.part_number} rev {subunit.revision}"
        actual_count = actual_parts.get(key, 0)
        if actual_count != subunit.quantity:
            print(f"   ⚠️  Mismatch: Expected {subunit.quantity}x {key}, got {actual_count}x")
            is_valid = False
    
    if is_valid:
        print("\n✅ Assembly matches template perfectly!")
    else:
        print("\n⚠️  Assembly does not match template (missing components)")


# =============================================================================
# ADVANCED PATTERNS
# =============================================================================

def example_9_multi_level_assemblies(api: pyWATS):
    """
    Advanced: Multi-level assemblies (assemblies within assemblies).
    
    Example hierarchy:
    
    SYSTEM-100 (Top-level system)
      ├── CTRL-SN-001 (Controller Module) ← This is itself an assembly!
      │   ├── PSU-SN-456 (Power Supply)
      │   ├── SENSOR-SN-789 (Sensor #1)
      │   └── SENSOR-SN-790 (Sensor #2)
      └── DISPLAY-SN-999 (Display Module)
    
    WATS supports unlimited nesting levels.
    """
    print("\n" + "=" * 60)
    print("Advanced: Multi-Level Assemblies")
    print("=" * 60)
    
    print("\n💡 Multi-level assemblies allow:")
    print("   - Sub-assemblies to be pre-built and tested")
    print("   - Modular manufacturing workflows")
    print("   - Complex product hierarchies")
    print("   - Traceability at every level")
    
    print("\n📋 Example: Adding Controller Module (which is itself an assembly)")
    print("   to a top-level System:")
    
    # Create top-level system
    print("\n   1. Create SYSTEM-100 unit")
    # api.production.create_units([Unit(serial_number="SYS-SN-001", part_number="SYSTEM-100", revision="A")])
    
    # Add controller module (which contains PSU and sensors) to system
    print("   2. Add CTRL-SN-001 (complete assembly) to SYSTEM")
    # api.production.add_child_to_assembly(
    #     parent_serial="SYS-SN-001", parent_part="SYSTEM-100",
    #     child_serial="CTRL-SN-001", child_part="CTRL-100"
    # )
    
    print("\n   Result: SYSTEM contains CONTROLLER, which contains PSU and SENSORS")
    print("   ✅ Full traceability through all levels!")


def example_10_assembly_history_and_rework(api: pyWATS):
    """
    Advanced: Assembly history and rework tracking.
    
    WATS tracks:
    - When child was added (assembly timestamp)
    - Who added it (operator/user)
    - When removed (disassembly timestamp)
    - Why removed (disassembly reason)
    - How many times a child has been assembled/disassembled
    
    This is crucial for:
    - Quality tracking
    - Rework analysis
    - Warranty claims
    - Compliance/audit trails
    """
    print("\n" + "=" * 60)
    print("Advanced: Assembly History & Rework")
    print("=" * 60)
    
    print("\n💡 Every assembly/disassembly operation is recorded:")
    print("   - Timestamp (when)")
    print("   - Operator (who)")
    print("   - Reason (why, for disassembly)")
    print("   - Location/station (where)")
    
    print("\n📊 Use cases:")
    print("   - Identify units with high rework rates")
    print("   - Track which operators perform assemblies")
    print("   - Audit trail for regulatory compliance")
    print("   - Warranty claim validation")
    
    child_serial = "PSU-SN-456"
    print(f"\n✓ Getting assembly history for {child_serial}...")
    # history = api.production.get_unit_assembly_history(
    #     serial_number=child_serial,
    #     part_number="PSU-200"
    # )
    # for event in history:
    #     print(f"   {event.timestamp}: {event.action} - Parent: {event.parent_serial}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Initialize pyWATS connection
    api = pyWATS(
        base_url=os.getenv("WATS_BASE_URL", "https://your-wats-server.com"),
        token=os.getenv("WATS_API_TOKEN", "your-token")
    )
    
    print("\n" + "=" * 60)
    print("BOX BUILD EXAMPLES - COMPLETE WORKFLOW")
    print("=" * 60)
    
    # Run all examples in sequence
    example_1_create_products_and_revisions(api)
    example_2_define_box_build_template(api)
    example_3_create_production_units(api)
    example_4_test_and_finalize_child_units(api)
    example_5_build_assembly(api)
    example_6_query_assembly_structure(api)
    example_7_disassemble_units(api)
    example_8_validation_and_template_checking(api)
    
    # Advanced examples (demonstration only, not executed)
    example_9_multi_level_assemblies(api)
    example_10_assembly_history_and_rework(api)
    
    print("\n" + "=" * 60)
    print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("1. Template = Blueprint (what's required)")
    print("2. Assembly = Actual build (what was used)")
    print("3. Child units must be finalized before assembly")
    print("4. All operations are tracked for traceability")
    print("5. Multi-level assemblies are supported")
