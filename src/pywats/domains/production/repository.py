"""Production repository - data access layer.

All API interactions for production units, serial numbers, and batches.
"""
from typing import Optional, List, Dict, Any, Union, Sequence, TYPE_CHECKING, cast
import logging

if TYPE_CHECKING:
    from ...core import HttpClient
    from ...core.exceptions import ErrorHandler

from .models import (
    Unit, UnitChange, ProductionBatch, SerialNumberType,
    UnitVerification, UnitVerificationGrade, UnitPhase
)


class ProductionRepository:
    """
    Production data access layer.

    Handles all WATS API interactions for production management.
    """

    def __init__(
        self, 
        http_client: "HttpClient",
        error_handler: Optional["ErrorHandler"] = None
    ):
        """
        Initialize with HTTP client.

        Args:
            http_client: HttpClient for making HTTP requests
            error_handler: Optional ErrorHandler for error handling (default: STRICT mode)
        """
        self._http_client = http_client
        # Import here to avoid circular imports
        from ...core.exceptions import ErrorHandler, ErrorMode
        self._error_handler = error_handler or ErrorHandler(ErrorMode.STRICT)

    # =========================================================================
    # Unit CRUD
    # =========================================================================

    def get_unit(
        self, serial_number: str, part_number: str
    ) -> Optional[Unit]:
        """
        Get unit information.

        GET /api/Production/Unit/{serialNumber}/{partNumber}

        Args:
            serial_number: The unit serial number
            part_number: The product part number

        Returns:
            Unit object or None if not found
        """
        response = self._http_client.get(
            f"/api/Production/Unit/{serial_number}/{part_number}"
        )
        data = self._error_handler.handle_response(
            response, operation="get_unit", allow_empty=True
        )
        if data:
            return Unit.model_validate(data)
        return None

    def save_units(
        self, units: Sequence[Union[Unit, Dict[str, Any]]]
    ) -> List[Unit]:
        """
        Add or update units by serial number.

        PUT /api/Production/Units

        Args:
            units: List of Unit objects or data dictionaries

        Returns:
            List of created/updated Unit objects
        """
        payload = [
            u.model_dump(by_alias=True, exclude_none=True)
            if isinstance(u, Unit) else u
            for u in units
        ]
        response = self._http_client.put("/api/Production/Units", data=payload)
        data = self._error_handler.handle_response(
            response, operation="save_units", allow_empty=True
        )
        if data:
            # Check if response is a list (success) or dict (batch result)
            if isinstance(data, list):
                return [Unit.model_validate(item) for item in data]
            elif isinstance(data, dict):
                # Batch operation result - check if successful
                if data.get('errorCount', 0) == 0:
                    # Success - return the units we sent (can't get them back from API)
                    return [u if isinstance(u, Unit) else Unit.model_validate(u) for u in units]
                else:
                    # Has errors
                    from ...core.exceptions import PyWATSError
                    raise PyWATSError(f"Failed to save units: {data}")
        return []

    # =========================================================================
    # Unit Verification
    # =========================================================================

    def get_unit_verification(
        self,
        serial_number: str,
        part_number: str,
        revision: Optional[str] = None
    ) -> Optional[UnitVerification]:
        """
        Verifies the unit and returns its grade.

        GET /api/Production/UnitVerification

        Args:
            serial_number: The unit serial number
            part_number: The product part number
            revision: Optional product revision

        Returns:
            UnitVerification object or None
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number
        }
        if revision:
            params["revision"] = revision
        response = self._http_client.get(
            "/api/Production/UnitVerification", params=params
        )
        data = self._error_handler.handle_response(
            response, operation="get_unit_verification", allow_empty=True
        )
        if data:
            return UnitVerification.model_validate(data)
        return None

    def get_unit_verification_grade(
        self,
        serial_number: str,
        part_number: str,
        revision: Optional[str] = None
    ) -> Optional[UnitVerificationGrade]:
        """
        Get complete verification grade for a unit.

        GET /api/Production/UnitVerification

        Args:
            serial_number: The unit serial number
            part_number: The product part number
            revision: Optional product revision

        Returns:
            UnitVerificationGrade object or None
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number
        }
        if revision:
            params["revision"] = revision
        response = self._http_client.get(
            "/api/Production/UnitVerification", params=params
        )
        data = self._error_handler.handle_response(
            response, operation="get_unit_verification_grade", allow_empty=True
        )
        if data:
            return UnitVerificationGrade.model_validate(data)
        return None

    # =========================================================================
    # Unit Phase and Process
    # =========================================================================

    def set_unit_phase(
        self,
        serial_number: str,
        part_number: str,
        phase: Union[int, str],
        comment: Optional[str] = None
    ) -> bool:
        """
        Set a unit's current phase.

        PUT /api/Production/SetUnitPhase

        Args:
            serial_number: The unit serial number
            part_number: The product part number
            phase: The phase ID (int) or phase name (str)
            comment: Optional comment

        Returns:
            True if successful
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "phase": phase
        }
        if comment:
            params["comment"] = comment
        response = self._http_client.put(
            "/api/Production/SetUnitPhase", params=params
        )
        self._error_handler.handle_response(
            response, operation="set_unit_phase", allow_empty=True
        )
        return response.is_success

    def set_unit_process(
        self,
        serial_number: str,
        part_number: str,
        process_code: Optional[int] = None,
        comment: Optional[str] = None
    ) -> bool:
        """
        Set a unit's process.

        PUT /api/Production/SetUnitProcess

        Args:
            serial_number: The unit serial number
            part_number: The product part number
            process_code: The process code
            comment: Optional comment

        Returns:
            True if successful
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number
        }
        if process_code is not None:
            params["processCode"] = process_code
        if comment:
            params["comment"] = comment
        response = self._http_client.put(
            "/api/Production/SetUnitProcess", params=params
        )
        self._error_handler.handle_response(
            response, operation="set_unit_process", allow_empty=True
        )
        return response.is_success

    # =========================================================================
    # Unit Changes
    # =========================================================================

    def get_unit_changes(
        self,
        serial_number: Optional[str] = None,
        part_number: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[UnitChange]:
        """
        Get unit change records.

        GET /api/Production/Units/Changes

        Args:
            serial_number: Optional serial number filter
            part_number: Optional part number filter
            top: Number of records to return
            skip: Number of records to skip

        Returns:
            List of UnitChange objects
        """
        params: Dict[str, Any] = {}
        if serial_number:
            params["serialNumber"] = serial_number
        if part_number:
            params["partNumber"] = part_number
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        response = self._http_client.get(
            "/api/Production/Units/Changes",
            params=params if params else None
        )
        data = self._error_handler.handle_response(
            response, operation="get_unit_changes", allow_empty=True
        )
        if data:
            return [UnitChange.model_validate(item) for item in data]
        return []

    def delete_unit_change(self, change_id: str) -> bool:
        """
        Delete a unit change record.

        DELETE /api/Production/Units/Changes/{id}

        Args:
            change_id: The change record ID

        Returns:
            True if successful
        """
        response = self._http_client.delete(
            f"/api/Production/Units/Changes/{change_id}"
        )
        self._error_handler.handle_response(
            response, operation="delete_unit_change", allow_empty=True
        )
        return response.is_success

    # =========================================================================
    # Child Units (Assembly)
    # =========================================================================

    def add_child_unit(
        self,
        parent_serial: str,
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> bool:
        """
        Create a parent/child relation between two units.

        POST /api/Production/AddChildUnit

        Args:
            parent_serial: Parent unit serial number
            parent_part: Parent product part number
            child_serial: Child unit serial number
            child_part: Child product part number

        Returns:
            True if successful
        """
        params: Dict[str, Any] = {
            "parentSerialNumber": parent_serial,
            "parentPartNumber": parent_part,
            "childSerialNumber": child_serial,
            "childPartNumber": child_part
        }
        response = self._http_client.post(
            "/api/Production/AddChildUnit", params=params
        )
        self._error_handler.handle_response(
            response, operation="add_child_unit", allow_empty=True
        )
        return response.is_success

    def remove_child_unit(
        self,
        parent_serial: str,
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> bool:
        """
        Remove the parent/child relation between two units.

        POST /api/Production/RemoveChildUnit

        Args:
            parent_serial: Parent unit serial number
            parent_part: Parent product part number
            child_serial: Child unit serial number
            child_part: Child product part number

        Returns:
            True if successful
        """
        params: Dict[str, Any] = {
            "parentSerialNumber": parent_serial,
            "parentPartNumber": parent_part,
            "childSerialNumber": child_serial,
            "childPartNumber": child_part
        }
        response = self._http_client.post(
            "/api/Production/RemoveChildUnit", params=params
        )
        self._error_handler.handle_response(
            response, operation="remove_child_unit", allow_empty=True
        )
        return response.is_success

    def check_child_units(
        self,
        serial_number: str,
        part_number: str,
        revision: str
    ) -> Optional[Dict[str, Any]]:
        """
        Verify child units according to box build.

        GET /api/Production/CheckChildUnits

        Args:
            serial_number: Parent serial number
            part_number: Parent part number
            revision: Parent revision

        Returns:
            Child unit check results or None
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "revision": revision
        }
        response = self._http_client.get(
            "/api/Production/CheckChildUnits", params=params
        )
        data = self._error_handler.handle_response(
            response, operation="check_child_units", allow_empty=True
        )
        if data:
            return cast(Dict[str, Any], data)
        return None

    # =========================================================================
    # Serial Numbers
    # =========================================================================

    def get_serial_number_types(self) -> List[SerialNumberType]:
        """
        Get serial number types.

        GET /api/Production/SerialNumbers/Types

        Returns:
            List of SerialNumberType objects
        """
        response = self._http_client.get("/api/Production/SerialNumbers/Types")
        data = self._error_handler.handle_response(
            response, operation="get_serial_number_types", allow_empty=True
        )
        if data:
            return [
                SerialNumberType.model_validate(item)
                for item in data
            ]
        return []

    def take_serial_numbers(
        self,
        type_name: str,
        count: int = 1,
        reference_sn: Optional[str] = None,
        reference_pn: Optional[str] = None,
        station_name: Optional[str] = None
    ) -> List[str]:
        """
        Take free serial numbers.

        POST /api/Production/SerialNumbers/Take

        Args:
            type_name: Serial number type name
            count: Number of serial numbers to take (quantity)
            reference_sn: Optional reference serial number
            reference_pn: Optional reference part number
            station_name: Optional station name

        Returns:
            List of allocated serial numbers
        """
        import re
        
        params: Dict[str, Any] = {
            "serialNumberType": type_name,
            "quantity": count
        }
        if reference_sn:
            params["refSN"] = reference_sn
        if reference_pn:
            params["refPN"] = reference_pn
        if station_name:
            params["stationName"] = station_name
        response = self._http_client.post(
            "/api/Production/SerialNumbers/Take", params=params
        )
        data = self._error_handler.handle_response(
            response, operation="take_serial_numbers", allow_empty=True
        )
        if data:
            # Handle XML response - extract serial numbers from <SN id="..."/> tags
            if isinstance(data, str) and "<SerialNumbers" in data:
                # Parse XML to extract serial number IDs
                sn_ids = re.findall(r'<SN id="([^"]+)"', data)
                return sn_ids
            elif isinstance(data, list):
                return data
            else:
                return [data] if data else []
        return []

    def get_serial_numbers_by_range(
        self,
        type_name: str,
        from_serial: str,
        to_serial: str
    ) -> List[Dict[str, Any]]:
        """
        Get serial numbers in a range.

        GET /api/Production/SerialNumbers/ByRange

        Args:
            type_name: Serial number type name
            from_serial: Start of range
            to_serial: End of range

        Returns:
            List of serial number records
        """
        params: Dict[str, Any] = {
            "typeName": type_name,
            "from": from_serial,
            "to": to_serial
        }
        response = self._http_client.get(
            "/api/Production/SerialNumbers/ByRange", params=params
        )
        data = self._error_handler.handle_response(
            response, operation="get_serial_numbers_by_range", allow_empty=True
        )
        if data:
            return (
                data if isinstance(data, list) else []
            )
        return []

    def get_serial_numbers_by_reference(
        self,
        type_name: str,
        reference_serial: Optional[str] = None,
        reference_part: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get serial numbers by reference.

        GET /api/Production/SerialNumbers/ByReference

        Args:
            type_name: Serial number type name
            reference_serial: Reference serial number
            reference_part: Reference part number

        Returns:
            List of serial number records
        """
        params: Dict[str, Any] = {"typeName": type_name}
        if reference_serial:
            params["referenceSerialNumber"] = reference_serial
        if reference_part:
            params["referencePartNumber"] = reference_part
        response = self._http_client.get(
            "/api/Production/SerialNumbers/ByReference", params=params
        )
        data = self._error_handler.handle_response(
            response, operation="get_serial_numbers_by_reference", allow_empty=True
        )
        if data:
            return (
                data if isinstance(data, list) else []
            )
        return []

    def upload_serial_numbers(
        self,
        file_content: bytes,
        content_type: str = "text/csv"
    ) -> bool:
        """
        Upload serial numbers file (XML or CSV).

        PUT /api/Production/SerialNumbers

        Args:
            file_content: File content as bytes
            content_type: MIME type

        Returns:
            True if successful
        """
        headers = {"Content-Type": content_type}
        response = self._http_client.put(
            "/api/Production/SerialNumbers",
            data=file_content,
            headers=headers
        )
        self._error_handler.handle_response(
            response, operation="upload_serial_numbers", allow_empty=True
        )
        return response.is_success

    def export_serial_numbers(
        self,
        type_name: str,
        state: Optional[str] = None,
        format: str = "csv"
    ) -> Optional[bytes]:
        """
        Export serial numbers as file.

        GET /api/Production/SerialNumbers

        Args:
            type_name: Serial number type name
            state: Optional state filter
            format: Output format (csv or xml)

        Returns:
            File content as bytes or None
        """
        params: Dict[str, Any] = {"typeName": type_name}
        if state:
            params["state"] = state
        if format:
            params["format"] = format
        response = self._http_client.get(
            "/api/Production/SerialNumbers", params=params
        )
        self._error_handler.handle_response(
            response, operation="export_serial_numbers", allow_empty=True
        )
        if response.is_success:
            return response.raw
        return None

    # =========================================================================
    # Batches
    # =========================================================================

    def save_batches(
        self, batches: Sequence[Union[ProductionBatch, Dict[str, Any]]]
    ) -> List[ProductionBatch]:
        """
        Add or update batches.

        PUT /api/Production/Batches

        Args:
            batches: List of ProductionBatch objects or data dictionaries

        Returns:
            List of saved ProductionBatch objects
        """
        payload = [
            b.model_dump(by_alias=True, exclude_none=True)
            if isinstance(b, ProductionBatch) else b
            for b in batches
        ]
        response = self._http_client.put("/api/Production/Batches", data=payload)
        data = self._error_handler.handle_response(
            response, operation="save_batches", allow_empty=True
        )
        if data:
            return [
                ProductionBatch.model_validate(item)
                for item in data
            ]
        return []

    # =========================================================================
    # Unit Phases - Delegated to Internal Repository
    # =========================================================================

    def get_unit_phases(self, base_url: str) -> List[UnitPhase]:
        """
        Get all available unit phases.

        ⚠️ INTERNAL API - Delegated to ProductionRepositoryInternal.
        
        Note: This method is deprecated. Use ProductionServiceInternal instead.

        Args:
            base_url: The base URL for the Referer header

        Returns:
            List of UnitPhase objects
        """
        # Delegate to internal repository for proper separation
        from .repository_internal import ProductionRepositoryInternal
        internal_repo = ProductionRepositoryInternal(
            self._http_client, base_url, self._error_handler
        )
        return internal_repo.get_unit_phases()
