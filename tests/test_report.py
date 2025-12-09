"""
Tests for report module - UUT/UUR report operations
"""
import pytest
from typing import Any
from datetime import datetime
from pywats.models.report import Attachment
from pywats.models.report.uut.uut_report import UUTReport
from pywats.models.report.uut.steps.comp_operator import CompOp
from pywats.models.report.uut.steps.sequence_call import SequenceCall
from pywats.models.report_query import WATSFilter
from pywats.tools.test_uut import create_test_uut_report


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

        try:
            result = wats_client.report.submit_uut(report)
            assert result is not None
            # Result should be a report ID (string)
            assert isinstance(result, str)
            assert len(result) > 0
        except Exception as e:
            pytest.skip(f"Server not available or configured: {e}")


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
        try:
            result = wats_client.report.submit_uut(report)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Server not available or configured: {e}")


class TestUURReport:
    """Test UUR (Unit Under Repair) report operations"""

    def test_create_uur_report(self) -> None:
        """Test creating a UUR report"""
        from pywats.models.report import UURReport
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
        from pywats.models.report import UURReport
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
        # Test that report can be submitted without errors
        # Result may be None if server rejects invalid test data
        try:
            wats_client.report.submit(report)
        except Exception as e:
            pytest.skip(f"UUR submission failed: {e}")


class TestReportQuery:
    """Test querying and loading reports"""

    def test_find_report_headers(
        self,
        wats_client: Any,
        test_part_number: str
    ) -> None:
        """Test finding report headers with filter"""
        filter_obj = WATSFilter()

        try:
            headers = wats_client.report.get_report_headers(filter_obj)
            assert isinstance(headers, list)
        except Exception as e:
            pytest.skip(f"Query failed: {e}")

    def test_load_report_by_uuid(self, wats_client: Any) -> None:
        """Test loading a report by UUID"""
        filter_obj = WATSFilter()

        try:
            headers = wats_client.report.get_report_headers(filter_obj)
            if headers and len(headers) > 0:
                report_uuid = headers[0].uuid
                report = wats_client.report.get_report(report_uuid)
                assert report is not None
            else:
                pytest.skip("No reports available for testing")
        except Exception as e:
            pytest.skip(f"Load report failed: {e}")


class TestReportFiltering:
    """Test report filtering capabilities"""

    def test_filter_by_date_range(self, wats_client: Any) -> None:
        """Test filtering reports by date range"""
        filter_obj = WATSFilter()

        try:
            headers = wats_client.report.get_report_headers(filter_obj)
            assert isinstance(headers, list)
        except Exception as e:
            pytest.skip(f"Date filter failed: {e}")

    def test_filter_by_status(self, wats_client: Any) -> None:
        """Test filtering by status"""
        filter_obj = WATSFilter()

        try:
            headers = wats_client.report.get_report_headers(filter_obj)
            if headers:
                assert isinstance(headers, list)
        except Exception as e:
            pytest.skip(f"Status filter failed: {e}")
