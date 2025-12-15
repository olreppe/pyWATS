"""
Simple CSV Converter Example

This converter demonstrates parsing simple CSV files with test results
and converting them to WATS reports.

Expected CSV format:
    PartNumber,SerialNumber,Result,Station
    PCB-001,SN-12345,Pass,Station1
    PCB-001,SN-12346,Fail,Station1
    
See docs/CONVERTER_ARCHITECTURE.md for full documentation.
"""

from pathlib import Path
from typing import Dict, Any
from pywats_client.converters.base import (
    ConverterBase,
    ConverterResult,
    ConverterArguments,
    FileInfo,
    PostProcessAction,
)


class SimpleCSVConverter(ConverterBase):
    """
    Simple CSV converter for test results.
    
    Converts CSV files with test results to WATS UUT reports.
    Expects CSV format: PartNumber,SerialNumber,Result,Station
    """
    
    def __init__(self, delimiter: str = ",", skip_header: bool = True):
        """
        Initialize CSV converter.
        
        Args:
            delimiter: CSV delimiter character
            skip_header: Whether to skip first row as header
        """
        super().__init__()
        self.delimiter = delimiter
        self.skip_header = skip_header
    
    @property
    def name(self) -> str:
        """Human-readable converter name"""
        return "Simple CSV Converter"
    
    @property
    def version(self) -> str:
        """Converter version"""
        return "1.0.0"
    
    @property
    def description(self) -> str:
        """Description of what this converter does"""
        return "Converts CSV files with test results to WATS UUT reports"
    
    @property
    def supported_extensions(self) -> list[str]:
        """List of file extensions this converter supports"""
        return [".csv", ".txt"]
    
    @property
    def supported_mime_types(self) -> list[str]:
        """List of MIME types this converter supports"""
        return ["text/csv", "text/plain"]
    
    def validate_file(self, file_info: FileInfo) -> tuple[bool, str]:
        """
        Validate CSV file before conversion.
        
        Args:
            file_info: Information about the file
            
        Returns:
            Tuple of (is_valid, reason_if_invalid)
        """
        # Call base validation (checks extension and MIME type)
        valid, reason = super().validate_file(file_info)
        if not valid:
            return False, reason
        
        # Check file size
        max_size = 5 * 1024 * 1024  # 5 MB
        if file_info.size > max_size:
            return False, f"File exceeds {max_size} bytes limit"
        
        if file_info.size < 10:
            return False, "File too small, likely empty"
        
        # Quick check: try to read first line to verify it's text
        try:
            with open(file_info.path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if not first_line.strip():
                    return False, "File appears to be empty"
        except Exception as e:
            return False, f"Cannot read file: {e}"
        
        return True, ""
    
    def convert_file(
        self,
        file_path: Path,
        args: ConverterArguments
    ) -> ConverterResult:
        """
        Convert CSV file to WATS report.
        
        Args:
            file_path: Path to the CSV file to convert
            args: ConverterArguments with API client, file info, folders, settings
            
        Returns:
            ConverterResult with status and report data
        """
        try:
            # Access converter arguments
            api = args.api_client
            file_info = args.file_info
            settings = args.user_settings
            
            # Get settings
            delimiter = settings.get("delimiter", self.delimiter)
            skip_header = settings.get("skip_header", self.skip_header)
            encoding = settings.get("encoding", "utf-8")
            
            # Read CSV file
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            
            if not lines:
                return ConverterResult.failed_result(
                    error="CSV file is empty"
                )
            
            # Skip header if configured
            data_lines = lines[1:] if skip_header and len(lines) > 1 else lines
            
            if not data_lines:
                return ConverterResult.failed_result(
                    error="No data rows found in CSV"
                )
            
            # Parse first data row
            # Expected format: PartNumber,SerialNumber,Result,Station
            row = data_lines[0].strip().split(delimiter)
            
            if len(row) < 3:
                return ConverterResult.failed_result(
                    error=f"Insufficient columns in CSV. Expected at least 3, got {len(row)}"
                )
            
            # Extract fields (we've already validated len(row) >= 3)
            part_number = row[0].strip()
            serial_number = row[1].strip()
            result = row[2].strip()
            station = row[3].strip() if len(row) > 3 else settings.get("default_station", "TestStation")
            
            # Check if conversion should be suspended
            if not serial_number:
                return ConverterResult.suspended_result(
                    reason="No serial number found in CSV, waiting for complete data"
                )
            
            # Parse result
            test_result = "Passed" if result.lower() in ["pass", "passed", "p", "ok", "1"] else "Failed"
            
            # Create WATS report structure
            report = {
                "type": "UUT",
                "serialNumber": serial_number,
                "partNumber": part_number or settings.get("default_part", "UNKNOWN"),
                "result": test_result,
                "processCode": settings.get("process_code", 10),
                "stationName": station,
            }
            
            # Determine post-processing action from settings
            post_action_str = settings.get("post_action", "move")
            post_action = {
                "delete": PostProcessAction.DELETE,
                "move": PostProcessAction.MOVE,
                "zip": PostProcessAction.ZIP,
                "keep": PostProcessAction.KEEP
            }.get(post_action_str.lower(), PostProcessAction.MOVE)
            
            # Return success
            return ConverterResult.success_result(
                report=report,
                post_action=post_action,
                metadata={
                    "source_file": file_info.name,
                    "file_size": file_info.size,
                    "rows_in_file": len(data_lines),
                }
            )
        
        except UnicodeDecodeError as e:
            return ConverterResult.failed_result(
                error=f"Encoding error: {e}. Try different encoding."
            )
        
        except Exception as e:
            return ConverterResult.failed_result(
                error=f"CSV conversion error: {str(e)}"
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
            f"Successfully converted CSV {file_path.name}: "
            f"SN={result.report['serialNumber']}, "
            f"Result={result.report['result']}"
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
        logger.error(f"Failed to convert CSV {file_path.name}: {result.error}")
    
    def get_arguments(self) -> Dict[str, Any]:
        """Define configurable arguments for this converter"""
        return {
            "delimiter": {
                "type": "string",
                "default": ",",
                "description": "CSV delimiter character",
                "required": False
            },
            "encoding": {
                "type": "choice",
                "default": "utf-8",
                "choices": ["utf-8", "latin-1", "ascii", "utf-16"],
                "description": "File encoding"
            },
            "skip_header": {
                "type": "bool",
                "default": True,
                "description": "Skip first row as header"
            },
            "default_station": {
                "type": "string",
                "default": "TestStation",
                "description": "Default station name if not in CSV"
            },
            "default_part": {
                "type": "string",
                "default": "UNKNOWN",
                "description": "Default part number if not found in CSV"
            },
            "process_code": {
                "type": "int",
                "default": 10,
                "description": "Process code for reports",
                "min": 1,
                "max": 999
            },
            "post_action": {
                "type": "choice",
                "default": "move",
                "choices": ["delete", "move", "zip", "keep"],
                "description": "Post-processing action after successful conversion"
            },
        }
