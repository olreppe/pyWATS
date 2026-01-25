# Converter Architecture Guide

## Overview

The PyWATS Client converter architecture provides a flexible framework for converting various file formats into WATS report structures. Converters run on the client (and potentially on the server in the future) and integrate with the file monitoring system.

## � Standard Converters (Pre-installed)

These converters are bundled with pyWATS Client and ready to use out of the box:

| Converter | Format | File Patterns | Description |
|-----------|--------|---------------|-------------|
| `WATSStandardXMLConverter` | WSXF/WRML | `*.xml` | WATS Standard XML Format - the native WATS format |
| `WATSStandardJsonConverter` | WSJF | `*.json` | WATS Standard JSON Format - JSON equivalent of WSXF |
| `WATSStandardTextConverter` | WSTF | `*.txt` | WATS Standard Text Format - tab-delimited text |
| `TeradyneICTConverter` | Teradyne i3070 | `*.txt`, `*.log` | Teradyne i3070 In-Circuit Test format |
| `TeradyneSpectrumICTConverter` | Teradyne Spectrum | `*.txt`, `*.log` | Teradyne Spectrum ICT format |
| `SeicaXMLConverter` | Seica XML | `*.xml` | Seica Flying Probe XML format |

**Location:** `pywats_client.converters.standard`

```python
from pywats_client.converters import (
    WATSStandardXMLConverter,
    WATSStandardJsonConverter,
    WATSStandardTextConverter,
    TeradyneICTConverter,
    TeradyneSpectrumICTConverter,
    SeicaXMLConverter,
)
```

## �📚 Reference Implementations (V2 Converters)

All new converters should follow the patterns demonstrated in these V2 reference implementations:

| File | Description | Key Features |
|------|-------------|--------------|
| [converter_template.py](../converters/converter_template.py) | **Comprehensive Template** | Complete reference with all step types, mock file format, extensive documentation |
| [spea_converter_v2.py](../converters/spea_converter_v2.py) | SPEA ICT Converter | Component grouping, numeric steps with limits |
| [xj_log_converter_v2.py](../converters/xj_log_converter_v2.py) | XJTAG Log Converter | ZIP file processing, boolean steps |
| [xml_format_converter_v2.py](../converters/xml_format_converter_v2.py) | DBAudio XML Converter | Chart steps with series, multi-numeric statistics |
| [ict_converter_v2.py](../converters/ict_converter_v2.py) | Jungheinrich ICT Converter | Text parsing, SI unit conversion |
| [example_file_converter_v2.py](../converters/example_file_converter_v2.py) | CSV Test Converter | Simple CSV parsing, conditional limits |

**Start with `converter_template.py`** - it contains the complete API reference with all step types and detailed comments.

## ⚠️ CRITICAL: Use the PyWATS API Models - No Workarounds!

**All converters MUST use the PyWATS UUTReport model to build reports.** 

Do NOT build raw dictionaries directly. The API provides a complete model with factory methods for creating properly structured reports. If a feature you need is missing from the API, that is an API problem that must be fixed - no workarounds are acceptable.

### The Proper Pattern

```python
from pywats.domains.report.report_models import UUTReport
from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp
from pywats.domains.report.report_models.uut.uut_status import UUTStatus
from pywats.domains.report.report_models.uut.step_status import StepStatus

# 1. Create report with header information
report = UUTReport(
    pn="PN12345",
    sn="SN001", 
    rev="1.0",
    process_code=10,
    station_name="TestStation",
    result=UUTStatus.PASSED,
    start=datetime.now()
)

# 2. Get root sequence call
root = report.get_root_sequence_call()
root.name = "Main Test Sequence"

# 3. Add sub-sequences for test groups
group = root.add_sequence_call(
    name="Voltage Tests",
    file_name="voltage.seq",
    version="1.0"
)

# 4. Add test steps using factory methods
group.add_numeric_step(
    name="VCC Voltage",
    value=5.02,
    unit="V",
    comp_op=CompOp.GELE,  # Greater-or-equal, Less-or-equal
    low_limit=4.5,
    high_limit=5.5,
    status=StepStatus.PASSED
)

group.add_boolean_step(
    name="Power OK",
    status=StepStatus.PASSED
)

group.add_string_step(
    name="Firmware Version",
    value="v2.1.0",
    status=StepStatus.PASSED
)

# 5. Return ConverterResult with UUTReport (NOT a dictionary!)
return ConverterResult.success_result(
    report=report,  # UUTReport instance
    post_action=PostProcessAction.MOVE
)
```

