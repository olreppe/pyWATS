from typing import Optional, Union, Literal, TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, Field, model_serializer, model_validator

from report.uut.steps.comp_operator import CompOp

from ..step import Step
from .measurement import LimitMeasurement

# """
# StepTypes:

# SequenceCall        SequenceCall        
# NumericLimitTest    ET_NLT, ET_MNLT
# StringValueTest     ET_SVT, ET_MSVT
# PassFailTest        ET_PFT, ET_MPFT
# Action              ET_A
# Label               Label
# CallExecutable      CallExecutable
# MessagePopup        MessagePopUp
# """
class StringMeasurement(LimitMeasurement):
    value: Optional[str] = None
    limit: Optional[str] = Field(default=None, deserialization_alias="limit", serialization_alias="limit")
    
class MultiStringMeasurement(StringMeasurement):
    name: str = Field(...)


class StringStep(Step):
    step_type: Literal["ET_SVT"] = Field(default="ET_SVT", deserialization_alias="stepType", serialization_alias="stepType")
    measurement: Optional[StringMeasurement] = Field(default=None, deserialization_alias="stringMeas", serialization_alias="stringMeas")

    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        return True
    
    def add_measurement(self,*,name:str=None, value:float, unit:str, status:str, comp_op: CompOp, limit: str = None) -> StringMeasurement:
        sm = StringMeasurement(value=value, unit=unit, status=status, comp_op=comp_op, limit=limit, parent_step=self)
        self.measurement = sm
        return sm

    #Critical fix: Pre-process raw JSON data
    @model_validator(mode='before')
    def unpack_measurement(cls, data: dict) -> dict:
        if 'stringMeas' in data:
            meas_data = data['stringMeas']
            
            # Convert list to single item
            if isinstance(meas_data, list):
                data['stringMeas'] = meas_data[0] if meas_data else None
            
            # Ensure dicts get converted to models
            if isinstance(data['stringMeas'], dict):
                data['stringMeas'] = StringMeasurement(**data['stringMeas'])
        
        return data
    
    #custom serializer - outputs the single meas as if it was a list
    @model_serializer
    def serialize_model(self):
        return {
            "stepType": self.step_type,
            "stringMeas": [self.measurement.model_dump()] if self.measurement else []
        }

class MultiStringStep(Step):
    step_type: Literal["ET_MSVT"] = Field(default="ET_MSVT", deserialization_alias="stepType", serialization_alias="stepType")
    measurements: list[MultiStringMeasurement] = Field(default_factory=list, deserialization_alias="stringMeas", serialization_alias="stringMeas")

    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        return True
    
    def add_measurement(self,*,name:str=None, value:float, unit:str, status:str, comp_op: CompOp, limit: str = None):
        sm = MultiStringMeasurement(name=name, value=value, unit=unit, status=status, comp_op=comp_op, limit=limit, parent_step=self)
        # Import single/multi logic before adding the test to list[numericMeasurements]

        # ? How to handle name if single/double
        # ? Alter type if meascount > 1

        # Add to list
        self.measurements.append(sm)