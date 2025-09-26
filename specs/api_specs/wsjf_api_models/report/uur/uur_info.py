# Type imports
from typing import Annotated, Any, Optional, Union
from pydantic import BaseModel, Field, SerializationInfo
from uuid import UUID,uuid4

# Model imports
from ..report_info import ReportInfo

class UURInfo(ReportInfo):
    processCode: int | None = Field(default=None, deserialization_alias="processCode", serialization_alias="processCode")
    processCodeFormat: str | None = Field(default=None, deserialization_alias="processCodeFormat", serialization_alias="processCodeFormat")
    processName: str | None = Field(default=None, deserialization_alias="processName", serialization_alias="processName")
    refUUT: UUID | None = Field(default=None, deserialization_alias="refUUT", serialization_alias="refUUT")
    confirmDate: str | None = Field(default=None, deserialization_alias="confirmDate", serialization_alias="confirmDate")
    finalizeDate: str | None = Field(default=None, deserialization_alias="finalizeDate", serialization_alias="finalizeDate")
    parent: UUID | None = Field(default=None)
    children: list[UUID] | None = Field(default=None)