### Why This Matters

1. **Type Safety**: The model provides proper validation and type checking
2. **Consistency**: All reports follow the same structure
3. **Maintainability**: Changes to the report format are handled centrally
4. **API Evolution**: The model can evolve without breaking converters
5. **No Hacks**: If the API can't do something, we fix the API

### Available Factory Methods

| Method | Description | Parameters |
|--------|-------------|------------|
| `report.get_root_sequence_call()` | Get root SequenceCall | - |
| `seq.add_sequence_call()` | Add nested sequence | name, file_name, version |
| `seq.add_numeric_step()` | Single numeric measurement | name, value, unit, comp_op, low_limit, high_limit, status |
| `seq.add_boolean_step()` | Pass/fail boolean | name, status |
| `seq.add_string_step()` | String value | name, value, status, report_text |
| `seq.add_multi_numeric_step()` | Multiple measurements | name, status, then call add_measurement() |
| `seq.add_chart_step()` | Chart/waveform data | name, status, then add series |

### CompOp (Comparison Operators)

```python
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp

CompOp.LOG   # No limits (log only)
CompOp.EQ    # Equal
CompOp.NE    # Not Equal
CompOp.LT    # Less Than
CompOp.LE    # Less or Equal
CompOp.GT    # Greater Than
CompOp.GE    # Greater or Equal
CompOp.GELE  # Between (>=low, <=high)
CompOp.GTLT  # Between exclusive (>low, <high)
CompOp.GELT  # >=low, <high
CompOp.GTLE  # >low, <=high
```

## Architecture Components

### 1. ConverterBase (Base Class)

All converters must inherit from `ConverterBase` and implement the required methods.

**Location**: `src/pywats_client/converters/base.py`

**Key Features**:
- File validation before conversion
- Configurable arguments/parameters
- Post-processing actions (Move, Zip, Delete, Keep)
- Conversion status (Success, Failed, Suspended, Skipped)
- Custom success/failure handlers
- Access to file info, API client, and folders

### 2. ConverterProcessor (Service)

Handles the complete file conversion workflow.

**Location**: `src/pywats_client/services/converter_processor.py`

**Key Features**:
- File qualification and validation
- Conversion execution with retry logic
- Post-processing based on PPA settings
- Suspended conversion management
- Error handling and logging
- Statistics and monitoring

### 3. FileMonitor (Integration)

Monitors drop folders and triggers conversions.

**Location**: `src/pywats_client/services/file_monitor.py`

## Workflow

```
┌─────────────────┐
│ Drop Folder     │
│ (Monitored)     │
└────────┬────────┘
         │ New File Detected
         ▼
┌─────────────────────────────┐
│ 1. File Validation          │
│   - Check extension         │
│   - Check MIME type         │
│   - Check file signature    │
│   - Check size limits       │
└────────┬────────────────────┘
         │ Valid?
         ▼
┌─────────────────────────────┐
│ 2. Convert File             │
│   - Read file               │
│   - Parse data              │
│   - Create report           │
│   - Return status           │
└────────┬────────────────────┘
         │
         ├──── SUCCESS ────────────┐
         │                          ▼
         │                    ┌──────────────────┐
         │                    │ 3. Post-Process  │
         │                    │   - Delete       │
         │                    │   - Move         │
         │                    │   - Zip          │
         │                    │   - Keep         │
         │                    └──────────────────┘
         │
         ├──── FAILED ──────────────┐
         │                           ▼
         │                     ┌──────────────┐
         │                     │ Error Folder │
         │                     └──────────────┘
         │
         ├──── SUSPENDED ───────────┐
         │                           ▼
         │                     ┌────────────────────┐
         │                     │ Suspended Folder   │
         │                     │ (Retry Later)      │
         │                     └────────────────────┘
         │
         └──── SKIPPED ─────────────┐
                                    ▼
                              (No Action)
```

## Creating a Custom Converter

### Basic Structure

**IMPORTANT**: Always use the UUTReport model - never build raw dictionaries!

