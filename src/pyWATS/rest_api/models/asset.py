"""
Asset Models

Models for asset management endpoints.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import IntEnum
from uuid import UUID

from .common import PublicWatsFilter


class AssetState(IntEnum):
    """Asset state enumeration."""
    UNKNOWN = 0
    IN_OPERATION = 1
    IN_TRANSIT = 2
    IN_MAINTENANCE = 3
    IN_CALIBRATION = 4
    IN_STORAGE = 5
    SCRAPPED = 6


class AssetLogType(IntEnum):
    """Asset log type enumeration."""
    MESSAGE = 0
    REGISTER = 1
    UPDATE = 2
    RESET_COUNT = 3
    CALIBRATION = 4
    MAINTENANCE = 5


class Setting(BaseModel):
    """Key-value setting model."""
    key: Optional[str] = None
    value: Optional[str] = None
    change: Optional[int] = None


class AssetType(BaseModel):
    """Asset type model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    type_id: Optional[UUID] = Field(None, alias="typeId")
    type_name: str = Field(..., alias="typeName")
    running_count_limit: Optional[int] = Field(None, alias="runningCountLimit")
    total_count_limit: Optional[int] = Field(None, alias="totalCountLimit")
    maintenance_interval: Optional[float] = Field(None, alias="maintenanceInterval")
    calibration_interval: Optional[float] = Field(None, alias="calibrationInterval")
    warning_threshold: Optional[float] = Field(None, alias="warningThreshold")
    alarm_threshold: Optional[float] = Field(None, alias="alarmThreshold")
    is_readonly: Optional[bool] = Field(None, alias="isReadonly")
    icon: Optional[str] = None


class AssetLog(BaseModel):
    """Asset log entry model."""
    
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )
    
    log_id: Optional[int] = Field(None, alias="logId")
    asset_id: Optional[str] = Field(None, alias="assetId")
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    date: Optional[datetime] = None
    user: Optional[str] = None
    type: Optional[AssetLogType] = None
    property: Optional[str] = None
    value: Optional[str] = None
    comment: Optional[str] = None


class Asset(BaseModel):
    """Asset model."""
    
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )
    
    asset_id: Optional[str] = Field(None, alias="assetId")
    parent_asset_id: Optional[str] = Field(None, alias="parentAssetId")
    serial_number: str = Field(..., alias="serialNumber")
    parent_serial_number: Optional[str] = Field(None, alias="parentSerialNumber")
    asset_name: Optional[str] = Field(None, alias="assetName")
    part_number: Optional[str] = Field(None, alias="partNumber")
    revision: Optional[str] = None
    type_id: UUID = Field(..., alias="typeId")
    client_id: Optional[int] = Field(None, alias="ClientId")
    state: Optional[AssetState] = None
    description: Optional[str] = None
    location: Optional[str] = None
    first_seen_date: Optional[datetime] = Field(None, alias="firstSeenDate")
    last_seen_date: Optional[datetime] = Field(None, alias="lastSeenDate")
    last_maintenance_date: Optional[datetime] = Field(None, alias="lastMaintenanceDate")
    next_maintenance_date: Optional[datetime] = Field(None, alias="nextMaintenanceDate")
    last_calibration_date: Optional[datetime] = Field(None, alias="lastCalibrationDate")
    next_calibration_date: Optional[datetime] = Field(None, alias="nextCalibrationDate")
    total_count: Optional[int] = Field(None, alias="totalCount")
    running_count: Optional[int] = Field(None, alias="runningCount")
    tags: Optional[List[Setting]] = []
    asset_children: Optional[List['Asset']] = Field([], alias="assetChildren")
    asset_type: Optional[AssetType] = Field(None, alias="assetType")
    asset_log: Optional[List[AssetLog]] = Field([], alias="assetLog")


class AssetMessage(BaseModel):
    """Asset message model for posting messages."""
    content: str


# Forward reference update
Asset.model_rebuild()