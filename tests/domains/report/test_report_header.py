"""
Test ReportHeader model matches C# API specification.

This test suite validates that the ReportHeader class correctly matches
the C# WATS API ReportHeader structure, ensuring field naming and availability
matches the backend API.
"""

import pytest
from uuid import UUID
from datetime import datetime

from pywats.domains.report.models import ReportHeader


class TestReportHeaderAPICompliance:
    """Test ReportHeader matches C# API specification"""
    
    def test_has_result_not_status(self):
        """ReportHeader should have 'result' field, not 'status' (matches C# API)"""
        header = ReportHeader(
            uuid=UUID('12345678-1234-1234-1234-123456789012'),
            result="P"  # C# uses 'Result' (string) not 'Status'
        )
        
        # Should have result field
        assert hasattr(header, 'result')
        assert header.result == "P"
        
        # Should NOT have status field (this was wrong - not in C# API)
        assert not hasattr(header, 'status')
    
    def test_has_process_code_and_name(self):
        """ReportHeader should have process_code and process_name (matches C# API)"""
        header = ReportHeader(
            uuid=UUID('12345678-1234-1234-1234-123456789012'),
            process_code=100,
            process_name="End of line test"
        )
        
        assert hasattr(header, 'process_code')
        assert hasattr(header, 'process_name')
        assert header.process_code == 100
        assert header.process_name == "End of line test"
    
    def test_no_test_operation_code_fields(self):
        """ReportHeader should NOT have test_operation_code or test_operation_name
        
        These fields don't exist in the C# ReportHeader API.
        Test operation information is only available in the full UUR report,
        not in ReportHeader.
        """
        header = ReportHeader(
            uuid=UUID('12345678-1234-1234-1234-123456789012')
        )
        
        # These fields should NOT exist (they were mistakenly added before)
        assert not hasattr(header, 'test_operation_code')
        assert not hasattr(header, 'test_operation_name')
    
    def test_core_fields_match_csharp(self):
        """Validate core fields match C# ReportHeader structure"""
        test_uuid = UUID('12345678-1234-1234-1234-123456789012')
        test_time = datetime.now()
        
        header = ReportHeader(
            uuid=test_uuid,  # Field is called 'uuid' not 'id'
            serial_number="SN12345",
            part_number="PN12345",
            revision="A",
            result="P",  # C# uses string: "P" (Pass), "F" (Fail)
            report_type="T",
            process_code=100,
            process_name="End of line test",
            station_name="Station1",
            location="Building A",
            purpose="Production",
            start_utc=test_time,
            execution_time=10.5
        )
        
        # Validate all fields match C# API
        assert header.uuid == test_uuid
        assert header.serial_number == "SN12345"
        assert header.part_number == "PN12345"
        assert header.revision == "A"
        assert header.result == "P"  # C# uses 'Result' (string)
        assert header.report_type == "T"
        assert header.process_code == 100
        assert header.process_name == "End of line test"
        assert header.station_name == "Station1"
        assert header.location == "Building A"
        assert header.purpose == "Production"
        assert header.start_utc == test_time
        assert header.execution_time == 10.5
    
    def test_result_field_serialization(self):
        """Validate 'result' field serializes correctly (not 'status')"""
        header = ReportHeader(
            uuid=UUID('12345678-1234-1234-1234-123456789012'),
            result="P"  # String value: P (Pass), F (Fail)
        )
        
        # Serialize to dict
        data = header.model_dump(by_alias=True)
        
        # Should have 'result' key
        assert 'result' in data
        assert data['result'] == "P"
        
        # Should NOT have 'status' key
        assert 'status' not in data
    
    def test_create_from_api_response(self):
        """Test creating ReportHeader from C#-style API response"""
        # Simulate C# API response (uses 'result' not 'status')
        api_data = {
            'id': '12345678-1234-1234-1234-123456789012',
            'serialNumber': 'SN12345',
            'partNumber': 'PN12345',
            'revision': 'A',
            'result': 'P',  # C# API uses 'result' (string: P/F)
            'reportType': 'T',
            'processCode': 100,
            'processName': 'End of line test',
            'stationName': 'Station1',
            'location': 'Building A',
            'purpose': 'Production'
        }
        
        # Should parse correctly
        header = ReportHeader(**api_data)
        
        assert header.serial_number == 'SN12345'
        assert header.result == 'P'
        assert header.process_code == 100
        assert header.process_name == 'End of line test'


class TestReportHeaderUURArchitecture:
    """Test UUR dual-process architecture understanding"""
    
    def test_uur_header_has_repair_process_code(self):
        """For UUR reports, ReportHeader.process_code is the REPAIR operation
        
        In UUR architecture:
        - ReportHeader.process_code = Repair operation (500, 510, etc.)
        - UURInfo.process_code = Test operation that was running (100, 50, etc.)
        
        ReportHeader does NOT have test_operation_code.
        """
        # UUR report header has repair operation in process_code
        uur_header = ReportHeader(
            uuid=UUID('12345678-1234-1234-1234-123456789012'),
            process_code=500,  # Repair operation
            process_name="Repair",
            report_type="R"  # UUR type
        )
        
        assert uur_header.process_code == 500  # Repair code
        assert uur_header.process_name == "Repair"
        
        # Should NOT have test_operation_code (that's in UURInfo, not header)
        assert not hasattr(uur_header, 'test_operation_code')
    
    def test_uut_header_has_test_process_code(self):
        """For UUT reports, ReportHeader.process_code is the TEST operation"""
        # UUT report header has test operation in process_code
        uut_header = ReportHeader(
            uuid=UUID('12345678-1234-1234-1234-123456789012'),
            process_code=100,  # Test operation
            process_name="End of line test",
            report_type="T"  # UUT type
        )
        
        assert uut_header.process_code == 100  # Test code
        assert uut_header.process_name == "End of line test"
