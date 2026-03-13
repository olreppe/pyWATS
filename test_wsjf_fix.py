"""Test WSJF converter fix"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pywats_client.converters.standard.wats_standard_json_converter import WATSStandardJsonConverter
from pywats_client.converters.models import ConverterSource
from pywats_client.converters.context import ConverterContext

# Test file path
test_file = Path(r"C:\ProgramData\Virinco\pyWATS\instances\default\WSJF\Error\1004est-295_FATPartNo_Rev1_2026-02-12_12-48-04.json")

if not test_file.exists():
    print(f"ERROR: Test file not found: {test_file}")
    sys.exit(1)

print(f"Testing converter with file: {test_file.name}\n")

# Create converter
converter = WATSStandardJsonConverter()

# Set runtime paths (as async_converter_pool would)
converter.watch_path = test_file.parent.parent / "Watch"
converter.done_path = test_file.parent.parent / "Done"
converter.error_path = test_file.parent.parent / "Error"
converter.pending_path = test_file.parent.parent / "Pending"

print(f"✓ Converter loaded: {converter.name}")
print(f"✓ Has error_path: {converter.error_path}")
print(f"✓ Has watch_path: {converter.watch_path}\n")

# Validate file
source = ConverterSource.from_file(test_file)
context = ConverterContext()

validation = converter.validate(source, context)
print(f"Validation Results:")
print(f"  Can convert: {validation.can_convert}")
print(f"  Confidence: {validation.confidence:.2f}")
print(f"  Message: {validation.message}")
print(f"  Part Number: {validation.detected_part_number}")
print(f"  Serial Number: {validation.detected_serial_number}")
print()

# Convert file
if validation.can_convert:
    try:
        result = converter.convert(source, context)
        
        if result.success:
            print(f"✓ Conversion successful!")
            print(f"  Report type: {type(result.report).__name__}")
            print(f"  Part Number: {result.report.pn if hasattr(result.report, 'pn') else 'N/A'}")
            print(f"  Serial Number: {result.report.sn if hasattr(result.report, 'sn') else 'N/A'}")
            print(f"  Result: {result.report.result if hasattr(result.report, 'result') else 'N/A'}")
            print(f"\n✓ WSJF files should now process correctly!")
        else:
            print(f"✗ Conversion failed: {result.error}")
            
    except Exception as e:
        print(f"✗ Exception during conversion: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"✗ File cannot be converted")
