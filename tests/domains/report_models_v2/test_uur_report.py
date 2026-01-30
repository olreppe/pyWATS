"""
Tests for UURReport v2 (composition-based)

Verifies:
- Basic creation (constructor + factory)
- Main unit auto-creation
- Sub-unit management
- Dual process code architecture
- create_from_uut() workflow
- Serialization (v1 JSON compatibility)
- Deserialization (flat + nested formats)
"""

import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone

from pywats.domains.report.report_models_v2.uur_report import UURReport
from pywats.domains.report.report_models_v2.uut_report import UUTReport
from pywats.domains.report.report_models_v2.report_common import ReportCommon
from pywats.domains.report.report_models.uur.uur_info import UURInfo
from pywats.domains.report.report_models.uur.uur_sub_unit import UURSubUnit


class TestUURReportCreation:
    """Test basic UURReport creation patterns."""
    
    def test_constructor_pattern(self):
        """Test creating UURReport using constructor."""
        common = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=500,  # Repair code
            station_name="RepairStation",
            location="RepairLab",
            purpose="Repair"
        )
        
        uur_info = UURInfo(
            test_operation_code=100,  # Original test code
            operator="John Doe"
        )
        
        uur = UURReport(common=common, uur_info=uur_info)
        
        assert uur.type == "R"
        assert uur.common.pn == "ABC123"
        assert uur.common.sn == "SN-001"
        assert uur.common.process_code == 500  # Repair code
        assert uur.uur_info.test_operation_code == 100  # Test code
        assert uur.uur_info.operator == "John Doe"
        
    def test_factory_pattern(self):
        """Test creating UURReport using factory method."""
        uur = UURReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="RepairStation",
            location="RepairLab",
            purpose="Repair",
            operator="Jane Doe",
            comment="Replace capacitor"
        )
        
        assert uur.type == "R"
        assert uur.common.pn == "ABC123"
        assert uur.common.process_code == 500
        assert uur.uur_info.test_operation_code == 100
        assert uur.uur_info.operator == "Jane Doe"
        assert uur.uur_info.comment == "Replace capacitor"
        
    def test_main_unit_auto_creation(self):
        """Test that main unit (idx=0) is auto-created."""
        uur = UURReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="RepairStation",
            location="RepairLab",
            purpose="Repair"
        )
        
        # Main unit should exist
        main = uur.get_main_unit()
        assert main.idx == 0
        assert main.pn == "ABC123"
        assert main.sn == "SN-001"
        assert main.rev == "A"


class TestDualProcessCodeArchitecture:
    """Test dual process code handling (repair + test)."""
    
    def test_dual_process_codes(self):
        """Test that UUR correctly stores both repair and test codes."""
        uur = UURReport.create(
            pn="BOARD-X",
            sn="B-001",
            rev="2.0",
            repair_process_code=500,  # Repair operation
            test_operation_code=100,  # Original test operation
            station_name="RepairStation",
            location="Lab",
            purpose="Repair"
        )
        
        # Top-level process_code is repair code
        assert uur.common.process_code == 500
        
        # uur_info stores original test code
        assert uur.uur_info.test_operation_code == 100
        
    def test_different_process_codes(self):
        """Test various repair and test code combinations."""
        test_cases = [
            (500, 100),  # Repair + Functional Test
            (501, 200),  # Rework + Environmental Test
            (502, 300),  # Replace + In-Circuit Test
        ]
        
        for repair_code, test_code in test_cases:
            uur = UURReport.create(
                pn="PART",
                sn="SN",
                rev="A",
                repair_process_code=repair_code,
                test_operation_code=test_code,
                station_name="Station",
                location="Lab",
                purpose="Test"
            )
            
            assert uur.common.process_code == repair_code
            assert uur.uur_info.test_operation_code == test_code


class TestUURFromUUT:
    """Test creating UURReport from failed UUTReport."""
    
    def test_create_from_uut_basic(self):
        """Test creating UUR from UUT."""
        # Create a UUT report that failed
        uut = UUTReport.create(
            pn="BOARD-X",
            sn="B-001",
            rev="2.0",
            process_code=100,
            station_name="TestStation",
            location="TestLab",
            purpose="Final Test"
        )
        uut.common.result = False  # Failed!
        
        # Create UUR from failed UUT
        uur = UURReport.create_from_uut(
            uut,
            repair_process_code=500,
            operator="John Doe",
            comment="Replace capacitor C5"
        )
        
        # Should link to UUT
        assert uur.uur_info.ref_uut == uut.common.id
        
        # Should copy identity
        assert uur.common.id == uut.common.id
        assert uur.common.pn == uut.common.pn
        assert uur.common.sn == uut.common.sn
        assert uur.common.rev == uut.common.rev
        
        # Should have different process codes
        assert uur.common.process_code == 500  # Repair code
        assert uur.uur_info.test_operation_code == 100  # Original test code
        
        # Should preserve operator/comment
        assert uur.uur_info.operator == "John Doe"
        assert uur.uur_info.comment == "Replace capacitor C5"
        
    def test_create_from_uut_with_overrides(self):
        """Test creating UUR from UUT with station overrides."""
        uut = UUTReport.create(
            pn="BOARD-X",
            sn="B-001",
            rev="2.0",
            process_code=100,
            station_name="TestStation",
            location="TestLab",
            purpose="Final Test"
        )
        
        uur = UURReport.create_from_uut(
            uut,
            repair_process_code=500,
            operator="Jane Doe",
            station_name="RepairStation",  # Override
            location="RepairLab",  # Override
            purpose="Repair"  # Override
        )
        
        # Overrides should be applied
        assert uur.common.station_name == "RepairStation"
        assert uur.common.location == "RepairLab"
        assert uur.common.purpose == "Repair"
        
        # But still linked to UUT
        assert uur.uur_info.ref_uut == uut.common.id


