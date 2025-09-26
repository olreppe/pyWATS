"""
UUT Report Testing Suite

Automated tests for UUT report functionality including creation, submission, 
loading, and deserialization scenarios.
"""

import sys
import os
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional

# Add src to path for importing pyWATS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from pyWATS.rest_api.models.wsjf_reports import UUTReport, MiscInfo
from pyWATS.rest_api.endpoints.report import submit_wsjf_report
from .test_utils import (
    TestResult, setup_test_client, wait_and_retry_load, 
    cleanup_test_client, print_test_header, print_test_result
)
from .test_config import (
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
            
        finally:
            # Cleanup
            cleanup_result = self._cleanup()
            self.results.append(cleanup_result)
            
        # Summary
        self._print_summary()
        
    def _setup(self) -> TestResult:
        """Setup test environment."""
        print_test_header("Test Setup")
        
        self.client, result = setup_test_client()
        self.results.append(result)
        print_test_result(result)
        
        return result
        
    def _cleanup(self) -> TestResult:
        """Cleanup test environment."""
        print_test_header("Test Cleanup")
        
        result = cleanup_test_client(self.client)
        print_test_result(result)
        
        return result
        
    def _test_simple_uut_workflow(self):
        """Test 1: Simple UUT workflow - Create → Submit → Load."""
        print_test_header("Test 1: Simple UUT Workflow")
        
        if not self.client:
            result = TestResult(False, "No client available")
            self.results.append(result)
            print_test_result(result)
            return
            
        try:
            # Step 1: Create UUT report
            print("[1] Creating UUT report...")
            uut_report = self._create_test_uut_report()
            
            if not uut_report:
                result = TestResult(False, "Failed to create UUT report")
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
            result = TestResult(False, f"Test workflow failed: {e}")
            self.results.append(result)
            print_test_result(result)
            
    def _test_load_fat_report(self):
        """Test 2: Load known FAT report from server."""
        print_test_header("Test 2: Load FAT Report")
        
        if not self.client:
            result = TestResult(False, "No client available")
            self.results.append(result)
            print_test_result(result)
            return
            
        try:
            print(f"[1] Loading known FAT report: {KNOWN_FAT_REPORT_ID}")
            
            # Attempt to load the known report
            report_data, load_result = wait_and_retry_load(self.client, KNOWN_FAT_REPORT_ID)
            
            if not load_result.success:
                # Expected to potentially fail - this is a stress test for our models
                result = TestResult(
                    False, 
                    f"Could not load FAT report (expected): {load_result.message}",
                    {"report_id": KNOWN_FAT_REPORT_ID, "expected_failure": True}
                )
                self.results.append(result)
                print_test_result(result)
                return
            
            if report_data is None:
                result = TestResult(False, "Report data is None")
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
            result = TestResult(False, f"FAT test failed: {e}")
            self.results.append(result)
            print_test_result(result)
            
    def _create_test_uut_report(self) -> Optional[UUTReport]:
        """Create a test UUT report."""
        try:
            if self.client is None:
                print("    ❌ No client available")
                return None
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create UUT report
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
            
            return uut_report
            
        except Exception as e:
            print(f"    ❌ Error creating UUT report: {e}")
            return None
            
    def _submit_uut_report(self, uut_report: UUTReport) -> TestResult:
        """Submit UUT report to server."""
        try:
            if self.client is None or not hasattr(self.client, '_connection') or self.client._connection is None:
                return TestResult(False, "No client connection available")
            
            # Use the TDM client's submission functionality
            from pyWATS.rest_api.endpoints.report import submit_wsjf_report
            
            # Serialize the report
            report_data = uut_report.model_dump(by_alias=True, mode='json')
            
            # Submit via the client's connection
            result = submit_wsjf_report(report_data, client=self.client._connection._client)
            
            if result.success:
                return TestResult(
                    True, 
                    f"UUT submitted successfully",
                    {"report_id": str(result.report_id), "message": result.message}
                )
            else:
                return TestResult(False, f"Submission failed: {result.message}")
                
        except Exception as e:
            return TestResult(False, f"Submission error: {e}")
            
    def _load_and_validate_uut(self, report_id: str) -> TestResult:
        """Load and validate UUT report from server."""
        try:
            if self.client is None:
                return TestResult(False, "No client available")
                
            # Load the report
            report_data, load_result = wait_and_retry_load(self.client, report_id)
            
            if not load_result.success:
                return TestResult(False, f"Load failed: {load_result.message}")
            
            if report_data is None:
                return TestResult(False, "Report data is None")
                
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
                    return TestResult(
                        False, 
                        f"Validation failed: {', '.join(failed_checks)}",
                        {"loaded_fields": len(report_data), "failed_validations": failed_checks}
                    )
                else:
                    return TestResult(
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
                return TestResult(False, f"Deserialization failed: {deserialize_error}")
                
        except Exception as e:
            return TestResult(False, f"Load and validate error: {e}")
            
    def _deserialize_fat_report(self, report_data: dict) -> TestResult:
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
            
            return TestResult(
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
            return TestResult(
                False, 
                f"FAT deserialization failed (expected): {e}",
                {
                    "error_type": type(e).__name__,
                    "available_fields": list(report_data.keys())[:10],  # First 10 fields
                    "total_fields": len(report_data),
                    "note": "This failure helps identify missing model fields"
                }
            )
            
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


def run_uut_tests():
    """Main entry point for UUT testing."""
    runner = UUTTestRunner()
    runner.run_all_tests()


if __name__ == "__main__":
    run_uut_tests()