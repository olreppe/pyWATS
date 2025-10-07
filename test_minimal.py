"""
Minimal test of just the core report models.
"""

import sys
import os

# Add the source path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test just the basic models first
    from pyWATS.models.report.wats_base import WATSBase
    print("✓ WATSBase import successful")
    
    from pyWATS.models.report.common_types import *
    print("✓ Common types import successful")
    
    from pyWATS.models.report.report import Report, ReportStatus
    print("✓ Report base class import successful")
    
    # Test info classes
    from pyWATS.models.report.uut.uut_info import UUTInfo
    from pyWATS.models.report.uur.uur_info import UURInfo
    print("✓ Info classes import successful")
    
    # Test the actual report classes
    from pyWATS.models.report.uut.uut_report import UUTReport
    from pyWATS.models.report.uur.uur_report import UURReport
    print("✓ Report classes import successful")
    
    # Test creating instances
    from uuid import uuid4
    import datetime
    
    uut_info = UUTInfo(
        operator="Test Operator"  # Only required field
    )
    
    uut_report = UUTReport(
        id=uuid4(),
        type="T",
        pn="TEST-001",
        sn="SN001",
        rev="A",
        process_code=1,
        station_name="Test Station",
        location="Test Location",
        purpose="Development",
        start=datetime.datetime.now(),
        info=uut_info
    )
    
    print("✓ UUTReport creation successful")
    print(f"  ID: {uut_report.id}")
    print(f"  Type: {uut_report.type}")
    print(f"  PN: {uut_report.pn}")
    
    # Test JSON serialization
    json_data = uut_report.model_dump_json(by_alias=True)
    print("✓ JSON serialization successful")
    print(f"  JSON length: {len(json_data)} chars")
    
    print("\n=== Minimal Test Successful ===")
    print("Core report models are working!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()