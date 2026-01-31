"""
ActionStep - v3 Implementation

Action step (no measurement, just execution).
"""
from __future__ import annotations

from typing import (
    Optional,
    List,
    Literal,
)

from ..step import Step
from ...common_types import (
    Field,
    StepStatus,
)


class ActionStep(Step):
    """
    Action step with no measurement.
    
    Represents an action that was executed but has no measurement data.
    Typically used for setup/cleanup actions or logging.
    
    C# Name: ActionStep
    
    Example:
        step = ActionStep(name="Initialize Equipment")
    """
    
    # Step type discriminator
    step_type: Literal["Action"] = Field(
        default="Action",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def validate_step(
        self,
        trigger_children: bool = False,
        errors: Optional[List[str]] = None
    ) -> bool:
        """Validate the action step (passes unless explicitly failed)."""
        return self.status != StepStatus.Failed
