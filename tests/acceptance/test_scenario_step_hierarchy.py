"""
Acceptance Test: Step Hierarchy and Discrimination Scenario

This scenario tests the step graph model architecture:
1. Create reports with various step types
2. Verify correct step type discrimination
3. Validate parent-child relationships
4. Test sequence call hierarchy
"""
import pytest
from pywats import pyWATS
from pywats.domains.report.report_models import UUTReport, SequenceCall
from pywats.domains.report.report_models.uut.steps import FlowType
from .conftest import AcceptanceTestHelper


@pytest.mark.acceptance
class TestStepHierarchyScenario:
    """
    Test step hierarchy and type discrimination in real scenarios
    """
    
    def test_nested_sequence_hierarchy(
        self,
        wats_client: pyWATS,
        test_product_data: dict,
        unique_identifier: str,
        acceptance_helper: AcceptanceTestHelper
    ):
        """
        Test nested sequence call hierarchy with automatic verification.
        
        Creates a report with:
        - Main sequence
        - Multiple nested sequence calls
        - Various step types (numeric, string, boolean, generic)
        - Parent-child relationships
        """
        part_number = test_product_data["part_number"]
        part_revision = test_product_data["part_revision"]
        serial_number = f"SN-HIERARCHY-{unique_identifier}"
        
        # Create report with nested hierarchy
        report = UUTReport(
            part_number=part_number,
            part_revision=part_revision,
            serial_number=serial_number,
            uut_result="P"
        )
        
        main_seq = report.main_sequence
        main_seq.name = "Main Test Sequence"
        
        # Level 1: Setup sequence
        setup_seq = main_seq.add_sequence_call(
            name="Setup and Initialize",
            file_name="setup.seq",
            version="1.0",
            path="tests/setup"
        )
        
        # Add steps to setup
        setup_seq.add_generic_step(
            step_type=FlowType.Action,
            name="Initialize Hardware",
            status="P"
        )
        setup_seq.add_numeric_step(
            name="Verify Voltage",
            status="P",
            value=5.0,
            units="V",
            comp_operator="GELE",
            low_limit=4.5,
            high_limit=5.5
        )
        
        # Level 1: Main test sequence
        main_test_seq = main_seq.add_sequence_call(
            name="Main Tests",
            file_name="main_tests.seq",
            version="2.0",
            path="tests/main"
        )
        
        # Level 2: Nested functional test
        func_test_seq = main_test_seq.add_sequence_call(
            name="Functional Tests",
            file_name="functional.seq",
            version="1.5",
            path="tests/main/functional"
        )
        
        # Add various step types to functional tests
        func_test_seq.add_numeric_step(
            name="Temperature Check",
            status="P",
            value=25.3,
            units="°C",
            comp_operator="GELE",
            low_limit=20.0,
            high_limit=30.0
        )
        
        func_test_seq.add_boolean_step(
            name="Power Supply OK",
            status="P",
            value=True
        )
        
        func_test_seq.add_string_step(
            name="Device ID",
            status="P",
            value="DEV-12345"
        )
        
        func_test_seq.add_generic_step(
            step_type=FlowType.Statement,
            name="Log Status",
            status="P"
        )
        
        # Level 2: Performance tests
        perf_test_seq = main_test_seq.add_sequence_call(
            name="Performance Tests",
            file_name="performance.seq",
            version="1.0",
            path="tests/main/performance"
        )
        
        perf_test_seq.add_numeric_step(
            name="Response Time",
            status="P",
            value=15.2,
            units="ms",
            comp_operator="LT",
            high_limit=20.0
        )
        
        # Level 1: Cleanup
        cleanup_seq = main_seq.add_sequence_call(
            name="Cleanup",
            file_name="cleanup.seq",
            version="1.0",
            path="tests/cleanup"
        )
        
        cleanup_seq.add_generic_step(
            step_type=FlowType.Action,
            name="Shutdown",
            status="P"
        )
        
        # Verify local structure before sending
        assert len(main_seq.steps) == 3, "Main sequence should have 3 top-level sequences"
        assert len(setup_seq.steps) == 2, "Setup should have 2 steps"
        assert len(main_test_seq.steps) == 2, "Main tests should have 2 sub-sequences"
        assert len(func_test_seq.steps) == 4, "Functional tests should have 4 steps"
        
        # Send to server
        result = wats_client.report.send_uut_report(report)
        assert result is True, "Failed to send report"
        
        # Load and verify from server
        loaded_report = acceptance_helper.verify_report_created(
            wats_client, serial_number, timeout=30
        )
        
        # Verify hierarchy preserved
        loaded_main = loaded_report.main_sequence
        assert len(loaded_main.steps) == 3, "Loaded main sequence step count mismatch"
        
        # Find and verify nested sequences
        loaded_setup = next((s for s in loaded_main.steps if s.name == "Setup and Initialize"), None)
        assert loaded_setup is not None, "Setup sequence not found"
        assert len(loaded_setup.steps) == 2, "Setup steps not preserved"
        
        loaded_main_test = next((s for s in loaded_main.steps if s.name == "Main Tests"), None)
        assert loaded_main_test is not None, "Main test sequence not found"
        assert len(loaded_main_test.steps) == 2, "Main test sub-sequences not preserved"
        
        # Verify deeply nested sequence
        loaded_func = next((s for s in loaded_main_test.steps if s.name == "Functional Tests"), None)
        assert loaded_func is not None, "Functional test sequence not found"
        assert len(loaded_func.steps) == 4, "Functional test steps not preserved"
        
        # Verify step types are correctly discriminated
        numeric_step = next((s for s in loaded_func.steps if s.name == "Temperature Check"), None)
        assert numeric_step is not None, "Numeric step not found"
        assert hasattr(numeric_step, 'measurement'), "Step not discriminated as NumericStep"
        assert numeric_step.measurement.value == 25.3, "Numeric value not preserved"
        
        boolean_step = next((s for s in loaded_func.steps if s.name == "Power Supply OK"), None)
        assert boolean_step is not None, "Boolean step not found"
        assert hasattr(boolean_step, 'measurement'), "Step not discriminated as BooleanStep"
        
        string_step = next((s for s in loaded_func.steps if s.name == "Device ID"), None)
        assert string_step is not None, "String step not found"
        assert hasattr(string_step, 'measurement'), "Step not discriminated as StringStep"
        
        print(f"\n✓ Nested hierarchy test completed for {serial_number}")
        print(f"  - 3 levels of nesting verified")
        print(f"  - All step types correctly discriminated")
        print(f"  - Parent-child relationships preserved")
    
    def test_mixed_step_types_in_sequence(
        self,
        wats_client: pyWATS,
        test_product_data: dict,
        unique_identifier: str,
        acceptance_helper: AcceptanceTestHelper
    ):
        """
        Test a sequence with mixed step types to verify discrimination.
        """
        part_number = test_product_data["part_number"]
        part_revision = test_product_data["part_revision"]
        serial_number = f"SN-MIXED-{unique_identifier}"
        
        report = UUTReport(
            part_number=part_number,
            part_revision=part_revision,
            serial_number=serial_number,
            uut_result="P"
        )
        
        main_seq = report.main_sequence
        
        # Add all different step types
        main_seq.add_generic_step(FlowType.Action, "Action Step", "P")
        main_seq.add_generic_step(FlowType.Statement, "Statement Step", "P")
        main_seq.add_generic_step(FlowType.Goto, "Goto Step", "P")
        main_seq.add_numeric_step("Numeric Test", "P", 100.0, "Ω")
        main_seq.add_string_step("String Test", "P", "PASS")
        main_seq.add_boolean_step("Boolean Test", "P", True)
        
        # Send and verify
        result = wats_client.report.send_uut_report(report)
        assert result is True, "Failed to send report"
        
        loaded_report = acceptance_helper.verify_report_created(
            wats_client, serial_number, timeout=30
        )
        
        # Verify all steps present and correctly typed
        assert len(loaded_report.main_sequence.steps) == 6, "Not all steps preserved"
        
        # Verify each step type
        step_types = [type(step).__name__ for step in loaded_report.main_sequence.steps]
        assert "GenericStep" in step_types, "GenericStep not found"
        assert "NumericStep" in step_types, "NumericStep not found"
        assert "StringStep" in step_types, "StringStep not found"
        assert "BooleanStep" in step_types, "BooleanStep not found"
        
        print(f"\n✓ Mixed step types test completed for {serial_number}")
        print(f"  - Step types found: {set(step_types)}")
