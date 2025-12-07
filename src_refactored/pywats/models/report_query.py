"""
Report models for pyWATS
"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import IntEnum
from uuid import UUID


class DateGrouping(IntEnum):
    """Date grouping options for filters"""
    NONE = -1
    YEAR = 0
    QUARTER = 1
    MONTH = 2
    WEEK = 3
    DAY = 4
    HOUR = 5


@dataclass
class WATSFilter:
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
    serial_number: Optional[str] = None
    part_number: Optional[str] = None
    revision: Optional[str] = None
    batch_number: Optional[str] = None
    station_name: Optional[str] = None
    test_operation: Optional[str] = None
    status: Optional[str] = None
    yield_value: Optional[int] = None
    misc_description: Optional[str] = None
    misc_value: Optional[str] = None
    product_group: Optional[str] = None
    level: Optional[str] = None
    sw_filename: Optional[str] = None
    sw_version: Optional[str] = None
    socket: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    date_grouping: Optional[DateGrouping] = None
    period_count: Optional[int] = None
    include_current_period: Optional[bool] = None
    max_count: Optional[int] = None
    min_count: Optional[int] = None
    top_count: Optional[int] = None
    dimensions: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for API requests"""
        result = {}
        
        if self.serial_number:
            result["serialNumber"] = self.serial_number
        if self.part_number:
            result["partNumber"] = self.part_number
        if self.revision:
            result["revision"] = self.revision
        if self.batch_number:
            result["batchNumber"] = self.batch_number
        if self.station_name:
            result["stationName"] = self.station_name
        if self.test_operation:
            result["testOperation"] = self.test_operation
        if self.status:
            result["status"] = self.status
        if self.yield_value is not None:
            result["yield"] = self.yield_value
        if self.misc_description:
            result["miscDescription"] = self.misc_description
        if self.misc_value:
            result["miscValue"] = self.misc_value
        if self.product_group:
            result["productGroup"] = self.product_group
        if self.level:
            result["level"] = self.level
        if self.sw_filename:
            result["swFilename"] = self.sw_filename
        if self.sw_version:
            result["swVersion"] = self.sw_version
        if self.socket:
            result["socket"] = self.socket
        if self.date_from:
            result["dateFrom"] = self.date_from.isoformat()
        if self.date_to:
            result["dateTo"] = self.date_to.isoformat()
        if self.date_grouping is not None:
            result["dateGrouping"] = self.date_grouping.value
        if self.period_count is not None:
            result["periodCount"] = self.period_count
        if self.include_current_period is not None:
            result["includeCurrentPeriod"] = self.include_current_period
        if self.max_count is not None:
            result["maxCount"] = self.max_count
        if self.min_count is not None:
            result["minCount"] = self.min_count
        if self.top_count is not None:
            result["topCount"] = self.top_count
        if self.dimensions:
            result["dimensions"] = self.dimensions
            
        return result


@dataclass
class ReportHeader:
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
    uuid: Optional[UUID] = None
    serial_number: Optional[str] = None
    part_number: Optional[str] = None
    revision: Optional[str] = None
    batch_number: Optional[str] = None
    station_name: Optional[str] = None
    test_operation: Optional[str] = None
    status: Optional[str] = None
    start_utc: Optional[datetime] = None
    root_node_type: Optional[str] = None
    operator: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ReportHeader":
        """Create ReportHeader from API response dictionary"""
        start_utc = None
        if data.get("startUtc"):
            try:
                start_utc = datetime.fromisoformat(data["startUtc"].replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
                
        return cls(
            uuid=UUID(data["uuid"]) if data.get("uuid") else None,
            serial_number=data.get("serialNumber"),
            part_number=data.get("partNumber"),
            revision=data.get("revision"),
            batch_number=data.get("batchNumber"),
            station_name=data.get("stationName"),
            test_operation=data.get("testOperation"),
            status=data.get("status"),
            start_utc=start_utc,
            root_node_type=data.get("rootNodeType"),
            operator=data.get("operator")
        )


@dataclass
class Attachment:
    """
    Represents a report attachment.
    
    Attributes:
        attachment_id: Attachment ID
        file_name: Original filename
        mime_type: MIME type
        size: File size in bytes
        description: Attachment description
    """
    attachment_id: Optional[int] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Attachment":
        """Create Attachment from API response dictionary"""
        return cls(
            attachment_id=data.get("attachmentId") or data.get("id"),
            file_name=data.get("fileName") or data.get("filename"),
            mime_type=data.get("mimeType") or data.get("contentType"),
            size=data.get("size"),
            description=data.get("description")
        )


@dataclass
class YieldData:
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
    part_number: Optional[str] = None
    revision: Optional[str] = None
    product_name: Optional[str] = None
    product_group: Optional[str] = None
    station_name: Optional[str] = None
    test_operation: Optional[str] = None
    period: Optional[str] = None
    unit_count: Optional[int] = None
    fp_count: Optional[int] = None
    sp_count: Optional[int] = None
    tp_count: Optional[int] = None
    lp_count: Optional[int] = None
    fpy: Optional[float] = None
    spy: Optional[float] = None
    tpy: Optional[float] = None
    lpy: Optional[float] = None

    @classmethod
    def from_dict(cls, data: dict) -> "YieldData":
        """Create YieldData from API response dictionary"""
        return cls(
            part_number=data.get("partNumber"),
            revision=data.get("revision"),
            product_name=data.get("productName"),
            product_group=data.get("productGroup"),
            station_name=data.get("stationName"),
            test_operation=data.get("testOperation"),
            period=data.get("period"),
            unit_count=data.get("unitCount"),
            fp_count=data.get("fpCount"),
            sp_count=data.get("spCount"),
            tp_count=data.get("tpCount"),
            lp_count=data.get("lpCount"),
            fpy=data.get("fpy"),
            spy=data.get("spy"),
            tpy=data.get("tpy"),
            lpy=data.get("lpy")
        )


@dataclass
class ProcessInfo:
    """
    Represents process/test operation information.
    
    Attributes:
        process_code: Process code
        process_name: Process name
        process_index: Process order index
    """
    process_code: Optional[int] = None
    process_name: Optional[str] = None
    process_index: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ProcessInfo":
        """Create ProcessInfo from API response dictionary"""
        return cls(
            process_code=data.get("processCode") or data.get("code"),
            process_name=data.get("processName") or data.get("name"),
            process_index=data.get("processIndex") or data.get("index")
        )


@dataclass
class LevelInfo:
    """
    Represents production level information.
    
    Attributes:
        level_id: Level ID
        level_name: Level name
    """
    level_id: Optional[int] = None
    level_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "LevelInfo":
        """Create LevelInfo from API response dictionary"""
        return cls(
            level_id=data.get("levelId") or data.get("id"),
            level_name=data.get("levelName") or data.get("name")
        )


@dataclass
class ProductGroup:
    """
    Represents a product group.
    
    Attributes:
        product_group_id: Product group ID
        product_group_name: Product group name
    """
    product_group_id: Optional[int] = None
    product_group_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ProductGroup":
        """Create ProductGroup from API response dictionary"""
        return cls(
            product_group_id=data.get("productGroupId") or data.get("id"),
            product_group_name=data.get("productGroupName") or data.get("name")
        )
