from .common_types import *

# -----------------------------------------------------------
# Class: ReportInfo
class ReportInfo(BaseModel):
    """
    Generic info class for both UUT&UUR
    """
    operator: str = Field(default="Operator", max_length=100, min_length=1, deserialization_alias="user", serialization_alias="user",
                            description="The name id ID of the operator")
    comment: Optional[str] = Field(default=None, max_length=5000, min_length=0,
                                   description="")
    exec_time: Optional[float] = Field(default=None, alias = "execTime",
                                       description="The execution time of the test in seconds.")
    exec_time_format: Optional[str] = Field(default=None, deserialization_alias="execTimeFormat", serialization_alias="execTimeFormat",
                                            description="")
    
    @model_validator(mode="before")
    @classmethod
    def replace_none_during_deserialization(cls, data, info):
        # Check if deserialization context is set
        if info.context.get("is_deserialization", False):
            for key in ["user"]:
                if data.get(key) in (None, ""):
                    data[key] = "Operator"
        return data