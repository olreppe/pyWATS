"""
Report Info Base Class - v3 Implementation

Base class for UUTInfo and UURInfo with common fields.
"""
from __future__ import annotations

from typing import Optional

from .common_types import (
    WATSBase,
    Field,
    field_serializer,
)


class ReportInfo(WATSBase):
    """
    Base class for report-specific information.
    
    Contains fields common to both UUT (test) and UUR (repair) reports.
    Subclassed by UUTInfo and UURInfo.
    
    JSON Naming:
        - Python: report.info.operator
        - JSON UUT: {"uut": {"user": "John"}}
        - JSON UUR: {"uur": {"user": "John"}}
    """
    
    # Operator/User who ran the test or performed repair
    operator: str = Field(
        default="",
        max_length=100,
        validation_alias="user",
        serialization_alias="user",
        description="The operator/user who ran the test or performed the repair."
    )
    
    # Comment field
    comment: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Optional comment about the test or repair."
    )
    
    # Execution time in seconds
    exec_time: Optional[float] = Field(
        default=None,
        validation_alias="execTime",
        serialization_alias="execTime",
        description="Execution time in seconds."
    )
    
    @field_serializer('exec_time', when_used='json')
    def serialize_exec_time(self, value: Optional[float]) -> Optional[float]:
        """Ensure exec_time is serialized as a number (not string)."""
        if value is None:
            return None
        return float(value)
