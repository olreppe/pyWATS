"""
AOI Converter Example

This converter demonstrates parsing AOI (Automated Optical Inspection) 
log files and converting them to WATS reports.

Example AOI log format:
    BOARD_ID: PCB-12345
    SERIAL: SN-001
    TEST_DATE: 2024-01-01 12:00:00
    RESULT: PASS
    DEFECTS: 0
    
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


class AOIConverter(ConverterBase):
    """
    AOI (Automated Optical Inspection) converter.
    
    Converts AOI log files to WATS UUT reports.
    """
    
    def __init__(self, default_process_code: int = 10):
        """
        Initialize AOI converter.
        
        Args:
            default_process_code: Default process code for reports
        """
        super().__init__()
        self.default_process_code = default_process_code
    
    @property
    def name(self) -> str:
        """Human-readable converter name"""
        return "AOI Converter"
    
    @property
    def version(self) -> str:
        """Converter version"""
        return "1.0.0"
    
    @property
    def description(self) -> str:
        """Description of what this converter does"""
        return "Converts AOI (Automated Optical Inspection) log files to WATS UUT reports"
    
    @property
    def supported_extensions(self) -> list[str]:
        """List of file extensions this converter supports"""
        return [".aoi", ".log", ".txt"]
    
    @property
    def supported_mime_types(self) -> list[str]:
        """List of MIME types this converter supports"""
        return ["text/plain"]
    
    def validate_file(self, file_info: FileInfo) -> tuple[bool, str]:
        """
        Validate AOI file before conversion.
        
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
        max_size = 10 * 1024 * 1024  # 10 MB
        if file_info.size > max_size:
            return False, f"File exceeds {max_size} bytes limit"
        
        if file_info.size < 20:
            return False, "File too small to be valid AOI log"
        
        # Check file signature (AOI files typically start with a header)
        try:
            with open(file_info.path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                # AOI files often start with a specific marker
                if not first_line or len(first_line) < 5:
                    return False, "Invalid AOI file format"
        except Exception as e:
            return False, f"Cannot read file: {e}"
        
        return True, ""
    
    def convert_file(
        self,
        file_path: Path,
        args: ConverterArguments
    ) -> ConverterResult:
        """
        Convert AOI file to WATS report.
        
        Args:
            file_path: Path to the AOI file to convert
            args: ConverterArguments with API client, file info, folders, settings
            
        Returns:
            ConverterResult with status and report data
        """
        try:
            # Access converter arguments
            api = args.api_client
            file_info = args.file_info
            settings = args.user_settings
            
            # Read AOI log file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AOI data
            data = self._parse_aoi_log(content)
            
            # Extract required fields
            serial_number = data.get('serial')
            board_id = data.get('board_id')
            result = data.get('result')
            defect_count = data.get('defects', 0)
            
            # Check if conversion should be suspended
            if not serial_number:
                return ConverterResult.suspended_result(
                    reason="No serial number found in AOI log, waiting for complete data"
                )
            
            # Determine pass/fail based on defects and result
            test_result = "Passed" if result == "PASS" and defect_count == 0 else "Failed"
            
            # Create WATS report structure
            report = {
                "type": "UUT",
                "serialNumber": serial_number,
                "partNumber": board_id or settings.get("default_part", "UNKNOWN"),
                "result": test_result,
                "processCode": settings.get("process_code", self.default_process_code),
                "stationName": settings.get("station", "AOI_Station"),
            }
            
            # Add defect information if available
            if defect_count > 0:
                report["comment"] = f"AOI detected {defect_count} defect(s)"
            
            # Determine post-processing action from settings
            post_action_str = settings.get("post_action", "zip")
            post_action = {
                "delete": PostProcessAction.DELETE,
                "move": PostProcessAction.MOVE,
                "zip": PostProcessAction.ZIP,
                "keep": PostProcessAction.KEEP
            }.get(post_action_str.lower(), PostProcessAction.ZIP)
            
            # Return success
            return ConverterResult.success_result(
                report=report,
                post_action=post_action,
                metadata={
                    "source_file": file_info.name,
                    "file_size": file_info.size,
                    "defect_count": defect_count,
                    "aoi_result": result,
                }
            )
        
        except Exception as e:
            return ConverterResult.failed_result(
                error=f"AOI conversion error: {str(e)}"
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
            f"Successfully converted AOI file {file_path.name}: "
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
        logger.error(f"Failed to convert AOI file {file_path.name}: {result.error}")
    
    def get_arguments(self) -> Dict[str, Any]:
        """Define configurable arguments for this converter"""
        return {
            "station": {
                "type": "string",
                "default": "AOI_Station",
                "description": "AOI test station name",
                "required": True
            },
            "default_part": {
                "type": "string",
                "default": "UNKNOWN",
                "description": "Default part number if not found in AOI log"
            },
            "process_code": {
                "type": "int",
                "default": 10,
                "description": "Process code for AOI tests",
                "min": 1,
                "max": 999
            },
            "post_action": {
                "type": "choice",
                "default": "zip",
                "choices": ["delete", "move", "zip", "keep"],
                "description": "Post-processing action after successful conversion"
            },
        }
    
    def _parse_aoi_log(self, content: str) -> Dict[str, Any]:
        """
        Parse AOI log file content.
        
        This is a simplified parser. Customize based on your AOI format.
        
        Args:
            content: Raw file content
            
        Returns:
            Dictionary with parsed data
        """
        data = {}
        
        # Parse line by line
        for line in content.split('\n'):
            line = line.strip()
            if not line or ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            # Map AOI fields to our data structure
            if 'serial' in key:
                data['serial'] = value
            elif 'board' in key or 'board_id' in key:
                data['board_id'] = value
            elif 'result' in key:
                data['result'] = value.upper()
            elif 'defect' in key:
                try:
                    data['defects'] = int(value)
                except ValueError:
                    data['defects'] = 0
        
        return data
