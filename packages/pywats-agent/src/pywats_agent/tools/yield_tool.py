"""
Intelligent yield analysis tool with semantic dimension mapping.

Translates natural language concepts to WATS API dimensions and filters.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field

from ..result import AgentResult

if TYPE_CHECKING:
    from pywats import pyWATS


class AnalysisPerspective(str, Enum):
    """
    High-level analysis perspectives that map to dimension combinations.
    
    These are semantic concepts that LLMs understand naturally.
    """
    # Time-based
    TREND = "trend"                      # How is yield changing over time?
    DAILY = "daily"                      # Day-by-day breakdown
    WEEKLY = "weekly"                    # Week-by-week breakdown
    MONTHLY = "monthly"                  # Month-by-month breakdown
    
    # Location/Equipment
    BY_STATION = "by_station"            # Compare test stations
    BY_LINE = "by_line"                  # Compare production lines
    BY_FIXTURE = "by_fixture"            # Compare test fixtures
    
    # Product
    BY_PRODUCT = "by_product"            # Compare products/part numbers
    BY_REVISION = "by_revision"          # Compare product revisions
    BY_PRODUCT_GROUP = "by_product_group"  # Compare product groups
    
    # Process
    BY_OPERATION = "by_operation"        # Compare test operations
    BY_PROCESS = "by_process"            # Compare process codes
    
    # Software
    BY_SOFTWARE = "by_software"          # Compare test software versions
    
    # Other
    BY_OPERATOR = "by_operator"          # Compare operators
    BY_BATCH = "by_batch"                # Compare production batches
    BY_LEVEL = "by_level"                # Compare production levels (PCBA, Box Build)
    
    # Combinations
    STATION_TREND = "station_trend"      # Station performance over time
    PRODUCT_TREND = "product_trend"      # Product performance over time
    OPERATION_TREND = "operation_trend"  # Operation performance over time
    STATION_PRODUCT = "station_product"  # Station by product breakdown
    LINE_STATION = "line_station"        # Line by station breakdown


# Mapping from semantic perspectives to WATS dimensions
PERSPECTIVE_TO_DIMENSIONS: Dict[AnalysisPerspective, str] = {
    # Time-based (period is implicit in most)
    AnalysisPerspective.TREND: "period",
    AnalysisPerspective.DAILY: "period",
    AnalysisPerspective.WEEKLY: "period",
    AnalysisPerspective.MONTHLY: "period",
    
    # Location/Equipment
    AnalysisPerspective.BY_STATION: "stationName",
    AnalysisPerspective.BY_LINE: "location",
    AnalysisPerspective.BY_FIXTURE: "fixtureId",
    
    # Product
    AnalysisPerspective.BY_PRODUCT: "partNumber",
    AnalysisPerspective.BY_REVISION: "partNumber;revision",
    AnalysisPerspective.BY_PRODUCT_GROUP: "productGroup",
    
    # Process
    AnalysisPerspective.BY_OPERATION: "testOperation",
    AnalysisPerspective.BY_PROCESS: "processCode",
    
    # Software
    AnalysisPerspective.BY_SOFTWARE: "swFilename;swVersion",
    
    # Other
    AnalysisPerspective.BY_OPERATOR: "operator",
    AnalysisPerspective.BY_BATCH: "batchNumber",
    AnalysisPerspective.BY_LEVEL: "level",
    
    # Combinations (with period for trends)
    AnalysisPerspective.STATION_TREND: "stationName;period",
    AnalysisPerspective.PRODUCT_TREND: "partNumber;period",
    AnalysisPerspective.OPERATION_TREND: "testOperation;period",
    AnalysisPerspective.STATION_PRODUCT: "stationName;partNumber",
    AnalysisPerspective.LINE_STATION: "location;stationName",
}

# Date grouping for time-based perspectives
PERSPECTIVE_TO_DATE_GROUPING: Dict[AnalysisPerspective, str] = {
    AnalysisPerspective.DAILY: "DAY",
    AnalysisPerspective.WEEKLY: "WEEK",
    AnalysisPerspective.MONTHLY: "MONTH",
    AnalysisPerspective.TREND: "DAY",  # Default for trend
    AnalysisPerspective.STATION_TREND: "DAY",
    AnalysisPerspective.PRODUCT_TREND: "DAY",
    AnalysisPerspective.OPERATION_TREND: "DAY",
}

# Natural language aliases for perspectives
PERSPECTIVE_ALIASES: Dict[str, AnalysisPerspective] = {
    # Trend aliases
    "trend": AnalysisPerspective.TREND,
    "over time": AnalysisPerspective.TREND,
    "timeline": AnalysisPerspective.TREND,
    "history": AnalysisPerspective.TREND,
    "time series": AnalysisPerspective.TREND,
    "time-series": AnalysisPerspective.TREND,
    "trending": AnalysisPerspective.TREND,
    
    # Daily
    "daily": AnalysisPerspective.DAILY,
    "day by day": AnalysisPerspective.DAILY,
    "per day": AnalysisPerspective.DAILY,
    "each day": AnalysisPerspective.DAILY,
    "by day": AnalysisPerspective.DAILY,
    
    # Weekly
    "weekly": AnalysisPerspective.WEEKLY,
    "week by week": AnalysisPerspective.WEEKLY,
    "per week": AnalysisPerspective.WEEKLY,
    "each week": AnalysisPerspective.WEEKLY,
    "by week": AnalysisPerspective.WEEKLY,
    
    # Monthly
    "monthly": AnalysisPerspective.MONTHLY,
    "month by month": AnalysisPerspective.MONTHLY,
    "per month": AnalysisPerspective.MONTHLY,
    "each month": AnalysisPerspective.MONTHLY,
    "by month": AnalysisPerspective.MONTHLY,
    
    # Station aliases
    "by station": AnalysisPerspective.BY_STATION,
    "per station": AnalysisPerspective.BY_STATION,
    "station comparison": AnalysisPerspective.BY_STATION,
    "compare stations": AnalysisPerspective.BY_STATION,
    "test station": AnalysisPerspective.BY_STATION,
    "tester": AnalysisPerspective.BY_STATION,
    "by tester": AnalysisPerspective.BY_STATION,
    "equipment": AnalysisPerspective.BY_STATION,
    "by equipment": AnalysisPerspective.BY_STATION,
    "stations": AnalysisPerspective.BY_STATION,
    
    # Line aliases
    "by line": AnalysisPerspective.BY_LINE,
    "production line": AnalysisPerspective.BY_LINE,
    "manufacturing line": AnalysisPerspective.BY_LINE,
    "line comparison": AnalysisPerspective.BY_LINE,
    "by location": AnalysisPerspective.BY_LINE,
    "location": AnalysisPerspective.BY_LINE,
    "lines": AnalysisPerspective.BY_LINE,
    
    # Fixture aliases
    "by fixture": AnalysisPerspective.BY_FIXTURE,
    "fixture comparison": AnalysisPerspective.BY_FIXTURE,
    "test fixture": AnalysisPerspective.BY_FIXTURE,
    "socket": AnalysisPerspective.BY_FIXTURE,
    "by socket": AnalysisPerspective.BY_FIXTURE,
    "fixtures": AnalysisPerspective.BY_FIXTURE,
    
    # Product aliases
    "by product": AnalysisPerspective.BY_PRODUCT,
    "per product": AnalysisPerspective.BY_PRODUCT,
    "product comparison": AnalysisPerspective.BY_PRODUCT,
    "compare products": AnalysisPerspective.BY_PRODUCT,
    "by part": AnalysisPerspective.BY_PRODUCT,
    "by part number": AnalysisPerspective.BY_PRODUCT,
    "products": AnalysisPerspective.BY_PRODUCT,
    "parts": AnalysisPerspective.BY_PRODUCT,
    
    # Revision aliases
    "by revision": AnalysisPerspective.BY_REVISION,
    "revision comparison": AnalysisPerspective.BY_REVISION,
    "compare revisions": AnalysisPerspective.BY_REVISION,
    "by version": AnalysisPerspective.BY_REVISION,
    "revisions": AnalysisPerspective.BY_REVISION,
    "versions": AnalysisPerspective.BY_REVISION,
    
    # Product group aliases
    "by product group": AnalysisPerspective.BY_PRODUCT_GROUP,
    "by group": AnalysisPerspective.BY_PRODUCT_GROUP,
    "group comparison": AnalysisPerspective.BY_PRODUCT_GROUP,
    "by category": AnalysisPerspective.BY_PRODUCT_GROUP,
    "product groups": AnalysisPerspective.BY_PRODUCT_GROUP,
    "groups": AnalysisPerspective.BY_PRODUCT_GROUP,
    "categories": AnalysisPerspective.BY_PRODUCT_GROUP,
    
    # Operation aliases
    "by operation": AnalysisPerspective.BY_OPERATION,
    "by test operation": AnalysisPerspective.BY_OPERATION,
    "operation comparison": AnalysisPerspective.BY_OPERATION,
    "by test type": AnalysisPerspective.BY_OPERATION,
    "by test": AnalysisPerspective.BY_OPERATION,
    "operations": AnalysisPerspective.BY_OPERATION,
    "test operations": AnalysisPerspective.BY_OPERATION,
    "test types": AnalysisPerspective.BY_OPERATION,
    
    # Process aliases
    "by process": AnalysisPerspective.BY_PROCESS,
    "process comparison": AnalysisPerspective.BY_PROCESS,
    "by process code": AnalysisPerspective.BY_PROCESS,
    "processes": AnalysisPerspective.BY_PROCESS,
    
    # Software aliases
    "by software": AnalysisPerspective.BY_SOFTWARE,
    "software comparison": AnalysisPerspective.BY_SOFTWARE,
    "by test software": AnalysisPerspective.BY_SOFTWARE,
    "by sw version": AnalysisPerspective.BY_SOFTWARE,
    "software versions": AnalysisPerspective.BY_SOFTWARE,
    
    # Operator aliases
    "by operator": AnalysisPerspective.BY_OPERATOR,
    "operator comparison": AnalysisPerspective.BY_OPERATOR,
    "by technician": AnalysisPerspective.BY_OPERATOR,
    "by user": AnalysisPerspective.BY_OPERATOR,
    "operators": AnalysisPerspective.BY_OPERATOR,
    "technicians": AnalysisPerspective.BY_OPERATOR,
    
    # Batch aliases
    "by batch": AnalysisPerspective.BY_BATCH,
    "batch comparison": AnalysisPerspective.BY_BATCH,
    "by lot": AnalysisPerspective.BY_BATCH,
    "by production batch": AnalysisPerspective.BY_BATCH,
    "batches": AnalysisPerspective.BY_BATCH,
    "lots": AnalysisPerspective.BY_BATCH,
    
    # Level aliases
    "by level": AnalysisPerspective.BY_LEVEL,
    "level comparison": AnalysisPerspective.BY_LEVEL,
    "by production level": AnalysisPerspective.BY_LEVEL,
    "pcba vs box build": AnalysisPerspective.BY_LEVEL,
    "levels": AnalysisPerspective.BY_LEVEL,
    "production levels": AnalysisPerspective.BY_LEVEL,
    
    # Combined aliases
    "station trend": AnalysisPerspective.STATION_TREND,
    "station over time": AnalysisPerspective.STATION_TREND,
    "station performance trend": AnalysisPerspective.STATION_TREND,
    "stations over time": AnalysisPerspective.STATION_TREND,
    
    "product trend": AnalysisPerspective.PRODUCT_TREND,
    "product over time": AnalysisPerspective.PRODUCT_TREND,
    "product performance trend": AnalysisPerspective.PRODUCT_TREND,
    "products over time": AnalysisPerspective.PRODUCT_TREND,
    
    "operation trend": AnalysisPerspective.OPERATION_TREND,
    "operation over time": AnalysisPerspective.OPERATION_TREND,
    "operations over time": AnalysisPerspective.OPERATION_TREND,
    
    "station product": AnalysisPerspective.STATION_PRODUCT,
    "station by product": AnalysisPerspective.STATION_PRODUCT,
    "product by station": AnalysisPerspective.STATION_PRODUCT,
    
    "line station": AnalysisPerspective.LINE_STATION,
    "line by station": AnalysisPerspective.LINE_STATION,
    "stations by line": AnalysisPerspective.LINE_STATION,
}


class YieldFilter(BaseModel):
    """
    Yield analysis filter with semantic perspective support.
    
    This is the LLM-friendly interface that translates natural concepts
    to WATS API parameters.
    """
    
    # Semantic perspective (the key intelligence)
    perspective: Optional[str] = Field(
        default=None,
        description="""
        How to analyze/group the yield data. Use natural language like:
        - "trend", "over time", "daily", "weekly", "monthly" - Time-based analysis
        - "by station", "by tester", "by equipment" - Compare test stations
        - "by product", "by part number" - Compare products
        - "by revision", "by version" - Compare product revisions
        - "by operation", "by test type" - Compare test operations
        - "by line", "by location" - Compare production lines
        - "by batch", "by lot" - Compare production batches
        - "station trend" - Station performance over time
        - "product trend" - Product performance over time
        
        If not specified, returns overall yield for the filtered data.
        """
    )
    
    # Custom dimensions (advanced - override perspective)
    dimensions: Optional[str] = Field(
        default=None,
        description="""
        Advanced: Raw WATS dimensions string (semicolon-separated).
        Only use if perspective doesn't cover your need.
        Valid: partNumber, productName, stationName, location, purpose,
        revision, testOperation, processCode, swFilename, swVersion,
        productGroup, level, period, batchNumber, operator, fixtureId
        """
    )
    
    # Filters (narrow down what data to analyze)
    part_number: Optional[str] = Field(
        default=None,
        description="Filter by product part number (e.g., 'WIDGET-001')"
    )
    revision: Optional[str] = Field(
        default=None,
        description="Filter by product revision (e.g., 'A', '1.0')"
    )
    station_name: Optional[str] = Field(
        default=None,
        description="Filter by test station name (e.g., 'Line1-EOL')"
    )
    product_group: Optional[str] = Field(
        default=None,
        description="Filter by product group (e.g., 'Electronics')"
    )
    level: Optional[str] = Field(
        default=None,
        description="Filter by production level (e.g., 'PCBA', 'Box Build')"
    )
    test_operation: Optional[str] = Field(
        default=None,
        description="Filter by test operation (e.g., 'FCT', 'EOL')"
    )
    process_code: Optional[str] = Field(
        default=None,
        description="Filter by process code"
    )
    batch_number: Optional[str] = Field(
        default=None,
        description="Filter by production batch number"
    )
    operator: Optional[str] = Field(
        default=None,
        description="Filter by operator name"
    )
    location: Optional[str] = Field(
        default=None,
        description="Filter by location/production line"
    )
    
    # Time range
    days: int = Field(
        default=30,
        description="Number of days to analyze (default: 30)"
    )
    date_from: Optional[datetime] = Field(
        default=None,
        description="Start date (overrides 'days' if specified)"
    )
    date_to: Optional[datetime] = Field(
        default=None,
        description="End date (default: now)"
    )
    
    # Result options
    include_current_period: bool = Field(
        default=True,
        description="Include the current incomplete period"
    )
    
    # Metric selection
    metric: str = Field(
        default="fpy",
        description="Which yield metric: 'fpy' (First Pass Yield), 'yield' (Final Yield), 'all'"
    )


def resolve_perspective(perspective_input: Optional[str]) -> Optional[AnalysisPerspective]:
    """
    Resolve a natural language perspective to an AnalysisPerspective enum.
    
    Args:
        perspective_input: Natural language perspective string
        
    Returns:
        AnalysisPerspective enum value, or None if not recognized
        
    Examples:
        >>> resolve_perspective("by station")
        AnalysisPerspective.BY_STATION
        >>> resolve_perspective("trending over time")
        AnalysisPerspective.TREND
        >>> resolve_perspective("daily")
        AnalysisPerspective.DAILY
    """
    if not perspective_input:
        return None
    
    # Normalize input
    normalized = perspective_input.lower().strip()
    
    # Direct enum match
    try:
        return AnalysisPerspective(normalized)
    except ValueError:
        pass
    
    # Exact alias match
    if normalized in PERSPECTIVE_ALIASES:
        return PERSPECTIVE_ALIASES[normalized]
    
    # Fuzzy match - check if any alias is contained in the input
    for alias, perspective in sorted(PERSPECTIVE_ALIASES.items(), key=lambda x: -len(x[0])):
        # Prefer longer matches first
        if alias in normalized:
            return perspective
    
    # Check if input contains any alias
    for alias, perspective in sorted(PERSPECTIVE_ALIASES.items(), key=lambda x: -len(x[0])):
        if normalized in alias:
            return perspective
    
    return None


def get_available_perspectives() -> Dict[str, List[str]]:
    """
    Get available perspectives organized by category.
    
    Returns:
        Dictionary mapping category to list of perspective names
    """
    return {
        "time_based": ["trend", "daily", "weekly", "monthly"],
        "equipment": ["by_station", "by_line", "by_fixture"],
        "product": ["by_product", "by_revision", "by_product_group"],
        "process": ["by_operation", "by_process"],
        "other": ["by_operator", "by_batch", "by_level", "by_software"],
        "combined": ["station_trend", "product_trend", "operation_trend", "station_product"],
    }


def build_wats_filter(yield_filter: YieldFilter) -> Dict[str, Any]:
    """
    Convert YieldFilter to WATS API filter parameters.
    
    Args:
        yield_filter: The semantic yield filter
        
    Returns:
        Dictionary of WATS API parameters
    """
    # Resolve perspective to dimensions
    perspective = resolve_perspective(yield_filter.perspective)
    
    # Use explicit dimensions if provided, otherwise resolve from perspective
    if yield_filter.dimensions:
        dimensions = yield_filter.dimensions
    elif perspective:
        dimensions = PERSPECTIVE_TO_DIMENSIONS.get(perspective, "period")
    else:
        dimensions = None  # No grouping, aggregate all
    
    # Calculate date range
    date_to = yield_filter.date_to or datetime.now()
    if yield_filter.date_from:
        date_from = yield_filter.date_from
    else:
        date_from = date_to - timedelta(days=yield_filter.days)
    
    # Determine date grouping
    date_grouping = None
    if perspective:
        date_grouping = PERSPECTIVE_TO_DATE_GROUPING.get(perspective)
    
    # Build filter dict
    filter_params: Dict[str, Any] = {
        "date_from": date_from,
        "date_to": date_to,
        "include_current_period": yield_filter.include_current_period,
    }
    
    if dimensions:
        filter_params["dimensions"] = dimensions
    if date_grouping:
        filter_params["date_grouping"] = date_grouping
    
    # Add explicit filters
    if yield_filter.part_number:
        filter_params["part_number"] = yield_filter.part_number
    if yield_filter.revision:
        filter_params["revision"] = yield_filter.revision
    if yield_filter.station_name:
        filter_params["station_name"] = yield_filter.station_name
    if yield_filter.product_group:
        filter_params["product_group"] = yield_filter.product_group
    if yield_filter.level:
        filter_params["level"] = yield_filter.level
    if yield_filter.test_operation:
        filter_params["test_operation"] = yield_filter.test_operation
    if yield_filter.process_code:
        filter_params["process_code"] = yield_filter.process_code
    if yield_filter.batch_number:
        filter_params["batch_number"] = yield_filter.batch_number
    if yield_filter.operator:
        filter_params["operator"] = yield_filter.operator
    if yield_filter.location:
        filter_params["location"] = yield_filter.location
    
    return filter_params


class YieldAnalysisTool:
    """
    Intelligent yield analysis tool for AI agents.
    
    Translates semantic analysis requests to WATS API calls.
    
    Example:
        >>> tool = YieldAnalysisTool(api)
        >>> 
        >>> # Natural language perspective
        >>> result = tool.analyze(YieldFilter(
        ...     part_number="WIDGET-001",
        ...     perspective="by station",
        ...     days=7
        ... ))
        >>> 
        >>> # The tool automatically translates to:
        >>> # dimensions="stationName", filters for WIDGET-001, last 7 days
    """
    
    name = "analyze_yield"
    description = """
