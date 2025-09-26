# MessagePopUp
# messagePopup: Optional[MessagePopup] = None

# Type/lib
from typing import Literal, Optional
from pydantic import BaseModel, Field

# Imports
from ..step import Step


# Example

# Class: MessagePopUpStep
# A step type that displays a popup message.
class MessagePopUpStep(Step):
    step_type: Literal["MessagePopup"] = Field(default="MessagePopup", deserialization_alias="stepType", serialization_alias="stepType")
    response: Optional[str] = Field(default=" ", max_length=100, min_length=1, description="The popup message.")
    button: Optional[int] = Field(default=None, description="The code of the button that was pressed.")
    button_format: Optional[str] = Field(default=None, description="", deserialization_alias="buttonFormat", serialization_alias="buttonFormat")

    def validate_step(self, trigger_children=False, errors=None) -> bool:
        """ No validation required """
        return True


