from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from .uur_info import UURInfo
from ..report import Report

class UURReport(Report):
    # Overloads
    type: Literal["R"] = "R"

    # UUR Specific
    info: UURInfo = Field(default=None, deserialization_alias="uur", serialization_alias="uur")


