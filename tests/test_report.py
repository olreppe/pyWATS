"""
Tests for report module - UUT/UUR report operations
"""
import pytest
from typing import Any, Dict
from datetime import datetime
from pywats.domains.report import UUTReport, WATSFilter
from pywats.domains.report.report_models import Attachment
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp
from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall
from pywats.tools.test_uut import create_test_uut_report


class TestServerConfiguration:
    """Verify test configuration is correct"""

    def test_verify_server_url_and_token(self, wats_config: Dict[str, str]) -> None:
        """Verify which server URL and token is being used"""
        print(f"\n=== TEST CONFIGURATION ===")
        print(f"Server URL: {wats_config['base_url']}")
        print(f"Token (first 20 chars): {wats_config['token'][:20]}...")
        print(f"==========================\n")
        
        assert wats_config['base_url'] == "https://python.wats.com"
        assert len(wats_config['token']) > 0


class TestReportCreation:
    """Test creating and sending reports using factory methods"""

    def test_create_minimal_uut_report(
        self,
        test_serial_number: str,
        test_part_number: str,
        test_revision: str
    ) -> None:
        """Test creating a minimal UUT report with basic structure"""
        # Create report using factory method
        report = UUTReport(
            pn=test_part_number,
            sn=test_serial_number,
            rev=test_revision,
            process_code=10,
            station_name="TestStation",
            location="TestLab",
            purpose="Debug",
            result="P",
            start=datetime.now().astimezone()
        )
        
        # Verify report structure
        assert report.pn == test_part_number
        assert report.sn == test_serial_number
        assert report.rev == test_revision
        assert report.type == "T"  # UUT report type
        
        # Get root sequence and verify it exists
        root = report.get_root_sequence_call()
        assert root is not None
        assert root.name == "MainSequence Callback"
        
        # Add a simple test step
        root.add_boolean_step(name="Connection Test", status="P")
        
        # Verify step was added
        assert root.steps is not None
        steps = root.steps
        assert len(steps) == 1
        assert steps[0].name == "Connection Test"
        assert steps[0].status == "P"

    def test_create_uut_with_numeric_steps(
        self,
        test_part_number: str
    ) -> None:
        """Test creating UUT report with numeric limit test steps"""
        report = UUTReport(
            pn=test_part_number,
            sn="TEST-NUM-001",
            rev="A",
            process_code=10,
            station_name="NumericTestStation",
            location="TestLab",
            purpose="Testing",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        
        # Add numeric tests with different comparison operators
        root.add_numeric_step(
            name="Voltage Test (GELE)",
            value=3.3,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=3.0,
            high_limit=3.6,
            status="P"
        )
        
        root.add_numeric_step(
            name="Current Test (LOG)",
            value=1.25,
            unit="A",
            comp_op=CompOp.LOG,
            status="P"
        )
        
        # Verify steps were created correctly
        assert root.steps is not None
        steps = root.steps
        assert len(steps) == 2
        
        voltage_step = steps[0]
        assert voltage_step.name == "Voltage Test (GELE)"
        
        current_step = steps[1]
        assert current_step.name == "Current Test (LOG)"

    def test_create_uut_with_sequence_hierarchy(
        self,
        test_part_number: str
    ) -> None:
        """Test creating nested sequence calls"""
        report = UUTReport(
            pn=test_part_number,
            sn="TEST-SEQ-001",
            rev="A",
            process_code=10,
            station_name="SeqTestStation",
            location="TestLab",
            purpose="Testing",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        
        # Add sub-sequence
        power_seq = root.add_sequence_call(
            name="Power Supply Tests",
            file_name="power_tests.py",
            version="1.0.0"
        )
        
        # Add tests to sub-sequence
        power_seq.add_numeric_step(
            name="3V3 Rail",
            value=3.31,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=3.1,
            high_limit=3.5,
            status="P"
        )
        
        power_seq.add_numeric_step(
            name="5V Rail",
            value=5.02,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=4.8,
            high_limit=5.2,
            status="P"
        )
        
        # Verify hierarchy
        assert root.steps is not None
        steps = root.steps
        assert len(steps) == 1
        
        nested_seq = steps[0]
        assert isinstance(nested_seq, SequenceCall)
        assert nested_seq.name == "Power Supply Tests"
        assert nested_seq.steps is not None
        nested_steps = nested_seq.steps
        assert len(nested_steps) == 2
        assert nested_steps[0].name == "3V3 Rail"
        assert nested_steps[1].name == "5V Rail"

    def test_create_uut_using_test_tool(self) -> None:
        """Test comprehensive report created by test_uut tool"""
        report = create_test_uut_report(
            part_number="TOOL-TEST-001",
            serial_number="TOOL-SN-001"
        )
        
        # Verify basic report structure
        assert report is not None
        assert report.pn == "TOOL-TEST-001"
        assert report.sn == "TOOL-SN-001"
        assert report.type == "T"
        
        # Verify root sequence exists and has steps
        root = report.get_root_sequence_call()
        assert root is not None
        assert root.steps is not None
        steps = root.steps
        assert len(steps) > 0
        
        # Verify root sequence was created properly
        assert isinstance(root, SequenceCall)

    def test_send_uut_report(
        self,
        wats_client: Any,
        test_serial_number: str,
        test_part_number: str
    ) -> None:
        """Test sending a UUT report to server and verifying it was accepted"""
        report = create_test_uut_report(
            part_number=test_part_number,
            serial_number=test_serial_number
        )

        # Verify UUT report has at least one step (CRITICAL: all reports must have at least one step)
        root = report.get_root_sequence_call()
        assert root is not None, "UUT report missing root sequence"
        assert root.steps is not None and len(root.steps) > 0, "UUT report must have at least one test step"

        print(f"\n=== SUBMITTING UUT REPORT ===")
        print(f"Part Number: {report.pn}")
        print(f"Serial Number: {report.sn}")
        print(f"Station: {report.station_name}")
        print(f"Result: {report.result}")
        print(f"Steps: {len(root.steps)}")
        
        result = wats_client.report.submit_report(report)
        
        print(f"\nSubmit Result: {result}")
        print(f"==============================\n")
        
        assert result is not None, "Report submission returned None - check server logs"
        # Result should be a report ID (string)
        assert isinstance(result, str), f"Expected string result, got {type(result)}"
        assert len(result) > 0, "Report ID is empty"
        
        # CRITICAL: Verify the report was actually accepted by retrieving it from server
        print(f"\n=== VERIFYING REPORT ON SERVER ===")
        print(f"Attempting to retrieve report ID: {result}")
        
        retrieved_report = wats_client.report.get_report(result)
        
        print(f"Report retrieved successfully: {retrieved_report is not None}")
        assert retrieved_report is not None, f"Failed to retrieve submitted report {result} from server - report was NOT accepted!"
        
        # Verify the retrieved report has the expected data
        assert retrieved_report.pn == test_part_number, f"Part number mismatch: {retrieved_report.pn} != {test_part_number}"
        assert retrieved_report.sn == test_serial_number, f"Serial number mismatch: {retrieved_report.sn} != {test_serial_number}"
        print(f"Report verification PASSED - report was fully accepted by server")
        print(f"==============================\n")


class TestAttachments:
    """Test report attachments"""

    def test_create_attachment(self) -> None:
        """Test creating an attachment"""
        attachment = Attachment(
            name="inspection_photo.jpg",
            content_type="image/jpeg",
            data="base64encodeddata"
        )
        assert attachment.name == "inspection_photo.jpg"


class TestReportSubmission:
    """Test sending reports to server"""

    def test_send_uut_report_from_test_tool(self, wats_client: Any) -> None:
        """Test sending a UUT report created by test_uut tool and verifying it was accepted"""
        report = create_test_uut_report()
        
        # Verify UUT report has at least one step (CRITICAL: all reports must have at least one step)
        root = report.get_root_sequence_call()
        assert root is not None, "UUT report missing root sequence"
        assert root.steps is not None and len(root.steps) > 0, "UUT report must have at least one test step"
        
        print(f"\n=== SUBMITTING TEST TOOL REPORT ===")
        print(f"Part Number: {report.pn}")
        print(f"Serial Number: {report.sn}")
        print(f"Steps: {len(root.steps)}")
        
        result = wats_client.report.submit_report(report)
        
        print(f"Submit Result: {result}")
        print(f"====================================\n")
        
        assert result is not None, "Report submission returned None"
        
        # CRITICAL: Verify the report was actually accepted by retrieving it
        print(f"\n=== VERIFYING REPORT WAS ACCEPTED ===")
        retrieved_report = wats_client.report.get_report(result)
        assert retrieved_report is not None, f"Failed to retrieve submitted report {result} - report was NOT accepted!"
        print(f"Report verification PASSED\n")


class TestUURReport:
    """Test UUR (Unit Under Repair) report operations"""

    def test_create_uur_report(self, wats_client: Any) -> None:
        """Test creating and submitting a basic UUR report with structure"""
        from pywats.domains.report import UURReport
        from datetime import datetime
        
        # First create and submit a failed UUT (UUR must reference a UUT)
        uut = wats_client.report.create_uut_report(
            operator="TestOperator",
            part_number="PN-12345",
            revision="A",
            serial_number="REPAIR-001",
            operation_type=100,
            station_name="RepairStation",
            location="TestLab"
        )
        
        # Add a failed test step to the UUT
        root = uut.get_root_sequence_call()
        root.add_boolean_step(name="Initial Test", status="F")
        
        # Submit the failed UUT
        uut_id = wats_client.report.submit_report(uut)
        assert uut_id is not None, "Failed to submit UUT report"
        
        # Create UUR from the failed UUT
        report = wats_client.report.create_uur_report(
            uut,
            operator="RepairOperator",
            station_name="RepairStation",
            location="TestLab"
        )
        
        # Add failure information to the UUR
        if report.sub_units and len(report.sub_units) > 0:
            report.sub_units[0].add_failure(
                category="Component",
                code="Defect Component",
                comment="Component R1 failed - replaced",
                component_ref="R1"
            )
        
        # Verify UUR report structure
        assert report is not None
        assert report.sn == "REPAIR-001"
        assert report.pn == "PN-12345"
        assert report.rev == "A"
        assert report.uur_info is not None

    def test_send_uur_report(self, wats_client: Any) -> None:
        """Test sending a UUR report
        
        NOTE: This test requires failure categories and codes configured in WATS.
        Skips if not configured.
        """
        import pytest
        from datetime import datetime
        
        # Create a failed UUT first (UUR must reference a UUT)
        uut = wats_client.report.create_uut_report(
            operator="test_operator",
            part_number="PN-12345",
            revision="A",
            serial_number="REPAIR-001",
            operation_type=100,
            station_name="RepairStation",
            location="TestLab"
        )
        # Submit the UUT first
        uut_id = wats_client.report.submit_report(uut)
        
        # Now create UUR from the failed UUT
        report = wats_client.report.create_uur_report(
            uut,
            operator="test_operator",
            station_name="RepairStation",
            location="TestLab"
        )
        
        # Add a failure (required for UUR submission)
        if report.sub_units and len(report.sub_units) > 0:
            report.sub_units[0].add_failure(
                category="Component",  # Must be configured in WATS
                code="Defective",
                comment="Component failed during test",
                component_ref="C12"
            )
        
        # Test that UUR report can be submitted
        print(f"\n=== SUBMITTING UUR REPORT ===")
        print(f"Serial: {report.sn}, Part: {report.pn}")
        print(f"References UUT: {uut_id}")
        
        try:
            result = wats_client.report.submit_report(report)
            print(f"Submit result: {result}")
            
            # CRITICAL: Verify the UUR was actually accepted by retrieving it
            print(f"=== VERIFYING UUR WAS ACCEPTED ===")
            retrieved_report = wats_client.report.get_report(result)
            assert retrieved_report is not None, f"Failed to retrieve submitted UUR {result} - report was NOT accepted!"
            print("UUR verification PASSED")
            print("==============================\n")
            
            assert result is not None
        except ValueError as e:
            if "Category must be a valid value" in str(e) or "Code must be a valid value" in str(e):
                pytest.skip(f"Failure categories/codes not configured in WATS: {e}")
            raise

    def test_create_uur_from_uut_object(self, wats_client: Any) -> None:
        """Test creating UUR from a UUTReport object"""
        from datetime import datetime
        
        # Create a failed UUT report
        uut = wats_client.report.create_uut_report(
            operator="TestOperator",
            part_number="PN-REPAIR-TEST",
            revision="B",
            serial_number=f"SN-{datetime.now().strftime('%H%M%S')}",
            operation_type=100,
            station_name="TestStation",
            location="TestLab"
        )
        
        # Create UUR from the UUT object
        uur = wats_client.report.create_uur_report(
            uut,
            operator="RepairTech",
            comment="Repair initiated from failed UUT"
        )
        
        print(f"\n=== CREATE UUR FROM UUT OBJECT ===")
        print(f"UUT ID: {uut.id}")
        print(f"UUR references UUT: {uur.uur_info.ref_uut}")
        print(f"UUR part_number: {uur.pn}")
        print(f"UUR serial: {uur.sn}")
        print("==================================\n")
        
        assert uur is not None
        assert uur.pn == uut.pn
        assert uur.sn == uut.sn
        assert uur.uur_info.ref_uut == uut.id

    def test_create_uur_from_part_and_process(self, wats_client: Any) -> None:
        """Test creating UUR from part number and process code"""
        from datetime import datetime
        
        # Create UUR using part_number and process_code pattern
        uur = wats_client.report.create_uur_report(
            "PN-DIRECT-CREATE",
            100,
            serial_number=f"SN-{datetime.now().strftime('%H%M%S')}",
            operator="DirectRepairTech"
        )
        
        print(f"\n=== CREATE UUR FROM PART/PROCESS ===")
        print(f"UUR part_number: {uur.pn}")
        print(f"UUR repair_process_code: {uur.process_code}")
        print(f"UUR test_operation_code: {uur.uur_info.test_operation_code}")
        print("====================================\n")
        
        assert uur is not None
        assert uur.pn == "PN-DIRECT-CREATE"
        # UUR has dual process codes:
        assert uur.process_code == 500  # repair_process_code (default)
        assert uur.uur_info.test_operation_code == 100  # original test that failed


class TestRepairScenario:
    """
    Test complete repair workflow scenario:
    1. Failed UUT in a test operation
    2. Repair report linking to the failure
    3. Retest that passes
    """

    def test_complete_repair_workflow(self, wats_client: Any) -> None:
        """
        Complete repair scenario:
        - Submit a FAILED UUT report
        - Create a UUR (repair) report linked to the failed UUT
        - Submit the UUR with repair information
        - Submit a PASSING UUT report (retest)
        """
        from datetime import datetime
        from pywats.domains.report.report_models.uut.step import StepStatus
        
        # Use consistent serial number for the workflow
        test_serial = f"REPAIR-WORKFLOW-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        part_number = "PN-REPAIR-SCENARIO"
        process_code = 100
        
        print(f"\n{'='*60}")
        print(f"COMPLETE REPAIR WORKFLOW SCENARIO")
        print(f"Serial Number: {test_serial}")
        print(f"Part Number: {part_number}")
        print(f"{'='*60}\n")
        
        # ============================================================
        # STEP 1: Create and submit a FAILED UUT report
        # ============================================================
        print("STEP 1: Creating FAILED UUT report...")
        
        failed_uut = wats_client.report.create_uut_report(
            operator="TestOperator",
            part_number=part_number,
            revision="A",
            serial_number=test_serial,
            operation_type=process_code,
            station_name="TestStation-01",
            location="Production Line A"
        )
        
        # Add a sequence with test steps including a failing one
        main_seq = failed_uut.root.add_sequence_call("Functional Test Sequence")
        
        # Add passing setup step
        setup_step = main_seq.add_numeric_step(
            name="Power Supply Voltage",
            value=12.05,
            unit="V",
            low_limit=11.5,
            high_limit=12.5,
            comp_op="GELE",
            status="P"
        )
        
        # Add FAILING step - this is the failure we'll repair
        failing_step = main_seq.add_numeric_step(
            name="Current Draw Test",
            value=2.5,  # Value exceeds limit
            unit="A",
            low_limit=0.5,
            high_limit=2.0,
            comp_op="GELE",
            status="F"  # FAILED
        )
        failing_step.error_message = "Current draw exceeds maximum specification"
        failing_step.caused_uut_failure = True
        
        # Add another passing step (but UUT already failed)
        post_step = main_seq.add_boolean_step(
            name="Communication Check",
            status="P"
        )
        
        # Set overall UUT status to FAILED
        # IMPORTANT: Root sequence status must match report result!
        failed_uut.result = "F"
        failed_uut.root.status = "F"
        main_seq.status = "F"
        
        print(f"  - UUT ID: {failed_uut.id}")
        print(f"  - Status: FAILED")
        print(f"  - Failing step: '{failing_step.name}' (value={failing_step.measurement.value})")
        
        # Submit the failed UUT
        failed_result = wats_client.report.submit_report(failed_uut)
        print(f"  - Submit result: {failed_result}")
        
        assert failed_result is not None, "Failed UUT submission returned None - check server connection"
        print(f"  - Successfully submitted failed UUT: {failed_result}")
        
        # ============================================================
        # STEP 2: Create repair report (UUR) linked to failed UUT
        # ============================================================
        print("\nSTEP 2: Creating UUR (repair) report linked to failed UUT...")
        
        # Create UUR from the failed UUT object
        repair_report = wats_client.report.create_uur_report(
            failed_uut,
            operator="RepairTechnician",
            comment="Investigating high current draw issue"
        )
        
        # Set repair information
        repair_report.comment = "Replaced faulty capacitor C12 causing excessive current draw"
        
        # Add a failure to the main unit (required by API)
        # This represents the failure that was repaired
        # Use valid category and fail code from server's RepairOperationConfig
        repair_report.add_failure_to_main_unit(
            category="Component",
            code="Defect Component",
            comment="Capacitor C12 exceeded current specification",
            component_ref="C12"
        )
        
        print(f"  - UUR ID: {repair_report.id}")
        print(f"  - References UUT: {repair_report.uur_info.ref_uut}")  # Use snake_case
        print(f"  - Operator: {repair_report.operator}")
        print(f"  - Comment: {repair_report.comment}")
        
        # Submit the repair report
        repair_result = wats_client.report.submit_report(repair_report)
        print(f"  - Submit result: {repair_result}")
        
        assert repair_result is not None, "UUR submission returned None - check server connection"
        print(f"  - Successfully submitted UUR: {repair_result}")
        
        # ============================================================
        # STEP 3: Create PASSING retest UUT report
        # ============================================================
        print("\nSTEP 3: Creating PASSING retest UUT report...")
        
        retest_uut = wats_client.report.create_uut_report(
            operator="TestOperator",
            part_number=part_number,
            revision="A",
            serial_number=test_serial,  # Same serial number
            operation_type=process_code,
            station_name="TestStation-01",
            location="Production Line A"
        )
        
        # Add the same test sequence - all passing now
        retest_seq = retest_uut.root.add_sequence_call("Functional Test Sequence")
        
        # Add passing setup step
        retest_seq.add_numeric_step(
            name="Power Supply Voltage",
            value=12.02,
            unit="V",
            low_limit=11.5,
            high_limit=12.5,
            comp_op="GELE",
            status="P"
        )
        
        # Previously failing step now PASSES after repair
        fixed_step = retest_seq.add_numeric_step(
            name="Current Draw Test",
            value=1.2,  # Now within limits after capacitor replacement
            unit="A",
            low_limit=0.5,
            high_limit=2.0,
            comp_op="GELE",
            status="P"  # PASSED
        )
        
        # Communication check still passing
        retest_seq.add_boolean_step(
            name="Communication Check",
            status="P"
        )
        
        # Set overall UUT status to PASSED
        retest_uut.result = "P"
        
        print(f"  - UUT ID: {retest_uut.id}")
        print(f"  - Status: PASSED")
        print(f"  - Fixed step: '{fixed_step.name}' (value={fixed_step.measurement.value})")
        
        # Submit the passing retest
        retest_result = wats_client.report.submit_report(retest_uut)
        print(f"  - Submit result: {retest_result}")
        
        assert retest_result is not None, "Retest UUT submission returned None - check server connection"
        print(f"  - Successfully submitted retest UUT: {retest_result}")
        
        # ============================================================
        # Summary
        # ============================================================
        print(f"\n{'='*60}")
        print("REPAIR WORKFLOW COMPLETE")
        print(f"{'='*60}")
        print(f"Serial Number: {test_serial}")
        print(f"1. Failed UUT:  {failed_uut.id}")
        print(f"   - Server ID: {failed_result}")
        print(f"   - Status: F")
        print(f"2. Repair UUR:  {repair_report.id}")
        print(f"   - Server ID: {repair_result}")
        print(f"   - Linked to: {repair_report.uur_info.ref_uut}")
        print(f"3. Retest UUT:  {retest_uut.id}")
        print(f"   - Server ID: {retest_result}")
        print(f"   - Status: P")
        print(f"{'='*60}\n")
        
        # Assertions
        assert failed_uut.result == "F", "Initial UUT should be failed"
        assert repair_report.uur_info.ref_uut == failed_uut.id, "UUR should reference failed UUT"
        assert retest_uut.result == "P", "Retest UUT should be passed"
        assert retest_uut.sn == failed_uut.sn, "Retest should have same serial number"
        
        # Verify all submissions were successful
        assert failed_result is not None, "Failed UUT was not submitted"
        assert repair_result is not None, "UUR was not submitted"
        assert retest_result is not None, "Retest UUT was not submitted"


class TestReportQuery:
    """Test querying and loading reports"""

    def test_query_uut_headers(self, wats_client: Any) -> None:
        """Test querying UUT report headers"""
        print("\n=== QUERY UUT HEADERS ===")
        
        headers = wats_client.report.query_uut_headers()
        
        print(f"Found {len(headers)} UUT report headers")
        for h in headers[:3]:
            print(f"  - {h.serial_number}: {h.status}")
        print("=========================\n")
        
        assert isinstance(headers, list)

    def test_query_uur_headers(self, wats_client: Any) -> None:
        """Test querying UUR report headers"""
        print("\n=== QUERY UUR HEADERS ===")
        
        headers = wats_client.report.query_uur_headers()
        
        print(f"Found {len(headers)} UUR report headers")
        print("=========================\n")
        
        assert isinstance(headers, list)

    def test_load_report_by_uuid(self, wats_client: Any) -> None:
        """Test loading a full report by UUID"""
        print("\n=== LOAD REPORT BY UUID ===")
        
        # First get headers to find a report ID
        headers = wats_client.report.query_uut_headers()
        if not headers:
            pytest.skip("No reports available for testing")
        
        report_id = str(headers[0].uuid)
        print(f"Loading report: {report_id}")
        
        report = wats_client.report.get_report(report_id)
        
        print(f"Loaded report: {report}")
        print("===========================\n")


class TestReportFiltering:
    """Test report filtering capabilities"""

    def test_filter_by_date_range(self, wats_client: Any) -> None:
        """Test filtering reports by date range"""
        from datetime import datetime, timedelta
        
        print("\n=== FILTER BY DATE RANGE ===")
        
        # Get reports from last 7 days
        headers = wats_client.report.get_recent_headers(days=7)
        
        print(f"Found {len(headers)} reports in last 7 days")
        print("=============================\n")
        
        assert isinstance(headers, list)

    def test_filter_by_serial_number(self, wats_client: Any) -> None:
        """Test filtering by serial number"""
        print("\n=== FILTER BY SERIAL ===")
        
        # First get any headers to find a serial number
        all_headers = wats_client.report.query_uut_headers()
        if not all_headers:
            pytest.skip("No reports available")
        
        serial = all_headers[0].serial_number
        print(f"Searching for serial: {serial}")
        
        headers = wats_client.report.get_headers_by_serial(serial)
        
        print(f"Found {len(headers)} reports for {serial}")
        print("=========================\n")
        
        assert isinstance(headers, list)
        assert len(headers) > 0