```python
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# pyWATS model imports - REQUIRED
from pywats.domains.report.report_models import UUTReport
from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp
from pywats.domains.report.report_models.uut.uut_status import UUTStatus
from pywats.domains.report.report_models.uut.step_status import StepStatus
from pywats.domains.report.report_models.misc_info import MiscInfo

# Converter infrastructure
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


class MyConverter(FileConverter):
    """
    Custom converter for MyFormat files.
    
    Always uses the pyWATS UUTReport model for building reports.
    """
    
    @property
    def name(self) -> str:
        return "My Custom Converter"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Converts MyFormat files to UUT reports using pyWATS API"
    
    @property
    def file_patterns(self) -> List[str]:
        return ["*.myformat", "*.mf"]
    
    @property
    def arguments_schema(self) -> Dict[str, ArgumentDefinition]:
        return {
            "stationName": ArgumentDefinition(
                arg_type=ArgumentType.STRING,
                default="Station1",
                description="Test station name",
            ),
            "processCode": ArgumentDefinition(
                arg_type=ArgumentType.INTEGER,
                default=10,
                description="Process/operation code",
            ),
        }
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        """Validate file before conversion"""
        if not source.path or not source.path.exists():
            return ValidationResult.no_match("File not found")
        
        try:
            with open(source.path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # Read first 1KB
            
            # Check for file signature/pattern
            if "MYFORMAT_HEADER" in content:
                # Extract identifiers for validation result
                serial = self._extract_serial(content)
                part = self._extract_part(content)
                
                return ValidationResult(
                    can_convert=True,
                    confidence=0.95,
                    message="Valid MyFormat file",
                    detected_serial_number=serial,
                    detected_part_number=part,
                )
            
            return ValidationResult.no_match("Not a MyFormat file")
            
        except Exception as e:
            return ValidationResult.no_match(f"Error: {e}")
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        """
        Convert file to UUTReport.
        
        ALWAYS use the pyWATS model - never build raw dictionaries!
        """
        try:
            # Read file
            with open(source.path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse file data
            serial_number = self._extract_serial(content)
            part_number = self._extract_part(content)
            test_result = self._extract_result(content)
            tests = self._parse_tests(content)
            
            # Get arguments
            station = context.get_argument("stationName", "Station1")
            process_code = context.get_argument("processCode", 10)
            
            # ========================================
            # BUILD REPORT USING UUTReport MODEL
            # ========================================
            
            # 1. Create the report with header info
            report = UUTReport(
                pn=part_number,
                sn=serial_number,
                rev="1",
                process_code=process_code,
                station_name=station,
                result=UUTStatus.PASSED if test_result == "P" else UUTStatus.FAILED,
                start=datetime.now(),
            )
            
            # 2. Get root sequence
            root = report.get_root_sequence_call()
            root.name = "MyFormat Tests"
            
            # 3. Add test sequences and steps
            for group_name, group_tests in tests.items():
                # Create sequence for test group
                group_seq = root.add_sequence_call(
                    name=group_name,
                    file_name=f"{group_name}.seq",
                    version="1.0"
                )
                
                # Add individual tests
                for test in group_tests:
                    self._add_test_step(group_seq, test)
            
            # 4. Return success with UUTReport (NOT a dict!)
            return ConverterResult.success_result(
                report=report,
                post_action=PostProcessAction.MOVE,
            )
            
        except Exception as e:
            return ConverterResult.failed_result(error=f"Conversion error: {e}")
    
    def _add_test_step(self, sequence: SequenceCall, test: Dict[str, Any]) -> None:
        """Add a test step to the sequence using factory methods"""
        test_type = test.get("type", "numeric")
        name = test.get("name", "Unknown")
        status = StepStatus.PASSED if test.get("passed") else StepStatus.FAILED
        
        if test_type == "numeric":
            # Build kwargs conditionally (limits are optional)
            kwargs: Dict[str, Any] = {
                "name": name,
                "value": float(test.get("value", 0)),
                "unit": test.get("unit", ""),
                "comp_op": CompOp.GELE if test.get("low") else CompOp.LOG,
                "status": status,
            }
            if test.get("low") is not None:
                kwargs["low_limit"] = float(test["low"])
            if test.get("high") is not None:
                kwargs["high_limit"] = float(test["high"])
            
            sequence.add_numeric_step(**kwargs)
            
        elif test_type == "boolean":
            sequence.add_boolean_step(name=name, status=status)
            
        elif test_type == "string":
            sequence.add_string_step(
                name=name,
                value=str(test.get("value", "")),
                status=status,
            )
    
    # Helper methods for parsing
    def _extract_serial(self, content: str) -> str:
        """Extract serial number from content"""
        # Your parsing logic here
        return ""
    
    def _extract_part(self, content: str) -> str:
        """Extract part number from content"""
        # Your parsing logic here
        return ""
    
    def _extract_result(self, content: str) -> str:
        """Extract overall result (P/F) from content"""
        # Your parsing logic here
        return "P"
    
    def _parse_tests(self, content: str) -> Dict[str, List[Dict[str, Any]]]:
        """Parse test data from content"""
        # Your parsing logic here
        return {}
```

