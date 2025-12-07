"""
Base Converter Interface

Defines the interface that all converters must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, BinaryIO, List
from pathlib import Path


@dataclass
class ConverterResult:
    """
    Result of a conversion operation.
    
    Attributes:
        success: Whether the conversion was successful
        report: The converted UUT/UUR report data (if successful)
        error: Error message (if failed)
        warnings: List of warning messages
        metadata: Additional metadata about the conversion
    """
    success: bool
    report: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConverterBase(ABC):
    """
    Base class for file-to-report converters.
    
    All converters must inherit from this class and implement
    the convert() method.
    
    Example:
        class MyConverter(ConverterBase):
            def __init__(self, station_name: str = "Default"):
                super().__init__()
                self.station_name = station_name
            
            @property
            def name(self) -> str:
                return "My Custom Converter"
            
            @property
            def supported_extensions(self) -> List[str]:
                return [".csv", ".txt"]
            
            def convert(self, file_stream: BinaryIO, filename: str) -> ConverterResult:
                # Parse file and create report
                data = file_stream.read().decode('utf-8')
                
                report = {
                    "type": "UUT",
                    "partNumber": "...",
                    "serialNumber": "...",
                    ...
                }
                
                return ConverterResult(success=True, report=report)
    """
    
    def __init__(self):
        # File handling options
        self.delete_on_success: bool = False
        self.processed_folder: Optional[str] = None
        self.error_folder: Optional[str] = None
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable name of the converter.
        """
        pass
    
    @property
    def version(self) -> str:
        """
        Version string for the converter.
        """
        return "1.0.0"
    
    @property
    def description(self) -> str:
        """
        Description of what the converter does.
        """
        return ""
    
    @property
    def supported_extensions(self) -> List[str]:
        """
        List of file extensions this converter supports.
        
        Example: [".csv", ".txt", ".xml"]
        """
        return ["*"]
    
    @abstractmethod
    def convert(self, file_stream: BinaryIO, filename: str) -> ConverterResult:
        """
        Convert a file to a UUT/UUR report.
        
        Args:
            file_stream: Binary file stream to read from
            filename: Original filename (useful for extension checking)
        
        Returns:
            ConverterResult with success status and report data
        """
        pass
    
    def validate_report(self, report: Dict[str, Any]) -> List[str]:
        """
        Validate a report before submission.
        
        Returns list of validation errors (empty if valid).
        Can be overridden by subclasses for custom validation.
        """
        errors = []
        
        # Basic required fields
        required_fields = ['partNumber', 'serialNumber', 'result']
        for field in required_fields:
            if field not in report or not report[field]:
                errors.append(f"Missing required field: {field}")
        
        return errors
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get configurable parameters for this converter.
        
        Returns a dictionary of parameter definitions that can be
        shown in the GUI for configuration.
        
        Format:
            {
                "param_name": {
                    "type": "string" | "int" | "float" | "bool" | "choice",
                    "default": <default_value>,
                    "description": "Parameter description",
                    "choices": ["a", "b"]  # Only for type="choice"
                }
            }
        """
        return {}


class CSVConverter(ConverterBase):
    """
    Example CSV converter implementation.
    
    This is a template showing how to implement a converter.
    Customize for your specific CSV format.
    """
    
    def __init__(
        self,
        delimiter: str = ",",
        encoding: str = "utf-8",
        skip_header: bool = True,
        part_number_column: int = 0,
        serial_number_column: int = 1,
        result_column: int = 2
    ):
        super().__init__()
        self.delimiter = delimiter
        self.encoding = encoding
        self.skip_header = skip_header
        self.part_number_column = part_number_column
        self.serial_number_column = serial_number_column
        self.result_column = result_column
    
    @property
    def name(self) -> str:
        return "CSV Converter"
    
    @property
    def description(self) -> str:
        return "Converts CSV files to UUT reports"
    
    @property
    def supported_extensions(self) -> List[str]:
        return [".csv"]
    
    def convert(self, file_stream: BinaryIO, filename: str) -> ConverterResult:
        try:
            # Read and decode file
            content = file_stream.read().decode(self.encoding)
            lines = content.strip().split('\n')
            
            if not lines:
                return ConverterResult(
                    success=False,
                    error="Empty file"
                )
            
            # Skip header if configured
            data_lines = lines[1:] if self.skip_header else lines
            
            if not data_lines:
                return ConverterResult(
                    success=False,
                    error="No data rows found"
                )
            
            # Parse first data row (can be extended for multi-row files)
            row = data_lines[0].split(self.delimiter)
            
            # Extract fields
            part_number = row[self.part_number_column].strip() if len(row) > self.part_number_column else ""
            serial_number = row[self.serial_number_column].strip() if len(row) > self.serial_number_column else ""
            result = row[self.result_column].strip() if len(row) > self.result_column else ""
            
            # Create report
            report = {
                "partNumber": part_number,
                "serialNumber": serial_number,
                "result": result.upper() if result.lower() in ["pass", "passed", "p"] else "Failed",
                "processCode": 10,  # Default process code
            }
            
            # Validate
            errors = self.validate_report(report)
            if errors:
                return ConverterResult(
                    success=False,
                    error="; ".join(errors)
                )
            
            return ConverterResult(
                success=True,
                report=report,
                metadata={"source_file": filename, "rows_processed": len(data_lines)}
            )
            
        except Exception as e:
            return ConverterResult(
                success=False,
                error=f"Conversion error: {str(e)}"
            )
    
    def get_parameters(self) -> Dict[str, Any]:
        return {
            "delimiter": {
                "type": "string",
                "default": ",",
                "description": "Field delimiter character"
            },
            "encoding": {
                "type": "choice",
                "default": "utf-8",
                "choices": ["utf-8", "latin-1", "ascii"],
                "description": "File encoding"
            },
            "skip_header": {
                "type": "bool",
                "default": True,
                "description": "Skip first row as header"
            },
            "part_number_column": {
                "type": "int",
                "default": 0,
                "description": "Column index for part number (0-based)"
            },
            "serial_number_column": {
                "type": "int",
                "default": 1,
                "description": "Column index for serial number (0-based)"
            },
            "result_column": {
                "type": "int",
                "default": 2,
                "description": "Column index for result (0-based)"
            }
        }
