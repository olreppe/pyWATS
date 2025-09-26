"""
WSJF Report Models

Models for WATS Standard JSON Format (WSJF) reports.
These models match the server's expected field names and validation.
"""

from typing import Optional, List, Any, Literal, Union
from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID
from pydantic import BaseModel, Field, model_validator

from .wsjf_constants import def_MissingString


class MiscInfo(BaseModel):
    """
    MiscInfo, or Miscellaneous information provides a key-value pair of properties 
    that can be used to log unit configurations that has no dedicated header field.
    """
    id: Optional[str] = Field(default=None, description="Index")
    description: str = Field(..., min_length=1, description="The misc infos display name/key")
    string_value: Optional[str] = Field(
        default=None, 
        max_length=100, 
        min_length=0, 
        alias="text",
        description="The misc info value as string."
    )
    numeric_value: Optional[int] = Field(
        default=None,
        deprecated=True, 
        alias="numeric",
        description="Numeric value. Not available for analysis - use string_value"
    )
    type_def: Optional[str] = Field(
        default=None, 
        max_length=30, 
        min_length=0, 
        alias="typedef",
        description="Type definition"
    )
    numeric_format: Optional[str] = Field(
        default=None, 
        deprecated=True, 
        alias="numericFormat",
        description="Numeric format"
    )


class SequenceCallInfo(BaseModel):
    """Sequence call info for UUT reports."""
    path: Optional[str] = Field(default="MainSequence", max_length=500)
    name: Optional[str] = Field(default="MainSequence", max_length=200, alias="name")
    version: Optional[str] = Field(default="1.0", max_length=30)


class SequenceCall(BaseModel):
    """Minimal sequence call for UUT reports."""
    step_type: str = Field(default="SequenceCall", alias="stepType")
    name: str = Field(default="MainSequence")
    group: str = Field(default="M", description="Step group")
    status: str = Field(default="P", description="Step status")
    seq_call: SequenceCallInfo = Field(default_factory=SequenceCallInfo, alias="seqCall")
    steps: List[Any] = Field(default_factory=list)


class ReportInfo(BaseModel):
    """
    Generic info class for both UUT & UUR reports.
    """
    operator: str = Field(
        default="Operator", 
        max_length=100, 
        min_length=1, 
        alias="user",
        description="The name or ID of the operator"
    )
    comment: Optional[str] = Field(
        default=None, 
        max_length=5000, 
        min_length=0,
        description="Report comment"
    )
    exec_time: Optional[float] = Field(
        default=0.0, 
        alias="execTime",
        description="The execution time of the test in seconds."
    )
    exec_time_format: Optional[str] = Field(
        default=None, 
        alias="execTimeFormat",
        description="Execution time format"
    )

    @model_validator(mode="before")
    @classmethod
    def replace_none_during_deserialization(cls, data):
        if isinstance(data, dict):
            if data.get("user") in (None, ""):
                data["user"] = "Operator"
        return data


class UUTInfo(ReportInfo):
    """UUT-specific information."""
    fixture_id: str = Field(default="", alias="fixtureId")


class UURInfo(ReportInfo):
    """UUR-specific information with required fields."""
    process_code: Optional[int] = Field(default=None, alias="processCode")
    process_code_format: Optional[str] = Field(default=None, alias="processCodeFormat")  
    process_name: Optional[str] = Field(default=None, alias="processName")
    ref_uut: Optional[str] = Field(default=None, alias="refUUT")
    confirm_date: Optional[str] = Field(default=None, alias="confirmDate")
    finalize_date: Optional[str] = Field(default=None, alias="finalizeDate")


class ReportStatus(str, Enum):
    """
    Report status enumeration.
    P = Passed, F = Failed, S = Skipped, D = Done, E = Error, T = Terminated
    """
    Passed = 'P'
    Failed = 'F'
    Skipped = 'S'
    Done = 'D'
    Error = 'E'
    Terminated = 'T'


