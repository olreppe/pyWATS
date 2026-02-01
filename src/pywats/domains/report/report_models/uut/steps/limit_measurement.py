"""
Limit Measurement - v3 Implementation

Numeric measurement with high/low limit checking and automatic pass/fail.
"""
from __future__ import annotations

from typing import Optional, Union
from pywats.shared.enums import CompOp
from ...common_types import Field
from .measurement import BaseMeasurement


class LimitMeasurement(BaseMeasurement):
    """
    A measurement with limit checking.
    
    Extends BaseMeasurement with:
    - Numeric value
    - High/low limits
    - Comparison operator
    - Automatic status calculation based on limits
    """
    
    value: Union[str, float] = Field(
        ...,
        description="The measured value (numeric or string)."
    )
    
    value_format: Optional[str] = Field(
        default=None,
        validation_alias="valueFormat",
        serialization_alias="valueFormat",
        description="Format string for displaying the value."
    )

    comp_op: Optional[CompOp] = Field(
        default=CompOp.LOG,
        validation_alias="compOp",
        serialization_alias="compOp",
        description="Comparison operator for limit checking."
    )
    
    high_limit: Optional[Union[float, str]] = Field(
        default=None,
        validation_alias="highLimit",
        serialization_alias="highLimit",
        description="Upper limit for comparison."
    )
    
    high_limit_format: Optional[str] = Field(
        default=None,
        validation_alias="highLimitFormat",
        serialization_alias="highLimitFormat",
        description="Format string for displaying the high limit."
    )
    
    low_limit: Optional[Union[float, str]] = Field(
        default=None,
        validation_alias="lowLimit",
        serialization_alias="lowLimit",
        description="Lower limit for comparison."
    )
    
    low_limit_format: Optional[str] = Field(
        default=None,
        validation_alias="lowLimitFormat",
        serialization_alias="lowLimitFormat",
        description="Format string for displaying the low limit."
    )

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
        # Get the comp_op - handle both enum and string forms
        comp_op = self.comp_op
        if isinstance(comp_op, str):
            try:
                comp_op = CompOp[comp_op]
            except (KeyError, ValueError):
                return "P"  # Unknown comp_op - default to pass
        
        if comp_op is None:
            return "P"
        
        # LOG always passes
        if comp_op == CompOp.LOG:
            return "P"
        
        # Try to convert value to float for comparison
        try:
            val = float(self.value) if isinstance(self.value, str) else self.value
        except (ValueError, TypeError):
            return "P"  # Non-numeric value - default to pass
        
        # Check limits based on comparison operator
        try:
            if comp_op == CompOp.GELE:
                # Greater than low, less than or equal to high
                if self.low_limit is None or self.high_limit is None:
                    return "P"
                low = float(self.low_limit) if isinstance(self.low_limit, str) else self.low_limit
                high = float(self.high_limit) if isinstance(self.high_limit, str) else self.high_limit
                return "P" if low < val <= high else "F"
            
            elif comp_op == CompOp.GTLT:
                # Greater than low, less than high
                if self.low_limit is None or self.high_limit is None:
                    return "P"
                low = float(self.low_limit) if isinstance(self.low_limit, str) else self.low_limit
                high = float(self.high_limit) if isinstance(self.high_limit, str) else self.high_limit
                return "P" if low < val < high else "F"
            
            elif comp_op == CompOp.GELT:
                # Greater than or equal to low, less than high
                if self.low_limit is None or self.high_limit is None:
                    return "P"
                low = float(self.low_limit) if isinstance(self.low_limit, str) else self.low_limit
                high = float(self.high_limit) if isinstance(self.high_limit, str) else self.high_limit
                return "P" if low <= val < high else "F"
            
            elif comp_op == CompOp.GELE:
                # Greater than or equal to low, less than or equal to high
                if self.low_limit is None or self.high_limit is None:
                    return "P"
                low = float(self.low_limit) if isinstance(self.low_limit, str) else self.low_limit
                high = float(self.high_limit) if isinstance(self.high_limit, str) else self.high_limit
                return "P" if low <= val <= high else "F"
            
            elif comp_op == CompOp.LT:
                # Less than high
                if self.high_limit is None:
                    return "P"
                high = float(self.high_limit) if isinstance(self.high_limit, str) else self.high_limit
                return "P" if val < high else "F"
            
            elif comp_op == CompOp.LE:
                # Less than or equal to high
                if self.high_limit is None:
                    return "P"
                high = float(self.high_limit) if isinstance(self.high_limit, str) else self.high_limit
                return "P" if val <= high else "F"
            
            elif comp_op == CompOp.GT:
                # Greater than low
                if self.low_limit is None:
                    return "P"
                low = float(self.low_limit) if isinstance(self.low_limit, str) else self.low_limit
                return "P" if val > low else "F"
            
            elif comp_op == CompOp.GE:
                # Greater than or equal to low
                if self.low_limit is None:
                    return "P"
                low = float(self.low_limit) if isinstance(self.low_limit, str) else self.low_limit
                return "P" if val >= low else "F"
            
            elif comp_op == CompOp.EQ:
                # Equal to (uses low_limit as target)
                if self.low_limit is None:
                    return "P"
                target = float(self.low_limit) if isinstance(self.low_limit, str) else self.low_limit
                return "P" if val == target else "F"
            
            elif comp_op == CompOp.NE:
                # Not equal to (uses low_limit as target)
                if self.low_limit is None:
                    return "P"
                target = float(self.low_limit) if isinstance(self.low_limit, str) else self.low_limit
                return "P" if val != target else "F"
            
            else:
                return "P"  # Unknown comp_op - default to pass
                
        except (ValueError, TypeError):
            return "P"  # Conversion error - default to pass
