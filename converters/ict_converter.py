"""
ICT Converter V2 (Jungheinrich Format) - Using UUTReport Model

Converts ICT test result files to WATS reports using the pyWATS UUTReport API.

This is the refactored version that uses proper API calls instead of dictionaries.

Port of the C# ICTConverter (TextConverterBase).

This converter handles semicolon-delimited ICT test files with:
- Header with dashes separating sections
- Serial number and timestamp from filename
- Test results with pass/fail or numeric limits

Filename format: SerialNo_YYYY_MM_DD_HH_MM_SS.txt
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# pyWATS Report Model API Imports
# ═══════════════════════════════════════════════════════════════════════════════
from pywats.domains.report.report_models import UUTReport
from pywats.domains.report.report_models.uut.uut_info import UUTInfo
from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp

# ═══════════════════════════════════════════════════════════════════════════════
# Converter Infrastructure Imports
# ═══════════════════════════════════════════════════════════════════════════════
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


class ICTConverter(FileConverter):
    """
    Converts ICT test result files to WATS reports using UUTReport model.
    
    This converter demonstrates the proper API-based pattern for:
    1. Creating UUTReport with header info parsed from filename
    2. Creating component group sequences
    3. Adding numeric steps with limits
    4. Adding pass/fail boolean steps
    
    File qualification:
    - Text file with semicolon-delimited test data
    - Filename contains serial number and timestamp
    - Content has dashed separator lines
    
    Test line formats:
    - Pass/Fail: ComponentRef;;;Result
    - Numeric: ComponentRef;LowLimit;HighLimit;Measured
    """
    
    # Component type mapping (prefix -> category name)
    COMPONENT_TYPES = {
        "R": "Resistors",
        "C": "Capacitors",
        "L": "Inductors",
        "D": "Diodes",
        "Q": "Transistors",
        "CON": "Connectors",
        "RSHORT": "Rshort",
        "TC": "Thermocouple",
        "PTC": "PTC",
        "DZ": "ZenerDiodes",
        "F": "Fuses",
        "J": "Jumpers",
        "T": "Transformers",
        "ISO": "Isolators",
        "Y": "Crystals",
        "NetC": "NetC",
        "N": "N-Component",
        "V": "Vacuum tubes",
        "K": "Relays",
        "U": "ICs",
    }
    
    # SI prefix multipliers
    PREFIX_UNITS = {
        "a": 1e-18,  # Atto
        "f": 1e-15,  # Femto
        "p": 1e-12,  # Pico
        "n": 1e-9,   # Nano
        "u": 1e-6,   # Micro
        "m": 1e-3,   # Milli
        "": 1.0,     # No prefix
        "k": 1e3,    # Kilo
        "M": 1e6,    # Mega
        "G": 1e9,    # Giga
        "T": 1e12,   # Tera
    }
    
    @property
    def name(self) -> str:
        return "ICT Converter (Jungheinrich)"
    
    @property
    def version(self) -> str:
        return "2.0.0"
    
    @property
    def description(self) -> str:
        return "Converts Jungheinrich ICT test result files to WATS reports using UUTReport model"
    
    @property
    def file_patterns(self) -> List[str]:
        return ["*.txt", "*.log"]
    
    @property
    def arguments_schema(self) -> Dict[str, ArgumentDefinition]:
        return {
            "operationTypeCode": ArgumentDefinition(
                arg_type=ArgumentType.INTEGER,
                default=20,
                description="Operation type code for ICT tests",
            ),
            "partRevision": ArgumentDefinition(
                arg_type=ArgumentType.STRING,
                default="1.0",
                description="Part revision number",
            ),
            "stationName": ArgumentDefinition(
                arg_type=ArgumentType.STRING,
                default="ICT Station",
                description="Station name",
            ),
            "location": ArgumentDefinition(
                arg_type=ArgumentType.STRING,
                default="Production",
                description="Station location",
            ),
            "purpose": ArgumentDefinition(
                arg_type=ArgumentType.STRING,
                default="ICT",
                description="Test purpose",
            ),
        }
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        """
        Validate that the file is an ICT test file.
        
        Checks:
        - Filename matches SerialNo_YYYY_MM_DD_HH_MM_SS pattern
        - Content has dash separator lines
        - Content has semicolon-delimited test data
        """
        if not source.path or not source.path.exists():
            return ValidationResult.no_match("File not found")
        
        # Skip files starting with "no serialnumber"
        if source.path.name.lower().startswith("no serialnumber"):
            return ValidationResult.no_match("File indicates no serial number")
        
        # Check filename pattern for serial number and timestamp
        filename_pattern = r'^(?P<SerialNo>[^_]+)_(?P<Year>\d{4})_(?P<Month>\d{2})_(?P<Day>\d{2})_(?P<Hour>\d{2})_(?P<Minute>\d{2})_(?P<Second>\d{2})'
        filename_match = re.match(filename_pattern, source.path.name)
        
        if not filename_match:
            return ValidationResult.pattern_match(
                message="Filename doesn't match expected ICT pattern"
            )
        
        try:
            with open(source.path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read(4096)  # Read first 4KB for validation
            
            lines = content.split('\n')
            
            # Count dash lines and semicolon lines
            dash_count = sum(1 for line in lines if line.strip().startswith('----'))
            semicolon_count = sum(1 for line in lines if ';' in line)
            
            if dash_count < 2:
                return ValidationResult.pattern_match(
                    message="File doesn't have expected ICT header structure"
                )
            
            if semicolon_count < 3:
                return ValidationResult.pattern_match(
                    message="File doesn't have enough semicolon-delimited test data"
                )
            
            # Extract serial number from filename
            serial_number = filename_match.group('SerialNo')
            
            # Try to find part number (line after 2nd dash line)
            part_number = ""
            dash_seen = 0
            for line in lines:
                if line.strip().startswith('----'):
                    dash_seen += 1
                elif dash_seen == 2 and line.strip():
                    part_number = line.strip()
                    break
            
            # Check for Board PASS indicator
            has_pass = any('Board PASS' in line for line in lines)
            
            confidence = 0.7
            if dash_count >= 3:
                confidence += 0.1
            if semicolon_count >= 10:
                confidence += 0.1
            if part_number:
                confidence += 0.05
            
            return ValidationResult(
                can_convert=True,
                confidence=min(0.95, confidence),
                message=f"Valid ICT file ({semicolon_count} test lines)",
                detected_serial_number=serial_number,
                detected_part_number=part_number,
                detected_result="Passed" if has_pass else "Failed",
            )
            
        except Exception as e:
            return ValidationResult.no_match(f"Error reading file: {e}")
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        """
        Convert ICT test file to WATS UUTReport.
        
        Uses the pyWATS UUTReport model API to build the report properly.
        """
        if not source.path:
            return ConverterResult.failed_result(error="No file path provided")
        
        try:
            # Parse filename for serial number and timestamp
            filename_pattern = r'^(?P<SerialNo>[^_]+)_(?P<Year>\d{4})_(?P<Month>\d{2})_(?P<Day>\d{2})_(?P<Hour>\d{2})_(?P<Minute>\d{2})_(?P<Second>\d{2})'
            filename_match = re.match(filename_pattern, source.path.name)
            
            if not filename_match:
                return ConverterResult.failed_result(
                    error="Filename doesn't match expected pattern"
                )
            
            serial_number = filename_match.group('SerialNo')
            start_time = datetime(
                int(filename_match.group('Year')),
                int(filename_match.group('Month')),
                int(filename_match.group('Day')),
                int(filename_match.group('Hour')),
                int(filename_match.group('Minute')),
                int(filename_match.group('Second'))
            ).astimezone()
            
            # Read file content
            with open(source.path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            
            # Parse content
            part_number = ""
            dash_count = 0
            uut_passed = False
            parsed_tests: List[Dict[str, Any]] = []
            
            # Regex patterns
            prefixed_passfail = re.compile(
                r'^(?P<Prefix>NetC|F|Y|R|C|L|D|Q|J|T|Y|N|V|K|U)(?P<Suffix>\d+\S*)\s*;;;(?P<Result>.*)'
            )
            non_prefixed_passfail = re.compile(
                r'^(?P<StepName>[^;]+);;;(?P<Result>.*)'
            )
            prefixed_numtest = re.compile(
                r'^(?P<Prefix>NetC|F|Y|R|C|L|D|Q|J|T|Y|N|V|K|U)(?P<Suffix>\d+\S*)\s*;(?P<Low>[-0-9.]+)(?P<LowU>\S*)\s*;(?P<Hi>[-0-9.]+)(?P<HiU>\S*)\s*;(?P<Meas>[-0-9.]+)(?P<MeasU>\S*)'
            )
            non_prefixed_numtest = re.compile(
                r'^(?P<StepName>[^;]+)\s*;(?P<Low>[-0-9.]+)(?P<LowU>\S*)\s*;(?P<Hi>[-0-9.]+)(?P<HiU>\S*)\s*;(?P<Meas>[-0-9.]+)(?P<MeasU>\S*)'
            )
            
            in_test = False
            
            for line in lines:
                line = line.strip()
                
                # Header parsing
                if line.startswith('----'):
                    dash_count += 1
                    if dash_count == 3:
                        in_test = True
                    continue
                
                if dash_count == 2 and line:
                    part_number = line
                    continue
                
                if 'Board PASS' in line:
                    uut_passed = True
                    continue
                
                if not in_test:
                    continue
                
                # Test parsing
                test = self._parse_test_line(
                    line, 
                    prefixed_passfail, 
                    non_prefixed_passfail,
                    prefixed_numtest, 
                    non_prefixed_numtest
                )
                
                if test:
                    parsed_tests.append(test)
            
            # Get arguments
            operation_code = context.get_argument("operationTypeCode", 20)
            part_revision = context.get_argument("partRevision", "1.0")
            station_name = context.get_argument("stationName", "ICT Station")
            location = context.get_argument("location", "Production")
            purpose = context.get_argument("purpose", "ICT")
            
            # ═══════════════════════════════════════════════════════════════════
            # Create UUTReport using the API
            # ═══════════════════════════════════════════════════════════════════
            report = UUTReport(
                pn=part_number or "UNKNOWN",
                sn=serial_number,
                rev=part_revision,
                process_code=int(operation_code),
                station_name=station_name,
                location=location,
                purpose=purpose,
                result="P" if uut_passed else "F",
                start=start_time,
            )
            
            # Add misc info
            report.add_misc_info(description="Source File", value=source.path.name)
            report.add_misc_info(description="Converter", value=f"{self.name} v{self.version}")
            
            # ═══════════════════════════════════════════════════════════════════
            # Get root sequence and set properties
            # ═══════════════════════════════════════════════════════════════════
            root = report.get_root_sequence_call()
            root.name = "ICT"
            root.sequence.version = self.version
            root.sequence.file_name = source.path.name
            
            # ═══════════════════════════════════════════════════════════════════
            # Build test hierarchy from parsed tests
            # ═══════════════════════════════════════════════════════════════════
            self._build_test_hierarchy(parsed_tests, root)
            
            return ConverterResult.success_result(
                report=report,  # UUTReport instance, NOT dict!
                post_action=PostProcessAction.MOVE,
            )
            
        except Exception as e:
            return ConverterResult.failed_result(error=f"Conversion error: {e}")
    
    def _parse_test_line(
        self,
        line: str,
        prefixed_passfail: re.Pattern,
        non_prefixed_passfail: re.Pattern,
        prefixed_numtest: re.Pattern,
        non_prefixed_numtest: re.Pattern,
    ) -> Optional[Dict[str, Any]]:
        """Parse a single test line into a test dictionary"""
        
        # Try prefixed pass/fail
        match = prefixed_passfail.match(line)
        if match:
            return {
                "type": "passfail",
                "prefix": match.group("Prefix"),
                "name": match.group("Prefix") + match.group("Suffix"),
                "result": match.group("Result"),
                "passed": match.group("Result") == "IN",
            }
        
        # Try non-prefixed pass/fail
        match = non_prefixed_passfail.match(line)
        if match:
            return {
                "type": "passfail",
                "prefix": "",
                "name": match.group("StepName"),
                "result": match.group("Result"),
                "passed": match.group("Result") == "IN",
            }
        
        # Try prefixed numeric
        match = prefixed_numtest.match(line)
        if match:
            return self._build_numeric_test(
                prefix=match.group("Prefix"),
                name=match.group("Prefix") + match.group("Suffix"),
                low=match.group("Low"),
                low_unit=match.group("LowU"),
                high=match.group("Hi"),
                high_unit=match.group("HiU"),
                meas=match.group("Meas"),
                meas_unit=match.group("MeasU"),
            )
        
        # Try non-prefixed numeric
        match = non_prefixed_numtest.match(line)
        if match:
            return self._build_numeric_test(
                prefix="",
                name=match.group("StepName"),
                low=match.group("Low"),
                low_unit=match.group("LowU"),
                high=match.group("Hi"),
                high_unit=match.group("HiU"),
                meas=match.group("Meas"),
                meas_unit=match.group("MeasU"),
            )
        
        return None
    
    def _build_numeric_test(
        self,
        prefix: str,
        name: str,
        low: str,
        low_unit: str,
        high: str,
        high_unit: str,
        meas: str,
        meas_unit: str,
    ) -> Dict[str, Any]:
        """Build a numeric test dictionary"""
        try:
            meas_val = float(meas)
            low_val = float(low) if low else 0.0
            high_val = float(high) if high else 0.0
            
            # Convert units to measurement unit
            low_factor = self.PREFIX_UNITS.get(low_unit, 1.0)
            high_factor = self.PREFIX_UNITS.get(high_unit, 1.0)
            meas_factor = self.PREFIX_UNITS.get(meas_unit, 1.0)
            
            if meas_factor != 0:
                low_converted = low_val * low_factor / meas_factor
                high_converted = high_val * high_factor / meas_factor
            else:
                low_converted = low_val
                high_converted = high_val
            
            # Determine pass/fail
            passed = True
            if low_converted > 0 and high_converted == 0:
                passed = meas_val >= low_converted
            elif low_converted > 0 and high_converted > 0:
                passed = low_converted <= meas_val <= high_converted
            
            return {
                "type": "numeric",
                "prefix": prefix,
                "name": name,
                "value": meas_val,
                "unit": meas_unit,
                "low_limit": low_converted if low_val else None,
                "high_limit": high_converted if high_val else None,
                "passed": passed,
            }
        except (ValueError, ZeroDivisionError):
            return {
                "type": "numeric",
                "prefix": prefix,
                "name": name,
                "value": 0.0,
                "unit": meas_unit,
                "passed": False,
            }
    
    def _build_test_hierarchy(
        self,
        parsed_tests: List[Dict[str, Any]],
        root: SequenceCall
    ) -> None:
        """
        Build step hierarchy grouped by component type.
        
        Uses pyWATS API to create sequences and steps.
        """
        # Group tests by component type
        groups: Dict[str, List[Dict[str, Any]]] = {}
        ungrouped_count = 0
        
        for test in parsed_tests:
            prefix = test.get("prefix", "")
            
            if prefix:
                group_name = self.COMPONENT_TYPES.get(prefix, prefix)
            else:
                group_name = f"Ungrouped_{ungrouped_count}"
                ungrouped_count += 1
            
            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append(test)
        
        # Create sequences for each group
        for group_name, tests in groups.items():
            if not tests:
                continue
            
            # Create sequence for this component group
            group_seq = root.add_sequence_call(
                name=group_name,
                file_name=f"{group_name.lower()}.seq",
                version="1.0"
            )
            
            # Add tests to the sequence
            for test in tests:
                self._add_test_step(group_seq, test)
    
    def _add_test_step(self, sequence: SequenceCall, test: Dict[str, Any]) -> None:
        """
        Add a test as a step using the pyWATS API.
        
        Converts parsed test dict to proper API call:
        - "passfail" -> add_boolean_step()
        - "numeric" -> add_numeric_step()
        """
        test_type = test.get("type", "")
        name = test.get("name", "Unknown")
        passed = test.get("passed", True)
        
        if test_type == "passfail":
            # Use boolean step for pass/fail tests
            sequence.add_boolean_step(
                name=name,
                value=passed,
                status="P" if passed else "F",
                report_text=test.get("result", ""),
            )
        
        elif test_type == "numeric":
            # Use numeric step with limits
            value = test.get("value", 0.0)
            unit = test.get("unit", "")
            low_limit = test.get("low_limit")
            high_limit = test.get("high_limit")
            
            # Determine comparison operator
            if low_limit is not None and high_limit is not None:
                comp_op = CompOp.GELE  # Low <= Value <= High
                sequence.add_numeric_step(
                    name=name,
                    value=value,
                    unit=unit,
                    low_limit=low_limit,
                    high_limit=high_limit,
                    comp_op=comp_op,
                    status="P" if passed else "F",
                )
            elif low_limit is not None:
                comp_op = CompOp.GE  # Value >= Low
                sequence.add_numeric_step(
                    name=name,
                    value=value,
                    unit=unit,
                    low_limit=low_limit,
                    comp_op=comp_op,
                    status="P" if passed else "F",
                )
            elif high_limit is not None:
                comp_op = CompOp.LE  # Value <= High
                sequence.add_numeric_step(
                    name=name,
                    value=value,
                    unit=unit,
                    high_limit=high_limit,
                    comp_op=comp_op,
                    status="P" if passed else "F",
                )
            else:
                # No limits - use LOG mode
                sequence.add_numeric_step(
                    name=name,
                    value=value,
                    unit=unit,
                    comp_op=CompOp.LOG,
                    status="P" if passed else "F",
                )


# ═══════════════════════════════════════════════════════════════════════════════
# Test/Demo Code
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import tempfile
    import os
    
    # Create sample ICT file content
    sample_content = """Pruefversion 1.0
