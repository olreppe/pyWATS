# Extracted and converted to Pydantic 2 BaseModel
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Dict, Any
from uuid import UUID
import datetime
from enum import IntEnum  # Assuming state is IntEnum; change to StrEnum if needed

# Placeholder for the state enum (replace with actual import if available)
class AssetState(IntEnum):
    AVAILABLE = 0  # Map based on actual values
    IN_USE = 1
    # ... add others

# Placeholder for nested models (convert them similarly)
class ProductSetting(BaseModel):
    # Define based on VirincoWATSWebDashboardModelsMesProductSetting
    pass

class AssetTypeModel(BaseModel):
    # Define based on VirincoWATSWebDashboardModelsMesAssetAssetType
    pass

class AssetLog(BaseModel):
    # Define based on VirincoWATSWebDashboardModelsMesAssetAssetLog
    pass

class AssetModel(BaseModel):
    model_config = {"populate_by_name": True}  # Allow both alias and field name

    serial_number: str = Field(alias="serialNumber")
    type_id: UUID = Field(alias="typeId")
    asset_id: Optional[str] = Field(default=None, alias="assetId")
    parent_asset_id: Optional[str] = Field(default=None, alias="parentAssetId")
    parent_serial_number: Optional[str] = Field(default=None, alias="parentSerialNumber")
    asset_name: Optional[str] = Field(default=None, alias="assetName")
    part_number: Optional[str] = Field(default=None, alias="partNumber")
    revision: Optional[str] = Field(default=None, alias="revision")
    client_id: Optional[int] = Field(default=None, alias="ClientId")  # Note: Mixed case in original
    state: Optional[AssetState] = Field(default=None)
    description: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    first_seen_date: Optional[datetime.datetime] = Field(default=None, alias="firstSeenDate")
    last_seen_date: Optional[datetime.datetime] = Field(default=None, alias="lastSeenDate")
    last_maintenance_date: Optional[datetime.datetime] = Field(default=None, alias="lastMaintenanceDate")
    next_maintenance_date: Optional[datetime.datetime] = Field(default=None, alias="nextMaintenanceDate")
    last_calibration_date: Optional[datetime.datetime] = Field(default=None, alias="lastCalibrationDate")
    next_calibration_date: Optional[datetime.datetime] = Field(default=None, alias="nextCalibrationDate")
    total_count: Optional[int] = Field(default=None, alias="totalCount")
    running_count: Optional[int] = Field(default=None, alias="runningCount")
    tags: Optional[List[ProductSetting]] = Field(default=None)
    asset_children: Optional[List['AssetModel']] = Field(default=None, alias="assetChildren")  # Recursive
    asset_type: Optional[AssetTypeModel] = Field(default=None, alias="assetType")
    asset_log: Optional[List[AssetLog]] = Field(default=None, alias="assetLog")

    # Handle additional properties (like attrs' additional_properties)
    model_extra: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('state', mode='before')
    @classmethod
    def validate_state(cls, v):
        if isinstance(v, int):
            return AssetState(v)
        return v

    # Example validator for dates if needed
    @field_validator('first_seen_date', 'last_seen_date', 'last_maintenance_date', 'next_maintenance_date', 'last_calibration_date', 'next_calibration_date', mode='before')
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return datetime.datetime.fromisoformat(v)
        return v

# Update forward references
AssetModel.model_rebuild()