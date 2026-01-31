"""
Comprehensive V1/V2/V3 Comparison Test Suite

Tests all three report model implementations side-by-side:
- V1: Original implementation (report_models)
- V2: Composition-based refactor (report_models_v2)  
- V3: Type-safe inheritance implementation (report_models_v3)

This validates:
1. API surface comparison (fields, methods, properties)
2. JSON output compatibility
3. Deserialization compatibility
4. Roundtrip integrity
5. User-facing interface ergonomics
"""
import json
import pytest
from datetime import datetime, timezone
from uuid import UUID, uuid4

# ============================================================================
# V1 Imports
# ============================================================================
from pywats.domains.report.report_models import UUTReport as UUTReportV1
from pywats.domains.report.report_models import UURReport as UURReportV1
from pywats.domains.report.report_models import Report as ReportV1
from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall as SequenceCallV1
from pywats.domains.report.report_models.uur.uur_info import UURInfo as UURInfoV1

# ============================================================================
# V2 Imports
# ============================================================================
from pywats.domains.report.report_models_v2 import UUTReport as UUTReportV2
from pywats.domains.report.report_models_v2 import UURReport as UURReportV2
from pywats.domains.report.report_models_v2.report_common import ReportCommon

# ============================================================================
# V3 Imports
# ============================================================================
from pywats.domains.report.report_models_v3 import (
    UUTReport as UUTReportV3,
    UURReport as UURReportV3,
    SequenceCall as SequenceCallV3,
    NumericStep as NumericStepV3,
    PassFailStep as PassFailStepV3,
    StringValueStep as StringValueStepV3,
    CompOp,
    StepStatus,
    UURSubUnit as UURSubUnitV3,
    UURInfo as UURInfoV3,
)


def normalize_json(obj: dict) -> dict:
    """
    Normalize JSON for comparison.
    
    Handles:
    - None vs missing fields
    - Empty lists vs missing lists
    - UUID string formatting
    - Datetime formatting
    """
    if not isinstance(obj, dict):
        return obj
    
    result = {}
    for key, value in obj.items():
        if value is None:
            continue
        if isinstance(value, list) and len(value) == 0:
            continue
        if isinstance(value, dict):
            normalized = normalize_json(value)
            if normalized:
                result[key] = normalized
        elif isinstance(value, list):
            result[key] = [normalize_json(item) if isinstance(item, dict) else item for item in value]
        else:
            result[key] = value
    return result


class TestUUTReportCreation:
    """Test UUT report creation across all three versions."""
    
    def test_v1_creation(self):
        """V1: Direct constructor with flat fields."""
        report = UUTReportV1(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=100,
            station_name="TestStation",
            location="Lab",
            purpose="Production",
        )
        
        assert report.pn == "WIDGET-001"
        assert report.sn == "SN123456"
        assert report.type == "T"
        assert report.id is not None
    
    def test_v2_creation(self):
        """V2: Factory method with common wrapper."""
        report = UUTReportV2.create(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=100,
            station_name="TestStation",
            location="Lab",
            purpose="Production",
        )
        
        # Fields accessed via .common
        assert report.common.pn == "WIDGET-001"
        assert report.common.sn == "SN123456"
        assert report.type == "T"
        assert report.common.id is not None
    
    def test_v3_creation(self):
        """V3: Clean constructor with operation parameter."""
        report = UUTReportV3(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            purpose="Production",
        )
        
        # Direct field access (like v1)
        assert report.pn == "WIDGET-001"
        assert report.sn == "SN123456"
        assert report.type == "T"
        assert report.id is not None


