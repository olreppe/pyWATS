"""
Production Models

Models for production management endpoints.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from enum import IntEnum

from .product import Product, ProductRevision, Setting


class SerialNumberIdentifier(IntEnum):
    """Serial number identifier enumeration."""
    NONE = 0
    ALPHANUMERIC = 1
    NUMERIC = 2


class SerialNumberType(BaseModel):
    """Serial number type model."""
    
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )
    
    name: Optional[str] = None
    description: Optional[str] = None
    format: Optional[str] = None
    reg_ex: Optional[str] = Field(None, alias="regEx")
    identifier: Optional[SerialNumberIdentifier] = None
    identifier_name: Optional[str] = Field(None, alias="identifierName")


class Unit(BaseModel):
    """Production unit model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    serial_number: Optional[str] = Field(None, alias="serialNumber")
    part_number: Optional[str] = Field(None, alias="partNumber")
    revision: Optional[str] = None
    parent_serial_number: Optional[str] = Field(None, alias="parentSerialNumber")
    batch_number: Optional[str] = Field(None, alias="batchNumber")
    serial_date: Optional[datetime] = Field(None, alias="serialDate")
    current_location: Optional[str] = Field(None, alias="currentLocation")
    xml_data: Optional[str] = Field(None, alias="xmlData")
    unit_phase_id: Optional[int] = Field(None, alias="unitPhaseId")
    unit_phase: Optional[str] = Field(None, alias="unitPhase")
    process_code: Optional[str] = Field(None, alias="processCode")
    tags: Optional[List[Setting]] = []
    product_revision: Optional[ProductRevision] = Field(None, alias="productRevision")
    product: Optional[Product] = None
    sub_units: Optional[List['Unit']] = Field([], alias="subUnits")


class UnitChange(BaseModel):
    """Unit change model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[int] = None
    unit_serial_number: Optional[str] = Field(None, alias="unitSerialNumber")
    new_parent_serial_number: Optional[str] = Field(None, alias="newParentSerialNumber")
    new_part_number: Optional[str] = Field(None, alias="newPartNumber")
    new_revision: Optional[str] = Field(None, alias="newRevision")
    new_unit_phase_id: Optional[int] = Field(None, alias="newUnitPhaseId")


class ProductionBatch(BaseModel):
    """Production batch model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    batch_number: Optional[str] = Field(None, alias="batchNumber")
    batch_size: Optional[int] = Field(None, alias="batchSize")


class UnitVerification(BaseModel):
    """Unit verification details model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    process_code: Optional[int] = Field(None, alias="processCode")
    process_name: Optional[str] = Field(None, alias="processName")
    process_index: Optional[int] = Field(None, alias="processIndex")
    status: Optional[str] = None
    start_utc: Optional[datetime] = Field(None, alias="startUtc")
    station_name: Optional[str] = Field(None, alias="stationName")
    total_count: Optional[int] = Field(None, alias="totalCount")
    non_passed_count: Optional[int] = Field(None, alias="nonPassedCount")
    repair_count: Optional[int] = Field(None, alias="repairCount")


class UnitVerificationGrade(BaseModel):
    """Unit verification grade model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    status: Optional[str] = None
    grade: Optional[str] = None
    all_processes_executed_in_correct_order: Optional[bool] = Field(
        None, alias="allProcessesExecutedInCorrectOrder"
    )
    all_processes_passed_first_run: Optional[bool] = Field(
        None, alias="allProcessesPassedFirstRun"
    )
    all_processes_passed_any_run: Optional[bool] = Field(
        None, alias="allProcessesPassedAnyRun"
    )
    all_processes_passed_last_run: Optional[bool] = Field(
        None, alias="allProcessesPassedLastRun"
    )
    no_repairs: Optional[bool] = Field(None, alias="noRepairs")
    results: Optional[List[UnitVerification]] = []


# Forward reference update
Unit.model_rebuild()