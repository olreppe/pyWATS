# Converter Development Guide

**Version:** 0.2.0-beta  
**Last Updated:** February 14, 2026  
**Audience:** Converter developers

---

## Quick Start

### Creating Your First Converter

**1. Create converter class** inheriting from `ConverterBase`:

```python
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from pywats_client.converters.base import ConverterBase
from pywats.models import UUTReport, ReportStatus

class MyCustomConverter(ConverterBase):
    """Converts custom test result files to WATS UUT reports."""
    
    @property
    def name(self) -> str:
        return "MyCustomConverter"
    
    @property
    def supported_extensions(self) -> List[str]:
        return [".custom", ".cst"]
    
    def matches_file(self, file_path: Path) -> bool:
        """Check if this converter can handle the file."""
        return file_path.suffix.lower() in self.supported_extensions
    
    def convert(self, content: str, file_path: Path) -> Dict:
        """
        Convert file content to UUT report.
        
        Args:
            content: File content as string
            file_path: Path to file being converted
            
        Returns:
            dict: UUTReport.model_dump() format
            
        Raises:
            ValueError: If file format is invalid
        """
        # Parse your custom format
        lines = content.strip().split('\n')
        
        # Extract required fields
        serial_number = self._extract_field(lines, "SERIAL:")
        part_number = self._extract_field(lines, "PART:")
        test_result = self._extract_field(lines, "RESULT:")
        
        # Create UUT report
        report = UUTReport(
            pn=part_number,
            sn=serial_number,
            rev="A",
            process_code=1,
            station_name="TestStation",
            location="Factory",
            purpose="Production",
            result=ReportStatus.Passed if test_result == "PASS" else ReportStatus.Failed,
            start=datetime.now().astimezone(),
        )
        
        return report.model_dump()
    
    def _extract_field(self, lines: List[str], prefix: str) -> str:
        """Helper to extract field from lines."""
        for line in lines:
            if line.startswith(prefix):
                return line.split(":", 1)[1].strip()
        raise ValueError(f"Missing required field: {prefix}")
```

**2. Add converter to configuration**:

```yaml
# converters.yaml
converters:
  - name: MyCustomConverter
    module_path: my_project.converters.custom_converter
    class_name: MyCustomConverter
    enabled: true
    priority: 5
    watch_folder: /data/custom-results
    done_folder: /data/done
    error_folder: /data/error
    post_process_action: DELETE
```

**3. Test your converter**:

```python
import pytest
from pathlib import Path
from my_project.converters.custom_converter import MyCustomConverter

def test_custom_converter():
    converter = MyCustomConverter()
    
    # Create test file content
    content = """
    PART: TEST-123
    SERIAL: SN-00001
    RESULT: PASS
    """
    
    # Convert
    result = converter.convert(content, Path("test.custom"))
    
    # Verify
    assert result['pn'] == "TEST-123"
    assert result['sn'] == "SN-00001"
    assert result['result'] == "Passed"
```

---

## ConverterBase API Reference

### Required Properties

#### `name: str`

**Purpose**: Unique identifier for the converter (used in logs, config, errors)

**Example**:
```python
@property
def name(self) -> str:
    return "CSVConverter"
```

**Best Practices**:
- Use descriptive names: `XMLConverter`, `LabVIEWConverter`, `TestStandConverter`
- Avoid generic names: `Converter`, `FileConverter`
- Use consistent naming convention across converters

---

#### `supported_extensions: List[str]`

**Purpose**: File extensions this converter can process

**Example**:
```python
@property
def supported_extensions(self) -> List[str]:
    return [".csv", ".txt", ".dat"]
```

**Best Practices**:
- Always use lowercase: `[".csv"]` not `[".CSV"]`
- Include the dot: `[".xml"]` not `["xml"]`
- List all variants: `[".jpg", ".jpeg"]`
- Be specific to avoid conflicts

---

### Required Methods

#### `matches_file(file_path: Path) -> bool`

**Purpose**: Determine if this converter can process a specific file

**Signature**:
```python
def matches_file(self, file_path: Path) -> bool:
    """
    Check if this converter can handle the file.
    
    Args:
        file_path: Path to file to check
        
    Returns:
        bool: True if converter can process this file
    """
```