Analyze manufacturing yield/quality data with flexible grouping.

Use this tool to answer questions like:
- "What's the yield for WIDGET-001?" (overall yield)
- "How is yield trending over time?" (perspective: "trend")
- "Compare yield by station" (perspective: "by station")
- "Which product has the worst yield?" (perspective: "by product")
- "Show daily yield for the past week" (perspective: "daily", days: 7)
- "How does Line1-EOL yield compare over time?" (station_name + perspective: "trend")

The 'perspective' parameter is the key - it determines how data is grouped.
Use natural language like "by station", "trend", "daily", "by product", etc.

Available perspectives:
- Time: trend, daily, weekly, monthly
- Equipment: by station, by fixture, by line
- Product: by product, by revision, by product group
- Process: by operation, by process
- Other: by operator, by batch, by level
- Combined: station trend, product trend, operation trend
"""
    
    def __init__(self, api: "pyWATS"):
        """Initialize with a pyWATS instance."""
        self._api = api
    
    @staticmethod
    def get_parameters_schema() -> Dict[str, Any]:
        """Get OpenAI-compatible parameter schema."""
        return {
            "type": "object",
            "properties": {
                "perspective": {
                    "type": "string",
                    "description": """
How to group/analyze the data. Natural language options:
- Time: "trend", "daily", "weekly", "monthly"
- Equipment: "by station", "by fixture", "by line"
- Product: "by product", "by revision", "by product group"
- Process: "by operation", "by process"
- Other: "by operator", "by batch", "by level"
- Combined: "station trend", "product trend"
Leave empty for overall aggregated yield.
                    """.strip()
                },
                "part_number": {
                    "type": "string",
                    "description": "Filter by product part number"
                },
                "revision": {
                    "type": "string",
                    "description": "Filter by product revision"
                },
                "station_name": {
                    "type": "string",
                    "description": "Filter by test station name"
                },
                "product_group": {
                    "type": "string",
                    "description": "Filter by product group"
                },
                "level": {
                    "type": "string",
                    "description": "Filter by production level (PCBA, Box Build, etc.)"
                },
                "test_operation": {
                    "type": "string",
                    "description": "Filter by test operation (FCT, EOL, etc.)"
                },
                "process_code": {
                    "type": "string",
                    "description": "Filter by process code"
                },
                "batch_number": {
                    "type": "string",
                    "description": "Filter by production batch"
                },
                "operator": {
                    "type": "string",
                    "description": "Filter by operator name"
                },
                "location": {
                    "type": "string",
                    "description": "Filter by location/production line"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to analyze (default: 30)",
                    "default": 30
                },
                "dimensions": {
                    "type": "string",
                    "description": "Advanced: Raw WATS dimensions (semicolon-separated). Use perspective instead when possible."
                },
            },
            "required": []  # All optional - flexible querying
        }
    
    def analyze(self, filter_input: YieldFilter) -> AgentResult:
        """
        Analyze yield with the given filter.
        
        Args:
            filter_input: YieldFilter with perspective and filters
            
        Returns:
            AgentResult with yield data and summary
        """
        try:
            # Build WATS filter
            wats_params = build_wats_filter(filter_input)
            
            # Import here to avoid circular imports
            from pywats.domains.report.models import WATSFilter
            
            wats_filter = WATSFilter(**wats_params)
            
            # Call the API
            data = self._api.analytics.get_dynamic_yield(wats_filter)
            
            if not data:
                return AgentResult.success(
                    data=[],
                    summary=self._build_no_data_summary(filter_input)
                )
            
            # Build rich summary
            summary = self._build_summary(data, filter_input, wats_params)
            
            # Resolve perspective for metadata
            perspective = resolve_perspective(filter_input.perspective)
            
            return AgentResult.success(
                data=[d.model_dump() for d in data],
                summary=summary,
                metadata={
                    "perspective": filter_input.perspective,
                    "resolved_perspective": perspective.value if perspective else None,
                    "dimensions": wats_params.get("dimensions"),
                    "record_count": len(data),
                    "filters_applied": {
                        k: v for k, v in wats_params.items() 
                        if k not in ["dimensions", "date_from", "date_to", "date_grouping", "include_current_period"]
                        and v is not None
                    }
                }
            )
            
        except Exception as e:
            return AgentResult.error(f"Yield analysis failed: {str(e)}")
    
    def analyze_from_dict(self, params: Dict[str, Any]) -> AgentResult:
        """
        Analyze yield from a dictionary of parameters.
        
        This is the main entry point for agent tool calls.
        
        Args:
            params: Dictionary of parameters from LLM tool call
            
        Returns:
            AgentResult with yield data and summary
        """
        filter_input = YieldFilter(**params)
        return self.analyze(filter_input)
    
    def _build_summary(
        self, 
        data: List, 
        filter_input: YieldFilter,
        wats_params: Dict[str, Any]
    ) -> str:
        """Build a human-readable summary of the yield data."""
        
        # Calculate overall statistics
        total_units = sum(getattr(d, 'unit_count', 0) or 0 for d in data)
        
        # Try to get FPY (first_pass_yield)
        fpy_values = []
        for d in data:
            fpy = getattr(d, 'first_pass_yield', None)
            if fpy is not None:
                fpy_values.append(fpy)
        
        avg_fpy = sum(fpy_values) / len(fpy_values) if fpy_values else None
        
        # Build context string
        context_parts = []
        if filter_input.part_number:
            context_parts.append(f"product {filter_input.part_number}")
        if filter_input.station_name:
            context_parts.append(f"station {filter_input.station_name}")
        if filter_input.product_group:
            context_parts.append(f"group {filter_input.product_group}")
        if filter_input.test_operation:
            context_parts.append(f"operation {filter_input.test_operation}")
        if filter_input.location:
            context_parts.append(f"location {filter_input.location}")
        
        context = " for " + ", ".join(context_parts) if context_parts else ""
        
        # Build perspective description
        perspective = resolve_perspective(filter_input.perspective)
        if perspective:
            perspective_desc = f" grouped {filter_input.perspective}"
        else:
            perspective_desc = ""
        
        # Build the summary
        parts = [f"Yield analysis{context}{perspective_desc} (last {filter_input.days} days):"]
        
        if avg_fpy is not None:
            parts.append(f"• Average FPY: {avg_fpy:.1f}%")
        parts.append(f"• Total units: {total_units:,}")
        parts.append(f"• Data points: {len(data)}")
        
        # Add top/bottom if grouped
        if perspective and len(data) > 1:
            # Sort by FPY to find best/worst
            sorted_data = sorted(
                data, 
                key=lambda d: getattr(d, 'first_pass_yield', 0) or 0,
                reverse=True
            )
            
            if len(sorted_data) >= 2:
                best = sorted_data[0]
                worst = sorted_data[-1]
                
                best_fpy = getattr(best, 'first_pass_yield', None)
                worst_fpy = getattr(worst, 'first_pass_yield', None)
                
                # Try to get a label for best/worst based on dimensions
                best_label = self._get_data_label(best, perspective)
                worst_label = self._get_data_label(worst, perspective)
                
                if best_fpy is not None and best_label:
                    parts.append(f"• Best: {best_label} ({best_fpy:.1f}%)")
                if worst_fpy is not None and worst_label:
                    parts.append(f"• Worst: {worst_label} ({worst_fpy:.1f}%)")
        
        return "\n".join(parts)
    
    def _get_data_label(self, data_point: Any, perspective: AnalysisPerspective) -> Optional[str]:
        """Get a human-readable label for a data point based on the perspective."""
        
        # Map perspectives to likely label fields
        label_fields = {
            AnalysisPerspective.BY_STATION: ["station_name", "stationName"],
            AnalysisPerspective.STATION_TREND: ["station_name", "stationName", "period"],
            AnalysisPerspective.BY_PRODUCT: ["part_number", "partNumber"],
            AnalysisPerspective.PRODUCT_TREND: ["part_number", "partNumber", "period"],
            AnalysisPerspective.BY_LINE: ["location"],
            AnalysisPerspective.BY_OPERATION: ["test_operation", "testOperation"],
            AnalysisPerspective.BY_FIXTURE: ["fixture_id", "fixtureId"],
            AnalysisPerspective.BY_BATCH: ["batch_number", "batchNumber"],
            AnalysisPerspective.BY_OPERATOR: ["operator"],
            AnalysisPerspective.BY_LEVEL: ["level"],
            AnalysisPerspective.BY_REVISION: ["part_number", "revision"],
            AnalysisPerspective.BY_PRODUCT_GROUP: ["product_group", "productGroup"],
            AnalysisPerspective.TREND: ["period"],
            AnalysisPerspective.DAILY: ["period"],
            AnalysisPerspective.WEEKLY: ["period"],
            AnalysisPerspective.MONTHLY: ["period"],
        }
        
        fields_to_try = label_fields.get(perspective, ["period"])
        
        for field in fields_to_try:
            value = getattr(data_point, field, None)
            if value:
                return str(value)
        
        return None
    
    def _build_no_data_summary(self, filter_input: YieldFilter) -> str:
        """Build a summary when no data is found."""
        context_parts = []
        if filter_input.part_number:
            context_parts.append(f"product {filter_input.part_number}")
        if filter_input.station_name:
            context_parts.append(f"station {filter_input.station_name}")
        if filter_input.test_operation:
            context_parts.append(f"operation {filter_input.test_operation}")
        
        context = " for " + ", ".join(context_parts) if context_parts else ""
        return f"No yield data found{context} in the last {filter_input.days} days"
    
    # =========================================================================
    # Convenience methods for common analyses
    # =========================================================================
    
    def get_product_yield(
        self, 
        part_number: str, 
        days: int = 30,
        perspective: str = "trend"
    ) -> AgentResult:
        """Get yield for a specific product."""
        return self.analyze(YieldFilter(
            part_number=part_number,
            days=days,
            perspective=perspective
        ))
    
    def compare_stations(
        self,
        part_number: Optional[str] = None,
        days: int = 7
    ) -> AgentResult:
        """Compare yield across test stations."""
        return self.analyze(YieldFilter(
            part_number=part_number,
            days=days,
            perspective="by station"
        ))
    
    def get_station_trend(
        self,
        station_name: str,
        days: int = 30
    ) -> AgentResult:
        """Get yield trend for a specific station."""
        return self.analyze(YieldFilter(
            station_name=station_name,
            days=days,
            perspective="trend"
        ))
    
    def get_worst_performing(
        self,
        perspective: str = "by product",
        days: int = 30,
        product_group: Optional[str] = None
    ) -> AgentResult:
        """Get worst performing items by the given perspective."""
        return self.analyze(YieldFilter(
            perspective=perspective,
            days=days,
            product_group=product_group
        ))
    
    def get_daily_summary(
        self,
        part_number: Optional[str] = None,
        station_name: Optional[str] = None,
        days: int = 7
    ) -> AgentResult:
        """Get daily yield summary."""
        return self.analyze(YieldFilter(
            part_number=part_number,
            station_name=station_name,
            days=days,
            perspective="daily"
        ))


def get_yield_tool_definition() -> Dict[str, Any]:
    """Get the yield tool definition for agent frameworks."""
    return {
        "name": YieldAnalysisTool.name,
        "description": YieldAnalysisTool.description,
        "parameters": YieldAnalysisTool.get_parameters_schema(),
    }


def get_yield_tool_openai_schema() -> Dict[str, Any]:
    """Get OpenAI function calling schema for the yield tool."""
    return {
        "type": "function",
        "function": get_yield_tool_definition()
    }
