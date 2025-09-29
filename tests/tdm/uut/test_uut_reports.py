"""
UUT Report Testing Suite

Comprehensive tests for UUT report functionality including creation, submission,
loading, deserialization, and the complete WSJF step hierarchy.

Tests the new C# Interface.TDM pattern: UUT creates sequence, sequence creates steps, steps create measurements.
"""

import sys
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional
import pytest

# Add src to path for importing pyWATS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from pyWATS.tdm.models import (
    UUTReport, MiscInfo, SequenceCall, NumericLimitStep, PassFailStep, StringValueStep,
    NumericMeasurement, BooleanMeasurement, StringMeasurement,
    StepStatusType, CompOperatorType, StepTypeEnum
)
from pyWATS.rest_api.endpoints.report import submit_wsjf_report
from test_utils import (
    TestOperationResult, setup_test_client, wait_and_retry_load, 
    cleanup_test_client, print_test_header, print_test_result
)
from ..test_config import (
    DEFAULT_TEST_OPERATION_CODE, KNOWN_FAT_REPORT_ID
)


class UUTTestRunner:
    """Test runner for UUT report scenarios."""
    
    def __init__(self):
        self.client = None
        self.results = []
        
    def run_all_tests(self):
        """Run all UUT test scenarios."""
        print_test_header("UUT REPORT TESTING SUITE")
        print(f"Starting UUT tests at {datetime.now()}")
        
        # Setup
        setup_result = self._setup()
        if not setup_result.success:
            print_test_result(setup_result)
            return
            
        try:
            # Test scenarios
            self._test_simple_uut_workflow()
            self._test_load_fat_report()
            
            # New WSJF step hierarchy tests
            self._test_complete_step_hierarchy()
            self._test_numeric_limit_steps()
            self._test_pass_fail_steps()
            self._test_string_value_steps()
            self._test_nested_sequence_calls()
            self._test_measurement_validations()
            self._test_step_creation_patterns()
            
        finally:
            # Cleanup
            cleanup_result = self._cleanup()
            self.results.append(cleanup_result)
            
        # Summary
        self._print_summary()
        
    def _setup(self) -> TestOperationResult:
        """Setup test environment."""
        print_test_header("Test Setup")
        
        self.client, result = setup_test_client()
        self.results.append(result)
        print_test_result(result)
        
        return result
        
    def _cleanup(self) -> TestOperationResult:
        """Cleanup test environment."""
        print_test_header("Test Cleanup")
        
        result = cleanup_test_client(self.client)
        print_test_result(result)
        
        return result
        
    def _test_simple_uut_workflow(self):
        """Test 1: Simple UUT workflow - Create → Submit → Load."""
        print_test_header("Test 1: Simple UUT Workflow")
        
        if not self.client:
            result = TestOperationResult(False, "No client available")
            self.results.append(result)
            print_test_result(result)
            return
            
        try:
            # Step 1: Create UUT report
            print("[1] Creating UUT report...")
            uut_report = self._create_test_uut_report()
            
            if not uut_report:
                result = TestOperationResult(False, "Failed to create UUT report")
                self.results.append(result)
                print_test_result(result)
                return
                
            print(f"    ✓ Created UUT: {uut_report.id}")
            print(f"    ✓ Serial: {uut_report.sn}")
            print(f"    ✓ Process Code: {uut_report.process_code}")
            
            # Step 2: Submit UUT report
            print("[2] Submitting UUT report...")
            submit_result = self._submit_uut_report(uut_report)
            self.results.append(submit_result)
            print_test_result(submit_result)
            
            if not submit_result.success:
                return
                
            # Step 3: Load UUT report
            print("[3] Loading submitted UUT report...")
            load_result = self._load_and_validate_uut(str(uut_report.id))
            self.results.append(load_result)
            print_test_result(load_result)
            
        except Exception as e:
            result = TestOperationResult(False, f"Test workflow failed: {e}")
            self.results.append(result)
            print_test_result(result)
            
    def _test_load_fat_report(self):
        """Test 2: Load known FAT report from server."""
        print_test_header("Test 2: Load FAT Report")
        
        if not self.client:
            result = TestOperationResult(False, "No client available")
            self.results.append(result)
            print_test_result(result)
            return
            
        try:
            print(f"[1] Loading known FAT report: {KNOWN_FAT_REPORT_ID}")
            
            # Attempt to load the known report
            report_data, load_result = wait_and_retry_load(self.client, KNOWN_FAT_REPORT_ID)
            
            if not load_result.success:
                # Expected to potentially fail - this is a stress test for our models
                result = TestOperationResult(
                    False, 
                    f"Could not load FAT report (expected): {load_result.message}",
                    {"report_id": KNOWN_FAT_REPORT_ID, "expected_failure": True}
                )
                self.results.append(result)
                print_test_result(result)
                return
            
            if report_data is None:
                result = TestOperationResult(False, "Report data is None")
                self.results.append(result)
                print_test_result(result)
                return
                
            print(f"    ✓ Successfully loaded report data")
            print(f"    ✓ Response size: {len(str(report_data))} chars")
            print(f"    ✓ Response keys: {list(report_data.keys())}")
            
            # Attempt deserialization
            print("[2] Attempting deserialization...")
            deserialize_result = self._deserialize_fat_report(report_data)
            self.results.append(deserialize_result)
            print_test_result(deserialize_result)
            
        except Exception as e:
            result = TestOperationResult(False, f"FAT test failed: {e}")
            self.results.append(result)
            print_test_result(result)
            
    def _create_test_uut_report(self) -> Optional[UUTReport]:
        """Create a test UUT report with new step hierarchy."""
        try:
            if self.client is None:
                print("    ❌ No client available")
                return None
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create UUT report with new structure
            uut_report = UUTReport(
                id=uuid4(),
                type="T",
                pn="TEST_PART_001",
                sn=f"TEST_SN_{timestamp}",
                rev="Rev_Test",
                process_code=DEFAULT_TEST_OPERATION_CODE,
                result="F",  # Failed - for testing workflow
                station_name=self.client.station_name,
                location=self.client.location,
                purpose=self.client.purpose,
                start=datetime.now(timezone.utc)
            )
            
            # Add some test misc info using proper MiscInfo objects
            uut_report.misc_infos = [
                MiscInfo(description="TestType", text="Automated Test"),
                MiscInfo(description="TestRunner", text="UUTTestRunner"),
                MiscInfo(description="Timestamp", text=timestamp)
            ]
            
            # Create complete step hierarchy for testing
            print("    ✓ Creating root sequence call with step hierarchy...")
            root = uut_report.get_root_Sequence_call()
            
            # Add a numeric limit step with measurement
            voltage_step = root.add_numeric_limit_step("Voltage Test")
            voltage_step.add_test(3.3, CompOperatorType.GELE, 3.0, 3.6, "V")
            print(f"    ✓ Added voltage test: {voltage_step.measurements[0].numeric_value}V")
            
            # Add a pass/fail step with measurement  
            connection_step = root.add_pass_fail_step("Connection Test")
            connection_step.add_test(False)  # Failed connection for testing
            print(f"    ✓ Added connection test: {connection_step.measurements[0].boolean_value}")
            
            # Add a string value step with measurement
            serial_step = root.add_string_value_step("Serial Number Check")
            serial_step.add_test(f"TEST_SN_{timestamp}")
            print(f"    ✓ Added serial check: {serial_step.measurements[0].string_value}")
            
            print(f"    ✓ Created complete UUT hierarchy with {len(root.steps)} steps")
            
            return uut_report
            
        except Exception as e:
            print(f"    ❌ Error creating UUT report: {e}")
            return None
            
    def _submit_uut_report(self, uut_report: UUTReport) -> TestOperationResult:
        """Submit UUT report to server."""
        try:
            if self.client is None or not hasattr(self.client, '_connection') or self.client._connection is None:
                return TestOperationResult(False, "No client connection available")
            
            # Use the TDM client's submission functionality
            from pyWATS.rest_api.endpoints.report import submit_wsjf_report
            
            # Serialize the report
            report_data = uut_report.model_dump(by_alias=True, mode='json')
            
            # Submit via the client's connection
            result = submit_wsjf_report(report_data, client=self.client._connection._client)
            
            if result.success:
                return TestOperationResult(
                    True, 
                    f"UUT submitted successfully",
                    {"report_id": str(result.report_id), "message": result.message}
                )
            else:
                return TestOperationResult(False, f"Submission failed: {result.message}")
                
        except Exception as e:
            return TestOperationResult(False, f"Submission error: {e}")
            
    def _load_and_validate_uut(self, report_id: str) -> TestOperationResult:
        """Load and validate UUT report from server."""
        try:
            if self.client is None:
                return TestOperationResult(False, "No client available")
                
            # Load the report
            report_data, load_result = wait_and_retry_load(self.client, report_id)
            
            if not load_result.success:
                return TestOperationResult(False, f"Load failed: {load_result.message}")
            
            if report_data is None:
                return TestOperationResult(False, "Report data is None")
                
            # Attempt deserialization
            try:
                loaded_uut = UUTReport.model_validate(report_data)
                
                # Basic validation
                validation_checks = [
                    (str(loaded_uut.id) == report_id, "ID matches"),
                    (loaded_uut.type == "T", "Type is T"),
                    (loaded_uut.process_code == DEFAULT_TEST_OPERATION_CODE, "Process code matches"),
                    (loaded_uut.sn.startswith("TEST_SN_"), "Serial number format correct")
                ]
                
                failed_checks = [check[1] for check in validation_checks if not check[0]]
                
                if failed_checks:
                    return TestOperationResult(
                        False, 
                        f"Validation failed: {', '.join(failed_checks)}",
                        {"loaded_fields": len(report_data), "failed_validations": failed_checks}
                    )
                else:
                    return TestOperationResult(
                        True, 
                        "UUT loaded and validated successfully",
                        {
                            "loaded_fields": len(report_data), 
                            "validation_checks": len(validation_checks),
                            "serial_number": loaded_uut.sn,
                            "process_code": loaded_uut.process_code
                        }
                    )
                    
            except Exception as deserialize_error:
                return TestOperationResult(False, f"Deserialization failed: {deserialize_error}")
                
        except Exception as e:
            return TestOperationResult(False, f"Load and validate error: {e}")
            
    def _deserialize_fat_report(self, report_data: dict) -> TestOperationResult:
        """Attempt to deserialize FAT report data."""
        try:
            # This is expected to potentially fail as the FAT report might have 
            # fields or structures not yet supported by our model
            
            print(f"    Report data overview:")
            print(f"      Type: {report_data.get('type', 'Unknown')}")
            print(f"      ID: {report_data.get('id', 'Unknown')}")
            print(f"      Process Code: {report_data.get('processCode', 'Unknown')}")
            print(f"      Result: {report_data.get('result', 'Unknown')}")
            print(f"      Total fields: {len(report_data)}")
            
            # Attempt deserialization
            fat_uut = UUTReport.model_validate(report_data)
            
            return TestOperationResult(
                True, 
                "FAT report deserialized successfully! 🎉",
                {
                    "report_id": str(fat_uut.id),
                    "process_code": fat_uut.process_code,
                    "result": fat_uut.result,
                    "serial_number": fat_uut.sn,
                    "total_fields": len(report_data)
                }
            )
            
        except Exception as e:
            # This is somewhat expected - FAT reports may have complex structures
            return TestOperationResult(
                False, 
                f"FAT deserialization failed (expected): {e}",
                {
                    "error_type": type(e).__name__,
                    "available_fields": list(report_data.keys())[:10],  # First 10 fields
                    "total_fields": len(report_data),
                    "note": "This failure helps identify missing model fields"
                }
            )
            
    def _test_complete_step_hierarchy(self):
        """Test 3: Complete WSJF step hierarchy creation and validation."""
        print_test_header("Test 3: Complete WSJF Step Hierarchy")
        
        try:
            print("[1] Creating UUT with complete step hierarchy...")
            uut = self._create_test_uut_with_hierarchy()
            
            if not uut:
                result = TestOperationResult(False, "Failed to create UUT with step hierarchy")
                self.results.append(result)
                print_test_result(result)
                return
                
            root = uut.get_root_Sequence_call()
            print(f"    ✓ Root sequence created: {root.name}")
            print(f"    ✓ Root has {len(root.steps)} child steps")
            
            # Validate step hierarchy
            validation_checks = [
                (root.step_type == StepTypeEnum.SEQUENCE_CALL, "Root is sequence call"),
                (len(root.steps) >= 3, "Root has multiple child steps"),
                (any(isinstance(step, NumericLimitStep) for step in root.steps), "Has numeric step"),
                (any(isinstance(step, PassFailStep) for step in root.steps), "Has pass/fail step"),
                (any(isinstance(step, StringValueStep) for step in root.steps), "Has string step"),
            ]
            
            failed_checks = [check[1] for check in validation_checks if not check[0]]
            
            if failed_checks:
                result = TestOperationResult(
                    False, 
                    f"Hierarchy validation failed: {', '.join(failed_checks)}"
                )
            else:
                result = TestOperationResult(
                    True,
                    "Complete step hierarchy created and validated successfully",
                    {
                        "root_steps": len(root.steps),
                        "step_types": [type(step).__name__ for step in root.steps]
                    }
                )
            
            self.results.append(result)
            print_test_result(result)
            
        except Exception as e:
            result = TestOperationResult(False, f"Step hierarchy test failed: {e}")
            self.results.append(result)
            print_test_result(result)
    
    def _test_numeric_limit_steps(self):
        """Test 4: Numeric limit steps with single and multiple measurements."""
        print_test_header("Test 4: Numeric Limit Steps")
        
        try:
            print("[1] Testing single numeric measurement...")
            uut = self._create_basic_uut()
            root = uut.get_root_Sequence_call()
            
            # Test single numeric step
            numeric_step = root.add_numeric_limit_step("Voltage Test")
            measurement = numeric_step.add_test(
                value=3.3,
                comp_operator=CompOperatorType.GELE,
                low_limit=3.0,
                high_limit=3.6,
                unit="V"
            )
            
            single_checks = [
                (numeric_step.is_single, "Step is single mode"),
                (not numeric_step.is_multiple, "Step is not multiple mode"),
                (len(numeric_step.measurements) == 1, "Has one measurement"),
                (measurement.numeric_value == 3.3, "Correct measurement value"),
                (measurement.comp_operator == CompOperatorType.GELE, "Correct operator"),
                (measurement.unit == "V", "Correct unit")
            ]
            
            print("[2] Testing multiple numeric measurements...")
            multi_step = root.add_numeric_limit_step("Multi Voltage Test")
            
            # Add multiple measurements
            m1 = multi_step.add_multiple_test("VCC", 5.0, CompOperatorType.GELE, 4.8, 5.2, "V")
            m2 = multi_step.add_multiple_test("GND", 0.0, CompOperatorType.EQ, 0.0, 0.0, "V") 
            
            multi_checks = [
                (multi_step.is_multiple, "Step is multiple mode"),
                (not multi_step.is_single, "Step is not single mode"),
                (len(multi_step.measurements) == 2, "Has two measurements"),
                (multi_step.step_type == StepTypeEnum.ET_MNLT, "Correct step type for multiple"),
                (m1.measure_name == "VCC", "First measurement name correct"),
                (m2.measure_name == "GND", "Second measurement name correct")
            ]
            
            print("[3] Testing error conditions...")
            error_checks = []
            
            # Test adding single to multiple - should fail
            try:
                multi_step.add_test(1.0)
                error_checks.append((False, "Should not allow single test on multiple step"))
            except ValueError:
                error_checks.append((True, "Correctly prevents single test on multiple step"))
            
            # Test adding multiple single tests - should fail
            try:
                single_step = root.add_numeric_limit_step("Single Test")
                single_step.add_test(1.0)
                single_step.add_test(2.0)  # This should fail
                error_checks.append((False, "Should not allow multiple single tests"))
            except ValueError:
                error_checks.append((True, "Correctly prevents multiple single tests"))
            
            all_checks = single_checks + multi_checks + error_checks
            failed_checks = [check[1] for check in all_checks if not check[0]]
            
            if failed_checks:
                result = TestOperationResult(
                    False,
                    f"Numeric step validation failed: {', '.join(failed_checks)}"
                )
            else:
                result = TestOperationResult(
                    True,
                    "Numeric limit steps validated successfully",
                    {
                        "single_measurements": len(numeric_step.measurements),
                        "multiple_measurements": len(multi_step.measurements),
                        "validations_passed": len(all_checks)
                    }
                )
            
            self.results.append(result)
            print_test_result(result)
            
        except Exception as e:
            result = TestOperationResult(False, f"Numeric step test failed: {e}")
            self.results.append(result)
            print_test_result(result)
    
    def _test_pass_fail_steps(self):
        """Test 5: Pass/Fail steps with boolean measurements."""
        print_test_header("Test 5: Pass/Fail Steps")
        
        try:
            uut = self._create_basic_uut()
            root = uut.get_root_Sequence_call()
            
            print("[1] Testing single pass/fail measurement...")
            pf_step = root.add_pass_fail_step("Connection Test")
            bool_measurement = pf_step.add_test(True)
            
            print("[2] Testing multiple pass/fail measurements...")
            multi_pf_step = root.add_pass_fail_step("Multi Connection Test")
            m1 = multi_pf_step.add_multiple_test("Pin1", True)
            m2 = multi_pf_step.add_multiple_test("Pin2", False)
            
            validation_checks = [
                (pf_step.is_single, "Single step is single mode"),
                (bool_measurement.boolean_value == True, "Correct boolean value"),
                (multi_pf_step.is_multiple, "Multiple step is multiple mode"),
                (multi_pf_step.step_type == StepTypeEnum.ET_MPFT, "Correct multiple step type"),
                (len(multi_pf_step.measurements) == 2, "Has two boolean measurements"),
                (m1.measure_name == "Pin1", "First measurement name correct"),
                (m2.boolean_value == False, "Second measurement value correct")
            ]
            
            failed_checks = [check[1] for check in validation_checks if not check[0]]
            
            if failed_checks:
                result = TestOperationResult(
                    False,
                    f"Pass/Fail step validation failed: {', '.join(failed_checks)}"
                )
            else:
                result = TestOperationResult(
                    True,
                    "Pass/Fail steps validated successfully",
                    {
                        "single_measurements": len(pf_step.measurements),
                        "multiple_measurements": len(multi_pf_step.measurements)
                    }
                )
            
            self.results.append(result)
            print_test_result(result)
            
        except Exception as e:
            result = TestOperationResult(False, f"Pass/Fail step test failed: {e}")
            self.results.append(result)
            print_test_result(result)
    
    def _test_string_value_steps(self):
        """Test 6: String value steps with string measurements."""
        print_test_header("Test 6: String Value Steps")
        
        try:
            uut = self._create_basic_uut()
            root = uut.get_root_Sequence_call()
            
            print("[1] Testing single string measurement...")
            str_step = root.add_string_value_step("Serial Check")
            str_measurement = str_step.add_test("TEST_SN_12345")
            
            print("[2] Testing multiple string measurements...")
            multi_str_step = root.add_string_value_step("Multi String Test")
            m1 = multi_str_step.add_multiple_test("SerialNumber", "SN123")
            m2 = multi_str_step.add_multiple_test("PartNumber", "PN456")
            
            validation_checks = [
                (str_step.step_type == StepTypeEnum.ET_SVT, "Correct single step type"),
                (str_measurement.string_value == "TEST_SN_12345", "Correct string value"),
                (multi_str_step.step_type == StepTypeEnum.ET_MSVT, "Correct multiple step type"),
                (len(multi_str_step.measurements) == 2, "Has two string measurements"),
                (m1.measure_name == "SerialNumber", "First measurement name correct"),
                (m2.string_value == "PN456", "Second measurement value correct")
            ]
            
            failed_checks = [check[1] for check in validation_checks if not check[0]]
            
            if failed_checks:
                result = TestOperationResult(
                    False,
                    f"String step validation failed: {', '.join(failed_checks)}"
                )
            else:
                result = TestOperationResult(
                    True,
                    "String value steps validated successfully",
                    {
                        "single_measurements": len(str_step.measurements),
                        "multiple_measurements": len(multi_str_step.measurements)
                    }
                )
            
            self.results.append(result)
            print_test_result(result)
            
        except Exception as e:
            result = TestOperationResult(False, f"String step test failed: {e}")
            self.results.append(result)
            print_test_result(result)
    
    def _test_nested_sequence_calls(self):
        """Test 7: Nested sequence calls with proper hierarchy."""
        print_test_header("Test 7: Nested Sequence Calls")
        
        try:
            uut = self._create_basic_uut()
            root = uut.get_root_Sequence_call()
            
            print("[1] Creating nested sequence...")
            nested_seq = root.add_sequence_call("SubSequence", "SubSeq", "2.0")
            
            print("[2] Adding steps to nested sequence...")
            nested_numeric = nested_seq.add_numeric_limit_step("Nested Voltage")
            nested_measurement = nested_numeric.add_test(1.8, CompOperatorType.GELE, 1.6, 2.0, "V")
            
            nested_pf = nested_seq.add_pass_fail_step("Nested Connection")
            nested_bool = nested_pf.add_test(True)
            
            print("[3] Creating deeply nested sequence...")
            deep_nested = nested_seq.add_sequence_call("DeepNested", "DeepSeq", "3.0")
            deep_step = deep_nested.add_string_value_step("Deep String")
            deep_measurement = deep_step.add_test("DEEP_TEST")
            
            validation_checks = [
                (nested_seq.sequence_name == "SubSeq", "Nested sequence name correct"),
                (nested_seq.parent_step_id == root.step_id, "Nested sequence has correct parent"),
                (len(nested_seq.steps) == 3, "Nested sequence has 3 child steps"),  # 2 steps + 1 deep nested
                (nested_numeric.parent_step_id == nested_seq.step_id, "Nested step has correct parent"),
                (deep_nested.parent_step_id == nested_seq.step_id, "Deep nested has correct parent"),
                (len(deep_nested.steps) == 1, "Deep nested has 1 step"),
                (deep_measurement.string_value == "DEEP_TEST", "Deep measurement value correct")
            ]
            
            failed_checks = [check[1] for check in validation_checks if not check[0]]
            
            if failed_checks:
                result = TestOperationResult(
                    False,
                    f"Nested sequence validation failed: {', '.join(failed_checks)}"
                )
            else:
                result = TestOperationResult(
                    True,
                    "Nested sequence calls validated successfully",
                    {
                        "root_steps": len(root.steps),
                        "nested_steps": len(nested_seq.steps),
                        "deep_nested_steps": len(deep_nested.steps),
                        "total_hierarchy_depth": 3
                    }
                )
            
            self.results.append(result)
            print_test_result(result)
            
        except Exception as e:
            result = TestOperationResult(False, f"Nested sequence test failed: {e}")
            self.results.append(result)
            print_test_result(result)
    
    def _test_measurement_validations(self):
        """Test 8: Measurement validation and comparison operators."""
        print_test_header("Test 8: Measurement Validations")
        
        try:
            uut = self._create_basic_uut()
            root = uut.get_root_Sequence_call()
            
            print("[1] Testing all comparison operators...")
            operators_step = root.add_numeric_limit_step("Operator Tests")
            
            # Test different operators (as multiple measurements)
            operators = [
                ("EQ_Test", 5.0, CompOperatorType.EQ, 5.0, None),
                ("NE_Test", 5.0, CompOperatorType.NE, 3.0, None),
                ("GT_Test", 5.0, CompOperatorType.GT, 3.0, None),
                ("GE_Test", 5.0, CompOperatorType.GE, 5.0, None),
                ("LT_Test", 3.0, CompOperatorType.LT, 5.0, None),
                ("LE_Test", 5.0, CompOperatorType.LE, 5.0, None),
                ("GELE_Test", 4.0, CompOperatorType.GELE, 3.0, 5.0),
                ("GTLT_Test", 4.0, CompOperatorType.GTLT, 3.0, 5.0)
            ]
            
            measurements = []
            for name, value, op, low, high in operators:
                m = operators_step.add_multiple_test(name, value, op, low, high, "V")
                measurements.append(m)
            
            print("[2] Testing measurement properties...")
            validation_checks = [
                (len(measurements) == len(operators), "All operator measurements created"),
                (all(m.comp_operator == op[2] for m, op in zip(measurements, operators)), "All operators set correctly"),
                (measurements[0].comp_operator == CompOperatorType.EQ, "EQ operator correct"),
                (measurements[6].low_limit == 3.0 and measurements[6].high_limit == 5.0, "GELE limits correct"),
                (all(m.unit == "V" for m in measurements), "All units set correctly"),
                (all(m.status == StepStatusType.PASSED for m in measurements), "All statuses default to PASSED")
            ]
            
            print("[3] Testing measurement indexing...")
            index_checks = [
                (measurements[0].measure_index == 0, "First measurement index is 0"),
                (measurements[1].measure_index == 1, "Second measurement index is 1"),
                (measurements[-1].measure_index == len(measurements) - 1, "Last measurement index correct")
            ]
            
            all_checks = validation_checks + index_checks
            failed_checks = [check[1] for check in all_checks if not check[0]]
            
            if failed_checks:
                result = TestOperationResult(
                    False,
                    f"Measurement validation failed: {', '.join(failed_checks)}"
                )
            else:
                result = TestOperationResult(
                    True,
                    "Measurement validations passed successfully",
                    {
                        "operators_tested": len(operators),
                        "measurements_created": len(measurements),
                        "validations_passed": len(all_checks)
                    }
                )
            
            self.results.append(result)
            print_test_result(result)
            
        except Exception as e:
            result = TestOperationResult(False, f"Measurement validation test failed: {e}")
            self.results.append(result)
            print_test_result(result)
    
    def _test_step_creation_patterns(self):
        """Test 9: Step creation patterns matching C# Interface.TDM."""
        print_test_header("Test 9: Step Creation Patterns")
        
        try:
            print("[1] Testing C# pattern: UUT creates sequence...")
            uut = self._create_basic_uut()
            root = uut.get_root_Sequence_call()
            
            print("[2] Testing pattern: Sequence creates steps...")
            voltage_step = root.add_numeric_limit_step("Voltage Test")
            connection_step = root.add_pass_fail_step("Connection Test") 
            serial_step = root.add_string_value_step("Serial Check")
            sub_sequence = root.add_sequence_call("SubTest", "SubSequence", "1.0")
            
            print("[3] Testing pattern: Steps create measurements...")
            v_measurement = voltage_step.add_test(3.3, CompOperatorType.GELE, 3.0, 3.6, "V")
            c_measurement = connection_step.add_test(True)
            s_measurement = serial_step.add_test("TEST_SERIAL")
            
            print("[4] Testing step ordering and indexing...")
            step_indexing_checks = [
                (root.step_index == 0, "Root step index is 0"),
                (voltage_step.step_index == 0, "First child step index is 0"),
                (connection_step.step_index == 1, "Second child step index is 1"),
                (serial_step.step_index == 2, "Third child step index is 2"),
                (sub_sequence.step_index == 3, "Fourth child step index is 3"),
                (all(step.parent_step_id == root.step_id for step in root.steps), "All steps have correct parent")
            ]
            
            print("[5] Testing step ID assignment...")
            step_id_checks = [
                (root.step_id == 1, "Root step ID is 1"),
                (voltage_step.step_id == 2, "First child step ID is 2"),
                (connection_step.step_id == 3, "Second child step ID is 3"),
                (serial_step.step_id == 4, "Third child step ID is 4"),
                (sub_sequence.step_id == 5, "Fourth child step ID is 5")
            ]
            
            print("[6] Testing measurement properties...")
            measurement_checks = [
                (v_measurement.measure_index == 0, "Voltage measurement index is 0"),
                (c_measurement.measure_index == 0, "Connection measurement index is 0"),
                (s_measurement.measure_index == 0, "Serial measurement index is 0"),
                (v_measurement.numeric_value == 3.3, "Voltage value correct"),
                (c_measurement.boolean_value == True, "Connection value correct"),
                (s_measurement.string_value == "TEST_SERIAL", "Serial value correct")
            ]
            
            all_checks = step_indexing_checks + step_id_checks + measurement_checks
            failed_checks = [check[1] for check in all_checks if not check[0]]
            
            if failed_checks:
                result = TestOperationResult(
                    False,
                    f"Step creation pattern validation failed: {', '.join(failed_checks)}"
                )
            else:
                result = TestOperationResult(
                    True,
                    "C# Interface.TDM step creation patterns validated successfully",
                    {
                        "uut_sequences": 1,
                        "sequence_steps": len(root.steps),
                        "step_measurements": sum(len(getattr(step, 'measurements', [])) for step in root.steps if hasattr(step, 'measurements')),
                        "pattern_validations": len(all_checks)
                    }
                )
            
            self.results.append(result)
            print_test_result(result)
            
        except Exception as e:
            result = TestOperationResult(False, f"Step creation pattern test failed: {e}")
            self.results.append(result)
            print_test_result(result)
    
    def _create_basic_uut(self) -> UUTReport:
        """Create a basic UUT report for testing."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return UUTReport(
            pn="TEST_PART_001",
            sn=f"TEST_SN_{timestamp}",
            rev="Rev_Test",
            process_code=DEFAULT_TEST_OPERATION_CODE,
            result="P",  # Passed for testing
            station_name="TestStation",
            location="TestLab", 
            purpose="Automated Testing"
        )
    
    def _create_test_uut_with_hierarchy(self) -> Optional[UUTReport]:
        """Create a test UUT report with complete step hierarchy."""
        try:
            uut = self._create_basic_uut()
            
            # Create root sequence call
            root = uut.get_root_Sequence_call()
            
            # Add numeric limit step
            numeric_step = root.add_numeric_limit_step("Voltage Test")
            numeric_step.add_test(3.3, CompOperatorType.GELE, 3.0, 3.6, "V")
            
            # Add pass/fail step
            pf_step = root.add_pass_fail_step("Connection Test")
            pf_step.add_test(True)
            
            # Add string value step
            str_step = root.add_string_value_step("Serial Check")
            str_step.add_test("TEST_SN_12345")
            
            # Add nested sequence
            nested_seq = root.add_sequence_call("SubSequence", "SubSeq", "1.0")
            nested_numeric = nested_seq.add_numeric_limit_step("Current Test")
            nested_numeric.add_test(0.5, CompOperatorType.LE, None, 1.0, "A")
            
            return uut
            
        except Exception as e:
            print(f"    ❌ Error creating UUT with hierarchy: {e}")
            return None

    def _print_summary(self):
        """Print test summary."""
        print_test_header("TEST SUMMARY")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\nDetailed Results:")
        for i, result in enumerate(self.results, 1):
            print(f"  {i}. {result}")


# Pytest-style unit tests for individual components
class TestWSJFStepHierarchy:
    """Unit tests for WSJF step hierarchy components."""
    
    def test_uut_report_creation(self):
        """Test basic UUT report creation."""
        uut = UUTReport(
            pn="TEST_PART",
            sn="TEST_SN_001",
            rev="Rev_1.0",
            process_code=1000,
            station_name="TestStation",
            location="Lab",
            purpose="Testing"
        )
        
        assert uut.type == "T"
        assert uut.sn == "TEST_SN_001"
        assert uut.process_code == 1000
        
    def test_root_sequence_creation(self):
        """Test root sequence call creation."""
        uut = UUTReport(
            pn="TEST_PART", sn="TEST_SN", rev="Rev_1.0",
            process_code=1000, station_name="Test", location="Lab", purpose="Test"
        )
        
        root = uut.get_root_Sequence_call()
        
        assert root is not None
        assert root.sequence_name == "MainSequence"
        assert root.sequence_version == "1.0"
        assert root.step_type == StepTypeEnum.SEQUENCE_CALL
        assert root.step_id == 1  # First step gets ID 1
        
    def test_numeric_limit_step(self):
        """Test numeric limit step creation and measurements."""
        uut = UUTReport(
            pn="TEST_PART", sn="TEST_SN", rev="Rev_1.0",
            process_code=1000, station_name="Test", location="Lab", purpose="Test"
        )
        
        # Test single numeric measurement
        root = uut.get_root_Sequence_call()
        numeric_step = root.add_numeric_limit_step("Voltage Test")
        measurement = numeric_step.add_test(3.3, CompOperatorType.GELE, 3.0, 3.6, "V")
        
        assert numeric_step.step_type == StepTypeEnum.ET_NLT
        assert numeric_step.is_single == True
        assert numeric_step.is_multiple == False
        assert len(numeric_step.measurements) == 1
        assert measurement.numeric_value == 3.3
        assert measurement.comp_operator == CompOperatorType.GELE
        assert measurement.low_limit == 3.0
        assert measurement.high_limit == 3.6
        assert measurement.unit == "V"
        
    def test_numeric_multiple_measurements(self):
        """Test multiple numeric measurements."""
        uut = UUTReport(
            pn="TEST_PART", sn="TEST_SN", rev="Rev_1.0",
            process_code=1000, station_name="Test", location="Lab", purpose="Test"
        )
        root = uut.get_root_Sequence_call()
        
        numeric_step = root.add_numeric_limit_step("Multi Voltage Test")
        m1 = numeric_step.add_multiple_test("VCC", 5.0, CompOperatorType.GELE, 4.8, 5.2, "V")
        m2 = numeric_step.add_multiple_test("VDD", 3.3, CompOperatorType.GELE, 3.0, 3.6, "V")
        
        assert numeric_step.step_type == StepTypeEnum.ET_MNLT
        assert numeric_step.is_multiple == True
        assert numeric_step.is_single == False
        assert len(numeric_step.measurements) == 2
        assert m1.measure_name == "VCC"
        assert m2.measure_name == "VDD"
        
    def test_pass_fail_step(self):
        """Test pass/fail step creation and measurements."""
        uut = UUTReport(
            pn="TEST_PART", sn="TEST_SN", rev="Rev_1.0",
            process_code=1000, station_name="Test", location="Lab", purpose="Test"
        )
        root = uut.get_root_Sequence_call()
        
        pf_step = root.add_pass_fail_step("Connection Test")
        measurement = pf_step.add_test(True)
        
        assert pf_step.step_type == StepTypeEnum.ET_PFT
        assert len(pf_step.measurements) == 1
        assert measurement.boolean_value == True
        
    def test_string_value_step(self):
        """Test string value step creation and measurements."""
        uut = UUTReport(
            pn="TEST_PART", sn="TEST_SN", rev="Rev_1.0",
            process_code=1000, station_name="Test", location="Lab", purpose="Test"
        )
        root = uut.get_root_Sequence_call()
        
        str_step = root.add_string_value_step("Serial Check")
        measurement = str_step.add_test("TEST_SERIAL_123")
        
        assert str_step.step_type == StepTypeEnum.ET_SVT
        assert len(str_step.measurements) == 1
        assert measurement.string_value == "TEST_SERIAL_123"
        
    def test_nested_sequences(self):
        """Test nested sequence calls."""
        uut = UUTReport(
            pn="TEST_PART", sn="TEST_SN", rev="Rev_1.0",
            process_code=1000, station_name="Test", location="Lab", purpose="Test"
        )
        root = uut.get_root_Sequence_call()
        
        nested = root.add_sequence_call("SubSequence", "SubSeq", "2.0")
        nested_step = nested.add_numeric_limit_step("Nested Voltage")
        nested_measurement = nested_step.add_test(1.8, CompOperatorType.GELE, 1.6, 2.0, "V")
        
        assert nested.sequence_name == "SubSeq"
        assert nested.parent_step_id == root.step_id
        assert len(nested.steps) == 1
        assert nested_step.parent_step_id == nested.step_id
        assert nested_measurement.numeric_value == 1.8
        
    def test_step_validation_errors(self):
        """Test step validation error conditions."""
        uut = UUTReport(
            pn="TEST_PART", sn="TEST_SN", rev="Rev_1.0",
            process_code=1000, station_name="Test", location="Lab", purpose="Test"
        )
        root = uut.get_root_Sequence_call()
        
        # Test cannot add single test to multiple step
        multi_step = root.add_numeric_limit_step("Multi Test")
        multi_step.add_multiple_test("Test1", 1.0)
        
        with pytest.raises(ValueError, match="Cannot add single test to multiple test step"):
            multi_step.add_test(2.0)
            
        # Test cannot add multiple single tests
        single_step = root.add_numeric_limit_step("Single Test")
        single_step.add_test(1.0)
        
        with pytest.raises(ValueError, match="Cannot add multiple single tests to single test step"):
            single_step.add_test(2.0)


def run_uut_tests():
    """Main entry point for UUT testing."""
    runner = UUTTestRunner()
    runner.run_all_tests()


def test_run_all_unit_tests():
    """Run all pytest unit tests."""
    pytest.main([__file__, "-v"])


if __name__ == "__main__":
    run_uut_tests()
