"""
Unit tests for test file generators.

This module tests the TestFileGenerator class to ensure it creates
valid test files with the expected properties.
"""

import pytest
from pathlib import Path
import csv
import json
from xml.etree import ElementTree as ET

from tests.fixtures.test_file_generators import TestFileGenerator, LockedFile


class TestCSVGeneration:
    """Tests for CSV file generation."""
    
    def test_generate_csv_file(self, temp_dir):
        """Test basic CSV file generation."""
        csv_file = TestFileGenerator.generate_csv_file(
            temp_dir / "test.csv",
            rows=100,
            include_header=True
        )
        
        # Verify file exists
        assert csv_file.exists()
        
        # Verify content
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Should have header + 100 data rows
        assert len(rows) == 101
        
        # Verify header
        assert rows[0] == ['SerialNumber', 'PartNumber', 'TestResult', 'TestDate', 'Operator', 'Station']
        
        # Verify first data row has correct columns
        assert len(rows[1]) == 6
        assert rows[1][0].startswith('SN')
        assert rows[1][2] in ['PASS', 'FAIL']
    
    def test_csv_without_header(self, temp_dir):
        """Test CSV generation without header."""
        csv_file = TestFileGenerator.generate_csv_file(
            temp_dir / "test.csv",
            rows=10,
            include_header=False
        )
        
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Should have only 10 rows (no header)
        assert len(rows) == 10
        
        # First row should be data, not header
        assert rows[0][0].startswith('SN')
    
    def test_corrupted_csv(self, temp_dir):
        """Test corrupted CSV file generation."""
        csv_file = TestFileGenerator.generate_csv_file(
            temp_dir / "corrupt.csv",
            rows=100,
            corrupt=True
        )
        
        assert csv_file.exists()
        
        # Verify file has corrupted content
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Should have some rows with incorrect number of fields
        field_counts = [len(row) for row in rows[1:]]  # Skip header
        assert min(field_counts) < 6 or max(field_counts) > 6


class TestXMLGeneration:
    """Tests for XML file generation."""
    
    def test_generate_xml_file(self, temp_dir):
        """Test basic XML file generation."""
        xml_file = TestFileGenerator.generate_xml_file(
            temp_dir / "test.xml",
            test_steps=10
        )
        
        # Verify file exists
        assert xml_file.exists()
        
        # Parse and verify structure
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Verify root element
        assert root.tag == 'UUTReport'
        
        # Verify UUT info
        uut = root.find('UUT')
        assert uut is not None
        assert 'SerialNumber' in uut.attrib
        assert 'PartNumber' in uut.attrib
        
        # Verify test results
        test_results = root.find('TestResults')
        assert test_results is not None
        assert 'OverallResult' in test_results.attrib
        
        # Verify test steps
        steps = test_results.findall('Step')
        assert len(steps) == 10
        
        # Verify step attributes
        step = steps[0]
        assert 'Name' in step.attrib
        assert 'Result' in step.attrib
        assert 'Value' in step.attrib
    
    def test_xml_with_specific_serial(self, temp_dir):
        """Test XML generation with specific serial number."""
        xml_file = TestFileGenerator.generate_xml_file(
            temp_dir / "test.xml",
            test_steps=5,
            serial_number="SN123456"
        )
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        uut = root.find('UUT')
        
        assert uut.get('SerialNumber') == 'SN123456'
    
    def test_xml_with_specific_result(self, temp_dir):
        """Test XML generation with specific pass/fail result."""
        xml_file = TestFileGenerator.generate_xml_file(
            temp_dir / "test.xml",
            test_steps=5,
            pass_fail='FAIL'
        )
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        test_results = root.find('TestResults')
        
        assert test_results.get('OverallResult') == 'FAIL'
    
    def test_malformed_xml(self, temp_dir):
        """Test malformed XML generation."""
        xml_file = TestFileGenerator.generate_xml_file(
            temp_dir / "malformed.xml",
            test_steps=5,
            malformed=True
        )
        
        assert xml_file.exists()
        
        # Should raise exception when parsing
        with pytest.raises(ET.ParseError):
            ET.parse(xml_file)


class TestTXTGeneration:
    """Tests for TXT file generation."""
    
    def test_generate_txt_file(self, temp_dir):
        """Test basic TXT file generation."""
        txt_file = TestFileGenerator.generate_txt_file(
            temp_dir / "test.txt",
            size_kb=10
        )
        
        # Verify file exists
        assert txt_file.exists()
        
        # Verify size approximately correct (within 10%)
        file_size = txt_file.stat().st_size
        target_size = 10 * 1024
        assert abs(file_size - target_size) / target_size < 0.1
    
    def test_txt_log_format(self, temp_dir):
        """Test TXT file with log format."""
        txt_file = TestFileGenerator.generate_txt_file(
            temp_dir / "test.txt",
            size_kb=5,
            content_type='log'
        )
        
        # Read content and verify log format
        with open(txt_file, 'r') as f:
            lines = f.readlines()
        
        # Should have timestamp prefix
        assert '[INFO' in lines[0] or '[DEBUG' in lines[0] or '[WARNING' in lines[0] or '[ERROR' in lines[0]
    
    def test_txt_random_format(self, temp_dir):
        """Test TXT file with random text."""
        txt_file = TestFileGenerator.generate_txt_file(
            temp_dir / "test.txt",
            size_kb=2,
            content_type='random'
        )
        
        # Read content
        with open(txt_file, 'r') as f:
            content = f.read()
        
        # Should contain random words
        assert len(content) > 0


