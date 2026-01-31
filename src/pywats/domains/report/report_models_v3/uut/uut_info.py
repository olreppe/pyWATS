"""
UUTInfo - v3 Implementation

UUT-specific ReportInfo subclass with test execution information.
Serializes as the "uut" object in JSON.

NOTE: pn, sn, rev are at the report top level, NOT in the uut object.
"""
from __future__ import annotations

from typing import Optional, List
from uuid import UUID

from ..report_info import ReportInfo
from ..common_types import Field, WATSBase


class RefUURs(WATSBase):
    """
    Repair reports that reference this test report.
    """
    
    id: UUID = Field(
        ...,
        description="ID of the referencing repair report."
    )
    
    start: Optional[str] = Field(
        default=None,
        description="Start date and time of the repair report."
    )


class UUTInfo(ReportInfo):
    """
    Unit Under Test information.
    
    Extends ReportInfo with UUT-specific test execution fields.
    This serializes as the "uut" object in JSON.
    
    NOTE: pn, sn, rev are at the report top level, NOT in this object.
    
    C# Name: UutInfo
    """
    
    # ========================================================================
    # Test Socket/Fixture
    # ========================================================================
    
    fixture_id: Optional[str] = Field(
        default="Fixture",
        max_length=100,
        validation_alias="fixtureId",
        serialization_alias="fixtureId",
        description="Fixture identifier."
    )
    
    socket_index: Optional[int] = Field(
        default=None,
        validation_alias="testSocketIndex",
        serialization_alias="testSocketIndex",
        description="Test socket index."
    )
    
    socket_index_format: Optional[str] = Field(
        default=None,
        validation_alias="testSocketIndexFormat",
        serialization_alias="testSocketIndexFormat",
        description="Test socket index format string."
    )
    
    # ========================================================================
    # Error Information
    # ========================================================================
    
    error_code: Optional[int] = Field(
        default=None,
        validation_alias="errorCode",
        serialization_alias="errorCode",
        description="Error code from test execution."
    )
    
    error_code_format: Optional[str] = Field(
        default=None,
        validation_alias="errorCodeFormat",
        serialization_alias="errorCodeFormat",
        description="Error code format string."
    )
    
    error_message: Optional[str] = Field(
        default=None,
        validation_alias="errorMessage",
        serialization_alias="errorMessage",
        description="Error message from test execution."
    )
    
    # ========================================================================
    # Batch Information
    # ========================================================================
    
    batch_number: Optional[str] = Field(
        default=None,
        max_length=100,
        validation_alias="batchSN",
        serialization_alias="batchSN",
        description="Batch serial number."
    )
    
    batch_fail_count: Optional[int] = Field(
        default=None,
        validation_alias="batchFailCount",
        serialization_alias="batchFailCount",
        description="Batch fail count."
    )
    
    batch_fail_count_format: Optional[str] = Field(
        default=None,
        validation_alias="batchFailCountFormat",
        serialization_alias="batchFailCountFormat",
        description="Batch fail count format string."
    )
    
    batch_loop_index: Optional[int] = Field(
        default=None,
        validation_alias="batchLoopIndex",
        serialization_alias="batchLoopIndex",
        description="Batch loop index."
    )
    
    batch_loop_index_format: Optional[str] = Field(
        default=None,
        validation_alias="batchLoopIndexFormat",
        serialization_alias="batchLoopIndexFormat",
        description="Batch loop index format string."
    )
    
    # ========================================================================
    # Failure Tracking
    # ========================================================================
    
    step_id_caused_uut_failure: Optional[int] = Field(
        default=None,
        validation_alias="stepIdCausedUUTFailure",
        serialization_alias="stepIdCausedUUTFailure",
        description="Step ID that caused the UUT failure."
    )
    
    referenced_by_uurs: Optional[List[RefUURs]] = Field(
        default=None,
        validation_alias="referencedByUURs",
        serialization_alias="referencedByUURs",
        description="Repair reports that reference this test report."
    )
