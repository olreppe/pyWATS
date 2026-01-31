"""
Common Types for v3 Report Models

This module provides all shared types, enums, and utilities.
NO WILDCARD IMPORTS - everything is explicit for mypy --strict compatibility.
"""
from __future__ import annotations

# Standard library - explicit imports only
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Union,
    Literal,
    List,
    Dict,
    Annotated,
    ClassVar,
    TypeVar,
    Generic,
    Callable,
    Sequence,
    Tuple,
    overload,
)
from datetime import datetime, timezone, timedelta
from enum import Enum, IntEnum
from uuid import uuid4, UUID
from abc import ABC, abstractmethod
from decimal import Decimal

# Pydantic - explicit imports only  
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    model_validator,
    field_validator,
    field_serializer,
    computed_field,
    PrivateAttr,
)

# Import CompOp from shared enums (single source of truth)
from pywats.shared.enums import CompOp

from pydantic_core import core_schema

# Type variable for generic Step parent
if TYPE_CHECKING:
    from .uut.steps.sequence_call import SequenceCall

# Re-export base class
from .wats_base import WATSBase, DeserializationContext


# ============================================================================
# Enums
# ============================================================================

class StepStatus(str, Enum):
    """Step execution status."""
    Passed = "P"
    Failed = "F"
    Skipped = "S"
    Done = "D"
    Error = "E"
    Terminated = "T"


class ReportStatus(str, Enum):
    """Overall report status."""
    Passed = "P"
    Failed = "F"
    Done = "D"
    Error = "E"
    Terminated = "T"


# Alias for backwards compatibility (if needed)
ReportResult = ReportStatus


class StepGroup(str, Enum):
    """Step group classification."""
    Setup = "S"
    Main = "M"
    Cleanup = "C"


class ReportType(str, Enum):
    """Report type discriminator."""
    UUT = "T"  # Test/UUT Report
    UUR = "R"  # Repair/UUR Report


class ChartType(str, Enum):
    """Chart visualization types."""
    LINE = "Line"
    LINE_LOG_XY = "LineLogXY"
    LINE_LOG_X = "LineLogX"
    LINE_LOG_Y = "LineLogY"



# CompOp imported from shared enums (see below)

class FlowType(str, Enum):
    """Flow control step types for GenericStep."""
    NOP = "NOP"
    Statement = "Statement"
    Label = "Label"
    Goto = "Goto"
    WATS_Goto = "WATS_Goto"
    Flow_If = "Flow_If"
    Flow_ElseIf = "Flow_ElseIf"
    Flow_Else = "Flow_Else"
    Flow_End = "Flow_End"
    Flow_For = "Flow_For"
    Flow_ForEach = "Flow_ForEach"
    Flow_Break = "Flow_Break"
    Flow_Continue = "Flow_Continue"
    Flow_EndLoop = "Flow_EndLoop"
    Flow_While = "Flow_While"
    Flow_DoWhile = "Flow_DoWhile"
    Flow_Select = "Flow_Select"
    Flow_Case = "Flow_Case"
    Flow_Default = "Flow_Default"
    Flow_EndSelect = "Flow_EndSelect"


# ============================================================================
# Validation Utilities
# ============================================================================

# Import actual validation functions from core module
from pywats.core.validation import (
    validate_serial_number,
    validate_part_number,
    PROBLEMATIC_CHARS,
)


# ============================================================================
# Shared Field Definitions  
# ============================================================================

def create_sn_field(
    description: str = "Serial number",
    **kwargs: Any
) -> Any:
    """Create a standardized serial number field."""
    return Field(
        ...,
        max_length=100,
        min_length=1,
        description=description,
        **kwargs
    )


def create_pn_field(
    description: str = "Part number", 
    **kwargs: Any
) -> Any:
    """Create a standardized part number field."""
    return Field(
        ...,
        max_length=100,
        min_length=1,
        description=description,
        **kwargs
    )


def create_rev_field(
    description: str = "Revision",
    required: bool = True,
    **kwargs: Any
) -> Any:
    """Create a standardized revision field."""
    if required:
        return Field(
            ...,
            max_length=100,
            min_length=1,
            description=description,
            **kwargs
        )
    return Field(
        default=None,
        max_length=100,
        description=description,
        **kwargs
    )


# ============================================================================
# Type Aliases
# ============================================================================

# Numeric value that may come as string (e.g., "NaN", "Inf")
NumericValue = Union[float, int, str]

# Limit value - can be None, numeric, or string representation
LimitValue = Optional[Union[float, str]]

# JSON-serializable dictionary
JsonDict = Dict[str, Any]

# Status string literal
StatusLiteral = Literal["P", "F", "S", "D", "E", "T"]

# Group string literal
GroupLiteral = Literal["S", "M", "C"]


# ============================================================================
# Sequence Call Info - Additional info in sequence call steps
# ============================================================================

class SequenceCallInfo(WATSBase):
    """
    Sequence call information for SequenceCall steps.
    
    Contains path, name, and version of the sequence file.
    Serializes to 'seqCall' in JSON output.
    """
    # Fields - path, name, and version are required by the server
    path: str = Field(default="C:/SequenceCall.seq", max_length=500)
    file_name: str = Field(
        default="TestSequence.seq", 
        max_length=200, 
        validation_alias="name", 
        serialization_alias="name"
    )
    version: str = Field(default="1.0.0", max_length=30)
    
    @model_validator(mode='before')
    @classmethod
    def set_defaults(cls, data):
        """If required fields are None, null, or missing, use sensible defaults."""
        if isinstance(data, dict):
            # Handle missing OR null values
            if not data.get('version'):
                data['version'] = '1.0.0'
            if not data.get('path'):
                data['path'] = 'C:/SequenceCall.seq'
            if not data.get('name'):
                data['name'] = 'TestSequence.seq'
        return data


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Base class
    'WATSBase',
    'DeserializationContext',
    
    # Typing
    'TYPE_CHECKING',
    'Any',
    'Optional',
    'Union',
    'Literal',
    'List',
    'Dict',
    'Annotated',
    'ClassVar',
    'TypeVar',
    'Generic',
    'Callable',
    'Sequence',
    'Tuple',
    'overload',
    
    # Datetime
    'datetime',
    'timezone',
    'timedelta',
    
    # Enum
    'Enum',
    'IntEnum',
    
    # UUID
    'uuid4',
    'UUID',
    
    # ABC
    'ABC',
    'abstractmethod',
    
    # Decimal
    'Decimal',
    
    # Pydantic
    'BaseModel',
    'ConfigDict',
    'Field',
    'ValidationInfo',
    'model_validator',
    'field_validator',
    'field_serializer',
    'computed_field',
    'PrivateAttr',
    'core_schema',
    
    # Enums
    'StepStatus',
    'ReportResult', 
    'StepGroup',
    'ReportType',
    'ChartType',
    'CompOp',
    'FlowType',
    
    # Sequence call info
    'SequenceCallInfo',
    
    # Validation utilities
    'validate_serial_number',
    'validate_part_number',
    'PROBLEMATIC_CHARS',
    
    # Field factories
    'create_sn_field',
    'create_pn_field', 
    'create_rev_field',
    
    # Type aliases
    'NumericValue',
    'LimitValue',
    'JsonDict',
    'StatusLiteral',
    'GroupLiteral',
]
