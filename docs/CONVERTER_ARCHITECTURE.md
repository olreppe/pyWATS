# Converter Architecture Guide

## Overview

The pyWATS Client converter architecture provides a flexible framework for converting various file formats into WATS report structures. Converters run on the client (and potentially on the server in the future) and integrate with the file monitoring system.

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

```python
from pathlib import Path
from typing import Dict, Any
from pywats_client.converters.base import (
    ConverterBase,
    ConverterResult,
    ConverterArguments,
    FileInfo,
    PostProcessAction,
    ConversionStatus,
)

class MyConverter(ConverterBase):
    """
    Custom converter for MyFormat files.
    """
    
    def __init__(self, default_station: str = "Station1"):
        super().__init__()
        self.default_station = default_station
    
    @property
    def name(self) -> str:
        return "My Custom Converter"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Converts MyFormat files to UUT reports"
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".myformat", ".mf"]
    
    @property
    def supported_mime_types(self) -> list[str]:
        return ["application/x-myformat"]
    
    def validate_file(self, file_info: FileInfo) -> tuple[bool, str]:
        """Validate file before conversion"""
        # Call base validation (checks extension and MIME type)
        valid, reason = super().validate_file(file_info)
        if not valid:
            return False, reason
        
        # Custom validation
        if file_info.size > 5 * 1024 * 1024:  # 5 MB limit
            return False, "File exceeds 5 MB limit"
        
        # Check file signature (first bytes)
        try:
            with open(file_info.path, 'rb') as f:
                header = f.read(4)
                if header != b'MFMT':  # Expected magic number
                    return False, "Invalid file signature"
        except Exception as e:
            return False, f"Cannot read file: {e}"
        
        return True, ""
    
    def convert_file(
        self,
        file_path: Path,
        args: ConverterArguments
    ) -> ConverterResult:
        """Convert file to UUT report"""
        try:
            # Access converter arguments
            api = args.api_client
            file_info = args.file_info
            settings = args.user_settings
            
            # Read and parse file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()
            
            # Extract data (your custom parsing logic)
            serial_number = self._extract_serial(data)
            part_number = self._extract_part(data)
            result = self._extract_result(data)
            
            # Check if conversion should be suspended
            if not serial_number:
                return ConverterResult.suspended_result(
                    reason="No serial number found, waiting for complete data"
                )
            
            # Create WATS report structure
            report = {
                "type": "UUT",
                "serialNumber": serial_number,
                "partNumber": part_number or settings.get("default_part", "UNKNOWN"),
                "result": result,
                "processCode": 10,
                "stationName": settings.get("station", self.default_station),
            }
            
            # Determine post-processing action
            post_action_str = settings.get("post_action", "move")
            post_action = {
                "delete": PostProcessAction.DELETE,
                "move": PostProcessAction.MOVE,
                "zip": PostProcessAction.ZIP,
                "keep": PostProcessAction.KEEP
            }.get(post_action_str, PostProcessAction.MOVE)
            
            # Return success
            return ConverterResult.success_result(
                report=report,
                post_action=post_action,
                metadata={
                    "source_file": file_info.name,
                    "file_size": file_info.size,
                }
            )
        
        except Exception as e:
            return ConverterResult.failed_result(
                error=f"Conversion error: {str(e)}"
            )
    
    def on_success(
        self,
        file_path: Path,
        result: ConverterResult,
        args: ConverterArguments
    ) -> None:
        """Called after successful conversion"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(
            f"Successfully converted {file_path.name}: "
            f"SN={result.report['serialNumber']}"
        )
    
    def on_failure(
        self,
        file_path: Path,
        result: ConverterResult,
        args: ConverterArguments
    ) -> None:
        """Called after failed conversion"""
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to convert {file_path.name}: {result.error}")
    
    def get_arguments(self) -> Dict[str, Any]:
        """Define configurable arguments"""
        return {
            "station": {
                "type": "string",
                "default": self.default_station,
                "description": "Test station name",
                "required": True
            },
            "default_part": {
                "type": "string",
                "default": "UNKNOWN",
                "description": "Default part number if not found in file"
            },
            "post_action": {
                "type": "choice",
                "default": "move",
                "choices": ["delete", "move", "zip", "keep"],
                "description": "Post-processing action"
            },
            "timeout": {
                "type": "int",
                "default": 30,
                "description": "Conversion timeout (seconds)",
                "min": 1,
                "max": 300
            }
        }
    
    # Helper methods
    def _extract_serial(self, data: str) -> str:
        """Extract serial number from data"""
        # Your parsing logic here
        pass
    
    def _extract_part(self, data: str) -> str:
        """Extract part number from data"""
        # Your parsing logic here
        pass
    
    def _extract_result(self, data: str) -> str:
        """Extract test result from data"""
        # Your parsing logic here
        pass
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

```python
return ConverterResult.success_result(
    report={...},                           # WATS report structure
    post_action=PostProcessAction.MOVE,     # What to do with file
    warnings=["Minor issue detected"],      # Optional warnings
    metadata={"rows": 10, "time_ms": 250}   # Optional metadata
)
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

1. **File Validation**
   - Always validate files in `validate_file()` before conversion
   - Check file signature, not just extension
   - Validate size limits

2. **Error Messages**
   - Provide clear, actionable error messages
   - Include context (line numbers, field names, etc.)

3. **Suspended Conversions**
   - Use sparingly and only for recoverable conditions
   - Provide clear suspend reasons
   - Set reasonable retry limits

4. **Post-Processing**
   - Let users configure the post-action
   - Default to MOVE for safety
   - Use ZIP for audit trails

5. **Logging**
   - Log all conversion attempts
   - Include file names and serial numbers
   - Use appropriate log levels

6. **Performance**
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
