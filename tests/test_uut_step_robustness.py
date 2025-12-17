"""
Test UUT Step Parsing Robustness

Tests for:
1. Unknown step type handling (falls back to UnknownStep)
2. Numeric measurement with null/None unit tolerance
3. MultiNumericStep validation using correct high_limit (bug fix)
"""

import json
from datetime import datetime
import pytest
from pyWATS.domains.report.report_models.uut.uut_report import UUTReport
from pyWATS.domains.report.report_models.uut.steps.unknown_step import UnknownStep
from pyWATS.domains.report.report_models.uut.steps.numeric_step import NumericStep, MultiNumericStep
from pyWATS.domains.report.report_models.uut.steps.generic_step import GenericStep
from pyWATS.domains.report.report_models.uut.steps.sequence_call import SequenceCall


class TestUnknownStepParsing:
    """Test that unknown step types don't crash report parsing"""
    
    def test_unknown_step_type_parsed_as_unknown_step(self):
        """Unknown stepType should create UnknownStep instance"""
        report_json = {
            'pn': 'TEST',
            'sn': 'TEST-UNKNOWN-001',
            'rev': '1.0',
            'processCode': 100,
            'stationName': 'Test',
            'location': 'Lab',
            'purpose': 'Test',
            'result': 'P',
            'machineName': 'TestMachine',
            'start': '2024-01-01T00:00:00+00:00',
            'root': {
                'stepType': 'SequenceCall',
                'name': 'MainSequence',
                'group': 'M',
                'status': 'P',
                'seqCall': {
                    'name': 'main.seq',
                    'path': '/path',
                    'version': '1.0'
                },
                'steps': [
                    {
                        'stepType': 'ET_A',  # Unknown step type
                        'name': 'UnknownStepType',
                        'group': 'M',
                        'status': 'P'
                    }
                ]
            }
        }
        
        # Should not raise exception
        report = UUTReport.model_validate(report_json)
        
        # Check that the step was parsed as UnknownStep
        assert len(report.root.steps) == 1
        step = report.root.steps[0]
        assert isinstance(step, UnknownStep)
        assert step.step_type == 'ET_A'
        assert step.name == 'UnknownStepType'
    
    def test_multiple_unknown_step_types(self):
        """Multiple unknown step types should all be handled"""
        report_json = {
            'pn': 'TEST',
            'sn': 'TEST-UNKNOWN-002',
            'rev': '1.0',
            'processCode': 100,
            'stationName': 'Test',
            'location': 'Lab',
            'purpose': 'Test',
            'result': 'P',
            'machineName': 'TestMachine',
            'start': '2024-01-01T00:00:00+00:00',
            'root': {
                'stepType': 'SequenceCall',
                'name': 'MainSequence',
                'group': 'M',
                'status': 'P',
                'seqCall': {
                    'name': 'main.seq',
                    'path': '/path',
                    'version': '1.0'
                },
                'steps': [
                    {'stepType': 'ET_A', 'name': 'Unknown1', 'group': 'M', 'status': 'P'},
                    {'stepType': 'ET_CUSTOM', 'name': 'Unknown2', 'group': 'M', 'status': 'F'},
                    {'stepType': 'FUTURE_TYPE', 'name': 'Unknown3', 'group': 'M', 'status': 'P'}
                ]
            }
        }
        
        report = UUTReport.model_validate(report_json)
        
        assert len(report.root.steps) == 3
        for step in report.root.steps:
            assert isinstance(step, UnknownStep)
    
    def test_unknown_step_preserves_step_type_in_serialization(self):
        """Unknown step types should be preserved during serialization"""
        report_json = {
            'pn': 'TEST',
            'sn': 'TEST-UNKNOWN-003',
            'rev': '1.0',
            'processCode': 100,
            'stationName': 'Test',
            'location': 'Lab',
            'purpose': 'Test',
            'result': 'P',
            'machineName': 'TestMachine',
            'start': '2024-01-01T00:00:00+00:00',
            'root': {
                'stepType': 'SequenceCall',
                'name': 'MainSequence',
                'group': 'M',
                'status': 'P',
                'seqCall': {
                    'name': 'main.seq',
                    'path': '/path',
                    'version': '1.0'
                },
                'steps': [
                    {'stepType': 'ET_FUTURE', 'name': 'FutureStep', 'group': 'M', 'status': 'P'}
                ]
            }
        }
        
        report = UUTReport.model_validate(report_json)
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        json_data = json.loads(json_str)
        
        # Check that stepType is preserved in JSON
        assert json_data['root']['steps'][0]['stepType'] == 'ET_FUTURE'
        
        # Round-trip should work
        report2 = UUTReport.model_validate_json(json_str)
        assert isinstance(report2.root.steps[0], UnknownStep)
        assert report2.root.steps[0].step_type == 'ET_FUTURE'
    
    def test_mixed_known_and_unknown_steps(self):
        """Mix of known and unknown step types should all parse correctly"""
        report_json = {
            'pn': 'TEST',
            'sn': 'TEST-MIXED-001',
            'rev': '1.0',
            'processCode': 100,
            'stationName': 'Test',
            'location': 'Lab',
            'purpose': 'Test',
            'result': 'P',
            'machineName': 'TestMachine',
            'start': '2024-01-01T00:00:00+00:00',
            'root': {
                'stepType': 'SequenceCall',
                'name': 'MainSequence',
                'group': 'M',
                'status': 'P',
                'seqCall': {
                    'name': 'main.seq',
                    'path': '/path',
                    'version': '1.0'
                },
                'steps': [
                    {
                        'stepType': 'ET_NLT',
                        'name': 'NumStep',
                        'group': 'M',
                        'status': 'P',
                        'numericMeas': [{'value': 1.5, 'unit': 'V', 'status': 'P'}]
                    },
                    {
                        'stepType': 'ET_UNKNOWN',
                        'name': 'UnknownStep',
                        'group': 'M',
                        'status': 'P'
                    },
                    {
                        'stepType': 'NI_Flow_If',
                        'name': 'IfStep',
                        'group': 'M',
                        'status': 'P'
                    }
                ]
            }
        }
        
        report = UUTReport.model_validate(report_json)
        
        assert len(report.root.steps) == 3
        assert isinstance(report.root.steps[0], NumericStep)
        assert isinstance(report.root.steps[1], UnknownStep)
        assert isinstance(report.root.steps[2], GenericStep)


