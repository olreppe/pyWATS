"""
Production Endpoints

Production management endpoints for units, batches, and workflows.
These endpoints are grouped by the "Production" tag in the OpenAPI specification.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import httpx

from ..client import get_default_client, WATSClient
from ..exceptions import handle_response_error
from ..models import Unit, UnitChange, ProductionBatch, SerialNumberType, UnitVerificationGrade


def add_child_unit(
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Create a parent/child relation between two units.
    
    Args:
        parent_serial_number: Serial number of the parent unit
        parent_part_number: Part number of the parent unit
        child_serial_number: Serial number of the child unit
        child_part_number: Part number of the child unit
        check_part_number: Part number to validate child unit against
        check_revision: Revision to validate child unit against
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "parentSerialNumber": parent_serial_number,
        "parentPartNumber": parent_part_number,
        "childSerialNumber": child_serial_number,
        "childPartNumber": child_part_number,
        "checkPartNumber": check_part_number,
        "checkRevision": check_revision
    }
    
    response = client.post("/api/Production/AddChildUnit", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def create_batches(
    batches: List[ProductionBatch],
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Add or update unit batches.
    
    Args:
        batches: List of batches to add
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    batch_data = [batch.model_dump(exclude_none=True, by_alias=True) for batch in batches]
    
    response = client.put("/api/Production/Batches", json={"batches": batch_data})
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def check_child_units(
    parent_serial_number: str,
    parent_part_number: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Verify that the direct child units of the parent unit are correct.
    
    Args:
        parent_serial_number: Serial number of the parent unit
        parent_part_number: Part number of the parent unit
        client: Optional WATS client instance
        
    Returns:
        Verification result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "parentSerialNumber": parent_serial_number,
        "parentPartNumber": parent_part_number
    }
    
    response = client.get("/api/Production/CheckChildUnits", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def remove_child_unit(
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Remove the parent/child relation between two units.
    
    Args:
        parent_serial_number: Serial number of the parent unit
        parent_part_number: Part number of the parent unit
        child_serial_number: Serial number of the child unit
        child_part_number: Part number of the child unit
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "parentSerialNumber": parent_serial_number,
        "parentPartNumber": parent_part_number,
        "childSerialNumber": child_serial_number,
        "childPartNumber": child_part_number
    }
    
    response = client.post("/api/Production/RemoveChildUnit", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def export_serial_numbers(
    serial_number_type: str,
    format: str,
    start_address: Optional[str] = None,
    end_address: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    client: Optional[WATSClient] = None
) -> bytes:
    """
    Get an export of serial numbers as XML or CSV file.
    
    Args:
        serial_number_type: Serial number type to export
        format: File format (XML or CSV)
        start_address: First serial number to export
        end_address: Last serial number to export
        start_date: Earliest generated serial number to export
        end_date: Latest generated serial number to export
        client: Optional WATS client instance
        
    Returns:
        File content as bytes
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "serialNumberType": serial_number_type,
        "format": format
    }
    if start_address:
        params["startAddress"] = start_address
    if end_address:
        params["endAddress"] = end_address
    if start_date:
        params["startDate"] = start_date.isoformat()
    if end_date:
        params["endDate"] = end_date.isoformat()
    
    response = client.get("/api/Production/SerialNumbers", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.content


def upload_serial_numbers(
    serial_number_type: str,
    format: str,
    file_content: bytes,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Upload an XML or CSV file with serial numbers as multipart form data.
    
    Args:
        serial_number_type: Serial number type to add to
        format: File format (XML or CSV)
        file_content: File content as bytes
        client: Optional WATS client instance
        
    Returns:
        Upload result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "serialNumberType": serial_number_type,
        "format": format
    }
    
    files = {"file": file_content}
    
    response = client.put("/api/Production/SerialNumbers", params=params, files=files)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_serial_numbers_by_range(
    serial_number_type: str,
    start_address: str,
    end_address: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get serial numbers in a range.
    
    Args:
        serial_number_type: Serial number type to get
        start_address: First serial number to get
        end_address: Last serial number to get
        start_date: Earliest generated serial number to get
        end_date: Latest generated serial number to get
        client: Optional WATS client instance
        
    Returns:
        Serial numbers data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "serialNumberType": serial_number_type,
        "startAddress": start_address,
        "endAddress": end_address
    }
    if start_date:
        params["startDate"] = start_date.isoformat()
    if end_date:
        params["endDate"] = end_date.isoformat()
    
    response = client.get("/api/Production/SerialNumbers/ByRange", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_serial_numbers_by_reference(
    serial_number_type: str,
    ref_sn: Optional[str] = None,
    ref_pn: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get taken serial numbers by reference serial number or part number.
    
    Args:
        serial_number_type: Serial number type to get
        ref_sn: Reference serial number
        ref_pn: Reference part number
        start_date: Earliest generated serial number to get
        end_date: Latest generated serial number to get
        client: Optional WATS client instance
        
    Returns:
        Serial numbers data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"serialNumberType": serial_number_type}
    if ref_sn:
        params["refSN"] = ref_sn
    if ref_pn:
        params["refPN"] = ref_pn
    if start_date:
        params["startDate"] = start_date.isoformat()
    if end_date:
        params["endDate"] = end_date.isoformat()
    
    response = client.get("/api/Production/SerialNumbers/ByReference", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def take_serial_numbers(
    serial_number_type: str,
    quantity: int,
    ref_sn: Optional[str] = None,
    ref_pn: Optional[str] = None,
    station_name: Optional[str] = None,
    only_in_sequence: Optional[bool] = None,
    format: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Any:
    """
    Take free serial numbers and return them in XML or CSV format.
    
    Args:
        serial_number_type: Serial number type to get
        quantity: Amount of serial numbers to attempt to take
        ref_sn: Reference serial number
        ref_pn: Reference part number
        station_name: Reference station that requested the serial numbers
        only_in_sequence: Only take continuous serial numbers with no gaps
        format: Format to return serial numbers in (XML or CSV)
        client: Optional WATS client instance
        
    Returns:
        Serial numbers data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "serialNumberType": serial_number_type,
        "quantity": quantity
    }
    if ref_sn:
        params["refSN"] = ref_sn
    if ref_pn:
        params["refPN"] = ref_pn
    if station_name:
        params["stationName"] = station_name
    if only_in_sequence is not None:
        params["onlyInSequence"] = only_in_sequence
    if format:
        params["format"] = format
    
    response = client.post("/api/Production/SerialNumbers/Take", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    # Return raw content if format is specified, otherwise JSON
    if format:
        return response.content
    return response.json()


def get_serial_number_types(
    client: Optional[WATSClient] = None
) -> List[SerialNumberType]:
    """
    Get the serial number types.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        List of serial number types
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/Production/SerialNumbers/Types")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return [SerialNumberType(**item) for item in data]


def set_unit_phase(
    serial_number: str,
    part_number: str,
    phase: int,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Set a unit's current phase.
    
    Args:
        serial_number: Serial number
        part_number: Part number
        phase: Current phase (see documentation for phase values)
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "serialNumber": serial_number,
        "partNumber": part_number,
        "phase": phase
    }
    
    response = client.put("/api/Production/SetUnitPhase", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def set_unit_process(
    serial_number: str,
    part_number: str,
    process_name: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Set a unit's current process.
    
    Args:
        serial_number: Serial number
        part_number: Part number
        process_name: Process name
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "serialNumber": serial_number,
        "partNumber": part_number,
        "processName": process_name
    }
    
    response = client.put("/api/Production/SetUnitProcess", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_unit(
    serial_number: str,
    part_number: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get unit information (PREVIEW endpoint).
    
    Args:
        serial_number: Serial number
        part_number: Part number (optional)
        client: Optional WATS client instance
        
    Returns:
        Unit information
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get(f"/api/Production/Unit/{serial_number}/{part_number}")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def create_units(
    units: List[Unit],
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Add or update units by serial number.
    
    Args:
        units: List of units to add or update
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    unit_data = [unit.model_dump(exclude_none=True, by_alias=True) for unit in units]
    
    response = client.put("/api/Production/Units", json=unit_data)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_unit_changes(
    max_count: int,
    client: Optional[WATSClient] = None
) -> List[UnitChange]:
    """
    Get unit changes.
    
    Args:
        max_count: Maximum number of changes to return
        client: Optional WATS client instance
        
    Returns:
        List of unit changes
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"maxCount": max_count}
    
    response = client.get("/api/Production/Units/Changes", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return [UnitChange(**item) for item in data]


def delete_unit_change(
    change_id: int,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Delete a unit change once it has been handled.
    
    Args:
        change_id: ID of the change to delete
        client: Optional WATS client instance
        
    Returns:
        Deletion result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.delete(f"/api/Production/Units/Changes/{change_id}")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_unit_verification(
    serial_number: str,
    part_number: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> UnitVerificationGrade:
    """
    Verify the unit according to verification rules and return its grade.
    
    Args:
        serial_number: Serial number
        part_number: Part number
        client: Optional WATS client instance
        
    Returns:
        Unit verification grade
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"serialNumber": serial_number}
    if part_number:
        params["partNumber"] = part_number
    
    response = client.get("/api/Production/UnitVerification", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return UnitVerificationGrade(**data)