**Basic Implementation**:
```python
def matches_file(self, file_path: Path) -> bool:
    return file_path.suffix.lower() in self.supported_extensions
```

**Advanced Implementation** (with content inspection):
```python
def matches_file(self, file_path: Path) -> bool:
    # Check extension first
    if file_path.suffix.lower() not in self.supported_extensions:
        return False
    
    # Check file signature/header
    try:
        with open(file_path, 'r') as f:
            first_line = f.readline()
            return first_line.startswith("<?xml")  # XML detection
    except Exception:
        return False
```

---

#### `convert(content: str, file_path: Path) -> dict`

**Purpose**: Convert file content to UUTReport dictionary

**Signature**:
```python
def convert(self, content: str, file_path: Path) -> dict:
    """
    Convert file content to UUT report dict.
    
    Args:
        content: Complete file content as string
        file_path: Path to file being converted (for context/logging)
        
    Returns:
        dict: UUTReport.model_dump() format
        
    Raises:
        ValueError: If content format is invalid
        KeyError: If required field is missing
    """
```

**Implementation Pattern**:
```python
def convert(self, content: str, file_path: Path) -> dict:
    # 1. Parse content
    data = self._parse_content(content)
    
    # 2. Validate required fields
    self._validate_data(data)
    
    # 3. Transform to UUTReport
    report = UUTReport(
        pn=data['part_number'],
        sn=data['serial_number'],
        rev=data.get('revision', 'A'),
        process_code=data['process_code'],
        station_name=data['station'],
        location=data.get('location', 'Unknown'),
        purpose=data.get('purpose', 'Production'),
        result=self._map_result(data['result']),
        start=self._parse_timestamp(data['start_time']),
    )
    
    # 4. Add test steps (if any)
    if 'test_steps' in data:
        report.steps = self._convert_steps(data['test_steps'])
    
    # 5. Return as dict
    return report.model_dump()
```

---

## UUTReport Structure

### Required Fields

```python
from pywats.models import UUTReport, ReportStatus
from datetime import datetime

report = UUTReport(
    # Product Information (REQUIRED)
    pn="PART-NUMBER",        # Part number
    sn="SERIAL-NUMBER",      # Serial number
    rev="A",                 # Revision
    
    # Process Information (REQUIRED)
    process_code=1,          # WATS process code (int)
    station_name="Station1", # Test station name
    location="Factory1",     # Test location
    purpose="Production",    # Test purpose
    
    # Result (REQUIRED)
    result=ReportStatus.Passed,  # or ReportStatus.Failed
    
    # Timing (REQUIRED)
    start=datetime.now().astimezone(),  # Test start time (must have timezone)
)
```

### Optional Fields

```python
report = UUTReport(
    # ... required fields ...
    
    # Optional metadata
    batch_serial_number="BATCH-001",
    operator="John Doe",
    comment="Initial production run",
    
    # Optional timing
    stop=datetime.now().astimezone(),  # Test end time
    
    # Test steps (sequence of operations)
    steps=[
        # Add test steps here
    ],
    
    # Root cause (for failures)
    root_causes=[
        # Add root cause info
    ],
)
```

---

## Common Patterns

### Pattern 1: CSV File Conversion

```python
import csv
from io import StringIO

class CSVConverter(ConverterBase):
    def convert(self, content: str, file_path: Path) -> dict:
        # Parse CSV
        reader = csv.DictReader(StringIO(content))
        rows = list(reader)
        
        if not rows:
            raise ValueError("Empty CSV file")
        
        # Assume first row is header info, rest are test steps
        header = rows[0]
        
        report = UUTReport(
            pn=header['PartNumber'],
            sn=header['SerialNumber'],
            rev=header.get('Revision', 'A'),
            process_code=int(header['ProcessCode']),
            station_name=header['Station'],
            location=header.get('Location', 'Unknown'),
            purpose=header.get('Purpose', 'Production'),
            result=self._parse_result(header['Result']),
            start=self._parse_datetime(header['StartTime']),
        )
        
        return report.model_dump()
    
    def _parse_result(self, result_str: str) -> ReportStatus:
        """Convert string result to ReportStatus enum."""
        result_map = {
            'PASS': ReportStatus.Passed,
            'FAIL': ReportStatus.Failed,
            'ERROR': ReportStatus.Error,
            'TERMINATED': ReportStatus.Terminated,
        }
        return result_map.get(result_str.upper(), ReportStatus.Failed)
    
    def _parse_datetime(self, dt_str: str) -> datetime:
        """Parse datetime string to timezone-aware datetime."""
        # Example: "2026-02-14 10:30:00"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.astimezone()  # Add local timezone
```

