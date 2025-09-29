"""
Complete WSJF report models implementing full step hierarchy.
Based on C# Interface.TDM pattern: UUT creates sequence, sequence creates steps, steps create measurements.
"""
from typing import List, Optional, Dict, Any, Union, Literal
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID

# Import constants from original location
from ...rest_api.models.wsjf_constants import def_MissingString


class StepStatusType(str, Enum):
    """Step status enumeration matching C# StepStatusType"""
    PASSED = "Passed"
    FAILED = "Failed"
    ERROR = "Error"
    TERMINATED = "Terminated"
    DONE = "Done"
    SKIPPED = "Skipped"
    RUNNING = "Running"


class CompOperatorType(str, Enum):
    """Comparison operator types for numeric limits"""
    EQ = "EQ"  # Equal
    NE = "NE"  # Not Equal
    GT = "GT"  # Greater Than
    GE = "GE"  # Greater or Equal
    LT = "LT"  # Less Than
    LE = "LE"  # Less or Equal
    GELE = "GELE"  # Greater or Equal AND Less or Equal (between)
    GTLT = "GTLT"  # Greater Than AND Less Than
    GELT = "GELT"  # Greater or Equal AND Less Than
    GTLE = "GTLE"  # Greater Than AND Less or Equal
    LTGT = "LTGT"  # Less Than OR Greater Than (outside)
    LEGE = "LEGE"  # Less or Equal OR Greater or Equal


class StepTypeEnum(str, Enum):
    """Step type enumeration matching C# StepTypeEnum"""
    SEQUENCE_CALL = "SequenceCall"
    ET_NLT = "ET_NLT"  # Single Numeric Limit Test
    ET_MNLT = "ET_MNLT"  # Multiple Numeric Limit Test
    ET_PFT = "ET_PFT"  # Single Pass/Fail Test
    ET_MPFT = "ET_MPFT"  # Multiple Pass/Fail Test
    ET_SVT = "ET_SVT"  # Single String Value Test
    ET_MSVT = "ET_MSVT"  # Multiple String Value Test
    MESSAGE_POPUP = "MessagePopup"
    CALL_EXE = "CallExe"
    GENERIC = "Generic"


# Base Measurement Classes
class Measurement(BaseModel):
    """Base measurement class"""
    measure_name: Optional[str] = Field(None, description="Name of the measurement")
    measure_index: int = Field(..., description="Index of measurement within step")
    measure_order: int = Field(..., description="Global measurement order")
    status: StepStatusType = Field(StepStatusType.PASSED, description="Measurement status")
    

class NumericMeasurement(Measurement):
    """Single numeric measurement with limits"""
    numeric_value: float = Field(..., description="Measured numeric value")
    low_limit: Optional[float] = Field(None, description="Lower limit")
    high_limit: Optional[float] = Field(None, description="Upper limit")
    comp_operator: CompOperatorType = Field(CompOperatorType.GELE, description="Comparison operator")
    unit: Optional[str] = Field(None, description="Unit of measurement")


class MultiNumericMeasurement(Measurement):
    """Multiple numeric measurement (named measurement)"""
    numeric_value: float = Field(..., description="Measured numeric value")
    low_limit: Optional[float] = Field(None, description="Lower limit")
    high_limit: Optional[float] = Field(None, description="Upper limit")
    comp_operator: CompOperatorType = Field(CompOperatorType.GELE, description="Comparison operator")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    measure_name: str = Field(..., description="Name of this specific measurement")


class BooleanMeasurement(Measurement):
    """Boolean (Pass/Fail) measurement"""
    boolean_value: bool = Field(..., description="Boolean measurement value")


class StringMeasurement(Measurement):
    """String value measurement"""
    string_value: str = Field(..., description="String measurement value")


# Base Step Class
class Step(BaseModel):
    """Base step class matching C# Step pattern"""
    step_id: int = Field(..., description="Unique step ID")
    step_index: int = Field(..., description="Step index within parent")
    name: str = Field(..., description="Step name")
    step_type: StepTypeEnum = Field(..., description="Type of step")
    status: StepStatusType = Field(StepStatusType.PASSED, description="Step status")
    parent_step_id: Optional[int] = Field(None, description="Parent step ID")
    total_time: float = Field(0.0, description="Total execution time")
    start_time: Optional[datetime] = Field(None, description="Step start time")