## Converter Arguments (ConverterArguments)

When `convert_file()` is called, you receive a `ConverterArguments` object with:

| Attribute | Type | Description |
|-----------|------|-------------|
| `api_client` | `pyWATS` | WATS API client instance |
| `file_info` | `FileInfo` | File metadata (name, path, size, extension, MIME type) |
| `drop_folder` | `Path` | The monitored drop folder |
| `done_folder` | `Path` | Folder for successfully processed files |
| `error_folder` | `Path` | Folder for failed conversions |
| `user_settings` | `dict` | User-configured settings for this converter |

### FileInfo Properties

```python
file_info.path        # Full path to file
file_info.name        # Filename with extension
file_info.stem        # Filename without extension
file_info.extension   # File extension (.csv, .txt, etc.)
file_info.size        # File size in bytes
file_info.parent      # Parent directory
file_info.mime_type   # MIME type (text/csv, etc.)
file_info.file_type   # Detected file type (via magic)
```

## Conversion Results

### Success Result

**Always return a UUTReport instance, not a dictionary!**

```python
# ✅ CORRECT - Using UUTReport model
from pywats.domains.report.report_models import UUTReport

report = UUTReport(pn="PN123", sn="SN001", ...)
# ... build report using factory methods ...

return ConverterResult.success_result(
    report=report,                           # UUTReport instance!
    post_action=PostProcessAction.MOVE,
    warnings=["Minor issue detected"],
    metadata={"rows": 10, "time_ms": 250}
)

# ❌ WRONG - Do NOT use raw dictionaries
# return ConverterResult.success_result(
#     report={"serialNumber": "SN001", ...},  # NO! Use UUTReport!
#     ...
# )
```

### Failed Result

```python
return ConverterResult.failed_result(
    error="Invalid file format",
    warnings=["Header missing"]
)
```

### Suspended Result (Retry Later)

```python
return ConverterResult.suspended_result(
    reason="Waiting for serial number reservation",
    metadata={"retry_after": 60}
)
```

### Skipped Result (File Doesn't Qualify)

```python
return ConverterResult.skipped_result(
    reason="File is not ready for processing"
)
```

## Post-Processing Actions (PPA)

After successful conversion, one of these actions is applied:

| Action | Enum | Description |
|--------|------|-------------|
| **Move** | `PostProcessAction.MOVE` | Move to `Done` folder (default) |
| **Zip** | `PostProcessAction.ZIP` | Zip and move to `Done` folder |
| **Delete** | `PostProcessAction.DELETE` | Delete the source file |
| **Keep** | `PostProcessAction.KEEP` | Keep file in place (no action) |

Failed conversions are always moved to the `Error` folder.

## File Qualification (validate_file)

The `validate_file()` method is called before conversion to quickly filter files:

```python
def validate_file(self, file_info: FileInfo) -> tuple[bool, str]:
    # Check extension
    if file_info.extension.lower() not in [".csv", ".txt"]:
        return False, "Unsupported file extension"
    
    # Check size
    if file_info.size > 10 * 1024 * 1024:  # 10 MB
        return False, "File too large"
    
    # Check MIME type
    if file_info.file_type and "text" not in file_info.file_type:
        return False, "Not a text file"
    
    # Check file signature (magic number)
    with open(file_info.path, 'rb') as f:
        header = f.read(4)
        if header != b'HEAD':
            return False, "Invalid file signature"
    
    return True, ""
```

## Suspended Conversions

Use suspended conversions when:
- Waiting for external resources (serial numbers, etc.)
- File is incomplete (still being written)
- Temporary condition that may resolve later

```python
# In convert_file():
if not serial_available:
    return ConverterResult.suspended_result(
        reason="Waiting for serial number reservation"
    )
```

Suspended files are:
1. Moved to `Suspended` folder
2. Retried automatically after delay
3. Moved to `Error` folder if max attempts reached

## Configuration

### Converter Settings

Users can configure converter behavior in `settings.json`:

```json
{
  "converters": [
    {
      "name": "csv",
      "type": "csv",
      "enabled": true,
      "settings": {
        "delimiter": ",",
        "encoding": "utf-8",
        "skip_header": true,
        "post_action": "zip"
      }
    }
  ]
}
```

### Monitor Folder Configuration

