"""Test null sanitization for WSJF converter"""
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pywats_client.converters.standard.wats_standard_json_converter import WATSStandardJSONConverter
from pywats_client.converters.converter import ConverterSource, ConverterContext

# Test file path
test_file = Path(r"C:\ProgramData\Virinco\pyWATS\instances\default\WSJF\Error\1004est-295_FATPartNo_Rev1_2026-02-12_12-48-04.json")

if not test_file.exists():
    print(f"ERROR: Test file not found: {test_file}")
    sys.exit(1)

# Load raw JSON
with open(test_file, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Count nulls BEFORE sanitization
json_before = json.dumps(raw_data)
nulls_before = json_before.count(': null')
print(f"Nulls BEFORE sanitization: {nulls_before}")

# Create converter and convert
converter = WATSStandardJSONConverter()
source = ConverterSource(path=test_file, converter_name="WSJF")
context = ConverterContext(api_url="https://python.wats.com", credentials="test:test")

result = converter.convert(source, context)

if result.success:
    print(f"\n✓ Conversion successful!")
    print(f"  Report type: {type(result.report).__name__}")
    
    # Serialize the report back to JSON
    if hasattr(result.report, 'model_dump'):
        report_dict = result.report.model_dump(mode="json", by_alias=True, exclude_none=True)
        json_after = json.dumps(report_dict)
        nulls_after = json_after.count(': null')
        print(f"  Nulls AFTER conversion: {nulls_after}")
        
        # Check specific field
        if 'root' in report_dict and 'steps' in report_dict['root']:
            steps = report_dict['root']['steps']
            if steps:
                first_step = steps[0]
                if 'messagePopup' in first_step:
                    response = first_step['messagePopup'].get('response')
                    print(f"\n  First step messagePopup.response: {repr(response)}")
else:
    print(f"\n✗ Conversion failed: {result.error}")
