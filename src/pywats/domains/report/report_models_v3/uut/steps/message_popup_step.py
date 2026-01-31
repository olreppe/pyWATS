"""
MessagePopup Step - v3 Implementation

Represents a step that displays a message popup to the user.
"""
from __future__ import annotations

from typing import Optional

from ..step import Step
from ...common_types import WATSBase, Field, model_validator


class MessagePopupInfo(WATSBase):
    """Information about a MessagePopup step."""
    
    response: Optional[str] = Field(
        default=None,
        max_length=100,
        description="User's response to the popup."
    )
    
    button: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Button that was clicked."
    )
    
    @model_validator(mode='after')
    def set_default_response(self) -> "MessagePopupInfo":
        """Set default response if not provided."""
        if self.response is None:
            self.response = "NOT SET"
        return self


class MessagePopUpStep(Step):
    """
    Represents a step that displays a message popup to the user.
    
    This step type shows a message dialog and captures the user's response.
    """
    
    step_type: str = Field(
        default="MessagePopup",
        frozen=True,
        validation_alias="stepType",
        serialization_alias="stepType",
        description="Step type identifier."
    )
    
    info: Optional[MessagePopupInfo] = Field(
        default=None,
        description="MessagePopup-specific information."
    )
