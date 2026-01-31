"""
Steps Package - v3 Implementation

Contains all step types and the StepList container.
"""
from __future__ import annotations

from .step_list import StepList
from .step_discriminator import discriminate_step_type, get_step_class
from .measurement import (
    BaseMeasurement,
    NumericMeasurement,
    BooleanMeasurement,
    StringMeasurement,
    SingleMeasurementMixin,
)
from .sequence_call import SequenceCall, StepType
from .numeric_step import NumericStep, MultiNumericStep
from .boolean_step import PassFailStep, BooleanStep
from .string_step import StringValueStep, StringStep
from .generic_step import GenericStep
from .action_step import ActionStep
from .chart_step import ChartStep
from .limit_measurement import LimitMeasurement

# Import CompOp from shared enums for convenience
from pywats.shared.enums import CompOp

__all__ = [
    # Container
    "StepList",
    "StepType",
    
    # Discriminator
    "discriminate_step_type",
    "get_step_class",
    
    # Measurements
    "BaseMeasurement",
    "NumericMeasurement",
    "BooleanMeasurement",
    "StringMeasurement",
    "SingleMeasurementMixin",
    "LimitMeasurement",
    
    # Step Classes
    "SequenceCall",
    "NumericStep",
    "MultiNumericStep",
    "PassFailStep",
    "BooleanStep",  # Alias
    "StringValueStep",
    "StringStep",  # Alias
    "GenericStep",
    "ActionStep",
    "ChartStep",
    
    # Enums
    "CompOp",
]
