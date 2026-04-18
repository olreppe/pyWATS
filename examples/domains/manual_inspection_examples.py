"""
Manual Inspection Examples - Definitions, Relations, and Sequences

This example demonstrates how to work with manual inspections in pyWATS.

DOMAIN KNOWLEDGE: Manual Inspection
=====================================

Manual Inspections (MI) in WATS allow you to define structured inspection
sequences that operators follow during manufacturing. Unlike automated tests,
these are human-driven steps (visual inspection, measurement entry, pass/fail
checks) executed through an operator interface.

KEY CONCEPTS:
=============

1. TEST SEQUENCE DEFINITION
   - The blueprint for a manual inspection
   - Defines name, description, fail behaviour
   - Example: "PCB Visual Inspection", "Final Assembly Check"
   - Properties: IsGlobal, OnFailGotoCleanup, OnFailRequireRepair

2. TEST SEQUENCE RELATION
   - Links a definition to a product/process entity
   - EntitySchema: "Product", "Process", etc.
   - EntityName: part number or process name
   - Example: Definition "Board Check" → Product "CTRL-1000"

3. TEST SEQUENCE INSTANCE
   - A single execution of an inspection for a specific unit
   - Tracks the unit (serial number, part number) and timestamps
   - Created automatically when an operator starts an inspection

4. MI SEQUENCE
   - An available sequence shown in the operator interface

WORKFLOW:
=========

1. Create a definition (what to inspect)
2. Add relations to products/processes (where to apply it)
3. Operators execute instances against specific units (runtime)
4. Query instance data for reporting/traceability
"""

from pywats import pyWATS
import os


def example_1_list_definitions(api: pyWATS):
    """
    List all manual inspection definitions.

    Shows every MI definition configured in WATS, with key properties.
    """
    print("=" * 60)
    print("EXAMPLE 1: List Manual Inspection Definitions")
    print("=" * 60)

    definitions = api.manual_inspection.list_definitions()

    if not definitions:
        print("No MI definitions found.")
        print("Create one via the WATS web app or example_2 below.")
        return

    print(f"Found {len(definitions)} definition(s):\n")
    for defn in definitions:
        print(f"  Name: {defn.name}")
        print(f"  ID:   {defn.test_sequence_definition_id}")
        if defn.description:
            print(f"  Desc: {defn.description}")
        print(f"  Global: {defn.is_global}")
        print(f"  Status: {defn.status}")
        print()

    print("=" * 60)


def example_2_create_definition(api: pyWATS):
    """
    Create a new manual inspection definition.

    Defines a visual inspection for a PCB assembly with fail-to-cleanup
    behaviour enabled.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Create MI Definition")
    print("=" * 60)

    defn = api.manual_inspection.create_definition(
        name="PCB Visual Inspection",
        description="Visual inspection of PCB solder joints and component placement",
        is_global=False,
        on_fail_goto_cleanup=True,
        on_fail_require_submit=True,
    )

    if defn is None:
        print("Failed to create definition.")
        return None

    print(f"Created definition: {defn.name}")
    print(f"  ID: {defn.test_sequence_definition_id}")
    print(f"  OnFailGotoCleanup: {defn.on_fail_goto_cleanup}")
    print(f"  OnFailRequireSubmit: {defn.on_fail_require_submit}")

    print("=" * 60)
    return defn.test_sequence_definition_id


def example_3_relations(api: pyWATS, definition_id: str):
    """
    Manage relations between a definition and products.

    Links the definition to specific products so the inspection
    appears when operators test those products.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Manage Relations")
    print("=" * 60)

    # Create a relation to a product
    relation = api.manual_inspection.create_relation(
        definition_id=definition_id,
        entity_schema="Product",
        entity_name="CTRL-1000",
        entity_value="PartNumber",
    )

    if relation:
        print(f"Created relation:")
        print(f"  Schema: {relation.entity_schema}")
        print(f"  Name:   {relation.entity_name}")
        print(f"  Value:  {relation.entity_value}")

    # List all relations for this definition
    relations = api.manual_inspection.list_relations(definition_id)
    print(f"\nRelations for definition: {len(relations)}")
    for rel in relations:
        print(f"  {rel.entity_schema} / {rel.entity_name}")

    # Check for conflicts
    conflicts = api.manual_inspection.get_relation_conflicts(definition_id)
    if conflicts:
        print(f"\n⚠ {len(conflicts)} conflict(s) found:")
        for c in conflicts:
            print(f"  {c.entity_schema}/{c.entity_name}: {c.message}")
    else:
        print("\nNo relation conflicts.")

    print("=" * 60)


def example_4_sequences(api: pyWATS):
    """
    List available MI sequences.

    Sequences represent the inspection workflows available in the
    operator interface.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: MI Sequences")
    print("=" * 60)

    sequences = api.manual_inspection.list_sequences()

    if not sequences:
        print("No MI sequences available.")
        return

    print(f"Available sequences: {len(sequences)}\n")
    for seq in sequences:
        print(f"  {seq.name}")
        if seq.description:
            print(f"    {seq.description}")

    print("=" * 60)


def example_5_copy_definition(api: pyWATS, definition_id: str):
    """
    Copy an existing definition to create a variant.

    Useful when creating similar inspections for related products.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Copy Definition")
    print("=" * 60)

    copy = api.manual_inspection.copy_inspection(definition_id)

    if copy:
        print(f"Copied definition:")
        print(f"  Original ID: {definition_id}")
        print(f"  Copy ID:     {copy.test_sequence_definition_id}")
        print(f"  Name:        {copy.name}")
    else:
        print("Copy failed.")

    print("=" * 60)


