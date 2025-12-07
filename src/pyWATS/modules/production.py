"""Production Module for pyWATS

Provides high-level operations for managing production units, serial numbers, and batches.
Includes sub-modules for serial number handling and unit verification.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime

from ..models import (
    Unit, UnitChange, ProductionBatch, SerialNumberType,
    UnitVerification, UnitVerificationGrade
)
from ..rest_api import ProductionApi


class SerialNumberHandler:
    """
    Sub-module for serial number operations.
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # Get serial number types
        types = api.production.serial_number.get_types()
        
        # Take serial numbers
        serials = api.production.serial_number.take(type_name="SN-Type", count=10)
    """
    
    def __init__(self, api: ProductionApi):
        self._api = api
    
    def get_types(self) -> List[SerialNumberType]:
        """
        Get all serial number types.
        
        Returns:
            List of SerialNumberType objects
        """
        # REST API now returns List[SerialNumberType] directly
        return self._api.get_serial_number_types()
    
    def get_by_range(
        self,
        type_name: str,
        from_serial: str,
        to_serial: str
    ) -> List[Dict[str, Any]]:
        """
        Get serial numbers by range.
        
        Args:
            type_name: Serial number type name
            from_serial: Start of range
            to_serial: End of range
            
        Returns:
            List of serial number data
        """
        # REST API now returns List[Dict] directly
        return self._api.get_serial_numbers_by_range(type_name, from_serial, to_serial)
    
    def get_by_reference(
        self, 
        type_name: str, 
        reference_serial: Optional[str] = None,
        reference_part: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get serial numbers by reference.
        
        Args:
            type_name: Serial number type name
            reference_serial: Reference serial number
            reference_part: Reference part number
            
        Returns:
            List of serial number data
        """
        # REST API now returns List[Dict] directly
        return self._api.get_serial_numbers_by_reference(
            type_name, 
            reference_serial=reference_serial,
            reference_part=reference_part
        )
    
    def take(
        self,
        type_name: str,
        count: int = 1,
        reference: Optional[str] = None,
        format: str = "json"
    ) -> List[str]:
        """
        Take (reserve) serial numbers from the system.
        
        Args:
            type_name: Serial number type name
            count: Number of serial numbers to take
            reference: Optional reference string
            format: Output format (json, xml, csv)
            
        Returns:
            List of reserved serial number strings
        """
        # REST API now returns List[str] directly
        return self._api.take_serial_numbers(
            type_name=type_name,
            count=count,
            reference=reference,
            format=format
        )
    
    def upload(self, file_content: bytes, content_type: str = "text/csv") -> bool:
        """
        Upload serial numbers to the system.
        
        Args:
            file_content: File content as bytes (CSV or XML)
            content_type: MIME type (text/csv or application/xml)
            
        Returns:
            True if successful
        """
        # REST API now returns bool directly
        return self._api.upload_serial_numbers(file_content, content_type)
    
    def export(
        self, 
        type_name: str, 
        state: Optional[str] = None,
        format: str = "csv"
    ) -> Optional[bytes]:
        """
        Export serial numbers as XML or CSV.
        
        Args:
            type_name: Serial number type name
            state: Optional state filter
            format: Output format (csv or xml)
            
        Returns:
            Exported serial number data as bytes, or None
        """
        # REST API now returns Optional[bytes] directly
        return self._api.export_serial_numbers(type_name, state=state, format=format)


class UnitVerificationHandler:
    """
    Sub-module for unit verification operations.
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # Verify a unit
        result = api.production.verification.verify("SN-12345", "PART-001", "A")
    """
    
    def __init__(self, api: ProductionApi):
        self._api = api
    
    def verify(
        self,
        serial_number: str,
        part_number: str,
        revision: Optional[str] = None
    ) -> Optional[UnitVerification]:
        """
        Verify a unit against verification rules.
        
        Args:
            serial_number: Unit serial number
            part_number: Product part number
            revision: Optional product revision
            
        Returns:
            UnitVerification with verification results, or None
        """
        # REST API now returns Optional[UnitVerification] directly
        return self._api.get_unit_verification(
            serial_number=serial_number,
            part_number=part_number,
            revision=revision
        )


