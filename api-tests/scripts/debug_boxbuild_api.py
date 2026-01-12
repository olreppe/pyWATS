"""Debug script to test box build and assembly API calls directly."""
import sys
import os
sys.path.insert(0, "src")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pywats import pyWATS
from pywats.domains.product.models import ProductRevisionRelation
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
print("DEBUG: Box Build API Testing")
print("=" * 70)

# 0. Fetch available unit phases from the server
print("\n0. Fetching unit phases from server...")
http_product = api.product_internal._repo_internal._http
base_url = api.product_internal._repo_internal._base_url
phases_response = http_product.get(
    "/api/internal/Mes/GetUnitPhases",
    headers={"Referer": base_url}
)
print(f"   HTTP Status: {phases_response.status_code}")
if phases_response.is_success and phases_response.data:
    phases = phases_response.data
    print(f"   Found {len(phases)} phases:")
    for phase in phases:
        print(f"     - ID={phase.get('UnitPhaseId'):3d} Code='{phase.get('Code', '')}' Name='{phase.get('Name', '')}'")
    # Store Finalized phase ID for later
    finalized_phase = next((p for p in phases if p.get('Name') == 'Finalized' or p.get('Code') == 'Finalized'), None)
    if finalized_phase:
        FINALIZED_PHASE_ID = finalized_phase.get('UnitPhaseId')
        print(f"   => Finalized phase ID: {FINALIZED_PHASE_ID}")
    else:
        print("   [WARN] Could not find 'Finalized' phase!")
        FINALIZED_PHASE_ID = 16  # Default fallback
else:
    print(f"   [ERROR] Could not fetch phases: {phases_response.data}")
    FINALIZED_PHASE_ID = 16  # Default fallback

# 1. Check if products exist
print("\n1. Checking products...")
module = api.product.get_product(module_pn)
sub = api.product.get_product(sub_pn)
print(f"   Module: {module.part_number if module else 'NOT FOUND'}")
print(f"   Sub-part: {sub.part_number if sub else 'NOT FOUND'}")

# 2. Check revisions
print("\n2. Checking revisions...")
module_rev_obj = api.product.get_revision(module_pn, module_rev)
sub_rev_obj = api.product.get_revision(sub_pn, sub_rev)
print(f"   Module rev {module_rev}: {module_rev_obj.product_revision_id if module_rev_obj else 'NOT FOUND'}")
print(f"   Sub-part rev {sub_rev}: {sub_rev_obj.product_revision_id if sub_rev_obj else 'NOT FOUND'}")

# 3. Test create_revision_relation directly with RAW HTTP
print("\n3. Testing create_revision_relation API (RAW HTTP)...")
if module_rev_obj and sub_rev_obj:
    print(f"   Parent revision ID: {module_rev_obj.product_revision_id}")
    print(f"   Child revision ID: {sub_rev_obj.product_revision_id}")
    
    # First check if relation already exists
    print("\n   Checking if relation already exists...")
    try:
        existing = api.product_internal.get_box_build_subunits(module_pn, module_rev)
        existing_match = [su for su in existing if su.child_part_number == sub_pn]
        if existing_match:
            print(f"   [SKIP] Relation already exists: {existing_match[0].relation_id}")
        else:
            # Access the HTTP client directly
            http = api.product_internal._repo_internal._http
            base_url = api.product_internal._repo_internal._base_url
            
            # API expects PascalCase field names:
            # - ParentProductRevisionId: Parent revision
            # - ProductRevisionId: Child revision (NOT "childProductRevisionId")
            data = {
                "ParentProductRevisionId": str(module_rev_obj.product_revision_id),
                "ProductRevisionId": str(sub_rev_obj.product_revision_id),
                "Quantity": 1,
            }
            
            print(f"\n   POST /api/internal/Product/PostProductRevisionRelation")
            print(f"   Headers: Referer={base_url}")
            print(f"   Data: {data}")
            
            response = http.post(
                "/api/internal/Product/PostProductRevisionRelation",
                data=data,
                headers={"Referer": base_url}
            )
            print(f"\n   HTTP Status: {response.status_code}")
            print(f"   Is Success: {response.is_success}")
            print(f"   Response Data: {response.data}")
            if hasattr(response, 'error'):
                print(f"   Error: {response.error}")
    except Exception as e:
        print(f"   [ERROR] {e}")

# 4. Check existing relations
print("\n4. Checking existing box build relations...")
try:
    subunits = api.product_internal.get_box_build_subunits(module_pn, module_rev)
    print(f"   Found {len(subunits)} subunit(s):")
    for su in subunits:
        print(f"     - {su.child_part_number} rev {su.child_revision} (ID: {su.relation_id})")
