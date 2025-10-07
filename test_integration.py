"""
Test script to verify the report model integration.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test basic imports
    from pyWATS import TDM, UUTReport, UURReport
    from pyWATS.models.report import Report
    from pyWATS import report_utils
    
    print("✓ All imports successful")
    
    # Test TDM instantiation (without actual client)
    class MockClient:
        pass
    
    mock_client = MockClient()
    tdm = TDM(mock_client)
    tdm.setup_api("./test_data", "Test Station", "Development")
    
    print("✓ TDM setup successful")
    
    # Test UUT report creation
    try:
        uut_report = tdm.create_uut_report(
            operator="Test Operator",
            part_number="TEST-PCB-001",
            revision="A",
            serial_number="SN12345",
            operation_type="Final Test",
            sequence_file="test_sequence.seq",
            version="1.0"
        )
        print("✓ UUT Report creation successful")
        print(f"  Report ID: {uut_report.id}")
        print(f"  Report Type: {uut_report.type}")
        print(f"  Part Number: {uut_report.pn}")
        
    except Exception as e:
        print(f"✗ UUT Report creation failed: {e}")
    
    # Test UUR report creation
    try:
        uur_report = tdm.create_uur_report(
            operator="Repair Operator",
            repair_type="Component Replacement",
            operation_type="Repair",
            serial_number="SN67890",
            part_number="TEST-PCB-002",
            revision="B"
        )
        print("✓ UUR Report creation successful")
        print(f"  Report ID: {uur_report.id}")
        print(f"  Report Type: {uur_report.type}")
        print(f"  Part Number: {uur_report.pn}")
        
    except Exception as e:
        print(f"✗ UUR Report creation failed: {e}")
    
    # Test report utilities
    try:
        summary = report_utils.get_report_summary(uut_report)
        print("✓ Report summary generation successful")
        print(f"  Summary keys: {list(summary.keys())}")
        
        errors = report_utils.validate_report(uut_report)
        if not errors:
            print("✓ Report validation successful - no errors found")
        else:
            print(f"⚠ Report validation found issues: {errors}")
            
    except Exception as e:
        print(f"✗ Report utilities failed: {e}")
    
    print("\n=== Integration Test Complete ===")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("This indicates there are still import issues to resolve")
    
except Exception as e:
    print(f"✗ Unexpected error: {e}")
    import traceback
    traceback.print_exc()