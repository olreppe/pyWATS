"""
Attachment and Binary Data - v3 Implementation

Support for file attachments and binary data in reports and steps.
"""
from __future__ import annotations

from typing import Optional, List
import base64

from .common_types import (
    WATSBase,
    Field,
)


class BinaryData(WATSBase):
    """
    Binary data embedded in a report.
    
    Used for storing raw data like:
    - Waveform data
    - Images
    - Binary measurement files
    """
    
    # Content type (MIME type)
    content_type: str = Field(
        ...,
        max_length=100,
        min_length=1,
        validation_alias="contentType",
        serialization_alias="contentType",
        description="MIME type of the binary data (e.g., 'application/octet-stream')."
    )
    
    # The actual binary data (base64 encoded in JSON)
    data: str = Field(
        ...,
        description="Base64 encoded binary data."
    )
    
    # File name
    name: str = Field(
        ...,
        max_length=256,
        min_length=1,
        description="Name/filename of the binary data."
    )
    
    def get_bytes(self) -> bytes:
        """Decode the base64 data to bytes."""
        return base64.b64decode(self.data)
    
    @classmethod
    def from_bytes(
        cls, 
        data: bytes, 
        name: str, 
        content_type: str = "application/octet-stream"
    ) -> "BinaryData":
        """Create BinaryData from raw bytes."""
        return cls(
            content_type=content_type,
            data=base64.b64encode(data).decode('ascii'),
            name=name
        )


class Attachment(WATSBase):
    """
    File attachment for reports or steps.
    
    Attachments can include:
    - Log files
    - Screenshots
    - Configuration files
    - Any other supporting documentation
    """
    
    # Content type (MIME type)
    content_type: str = Field(
        ...,
        max_length=100,
        min_length=1,
        validation_alias="contentType",
        serialization_alias="contentType",
        description="MIME type of the attachment."
    )
    
    # The actual data (base64 encoded in JSON)
    data: str = Field(
        ...,
        description="Base64 encoded attachment data."
    )
    
    # File name
    name: str = Field(
        ...,
        max_length=256,
        min_length=1,
        description="Filename of the attachment."
    )
    
    # Optional description
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Description of the attachment."
    )
    
    def get_bytes(self) -> bytes:
        """Decode the base64 data to bytes."""
        return base64.b64decode(self.data)
    
    @classmethod
    def from_bytes(
        cls,
        data: bytes,
        name: str,
        content_type: str = "application/octet-stream",
        description: Optional[str] = None
    ) -> "Attachment":
        """Create Attachment from raw bytes."""
        return cls(
            content_type=content_type,
            data=base64.b64encode(data).decode('ascii'),
            name=name,
            description=description
        )


class AdditionalData(WATSBase):
    """
    A collection of additional step, header, or station data.
    
    Container for structured additional properties that can include
    nested objects and arrays.
    """
    
    name: str = Field(
        ...,
        max_length=200,
        min_length=1,
        description="The name of the additional data."
    )
    
    props: List["AdditionalDataProperty"] = Field(
        default_factory=list,
        description="List of properties in the additional data."
    )


class AdditionalDataProperty(WATSBase):
    """
    An additional data property.
    
    Can represent simple values, nested objects, or arrays.
    """
    
    name: str = Field(
        ...,
        min_length=1,
        description="Name of property."
    )
    
    type: str = Field(
        ...,
        min_length=1,
        description="Value type of property."
    )
    
    flags: Optional[int] = Field(
        default=None,
        description="Bit flags of property."
    )
    
    value: Optional[str] = Field(
        default=None,
        description="Value string of property."
    )
    
    comment: Optional[str] = Field(
        default=None,
        description="Comment of property."
    )
    
    num_format: Optional[str] = Field(
        default=None,
        validation_alias="numFormat",
        serialization_alias="numFormat",
        description="Number format for value with type Number."
    )
    
    props: Optional[List[Optional["AdditionalDataProperty"]]] = Field(
        default=None,
        description="Array of sub-properties. Used for type Obj."
    )
    
    array: Optional["AdditionalDataArray"] = Field(
        default=None,
        description="Array information. Used for type Array."
    )


class AdditionalDataArray(WATSBase):
    """
    Information about array in additional data.
    """
    
    dimension: int = Field(
        ...,
        description="Dimension of array."
    )
    
    type: str = Field(
        ...,
        description="Type of the values in the array."
    )
    
    indexes: List[Optional["AdditionalDataArrayIndex"]] = Field(
        ...,
        description="List of indexes in the array."
    )


class AdditionalDataArrayIndex(WATSBase):
    """
    Information about an index in an array.
    """
    
    text: str = Field(
        ...,
        description="The index as text."
    )
    
    indexes: List[int] = Field(
        ...,
        description="List of indexes ordered by dimension."
    )
    
    value: Optional[AdditionalDataProperty] = Field(
        default=None,
        description="The value at this index."
    )


class LoopInfo(WATSBase):
    """
    Loop iteration information for steps executed in loops.
    
    When a step is part of a loop, this captures which iteration
    the step result belongs to.
    """
    
    # Loop index (0-based)
    index: int = Field(
        default=0,
        validation_alias="i",
        serialization_alias="i",
        description="Current loop index (0-based)."
    )
    
    # Total iterations
    count: Optional[int] = Field(
        default=None,
        validation_alias="n",
        serialization_alias="n",
        description="Total number of loop iterations."
    )
    
    # Parent loop info (for nested loops)
    parent: Optional["LoopInfo"] = Field(
        default=None,
        description="Parent loop info for nested loops."
    )