class WSJFReport(BaseModel):
    """
    Base class for WSJF reports (UUT and UUR).
    Contains all the required fields that the WATS server expects.
    """
    # Required fields for WSJF format
    id: UUID = Field(
        default_factory=uuid4, 
        description="A UUID identifying the report. Submitting a report with an existing id will overwrite the existing report."
    )
    type: str = Field(
        ..., 
        max_length=1, 
        min_length=1, 
        pattern='^[TR]$',
        description="The type of report. 'T'=TestReport(UUT) 'R'=RepairReport(UUR)"
    )
    pn: str = Field(
        ..., 
        max_length=100, 
        min_length=1,
        description="The part number of the unit tested or repaired."
    )
    sn: str = Field(
        ..., 
        max_length=100, 
        min_length=1, 
        description="The serial number of the unit tested or repaired."
    )
    rev: str = Field(
        ..., 
        max_length=100, 
        min_length=1, 
        description="The revision of the unit(part number) tested or repaired."
    )
    
    # Process code with alias for server compatibility
    process_code: int = Field(
        ..., 
        alias="processCode", 
        description="The process code for the operation type"
    )
    
    # Report result
    result: str = Field(
        default="P", 
        max_length=1, 
        min_length=1, 
        pattern='^[PFDET]$',
        description="Report result: P=Passed, F=Failed, D=Done, E=Error, T=Terminated"
    )
    
    # Station info - machineName is the alias the server expects
    station_name: str = Field(
        ..., 
        max_length=100, 
        min_length=1, 
        alias="machineName",
        description="The name of the test station/machine"
    )
    location: str = Field(
        ..., 
        max_length=100, 
        min_length=1,
        description="The location where the test was performed"
    )
    purpose: str = Field(
        ..., 
        max_length=100, 
        min_length=1,
        description="The purpose of the test"
    )

    # Timing - start is the field name the server expects
    start: datetime = Field(
        default_factory=lambda: datetime.now().astimezone(), 
        description="Start time of the report"
    )
    start_utc: Optional[datetime] = Field(
        default=None, 
        alias="startUTC", 
        exclude=True,
        description="UTC start time (excluded from serialization)"
    )
   
    # Optional info - can be ReportInfo, UUTInfo, or UURInfo  
    info: Optional[Union[ReportInfo, "UUTInfo", "UURInfo"]] = Field(default=None, description="Additional report information")
    
    # Miscellaneous information
    misc_infos: List[MiscInfo] = Field(
        default_factory=list, 
        alias="miscInfos",
        description="Miscellaneous information"
    )

    def add_misc_info(self, description: str, value: Any) -> MiscInfo:
        """Add miscellaneous information to the report."""
        str_val = str(value)
        mi = MiscInfo(description=description, text=str_val)
        self.misc_infos.append(mi)
        return mi

    # Model validator to inject defaults for missing requirements when deserializing
    @model_validator(mode="before")
    @classmethod
    def replace_none_during_deserialization(cls, data):
        if isinstance(data, dict):
            # Replace None values with defaults for required fields
            for key in ["pn", "sn", "rev", "machineName", "location", "purpose"]:
                if data.get(key) in (None, ""):
                    data[key] = def_MissingString
        return data

    model_config = {"populate_by_name": True}  # Allows deserialization using alias names


class UUTReport(WSJFReport):
    """
    Unit Under Test (UUT) Report for test results.
    """
    # Required root sequence call for UUT reports
    root: SequenceCall = Field(default_factory=SequenceCall, description="Root sequence call")

    def __init__(self, **data):
        # Ensure type is always 'T' for UUT reports
        data['type'] = 'T'
        # Create default UUT info if not provided
        if 'info' not in data and 'uut' not in data:
            data['uut'] = UUTInfo()
        super().__init__(**data)


class UURReport(WSJFReport):
    """
    Unit Under Repair (UUR) Report for repair results.
    """
    # UUT report reference for repair reports
    uut_report_id: Optional[UUID] = Field(
        default=None,
        description="Reference to the original UUT report being repaired"
    )

    def __init__(self, **data):
        # Ensure type is always 'R' for UUR reports
        data['type'] = 'R'
        
        # Get process code from the report level
        process_code = data.get('process_code', 0)
        uut_ref = data.get('uut_report_id')
        
        # Create default UUR info with required fields if not provided
        if 'info' not in data and 'uur' not in data:
            data['uur'] = UURInfo(
                processCode=process_code,
                refUUT=str(uut_ref) if uut_ref else None,
                confirmDate=datetime.now().isoformat() + "Z",
                finalizeDate=datetime.now().isoformat() + "Z"
            )
        
        super().__init__(**data)