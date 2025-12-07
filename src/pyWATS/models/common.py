"""Common models shared across modules

Uses Pydantic 2 for validation and serialization.
"""
from typing import Optional
from enum import IntEnum
from pydantic import BaseModel, Field, ConfigDict


class ChangeType(IntEnum):
    """Change type for settings"""
    NONE = 0
    ADD = 1
    UPDATE = 2
    DELETE = 3
    UNKNOWN_4 = 4
    UNKNOWN_5 = 5
    UNKNOWN_6 = 6


class PyWATSModel(BaseModel):
    """
    Base class for all pyWATS models.
    
    Provides consistent Pydantic 2 configuration for serialization/deserialization.
    """
    model_config = ConfigDict(
        populate_by_name=True,          # Allow using field names or aliases
        use_enum_values=True,           # Serialize enums as values
        arbitrary_types_allowed=True,   # Allow custom types
        from_attributes=True,           # Allow creating from ORM objects
        validate_assignment=True,       # Validate on attribute assignment
    )


class Setting(PyWATSModel):
    """
    Key-value setting used for tags/custom data.
    Used in Products, ProductRevisions, Assets, and Units.
    """
    key: str = Field(..., alias="key")
    value: str = Field(..., alias="value")
    change: Optional[ChangeType] = Field(default=None, alias="change")
