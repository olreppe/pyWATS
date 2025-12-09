"""Production service - business logic layer.

High-level operations for production unit management.
"""
from typing import Optional, List, Dict, Any, Sequence

from .models import (
    Unit, UnitChange, ProductionBatch, SerialNumberType,
    UnitVerification, UnitVerificationGrade
)
from .repository import ProductionRepository


class ProductionService:
    """
    Production business logic.

    Provides high-level operations for managing production units,
    serial numbers, batches, and assembly relationships.
    """

    def __init__(self, repository: ProductionRepository):
        """
        Initialize with repository.

        Args:
            repository: ProductionRepository for data access
        """
        self._repo = repository

    # =========================================================================
    # Unit Operations
    # =========================================================================

    def get_unit(
        self, serial_number: str, part_number: str
    ) -> Optional[Unit]:
        """
        Get a production unit.

        Args:
            serial_number: The unit serial number
            part_number: The product part number

        Returns:
            Unit if found, None otherwise
        """
        return self._repo.get_unit(serial_number, part_number)

    def create_units(self, units: Sequence[Unit]) -> List[Unit]:
        """
        Create multiple production units.

        Args:
            units: List of Unit objects to create

        Returns:
            List of created Unit objects
        """
        return self._repo.save_units(units)

    def update_unit(self, unit: Unit) -> Optional[Unit]:
        """
        Update a production unit.

        Args:
            unit: Unit object with updated fields

        Returns:
            Updated Unit object
        """
        result = self._repo.save_units([unit])
        return result[0] if result else None

    # =========================================================================
    # Unit Verification
    # =========================================================================

    def verify_unit(
        self,
        serial_number: str,
        part_number: str,
        revision: Optional[str] = None
    ) -> Optional[UnitVerification]:
        """
        Verify a unit and get its status.

        Args:
            serial_number: The unit serial number
            part_number: The product part number
            revision: Optional product revision

        Returns:
            UnitVerification result
        """
        return self._repo.get_unit_verification(
            serial_number, part_number, revision
        )

    def get_unit_grade(
        self,
        serial_number: str,
        part_number: str,
        revision: Optional[str] = None
    ) -> Optional[UnitVerificationGrade]:
        """
        Get complete verification grade for a unit.

        Args:
            serial_number: The unit serial number
            part_number: The product part number
            revision: Optional product revision

        Returns:
            UnitVerificationGrade result
        """
        return self._repo.get_unit_verification_grade(
            serial_number, part_number, revision
        )

    def is_unit_passing(
        self,
        serial_number: str,
        part_number: str
    ) -> bool:
        """
        Check if a unit is passing all tests.

        Args:
            serial_number: The unit serial number
            part_number: The product part number

        Returns:
            True if unit is passing
        """
        grade = self._repo.get_unit_verification_grade(
            serial_number, part_number
        )
        if grade:
            return grade.all_processes_passed_last_run
        return False

    # =========================================================================
    # Unit Phase and Process
    # =========================================================================

    def set_unit_phase(
        self,
        serial_number: str,
        part_number: str,
        phase: str,
        comment: Optional[str] = None
    ) -> bool:
        """
        Set a unit's current phase.

        Args:
            serial_number: The unit serial number
            part_number: The product part number
            phase: The new phase
            comment: Optional comment

        Returns:
            True if successful
        """
        return self._repo.set_unit_phase(
            serial_number, part_number, phase, comment
        )

    def set_unit_process(
        self,
        serial_number: str,
        part_number: str,
        process_code: Optional[int] = None,
        comment: Optional[str] = None
    ) -> bool:
        """
        Set a unit's process.

        Args:
            serial_number: The unit serial number
            part_number: The product part number
            process_code: The process code
            comment: Optional comment

        Returns:
            True if successful
        """
        return self._repo.set_unit_process(
            serial_number, part_number, process_code, comment
        )

    # =========================================================================
    # Unit Changes
    # =========================================================================

    def get_unit_changes(
        self,
        serial_number: Optional[str] = None,
        part_number: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[UnitChange]:
        """
        Get unit change records.

        Args:
            serial_number: Optional serial number filter
            part_number: Optional part number filter
            top: Max number of records

        Returns:
            List of UnitChange objects
        """
        return self._repo.get_unit_changes(
            serial_number=serial_number,
            part_number=part_number,
            top=top
        )

    def acknowledge_unit_change(self, change_id: str) -> bool:
        """
        Acknowledge and delete a unit change record.

        Args:
            change_id: The change record ID

        Returns:
            True if successful
        """
        return self._repo.delete_unit_change(change_id)

    # =========================================================================
    # Assembly (Parent/Child)
    # =========================================================================

    def add_child_to_assembly(
        self,
        parent_serial: str,
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> bool:
        """
        Add a child unit to a parent assembly.

        Args:
            parent_serial: Parent unit serial number
            parent_part: Parent product part number
            child_serial: Child unit serial number
            child_part: Child product part number

        Returns:
            True if successful
        """
        return self._repo.add_child_unit(
            parent_serial, parent_part, child_serial, child_part
        )

    def remove_child_from_assembly(
        self,
        parent_serial: str,
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> bool:
        """
        Remove a child unit from a parent assembly.

        Args:
            parent_serial: Parent unit serial number
            parent_part: Parent product part number
            child_serial: Child unit serial number
            child_part: Child product part number

        Returns:
            True if successful
        """
        return self._repo.remove_child_unit(
            parent_serial, parent_part, child_serial, child_part
        )

    def verify_assembly(
        self,
        serial_number: str,
        part_number: str,
        revision: str
    ) -> Optional[Dict[str, Any]]:
        """
        Verify that assembly child units match box build.

        Args:
            serial_number: Parent serial number
            part_number: Parent part number
            revision: Parent revision

        Returns:
            Verification results or None
        """
        return self._repo.check_child_units(
            serial_number, part_number, revision
        )

    # =========================================================================
    # Serial Numbers
    # =========================================================================

    def get_serial_number_types(self) -> List[SerialNumberType]:
        """
        Get all serial number types.

        Returns:
            List of SerialNumberType objects
        """
        return self._repo.get_serial_number_types()

    def allocate_serial_numbers(
        self,
        type_name: str,
        count: int = 1,
        reference_sn: Optional[str] = None,
        reference_pn: Optional[str] = None,
        station_name: Optional[str] = None
    ) -> List[str]:
        """
        Allocate serial numbers from pool.

        Args:
            type_name: Serial number type name
            count: Number to allocate
            reference_sn: Optional reference serial number
            reference_pn: Optional reference part number
            station_name: Optional station name

        Returns:
            List of allocated serial numbers
        """
        return self._repo.take_serial_numbers(
            type_name, count, reference_sn, reference_pn, station_name
        )

    def find_serial_numbers_in_range(
        self,
        type_name: str,
        from_serial: str,
        to_serial: str
    ) -> List[Dict[str, Any]]:
        """
        Find serial numbers in a range.

        Args:
            type_name: Serial number type name
            from_serial: Start of range
            to_serial: End of range

        Returns:
            List of serial number records
        """
        return self._repo.get_serial_numbers_by_range(
            type_name, from_serial, to_serial
        )

    def find_serial_numbers_by_reference(
        self,
        type_name: str,
        reference_serial: Optional[str] = None,
        reference_part: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find serial numbers by reference.

        Args:
            type_name: Serial number type name
            reference_serial: Reference serial number
            reference_part: Reference part number

        Returns:
            List of serial number records
        """
        return self._repo.get_serial_numbers_by_reference(
            type_name, reference_serial, reference_part
        )

    def import_serial_numbers(
        self,
        file_content: bytes,
        content_type: str = "text/csv"
    ) -> bool:
        """
        Import serial numbers from file.

        Args:
            file_content: File content as bytes
            content_type: MIME type (text/csv or application/xml)

        Returns:
            True if successful
        """
        return self._repo.upload_serial_numbers(file_content, content_type)

    def export_serial_numbers(
        self,
        type_name: str,
        state: Optional[str] = None,
        format: str = "csv"
    ) -> Optional[bytes]:
        """
        Export serial numbers to file.

        Args:
            type_name: Serial number type name
            state: Optional state filter
            format: Output format (csv or xml)

        Returns:
            File content as bytes or None
        """
        return self._repo.export_serial_numbers(type_name, state, format)

    # =========================================================================
    # Batches
    # =========================================================================

    def save_batches(
        self, batches: Sequence[ProductionBatch]
    ) -> List[ProductionBatch]:
        """
        Create or update production batches.

        Args:
            batches: List of ProductionBatch objects

        Returns:
            List of saved ProductionBatch objects
        """
        return self._repo.save_batches(batches)
