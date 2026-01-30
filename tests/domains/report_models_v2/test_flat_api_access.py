"""
Tests for flat API access via ReportProxyMixin.

Verifies that v2 reports can be accessed with flat API like v1:
    report.pn           # Works (v1 compatible)
    report.common.pn    # Also works (explicit composition)
"""

import pytest
from datetime import datetime, timezone
from uuid import UUID, uuid4

from pywats.domains.report.report_models_v2 import (
    UUTReport,
    UURReport,
    ReportCommon,
)
from pywats.domains.report.report_models.uur.uur_info import UURInfo


class TestUUTFlatAPIConstruction:
    """Test that UUTReport can be constructed with flat fields (v1 compatible)."""
    
    def test_flat_constructor(self):
        """UUTReport can be created with flat fields (no explicit common)."""
        report = UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
        )
        
        # Verify flat access works
        assert report.pn == "PART-001"
        assert report.sn == "SERIAL-001"
        assert report.rev == "A"
        assert report.process_code == 100
        assert report.station_name == "Station1"
        assert report.location == "TestLab"
        assert report.purpose == "Development"
        
        # Verify common access also works
        assert report.common.pn == "PART-001"
        assert report.common.sn == "SERIAL-001"
    
    def test_flat_constructor_with_result(self):
        """UUTReport flat constructor accepts result field."""
        report = UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
            result="F",
        )
        
        assert report.result == "F"
        assert report.common.result == "F"
    
    def test_flat_constructor_with_start_time(self):
        """UUTReport flat constructor accepts timing fields."""
        start = datetime.now(timezone.utc)
        
        report = UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
            start=start,
        )
        
        assert report.start == start
        assert report.start_utc is not None


class TestUUTFlatAPIAccess:
    """Test flat field access via property proxies."""
    
    @pytest.fixture
    def uut_report(self) -> UUTReport:
        """Create a UUTReport for testing."""
        return UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
        )
    
    def test_read_identity_fields(self, uut_report):
        """Can read identity fields via flat API."""
        assert isinstance(uut_report.id, UUID)
        assert uut_report.pn == "PART-001"
        assert uut_report.sn == "SERIAL-001"
        assert uut_report.rev == "A"
        assert uut_report.process_code == 100
    
    def test_write_identity_fields(self, uut_report):
        """Can write identity fields via flat API."""
        uut_report.pn = "NEW-PART"
        uut_report.sn = "NEW-SERIAL"
        
        assert uut_report.pn == "NEW-PART"
        assert uut_report.common.pn == "NEW-PART"
        assert uut_report.sn == "NEW-SERIAL"
        assert uut_report.common.sn == "NEW-SERIAL"
    
    def test_read_station_fields(self, uut_report):
        """Can read station info fields via flat API."""
        assert uut_report.station_name == "Station1"
        assert uut_report.location == "TestLab"
        assert uut_report.purpose == "Development"
    
    def test_write_station_fields(self, uut_report):
        """Can write station info fields via flat API."""
        uut_report.station_name = "NewStation"
        uut_report.location = "NewLab"
        
        assert uut_report.station_name == "NewStation"
        assert uut_report.common.station_name == "NewStation"
    
    def test_read_collections(self, uut_report):
        """Can read collections via flat API."""
        assert uut_report.misc_infos == []
        assert uut_report.assets == []
        assert uut_report.misc_info_list == []  # v1 alias
        assert uut_report.asset_list == []  # v1 alias
    
    def test_helper_methods_via_flat_api(self, uut_report):
        """Helper methods work via flat API."""
        # add_misc_info
        mi = uut_report.add_misc_info("Key", "Value")
        assert len(uut_report.misc_infos) == 1
        assert uut_report.misc_info_list[0] == mi
        
        # add_asset
        asset = uut_report.add_asset("ASSET-001", 5)
        assert len(uut_report.assets) == 1
        assert uut_report.asset_list[0] == asset


class TestUURFlatAPIConstruction:
    """Test that UURReport can be constructed with flat fields (v1 compatible)."""
    
    def test_flat_constructor(self):
        """UURReport can be created with flat fields (no explicit common)."""
        report = UURReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="RepairLab",
            purpose="Repair",
            uur_info=UURInfo(operator="John", test_operation_code=100),
        )
        
        # Verify flat access works
        assert report.pn == "PART-001"
        assert report.sn == "SERIAL-001"
        assert report.process_code == 500
        
        # Verify common access also works
        assert report.common.pn == "PART-001"
        assert report.common.process_code == 500


class TestUURFlatAPIAccess:
    """Test flat field access via property proxies for UURReport."""
    
    @pytest.fixture
    def uur_report(self) -> UURReport:
        """Create a UURReport for testing."""
        return UURReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="RepairLab",
            purpose="Repair",
            uur_info=UURInfo(operator="John", test_operation_code=100),
        )
    
    def test_read_identity_fields(self, uur_report):
        """Can read identity fields via flat API."""
        assert uur_report.pn == "PART-001"
        assert uur_report.sn == "SERIAL-001"
        assert uur_report.process_code == 500
    
    def test_write_identity_fields(self, uur_report):
        """Can write identity fields via flat API."""
        uur_report.pn = "NEW-PART"
        
        assert uur_report.pn == "NEW-PART"
        assert uur_report.common.pn == "NEW-PART"
    
    def test_helper_methods_via_flat_api(self, uur_report):
        """Helper methods work via flat API."""
        mi = uur_report.add_misc_info("RepairNote", "Fixed capacitor")
        assert len(uur_report.misc_infos) == 1


class TestFlatAPIJSONCompatibility:
    """Test that flat API constructed reports produce correct JSON."""
    
    def test_flat_constructed_uut_json_matches_factory(self):
        """Flat constructor and factory produce identical JSON structure."""
        # Flat constructor
        flat = UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
        )
        
        # Factory method
        factory = UUTReport.create(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
        )
        
        # Exclude dynamic fields (id, timestamps) for comparison
        exclude_fields = {'id', 'start', 'start_utc', 'startUTC'}
        flat_data = {k: v for k, v in flat.model_dump().items() if k not in exclude_fields}
        factory_data = {k: v for k, v in factory.model_dump().items() if k not in exclude_fields}
        
        assert flat_data == factory_data
    
    def test_flat_constructor_json_is_flat(self):
        """JSON from flat-constructed report is flat (no 'common' key)."""
        report = UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
        )
        
        data = report.model_dump()
        
        # Should NOT have 'common' key - it's flattened
        assert 'common' not in data
        
        # Should have flat fields at top level
        assert data['pn'] == "PART-001"
        assert data['sn'] == "SERIAL-001"
        # model_dump uses by_alias=False by default, so use Python field names
        assert data['process_code'] == 100


class TestBothAccessPatternsWork:
    """Verify that both access patterns work interchangeably."""
    
    def test_read_via_both_patterns(self):
        """Both report.pn and report.common.pn return same value."""
        report = UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
        )
        
        # Both patterns return same value
        assert report.pn == report.common.pn
        assert report.sn == report.common.sn
        assert report.process_code == report.common.process_code
    
    def test_write_via_flat_reflects_in_common(self):
        """Writing via flat API reflects in common."""
        report = UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
        )
        
        report.pn = "NEW-PART"
        assert report.common.pn == "NEW-PART"
    
    def test_write_via_common_reflects_in_flat(self):
        """Writing via common reflects in flat API."""
        report = UUTReport(
            pn="PART-001",
            sn="SERIAL-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development",
        )
        
        report.common.pn = "COMMON-PART"
        assert report.pn == "COMMON-PART"
