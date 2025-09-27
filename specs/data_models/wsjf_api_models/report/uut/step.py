from __future__ import annotations  # Enable forward references
from report.common_types import *
from abc import ABC
from enum import Enum
from typing import Optional, Union, Literal
from pydantic import BaseModel, Field, model_validator
from abc import ABC, abstractmethod

from ..chart import Chart, ChartType
from ..additional_data import AdditionalData
from ..attachment import Attachment
# -----------------------------------------------------------------------
# LoopInfo for looping steps
class LoopInfo(BaseModel):
    idx: Optional[int] = Field(default=None)
    num: Optional[int] = Field(default=None)
    ending_index: Optional[int] = Field(default=None, deserialization_alias="endingIndex",serialization_alias="endingIndex")
    passed: Optional[int] = Field(default=None)
    failed: Optional[int] = Field(default=None)

class StepStatus(Enum):
    Passed = 'P'
    Failed = 'F'
    Skipped = 'S'
    Terminated = 'T'
    Done = 'D'
    
# -----------------------------------------------------------------------
# Step: Abstract base step for all steps
class Step(BaseModel, ABC):  
    # Parent Step - For internal use only - does not seriallize
    parent: Optional['Step'] = Field(default=None, exclude=True)

    # Required
    step_type: Literal["NONE"] = Field(default="NONE",deserialization_alias="stepType", serialization_alias="stepType")
    #step_type: str = Field(default="NO_VALID_STEP",deserialization_alias="stepType")
    
    name: str = Field(..., max_length=100, min_length=1)
    group: str = Field(default="M", max_length=1, min_length=1, pattern='^[SMC]$')
    #status: str = Field(default="P", max_length=1, min_length=1, pattern='^[PFSDET]$')
    status: StepStatus = Field(default=StepStatus.Passed)

    id: Optional[Union[int, str]] = Field(default=None)

    # Error code and report text
    error_code: Optional[Union[int, str]] = Field(default=None, deserialization_alias="errorCode",serialization_alias="errorCode")
    error_code_format: Optional[str] = Field(default=None, deserialization_alias="errorCodeFormat", serialization_alias="errorCodeFormat")
    error_message: Optional[str] = Field(default=None, deserialization_alias="errorMessage",serialization_alias="errorMessage")
    report_text: Optional[str] = Field(default=None, deserialization_alias="reportText",serialization_alias="reportText")
    
    start: Optional[str] = Field(default=None, deserialization_alias="start",serialization_alias="start")
    tot_time: Optional[Union[float, str]] = Field(default=None, deserialization_alias="totTime",serialization_alias="totTime")
    tot_time_format: Optional[str] = Field(default=None, deserialization_alias="totTimeFormat",serialization_alias="totTimeFormat")
    ts_guid: Optional[str] = Field(default=None, deserialization_alias="tsGuid",serialization_alias="tsGuid")
    
    # Step Caused Failure (ReadOnly)
    caused_seq_failure: Optional[bool] = Field(default=None, deserialization_alias="causedSeqFailure", serialization_alias="causedSeqFailure")
    caused_uut_failure: Optional[bool] = Field(default=None, deserialization_alias="causedUUTFailure", serialization_alias="causedUUTFailure")
    
    # LoopInfo
    loop: Optional[LoopInfo] = Field(default=None)
   
    # Additional Results, Charts and Attachments
    additional_results: Optional[list[AdditionalData]] = Field(default=None, deserialization_alias="additionalResults", serialization_alias="additionalResults")
    
    chart: Optional[Chart] = Field(default=None)
    attachment: Optional[Attachment] = Field(default=None)  
    
    @model_validator(mode="before")
    @classmethod
    def replace_none_during_deserialization(cls, data, info):
        # Check if deserialization context is set
        if info.context is not None:
            if info.context.get("is_deserialization", False):
                for key in ["name"]:
                    if data.get(key) in (None, ""):
                        data[key] = def_MissingString
        return data
    
    # validate - all step types
    @abstractmethod
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        # Implement generic step validation here

        # Validate Step
            # Validate LoopInfo
            # Validate Additional Results
            # Validate Chart
            # Validate Attachment

        return True
        # validate_step template:
        # @abstractmethod
        # def validate_step(self, trigger_children=False, errors=None) -> bool:
        #     if errors is None:
        #         errors = []
        #     if not super().validate_step(trigger_children=trigger_children, errors=errors):
        #         return False
        #     # Current Class Validation:
        #       # For every validation failure        
        #           errors.append(f"{self.get_step_path()} ErrorMessage.")
        #     return True

    # return the steps path
    def get_step_path(self) -> str:
        path = []
        current_step = self
        while current_step is not None:
            path.append(current_step.name)
            current_step = current_step.parent
        return '/'.join(reversed(path))

    # Add chart to any step
    def add_chart(self, chart_type:ChartType, chart_label: str, x_label:str, x_unit:str, y_label: str, y_unit: str) -> Chart:
        self.chart = Chart(chart_type=chart_type, label=chart_label, xLabel=x_label, yLabel=y_label, xUnit=x_unit, yUnit=y_unit)
        return self.chart
    
    model_config = {
        "populate_by_name": True,  # Keeps existing behavior
        "arbitrary_types_allowed": True,  # Fixes StepList issue
    }
        

StepType = Union['NumericStep','MultiNumericStep','SequenceCall','BooleanStep','MultiBooleanStep', 'MultiStringStep', 'StringStep', 'ChartStep', 'CallExeStep','MessagePopUpStep','GenericStep', 'ActionStep']
from .steps import NumericStep,MultiNumericStep,SequenceCall,BooleanStep,MultiBooleanStep,MultiStringStep,StringStep,ChartStep,CallExeStep,MessagePopUpStep,GenericStep,ActionStep  # noqa: E402

Step.model_rebuild()
