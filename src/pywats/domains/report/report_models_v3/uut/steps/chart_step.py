"""
ChartStep - v3 Implementation

Chart step for displaying charts as standalone test steps.

Fix: Uses string stepType instead of Literal to avoid type override conflict.
"""
from __future__ import annotations

from typing import (
    Optional,
    List,
)

from ..step import Step
from ...common_types import (
    Field,
    StepStatus,
)
from ...chart import Chart


class ChartStep(Step):
    """
    Chart step for standalone chart display.
    
    Unlike charts attached to other steps, this step exists solely to
    display chart data.
    
    C# Name: ChartStep
    
    Note: stepType is a string field (not Literal) to avoid mypy conflicts
    with base class override rules. Default is "Chart".
    
    Example:
        step = ChartStep(name="Waveform Display")
        step.add_chart(
            chart_type=ChartType.LineChart,
            chart_label="Voltage",
            x_label="Time",
            x_unit="s",
            y_label="Voltage",
            y_unit="V"
        )
    """
    
    # Step type discriminator - uses string to avoid Literal override conflict
    step_type: str = Field(
        default="Chart",
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
        """Validate the chart step."""
        if errors is None:
            errors = []
            
        # A chart step should have a chart
        if self.chart is None:
            errors.append(f"ChartStep '{self.name}' has no chart data")
            # Not a failure, just a warning
            
        return self.status != StepStatus.Failed