----
Test Header Info
----
PN-ICT-12345
----
R100;100k;120k;110k
R101;1M;1.2M;1.1M
R102;;;IN
C200;10n;12n;11n
C201;;;OUT
NetC1;;;IN
Board PASS
"""
    
    # Create temp file with ICT naming convention
    temp_dir = tempfile.mkdtemp()
    filename = "SN00001_2024_01_15_10_30_45.txt"
    temp_path = Path(temp_dir) / filename
    
    with open(temp_path, 'w') as f:
        f.write(sample_content)
    
    try:
        converter = ICTConverter()
        source = ConverterSource.from_file(temp_path)
        context = ConverterContext()
        
        # Validate
        validation = converter.validate(source, context)
        print(f"Validation: can_convert={validation.can_convert}, confidence={validation.confidence:.2f}")
        print(f"  Detected: SN={validation.detected_serial_number}, PN={validation.detected_part_number}")
        
        # Convert
        result = converter.convert(source, context)
        print(f"\nConversion status: {result.status.value}")
        
        if result.report:
            report = result.report
            print(f"\n=== Generated UUTReport ===")
            print(f"Part Number: {report.pn}")
            print(f"Serial Number: {report.sn}")
            print(f"Result: {'PASSED' if report.result == 'P' else 'FAILED'}")
            print(f"Station: {report.station_name}")
            
            # Show hierarchy
            print(f"\n=== Test Hierarchy ===")
            root = report.get_root_sequence_call()
            print(f"Root: {root.name}")
            
            def print_steps(step, indent=1):
                prefix = "  " * indent + "└─"
                step_type = step.step_type if hasattr(step, 'step_type') else 'SEQ'
                print(f"{prefix} {step_type}: {step.name} [{step.status}]")
                if hasattr(step, 'steps'):
                    for child in step.steps:
                        print_steps(child, indent + 1)
            
            for step in root.steps:
                print_steps(step)
            
            # Show JSON (truncated)
            print(f"\n=== JSON Output (truncated) ===")
            json_output = report.model_dump_json(by_alias=True, indent=2, exclude_none=True)
            print(json_output[:1500] + "..." if len(json_output) > 1500 else json_output)
    finally:
        temp_path.unlink()
        os.rmdir(temp_dir)
