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


class ReportResult(str, Enum):
    """Overall report result."""
    Passed = "P"
    Failed = "F"
    Done = "D"
    Error = "E"
    Terminated = "T"


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
    LineChart = "LineChart"
    XYGraph = "XYGraph"
    BarChart = "BarChart"
    Histogram = "Histogram"
    ScatterPlot = "ScatterPlot"


class CompOp(str, Enum):
    """
    Comparison operators for measurements.
    
    Defines how measured values are compared against limits.
    """
    LOG = "LOG"      # No comparison, just log
    EQ = "EQ"        # Equal
    NE = "NE"        # Not Equal
    LT = "LT"        # Less Than
    LE = "LE"        # Less Than or Equal
    GT = "GT"        # Greater Than
    GE = "GE"        # Greater Than or Equal
    GELE = "GELE"    # Between (inclusive): low <= value <= high
    GTLT = "GTLT"    # Between (exclusive): low < value < high
    GELT = "GELT"    # low <= value < high
    GTLE = "GTLE"    # low < value <= high
    LTGT = "LTGT"    # Outside (exclusive): value < low OR value > high
    LEGE = "LEGE"    # Outside (inclusive): value <= low OR value >= high
    CASESENSITIVESTRINGCOMPARE = "CASESENSITIVESTRINGCOMPARE"
    CASEINSENSITIVESTRINGCOMPARE = "CASEINSENSITIVESTRINGCOMPARE"
    CASELESSEQ = "CASELESSEQ"    # Case-insensitive equal
    CASELESSNE = "CASELESSNE"    # Case-insensitive not equal

    def validate_limits(
        self, 
        low_limit: Optional[float] = None, 
        high_limit: Optional[float] = None
    ) -> bool:
        """
        Validate that the required limits are provided for this comparison operator.
        
        Returns True if limits are valid for the operator, False otherwise.
        """
        # Operators requiring no limits
        if self in (CompOp.LOG,):
            return True
            
        # Operators requiring only low limit
        if self in (CompOp.GE, CompOp.GT):
            return low_limit is not None
            
        # Operators requiring only high limit  
        if self in (CompOp.LE, CompOp.LT):
            return high_limit is not None
            
        # Operators requiring both limits
        if self in (CompOp.GELE, CompOp.GTLT, CompOp.GELT, CompOp.GTLE, 
                    CompOp.LTGT, CompOp.LEGE):
            return low_limit is not None and high_limit is not None
            
        # String comparison and EQ/NE - no numeric limits needed
        if self in (CompOp.EQ, CompOp.NE, 
                    CompOp.CASESENSITIVESTRINGCOMPARE, 
                    CompOp.CASEINSENSITIVESTRINGCOMPARE):
            return True
            
        return True
    
    def evaluate(
        self,
        value: float,
        low_limit: Optional[float] = None,
        high_limit: Optional[float] = None,
        string_value: Optional[str] = None,
        string_limit: Optional[str] = None,
    ) -> bool:
        """
        Evaluate if a value passes this comparison.
        
        Returns True if value passes, False if it fails.
        """
        # Handle special float values
        if value != value:  # NaN check
            return False
            
        if self == CompOp.LOG:
            return True
        elif self == CompOp.EQ:
            if low_limit is not None:
                return value == low_limit
            return True
        elif self == CompOp.NE:
            if low_limit is not None:
                return value != low_limit
            return True
        elif self == CompOp.LT:
            return high_limit is not None and value < high_limit
        elif self == CompOp.LE:
            return high_limit is not None and value <= high_limit
        elif self == CompOp.GT:
            return low_limit is not None and value > low_limit
        elif self == CompOp.GE:
            return low_limit is not None and value >= low_limit
        elif self == CompOp.GELE:
            return (low_limit is not None and high_limit is not None and 
                    low_limit <= value <= high_limit)
        elif self == CompOp.GTLT:
            return (low_limit is not None and high_limit is not None and 
                    low_limit < value < high_limit)
        elif self == CompOp.GELT:
            return (low_limit is not None and high_limit is not None and 
                    low_limit <= value < high_limit)
        elif self == CompOp.GTLE:
            return (low_limit is not None and high_limit is not None and 
                    low_limit < value <= high_limit)
        elif self == CompOp.LTGT:
            return (low_limit is not None and high_limit is not None and 
                    (value < low_limit or value > high_limit))
        elif self == CompOp.LEGE:
            return (low_limit is not None and high_limit is not None and 
                    (value <= low_limit or value >= high_limit))
        elif self == CompOp.CASESENSITIVESTRINGCOMPARE:
            return string_value == string_limit if string_limit else True
        elif self == CompOp.CASEINSENSITIVESTRINGCOMPARE:
            if string_value and string_limit:
                return string_value.lower() == string_limit.lower()
            return True
            
        return True


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

# Characters that cause issues in WATS API
PROBLEMATIC_CHARS = ['/', '\\', '<', '>', ':', '"', '|', '?', '*']


def validate_serial_number(sn: str) -> str:
    """
    Validate and clean serial number.
    
    Warns if problematic characters are found but allows them through
    since the WATS API may handle them.
    """
    for char in PROBLEMATIC_CHARS:
        if char in sn:
            # Could log warning here
            pass
    return sn


def validate_part_number(pn: str) -> str:
    """
    Validate and clean part number.
    
    Warns if problematic characters are found but allows them through.
    """
    for char in PROBLEMATIC_CHARS:
        if char in pn:
            # Could log warning here
            pass
    return pn


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
