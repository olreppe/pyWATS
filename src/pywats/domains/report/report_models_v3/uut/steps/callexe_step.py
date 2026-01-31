"""
CallExecutable Step - v3 Implementation

Represents a step that calls an external executable.
"""
from __future__ import annotations

from typing import Optional

from ..step import Step
from ...common_types import WATSBase, Field


class CallExeStepInfo(WATSBase):
    """Information about a CallExecutable step."""
    
    exit_code: Optional[int] = Field(
        default=None,
        validation_alias="exitCode",
        serialization_alias="exitCode",
        description="Exit code from the executable."
    )


class CallExeStep(Step):
    """
    Represents a step that calls an external executable.
    
    This step type executes an external program and captures its exit code.
    """
    
    step_type: str = Field(
        default="CallExecutable",
        frozen=True,
        validation_alias="stepType",
        serialization_alias="stepType",
        description="Step type identifier."
    )
    
    info: Optional[CallExeStepInfo] = Field(
        default=None,
        description="CallExecutable-specific information."
    )
