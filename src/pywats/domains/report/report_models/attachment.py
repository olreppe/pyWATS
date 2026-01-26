
"""
Attachment model for report attachments.

Shared base for both UUT and UUR reports. Provides file loading,
MIME type detection, and base64 encoding.
"""

from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path
from typing import Optional, ClassVar
from uuid import UUID, uuid4

from pydantic import Field
from .wats_base import WATSBase


class Attachment(WATSBase):
    """
    A document or file in binary format.
    
    Used by both UUT (step-level) and UUR (report/failure-level) reports.
    
    Example:
        >>> # From file
        >>> attachment = Attachment.from_file("report.pdf")
        >>> 
        >>> # From bytes
        >>> attachment = Attachment.from_bytes("data.bin", b"\\x00\\x01\\x02")
        >>> 
        >>> # Manual construction
        >>> attachment = Attachment(name="test.txt", data="SGVsbG8=", content_type="text/plain")
    """
    
    # Default max size (10 MB)
    DEFAULT_MAX_SIZE: ClassVar[int] = 10 * 1024 * 1024
    
    name: str = Field(..., min_length=1)
    """The name of the attached document or file."""
    
    content_type: Optional[str] = Field(
        default=None, 
        examples=[['image/png', 'text/plain']], 
        min_length=1, 
        validation_alias="contentType", 
        serialization_alias="contentType"
    )
    """The document or file MIME type."""
    
    data: Optional[str] = Field(default=None, min_length=1)
    """The data of the document or file in base64 format."""
    
    # Optional: failure index for UUR attachments (None = report level)
    failure_idx: Optional[int] = Field(
        default=None, 
        validation_alias="failIdx", 
        serialization_alias="failIdx",
        exclude=True  # Excluded from default serialization, added separately for UUR
    )
    """Index of failure this attachment belongs to (None for report-level, UUR only)."""
    
    # Internal tracking
    binary_data_guid: Optional[UUID] = Field(default_factory=uuid4, exclude=True)
    """Unique identifier for this binary data."""
    
    @classmethod
    def from_file(
        cls,
        file_path: str,
        delete_after: bool = False,
        name: Optional[str] = None,
        content_type: Optional[str] = None,
        failure_idx: Optional[int] = None,
        max_size: Optional[int] = None
    ) -> "Attachment":
        """
        Create an attachment from a file.
        
        Args:
            file_path: Path to the file
            delete_after: Delete the file after reading
            name: Custom name (defaults to filename)
            content_type: MIME type (auto-detected if not provided)
            failure_idx: Failure index (UUR only)
            max_size: Maximum file size in bytes (default: 10 MB)
            
        Returns:
            Attachment instance
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file exceeds max size
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Check size
        file_size = path.stat().st_size
        max_allowed = max_size or cls.DEFAULT_MAX_SIZE
        if file_size > max_allowed:
            raise ValueError(
                f"File size ({file_size} bytes) exceeds maximum ({max_allowed} bytes)"
            )
        
        # Read and encode
        with open(path, 'rb') as f:
            content = f.read()
        data_b64 = base64.b64encode(content).decode('utf-8')
        
        # Auto-detect MIME type
        if not content_type:
            content_type, _ = mimetypes.guess_type(str(path))
            content_type = content_type or "application/octet-stream"
        
        # Use filename if name not provided
        if not name:
            name = path.name
        
        # Delete if requested
        if delete_after:
            try:
                path.unlink()
            except OSError:
                pass  # Best effort deletion
        
        return cls(
            name=name,
            data=data_b64,
            content_type=content_type,
            failure_idx=failure_idx
        )
    
    @classmethod
    def from_bytes(
        cls,
        name: str,
        content: bytes,
        content_type: str = "application/octet-stream",
        failure_idx: Optional[int] = None,
        max_size: Optional[int] = None
    ) -> "Attachment":
        """
        Create an attachment from bytes.
        
        Args:
            name: Display name for the attachment
            content: Binary content
            content_type: MIME type
            failure_idx: Failure index (UUR only)
            max_size: Maximum size in bytes (default: 10 MB)
            
        Returns:
            Attachment instance
            
        Raises:
            ValueError: If content exceeds max size
        """
        max_allowed = max_size or cls.DEFAULT_MAX_SIZE
        if len(content) > max_allowed:
            raise ValueError(
                f"Content size ({len(content)} bytes) exceeds maximum ({max_allowed} bytes)"
            )
        
        data_b64 = base64.b64encode(content).decode('utf-8')
        
        return cls(
            name=name,
            data=data_b64,
            content_type=content_type,
            failure_idx=failure_idx
        )
    
    def get_bytes(self) -> bytes:
        """
        Get the attachment data as bytes.
        
        Returns:
            Decoded binary data
        """
        if not self.data:
            return b""
        return base64.b64decode(self.data)
    
    @property
    def size(self) -> int:
        """Size of the attachment in bytes (decoded)."""
        if not self.data:
            return 0
        # Base64 is ~4/3 of original size
        return len(base64.b64decode(self.data))
    
    @property
    def is_failure_attachment(self) -> bool:
        """True if attached to a specific failure (UUR), False if report/step level."""
        return self.failure_idx is not None
    
    # Alias for backward compatibility
    @property
    def mime_type(self) -> str:
        """MIME type of the attachment (alias for content_type)."""
        return self.content_type or "application/octet-stream"
    
    @mime_type.setter
    def mime_type(self, value: str) -> None:
        self.content_type = value
    
    @property
    def file_name(self) -> str:
        """Filename (alias for name)."""
        return self.name
    
