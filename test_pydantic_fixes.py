"""
Test script to validate the fixes for Pydantic model issues.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing the fixed report models...")
    
    # Test basic imports
    from pyWATS.models.report.wats_base import WATSBase
    from pyWATS.models.report.uut.uut_report import UUTReport
    from pyWATS.models.report.uut.uut_info import UUTInfo
    from pyWATS.models.report.uur.uur_report import UURReport
    from pyWATS.models.report.uur.uur_info import UURInfo
    print("✓ All imports successful")
    
    # Test step imports  
    from pyWATS.models.report.uut.step import Step, StepStatus
    from pyWATS.models.report.uut.steps.boolean_step import BooleanStep, MultiBooleanStep
    from pyWATS.models.report.uut.steps.string_step import StringStep, MultiStringStep
    from pyWATS.models.report.uut.steps.measurement import BooleanMeasurement, MultiBooleanMeasurement
    print("✓ Step imports successful")
    
    # Test creating instances
    from uuid import uuid4
    import datetime
    
    # Test UUT report creation
    uut_info = UUTInfo(operator="Test Operator")
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
    
    # Test UUR report creation
    uur_info = UURInfo(operator="Repair Operator")
    uur_report = UURReport(
        id=uuid4(),
        type="R",
        pn="TEST-002",
        sn="SN002", 
        rev="B",
        process_code=1,
        station_name="Repair Station",
        location="Repair Location",
        purpose="Production",
        start=datetime.datetime.now(),
        info=uur_info
    )
    print("✓ UURReport creation successful")
    
    # Test step creation with proper step_types
    boolean_step = BooleanStep(
        step_type="ET_PFT",
        name="Boolean Test Step",
        status=StepStatus.Passed
    )
    print("✓ BooleanStep creation successful")
    print(f"  Step type: {boolean_step.step_type}")
    print(f"  Step name: {boolean_step.name}")
    print(f"  Step status: {boolean_step.status}")
    
    string_step = StringStep(
        step_type="ET_SVT", 
        name="String Test Step",
        status=StepStatus.Passed
    )
    print("✓ StringStep creation successful")
    print(f"  Step type: {string_step.step_type}")
    
    # Test measurement creation
    bool_measurement = BooleanMeasurement(status="P")
    multi_bool_measurement = MultiBooleanMeasurement(name="Test Measurement", status="P")
    print("✓ Measurement creation successful")
    
    # Test step with measurement
    boolean_step_with_meas = BooleanStep(
        step_type="ET_PFT",
        name="Boolean Test with Measurement",
        status=StepStatus.Passed,
        measurement=bool_measurement
    )
    print("✓ BooleanStep with measurement creation successful")
    
    # Test JSON serialization
    uut_json = uut_report.model_dump_json(by_alias=True)
    uur_json = uur_report.model_dump_json(by_alias=True)
    step_json = boolean_step.model_dump_json(by_alias=True)
    print("✓ JSON serialization successful")
    print(f"  UUT JSON length: {len(uut_json)} chars")
    print(f"  UUR JSON length: {len(uur_json)} chars") 
    print(f"  Step JSON length: {len(step_json)} chars")
    
    # Test model validation
    from pyWATS.models.report.uur.failure import Failure
    failure = Failure(
        category="Test Category",
        code="TC001",
        ref_step_name="Test Step",
        com_ref=None  # Test Optional field
    )
    print("✓ Optional field validation successful")
    
    print("\n=== All Fixes Validated Successfully! ===")
    print("✓ Optional field type annotations fixed")
    print("✓ Step type hierarchy inconsistencies resolved") 
    print("✓ Pydantic model validation issues fixed")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()