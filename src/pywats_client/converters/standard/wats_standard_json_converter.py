"""
WATS Standard JSON Format Converter (WSJF)

Converts WATS Standard JSON Format (WSJF) files into WATS reports.
Port of the C# WATSStandardJsonFormat converter.

Expected file format:
- JSON file with WSJF schema
- Root object with type, pn, sn, rev, result, root (step tree)

The WSJF format is a JSON representation of WATS test reports that closely
mirrors the WATS data model. This converter essentially passes through
the data with minimal transformation since it's already in WATS-compatible format.

Step types:
- SequenceCall: Container for nested steps
- ET_NLT: Numeric Limit Test
- ET_MNLT: Multiple Numeric Limit Test
- ET_PFT: Pass/Fail Test
- ET_SVT: String Value Test
- ET_A: Action Step

Returns:
    UUTReport or UURReport models - NOT dicts. These are proper Pydantic models
    that can be submitted directly to the WATS API.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pywats_client.converters.file_converter import FileConverter
from pywats_client.converters.context import ConverterContext
from pywats_client.converters.models import (
    ConverterSource,
    ConverterResult,
    ValidationResult,
    PostProcessAction,
    ArgumentDefinition,
    ArgumentType,
)

# Import report models for proper typed returns
from pywats.domains.report.report_models import UUTReport, UURReport


class WATSStandardJsonConverter(FileConverter):
    """
    Converts WATS Standard JSON Format (WSJF) files to WATS reports.
    
    File qualification:
    - JSON file with .json extension
    - Contains required WSJF fields: type, pn/partNumber, sn/serialNumber, root
    """
    
    def __init__(self):
        """Initialize converter with default post-process action"""
        from ..models import PostProcessAction
        super().__init__()
        self.post_process_action = PostProcessAction.MOVE
        self.archive_path = None  # Set by async_converter_pool from config
    
    @property
    def name(self) -> str:
        return "WATS Standard JSON Format Converter"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Converts WATS Standard JSON Format (WSJF) files into WATS reports"
    
    @property
    def file_patterns(self) -> List[str]:
        return ["*.json"]
    
    @property
    def arguments_schema(self) -> Dict[str, ArgumentDefinition]:
        return {
            "defaultProcessCode": ArgumentDefinition(
                arg_type=ArgumentType.STRING,
                default="10",
                description="Default process code if not specified in file",
            ),
        }
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        """
        Validate that the file is a WSJF format file.
        
        Confidence levels:
        - 0.98: Valid JSON with all required WSJF fields
        - 0.85: Valid JSON with partial WSJF fields
        - 0.5: Valid JSON but not WSJF format
        - 0.0: Not valid JSON
        """
        if not source.path or not source.path.exists():
            return ValidationResult.no_match("File not found")
        
        suffix = source.path.suffix.lower()
        if suffix != '.json':
            return ValidationResult.no_match("Not a JSON file")
        
        try:
            with open(source.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, dict):
                return ValidationResult.no_match("JSON is not an object")
            
            # Check for WSJF required fields
            has_type = 'type' in data
            has_pn = 'pn' in data or 'partNumber' in data
            has_sn = 'sn' in data or 'serialNumber' in data
            has_root = 'root' in data
            
            # Type should be 'T' (Test/UUT) or 'U' (UUR)
            report_type = data.get('type', '')
            is_valid_type = report_type in ('T', 'U', 'UUT', 'UUR', 'Test')
            
            if has_type and has_root and is_valid_type:
                part_number = data.get('pn', data.get('partNumber', ''))
                serial_number = data.get('sn', data.get('serialNumber', ''))
                result = data.get('result', 'P')
                
                return ValidationResult(
                    can_convert=True,
                    confidence=0.98,
                    message="WATS Standard JSON Format (WSJF) file",
                    detected_part_number=part_number,
                    detected_serial_number=serial_number,
                    detected_result="Passed" if result in ('P', 'Passed') else "Failed",
                )
            
            if has_pn or has_sn:
                return ValidationResult(
                    can_convert=True,
                    confidence=0.7,
                    message="Possible WSJF file (partial structure)",
                )
            
            return ValidationResult(
                can_convert=True,
                confidence=0.5,
                message="JSON file but not WSJF format",
            )
            
        except json.JSONDecodeError as e:
            return ValidationResult.no_match(f"Invalid JSON: {e}")
        except Exception as e:
            return ValidationResult.no_match(f"Error reading file: {e}")
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        """
        Convert WSJF file to WATS report with legacy format tolerance.
        
        Sanitizes legacy WSJF data and applies API model defaults for missing fields.
        """
        if not source.path:
            return ConverterResult.failed_result(error="No file path provided")
        
        try:
            with open(source.path, 'r', encoding='utf-8') as f:
                wsjf_data = json.load(f)
            
            # Sanitize data before validation
            self._sanitize_wsjf_data(wsjf_data, context)
            print(f"[DEBUG] Sanitization complete")
            
            # Detect report type: UUT (test) or UUR (repair)
            report_type = wsjf_data.get('type', 'T')
            is_uur = report_type in ('U', 'UUR', 'R', 'Repair')
            print(f"[DEBUG] Report type: {report_type}, is_uur: {is_uur}")
            
            # Let Pydantic do validation with sanitized data
            try:
                if is_uur:
                    validated_report: Union[UUTReport, UURReport] = UURReport.model_validate(wsjf_data)
                else:
                    validated_report = UUTReport.model_validate(wsjf_data)
                print(f"[DEBUG] Validation successful")
            except Exception as validation_error:
                print(f"[DEBUG] Validation failed: {validation_error}")
                return ConverterResult.failed_result(
                    error=f"WSJF validation failed: {validation_error}"
                )
            
            print(f"[DEBUG] Returning success result")
            return ConverterResult.success_result(
                report=validated_report,
                post_action=PostProcessAction.MOVE,
            )
            
        except json.JSONDecodeError as e:
            return ConverterResult.failed_result(error=f"Invalid JSON: {e}")
        except Exception as e:
            return ConverterResult.failed_result(error=f"Conversion error: {e}")
    
    def _sanitize_wsjf_data(self, data: Dict[str, Any], context: ConverterContext) -> None:
        """
        Sanitize WSJF data for API compatibility.
        
        - Removes legacy fields not in current API models
        - Applies defaults from API models for missing required fields
        - Uses "" for missing string fields with no API default
        - Recursively cleans nested structures
        """
        print(f"[DEBUG] _sanitize_wsjf_data called for SN: {data.get('sn', 'N/A')}")
        
        # Legacy fields that don't exist in current API - remove them
        legacy_fields = ['num', 'passed', 'failed', 'startingIndex', 'endingIndex']
        for field in legacy_fields:
            data.pop(field, None)
        
        # Apply API model defaults for missing required fields
        # Report level defaults
        if 'type' not in data or not data['type']:
            data['type'] = 'T'
        if 'result' not in data or not data['result']:
            data['result'] = 'P'
        if 'rev' not in data or not data['rev']:
            data['rev'] = "-"
        if 'processCode' not in data or data['processCode'] is None:
            data['processCode'] = int(context.get_argument("defaultProcessCode", "10"))
        if 'machineName' not in data or not data['machineName']:
            data['machineName'] = "-"
        if 'location' not in data or not data['location']:
            data['location'] = "-"
        if 'purpose' not in data or not data['purpose']:
            data['purpose'] = "-"
        
        # Clean root step if present
        if 'root' in data and isinstance(data['root'], dict):
            self._sanitize_step(data['root'])
        
        # Clean unit/uut if present
        if 'unit' in data and isinstance(data['unit'], dict):
            self._sanitize_unit(data['unit'])
        if 'uut' in data and isinstance(data['uut'], dict):
            self._sanitize_unit(data['uut'])
    
    def _sanitize_step(self, step: Dict[str, Any]) -> None:
        """
        Sanitize a step object recursively.
        
        Removes legacy summary fields from steps but preserves loop summary fields.
        """
        # Remove legacy fields from step level ONLY (not from loop objects)
        # These fields are not in the Step model but may be in legacy WSJF
        legacy_step_fields = ['num', 'passed', 'failed', 'startingIndex', 'endingIndex']
        for field in legacy_step_fields:
            step.pop(field, None)
        
        # Apply step defaults
        if 'name' not in step or not step['name']:
            step['name'] = "Step"
        if 'stepType' not in step or not step['stepType']:
            step['stepType'] = "SequenceCall"
        if 'status' not in step or not step['status']:
            step['status'] = "Passed"
        if 'group' not in step or not step['group']:
            step['group'] = "M"
        
        # Preserve loop object if it exists - DO NOT remove loop summary fields!
        # WSJF legacy files have 'loop' (lowercase) with either:
        #   - Summary fields (num, passed, failed, endingIndex) for Summary Steps
        #   - Index fields (idx) for Index Steps
        # DON'T add defaults - let WATS server validate what's actually there
        if 'loop' in step and isinstance(step['loop'], dict):
            loop = step['loop']
            # Only set defaults for fields that are missing AND that might be expected
            # Don't force defaults that create "Cannot have X in Index Step" errors
            pass  # Keep loop as-is from source file
        
        # Fix numeric measurements - ensure unit field exists
        if 'numericMeas' in step and isinstance(step['numericMeas'], list):
            for meas in step['numericMeas']:
                if isinstance(meas, dict):
                    if 'unit' not in meas or not meas['unit']:
                        meas['unit'] = ""
        
        # Fix chart objects - ensure required string fields are non-empty
        if 'chart' in step and isinstance(step['chart'], dict):
            chart = step['chart']
            if 'yLabel' not in chart or not chart['yLabel']:
                chart['yLabel'] = "-"
            if 'xLabel' not in chart or not chart['xLabel']:
                chart['xLabel'] = "-"
            if 'name' not in chart or not chart['name']:
                chart['name'] = "-"
        
        # Recursively clean child steps
        if 'steps' in step and isinstance(step['steps'], list):
            for child_step in step['steps']:
                if isinstance(child_step, dict):
                    self._sanitize_step(child_step)
    
    def _sanitize_unit(self, unit: Dict[str, Any]) -> None:
        """Sanitize unit/uut info object."""
        # Unit fields typically don't need sanitization but we can add defaults if needed
        pass


# Test code
if __name__ == "__main__":
    sample = {
        "type": "T",
        "pn": "TestPart-001",
        "sn": "SN12345",
        "rev": "A",
        "processCode": 10,
        "processName": "Functional Test",
        "result": "P",
        "machineName": "Station1",
        "start": "2024-01-15T10:00:00",
        "root": {
            "stepType": "SequenceCall",
            "name": "MainSequence",
            "status": "P",
            "totTime": 10.5,
            "steps": [
                {
                    "stepType": "ET_NLT",
                    "name": "VoltageTest",
                    "status": "P",
                    "totTime": 1.2,
                    "numericMeas": [
                        {
                            "compOp": "GELE",
                            "status": "P",
                            "unit": "V",
                            "value": 12.05,
                            "lowLimit": 11.5,
                            "highLimit": 12.5
                        }
                    ]
                },
                {
                    "stepType": "ET_PFT",
                    "name": "SelfTest",
                    "status": "P",
                    "totTime": 0.5,
                    "passFail": [
                        {"status": "P"}
                    ]
                }
            ]
        }
    }
    
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample, f)
        temp_path = Path(f.name)
    
    try:
        converter = WATSStandardJsonConverter()
        source = ConverterSource.from_file(temp_path)
        context = ConverterContext()
        
        # Validate
        validation = converter.validate(source, context)
        print(f"Validation: can_convert={validation.can_convert}, confidence={validation.confidence:.2f}")
        print(f"  Message: {validation.message}")
        print(f"  Detected: SN={validation.detected_serial_number}, PN={validation.detected_part_number}")
        
        # Convert
        result = converter.convert(source, context)
        print(f"\nConversion status: {result.status.value}")
        if result.report:
            print("\nGenerated report:")
            print(json.dumps(result.report, indent=2))
    finally:
        temp_path.unlink()
