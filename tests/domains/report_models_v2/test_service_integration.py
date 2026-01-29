"""Integration tests for v2 reports with async_service.

Tests that v2 UUTReport and UURReport work correctly with the AsyncReportService
factory methods and can be submitted to WATS.
"""
import pytest
from datetime import datetime
from uuid import uuid4

# v2 imports
from pywats.domains.report.report_models_v2 import UUTReport as UUTReportV2
from pywats.domains.report.report_models_v2 import UURReport as UURReportV2
from pywats.domains.report.report_models_v2.report_common import ReportCommon

# v1 imports for comparison
from pywats.domains.report.report_models import UUTReport as UUTReportV1
from pywats.domains.report.report_models import UURReport as UURReportV1


class TestV2ServiceIntegration:
    """Test that v2 reports integrate with service patterns."""
    
    def test_v2_uut_can_be_created_like_v1(self):
        """Test that v2 UUTReport can be created using same pattern as service uses."""
        # This is how async_service creates UUTReport (line 122-132)
        # We need v2 to support this exact pattern
        
        # v1 pattern (what service currently does)
        v1_report = UUTReportV1(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
            result="P",
            start=datetime.now().astimezone(),
        )
        
        # v2 should support the same flat constructor pattern
        # Currently v2 requires: UUTReportV2(common=ReportCommon(...))
        # But async_service uses flat fields
        
        # Test via factory method (create)
        v2_report = UUTReportV2.create(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
            result="P",
            start=datetime.now().astimezone(),
        )
        
        # Verify fields are accessible at top level
        assert v2_report.common.pn == "PART-001"
        assert v2_report.common.sn == "SN-001"
        assert v2_report.type == "T"
    
    def test_v2_uut_json_matches_v1(self):
        """Test that v2 JSON output matches v1 format (flat structure)."""
        v1_report = UUTReportV1(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
        )
        
        v2_report = UUTReportV2.create(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
        )
        
        # Serialize both
        v1_data = v1_report.model_dump(by_alias=True, exclude_none=True)
        v2_data = v2_report.model_dump(by_alias=True, exclude_none=True)
        
        # Check key fields match (ignore id which is different)
        assert v2_data['pn'] == v1_data['pn']
        assert v2_data['sn'] == v1_data['sn']
        assert v2_data['processCode'] == v1_data['processCode']
        assert v2_data['machineName'] == v1_data['machineName']
        
        # Verify no 'common' key in serialized output
        assert 'common' not in v2_data, "v2 should flatten common fields in JSON"
    
    def test_v2_can_parse_v1_json_format(self):
        """Test that v2 can parse JSON produced by v1."""
        v1_report = UUTReportV1(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
        )
        
        # Serialize v1
        v1_json = v1_report.model_dump_json(by_alias=True)
        
        # Parse with v2
        v2_report = UUTReportV2.model_validate_json(v1_json)
        
        # Verify fields
        assert v2_report.common.pn == "PART-001"
        assert v2_report.common.sn == "SN-001"
        assert v2_report.type == "T"
    
    def test_v2_get_root_sequence_call(self):
        """Test that get_root_sequence_call works like v1."""
        v2_report = UUTReportV2.create(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
        )
        
        root = v2_report.get_root_sequence_call()
        
        assert root is not None
        assert root.name == "MainSequence Callback"
    
    def test_v2_add_steps(self):
        """Test adding steps to v2 report."""
        v2_report = UUTReportV2.create(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
        )
        
        root = v2_report.get_root_sequence_call()
        
        # Add steps (using v1 step methods - imported from v1)
        step = root.add_numeric_step(
            name="Voltage Test",
            value=5.0,
            unit="V",
            low_limit=4.5,
            high_limit=5.5
        )
        
        # Verify step was added
        assert len(root.steps) == 1
        assert root.steps[0].name == "Voltage Test"


class TestV2UURIntegration:
    """Test that v2 UURReport integrates correctly."""
    
    def test_v2_uur_can_be_created(self):
        """Test basic UUR v2 creation."""
        v2_uur = UURReportV2.create(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            repair_process_code=500,  # Repair process code
            test_operation_code=100,  # Original test that failed
            station_name="RepairStation",
            location="RepairLab",
            purpose="Repair",
            operator="TestOperator",
        )
        
        assert v2_uur.type == "R"
        assert v2_uur.common.pn == "PART-001"
    
    def test_v2_uur_dual_process_codes(self):
        """Test UUR dual process code architecture."""
        v2_uur = UURReportV2.create(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            repair_process_code=500,  # Repair process code (top-level)
            test_operation_code=100,  # Original test that failed
            station_name="RepairStation",
            location="RepairLab",
            purpose="Repair",
            operator="RepairTech",
        )
        
        # Verify dual process codes are set correctly
        assert v2_uur.common.process_code == 500  # Repair code at top level
        assert v2_uur.uur_info.test_operation_code == 100  # Original test code


class TestServiceCompatibility:
    """Test that v2 can work as drop-in for async_service if needed."""
    
    def test_v2_supports_flat_constructor_via_model_validate(self):
        """Test that v2 can parse flat field dict (like service would create)."""
        # This simulates what async_service does internally
        flat_data = {
            'pn': 'PART-001',
            'sn': 'SN-001',
            'rev': 'A',
            'process_code': 100,
            'station_name': 'Station1',
            'location': 'TestLab',
            'purpose': 'Production',
            'result': 'P',
            'type': 'T',
        }
        
        # v2 should handle this via model_validate
        v2_report = UUTReportV2.model_validate(flat_data)
        
        assert v2_report.common.pn == 'PART-001'
        assert v2_report.common.sn == 'SN-001'
        assert v2_report.type == 'T'
    
    def test_v2_with_info_field(self):
        """Test that info field works correctly."""
        from pywats.domains.report.report_models.uut.uut_info import UUTInfo
        
        v2_report = UUTReportV2.create(
            pn="PART-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
        )
        
        # Set info like service does
        v2_report.info = UUTInfo(operator="TestOperator")
        
        assert v2_report.info is not None
        assert v2_report.info.operator == "TestOperator"
        
        # Verify it serializes correctly (operator -> user alias)
        data = v2_report.model_dump(by_alias=True)
        assert 'uut' in data
        assert data['uut']['user'] == "TestOperator"  # 'user' is the serialization alias for 'operator'