### Pattern 2: XML File Conversion

```python
import xml.etree.ElementTree as ET

class XMLConverter(ConverterBase):
    def convert(self, content: str, file_path: Path) -> dict:
        # Parse XML
        root = ET.fromstring(content)
        
        # Extract fields using XPath-like queries
        report = UUTReport(
            pn=root.find('.//PartNumber').text,
            sn=root.find('.//SerialNumber').text,
            rev=root.find('.//Revision').text or 'A',
            process_code=int(root.find('.//ProcessCode').text),
            station_name=root.find('.//Station').text,
            location=root.find('.//Location').text or 'Unknown',
            purpose=root.find('.//Purpose').text or 'Production',
            result=self._parse_result(root.find('.//Result').text),
            start=self._parse_datetime(root.find('.//StartTime').text),
        )
        
        # Add test steps
        steps = []
        for step_elem in root.findall('.//TestStep'):
            step = self._convert_step(step_elem)
            steps.append(step)
        
        if steps:
            report.steps = steps
        
        return report.model_dump()
    
    def _convert_step(self, step_elem: ET.Element) -> dict:
        """Convert XML step element to test step dict."""
        # Implement based on your XML structure
        return {
            'name': step_elem.find('Name').text,
            'result': step_elem.find('Result').text,
            # ... other step fields
        }
```

### Pattern 3: JSON File Conversion

```python
import json

class JSONConverter(ConverterBase):
    def convert(self, content: str, file_path: Path) -> dict:
        # Parse JSON
        data = json.loads(content)
        
        # Direct mapping if JSON structure matches UUTReport
        report = UUTReport(
            pn=data['partNumber'],
            sn=data['serialNumber'],
            rev=data.get('revision', 'A'),
            process_code=data['processCode'],
            station_name=data['station'],
            location=data.get('location', 'Unknown'),
            purpose=data.get('purpose', 'Production'),
            result=ReportStatus[data['result']],  # Use enum name
            start=datetime.fromisoformat(data['startTime']),
        )
        
        # Handle nested test steps
        if 'testSteps' in data:
            report.steps = data['testSteps']  # Already in correct format
        
        return report.model_dump()
```

### Pattern 4: Multi-UUT Report (Batch Files)

```python
class BatchConverter(ConverterBase):
    """Handle files containing multiple UUT reports."""
    
    def convert(self, content: str, file_path: Path) -> dict:
        """
        For batch files, return the first report.
        Store others in .queued files for separate processing.
        """
        reports = self._parse_all_reports(content)
        
        if not reports:
            raise ValueError("No reports found in batch file")
        
        # Save additional reports as separate .queued files
        if len(reports) > 1:
            self._save_additional_reports(reports[1:], file_path)
        
        # Return first report
        return reports[0]
    
    def _save_additional_reports(self, reports: List[dict], source_file: Path):
        """Save additional reports as .queued files."""
        pending_dir = source_file.parent.parent / "pending"
        pending_dir.mkdir(exist_ok=True)
        
        for i, report in enumerate(reports):
            queued_file = pending_dir / f"{source_file.stem}_{i+1}.json.queued"
            queued_file.write_text(json.dumps(report, indent=2))
```

---

## Error Handling

### Validation Best Practices

```python
def convert(self, content: str, file_path: Path) -> dict:
    # Validate content is not empty
    if not content or not content.strip():
        raise ValueError("File is empty")
    
    # Parse content
    try:
        data = self._parse(content)
    except Exception as e:
        raise ValueError(f"Invalid file format: {e}")
    
    # Validate required fields
    required_fields = ['part_number', 'serial_number', 'result']
    missing = [f for f in required_fields if f not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    
    # Validate field formats
    if not data['serial_number']:
        raise ValueError("Serial number cannot be empty")
    
    if len(data['part_number']) > 50:
        raise ValueError("Part number too long (max 50 characters)")
    
    # Create report...
```

