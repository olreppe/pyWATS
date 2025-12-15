"""
Custom Converter Template

This is an example converter that demonstrates the pyWATS converter architecture.
Use this as a starting point for creating your own converters.

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


class MyConverter(ConverterBase):
    """Example converter implementation"""
    
    def __init__(self, default_station: str = "Station1"):
        """
        Initialize converter with optional default values.
        
        Args:
            default_station: Default station name if not in file
        """
        super().__init__()
        self.default_station = default_station
    
    @property
    def name(self) -> str:
        """Human-readable converter name"""
        return "My Custom Converter"
    
    @property
    def version(self) -> str:
        """Converter version"""
        return "1.0.0"
    
    @property
    def description(self) -> str:
        """Description of what this converter does"""
        return "Converts custom log files to WATS UUT reports"
    
    @property
    def supported_extensions(self) -> list[str]:
        """List of file extensions this converter supports"""
        return [".log", ".txt"]
    
    @property
    def supported_mime_types(self) -> list[str]:
        """List of MIME types this converter supports"""
        return ["text/plain"]
    
    def validate_file(self, file_info: FileInfo) -> tuple[bool, str]:
        """
        Validate file before conversion.
        
        This is called before convert_file() to quickly filter files.
        
        Args:
            file_info: Information about the file
            
        Returns:
            Tuple of (is_valid, reason_if_invalid)
        """
        # Call base validation (checks extension and MIME type)
        valid, reason = super().validate_file(file_info)
        if not valid:
            return False, reason
        
        # Custom validation: check file size
        max_size = 5 * 1024 * 1024  # 5 MB
        if file_info.size > max_size:
            return False, f"File exceeds {max_size} bytes limit"
        
        # Check minimum size
        if file_info.size < 10:
            return False, "File too small, likely empty"
        
        return True, ""
    
    def convert_file(
        self,
        file_path: Path,
        args: ConverterArguments
    ) -> ConverterResult:
        """
        Convert file to WATS report.
        
        Args:
            file_path: Path to the file to convert
            args: ConverterArguments with API client, file info, folders, settings
            
        Returns:
            ConverterResult with status and report data
        """
        try:
            # Access converter arguments
            api = args.api_client
            file_info = args.file_info
            settings = args.user_settings
            
            # Read source file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse data (implement your custom parsing logic here)
            serial_number = self._extract_serial(content)
            part_number = self._extract_part(content)
            result = self._extract_result(content)
            
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
        """
        Called after successful conversion.
        
        Override for custom post-processing logic.
        """
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
        """
        Called after failed conversion.
        
        Override for custom error handling logic.
        """
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Failed to convert {file_path.name}: {result.error}")
    
    def get_arguments(self) -> Dict[str, Any]:
        """
        Define configurable arguments for this converter.
        
        These can be configured by users in the GUI or settings file.
        """
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
                "description": "Post-processing action after successful conversion"
            },
        }
    
    # Helper methods for parsing (implement your custom logic)
    def _extract_serial(self, content: str) -> str:
        """Extract serial number from file content"""
        # TODO: Implement your parsing logic
        # Example: return re.search(r'SN:(\w+)', content).group(1)
        return "DEMO-SERIAL-001"
    
    def _extract_part(self, content: str) -> str:
        """Extract part number from file content"""
        # TODO: Implement your parsing logic
        return "DEMO-PART-001"
    
    def _extract_result(self, content: str) -> str:
        """Extract test result from file content"""
        # TODO: Implement your parsing logic
        # Return "Passed" or "Failed"
        return "Passed"
