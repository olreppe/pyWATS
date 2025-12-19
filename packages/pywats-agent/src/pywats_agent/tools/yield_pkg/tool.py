"""
Intelligent yield analysis tool with semantic dimension mapping.

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

from typing import Any, Dict, List, Optional, TYPE_CHECKING
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field

from ...result import AgentResult

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
        - "by operation", "by test type", "by process" - Compare test operations
        - "by line", "by level" - Compare production lines
        - "by batch", "by lot", "by work order" - Compare production batches
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
        description="Filter by test operation (e.g., 'FCT', 'EOL'). Use fuzzy names like 'PCBA' or 'board test'."
    )
    process_code: Optional[str] = Field(
        default=None,
        description="NOTE: Can only be used as a DIMENSION for grouping, not as a filter. Use test_operation for filtering."
    )
    batch_number: Optional[str] = Field(
        default=None,
        description="Filter by production batch number"
    )
    operator: Optional[str] = Field(
        default=None,
        description="NOTE: Can only be used as a DIMENSION for grouping (via perspective='by operator'), not as a filter."
    )
    location: Optional[str] = Field(
        default=None,
        description="NOTE: Can only be used as a DIMENSION for grouping (via perspective='by location'), not as a filter."
    )
    
    # Time range
    # NOTE: WATS defaults to last 30 days if no date range specified.
    # WATS always assumes you want the most recent data.
    # WARNING: 30 days can be too much for high-volume customers (millions/week).
    # Consider using adaptive_time=True for automatic adjustment.
    days: int = Field(
        default=30,
        description="Number of days to analyze (default: 30). WARNING: May be too large for high-volume production."
    )
    date_from: Optional[datetime] = Field(
        default=None,
        description="Start date (overrides 'days' if specified). If omitted, WATS uses last 30 days."
    )
    date_to: Optional[datetime] = Field(
        default=None,
        description="End date (default: now). WATS always assumes you want the most recent data."
    )
    
    # Adaptive time filter
    adaptive_time: bool = Field(
        default=False,
        description="""
Enable adaptive time filtering based on production volume.
When True, starts with small window (1 day) and expands as needed.
Useful for high-volume production where 30 days would be too much data.
        """
    )
    
    # Result options
    include_current_period: bool = Field(
        default=True,
        description="Include the current incomplete period in time-based analysis"
    )
    
    # Periodic yield parameters
    # NOTE: For yield over time, use perspective="trend/daily/weekly/monthly"
    # which automatically sets date_grouping. These are advanced overrides.
    period_count: Optional[int] = Field(
        default=None,
        description="""
Number of time periods to return (used with date_grouping).
Example: period_count=7 with daily perspective returns 7 days of data.
        """
    )
    date_grouping: Optional[str] = Field(
        default=None,
        description="""
How to group data by time: HOUR, DAY, WEEK, MONTH, QUARTER, YEAR.
Usually set automatically by perspective (daily=DAY, weekly=WEEK, etc.).
Only specify for advanced use cases.
        """
    )
    
    # Metric selection
    metric: str = Field(
        default="fpy",
        description="Which yield metric: 'fpy' (First Pass Yield), 'yield' (Final Yield), 'all'"
    )
    
    # Yield calculation type - critical for understanding results
    yield_type: str = Field(
        default="unit",
        description="""
Type of yield calculation:
- 'unit' (default): Unit-based yield (FPY, SPY, TPY, LPY)
  * Measures % of units that passed
  * IMPORTANT: Units included only if their FIRST RUN matches filter
  * Use for product quality, overall line performance
  
- 'report': Report-based yield (TRY - Test Report Yield)
  * Measures passed reports / all reports
  * Use for station/fixture/operator performance
  * REQUIRED for retest-only stations (repair lines) that never see first runs

