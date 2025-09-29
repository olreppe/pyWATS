"""
Simple UUT Test Runner

A straightforward test runner for UUT functionality with minimal dependencies.
Run this directly to test UUT creation, submission, and loading.
"""

import sys
import os
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Test configuration
TEST_BASE_URL = "https:        from pyWATS.tdm.models import UURReport/ola.wats.com"
TEST_AUTH_TOKEN = "cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
KNOWN_FAT_REPORT_ID = "14ca0682-35b9-415d-8c61-de8367c5a9df"


def print_header(title):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def test_simple_uut_workflow():
    """Test 1: Simple UUT workflow - Create → Submit → Load."""
    print_header("TEST 1: Simple UUT Workflow")
    
    try:
        # Import here to avoid issues
        from pyWATS.tdm_client import TDMClient, APIStatusType, SubmitMethod
        from pyWATS.tdm.models import SubRepair, UUTReport
        
        # Setup client
        print("[1] Setting up test client...")
        client = TDMClient()
        client.setup_api(
            data_dir="./test_data",
            location="Test Lab",
            purpose="Automated Testing"
        )
        client.station_name = "Test_Station"
        
        # Connect
        client.register_client(base_url=TEST_BASE_URL, token=TEST_AUTH_TOKEN)
        client.initialize_api()
        
        if client.status != APIStatusType.Online:
            print(f"❌ Client not online: {client.status}")
            return False
        
        print("    ✅ Client setup successful")
        
        # Create UUT
        print("[2] Creating UUT report...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Use client's create_uut_report method like in tdm_example.py
        operation_type = {
            'code': 122,  # ABI Test operation
            'name': 'Test Operation',
            'description': 'Automated test operation'
        }
        
        uut_report = client.create_uut_report(
            operator_name="Test_Operator",
            part_number="TEST_PART_001",
            revision="Rev_Test",
            serial_number=f"TEST_SN_{timestamp}",
            operation_type=operation_type,
            sequence_file_name="automated_test_sequence.py",
            sequence_file_version="1.0.0"
        )
        
        # Add test info
        uut_report.add_misc_info("TestType", "Automated")
        uut_report.add_misc_info("Timestamp", timestamp)
        
        print(f"    ✅ Created UUT: {uut_report.id}")
        print(f"    ✅ Serial: {uut_report.sn}")
        
        # Submit UUT  
        print("[3] Submitting UUT report...")
        
        success = client.submit_report(uut_report, SubmitMethod.Automatic)
        
        if not success:
            print(f"❌ Submission failed")
            return False
            
        print(f"    ✅ UUT submitted successfully")
        print(f"    ✅ Report ID: {uut_report.id}")
        
        # Load UUT
        print("[4] Loading UUT report...")
        time.sleep(5)  # Wait for processing
        
        if not client._connection or not client._connection._client:
            print(f"❌ No connection available")
            return False
        
        url = f"/api/Report/Wsjf/{uut_report.id}"
        response = client._connection._client.get(url)
        
        if response.status_code != 200:
            print(f"❌ Load failed: HTTP {response.status_code}")
            return False
            
        if not response.text.strip():
            print(f"❌ Empty response")
            return False
            
        try:
            loaded_data = response.json()
            loaded_uut = UUTReport.model_validate(loaded_data)
            
            print(f"    ✅ UUT loaded successfully")
            print(f"    ✅ Loaded ID: {loaded_uut.id}")
            print(f"    ✅ Loaded SN: {loaded_uut.sn}")
            print(f"    ✅ Round-trip successful!")
            
            return True
            
        except Exception as e:
            print(f"❌ Deserialization failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_uur_workflow():
    """Test 2: Simple UUR workflow - Create → Submit → Load with repair steps."""
    print_header("TEST 2: Simple UUR Workflow")
    
    try:
        # Import here to avoid issues
        from pyWATS.tdm_client import TDMClient, APIStatusType, SubmitMethod
        from pyWATS.tdm.models import UURReport
        
        # Setup client
        print("[1] Setting up test client...")
        client = TDMClient()
        client.setup_api(
            data_dir="./test_data",
            location="Test Lab",
            purpose="Automated Testing"
        )
        client.station_name = "Test_Station"
        
        # Connect
        client.register_client(base_url=TEST_BASE_URL, token=TEST_AUTH_TOKEN)
        client.initialize_api()
        
        if client.status != APIStatusType.Online:
            print(f"❌ Client not online: {client.status}")
            return False
        
        print("    ✅ Client setup successful")
        
        # Create UUR
        print("[2] Creating UUR report...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # ========================================================================
        # UUR DUAL PROCESS CODE SYSTEM EXPLANATION:
        # ========================================================================
        # UUR (Unit Under Repair) reports require TWO different process codes:
        #
        # 1. REPAIR OPERATION CODE (500) - Goes in report.processCode field
        #    - This identifies the current repair operation being performed
        #    - Server uses this to categorize the repair activity
        #
        # 2. TEST OPERATION CODE (122) - Goes in uur.processCode field  
        #    - This references the original test operation that failed
        #    - Links the repair back to what was being tested when it failed
        #    - Also goes in uur.refUUT field as string reference
        #
        # This dual system allows WATS to:
        # - Track repair operations separately from test operations
        # - Maintain traceability between failed tests and repairs
        # - Generate proper repair vs test statistics
        # ========================================================================
        
        # Step 1: Get actual REPAIR operations from the system
        print("    Getting available repair operations from server...")
        repair_operations = client.get_repair_operations()
        if not repair_operations:
            print("    ❌ No repair operations available")
            return False
        
        repair_operation = repair_operations[0]  # Use first available repair operation
        print(f"    Using repair operation: {repair_operation.get('name')} (Code: {repair_operation.get('code')})")
        
        # Step 2: Get actual TEST operations from the system
        print("    Getting available test operations from server...")
        test_operations = client.get_test_operations() 
        if not test_operations:
            print("    ❌ No test operations available")
            return False
            
        original_test_operation = test_operations[0]  # Use first available test operation
        print(f"    Using test operation: {original_test_operation.get('name')} (Code: {original_test_operation.get('code')})")
        
        # Step 3: Create UUR with dual process code system
        uur_report = client.create_uur_report(
            operator_name="Repair_Operator",
            repair_type=repair_operation,  # Sets report.processCode = 500 (repair op)
            part_number="TEST_PART_001",
            revision="Rev_Test", 
            serial_number=f"REPAIR_SN_{timestamp}",
            failure_category=None,  # Will be set from actual system values
            failure_code=None       # Will be set from actual system values
        )
        
        # Step 4: Manually set the UUT reference process code (the missing piece!)
        # This is what was missing - the UUR info needs the original test process code
        if uur_report.uur_info:
            # Set the process code to reference the original test operation
            uur_report.uur_info.process_code = original_test_operation['code']  # Original test op code
            
            # refUUT should be a UUID of the original UUT report, but since this is a standalone
            # repair test, we'll use a dummy UUID format. In real scenarios, this would be
            # the actual UUID of the failed UUT report being repaired.
            uur_report.uur_info.ref_uut = str(uur_report.id)  # Use our own report ID as demo
        
        # Get actual failure categories and codes from the system for proper validation
        print("    Getting available failure categories and codes from server...")
        all_processes = client.get_all_processes()
        
        # Find a valid failure category and code from the available processes
        valid_category = None
        valid_code = None
        
        for process in all_processes:
            if 'failureCategories' in process and process['failureCategories']:
                for category in process['failureCategories']:
                    if isinstance(category, dict) and 'name' in category:
                        valid_category = category['name']
                        break
                    elif isinstance(category, str):
                        valid_category = category
                        break
                        
            if 'failureCodes' in process and process['failureCodes']:
                for code in process['failureCodes']:
                    if isinstance(code, dict) and 'code' in code:
                        valid_code = code['code']
                        break
                    elif isinstance(code, str):
                        valid_code = code
                        break
                        
            if valid_category and valid_code:
                break
        
        print(f"    Using failure category: {valid_category}")
        print(f"    Using failure code: {valid_code}")
        
        # Skip adding misc info for now - server has strict validation on descriptions
        # In production, you would need to get valid misc info descriptions from the system
        # uur_report.add_misc_info("Operation", repair_operation.get('name', 'Repair'))
        print("    Skipping misc info (server has strict validation requirements)")
        
        # Add repair steps with proper hierarchical structure
        print("[3] Adding repair steps...")
        
        # The create_uur_report already creates a main unit with idx=0
        # Let's add additional failure info to the existing main unit
        from pyWATS.tdm.models import SubRepair
        if uur_report.sub_units:
            # Get the existing main unit (should be at idx=0) 
            main_unit = uur_report.sub_units[0]
            if isinstance(main_unit, SubRepair) and valid_category and valid_code:
                main_unit.add_failure(
                    category=valid_category,  # Use actual system category
                    code=valid_code,          # Use actual system code
                    comment="Main unit analysis completed",
                    com_ref="MAIN"
                )
        
        # Add a sub-component repair with proper parent relationship
        sub_repair = uur_report.add_sub_repair(
            part_type="PCBA",
            sn=f"PCBA_SN_{timestamp}",
            pn="PCBA_PART_001",
            rev="Rev_A", 
            idx=1,        # Sub-component gets unique idx
            parent_idx=0  # References the main unit (idx=0) as parent
        )
        
        # Add failure information to sub-component (use actual system values)
        if valid_category and valid_code:
            sub_repair.add_failure(
                category=valid_category,  # Use actual system category
                code=valid_code,          # Use actual system code
                comment="Capacitor C15 failed - replaced",
                com_ref="C15"
            )
            
            sub_repair.add_failure(
                category=valid_category,  # Use same valid category for consistency
                code=valid_code,          # Use same valid code for consistency
                comment="Short circuit detected and repaired",
                com_ref="R22"
            )
        
        print(f"    ✅ Created UUR: {uur_report.id}")
        print(f"    ✅ Serial: {uur_report.sn}")
        
        # Count total failures across all sub-repair units
        from pyWATS.tdm.models import SubRepair
        total_failures = 0
        for unit in uur_report.sub_units:
            if isinstance(unit, SubRepair) and unit.failures:
                total_failures += len(unit.failures)
        print(f"    ✅ Added {len(uur_report.sub_units)} repair units with {total_failures} total failures")
        
        # Submit UUR  
        print("[4] Submitting UUR report...")
        
        success = client.submit_report(uur_report, SubmitMethod.Automatic)
        
        if not success:
            print(f"❌ Submission failed")
            return False
            
        print(f"    ✅ UUR submitted successfully")
        print(f"    ✅ Report ID: {uur_report.id}")
        
        # Load UUR
        print("[5] Loading UUR report...")
        time.sleep(5)  # Wait for processing
        
        if not client._connection or not client._connection._client:
            print(f"❌ No connection available")
            return False
        
        url = f"/api/Report/Wsjf/{uur_report.id}"
        response = client._connection._client.get(url)
        
        if response.status_code != 200:
            print(f"❌ Load failed: HTTP {response.status_code}")
            return False
            
        if not response.text.strip():
            print(f"❌ Empty response")
            return False
            
        try:
            loaded_data = response.json()
            loaded_uur = UURReport.model_validate(loaded_data)
            
            print(f"    ✅ UUR loaded successfully")
            print(f"    ✅ Loaded ID: {loaded_uur.id}")
            print(f"    ✅ Loaded SN: {loaded_uur.sn}")
            print(f"    ✅ Loaded Type: {loaded_uur.type}")
            print(f"    ✅ Sub repairs: {len(loaded_uur.sub_units)}")
            
            # Verify repair data
            if loaded_uur.sub_units:
                sub_unit = loaded_uur.sub_units[0]
                # Check if it's a SubRepair (has failures attribute)
                from pyWATS.tdm.models import SubRepair
                if isinstance(sub_unit, SubRepair) and sub_unit.failures:
                    print(f"    ✅ Failures loaded: {len(sub_unit.failures)}")
                    for failure in sub_unit.failures:
                        print(f"      - {failure.category}: {failure.comment}")
                else:
                    print(f"    ℹ Sub unit type: {type(sub_unit).__name__}")
            
            print(f"    ✅ UUR round-trip successful!")
            
            return True
            
        except Exception as e:
            print(f"❌ Deserialization failed: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_load_fat_report():
    """Test 3: Load known FAT report."""
    print_header("TEST 3: Load FAT Report")
    
    try:
        from pyWATS.tdm_client import TDMClient, APIStatusType
        from pyWATS.tdm.models import UUTReport
        
        # Setup client
        print("[1] Setting up test client...")
        client = TDMClient()
        client.setup_api(data_dir="./test_data", location="Test Lab", purpose="Testing")
        client.station_name = "Test_Station"
        
        client.register_client(base_url=TEST_BASE_URL, token=TEST_AUTH_TOKEN)
        client.initialize_api()
        
        if client.status != APIStatusType.Online:
            print(f"❌ Client not online: {client.status}")
            return False
            
        print("    ✅ Client setup successful")
        
        # Load FAT report
        print(f"[2] Loading FAT report: {KNOWN_FAT_REPORT_ID}")
        
        if not client._connection or not client._connection._client:
            print(f"❌ No connection available")
            return False
        
        url = f"/api/Report/Wsjf/{KNOWN_FAT_REPORT_ID}"
        response = client._connection._client.get(url)
        
        if response.status_code != 200:
            print(f"❌ Load failed: HTTP {response.status_code}")
            print(f"    Response: {response.text[:100]}...")
            return False
            
        if not response.text.strip():
            print(f"❌ Empty response")
            return False
            
        print(f"    ✅ FAT report loaded from server")
        
        try:
            loaded_data = response.json()
            print(f"    ✅ JSON parsed successfully")
            print(f"    ✅ Response size: {len(loaded_data)} fields")
            print(f"    ✅ Report type: {loaded_data.get('type', 'Unknown')}")
            print(f"    ✅ Process code: {loaded_data.get('processCode', 'Unknown')}")
            
            # Attempt deserialization
            print("[3] Attempting deserialization...")
            fat_uut = UUTReport.model_validate(loaded_data)
            
            print(f"    🎉 FAT report deserialized successfully!")
            print(f"    ✅ ID: {fat_uut.id}")
            print(f"    ✅ Type: {fat_uut.type}")
            print(f"    ✅ Process Code: {fat_uut.process_code}")
            print(f"    ✅ Result: {fat_uut.result}")
            
            return True
            
        except Exception as e:
            print(f"❌ Deserialization failed: {e}")
            print(f"    This is expected - helps identify model gaps")
            
            # Show some details to help debug
            try:
                loaded_data = response.json()
                print(f"    Available fields: {list(loaded_data.keys())}")
                print(f"    First 3 fields: {dict(list(loaded_data.items())[:3])}")
            except:
                pass
                
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all UUT tests."""
    print_header("UUT REPORT TESTING SUITE")
    print(f"Started at: {datetime.now()}")
    
    results = []
    
    # Test 1: Simple UUT workflow
    result1 = test_simple_uut_workflow()
    results.append(("Simple UUT Workflow", result1))
    
    # Test 2: Simple UUR workflow
    result2 = test_simple_uur_workflow()
    results.append(("Simple UUR Workflow", result2))
    
    # Test 3: FAT report
    result3 = test_load_fat_report()
    results.append(("Load FAT Report", result3))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Tests Run: {total}")
    print(f"Passed: {passed} ✅")
    print(f"Failed: {total - passed} ❌")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    print(f"\nResults:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")


if __name__ == "__main__":
    run_all_tests()