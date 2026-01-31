"""
SubUnit Base Class - v3 Implementation

Base class for UUT SubUnit and UUR SubUnit (which adds repair-specific fields).
"""
from __future__ import annotations

from typing import Optional

from .common_types import (
    WATSBase,
    Field,
    field_validator,
    validate_serial_number,
    validate_part_number,
)


class SubUnit(WATSBase):
    """
    Represents a sub-unit/component of a tested or repaired unit.
    
    A SubUnit captures information about components that make up the
    main unit being tested or repaired. This is used for traceability
    and tracking of component serial numbers.
    
    UURSubUnit extends this with repair-specific fields (idx, parent_idx, failures).
    """
    
    # Part Number - required
    pn: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Part number of the sub-unit."
    )
    
    # Revision - optional
    rev: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Revision of the sub-unit part number."
    )
    
    # Serial Number - required
    sn: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Serial number of the sub-unit."
    )
    
    # Part Type - categorizes the sub-unit
    part_type: Optional[str] = Field(
        default="Unknown",
        max_length=50,
        min_length=1,
        validation_alias="partType",
        serialization_alias="partType",
        description="Type/category of the sub-unit (e.g., 'Module', 'PCB', 'Component')."
    )
    
    @field_validator('sn', mode='after')
    @classmethod
    def validate_sn(cls, v: str) -> str:
        """Validate serial number for problematic characters."""
        return validate_serial_number(v)
    
    @field_validator('pn', mode='after')
    @classmethod
    def validate_pn(cls, v: str) -> str:
        """Validate part number for problematic characters."""
        return validate_part_number(v)