### Error Messages

**Good Error Messages** (actionable, specific):
```python
raise ValueError("Missing required field 'SerialNumber' in header row")
raise ValueError("Invalid date format: expected 'YYYY-MM-DD', got '02/14/2026'")
raise ValueError("Test result must be one of: PASS, FAIL, ERROR, TERMINATED")
```

**Bad Error Messages** (vague, unhelpful):
```python
raise ValueError("Invalid file")
raise ValueError("Error")
raise ValueError("Bad data")
```

### Logging

```python
import logging

class MyConverter(ConverterBase):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(f"converter.{self.name}")
    
    def convert(self, content: str, file_path: Path) -> dict:
        self.logger.info(f"Converting {file_path.name}")
        
        try:
            data = self._parse(content)
            self.logger.debug(f"Parsed data: {len(data)} fields")
            
            report = self._create_report(data)
            self.logger.info(f"Converted to report: {report['sn']}")
            
            return report
        except Exception as e:
            self.logger.error(f"Conversion failed for {file_path.name}: {e}")
            raise
```

---

## Testing Your Converter

### Unit Test Template

```python
import pytest
from pathlib import Path
from my_converter import MyConverter
from pywats.models import ReportStatus

class TestMyConverter:
    """Unit tests for MyConverter."""
    
    @pytest.fixture
    def converter(self):
        """Create converter instance."""
        return MyConverter()
    
    def test_name(self, converter):
        """Test converter name property."""
        assert converter.name == "MyConverter"
    
    def test_supported_extensions(self, converter):
        """Test supported extensions."""
        assert ".custom" in converter.supported_extensions
    
    def test_matches_file(self, converter):
        """Test file matching."""
        assert converter.matches_file(Path("test.custom"))
        assert not converter.matches_file(Path("test.txt"))
    
    def test_convert_valid_file(self, converter):
        """Test conversion of valid file."""
        content = """
        PART: TEST-123
        SERIAL: SN-00001
        RESULT: PASS
        """
        
        result = converter.convert(content, Path("test.custom"))
        
        assert result['pn'] == "TEST-123"
        assert result['sn'] == "SN-00001"
        assert result['result'] == ReportStatus.Passed.value
    
    def test_convert_empty_file(self, converter):
        """Test conversion fails on empty file."""
        with pytest.raises(ValueError, match="empty"):
            converter.convert("", Path("test.custom"))
    
    def test_convert_missing_field(self, converter):
        """Test conversion fails on missing required field."""
        content = "PART: TEST-123"  # Missing SERIAL
        
        with pytest.raises(ValueError, match="SERIAL"):
            converter.convert(content, Path("test.custom"))
    
    def test_convert_invalid_result(self, converter):
        """Test conversion handles invalid result gracefully."""
        content = """
        PART: TEST-123
        SERIAL: SN-00001
        RESULT: UNKNOWN
        """
        
        with pytest.raises(ValueError, match="result"):
            converter.convert(content, Path("test.custom"))
```

### Integration Test Template

```python
import pytest
from pathlib import Path
from tests.fixtures.test_file_generators import TestFileGenerator

class TestMyConverterIntegration:
    """Integration tests for MyConverter."""
    
    @pytest.fixture
    def test_file(self, tmp_path):
        """Create test file."""
        file_path = tmp_path / "test.custom"
        file_path.write_text("""
        PART: TEST-123
        SERIAL: SN-00001
        RESULT: PASS
        """)
        return file_path
    
    @pytest.mark.asyncio
    async def test_end_to_end_conversion(self, test_file, converter_pool):
        """Test complete conversion pipeline."""
        # Add file to watch folder
        watch_file = converter_pool.watch_folder / test_file.name
        watch_file.write_text(test_file.read_text())
        
        # Start pool
        task = asyncio.create_task(converter_pool.run())
        await asyncio.sleep(2.0)
        
        # Verify file processed
        assert not watch_file.exists()
        
        # Stop pool
        converter_pool.stop()
        await task
```

---

## Performance Optimization

### Optimization Tips

