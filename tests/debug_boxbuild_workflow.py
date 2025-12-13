"""Debug script to demonstrate proper box build workflow using high-level API."""
import sys
import os
sys.path.insert(0, "src")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pywats import pyWATS
from pywats.domains.production.models import Unit
from tests.test_instances import get_test_instance_manager

# Connect to WATS using test instance config
manager = get_test_instance_manager()
config = manager.get_test_instance_config("A")
api = pyWATS(base_url=config.base_url, token=config.token)

print(f"Base URL: {config.base_url}")

# Test products
module_pn = "BOXBUILD-CONTROLLER-MODULE"
module_rev = "1.0"
sub_pn = "BOXBUILD-POWER-SUPPLY"
sub_rev = "A"

print("=" * 70)
print("DEBUG: Box Build Workflow Using High-Level API")
print("=" * 70)

# =========================================================================
# 1. Unit Phases (now cached in production service)
# =========================================================================
print("\n1. Available Unit Phases (via api.production.get_phases())...")
phases = api.production.get_phases()
print(f"   Found {len(phases)} phases:")
for phase in phases:
    print(f"     - {repr(phase)}")

# Test phase lookup
finalized = api.production.get_phase("Finalized")
print(f"\n   get_phase('Finalized'): {finalized}")
print(f"   get_phase_id('Finalized'): {api.production.get_phase_id('Finalized')}")

# =========================================================================
# 2. Box Build Template (uses BoxBuildTemplate manager)
# =========================================================================
print("\n2. Box Build Template Setup (via api.product_internal.get_box_build())...")

# The BoxBuildTemplate class prevents duplicates automatically
with api.product_internal.get_box_build(module_pn, module_rev) as bb:
    print(f"   Parent: {bb.parent_part_number} rev {bb.parent_revision}")
    print(f"   Existing subunits: {len(bb.subunits)}")
    
    # Check if we already have the subunit
    existing = [s for s in bb.subunits if s.child_part_number == sub_pn]
    if existing:
        print(f"   [SKIP] Subunit already exists: {sub_pn}")
    else:
        print(f"   Adding subunit: {sub_pn} rev {sub_rev}")
        bb.add_subunit(sub_pn, sub_rev, quantity=1)
    
    # Show final state
    print(f"   Final subunits: {len(bb.subunits)}")
    for su in bb.subunits:
        print(f"     - {su.child_part_number} rev {su.child_revision} (qty={su.quantity})")

# =========================================================================
# 3. Create/Get Test Units
# =========================================================================
print("\n3. Test Units...")
test_module_sn = "DEBUG-MODULE-003"
test_sub_sn = "DEBUG-PSU-003"

# Create or get module unit
try:
    mod_unit = api.production.get_unit(test_module_sn, module_pn)
    print(f"   Module unit exists: {mod_unit.serial_number}, phase={mod_unit.unit_phase}")
except:
    mod_unit = Unit(serial_number=test_module_sn, part_number=module_pn, revision=module_rev)
    api.production.create_units([mod_unit])
    mod_unit = api.production.get_unit(test_module_sn, module_pn)
    print(f"   Module unit created: {mod_unit.serial_number}")

# Create or get sub-part unit
try:
    sub_unit = api.production.get_unit(test_sub_sn, sub_pn)
    print(f"   Sub-part unit exists: {sub_unit.serial_number}, phase={sub_unit.unit_phase}")
except:
    sub_unit = Unit(serial_number=test_sub_sn, part_number=sub_pn, revision=sub_rev)
    api.production.create_units([sub_unit])
    sub_unit = api.production.get_unit(test_sub_sn, sub_pn)
    print(f"   Sub-part unit created: {sub_unit.serial_number}")

# =========================================================================
# 4. Set Phase (using name instead of ID)
# =========================================================================
print("\n4. Set Sub-part Phase to 'Finalized' (via api.production.set_unit_phase())...")

# Can use phase name OR phase ID
result = api.production.set_unit_phase(
    test_sub_sn, 
    sub_pn, 
    "Finalized",  # Can use "Finalized", "finalized", or 16
    comment="Finalized for assembly via debug script"
)
print(f"   Result: {result}")

# Verify
sub_unit = api.production.get_unit(test_sub_sn, sub_pn)
print(f"   Sub-part phase after update: {sub_unit.unit_phase}")

# =========================================================================
# 5. Add Child Unit (Assembly Link)
# =========================================================================
print("\n5. Add Child Unit to Assembly (via api.production.add_child_to_assembly())...")

# Check if already linked
mod_unit = api.production.get_unit(test_module_sn, module_pn)
if mod_unit.sub_units:
    existing_link = [su for su in mod_unit.sub_units if su.serial_number == test_sub_sn]
    if existing_link:
        print(f"   [SKIP] Child already linked: {test_sub_sn}")
    else:
        result = api.production.add_child_to_assembly(
            parent_serial=test_module_sn,
            parent_part=module_pn,
            child_serial=test_sub_sn,
            child_part=sub_pn
        )
        print(f"   Result: {result}")
else:
    result = api.production.add_child_to_assembly(
        parent_serial=test_module_sn,
        parent_part=module_pn,
        child_serial=test_sub_sn,
        child_part=sub_pn
    )
    print(f"   Result: {result}")

# =========================================================================
# 6. Verify Final State
# =========================================================================
print("\n6. Verify Final State...")
mod_unit = api.production.get_unit(test_module_sn, module_pn)
print(f"   Module unit: {mod_unit.serial_number}, phase={mod_unit.unit_phase}")
if mod_unit.sub_units:
    print(f"   Sub-units: {len(mod_unit.sub_units)}")
    for su in mod_unit.sub_units:
        print(f"     - {su.serial_number} / {su.part_number}")
else:
    print(f"   Sub-units: None/Empty")

print("\n" + "=" * 70)
print("DEBUG COMPLETE")
print("=" * 70)