class TestSubUnitManagement:
    """Test sub-unit creation and management."""
    
    def test_add_uur_sub_unit(self):
        """Test adding sub-units to UUR."""
        uur = UURReport.create(
            pn="MAIN-BOARD",
            sn="MB-001",
            rev="1.0",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair"
        )
        
        # Add a sub-unit
        sub1 = uur.add_uur_sub_unit(pn="PCB-123", sn="PCB-001", rev="A")
        assert sub1.idx == 1  # First sub-unit after main (idx=0)
        assert sub1.pn == "PCB-123"
        
        # Add another
        sub2 = uur.add_uur_sub_unit(pn="PCB-456", sn="PCB-002", rev="B")
        assert sub2.idx == 2
        
        # Should have 3 total (main + 2 sub-units)
        assert len(uur.sub_units) == 3
        
    def test_main_unit_failures(self):
        """Test adding failures to main unit."""
        uur = UURReport.create(
            pn="BOARD",
            sn="B-001",
            rev="1.0",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair"
        )
        
        # Add failure to main unit
        main = uur.get_main_unit()
        main.add_failure(category="Component", code="CAPACITOR_FAIL")
        
        assert len(main.failures) == 1
        assert main.failures[0].category == "Component"
        assert main.failures[0].code == "CAPACITOR_FAIL"


class TestSerialization:
    """Test v1 JSON compatibility."""
    
    def test_serialization_flattens_common(self):
        """Test that serialization flattens common fields to top level."""
        uur = UURReport.create(
            pn="PART",
            sn="SN-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            operator="John Doe"
        )
        
        data = uur.model_dump()
        
        # Common fields should be at top level
        assert 'pn' in data
        assert 'sn' in data
        assert 'process_code' in data or 'processCode' in data
        assert 'common' not in data  # Should be flattened
        
        # UUR fields should exist
        assert 'uur' in data or 'uur_info' in data
        assert data['type'] == 'R'
        
    def test_roundtrip_serialization(self):
        """Test that UUR can be serialized and deserialized."""
        original = UURReport.create(
            pn="PART",
            sn="SN-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            operator="Jane Doe",
            comment="Replace resistor"
        )
        
        # Serialize to JSON
        json_str = original.model_dump_json()
        
        # Deserialize back
        restored = UURReport.model_validate_json(json_str)
        
        # Should match
        assert restored.common.pn == original.common.pn
        assert restored.common.sn == original.common.sn
        assert restored.common.process_code == original.common.process_code
        assert restored.uur_info.test_operation_code == original.uur_info.test_operation_code
        assert restored.uur_info.operator == original.uur_info.operator
        assert restored.uur_info.comment == original.uur_info.comment
        
    def test_deserialization_handles_flattened(self):
        """Test that deserialization handles v1 flattened format."""
        flat_data = {
            'type': 'R',
            'pn': 'PART',
            'sn': 'SN-001',
            'rev': 'A',
            'processCode': 500,
            'machineName': 'Station',
            'location': 'Lab',
            'purpose': 'Repair',
            'uur': {
                'testOperationCode': 100,
                'operator': 'John Doe'
            }
        }
        
        uur = UURReport.model_validate(flat_data)
        
        assert uur.common.pn == 'PART'
        assert uur.common.sn == 'SN-001'
        assert uur.common.process_code == 500
        assert uur.uur_info.test_operation_code == 100
        assert uur.uur_info.operator == 'John Doe'
        
    def test_deserialization_handles_nested(self):
        """Test that deserialization handles v2 nested format."""
        nested_data = {
            'type': 'R',
            'common': {
                'pn': 'PART',
                'sn': 'SN-001',
                'rev': 'A',
                'process_code': 500,
                'station_name': 'Station',
                'location': 'Lab',
                'purpose': 'Repair'
            },
            'uur_info': {
                'test_operation_code': 100,
                'operator': 'Jane Doe'
            }
        }
        
        uur = UURReport.model_validate(nested_data)
        
        assert uur.common.pn == 'PART'
        assert uur.common.process_code == 500
        assert uur.uur_info.test_operation_code == 100
        assert uur.uur_info.operator == 'Jane Doe'


class TestAttachments:
    """Test attachment handling."""
    
    def test_add_attachments(self):
        """Test adding attachments to UUR."""
        from pywats.domains.report.report_models.attachment import Attachment
        
        uur = UURReport.create(
            pn="PART",
            sn="SN-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair"
        )
        
        # Add attachment
        att = Attachment(
            name="before_repair.jpg",  # Fixed: 'name' not 'filename'
            content_type="image/jpeg",
            data="ZmFrZSBpbWFnZSBkYXRh"  # Fixed: base64 string, not bytes
        )
        uur.attachments.append(att)
        
        assert len(uur.attachments) == 1
        assert uur.attachments[0].name == "before_repair.jpg"  # Fixed: 'name' not 'filename'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
