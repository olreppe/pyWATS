from ...constants import def_MissingString
from ...common_types import BaseModel, Field, model_validator, field_serializer, Optional, Literal

from ..step import Step, StepStatus
from .measurement import LimitMeasurement
from .comp_operator import CompOp

class NumericMeasurement(LimitMeasurement):
    value: float = Field(..., description="The measured value as float.")
    unit: str = Field(..., description="The units of the measurement.")
 
    # -------------------------------------------------------------------
    # Model validator
    # Inject defaults for missing requirements when deserializing - to support legacy reports
    @model_validator(mode="before")
    @classmethod
    def replace_none_during_deserialization(cls, data):
        print(data)
        if isinstance(data, dict) and data.get("unit") in (None, ""):
            data["unit"] = def_MissingString  # Replace None only during deserialization
        return data
class MultiNumericMeasurement(LimitMeasurement):
    name: Optional[str] = Field(..., description="The name of the measurement - required for MultiStepTypes")
    value: float = Field(..., description="The measured value as float.")
    unit: str = Field(..., description="The units of the measurement.")
    
    # -------------------------------------------------------------------
    # Model validator
    # Inject defaults for missing requirements when deserializing - to support legacy reports
    @model_validator(mode="before")
    @classmethod
    def replace_none_during_deserialization(cls, data):
        print(data)
        if isinstance(data, dict) and data.get("unit") in (None, ""):
            data["unit"] = def_MissingString  # Replace None only during deserialization
        return data

# -------------------------------------------------------
# Numeric Step
class NumericStep(Step):
    step_type: Literal["ET_NLT", "NumericLimitStep"] = Field(default="ET_NLT", deserialization_alias="stepType",  serialization_alias="stepType")  # noqa: F821
    measurement: NumericMeasurement = Field(default=None, deserialization_alias="numericMeas", serialization_alias="numericMeas")

    #Critical fix: Pre-process raw JSON data
    @model_validator(mode='before')
    def unpack_measurement(cls, data: dict) -> dict:
        if 'numericMeas' in data:
            meas_data = data['numericMeas']
            
            # Convert list to single item
            if isinstance(meas_data, list):
                data['numericMeas'] = meas_data[0] if meas_data else None
            
            # Ensure dicts get converted to models
            if isinstance(data['numericMeas'], dict):
                data['numericMeas'] = NumericMeasurement(**data['numericMeas'])
    
        return data
    
    # Custom serializer for the measurement field
    @field_serializer('measurement', when_used='json')
    def serialize_measurement(self, measurement: Optional[NumericMeasurement]) -> list:
        if measurement is None:
            return []
        return [measurement.model_dump(by_alias=True, exclude_none=True)]  # Use aliases during serialization

    # validate_step:
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if errors is None:
            errors = []
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        # Numeric Step Validation:
        if not self.measurement.comp_op.validate_limits(low_limit=self.measurement.low_limit, high_limit=self.measurement.high_limit):
            errors.append(f"{self.get_step_path()} Invalig limits / comp_op.")
            return False
        return True
    
    model_config = {
        "allow_populate_by_name": True,  # Allows deserialization using alias
        "exclude_none": True
    }

# -------------------------------------------------------
# Numeric Step
class MultiNumericStep(Step):
    step_type: Literal["ET_MNLT"] = Field(default="ET_MNLT", deserialization_alias="stepType", serialization_alias="stepType")  # noqa: F821
    measurements: list[MultiNumericMeasurement] = Field(default_factory=list, deserialization_alias="numericMeas", serialization_alias="numericMeas")

    # validate_step:
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if errors is None:
            errors = []
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        # Numeric Step Validation:
        valid_limits = True
        for index, m in enumerate(self.measurements):
            if not m.comp_op.validate_limits(low_limit=m.low_limit, high_limit=m.low_limit):
                errors.append(f"{self.get_step_path()} Measurement index: {index} - Invalid limits / comp_op.")
                valid_limits = False
        if not valid_limits:
            return False
        
        # Validate measurement count
        if len(self.measurements) < 2:
            errors.append(f"{self.get_step_path()} MultiNumericStep requires more than one measurement.")
            return False
        
        # Validate that step status corresponds with measurement statuses. 
        statuslist = [m.status for m in self.measurements]
        if self.status == StepStatus.Passed:
            # Step is "P", all measurements must be "P"
            if not all(status == "P" for status in statuslist):
                errors.append(f"{self.get_step_path()} Step is passed, but one or more measurements are not.")
                return False
        elif self.status == "F":
            # Step is "F", at least one measurement must be "F"
            if "F" not in statuslist:
                errors.append(f"{self.get_step_path()} Step is failed, but all measurements are passed.")
                return False
        return True
    
    model_config = {
        "populate_by_name": True  # Allows deserialization using alias
    }

    def add_measurement(self,*, name:str, value:float, unit:str = "", status:str = "P", comp_op: CompOp = CompOp.LOG, high_limit: float=None, low_limit:float=None):
        nm = MultiNumericMeasurement(name=name, value=value, unit=unit, status=status, compOp=comp_op, highLimit=high_limit, lowLimit=low_limit, parent_step=self)
        self.measurements.append(nm)