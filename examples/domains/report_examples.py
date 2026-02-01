"""
Report Examples - UUT and UUR Test Reports

This example demonstrates how to work with test reports in pyWATS.

DOMAIN KNOWLEDGE: UUT vs UUR Reports
=====================================

1. UUT REPORT (Unit Under Test)
   - Records test results for a PRODUCTION UNIT (with serial number)
   - Example: Testing serial number "SN-12345" of product "Widget-100"
   - Use case: Final product testing, assembly verification
   - Links to: Production domain (units with serial numbers)

2. UUR REPORT (Unit Under Rework)
   - Records test results for REWORK/REPAIR operations
   - Example: Re-testing repaired unit "SN-12345" after board replacement
   - Use case: Repair validation, failure analysis, re-test after modification
   - Links to: UUT reports (tracks rework history)

STEP TYPES:
===========

Core step types for test sequences:

1. NumericLimitTest
   - Measures a value against min/max limits
   - Example: Voltage = 5.02V (min: 4.9, max: 5.1) → PASS
   - Result: Status (Pass/Fail) + measured value

2. MultipleNumericLimitTest
   - Multiple measurements in one step
   - Example: LED RGB test (R=255, G=128, B=64) with individual limits
   - Result: Overall status + array of measurements

3. PassFailTest
   - Boolean pass/fail decision
   - Example: "Visual Inspection" → PASS
   - Result: Status only (no measurement)

4. StringValueTest
   - Records string data (serial numbers, firmware versions)
   - Example: "Firmware Version" → "v2.4.1"
   - Result: String value + optional limits

5. MessageLog
   - Informational message, no pass/fail
   - Example: "Starting test sequence..."
   - Result: Message only

COMPLETE WORKFLOW:
==================
1. Create a production unit (UUT) or reference existing unit (UUR)
2. Start report (UUT or UUR mode)
3. Add test steps (NumericLimit, PassFail, etc.)
4. Set overall result (Pass/Fail)
5. End report
6. Query reports and results
"""

from pywats import pyWATS
from pywats.domains.report.enums import UUTStepType
from pywats.domains.report import (
    UUTStepNumericLimitUpdate,
    UUTStepMultipleNumericLimitUpdate,
    UUTStepPassFailUpdate,
    UUTStepStringValueUpdate,
    UUTStepMessageLogUpdate,
    NumericMeasurement,
)
from pywats.domains.report.report_models.common_types import StepStatus
from datetime import datetime
import os


def example_1_create_simple_uut_report(api: pyWATS):
    """
    Step 1: Create a basic UUT report with numeric and pass/fail tests.
    
    This is the most common scenario: testing a production unit with serial number.
    """
    print("=" * 60)
    print("EXAMPLE 1: Simple UUT Report (Pass)")
    print("=" * 60)
    
    # First, ensure we have a product and unit
    # (In practice, these would already exist from production)
    product_name = "WIDGET-100"
    revision = "Rev A"
    serial_number = f"SN-DEMO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Get or create product
    product = api.product.get_product_by_name(product_name)
    if not product:
        product = api.product.create_product(
            name=product_name,
            description="Demo widget for report examples"
        )
        api.product.create_product_revision(
            product_id=product.id,
            name=revision,
            description="First revision"
        )
    
    # Create production unit
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="FINAL-TEST"
    )
    
    print(f"Created unit: {serial_number}")
    print(f"Unit ID: {unit.id}")
    
    # Start UUT report
    report = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="FINAL-TEST",
        serial_number=serial_number
    )
    
    print(f"Started UUT report: {report.id}")
    
    # Add test steps
    # Step 1: Voltage measurement (NumericLimitTest)
    step1 = api.report.add_uut_step(
        report_id=report.id,
        step_name="5V Rail Voltage",
        step_type=UUTStepType.NumericLimitTest,
        step_data=UUTStepNumericLimitUpdate(
            measured_value=5.02,
            low_limit=4.9,
            high_limit=5.1,
            units="V",
            status=StepStatus.Passed
        )
    )
    print(f"  Step 1: {step1.name} = {step1.measured_value}V → {step1.status}")
    
    # Step 2: Current measurement (NumericLimitTest)
    step2 = api.report.add_uut_step(
        report_id=report.id,
        step_name="Load Current",
        step_type=UUTStepType.NumericLimitTest,
        step_data=UUTStepNumericLimitUpdate(
            measured_value=1.25,
            low_limit=1.0,
            high_limit=2.0,
            units="A",
            status=StepStatus.Passed
        )
    )
    print(f"  Step 2: {step2.name} = {step2.measured_value}A → {step2.status}")
    
    # Step 3: Visual inspection (PassFailTest)
    step3 = api.report.add_uut_step(
        report_id=report.id,
        step_name="Visual Inspection",
        step_type=UUTStepType.PassFailTest,
        step_data=UUTStepPassFailUpdate(
            status=StepStatus.Passed
        )
    )
    print(f"  Step 3: {step3.name} → {step3.status}")
    
    # Step 4: Firmware version (StringValueTest)
    step4 = api.report.add_uut_step(
        report_id=report.id,
        step_name="Firmware Version",
        step_type=UUTStepType.StringValueTest,
        step_data=UUTStepStringValueUpdate(
            string_value="v2.4.1",
            status=StepStatus.Passed
        )
    )
    print(f"  Step 4: {step4.name} = {step4.string_value} → {step4.status}")
    
    # Set overall result and end report
    api.report.set_uut_result(
        report_id=report.id,
        result=True  # True = Pass, False = Fail
    )
    
    api.report.end_uut_report(report_id=report.id)
    
    print(f"\nReport completed: PASSED")
    print(f"Report ID: {report.id}")
    print("=" * 60)
    
    return report.id, unit.id


