"""
Integration test for Step Graph Model architecture changes.
Tests that all step types with discriminated unions work correctly with the WATS server.
This validates the architecture fixes for step-type literals and field conflicts.
"""
import pytest
from datetime import datetime
from typing import Any

from pyWATS.domains.report.report_models.uut.uut_report import UUTReport
from pyWATS.domains.report.report_models.uut.steps.comp_operator import CompOp
from pyWATS.domains.report.report_models.chart import ChartType, ChartSeries


@pytest.mark.integration
class TestStepTypesServerIntegration:
    """Test that all step types work correctly with the WATS server"""
    
    def test_submit_report_with_all_step_types(
        self,
        wats_client: Any,
        test_serial_number: str,
        test_part_number: str
    ) -> None:
        """
        Test submitting a report with ALL step types to verify architecture changes.
        
        This test validates:
        1. step_type literals are correctly serialized
        2. Discriminated union architecture works
        3. MultiBooleanStep field conflicts are resolved
        4. GenericStep catch-all functionality works
        5. Server accepts all step types
        """
        
        # Create report
        report = UUTReport(
            pn=test_part_number,
            sn=test_serial_number,
            rev="1.0",
            process_code=100,
            station_name="StepTypeTestStation",
            location="IntegrationTestLab",
            purpose="Test All Step Types",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        
        print(f"\n=== TESTING ALL STEP TYPES ===")
        print(f"Part Number: {report.pn}")
        print(f"Serial Number: {report.sn}")
        
        # ========================================
        # 1. NUMERIC STEPS (Single)
        # ========================================
        print("\n1. Adding NumericStep (ET_NLT)...")
        root.add_numeric_step(
            name="Voltage_3V3",
            value=3.3,
            unit="V",
            comp_op=CompOp.GELE,
            low_limit=3.0,
            high_limit=3.6,
            status="P"
        )
        
        # ========================================
        # 2. MULTI NUMERIC STEPS (ET_MNLT)
        # ========================================
        print("2. Adding MultiNumericStep (ET_MNLT)...")
        multi_num = root.add_multi_numeric_step(
            name="PowerRails",
            status="P"
        )
        multi_num.add_measurement(name="3V3", value=3.3, unit="V", comp_op=CompOp.GELE, low_limit=3.0, high_limit=3.6)
        multi_num.add_measurement(name="5V0", value=5.0, unit="V", comp_op=CompOp.GELE, low_limit=4.8, high_limit=5.2)
        
        # ========================================
        # 3. BOOLEAN STEPS (Single)
        # ========================================
        print("3. Adding BooleanStep (ET_PFT)...")
        root.add_boolean_step(
            name="ConnectionTest",
            status="P"
        )
        
        # ========================================
        # 4. MULTI BOOLEAN STEPS (ET_MPFT)
        # Testing the fixed MultiBooleanStep inheritance
        # ========================================
        print("4. Adding MultiBooleanStep (ET_MPFT) - Testing fixed inheritance...")
        multi_bool = root.add_multi_boolean_step(
            name="InterfaceChecks",
            status="P"
        )
        multi_bool.add_measurement(name="USB_Present", status="P")
        multi_bool.add_measurement(name="Ethernet_Present", status="P")
        
        # ========================================
        # 5. STRING STEPS (Single)
        # ========================================
        print("5. Adding StringStep (ET_SVT)...")
        root.add_string_step(
            name="FirmwareVersion",
            value="v2.1.3",
            status="P"
        )
        
        # ========================================
        # 6. MULTI STRING STEPS (ET_MSVT)
        # ========================================
        print("6. Adding MultiStringStep (ET_MSVT)...")
        multi_str = root.add_multi_string_step(
            name="SystemInfo",
            status="P"
        )
        multi_str.add_measurement(name="OS_Version", value="Ubuntu 20.04", status="P", comp_op=CompOp.LOG)
        multi_str.add_measurement(name="Kernel", value="5.4.0", status="P", comp_op=CompOp.LOG)
        
        # ========================================
        # 7. NESTED SEQUENCE CALLS
        # ========================================
        print("7. Adding nested SequenceCall...")
        sub_seq = root.add_sequence_call(
            name="CalibrationSequence",
            file_name="calibration.seq",
            version="1.0.0"
        )
        sub_seq.add_numeric_step(
            name="CalibrationOffset",
            value=0.05,
            unit="V",
            status="P"
        )
        
        # ========================================
        # 8. GENERIC STEPS (FlowType catch-all)
        # Testing the GenericStep str type catch-all
        # ========================================
        print("8. Adding GenericStep (NI_Flow_If) - Testing catch-all...")
        root.add_generic_step(
            step_type="NI_Flow_If",
            name="ConditionalBranch",
            status="P"
        )
        
        print("9. Adding GenericStep (Statement)...")
        root.add_generic_step(
            step_type="Statement",
            name="LogStatement",
            status="P"
        )
        
        print("10. Adding GenericStep (Goto)...")
        root.add_generic_step(
            step_type="Goto",
            name="JumpToEnd",
            status="P"
        )
        
        # ========================================
        # 11. CHART STEPS (WATS_XYGMNLT)
        # ========================================
        print("11. Adding ChartStep (WATS_XYGMNLT)...")
        x_data = ";".join([str(float(i)) for i in range(5)])
        y_data = ";".join([str(float(i * 2)) for i in range(5)])
        series = ChartSeries(name="DataSeries", x_data=x_data, y_data=y_data)
        
        root.add_chart_step(
            name="TemperatureProfile",
            chart_type=ChartType.LINE,
            label="Temperature vs Time",
            x_label="Time",
            x_unit="s",
            y_label="Temperature",
            y_unit="°C",
            series=[series],
            status="P"
        )
        
        # ========================================
        # VERIFY STEP COUNT
        # ========================================
        step_count = len(root.steps)
        print(f"\n✓ Created {step_count} steps of various types")
        # We have 11 top-level steps (the nested sequence has 1 child but we count top-level only)
        assert step_count == 11, f"Expected 11 steps, got {step_count}"
        
        # ========================================
        # SERIALIZE AND VERIFY STEP_TYPE LITERALS
        # ========================================
        print("\n=== VERIFYING SERIALIZATION ===")
        import json
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        json_data = json.loads(json_str)
        
        steps_json = json_data["root"]["steps"]
        
        # Verify step_type literals are preserved
        assert steps_json[0]["stepType"] == "ET_NLT", "NumericStep should have ET_NLT"
        assert steps_json[1]["stepType"] == "ET_MNLT", "MultiNumericStep should have ET_MNLT"
        assert steps_json[2]["stepType"] == "ET_PFT", "BooleanStep should have ET_PFT"
        assert steps_json[3]["stepType"] == "ET_MPFT", "MultiBooleanStep should have ET_MPFT"
        assert steps_json[4]["stepType"] == "ET_SVT", "StringStep should have ET_SVT"
        assert steps_json[5]["stepType"] == "ET_MSVT", "MultiStringStep should have ET_MSVT"
        assert steps_json[6]["stepType"] == "SequenceCall", "SequenceCall should have SequenceCall"
        assert steps_json[7]["stepType"] == "NI_Flow_If", "GenericStep should preserve NI_Flow_If"
        assert steps_json[8]["stepType"] == "Statement", "GenericStep should preserve Statement"
        assert steps_json[9]["stepType"] == "Goto", "GenericStep should preserve Goto"
        assert steps_json[10]["stepType"] == "WATS_XYGMNLT", "ChartStep should have WATS_XYGMNLT"
        
        # Verify nested sequence has correct step_type
        assert "steps" in steps_json[6], "SequenceCall should have nested steps"
        nested_steps = steps_json[6]["steps"]
        assert len(nested_steps) == 1, "SequenceCall should have 1 child"
        assert nested_steps[0]["stepType"] == "ET_NLT", "Nested step should be NumericStep"
        
        print("✓ All step_type literals correctly serialized")
        
        # ========================================
        # DESERIALIZE AND VERIFY DISCRIMINATION
        # ========================================
        print("\n=== VERIFYING DESERIALIZATION ===")
        report2 = UUTReport.model_validate_json(json_str)
        root2 = report2.get_root_sequence_call()
        
        # Import step classes for type checking
        from pyWATS.domains.report.report_models.uut.steps.numeric_step import NumericStep, MultiNumericStep
        from pyWATS.domains.report.report_models.uut.steps.boolean_step import BooleanStep, MultiBooleanStep
        from pyWATS.domains.report.report_models.uut.steps.string_step import StringStep, MultiStringStep
        from pyWATS.domains.report.report_models.uut.steps.sequence_call import SequenceCall
        from pyWATS.domains.report.report_models.uut.steps.generic_step import GenericStep
        from pyWATS.domains.report.report_models.uut.steps.chart_step import ChartStep
        
        # Verify correct types were created by discriminator
        assert isinstance(root2.steps[0], NumericStep), "Should be NumericStep"
        assert isinstance(root2.steps[1], MultiNumericStep), "Should be MultiNumericStep"
        assert isinstance(root2.steps[2], BooleanStep), "Should be BooleanStep"
        assert isinstance(root2.steps[3], MultiBooleanStep), "Should be MultiBooleanStep"
        assert isinstance(root2.steps[4], StringStep), "Should be StringStep"
        assert isinstance(root2.steps[5], MultiStringStep), "Should be MultiStringStep"
        assert isinstance(root2.steps[6], SequenceCall), "Should be SequenceCall"
        assert isinstance(root2.steps[7], GenericStep), "Should be GenericStep"
        assert isinstance(root2.steps[8], GenericStep), "Should be GenericStep"
        assert isinstance(root2.steps[9], GenericStep), "Should be GenericStep"
        assert isinstance(root2.steps[10], ChartStep), "Should be ChartStep"
        
        print("✓ All step types correctly discriminated on deserialization")
        
        # Verify MultiBooleanStep doesn't have measurement field conflict
        multi_bool_step = root2.steps[3]
        assert hasattr(multi_bool_step, "measurements"), "MultiBooleanStep should have measurements"
        assert not hasattr(multi_bool_step, "measurement") or getattr(multi_bool_step, "measurement", None) is None, \
            "MultiBooleanStep should not have singular measurement field"
        print("✓ MultiBooleanStep field conflict resolved")
        
        # ========================================
        # SUBMIT TO SERVER
        # ========================================
        print("\n=== SUBMITTING TO SERVER ===")
        print(f"Submitting report with {step_count} different step types...")
        
        result = wats_client.report.submit_report(report)
        
        print(f"\n✓ Server accepted report: {result}")
        print(f"==============================\n")
        
        # Verify submission was successful
        assert result is not None, "Report submission returned None - server rejected the report"
        assert isinstance(result, str), f"Expected string result, got {type(result)}"
        assert len(result) > 0, "Report ID is empty"
        
        print(f"\n✅ SUCCESS: All step types accepted by server!")
        print(f"   Report ID: {result}")
        print(f"   Step count: {step_count}")
        print(f"   Architecture changes validated ✓")
        
    def test_submit_report_with_deeply_nested_sequences(
        self,
        wats_client: Any,
        test_serial_number: str,
        test_part_number: str
    ) -> None:
        """
        Test nested sequences with various step types at each level.
        Validates parent reference handling after deserialization.
        """
        report = UUTReport(
            pn=test_part_number,
            sn=f"{test_serial_number}-NESTED",
            rev="1.0",
            process_code=100,
            station_name="NestedTestStation",
            location="IntegrationTestLab",
            purpose="Test Nested Sequences",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        
        print(f"\n=== TESTING NESTED SEQUENCES ===")
        
        # Level 1
        root.add_numeric_step(name="RootTest", value=1.0, unit="V", status="P")
        
        # Level 2
        level2 = root.add_sequence_call(name="Level2Seq", file_name="l2.seq")
        level2.add_boolean_step(name="Level2Test", status="P")
        multi_num = level2.add_multi_numeric_step(name="Level2Multi", status="P")
        multi_num.add_measurement(name="M1", value=2.0, unit="V")
        multi_num.add_measurement(name="M2", value=3.0, unit="A")
        
        # Level 3
        level3 = level2.add_sequence_call(name="Level3Seq", file_name="l3.seq")
        level3.add_string_step(name="Level3Test", value="test", status="P")
        level3.add_generic_step(step_type="NI_Flow_While", name="WhileLoop", status="P")
        
        print(f"✓ Created 3-level nested structure")
        
        # Serialize and deserialize
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        report2 = UUTReport.model_validate_json(json_str)
        root2 = report2.get_root_sequence_call()
        
        # Verify parent references
        level2_2 = root2.steps[1]
        assert level2_2.parent == root2, "Level2 parent should be root"
        
        level3_2 = level2_2.steps[2]
        assert level3_2.parent == level2_2, "Level3 parent should be level2"
        
        assert level3_2.steps[0].parent == level3_2, "Level3 step parent should be level3"
        
        print("✓ Parent references correctly established")
        
        # Submit to server
        print("\n=== SUBMITTING TO SERVER ===")
        result = wats_client.report.submit_report(report)
        
        assert result is not None, "Nested report submission failed"
        print(f"\n✅ SUCCESS: Nested sequences accepted by server!")
        print(f"   Report ID: {result}")


if __name__ == "__main__":
    """Run tests manually for debugging"""
    pytest.main([__file__, "-v", "-s", "--tb=short"])
