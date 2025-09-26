"""
Comprehensive TDM Example

This example demonstrates the complete TDM workflow including:
- Finding existing reports
- Loading reports from server
- Creating new UUT reports
- Creating UUR (repair) reports
- Submitting reports online and offline
- Managing pending reports

This showcases the TDMClient functionality equivalent to the C# TDM class.
"""

import sys
import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

# Add src to path so we can import pyWATS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pyWATS import TDMClient
from pyWATS.tdm_client import (
    APIStatusType, 
    ClientStateType, 
    SubmitMethod, 
    ValidationModeType,
    TestModeType
)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def print_subsection(title: str) -> None:
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---")


def print_report_summary(report) -> None:
    """Print a summary of a report."""
    # Handle both new WSJF models and legacy dictionary format
    if hasattr(report, 'type'):
        # New WSJF model format
        report_type = report.type
        report_id = str(report.id)
        serial_number = report.sn
        part_number = report.pn
        operator = report.info.operator if report.info else 'N/A'
    else:
        # Legacy dictionary format
        report_type = report.get('report_type', 'Unknown')
        report_id = report.get('report_id', 'N/A')
        serial_number = report.get('serial_number', 'N/A')
        part_number = report.get('part_number', 'N/A')
        operator = report.get('operator_name', 'N/A')
    
    print(f"  Type: {report_type}")
    print(f"  ID: {report_id}")
    print(f"  Serial Number: {serial_number}")
    print(f"  Part Number: {part_number}")
    print(f"  Operator: {operator}")


def demonstrate_tdm_client_setup() -> TDMClient:
    """Demonstrate TDM client setup and configuration."""
    print_section("TDM CLIENT SETUP")
    
    # Create TDM client instance
    print("[1] Creating TDMClient instance...")
    tdm = TDMClient()
    print("    ✓ TDMClient created successfully")
    
    # Configure API settings
    print("\n[2] Configuring API settings...")
    tdm.setup_api(
        data_dir="./wats_tdm_data",
        location="TDM Demo Lab",
        purpose="Development Testing",
        persist=False
    )
    
    # Set additional properties
    tdm.station_name = "TDM_Demo_Station"
    tdm.validation_mode = ValidationModeType.ThrowExceptions
    tdm.test_mode = TestModeType.Active
    tdm.root_step_name = "TDM Demo Sequence"
    
    print("    ✓ API configured successfully")
    print(f"    ✓ Station Name: {tdm.station_name}")
    print(f"    ✓ Data Directory: {tdm.data_dir}")
    print(f"    ✓ Location: {tdm.location}")
    print(f"    ✓ Purpose: {tdm.purpose}")
    
    return tdm


def demonstrate_connection_management(tdm: TDMClient) -> bool:
    """Demonstrate connection and registration."""
    print_section("CONNECTION MANAGEMENT")
    
    # Configuration - replace with your actual WATS server details
    BASE_URL = "https://ola.wats.com"
    AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
    
    try:
        print("[1] Registering client with WATS server...")
        tdm.register_client(base_url=BASE_URL, token=AUTH_TOKEN)
        print("    ✓ Client registered successfully")
        
        print("\n[2] Initializing API...")
        tdm.initialize_api(
            try_connect_to_server=True,
            download_metadata=True
        )
        
        print(f"    ✓ API Status: {tdm.status}")
        print(f"    ✓ Client State: {tdm.client_state}")
        
        if tdm.status == APIStatusType.Online:
            print("    ✓ Successfully connected to WATS server!")
            return True
        else:
            print("    ⚠ Connected but not online - will demonstrate offline mode")
            return False
            
    except Exception as e:
        print(f"    ✗ Connection failed: {e}")
        print("    ⚠ Will demonstrate offline mode")
        return False