def example_6_lifecycle_workflow(api: pyWATS):
    """
    Complete lifecycle: create → pending → release.

    Demonstrates the full inspection lifecycle from creation
    through release for production use.

    LIFECYCLE STATES:
    =================
    - Draft (0):    Editable. Create/modify steps and relations.
    - Pending (1):  Test mode. Operators can validate the sequence.
    - Released (2): Production. Immutable, active for operators.
    - Revoked (3):  Retired. Superseded by newer version.

    TRANSITIONS:
    ============
    Draft <--> Pending --> Released
                              |
                  [auto-revokes previous version]
                              |
                          Revoked
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Full Lifecycle Workflow")
    print("=" * 60)

    # 1. Create a new inspection (starts as Draft)
    inspection = api.manual_inspection.create_inspection(
        name="Thermal Test Inspection",
        description="Temperature verification for PCB assembly",
        on_fail_goto_cleanup=True,
        on_fail_require_repair=1,  # Optional repair
    )

    if inspection is None:
        print("Failed to create inspection.")
        return

    defn_id = str(inspection.test_sequence_definition_id)
    print(f"1. Created inspection: {inspection.name}")
    print(f"   ID: {defn_id}")
    print(f"   Status: Draft ({inspection.status})")

    # 2. Add a product relation
    relation = api.manual_inspection.create_relation(
        definition_id=defn_id,
        entity_schema="product",
        entity_name="product",
        entity_key="partnumber",
        entity_value="THERMAL-%",  # Wildcard for all thermal products
    )
    if relation:
        print(f"2. Added relation: {relation.entity_value}")

    # 3. Move to Pending for testing
    pending = api.manual_inspection.move_to_pending(defn_id)
    if pending:
        print(f"3. Moved to Pending (status={pending.status})")
        print("   → Operators can now test the inspection")

    # 4. Release for production
    released = api.manual_inspection.release_inspection(defn_id)
    if released:
        print(f"4. Released! (status={released.status})")
        print("   → Inspection is now active in production")
        print(f"   → Version: {released.version}")

    print("=" * 60)
    return defn_id


def example_7_modify_released_inspection(api: pyWATS, released_id: str):
    """
    Modify a released inspection by copying and editing.

    Released inspections are immutable. To make changes:
    1. Copy the released inspection (creates new Draft version)
    2. Modify the copy
    3. Release the new version (auto-revokes the old one)
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Modify Released Inspection")
    print("=" * 60)

    # 1. Copy the released inspection
    new_version = api.manual_inspection.copy_inspection(released_id)

    if new_version is None:
        print("Failed to copy inspection.")
        return

    new_id = str(new_version.test_sequence_definition_id)
    print(f"1. Created new version:")
    print(f"   Original ID: {released_id}")
    print(f"   New ID:      {new_id}")
    print(f"   Version:     {new_version.version}")
    print(f"   Status:      Draft ({new_version.status})")

    # 2. Modify the copy
    updated = api.manual_inspection.update_definition(
        new_id,
        Description="Updated: Added humidity check step",
    )
    if updated:
        print(f"2. Modified description")

    # 3. Release the new version
    released = api.manual_inspection.release_inspection(new_id)
    if released:
        print(f"3. Released new version!")
        print(f"   → Old version automatically revoked")

    print("=" * 60)


def example_8_check_inspection_status(api: pyWATS, definition_id: str):
    """
    Check and display the current status of an inspection.

    Uses the DefinitionStatus enum for clear status handling.
    """
    from pywats.domains.manual_inspection import DefinitionStatus

    print("\n" + "=" * 60)
    print("EXAMPLE 8: Check Inspection Status")
    print("=" * 60)

    inspection = api.manual_inspection.get_inspection(definition_id)

    if inspection is None:
        print(f"Inspection not found: {definition_id}")
        return

    print(f"Inspection: {inspection.name}")
    print(f"Version:    {inspection.version}")

    # Use enum for clear status handling
    if inspection.status == DefinitionStatus.DRAFT:
        print("Status:     DRAFT (editable)")
        print("Actions:    Can modify, move to Pending")
    elif inspection.status == DefinitionStatus.PENDING:
        print("Status:     PENDING (testing)")
        print("Actions:    Move to Draft or Release")
    elif inspection.status == DefinitionStatus.RELEASED:
        print("Status:     RELEASED (production)")
        print("Actions:    Copy to create new version")
    elif inspection.status == DefinitionStatus.REVOKED:
        print("Status:     REVOKED (superseded)")
        print("Actions:    Read-only, archived")

    print("=" * 60)


def main():
    """Run all manual inspection examples."""
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")

    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)

    print("=" * 60)
    print("MANUAL INSPECTION DOMAIN EXAMPLES")
    print("=" * 60)

    example_1_list_definitions(api)

    defn_id = example_2_create_definition(api)

    if defn_id:
        example_3_relations(api, defn_id)
        example_5_copy_definition(api, defn_id)
        example_8_check_inspection_status(api, defn_id)

    example_4_sequences(api)

    # Lifecycle examples (create new inspections)
    released_id = example_6_lifecycle_workflow(api)
    if released_id:
        example_7_modify_released_inspection(api, released_id)

    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
