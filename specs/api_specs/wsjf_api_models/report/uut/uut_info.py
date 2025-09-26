# Type imports
from typing import Annotated, Any, Optional, Union
from pydantic import BaseModel, Field, SerializationInfo, model_validator
from uuid import UUID,uuid4

# Model imports
from ..constants import *
from ..report_info import ReportInfo

class RefUURs(BaseModel):
    """
    Repair reports that reference this test report.
    """

    id: UUID
    """
    Id of the referencing repair report.
    """
    start: Optional[str] = Field(default=None)
    """
    The start date and time of the repair report.
    """

class UUTInfo(ReportInfo):
    fixture_id: str = Field(..., max_length=100, min_length=0, deserialization_alias="fixtureId", serialization_alias="fixtureId")

    socket_index: int | None = Field(default=None, deserialization_alias="testSocketIndex", serialization_alias="testSocketIndex")
    socket_index_format: str | None = Field(default=None, deserialization_alias="testSocketIndexFormat", serialization_alias="testSocketIndexFormat")

    error_code: int | str | None = Field(default=None, deserialization_alias="errorCode", serialization_alias="errorCode")
    error_code_format: str | None = Field(default=None, deserialization_alias="errorCodeFormat", serialization_alias="errorCodeFormat")
    error_message: str | None = Field(default=None, deserialization_alias="errorMessage", serialization_alias="errorMessage")
    
    batch_number: Optional[str] = Field(default=None, max_length=100, min_length=0, deserialization_alias="batchSN", serialization_alias="batchSN")
    batch_fail_count: int | None = Field(default=None, deserialization_alias="batchFailCount", serialization_alias="batchFailCount")
    batch_fail_count_format: str | None = Field(default=None, deserialization_alias="batchFailCountFormat", serialization_alias="batchFailCountFormat")
    batch_loop_index: int | None = Field(default=None, deserialization_alias="batchLoopIndex", serialization_alias="batchLoopIndex")
    batch_loop_index_format: str | None = Field(default=None, deserialization_alias="batchLoopIndexFormat", serialization_alias="batchLoopIndexFormat")

    step_id_caused_uut_failure: int | None = Field(default=None, deserialization_alias="stepIdCausedUUTFailure", serialization_alias="stepIdCausedUUTFailure")
    referenced_by_uurs: list[RefUURs] | None = Field(default=None, deserialization_alias="referencedByUURs", serialization_alias="referencedByUURs")

        # -------------------------------------------------------------------
    # Model validator - before
    # Inject defaults for missing requirements when deserializing - to support reading legacy reports
    # @model_validator(mode="before")
    # @classmethod
    # def replace_none_during_deserialization(cls, data):
    #     if isinstance(data, dict):
    #         if data.get("fixtureId") is None or data.get("fixtureId") == "":
    #             data["fixtureId"] = def_MissingString  # Replace None only during deserialization
    #     return data
