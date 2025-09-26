# CallExeStep

# Type/lib
from typing import Literal, Optional
from pydantic import BaseModel, Field

# Imports
from ..step import Step


# Example json object and schema:


# Class: MessagePopUpStep
# A step type that displays a popup message.
class CallExeStep(Step):
    step_type: Literal["CallExecutable"] = Field(default="CallExecutable", deserialization_alias="stepType", serialization_alias="stepType")
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        return True




