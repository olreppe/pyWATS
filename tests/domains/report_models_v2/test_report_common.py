"""
Unit tests for ReportCommon (v2 composition model)

Tests:
- Field validation (PN/SN problematic characters)
- Time synchronization (start <-> start_utc)
- Helper methods (add_misc_info, add_sub_unit, add_asset)
- Serialization/deserialization
- List fields (never None, always list)
"""

import pytest
from datetime import datetime, timezone
from uuid import UUID

from pywats.domains.report.report_models_v2.report_common import ReportCommon
from pywats.domains.report.report_models.misc_info import MiscInfo
from pywats.domains.report.report_models.sub_unit import SubUnit
from pywats.domains.report.report_models.asset import Asset


class TestReportCommonBasicFields:
    """Test basic field creation and validation."""
    
    def test_create_minimal_report_common(self):
        """Test creating with minimal required fields."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        assert rc.pn == "ABC123"
        assert rc.sn == "SN-001"
        assert rc.rev == "A"
        assert rc.process_code == 100
        assert rc.station_name == "Station1"
        assert rc.location == "TestLab"
        assert rc.purpose == "Development"
        assert rc.result == "P"  # Default
        assert isinstance(rc.id, UUID)
    
    def test_collections_are_always_lists(self):
        """Verify list fields are never None (clean pattern)."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        # Collections should be empty lists, NOT None
        assert rc.misc_infos == []
        assert rc.sub_units == []
        assert rc.assets == []
        assert rc.binary_data == []
        assert rc.additional_data == []
        
        # Type assertions
        assert isinstance(rc.misc_infos, list)
        assert isinstance(rc.sub_units, list)
        assert isinstance(rc.assets, list)


class TestReportCommonValidation:
    """Test PN/SN validation for problematic characters."""
    
    def test_valid_pn_sn(self):
        """Test that valid PN/SN pass validation."""
        rc = ReportCommon(
            pn="ABC-123_456",
            sn="SN.2024.001",
            rev="B",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        assert rc.pn == "ABC-123_456"
        assert rc.sn == "SN.2024.001"
    
    def test_problematic_pn_raises_error(self):
        """Test that problematic characters in PN raise validation error."""
        from pywats.core.validation import ReportHeaderValidationError
        
        with pytest.raises(ReportHeaderValidationError, match="contains problematic character"):
            ReportCommon(
                pn="ABC*123",  # * is problematic
                sn="SN-001",
                rev="A",
                process_code=100,
                station_name="Station1",
                location="TestLab",
                purpose="Development"
            )
    
    def test_problematic_sn_raises_error(self):
        """Test that problematic characters in SN raise validation error."""
        from pywats.core.validation import ReportHeaderValidationError
        
        with pytest.raises(ReportHeaderValidationError, match="contains problematic character"):
            ReportCommon(
                pn="ABC123",
                sn="SN%001",  # % is problematic
                rev="A",
                process_code=100,
                station_name="Station1",
                location="TestLab",
                purpose="Development"
            )
    
    def test_suppress_prefix_bypasses_validation(self):
        """Test that SUPPRESS: prefix bypasses validation."""
        rc = ReportCommon(
            pn="SUPPRESS:ABC*123",
            sn="SUPPRESS:SN%001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        assert rc.pn == "ABC*123"  # Prefix removed, * allowed
        assert rc.sn == "SN%001"   # Prefix removed, % allowed


class TestReportCommonTimeSync:
    """Test start/start_utc synchronization."""
    
    def test_both_times_none_defaults_to_current(self):
        """When neither time is set, defaults to current time."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        assert rc.start is not None
        assert rc.start_utc is not None
        assert rc.start.tzinfo is not None  # Timezone-aware
        assert rc.start_utc.tzinfo == timezone.utc
    
    def test_only_start_set_computes_utc(self):
        """When only start is set, start_utc is computed."""
        local_time = datetime.now().astimezone()
        
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
            start=local_time
        )
        
        assert rc.start == local_time
        assert rc.start_utc is not None
        assert rc.start_utc == local_time.astimezone(timezone.utc)
    
    def test_only_start_utc_set_computes_local(self):
        """When only start_utc is set, start is computed."""
        utc_time = datetime.now(timezone.utc)
        
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
            start_utc=utc_time
        )
        
        assert rc.start_utc == utc_time
        assert rc.start is not None
        assert rc.start == utc_time.astimezone()


class TestReportCommonHelperMethods:
    """Test helper methods for adding misc_info, sub_units, assets."""
    
    def test_add_misc_info(self):
        """Test adding miscellaneous information."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        mi = rc.add_misc_info("Operator", "John Doe")
        
        assert len(rc.misc_infos) == 1
        assert rc.misc_infos[0] == mi
        assert mi.description == "Operator"
        assert mi.string_value == "John Doe"
    
    def test_add_sub_unit(self):
        """Test adding a sub-unit."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        su = rc.add_sub_unit(
            part_type="PCB",
            sn="PCB-001",
            pn="PCB-ABC",
            rev="1.0"
        )
        
        assert len(rc.sub_units) == 1
        assert rc.sub_units[0] == su
        assert su.part_type == "PCB"
        assert su.sn == "PCB-001"
    
    def test_add_asset(self):
        """Test adding an asset."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        asset = rc.add_asset(sn="DMM-001", usage_count=5)
        
        assert len(rc.assets) == 1
        assert rc.assets[0] == asset
        assert asset.sn == "DMM-001"
        assert asset.usage_count == 5


class TestReportCommonSerialization:
    """Test JSON serialization/deserialization."""
    
    def test_serialization_excludes_computed_fields(self):
        """Test that start_utc and other exclude=True fields are not serialized."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        json_dict = rc.model_dump(mode='json', by_alias=True)
        
        # start_utc should be excluded
        assert "startUTC" not in json_dict
        assert "start_utc" not in json_dict
        
        # Output-only fields should be excluded
        assert "origin" not in json_dict
        assert "productName" not in json_dict
        assert "processName" not in json_dict
    
    def test_serialization_uses_aliases(self):
        """Test that serialization uses the correct aliases."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        json_dict = rc.model_dump(mode='json', by_alias=True)
        
        # Check aliases are used
        assert "processCode" in json_dict
        assert "machineName" in json_dict
        assert "miscInfos" in json_dict
        assert "subUnits" in json_dict
    
    def test_roundtrip_serialization(self):
        """Test that serialization and deserialization preserve data."""
        rc = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        rc.add_misc_info("Operator", "Jane")
        rc.add_sub_unit("PCB", "PCB-001", "PCB-ABC", "1.0")
        
        # Serialize
        json_str = rc.model_dump_json(by_alias=True)
        
        # Deserialize
        rc2 = ReportCommon.model_validate_json(json_str)
        
        assert rc2.pn == rc.pn
        assert rc2.sn == rc.sn
        assert len(rc2.misc_infos) == 1
        assert len(rc2.sub_units) == 1
