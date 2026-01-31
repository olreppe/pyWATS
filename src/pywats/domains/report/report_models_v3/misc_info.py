"""
Miscellaneous Info - v3 Implementation

Key-value pair storage for unit configuration data.
"""
from __future__ import annotations

from typing import Optional, Union, List

from pydantic import model_validator

from .common_types import (
    WATSBase,
    Field,
)


class MiscInfo(WATSBase):
    """
    Miscellaneous information key-value pair.
    
    Provides a flexible way to store additional unit configuration
    data that doesn't have a dedicated header field.
    
    Note: The 'numeric' field is deprecated. On deserialization, numeric values
    are automatically converted to string_value.
    
    Example:
        report.add_misc_info("BuildDate", "2026-01-30")
        report.add_misc_info("FirmwareVersion", "1.2.3")
    """
    
    # Optional ID/index
    id: Optional[str] = Field(
        default=None,
        description="Optional unique identifier."
    )
    
    # Key/Description - required
    description: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The misc info display name/key."
    )
    
    # String value
    string_value: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias="text",
        serialization_alias="text",
        description="The misc info value as string."
    )
    
    # Numeric value - DEPRECATED, kept only for deserialization compatibility
    # Will be converted to string_value during validation
    numeric_value: Optional[float] = Field(
        default=None,
        validation_alias="numeric",
        serialization_alias="numeric",
        exclude=True,  # Don't serialize this field
        description="DEPRECATED: numeric values are converted to text."
    )
    
    @model_validator(mode='after')
    def convert_numeric_to_string(self) -> 'MiscInfo':
        """Convert deprecated numeric field to string_value."""
        if self.numeric_value is not None:
            numeric_str = str(int(self.numeric_value) if self.numeric_value == int(self.numeric_value) else self.numeric_value)
            if self.string_value is None or self.string_value == "":
                # Move numeric to string_value
                self.string_value = numeric_str
            # If string_value already has a value, we ignore numeric
            # (the parent collection handles creating duplicates if needed)
            self.numeric_value = None  # Clear the deprecated field
        return self


class UURMiscInfo(WATSBase):
    """
    UUR-specific miscellaneous information.
    
    Similar to MiscInfo but with UUR-specific field naming.
    """
    
    key: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The misc info key/name."
    )
    
    value: Optional[str] = Field(
        default=None,
        max_length=500,
        description="The misc info value."
    )