**1. Parse Once, Use Many Times**:
```python
# Bad: Parse multiple times
def convert(self, content: str, file_path: Path) -> dict:
    lines = content.split('\n')  # Parse 1
    sn = self._extract(content.split('\n'), 'SN')  # Parse 2
    pn = self._extract(content.split('\n'), 'PN')  # Parse 3

# Good: Parse once
def convert(self, content: str, file_path: Path) -> dict:
    lines = content.split('\n')  # Parse once
    sn = self._extract(lines, 'SN')
    pn = self._extract(lines, 'PN')
```

**2. Use Efficient Data Structures**:
```python
# Bad: List search (O(n))
def find_value(lines: List[str], prefix: str) -> str:
    for line in lines:
        if line.startswith(prefix):
            return line.split(':', 1)[1]

# Good: Dict lookup (O(1))
def parse_to_dict(lines: List[str]) -> Dict[str, str]:
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    return data
```

**3. Lazy Evaluation for Large Files**:
```python
def convert(self, content: str, file_path: Path) -> dict:
    # Don't parse entire file if only header is needed
    lines = content.split('\n', 10)  # Only split first 10 lines
    header = self._parse_header(lines[:5])
    
    # Only parse rest if needed
    if header['has_steps']:
        all_lines = content.split('\n')
        steps = self._parse_steps(all_lines[10:])
```

**4. Cache Compiled Patterns**:
```python
import re

class MyConverter(ConverterBase):
    # Class-level compiled patterns (shared across instances)
    SERIAL_PATTERN = re.compile(r'SERIAL:\s*(\S+)')
    PART_PATTERN = re.compile(r'PART:\s*(\S+)')
    
    def convert(self, content: str, file_path: Path) -> dict:
        # Fast pattern matching
        sn_match = self.SERIAL_PATTERN.search(content)
        pn_match = self.PART_PATTERN.search(content)
        
        if not sn_match or not pn_match:
            raise ValueError("Missing required fields")
        
        # ... create report
```

---

## Deployment

### Adding Converter to System

**1. Package your converter**:
```
my_converters/
├── __init__.py
├── custom_converter.py
└── tests/
    └── test_custom_converter.py
```

**2. Install package**:
```bash
pip install -e ./my_converters
```

**3. Configure converter**:
```yaml
# /etc/pywats/converters.yaml
converters:
  - name: MyCustomConverter
    module_path: my_converters.custom_converter
    class_name: MyCustomConverter
    enabled: true
    priority: 5
    watch_folder: /data/custom
    done_folder: /data/done
    error_folder: /data/error
```

**4. Test configuration**:
```python
from pywats_client.core.config import load_converter_config

configs = load_converter_config('/etc/pywats/converters.yaml')
print(f"Loaded {len(configs)} converters")
```

**5. Start converter pool**:
```bash
python -m pywats_client.service.converter_service \
    --config /etc/pywats/converters.yaml
```

---

## Troubleshooting

### Common Issues

**Issue**: "Converter not processing files"
- **Check**: File extension matches `supported_extensions`
- **Check**: Converter enabled in config (`enabled: true`)
- **Check**: Watch folder path is correct
- **Check**: File permissions (can read files)

**Issue**: "Module not found error"
- **Check**: Converter package installed
- **Check**: `module_path` matches actual Python import path
- **Check**: `__init__.py` exists in package
- **Check**: Python path (`sys.path`) includes converter location

**Issue**: "Files move to error folder immediately"
- **Check**: Converter logs for exception details
- **Check**: File format matches converter expectations
- **Check**: Required fields present in file
- **Check**: Field value formats are valid

**Issue**: "Memory usage grows over time"
- **Check**: No global state accumulation in converter
- **Check**: Files properly closed (use `with` statement or `Path.read_text()`)
- **Check**: Large objects not stored in instance variables
- **Solution**: See [Memory Management](#memory-management) section

---

## Next Steps

**Read More**:
- [Architecture Guide](converter-architecture.md) - System overview
- [Best Practices Guide](converter-best-practices.md) - Production patterns
- [Known Issues](converter-known-issues.md) - Common problems

**Get Help**:
- Check existing converters in `src/pywats_client/converters/`
- Review integration tests in `tests/integration/`
- Ask on pyWATS discussions

---

**Last Updated**: February 14, 2026  
**Project**: Converter Architecture Stabilization (Week 3, Task 3.4)
