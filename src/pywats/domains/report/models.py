"""Report domain models - filter and header classes for querying.

FIELD NAMING CONVENTION:
------------------------
All fields use Python snake_case naming (e.g., part_number, station_name).
Backend API aliases (camelCase) are handled automatically.
Always use the Python field names when creating or accessing these models.
"""
from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import Field, AliasChoices, field_serializer, field_validator

from ...shared import PyWATSModel
from .enums import DateGrouping


class WATSFilter(PyWATSModel):
    """
    WATS filter for querying reports and statistics.
    
    This filter is used across multiple API endpoints to query reports,
    yield statistics, and analytics data. All fields are optional - 
    only specify the fields you want to filter by.
    
    IMPORTANT: Use Python field names (snake_case), not camelCase aliases.
    
    Filter Fields (all optional):
    -----------------------------
    Identity Filters:
        serial_number (str): Filter by exact serial number match
        part_number (str): Filter by product part number
        revision (str): Filter by product revision
        batch_number (str): Filter by production batch number
        
    Location/Operation Filters:
        station_name (str): Filter by test station name
        test_operation (str): Filter by test operation name (e.g., "End of line test")
        level (str): Filter by production level (e.g., "PCBA", "Module")
        
    Status Filters:
        status (str): Filter by result status. Values: "Passed", "Failed", "Error", 
                      or None/empty for all. Note: "all" is treated as unset.
        yield_value (int): Filter by yield percentage (0-100)
        
    Product Filters:
        product_group (str): Filter by product group name
        
    Software Filters:
        sw_filename (str): Filter by test software filename
        sw_version (str): Filter by test software version
        
    Misc Info Filters:
        misc_description (str): Filter by misc info description field
        misc_value (str): Filter by misc info value field
        socket (str): Filter by socket/fixture identifier
        
    Date Range Filters:
        date_from (datetime): Start of date range (inclusive)
        date_to (datetime): End of date range (inclusive)
        
    Aggregation Options:
        date_grouping (DateGrouping): How to group results by time period.
            Values: HOUR, DAY, WEEK, MONTH, QUARTER, YEAR
        period_count (int): Number of periods to return (default varies by endpoint)
        include_current_period (bool): Whether to include the current incomplete period
        
    Result Limiting:
        max_count (int): Maximum number of results to return
        min_count (int): Minimum count threshold for filtering
        top_count (int): Return only top N results
        
    Advanced Options:
        dimensions (str): Custom dimensions string for dynamic queries.
            Comma-separated list: "partNumber,stationName,period"
            Valid dimensions: partNumber, productName, stationName, location,
            purpose, revision, testOperation, processCode, swFilename, swVersion,
            productGroup, level, period, batchNumber, operator, fixtureId
        run (int): Run filter for step analysis.
            Values: 1=first run, 2=second, 3=third, -1=last run, -2=all runs
    
    Example:
        >>> # Filter reports from last 7 days for a specific part
        >>> from datetime import datetime, timedelta
        >>> filter = WATSFilter(
        ...     part_number="WIDGET-001",
        ...     date_from=datetime.now() - timedelta(days=7),
        ...     status="Failed",
        ...     max_count=100
        ... )
        >>> 
        >>> # Get yield by station for a product group
        >>> filter = WATSFilter(
        ...     product_group="Electronics",
        ...     dimensions="stationName,period",
        ...     date_grouping=DateGrouping.DAY,
        ...     period_count=30
        ... )
    """
    serial_number: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("serialNumber", "serial_number"),
        serialization_alias="serialNumber",
        description="Filter by exact serial number match"
    )
    part_number: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("partNumber", "part_number"),
        serialization_alias="partNumber",
        description="Filter by product part number"
    )
    revision: Optional[str] = Field(
        default=None,
        description="Filter by product revision"
    )
    batch_number: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("batchNumber", "batch_number"),
        serialization_alias="batchNumber",
        description="Filter by production batch number"
    )
    station_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("stationName", "station_name"),
        serialization_alias="stationName",
        description="Filter by test station name"
    )
    test_operation: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("testOperation", "test_operation"),
        serialization_alias="testOperation",
        description="Filter by test operation name"
    )
    status: Optional[str] = Field(
        default=None,
        description="Filter by result status: 'Passed', 'Failed', 'Error', or None for all"
    )
    yield_value: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("yield", "yield_value"),
        serialization_alias="yield",
        description="Filter by yield percentage (0-100)"
    )
    misc_description: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("miscDescription", "misc_description"),
        serialization_alias="miscDescription",
        description="Filter by misc info description field"
    )
    misc_value: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("miscValue", "misc_value"),
        serialization_alias="miscValue",
        description="Filter by misc info value field"
    )
    product_group: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("productGroup", "product_group"),
        serialization_alias="productGroup",
        description="Filter by product group name"
    )
    level: Optional[str] = Field(
        default=None,
        description="Filter by production level (e.g., 'PCBA', 'Module')"
    )
    sw_filename: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("swFilename", "sw_filename"),
        serialization_alias="swFilename",
        description="Filter by test software filename"
    )
    sw_version: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("swVersion", "sw_version"),
        serialization_alias="swVersion",
        description="Filter by test software version"
    )
    socket: Optional[str] = Field(
        default=None,
        description="Filter by socket/fixture identifier"
    )
    date_from: Optional[datetime] = Field(
        default=None,
        validation_alias=AliasChoices("dateFrom", "date_from"),
        serialization_alias="dateFrom",
        description="Start of date range filter (inclusive)"
    )
    date_to: Optional[datetime] = Field(
        default=None,
        validation_alias=AliasChoices("dateTo", "date_to"),
        serialization_alias="dateTo",
        description="End of date range filter (inclusive)"
    )
    date_grouping: Optional[DateGrouping] = Field(
        default=None,
        validation_alias=AliasChoices("dateGrouping", "date_grouping"),
        serialization_alias="dateGrouping",
        description="Time period grouping: HOUR, DAY, WEEK, MONTH, QUARTER, YEAR"
    )
    period_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("periodCount", "period_count"),
        serialization_alias="periodCount",
        description="Number of time periods to return"
    )
    include_current_period: Optional[bool] = Field(
        default=None,
        validation_alias=AliasChoices(
            "includeCurrentPeriod", "include_current_period"
        ),
        serialization_alias="includeCurrentPeriod",
        description="Whether to include current incomplete period"
    )
    max_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("maxCount", "max_count"),
        serialization_alias="maxCount",
        description="Maximum number of results to return"
    )
    min_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("minCount", "min_count"),
        serialization_alias="minCount",
        description="Minimum count threshold for filtering"
    )
    top_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("topCount", "top_count"),
        serialization_alias="topCount",
        description="Return only top N results"
    )
    dimensions: Optional[str] = Field(
        default=None,
        description="Comma-separated dimension list for dynamic queries"
    )

    # Used by some analytics endpoints (e.g. App/TestStepAnalysis)
    run: Optional[int] = Field(
        default=None,
        description="Run filter: 1=first, 2=second, 3=third, -1=last, -2=all"
    )

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status_all(cls, v: object) -> object:
        """Treat status='all' as unset.

        Some WATS servers interpret the literal string 'all' as an actual status
        value and return empty result sets.
        """
        if v is None:
            return None
        if isinstance(v, str) and v.strip().lower() == "all":
            return None
        return v

    @field_serializer('date_from', 'date_to')
    def serialize_datetime(self, v: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO format."""
        return v.isoformat() if v else None


class ReportHeader(PyWATSModel):
    """
    Represents a report header (summary info).

    Attributes:
        uuid: Report unique identifier
        serial_number: Unit serial number
        part_number: Product part number
        revision: Product revision
        batch_number: Batch number
        station_name: Test station name
        test_operation: Test operation name
        status: Report status
        start_utc: Test start time
        root_node_type: Root node type
        operator: Operator name
    """
    uuid: Optional[UUID] = Field(default=None)
    serial_number: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("serialNumber", "serial_number"),
        serialization_alias="serialNumber"
    )
    part_number: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("partNumber", "part_number"),
        serialization_alias="partNumber"
    )
    revision: Optional[str] = Field(default=None)
    batch_number: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("batchNumber", "batch_number"),
        serialization_alias="batchNumber"
    )
    station_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("stationName", "station_name"),
        serialization_alias="stationName"
    )
    test_operation: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("testOperation", "test_operation"),
        serialization_alias="testOperation"
    )
    status: Optional[str] = Field(default=None)
    start_utc: Optional[datetime] = Field(
        default=None,
        validation_alias=AliasChoices("startUtc", "start_utc"),
        serialization_alias="startUtc"
    )
    root_node_type: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("rootNodeType", "root_node_type"),
        serialization_alias="rootNodeType"
    )
    operator: Optional[str] = Field(default=None)


class Attachment(PyWATSModel):
    """
    Represents a report attachment.

    Attributes:
        attachment_id: Attachment ID
        file_name: Original filename
        mime_type: MIME type
        size: File size in bytes
        description: Attachment description
    """
    attachment_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("attachmentId", "attachment_id"),
        serialization_alias="attachmentId"
    )
    file_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("fileName", "file_name"),
        serialization_alias="fileName"
    )
    mime_type: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("mimeType", "mime_type"),
        serialization_alias="mimeType"
    )
    size: Optional[int] = Field(default=None)
    description: Optional[str] = Field(default=None)


# Re-export the core report structures so importing `pywats.domains.report.models` also pulls in
# the essential UUT/UUR types (avoids accidentally leaving them out).
from .report_models import (
    Report,
    ReportStatus,
    ReportInfo,
    AdditionalData,
    BinaryData,
    Asset,
    AssetStats,
    Chart,
    ChartSeries,
    ChartType,
    SubUnit,
    Attachment as ReportAttachment,
    DeserializationContext,
    UUTReport,
    UURReport,
)