# Step Implementations
class NumericLimitStep(Step):
    """Numeric limit step containing numeric measurements"""
    step_type: StepTypeEnum = Field(StepTypeEnum.ET_NLT, description="Numeric limit step type")
    measurements: List[Union[NumericMeasurement, MultiNumericMeasurement]] = Field(
        default_factory=list, description="Numeric measurements"
    )
    is_single: bool = Field(False, description="True for single measurement, False for multiple")
    is_multiple: bool = Field(False, description="True for multiple measurements, False for single")

    @classmethod
    def create_single(cls, **kwargs):
        return cls(is_single=True, is_multiple=False, **kwargs)

    @classmethod
    def create_multiple(cls, **kwargs):
        return cls(is_single=False, is_multiple=True, **kwargs)
    
    def add_test(self, value: float, comp_operator: CompOperatorType = CompOperatorType.GELE, 
                 low_limit: Optional[float] = None, high_limit: Optional[float] = None, 
                 unit: Optional[str] = None) -> NumericMeasurement:
        """Add a single numeric test"""
        if self.is_multiple:
            raise ValueError("Cannot add single test to multiple test step")
        if len(self.measurements) > 0:
            raise ValueError("Cannot add multiple single tests to single test step")
        measurement = NumericMeasurement(
            measure_index=len(self.measurements),
            measure_order=0,  # Will be set by parent
            numeric_value=value,
            comp_operator=comp_operator,
            low_limit=low_limit,
            high_limit=high_limit,
            unit=unit,
            status=StepStatusType.PASSED  # Default, can be updated later
        )
        self.measurements.append(measurement)
        self.is_single = True
        self.is_multiple = False
        self.update_status()
        return measurement
    
    def add_multiple_test(self, measure_name: str, value: float, 
                         comp_operator: CompOperatorType = CompOperatorType.GELE,
                         low_limit: Optional[float] = None, high_limit: Optional[float] = None,
                         unit: Optional[str] = None) -> MultiNumericMeasurement:
        """Add a named numeric test to multiple test step"""
        if self.is_single:
            raise ValueError("Cannot add multiple test to single test step")
        if not self.is_multiple:
            self.is_multiple = True
            self.is_single = False
        measurement = MultiNumericMeasurement(
            measure_name=measure_name,
            measure_index=len(self.measurements),
            measure_order=0,  # Will be set by parent
            numeric_value=value,
            comp_operator=comp_operator,
            low_limit=low_limit,
            high_limit=high_limit,
            unit=unit,
            status=StepStatusType.PASSED  # Default, can be updated later
        )
        self.measurements.append(measurement)
        self.update_status()
        return measurement

    def update_status(self):
        """Update step status based on measurement results"""
        if self.is_single and self.measurements:
            self.status = self.measurements[0].status
        elif self.is_multiple and self.measurements:
            # Step is passed only if all measurements are passed
            if all(m.status == StepStatusType.PASSED for m in self.measurements):
                self.status = StepStatusType.PASSED
            elif any(m.status == StepStatusType.FAILED for m in self.measurements):
                self.status = StepStatusType.FAILED
            else:
                self.status = StepStatusType.ERROR