except Exception as e:
    print(f"   [ERROR] {e}")

# 5. Test add_child_unit API with RAW HTTP
print("\n5. Testing add_child_unit API (RAW HTTP)...")
# First get or create test units
test_module_sn = "DEBUG-MODULE-002"
test_sub_sn = "DEBUG-PSU-002"

print(f"   Creating/getting test units...")
try:
    # Try to get existing
    mod_unit = api.production.get_unit(test_module_sn, module_pn)
    print(f"   Module unit exists: {mod_unit.serial_number}, phase={mod_unit.unit_phase}")
except:
    # Create new
    mod_unit = Unit(serial_number=test_module_sn, part_number=module_pn, revision=module_rev)
    api.production.create_units([mod_unit])
    print(f"   Module unit created: {test_module_sn}")

try:
    sub_unit = api.production.get_unit(test_sub_sn, sub_pn)
    print(f"   Sub-part unit exists: {sub_unit.serial_number}, phase={sub_unit.unit_phase}")
except:
    sub_unit = Unit(serial_number=test_sub_sn, part_number=sub_pn, revision=sub_rev)
    api.production.create_units([sub_unit])
    print(f"   Sub-part unit created: {test_sub_sn}")

# CRITICAL: Child unit MUST be in "Finalized" phase for add_child_unit to work!
print(f"\n   Setting sub-part phase to 'Finalized' (phase={FINALIZED_PHASE_ID})...")
try:
    # Use the integer phase ID from the fetched phases
    http = api.production._repository._http_client
    params = {
        "serialNumber": test_sub_sn,
        "partNumber": sub_pn,
        "phase": FINALIZED_PHASE_ID,  # Integer phase ID
        "comment": "Finalized for assembly"
    }
    response = http.put("/api/Production/SetUnitPhase", params=params)
    print(f"   HTTP Status: {response.status_code}, Success: {response.is_success}")
    if response.is_success:
        print(f"   [OK] Sub-part phase set to 'Finalized' ({FINALIZED_PHASE_ID})")
    else:
        print(f"   [ERROR] Response: {response.data}")
except Exception as e:
    print(f"   [ERROR] Could not set phase: {e}")

# Verify the phase was set
sub_unit = api.production.get_unit(test_sub_sn, sub_pn)
print(f"   Sub-part phase after update: {sub_unit.unit_phase}")

# Try add_child_unit with PUBLIC API (correct parameter names)
print(f"\n   Calling POST /api/Production/AddChildUnit (PUBLIC API)...")
print(f"   Parent: {test_module_sn} / {module_pn}")
print(f"   Child:  {test_sub_sn} / {sub_pn}")

# PUBLIC API uses: parentSerialNumber, parentPartNumber, childSerialNumber, childPartNumber
# checkPartNumber and checkRevision can be empty to use box build validation
params = {
    "parentSerialNumber": test_module_sn,
    "parentPartNumber": module_pn,
    "childSerialNumber": test_sub_sn,
    "childPartNumber": sub_pn,
    "checkPartNumber": "",   # Use box build for validation
    "checkRevision": "",     # Use box build for validation
}
response = http.post("/api/Production/AddChildUnit", params=params)
print(f"   HTTP Status: {response.status_code}, Success: {response.is_success}")
print(f"   Response Data: {response.data}")

if not response.is_success:
    # Also try internal API as fallback
    print(f"\n   Trying INTERNAL API: POST /api/internal/Production/AddChildUnit...")
    internal_params = {
        "serialNumber": test_module_sn,  # Parent serial
        "partNumber": module_pn,          # Parent part
        "childSerialNumber": test_sub_sn,
        "childPartNumber": sub_pn,
        "checkPartNumber": sub_pn,
        "checkRevision": sub_rev,
        "cultureCode": "en-US",
        "checkPhase": "true",
    }
    headers = {"Referer": base_url}
    response = http.post("/api/internal/Production/AddChildUnit", params=internal_params, headers=headers)
    print(f"   HTTP Status: {response.status_code}, Success: {response.is_success}")
    print(f"   Response Data: {response.data}")

# 6. Check unit sub_units
print("\n6. Checking unit sub_units from server...")
mod_unit = api.production.get_unit(test_module_sn, module_pn)
if mod_unit:
    print(f"   Module unit: {mod_unit.serial_number}")
    if mod_unit.sub_units:
        print(f"   Sub-units: {len(mod_unit.sub_units)}")
        for su in mod_unit.sub_units:
            print(f"     - {su.serial_number} / {su.part_number}")
    else:
        print(f"   Sub-units: None/Empty")
else:
    print(f"   [FAILED] Could not get module unit")

print("\n" + "=" * 70)
print("DEBUG COMPLETE")
print("=" * 70)