def demonstrate_metadata_operations(tdm: TDMClient) -> tuple[List[Dict], List[Dict]]:
    """Demonstrate metadata retrieval operations."""
    print_section("METADATA OPERATIONS")
    
    operation_types = []
    repair_types = []
    
    try:
        print("[1] Retrieving operation types...")
        operation_types = tdm.get_operation_types()
        print(f"    ✓ Found {len(operation_types)} operation types")
        
        # Show first few operation types
        for i, op_type in enumerate(operation_types[:3]):
            print(f"    {i+1}. {op_type['name']} (Code: {op_type['code']}, ID: {op_type['id']})")
            
        if len(operation_types) > 3:
            print(f"    ... and {len(operation_types) - 3} more")
    
    except Exception as e:
        print(f"    ✗ Failed to get operation types: {e}")
        # Create mock operation types for demo
        operation_types = [
            {'id': 'mock-op-1', 'code': '10', 'name': 'Mock Test Operation', 'description': 'Mock test for demo'},
            {'id': 'mock-op-2', 'code': '20', 'name': 'Mock Calibration', 'description': 'Mock calibration for demo'}
        ]
        print("    ⚠ Using mock operation types for demonstration")
    
    try:
        print("\n[2] Retrieving repair types...")
        repair_types = tdm.get_repair_types()
        print(f"    ✓ Found {len(repair_types)} repair types")
        
        # Show first few repair types
        for i, repair_type in enumerate(repair_types[:3]):
            print(f"    {i+1}. {repair_type['name']} (Code: {repair_type['code']}, UUT Required: {repair_type.get('uut_required', False)})")
            
        if len(repair_types) > 3:
            print(f"    ... and {len(repair_types) - 3} more")
    
    except Exception as e:
        print(f"    ✗ Failed to get repair types: {e}")
        # Create mock repair types for demo
        repair_types = [
            {'id': 'mock-repair-1', 'code': '30', 'name': 'Mock Component Repair', 'description': 'Mock repair for demo', 'uut_required': True},
            {'id': 'mock-repair-2', 'code': '40', 'name': 'Mock Adjustment', 'description': 'Mock adjustment for demo', 'uut_required': False}
        ]
        print("    ⚠ Using mock repair types for demonstration")
    
    return operation_types, repair_types


def demonstrate_finding_reports(tdm: TDMClient) -> List[Dict]:
    """Demonstrate finding existing reports."""
    print_section("FINDING EXISTING REPORTS")
    
    found_reports = []
    
    try:
        print("[1] Attempting to find reports from server...")
        
        # In a real implementation, you would use REST API endpoints to find reports
        # For this demo, we'll simulate the process
        if tdm.status == APIStatusType.Online and tdm.connection:
            print("    ℹ Server connection available - would query report endpoints")
            print("    ℹ Example queries:")
            print("      - Find reports by part number: GET /api/Report?$filter=partNumber eq 'DEMO_PART'")
            print("      - Find reports by date range: GET /api/Report?$filter=start ge 2023-01-01")
            print("      - Find reports by serial number: GET /api/Report?$filter=serialNumber eq 'DEMO001'")
            
            # Simulate found reports
            found_reports = [
                {
                    'report_id': 'existing-report-1',
                    'report_type': 'UUT',
                    'serial_number': 'EXISTING001',
                    'part_number': 'EXISTING_PART',
                    'operator_name': 'ExistingOperator',
                    'start_time': '2023-09-01T10:00:00Z',
                    'result': 'Passed'
                }
            ]
            print(f"    ✓ Simulation: Found {len(found_reports)} existing reports")
        else:
            print("    ⚠ No server connection - cannot query existing reports")
            
    except Exception as e:
        print(f"    ✗ Error finding reports: {e}")
    
    # Check for pending local reports
    print("\n[2] Checking for pending local reports...")
    try:
        pending_count = tdm.get_pending_report_count()
        print(f"    ✓ Found {pending_count} pending reports in local queue")
    except Exception as e:
        print(f"    ✗ Error checking pending reports: {e}")
    
    return found_reports


def demonstrate_loading_reports(tdm: TDMClient, found_reports: List[Dict]) -> Optional[Dict]:
    """Demonstrate loading reports from server."""
    print_section("LOADING REPORTS")
    
    loaded_report = None
    
    if found_reports:
        print("[1] Attempting to load report from server...")
        try:
            report_id = found_reports[0]['report_id']
            print(f"    ℹ Loading report ID: {report_id}")
            
            # In a real implementation, you would load from server
            if tdm.status == APIStatusType.Online and tdm.connection:
                print("    ℹ Would use: GET /api/Internal/Report/WRML/{report_id}")
                
                # Simulate loaded report with more details
                loaded_report = {
                    **found_reports[0],
                    'steps': [
                        {'name': 'Initialize', 'result': 'Passed', 'duration': 1.5},
                        {'name': 'Test Voltage', 'result': 'Passed', 'measurement': 5.02, 'units': 'V'},
                        {'name': 'Test Current', 'result': 'Passed', 'measurement': 2.1, 'units': 'A'}
                    ],
                    'measurements': [
                        {'name': 'Supply Voltage', 'value': 5.02, 'units': 'V', 'limits': {'low': 4.9, 'high': 5.1}},
                        {'name': 'Load Current', 'value': 2.1, 'units': 'A', 'limits': {'low': 2.0, 'high': 2.5}}
                    ]
                }
                print("    ✓ Report loaded successfully (simulated)")
                print_report_summary(loaded_report)
            else:
                print("    ⚠ No server connection - cannot load reports")
                
        except Exception as e:
            print(f"    ✗ Error loading report: {e}")
    else:
        print("[1] No reports found to load")
    
    return loaded_report


