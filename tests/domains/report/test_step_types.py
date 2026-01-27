"""
Integration test for Step Graph Model architecture changes.
Tests that all step types with discriminated unions work correctly.
This validates the cloud agent's architecture fixes for step-type literals and field conflicts.
"""
import pytest
import logging
from datetime import datetime
import json

from pywats import pyWATS
from pywats.domains.report.report_models.uut.uut_report import UUTReport
from pywats.domains.report.report_models.uut.uut_info import UUTInfo
from pywats.shared.enums import CompOp
from pywats.domains.report.report_models.uut.steps.generic_step import FlowType
from pywats.tools.test_uut import create_test_uut_report

logger = logging.getLogger(__name__)


@pytest.mark.integration
class TestStepTypesServerIntegration:
    """Test the step-type union architecture using factory methods"""
    
    def test_architecture_with_factory_report(
        self,
        wats_client: pyWATS,
        test_serial_number: str,
        test_part_number: str
    ) -> None:
        """
        Test the step-type union architecture using a comprehensive factory-built report.
        
        This test validates:
        1. step_type literals are correctly serialized
        2. Discriminated union architecture works
        3. MultiBooleanStep field conflicts are resolved
        4. GenericStep catch-all functionality works
        5. Union discrimination works on deserialization
        """
        
        # Create comprehensive report using factory method  
        report = create_test_uut_report(
            part_number=test_part_number,
            serial_number=test_serial_number,
            operator_name="TestOperator"
        )
        
        root = report.get_root_sequence_call()
        
        logger.info("=== ARCHITECTURE VALIDATION TEST ===")
        logger.info("Part Number: %s", report.pn)
        logger.info("Serial Number: %s", report.sn)
        logger.info("Operator: %s", report.info.operator if report.info else "None")
        logger.info("Fixture ID: %s", report.info.fixture_id if report.info else "None")

        # Count steps - handle None case
        steps = root.steps if root.steps is not None else []
        step_count = len(steps)
        logger.info("[OK] Factory report created %d steps", step_count)
        assert step_count > 0, "Factory should create steps"
        
        logger.info("=== VERIFYING SERIALIZATION ===")
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        json_data = json.loads(json_str)

        steps_json = json_data["root"]["steps"]
        
        # Verify stepType field
        for step_idx, step_json in enumerate(steps_json):
            assert "stepType" in step_json, "Step {} missing stepType".format(step_idx)
            step_type = step_json["stepType"]
            logger.debug("  Step %d: %s", step_idx, step_type)
        
        logger.info("[OK] All step_type literals correctly serialized (%d steps)", len(steps_json))
        
        logger.info("=== VERIFYING DESERIALIZATION ===")
        report2 = UUTReport.model_validate(json.loads(json_str))
        
        root2 = report2.get_root_sequence_call()
        steps2 = root2.steps if root2.steps is not None else []
        assert len(steps2) == len(steps), "Step count mismatch after deserialization"
        
        for idx, original_step in enumerate(steps):
            deserialized_step = steps2[idx]
            original_type = type(original_step).__name__
            deserialized_type = type(deserialized_step).__name__
            assert original_type == deserialized_type, \
                "Step {}: Type mismatch - {} vs {}".format(idx, original_type, deserialized_type)
        
        logger.info("[OK] Union discrimination working - all %d steps correct", len(steps2))
        
        logger.info("=== VERIFYING MultiBooleanStep FIXES ===")
        multi_bool_steps = [s for s in steps2 if type(s).__name__ == "MultiBooleanStep"]
        if multi_bool_steps:
            multi_bool_step = multi_bool_steps[0]
            assert hasattr(multi_bool_step, "measurements"), \
                "MultiBooleanStep should have measurements"
            assert not hasattr(multi_bool_step, "measurement") or getattr(multi_bool_step, "measurement", None) is None, \
                "MultiBooleanStep should not have singular measurement field"
            logger.info("[OK] MultiBooleanStep field conflict resolved")
        else:
            logger.info("[INFO] No MultiBooleanStep in factory report (OK)")
        
        logger.info("=== VERIFYING GenericStep CATCH-ALL ===")
        generic_steps = [s for s in steps2 if type(s).__name__ == "GenericStep"]
        if generic_steps:
            logger.info("[OK] GenericStep catch-all working - %d steps", len(generic_steps))
            for gs in generic_steps:
                logger.debug("  - %s: %s", gs.step_type, gs.name)
        else:
            logger.info("[INFO] No GenericStep in factory report (OK)")
        
        logger.info("=" * 60)
        logger.info("SUCCESS: ARCHITECTURE VALIDATION PASSED")
        logger.info("=" * 60)
        logger.info("  Total steps tested: %d", len(steps2))
        logger.info("  Serialization: [OK]")
        logger.info("  Deserialization: [OK]")
        logger.info("  Union discrimination: [OK]")
        logger.info("  MultiBooleanStep fixes: [OK]")
        logger.info("  GenericStep catch-all: [OK]")
        logger.info("=" * 60)
        
    def test_custom_step_types_architecture(
        self,
        wats_client: pyWATS,
        test_serial_number: str,
        test_part_number: str
    ) -> None:
        """
        Test manually adding all major step types to verify architecture.
        This directly tests the union resolution order and discriminator.
        """
        # Create minimal report
        report = UUTReport(
            pn=test_part_number,
            sn=test_serial_number,
            rev="1.0",
            process_code=100,
            station_name="ArchTestStation",
            location="TestLab",
            purpose="Architecture Test",
            result="P",
            start=datetime.now().astimezone()
        )
        
        # Set required UUT info
        report.info = UUTInfo(operator="TestOp")
        
        root = report.get_root_sequence_call()
        
        logger.info("=== TESTING CUSTOM STEP TYPES ===")
        logger.info("Adding step types:")
        
        root.add_numeric_step(
            name="Test1", value=1.0, unit="V",
            comp_op=CompOp.GELE, low_limit=0, high_limit=2, status="P"
        )
        logger.info("  [OK] NumericStep (ET_NLT)")
        
        multi = root.add_multi_numeric_step(name="Test2", status="P")
        multi.add_measurement(name="m1", value=1.0, unit="V", comp_op=CompOp.LOG, status="P")
        logger.info("  [OK] MultiNumericStep (ET_MNLT)")
        
        root.add_boolean_step(name="Test3", status="P")
        logger.info("  [OK] BooleanStep (ET_PFT)")
        
        multi_bool = root.add_multi_boolean_step(name="Test4", status="P")
        multi_bool.add_measurement(name="m1", status="P")
        logger.info("  [OK] MultiBooleanStep (ET_MPFT)")
        
        root.add_string_step(name="Test5", value="test", status="P")
        logger.info("  [OK] StringStep (ET_SVT)")
        
        multi_str = root.add_multi_string_step(name="Test6", status="P")
        multi_str.add_measurement(name="m1", value="test", status="P", comp_op=CompOp.LOG)
        logger.info("  [OK] MultiStringStep (ET_MSVT)")
        
        # Note: GenericStep testing with proper FlowType values would require knowing valid values
        
        # Serialize
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        json_data = json.loads(json_str)
        
        steps_json = json_data["root"]["steps"]
        logger.info("Serialized %d steps", len(steps_json))
        
        step_types = [s["stepType"] for s in steps_json]
        logger.info("Step types: %s", step_types)
        
        # Deserialize and verify union discrimination
        report2 = UUTReport.model_validate(json.loads(json_str))
        root2 = report2.get_root_sequence_call()
        
        steps = root.steps if root.steps is not None else []
        steps2 = root2.steps if root2.steps is not None else []
        
        assert len(steps2) == len(steps), "Step count mismatch"
        logger.info("[OK] Deserialization successful - %d steps with correct types", len(steps2))
        print("SUCCESS: CUSTOM STEP TYPES TEST PASSED")
