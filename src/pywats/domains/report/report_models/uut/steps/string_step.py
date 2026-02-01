"""
StringValueStep (StringStep) - v3 Implementation

String value test step.

C# Name: StringValueStep
"""
from __future__ import annotations

from typing import (
    Optional,
    List,
    Literal,
    Union,
    Any,
)

from pydantic import model_validator, field_serializer

from ..step import Step
from .measurement import (
    StringMeasurement,
    MultiStringMeasurement,
)
from ...common_types import (
    Field,
    StepStatus,
    CompOp,
)


class StringValueStep(Step):
    """
    String value test step.
    
    Tests a string value against an expected value using comparison operators.
    
    C# Name: StringValueStep (alias: ET_SVT in TestStand)
    
    Example:
        step = StringValueStep(
            name="Firmware Version",
            value="1.2.3",
            comp=CompOp.EQ,
            limit="1.2.3"
        )
    """
    
    # Step type discriminator
    step_type: Literal["StringValueTest", "ET_SVT"] = Field(
        default="ET_SVT",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # Single measurement (unwrap from array, wrap to array on serialize)
    measurement: Optional[StringMeasurement] = Field(
        default=None,
        validation_alias="stringMeas",
        serialization_alias="stringMeas",
        description="String measurement with comparison."
    )
    
    @model_validator(mode='before')
    @classmethod
    def unwrap_measurement(cls, data: Any) -> Any:
        """Unwrap measurement from list (API returns single-item array)."""
        if isinstance(data, dict) and 'stringMeas' in data:
            meas = data['stringMeas']
            if isinstance(meas, list) and len(meas) > 0:
                data = dict(data)
                data['stringMeas'] = meas[0]
        return data
    
    @field_serializer('measurement', when_used='always')
    @classmethod
    def wrap_measurement(cls, value: Optional[StringMeasurement]) -> Optional[List[Any]]:
        """Wrap measurement to list format for serialization."""
        if value is None:
            return None
        return [value.model_dump(by_alias=True, exclude_none=True)]
    
    # ========================================================================
    # Convenience Properties
    # ========================================================================
    
    @property
    def value(self) -> Optional[str]:
        """Get the measured value."""
        return self.measurement.value if self.measurement else None
    
    @value.setter
    def value(self, val: str | None) -> None:
        """Set the measured value."""
        if self.measurement is None:
            self.measurement = StringMeasurement()
        self.measurement.value = val
    
    @property
    def comp(self) -> Optional[CompOp]:
        """Get the comparison operator."""
        return self.measurement.comp_op if self.measurement else None
    
    @comp.setter
    def comp(self, val: CompOp | None) -> None:
        """Set the comparison operator."""
        if self.measurement is None:
            self.measurement = StringMeasurement()
        self.measurement.comp_op = val
    
    @property
    def limit(self) -> Optional[str]:
        """Get the limit string."""
        return self.measurement.limit if self.measurement else None
    
    @limit.setter
    def limit(self, val: str | None) -> None:
        """Set the limit string."""
        if self.measurement is None:
            self.measurement = StringMeasurement()
        self.measurement.limit = val
    
    # ========================================================================
    # Factory Method
    # ========================================================================
    
    @classmethod
    def create(
        cls,
        name: str,
        value: str | None = None,
        *,
        comp_op: CompOp | None = None,
        limit: str | None = None,
        status: StepStatus | str = StepStatus.Passed,
    ) -> "StringValueStep":
        """
        Factory method to create a StringValueStep.
        
        Args:
            name: Step name
            value: Measured string value
            comp_op: Comparison operator
            limit: Expected string value
            status: Step status
            
        Returns:
            Configured StringValueStep instance.
        """
        # Convert string status to enum if needed
        if isinstance(status, str):
            status = StepStatus(status)
            
        measurement = StringMeasurement(
            value=value,
            comp_op=comp_op,
            limit=limit,
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
        """Validate the string value step."""
        if errors is None:
            errors = []
            
        if self.measurement:
            status, passed = self.measurement.validate_against_limit()
            self.measurement.status = status
            
            if not passed:
                self.status = status
                if self.fail_parent_on_failure:
                    self.propagate_failure()
                    
        return self.status != StepStatus.Failed


class MultiStringStep(Step):
    """
    Multi-string test step with multiple measurements.
    
    Container for multiple string measurements.
    
    C# Name: MultiStringStep (alias: ET_MSVT in TestStand)
    
    Example:
        step = MultiStringStep(name="Configuration Checks")
        step.add_measurement(name="Firmware", value="1.2.3", status="P", comp_op=CompOp.EQ, limit="1.2.3")
    """
    
    # Step type discriminator
    step_type: Literal["MultiStringTest", "ET_MSVT"] = Field(
        default="ET_MSVT",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # List of measurements
    measurements: List[MultiStringMeasurement] = Field(
        default_factory=list,
        validation_alias="stringMeas",
        serialization_alias="stringMeas",
        description="List of string measurements."
    )
    
    # ========================================================================
    # Factory Method
    # ========================================================================
    
    def add_measurement(
        self,
        *,
        name: str | None = None,
        value: Union[str, float],
        status: StepStatus | str,
        comp_op: CompOp,
        limit: str | None = None,
    ) -> MultiStringMeasurement:
        """
        Add a string measurement to this step.
        
        Args:
            name: Measurement name (optional, uses step name if not provided)
            value: Measured string value
            status: Status (StepStatus enum or "P"/"F")
            comp_op: Comparison operator
            limit: Expected string value
            
        Returns:
            The created MultiStringMeasurement.
        """
        if name is None:
            name = self.name or "Measurement"
            
        name = self._check_for_duplicates(name)
        
        # Convert string status to enum
        step_status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
        
        measurement = MultiStringMeasurement(
            name=name,
            value=str(value),
            status=step_status,
            comp_op=comp_op,
            limit=limit,
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
        """Validate the multi-string step."""
        if errors is None:
            errors = []
            
        return self.status != StepStatus.Failed


# Alias for v1 compatibility
StringStep = StringValueStep
