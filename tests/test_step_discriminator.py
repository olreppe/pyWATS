"""
Test Step Type Discrimination and Serialization
Tests that step_type literals are preserved and discrimination works correctly
"""
import json
from datetime import datetime
from pyWATS.domains.report.report_models.uut.uut_report import UUTReport
from pyWATS.domains.report.report_models.uut.steps.numeric_step import NumericStep, MultiNumericStep
from pyWATS.domains.report.report_models.uut.steps.boolean_step import BooleanStep, MultiBooleanStep
from pyWATS.domains.report.report_models.uut.steps.string_step import StringStep, MultiStringStep
from pyWATS.domains.report.report_models.uut.steps.sequence_call import SequenceCall
from pyWATS.domains.report.report_models.uut.steps.generic_step import GenericStep
from pyWATS.domains.report.report_models.uut.steps.action_step import ActionStep
from pyWATS.domains.report.report_models.uut.steps.chart_step import ChartStep
from pyWATS.domains.report.report_models.uut.steps.callexe_step import CallExeStep
from pyWATS.domains.report.report_models.uut.steps.message_popup_step import MessagePopUpStep


class TestStepDiscriminator:
    """Test that step type discrimination and serialization work correctly"""
    
    def test_step_type_literals_in_serialization(self):
        """Test that step_type literals are preserved in JSON serialization"""
        report = UUTReport(
            pn="DISC-TEST",
            sn=f"SN-DISC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            rev="1.0",
            process_code=100,
            station_name="DiscriminatorTest",
            location="TestLab",
            purpose="Test Discriminator",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        
        # Add one of each step type
        root.add_numeric_step(name="NumTest", value=1.0, status="P")
        root.add_multi_numeric_step(name="MultiNumTest", status="P").add_measurement(
            name="M1", value=2.0, unit="V"
        )
        root.add_boolean_step(name="BoolTest", status="P")
        root.add_multi_boolean_step(name="MultiBoolTest", status="P").add_measurement(
            name="B1", status="P"
        )
        root.add_string_step(name="StringTest", value="test", status="P")
        root.add_multi_string_step(name="MultiStringTest", status="P").add_measurement(
            name="S1", value="val", status="P", comp_op="LOG"
        )
        sub_seq = root.add_sequence_call(name="SubSeq", file_name="sub.seq")
        root.add_generic_step(step_type="NI_Flow_If", name="IfStep", status="P")
        root.add_generic_step(step_type="Statement", name="StatementStep", status="P")
        
        # Serialize to JSON
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        json_data = json.loads(json_str)
        
        # Get steps from JSON (steps is at root level, not inside seqCall)
        steps = json_data["root"]["steps"]
        
        # Verify each step has correct step_type literal
        assert steps[0]["stepType"] == "ET_NLT", "NumericStep should have ET_NLT"
        assert steps[1]["stepType"] == "ET_MNLT", "MultiNumericStep should have ET_MNLT"
        assert steps[2]["stepType"] == "ET_PFT", "BooleanStep should have ET_PFT"
        assert steps[3]["stepType"] == "ET_MPFT", "MultiBooleanStep should have ET_MPFT"
        assert steps[4]["stepType"] == "ET_SVT", "StringStep should have ET_SVT"
        assert steps[5]["stepType"] == "ET_MSVT", "MultiStringStep should have ET_MSVT"
        assert steps[6]["stepType"] == "SequenceCall", "SequenceCall should have SequenceCall"
        assert steps[7]["stepType"] == "NI_Flow_If", "GenericStep should have NI_Flow_If"
        assert steps[8]["stepType"] == "Statement", "GenericStep should have Statement"
        
        print(f"✓ All step_type literals correctly serialized")
        
    def test_step_type_discrimination_on_deserialization(self):
        """Test that deserialization creates the correct Step subclass based on step_type"""
        report = UUTReport(
            pn="DISC-TEST-2",
            sn=f"SN-DISC2-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            rev="1.0",
            process_code=100,
            station_name="DiscriminatorTest2",
            location="TestLab",
            purpose="Test Discriminator 2",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        
        # Add various step types
        root.add_numeric_step(name="NumTest", value=1.0, status="P")
        root.add_multi_numeric_step(name="MultiNumTest", status="P").add_measurement(
            name="M1", value=2.0, unit="V"
        )
        root.add_multi_numeric_step(name="MultiNumTest2", status="P").add_measurement(
            name="M2", value=3.0, unit="A"
        )
        root.add_boolean_step(name="BoolTest", status="P")
        root.add_string_step(name="StringTest", value="test", status="P")
        sub_seq = root.add_sequence_call(name="SubSeq", file_name="sub.seq")
        sub_seq.add_numeric_step(name="NestedNum", value=5.0, status="P")
        root.add_generic_step(step_type="NI_Flow_If", name="IfStep", status="P")
        root.add_generic_step(step_type="Goto", name="GotoStep", status="P")
        
        # Serialize
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        
        # Deserialize
        report2 = UUTReport.model_validate_json(json_str)
        root2 = report2.get_root_sequence_call()
        
        # Verify correct types were created
        assert isinstance(root2.steps[0], NumericStep), "Should be NumericStep"
        assert root2.steps[0].step_type == "ET_NLT", "NumericStep should have ET_NLT"
        
        assert isinstance(root2.steps[1], MultiNumericStep), "Should be MultiNumericStep"
        assert root2.steps[1].step_type == "ET_MNLT", "MultiNumericStep should have ET_MNLT"
        assert len(root2.steps[1].measurements) == 1, "Should have 1 measurement"
        
        assert isinstance(root2.steps[2], MultiNumericStep), "Should be MultiNumericStep"
        assert len(root2.steps[2].measurements) == 1, "Should have 1 measurement"
        
        assert isinstance(root2.steps[3], BooleanStep), "Should be BooleanStep"
        assert root2.steps[3].step_type == "ET_PFT", "BooleanStep should have ET_PFT"
        
        assert isinstance(root2.steps[4], StringStep), "Should be StringStep"
        assert root2.steps[4].step_type == "ET_SVT", "StringStep should have ET_SVT"
        
        assert isinstance(root2.steps[5], SequenceCall), "Should be SequenceCall"
        assert root2.steps[5].step_type == "SequenceCall", "SequenceCall should have SequenceCall"
        assert len(root2.steps[5].steps) == 1, "SubSeq should have 1 child"
        assert isinstance(root2.steps[5].steps[0], NumericStep), "Nested should be NumericStep"
        
        assert isinstance(root2.steps[6], GenericStep), "Should be GenericStep"
        assert root2.steps[6].step_type == "NI_Flow_If", "Should preserve NI_Flow_If"
        
        assert isinstance(root2.steps[7], GenericStep), "Should be GenericStep"
        assert root2.steps[7].step_type == "Goto", "Should preserve Goto"
        
        print(f"✓ All step types correctly discriminated on deserialization")
        
    def test_parent_references_after_deserialization(self):
        """Test that parent references are correctly re-established after deserialization"""
        report = UUTReport(
            pn="PARENT-TEST",
            sn=f"SN-PARENT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            rev="1.0",
            process_code=100,
            station_name="ParentTest",
            location="TestLab",
            purpose="Test Parent References",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        root.add_numeric_step(name="RootNum", value=1.0, status="P")
        
        sub_seq = root.add_sequence_call(name="SubSeq", file_name="sub.seq")
        sub_seq.add_numeric_step(name="SubNum", value=2.0, status="P")
        
        deeper_seq = sub_seq.add_sequence_call(name="DeeperSeq", file_name="deeper.seq")
        deeper_seq.add_boolean_step(name="DeepBool", status="P")
        
        # Serialize and deserialize
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        report2 = UUTReport.model_validate_json(json_str)
        root2 = report2.get_root_sequence_call()
        
        # Verify parent references
        assert root2.parent is None, "Root should have no parent"
        
        assert root2.steps[0].parent == root2, "RootNum parent should be root"
        assert root2.steps[0].parent.name == "MainSequence Callback", "Parent name should match"
        
        sub_seq2 = root2.steps[1]
        assert sub_seq2.parent == root2, "SubSeq parent should be root"
        assert sub_seq2.steps[0].parent == sub_seq2, "SubNum parent should be SubSeq"
        
        deeper_seq2 = sub_seq2.steps[1]
        assert deeper_seq2.parent == sub_seq2, "DeeperSeq parent should be SubSeq"
        assert deeper_seq2.steps[0].parent == deeper_seq2, "DeepBool parent should be DeeperSeq"
        
        print(f"✓ All parent references correctly established after deserialization")
        
    def test_step_path_generation(self):
        """Test that get_step_path() works correctly with parent references"""
        report = UUTReport(
            pn="PATH-TEST",
            sn=f"SN-PATH-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            rev="1.0",
            process_code=100,
            station_name="PathTest",
            location="TestLab",
            purpose="Test Step Paths",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        step1 = root.add_numeric_step(name="Level1Test", value=1.0, status="P")
        
        level2 = root.add_sequence_call(name="Level2Seq", file_name="l2.seq")
        step2 = level2.add_boolean_step(name="Level2Test", status="P")
        
        level3 = level2.add_sequence_call(name="Level3Seq", file_name="l3.seq")
        step3 = level3.add_string_step(name="Level3Test", value="test", status="P")
        
        # Test paths
        assert step1.get_step_path() == "MainSequence Callback/Level1Test"
        assert step2.get_step_path() == "MainSequence Callback/Level2Seq/Level2Test"
        assert step3.get_step_path() == "MainSequence Callback/Level2Seq/Level3Seq/Level3Test"
        
        # Serialize/deserialize and test again
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        report2 = UUTReport.model_validate_json(json_str)
        root2 = report2.get_root_sequence_call()
        
        step1_2 = root2.steps[0]
        level2_2 = root2.steps[1]
        step2_2 = level2_2.steps[0]
        level3_2 = level2_2.steps[1]
        step3_2 = level3_2.steps[0]
        
        assert step1_2.get_step_path() == "MainSequence Callback/Level1Test"
        assert step2_2.get_step_path() == "MainSequence Callback/Level2Seq/Level2Test"
        assert step3_2.get_step_path() == "MainSequence Callback/Level2Seq/Level3Seq/Level3Test"
        
        print(f"✓ Step paths correctly generated before and after deserialization")


if __name__ == "__main__":
    test = TestStepDiscriminator()
    test.test_step_type_literals_in_serialization()
    test.test_step_type_discrimination_on_deserialization()
    test.test_parent_references_after_deserialization()
    test.test_step_path_generation()
    print("\n✅ All discriminator tests passed!")
