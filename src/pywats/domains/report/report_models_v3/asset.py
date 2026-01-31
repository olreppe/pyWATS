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
