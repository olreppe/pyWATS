from typing import Any, Optional, Union, Generic, TypeVar
from uuid import UUID
from pydantic import BaseModel, Field, model_validator, root_validator
from pydantic_core.core_schema import FieldPlainInfoSerializerFunction

from ...constants import *
from .comp_operator import CompOp

class Measurement(BaseModel):
    parent_step: Optional[Any] = Field(default=None, exclude=True)

class BooleanMeasurement(Measurement):    
    status: str = Field(default="P", max_length=1, min_length=1, pattern='^[PFS]$')

# ------------------------------------------------------------------------------------------
# LimitMeasurement 
class LimitMeasurement(BooleanMeasurement):
    value: Union[str,float] = Field(...)
    value_format: str | None = Field(default=None, deserialization_alias="valueFormat", serialization_alias="valueFormat")

    comp_op: Optional[CompOp] = Field(default=CompOp.LOG, deserialization_alias="compOp", serialization_alias="compOp")
    
    high_limit: float | str | None = Field(default=None, deserialization_alias="highLimit", serialization_alias="highLimit")
    high_limit_format: str | None = Field(default=None, deserialization_alias="highLimitFormat", serialization_alias="highLimitFormat")
    low_limit: float | str | None = Field(default=None, deserialization_alias="lowLimit", serialization_alias="lowLimit")
    low_limit_format: str | None = Field(default=None, deserialization_alias="lowLimitFormat", serialization_alias="lowLimitFormat")
        
    model_config = {
        "json_encoders": {CompOp: lambda c: c.name}  # ✅ Serialize enums as their names
    }

    # Validate limits and comOp
    # @model_validator(mode="after")
    # def check_comp_op_limits(self):  
    #     if not self.comp_op.validate_limits(self.low_limit, self.high_limit):
    #         raise ValueError("Invalid limits")
    #     return self  
    
    # Using a Pydantic parsing method that supports current functionalities
    # @classmethod
    # def parse_obj(cls, obj):
    #     if isinstance(obj.get('comp_op'), str):
    #         obj['comp_op'] = CompOp[obj['comp_op']].value
    #     return super().model_validate(obj)