REPAIR LINE WARNING: If you filter by a station/fixture/operator that only 
handles retests, unit-based yield will show 0 units. Use 'report' instead.
        """
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
        
    Time Filter Logic:
        - If period_count is set WITHOUT explicit date_from: Let API calculate
          date range from period_count (WATS default behavior)
        - If explicit date_from is set: Use the explicit date range
        - If neither: Calculate date range from 'days' parameter
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
    
    # Determine date grouping (explicit override or from perspective)
    date_grouping = yield_filter.date_grouping  # Explicit override first
    if not date_grouping and perspective:
        date_grouping = PERSPECTIVE_TO_DATE_GROUPING.get(perspective)
    
    # Build filter dict
    filter_params: Dict[str, Any] = {
        "include_current_period": yield_filter.include_current_period,
    }
    
    # Time filter logic:
    # When period_count is set WITHOUT explicit date_from, let the API
    # calculate the date range from period_count (this is WATS default behavior).
    # Otherwise, calculate date range from explicit dates or 'days' parameter.
    user_provided_date_from = yield_filter.date_from is not None
    
    if yield_filter.period_count and not user_provided_date_from:
        # Let API calculate date range from period_count
        # Don't include date_from/date_to
        filter_params["period_count"] = yield_filter.period_count
    else:
        # Calculate explicit date range
        date_to = yield_filter.date_to or datetime.now()
        if yield_filter.date_from:
            date_from = yield_filter.date_from
        else:
            date_from = date_to - timedelta(days=yield_filter.days)
        
        filter_params["date_from"] = date_from
        filter_params["date_to"] = date_to
        
        # If period_count was also set (with explicit date range), include it
        if yield_filter.period_count:
            filter_params["period_count"] = yield_filter.period_count
    
    if dimensions:
        filter_params["dimensions"] = dimensions
    if date_grouping:
        filter_params["date_grouping"] = date_grouping
    
    # Add explicit filters
    # NOTE: Only add fields that exist in WATSFilter (PublicWatsFilter schema)
    # Fields like process_code, operator, location are DIMENSION values,
    # not filter fields. They can be used in the 'dimensions' string to
    # group by, but cannot filter by them directly.
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
    # NOTE: process_code is NOT a valid WATSFilter field - removed
    # It can be used as a dimension for grouping but not for filtering
    if yield_filter.batch_number:
        filter_params["batch_number"] = yield_filter.batch_number
    # NOTE: operator and location are NOT valid WATSFilter fields - removed
    # They can be used as dimensions for grouping but not for filtering
    
    return filter_params


class YieldAnalysisTool:
    """
    Intelligent yield analysis tool for AI agents.
    
    Translates semantic analysis requests to WATS API calls.
    
    YIELD METRICS OVERVIEW:
    
    UNIT-BASED METRICS (FPY, SPY, TPY, LPY):
    - Measure what percentage of UNITS passed at each attempt
    - FPY (First Pass Yield): Units that passed on Run 1 / Total units
    - SPY (Second Pass Yield): Units that passed by Run 2 / Total units  
    - TPY (Third Pass Yield): Units that passed by Run 3 / Total units
    - LPY (Last Pass Yield): Units that eventually passed / Total units
    
    REPORT-BASED METRIC (TRY - Test Report Yield):
    - TRY = Passed reports / All reports
    - Measures test execution success rate, not unit success rate
    
    ROLLED THROUGHPUT YIELD (RTY):
    - RTY = Product of FPY across ALL processes/test_operations
    - Example: If PCBA FPY=95% and EOL FPY=98%, then RTY = 0.95 x 0.98 = 93.1%
    - Use RTY for overall unit quality across the entire production flow
    - Yield for a product WITHOUT specifying process is ambiguous - clarify!
    
    CRITICAL - PROCESS/TEST_OPERATION CONTEXT:
    Yield should ALWAYS be considered per process (test_operation):
    - A product may go through multiple processes (ICT, FCT, EOL, etc.)
    - Each process has its own yield (FPY, LPY, etc.)
    - "Yield for WIDGET-001" is incomplete - need to specify which process
    - Use RTY when asking about overall product quality across all processes
    
    TOP RUNNERS:
    - Products with highest test volume (unit count or report count)
    - Volume must be considered PER PROCESS - a top runner in FCT may not be
      a top runner in EOL
    - Use perspective="by product" with process filter to find top runners
    
    CRITICAL - UNIT INCLUSION RULE:
    A unit is ONLY included if its FIRST RUN matches the filter criteria.
    If included, ALL runs for that unit count (even runs outside the filter).
    This ensures mathematically correct FPY-to-LPY calculations.
    
    REPAIR LINE SCENARIO (Important edge case):
    When filtering by station/fixture/operator that only handles retests (Run 2+),
    the unit count will be ZERO because no first runs exist at that location.
    Example: A repair line station only sees failed units from main line.
    Solution: Use yield_type='report' (TRY) for retest-only station analysis.
    
    YIELD OVER TIME (Temporal Analysis):
    
    DATE RANGE DEFAULTS:
    - If date_from/date_to are not specified, WATS defaults to last 30 days
    - WATS always assumes you want the MOST RECENT data
    - Use 'days' parameter for simple "last N days" queries
    
    PERIODIC YIELD (Time-Series Analysis):
    Use perspective="daily/weekly/monthly" or "trend" for yield over time.
    - This automatically sets date_grouping (DAY, WEEK, MONTH, etc.)
    - Returns yield for each time period within the date range
    - Include period_count to limit number of periods returned
    
    YIELD TREND METRICS:
    - Yield trend describes CHANGE compared to the PREVIOUS equally-sized period
    - Example: "today vs yesterday", "this week vs last week"
    - Useful for detecting improvement or degradation patterns
    
    PERIOD AGGREGATION (Safe Summing):
    - When fetching yield over periods, the first-pass-included rule applies
    - This means periods can be safely aggregated (summed) together
    - Each unit is counted only once in its first-run period
    - Example: Sum Monday-Friday yields for weekly total (units won't double-count)
    
    UNIT VERIFICATION RULES:
    - API functions exist to define which processes must pass for each product
    - These rules can be auto-suggested based on yield data analysis
    - Rarely kept up-to-date by customers, but useful for validation
    
    Example:
        >>> tool = YieldAnalysisTool(api)
        >>> 
        >>> # Yield per process (recommended approach)
        >>> result = tool.analyze(YieldFilter(
        ...     part_number="WIDGET-001",
        ...     test_operation="FCT",  # Always specify process!
        ...     perspective="trend",
        ...     days=7
        ... ))
        >>> 
        >>> # Check what processes exist for a product
        >>> result = tool.analyze(YieldFilter(
        ...     part_number="WIDGET-001",
        ...     perspective="by operation",  # Lists processes with their yields
        ...     days=30
        ... ))
        >>> 
        >>> # Daily yield trend for the last week
        >>> result = tool.analyze(YieldFilter(
        ...     part_number="WIDGET-001",
        ...     test_operation="FCT",
        ...     perspective="daily",
        ...     days=7
        ... ))
        >>> 
        >>> # Report-based yield for repair line analysis
        >>> result = tool.analyze(YieldFilter(
        ...     station_name="REPAIR-STATION-01",
        ...     yield_type="report",
        ...     days=30
        ... ))
        >>>
        >>> # High-volume production - use adaptive time
        >>> result = tool.analyze(YieldFilter(
        ...     part_number="HIGH-VOLUME-PRODUCT",
        ...     adaptive_time=True  # Starts small, expands as needed
        ... ))
    """
    
    name = "analyze_yield"
    description = """
Analyze manufacturing yield/quality data with flexible grouping.

UNDERSTANDING YIELD METRICS:

UNIT-BASED YIELD (FPY, SPY, TPY, LPY) - Default:
- FPY = Units passed on first try / Total units (the key quality metric)
- SPY/TPY = Units passed by 2nd/3rd try / Total units
- LPY = Units eventually passed / Total units
- Use for: Product quality per process, overall line performance

REPORT-BASED YIELD (TRY - Test Report Yield):
- TRY = Passed reports / All reports
- Use for: Station/fixture/operator performance, especially retest stations

ROLLED THROUGHPUT YIELD (RTY):
- RTY = FPY(Process1) x FPY(Process2) x ... x FPY(ProcessN)
- Use for: Overall unit quality across ALL processes
- Example: FCT FPY=95%, EOL FPY=98% -> RTY = 93.1%

CRITICAL - PROCESS TERMINOLOGY:
- test_operation: For testing (UUT/UUTReport - Unit Under Test)
- repair_operation: For repair logging (UUR/UURReport - Unit Under Repair)
- Process names are fuzzy-matched - "PCBA", "pcba test", "board test" all work

CRITICAL - YIELD IS PER PROCESS:
Yield should always be considered per process/test_operation!
- A product goes through multiple processes (ICT, FCT, EOL, etc.)
- Each process has its own yield
- "What's yield for WIDGET-001?" -> Clarify: which process, or RTY?
- Use perspective="by operation" to see all processes for a product

IMPORTANT - MIXED PROCESS PROBLEM:
If users send different tests (AOI, ICT) to the same process ("Structural Tests"):
- First test determines unit counts and FPY
- Second test shows 0 units (treated as "retest after pass")
- SYMPTOM: "Why is ICT showing 0 units?"
- DIAGNOSIS: Look for different sw_filename in the same process

TOP RUNNERS:
"Top runners" = products with highest volume (units or reports)
- Volume must be considered PER PROCESS
- A top runner in FCT may differ from top runner in EOL
- Use perspective="by product" with test_operation filter

IMPORTANT - UNIT INCLUSION RULE:
Units are included ONLY if their FIRST RUN matches your filter!
If filtering by a repair/retest station that never sees first runs,
you will get ZERO units. Use yield_type='report' (TRY) instead.

YIELD OVER TIME (Temporal Analysis):
- Date range defaults to last 30 days (may be too much for high-volume!)
- Use adaptive_time=True for high-volume production
- Use perspective: "trend", "daily", "weekly", "monthly" for time-series
- Period data can be safely aggregated (first-pass rule applies)

YIELD TREND (Change Detection):
- Yield trend = change compared to previous equally-sized period
- Example: today vs yesterday, this week vs last week
- Useful for improvement/degradation analysis

Example questions this tool answers:
- "What's FCT yield for WIDGET-001?" (test_operation: "FCT")
- "What processes does WIDGET-001 go through?" (perspective: "by operation")
- "What's the RTY for WIDGET-001?" (calculate from by-operation results)
- "Who are the top runners in FCT?" (perspective: "by product", test_operation: "FCT")
- "Compare yield by station" (perspective: "by station")
- "Show daily yield for the past week" (perspective: "daily", days: 7)
- "What's the repair station performance?" (yield_type: "report")
- "Why is ICT showing 0 units?" (check for mixed process problem)

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
        self._process_resolver = None  # Lazy-loaded
        self._adaptive_time = None  # Lazy-loaded
    
    def _get_process_resolver(self):
        """Get process resolver (lazy-loaded)."""
        if self._process_resolver is None:
            from ..shared.process_resolver import ProcessResolver
            self._process_resolver = ProcessResolver(self._api)
        return self._process_resolver
    
    def _get_adaptive_time(self):
        """Get adaptive time filter (lazy-loaded)."""
        if self._adaptive_time is None:
            from ..shared.adaptive_time import AdaptiveTimeFilter
            self._adaptive_time = AdaptiveTimeFilter(self._api)
        return self._adaptive_time
    
    def resolve_process_name(self, user_input: str) -> Optional[str]:
        """
        Resolve a fuzzy process name to the actual process name.
        
        Handles common aliases like "PCBA" -> "PCBA test", "board test" -> "PCBA test".
        
        Args:
            user_input: User's process name (may be imprecise)
            
        Returns:
            Resolved process name, or None if no match found
        """
        resolver = self._get_process_resolver()
        match = resolver.resolve(user_input)
        return match.name if match else None
    
    def get_available_processes(self) -> List[Dict[str, Any]]:
        """
        Get list of available processes for user context.
        
        Returns:
            List of process info dicts with code, name, and type
        """
        resolver = self._get_process_resolver()
        return resolver.get_process_summary()
    
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
                    "description": "Filter by test operation (FCT, EOL, PCBA, board test, etc.). Fuzzy names accepted."
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
                "yield_type": {
                    "type": "string",
                    "enum": ["unit", "report"],
                    "default": "unit",
                    "description": """
Type of yield calculation:
- 'unit' (default): Unit-based yield (FPY/SPY/TPY/LPY). 
  Measures % of UNITS that passed. Units included only if FIRST RUN matches filter.
- 'report': Report-based yield (TRY). 
  Measures passed reports / all reports. Use for retest stations/repair lines.
WARNING: Retest-only stations show 0 units with 'unit' type - use 'report' instead.
                    """.strip()
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
            # Track any resolution messages for summary
            resolution_notes = []
            
            # Resolve fuzzy process name if provided
            resolved_process = None
            if filter_input.test_operation:
                try:
                    resolver = self._get_process_resolver()
                    match = resolver.resolve(filter_input.test_operation)
                    if match:
                        if match.name.lower() != filter_input.test_operation.lower():
                            resolution_notes.append(
                                f"Process '{filter_input.test_operation}' resolved to '{match.name}'"
                            )
                        resolved_process = match.name
                        # Update filter with resolved name
                        filter_input = filter_input.model_copy(
                            update={"test_operation": resolved_process}
                        )
                    else:
                        # No match found, could suggest alternatives
                        candidates = resolver.resolve_with_candidates(filter_input.test_operation)
                        if candidates:
                            suggestions = [c.name for c in candidates[:3]]
                            resolution_notes.append(
                                f"Process '{filter_input.test_operation}' not found. "
                                f"Did you mean: {', '.join(suggestions)}?"
                            )
                except Exception:
                    # Process resolution failed - continue with original value
                    pass
            
            # Handle adaptive time filtering
            adaptive_time_info = None
            if getattr(filter_input, 'adaptive_time', False):
                try:
                    adaptive = self._get_adaptive_time()
                    result = adaptive.calculate_optimal_window(
                        part_number=filter_input.part_number,
                        test_operation=filter_input.test_operation,
                        station_name=filter_input.station_name,
                    )
                    if result:
                        adaptive_time_info = result
                        # Update filter with optimal dates
                        filter_input = filter_input.model_copy(
                            update={
                                "date_from": result.date_from,
                                "date_to": result.date_to,
                                "days": None  # Clear days since we have explicit dates
                            }
                        )
                        resolution_notes.append(
                            f"Adaptive time: Using {result.days_used}-day window "
                            f"({result.volume_category.value} volume, ~{result.estimated_records:,} records)"
                        )
                except Exception:
                    # Adaptive time failed - continue with default
                    resolution_notes.append(
                        "Adaptive time filter failed - using default time range"
                    )
            
            # Build WATS filter
            wats_params = build_wats_filter(filter_input)
            
            # Import here to avoid circular imports
            from pywats.domains.report.models import WATSFilter
            
            wats_filter = WATSFilter(**wats_params)
            
            # Call the appropriate API based on yield_type
            yield_type = getattr(filter_input, 'yield_type', 'unit')
            
            if yield_type == 'report':
                # Report-based yield (TRY) - for retest stations, fixtures, operators
                data = self._api.analytics.get_dynamic_yield(wats_filter)
                # Note: TRY would be computed differently if API supports it
                # For now, use same API but adjust interpretation in summary
            else:
                # Unit-based yield (FPY, SPY, TPY, LPY) - default
                data = self._api.analytics.get_dynamic_yield(wats_filter)
            
            if not data:
                # Check for repair line scenario
                summary = self._build_no_data_summary(filter_input)
                warning = self._check_repair_line_scenario(filter_input)
                if warning:
                    summary += f"\n\n{warning}"
                
                # Check for mixed process problem
                mixed_warning = self._check_mixed_process_problem(filter_input)
                if mixed_warning:
                    summary += f"\n\n{mixed_warning}"
                
                # Add resolution notes
                if resolution_notes:
                    summary = "\n".join(resolution_notes) + "\n\n" + summary
                
                return AgentResult.ok(
                    data=[],
                    summary=summary,
                    metadata={
                        "resolution_notes": resolution_notes,
                        "adaptive_time": adaptive_time_info.__dict__ if adaptive_time_info else None
                    }
                )
            
            # Check for potential repair line issue (0 units but filters applied)
            total_units = sum(getattr(d, 'unit_count', 0) or 0 for d in data)
            warning = None
            mixed_warning = None
            if total_units == 0 and yield_type == 'unit':
                warning = self._check_repair_line_scenario(filter_input)
                mixed_warning = self._check_mixed_process_problem(filter_input)
            
            # Build rich summary
            summary = self._build_summary(data, filter_input, wats_params)
            
            # Add any warnings
            if warning:
                summary += f"\n\n{warning}"
            if mixed_warning:
                summary += f"\n\n{mixed_warning}"
            
            # Prepend resolution notes if any
            if resolution_notes:
                summary = "\n".join(resolution_notes) + "\n\n" + summary
            
            # Resolve perspective for metadata
            perspective = resolve_perspective(filter_input.perspective)
            
            return AgentResult.ok(
                data=[d.model_dump() for d in data],
                summary=summary,
                metadata={
                    "perspective": filter_input.perspective,
                    "resolved_perspective": perspective.value if perspective else None,
                    "yield_type": yield_type,
                    "dimensions": wats_params.get("dimensions"),
                    "record_count": len(data),
                    "total_units": total_units,
                    "repair_line_warning": warning is not None,
                    "mixed_process_warning": mixed_warning is not None,
                    "resolution_notes": resolution_notes,
                    "adaptive_time": adaptive_time_info.__dict__ if adaptive_time_info else None,
                    "filters_applied": {
                        k: v for k, v in wats_params.items() 
                        if k not in ["dimensions", "date_from", "date_to", "date_grouping", "include_current_period"]
                        and v is not None
                    }
                }
            )
            
        except Exception as e:
            return AgentResult.fail(f"Yield analysis failed: {str(e)}")
    
    def _check_repair_line_scenario(self, filter_input: YieldFilter) -> Optional[str]:
        """
        Check if the filter might be hitting the repair line scenario.
        
        The repair line problem occurs when filtering by station/fixture/operator
        that only handles retests (Run 2+), not first runs. In this case,
        unit-based yield will show 0 units because units are only included
        if their FIRST RUN matches the filter.
        
        Returns a warning message if this scenario is detected.
        """
        yield_type = getattr(filter_input, 'yield_type', 'unit')
        
        # Only warn for unit-based yield with station/fixture/operator filters
        if yield_type == 'report':
            return None
        
        # Check if filtering in a way that might hit repair line issue
        has_equipment_filter = any([
            filter_input.station_name,
            filter_input.operator,
        ])
        
        # Also check perspective - by_fixture, by_operator could be affected
        perspective = filter_input.perspective or ""
        has_equipment_perspective = any(p in perspective.lower() for p in [
            "fixture", "operator"
        ])
        
        if has_equipment_filter or has_equipment_perspective:
            return (
                "NOTE: If you're seeing 0 units, this station/fixture/operator might be "
                "a retest-only location (repair line). Units are counted only if their FIRST RUN "
                "matches your filter. For retest station performance, try using yield_type='report' "
                "to get Test Report Yield (TRY) instead of unit-based yield."
            )
        
        return None
    
    def _check_mixed_process_problem(self, filter_input: YieldFilter) -> Optional[str]:
        """
        Check if the filter might be hitting the mixed process problem.
        
        The mixed process problem occurs when customers send different test types
        (e.g., AOI and ICT) to the same process/test_operation. In this case:
        - The first test type (e.g., AOI) determines unit counts and FPY
        - Subsequent test types (e.g., ICT) are treated as "retests after pass"
        - This causes the second test to show 0 units and no FPY/LPY
        
        DIAGNOSIS: Look for reports with different sw_filename in the same process.
        
        Returns a warning message if this scenario might be relevant.
        """
        # Only relevant when filtering by test_operation and getting 0 units
        if not filter_input.test_operation:
            return None
        
        # Try to diagnose using the process resolver
        try:
            from ..shared.process_resolver import diagnose_mixed_process_problem
            diagnosis = diagnose_mixed_process_problem(
                self._api,
                test_operation=filter_input.test_operation,
                part_number=filter_input.part_number
            )
            if diagnosis:
                return diagnosis
        except Exception:
            # Diagnosis failed - return generic warning
            pass
        
        # Generic warning if we can't diagnose but might be relevant
        return (
            "NOTE: If you're seeing 0 units for a process that should have data, "
            "check if multiple test types (e.g., AOI, ICT) are being sent to the same process. "
            "This 'mixed process' problem causes the second test type to show 0 units. "
            "Look for different sw_filename values in reports to this process."
        )
    
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
        
        # Get yield type
        yield_type = getattr(filter_input, 'yield_type', 'unit')
        
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
        
        # Yield type indicator
        if yield_type == 'report':
            yield_type_desc = " (Report-based TRY)"
        else:
            yield_type_desc = " (Unit-based FPY)"
        
        # Build the summary
        parts = [f"Yield analysis{context}{perspective_desc}{yield_type_desc} (last {filter_input.days} days):"]
        
        if avg_fpy is not None:
            if yield_type == 'report':
                parts.append(f"* Average TRY: {avg_fpy:.1f}%")
            else:
                parts.append(f"* Average FPY: {avg_fpy:.1f}%")
        parts.append(f"* Total units: {total_units:,}")
        parts.append(f"* Data points: {len(data)}")
        
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
                    parts.append(f"* Best: {best_label} ({best_fpy:.1f}%)")
                if worst_fpy is not None and worst_label:
                    parts.append(f"* Worst: {worst_label} ({worst_fpy:.1f}%)")
        
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
