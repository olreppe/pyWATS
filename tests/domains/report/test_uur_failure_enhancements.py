"""
Tests for enhanced UUR failure API.

Tests the new sub_unit_idx parameter and add_failure_to_sub_unit() method.
"""
import pytest
from pywats.domains.report.report_models.uur.uur_report import UURReport
from pywats.domains.report.report_models.uur.uur_sub_unit import UURSubUnit


class TestUURFailureAPIEnhancements:
    """Test enhanced UUR failure methods."""
    
    def test_add_failure_to_main_unit_default(self):
        """Test add_failure() defaults to main unit (idx=0)."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        # Add failure without sub_unit_idx (should go to main unit)
        failure = uur.add_failure(category="Component", code="CAP_FAIL")
        
        assert failure is not None
        assert failure.category == "Component"
        assert failure.code == "CAP_FAIL"
        
        # Verify failure is on main unit
        main = uur.get_main_unit()
        assert len(main.get_failures()) == 1
        assert main.get_failures()[0] == failure
    
    def test_add_failure_with_sub_unit_idx_zero(self):
        """Test add_failure() with explicit sub_unit_idx=0 (main unit)."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        # Explicitly target main unit
        failure = uur.add_failure(
            category="Component",
            code="CAP_FAIL",
            sub_unit_idx=0
        )
        
        main = uur.get_main_unit()
        assert len(main.get_failures()) == 1
        assert main.get_failures()[0] == failure
    
    def test_add_failure_to_sub_unit_by_idx(self):
        """Test add_failure() with sub_unit_idx for non-main unit."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        # Add a sub-unit
        sub_unit = uur.add_sub_unit(
            pn="SUBWIDGET-001",
            sn="SUB-SN-123",
            rev="B"
        )
        
        # Add failure to sub-unit using sub_unit_idx
        failure = uur.add_failure(
            category="Component",
            code="RES_FAIL",
            component_ref="R10",
            sub_unit_idx=sub_unit.idx
        )
        
        assert failure.category == "Component"
        assert failure.code == "RES_FAIL"
        assert failure.com_ref == "R10"
        
        # Verify failure is on the sub-unit
        assert len(sub_unit.get_failures()) == 1
        assert sub_unit.get_failures()[0] == failure
        
        # Verify main unit has no failures
        main = uur.get_main_unit()
        assert len(main.get_failures()) == 0
    
    def test_add_failure_invalid_sub_unit_idx(self):
        """Test add_failure() raises IndexError for invalid idx."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        # Try to add failure to non-existent sub-unit
        with pytest.raises(IndexError, match="Sub-unit with idx=99 not found"):
            uur.add_failure(
                category="Component",
                code="FAIL",
                sub_unit_idx=99
            )
    
    def test_add_failure_to_sub_unit_by_serial_number(self):
        """Test add_failure_to_sub_unit() with serial_number parameter."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        # Add sub-units
        sub1 = uur.add_sub_unit(pn="SUB-A", sn="SUB-SN-001", rev="1")
        sub2 = uur.add_sub_unit(pn="SUB-B", sn="SUB-SN-002", rev="1")
        
        # Add failure to sub2 by serial number
        failure = uur.add_failure_to_sub_unit(
            category="Component",
            code="IC_FAIL",
            serial_number="SUB-SN-002",
            comment="IC failed verification"
        )
        
        assert failure.category == "Component"
        assert failure.code == "IC_FAIL"
        assert failure.comment == "IC failed verification"
        
        # Verify failure is on sub2
        assert len(sub2.get_failures()) == 1
        assert sub2.get_failures()[0] == failure
        
        # Verify sub1 has no failures
        assert len(sub1.get_failures()) == 0
    
    def test_add_failure_to_sub_unit_by_idx(self):
        """Test add_failure_to_sub_unit() with idx parameter."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        # Add sub-units
        sub1 = uur.add_sub_unit(pn="SUB-A", sn="SUB-SN-001", rev="1")
        sub2 = uur.add_sub_unit(pn="SUB-B", sn="SUB-SN-002", rev="1")
        
        # Add failure to sub1 by idx
        failure = uur.add_failure_to_sub_unit(
            category="Component",
            code="CAP_FAIL",
            idx=sub1.idx,
            component_ref="C5"
        )
        
        assert failure.code == "CAP_FAIL"
        assert failure.com_ref == "C5"
        
        # Verify failure is on sub1
        assert len(sub1.get_failures()) == 1
        assert sub1.get_failures()[0] == failure
    
    def test_add_failure_to_sub_unit_no_parameters(self):
        """Test add_failure_to_sub_unit() raises ValueError without parameters."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        # Must provide either serial_number or idx
        with pytest.raises(ValueError, match="Must provide either 'serial_number' or 'idx'"):
            uur.add_failure_to_sub_unit(
                category="Component",
                code="FAIL"
            )
    
    def test_add_failure_to_sub_unit_invalid_serial_number(self):
        """Test add_failure_to_sub_unit() raises ValueError for invalid serial."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        uur.add_sub_unit(pn="SUB-A", sn="SUB-SN-001", rev="1")
        
        # Try invalid serial number
        with pytest.raises(ValueError, match="Sub-unit with serial_number='INVALID' not found"):
            uur.add_failure_to_sub_unit(
                category="Component",
                code="FAIL",
                serial_number="INVALID"
            )
    
    def test_add_failure_to_sub_unit_invalid_idx(self):
        """Test add_failure_to_sub_unit() raises ValueError for invalid idx."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        # Try invalid idx
        with pytest.raises(ValueError, match="Sub-unit with idx=99 not found"):
            uur.add_failure_to_sub_unit(
                category="Component",
                code="FAIL",
                idx=99
            )
    
    def test_uur_sub_unit_add_failure_directly(self):
        """Test UURSubUnit.add_failure() method works directly."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        sub_unit = uur.add_sub_unit(pn="SUB-A", sn="SUB-SN-001", rev="1")
        
        # Add failure directly to sub-unit
        failure = sub_unit.add_failure(
            category="Component",
            code="DIODE_FAIL",
            com_ref="D3",
            comment="Diode shorted"
        )
        
        assert failure.category == "Component"
        assert failure.code == "DIODE_FAIL"
        assert failure.com_ref == "D3"
        
        # Verify failure is in sub-unit's list
        assert len(sub_unit.get_failures()) == 1
        assert sub_unit.get_failures()[0] == failure
    
    def test_multiple_failures_across_units(self):
        """Test adding failures to multiple sub-units."""
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab1",
            purpose="Repair"
        )
        
        sub1 = uur.add_sub_unit(pn="SUB-A", sn="SUB-SN-001", rev="1")
        sub2 = uur.add_sub_unit(pn="SUB-B", sn="SUB-SN-002", rev="1")
        
        # Add failures to main unit
        uur.add_failure(category="Component", code="FAIL1")
        uur.add_failure(category="Component", code="FAIL2")
        
        # Add failures to sub1
        uur.add_failure(category="Component", code="FAIL3", sub_unit_idx=sub1.idx)
        
        # Add failures to sub2 by serial
        uur.add_failure_to_sub_unit(
            category="Component",
            code="FAIL4",
            serial_number="SUB-SN-002"
        )
        uur.add_failure_to_sub_unit(
            category="Component",
            code="FAIL5",
            serial_number="SUB-SN-002"
        )
        
        # Verify counts
        main = uur.get_main_unit()
        assert len(main.get_failures()) == 2
        assert len(sub1.get_failures()) == 1
        assert len(sub2.get_failures()) == 2
        
        # Total failures
        assert uur.count_failures() == 5
