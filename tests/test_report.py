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
        """Test sending a UUT report to server"""
        report = create_test_uut_report(
            part_number=test_part_number,
            serial_number=test_serial_number
        )

        print(f"\n=== SUBMITTING UUT REPORT ===")
        print(f"Part Number: {report.pn}")
        print(f"Serial Number: {report.sn}")
        print(f"Station: {report.station_name}")
        print(f"Result: {report.result}")
        
        result = wats_client.report.submit_report(report)
        
        print(f"\nSubmit Result: {result}")
        print(f"==============================\n")
        
        assert result is not None, "Report submission returned None - check server logs"
        # Result should be a report ID (string)
        assert isinstance(result, str), f"Expected string result, got {type(result)}"
        assert len(result) > 0, "Report ID is empty"


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
        """Test sending a UUT report created by test_uut tool"""
        report = create_test_uut_report()
        
        print(f"\n=== SUBMITTING TEST TOOL REPORT ===")
        print(f"Part Number: {report.pn}")
        print(f"Serial Number: {report.sn}")
        
        result = wats_client.report.submit_report(report)
        
        print(f"Submit Result: {result}")
        print(f"====================================\n")
        
        assert result is not None, "Report submission returned None"


class TestUURReport:
    """Test UUR (Unit Under Repair) report operations"""

    def test_create_uur_report(self) -> None:
        """Test creating a UUR report"""
        from pywats.domains.report import UURReport
        from datetime import datetime
        
        report = UURReport(
            sn="REPAIR-001",
            pn="PN-12345",
            rev="A",
            process_code=100,
            uur={"user": "test_operator"},
            start=datetime.now().astimezone(),
            station_name="RepairStation",
            location="TestLab",
            purpose="Repair"
        )
        assert report is not None
        assert report.sn == "REPAIR-001"
        assert report.pn == "PN-12345"

    def test_send_uur_report(self, wats_client: Any) -> None:
        """Test sending a UUR report"""
        from pywats.domains.report import UURReport
        from datetime import datetime
        
        report = UURReport(
            sn="REPAIR-001",
            pn="PN-12345",
            rev="A",
            process_code=100,
            uur={"user": "test_operator"},
            start=datetime.now().astimezone(),
            station_name="RepairStation",
            location="TestLab",
            purpose="Repair"
        )
        # Test that report can be submitted
        print(f"\n=== SUBMITTING UUR REPORT ===")
        print(f"Serial: {report.sn}, Part: {report.pn}")
        
        result = wats_client.report.submit_report(report)
        
        print(f"Submit result: {result}")
        print("==============================\n")


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
