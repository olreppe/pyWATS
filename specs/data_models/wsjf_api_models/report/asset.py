from __future__ import annotations

from typing import Any, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class Asset(BaseModel):
    sn: Optional[str] = Field(default="123", max_length=100, min_length=1, deserialization_alias="assetSN", serialization_alias="assetSN")
    usage_count: Optional[int] = Field(default=0, deserialization_alias="usageCount",serialization_alias="usageCount")
    usage_count_format: Optional[str] = Field(default=None, deserialization_alias="usageCountFormat", serialization_alias="usageCountFormat")

class AssetStats(BaseModel):
    sn: str = Field(..., max_length=100, min_length=1, deserialization_alias="assetSN", serialization_alias="assetSN")
    """
    The Serial number of the asset. This property is not used for incoming report (read-only).
    """
    running_count: Optional[int] = Field(default=None, deserialization_alias="runningCount", serialization_alias="runningCount")
    """
    How many times the asset has been used since last calibration. This property is not used for incoming report (read-only).
    """
    running_count_exceeded: Optional[int] = Field(default=None, deserialization_alias="runningCountExceeded", serialization_alias="runningCountExceeded")
    """
    How many times more than the limit the asset has been used since last calibration. This property is not used for incoming report (read-only).
    """
    total_count: Optional[int] = Field(default=None, deserialization_alias="totalCount", serialization_alias="totalCount")
    """
    How many times the asset has been used in its lifetime. This property is not used for incoming report (read-only).
    """
    total_count_exceeded: Optional[int] = Field(default=None, deserialization_alias="totalCountExceeded", serialization_alias="totalCountExceeded")
    """
    How many times more than the limit the asset has been used in its lifetime. This property is not used for incoming report (read-only).
    """
    days_since_calibration: Optional[float] = Field(default=None, deserialization_alias="daysSinceCalibration", serialization_alias="daysSinceCalibration")
    """
    How many days since the last calibration. This property is not used for incoming report (read-only).
    """
    is_days_since_calibration_unknown: Optional[bool] = Field(default=None, deserialization_alias="isDaysSinceCalibrationUnknown", serialization_alias="isDaysSinceCalibrationUnknown")
    """
    If the asset has never been calibrated, then it is unknown. This property is not used for incoming report (read-only).
    """
    calibration_days_overdue: Optional[float] = Field(default=None, deserialization_alias="calibrationDaysOverdue", serialization_alias="calibrationDaysOverdue")
    """
    How many days since calibration was overdue. This property is not used for incoming report (read-only).
    """
    days_since_maintenance: Optional[float] = Field(default=None, deserialization_alias="daysSinceMaintenance", serialization_alias="daysSinceMaintenance")
    """
    How many days since the last maintenance. This property is not used for incoming report (read-only).
    """
    is_days_since_maintenance_unknown: Optional[bool] = Field(default=None, deserialization_alias="isDaysSinceMaintenanceUnknown", serialization_alias="isDaysSinceMaintenanceUnknown")
    """
    If the asset has never been maintenance, then it is unknown. This property is not used for incoming report (read-only).
    """
    maintenance_days_overdue: Optional[float] = Field(default=None, deserialization_alias="maintenanceDaysOverdue", serialization_alias="maintenanceDaysOverdue")
    """
    How many days since maintenance was overdue. This property is not used for incoming report (read-only).
    """
    message: Optional[str] = Field(default=None)
    """
    Message from stats calulation. This property is not used for incoming report (read-only).
    """

