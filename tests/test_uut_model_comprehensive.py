"""
Comprehensive UUT Model Test
Tests all variants of all step types with extensive examples
"""
"""
Comprehensive UUT Model Test
Tests all variants of all step types with extensive examples
"""
from datetime import datetime

from pyWATS.domains.report.report_models.chart import ChartType
from pyWATS.domains.report.report_models.uut.steps.comp_operator import CompOp
from pyWATS.domains.report.report_models.uut.steps.generic_step import FlowType
from pyWATS.domains.report.report_models.uut.steps.sequence_call import SequenceCall
from pyWATS.domains.report.report_models.uut.uut_report import UUTReport


class TestUUTModelComprehensive:
    """Comprehensive test of all UUT step types and variants"""
    
    def test_extensive_uut_model(self):
        """
        Create an extensive UUT test with virtually all variants of all step types.
        Part number: UUTMODELTEST
        Keep total steps under 1000
        """
        report = UUTReport(
            pn="UUTMODELTEST",
            sn=f"SN-COMPREHENSIVE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            rev="1.0",
            process_code=100,
            station_name="ComprehensiveTestStation",
            location="TestLab",
            purpose="Comprehensive Model Test",
            result="P",
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        step_count = 0
        
        # ==================== NUMERIC STEPS ====================
        print("\n=== Testing Numeric Steps ===")
        numeric_seq = root.add_sequence_call(name="NumericTests", file_name="numeric.seq")
        
        # Single numeric steps with different comparison operators
        for i, (comp_op, name) in enumerate([
            (CompOp.GELE, "VoltageTest_GELE"),
            (CompOp.GT, "CurrentTest_GT"),
            (CompOp.LT, "ResistanceTest_LT"),
            (CompOp.GE, "PowerTest_GE"),
            (CompOp.LE, "FrequencyTest_LE"),
            (CompOp.EQ, "CountTest_EQ"),
            (CompOp.NE, "StatusTest_NE"),
            (CompOp.LOG, "DataLogging_LOG"),
            (CompOp.GTLT, "RangeTest_GTLT"),
            (CompOp.LEGE, "ToleranceTest_LEGE"),
        ]):
            numeric_seq.add_numeric_step(
                name=name,
                value=float(i + 1) * 1.5,
                unit="V" if i % 2 == 0 else "A",
                comp_op=comp_op,
                low_limit=float(i) if comp_op in [CompOp.GELE, CompOp.GE, CompOp.GTLT, CompOp.LEGE] else None,
                high_limit=float(i + 2) if comp_op in [CompOp.GELE, CompOp.LE, CompOp.GTLT, CompOp.LEGE] else None,
                status="P"
            )
            step_count += 1
        
        # Multi numeric steps with varying measurement counts
        for test_num in range(5):
            mns = numeric_seq.add_multi_numeric_step(
                name=f"MultiNumericTest_{test_num}",
                status="P"
            )
            # Add different numbers of measurements (2-6)
            for meas_num in range(2 + test_num):
                mns.add_measurement(
                    name=f"Measurement_{meas_num}",
                    value=float(test_num * 10 + meas_num),
                    unit="V" if meas_num % 2 == 0 else "mA",
                    comp_op=CompOp.GELE if meas_num % 2 == 0 else CompOp.LOG,
                    low_limit=float(test_num * 10) if meas_num % 2 == 0 else None,
                    high_limit=float(test_num * 10 + 10) if meas_num % 2 == 0 else None
                )
            step_count += 1
        
        print(f"Numeric steps created: {step_count}")
        
        # ==================== BOOLEAN STEPS ====================
        print("\n=== Testing Boolean Steps ===")
        boolean_seq = root.add_sequence_call(name="BooleanTests", file_name="boolean.seq")
        
        # Single boolean steps
        for i, status in enumerate(["P", "P", "P", "F", "P", "P", "F", "P", "S", "P"]):
            boolean_seq.add_boolean_step(
                name=f"BooleanTest_{i}_{status}",
                status=status
            )
            step_count += 1
        
        # Multi boolean steps with varying measurement counts
        for test_num in range(5):
            mbs = boolean_seq.add_multi_boolean_step(
                name=f"MultiBooleanTest_{test_num}",
                status="P" if test_num < 4 else "F"
            )
            # Add different numbers of measurements (2-6)
            for meas_num in range(2 + test_num):
                mbs.add_measurement(
                    name=f"Check_{meas_num}",
                    status="P" if (test_num < 4 or meas_num != 0) else "F"
                )
            step_count += 1
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== STRING STEPS ====================
        print("\n=== Testing String Steps ===")
        string_seq = root.add_sequence_call(name="StringTests", file_name="string.seq")
        
        # Single string steps
        test_strings = [
            "SerialNumber", "FirmwareVersion", "HardwareRevision",
            "CalibrationDate", "Manufacturer", "Model",
            "BatchNumber", "LotCode", "ProductionLine", "Inspector"
        ]
        for i, value in enumerate(test_strings):
            string_seq.add_string_step(
                name=f"StringTest_{i}",
                value=f"{value}_{i}",
                unit="NA",
                comp_op=CompOp.LOG,
                status="P"
            )
            step_count += 1
        
        # Multi string steps
        for test_num in range(5):
            mss = string_seq.add_multi_string_step(
                name=f"MultiStringTest_{test_num}",
                status="P"
            )
            # Add different numbers of measurements
            string_names = ["Serial", "Version", "Revision", "Date", "Operator", "Location"]
            for meas_num in range(2 + test_num):
                if meas_num < len(string_names):
                    mss.add_measurement(
                        name=string_names[meas_num],
                        value=f"{string_names[meas_num]}_{test_num}_{meas_num}",
                        status="P",
                        comp_op=CompOp.LOG
                    )
            step_count += 1
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== NESTED SEQUENCES ====================
        print("\n=== Testing Nested Sequences ===")
        nested_seq = root.add_sequence_call(name="NestedSequences", file_name="nested.seq")
        
        # Create 3 levels of nesting with tests at each level
        for level1 in range(3):
            seq_l1 = nested_seq.add_sequence_call(
                name=f"Level1_Seq_{level1}",
                file_name=f"level1_{level1}.seq"
            )
            seq_l1.add_numeric_step(name=f"L1_Test_{level1}", value=float(level1), status="P")
            step_count += 2  # sequence + test
            
            for level2 in range(2):
                seq_l2 = seq_l1.add_sequence_call(
                    name=f"Level2_Seq_{level1}_{level2}",
                    file_name=f"level2_{level1}_{level2}.seq"
                )
                seq_l2.add_boolean_step(name=f"L2_Test_{level1}_{level2}", status="P")
                step_count += 2  # sequence + test
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== MIXED SEQUENCE ====================
        print("\n=== Testing Mixed Step Types ===")
        mixed_seq = root.add_sequence_call(name="MixedTests", file_name="mixed.seq")
        
        # Create a sequence with all step types mixed
        for i in range(10):
            # Rotate through different step types
            if i % 5 == 0:
                mixed_seq.add_numeric_step(name=f"Mixed_Numeric_{i}", value=float(i), status="P")
            elif i % 5 == 1:
                mixed_seq.add_boolean_step(name=f"Mixed_Boolean_{i}", status="P")
            elif i % 5 == 2:
                mixed_seq.add_string_step(name=f"Mixed_String_{i}", value=f"Value_{i}", status="P")
            elif i % 5 == 3:
                mns = mixed_seq.add_multi_numeric_step(name=f"Mixed_MultiNum_{i}", status="P")
                mns.add_measurement(name="M1", value=float(i), unit="V")
                mns.add_measurement(name="M2", value=float(i+1), unit="A")
            else:
                mbs = mixed_seq.add_multi_boolean_step(name=f"Mixed_MultiBool_{i}", status="P")
                mbs.add_measurement(name="C1", status="P")
                mbs.add_measurement(name="C2", status="P")
            step_count += 1
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== ACTION STEPS ====================
        print("\n=== Testing Action Steps ===")
        action_seq = root.add_sequence_call(name="ActionTests", file_name="action.seq")
        
        # Add various action steps
        for i in range(10):
            action_seq.add_generic_step(
                step_type="Action",
                name=f"ActionStep_{i}",
                status="P"
            )
            step_count += 1
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== GENERIC/FLOW STEPS ====================
        print("\n=== Testing Generic/Flow Steps ===")
        flow_seq = root.add_sequence_call(name="FlowTests", file_name="flow.seq")
        
        # Test various flow types
        flow_types = [
            "NI_Flow_If", "NI_Flow_Else", "NI_Flow_End",
            "NI_Flow_For", "NI_Flow_While",
            "Goto", "Statement", "Label"
        ]
        for i, flow_type in enumerate(flow_types):
            flow_seq.add_generic_step(
                step_type=flow_type,
                name=f"FlowStep_{flow_type}_{i}",
                status="P"
            )
            step_count += 1
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== CHART STEPS ====================
        print("\n=== Testing Chart Steps ===")
        chart_seq = root.add_sequence_call(name="ChartTests", file_name="chart.seq")
        
        # Create chart steps with different chart types
        from pyWATS.domains.report.report_models.chart import ChartSeries
        
        for i, chart_type in enumerate([ChartType.LINE, ChartType.LINE_LOG_X]):
            # Create series data (x_data and y_data are semicolon-separated strings)
            x_values = ";".join([str(float(j)) for j in range(5)])
            y_values = ";".join([str(float(j * 2)) for j in range(5)])
            
            series = ChartSeries(
                name=f"Series_{i}",
                x_data=x_values,
                y_data=y_values
            )
            
            chart_seq.add_chart_step(
                name=f"ChartStep_{chart_type.value}_{i}",
                chart_type=chart_type,
                label=f"Chart {i}",
                x_label="Time",
                x_unit="s",
                y_label="Value",
                y_unit="V",
                series=[series],
                status="P"
            )
            step_count += 1
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== STATUS VARIATIONS ====================
        print("\n=== Testing Status Variations ===")
        status_seq = root.add_sequence_call(name="StatusTests", file_name="status.seq")
        
        # Create steps with different status values
        statuses = ["P", "P", "P", "F", "S", "P", "F", "P", "P", "P"]
        for i, status in enumerate(statuses):
            status_seq.add_numeric_step(
                name=f"StatusTest_{status}_{i}",
                value=float(i),
                unit="V",
                status=status
            )
            step_count += 1
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== EDGE CASES ====================
        print("\n=== Testing Edge Cases ===")
        edge_seq = root.add_sequence_call(name="EdgeCaseTests", file_name="edge.seq")
        
        # Very large values
        edge_seq.add_numeric_step(name="LargeValue", value=1e10, unit="V", status="P")
        
        # Very small values
        edge_seq.add_numeric_step(name="SmallValue", value=1e-10, unit="V", status="P")
        
        # Negative values
        edge_seq.add_numeric_step(name="NegativeValue", value=-123.456, unit="V", status="P")
        
        # Zero value
        edge_seq.add_numeric_step(name="ZeroValue", value=0.0, unit="V", status="P")
        
        # Long name
        edge_seq.add_numeric_step(
            name="VeryLongStepNameToTestNameLengthHandling" * 2,
            value=1.0,
            unit="V",
            status="P"
        )
        
        step_count += 5
        
        print(f"Total steps so far: {step_count}")
        
        # ==================== BULK TESTS ====================
        print("\n=== Adding Bulk Tests to Reach Target ===")
        bulk_seq = root.add_sequence_call(name="BulkTests", file_name="bulk.seq")
        
        # Add more tests to approach but stay under 1000 steps
        remaining = 950 - step_count  # Leave buffer for safety
        if remaining > 0:
            # Add bulk numeric tests
            for i in range(min(remaining, 500)):
                bulk_seq.add_numeric_step(
                    name=f"BulkTest_{i}",
                    value=float(i),
                    unit="V",
                    status="P" if i % 10 != 0 else "F"
                )
                step_count += 1
                if step_count >= 950:
                    break
        
        print(f"\n=== FINAL STEP COUNT: {step_count} ===")
        assert step_count < 1000, f"Step count {step_count} exceeds 1000"
        
        # ==================== SERIALIZATION TEST ====================
        print("\n=== Testing Serialization/Deserialization ===")
        
        # Serialize to JSON
        json_data = report.model_dump_json(by_alias=True, exclude_none=True)
        json_size = len(json_data)
        print(f"JSON size: {json_size:,} bytes ({json_size / 1024 / 1024:.2f} MB)")
        
        # Deserialize
        report2 = UUTReport.model_validate_json(json_data)
        root2 = report2.get_root_sequence_call()
        
        # Verify structure
        assert report2.pn == "UUTMODELTEST"
        assert len(root2.steps) == len(root.steps)
        
        # Count steps in deserialized report
        def count_steps(seq):
            count = 0
            for step in seq.steps:
                count += 1
                if isinstance(step, SequenceCall):
                    count += count_steps(step)
            return count
        
        deserialized_count = count_steps(root2)
        print(f"Deserialized step count: {deserialized_count}")
        
        print("\n=== TEST COMPLETE ===")
        print(f"✓ Created {step_count} steps")
        print(f"✓ All step types tested")
        print(f"✓ Serialization/deserialization successful")
        print(f"✓ Part number: {report.pn}")
        print(f"✓ Serial number: {report.sn}")
