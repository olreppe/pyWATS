"""
Discriminated Union for Report Types

Provides type-safe report parsing based on the 'type' field:
- type="T" → UUTReport
- type="R" → UURReport

This enables polymorphic report handling with full type safety.
"""

from typing import Annotated, Union
from pydantic import Field, TypeAdapter

from .uut_report import UUTReport
from .uur_report import UURReport


# Discriminated union based on 'type' field
Report = Annotated[
    Union[UUTReport, UURReport],
    Field(discriminator='type')
]
"""
Type-safe union of all report types.

The discriminator is the 'type' field:
- "T" → UUTReport
- "R" → UURReport

Example usage:

Parsing unknown report JSON:
    json_data = '{"type": "T", "pn": "ABC123", ...}'
    report = parse_report(json_data)
    
    if isinstance(report, UUTReport):
        # TypeScript-style narrowing
        print(report.sequence_call.name)
    elif isinstance(report, UURReport):
        print(report.uur_info.operator)

Polymorphic handling:
    reports: list[Report] = [
        UUTReport.create(...),
        UURReport.create(...)
    ]
    
    for report in reports:
        if isinstance(report, UUTReport):
            process_uut(report)
        elif isinstance(report, UURReport):
            process_uur(report)
"""


# Type adapter for parsing
_report_adapter = TypeAdapter(Report)


def parse_report(data: dict | str | bytes) -> Report:
    """
    Parse JSON into the appropriate report type based on 'type' field.
    
    Args:
        data: JSON string, bytes, or dict representing a report
        
    Returns:
        UUTReport or UURReport based on type field
        
    Raises:
        ValidationError: If data is invalid or type field is unrecognized
        
    Example:
        json_str = '{"type": "T", "pn": "ABC123", "sn": "001", ...}'
        report = parse_report(json_str)
        assert isinstance(report, UUTReport)
    """
    import json
    
    # Parse JSON if needed
    if isinstance(data, (str, bytes)):
        obj = json.loads(data)
    else:
        obj = data
    
    # Discriminate based on type field
    report_type = obj.get('type')
    
    if report_type == 'T':
        return UUTReport.model_validate(obj)
    elif report_type == 'R':
        return UURReport.model_validate(obj)
    else:
        raise ValueError(f"Unknown report type: {report_type}. Expected 'T' or 'R'.")


def parse_reports(data: list[dict] | str | bytes) -> list[Report]:
    """
    Parse a list of reports from JSON.
    
    Args:
        data: JSON string, bytes, or list of dicts
        
    Returns:
        List of Report instances (UUTReport or UURReport)
        
    Example:
        json_str = '''[
            {"type": "T", "pn": "ABC123", ...},
            {"type": "R", "pn": "DEF456", ...}
        ]'''
        reports = parse_reports(json_str)
        assert isinstance(reports[0], UUTReport)
        assert isinstance(reports[1], UURReport)
    """
    if isinstance(data, (str, bytes)):
        import json
        data = json.loads(data)
    
    return [parse_report(item) for item in data]


def serialize_report(report: Report) -> str:
    """
    Serialize a report to JSON string.
    
    Args:
        report: UUTReport or UURReport instance
        
    Returns:
        JSON string representation
        
    Example:
        uut = UUTReport.create(...)
        json_str = serialize_report(uut)
    """
    return report.model_dump_json()


def serialize_reports(reports: list[Report]) -> str:
    """
    Serialize a list of reports to JSON string.
    
    Args:
        reports: List of Report instances
        
    Returns:
        JSON array string
        
    Example:
        reports = [uut1, uur1, uut2]
        json_str = serialize_reports(reports)
    """
    import json
    from pydantic.json import pydantic_encoder
    
    data = [report.model_dump() for report in reports]
    return json.dumps(data, default=pydantic_encoder)


def is_uut_report(report: Report) -> bool:
    """
    Type guard: Check if report is a UUTReport.
    
    Args:
        report: Any report instance
        
    Returns:
        True if report is UUTReport
    """
    return isinstance(report, UUTReport)


def is_uur_report(report: Report) -> bool:
    """
    Type guard: Check if report is a UURReport.
    
    Args:
        report: Any report instance
        
    Returns:
        True if report is UURReport
    """
    return isinstance(report, UURReport)


__all__ = [
    'Report',
    'parse_report',
    'parse_reports',
    'serialize_report',
    'serialize_reports',
    'is_uut_report',
    'is_uur_report',
]