class PassFailStep(Step):
    """Pass/Fail step containing boolean measurements"""
    step_type: StepTypeEnum = Field(StepTypeEnum.ET_PFT, description="Pass/Fail step type")
    measurements: List[BooleanMeasurement] = Field(
        default_factory=list, description="Boolean measurements"
    )
    is_single: bool = Field(True, description="True for single measurement, False for multiple")
    is_multiple: bool = Field(False, description="True for multiple measurements, False for single")
    
    def add_test(self, value: bool) -> BooleanMeasurement:
        """Add a single boolean test"""
        if self.is_multiple:
            raise ValueError("Cannot add single test to multiple test step")
            
        if len(self.measurements) > 0:
            raise ValueError("Cannot add multiple single tests to single test step")
            
        measurement = BooleanMeasurement(
            measure_index=len(self.measurements),
            measure_order=0,  # Will be set by parent
            boolean_value=value
        )
        self.measurements.append(measurement)
        self.is_single = True
        return measurement
    
    def add_multiple_test(self, measure_name: str, value: bool) -> BooleanMeasurement:
        """Add a named boolean test to multiple test step"""
        if self.is_single:
            raise ValueError("Cannot add multiple test to single test step")
            
        if not self.is_multiple:
            self.step_type = StepTypeEnum.ET_MPFT
            self.is_multiple = True
            
        measurement = BooleanMeasurement(
            measure_name=measure_name,
            measure_index=len(self.measurements),
            measure_order=0,  # Will be set by parent
            boolean_value=value
        )
        self.measurements.append(measurement)
        return measurement


class StringValueStep(Step):
    """String value step containing string measurements"""
    step_type: StepTypeEnum = Field(StepTypeEnum.ET_SVT, description="String value step type")
    measurements: List[StringMeasurement] = Field(
        default_factory=list, description="String measurements"
    )
    is_single: bool = Field(True, description="True for single measurement, False for multiple")
    is_multiple: bool = Field(False, description="True for multiple measurements, False for single")
    
    def add_test(self, value: str) -> StringMeasurement:
        """Add a single string test"""
        if self.is_multiple:
            raise ValueError("Cannot add single test to multiple test step")
            
        if len(self.measurements) > 0:
            raise ValueError("Cannot add multiple single tests to single test step")
            
        measurement = StringMeasurement(
            measure_index=len(self.measurements),
            measure_order=0,  # Will be set by parent
            string_value=value
        )
        self.measurements.append(measurement)
        self.is_single = True
        return measurement
    
    def add_multiple_test(self, measure_name: str, value: str) -> StringMeasurement:
        """Add a named string test to multiple test step"""
        if self.is_single:
            raise ValueError("Cannot add multiple test to single test step")
            
        if not self.is_multiple:
            self.step_type = StepTypeEnum.ET_MSVT
            self.is_multiple = True
            
        measurement = StringMeasurement(
            measure_name=measure_name,
            measure_index=len(self.measurements),
            measure_order=0,  # Will be set by parent
            string_value=value
        )
        self.measurements.append(measurement)
        return measurement