def create_sample_uut_report(tdm: TDMClient, operation_types: List[Dict]):
    """Create a comprehensive UUT report with test data."""
    print_subsection("Creating UUT Report")
    
    # Select operation type
    op_type = operation_types[0] if operation_types else {
        'id': 'demo-op',
        'code': '100', 
        'name': 'Demo Test Operation',
        'description': 'Demo operation for testing'
    }
    
    print(f"    Using operation type: {op_type['name']} (Code: {op_type['code']})")
    
    # Create the UUT report - now returns UUTReport instance
    uut_report = tdm.create_uut_report(
        operator_name="Demo_Operator",
        part_number="DEMO_PART_001",
        revision="Rev_A",
        serial_number=f"DEMO_SN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        operation_type=op_type,
        sequence_file_name="demo_test_sequence.py",
        sequence_file_version="1.2.3"
    )
    
    # Add test information as misc info (since WSJF model doesn't have steps/measurements as direct fields)
    uut_report.add_misc_info("TestSteps", "Initialize System, Power Supply Test, Signal Integrity Test")
    uut_report.add_misc_info("TotalTestTime", "8900 ms")
    uut_report.add_misc_info("PassRate", "100%")
    uut_report.add_misc_info("TestConfiguration", "Automated Test Suite v1.2.3")
    
    # Set final result
    uut_report.result = 'P'  # Passed
    
    print("    ✓ UUT report created successfully")
    print_report_summary(uut_report)
    print(f"    Misc Info Items: {len(uut_report.misc_infos)}")
    print(f"    Result: {uut_report.result}")
    
    return uut_report


def create_sample_uur_report(tdm: TDMClient, repair_types: List[Dict], uut_report=None):
    """Create a comprehensive UUR (repair) report."""
    print_subsection("Creating UUR Report")
    
    # Select repair type
    repair_type = repair_types[0] if repair_types else {
        'id': 'demo-repair',
        'code': '200',
        'name': 'Demo Component Repair',
        'description': 'Demo repair operation',
        'uut_required': False
    }
    
    print(f"    Using repair type: {repair_type['name']} (Code: {repair_type['code']})")
    
    # Get part info from UUT if available
    if uut_report and hasattr(uut_report, 'uut'):
        part_number = uut_report.uut.pn
        serial_number = uut_report.uut.sn
        revision = uut_report.uut.rev
    else:
        part_number = "REPAIR_PART_001"
        serial_number = f"REPAIR_SN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        revision = "Rev_B"
    
    # Create the UUR report - now returns UURReport instance
    uur_report = tdm.create_uur_report(
        operator_name="Repair_Technician",
        repair_type=repair_type,
        part_number=part_number,
        revision=revision,
        serial_number=serial_number
    )
    
    # Add repair information as misc info (since WSJF model structure is different)
    uur_report.add_misc_info("RepairType", "Component Replacement and Calibration")
    uur_report.add_misc_info("ComponentsReplaced", "CAP_100uF_25V (C15)")
    uur_report.add_misc_info("CalibrationAdjustments", "Voltage reference trimmer R23: 2.3k ohm")
    uur_report.add_misc_info("VerificationTests", "Post-Repair Voltage: 5.01V (Pass), Current: 0.82A (Pass)")
    uur_report.add_misc_info("RepairTechnician", "Repair_Technician")
    uur_report.add_misc_info("ToolsUsed", "Soldering Iron, Multimeter")
    
    # Set final result
    uur_report.result = 'P'  # Passed (repaired)
    
    print("    ✓ UUR report created successfully")
    print_report_summary(uur_report)
    print(f"    Misc Info Items: {len(uur_report.misc_infos)}")
    print(f"    Result: {uur_report.result}")
    
    return uur_report


