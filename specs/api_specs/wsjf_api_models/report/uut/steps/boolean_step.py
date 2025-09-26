from ...common_types import *

from report.uut.steps.comp_operator import CompOp

from ..step import Step
from .measurement import BooleanMeasurement


class BooleanStep(Step):
    step_type: Literal["ET_PFT"] = Field(default="ET_PFT", deserialization_alias="stepType",serialization_alias="stepType")
 
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        return True
    
    model_config = {
        "populate_by_name": True  # Allows deserialization using alias
    }

class MultiBooleanStep(BooleanStep):
    step_type: Literal["ET_MPFT"] = Field(default="ET_MPFT", deserialization_alias="stepType", serialization_alias="stepType")
    measurements: list[BooleanMeasurement] = Field(default_factory=list, deserialization_alias="numericMeas",serialization_alias="numericMeas")

    # validate_step
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if errors is None:
            errors = []
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        # Current Class Validation:
            
          # For every validation failure        
              # errors.append(f"{self.get_step_path()} ErrorMessage.")
        return True
    
    def add_measurement(self,*,name:str=None, status:str):
        nm = BooleanMeasurement(name=name, status=status, parent_step=self)
        # Import single/multi logic before adding the test to list[numericMeasurements]

        # ? How to handle name if single/double
        # ? Alter type if meascount > 1

        # Add to list
        self.measurements.append(nm)

    model_config = {
        "populate_by_name": True  # Allows deserialization using alias
    }



   