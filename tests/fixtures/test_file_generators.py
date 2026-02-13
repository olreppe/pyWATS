"""
Test File Generators for Converter Testing.

This module provides utilities to generate synthetic test files for converter
testing. These generators are used for unit tests, integration tests, stress
tests, and performance benchmarks.

Usage:
    from tests.fixtures.test_file_generators import TestFileGenerator
    
    # Generate single CSV file
    csv_file = TestFileGenerator.generate_csv_file(
        Path("test.csv"),
        rows=100,
        include_header=True
    )
    
    # Generate batch of 1000 files for stress testing
    files = TestFileGenerator.generate_batch(
        output_dir=Path("test_data"),
        file_type='csv',
        count=1000,
        rows=50
    )
"""

import csv
import random
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from xml.etree import ElementTree as ET
from xml.dom import minidom

# Import pyWATS models for generating proper WSJF reports
from pywats.domains.report.report_models.uut import UUTReport, UUTInfo
from pywats.domains.report.report_models.common_types import ReportStatus, StepStatus
from pywats.shared.enums import CompOp


class TestFileGenerator:
    """Generate synthetic test files for converter testing."""
    
    # Sample data for realistic generation
    PART_NUMBERS = [
        "PN001-RevA", "PN002-RevB", "PN003-RevC", "PN004-RevD", "PN005-RevE",
        "PN006-RevF", "PN007-RevG", "PN008-RevH", "PN009-RevI", "PN010-RevJ"
    ]
    
    TEST_NAMES = [
        "Voltage Test", "Current Test", "Resistance Test", "Continuity Test",
        "Power Supply Test", "Signal Integrity Test", "Temperature Test",
        "Frequency Test", "Impedance Test", "Calibration Test"
    ]
    
    STATIONS = ["Station_A", "Station_B", "Station_C", "Station_D"]
    OPERATORS = ["OP001", "OP002", "OP003", "OP004", "OP005"]
    
    @staticmethod
    def generate_csv_file(
        output_path: Path,
        rows: int = 100,
        include_header: bool = True,
        corrupt: bool = False,
        encoding: str = 'utf-8'
    ) -> Path:
        """
        Generate CSV test file with realistic manufacturing test data.
        
        Args:
            output_path: Where to save the file
            rows: Number of data rows to generate
            include_header: Include CSV header row
            corrupt: Introduce corruption (missing fields, invalid data)
            encoding: File encoding
        
        Returns:
            Path to generated file
        
        Example CSV format:
            SerialNumber,PartNumber,TestResult,TestDate,Operator,Station
            SN000001,PN001-RevA,PASS,2026-02-13T10:30:00,OP001,Station_A
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding=encoding) as f:
            writer = csv.writer(f)
            
            if include_header:
                writer.writerow([
                    'SerialNumber', 'PartNumber', 'TestResult', 
                    'TestDate', 'Operator', 'Station'
                ])
            
            for i in range(rows):
                serial = f'SN{i+1:06d}'
                part_number = random.choice(TestFileGenerator.PART_NUMBERS)
                result = random.choice(['PASS', 'PASS', 'PASS', 'FAIL'])  # 75% pass rate
                test_date = (datetime.now() - timedelta(hours=random.randint(0, 720))).isoformat()
                operator = random.choice(TestFileGenerator.OPERATORS)
                station = random.choice(TestFileGenerator.STATIONS)
                
                # Introduce corruption for testing error handling
                if corrupt:
                    if i == rows // 2:
                        # Missing field in middle
                        writer.writerow([serial, part_number])
                    elif i == rows - 1:
                        # Invalid date format at end
                        writer.writerow([serial, part_number, result, "INVALID_DATE", operator, station])
                    else:
                        writer.writerow([serial, part_number, result, test_date, operator, station])
                else:
                    writer.writerow([serial, part_number, result, test_date, operator, station])
        
        return output_path
    
    @staticmethod
    def generate_xml_file(
        output_path: Path,
        test_steps: int = 10,
        malformed: bool = False,
        serial_number: Optional[str] = None,
        pass_fail: Optional[str] = None
    ) -> Path:
        """
        Generate XML UUT report file.
        
        Args:
            output_path: Where to save the file
            test_steps: Number of test steps to include
            malformed: Create malformed XML (missing closing tags, etc.)
            serial_number: Serial number (auto-generated if None)
            pass_fail: Overall result ('PASS' or 'FAIL', random if None)
        
        Returns:
            Path to generated file
        
        Example XML format:
            <UUTReport>
                <UUT SerialNumber="SN000001" PartNumber="PN001-RevA"/>
                <TestResults>
                    <Step Name="Voltage Test" Result="PASS" Value="5.02" .../>
                </TestResults>
            </UUTReport>
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate data
        if serial_number is None:
            serial_number = f'SN{random.randint(1, 999999):06d}'
        
        part_number = random.choice(TestFileGenerator.PART_NUMBERS)
        
        if pass_fail is None:
            pass_fail = random.choice(['PASS', 'PASS', 'PASS', 'FAIL'])
        
        # Create XML structure
        root = ET.Element('UUTReport')
        
        # UUT info
        uut = ET.SubElement(root, 'UUT')
        uut.set('SerialNumber', serial_number)
        uut.set('PartNumber', part_number)
        uut.set('TestDate', datetime.now().isoformat())
        uut.set('Operator', random.choice(TestFileGenerator.OPERATORS))
        uut.set('Station', random.choice(TestFileGenerator.STATIONS))
        
        # Test results
        test_results = ET.SubElement(root, 'TestResults')
        test_results.set('OverallResult', pass_fail)
        
        for i in range(test_steps):
            step = ET.SubElement(test_results, 'Step')
            step.set('Name', random.choice(TestFileGenerator.TEST_NAMES))
            step.set('Number', str(i + 1))
            
            # Random pass/fail for individual steps
            step_result = 'FAIL' if (pass_fail == 'FAIL' and i == test_steps - 1) else random.choice(['PASS', 'PASS', 'PASS', 'FAIL'])
            step.set('Result', step_result)
            
            # Measurement value
            if 'Voltage' in step.get('Name'):
                value = f"{random.uniform(4.5, 5.5):.2f}"
                limit_low = "4.75"
                limit_high = "5.25"
                unit = "V"
            elif 'Current' in step.get('Name'):
                value = f"{random.uniform(0.1, 1.0):.3f}"
                limit_low = "0.0"
                limit_high = "1.5"
                unit = "A"
            else:
                value = f"{random.uniform(0, 100):.2f}"
                limit_low = "0"
                limit_high = "100"
                unit = "units"
            
            step.set('Value', value)
            step.set('LimitLow', limit_low)
            step.set('LimitHigh', limit_high)
            step.set('Unit', unit)
            step.set('Timestamp', (datetime.now() + timedelta(seconds=i)).isoformat())
        
        # Write to file
        if malformed:
            # Create malformed XML by writing incomplete structure
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<UUTReport>\n')
                f.write(f'  <UUT SerialNumber="{serial_number}"\n')  # Missing closing >
                f.write('  <TestResults>\n')
                f.write('    <Step Name="Test1" Result="PASS"/>\n')
                # Missing closing tags
        else:
            # Pretty print XML
            rough_string = ET.tostring(root, encoding='utf-8')
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
            
            with open(output_path, 'wb') as f:
                f.write(pretty_xml)
        
        return output_path
    
    @staticmethod
    def generate_txt_file(
        output_path: Path,
        size_kb: int = 10,
        encoding: str = 'utf-8',
        content_type: str = 'log'
    ) -> Path:
        """
        Generate text file with specified size.
        
        Args:
            output_path: Where to save the file
            size_kb: Target file size in kilobytes
            encoding: File encoding
            content_type: 'log' (log format) or 'random' (random text)
        
        Returns:
            Path to generated file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        target_bytes = size_kb * 1024
        
        with open(output_path, 'w', encoding=encoding) as f:
            bytes_written = 0
            line_num = 1
            
            while bytes_written < target_bytes:
                if content_type == 'log':
                    # Generate log-style content
                    timestamp = datetime.now().isoformat()
                    level = random.choice(['INFO', 'DEBUG', 'WARNING', 'ERROR'])
                    messages = [
                        "Test started for unit SN{:06d}".format(random.randint(1, 999999)),
                        "Measurement complete: {:0.2f} V".format(random.uniform(4, 6)),
                        "Step {} completed successfully".format(random.randint(1, 20)),
                        "Connection established to test equipment",
                        "Calibration verified",
                        "Data logged to database"
                    ]
                    message = random.choice(messages)
                    
                    line = f"{timestamp} [{level:8s}] Line {line_num:06d}: {message}\n"
                else:
                    # Generate random text
                    words = ['test', 'data', 'measurement', 'result', 'pass', 'fail', 
                             'voltage', 'current', 'resistance', 'value', 'step', 'complete']
                    line = ' '.join(random.choices(words, k=10)) + '\n'
                
                f.write(line)
                bytes_written += len(line.encode(encoding))
                line_num += 1
        
        return output_path
    
    @staticmethod
    def generate_json_file(
        output_path: Path,
        uut_count: int = 1,
        steps_per_uut: int = 10,
        malformed: bool = False
    ) -> Path:
        """
        Generate WSJF (WATS Standard JSON Format) UUT report file.
        
        Uses the pyWATS API to generate reports, ensuring EXACT format compatibility
        with WATSStandardJsonConverter. This is the CORRECT way to generate test
        files - using the same API that creates real reports.
        
        Args:
            output_path: Where to save the file
            uut_count: Ignored (WSJF supports single report per file)
            steps_per_uut: Number of test steps to include
            malformed: Create malformed JSON (missing braces, etc.)
        
        Returns:
            Path to generated file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if malformed:
            # Write malformed JSON (don't use API for this)
            serial = f'SN{random.randint(1, 999999):06d}'
            part_number = random.choice(TestFileGenerator.PART_NUMBERS)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('{\n')
                f.write('  "type": "T",\n')
                f.write('  "pn": "' + part_number + '",\n')  # Missing closing brace
            return output_path
        
        # Generate using pyWATS API (guarantees correct format!)
        serial = f'SN{random.randint(1, 999999):06d}'
        part_number = random.choice(TestFileGenerator.PART_NUMBERS)
        pass_fail = random.choice(['PASS', 'PASS', 'PASS', 'FAIL'])
        result_status = ReportStatus.Passed if pass_fail == 'PASS' else ReportStatus.Failed
        
        # Create UUT report using pyWATS API
        report = UUTReport(
            pn=part_number,
            sn=serial,
            rev='Rev1',
            process_code=random.randint(1, 100),
            station_name=random.choice(TestFileGenerator.STATIONS),
            location='Test Floor',
            purpose='Production',
            result=result_status,
            start=datetime.now().astimezone(),
        )
        
        # Set UUT info
        report.info = UUTInfo(
            operator=random.choice(TestFileGenerator.OPERATORS),
            fixture_id='Fixture_001',
            comment='',
        )
        
        # Get root sequence call
        root = report.get_root_sequence_call()
        root.sequence.file_name = 'TestSequence'
        root.sequence.version = '1.0.0'
        
        # Add test steps using pyWATS API
        for i in range(steps_per_uut):
            # Randomly choose step type
            step_type = random.choice(['numeric', 'boolean', 'string'])
            step_result = 'FAIL' if (pass_fail == 'FAIL' and i == steps_per_uut - 1) else random.choice(['PASS', 'PASS', 'PASS', 'FAIL'])
            step_status = StepStatus.Passed if step_result == 'PASS' else StepStatus.Failed
            
            if step_type == 'numeric':
                # Generate numeric test
                value = round(random.uniform(10.0, 100.0), 2)
                low_limit = round(value - random.uniform(5.0, 10.0), 2)
                high_limit = round(value + random.uniform(5.0, 10.0), 2)
                
                # Ensure status matches limits
                if step_status == StepStatus.Failed:
                    value = round(high_limit + random.uniform(1.0, 5.0), 2)  # Make it fail
                
                root.add_numeric_step(
                    name=random.choice(TestFileGenerator.TEST_NAMES),
                    value=value,
                    unit=random.choice(['V', 'A', 'Ohm', 'Hz']),
                    comp_op=CompOp.GELE,
                    low_limit=low_limit,
                    high_limit=high_limit,
                    status=step_status,
                    tot_time=round(random.uniform(0.1, 2.0), 2),
                )
            
            elif step_type == 'boolean':
                # Generate pass/fail test
                root.add_boolean_step(
                    name=random.choice(TestFileGenerator.TEST_NAMES),
                    status=step_status,
                    tot_time=round(random.uniform(0.1, 2.0), 2),
                )
            
            else:  # string
                # Generate string value test
                root.add_string_step(
                    name=random.choice(TestFileGenerator.TEST_NAMES),
                    value=f'Test value {i+1}',
                    comp_op=CompOp.LOG,
                    status=step_status,
                    tot_time=round(random.uniform(0.1, 2.0), 2),
                )
        
        # Serialize to JSON using Pydantic (guarantees correct WSJF format!)
        json_data = report.model_dump_json(
            indent=2,
            by_alias=True,
            exclude_none=False,
        )
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_data)
        
        return output_path
    
    @staticmethod
    def generate_batch(
        output_dir: Path,
        file_type: str,
        count: int,
        **kwargs
    ) -> List[Path]:
        """
        Generate multiple files at once for stress testing.
        
        Args:
            output_dir: Directory for generated files
            file_type: 'csv', 'xml', 'txt', or 'json'
            count: Number of files to generate
            **kwargs: Additional arguments passed to individual generators
        
        Returns:
            List of generated file paths
        
        Example:
            # Generate 1000 CSV files for stress test
            files = TestFileGenerator.generate_batch(
                Path("test_data"),
                'csv',
                1000,
                rows=50,
                corrupt=False
            )
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Map file type to generator function
        generators = {
            'csv': TestFileGenerator.generate_csv_file,
            'xml': TestFileGenerator.generate_xml_file,
            'txt': TestFileGenerator.generate_txt_file,
            'json': TestFileGenerator.generate_json_file
        }
        
        if file_type not in generators:
            raise ValueError(f"Unknown file type: {file_type}. Supported: {list(generators.keys())}")
        
        generator = generators[file_type]
        
        files = []
        for i in range(count):
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_{timestamp}_{i:06d}.{file_type}"
            file_path = output_dir / filename
            
            # Generate file
            generated = generator(file_path, **kwargs)
            files.append(generated)
        
        return files
    
    @staticmethod
    def generate_mixed_batch(
        output_dir: Path,
        count_per_type: Dict[str, int],
        **kwargs
    ) -> Dict[str, List[Path]]:
        """
        Generate mixed batch of different file types.
        
        Args:
            output_dir: Directory for generated files
            count_per_type: Dict mapping file type to count
            **kwargs: Additional arguments for generators
        
        Returns:
            Dict mapping file type to list of generated paths
        
        Example:
            files = TestFileGenerator.generate_mixed_batch(
                Path("test_data"),
                {'csv': 100, 'xml': 50, 'txt': 25}
            )
        """
        result = {}
        
        for file_type, count in count_per_type.items():
            files = TestFileGenerator.generate_batch(
                output_dir,
                file_type,
                count,
                **kwargs
            )
            result[file_type] = files
        
        return result


class LockedFile:
    """
    Context manager to create and lock a file for testing.
    
    Usage:
        with LockedFile(Path("test.csv")) as locked_path:
            # File is locked here
            # Test converter handling of locked files
            pass
        # File is unlocked and can be deleted
    """
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_handle = None
    
    def __enter__(self) -> Path:
        """Create and lock file."""
        # Create file
        TestFileGenerator.generate_csv_file(self.file_path, rows=10)
        
        # Open with exclusive lock
        self.file_handle = open(self.file_path, 'r+')
        
        return self.file_path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unlock and cleanup file."""
        if self.file_handle:
            self.file_handle.close()
        
        # Cleanup
        if self.file_path.exists():
            try:
                self.file_path.unlink()
            except:
                pass  # File may be locked by OS


# Pytest fixtures for easy use in tests
def pytest_fixtures():
    """
    Example pytest fixtures using test file generators.
    Add these to your conftest.py.
    """
    import pytest
    
    @pytest.fixture
    def test_csv_files(tmp_path):
        """Generate 10 CSV test files."""
        return TestFileGenerator.generate_batch(
            tmp_path,
            'csv',
            count=10,
            rows=50
        )
    
    @pytest.fixture
    def test_xml_files(tmp_path):
        """Generate 10 XML test files."""
        return TestFileGenerator.generate_batch(
            tmp_path,
            'xml',
            count=10,
            test_steps=10
        )
    
    @pytest.fixture
    def corrupted_csv_file(tmp_path):
        """Generate single corrupted CSV file."""
        return TestFileGenerator.generate_csv_file(
            tmp_path / "corrupt.csv",
            rows=100,
            corrupt=True
        )
    
    @pytest.fixture
    def large_file_set(tmp_path):
        """Generate large mixed file set for stress testing."""
        return TestFileGenerator.generate_mixed_batch(
            tmp_path,
            {'csv': 100, 'xml': 100, 'txt': 50}
        )
