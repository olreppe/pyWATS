"""
Production models for pyWATS
"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import IntEnum

from .common import Setting
from .product import Product, ProductRevision


class SerialNumberIdentifier(IntEnum):
    """Serial number identifier type"""
    SERIAL_NUMBER = 0
    MAC_ADDRESS = 1
    IMEI = 2


@dataclass
class SerialNumberType:
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
    name: Optional[str] = None
    description: Optional[str] = None
    format: Optional[str] = None
    reg_ex: Optional[str] = None
    identifier: SerialNumberIdentifier = SerialNumberIdentifier.SERIAL_NUMBER
    identifier_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "SerialNumberType":
        """Create SerialNumberType from API response dictionary"""
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            format=data.get("format"),
            reg_ex=data.get("regEx"),
            identifier=SerialNumberIdentifier(data.get("identifier", 0)),
            identifier_name=data.get("identifierName")
        )


@dataclass
class ProductionBatch:
    """
    Represents a production batch.
    
    Attributes:
        batch_number: Batch number/identifier
        batch_size: Number of units in batch
    """
    batch_number: Optional[str] = None
    batch_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ProductionBatch":
        """Create ProductionBatch from API response dictionary"""
        return cls(
            batch_number=data.get("batchNumber"),
            batch_size=data.get("batchSize")
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for API requests"""
        result = {}
        if self.batch_number:
            result["batchNumber"] = self.batch_number
        if self.batch_size is not None:
            result["batchSize"] = self.batch_size
        return result


@dataclass
class UnitChange:
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
    id: Optional[int] = None
    unit_serial_number: Optional[str] = None
    new_parent_serial_number: Optional[str] = None
    new_part_number: Optional[str] = None
    new_revision: Optional[str] = None
    new_unit_phase_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "UnitChange":
        """Create UnitChange from API response dictionary"""
        return cls(
            id=data.get("id"),
            unit_serial_number=data.get("unitSerialNumber"),
            new_parent_serial_number=data.get("newParentSerialNumber"),
            new_part_number=data.get("newPartNumber"),
            new_revision=data.get("newRevision"),
            new_unit_phase_id=data.get("newUnitPhaseId")
        )


@dataclass
class Unit:
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
    serial_number: Optional[str] = None
    part_number: Optional[str] = None
    revision: Optional[str] = None
    parent_serial_number: Optional[str] = None
    batch_number: Optional[str] = None
    serial_date: Optional[datetime] = None
    current_location: Optional[str] = None
    xml_data: Optional[str] = None
    unit_phase_id: Optional[int] = None
    unit_phase: Optional[str] = None
    process_code: Optional[str] = None
    tags: List[Setting] = field(default_factory=list)
    product_revision: Optional[ProductRevision] = None
    product: Optional[Product] = None
    sub_units: List["Unit"] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Unit":
        """Create Unit from API response dictionary"""
        serial_date = None
        if data.get("serialDate"):
            try:
                serial_date = datetime.fromisoformat(data["serialDate"].replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
                
        return cls(
            serial_number=data.get("serialNumber"),
            part_number=data.get("partNumber"),
            revision=data.get("revision"),
            parent_serial_number=data.get("parentSerialNumber"),
            batch_number=data.get("batchNumber"),
            serial_date=serial_date,
            current_location=data.get("currentLocation"),
            xml_data=data.get("xmlData"),
            unit_phase_id=data.get("unitPhaseId"),
            unit_phase=data.get("unitPhase"),
            process_code=data.get("processCode"),
            tags=[Setting.from_dict(t) for t in data.get("tags", [])],
            product_revision=ProductRevision.from_dict(data["productRevision"]) if data.get("productRevision") else None,
            product=Product.from_dict(data["product"]) if data.get("product") else None,
            sub_units=[Unit.from_dict(u) for u in data.get("subUnits", [])]
        )

    def to_dict(self) -> dict:
        """Convert to dictionary for API requests"""
        result = {}
        
        if self.serial_number:
            result["serialNumber"] = self.serial_number
        if self.part_number:
            result["partNumber"] = self.part_number
        if self.revision:
            result["revision"] = self.revision
        if self.parent_serial_number:
            result["parentSerialNumber"] = self.parent_serial_number
        if self.batch_number:
            result["batchNumber"] = self.batch_number
        if self.current_location:
            result["currentLocation"] = self.current_location
        if self.xml_data:
            result["xmlData"] = self.xml_data
        if self.unit_phase_id is not None:
            result["unitPhaseId"] = self.unit_phase_id
        if self.process_code:
            result["processCode"] = self.process_code
            
        return result


@dataclass
class UnitVerification:
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
    process_code: Optional[int] = None
    process_name: Optional[str] = None
    process_index: Optional[int] = None
    status: Optional[str] = None
    start_utc: Optional[datetime] = None
    station_name: Optional[str] = None
    total_count: Optional[int] = None
    non_passed_count: Optional[int] = None
    repair_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "UnitVerification":
        """Create UnitVerification from API response dictionary"""
        start_utc = None
        if data.get("startUtc"):
            try:
                start_utc = datetime.fromisoformat(data["startUtc"].replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                pass
                
        return cls(
            process_code=data.get("processCode"),
            process_name=data.get("processName"),
            process_index=data.get("processIndex"),
            status=data.get("status"),
            start_utc=start_utc,
            station_name=data.get("stationName"),
            total_count=data.get("totalCount"),
            non_passed_count=data.get("nonPassedCount"),
            repair_count=data.get("repairCount")
        )


@dataclass
class UnitVerificationGrade:
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
    status: Optional[str] = None
    grade: Optional[str] = None
    all_processes_executed_in_correct_order: bool = False
    all_processes_passed_first_run: bool = False
    all_processes_passed_any_run: bool = False
    all_processes_passed_last_run: bool = False
    no_repairs: bool = False
    results: List[UnitVerification] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "UnitVerificationGrade":
        """Create UnitVerificationGrade from API response dictionary"""
        return cls(
            status=data.get("status"),
            grade=data.get("grade"),
            all_processes_executed_in_correct_order=data.get("allProcessesExecutedInCorrectOrder", False),
            all_processes_passed_first_run=data.get("allProcessesPassedFirstRun", False),
            all_processes_passed_any_run=data.get("allProcessesPassedAnyRun", False),
            all_processes_passed_last_run=data.get("allProcessesPassedLastRun", False),
            no_repairs=data.get("noRepairs", False),
            results=[UnitVerification.from_dict(r) for r in data.get("results", [])]
        )
