"""
Comprehensive timezone validation test.

This test documents and verifies that:
1. Reports created with naive datetimes get timezone added automatically
2. Reports created with timezone-aware datetimes preserve the timezone
3. All serialized reports include the timezone offset in JSON
4. Server round-trip preserves timezone information correctly
"""
import pytest
from datetime import datetime, timezone
from typing import Any
from pywats.domains.report.report_models.uut.uut_report import UUTReport
from pywats.tools.test_uut import create_test_uut_report


class TestTimezoneHandling:
    """Comprehensive timezone validation tests"""

    def test_naive_datetime_gets_timezone_added(self) -> None:
        """Verify that naive datetime (no timezone) gets timezone added by validator"""
        naive_dt = datetime.now()
        assert naive_dt.tzinfo is None, "Precondition: datetime should be naive"
        
        report = UUTReport(
            pn="TEST-001",
            sn="TZ-TEST-001",
            rev="A",
            process_code=10,
            station_name="TestStation",
            location="TestLab",
            purpose="Debug",
            result="P",
            start=naive_dt
        )
        
        # Validator should have added timezone
        assert report.start.tzinfo is not None, "Validator should add timezone to naive datetime"
        
        # JSON should include timezone offset
        json_str = report.model_dump_json()
        assert '+' in json_str or 'Z' in json_str, "JSON must include timezone offset"
        
    def test_timezone_aware_datetime_preserved(self) -> None:
        """Verify that timezone-aware datetime is preserved"""
        aware_dt = datetime.now().astimezone()
        assert aware_dt.tzinfo is not None, "Precondition: datetime should be timezone-aware"
        
        report = UUTReport(
            pn="TEST-002",
            sn="TZ-TEST-002",
            rev="A",
            process_code=10,
            station_name="TestStation",
            location="TestLab",
            purpose="Debug",
            result="P",
            start=aware_dt
        )
        
        # Timezone should be preserved
        assert report.start.tzinfo is not None
        assert report.start == aware_dt
        
    def test_server_roundtrip_preserves_timezone(
        self, 
        wats_client: Any, 
        test_serial_number: str, 
        test_part_number: str
    ) -> None:
        """Verify server round-trip preserves timezone correctly"""
        # Create report with known timezone-aware timestamp
        client_time = datetime.now().astimezone()
        
        report = create_test_uut_report(
            part_number=test_part_number,
            serial_number=test_serial_number
        )
        report.start = client_time
        
        # Submit to server
        report_id = wats_client.report.submit_report(report)
        assert report_id is not None
        
        # Retrieve from server
        retrieved = wats_client.report.get_report(report_id)
        
        # Verify timestamps match exactly
        assert retrieved.start.tzinfo is not None, "Retrieved report must have timezone"
        assert retrieved.start == client_time, f"Timestamps should match: sent {client_time}, got {retrieved.start}"
        
        # Calculate difference should be zero
        diff = client_time - retrieved.start
        assert diff.total_seconds() == 0, f"Time difference should be 0, got {diff.total_seconds()} seconds"