class TestNumericMeasurementNullTolerance:
    """Test that numeric measurements tolerate null/None unit values"""
    
    def test_numeric_measurement_with_null_unit(self):
        """NumericMeasurement should accept unit=None"""
        report_json = {
            'pn': 'TEST',
            'sn': 'TEST-NULL-UNIT-001',
            'rev': '1.0',
            'processCode': 100,
            'stationName': 'Test',
            'location': 'Lab',
            'purpose': 'Test',
            'result': 'P',
            'machineName': 'TestMachine',
            'start': '2024-01-01T00:00:00+00:00',
            'root': {
                'stepType': 'SequenceCall',
                'name': 'MainSequence',
                'group': 'M',
                'status': 'P',
                'seqCall': {
                    'name': 'main.seq',
                    'path': '/path',
                    'version': '1.0'
                },
                'steps': [
                    {
                        'stepType': 'ET_NLT',
                        'name': 'NumericWithNullUnit',
                        'group': 'M',
                        'status': 'P',
                        'numericMeas': [
                            {
                                'value': 42.0,
                                'unit': None,  # Null unit
                                'status': 'P'
                            }
                        ]
                    }
                ]
            }
        }
        
        # Should not raise exception
        report = UUTReport.model_validate(report_json)
        
        step = report.root.steps[0]
        assert isinstance(step, NumericStep)
        assert step.measurement.value == 42.0
        assert step.measurement.unit is None
    
    def test_multi_numeric_measurement_with_null_unit(self):
        """MultiNumericMeasurement should accept unit=None"""
        report_json = {
            'pn': 'TEST',
            'sn': 'TEST-MULTI-NULL-001',
            'rev': '1.0',
            'processCode': 100,
            'stationName': 'Test',
            'location': 'Lab',
            'purpose': 'Test',
            'result': 'P',
            'machineName': 'TestMachine',
            'start': '2024-01-01T00:00:00+00:00',
            'root': {
                'stepType': 'SequenceCall',
                'name': 'MainSequence',
                'group': 'M',
                'status': 'P',
                'seqCall': {
                    'name': 'main.seq',
                    'path': '/path',
                    'version': '1.0'
                },
                'steps': [
                    {
                        'stepType': 'ET_MNLT',
                        'name': 'MultiNumericStep',
                        'group': 'M',
                        'status': 'P',
                        'numericMeas': [
                            {'name': 'M1', 'value': 1.0, 'unit': None, 'status': 'P'},
                            {'name': 'M2', 'value': 2.0, 'unit': 'V', 'status': 'P'}
                        ]
                    }
                ]
            }
        }
        
        report = UUTReport.model_validate(report_json)
        
        step = report.root.steps[0]
        assert isinstance(step, MultiNumericStep)
        assert len(step.measurements) == 2
        assert step.measurements[0].unit is None
        assert step.measurements[1].unit == 'V'
    
    def test_numeric_measurement_serialization_with_null_unit(self):
        """Serialization should handle null units correctly"""
        report_json = {
            'pn': 'TEST',
            'sn': 'TEST-NULL-SER-001',
            'rev': '1.0',
            'processCode': 100,
            'stationName': 'Test',
            'location': 'Lab',
            'purpose': 'Test',
            'result': 'P',
            'machineName': 'TestMachine',
            'start': '2024-01-01T00:00:00+00:00',
            'root': {
                'stepType': 'SequenceCall',
                'name': 'MainSequence',
                'group': 'M',
                'status': 'P',
                'seqCall': {
                    'name': 'main.seq',
                    'path': '/path',
                    'version': '1.0'
                },
                'steps': [
                    {
                        'stepType': 'ET_NLT',
                        'name': 'NumStep',
                        'group': 'M',
                        'status': 'P',
                        'numericMeas': [{'value': 1.0, 'unit': None, 'status': 'P'}]
                    }
                ]
            }
        }
        
        report = UUTReport.model_validate(report_json)
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        
        # Should not raise exception
        report2 = UUTReport.model_validate_json(json_str)
        assert report2.root.steps[0].measurement.unit is None


