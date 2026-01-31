"""
Unknown Step - v3 Implementation

Fallback step type for forward compatibility.
"""
from __future__ import annotations

from ..step import Step
from ...common_types import Field, ConfigDict


class UnknownStep(Step):
    """
    Fallback step type for steps not recognized by this version.
    
    This allows the API to handle reports containing step types
    that were added in newer versions, maintaining forward compatibility.
    
    The extra="allow" configuration means any additional fields
    will be preserved during serialization/deserialization.
    """
    
    model_config = ConfigDict(extra="allow")
    
    step_type: str = Field(
        ...,
        validation_alias="stepType",
        serialization_alias="stepType",
        description="Step type identifier (can be any value)."
    )
