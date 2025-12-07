"""
Production models for pyWATS

Uses Pydantic 2 for validation and serialization.
"""
from typing import Optional, List
from datetime import datetime
from enum import IntEnum
from pydantic import Field

from .common import PyWATSModel, Setting
from .product import Product, ProductRevision


class SerialNumberIdentifier(IntEnum):
    """Serial number identifier type"""
    SERIAL_NUMBER = 0
    MAC_ADDRESS = 1
    IMEI = 2


class SerialNumberType(PyWATSModel):
    """
    Represents a serial number type configuration.
    
    Attributes:
        name: Type name
        description: Type description
        format: Serial number format pattern
        reg_ex: Validation regex
        identifier: Identifier type (0=SerialNumber, 1=MAC, 2=IMEI)
        identifier_name: Human readable identifier name
    """
    name: Optional[str] = Field(default=None, alias="name")
    description: Optional[str] = Field(default=None, alias="description")
    format: Optional[str] = Field(default=None, alias="format")
    reg_ex: Optional[str] = Field(default=None, alias="regEx")
    identifier: SerialNumberIdentifier = Field(default=SerialNumberIdentifier.SERIAL_NUMBER, alias="identifier")
    identifier_name: Optional[str] = Field(default=None, alias="identifierName")


class ProductionBatch(PyWATSModel):
    """
    Represents a production batch.
    
    Attributes:
        batch_number: Batch number/identifier
        batch_size: Number of units in batch
    """
    batch_number: Optional[str] = Field(default=None, alias="batchNumber")
    batch_size: Optional[int] = Field(default=None, alias="batchSize")


class UnitChange(PyWATSModel):
    """
    Represents a unit change record.
    
    Attributes:
        id: Change record ID
        unit_serial_number: Serial number of the unit
        new_parent_serial_number: New parent serial number
        new_part_number: New part number
        new_revision: New revision
        new_unit_phase_id: New unit phase ID
    """
    id: Optional[int] = Field(default=None, alias="id")
    unit_serial_number: Optional[str] = Field(default=None, alias="unitSerialNumber")
    new_parent_serial_number: Optional[str] = Field(default=None, alias="newParentSerialNumber")
    new_part_number: Optional[str] = Field(default=None, alias="newPartNumber")
    new_revision: Optional[str] = Field(default=None, alias="newRevision")
    new_unit_phase_id: Optional[int] = Field(default=None, alias="newUnitPhaseId")


class Unit(PyWATSModel):
    """
    Represents a production unit in WATS.
    
    Attributes:
        serial_number: Unit serial number
        part_number: Product part number
        revision: Product revision
        parent_serial_number: Parent unit serial number
        batch_number: Production batch number
        serial_date: Serial number assignment date
        current_location: Current location
        xml_data: XML document with custom data
        unit_phase_id: Current unit phase ID
        unit_phase: Current unit phase name (read-only)
        process_code: Current process code
        tags: Custom key-value tags (read-only)
        product_revision: Associated product revision
        product: Associated product
        sub_units: Child units
    """
    serial_number: Optional[str] = Field(default=None, alias="serialNumber")
    part_number: Optional[str] = Field(default=None, alias="partNumber")
    revision: Optional[str] = Field(default=None, alias="revision")
    parent_serial_number: Optional[str] = Field(default=None, alias="parentSerialNumber")
    batch_number: Optional[str] = Field(default=None, alias="batchNumber")
    serial_date: Optional[datetime] = Field(default=None, alias="serialDate")
    current_location: Optional[str] = Field(default=None, alias="currentLocation")
    xml_data: Optional[str] = Field(default=None, alias="xmlData")
    unit_phase_id: Optional[int] = Field(default=None, alias="unitPhaseId")
    unit_phase: Optional[str] = Field(default=None, alias="unitPhase")
    process_code: Optional[str] = Field(default=None, alias="processCode")
    tags: List[Setting] = Field(default_factory=list, alias="tags")
    product_revision: Optional[ProductRevision] = Field(default=None, alias="productRevision")
    product: Optional[Product] = Field(default=None, alias="product")
    sub_units: List["Unit"] = Field(default_factory=list, alias="subUnits")


class UnitVerification(PyWATSModel):
    """
    Represents unit verification result for a single process.
    
    Attributes:
        process_code: Test operation code
        process_name: Test operation name
        process_index: Test operation order index
        status: Unit test status in this process
        start_utc: Test start date and time
        station_name: Name of test station
        total_count: How many times the unit was tested
        non_passed_count: How many times the unit didn't pass
        repair_count: How many times the unit was repaired
    """
    process_code: Optional[int] = Field(default=None, alias="processCode")
    process_name: Optional[str] = Field(default=None, alias="processName")
    process_index: Optional[int] = Field(default=None, alias="processIndex")
    status: Optional[str] = Field(default=None, alias="status")
    start_utc: Optional[datetime] = Field(default=None, alias="startUtc")
    station_name: Optional[str] = Field(default=None, alias="stationName")
    total_count: Optional[int] = Field(default=None, alias="totalCount")
    non_passed_count: Optional[int] = Field(default=None, alias="nonPassedCount")
    repair_count: Optional[int] = Field(default=None, alias="repairCount")


class UnitVerificationGrade(PyWATSModel):
    """
    Represents complete unit verification grade result.
    
    Attributes:
        status: Unit status
        grade: Unit grade
        all_processes_executed_in_correct_order: Unit tested in correct process order
        all_processes_passed_first_run: Unit passed each process first time
        all_processes_passed_any_run: Unit passed at some point in each process
        all_processes_passed_last_run: Unit eventually passed each process
        no_repairs: Unit never needed repair
        results: Unit results per process
    """
    status: Optional[str] = Field(default=None, alias="status")
    grade: Optional[str] = Field(default=None, alias="grade")
    all_processes_executed_in_correct_order: bool = Field(default=False, alias="allProcessesExecutedInCorrectOrder")
    all_processes_passed_first_run: bool = Field(default=False, alias="allProcessesPassedFirstRun")
    all_processes_passed_any_run: bool = Field(default=False, alias="allProcessesPassedAnyRun")
    all_processes_passed_last_run: bool = Field(default=False, alias="allProcessesPassedLastRun")
    no_repairs: bool = Field(default=False, alias="noRepairs")
    results: List[UnitVerification] = Field(default_factory=list, alias="results")
