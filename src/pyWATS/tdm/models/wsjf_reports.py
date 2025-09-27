"""
WSJF Report Models

Models for WATS Standard JSON Format (WSJF) reports.
These models match the server's expected field names and validation.

Moved from rest_api.models.wsjf_reports to consolidate TDM-related models.
"""

from typing import Optional, List, Any, Literal, Union
from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID
from pydantic import BaseModel, Field, model_validator

# Import constants from original location
from ...rest_api.models.wsjf_constants import def_MissingString


class Failure(BaseModel):
    """A failure on a unit."""
    category: str = Field(..., min_length=1, description="The failure category")
    code: str = Field(..., min_length=1, description="The failure category code")
    comment: Optional[str] = Field(default=None, description="A comment about the failure")
    com_ref: Optional[str] = Field(default=None, max_length=50, min_length=1, alias="comRef", description="Component reference")
    art_number: Optional[str] = Field(default=None, max_length=100, alias="artNumber", description="Article number of failed component")
    art_rev: Optional[str] = Field(default=None, max_length=100, alias="artRev", description="Article revision of failed component")
    art_vendor: Optional[str] = Field(default=None, max_length=100, alias="artVendor", description="Article vendor of failed component")
    art_description: Optional[str] = Field(default=None, max_length=100, alias="artDescription", description="Article description of failed component")
    func_block: Optional[str] = Field(default=None, max_length=100, min_length=1, alias="funcBlock", description="Component group")
    ref_step_id: Optional[int] = Field(default=None, alias="refStepId", description="Reference to UUT step that found failure")
    ref_step_name: Optional[str] = Field(default=None, alias="refStepName", description="Name of UUT step that found failure")


class SubUnit(BaseModel):
    """A sub unit. Used in UUT reports where idx is optional."""
    pn: str = Field(..., max_length=100, min_length=1, description="Part number of the sub unit")
    sn: str = Field(..., max_length=100, min_length=1, description="Serial number of the sub unit") 
    rev: Optional[str] = Field(default=None, max_length=100, min_length=0, description="Revision of the sub unit")
    part_type: Optional[str] = Field(default="Unknown", max_length=50, min_length=1, alias="partType", description="Type of sub unit")
    idx: Optional[int] = Field(default=None, description="Index of the sub unit (optional for UUT reports)")
    parent_idx: Optional[int] = Field(default=None, alias="parentIdx", description="Index of the parent sub unit")


class SubRepair(BaseModel):
    """A sub repair unit for UUR reports with required idx and failure tracking."""
    pn: str = Field(..., max_length=100, min_length=1, description="Part number of the sub unit")
    sn: str = Field(..., max_length=100, min_length=1, description="Serial number of the sub unit") 
    rev: Optional[str] = Field(default=None, max_length=100, min_length=0, description="Revision of the sub unit")
    part_type: Optional[str] = Field(default="Unknown", max_length=50, min_length=1, alias="partType", description="Type of sub unit")
    idx: int = Field(..., description="Index of the sub unit. Required for UUR reports.")
    parent_idx: Optional[int] = Field(default=None, alias="parentIdx", description="Index of the parent sub unit")
    position: Optional[int] = Field(default=None, description="Position of the unit")
    replaced_idx: Optional[int] = Field(default=None, alias="replacedIdx", description="Index of the sub unit that replaced this unit")
    failures: Optional[List[Failure]] = Field(default_factory=list, description="List of failures on this sub unit")

    def add_failure(self, category: str, code: str, comment: Optional[str] = None, com_ref: Optional[str] = None) -> Failure:
        """Add a failure to this sub repair unit."""
        failure = Failure(category=category, code=code, comment=comment, comRef=com_ref)
        if self.failures is None:
            self.failures = []
        self.failures.append(failure)
        return failure


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
    fixture_id: Optional[str] = Field(default="", alias="fixtureId")


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
        
    # SubUnits
    sub_units: List[Union[SubUnit, SubRepair]] = Field(
        default_factory=list,
        alias="subUnits", 
        description="Sub units of the report"
    )

    def add_sub_unit(self, part_type: str, sn: str, pn: str, rev: str, idx: Optional[int] = None, parent_idx: Optional[int] = None) -> SubUnit:
        """Add a sub unit to the report."""
        if idx is None:
            # Auto-assign index based on existing sub units
            idx = len(self.sub_units)
        su = SubUnit(partType=part_type, sn=sn, pn=pn, rev=rev, idx=idx, parentIdx=parent_idx)
        self.sub_units.append(su)
        return su

    def add_sub_repair(self, part_type: str, sn: str, pn: str, rev: str, idx: Optional[int] = None, parent_idx: Optional[int] = None) -> SubRepair:
        """Add a sub repair unit to the report (for UUR reports)."""
        if idx is None:
            # Auto-assign index based on existing sub units
            idx = len(self.sub_units)
        sr = SubRepair(partType=part_type, sn=sn, pn=pn, rev=rev, idx=idx, parentIdx=parent_idx)
        self.sub_units.append(sr)
        return sr

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
    
    # UUT-specific info field with uut alias (overrides base info field)
    uut_info: Optional[UUTInfo] = Field(default=None, alias="uut", description="UUT-specific information")

    def __init__(self, **data):
        # Ensure type is always 'T' for UUT reports
        data['type'] = 'T'
        super().__init__(**data)
        
    def model_dump(self, **kwargs):
        """Custom serialization to exclude base info field and use uut_info with uut alias."""
        data = super().model_dump(**kwargs)
        # Remove the base info field to avoid conflicts
        data.pop('info', None)
        return data


class UURReport(WSJFReport):
    """
    Unit Under Repair (UUR) Report for repair results.
    """
    # UUT report reference for repair reports
    uut_report_id: Optional[UUID] = Field(
        default=None,
        description="Reference to the original UUT report being repaired"
    )
    
    # UUR-specific info field with uur alias (overrides base info field)
    uur_info: Optional[UURInfo] = Field(default=None, alias="uur", description="UUR-specific information")

    def __init__(self, **data):
        # Ensure type is always 'R' for UUR reports
        data['type'] = 'R'
        super().__init__(**data)
        
    def model_dump(self, **kwargs):
        """Custom serialization to exclude base info field and use uur_info with uur alias."""
        data = super().model_dump(**kwargs)
        # Remove the base info field to avoid conflicts
        data.pop('info', None)
        return data