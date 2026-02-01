"""
Production Examples - Units, Serial Numbers, and Production Phases

This example demonstrates how to work with production units in pyWATS.

DOMAIN KNOWLEDGE: Production Units vs Products
===============================================

Critical distinction:

1. PRODUCT (Design)
   - What you're building (the design/blueprint)
   - Example: "Widget-2000 Controller Rev A"
   - Lives in: Product domain
   - Created: Once during product development

2. PRODUCTION UNIT (Instance)
   - Specific physical instance being built
   - Example: Serial number "SN-12345" of Widget-2000 Rev A
   - Lives in: Production domain
   - Created: Every time you build one

Think of it as: Product = Class, Unit = Instance

UNIT LIFECYCLE:
===============

Production units move through manufacturing stages:

1. Start Production Unit
   - Creates unit record with serial number
   - Links to product + revision
   - Associates with operation type (e.g., "ASSEMBLY", "FINAL-TEST")
   - Status: In Progress

2. Testing Phase
   - Create UUT reports for the unit
   - Record pass/fail results
   - Track test data

3. Finalize Unit
   - Mark unit as complete
   - Status: Completed (if passed) or Failed

4. Rework (if needed)
   - Create UUR report
   - Track rework operations
   - Re-finalize

OPERATION TYPES:
================

Units are associated with operation types that define the manufacturing step:

- ASSEMBLY: Building the unit
- FINAL-TEST: Final verification before shipping
- BURN-IN: Extended stress testing
- CALIBRATION: Sensor/instrument calibration
- REWORK: Repair failed units
- INSPECTION: Visual/quality checks

COMPLETE WORKFLOW:
==================
1. Create/reference product and revision
2. Start production unit with serial number
3. Perform tests (create UUT reports)
4. Finalize unit (pass/fail)
5. Track unit through multiple operations
6. Query unit history and status
7. Handle rework if needed
"""

from pywats import pyWATS
from pywats.domains.production import Unit
from pywats.domains.report.enums import UUTStepType
from pywats.domains.report import UUTStepPassFailUpdate
from datetime import datetime
import os


def example_1_create_simple_unit(api: pyWATS):
    """
    Step 1: Create a basic production unit.
    
    This creates a unit record with serial number.
    """
    print("=" * 60)
    print("EXAMPLE 1: Simple Production Unit")
    print("=" * 60)
    
    # First, ensure product exists
    product_name = "WIDGET-2000"
    revision = "Rev A"
    
    product = api.product.get_product_by_name(product_name)
    if not product:
        product = api.product.create_product(
            name=product_name,
            description="Example widget for production tracking"
        )
        api.product.create_product_revision(
            product_id=product.id,
            name=revision
        )
    
    # Generate unique serial number
    serial_number = f"SN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Start production unit
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="ASSEMBLY"
    )
    
    print(f"Created production unit:")
    print(f"  Serial Number: {unit.serial_number}")
    print(f"  Unit ID: {unit.id}")
    print(f"  Product: {product_name} {revision}")
    print(f"  Operation: {unit.operation_type_name}")
    print(f"  Status: In Progress")
    
    print("\n" + "=" * 60)
    
    return unit.id, serial_number


