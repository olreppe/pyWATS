"""
MES Models

Data models for MES operations, mirroring the C# Interface.MES data structures
while using Python conventions and Pydantic for data validation.
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import IntEnum, Enum
from uuid import UUID


class UnitPhase(IntEnum):
    """Unit phase enumeration matching C# Unit_Phase."""
    UNKNOWN = 0
    CREATED = 1
    IN_PROCESS = 2
    PASSED = 3
    FAILED = 4
    TERMINATED = 5
    SCRAPPED = 6
    REPAIRED = 7


class StatusEnum(IntEnum):
    """Status enumeration for packages and workflows."""
    DEVELOPMENT = 0
    RELEASED = 1
    OBSOLETE = 2


class ActivityTestResult(IntEnum):
    """Test result enumeration for workflow activities."""
    NONE = 0
    PASSED = 1
    FAILED = 2
    ERROR = 3
    TERMINATED = 4


class ActivityMethod(IntEnum):
    """Activity method enumeration for workflow validation."""
    NONE = 0
    VALIDATE = 1
    INITIALIZE = 2
    CHECKIN = 3
    CHECKOUT = 4


class UnitInfo(BaseModel):
    """Unit information model."""
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    part_number: Optional[str] = Field(None, alias="partNumber")
    revision: Optional[str] = None
    batch_number: Optional[str] = Field(None, alias="batchNumber")
    phase: Optional[UnitPhase] = None
    process: Optional[str] = None
    created_date: Optional[datetime] = Field(None, alias="createdDate")
    updated_date: Optional[datetime] = Field(None, alias="updatedDate")
    tags: Optional[Dict[str, str]] = {}
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class UnitHistory(BaseModel):
    """Unit history entry model."""
    id: Optional[int] = None
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    part_number: Optional[str] = Field(None, alias="partNumber")
    operation: Optional[str] = None
    station_name: Optional[str] = Field(None, alias="stationName")
    operator: Optional[str] = None
    start_time: Optional[datetime] = Field(None, alias="startTime")
    end_time: Optional[datetime] = Field(None, alias="endTime")
    result: Optional[str] = None
    comments: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class UnitVerificationResponse(BaseModel):
    """Unit verification response model."""
    is_valid: bool = Field(..., alias="isValid")
    verification_code: Optional[str] = Field(None, alias="verificationCode")
    message: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class ProductInfo(BaseModel):
    """Product information model."""
    part_number: str = Field(..., alias="partNumber")
    revision: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    product_group: Optional[str] = Field(None, alias="productGroup")
    created_date: Optional[datetime] = Field(None, alias="createdDate")
    updated_date: Optional[datetime] = Field(None, alias="updatedDate")
    
    class Config:
        allow_population_by_field_name = True


class Product(BaseModel):
    """Product model for search results."""
    part_number: str = Field(..., alias="partNumber")
    revision: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    include_revision: bool = Field(False, alias="includeRevision")
    include_serial_number: bool = Field(False, alias="includeSerialNumber")
    
    class Config:
        allow_population_by_field_name = True


class AssetResponse(BaseModel):
    """Asset operation response model.""" 
    model_config = ConfigDict(populate_by_name=True)
    
    success: bool = True
    message: Optional[str] = None
    asset_id: Optional[str] = Field(None, alias="assetId")
    error_code: Optional[str] = Field(None, alias="errorCode")


class Package(BaseModel):
    """Software package model."""
    id: Optional[int] = None
    name: str
    version: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = Field(None, alias="filePath")
    file_size: Optional[int] = Field(None, alias="fileSize")
    checksum: Optional[str] = None
    status: Optional[StatusEnum] = None
    created_date: Optional[datetime] = Field(None, alias="createdDate")
    updated_date: Optional[datetime] = Field(None, alias="updatedDate")
    tags: Optional[Dict[str, str]] = {}
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class WorkflowContext(BaseModel):
    """Workflow context model."""
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    part_number: Optional[str] = Field(None, alias="partNumber")
    operation: Optional[str] = None
    station_name: Optional[str] = Field(None, alias="stationName")
    operator: Optional[str] = None
    context_data: Optional[Dict[str, Any]] = Field({}, alias="contextData")
    
    class Config:
        allow_population_by_field_name = True


class WorkflowResult(BaseModel):
    """Workflow operation result model."""
    success: bool = True
    message: Optional[str] = None
    result: Optional[ActivityTestResult] = None
    workflow_id: Optional[str] = Field(None, alias="workflowId")
    context: Optional[WorkflowContext] = None
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class MESResponse(BaseModel):
    """Generic MES operation response model."""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = Field(None, alias="errorCode")
    
    class Config:
        allow_population_by_field_name = True


class IdentifyUnitRequest(BaseModel):
    """Request model for unit identification dialog."""
    part_number: Optional[str] = Field(None, alias="partNumber")
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    include_test_operation: bool = Field(False, alias="includeTestOperation")
    select_test_operation: bool = Field(True, alias="selectTestOperation")
    custom_text: Optional[str] = Field(None, alias="customText")
    always_on_top: bool = Field(True, alias="alwaysOnTop")
    use_workflow: bool = Field(False, alias="useWorkflow")
    workflow_status: Optional[StatusEnum] = Field(None, alias="workflowStatus")
    context: Optional[Dict[str, Any]] = {}
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


class IdentifyProductRequest(BaseModel):
    """Request model for product identification dialog."""
    filter: Optional[str] = None
    top_count: int = Field(10, alias="topCount")
    free_partnumber: bool = Field(False, alias="freePartnumber")
    include_revision: bool = Field(True, alias="includeRevision")
    include_serial_number: bool = Field(False, alias="includeSerialNumber")
    custom_text: Optional[str] = Field(None, alias="customText")
    always_on_top: bool = Field(True, alias="alwaysOnTop")
    
    class Config:
        allow_population_by_field_name = True