class ProductionModule:
    """
    Production management module.
    
    Provides operations for:
    - Managing production units
    - Handling serial numbers
    - Managing batches
    - Unit verification
    - Tracking unit changes
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # Get a unit
        unit = api.production.get_unit("SN-12345", "PART-001")
        
        # Set unit phase
        api.production.set_phase("SN-12345", "PART-001", "Phase1")
        
        # Serial number operations
        serials = api.production.serial_number.take("SN-Type", 10)
        
        # Verify unit
        result = api.production.verification.verify("SN-12345", "PART-001", "A")
    """
    
    def __init__(self, api: ProductionApi):
        """
        Initialize ProductionModule with REST API client.
        
        Args:
            api: ProductionApi instance for making HTTP requests
        """
        self._api = api
        
        # Sub-modules
        self.serial_number = SerialNumberHandler(api)
        self.verification = UnitVerificationHandler(api)
    
    # -------------------------------------------------------------------------
    # Unit Operations
    # -------------------------------------------------------------------------
    
    def get_unit(
        self,
        serial_number: str,
        part_number: str
    ) -> Optional[Unit]:
        """
        Get a production unit (PREVIEW).
        
        Args:
            serial_number: Unit serial number
            part_number: Product part number
            
        Returns:
            Unit object if found, None otherwise
        """
        # REST API now returns Optional[Unit] directly
        return self._api.get_unit(serial_number, part_number)
    
    def create_or_update_units(self, units: List[Unit]) -> List[Unit]:
        """
        Add or update multiple units by serial number.
        
        Args:
            units: List of Unit objects to add/update
            
        Returns:
            List of updated Unit objects
        """
        # REST API now accepts List[Unit] and returns List[Unit] directly
        return self._api.create_or_update_units(units)  # type: ignore[arg-type]
    
    def set_phase(
        self,
        serial_number: str,
        part_number: str,
        phase: str,
        comment: Optional[str] = None
    ) -> bool:
        """
        Set the phase for a unit.
        
        Args:
            serial_number: Unit serial number
            part_number: Product part number
            phase: The phase to set
            comment: Optional comment
            
        Returns:
            True if successful
        """
        # REST API now returns bool directly
        return self._api.set_unit_phase(
            serial_number=serial_number,
            part_number=part_number,
            phase=phase,
            comment=comment
        )
    
    def set_process(
        self,
        serial_number: str,
        part_number: str,
        process_code: Optional[int] = None,
        comment: Optional[str] = None
    ) -> bool:
        """
        Set the process code for a unit.
        
        Args:
            serial_number: Unit serial number
            part_number: Product part number
            process_code: The process code to set
            comment: Optional comment
            
        Returns:
            True if successful
        """
        # REST API now returns bool directly
        return self._api.set_unit_process(
            serial_number=serial_number,
            part_number=part_number,
            process_code=process_code,
            comment=comment
        )
    
    # -------------------------------------------------------------------------
    # Parent/Child Operations
    # -------------------------------------------------------------------------
    
    def add_child(
        self, 
        parent_serial: str, 
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> bool:
        """
        Add a child unit to a parent unit.
        
        Args:
            parent_serial: Parent unit serial number
            parent_part: Parent product part number
            child_serial: Child unit serial number
            child_part: Child product part number
            
        Returns:
            True if successful
        """
        # REST API now returns bool directly
        return self._api.add_child_unit(
            parent_serial=parent_serial,
            parent_part=parent_part,
            child_serial=child_serial,
            child_part=child_part
        )
    
    def remove_child(
        self, 
        parent_serial: str, 
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> bool:
        """
        Remove a child unit from a parent unit.
        
        Args:
            parent_serial: Parent unit serial number
            parent_part: Parent product part number
            child_serial: Child unit serial number
            child_part: Child product part number
            
        Returns:
            True if successful
        """
        # REST API now returns bool directly
        return self._api.remove_child_unit(
            parent_serial=parent_serial,
            parent_part=parent_part,
            child_serial=child_serial,
            child_part=child_part
        )
    
    def check_children(
        self, 
        serial_number: str, 
        part_number: str,
        revision: str
    ) -> Optional[Dict[str, Any]]:
        """
        Check if child units of a parent are valid according to box build.
        
        Args:
            serial_number: Parent serial number
            part_number: Parent part number
            revision: Parent revision
            
        Returns:
            Validation result dictionary, or None
        """
        # REST API now returns Optional[Dict] directly
        return self._api.check_child_units(
            serial_number=serial_number,
            part_number=part_number,
            revision=revision
        )
    
    # -------------------------------------------------------------------------
    # Batch Operations
    # -------------------------------------------------------------------------
    
    def create_or_update_batches(
        self,
        batches: List[ProductionBatch]
    ) -> List[ProductionBatch]:
        """
        Add or update unit batches.
        
        Args:
            batches: List of ProductionBatch objects to add/update
            
        Returns:
            List of updated ProductionBatch objects
        """
        # REST API now accepts List[ProductionBatch] and returns List[ProductionBatch] directly
        return self._api.create_or_update_batches(batches)  # type: ignore[arg-type]
    
    # -------------------------------------------------------------------------
    # Unit Changes
    # -------------------------------------------------------------------------
    
    def get_unit_changes(
        self,
        serial_number: Optional[str] = None,
        part_number: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[UnitChange]:
        """
        Get unit change history.
        
        Args:
            serial_number: Optional serial number filter
            part_number: Optional part number filter
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            List of UnitChange records
        """
        # REST API now returns List[UnitChange] directly
        return self._api.get_unit_changes(
            serial_number=serial_number,
            part_number=part_number,
            top=top,
            skip=skip
        )
    
    def delete_unit_change(self, change_id: str) -> bool:
        """
        Delete a unit change record.
        
        Args:
            change_id: ID of the change record to delete (string)
            
        Returns:
            True if deletion was successful
        """
        # REST API now returns bool directly
        return self._api.delete_unit_change(change_id)
    
    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------
    
    def exists(self, serial_number: str, part_number: str) -> bool:
        """
        Check if a unit exists.
        
        Args:
            serial_number: Unit serial number
            part_number: Product part number
            
        Returns:
            True if unit exists, False otherwise
        """
        try:
            return self.get_unit(serial_number, part_number) is not None
        except Exception:
            return False
