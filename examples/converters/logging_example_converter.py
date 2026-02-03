"""
Example Converter with ConversionLog

Demonstrates best practices for using ConversionLog in converters:
- Step-by-step logging
- Warning and error capture
- Metadata tracking
- Proper finalization

This example shows how to track the conversion process in detail
for debugging and audit purposes.
"""

from pathlib import Path
from typing import List

from pywats_client.converters.base import (
    ConverterBase,
    ConverterArguments,
    ConverterResult,
    PostProcessAction,
)


class LoggingExampleConverter(ConverterBase):
    """
    Example converter demonstrating ConversionLog usage.
    
    This converter shows best practices for:
    - Using ConversionLog to track conversion steps
    - Logging warnings for non-critical issues
    - Logging errors with full context
    - Adding metadata for debugging
    
    The ConversionLog creates a detailed JSON line format log file
    for each conversion, making it easy to:
    - Debug conversion issues
    - Track conversion performance
    - Audit conversion history
    - Identify patterns in failures
    """
    
    def __init__(self, default_part_number: str = "UNKNOWN"):
        """
        Initialize converter.
        
        Args:
            default_part_number: Default part number if not found in file
        """
        super().__init__(priority=5)
        self.default_part_number = default_part_number
    
    @property
    def name(self) -> str:
        return "Logging Example Converter"
    
    @property
    def description(self) -> str:
        return "Demonstrates ConversionLog usage in converters"
    
    @property
    def supported_extensions(self) -> List[str]:
        return [".csv", ".txt"]
    
    def convert_file(
        self,
        file_path: Path,
        args: ConverterArguments
    ) -> ConverterResult:
        """
        Convert file with detailed logging.
        
        This example shows the recommended pattern:
        1. Check if ConversionLog is available
        2. Log each major step
        3. Log warnings for non-critical issues
        4. Log errors with full context
        5. Let the caller finalize the log
        """
        # Get ConversionLog if provided
        log = args.conversion_log
        
        try:
            # Step 1: Read file
            if log:
                log.step("Reading file", metadata={"path": str(file_path)})
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            file_size = len(content)
            if log:
                log.step("File read complete", metadata={"size_bytes": file_size})
            
            # Step 2: Parse content
            if log:
                log.step("Parsing content")
            
            lines = content.strip().split('\n')
            
            if len(lines) < 2:
                error_msg = "File has insufficient data (needs at least 2 lines)"
                if log:
                    log.error(error_msg, step="Parsing", metadata={"lines": len(lines)})
                return ConverterResult.failed_result(error=error_msg)
            
            if log:
                log.step("Parsing complete", metadata={"lines": len(lines)})
            
            # Step 3: Extract data
            if log:
                log.step("Extracting data")
            
            # Assume first line is header, second line is data
            header = lines[0].split(',')
            data = lines[1].split(',')
            
            # Check for required fields
            required_fields = ['serial', 'result']
            missing_fields = [f for f in required_fields if f not in [h.lower() for h in header]]
            
            if missing_fields:
                error_msg = f"Missing required fields: {', '.join(missing_fields)}"
                if log:
                    log.error(
                        error_msg,
                        step="Validation",
                        metadata={"header": header, "missing": missing_fields}
                    )
                return ConverterResult.failed_result(error=error_msg)
            
            # Extract values
            serial_idx = next(i for i, h in enumerate(header) if h.lower() == 'serial')
            result_idx = next(i for i, h in enumerate(header) if h.lower() == 'result')
            
            serial_number = data[serial_idx].strip()
            test_result = data[result_idx].strip()
            
            # Get part number (optional)
            part_number = self.default_part_number
            try:
                part_idx = next(i for i, h in enumerate(header) if h.lower() == 'part')
                part_number = data[part_idx].strip()
            except StopIteration:
                # Part number not in file - use default
                if log:
                    log.warning(
                        f"Part number not found in file, using default: {self.default_part_number}",
                        metadata={"default_part": self.default_part_number}
                    )
            
            if log:
                log.step(
                    "Data extraction complete",
                    metadata={
                        "serial": serial_number,
                        "part": part_number,
                        "result": test_result
                    }
                )
            
            # Step 4: Validate data
            if log:
                log.step("Validating data")
            
            if not serial_number:
                error_msg = "Serial number is empty"
                if log:
                    log.error(error_msg, step="Validation")
                return ConverterResult.failed_result(error=error_msg)
            
            # Normalize result
            result_normalized = test_result.upper()
            if result_normalized not in ['PASSED', 'FAILED']:
                if log:
                    log.warning(
                        f"Unusual result value: {test_result}",
                        metadata={"original_value": test_result}
                    )
                # Try to map common variants
                if result_normalized in ['PASS', 'OK', 'GOOD']:
                    result_normalized = 'PASSED'
                    if log:
                        log.step("Normalized result", metadata={"from": test_result, "to": "PASSED"})
                elif result_normalized in ['FAIL', 'BAD', 'ERROR']:
                    result_normalized = 'FAILED'
                    if log:
                        log.step("Normalized result", metadata={"from": test_result, "to": "FAILED"})
                else:
                    # Unknown result - default to FAILED for safety
                    if log:
                        log.warning(
                            f"Unknown result value '{test_result}', defaulting to FAILED",
                            metadata={"original": test_result}
                        )
                    result_normalized = 'FAILED'
            
            if log:
                log.step("Validation complete", metadata={"result": result_normalized})
            
            # Step 5: Create WATS report
            if log:
                log.step("Creating WATS report")
            
            report = {
                "type": "UUT",
                "serialNumber": serial_number,
                "partNumber": part_number,
                "result": result_normalized,
                "steps": [
                    {
                        "name": "TestSequence",
                        "result": result_normalized,
                        "measurements": []
                    }
                ]
            }
            
            if log:
                log.step(
                    "Report created",
                    metadata={
                        "report_type": "UUT",
                        "serial": serial_number,
                        "result": result_normalized
                    }
                )
            
            # Note: The caller (ConverterPool or similar) will finalize the log
            # with success=True and the report_id after upload
            
            return ConverterResult.success_result(
                report=report,
                post_action=PostProcessAction.ZIP,
                metadata={"lines_processed": len(lines)}
            )
        
        except Exception as e:
            # Log the exception with full context
            if log:
                log.error(
                    f"Unexpected error during conversion: {str(e)}",
                    step="Conversion",
                    exception=e
                )
            
            # Return failure (caller will finalize log)
            return ConverterResult.failed_result(
                error=f"Conversion error: {type(e).__name__}: {str(e)}"
            )


