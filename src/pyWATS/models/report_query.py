"""
Report query models for pyWATS

Uses Pydantic 2 for validation and serialization.
"""
from typing import Optional
from datetime import datetime
from enum import IntEnum
from uuid import UUID
from pydantic import Field, field_serializer

from .common import PyWATSModel


class DateGrouping(IntEnum):
    """Date grouping options for filters"""
    NONE = -1
    YEAR = 0
    QUARTER = 1
    MONTH = 2
    WEEK = 3
    DAY = 4
    HOUR = 5


class WATSFilter(PyWATSModel):
    """
    WATS filter for querying reports and statistics.
    
    Attributes:
        serial_number: Filter by serial number
        part_number: Filter by part number
        revision: Filter by revision
        batch_number: Filter by batch number
        station_name: Filter by station name
        test_operation: Filter by test operation
        status: Filter by status
        yield_value: Filter by yield percentage
        misc_description: Filter by misc info description
        misc_value: Filter by misc info value
        product_group: Filter by product group
        level: Filter by level
        sw_filename: Filter by software filename
        sw_version: Filter by software version
        socket: Filter by socket
        date_from: Filter by start date
        date_to: Filter by end date
        date_grouping: Date grouping option
        period_count: Number of periods
        include_current_period: Include current period
        max_count: Maximum results
        min_count: Minimum count filter
        top_count: Top N results
        dimensions: Custom dimensions string
    """
    serial_number: Optional[str] = Field(default=None, alias="serialNumber")
    part_number: Optional[str] = Field(default=None, alias="partNumber")
    revision: Optional[str] = Field(default=None, alias="revision")
    batch_number: Optional[str] = Field(default=None, alias="batchNumber")
    station_name: Optional[str] = Field(default=None, alias="stationName")
    test_operation: Optional[str] = Field(default=None, alias="testOperation")
    status: Optional[str] = Field(default=None, alias="status")
    yield_value: Optional[int] = Field(default=None, alias="yield")
    misc_description: Optional[str] = Field(
        default=None, alias="miscDescription"
    )
    misc_value: Optional[str] = Field(default=None, alias="miscValue")
    product_group: Optional[str] = Field(default=None, alias="productGroup")
    level: Optional[str] = Field(default=None, alias="level")
    sw_filename: Optional[str] = Field(default=None, alias="swFilename")
    sw_version: Optional[str] = Field(default=None, alias="swVersion")
    socket: Optional[str] = Field(default=None, alias="socket")
    date_from: Optional[datetime] = Field(default=None, alias="dateFrom")
    date_to: Optional[datetime] = Field(default=None, alias="dateTo")
    date_grouping: Optional[DateGrouping] = Field(
        default=None, alias="dateGrouping"
    )
    period_count: Optional[int] = Field(default=None, alias="periodCount")
    include_current_period: Optional[bool] = Field(
        default=None, alias="includeCurrentPeriod"
    )
    max_count: Optional[int] = Field(default=None, alias="maxCount")
    min_count: Optional[int] = Field(default=None, alias="minCount")
    top_count: Optional[int] = Field(default=None, alias="topCount")
    dimensions: Optional[str] = Field(default=None, alias="dimensions")

    @field_serializer('date_from', 'date_to')
    def serialize_datetime(self, v: Optional[datetime]) -> Optional[str]:
        """Serialize datetime to ISO format"""
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
    uuid: Optional[UUID] = Field(default=None, alias="uuid")
    serial_number: Optional[str] = Field(default=None, alias="serialNumber")
    part_number: Optional[str] = Field(default=None, alias="partNumber")
    revision: Optional[str] = Field(default=None, alias="revision")
    batch_number: Optional[str] = Field(default=None, alias="batchNumber")
    station_name: Optional[str] = Field(default=None, alias="stationName")
    test_operation: Optional[str] = Field(default=None, alias="testOperation")
    status: Optional[str] = Field(default=None, alias="status")
    start_utc: Optional[datetime] = Field(default=None, alias="startUtc")
    root_node_type: Optional[str] = Field(default=None, alias="rootNodeType")
    operator: Optional[str] = Field(default=None, alias="operator")


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
    attachment_id: Optional[int] = Field(default=None, alias="attachmentId")
    file_name: Optional[str] = Field(default=None, alias="fileName")
    mime_type: Optional[str] = Field(default=None, alias="mimeType")
    size: Optional[int] = Field(default=None, alias="size")
    description: Optional[str] = Field(default=None, alias="description")


class YieldData(PyWATSModel):
    """
    Represents yield statistics data.
    
    Attributes:
        part_number: Product part number
        revision: Product revision
        product_name: Product name
        product_group: Product group
        station_name: Test station name
        test_operation: Test operation
        period: Time period
        unit_count: Total unit count
        fp_count: First pass count
        sp_count: Second pass count
        tp_count: Third pass count
        lp_count: Last pass count
        fpy: First pass yield
        spy: Second pass yield
        tpy: Third pass yield
        lpy: Last pass yield
    """
    part_number: Optional[str] = Field(default=None, alias="partNumber")
    revision: Optional[str] = Field(default=None, alias="revision")
    product_name: Optional[str] = Field(default=None, alias="productName")
    product_group: Optional[str] = Field(default=None, alias="productGroup")
    station_name: Optional[str] = Field(default=None, alias="stationName")
    test_operation: Optional[str] = Field(default=None, alias="testOperation")
    period: Optional[str] = Field(default=None, alias="period")
    unit_count: Optional[int] = Field(default=None, alias="unitCount")
    fp_count: Optional[int] = Field(default=None, alias="fpCount")
    sp_count: Optional[int] = Field(default=None, alias="spCount")
    tp_count: Optional[int] = Field(default=None, alias="tpCount")
    lp_count: Optional[int] = Field(default=None, alias="lpCount")
    fpy: Optional[float] = Field(default=None, alias="fpy")
    spy: Optional[float] = Field(default=None, alias="spy")
    tpy: Optional[float] = Field(default=None, alias="tpy")
    lpy: Optional[float] = Field(default=None, alias="lpy")


class ProcessInfo(PyWATSModel):
    """
    Represents process/test operation information.
    
    Attributes:
        process_code: Process code
        process_name: Process name
        process_index: Process order index
    """
    process_code: Optional[int] = Field(default=None, alias="processCode")
    process_name: Optional[str] = Field(default=None, alias="processName")
    process_index: Optional[int] = Field(default=None, alias="processIndex")


class LevelInfo(PyWATSModel):
    """
    Represents production level information.
    
    Attributes:
        level_id: Level ID
        level_name: Level name
    """
    level_id: Optional[int] = Field(default=None, alias="levelId")
    level_name: Optional[str] = Field(default=None, alias="levelName")


class ProductGroup(PyWATSModel):
    """
    Represents a product group.
    
    Attributes:
        product_group_id: Product group ID
        product_group_name: Product group name
    """
    product_group_id: Optional[int] = Field(
        default=None, alias="productGroupId"
    )
    product_group_name: Optional[str] = Field(
        default=None, alias="productGroupName"
    )
