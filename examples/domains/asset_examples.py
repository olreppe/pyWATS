"""
Asset Examples - Equipment, Calibration, and Maintenance Tracking

This example demonstrates how to work with assets (equipment) in pyWATS.

DOMAIN KNOWLEDGE: Assets vs Production Units
=============================================

Understanding the distinction:

1. ASSET (Equipment/Tools)
   - Manufacturing equipment, test equipment, calibration standards
   - Example: Oscilloscope, Burn-in chamber, Calibration weight
   - Tracked for: Calibration status, maintenance, location
   - Lifecycle: Years (equipment lifespan)

2. PRODUCTION UNIT (Products)
   - Things being manufactured
   - Example: Widget-2000 with serial SN-12345
   - Tracked for: Test results, assembly, quality
   - Lifecycle: Days/weeks (production cycle)

Think of it as: Assets are tools you USE to build/test units

ASSET TYPES:
============

Common asset categories:

1. Test Equipment
   - Oscilloscopes, multimeters, spectrum analyzers
   - Requires: Regular calibration
   - Tracks: Calibration due dates, accuracy specs

2. Manufacturing Equipment
   - Pick-and-place machines, reflow ovens, presses
   - Requires: Preventive maintenance
   - Tracks: Maintenance schedules, downtime

3. Calibration Standards
   - Reference standards, calibration weights
   - Requires: Certification tracking
   - Tracks: Traceability to national standards

4. Tooling & Fixtures
   - Test fixtures, programming fixtures
   - Requires: Wear tracking
   - Tracks: Usage count, replacement schedules

CALIBRATION WORKFLOW:
=====================

1. Create asset record
2. Set calibration requirements (frequency, standards)
3. Perform calibration
4. Record calibration results
5. Schedule next calibration
6. Track calibration history
7. Alert on expiring calibrations

COMPLETE WORKFLOW:
==================
1. Register equipment as asset
2. Set calibration/maintenance schedule
3. Use asset in production (link to tests)
4. Perform periodic calibration
5. Record calibration certificates
6. Track maintenance history
7. Report on asset utilization and status
"""

from pywats import pyWATS
from pywats.domains.asset import Asset, CalibrationRecord
from datetime import datetime, timedelta
import os


def example_1_create_simple_asset(api: pyWATS):
    """
    Step 1: Register a basic asset (test equipment).
    
    Creates asset record with essential information.
    """
    print("=" * 60)
    print("EXAMPLE 1: Register Test Equipment")
    print("=" * 60)
    
    # Create a digital multimeter asset
    asset = api.asset.create_asset(
        asset_id="DMM-001",  # Unique identifier (asset tag)
        name="Fluke 87V Digital Multimeter",
        asset_type="Test Equipment",
        manufacturer="Fluke",
        model="87V",
        serial_number="12345678",
        location="Test Station 1"
    )
    
    print(f"Registered asset:")
    print(f"  Asset ID: {asset.asset_id}")
    print(f"  Name: {asset.name}")
    print(f"  Type: {asset.asset_type}")
    print(f"  Manufacturer: {asset.manufacturer}")
    print(f"  Model: {asset.model}")
    print(f"  Serial: {asset.serial_number}")
    print(f"  Location: {asset.location}")
    
    print("=" * 60)
    
    return asset.asset_id


