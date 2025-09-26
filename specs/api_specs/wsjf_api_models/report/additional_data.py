
from __future__ import annotations

from typing import Any, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field



class AdditionalData(BaseModel):
    """
    A collection of additional step, header, or station data.
    """

    name: str = Field(..., max_length=200, min_length=1)
    """
    The name of the additional data.
    """
    props: list[Optional[AdditionalDataProperty]] = Field(default_factory=list)
    """
    List of properties in the additional data.
    """

class AdditionalDataArray(BaseModel):
    """
    Information about array in additional data.
    """

    dimension: int
    """
    Dimension of array.
    """
    type: str
    """
    Type of the values in the array.
    """
    indexes: list[Optional[AdditionalDataArrayIndex]]
    """
    List of indexes in the array.
    """

class AdditionalDataArrayIndex(BaseModel):
    """
    Information about an index in an array.
    """

    text: str
    """
    The index as text.
    """
    indexes: list[int]
    """
    List of indexes ordered by dimension.
    """
    value: Optional[AdditionalDataProperty] = None


class AdditionalDataProperty(BaseModel):
    """
    An additional data property.
    """

    name: str = Field(..., min_length=1)
    """
    Name of property.
    """
    type: str = Field(..., min_length=1)  #?
    """
    Value type of property.
    """
    flags: Optional[int] = None
    """
    Bit flags of property.
    """
    value: Optional[str] = None
    """
    Value string of property.
    """
    comment: Optional[str] = None
    """
    Comment of property.
    """
    num_format: Optional[str] = Field(default=None, deserialization_alias="numFormat", serialization_alias="numFormat")
    """
    Number format for value with type Number.
    """
    props: Optional[list[Optional[AdditionalDataProperty]]] = None
    """
    Array of sub-properties. Used for type Obj.
    """
    array: Optional[AdditionalDataArray] = None
    """
    Array information. Used for type Array.
    """
    @staticmethod
    def from_dict(name: str, data: any) -> 'AdditionalDataProperty':
        if isinstance(data, dict):
            props = [AdditionalDataProperty.from_dict(k, v) for k, v in data.items()]
            return AdditionalDataProperty(name=name, type='Obj', props=props)
        elif isinstance(data, list):
            # You might need to define how to handle lists
            return AdditionalDataProperty(name=name, type='Array', array=AdditionalDataArray())  # Example placeholder
        else:
            return AdditionalDataProperty(name=name, type=type(data).__name__, value=str(data))

def json_to_properties(json_dict: dict) -> List[AdditionalDataProperty]:
    return [AdditionalDataProperty.from_dict(name, data) for name, data in json_dict.items()]


AdditionalData.model_rebuild()
AdditionalDataArray.model_rebuild()
AdditionalDataArrayIndex.model_rebuild()
