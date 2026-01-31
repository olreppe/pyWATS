"""
Step Type Discriminator - v3 Implementation

Maps stepType values to their corresponding step classes for polymorphic
deserialization.

This is a function rather than a dict to allow lazy import of step classes,
avoiding circular import issues.
"""
from __future__ import annotations

from typing import Dict, Any
from pydantic_core import CoreSchema, core_schema


def discriminate_step_type() -> Dict[str, CoreSchema]:
    """
    Return mapping from stepType values to Pydantic core schemas.
    
    This function is called lazily to avoid circular imports.
    All step classes are imported here and mapped to their stepType discriminator.
    
    Returns:
        Dict mapping stepType strings to CoreSchema for each step class.
    """
    # Import step classes here to avoid circular imports
    from .sequence_call import SequenceCall
    from .numeric_step import NumericStep, MultiNumericStep
    from .boolean_step import PassFailStep
    from .string_step import StringValueStep
    from .generic_step import GenericStep
    from .action_step import ActionStep
    from .chart_step import ChartStep
    
    return {
        # Sequence/container step
        'SequenceCall': SequenceCall.__pydantic_core_schema__,
        
        # Measurement steps
        'NumericLimitTest': NumericStep.__pydantic_core_schema__,
        'ET_NLT': NumericStep.__pydantic_core_schema__,  # TestStand alias
        'MultiNumericLimitTest': MultiNumericStep.__pydantic_core_schema__,
        'ET_MNLT': MultiNumericStep.__pydantic_core_schema__,  # TestStand alias
        
        # Pass/Fail step
        'PassFailTest': PassFailStep.__pydantic_core_schema__,
        'ET_PFT': PassFailStep.__pydantic_core_schema__,  # TestStand alias
        
        # String value step
        'StringValueTest': StringValueStep.__pydantic_core_schema__,
        'ET_SVT': StringValueStep.__pydantic_core_schema__,  # TestStand alias
        
        # Generic/custom step
        'GenericTest': GenericStep.__pydantic_core_schema__,
        
        # Chart step
        'Chart': ChartStep.__pydantic_core_schema__,
        
        # Action step (no measurement)
        'Action': ActionStep.__pydantic_core_schema__,
        
        # Catch-all for unknown types - defaults to GenericStep
        'NONE': GenericStep.__pydantic_core_schema__,
    }


def get_step_class(step_type: str) -> Any:
    """
    Get the step class for a given step type.
    
    Args:
        step_type: The stepType discriminator value
        
    Returns:
        The step class for the given type, or UnknownStep if unknown.
    """
    from .sequence_call import SequenceCall
    from .numeric_step import NumericStep, MultiNumericStep
    from .boolean_step import PassFailStep
    from .string_step import StringValueStep
    from .generic_step import GenericStep
    from .action_step import ActionStep
    from .chart_step import ChartStep
    from .unknown_step import UnknownStep
    
    mapping = {
        'SequenceCall': SequenceCall,
        'NumericLimitTest': NumericStep,
        'ET_NLT': NumericStep,
        'MultiNumericLimitTest': MultiNumericStep,
        'ET_MNLT': MultiNumericStep,
        'PassFailTest': PassFailStep,
        'ET_PFT': PassFailStep,
        'StringValueTest': StringValueStep,
        'ET_SVT': StringValueStep,
        'GenericTest': GenericStep,
        'Chart': ChartStep,
        'Action': ActionStep,
        'NONE': GenericStep,
    }
    
    return mapping.get(step_type, UnknownStep)
