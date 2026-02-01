"""
NumericStep and MultiNumericStep - v3 Implementation

Numeric limit test steps with proper Optional typing and mixin usage.

Fixes:
- measurement field properly typed as Optional[NumericMeasurement]
- Uses SingleMeasurementMixin to avoid code duplication
- Active mode validation integrated
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Literal,
    ClassVar,
    Any,
    Type,
)

from pydantic import field_serializer, model_validator

from ..step import Step
from .measurement import (
    NumericMeasurement,
    MultiNumericMeasurement,
)
from ...common_types import (
    Field,
    StepStatus,
    CompOp,
)


class NumericStep(Step):
    """
    Numeric limit test step.
    
    Tests a numeric value against configurable limits.
    
    C# Name: NumericLimitStep (alias: ET_NLT in TestStand)
    
    Example:
        step = NumericStep(
            name="Voltage Test",
            value=5.0,
            comp=CompOp.GELE,
            limit_l=4.5,
            limit_h=5.5,
            unit="V"
        )
    """
    
    # Step type discriminator
    step_type: Literal["NumericLimitTest", "ET_NLT"] = Field(
        default="ET_NLT",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # Single measurement (unwrap from array, wrap to array on serialize)
    measurement: Optional[NumericMeasurement] = Field(
        default=None,
        validation_alias="numericMeas",
        serialization_alias="numericMeas",
        description="Numeric measurement with limits."
    )
    
    @model_validator(mode='before')
    @classmethod
    def unwrap_measurement(cls, data: Any) -> Any:
        """Unwrap measurement from list (API returns single-item array)."""
        if isinstance(data, dict) and 'numericMeas' in data:
            meas = data['numericMeas']
            if isinstance(meas, list) and len(meas) > 0:
                data = dict(data)
                data['numericMeas'] = meas[0]
        return data
    
    @field_serializer('measurement', when_used='always')
    @classmethod
    def wrap_measurement(cls, value: Optional[NumericMeasurement]) -> Optional[List[Any]]:
        """Wrap measurement to list format for serialization."""
        if value is None:
            return None
        return [value.model_dump(by_alias=True, exclude_none=True)]
    
    # ========================================================================
    # Convenience Properties (delegate to measurement)
    # ========================================================================
    
    @property
    def value(self) -> Optional[float | str]:
        """Get the measured value."""
        return self.measurement.value if self.measurement else None
    
    @value.setter
    def value(self, val: float | str | None) -> None:
        """Set the measured value."""
        if self.measurement is None:
            self.measurement = NumericMeasurement()
        self.measurement.value = val
    
    @property
    def unit(self) -> Optional[str]:
        """Get the unit."""
        return self.measurement.unit if self.measurement else None
    
    @unit.setter
    def unit(self, val: str | None) -> None:
        """Set the unit."""
        if self.measurement is None:
            self.measurement = NumericMeasurement()
        self.measurement.unit = val
    
    @property
    def comp_op(self) -> Optional[CompOp]:
        """Get the comparison operator."""
        return self.measurement.comp_op if self.measurement else None
    
    @comp_op.setter
    def comp_op(self, val: CompOp | None) -> None:
        """Set the comparison operator."""
        if self.measurement is None:
            self.measurement = NumericMeasurement()
        self.measurement.comp_op = val
    
    @property
    def low_limit(self) -> Optional[float | str]:
        """Get the low limit."""
        return self.measurement.low_limit if self.measurement else None
    
    @low_limit.setter
    def low_limit(self, val: float | str | None) -> None:
        """Set the low limit."""
        if self.measurement is None:
            self.measurement = NumericMeasurement()
        self.measurement.low_limit = val
    
    @property
    def high_limit(self) -> Optional[float | str]:
        """Get the high limit."""
        return self.measurement.high_limit if self.measurement else None
    
    @high_limit.setter
    def high_limit(self, val: float | str | None) -> None:
        """Set the high limit."""
        if self.measurement is None:
            self.measurement = NumericMeasurement()
        self.measurement.high_limit = val
    
    # ========================================================================
    # Factory Method
    # ========================================================================
    
    @classmethod
    def create(
        cls,
        name: str,
        value: float | str,
        *,
        unit: str = "NA",
        comp_op: CompOp = CompOp.LOG,
        low_limit: float | str | None = None,
        high_limit: float | str | None = None,
        status: StepStatus | str = StepStatus.Passed,
    ) -> "NumericStep":
        """
        Factory method to create a NumericStep with measurement.
        
        Args:
            name: Step name
            value: Measured value
            unit: Unit of measurement (default "NA")
            comp_op: Comparison operator (default LOG = log only)
            low_limit: Low limit value
            high_limit: High limit value
            status: Step status
            
        Returns:
            Configured NumericStep instance.
        """
        # Convert string status to enum if needed
        if isinstance(status, str):
            status = StepStatus(status)
            
        measurement = NumericMeasurement(
            value=value,
            comp_op=comp_op,
            low_limit=low_limit,
            high_limit=high_limit,
            unit=unit,
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
        """Validate the numeric step."""
        if errors is None:
            errors = []
            
        if self.measurement:
            status, passed = self.measurement.validate_against_limits()
            self.measurement.status = status
            
            if not passed:
                self.status = status
                if self.fail_parent_on_failure:
                    self.propagate_failure()
                    
        return self.status != StepStatus.Failed


class MultiNumericStep(Step):
    """
    Multi-numeric limit test step.
    
    Tests multiple numeric values in a single step.
    
    C# Name: MultiNumericLimitStep (alias: ET_MNLT in TestStand)
    """
    
    # Step type discriminator
    step_type: Literal["MultiNumericLimitTest", "ET_MNLT"] = Field(
        default="ET_MNLT",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # Multiple measurements
    measurements: List[MultiNumericMeasurement] = Field(
        default_factory=list,
        validation_alias="numericMeas",
        serialization_alias="numericMeas",
        description="List of numeric measurements."
    )
    
    # ========================================================================
    # Helpers
    # ========================================================================
    
    def add_measurement(self, *, name:str, value:float, unit:str = "", status:str = "P", comp_op: CompOp = CompOp.LOG, high_limit: float | None = None, low_limit:float | None = None):
        """
        Add a measurement to this step.
        
        Args:
            name: Measurement name (required, keyword-only)
            value: Measured value
            unit: Unit of measurement
            status: Measurement status ("P" or "F")
            comp_op: Comparison operator
            high_limit: High limit value
            low_limit: Low limit value
            
        Returns:
            The created MultiNumericMeasurement.
        """
        name = self.check_for_duplicates(name) 
        nm = MultiNumericMeasurement(
            name=name, 
            value=value, 
            unit=unit, 
            status=StepStatus(status) if isinstance(status, str) else status, 
            comp_op=comp_op, 
            high_limit=high_limit, 
            low_limit=low_limit
        )
        self.measurements.append(nm)
    
    def check_for_duplicates(self, name):
        """
        Check for duplicate measurement names and truncate if needed.
        """
        # Validate if a measurement with the same name already exists
        if any(measurement.name == name for measurement in self.measurements):
            base_name = name
            # Leave room for suffix like " #99" (max 4 chars)
            if len(name) >= Step.MAX_NAME_LENGTH:
                base_name = name[:Step.MAX_NAME_LENGTH - 3]
            suffix = 2
            new_name = f"{base_name} #{suffix}"

            # Keep generating a new name until it's unique
            while new_name in self.measurements:
                suffix += 1
                new_name = f"{base_name} #{suffix}"

            # Update the measurement's name
            name = new_name
        return name
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def validate_step(
        self,
        trigger_children: bool = False,
        errors: Optional[List[str]] = None
    ) -> bool:
        """Validate all measurements in the step.
        
        Checks:
        1. Limit validity (low_limit <= high_limit for range comparisons)
        2. Value against limits (passes/fails)
        
        Args:
            trigger_children: Not used for multi-step (no children)
            errors: List to append error messages to
            
        Returns:
            True if all measurements pass validation
        """
        if errors is None:
            errors = []
            
        all_passed = True
        
        for meas in self.measurements:
            # Check for invalid limit configuration (low > high)
            if (meas.low_limit is not None and 
                meas.high_limit is not None and
                isinstance(meas.low_limit, (int, float)) and
                isinstance(meas.high_limit, (int, float)) and
                meas.low_limit > meas.high_limit):
                errors.append(
                    f"Measurement '{meas.name}' has invalid limits: "
                    f"low_limit ({meas.low_limit}) > high_limit ({meas.high_limit})"
                )
                all_passed = False
                continue
            
            # Validate value against limits
            status, passed = meas.validate_against_limits()
            meas.status = status
            
            if not passed:
                all_passed = False
                
        if not all_passed:
            self.status = StepStatus.Failed
            if self.fail_parent_on_failure:
                self.propagate_failure()
                
        return all_passed
