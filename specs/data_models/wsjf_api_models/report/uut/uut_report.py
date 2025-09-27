"""
UUTReport.py
-
-
"""
from report.common_types import *
from ..report import Report
from .uut_info import UUTInfo
from .steps.sequence_call import SequenceCall
    
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
    info: UUTInfo = Field(default=None, deserialization_alias="uut", serialization_alias="uut")     # Info (serializes as alias:uut)

    # -------------------------------------------------------------------
    # Get root sequence call    
    def get_root_sequence_call(self) -> SequenceCall:
        self.root.name = "MainSequence Callback"
        return self.root

    # -------------------------------------------------------------------
    # Model validator - before
    # Inject defaults for missing requirements when deserializing - to support reading legacy reports
    @model_validator(mode="before")
    @classmethod
    def replace_none_during_deserialization(cls, data):
        if isinstance(data, dict):
            if data.get("pn") is None or data.get("pn") == "":
                data["pn"] = def_MissingString  # Replace None only during deserialization
            if data.get("sn") is None or data.get("sn") == "":
                data["sn"] = def_MissingString  # Replace None only during deserialization
            if data.get("rev") is None or data.get("rev") == "":
                data["rev"] = def_MissingString  # Replace None only during deserialization
            if data.get("station_name") is None or data.get("station_name") == "":
                data["station_name"] = def_MissingString  # Replace None only during deserialization
            if data.get("location") is None or data.get("location") == "":
                data["location"] = def_MissingString  # Replace None only during deserialization
            if data.get("purpose") is None or data.get("purpose") == "":
                data["purpose"] = def_MissingString  # Replace None only during deserialization
        return data

    # -------------------------------------------------------------------
    # Model Config
    # Make sure json is deserialized to alias names
    model_config = {
        "populate_by_name": True  # Allows deserialization using alias}
    }


UUTReport.model_rebuild()