"""
UURInfo - v3 Implementation

UUR-specific info with dual process code architecture.
Links repair report to original failed UUT report.
"""
from __future__ import annotations

from typing import Optional
from datetime import datetime
from uuid import UUID

from ..report_info import ReportInfo
from ..common_types import Field


class UURInfo(ReportInfo):
    """
    UUR-specific information.
    
    Key feature: Dual process code architecture
    - repair_process_code: What kind of repair this is
    - test_operation_code: Original test that was being performed
    
    C# Name: UUR_type
    """
    
    # ========================================================================
    # Dual Process Codes (Key Feature)
    # ========================================================================
    
    repair_process_code: Optional[int] = Field(
        default=None,
        validation_alias="repairProcessCode",
        serialization_alias="repairProcessCode",
        description="Repair process code - what kind of repair operation."
    )
    
    repair_process_name: Optional[str] = Field(
        default=None,
        validation_alias="repairProcessName",
        serialization_alias="repairProcessName",
        description="Repair process name."
    )
    
    test_operation_code: Optional[int] = Field(
        default=None,
        validation_alias="testOperationCode",
        serialization_alias="testOperationCode",
        description="Original test operation code that was being performed."
    )
    
    test_operation_name: Optional[str] = Field(
        default=None,
        validation_alias="testOperationName",
        serialization_alias="testOperationName",
        description="Original test operation name."
    )
    
    test_operation_guid: Optional[UUID] = Field(
        default=None,
        validation_alias="testOperationGuid",
        serialization_alias="testOperationGuid",
        description="Original test operation GUID."
    )
    
    # ========================================================================
    # API-Required Process Code (in uur object)
    # ========================================================================
    
    process_code: Optional[int] = Field(
        default=None,
        validation_alias="processCode",
        serialization_alias="processCode",
        description="Process code (required by API in uur object)."
    )
    
    process_code_format: Optional[str] = Field(
        default=None,
        validation_alias="processCodeFormat",
        serialization_alias="processCodeFormat",
        description="Process code format string."
    )
    
    process_name: Optional[str] = Field(
        default=None,
        validation_alias="processName",
        serialization_alias="processName",
        description="Process name."
    )
    
    # ========================================================================
    # UUT Reference (Links Repair to Failed Test)
    # ========================================================================
    
    ref_uut: Optional[UUID] = Field(
        default=None,
        validation_alias="refUUT",
        serialization_alias="refUUT",
        description="GUID of the UUT report being repaired."
    )
    
    # ========================================================================
    # Timing
    # ========================================================================
    
    confirm_date: Optional[datetime] = Field(
        default=None,
        validation_alias="confirmDate",
        serialization_alias="confirmDate",
        description="Date/time UUR was confirmed (UTC)."
    )
    
    finalize_date: Optional[datetime] = Field(
        default=None,
        validation_alias="finalizeDate",
        serialization_alias="finalizeDate",
        description="Date/time UUR was finalized (UTC)."
    )
    
    # ========================================================================
    # Status
    # ========================================================================
    
    active: bool = Field(
        default=True,
        description="Whether this UUR is active."
    )
    
    parent: Optional[UUID] = Field(
        default=None,
        description="Parent UUR GUID (for hierarchical repairs)."
    )