# Example usage (for testing)
if __name__ == "__main__":
    import tempfile
    from pywats_client.converters.conversion_log import ConversionLog
    from pywats_client.converters.models import ConversionStatus
    
    # Create test CSV file
    test_content = """serial,part,result
SN12345,PN-ABC-001,PASSED
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(test_content)
        test_file = Path(f.name)
    
    try:
        # Create ConversionLog for this conversion
        with ConversionLog.create_for_file(test_file.name, "example") as log:
            # Create converter
            converter = LoggingExampleConverter(default_part_number="DEFAULT-PART")
            
            # Create mock arguments
            from unittest.mock import Mock
            args = ConverterArguments(
                api_client=Mock(),
                file_info=Mock(name=test_file.name, extension=".csv", size=len(test_content)),
                drop_folder=test_file.parent,
                done_folder=test_file.parent / "done",
                error_folder=test_file.parent / "error",
                user_settings={},
                conversion_log=log  # Pass ConversionLog to converter
            )
            
            # Run conversion
            result = converter.convert_file(test_file, args)
            
            # Finalize log based on result
            if result.status == ConversionStatus.SUCCESS:
                log.finalize(success=True, report_id=999, metadata={"test": True})
                print(f"✅ Conversion successful!")
                print(f"   Report: {result.report}")
                print(f"   Log file: {log.log_file_path}")
            else:
                log.finalize(success=False, error=result.error)
                print(f"❌ Conversion failed: {result.error}")
                print(f"   Log file: {log.log_file_path}")
        
        # Show log content
        print(f"\n📋 Conversion Log Content:")
        print("=" * 60)
        if log.log_file_path.exists():
            print(log.log_file_path.read_text())
        
    finally:
        # Cleanup
        test_file.unlink(missing_ok=True)
