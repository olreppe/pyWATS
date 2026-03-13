"""
MessagePopup Step - v3 Implementation

Represents a step that displays a message popup to the user.
"""
from __future__ import annotations

from typing import Optional

from ..step import Step
from ...common_types import WATSBase, Field


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
        validation_alias="messagePopup",
        serialization_alias="messagePopup",
        description="MessagePopup-specific information."
    )
