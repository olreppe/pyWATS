# Converter Architecture - Quick Reference

## What's a Converter?

A converter is a Python script that converts files (CSV, XML, JSON, etc.) into WATS report structures. Converters run on the client and can potentially run on the server in the future.

## Key Concepts

### 1. File Lifecycle

```
Drop Folder → Validate → Convert → Post-Process → Done/Error/Suspended
```

### 2. Conversion Status

| Status | Description | Next Action |
|--------|-------------|-------------|
| **SUCCESS** | Converted successfully | Apply PPA (Move/Zip/Delete/Keep) |
| **FAILED** | Conversion failed | Move to Error folder |
| **SUSPENDED** | Temporarily suspended | Move to Suspended, retry later |
| **SKIPPED** | File doesn't qualify | No action |

### 3. Post-Processing Actions (PPA)

| Action | What It Does | When to Use |
|--------|--------------|-------------|
| **MOVE** | Move to Done folder | Default, safe option |
| **ZIP** | Zip and move to Done | Audit trails, space savings |
| **DELETE** | Delete source file | When source not needed |
| **KEEP** | Keep in place | Debugging, special cases |

## Creating a Converter

### Minimal Example

```python
from pathlib import Path
from pywats_client.converters.base import (
    ConverterBase,
    ConverterResult,
    ConverterArguments,
    PostProcessAction,
)

class MyConverter(ConverterBase):
    @property
    def name(self) -> str:
        return "My Converter"
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".myformat"]
    
    def convert_file(self, file_path: Path, args: ConverterArguments) -> ConverterResult:
        # Read file
        with open(file_path) as f:
            data = f.read()
        
        # Parse and create report
        report = {
            "type": "UUT",
            "serialNumber": extract_serial(data),
            "partNumber": extract_part(data),
            "result": "Passed"
        }
        
        # Return success
        return ConverterResult.success_result(
            report=report,
            post_action=PostProcessAction.MOVE
        )
```

### Full Featured Example

```python
from pathlib import Path
from typing import Tuple
from pywats_client.converters.base import (
    ConverterBase,
    ConverterResult,
    ConverterArguments,
    FileInfo,
    PostProcessAction,
)

class FullFeaturedConverter(ConverterBase):
    @property
    def name(self) -> str:
        return "Full Featured Converter"
    
    @property
    def supported_extensions(self) -> list[str]:
        return [".dat", ".txt"]
    
    @property
    def supported_mime_types(self) -> list[str]:
        return ["text/plain"]
    
    def validate_file(self, file_info: FileInfo) -> Tuple[bool, str]:
        """Validate file before conversion"""
        # Call base validation
        valid, reason = super().validate_file(file_info)
        if not valid:
            return False, reason
        
        # Check file size
        if file_info.size > 10 * 1024 * 1024:  # 10 MB
            return False, "File too large"
        
        # Check file signature
        with open(file_info.path, 'rb') as f:
            if f.read(4) != b'DATA':
                return False, "Invalid file signature"
        
        return True, ""
    
    def convert_file(self, file_path: Path, args: ConverterArguments) -> ConverterResult:
        """Convert file"""
        try:
            # Access converter arguments
            api = args.api_client
            settings = args.user_settings
            file_info = args.file_info
            
            # Read file
            with open(file_path) as f:
                data = f.read()
            
            # Parse data
            serial = self._extract_serial(data)
            
            # Check if we should suspend
            if not serial:
                return ConverterResult.suspended_result(
                    reason="No serial number found"
                )
            
            # Create report
            report = {
                "type": "UUT",
                "serialNumber": serial,
                "partNumber": settings.get("default_part", "UNKNOWN"),
                "result": "Passed"
            }
            
            # Get post-action from settings
            post_action = {
                "delete": PostProcessAction.DELETE,
                "move": PostProcessAction.MOVE,
                "zip": PostProcessAction.ZIP,
                "keep": PostProcessAction.KEEP
            }.get(settings.get("post_action", "move"), PostProcessAction.MOVE)
            
            return ConverterResult.success_result(
                report=report,
                post_action=post_action
            )
        
        except Exception as e:
            return ConverterResult.failed_result(
                error=f"Conversion error: {e}"
            )
    
    def on_success(self, file_path: Path, result: ConverterResult, args: ConverterArguments):
        """Called after success"""
        print(f"Converted: {file_path.name}")
    
    def on_failure(self, file_path: Path, result: ConverterResult, args: ConverterArguments):
        """Called after failure"""
        print(f"Failed: {file_path.name} - {result.error}")
    
    def get_arguments(self) -> dict:
        """Define configurable arguments"""
        return {
            "default_part": {
                "type": "string",
                "default": "UNKNOWN",
                "description": "Default part number"
            },
            "post_action": {
                "type": "choice",
                "default": "move",
                "choices": ["delete", "move", "zip", "keep"],
                "description": "Post-processing action"
            }
        }
    
    def _extract_serial(self, data: str) -> str:
        # Your parsing logic
        pass
```

