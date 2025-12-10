# NI_Step

# Type/lib
from typing import Literal, Optional
from pydantic import Field
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

# Class: GenericStep
# A step type that displays flow icon and acts as a catch-all for flow control steps
# Accepts ANY string value to support all FlowType enum values (50+ types) and other
# generic step types without listing them individually in the discriminator
class GenericStep(Step):
    # Type is str (not Literal) to act as fallback in discriminated union
    # Accepts all FlowType enum values and any other string step_type
    # This class will be selected when step_type doesn't match any specific Literal
    step_type: str = Field(..., validation_alias="stepType", serialization_alias="stepType")

    def validate_step(self, trigger_children=False, errors=None) -> bool:
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        return True