class SequenceCall(Step):
    """Sequence call step that can contain other steps"""
    step_type: StepTypeEnum = Field(StepTypeEnum.SEQUENCE_CALL, description="Sequence call step type")
    sequence_name: str = Field(..., description="Name of the sequence")
    sequence_version: Optional[str] = Field(None, description="Version of the sequence")
    filename: Optional[str] = Field(None, description="Sequence filename")
    filepath: Optional[str] = Field(None, description="Sequence filepath")
    steps: List[Union['SequenceCall', NumericLimitStep, PassFailStep, StringValueStep]] = Field(
        default_factory=list, description="Child steps"
    )
    
    # Internal counters
    current_step_index: int = Field(0, description="Current step index counter")
    current_step_order: int = Field(0, description="Current step order counter") 
    current_measure_order: int = Field(0, description="Current measure order counter")
    
    def _get_next_step_index(self) -> int:
        """Get next step index"""
        index = self.current_step_index
        self.current_step_index += 1
        return index
    
    def _get_next_step_order(self) -> int:
        """Get next step order"""
        order = self.current_step_order
        self.current_step_order += 1
        return order
        
    def _get_next_measure_order(self) -> int:
        """Get next measure order"""
        order = self.current_measure_order
        self.current_measure_order += 1
        return order
    
    def add_sequence_call(self, step_name: str, sequence_name: Optional[str] = None, 
                         sequence_version: Optional[str] = None) -> 'SequenceCall':
        """Add a nested sequence call"""
        sequence_call = SequenceCall(
            step_id=self._get_next_step_order(),
            step_index=self._get_next_step_index(),
            name=step_name,
            step_type=StepTypeEnum.SEQUENCE_CALL,
            status=StepStatusType.PASSED,
            parent_step_id=self.step_id,
            total_time=0.0,
            start_time=None,
            sequence_name=sequence_name or self.sequence_name,
            sequence_version=sequence_version or self.sequence_version,
            filename=None,
            filepath=None,
            current_step_index=0,
            current_step_order=0,
            current_measure_order=0
        )
        self.steps.append(sequence_call)
        return sequence_call
    
    def add_numeric_limit_step(self, step_name: str) -> NumericLimitStep:
        """Add a numeric limit step"""
        step = NumericLimitStep(
            step_id=self._get_next_step_order(),
            step_index=self._get_next_step_index(),
            name=step_name,
            step_type=StepTypeEnum.ET_NLT,
            status=StepStatusType.PASSED,
            parent_step_id=self.step_id,
            total_time=0.0,
            start_time=None,
            is_single=True,
            is_multiple=False
        )
        self.steps.append(step)
        return step
    
    def add_pass_fail_step(self, step_name: str) -> PassFailStep:
        """Add a pass/fail step"""
        step = PassFailStep(
            step_id=self._get_next_step_order(),
            step_index=self._get_next_step_index(),
            name=step_name,
            step_type=StepTypeEnum.ET_PFT,
            status=StepStatusType.PASSED,
            parent_step_id=self.step_id,
            total_time=0.0,
            start_time=None,
            is_single=True,
            is_multiple=False
        )
        self.steps.append(step)
        return step
    
    def add_string_value_step(self, step_name: str) -> StringValueStep:
        """Add a string value step"""
        step = StringValueStep(
            step_id=self._get_next_step_order(),
            step_index=self._get_next_step_index(),
            name=step_name,
            step_type=StepTypeEnum.ET_SVT,
            status=StepStatusType.PASSED,
            parent_step_id=self.step_id,
            total_time=0.0,
            start_time=None,
            is_single=True,
            is_multiple=False
        )
        self.steps.append(step)
        return step


# Update forward references
SequenceCall.model_rebuild()


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


class LegacySequenceCall(BaseModel):
    """Legacy minimal sequence call for backward compatibility."""
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
    Complete Unit Under Test (UUT) Report with full step hierarchy.
    Based on C# Interface.TDM pattern.
    """
    # Root sequence call with complete step hierarchy
    root_sequence_call: Optional[SequenceCall] = Field(None, description="Root sequence call with full step hierarchy")
    
    # Legacy root field for backward compatibility
    root: Optional[LegacySequenceCall] = Field(default_factory=LegacySequenceCall, description="Legacy root sequence call")
    
    # UUT-specific info field with uut alias (overrides base info field)
    uut_info: Optional[UUTInfo] = Field(default=None, alias="uut", description="UUT-specific information")
    
    # Internal counters
    next_step_order: int = Field(1, description="Next available step order")
    next_measure_order: int = Field(1, description="Next available measure order")

    def __init__(self, **data):
        # Ensure type is always 'T' for UUT reports
        data['type'] = 'T'
        super().__init__(**data)
    
    def get_next_step_order(self) -> int:
        """Get next step order number"""
        order = self.next_step_order
        self.next_step_order += 1
        return order
        
    def get_next_measure_order(self) -> int:
        """Get next measure order number"""
        order = self.next_measure_order
        self.next_measure_order += 1
        return order
    
    def create_root_sequence_call(self, sequence_name: str, sequence_version: Optional[str] = None) -> SequenceCall:
        """Create the root sequence call with complete step hierarchy"""
        self.root_sequence_call = SequenceCall(
            step_id=self.get_next_step_order(),
            step_index=0,
            name="Root",
            step_type=StepTypeEnum.SEQUENCE_CALL,
            status=StepStatusType.PASSED,
            parent_step_id=None,
            total_time=0.0,
            start_time=None,
            sequence_name=sequence_name,
            sequence_version=sequence_version,
            filename=None,
            filepath=None,
            current_step_index=0,
            current_step_order=0,
            current_measure_order=0
        )
        return self.root_sequence_call
        
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