def example_2_unit_through_operations(api: pyWATS):
    """
    Step 2: Track a unit through multiple manufacturing operations.
    
    Demonstrates: Assembly → Testing → Burn-in → Final Test
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Unit Through Manufacturing Operations")
    print("=" * 60)
    
    product_name = "CONTROLLER-500"
    revision = "Rev B"
    serial_number = f"CTRL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Ensure product exists
    product = api.product.get_product_by_name(product_name)
    if not product:
        product = api.product.create_product(name=product_name)
        api.product.create_product_revision(product_id=product.id, name=revision)
    
    print(f"Tracking unit: {serial_number}")
    print(f"Product: {product_name} {revision}\n")
    
    # Operation 1: Assembly
    print("1. ASSEMBLY:")
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="ASSEMBLY"
    )
    print(f"   Started assembly")
    print(f"   Unit ID: {unit.id}")
    
    # Finalize assembly
    api.production.finalize_unit(unit_id=unit.id, passed=True)
    print(f"   Assembly complete: PASS")
    
    # Operation 2: Initial Test
    print("\n2. INITIAL-TEST:")
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="INITIAL-TEST"
    )
    
    # Create test report
    report = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="INITIAL-TEST",
        serial_number=serial_number
    )
    api.report.add_uut_step(
        report_id=report.id,
        step_name="Power-On Test",
        step_type=UUTStepType.PassFailTest,
        step_data=UUTStepPassFailUpdate(status="Passed")
    )
    api.report.set_uut_result(report_id=report.id, result=True)
    api.report.end_uut_report(report_id=report.id)
    
    api.production.finalize_unit(unit_id=unit.id, passed=True)
    print(f"   Initial test complete: PASS")
    
    # Operation 3: Burn-in
    print("\n3. BURN-IN:")
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="BURN-IN"
    )
    print(f"   48-hour burn-in started...")
    
    api.production.finalize_unit(unit_id=unit.id, passed=True)
    print(f"   Burn-in complete: PASS")
    
    # Operation 4: Final Test
    print("\n4. FINAL-TEST:")
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="FINAL-TEST"
    )
    
    # Create final test report
    report = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="FINAL-TEST",
        serial_number=serial_number
    )
    api.report.add_uut_step(
        report_id=report.id,
        step_name="Full Functional Test",
        step_type=UUTStepType.PassFailTest,
        step_data=UUTStepPassFailUpdate(status="Passed")
    )
    api.report.set_uut_result(report_id=report.id, result=True)
    api.report.end_uut_report(report_id=report.id)
    
    api.production.finalize_unit(unit_id=unit.id, passed=True)
    print(f"   Final test complete: PASS")
    
    print(f"\n✓ Unit {serial_number} completed all operations")
    print("=" * 60)
    
    return serial_number


def example_3_batch_production(api: pyWATS):
    """
    Step 3: Create multiple units (batch production).
    
    Demonstrates creating a batch of units efficiently.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Batch Production")
    print("=" * 60)
    
    product_name = "SENSOR-100"
    revision = "Rev A"
    batch_size = 5
    
    # Ensure product exists
    product = api.product.get_product_by_name(product_name)
    if not product:
        product = api.product.create_product(name=product_name)
        api.product.create_product_revision(product_id=product.id, name=revision)
    
    print(f"Creating batch of {batch_size} units")
    print(f"Product: {product_name} {revision}\n")
    
    batch_serials = []
    
    for i in range(1, batch_size + 1):
        # Generate sequential serial numbers
        serial_number = f"BATCH-{datetime.now().strftime('%Y%m%d')}-{i:03d}"
        
        # Start unit
        unit = api.production.start_production_unit(
            product_name=product_name,
            revision=revision,
            serial_number=serial_number,
            operation_type_name="ASSEMBLY"
        )
        
        # Quick test
        report = api.report.start_uut_report(
            unit_id=unit.id,
            operation_type_name="ASSEMBLY",
            serial_number=serial_number
        )
        api.report.add_uut_step(
            report_id=report.id,
            step_name="Quick Check",
            step_type=UUTStepType.PassFailTest,
            step_data=UUTStepPassFailUpdate(status="Passed")
        )
        api.report.set_uut_result(report_id=report.id, result=True)
        api.report.end_uut_report(report_id=report.id)
        
        # Finalize
        api.production.finalize_unit(unit_id=unit.id, passed=True)
        
        batch_serials.append(serial_number)
        print(f"  [{i}/{batch_size}] {serial_number}: PASS")
    
    print(f"\n✓ Batch complete: {batch_size} units")
    print(f"  Serial range: {batch_serials[0]} to {batch_serials[-1]}")
    print("=" * 60)
    
    return batch_serials


def example_4_unit_with_failure(api: pyWATS):
    """
    Step 4: Handle a failing unit.
    
    Unit fails test and is marked for rework.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Unit Failure and Rework")
    print("=" * 60)
    
    product_name = "WIDGET-2000"
    revision = "Rev A"
    serial_number = f"FAIL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print(f"Testing unit: {serial_number}\n")
    
    # Start unit
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="FINAL-TEST"
    )
    
    # Create failing test
    report = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="FINAL-TEST",
        serial_number=serial_number
    )
    
    # Add failing step
    api.report.add_uut_step(
        report_id=report.id,
        step_name="Voltage Test",
        step_type=UUTStepType.PassFailTest,
        step_data=UUTStepPassFailUpdate(status="Failed")
    )
    
    api.report.set_uut_result(report_id=report.id, result=False)
    api.report.end_uut_report(report_id=report.id)
    
    # Finalize unit as FAILED
    api.production.finalize_unit(unit_id=unit.id, passed=False)
    
    print("✗ Unit FAILED final test")
    print("  Failure: Voltage test")
    print("  Action: Sent to rework")
    
    # Rework operation
    print("\n→ Rework:")
    rework_unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="REWORK"
    )
    
    # Create UUR report
    uur_report = api.report.start_uur_report(
        unit_id=rework_unit.id,
        operation_type_name="REWORK",
        serial_number=serial_number,
        uut_report_id=report.id  # Link to original failure
    )
    
    # Re-test after repair
    api.report.add_uur_step(
        report_id=uur_report.id,
        step_name="Voltage Test (Post-Repair)",
        step_type=UUTStepType.PassFailTest,
        step_data=UUTStepPassFailUpdate(status="Passed")
    )
    
    api.report.set_uur_result(report_id=uur_report.id, result=True)
    api.report.end_uur_report(report_id=uur_report.id)
    
    api.production.finalize_unit(unit_id=rework_unit.id, passed=True)
    
    print("  Repair completed")
    print("  Re-test: PASS")
    print(f"\n✓ Unit {serial_number} repaired and passed")
    print("=" * 60)
    
    return serial_number


def example_5_query_unit_history(api: pyWATS):
    """
    Step 5: Query complete history of a unit.
    
    Shows all operations and tests for a serial number.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Unit History Query")
    print("=" * 60)
    
    # Create a unit with full history
    product_name = "WIDGET-2000"
    revision = "Rev A"
    serial_number = f"HISTORY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print(f"Creating unit with full history: {serial_number}\n")
    
    # Track through multiple operations
    operations = ["ASSEMBLY", "INITIAL-TEST", "BURN-IN", "FINAL-TEST"]
    
    for op in operations:
        unit = api.production.start_production_unit(
            product_name=product_name,
            revision=revision,
            serial_number=serial_number,
            operation_type_name=op
        )
        
        # Create test report
        report = api.report.start_uut_report(
            unit_id=unit.id,
            operation_type_name=op,
            serial_number=serial_number
        )
        api.report.add_uut_step(
            report_id=report.id,
            step_name=f"{op} Check",
            step_type=UUTStepType.PassFailTest,
            step_data=UUTStepPassFailUpdate(status="Passed")
        )
        api.report.set_uut_result(report_id=report.id, result=True)
        api.report.end_uut_report(report_id=report.id)
        
        api.production.finalize_unit(unit_id=unit.id, passed=True)
        print(f"  {op}: PASS")
    
    # Query complete history
    print(f"\nQuerying history for {serial_number}:")
    
    # Get all units with this serial (across all operations)
    units = api.production.get_units_by_serial(serial_number)
    print(f"\nTotal operations: {len(units)}")
    
    for i, unit in enumerate(units, 1):
        print(f"  {i}. {unit.operation_type_name}")
        print(f"     Status: {'Passed' if unit.passed else 'Failed'}")
        print(f"     Unit ID: {unit.id}")
    
    # Get all reports
    reports = api.report.get_reports_by_serial(serial_number)
    print(f"\nTotal test reports: {len(reports)}")
    
    for i, report in enumerate(reports, 1):
        result = "PASS" if report.result else "FAIL"
        print(f"  {i}. {report.operation_type_name}: {result}")
    
    print("\n" + "=" * 60)


