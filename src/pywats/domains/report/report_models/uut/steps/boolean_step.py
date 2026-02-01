"""
PassFailStep (BooleanStep) - v3 Implementation

Boolean/pass-fail test step.

C# Name: PassFailStep
"""
from __future__ import annotations

from typing import (
    Optional,
    List,
    Literal,
    Any,
)

from pydantic import model_validator, field_serializer

from ..step import Step
from .measurement import (
    BooleanMeasurement,
    MultiBooleanMeasurement,
)
from ...common_types import (
    Field,
    StepStatus,
)


class PassFailStep(Step):
    """
    Pass/Fail test step.
    
    Simple boolean test that passes or fails based on a condition.
    
    C# Name: PassFailStep (alias: ET_PFT in TestStand)
    
    Example:
        step = PassFailStep(name="LED Check", value=True)
    """
    
    # Step type discriminator
    step_type: Literal["PassFailTest", "ET_PFT"] = Field(
        default="ET_PFT",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # Single measurement (unwrap from array, wrap to array on serialize)
    measurement: Optional[BooleanMeasurement] = Field(
        default=None,
        validation_alias="booleanMeas",
        serialization_alias="booleanMeas",
        description="Boolean measurement."
    )
    
    @model_validator(mode='before')
    @classmethod
    def unwrap_measurement(cls, data: Any) -> Any:
        """Unwrap measurement from list (API returns single-item array)."""
        if isinstance(data, dict) and 'booleanMeas' in data:
            meas = data['booleanMeas']
            if isinstance(meas, list) and len(meas) > 0:
                data = dict(data)
                data['booleanMeas'] = meas[0]
        return data
    
    @field_serializer('measurement', when_used='always')
    @classmethod
    def wrap_measurement(cls, value: Optional[BooleanMeasurement]) -> Optional[List[Any]]:
        """Wrap measurement to list format for serialization."""
        if value is None:
            return None
        return [value.model_dump(by_alias=True, exclude_none=True)]
    
    # ========================================================================
    # Convenience Properties
    # ========================================================================
    
    @property
    def value(self) -> Optional[bool]:
        """Get the measured value."""
        return self.measurement.value if self.measurement else None
    
    @value.setter
    def value(self, val: bool | None) -> None:
        """Set the measured value."""
        if self.measurement is None:
            self.measurement = BooleanMeasurement()
        self.measurement.value = val
    
    # ========================================================================
    # Factory Method
    # ========================================================================
    
    @classmethod
    def create(
        cls,
        name: str,
        value: bool | None = None,
        *,
        status: StepStatus | str = StepStatus.Passed,
    ) -> "PassFailStep":
        """
        Factory method to create a PassFailStep.
        
        Args:
            name: Step name
            value: Boolean result (True=pass, False=fail)
            status: Step status
            
        Returns:
            Configured PassFailStep instance.
        """
        # Convert string status to enum if needed
        if isinstance(status, str):
            status = StepStatus(status)
            
        measurement = BooleanMeasurement(
            value=value,
            status=status,
        )
        
        return cls(
            name=name,
            measurement=measurement,
            status=status,
        )
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def validate_step(
        self,
        trigger_children: bool = False,
        errors: Optional[List[str]] = None
    ) -> bool:
        """Validate the pass/fail step."""
        if errors is None:
            errors = []
            
        if self.measurement:
            status, passed = self.measurement.validate_against_expected(expected=True)
            self.measurement.status = status
            
            if not passed:
                self.status = status
                if self.fail_parent_on_failure:
                    self.propagate_failure()
                    
        return self.status != StepStatus.Failed


class MultiBooleanStep(Step):
    """
    Multi-boolean test step with multiple measurements.
    
    Container for multiple boolean pass/fail measurements.
    
    C# Name: MultiBooleanStep (alias: ET_MPFT in TestStand)
    
    Example:
        step = MultiBooleanStep(name="LED Tests")
        step.add_measurement(name="Red LED", status="P")
        step.add_measurement(name="Green LED", status="P")
    """
    
    # Step type discriminator
    step_type: Literal["MultiBooleanTest", "ET_MPFT"] = Field(
        default="ET_MPFT",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # List of measurements
    measurements: List[MultiBooleanMeasurement] = Field(
        default_factory=list,
        validation_alias="booleanMeas",
        serialization_alias="booleanMeas",
        description="List of boolean measurements."
    )
    
    # ========================================================================
    # Factory Method
    # ========================================================================
    
    def add_measurement(
        self,
        *,
        name: str,
        status: StepStatus | str = "P",
    ) -> MultiBooleanMeasurement:
        """
        Add a boolean measurement to this step.
        
        Args:
            name: Measurement name
            status: Status (StepStatus enum or "P"/"F")
            
        Returns:
            The created MultiBooleanMeasurement.
        """
        name = self._check_for_duplicates(name)
        
        # Convert string status to enum
        step_status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
        
        measurement = MultiBooleanMeasurement(
            name=name,
            status=step_status,
        )
        self.measurements.append(measurement)
        return measurement
    
    def check_for_duplicates(self, name: str) -> str:
        """
        Public method for checking duplicate measurement names (V1 compatibility).
        
        Args:
            name: Measurement name to check
            
        Returns:
            Unique name (original or modified with suffix)
        """
        return self._check_for_duplicates(name)
    
    def _check_for_duplicates(self, name: str) -> str:
        """
        Check for duplicate measurement names and generate unique name if needed.
        """
        existing_names = {m.name for m in self.measurements}
        if name not in existing_names:
            return name
            
        # Generate unique name
        base_name = name
        if len(name) >= Step.MAX_NAME_LENGTH:
            base_name = name[:Step.MAX_NAME_LENGTH - 4]
        
        suffix = 2
        new_name = f"{base_name} #{suffix}"
        while new_name in existing_names:
            suffix += 1
            new_name = f"{base_name} #{suffix}"
            
        return new_name
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def validate_step(
        self,
        trigger_children: bool = False,
        errors: Optional[List[str]] = None
    ) -> bool:
        """Validate the multi-boolean step."""
        if errors is None:
            errors = []
            
        return self.status != StepStatus.Failed


# Alias for v1 compatibility
BooleanStep = PassFailStep