class TestMultiNumericStepValidation:
    """Test that MultiNumericStep validation uses correct high_limit"""
    
    def test_validate_step_uses_correct_high_limit(self):
        """Validation should use high_limit, not low_limit for high limit check"""
        # Create a report with a MultiNumericStep
        report = UUTReport(
            pn='TEST',
            sn='TEST-VALIDATION-001',
            rev='1.0',
            process_code=100,
            station_name='Test',
            location='Lab',
            purpose='Test',
            result='P',
            machine_name='TestMachine',
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        
        # Add a MultiNumericStep with specific limits
        multi_step = root.add_multi_numeric_step(name='MultiTest', status='P')
        
        # Add measurements with different limits
        from pyWATS.domains.report.report_models.uut.steps.comp_operator import CompOp
        multi_step.add_measurement(
            name='M1',
            value=5.0,
            unit='V',
            status='P',
            comp_op=CompOp.GELE,  # Greater Equal, Less Equal
            low_limit=0.0,
            high_limit=10.0
        )
        multi_step.add_measurement(
            name='M2',
            value=15.0,
            unit='V',
            status='P',
            comp_op=CompOp.GELE,
            low_limit=10.0,
            high_limit=20.0
        )
        
        # Validate should pass without errors
        errors = []
        result = multi_step.validate_step(trigger_children=False, errors=errors)
        
        # Should validate successfully (using correct high_limit)
        assert result is True
        assert len(errors) == 0
    
    def test_validation_detects_invalid_limits(self):
        """Validation should detect when limits are actually invalid"""
        report = UUTReport(
            pn='TEST',
            sn='TEST-VALIDATION-002',
            rev='1.0',
            process_code=100,
            station_name='Test',
            location='Lab',
            purpose='Test',
            result='P',
            machine_name='TestMachine',
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        multi_step = root.add_multi_numeric_step(name='MultiTest', status='P')
        
        from pyWATS.domains.report.report_models.uut.steps.comp_operator import CompOp
        # Add measurement with invalid limits (low > high)
        multi_step.add_measurement(
            name='M1',
            value=5.0,
            unit='V',
            status='P',
            comp_op=CompOp.GELE,
            low_limit=20.0,   # Invalid: low > high
            high_limit=10.0
        )
        
        errors = []
        result = multi_step.validate_step(trigger_children=False, errors=errors)
        
        # Should detect the invalid limits
        assert result is False
        assert len(errors) > 0


class TestSequenceCallChildSteps:
    """Test that SequenceCall child step parsing still works correctly"""
    
    def test_nested_sequence_calls_with_unknown_steps(self):
        """Nested SequenceCalls should handle unknown steps in children"""
        report_json = {
            'pn': 'TEST',
            'sn': 'TEST-NESTED-001',
            'rev': '1.0',
            'processCode': 100,
            'stationName': 'Test',
            'location': 'Lab',
            'purpose': 'Test',
            'result': 'P',
            'machineName': 'TestMachine',
            'start': '2024-01-01T00:00:00+00:00',
            'root': {
                'stepType': 'SequenceCall',
                'name': 'MainSequence',
                'group': 'M',
                'status': 'P',
                'seqCall': {
                    'name': 'main.seq',
                    'path': '/path',
                    'version': '1.0'
                },
                'steps': [
                    {
                        'stepType': 'SequenceCall',
                        'name': 'SubSequence',
                        'group': 'M',
                        'status': 'P',
                        'seqCall': {
                            'name': 'sub.seq',
                            'path': '/path',
                            'version': '1.0'
                        },
                        'steps': [
                            {
                                'stepType': 'ET_UNKNOWN',
                                'name': 'UnknownInChild',
                                'group': 'M',
                                'status': 'P'
                            }
                        ]
                    }
                ]
            }
        }
        
        report = UUTReport.model_validate(report_json)
        
        # Check structure
        assert isinstance(report.root, SequenceCall)
        assert len(report.root.steps) == 1
        
        sub_seq = report.root.steps[0]
        assert isinstance(sub_seq, SequenceCall)
        assert len(sub_seq.steps) == 1
        
        child_step = sub_seq.steps[0]
        assert isinstance(child_step, UnknownStep)
        assert child_step.step_type == 'ET_UNKNOWN'
    
    def test_parent_references_with_unknown_steps(self):
        """Parent references should work correctly with UnknownStep"""
        report = UUTReport(
            pn='TEST',
            sn='TEST-PARENT-001',
            rev='1.0',
            process_code=100,
            station_name='Test',
            location='Lab',
            purpose='Test',
            result='P',
            machine_name='TestMachine',
            start=datetime.now().astimezone()
        )
        
        root = report.get_root_sequence_call()
        
        # Create JSON with unknown step and parse
        json_str = report.model_dump_json(by_alias=True, exclude_none=True)
        json_data = json.loads(json_str)
        
        # Add unknown step to JSON
        json_data['root']['steps'] = [
            {'stepType': 'ET_UNKNOWN', 'name': 'UnknownStep', 'group': 'M', 'status': 'P'}
        ]
        
        # Parse back
        report2 = UUTReport.model_validate(json_data)
        
        # Check parent reference
        unknown_step = report2.root.steps[0]
        assert isinstance(unknown_step, UnknownStep)
        assert unknown_step.parent == report2.root
        
        # Check get_step_path works
        path = unknown_step.get_step_path()
        assert 'UnknownStep' in path


if __name__ == "__main__":
    """Run tests manually for quick verification"""
    import sys
    
    test_classes = [
        TestUnknownStepParsing,
        TestNumericMeasurementNullTolerance,
        TestMultiNumericStepValidation,
        TestSequenceCallChildSteps
    ]
    
    passed = 0
    failed = 0
    
    for test_cls in test_classes:
        print(f"\n{'='*60}")
        print(f"Running {test_cls.__name__}")
        print('='*60)
        
        test_obj = test_cls()
        test_methods = [m for m in dir(test_obj) if m.startswith('test_')]
        
        for method_name in test_methods:
            try:
                print(f"\n  Testing: {method_name}")
                method = getattr(test_obj, method_name)
                method()
                print(f"    ✓ PASSED")
                passed += 1
            except Exception as e:
                print(f"    ✗ FAILED: {e}")
                import traceback
                traceback.print_exc()
                failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print('='*60)
    
    sys.exit(0 if failed == 0 else 1)
