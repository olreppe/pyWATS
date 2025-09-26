# NI_Step

# Type/lib
from typing import Literal, Optional
from pydantic import BaseModel, Field
from enum import Enum

# Imports
from ..step import Step
# Example json object and schema:

class FlowType(Enum):
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
    OpenDatabase = "NI_OpenDatabase"
    OpenSQLStatement = "NI_OpenSQLStatement"
    CloseSQLStatement = "NI_CloseSQLStatement"
    CloseDatabase = "NI_CloseDatabase"
    DataOperation = "NI_DataOperation"
    IVIDmm = "NI_IVIDmm"
    IVIScope = "NI_IVIScope"
    IVIFgen = "NI_IVIFgen"
    IVIPowerSupply = "NI_IVIPowerSupply"
    Switch = "NI_Switch"
    IVITools = "NI_IVITools"
    LV_CheckSystemStatus = "NI_LV_CheckSystemStatus"
    LV_RunVIAsynchronously = "NI_LV_RunVIAsynchronously"
    GoTo = "GoTo"
    Action = "Action"

# Class: GenericStep
# A step type that displays flow icon.
class GenericStep(Step):
    step_type: FlowType = Field(..., deserialization_alias="stepType",serialization_alias="stepType")

    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        return True

    model_config = {
        "json_encoders": {FlowType: lambda c: c.value}  
    }
    # stepType: Literal["NI_FTPFiles",
    # "NI_Flow_If",
    # "NI_Flow_ElseIf",
    # "NI_Flow_Else",
    # "NI_Flow_End",
    # "NI_Flow_For",
    # "NI_Flow_ForEach",
    # "NI_Flow_Break",
    # "NI_Flow_Continue",
    # "NI_Flow_DoWhile",
    # "NI_Flow_While",
    # "NI_Flow_Select",
    # "NI_Flow_Case",
    # "NI_Lock",
    # "NI_Rendezvous",
    # "NI_Queue",
    # "NI_Notification",
    # "NI_Wait",
    # "NI_Batch_Sync",
    # "NI_AutoSchedule",
    # "NI_UseResource",
    # "NI_ThreadPriority",
    # "NI_Semaphore",
    # "NI_BatchSpec",
    # "NI_OpenDatabase",
    # "NI_OpenSQLStatement",
    # "NI_CloseSQLStatement",
    # "NI_CloseDatabase",
    # "NI_DataOperation",
    # "NI_IVIDmm",
    # "NI_IVIScope",
    # "NI_IVIFgen",
    # "NI_IVIPowerSupply",
    # "NI_Switch",
    # "NI_IVITools",
    # "NI_LV_CheckSystemStatus",
    # "NI_LV_RunVIAsynchronously",
    # "GoTo",
    # "DoWhile"] = "NI_AutoSchedule"