def example_2_calibration_requirements(api: pyWATS):
    """
    Step 2: Set calibration requirements for equipment.
    
    Defines when and how equipment must be calibrated.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Calibration Requirements")
    print("=" * 60)
    
    # Create oscilloscope asset
    asset = api.asset.create_asset(
        asset_id="SCOPE-001",
        name="Tektronix MSO64 Oscilloscope",
        asset_type="Test Equipment",
        manufacturer="Tektronix",
        model="MSO64",
        serial_number="C012345"
    )
    
    print(f"Asset: {asset.name}")
    print(f"Asset ID: {asset.asset_id}\n")
    
    # Set calibration requirements
    print("Calibration Requirements:")
    print("  Frequency: Every 12 months")
    print("  Standard: NIST-traceable reference")
    print("  Parameters: Voltage, Frequency, Rise Time")
    print("  Tolerance: ±2% full scale")
    
    # Set next calibration due date
    calibration_due = datetime.now() + timedelta(days=365)
    
    api.asset.update_asset(
        asset_id=asset.asset_id,
        calibration_due_date=calibration_due,
        calibration_frequency_days=365
    )
    
    print(f"\nNext calibration due: {calibration_due.strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    return asset.asset_id


def example_3_perform_calibration(api: pyWATS):
    """
    Step 3: Record a calibration event.
    
    Documents calibration performed with results and certificate.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Perform Calibration")
    print("=" * 60)
    
    asset_id = "DMM-001"
    
    print(f"Performing calibration for {asset_id}\n")
    
    # Calibration details
    cal_date = datetime.now()
    cal_technician = "John Smith"
    cal_standard = "CAL-STD-001 (NIST-traceable)"
    
    print("Calibration Details:")
    print(f"  Date: {cal_date.strftime('%Y-%m-%d')}")
    print(f"  Technician: {cal_technician}")
    print(f"  Standard: {cal_standard}")
    print(f"  Certificate: CERT-2026-001")
    
    # Calibration results
    print("\nCalibration Results:")
    results = [
        {"parameter": "DC Voltage (10V)", "measured": "10.002V", "error": "+0.02%", "status": "PASS"},
        {"parameter": "AC Voltage (10V)", "measured": "9.998V", "error": "-0.02%", "status": "PASS"},
        {"parameter": "Resistance (1kΩ)", "measured": "1.001kΩ", "error": "+0.1%", "status": "PASS"},
        {"parameter": "Frequency (1kHz)", "measured": "1000.1Hz", "error": "+0.01%", "status": "PASS"}
    ]
    
    for result in results:
        print(f"  {result['parameter']}:")
        print(f"    Measured: {result['measured']} (Error: {result['error']})")
        print(f"    Status: {result['status']}")
    
    # Record calibration
    calibration = api.asset.create_calibration_record(
        asset_id=asset_id,
        calibration_date=cal_date,
        performed_by=cal_technician,
        calibration_standard=cal_standard,
        certificate_number="CERT-2026-001",
        results=results,
        passed=True
    )
    
    # Update next calibration due date
    next_due = cal_date + timedelta(days=365)
    api.asset.update_asset(
        asset_id=asset_id,
        last_calibration_date=cal_date,
        calibration_due_date=next_due
    )
    
    print(f"\n✓ Calibration recorded: PASSED")
    print(f"  Next calibration due: {next_due.strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    return calibration.id


def example_4_maintenance_tracking(api: pyWATS):
    """
    Step 4: Track maintenance events.
    
    Record preventive and corrective maintenance.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Maintenance Tracking")
    print("=" * 60)
    
    # Create manufacturing equipment
    asset = api.asset.create_asset(
        asset_id="OVEN-001",
        name="Reflow Oven",
        asset_type="Manufacturing Equipment",
        manufacturer="BTU International",
        model="Pyramax 100N",
        location="SMT Line 1"
    )
    
    print(f"Asset: {asset.name}")
    print(f"Location: {asset.location}\n")
    
    # Preventive maintenance
    print("Preventive Maintenance:")
    pm_date = datetime.now()
    
    pm_tasks = [
        "Clean heating elements",
        "Check temperature sensors",
        "Lubricate conveyor bearings",
        "Inspect heating zones",
        "Verify temperature profile accuracy"
    ]
    
    for task in pm_tasks:
        print(f"  ✓ {task}")
    
    # Record maintenance
    api.asset.create_maintenance_record(
        asset_id=asset.asset_id,
        maintenance_date=pm_date,
        maintenance_type="Preventive",
        performed_by="Maintenance Team",
        description="Quarterly preventive maintenance",
        tasks=pm_tasks,
        downtime_hours=2.5
    )
    
    print(f"\nMaintenance completed: {pm_date.strftime('%Y-%m-%d')}")
    print(f"Downtime: 2.5 hours")
    print(f"Next PM due: {(pm_date + timedelta(days=90)).strftime('%Y-%m-%d')}")
    
    # Corrective maintenance example
    print("\n" + "-" * 60)
    print("Corrective Maintenance (Repair):")
    
    repair_date = datetime.now() - timedelta(days=30)
    print(f"  Date: {repair_date.strftime('%Y-%m-%d')}")
    print(f"  Issue: Zone 3 heater failure")
    print(f"  Action: Replaced heating element")
    print(f"  Parts: Heating element P/N HE-Z3-001")
    print(f"  Downtime: 4 hours")
    
    api.asset.create_maintenance_record(
        asset_id=asset.asset_id,
        maintenance_date=repair_date,
        maintenance_type="Corrective",
        performed_by="Service Technician",
        description="Replaced failed Zone 3 heating element",
        parts_used=["HE-Z3-001"],
        downtime_hours=4.0
    )
    
    print("=" * 60)


def example_5_asset_utilization(api: pyWATS):
    """
    Step 5: Track asset usage in production.
    
    Link assets to test operations for utilization tracking.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Asset Utilization Tracking")
    print("=" * 60)
    
    # Create test fixture asset
    asset = api.asset.create_asset(
        asset_id="FIXTURE-001",
        name="Final Test Fixture",
        asset_type="Test Fixture",
        location="Test Station 3"
    )
    
    print(f"Asset: {asset.name}")
    print(f"Asset ID: {asset.asset_id}\n")
    
    print("Usage Tracking:")
    
    # Simulate usage over time
    total_cycles = 0
    
    # Example: Track fixture used for testing 10 units
    for i in range(1, 11):
        serial = f"SN-{datetime.now().strftime('%Y%m%d')}-{i:03d}"
        
        # In actual implementation, link asset to test report
        # api.report.add_asset_usage(
        #     report_id=report.id,
        #     asset_id=asset.asset_id
        # )
        
        total_cycles += 1
        
        if i <= 3:  # Show first few
            print(f"  Tested unit {serial} using {asset.asset_id}")
    
    print(f"  ... (7 more units)")
    print(f"\nTotal usage: {total_cycles} test cycles")
    print(f"Fixture rated for: 10,000 cycles")
    print(f"Remaining life: {10000 - total_cycles} cycles")
    
    # Update asset with usage count
    api.asset.update_asset(
        asset_id=asset.asset_id,
        usage_count=total_cycles
    )
    
    print("=" * 60)


def example_6_calibration_alerts(api: pyWATS):
    """
    Step 6: Check for expiring calibrations.
    
    Query assets needing calibration soon.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Calibration Alerts")
    print("=" * 60)
    
    # Create several assets with different calibration dates
    assets_data = [
        {"id": "DMM-002", "name": "Multimeter #2", "days_until_due": 5},
        {"id": "SCOPE-002", "name": "Oscilloscope #2", "days_until_due": 30},
        {"id": "PSU-001", "name": "Power Supply", "days_until_due": 60},
        {"id": "TEMP-001", "name": "Temperature Reference", "days_until_due": -10}  # Overdue!
    ]
    
    print("Calibration Status Report:\n")
    
    overdue = []
    due_soon = []
    
    for asset_data in assets_data:
        # Create asset
        asset = api.asset.create_asset(
            asset_id=asset_data["id"],
            name=asset_data["name"],
            asset_type="Test Equipment"
        )
        
        # Set calibration due date
        due_date = datetime.now() + timedelta(days=asset_data["days_until_due"])
        api.asset.update_asset(
            asset_id=asset.asset_id,
            calibration_due_date=due_date
        )
        
        days = asset_data["days_until_due"]
        
        if days < 0:
            status = f"⚠ OVERDUE by {abs(days)} days"
            overdue.append(asset_data)
        elif days <= 30:
            status = f"⚡ Due in {days} days"
            due_soon.append(asset_data)
        else:
            status = f"✓ Due in {days} days"
        
        print(f"  {asset_data['id']}: {asset_data['name']}")
        print(f"    {status}")
        print(f"    Due date: {due_date.strftime('%Y-%m-%d')}")
        print()
    
    # Summary
    print("Summary:")
    print(f"  ⚠ Overdue: {len(overdue)}")
    print(f"  ⚡ Due within 30 days: {len(due_soon)}")
    print(f"  ✓ Current: {len(assets_data) - len(overdue) - len(due_soon)}")
    
    if overdue:
        print(f"\n⚠ ACTION REQUIRED: {len(overdue)} asset(s) overdue for calibration!")
    
    print("=" * 60)


def example_7_asset_location_tracking(api: pyWATS):
    """
    Step 7: Track asset location and transfers.
    
    Manage asset movement between locations.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Asset Location Tracking")
    print("=" * 60)
    
    # Create portable test equipment
    asset = api.asset.create_asset(
        asset_id="DMM-PORTABLE-001",
        name="Portable Multimeter",
        asset_type="Test Equipment",
        location="Equipment Room"
    )
    
    print(f"Asset: {asset.name}")
    print(f"Asset ID: {asset.asset_id}\n")
    
    print("Location History:")
    
    # Simulate asset movement
    locations = [
        {"location": "Equipment Room", "date": "2026-01-15", "note": "Stored"},
        {"location": "Test Station 1", "date": "2026-01-16", "note": "Checked out by Tech A"},
        {"location": "Test Station 3", "date": "2026-01-20", "note": "Transferred"},
        {"location": "Calibration Lab", "date": "2026-01-25", "note": "Annual calibration"},
        {"location": "Equipment Room", "date": "2026-01-26", "note": "Returned to storage"}
    ]
    
    for i, loc in enumerate(locations, 1):
        print(f"  {i}. {loc['date']}: {loc['location']}")
        print(f"     {loc['note']}")
        
        # Update location (in actual implementation)
        # api.asset.update_asset(
        #     asset_id=asset.asset_id,
        #     location=loc['location']
        # )
        # api.asset.create_location_record(
        #     asset_id=asset.asset_id,
        #     location=loc['location'],
        #     date=loc['date'],
        #     note=loc['note']
        # )
    
    print(f"\nCurrent location: {locations[-1]['location']}")
    print(f"Available: Yes")
    print("=" * 60)


def example_8_asset_reports(api: pyWATS):
    """
    Step 8: Generate asset reports and analytics.
    
    Query asset data for management reports.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Asset Reports")
    print("=" * 60)
    
    # Get all assets
    all_assets = api.asset.get_all_assets()
    
    print(f"Asset Inventory Report\n")
    print(f"Total Assets: {len(all_assets)}")
    
    # Group by type
    by_type = {}
    for asset in all_assets:
        asset_type = asset.asset_type
        if asset_type not in by_type:
            by_type[asset_type] = []
        by_type[asset_type].append(asset)
    
    print(f"\nBy Type:")
    for asset_type, assets in by_type.items():
        print(f"  {asset_type}: {len(assets)}")
    
    # Calibration status
    print(f"\nCalibration Status:")
    
    today = datetime.now()
    cal_current = 0
    cal_due_soon = 0
    cal_overdue = 0
    
    for asset in all_assets:
        if hasattr(asset, 'calibration_due_date') and asset.calibration_due_date:
            if asset.calibration_due_date < today:
                cal_overdue += 1
            elif asset.calibration_due_date < today + timedelta(days=30):
                cal_due_soon += 1
            else:
                cal_current += 1
    
    print(f"  Current: {cal_current}")
    print(f"  Due within 30 days: {cal_due_soon}")
    print(f"  Overdue: {cal_overdue}")
    
    # Utilization (example data)
    print(f"\nUtilization (Top 3):")
    print(f"  1. FIXTURE-001: 1,247 cycles")
    print(f"  2. DMM-001: 892 measurements")
    print(f"  3. SCOPE-001: 543 captures")
    
    print("=" * 60)


def main():
    """Run all asset examples."""
    # Connect to WATS API
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")
    
    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)
    
    print("=" * 60)
    print("ASSET DOMAIN EXAMPLES")
    print("Demonstrates equipment, calibration, and maintenance tracking")
    print("=" * 60)
    
    # Run examples
    example_1_create_simple_asset(api)
    example_2_calibration_requirements(api)
    example_3_perform_calibration(api)
    example_4_maintenance_tracking(api)
    example_5_asset_utilization(api)
    example_6_calibration_alerts(api)
    example_7_asset_location_tracking(api)
    example_8_asset_reports(api)
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
