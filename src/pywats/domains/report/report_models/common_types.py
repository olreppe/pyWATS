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
    """
    Step execution status with flexible string conversion.
    
    Accepts multiple input formats:
    - Exact values: "P", "F", "S", "D", "E", "T"
    - Full names: "Passed", "Failed", "Skipped", "Done", "Error", "Terminated"
    - Case-insensitive: "PASSED", "passed", "Pass", etc.
    - Common aliases: "OK", "pass", "fail", etc.
    
    Always serializes to single-letter WATS API format ("P", "F", etc.).
    
    Examples:
        >>> StepStatus("P")           # Exact value
        >>> StepStatus("Passed")      # Full name
        >>> StepStatus("PASSED")      # Case-insensitive
        >>> StepStatus("pass")        # Lowercase
        >>> StepStatus("OK")          # Alias for Passed
        >>> status.value              # Always returns "P"
    """
    Passed = "P"
    Failed = "F"
    Skipped = "S"
    Done = "D"
    Error = "E"
    Terminated = "T"
    
    @classmethod
    def _missing_(cls, value: Any) -> "StepStatus":
        """
        Handle flexible string conversion.
        
        Tries:
        1. Case-insensitive match against enum values ("P", "F", etc.)
        2. Case-insensitive match against member names ("Passed", "Failed", etc.)
        3. Alias lookup ("OK" → "P", "fail" → "F", etc.)
        
        Raises:
            ValueError: If value cannot be converted to valid status
        """
        if not isinstance(value, str):
            raise ValueError(
                f"StepStatus value must be string, got {type(value).__name__}"
            )
        
        # Try case-insensitive match against enum values ("P", "F", etc.)
        value_upper = value.upper()
        for member in cls:
            if member.value.upper() == value_upper:
                return member
        
        # Try case-insensitive match against member names ("Passed", "Failed", etc.)
        value_lower = value.lower()
        for member in cls:
            if member.name.lower() == value_lower:
                return member
        
        # Try alias lookup (defined outside class as class attribute)
        canonical = StepStatus._STEP_ALIASES.get(value_lower)
        if canonical:
            return cls._value2member_map_[canonical]
        
        # No match found - provide helpful error message
        valid_options = ", ".join(m.name for m in cls)
        raise ValueError(
            f"Invalid step status: '{value}'. "
            f"Valid options: {valid_options} "
            "(case-insensitive, also accepts single letters and aliases like 'OK')"
        )
    
    @property
    def full_name(self) -> str:
        """Get full word representation (e.g., 'Passed')."""
        return self.name
    
    @property
    def is_passing(self) -> bool:
        """True if status indicates a passing result."""
        return self in (StepStatus.Passed, StepStatus.Done)
    
    @property
    def is_failure(self) -> bool:
        """True if status indicates a failure."""
        return self in (StepStatus.Failed, StepStatus.Error, StepStatus.Terminated)

# Alias mappings for StepStatus (defined outside class to avoid becoming enum member)
StepStatus._STEP_ALIASES = {
    # Passed variations
    "p": "P",
    "pass": "P",
    "passed": "P",
    "ok": "P",
    "success": "P",
    "successful": "P",
    
    # Failed variations
    "f": "F",
    "fail": "F",
    "failed": "F",
    "failure": "F",
    "ng": "F",  # Common in manufacturing (Not Good)
    
    # Skipped variations
    "s": "S",
    "skip": "S",
    "skipped": "S",
    
    # Done variations
    "d": "D",
    "done": "D",
    "complete": "D",
    "completed": "D",
    
    # Error variations
    "e": "E",
    "err": "E",
    "error": "E",
    
    # Terminated variations
    "t": "T",
    "term": "T",
    "terminated": "T",
    "abort": "T",
    "aborted": "T",
}


class ReportStatus(str, Enum):
    """
    Overall report status with flexible string conversion.
    
    Accepts multiple input formats:
    - Exact values: "P", "F", "D", "E", "T"
    - Full names: "Passed", "Failed", "Done", "Error", "Terminated"
    - Case-insensitive: "PASSED", "passed", etc.
    - Common aliases: "OK", "pass", "fail", etc.
    
    Always serializes to single-letter WATS API format ("P", "F", etc.).
    
    Note: ReportStatus does not include "Skipped" (only at step level).
    """
    Passed = "P"
    Failed = "F"
    Done = "D"
    Error = "E"
    Terminated = "T"
    
    @classmethod
    def _missing_(cls, value: Any) -> "ReportStatus":
        """Handle flexible string conversion (same logic as StepStatus)."""
        if not isinstance(value, str):
            raise ValueError(
                f"ReportStatus value must be string, got {type(value).__name__}"
            )
        
        value_upper = value.upper()
        for member in cls:
            if member.value.upper() == value_upper:
                return member
        
        value_lower = value.lower()
        for member in cls:
            if member.name.lower() == value_lower:
                return member
        
        canonical = ReportStatus._REPORT_ALIASES.get(value_lower)
        if canonical:
            return cls._value2member_map_[canonical]
        
        valid_options = ", ".join(m.name for m in cls)
        raise ValueError(
            f"Invalid report status: '{value}'. "
            f"Valid options: {valid_options} "
            "(case-insensitive, also accepts single letters and aliases like 'OK')"
        )
    
    @property
    def full_name(self) -> str:
        """Get full word representation."""
        return self.name
    
    @property
    def is_passing(self) -> bool:
        """True if status indicates a passing result."""
        return self in (ReportStatus.Passed, ReportStatus.Done)
    
    @property
    def is_failure(self) -> bool:
        """True if status indicates a failure."""
        return self in (ReportStatus.Failed, ReportStatus.Error, ReportStatus.Terminated)

# Alias mappings for ReportStatus (same as StepStatus but without Skipped)
ReportStatus._REPORT_ALIASES = {
    "p": "P",
    "pass": "P",
    "passed": "P",
    "ok": "P",
    "success": "P",
    "successful": "P",
    
    "f": "F",
    "fail": "F",
    "failed": "F",
    "failure": "F",
    "ng": "F",
    
    "d": "D",
    "done": "D",
    "complete": "D",
    "completed": "D",
    
    "e": "E",
    "err": "E",
    "error": "E",
    
    "t": "T",
    "term": "T",
    "terminated": "T",
    "abort": "T",
    "aborted": "T",
}


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
