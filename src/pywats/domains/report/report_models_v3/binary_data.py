"""
Attachment and Binary Data - v3 Implementation

Support for file attachments and binary data in reports and steps.
"""
from __future__ import annotations

from typing import Optional
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
    
    @classmethod
    def from_file(
        cls,
        file_path: str,
        content_type: Optional[str] = None
    ) -> "BinaryData":
        """Create BinaryData from a file."""
        import os
        import mimetypes
        
        name = os.path.basename(file_path)
        
        if content_type is None:
            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "application/octet-stream"
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        return cls.from_bytes(data, name, content_type)


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
    
    @classmethod
    def from_file(
        cls,
        file_path: str,
        content_type: Optional[str] = None,
        description: Optional[str] = None
    ) -> "Attachment":
        """Create Attachment from a file."""
        import os
        import mimetypes
        
        name = os.path.basename(file_path)
        
        if content_type is None:
            content_type, _ = mimetypes.guess_type(file_path)
            content_type = content_type or "application/octet-stream"
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        return cls.from_bytes(data, name, content_type, description)


class AdditionalData(WATSBase):
    """
    Additional data attached to a step.
    
    Used for storing extra information that doesn't fit
    into the standard step fields.
    """
    
    # Data type identifier
    data_type: str = Field(
        ...,
        max_length=100,
        validation_alias="dataType",
        serialization_alias="dataType",
        description="Type identifier for the additional data."
    )
    
    # The data content (can be various formats)
    data: Optional[str] = Field(
        default=None,
        description="The additional data content."
    )
    
    # Optional name/label
    name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional name for the additional data."
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