## Using ConverterProcessor

```python
from pathlib import Path
from pywats_client.services.converter_processor import ConverterProcessor
from my_converters import MyConverter

# Create processor
processor = ConverterProcessor(
    api_client=wats_client,
    converters={"myconverter": MyConverter()},
    drop_folder=Path("./uploads"),
    max_retry_attempts=3,
    retry_delay=60
)

# Process a file
result = await processor.process_file(
    file_path=Path("./uploads/test.dat"),
    converter_name="myconverter",
    user_settings={"default_part": "ABC123"}
)

# Check result
if result.status == ConversionStatus.SUCCESS:
    print(f"Report: {result.report}")
    # Queue for upload...
```

## Converter Arguments

When your `convert_file()` is called, you get `ConverterArguments`:

```python
args.api_client      # pyWATS API client
args.file_info       # FileInfo object
args.drop_folder     # Drop folder path
args.done_folder     # Done folder path
args.error_folder    # Error folder path
args.user_settings   # User configuration dict
```

### FileInfo Properties

```python
args.file_info.path        # Full path
args.file_info.name        # Filename with extension
args.file_info.stem        # Filename without extension
args.file_info.extension   # File extension (.csv, .txt)
args.file_info.size        # File size in bytes
args.file_info.parent      # Parent directory
args.file_info.mime_type   # MIME type
args.file_info.file_type   # Detected file type (magic)
```

## Return Results

### Success
```python
return ConverterResult.success_result(
    report={...},
    post_action=PostProcessAction.MOVE
)
```

### Failure
```python
return ConverterResult.failed_result(
    error="Invalid format"
)
```

### Suspend (Retry Later)
```python
return ConverterResult.suspended_result(
    reason="Waiting for serial number"
)
```

### Skip
```python
return ConverterResult.skipped_result(
    reason="File not ready"
)
```

## Folder Structure

```
uploads/                    # Drop folder (monitored)
├── file1.csv
├── file2.csv
├── Done/                   # Successful conversions
│   ├── file1.csv           # Moved
│   └── file2_20240101.zip  # Zipped
├── Error/                  # Failed conversions
│   ├── bad_file.csv
│   └── bad_file.csv.error.txt
└── Suspended/              # Suspended conversions (retry)
    ├── incomplete.csv
    └── incomplete.csv.suspend.txt
```

## Integration with File Monitor

```python
from pywats_client import FileMonitor, MonitorRule
from pywats_client.services.converter_processor import ConverterProcessor

# Create file monitor
file_monitor = FileMonitor(check_interval=2)

# Add monitoring rule
rule = MonitorRule(
    path="./uploads",
    converter_type="myconverter",
    auto_upload=True,
    file_pattern="*.dat"
)
file_monitor.add_rule(rule)

# Handle file events
async def on_file_event(event):
    if event['type'] == FileEventType.CREATED:
        result = await processor.process_file(
            file_path=event['path'],
            converter_name=event['converter_type'],
            user_settings={}
        )
        
        if result.status == ConversionStatus.SUCCESS:
            # Queue report
            app.report_queue.queue.append(result.report)

file_monitor.on_file_event(on_file_event)
await file_monitor.start()
```

## Configuration

### Settings File

```json
{
  "converters": [
    {
      "name": "myconverter",
      "enabled": true,
      "settings": {
        "default_part": "ABC123",
        "post_action": "zip"
      }
    }
  ],
  "monitor_folders": [
    {
      "path": "./uploads",
      "converter_type": "myconverter",
      "auto_upload": true
    }
  ]
}
```

## Best Practices

1. **Always validate files** in `validate_file()` before conversion
2. **Check file signatures** (magic numbers), not just extensions
3. **Validate file sizes** to prevent memory issues
4. **Use suspended conversions** for recoverable conditions only
5. **Provide clear error messages** with context
6. **Let users configure** post-processing actions
7. **Log all conversion attempts** with file names and serial numbers
8. **Test with various file formats** and edge cases

## Common Patterns

### Waiting for Serial Number

```python
serial = self._get_serial_from_pool()
if not serial:
    return ConverterResult.suspended_result(
        reason="Waiting for serial number reservation"
    )
```

### Multi-Row CSV Files

```python
rows = parse_csv(file_path)
for row in rows:
    report = create_report_from_row(row)
    # Submit each report...
```

### Custom Post-Processing

```python
def on_success(self, file_path, result, args):
    # Custom notification
    send_email(f"Converted {file_path.name}")
    
    # Custom archiving
    archive_file(file_path, result.report)
```

---

**See Full Documentation**: `docs/CONVERTER_ARCHITECTURE.md`
