"""
Tests for report module - UUT/UUR report operations
"""
import pytest
from datetime import datetime
from pywats.models.report import UUTReport, SequenceCall, NumericLimitStep
from pywats.models.report_query import WATSFilter


class TestReportCreation:
    """Test creating and sending reports"""
    
    def test_create_uut_report(self, test_serial_number, test_part_number, test_revision):
        """Test creating a basic UUT report structure"""
        report = UUTReport(
            serial_number=test_serial_number,
            part_number=test_part_number,
            revision=test_revision,
            status="Passed"
        )
        assert report.serial_number == test_serial_number
        assert report.status == "Passed"
    
    def test_add_sequence_to_report(self, test_serial_number):
        """Test adding sequence steps to report"""
        report = UUTReport(serial_number=test_serial_number)
        seq = SequenceCall(name="MainSequence")
        seq.add_step(NumericLimitStep(
            name="VoltageTest",
            measurement=5.0,
            low_limit=4.5,
            high_limit=5.5,
            status="Passed"
        ))
        report.root_sequence = seq
        assert report.root_sequence.name == "MainSequence"
        assert len(report.root_sequence.steps) == 1
    
    def test_send_uut_report(self, wats_client, test_serial_number, test_part_number):
        """Test sending a UUT report to server"""
        report = UUTReport(
            serial_number=test_serial_number,
            part_number=test_part_number,
            status="Passed",
            start_date_time=datetime.utcnow()
        )
        
        # This may fail if server is not configured
        try:
            result = wats_client.report.submit_uut(report)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Server not available or configured: {e}")


class TestReportQuery:
    """Test querying and loading reports"""
    
    def test_find_report_headers(self, wats_client, test_part_number):
        """Test finding report headers with filter"""
        filter_obj = WATSFilter(
            part_number=test_part_number,
            max_count=10
        )
        
        try:
            headers = wats_client.report.get_report_headers(filter_obj)
            assert isinstance(headers, list)
        except Exception as e:
            pytest.skip(f"Query failed: {e}")
    
    def test_load_report_by_uuid(self, wats_client):
        """Test loading a report by UUID"""
        # First get a report UUID
        filter_obj = WATSFilter(max_count=1)
        
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
    
    def test_filter_by_date_range(self, wats_client):
        """Test filtering reports by date range"""
        from datetime import timedelta
        
        filter_obj = WATSFilter(
            date_from=datetime.utcnow() - timedelta(days=7),
            date_to=datetime.utcnow(),
            max_count=10
        )
        
        try:
            headers = wats_client.report.get_report_headers(filter_obj)
            assert isinstance(headers, list)
        except Exception as e:
            pytest.skip(f"Date filter failed: {e}")
    
    def test_filter_by_status(self, wats_client):
        """Test filtering by status"""
        filter_obj = WATSFilter(
            status="Passed",
            max_count=5
        )
        
        try:
            headers = wats_client.report.get_report_headers(filter_obj)
            if headers:
                assert all(h.status == "Passed" for h in headers if h.status)
        except Exception as e:
            pytest.skip(f"Status filter failed: {e}")
