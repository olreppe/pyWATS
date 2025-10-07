"""
Direct test of report models without full package import.
"""

import sys
import os

# Add the source path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

try:
    # Import models directly
    from pyWATS.models.report.uut.uut_report import UUTReport
    from pyWATS.models.report.uur.uur_report import UURReport
    from pyWATS.models.report.uut.uut_info import UUTInfo
    from pyWATS.models.report.uur.uur_info import UURInfo
    from uuid import uuid4
    import datetime
    
    print("✓ Direct model imports successful")
    
    # Test UUTInfo creation
    uut_info = UUTInfo(
        part_number="TEST-PCB-001",
        revision="A", 
        serial_number="SN12345",
        operation_type="Final Test"
    )
    print("✓ UUTInfo creation successful")
    
    # Test UUTReport creation
    uut_report = UUTReport(
        id=uuid4(),
        type="T",
        pn="TEST-PCB-001",
        sn="SN12345",
        rev="A",
        process_code=1,
        station_name="Test Station",
        location="Test Location",
        purpose="Development",
        start=datetime.datetime.now(),
        info=uut_info
    )
    
    print("✓ UUTReport creation successful")
    print(f"  Report ID: {uut_report.id}")
    print(f"  Report Type: {uut_report.type}")
    print(f"  Part Number: {uut_report.pn}")
    print(f"  Serial Number: {uut_report.sn}")
    
    # Test UURInfo creation  
    uur_info = UURInfo(
        part_number="TEST-PCB-002",
        revision="B",
        serial_number="SN67890", 
        operation_type="Repair",
        repair_type="Component Replacement"
    )
    print("✓ UURInfo creation successful")
    
    # Test UURReport creation
    uur_report = UURReport(
        id=uuid4(),
        type="R",
        pn="TEST-PCB-002",
        sn="SN67890",
        rev="B", 
        process_code=1,
        station_name="Repair Station",
        location="Repair Location",
        purpose="Production",
        start=datetime.datetime.now(),
        info=uur_info
    )
    
    print("✓ UURReport creation successful")
    print(f"  Report ID: {uur_report.id}")
    print(f"  Report Type: {uur_report.type}")
    print(f"  Part Number: {uur_report.pn}")
    print(f"  Serial Number: {uur_report.sn}")
    
    # Test serialization
    uut_json = uut_report.model_dump_json(by_alias=True)
    print("✓ UUTReport JSON serialization successful")
    print(f"  JSON length: {len(uut_json)} characters")
    
    uur_json = uur_report.model_dump_json(by_alias=True)
    print("✓ UURReport JSON serialization successful")
    print(f"  JSON length: {len(uur_json)} characters")
    
    print("\n=== Direct Model Test Complete ===")
    print("The report models are working correctly!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()