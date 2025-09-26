
from __future__ import annotations

from typing import Any, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class Attachment(BaseModel):
    """
    A document or file in binary format.
    """

    name: str = Field(..., min_length=1)
    """
    The name of the attached document or file.
    """
    content_type: str = Field(..., examples=[['image/png', 'text/plain']], min_length=1, deserialization_alias="contentType", serialization_alias="contentType")
    """
    The document or file MIME type.
    """
    data: str = Field(..., min_length=1)
    """
    The data of the document or file in binary format.
    """