def example_2_create_failing_uut_report(api: pyWATS):
    """
    Step 2: Create a UUT report with a failing test.
    
    Demonstrates how to handle failures and record failure details.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Failing UUT Report")
    print("=" * 60)
    
    product_name = "WIDGET-100"
    revision = "Rev A"
    serial_number = f"SN-FAIL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create unit
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="FINAL-TEST"
    )
    
    # Start report
    report = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="FINAL-TEST",
        serial_number=serial_number
    )
    
    print(f"Testing unit: {serial_number}")
    
    # Add passing steps
    api.report.add_uut_step(
        report_id=report.id,
        step_name="5V Rail Voltage",
        step_type=UUTStepType.NumericLimitTest,
        step_data=UUTStepNumericLimitUpdate(
            measured_value=5.01,
            low_limit=4.9,
            high_limit=5.1,
            units="V",
            status=StepStatus.Passed
        )
    )
    print("  ✓ 5V Rail: PASS")
    
    # Add FAILING step - voltage out of spec
    failing_step = api.report.add_uut_step(
        report_id=report.id,
        step_name="3.3V Rail Voltage",
        step_type=UUTStepType.NumericLimitTest,
        step_data=UUTStepNumericLimitUpdate(
            measured_value=3.65,  # Too high!
            low_limit=3.2,
            high_limit=3.4,
            units="V",
            status=StepStatus.Failed
        )
    )
    print(f"  ✗ 3.3V Rail: FAIL ({failing_step.measured_value}V, limit: {failing_step.high_limit}V)")
    
    # Continue with remaining tests
    api.report.add_uut_step(
        report_id=report.id,
        step_name="Visual Inspection",
        step_type=UUTStepType.PassFailTest,
        step_data=UUTStepPassFailUpdate(status=StepStatus.Passed)
    )
    print("  ✓ Visual: PASS")
    
    # Set overall result to FAIL
    api.report.set_uut_result(
        report_id=report.id,
        result=False  # False = Fail
    )
    
    api.report.end_uut_report(report_id=report.id)
    
    print(f"\nReport completed: FAILED")
    print(f"Failure: 3.3V rail out of specification")
    print("=" * 60)
    
    return report.id, unit.id


def example_3_multiple_numeric_measurements(api: pyWATS):
    """
    Step 3: Use MultipleNumericLimitTest for array measurements.
    
    Example: Testing RGB LED with three separate color channels.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Multiple Numeric Measurements (RGB LED)")
    print("=" * 60)
    
    product_name = "LED-RGB-500"
    revision = "Rev A"
    serial_number = f"LED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Create product if needed
    product = api.product.get_product_by_name(product_name)
    if not product:
        product = api.product.create_product(
            name=product_name,
            description="RGB LED module"
        )
        api.product.create_product_revision(
            product_id=product.id,
            name=revision
        )
    
    # Create unit and start report
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="LED-TEST"
    )
    
    report = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="LED-TEST",
        serial_number=serial_number
    )
    
    print(f"Testing RGB LED: {serial_number}")
    
    # MultipleNumericLimitTest - measure all three colors
    rgb_step = api.report.add_uut_step(
        report_id=report.id,
        step_name="RGB Color Test",
        step_type=UUTStepType.MultipleNumericLimitTest,
        step_data=UUTStepMultipleNumericLimitUpdate(
            measurements=[
                NumericMeasurement(
                    name="Red Channel",
                    value=253.5,
                    low_limit=245.0,
                    high_limit=260.0,
                    units="intensity",
                    status=StepStatus.Passed
                ),
                NumericMeasurement(
                    name="Green Channel",
                    value=127.8,
                    low_limit=120.0,
                    high_limit=135.0,
                    units="intensity",
                    status=StepStatus.Passed
                ),
                NumericMeasurement(
                    name="Blue Channel",
                    value=63.2,
                    low_limit=60.0,
                    high_limit=70.0,
                    units="intensity",
                    status=StepStatus.Passed
                )
            ],
            status=StepStatus.Passed  # Overall status
        )
    )
    
    print(f"  RGB Test Results:")
    for m in rgb_step.measurements:
        print(f"    {m.name}: {m.value} {m.units} → {m.status}")
    print(f"  Overall: {rgb_step.status}")
    
    # Complete report
    api.report.set_uut_result(report_id=report.id, result=True)
    api.report.end_uut_report(report_id=report.id)
    
    print("\nReport completed: PASSED")
    print("=" * 60)
    
    return report.id


