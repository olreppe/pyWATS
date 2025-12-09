"""Asset data models.

Pure data models with no business logic.
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import Field

from ...shared import PyWATSModel, Setting
from .enums import AssetState, AssetLogType


class AssetType(PyWATSModel):
    """
    Represents an asset type in WATS.

    Attributes:
        type_id: Unique identifier
        type_name: Name of the asset type
        running_count_limit: Max count until next calibration
        total_count_limit: Asset total count limit
        maintenance_interval: Interval for maintenance (in days)
        calibration_interval: Interval for calibration (in days)
        warning_threshold: Warning threshold percent
        alarm_threshold: Alarm threshold percent
        is_readonly: Whether the type is read-only
        icon: Icon identifier
    """
    type_name: str = Field(..., alias="typeName")
    type_id: Optional[UUID] = Field(default=None, alias="typeId")
    running_count_limit: Optional[int] = Field(
        default=None, alias="runningCountLimit"
    )
    total_count_limit: Optional[int] = Field(
        default=None, alias="totalCountLimit"
    )
    maintenance_interval: Optional[float] = Field(
        default=None, alias="maintenanceInterval"
    )
    calibration_interval: Optional[float] = Field(
        default=None, alias="calibrationInterval"
    )
    warning_threshold: Optional[float] = Field(
        default=None, alias="warningThreshold"
    )
    alarm_threshold: Optional[float] = Field(
        default=None, alias="alarmThreshold"
    )
    is_readonly: bool = Field(default=False, alias="isReadonly")
    icon: Optional[str] = Field(default=None, alias="icon")


class AssetLog(PyWATSModel):
    """
    Represents an asset log entry.

    Attributes:
        log_id: Log entry ID
        asset_id: ID of the asset
        serial_number: Asset serial number
        date: Log entry date
        user: User who made the entry
        log_type: Type of log entry
        comment: Log entry comment
    """
    log_id: Optional[int] = Field(default=None, alias="logId")
    asset_id: Optional[str] = Field(default=None, alias="assetId")
    serial_number: Optional[str] = Field(default=None, alias="serialNumber")
    date: Optional[datetime] = Field(default=None, alias="date")
    user: Optional[str] = Field(default=None, alias="user")
    log_type: Optional[AssetLogType] = Field(default=None, alias="type")
    comment: Optional[str] = Field(default=None, alias="comment")


class Asset(PyWATSModel):
    """
    Represents an asset in WATS.

    Attributes:
        serial_number: Asset serial number (required)
        type_id: Asset type ID (required)
        asset_id: Unique identifier
        parent_asset_id: Parent asset ID (for hierarchical assets)
        parent_serial_number: Parent asset serial number
        asset_name: Asset name
        part_number: Part number
        revision: Revision
        client_id: Client ID
        state: Asset state
        description: Description
        location: Location
        first_seen_date: First seen date
        last_seen_date: Last seen date
        last_maintenance_date: Last maintenance date
        next_maintenance_date: Next maintenance date
        last_calibration_date: Last calibration date
        next_calibration_date: Next calibration date
        total_count: Total usage count
        running_count: Running count since last calibration
        tags: Custom key-value tags
        asset_children: Child assets
        asset_type: Asset type details
        asset_log: Log entries
    """
    serial_number: str = Field(..., alias="serialNumber")
    type_id: Optional[UUID] = Field(default=None, alias="typeId")
    asset_id: Optional[str] = Field(default=None, alias="assetId")
    parent_asset_id: Optional[str] = Field(default=None, alias="parentAssetId")
    parent_serial_number: Optional[str] = Field(
        default=None, alias="parentSerialNumber"
    )
    asset_name: Optional[str] = Field(default=None, alias="assetName")
    part_number: Optional[str] = Field(default=None, alias="partNumber")
    revision: Optional[str] = Field(default=None, alias="revision")
    client_id: Optional[int] = Field(default=None, alias="ClientId")
    state: AssetState = Field(default=AssetState.OK, alias="state")
    description: Optional[str] = Field(default=None, alias="description")
    location: Optional[str] = Field(default=None, alias="location")
    first_seen_date: Optional[datetime] = Field(
        default=None, alias="firstSeenDate"
    )
    last_seen_date: Optional[datetime] = Field(
        default=None, alias="lastSeenDate"
    )
    last_maintenance_date: Optional[datetime] = Field(
        default=None, alias="lastMaintenanceDate"
    )
    next_maintenance_date: Optional[datetime] = Field(
        default=None, alias="nextMaintenanceDate"
    )
    last_calibration_date: Optional[datetime] = Field(
        default=None, alias="lastCalibrationDate"
    )
    next_calibration_date: Optional[datetime] = Field(
        default=None, alias="nextCalibrationDate"
    )
    total_count: Optional[int] = Field(default=None, alias="totalCount")
    running_count: Optional[int] = Field(default=None, alias="runningCount")
    tags: List[Setting] = Field(default_factory=list, alias="tags")
    asset_children: List["Asset"] = Field(
        default_factory=list, alias="assetChildren"
    )
    asset_type: Optional[AssetType] = Field(default=None, alias="assetType")
    asset_log: List[AssetLog] = Field(default_factory=list, alias="assetLog")
