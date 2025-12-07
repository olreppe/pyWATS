"""
Asset models for pyWATS
"""
from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict
from uuid import UUID
from datetime import datetime
from enum import IntEnum

from .common import Setting


class AssetState(IntEnum):
    """Asset state enumeration"""
    UNKNOWN = 0
    OK = 1
    WARNING = 2
    ALERT = 3
    NEEDS_MAINTENANCE = 4
    NEEDS_CALIBRATION = 5
    DISABLED = 6


class AssetLogType(IntEnum):
    """Asset log entry type"""
    UNKNOWN = 0
    CREATED = 1
    CALIBRATION = 2
    MAINTENANCE = 3
    STATE_CHANGE = 4
    COUNT_RESET = 5
    COMMENT = 6


@dataclass
class AssetType:
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
    type_name: str
    type_id: Optional[UUID] = None
    running_count_limit: Optional[int] = None
    total_count_limit: Optional[int] = None
    maintenance_interval: Optional[float] = None
    calibration_interval: Optional[float] = None
    warning_threshold: Optional[float] = None
    alarm_threshold: Optional[float] = None
    is_readonly: bool = False
    icon: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "AssetType":
        """Create AssetType from API response dictionary"""
        return cls(
            type_id=UUID(data["typeId"]) if data.get("typeId") else None,
            type_name=data.get("typeName", ""),
            running_count_limit=data.get("runningCountLimit"),
            total_count_limit=data.get("totalCountLimit"),
            maintenance_interval=data.get("maintenanceInterval"),
            calibration_interval=data.get("calibrationInterval"),
            warning_threshold=data.get("warningThreshold"),
            alarm_threshold=data.get("alarmThreshold"),
            is_readonly=data.get("isReadonly", False),
            icon=data.get("icon")
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""
        result: Dict[str, Any] = {"typeName": self.type_name}
        
        if self.type_id:
            result["typeId"] = str(self.type_id)
        if self.running_count_limit is not None:
            result["runningCountLimit"] = self.running_count_limit
        if self.total_count_limit is not None:
            result["totalCountLimit"] = self.total_count_limit
        if self.maintenance_interval is not None:
            result["maintenanceInterval"] = self.maintenance_interval
        if self.calibration_interval is not None:
            result["calibrationInterval"] = self.calibration_interval
        if self.warning_threshold is not None:
            result["warningThreshold"] = self.warning_threshold
        if self.alarm_threshold is not None:
            result["alarmThreshold"] = self.alarm_threshold
        if self.icon:
            result["icon"] = self.icon
            
        return result


@dataclass
class AssetLog:
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
    log_id: Optional[int] = None
    asset_id: Optional[str] = None
    serial_number: Optional[str] = None
    date: Optional[datetime] = None
    user: Optional[str] = None
    log_type: Optional[AssetLogType] = None
    comment: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "AssetLog":
        """Create AssetLog from API response dictionary"""
        date_str = data.get("date")
        date_val = None
        if date_str:
            try:
                date_val = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
                
        return cls(
            log_id=data.get("logId"),
            asset_id=data.get("assetId"),
            serial_number=data.get("serialNumber"),
            date=date_val,
            user=data.get("user"),
            log_type=AssetLogType(data["type"]) if data.get("type") is not None else None,
            comment=data.get("comment")
        )


@dataclass
class Asset:
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
    serial_number: str
    type_id: Optional[UUID] = None
    asset_id: Optional[str] = None
    parent_asset_id: Optional[str] = None
    parent_serial_number: Optional[str] = None
    asset_name: Optional[str] = None
    part_number: Optional[str] = None
    revision: Optional[str] = None
    client_id: Optional[int] = None
    state: AssetState = AssetState.OK
    description: Optional[str] = None
    location: Optional[str] = None
    first_seen_date: Optional[datetime] = None
    last_seen_date: Optional[datetime] = None
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None
    last_calibration_date: Optional[datetime] = None
    next_calibration_date: Optional[datetime] = None
    total_count: Optional[int] = None
    running_count: Optional[int] = None
    tags: List[Setting] = field(default_factory=list)
    asset_children: List["Asset"] = field(default_factory=list)
    asset_type: Optional[AssetType] = None
    asset_log: List[AssetLog] = field(default_factory=list)

    @classmethod
    def _parse_date(cls, date_str: Optional[str]) -> Optional[datetime]:
        """Parse ISO date string to datetime"""
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None

    @classmethod
    def from_dict(cls, data: dict) -> "Asset":
        """Create Asset from API response dictionary"""
        return cls(
            asset_id=data.get("assetId"),
            parent_asset_id=data.get("parentAssetId"),
            serial_number=data.get("serialNumber", ""),
            parent_serial_number=data.get("parentSerialNumber"),
            asset_name=data.get("assetName"),
            part_number=data.get("partNumber"),
            revision=data.get("revision"),
            type_id=UUID(data["typeId"]) if data.get("typeId") else None,
            client_id=data.get("ClientId"),
            state=AssetState(data.get("state", 1)),
            description=data.get("description"),
            location=data.get("location"),
            first_seen_date=cls._parse_date(data.get("firstSeenDate")),
            last_seen_date=cls._parse_date(data.get("lastSeenDate")),
            last_maintenance_date=cls._parse_date(data.get("lastMaintenanceDate")),
            next_maintenance_date=cls._parse_date(data.get("nextMaintenanceDate")),
            last_calibration_date=cls._parse_date(data.get("lastCalibrationDate")),
            next_calibration_date=cls._parse_date(data.get("nextCalibrationDate")),
            total_count=data.get("totalCount"),
            running_count=data.get("runningCount"),
            tags=[Setting.from_dict(t) for t in data.get("tags", [])],
            asset_children=[Asset.from_dict(c) for c in data.get("assetChildren", [])],
            asset_type=AssetType.from_dict(data["assetType"]) if data.get("assetType") else None,
            asset_log=[AssetLog.from_dict(l) for l in data.get("assetLog", [])]
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""
        result: Dict[str, Any] = {
            "serialNumber": self.serial_number,
        }
        
        if self.type_id:
            result["typeId"] = str(self.type_id)
        if self.asset_id:
            result["assetId"] = self.asset_id
        if self.parent_asset_id:
            result["parentAssetId"] = self.parent_asset_id
        if self.parent_serial_number:
            result["parentSerialNumber"] = self.parent_serial_number
        if self.asset_name:
            result["assetName"] = self.asset_name
        if self.part_number:
            result["partNumber"] = self.part_number
        if self.revision:
            result["revision"] = self.revision
        if self.state:
            result["state"] = self.state.value
        if self.description:
            result["description"] = self.description
        if self.location:
            result["location"] = self.location
        if self.tags:
            result["tags"] = [t.to_dict() for t in self.tags]
            
        return result
