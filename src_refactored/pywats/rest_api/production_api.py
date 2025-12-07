"""
Production API Endpoints

Provides all REST API calls for production/unit management.

Public API Endpoints (from Swagger):
- POST /api/Production/AddChildUnit - Create parent/child relation
- PUT /api/Production/Batches - Add or update unit batches
- GET /api/Production/CheckChildUnits - Verify child units according to box build
- POST /api/Production/RemoveChildUnit - Remove parent/child relation
- GET /api/Production/SerialNumbers - Export serial numbers as XML/CSV
- PUT /api/Production/SerialNumbers - Upload serial numbers XML/CSV
- GET /api/Production/SerialNumbers/ByRange - Get serial numbers in range
- GET /api/Production/SerialNumbers/ByReference - Get serial numbers by reference
- POST /api/Production/SerialNumbers/Take - Take free serial numbers
- GET /api/Production/SerialNumbers/Types - Get serial number types
- PUT /api/Production/SetUnitPhase - Set unit's current phase
- PUT /api/Production/SetUnitProcess - Set unit's process
- GET /api/Production/Unit/{serialNumber}/{partNumber} - Get unit info (PREVIEW)
- PUT /api/Production/Units - Add or update units
- GET /api/Production/Units/Changes - Get unit changes
- DELETE /api/Production/Units/Changes/{id} - Delete unit change
- GET /api/Production/UnitVerification - Verify unit and get grade
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient, Response


class ProductionApi:
    """
    Production API endpoints.
    
    Endpoints for managing units, serial numbers, and production state.
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Unit Management
    # =========================================================================
    
    def get_unit(self, serial_number: str, part_number: str) -> 'Response':
        """
        Get unit information (PREVIEW).
        
        GET /api/Production/Unit/{serialNumber}/{partNumber}
        
        Args:
            serial_number: The unit serial number
            part_number: The product part number
            
        Returns:
            Response with unit data
        """
        return self._http.get(f"/api/Production/Unit/{serial_number}/{part_number}")
    
    def create_or_update_units(self, units: List[Dict[str, Any]]) -> 'Response':
        """
        Add or update units by serial number.
        
        PUT /api/Production/Units
        
        Args:
            units: List of unit data dictionaries
            
        Returns:
            Response with results
        """
        return self._http.put("/api/Production/Units", data=units)
    
    def get_unit_verification(
        self,
        serial_number: str,
        part_number: str,
        revision: Optional[str] = None
    ) -> 'Response':
        """
        Verifies the unit according to verification rules and returns its grade.
        
        GET /api/Production/UnitVerification
        
        Args:
            serial_number: The unit serial number
            part_number: The product part number
            revision: Optional product revision
            
        Returns:
            Response with verification status and grade
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number
        }
        if revision:
            params["revision"] = revision
        return self._http.get("/api/Production/UnitVerification", params=params)
    
    # =========================================================================
    # Unit Phase and Process
    # =========================================================================
    
    def set_unit_phase(
        self,
        serial_number: str,
        part_number: str,
        phase: str,
        comment: Optional[str] = None
    ) -> 'Response':
        """
        Set a unit's current phase.
        
        PUT /api/Production/SetUnitPhase
        
        Args:
            serial_number: The unit serial number
            part_number: The product part number
            phase: The new phase
            comment: Optional comment
            
        Returns:
            Response with result
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "phase": phase
        }
        if comment:
            params["comment"] = comment
        return self._http.put("/api/Production/SetUnitPhase", params=params)
    
    def set_unit_process(
        self,
        serial_number: str,
        part_number: str,
        process_code: Optional[int] = None,
        comment: Optional[str] = None
    ) -> 'Response':
        """
        Set a unit's process.
        
        PUT /api/Production/SetUnitProcess
        
        Args:
            serial_number: The unit serial number
            part_number: The product part number
            process_code: The process code
            comment: Optional comment
            
        Returns:
            Response with result
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number
        }
        if process_code is not None:
            params["processCode"] = process_code
        if comment:
            params["comment"] = comment
        return self._http.put("/api/Production/SetUnitProcess", params=params)
    
    # =========================================================================
    # Unit Changes
    # =========================================================================
    
    def get_unit_changes(
        self,
        serial_number: Optional[str] = None,
        part_number: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> 'Response':
        """
        Get old and new parent unit, part number, revision, and unitphase 
        for units that have changed.
        
        GET /api/Production/Units/Changes
        
        Args:
            serial_number: Optional serial number filter
            part_number: Optional part number filter
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            Response with unit changes
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
        return self._http.get("/api/Production/Units/Changes", params=params if params else None)
    
    def delete_unit_change(self, change_id: str) -> 'Response':
        """
        Delete a unit change once it has been handled.
        
        DELETE /api/Production/Units/Changes/{id}
        
        Args:
            change_id: The change record ID
            
        Returns:
            Response with result
        """
        return self._http.delete(f"/api/Production/Units/Changes/{change_id}")
    
    # =========================================================================
    # Child Units (Assembly)
    # =========================================================================
    
    def add_child_unit(
        self,
        parent_serial: str,
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> 'Response':
        """
        Create a parent/child relation between two units.
        
        POST /api/Production/AddChildUnit
        
        Args:
            parent_serial: Parent unit serial number
            parent_part: Parent product part number
            child_serial: Child unit serial number
            child_part: Child product part number
            
        Returns:
            Response with result
        """
        params: Dict[str, Any] = {
            "parentSerialNumber": parent_serial,
            "parentPartNumber": parent_part,
            "childSerialNumber": child_serial,
            "childPartNumber": child_part
        }
        return self._http.post("/api/Production/AddChildUnit", params=params)
    
    def remove_child_unit(
        self,
        parent_serial: str,
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> 'Response':
        """
        Removes the parent/child relation between two units.
        
        POST /api/Production/RemoveChildUnit
        
        Note: The parent/child relation must already exist.
        
        Args:
            parent_serial: Parent unit serial number
            parent_part: Parent product part number
            child_serial: Child unit serial number
            child_part: Child product part number
            
        Returns:
            Response with result
        """
        params: Dict[str, Any] = {
            "parentSerialNumber": parent_serial,
            "parentPartNumber": parent_part,
            "childSerialNumber": child_serial,
            "childPartNumber": child_part
        }
        return self._http.post("/api/Production/RemoveChildUnit", params=params)
    
    def check_child_units(
        self,
        serial_number: str,
        part_number: str,
        revision: str
    ) -> 'Response':
        """
        Verify that the direct child units of the parent unit are correct
        according to the box build.
        
        GET /api/Production/CheckChildUnits
        
        Args:
            serial_number: Parent serial number
            part_number: Parent part number
            revision: Parent revision
            
        Returns:
            Response with child unit check results
        """
        params: Dict[str, Any] = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "revision": revision
        }
        return self._http.get("/api/Production/CheckChildUnits", params=params)
    
    # =========================================================================
    # Serial Numbers
    # =========================================================================
    
    def get_serial_number_types(self) -> 'Response':
        """
        Gets the serial number types.
        
        GET /api/Production/SerialNumbers/Types
        
        Returns:
            Response with serial number types
        """
        return self._http.get("/api/Production/SerialNumbers/Types")
    
    def take_serial_numbers(
        self,
        type_name: str,
        count: int = 1,
        reference: Optional[str] = None,
        format: str = "json"
    ) -> 'Response':
        """
        Take free serial numbers and return them.
        
        POST /api/Production/SerialNumbers/Take
        
        Args:
            type_name: Serial number type name
            count: Number of serial numbers to take (default: 1)
            reference: Optional reference string
            format: Output format (json, xml, csv)
            
        Returns:
            Response with allocated serial numbers
        """
        params: Dict[str, Any] = {
            "typeName": type_name,
            "count": count
        }
        if reference:
            params["reference"] = reference
        if format != "json":
            params["format"] = format
        return self._http.post("/api/Production/SerialNumbers/Take", params=params)
    
    def get_serial_numbers_by_range(
        self,
        type_name: str,
        from_serial: str,
        to_serial: str
    ) -> 'Response':
        """
        Get serial numbers in a range.
        
        GET /api/Production/SerialNumbers/ByRange
        
        Args:
            type_name: Serial number type name
            from_serial: Start of range
            to_serial: End of range
            
        Returns:
            Response with serial numbers
        """
        params: Dict[str, Any] = {
            "typeName": type_name,
            "from": from_serial,
            "to": to_serial
        }
        return self._http.get("/api/Production/SerialNumbers/ByRange", params=params)
    
    def get_serial_numbers_by_reference(
        self,
        type_name: str,
        reference_serial: Optional[str] = None,
        reference_part: Optional[str] = None
    ) -> 'Response':
        """
        Get taken serial numbers by reference serial number or part number or both.
        
        GET /api/Production/SerialNumbers/ByReference
        
        Args:
            type_name: Serial number type name
            reference_serial: Reference serial number
            reference_part: Reference part number
            
        Returns:
            Response with serial numbers
        """
        params: Dict[str, Any] = {"typeName": type_name}
        if reference_serial:
            params["referenceSerialNumber"] = reference_serial
        if reference_part:
            params["referencePartNumber"] = reference_part
        return self._http.get("/api/Production/SerialNumbers/ByReference", params=params)
    
    def upload_serial_numbers(
        self,
        file_content: bytes,
        content_type: str = "text/csv"
    ) -> 'Response':
        """
        Upload an XML or CSV file with serial numbers.
        
        PUT /api/Production/SerialNumbers
        
        Args:
            file_content: File content as bytes
            content_type: MIME type (text/csv or application/xml)
            
        Returns:
            Response with result
        """
        headers = {"Content-Type": content_type}
        return self._http.put("/api/Production/SerialNumbers", data=file_content, headers=headers)
    
    def export_serial_numbers(
        self,
        type_name: str,
        state: Optional[str] = None,
        format: str = "csv"
    ) -> 'Response':
        """
        Get an export of serial numbers as XML or CSV file.
        
        GET /api/Production/SerialNumbers
        
        Args:
            type_name: Serial number type name
            state: Optional state filter
            format: Output format (csv or xml)
            
        Returns:
            Response with serial numbers
        """
        params: Dict[str, Any] = {"typeName": type_name}
        if state:
            params["state"] = state
        if format:
            params["format"] = format
        return self._http.get("/api/Production/SerialNumbers", params=params)
    
    # =========================================================================
    # Batches
    # =========================================================================
    
    def create_or_update_batches(self, batches: List[Dict[str, Any]]) -> 'Response':
        """
        Add or update unit batches.
        
        PUT /api/Production/Batches
        
        Args:
            batches: List of batch data dictionaries
            
        Returns:
            Response with results
        """
        return self._http.put("/api/Production/Batches", data=batches)
