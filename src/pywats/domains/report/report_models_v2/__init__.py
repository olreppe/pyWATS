"""
Report Models v2 - Composition-Based Architecture

This package contains the redesigned report models using composition instead of inheritance.

Key improvements over v1:
- Composition over inheritance (eliminates type conflicts)
- Clean list types (no Optional[list] anti-pattern)
- Discriminated union for UUT/UUR parsing
- Type-safe (mypy clean)
- 100% JSON compatible with v1

Status: IMPLEMENTED (Beta)
Feature Flag: USE_REPORT_V2 (see examples below)

Architecture:
    ReportCommon - Composable model with all shared fields
    UUTReport - UUT report with composition (common: ReportCommon)
    UURReport - UUR report with composition (common: ReportCommon)
    Report - Discriminated union (UUTReport | UURReport)

Example Usage:
    # Create UUT report
    from pywats.domains.report.report_models_v2 import UUTReport
    
    uut = UUTReport.create(
        pn="ABC123",
        sn="001",
        rev="A",
        process_code=100,
        station_name="TestStation",
        location="Lab",
        purpose="Test"
    )
    
    # Create UUR report from failed UUT
    from pywats.domains.report.report_models_v2 import UURReport
    
    uur = UURReport.create_from_uut(
        uut,
        repair_process_code=500,
        operator="John Doe",
        comment="Replaced capacitor"
    )
    
    # Polymorphic report handling
    from pywats.domains.report.report_models_v2 import Report, parse_report
    
    json_str = '{"type": "T", "pn": "ABC", ...}'
    report = parse_report(json_str)
    
    if isinstance(report, UUTReport):
        # Handle UUT
        pass
    elif isinstance(report, UURReport):
        # Handle UUR
        pass

Related Documentation:
- docs/internal_documentation/WIP/to_do/REDESIGNING_THE_REPORT_MODEL.md
- docs/internal_documentation/WIP/to_do/REPORT_REDESIGN_ARCHITECTURE_NOTES.md
- docs/internal_documentation/WIP/to_do/REPORT_REDESIGN_INDEX.md
- src/pywats/domains/report/report_models_v2/IMPORT_STRATEGY.md
"""

# Core exports
from .report_common import ReportCommon
from .uut_report import UUTReport
from .uur_report import UURReport
from .report_union import (
    Report,
    parse_report,
    parse_reports,
    serialize_report,
    serialize_reports,
    is_uut_report,
    is_uur_report,
)

# Optional: Export the mixin for advanced use cases
from .report_proxy_mixin import ReportProxyMixin

__all__ = [
    # Core models
    'ReportCommon',
    'UUTReport',
    'UURReport',
    'Report',
    
    # Mixin (for custom report types)
    'ReportProxyMixin',
    
    # Parsing utilities
    'parse_report',
    'parse_reports',
    
    # Serialization utilities
    'serialize_report',
    'serialize_reports',
    
    # Type guards
    'is_uut_report',
    'is_uur_report',
]

__version__ = "2.0.0-beta1"

# Feature flag status
USE_REPORT_V2 = False  # Default: use v1 models
"""
Feature flag for enabling v2 report models.

Set to True to use v2 models throughout the codebase.
This will be enabled by default after comprehensive validation.

Example:
    from pywats.domains.report import report_models_v2
    report_models_v2.USE_REPORT_V2 = True
"""

