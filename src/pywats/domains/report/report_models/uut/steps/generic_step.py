"""
GenericStep - v3 Implementation

Generic/custom step for arbitrary data.
"""
from __future__ import annotations

from typing import (
    Optional,
    List,
    Literal,
)
from enum import Enum

from ..step import Step
from ...common_types import (
    Field,
    StepStatus,
)


class FlowType(Enum):
    """Flow control step types from TestStand."""
    FTPFiles = "NI_FTPFiles"
    If = "NI_Flow_If"
    ElseIf = "NI_Flow_ElseIf"
    Else = "NI_Flow_Else"
    End = "NI_Flow_End"
    For = "NI_Flow_For"
    ForEach = "NI_Flow_ForEach"
    Break = "NI_Flow_Break"
    Continue = "NI_Flow_Continue"
    DoWhile = "NI_Flow_DoWhile"
    While = "NI_Flow_While"
    Select = "NI_Flow_Select"
    Case = "NI_Flow_Case"
    NI_Flow_StreamLoop = "NI_Flow_StreamLoop"
    NI_Flow_SweepLoop = "NI_Flow_SweepLoop"
    Lock = "NI_Lock"
    Rendezvous = "NI_Rendezvous"
    Queue = "NI_Queue"
    Notification = "NI_Notification"
    Wait = "NI_Wait"
    Batch_Sync = "NI_Batch_Sync"
    AutoSchedule = "NI_AutoSchedule"
    UseResource = "NI_UseResource"
    ThreadPriority = "NI_ThreadPriority"
    Semaphore = "NI_Semaphore"
    BatchSpec = "NI_BatchSpec"
    BatchSync = "NI_BatchSync"
    OpenDatabase = "NI_OpenDatabase"
    OpenSQLStatement = "NI_OpenSQLStatement"
    CloseSQLStatement = "NI_CloseSQLStatement"
    CloseDatabase = "NI_CloseDatabase"
    DataOperation = "NI_DataOperation"
    NI_CPUAffinity = "NI_CPUAffinity"
    NI_IviDmm = "NI_IviDmm"
    NI_IviScope = "NI_IviScope"
    NI_IviFgen = "NI_IviFgen"
    NI_IviDCPower = "NI_IviDCPower"
    NI_IviSwitch = "NI_IviSwitch"
    NI_IviTools = "NI_IviTools"
    NI_LV_DeployLibrary = "NI_LV_DeployLibrary"
    LV_CheckSystemStatus = "NI_LV_CheckSystemStatus"
    LV_RunVIAsynchronously = "NI_LV_RunVIAsynchronously"
    NI_PropertyLoader = "NI_PropertyLoader"
    NI_VariableAndPropertyLoader = "NI_VariableAndPropertyLoader"
    NI_NewCsvFileInputRecordStream = "NI_NewCsvFileInputRecordStream"
    NI_NewCsvFileOutputRecordStream = "NI_NewCsvFileOutputRecordStream"
    NI_WriteRecord = "NI_WriteRecord"
    Goto = "Goto"
    Action = "Action"
    Statement = "Statement"
    Label = "Label"
    GenericTest = "GT"


# Define all possible GenericStep step_type values as a Literal
GenericStepLiteral = Literal[
    "NI_FTPFiles", "NI_Flow_If", "NI_Flow_ElseIf", "NI_Flow_Else", "NI_Flow_End",
    "NI_Flow_For", "NI_Flow_ForEach", "NI_Flow_Break", "NI_Flow_Continue",
    "NI_Flow_DoWhile", "NI_Flow_While", "NI_Flow_Select", "NI_Flow_Case",
    "NI_Flow_StreamLoop", "NI_Flow_SweepLoop", "NI_Lock", "NI_Rendezvous",
    "NI_Queue", "NI_Notification", "NI_Wait", "NI_Batch_Sync", "NI_AutoSchedule",
    "NI_UseResource", "NI_ThreadPriority", "NI_Semaphore", "NI_BatchSpec",
    "NI_BatchSync", "NI_OpenDatabase", "NI_OpenSQLStatement",
    "NI_CloseSQLStatement", "NI_CloseDatabase", "NI_DataOperation",
    "NI_CPUAffinity", "NI_IviDmm", "NI_IviScope", "NI_IviFgen", "NI_IviDCPower",
    "NI_IviSwitch", "NI_IviTools", "NI_LV_DeployLibrary", "NI_LV_CheckSystemStatus",
    "NI_LV_RunVIAsynchronously", "NI_PropertyLoader", "NI_VariableAndPropertyLoader",
    "NI_NewCsvFileInputRecordStream", "NI_NewCsvFileOutputRecordStream",
    "NI_WriteRecord", "Goto", "Action", "Statement", "Label", "GT", "GenericTest", "NONE"
]


class GenericStep(Step):
    """
    Generic test step for custom/arbitrary data.
    
    Use when none of the specific step types fit your needs.
    Can contain any combination of report_text and additional_results.
    
    C# Name: GenericStep
    
    Example:
        step = GenericStep(
            name="Custom Data",
            report_text="Test completed with custom results"
        )
    """
    
    # Step type discriminator - uses Literal to limit to known flow types
    # Unknown types will fall through to UnknownStep
    step_type: GenericStepLiteral = Field(
        default="GT",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def validate_step(
        self,
        trigger_children: bool = False,
        errors: Optional[List[str]] = None
    ) -> bool:
        """Validate the generic step (always passes)."""
        return True