class TestJSONGeneration:
    """Tests for JSON file generation."""
    
    def test_generate_json_file(self, temp_dir):
        """Test basic JSON file generation."""
        json_file = TestFileGenerator.generate_json_file(
            temp_dir / "test.json",
            uut_count=1,
            steps_per_uut=10
        )
        
        # Verify file exists
        assert json_file.exists()
        
        # Parse and verify structure
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Verify structure
        assert 'reports' in data
        assert len(data['reports']) == 1
        
        report = data['reports'][0]
        assert 'serial_number' in report
        assert 'part_number' in report
        assert 'overall_result' in report
        assert 'test_steps' in report
        assert len(report['test_steps']) == 10
    
    def test_json_multiple_uuts(self, temp_dir):
        """Test JSON generation with multiple UUTs."""
        json_file = TestFileGenerator.generate_json_file(
            temp_dir / "test.json",
            uut_count=5,
            steps_per_uut=5
        )
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        assert len(data['reports']) == 5
        
        # Each should have 5 steps
        for report in data['reports']:
            assert len(report['test_steps']) == 5
    
    def test_malformed_json(self, temp_dir):
        """Test malformed JSON generation."""
        json_file = TestFileGenerator.generate_json_file(
            temp_dir / "malformed.json",
            uut_count=1,
            malformed=True
        )
        
        assert json_file.exists()
        
        # Should raise exception when parsing
        with pytest.raises(json.JSONDecodeError):
            with open(json_file, 'r') as f:
                json.load(f)


class TestBatchGeneration:
    """Tests for batch file generation."""
    
    def test_generate_batch(self, temp_dir):
        """Test batch generation."""
        files = TestFileGenerator.generate_batch(
            temp_dir,
            'csv',
            count=10,
            rows=50
        )
        
        # Verify count
        assert len(files) == 10
        
        # Verify all exist
        for file_path in files:
            assert file_path.exists()
            assert file_path.suffix == '.csv'
    
    def test_generate_mixed_batch(self, temp_dir):
        """Test mixed batch generation."""
        files = TestFileGenerator.generate_mixed_batch(
            temp_dir,
            {'csv': 5, 'xml': 3, 'txt': 2}
        )
        
        # Verify types
        assert 'csv' in files
        assert 'xml' in files
        assert 'txt' in files
        
        # Verify counts
        assert len(files['csv']) == 5
        assert len(files['xml']) == 3
        assert len(files['txt']) == 2
        
        # Verify all exist
        for file_type, file_list in files.items():
            for file_path in file_list:
                assert file_path.exists()
    
    @pytest.mark.slow
    def test_large_batch_generation(self, temp_dir):
        """Test generating 1000 files (stress test)."""
        files = TestFileGenerator.generate_batch(
            temp_dir,
            'csv',
            count=1000,
            rows=10
        )
        
        # Verify count
        assert len(files) == 1000
        
        # Verify first and last exist
        assert files[0].exists()
        assert files[-1].exists()


class TestLockedFile:
    """Tests for LockedFile context manager."""
    
    def test_locked_file_context(self, temp_dir):
        """Test LockedFile context manager."""
        test_path = temp_dir / "locked.csv"
        
        with LockedFile(test_path) as locked_path:
            # File should exist
            assert locked_path.exists()
            
            # File should be locked (this is OS-dependent)
            # On Windows, trying to open with exclusive access should fail
            # On Unix, file locking is advisory
        
        # After context, file may or may not exist (depends on cleanup)
        # This is OK - the purpose is to test locking behavior


class TestFixtures:
    """Test the pytest fixtures work correctly."""
    
    def test_test_csv_file_fixture(self, test_csv_file):
        """Test test_csv_file fixture."""
        assert test_csv_file.exists()
        assert test_csv_file.suffix == '.csv'
    
    def test_test_csv_files_fixture(self, test_csv_files):
        """Test test_csv_files fixture."""
        assert len(test_csv_files) == 10
        for csv_file in test_csv_files:
            assert csv_file.exists()
    
    def test_test_xml_file_fixture(self, test_xml_file):
        """Test test_xml_file fixture."""
        assert test_xml_file.exists()
        assert test_xml_file.suffix == '.xml'
    
    def test_corrupted_csv_file_fixture(self, corrupted_csv_file):
        """Test corrupted_csv_file fixture."""
        assert corrupted_csv_file.exists()
    
    def test_malformed_xml_file_fixture(self, malformed_xml_file):
        """Test malformed_xml_file fixture."""
        assert malformed_xml_file.exists()
        
        # Should not be parseable
        with pytest.raises(ET.ParseError):
            ET.parse(malformed_xml_file)
    
    def test_large_csv_file_fixture(self, large_csv_file):
        """Test large_csv_file fixture."""
        assert large_csv_file.exists()
        
        # Should have 10,000 rows
        with open(large_csv_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        assert len(rows) == 10001  # Header + 10,000 rows
    
    @pytest.mark.slow
    def test_stress_file_set_fixture(self, stress_file_set):
        """Test stress_file_set fixture."""
        assert len(stress_file_set) == 1000
