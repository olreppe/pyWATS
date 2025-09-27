from typing import Any, Optional

from pydantic import BaseModel, Field



class SubUnit(BaseModel):
    """
    A sub unit. The unit with index 0 is the main unit.
    """
    pn: str = Field(..., max_length=100, min_length=1)
    """
    The partnumber of the sub unit.
    """
    rev: Optional[str] = Field(default=None, max_length=100, min_length=0)
    """
    The revision of the sub unit.
    """
    sn: str = Field(..., max_length=100, min_length=1)
    """
    The serial number of the sub unit.
    """
    part_type: Optional[str] = Field(default="Unknown", max_length=50, min_length=1, deserialization_alias="partType",serialization_alias="partType")
    """
    The type of sub unit.
    """