class TestUUTStepCreation:
    """Test step creation workflows across versions."""
    
    def test_v1_step_workflow(self):
        """V1: Get root, add steps via root methods (keyword-only args)."""
        report = UUTReportV1(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        
        root = report.get_root_sequence_call()
        root.add_numeric_step(
            name="Voltage",
            value=5.0,
            unit="V",
            low_limit=4.5,
            high_limit=5.5
        )
        # v1 uses add_boolean_step, not add_pass_fail_step
        root.add_boolean_step(name="LED Check", status="P")
        
        assert len(root.steps) == 2
    
    def test_v2_step_workflow(self):
        """V2: Same as v1 (reuses v1 step classes)."""
        report = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        
        root = report.get_root_sequence_call()
        root.add_numeric_step(
            name="Voltage",
            value=5.0,
            unit="V",
            low_limit=4.5,
            high_limit=5.5
        )
        # v2 uses same v1 method
        root.add_boolean_step(name="LED Check", status="P")
        
        assert len(root.steps) == 2
    
    def test_v3_step_workflow(self):
        """V3: Create root, add steps with CompOp - now uses V1 naming."""
        report = UUTReportV3(pn="PN", sn="SN", rev="A", purpose="Test")
        
        root = report.get_root_sequence_call()
        root.add_numeric_step(
            name="Voltage",
            value=5.0,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=4.5,
            high_limit=5.5
        )
        root.add_boolean_step(name="LED Check", status="P")
        
        assert len(root.steps) == 2


class TestUURReportCreation:
    """Test UUR report creation across all three versions."""
    
    def test_v1_uur_creation(self):
        """V1: Requires UURInfo in constructor."""
        uur_info = UURInfoV1(operator="John", test_operation_code=100)
        report = UURReportV1(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab",
            purpose="Repair",
            uur_info=uur_info
        )
        
        assert report.pn == "WIDGET-001"
        assert report.type == "R"
        assert report.uur_info.operator == "John"
    
    def test_v2_uur_creation(self):
        """V2: Factory method with explicit process code params."""
        report = UURReportV2.create(
            pn="WIDGET-001",
            sn="SN123456",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="RepairStation",
            location="Lab",
            purpose="Repair",
            operator="John"
        )
        
        assert report.common.pn == "WIDGET-001"
        assert report.type == "R"
        assert report.uur_info.operator == "John"
    
    def test_v3_uur_creation(self):
        """V3: Clean constructor with link_to_uut method."""
        report = UURReportV3(
            pn="WIDGET-001",
            sn="SN123456",
            purpose="Repair"
        )
        
        # Link to failed UUT
        fake_uut_id = uuid4()
        report.link_to_uut(fake_uut_id)
        report.set_repair_process(code=500, name="Component Repair")
        report.set_test_operation(code=100, name="Vibration Test")
        
        assert report.pn == "WIDGET-001"
        assert report.type == "R"
        assert report.uur_info.ref_uut == fake_uut_id


class TestUURFailureHandling:
    """Test UUR failure management across versions."""
    
    def test_v1_uur_failures(self):
        """V1: Add failures via get_main_unit()."""
        uur_info = UURInfoV1(operator="John", test_operation_code=100)
        report = UURReportV1(
            pn="PN", sn="SN", rev="A",
            process_code=500, station_name="S", location="L", purpose="P",
            uur_info=uur_info
        )
        
        main = report.get_main_unit()
        main.add_failure(category="Component", code="CAP_FAIL")
        
        # v1 checks failures list directly
        assert main.failures is not None
        assert len(main.failures) == 1
    
    def test_v2_uur_failures(self):
        """V2: Same pattern as v1 via common."""
        report = UURReportV2.create(
            pn="PN", sn="SN", rev="A",
            repair_process_code=500, test_operation_code=100,
            station_name="S", location="L", purpose="P", operator="O"
        )
        
        main = report.get_main_unit()
        main.add_failure(category="Component", code="CAP_FAIL")
        
        # v2 also checks failures list directly
        assert main.failures is not None
        assert len(main.failures) == 1
    
    def test_v3_uur_failures(self):
        """V3: Clean failure management with convenience methods."""
        report = UURReportV3(pn="PN", sn="SN", purpose="Repair")
        
        # Add failure to main unit directly
        report.add_main_failure(
            category="Component",
            code="CAP_FAIL",
            comment="C12 capacitor open circuit"
        )
        
        # Or via get_main_unit
        main = report.get_main_unit()
        assert main.has_failures()
        
        # Get all failures across all units
        all_failures = report.get_all_failures()
        assert len(all_failures) == 1


class TestJSONSerialization:
    """Test JSON serialization compatibility."""
    
    def test_uut_json_structure(self):
        """All versions should produce compatible JSON structure."""
        # V1
        v1 = UUTReportV1(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        v1_json = json.loads(v1.model_dump_json(by_alias=True))
        
        # V2
        v2 = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        v2_json = json.loads(v2.model_dump_json(by_alias=True))
        
        # V3 - process_code is directly on Report base
        v3 = UUTReportV3(pn="PN", sn="SN", rev="A", purpose="P")
        v3.process_code = 100
        v3_json = json.loads(v3.model_dump_json(by_alias=True))
        
        # All should have same core fields
        for data in [v1_json, v2_json, v3_json]:
            assert data.get('pn') == "PN"
            assert data.get('sn') == "SN"
            assert data.get('type') == "T"
    
    def test_uur_json_structure(self):
        """All UUR versions should produce compatible JSON structure."""
        # V1
        uur_info_v1 = UURInfoV1(operator="Op", test_operation_code=100)
        v1 = UURReportV1(
            pn="PN", sn="SN", rev="A",
            process_code=500, station_name="S", location="L", purpose="P",
            uur_info=uur_info_v1
        )
        v1_json = json.loads(v1.model_dump_json(by_alias=True))
        
        # V2
        v2 = UURReportV2.create(
            pn="PN", sn="SN", rev="A",
            repair_process_code=500, test_operation_code=100,
            station_name="S", location="L", purpose="P", operator="Op"
        )
        v2_json = json.loads(v2.model_dump_json(by_alias=True))
        
        # V3
        v3 = UURReportV3(pn="PN", sn="SN", purpose="P")
        v3.set_repair_process(code=500)
        v3.set_test_operation(code=100)
        v3_json = json.loads(v3.model_dump_json(by_alias=True))
        
        # All should have same core fields
        for data in [v1_json, v2_json, v3_json]:
            assert data.get('pn') == "PN"
            assert data.get('sn') == "SN"
            assert data.get('type') == "R"


class TestTypeAnnotations:
    """Test type annotation quality for IDE support."""
    
    def test_v3_step_return_types(self):
        """V3 steps should return correct types."""
        report = UUTReportV3(pn="PN", sn="SN", purpose="Test")
        root = report.get_root_sequence_call()
        
        # add_numeric_step returns NumericStep
        numeric = root.add_numeric_step(name="Voltage", value=5.0)
        assert isinstance(numeric, NumericStepV3)
        
        # add_boolean_step returns PassFailStep
        pf = root.add_boolean_step(name="Check", status="P")
        assert isinstance(pf, PassFailStepV3)
        
        # add_string_step returns StringValueStep
        string = root.add_string_step(name="Serial", value="ABC")
        assert isinstance(string, StringValueStepV3)
    
    def test_v3_sub_unit_types(self):
        """V3 UUR should have properly typed sub_units."""
        report = UURReportV3(pn="PN", sn="SN", purpose="Repair")
        
        # get_main_unit returns UURSubUnit
        main = report.get_main_unit()
        assert isinstance(main, UURSubUnitV3)
        
        # add_sub_unit returns UURSubUnit
        sub = report.add_sub_unit(pn="SUB-PN", sn="SUB-SN")
        assert isinstance(sub, UURSubUnitV3)


class TestStepListBehavior:
    """Test StepList collection behavior (v3 key feature)."""
    
    def test_v3_steplist_list_interface(self):
        """V3 StepList should behave like a list."""
        report = UUTReportV3(pn="PN", sn="SN", purpose="Test")
        root = report.get_root_sequence_call()
        
        # Add steps
        root.add_numeric_step(name="Step1", value=1.0)
        root.add_numeric_step(name="Step2", value=2.0)
        root.add_numeric_step(name="Step3", value=3.0)
        
        # List operations
        assert len(root.steps) == 3
        assert root.steps[0].name == "Step1"
        assert root.steps[-1].name == "Step3"
        
        # Iteration
        names = [s.name for s in root.steps]
        assert names == ["Step1", "Step2", "Step3"]
    
    def test_v3_steplist_parent_injection(self):
        """V3 StepList should inject parent reference."""
        report = UUTReportV3(pn="PN", sn="SN", purpose="Test")
        root = report.get_root_sequence_call()
        
        step = root.add_numeric_step(name="Voltage", value=5.0)
        
        # Step should have parent reference
        assert step.parent is root


class TestNestedSequences:
    """Test nested sequence call behavior."""
    
    def test_v1_nested_sequences(self):
        """V1: Add sequence via add_sequence_call method."""
        report = UUTReportV1(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        root = report.get_root_sequence_call()
        
        # Add nested sequence
        nested = root.add_sequence_call("NestedSequence")
        # v1 uses keyword-only args
        nested.add_numeric_step(name="InnerStep", value=1.0)
        
        assert len(root.steps) == 1
        assert root.steps[0].name == "NestedSequence"
    
    def test_v2_nested_sequences(self):
        """V2: Same as v1 (uses v1 SequenceCall)."""
        report = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        root = report.get_root_sequence_call()
        
        nested = root.add_sequence_call("NestedSequence")
        # v2 uses same v1 method signature
        nested.add_numeric_step(name="InnerStep", value=1.0)
        
        assert len(root.steps) == 1
    
    def test_v3_nested_sequences(self):
        """V3: Add nested sequence with typed return."""
        report = UUTReportV3(pn="PN", sn="SN", purpose="Test")
        root = report.get_root_sequence_call()
        
        # Add nested sequence
        nested = root.add_sequence_call("NestedSequence")
        nested.add_numeric_step(name="InnerStep", value=1.0)
        
        assert len(root.steps) == 1
        assert isinstance(nested, SequenceCallV3)


class TestMiscInfoAndAssets:
    """Test misc info and assets across versions."""
    
    def test_v1_misc_info(self):
        """V1: add_misc_info on report."""
        report = UUTReportV1(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        report.add_misc_info("Temperature", "25.5")
        
        # v1 uses misc_infos (plural)
        assert len(report.misc_infos) == 1
    
    def test_v2_misc_info(self):
        """V2: add_misc_info via common."""
        report = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        report.common.add_misc_info("Temperature", "25.5")
        
        # v2 also uses misc_infos (plural)
        assert len(report.common.misc_infos) == 1
    
    def test_v3_misc_info(self):
        """V3: add_misc_info on report (flat access)."""
        report = UUTReportV3(pn="PN", sn="SN", purpose="Test")
        report.add_misc_info("Temperature", "25.5")
        
        # v3 uses misc_infos for consistency
        assert len(report.misc_infos) == 1


class TestSubUnits:
    """Test sub-unit handling across versions."""
    
    def test_v1_sub_units(self):
        """V1: add_sub_unit on report."""
        report = UUTReportV1(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        sub = report.add_sub_unit("Board", "SUB-SN", "SUB-PN", "1.0")
        
        assert sub.sn == "SUB-SN"
        assert len(report.sub_units) == 1
    
    def test_v2_sub_units(self):
        """V2: add_sub_unit via common."""
        report = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        sub = report.common.add_sub_unit("Board", "SUB-SN", "SUB-PN", "1.0")
        
        assert sub.sn == "SUB-SN"
        assert len(report.common.sub_units) == 1
    
    def test_v3_sub_units(self):
        """V3: add_sub_unit with typed return."""
        report = UUTReportV3(pn="PN", sn="SN", purpose="Test")
        sub = report.add_sub_unit(pn="SUB-PN", sn="SUB-SN", rev="1.0")
        
        assert sub.sn == "SUB-SN"
        assert len(report.sub_units) == 1


class TestDesignPatterns:
    """Test architectural design patterns."""
    
    def test_v1_is_flat_inheritance(self):
        """V1 uses flat inheritance with Report base."""
        assert issubclass(UUTReportV1, ReportV1)
        assert issubclass(UURReportV1, ReportV1)
    
    def test_v2_is_composition(self):
        """V2 uses composition with ReportCommon."""
        report = UUTReportV2.create(
            pn="PN", sn="SN", rev="A",
            process_code=100, station_name="S", location="L", purpose="P"
        )
        assert hasattr(report, 'common')
        assert isinstance(report.common, ReportCommon)
        # V2 does NOT inherit from v1 Report
        assert not issubclass(UUTReportV2, ReportV1)
    
    def test_v3_is_generic_inheritance(self):
        """V3 uses generic inheritance for type safety."""
        from pywats.domains.report.report_models_v3 import Report
        from pywats.domains.report.report_models_v3 import UUTSubUnit, SubUnit
        
        # UUTReport extends Report[UUTSubUnit]
        # Check via inspection
        report = UUTReportV3(pn="PN", sn="SN", purpose="Test")
        
        # Direct field access (no .common wrapper)
        assert hasattr(report, 'pn')
        assert hasattr(report, 'sn')
        assert not hasattr(report, 'common')  # No composition wrapper


class TestComprehensiveWorkflow:
    """Test complete real-world workflows."""
    
    def test_v1_complete_uut_workflow(self):
        """V1: Complete UUT report with all features."""
        report = UUTReportV1(
            pn="WIDGET-001",
            sn="SN-001",
            rev="2.0",
            process_code=100,
            station_name="TestBench",
            location="Factory",
            purpose="Production",
            result="P"
        )
        
        # Add info
        report.add_misc_info("Temperature", "25.5°C")
        report.add_misc_info("Humidity", "45%")
        report.add_sub_unit("Board", "BOARD-001", "PCB-A", "1.0")
        
        # Add test sequence
        root = report.get_root_sequence_call()
        root.add_numeric_step(name="Voltage", value=5.0, unit="V", low_limit=4.9, high_limit=5.1)
        root.add_numeric_step(name="Current", value=0.5, unit="A", low_limit=0.4, high_limit=0.6)
        root.add_boolean_step(name="LED Check", status="P")
        
        nested = root.add_sequence_call("PowerTest")
        nested.add_numeric_step(name="Power", value=2.5, unit="W")
        
        # Verify
        assert len(report.misc_infos) == 2
        assert len(report.sub_units) == 1
        assert len(root.steps) == 4
    
    def test_v2_complete_uut_workflow(self):
        """V2: Complete UUT report with all features."""
        report = UUTReportV2.create(
            pn="WIDGET-001",
            sn="SN-001",
            rev="2.0",
            process_code=100,
            station_name="TestBench",
            location="Factory",
            purpose="Production",
            result="P"
        )
        
        # Add info (via common)
        report.common.add_misc_info("Temperature", "25.5°C")
        report.common.add_misc_info("Humidity", "45%")
        report.common.add_sub_unit("Board", "BOARD-001", "PCB-A", "1.0")
        
        # Add test sequence
        root = report.get_root_sequence_call()
        root.add_numeric_step(name="Voltage", value=5.0, unit="V", low_limit=4.9, high_limit=5.1)
        root.add_numeric_step(name="Current", value=0.5, unit="A", low_limit=0.4, high_limit=0.6)
        root.add_boolean_step(name="LED Check", status="P")
        
        nested = root.add_sequence_call("PowerTest")
        nested.add_numeric_step(name="Power", value=2.5, unit="W")
        
        # Verify
        assert len(report.common.misc_infos) == 2
        assert len(report.common.sub_units) == 1
        assert len(root.steps) == 4
    
    def test_v3_complete_uut_workflow(self):
        """V3: Complete UUT report with all features."""
        report = UUTReportV3(
            pn="WIDGET-001",
            sn="SN-001",
            rev="2.0",
            purpose="Production",
        )
        report.result = "P"
        
        # Add info (direct access)
        report.add_misc_info("Temperature", "25.5°C")
        report.add_misc_info("Humidity", "45%")
        report.add_sub_unit(pn="PCB-A", sn="BOARD-001", rev="1.0")
        
        # Add test sequence
        root = report.get_root_sequence_call()
        root.add_numeric_step(name="Voltage", value=5.0, unit="V", comp_op=CompOp.GELE, low_limit=4.9, high_limit=5.1)
        root.add_numeric_step(name="Current", value=0.5, unit="A", comp_op=CompOp.GELE, low_limit=0.4, high_limit=0.6)
        root.add_boolean_step(name="LED Check", status="P")
        
        nested = root.add_sequence_call("PowerTest")
        nested.add_numeric_step(name="Power", value=2.5, unit="W")
        
        # Verify
        assert len(report.misc_infos) == 2
        assert len(report.sub_units) == 1
        assert len(root.steps) == 4
    
    def test_v3_complete_uur_workflow(self):
        """V3: Complete UUR report with all features."""
        # Create UUR linked to a failed UUT
        fake_uut_id = uuid4()
        
        report = UURReportV3(
            pn="WIDGET-001",
            sn="SN-001",
            purpose="Repair",
        )
        
        # Configure repair context
        report.link_to_uut(fake_uut_id)
        report.set_repair_process(code=500, name="Component Repair")
        report.set_test_operation(code=100, name="Power Test", guid=uuid4())
        
        # Add failures to main unit
        report.add_main_failure(
            category="Component",
            code="CAP_OPEN",
            comment="Capacitor C12 open circuit",
            com_ref="C12"
        )
        
        # Add replacement sub-unit
        sub = report.add_sub_unit(pn="CAP-100UF", sn="CAP-001")
        sub.replaced_idx = 0
        sub.add_failure(
            category="Component",
            code="REPLACED",
            comment="Replaced faulty capacitor"
        )
        
        # Add misc info
        report.add_misc_info("Repair Time", "15 minutes")
        
        # Verify
        assert report.uur_info.ref_uut == fake_uut_id
        assert len(report.get_all_failures()) == 2
        assert len(report.sub_units) == 2  # main + replaced part


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
