"""
Report management utilities for pyWATS.

This module provides utility functions for working with reports,
including loading, saving, and format conversion.
"""

from typing import Union, Dict, Any, List, Optional
from datetime import datetime
import json
import os
from pathlib import Path

from .models.report import UUTReport, UURReport, Report
from .exceptions import WATSException


def load_report_from_file(file_path: str) -> Union[UUTReport, UURReport]:
    """
    Load a report from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing the report
        
    Returns:
        The loaded report
        
    Raises:
        WATSException: If the file cannot be loaded or parsed
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Report file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Determine report type based on the 'type' field
        report_type = data.get('type', 'T')
        
        if report_type == 'T':
            return UUTReport.model_validate(data)
        elif report_type == 'R':
            return UURReport.model_validate(data)
        else:
            raise ValueError(f"Unknown report type: {report_type}")
            
    except Exception as e:
        raise WATSException(f"Failed to load report from file {file_path}: {str(e)}")


def save_report_to_file(report: Union[UUTReport, UURReport], file_path: str) -> str:
    """
    Save a report to a JSON file.
    
    Args:
        report: The report to save
        file_path: Path where the report should be saved
        
    Returns:
        The actual file path where the report was saved
        
    Raises:
        WATSException: If the file cannot be saved
    """
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Serialize report to JSON
        report_json = report.model_dump(mode='json', by_alias=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report_json, f, indent=2, ensure_ascii=False)
            
        return file_path
        
    except Exception as e:
        raise WATSException(f"Failed to save report to file {file_path}: {str(e)}")


def convert_report_format(report: Union[UUTReport, UURReport], 
                         target_format: str) -> str:
    """
    Convert a report to different format.
    
    Args:
        report: The report to convert
        target_format: Target format ('json', 'xml', 'dict')
        
    Returns:
        The report in the target format
        
    Raises:
        WATSException: If conversion fails
    """
    try:
        if target_format.lower() == 'json':
            return report.model_dump_json(by_alias=True, indent=2)
        elif target_format.lower() == 'dict':
            return str(report.model_dump(by_alias=True))
        elif target_format.lower() == 'xml':
            # For XML conversion, you might want to use a library like dicttoxml
            # For now, we'll return a basic XML representation
            data = report.model_dump(by_alias=True)
            return dict_to_simple_xml(data, root_tag=f"{report.type}Report")
        else:
            raise ValueError(f"Unsupported format: {target_format}")
            
    except Exception as e:
        raise WATSException(f"Failed to convert report to {target_format}: {str(e)}")


def dict_to_simple_xml(data: Dict[str, Any], root_tag: str = "report") -> str:
    """
    Convert a dictionary to simple XML format.
    
    Args:
        data: Dictionary to convert
        root_tag: Root XML tag name
        
    Returns:
        XML string representation
    """
    def _dict_to_xml(d: Dict[str, Any], level: int = 0) -> str:
        xml_lines = []
        indent = "  " * level
        
        for key, value in d.items():
            if isinstance(value, dict):
                xml_lines.append(f"{indent}<{key}>")
                xml_lines.append(_dict_to_xml(value, level + 1))
                xml_lines.append(f"{indent}</{key}>")
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        xml_lines.append(f"{indent}<{key}>")
                        xml_lines.append(_dict_to_xml(item, level + 1))
                        xml_lines.append(f"{indent}</{key}>")
                    else:
                        xml_lines.append(f"{indent}<{key}>{_escape_xml(str(item))}</{key}>")
            else:
                xml_lines.append(f"{indent}<{key}>{_escape_xml(str(value))}</{key}>")
                
        return "\n".join(xml_lines)
    
    xml_content = _dict_to_xml(data, 1)
    return f"<?xml version='1.0' encoding='UTF-8'?>\n<{root_tag}>\n{xml_content}\n</{root_tag}>"


def _escape_xml(text: str) -> str:
    """Escape special XML characters."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))


def get_report_summary(report: Union[UUTReport, UURReport]) -> Dict[str, Any]:
    """
    Get a summary of a report.
    
    Args:
        report: The report to summarize
        
    Returns:
        Dictionary containing report summary
    """
    summary = {
        "id": str(report.id),
        "type": "UUT Report" if report.type == "T" else "UUR Report",
        "part_number": report.pn,
        "serial_number": report.sn,
        "revision": report.rev,
        "result": report.result,
        "station": report.station_name,
        "location": report.location,
        "purpose": report.purpose,
        "start_time": report.start.isoformat() if report.start else None,
        "process_code": report.process_code
    }
    
    # Add type-specific information
    if isinstance(report, UUTReport) and hasattr(report, 'root') and report.root:
        # UUT Report
        summary["sequence_calls"] = len(getattr(report.root, 'steps', []) or [])
    
    if report.misc_infos:
        summary["misc_info_count"] = len(report.misc_infos)
        
    if report.assets:
        summary["asset_count"] = len(report.assets)
        
    if report.sub_units:
        summary["sub_unit_count"] = len(report.sub_units)
    
    return summary


def validate_report(report: Union[UUTReport, UURReport]) -> List[str]:
    """
    Validate a report and return any validation errors.
    
    Args:
        report: The report to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    try:
        # Basic validation - Pydantic will handle most of this
        report.model_validate(report.model_dump())
    except Exception as e:
        errors.append(f"Model validation failed: {str(e)}")
    
    # Additional business logic validation
    if not report.pn or not report.pn.strip():
        errors.append("Part number is required")
        
    if not report.sn or not report.sn.strip():
        errors.append("Serial number is required")
        
    if not report.rev or not report.rev.strip():
        errors.append("Revision is required")
        
    if report.result not in ['P', 'F', 'D', 'E', 'T']:
        errors.append(f"Invalid result code: {report.result}")
        
    if not report.station_name or not report.station_name.strip():
        errors.append("Station name is required")
        
    return errors