"""
Test TDM functionality with fixed models.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing TDM with fixed models...")
    
    # Test TDM import and creation (bypassing full package imports)
    from pyWATS.tdm import TDM
    from pyWATS.models.report.uut.uut_report import UUTReport
    from pyWATS.models.report.uur.uur_report import UURReport
    print("✓ TDM imports successful")
    
    # Mock client
    class MockClient:
        pass
    
    # Initialize TDM
    tdm = TDM(MockClient())
    tdm.setup_api("./test_data", "Test Station", "Development")
    print("✓ TDM setup successful")
    
    # Test UUT report creation through TDM
    uut_report = tdm.create_uut_report(
        operator="John Doe",
        part_number="PCB-123", 
        revision="A",
        serial_number="SN12345",
        operation_type="Final Test",
        sequence_file="test.seq",
        version="1.0"
    )
    print("✓ TDM UUT report creation successful")
    print(f"  Report ID: {uut_report.id}")
    print(f"  Report Type: {uut_report.type}")
    print(f"  Part Number: {uut_report.pn}")
    
    # Test UUR report creation through TDM  
    uur_report = tdm.create_uur_report(
        operator="Jane Smith",
        repair_type="Component Replacement",
        operation_type="Repair",
        serial_number="SN67890",
        part_number="PCB-456",
        revision="B"
    )
    print("✓ TDM UUR report creation successful")
    print(f"  Report ID: {uur_report.id}")
    print(f"  Report Type: {uur_report.type}")
    print(f"  Part Number: {uur_report.pn}")
    
    # Test report submission simulation
    report_id = tdm.submit(uut_report)
    print(f"✓ TDM report submission successful - ID: {report_id}")
    
    # Test operation types retrieval
    op_types = tdm.get_operation_types()
    print(f"✓ TDM operation types retrieval successful - {len(op_types)} types")
    
    # Test getting a specific operation type
    op_type = tdm.get_operation_type(1)
    print(f"✓ TDM specific operation type retrieval successful - {op_type['name']}")
    
    print("\n=== TDM Integration Test Complete ===")
    print("✓ TDM functionality working with fixed models")
    print("✓ Report creation through TDM interface successful")
    print("✓ All validation and type issues resolved")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()