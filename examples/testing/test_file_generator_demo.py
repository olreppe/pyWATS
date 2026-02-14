"""
Demo script showing how to use test file generators.

This script demonstrates the capabilities of the TestFileGenerator class
and is useful for validating the generators work correctly.

Run with: python -m examples.testing.test_file_generator_demo
"""

from pathlib import Path
import tempfile
import shutil
from tests.fixtures.test_file_generators import TestFileGenerator


def demo_single_file_generation(output_dir: Path):
    """Demo generating individual files."""
    print("\n" + "="*70)
    print("DEMO 1: Single File Generation")
    print("="*70)
    
    # Generate CSV file
    csv_file = TestFileGenerator.generate_csv_file(
        output_dir / "sample.csv",
        rows=100,
        include_header=True
    )
    print(f"✓ Generated CSV: {csv_file} ({csv_file.stat().st_size} bytes)")
    
    # Generate XML file
    xml_file = TestFileGenerator.generate_xml_file(
        output_dir / "sample.xml",
        test_steps=10,
        serial_number="SN123456",
        pass_fail="PASS"
    )
    print(f"✓ Generated XML: {xml_file} ({xml_file.stat().st_size} bytes)")
    
    # Generate TXT file
    txt_file = TestFileGenerator.generate_txt_file(
        output_dir / "sample.txt",
        size_kb=10,
        content_type='log'
    )
    print(f"✓ Generated TXT: {txt_file} ({txt_file.stat().st_size} bytes)")
    
    # Generate JSON file
    json_file = TestFileGenerator.generate_json_file(
        output_dir / "sample.json",
        uut_count=1,
        steps_per_uut=10
    )
    print(f"✓ Generated JSON: {json_file} ({json_file.stat().st_size} bytes)")


def demo_batch_generation(output_dir: Path):
    """Demo generating batches of files."""
    print("\n" + "="*70)
    print("DEMO 2: Batch Generation")
    print("="*70)
    
    batch_dir = output_dir / "batch"
    
    # Generate 100 CSV files
    print("\nGenerating 100 CSV files...", end=" ", flush=True)
    csv_files = TestFileGenerator.generate_batch(
        batch_dir / "csv",
        'csv',
        count=100,
        rows=50
    )
    print(f"✓ {len(csv_files)} files created")
    
    # Generate 50 XML files
    print("Generating 50 XML files...", end=" ", flush=True)
    xml_files = TestFileGenerator.generate_batch(
        batch_dir / "xml",
        'xml',
        count=50,
        test_steps=10
    )
    print(f"✓ {len(xml_files)} files created")


def demo_mixed_batch(output_dir: Path):
    """Demo generating mixed batches."""
    print("\n" + "="*70)
    print("DEMO 3: Mixed Batch Generation")
    print("="*70)
    
    mixed_dir = output_dir / "mixed"
    
    print("\nGenerating mixed batch (CSV: 100, XML: 50, TXT: 25)...")
    files = TestFileGenerator.generate_mixed_batch(
        mixed_dir,
        {'csv': 100, 'xml': 50, 'txt': 25}
    )
    
    for file_type, file_list in files.items():
        total_size = sum(f.stat().st_size for f in file_list)
        print(f"  ✓ {file_type.upper()}: {len(file_list)} files, {total_size:,} bytes total")


def demo_corrupted_files(output_dir: Path):
    """Demo generating corrupted/malformed files for error testing."""
    print("\n" + "="*70)
    print("DEMO 4: Corrupted/Malformed Files")
    print("="*70)
    
    corrupt_dir = output_dir / "corrupted"
    
    # Corrupted CSV
    corrupt_csv = TestFileGenerator.generate_csv_file(
        corrupt_dir / "corrupt.csv",
        rows=100,
        corrupt=True
    )
    print(f"✓ Generated corrupted CSV: {corrupt_csv.name}")
    print("  (Contains missing fields and invalid data)")
    
    # Malformed XML
    malformed_xml = TestFileGenerator.generate_xml_file(
        corrupt_dir / "malformed.xml",
        test_steps=5,
        malformed=True
    )
    print(f"✓ Generated malformed XML: {malformed_xml.name}")
    print("  (Missing closing tags - will fail parsing)")
    
    # Malformed JSON
    malformed_json = TestFileGenerator.generate_json_file(
        corrupt_dir / "malformed.json",
        uut_count=1,
        malformed=True
    )
    print(f"✓ Generated malformed JSON: {malformed_json.name}")
    print("  (Missing closing braces - will fail parsing)")


def demo_stress_test_files(output_dir: Path):
    """Demo generating large number of files for stress testing."""
    print("\n" + "="*70)
    print("DEMO 5: Stress Test File Generation")
    print("="*70)
    
    stress_dir = output_dir / "stress"
    
    print("\nGenerating 1000 small CSV files for stress testing...")
    print("(This simulates dropping 1000 files into watch folder)")
    
    import time
    start = time.time()
    
    files = TestFileGenerator.generate_batch(
        stress_dir,
        'csv',
        count=1000,
        rows=10  # Small files for speed
    )
    
    elapsed = time.time() - start
    
    total_size = sum(f.stat().st_size for f in files)
    avg_size = total_size / len(files)
    
    print(f"\n✓ Generated {len(files)} files in {elapsed:.2f} seconds")
    print(f"  Rate: {len(files)/elapsed:.0f} files/second")
    print(f"  Total size: {total_size:,} bytes")
    print(f"  Average size: {avg_size:.0f} bytes/file")


def main():
    """Run all demos."""
    print("\n" + "="*70)
    print("TEST FILE GENERATOR DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows the capabilities of the TestFileGenerator class.")
    print("Files will be created in a temporary directory and cleaned up after.")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir) / "demo_output"
        output_dir.mkdir()
        
        # Run demos
        demo_single_file_generation(output_dir)
        demo_batch_generation(output_dir)
        demo_mixed_batch(output_dir)
        demo_corrupted_files(output_dir)
        demo_stress_test_files(output_dir)
        
        # Summary
        print("\n" + "="*70)
        print("DEMO COMPLETE")
        print("="*70)
        
        # Count total files
        all_files = list(output_dir.rglob("*"))
        file_count = len([f for f in all_files if f.is_file()])
        total_size = sum(f.stat().st_size for f in all_files if f.is_file())
        
        print(f"\nTotal files generated: {file_count:,}")
        print(f"Total size: {total_size:,} bytes ({total_size/(1024*1024):.2f} MB)")
        print("\nAll files were created in a temporary directory and will be")
        print("automatically cleaned up when this script exits.")
        
        print("\n" + "="*70)
        print("USAGE IN TESTS")
        print("="*70)
        print("""
Example test using generators:

    def test_converter_with_100_files(watch_dir):
        # Generate 100 test files
        files = TestFileGenerator.generate_batch(
            watch_dir,
            'csv',
            count=100,
            rows=50
        )
        
        # Start converter watching the folder
        converter = FileConverter(watch_dir, ...)
        
        # Verify all files are processed
        assert converter.get_processed_count() == 100

Example using pytest fixtures:

    def test_with_csv_file(test_csv_file):
        # test_csv_file fixture provides a pre-generated CSV
        assert test_csv_file.exists()
        
    def test_with_csv_files(test_csv_files):
        # test_csv_files fixture provides 10 pre-generated CSVs
        assert len(test_csv_files) == 10
        
    def test_stress(stress_file_set):
        # stress_file_set fixture provides 1000 pre-generated files
        assert len(stress_file_set) == 1000
        """)


if __name__ == "__main__":
    main()