def demonstrate_report_creation(tdm: TDMClient, operation_types: List[Dict], repair_types: List[Dict]):
    """Demonstrate creating UUT and UUR reports."""
    print_section("REPORT CREATION")
    
    # Create UUT report
    uut_report = create_sample_uut_report(tdm, operation_types)
    
    # Create UUR report
    uur_report = create_sample_uur_report(tdm, repair_types, uut_report)
    
    return uut_report, uur_report


def demonstrate_report_submission(tdm: TDMClient, uut_report, uur_report, operation_types: List[Dict]) -> None:
    """Demonstrate report submission with different methods."""
    print_section("REPORT SUBMISSION")
    
    # Submit UUT report
    print_subsection("Submitting UUT Report")
    
    try:
        print("[1] Attempting automatic submission...")
        success = tdm.submit_report(uut_report, SubmitMethod.Automatic)
        
        if success:
            if tdm.status == APIStatusType.Online:
                print("    ✓ UUT report submitted online successfully")
            else:
                print("    ✓ UUT report saved to offline queue")
        else:
            print("    ✗ UUT report submission failed")
            
    except Exception as e:
        print(f"    ✗ Error submitting UUT report: {e}")
    
    # Submit UUR report  
    print_subsection("Submitting UUR Report")
    
    try:
        print("[1] Attempting automatic submission...")
        success = tdm.submit_report(uur_report, SubmitMethod.Automatic)
        
        if success:
            if tdm.status == APIStatusType.Online:
                print("    ✓ UUR report submitted online successfully")
            else:
                print("    ✓ UUR report saved to offline queue")
        else:
            print("    ✗ UUR report submission failed")
            
    except Exception as e:
        print(f"    ✗ Error submitting UUR report: {e}")
    
    # Demonstrate offline submission
    print_subsection("Demonstrating Offline Submission")
    
    # Create another report for offline demo
    demo_offline_report = tdm.create_uut_report(
        operator_name="Offline_Demo_Operator",
        part_number="OFFLINE_PART",
        revision="Rev_1",
        serial_number=f"OFFLINE_{datetime.now().strftime('%H%M%S')}",
        operation_type=operation_types[0] if operation_types else {"code": "OFFLINE", "name": "Offline Test"},
        sequence_file_name="offline_demo.py",
        sequence_file_version="1.0.0"
    )
    
    try:
        print("[1] Forcing offline submission...")
        success = tdm.submit_report(demo_offline_report, SubmitMethod.Offline)
        
        if success:
            print("    ✓ Report saved to offline queue successfully")
        else:
            print("    ✗ Failed to save report to offline queue")
            
    except Exception as e:
        print(f"    ✗ Error with offline submission: {e}")


def demonstrate_pending_reports_management(tdm: TDMClient) -> None:
    """Demonstrate managing pending reports."""
    print_section("PENDING REPORTS MANAGEMENT")
    
    try:
        print("[1] Checking pending reports...")
        pending_count = tdm.get_pending_report_count()
        print(f"    ✓ Found {pending_count} pending reports")
        
        if pending_count > 0:
            print("\n[2] Attempting to submit pending reports...")
            
            if tdm.status == APIStatusType.Online:
                submitted_count = tdm.submit_pending_reports()
                print(f"    ✓ Successfully submitted {submitted_count} reports")
                
                remaining_count = tdm.get_pending_report_count()
                print(f"    ✓ Remaining pending reports: {remaining_count}")
            else:
                print("    ⚠ Server offline - pending reports remain queued")
                print("    ℹ Reports will be submitted automatically when server becomes available")
        else:
            print("    ℹ No pending reports to submit")
            
    except Exception as e:
        print(f"    ✗ Error managing pending reports: {e}")


