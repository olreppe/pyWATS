"""
Asset Class - v3 Implementation

Represents test equipment/assets used during testing.
"""
from __future__ import annotations

from typing import Optional
from datetime import datetime

from .common_types import (
    WATSBase,
    Field,
    field_validator,
    validate_serial_number,
)


class Asset(WATSBase):
    """
    Represents test equipment or assets used during testing.
    
    Assets can be things like:
    - Test fixtures
    - Measurement equipment (DMMs, oscilloscopes)
    - Power supplies
    - Custom test hardware
    
    Tracking assets helps with:
    - Calibration management
    - Equipment utilization
    - Failure correlation (bad equipment)
    """
    
    # Serial number - required
    sn: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Asset serial number."
    )
    
    # Asset type/category
    asset_type: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias="assetType",
        serialization_alias="assetType",
        description="Type/category of the asset."
    )
    
    # Part number
    pn: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias="partNumber",
        serialization_alias="partNumber",
        description="Asset part number/model."
    )
    
    # Usage count
    usage_count: Optional[int] = Field(
        default=None,
        validation_alias="usageCount",
        serialization_alias="usageCount",
        description="Number of times this asset has been used."
    )
    
    # Calibration date
    calibration_date: Optional[datetime] = Field(
        default=None,
        validation_alias="calibrationDate",
        serialization_alias="calibrationDate",
        description="Date of last calibration."
    )
    
    # Calibration due date
    calibration_due: Optional[datetime] = Field(
        default=None,
        validation_alias="calibrationDue",
        serialization_alias="calibrationDue",
        description="Date when calibration is due."
    )
    
    @field_validator('sn', mode='after')
    @classmethod
    def validate_sn(cls, v: str) -> str:
        """Validate serial number for problematic characters."""
        return validate_serial_number(v)


class AssetStats(WATSBase):
    """
    Statistics about an asset.
    Read-only from server.
    """
    
    sn: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Asset serial number."
    )
    
    running_count: Optional[int] = Field(
        default=None,
        validation_alias="runningCount",
        serialization_alias="runningCount",
        description="Number of executions."
    )
    
    running_count_exceeded: Optional[bool] = Field(
        default=None,
        validation_alias="runningCountExceeded",
        serialization_alias="runningCountExceeded",
        description="Running count limit exceeded."
    )
    
    total_count: Optional[int] = Field(
        default=None,
        validation_alias="totalCount",
        serialization_alias="totalCount",
        description="Total count."
    )
    
    total_count_exceeded: Optional[bool] = Field(
        default=None,
        validation_alias="totalCountExceeded",
        serialization_alias="totalCountExceeded",
        description="Total count limit exceeded."
    )
    
    days_since_calibration: Optional[int] = Field(
        default=None,
        validation_alias="daysSinceCalibration",
        serialization_alias="daysSinceCalibration",
        description="Days since last calibration."
    )
    
    is_days_since_calibration_unknown: Optional[bool] = Field(
        default=None,
        validation_alias="isDaysSinceCalibrationUnknown",
        serialization_alias="isDaysSinceCalibrationUnknown",
        description="Whether days since calibration is unknown."
    )
    
    calibration_days_overdue: Optional[int] = Field(
        default=None,
        validation_alias="calibrationDaysOverdue",
        serialization_alias="calibrationDaysOverdue",
        description="Days overdue for calibration."
    )
    
    days_since_maintenance: Optional[int] = Field(
        default=None,
        validation_alias="daysSinceMaintenance",
        serialization_alias="daysSinceMaintenance",
        description="Days since last maintenance."
    )
    
    is_days_since_maintenance_unknown: Optional[bool] = Field(
        default=None,
        validation_alias="isDaysMaintenanceUnknown",
        serialization_alias="isDaysMaintenanceUnknown",
        description="Whether days since maintenance is unknown."
    )
    
    maintenance_days_overdue: Optional[int] = Field(
        default=None,
        validation_alias="maintenanceDaysOverdue",
        serialization_alias="maintenanceDaysOverdue",
        description="Days overdue for maintenance."
    )
    
    message: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Asset message."
    )