def example_4_message_logs(api: pyWATS):
    """
    Step 4: Use MessageLog steps for informational messages.
    
    These don't affect pass/fail but provide context.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Message Logs (Informational)")
    print("=" * 60)
    
    product_name = "WIDGET-100"
    revision = "Rev A"
    serial_number = f"SN-LOG-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="FINAL-TEST"
    )
    
    report = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="FINAL-TEST",
        serial_number=serial_number
    )
    
    print(f"Testing: {serial_number}")
    
    # Log messages throughout test
    api.report.add_uut_step(
        report_id=report.id,
        step_name="Test Start",
        step_type=UUTStepType.MessageLog,
        step_data=UUTStepMessageLogUpdate(
            message="Starting functional test sequence"
        )
    )
    print("  → Test sequence started")
    
    # Actual test
    api.report.add_uut_step(
        report_id=report.id,
        step_name="Power Supply Test",
        step_type=UUTStepType.NumericLimitTest,
        step_data=UUTStepNumericLimitUpdate(
            measured_value=12.01,
            low_limit=11.8,
            high_limit=12.2,
            units="V",
            status=StepStatus.Passed
        )
    )
    print("  ✓ Power test: PASS")
    
    # Log calibration info
    api.report.add_uut_step(
        report_id=report.id,
        step_name="Calibration Info",
        step_type=UUTStepType.MessageLog,
        step_data=UUTStepMessageLogUpdate(
            message="Using calibration standard CAL-12345, expires 2026-12-31"
        )
    )
    print("  → Calibration recorded")
    
    api.report.set_uut_result(report_id=report.id, result=True)
    api.report.end_uut_report(report_id=report.id)
    
    print("\nReport completed with message logs")
    print("=" * 60)
    
    return report.id


def example_5_uur_report_rework(api: pyWATS):
    """
    Step 5: Create a UUR (Unit Under Rework) report.
    
    This demonstrates re-testing after repair/rework.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: UUR Report (Rework/Repair)")
    print("=" * 60)
    
    # First, create a failing UUT report
    print("\n1. Initial test (FAIL):")
    failing_report_id, unit_id = example_2_create_failing_uut_report(api)
    
    # Now create a UUR report for the rework
    print("\n2. After repair, re-test with UUR:")
    
    unit = api.production.get_unit_by_id(unit_id)
    
    # Start UUR report (referencing the original UUT report)
    uur_report = api.report.start_uur_report(
        unit_id=unit_id,
        operation_type_name="REWORK",
        serial_number=unit.serial_number,
        uut_report_id=failing_report_id  # Link to original failure
    )
    
    print(f"Started UUR report: {uur_report.id}")
    print(f"Linked to original UUT report: {failing_report_id}")
    
    # Re-test the previously failing component
    api.report.add_uur_step(
        report_id=uur_report.id,
        step_name="3.3V Rail Voltage (Post-Repair)",
        step_type=UUTStepType.NumericLimitTest,
        step_data=UUTStepNumericLimitUpdate(
            measured_value=3.32,  # Now within spec!
            low_limit=3.2,
            high_limit=3.4,
            units="V",
            status=StepStatus.Passed
        )
    )
    print("  ✓ 3.3V Rail (after repair): PASS (3.32V)")
    
    # Verify other tests still pass
    api.report.add_uur_step(
        report_id=uur_report.id,
        step_name="5V Rail Voltage",
        step_type=UUTStepType.NumericLimitTest,
        step_data=UUTStepNumericLimitUpdate(
            measured_value=5.00,
            low_limit=4.9,
            high_limit=5.1,
            units="V",
            status=StepStatus.Passed
        )
    )
    print("  ✓ 5V Rail: PASS")
    
    # Complete UUR report as PASSED
    api.report.set_uur_result(
        report_id=uur_report.id,
        result=True
    )
    
    api.report.end_uur_report(report_id=uur_report.id)
    
    print("\nUUR report completed: PASSED")
    print("Unit successfully repaired and re-tested")
    print("=" * 60)
    
    return uur_report.id