def demonstrate_additional_features(tdm: TDMClient) -> None:
    """Demonstrate additional TDM client features."""
    print_section("ADDITIONAL FEATURES")
    
    # Test ping functionality
    print_subsection("Connection Testing")
    
    try:
        print("[1] Testing server connection (ping)...")
        if tdm.ping():
            print("    ✓ Server ping successful")
        else:
            print("    ✗ Server ping failed")
    except Exception as e:
        print(f"    ✗ Ping error: {e}")
    
    # Demonstrate sub-module access
    print_subsection("Sub-Module Access")
    
    print("[1] Accessing TDM sub-modules...")
    
    if tdm.statistics:
        print("    ✓ Statistics module available")
        print("      ℹ Use: tdm.statistics.get_last_result(), get_trend(), etc.")
    else:
        print("    ⚠ Statistics module not available (no connection)")
    
    if tdm.analytics:
        print("    ✓ Analytics module available") 
        print("      ℹ Use: tdm.analytics.get_aggregated_measurements(), analyze_trends(), etc.")
    else:
        print("    ⚠ Analytics module not available (no connection)")
    
    if tdm.reports:
        print("    ✓ Reports module available")
        print("      ℹ Use: tdm.reports.generate_report(), export_data(), etc.")
    else:
        print("    ⚠ Reports module not available (no connection)")
    
    # Show configuration
    print_subsection("Current Configuration")
    
    print(f"    API Status: {tdm.status}")
    print(f"    Client State: {tdm.client_state}")
    print(f"    Station Name: {tdm.station_name}")
    print(f"    Validation Mode: {tdm.validation_mode}")
    print(f"    Test Mode: {tdm.test_mode}")
    print(f"    Root Step Name: {tdm.root_step_name}")
    print(f"    Data Directory: {tdm.data_dir}")
    
    if tdm.last_service_exception:
        print(f"    Last Exception: {tdm.last_service_exception}")


def demonstrate_cleanup(tdm: TDMClient) -> None:
    """Demonstrate proper cleanup."""
    print_section("CLEANUP")
    
    print("[1] Performing cleanup...")
    
    try:
        # Show final status
        pending_count = tdm.get_pending_report_count()
        print(f"    Final pending reports count: {pending_count}")
        
        # Unregister client
        tdm.unregister_client()
        print("    ✓ Client unregistered successfully")
        print(f"    ✓ Final status: {tdm.status}")
        print(f"    ✓ Final client state: {tdm.client_state}")
        
    except Exception as e:
        print(f"    ✗ Error during cleanup: {e}")


def main():
    """Main demonstration function."""
    print("="*80)
    print(" COMPREHENSIVE TDM DEMONSTRATION")
    print(" Python equivalent of C# TDM class functionality")
    print("="*80)
    print(f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" pyWATS TDMClient Demo")
    print("="*80)
    
    tdm = None
    
    try:
        # 1. Setup TDM client
        tdm = demonstrate_tdm_client_setup()
        
        # 2. Connection management
        is_online = demonstrate_connection_management(tdm)
        
        # 3. Metadata operations
        operation_types, repair_types = demonstrate_metadata_operations(tdm)
        
        # 4. Finding existing reports
        found_reports = demonstrate_finding_reports(tdm)
        
        # 5. Loading reports
        loaded_report = demonstrate_loading_reports(tdm, found_reports)
        
        # 6. Creating new reports
        uut_report, uur_report = demonstrate_report_creation(tdm, operation_types, repair_types)
        
        # 7. Submitting reports
        demonstrate_report_submission(tdm, uut_report, uur_report, operation_types)
        
        # 8. Managing pending reports
        demonstrate_pending_reports_management(tdm)
        
        # 9. Additional features
        demonstrate_additional_features(tdm)
        
        print_section("DEMONSTRATION SUMMARY")
        print("✓ TDM Client Setup and Configuration")
        print("✓ Connection Management and Registration") 
        print("✓ Metadata Retrieval (Operation Types, Repair Types)")
        print("✓ Finding and Loading Existing Reports")
        print("✓ Creating UUT Reports with Test Data")
        print("✓ Creating UUR Reports with Repair Data")
        print("✓ Report Submission (Online/Offline/Automatic)")
        print("✓ Pending Reports Management")
        print("✓ Additional Features (Ping, Sub-modules)")
        
        if is_online:
            print("\n🌐 Server Connection: ONLINE")
            print("   Reports were submitted directly to server")
        else:
            print("\n📴 Server Connection: OFFLINE")
            print("   Reports were queued locally for later submission")
            
        print(f"\n📊 Reports Created: 3 (2 UUT, 1 UUR)")
        print(f"📁 Data Directory: {tdm.data_dir}")
        print(f"📋 Pending Reports: {tdm.get_pending_report_count()}")
        
    except Exception as e:
        print_section("ERROR")
        print(f"✗ Demonstration failed with error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        if tdm:
            demonstrate_cleanup(tdm)
        
        print_section("DEMONSTRATION COMPLETE")
        print("Thank you for exploring the pyWATS TDMClient!")
        print("For more information, see:")
        print("  - TDM_CLIENT_IMPLEMENTATION.md")
        print("  - examples/tdm_client_example.py")
        print("  - Source code: src/pyWATS/tdm_client.py")


if __name__ == "__main__":
    main()