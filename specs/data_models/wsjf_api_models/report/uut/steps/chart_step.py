# ChartStep

# Type/lib
from typing import Literal, Optional
from pydantic import BaseModel, Field

# Imports
from ..step import Step
from ...chart import Chart


# Example json object and schema

# Class: MessagePopUpStep
# A step type that displays a popup message.
class ChartStep(Step):
    step_type: Literal["WATS_XYGMNLT"] = Field(default="WATS_XYGMNLT", deserialization_alias="stepType", serialization_alias="stepType")
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False

        # Validate ChartStep here

        return True


