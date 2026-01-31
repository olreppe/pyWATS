"""
UUTReport.py
-
-
"""
from ..common_types import *
from ..report import Report
from .uut_info import UUTInfo
from .steps.sequence_call import SequenceCall, SequenceCallInfo
    
def_MissingString = "Missing"
def_MissingNumeric = "NaN"

class UUTReport(Report):
    """
    Class: UUTReport

    """
    # Overloads
    type: Literal["T"] = "T" #Field(default="T", max_length=1, min_length=1, pattern='^[T]$')

    # UUT Specific
    root: SequenceCall = Field(default_factory=SequenceCall)        # Root Sequence Call
    info: Optional[UUTInfo] = Field(default=None, validation_alias="uut", serialization_alias="uut")     # Info (serializes as alias:uut)

    # Aliases for process_code/process_name to be called test_operation_*
    @property
    def test_operation_code(self) -> int:
        """Alias for process_code (test operation code)."""
        return self.process_code
    
    @test_operation_code.setter
    def test_operation_code(self, value: int) -> None:
        self.process_code = value

    # -------------------------------------------------------------------
    # Get root sequence call    
    def get_root_sequence_call(self) -> SequenceCall:
        self.root.name = "MainSequence Callback"
        return self.root