def example_6_unit_genealogy(api: pyWATS):
    """
    Step 6: Track unit genealogy (parent/child relationships).
    
    For box build, track which sub-assemblies went into main assembly.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Unit Genealogy (Box Build)")
    print("=" * 60)
    
    # This example shows the metadata tracking
    # Actual assembly uses box build template (see box_build_examples.py)
    
    print("Unit Genealogy Tracking:\n")
    
    # Main assembly
    main_serial = f"MAIN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"Main Assembly: {main_serial}")
    
    # Create sub-assemblies
    sub_assemblies = []
    for i in range(1, 4):
        sub_serial = f"SUB-{datetime.now().strftime('%Y%m%d%H%M%S')}-{i}"
        sub_assemblies.append(sub_serial)
        print(f"  Contains: {sub_serial}")
    
    print("\nGenealogy structure:")
    print(f"  {main_serial}")
    for sub in sub_assemblies:
        print(f"    └─ {sub}")
    
    print("\nNote: For full box build implementation,")
    print("      see examples/domains/box_build_examples.py")
    print("=" * 60)


def example_7_production_statistics(api: pyWATS):
    """
    Step 7: Query production statistics.
    
    Get counts, pass rates, etc.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Production Statistics")
    print("=" * 60)
    
    product_name = "WIDGET-2000"
    
    # Get all units for product
    all_units = api.production.get_units_by_product(product_name)
    
    print(f"\nProduction Statistics for {product_name}:")
    print(f"  Total units: {len(all_units)}")
    
    # Calculate pass/fail
    passed = [u for u in all_units if u.passed]
    failed = [u for u in all_units if not u.passed]
    
    print(f"  Passed: {len(passed)}")
    print(f"  Failed: {len(failed)}")
    
    if len(all_units) > 0:
        pass_rate = (len(passed) / len(all_units)) * 100
        print(f"  Pass Rate: {pass_rate:.1f}%")
    
    # Group by operation
    print(f"\nBy Operation Type:")
    operations = {}
    for unit in all_units:
        op = unit.operation_type_name
        if op not in operations:
            operations[op] = {"total": 0, "passed": 0}
        operations[op]["total"] += 1
        if unit.passed:
            operations[op]["passed"] += 1
    
    for op, stats in operations.items():
        rate = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        print(f"  {op}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")
    
    print("\n" + "=" * 60)


def main():
    """Run all production examples."""
    # Connect to WATS API
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")
    
    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)
    
    print("=" * 60)
    print("PRODUCTION DOMAIN EXAMPLES")
    print("Demonstrates units, serial numbers, and production tracking")
    print("=" * 60)
    
    # Run examples
    example_1_create_simple_unit(api)
    example_2_unit_through_operations(api)
    example_3_batch_production(api)
    example_4_unit_with_failure(api)
    example_5_query_unit_history(api)
    example_6_unit_genealogy(api)
    example_7_production_statistics(api)
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