def example_6_query_reports(api: pyWATS):
    """
    Step 6: Query reports and analyze results.
    
    Demonstrates how to retrieve and filter reports.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Query Reports")
    print("=" * 60)
    
    # Get recent UUT reports
    recent_reports = api.report.get_uut_reports(
        limit=10,
        include_steps=True  # Include all step details
    )
    
    print(f"\nFound {len(recent_reports)} recent UUT reports:")
    
    for report in recent_reports[:5]:  # Show first 5
        result_str = "PASS" if report.result else "FAIL"
        print(f"\n  Report {report.id}:")
        print(f"    Serial: {report.serial_number}")
        print(f"    Result: {result_str}")
        print(f"    Steps: {len(report.steps) if report.steps else 0}")
        
        # Show failing steps if any
        if report.steps:
            failing_steps = [s for s in report.steps if s.status == "Failed"]
            if failing_steps:
                print(f"    Failed steps:")
                for step in failing_steps:
                    print(f"      - {step.name}: {step.status}")
    
    print("\n" + "=" * 60)


def example_7_report_by_serial(api: pyWATS):
    """
    Step 7: Get all reports for a specific serial number.
    
    Useful for tracking test history of a unit through production and rework.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Report History by Serial Number")
    print("=" * 60)
    
    # Create a unit with multiple test cycles
    product_name = "WIDGET-100"
    revision = "Rev A"
    serial_number = f"SN-HISTORY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print(f"Creating test history for: {serial_number}\n")
    
    # Test 1: Initial test
    unit = api.production.start_production_unit(
        product_name=product_name,
        revision=revision,
        serial_number=serial_number,
        operation_type_name="INITIAL-TEST"
    )
    
    report1 = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="INITIAL-TEST",
        serial_number=serial_number
    )
    api.report.add_uut_step(
        report_id=report1.id,
        step_name="Quick Test",
        step_type=UUTStepType.PassFailTest,
        step_data=UUTStepPassFailUpdate(status=StepStatus.Passed)
    )
    api.report.set_uut_result(report_id=report1.id, result=True)
    api.report.end_uut_report(report_id=report1.id)
    print("1. Initial test: PASS")
    
    # Test 2: Final test
    report2 = api.report.start_uut_report(
        unit_id=unit.id,
        operation_type_name="FINAL-TEST",
        serial_number=serial_number
    )
    api.report.add_uut_step(
        report_id=report2.id,
        step_name="Full Test",
        step_type=UUTStepType.PassFailTest,
        step_data=UUTStepPassFailUpdate(status=StepStatus.Passed)
    )
    api.report.set_uut_result(report_id=report2.id, result=True)
    api.report.end_uut_report(report_id=report2.id)
    print("2. Final test: PASS")
    
    # Query all reports for this serial
    all_reports = api.report.get_reports_by_serial(serial_number)
    
    print(f"\nComplete test history for {serial_number}:")
    print(f"Total reports: {len(all_reports)}")
    
    for i, report in enumerate(all_reports, 1):
        result_str = "PASS" if report.result else "FAIL"
        print(f"  {i}. Operation: {report.operation_type_name}")
        print(f"     Result: {result_str}")
        print(f"     Report ID: {report.id}")
    
    print("\n" + "=" * 60)


def main():
    """Run all report examples."""
    # Connect to WATS API
    # Use environment variable or direct connection
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")
    
    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)
    
    print("=" * 60)
    print("REPORT DOMAIN EXAMPLES")
    print("Demonstrates UUT/UUR reports and all step types")
    print("=" * 60)
    
    # Run examples
    example_1_create_simple_uut_report(api)
    example_2_create_failing_uut_report(api)
    example_3_multiple_numeric_measurements(api)
    example_4_message_logs(api)
    example_5_uur_report_rework(api)
    example_6_query_reports(api)
    example_7_report_by_serial(api)
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
