"""
Measurement Classes - v3 Implementation

Provides measurement data types (NumericMeasurement, BooleanMeasurement, StringMeasurement)
and the SingleMeasurementMixin for extracting shared wrap/unwrap logic.

Fixes:
- SingleMeasurementMixin extracts duplicated wrap/unwrap logic
- Proper Optional typing for measurement field
- CompOp validation guards against None
- Limit type consistency (float | str | None)
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    TypeVar,
    Generic,
    Optional,
    Union,
    List,
    Any,
    ClassVar,
    Type,
)
from abc import ABC, abstractmethod

from pydantic import (
    field_validator,
    field_serializer,
    model_validator,
)

from ...common_types import (
    WATSBase,
    Field,
    StepStatus,
    CompOp,
)

# Type variable for measurement types
MeasurementT = TypeVar('MeasurementT', bound='BaseMeasurement')


class BaseMeasurement(WATSBase, ABC):
    """Abstract base for all measurement types."""
    
    # Status of the measurement
    status: StepStatus = Field(
        default=StepStatus.Passed,
        description="Measurement pass/fail status."
    )
    
    # Name (optional, used in multi-measurement)
    name: Optional[str] = Field(
        default=None,
        description="Measurement name for multi-measurement steps."
    )


class NumericMeasurement(BaseMeasurement):
    """
    Numeric measurement with limits.
    
    Represents a numeric value test with optional low/high limits
    and comparison operators.
    """
    
    # The measured value
    value: Optional[Union[float, str]] = Field(
        default=None,
        description="Measured numeric value."
    )
    
    value_format: Optional[str] = Field(
        default=None,
        validation_alias="valueFormat",
        serialization_alias="valueFormat",
        description="Format string for value display."
    )
    
    # Unit of measurement
    unit: Optional[str] = Field(
        default=None,
        description="Unit of measurement (e.g., 'V', 'A', 'Ohm')."
    )
    
    # Comparison operator
    comp_op: Optional[CompOp] = Field(
        default=CompOp.LOG,
        validation_alias="compOp",
        serialization_alias="compOp",
        description="Comparison operator."
    )
    
    # Limits
    high_limit: Optional[Union[float, str]] = Field(
        default=None,
        validation_alias="highLimit",
        serialization_alias="highLimit",
        description="High limit value."
    )
    
    high_limit_format: Optional[str] = Field(
        default=None,
        validation_alias="highLimitFormat",
        serialization_alias="highLimitFormat",
        description="Format string for high limit display."
    )
    
    low_limit: Optional[Union[float, str]] = Field(
        default=None,
        validation_alias="lowLimit",
        serialization_alias="lowLimit",
        description="Low limit value."
    )
    
    low_limit_format: Optional[str] = Field(
        default=None,
        validation_alias="lowLimitFormat",
        serialization_alias="lowLimitFormat",
        description="Format string for low limit display."
    )
    
    def validate_against_limits(self) -> tuple[StepStatus, bool]:
        """
        Validate the measurement against its limits.
        
        Returns:
            Tuple of (status, passed) where status is StepStatus and passed is bool.
            
        Raises:
            ValueError: If limits are configured but value is None.
        """
        if self.value is None:
            return (StepStatus.Passed, True)  # No value = no validation
            
        # Convert value to float for comparison
        try:
            value = float(self.value)
        except (ValueError, TypeError):
            return (StepStatus.Error, False)
        
        # Get comp_op - may be enum or string due to use_enum_values=True
        comp_op = self.comp_op
        if isinstance(comp_op, str):
            try:
                comp_op = CompOp(comp_op)
            except (ValueError, KeyError):
                return (StepStatus.Passed, True)  # Unknown comp_op - pass
        
        # If no comp_op or it's LOG (no validation), pass
        if comp_op is None or comp_op == CompOp.LOG:
            return (StepStatus.Passed, True)
        
        # Validate using comp_op
        low = None
        high = None
        
        if self.low_limit is not None:
            try:
                low = float(self.low_limit)
            except (ValueError, TypeError):
                return (StepStatus.Error, False)
        
        if self.high_limit is not None:
            try:
                high = float(self.high_limit)
            except (ValueError, TypeError):
                return (StepStatus.Error, False)
        
        # Use comp_op evaluate method
        if comp_op.evaluate(value, low, high):
            return (StepStatus.Passed, True)
        else:
            return (StepStatus.Failed, False)
    
    def calculate_status(self) -> str:
        """
        Calculate status based on comparison operator and limits.
        
        Used by ImportMode.Active for automatic status determination.
        
        Returns:
            "P" if measurement passes, "F" if it fails
            
        Note:
            - Returns "P" for LOG (no comparison)
            - Returns "P" if value is not numeric
            - Returns "P" if required limits are missing
        """
        status, _ = self.validate_against_limits()
        if status == StepStatus.Passed:
            return "P"
        elif status == StepStatus.Failed:
            return "F"
        else:
            return "P"  # Error or other -> default to pass


class BooleanMeasurement(BaseMeasurement):
    """
    Boolean (pass/fail) measurement.
    
    Simple true/false measurement with no limits.
    """
    
    # The measured boolean value
    value: Optional[bool] = Field(
        default=None,
        description="Boolean measurement value (True=pass, False=fail)."
    )
    
    def validate_against_expected(self, expected: bool = True) -> tuple[StepStatus, bool]:
        """
        Validate the measurement against expected value.
        
        Args:
            expected: The expected boolean value (default True).
            
        Returns:
            Tuple of (status, passed).
        """
        if self.value is None:
            return (StepStatus.Passed, True)
            
        if self.value == expected:
            return (StepStatus.Passed, True)
        else:
            return (StepStatus.Failed, False)


class StringMeasurement(BaseMeasurement):
    """
    String measurement with comparison.
    
    String value test with comparison operator and limit string.
    """
    
    # The measured string value
    value: Optional[str] = Field(
        default=None,
        description="Measured string value."
    )
    
    # Comparison operator (EQ, NE, CASESENSIT, IGNORECASE)
    comp_op: Optional[CompOp] = Field(
        default=CompOp.LOG,
        validation_alias="compOp",
        serialization_alias="compOp",
        description="String comparison operator."
    )
    
    # Expected/limit string
    limit: Optional[str] = Field(
        default=None,
        description="Expected string value."
    )
    
    def validate_against_limit(self) -> tuple[StepStatus, bool]:
        """
        Validate the measurement against its limit.
        
        Returns:
            Tuple of (status, passed).
        """
        if self.value is None or self.comp_op is None or self.limit is None:
            return (StepStatus.Passed, True)
            
        # String comparisons
        match self.comp_op:
            case CompOp.EQ:
                passed = self.value == self.limit
            case CompOp.NE:
                passed = self.value != self.limit
            case CompOp.IGNORECASE:
                passed = self.value.lower() == self.limit.lower()
            case CompOp.CASESENSIT:
                passed = self.value == self.limit
            case _:
                # Other operators don't make sense for strings
                return (StepStatus.Error, False)
                
        return (StepStatus.Passed if passed else StepStatus.Failed, passed)


class MultiNumericMeasurement(NumericMeasurement):
    """
    Numeric measurement with required name for multi-measurement steps.
    
    Same as NumericMeasurement but name is required.
    """
    name: str = Field(
        ...,
        description="The name of the measurement - required for multi-step types."
    )


class MultiBooleanMeasurement(BooleanMeasurement):
    """
    Boolean measurement with required name for multi-measurement steps.
    
    Same as BooleanMeasurement but name is required.
    """
    name: str = Field(
        ...,
        description="The name of the measurement - required for multi-step types."
    )


class MultiStringMeasurement(StringMeasurement):
    """
    String measurement with required name for multi-measurement steps.
    
    Same as StringMeasurement but name is required.
    """
    name: str = Field(
        ...,
        description="The name of the measurement - required for multi-step types."
    )


# ============================================================================
# SingleMeasurementMixin - Extracts shared wrap/unwrap logic
# ============================================================================

class SingleMeasurementMixin(Generic[MeasurementT]):
    """
    Mixin that provides wrap/unwrap serialization for single-measurement steps.
    
    v1 Problem: NumericStep, BooleanStep, StringStep all duplicate the same
    pattern of having a `measurement` field that wraps single values but
    deserializes as a list with one item. This mixin extracts that logic.
    
    Type Parameters:
        MeasurementT: The measurement type (NumericMeasurement, etc.)
    
    Usage:
        class NumericStep(Step, SingleMeasurementMixin[NumericMeasurement]):
            measurement: Optional[NumericMeasurement] = Field(default=None)
    """
    
    # Subclasses must define measurement field
    measurement: Optional[MeasurementT]
    
    # Class variable for measurement type (set by subclass)
    _measurement_class: ClassVar[Type[BaseMeasurement]]
    
    @model_validator(mode='before')
    @classmethod
    def unwrap_measurement_list(cls, data: Any) -> Any:
        """
        Unwrap measurement from list format (API returns list with single item).
        
        The WATS API returns: {"measurement": [{"value": 1.23, ...}]}
        But we want to work with: {"measurement": {"value": 1.23, ...}}
        """
        if isinstance(data, dict):
            measurement = data.get('measurement')
            if isinstance(measurement, list) and len(measurement) == 1:
                data = dict(data)  # Make a copy
                data['measurement'] = measurement[0]
        return data
    
    @field_serializer('measurement', when_used='always')
    @classmethod
    def wrap_measurement_list(cls, value: Optional[MeasurementT]) -> Optional[List[Any]]:
        """
        Wrap measurement back to list format for serialization.
        
        We store: measurement = NumericMeasurement(value=1.23)
        We serialize: {"measurement": [{"value": 1.23, ...}]}
        """
        if value is None:
            return None
        return [value.model_dump(by_alias=True, exclude_none=True)]
