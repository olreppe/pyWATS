"""
Yield analysis tools for AI agents.

This package provides intelligent yield analysis with semantic dimension mapping.
Translates natural language concepts to WATS API dimensions and filters.

PROCESS TERMINOLOGY IN WATS:
- test_operation: For testing (UUT/UUTReport - Unit Under Test)
- repair_operation: For repair logging (UUR/UURReport - Unit Under Repair)  
- wip_operation: For production tracking (not used in analysis tools)

COMMON PROCESS PROBLEMS:
1. Mixed processes: Different tests (AOI, ICT) sent to same process causes
   second test to show 0 units (diagnosed by different sw_filename)
2. Name confusion: Users use "PCBA" instead of "PCBA test" - use fuzzy matching
"""

# Import everything from the combined tool module
# Future refactoring can split into separate files while keeping same exports
from .tool import (
    # Models
    YieldFilter,
    # Perspectives
    AnalysisPerspective,
    PERSPECTIVE_TO_DIMENSIONS,
    PERSPECTIVE_TO_DATE_GROUPING,
    PERSPECTIVE_ALIASES,
    resolve_perspective,
    get_available_perspectives,
    # Tool
    YieldAnalysisTool,
    get_yield_tool_definition,
    get_yield_tool_openai_schema,
    # Helpers
    build_wats_filter,
)

__all__ = [
    # Models
    "YieldFilter",
    # Perspectives
    "AnalysisPerspective",
    "PERSPECTIVE_TO_DIMENSIONS",
    "PERSPECTIVE_TO_DATE_GROUPING",
    "PERSPECTIVE_ALIASES",
    "resolve_perspective",
    "get_available_perspectives",
    # Tool
    "YieldAnalysisTool",
    "get_yield_tool_definition",
    "get_yield_tool_openai_schema",
    # Helpers
    "build_wats_filter",
]
