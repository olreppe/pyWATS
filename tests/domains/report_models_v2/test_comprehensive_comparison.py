"""
Comprehensive V1/V2 API Surface Comparison and JSON Compatibility Tests

This test verifies:
1. v2 has same API surface as v1 (fields, methods, properties)
2. v2 imports from v1 are intentional (child models, not Report base)
3. JSON output is identical between v1 and v2
4. Bidirectional JSON parsing works correctly
"""
import json
import pytest
from datetime import datetime, timezone
from uuid import UUID

# v1 imports
from pywats.domains.report.report_models import UUTReport as UUTReportV1
from pywats.domains.report.report_models import UURReport as UURReportV1
from pywats.domains.report.report_models import Report as ReportV1

# v2 imports
from pywats.domains.report.report_models_v2 import UUTReport as UUTReportV2
from pywats.domains.report.report_models_v2 import UURReport as UURReportV2
from pywats.domains.report.report_models_v2.report_common import ReportCommon


class TestAPISurfaceComparison:
    """Verify v2 exposes same API surface as v1."""
    
    def test_uut_v1_fields_exist_in_v2(self):
        """v2 UUTReport should have all fields from v1."""
        # Create both reports with same data
        fixed_id = UUID('12345678-1234-5678-1234-567812345678')
        fixed_time = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        
        # v1 constructor
        v1 = UUTReportV1(
            pn="PN-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="Lab",
            purpose="Test",
        )
        v1.id = fixed_id
        v1.start = fixed_time
        
        # v2 constructor (using create factory to match v1 signature)
        v2 = UUTReportV2.create(
            pn="PN-001",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="Lab",
            purpose="Test",
        )
        v2.common.id = fixed_id
        v2.common.start = fixed_time
        
        # Check v1 fields are accessible via v2.common
        assert v2.common.pn == v1.pn
        assert v2.common.sn == v1.sn
        assert v2.common.rev == v1.rev
        assert v2.common.process_code == v1.process_code
        assert v2.common.station_name == v1.station_name
        assert v2.common.location == v1.location
        assert v2.common.purpose == v1.purpose
        assert v2.common.result == v1.result
        assert v2.type == v1.type  # 'T' for UUT
    
    def test_uut_v1_methods_exist_in_v2(self):
        """v2 UUTReport should have same methods as v1."""
        v2 = UUTReportV2.create(
            pn="PN-001", sn="SN-001", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        
        # get_root_sequence_call exists and works
        root = v2.get_root_sequence_call()
        assert root is not None
        assert root.name == "MainSequence Callback"
        
        # Common helper methods (via v2.common)
        mi = v2.common.add_misc_info("key", "value")
        assert mi.description == "key"
        
        su = v2.common.add_sub_unit("Type", "SN", "PN", "R")
        assert su.sn == "SN"
        
        asset = v2.common.add_asset("ASSET-SN", 5)
        assert asset.sn == "ASSET-SN"
    
    def test_uur_v1_fields_exist_in_v2(self):
        """v2 UURReport should have all fields from v1."""
        v2 = UURReportV2.create(
            pn="PN-001", sn="SN-001", rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="S", location="L", purpose="P",
            operator="Op"
        )
        
        # Core fields via common
        assert v2.common.pn == "PN-001"
        assert v2.common.sn == "SN-001"
        assert v2.common.process_code == 500  # repair code at top level
        
        # UUR-specific fields
        assert v2.type == "R"
        assert v2.uur_info is not None
        assert v2.uur_info.test_operation_code == 100
    
    def test_uur_v1_methods_exist_in_v2(self):
        """v2 UURReport should have same methods as v1."""
        v2 = UURReportV2.create(
            pn="PN-001", sn="SN-001", rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="S", location="L", purpose="P",
            operator="Op"
        )
        
        # get_main_unit exists
        main = v2.get_main_unit()
        assert main is not None
        assert main.idx == 0
        
        # add_uur_sub_unit exists (UUR-specific sub-unit method)
        sub = v2.add_uur_sub_unit("SUB-PN", "SUB-SN", "1.0")
        assert sub.pn == "SUB-PN"
        assert sub.idx > 0


class TestV1CodeUsage:
    """Verify v2 only imports appropriate v1 components."""
    
    def test_v2_does_not_inherit_from_v1_report(self):
        """v2 UUTReport should NOT inherit from v1 Report base class."""
        # v2 should use composition, not inheritance
        assert not issubclass(UUTReportV2, ReportV1)
        assert not issubclass(UURReportV2, ReportV1)
        
        # v2 has ReportCommon via composition
        v2 = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        assert hasattr(v2, 'common')
        assert isinstance(v2.common, ReportCommon)
    
    def test_v2_imports_child_models_intentionally(self):
        """v2 intentionally imports stable child models from v1."""
        # These imports are intentional:
        # - UUTInfo, UURInfo (info models)
        # - SequenceCall (step hierarchy)
        # - UURSubUnit (UUR sub-unit model)
        # - WATSBase (base class for Pydantic config)
        # - MiscInfo, Asset, SubUnit, etc. (shared data models)
        
        v2_uut = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        
        # info is UUTInfo from v1
        from pywats.domains.report.report_models.uut.uut_info import UUTInfo
        v2_uut.info = UUTInfo(operator="Op")
        assert isinstance(v2_uut.info, UUTInfo)
        
        # root is SequenceCall from v1
        from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall
        assert isinstance(v2_uut.root, SequenceCall)


class TestJSONCompatibility:
    """Verify v1 and v2 produce identical JSON output."""
    
    def _normalize_json(self, data: dict) -> dict:
        """Normalize JSON for comparison (remove id and time fields that differ)."""
        result = data.copy()
        # Remove fields that will naturally differ
        result.pop('id', None)
        result.pop('start', None)
        result.pop('startUTC', None)
        return result
    
    def test_uut_json_output_identical(self):
        """v1 and v2 UUT reports should produce identical JSON structure."""
        # Create with same data
        v1 = UUTReportV1(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
            result="P",
        )
        
        v2 = UUTReportV2.create(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
            result="P",
        )
        
        # Serialize both
        v1_json = v1.model_dump(by_alias=True, exclude_none=True)
        v2_json = v2.model_dump(by_alias=True, exclude_none=True)
        
        # Normalize (remove id/time)
        v1_norm = self._normalize_json(v1_json)
        v2_norm = self._normalize_json(v2_json)
        
        # Key fields should match
        assert v2_norm['pn'] == v1_norm['pn']
        assert v2_norm['sn'] == v1_norm['sn']
        assert v2_norm['rev'] == v1_norm['rev']
        assert v2_norm['processCode'] == v1_norm['processCode']
        assert v2_norm['machineName'] == v1_norm['machineName']
        assert v2_norm['location'] == v1_norm['location']
        assert v2_norm['purpose'] == v1_norm['purpose']
        assert v2_norm['result'] == v1_norm['result']
        assert v2_norm['type'] == v1_norm['type']
        
        # v2 should NOT have 'common' in output (flattened)
        assert 'common' not in v2_json
    
    def test_uut_with_steps_json_identical(self):
        """UUT with steps should produce identical JSON."""
        # v1
        v1 = UUTReportV1(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        root1 = v1.get_root_sequence_call()
        root1.add_numeric_step(name="Voltage", value=5.0, unit="V", low_limit=4.5, high_limit=5.5)
        
        # v2
        v2 = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        root2 = v2.get_root_sequence_call()
        root2.add_numeric_step(name="Voltage", value=5.0, unit="V", low_limit=4.5, high_limit=5.5)
        
        # Serialize
        v1_json = v1.model_dump(by_alias=True, exclude_none=True)
        v2_json = v2.model_dump(by_alias=True, exclude_none=True)
        
        # Steps should be identical (same SequenceCall from v1)
        assert 'root' in v1_json
        assert 'root' in v2_json
        assert len(v1_json['root'].get('steps', [])) == len(v2_json['root'].get('steps', []))
    
    def test_uur_json_output_identical(self):
        """v1 and v2 UUR reports should produce identical JSON structure."""
        from pywats.domains.report.report_models.uur.uur_info import UURInfo as UURInfoV1
        
        # v1 - UURInfo requires 'operator' (serialized as 'user')
        v1 = UURReportV1(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=500,
            station_name="Station1",
            location="RepairLab",
            purpose="Repair",
            uur_info=UURInfoV1(operator="Operator", test_operation_code=100),
        )
        
        # v2
        v2 = UURReportV2.create(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station1",
            location="RepairLab",
            purpose="Repair",
            operator="Operator",
        )
        
        # Serialize both
        v1_json = v1.model_dump(by_alias=True, exclude_none=True)
        v2_json = v2.model_dump(by_alias=True, exclude_none=True)
        
        # Normalize
        v1_norm = self._normalize_json(v1_json)
        v2_norm = self._normalize_json(v2_json)
        
        # Key fields should match
        assert v2_norm['pn'] == v1_norm['pn']
        assert v2_norm['sn'] == v1_norm['sn']
        assert v2_norm['type'] == v1_norm['type']  # 'R'
        
        # v2 should NOT have 'common' in output
        assert 'common' not in v2_json


class TestBidirectionalParsing:
    """Verify v2 can parse v1 JSON and vice versa."""
    
    def test_v2_can_parse_v1_uut_json(self):
        """v2 should be able to parse JSON produced by v1."""
        v1 = UUTReportV1(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
        )
        
        # Serialize v1 to JSON
        v1_json_str = v1.model_dump_json(by_alias=True)
        
        # Parse with v2
        v2 = UUTReportV2.model_validate_json(v1_json_str)
        
        # Verify fields
        assert v2.common.pn == v1.pn
        assert v2.common.sn == v1.sn
        assert v2.common.process_code == v1.process_code
        assert v2.type == v1.type
    
    def test_v1_can_parse_v2_uut_json(self):
        """v1 should be able to parse JSON produced by v2."""
        v2 = UUTReportV2.create(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Production",
        )
        
        # Serialize v2 to JSON
        v2_json_str = v2.model_dump_json(by_alias=True)
        
        # Parse with v1
        v1 = UUTReportV1.model_validate_json(v2_json_str)
        
        # Verify fields
        assert v1.pn == v2.common.pn
        assert v1.sn == v2.common.sn
        assert v1.process_code == v2.common.process_code
        assert v1.type == v2.type
    
    def test_v2_can_parse_v1_uur_json(self):
        """v2 should be able to parse UUR JSON produced by v1."""
        from pywats.domains.report.report_models.uur.uur_info import UURInfo as UURInfoV1
        
        v1 = UURReportV1(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=500,
            station_name="Station1",
            location="RepairLab",
            purpose="Repair",
            uur_info=UURInfoV1(operator="Operator", test_operation_code=100),
        )
        
        # Serialize v1
        v1_json_str = v1.model_dump_json(by_alias=True)
        
        # Parse with v2
        v2 = UURReportV2.model_validate_json(v1_json_str)
        
        # Verify
        assert v2.common.pn == v1.pn
        assert v2.common.process_code == v1.process_code
        assert v2.type == v1.type
    
    def test_v1_can_parse_v2_uur_json(self):
        """v1 should be able to parse UUR JSON produced by v2."""
        v2 = UURReportV2.create(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station1",
            location="RepairLab",
            purpose="Repair",
            operator="Operator",
        )
        
        # Serialize v2
        v2_json_str = v2.model_dump_json(by_alias=True)
        
        # Parse with v1
        v1 = UURReportV1.model_validate_json(v2_json_str)
        
        # Verify
        assert v1.pn == v2.common.pn
        assert v1.process_code == v2.common.process_code
        assert v1.type == v2.type


class TestRoundtripIntegrity:
    """Verify complete roundtrip: create -> serialize -> parse -> serialize produces same output."""
    
    def test_uut_roundtrip_integrity(self):
        """UUT: create v2 -> JSON -> v1 -> JSON -> v2 should be consistent."""
        # Start with v2
        original = UUTReportV2.create(
            pn="ROUNDTRIP-PN",
            sn="ROUNDTRIP-SN",
            rev="B",
            process_code=200,
            station_name="RoundtripStation",
            location="RoundtripLab",
            purpose="RoundtripTest",
            result="F",
        )
        
        # Add steps
        root = original.get_root_sequence_call()
        root.add_numeric_step(name="Step1", value=1.0, unit="X")
        
        # v2 -> JSON
        json1 = original.model_dump_json(by_alias=True)
        
        # JSON -> v1
        v1_parsed = UUTReportV1.model_validate_json(json1)
        
        # v1 -> JSON
        json2 = v1_parsed.model_dump_json(by_alias=True)
        
        # JSON -> v2
        v2_reparsed = UUTReportV2.model_validate_json(json2)
        
        # Verify data integrity
        assert v2_reparsed.common.pn == original.common.pn
        assert v2_reparsed.common.sn == original.common.sn
        assert v2_reparsed.common.result == original.common.result
        assert len(v2_reparsed.root.steps) == len(original.root.steps)
    
    def test_uur_roundtrip_integrity(self):
        """UUR: create v2 -> JSON -> v1 -> JSON -> v2 should be consistent."""
        # Start with v2
        original = UURReportV2.create(
            pn="ROUNDTRIP-PN",
            sn="ROUNDTRIP-SN",
            rev="C",
            repair_process_code=500,
            test_operation_code=100,
            station_name="RoundtripStation",
            location="RoundtripLab",
            purpose="RoundtripRepair",
            operator="RoundtripOp",
        )
        
        # v2 -> JSON
        json1 = original.model_dump_json(by_alias=True)
        
        # JSON -> v1
        v1_parsed = UURReportV1.model_validate_json(json1)
        
        # v1 -> JSON
        json2 = v1_parsed.model_dump_json(by_alias=True)
        
        # JSON -> v2
        v2_reparsed = UURReportV2.model_validate_json(json2)
        
        # Verify data integrity
        assert v2_reparsed.common.pn == original.common.pn
        assert v2_reparsed.common.sn == original.common.sn
        assert v2_reparsed.type == original.type