```json
{
  "monitor_folders": [
    {
      "path": "./uploads",
      "enabled": true,
      "converter_type": "csv",
      "recursive": false,
      "delete_after_convert": false,
      "auto_upload": true
    }
  ]
}
```

## Integration Example

```python
from pathlib import Path
from pywats_client import (
    pyWATSApplication,
    FileMonitor,
    MonitorRule,
)
from pywats_client.services.converter_processor import ConverterProcessor
from my_converters import MyConverter

async def main():
    # Create application
    app = pyWATSApplication(config)
    await app.start()
    
    # Create converter
    my_converter = MyConverter(default_station="Station1")
    
    # Create processor
    processor = ConverterProcessor(
        api_client=app.wats_client,
        converters={"myformat": my_converter},
        drop_folder=Path("./uploads"),
        max_retry_attempts=3,
        retry_delay=60
    )
    
    # Setup file monitor
    file_monitor = FileMonitor(check_interval=2)
    
    rule = MonitorRule(
        path="./uploads",
        converter_type="myformat",
        auto_upload=True,
        file_pattern="*.myformat"
    )
    file_monitor.add_rule(rule)
    
    # Handle file events
    async def on_file_event(event):
        if event['type'] == FileEventType.CREATED:
            result = await processor.process_file(
                file_path=event['path'],
                converter_name="myformat",
                user_settings={"station": "Station1"}
            )
            
            if result.status == ConversionStatus.SUCCESS:
                # Queue report for upload
                app.report_queue.queue.append(result.report)
    
    file_monitor.on_file_event(on_file_event)
    await file_monitor.start()
    
    # Keep running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
```

## Error Handling

### Error Folder Structure

```
uploads/
├── Error/
│   ├── failed_file.csv
│   ├── failed_file.csv.error.txt       # Error details
│   ├── another_file_20240101_120000.csv
│   └── another_file_20240101_120000.csv.error.txt
```

### Error Info File Format

```
Conversion failed: Invalid format
Timestamp: 2024-01-01T12:00:00
```

### Suspended Folder Structure

```
uploads/
├── Suspended/
│   ├── pending_file.csv
│   ├── pending_file.csv.suspend.txt    # Suspend details
│   └── ...
```

## Best Practices

1. **ALWAYS Use UUTReport Model**
   - Never build raw dictionaries for reports
   - Use factory methods: `add_numeric_step()`, `add_sequence_call()`, etc.
   - If a feature is missing from the API, report it - don't create workarounds!

2. **File Validation**
   - Always validate files in `validate()` before conversion
   - Check file signature, not just extension
   - Validate size limits

3. **Error Messages**
   - Provide clear, actionable error messages
   - Include context (line numbers, field names, etc.)

4. **Suspended Conversions**
   - Use sparingly and only for recoverable conditions
   - Provide clear suspend reasons
   - Set reasonable retry limits

5. **Post-Processing**
   - Let users configure the post-action
   - Default to MOVE for safety
   - Use ZIP for audit trails

6. **Logging**
   - Log all conversion attempts
   - Include file names and serial numbers
   - Use appropriate log levels

7. **Performance**
   - Process files asynchronously
   - Avoid blocking operations
   - Handle large files efficiently

## Testing Converters

```python
import pytest
from pathlib import Path
from pywats_client.converters.base import ConverterArguments, FileInfo
from my_converters import MyConverter

def test_converter():
    # Create converter
    converter = MyConverter()
    
    # Create test file
    test_file = Path("test_data.myformat")
    test_file.write_text("test data...")
    
    # Create arguments
    file_info = FileInfo(test_file)
    args = ConverterArguments(
        api_client=None,
        file_info=file_info,
        drop_folder=Path("."),
        done_folder=Path("./Done"),
        error_folder=Path("./Error"),
        user_settings={}
    )
    
    # Test validation
    valid, reason = converter.validate_file(file_info)
    assert valid, reason
    
    # Test conversion
    result = converter.convert_file(test_file, args)
    assert result.status == ConversionStatus.SUCCESS
    assert result.report["serialNumber"] == "EXPECTED_SERIAL"
    
    # Cleanup
    test_file.unlink()
```

## Converter Registry

For server-side use, converters can be registered:

```python
# Future feature
from pywats_client.converters import register_converter

@register_converter
class MyConverter(ConverterBase):
    ...
```

This allows the server to discover and use converters automatically.

---

**See Also**:
- `src/pywats_client/converters/base.py` - Base classes and examples
- `src/pywats_client/services/converter_processor.py` - Processor service
- `ARCHITECTURE_REFACTORING.md` - Overall architecture
