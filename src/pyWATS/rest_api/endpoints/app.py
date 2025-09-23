"""
App Endpoints

Application-level endpoints for analytics, measurements, and yield data.
These endpoints are grouped by the "App" tag in the OpenAPI specification.
"""

from typing import Optional, Dict, Any, List, Union
import httpx

from ..client import get_default_client, WATSClient
from ..exceptions import handle_response_error
from ..models import PublicWatsFilter


def get_aggregated_measurements(
    filter_data: PublicWatsFilter,
    measurement_paths: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get aggregated numeric measurements by measurement path.
    
    Maximum of 10000 measurements are returned. Requesting with empty filter
    will return measurements from the last seven days most failed steps.
    
    Args:
        filter_data: WATS filter (partnumber and testOperation required)
        measurement_paths: Measurement paths separated by semicolon
        client: Optional WATS client instance
        
    Returns:
        Aggregated measurements data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if measurement_paths:
        params["measurementPaths"] = measurement_paths
    
    response = client.post(
        "/api/App/AggregatedMeasurements",
        json=filter_data.dict(exclude_none=True, by_alias=True),
        params=params
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_dynamic_repair(
    filter_data: PublicWatsFilter,
    dimensions: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Calculate repair statistics by custom dimensions.
    
    PREVIEW endpoint - subject to changes.
    
    Args:
        filter_data: WATS filter
        dimensions: Custom dimensions separated by semicolon
        client: Optional WATS client instance
        
    Returns:
        Repair statistics data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if dimensions:
        params["dimensions"] = dimensions
    
    response = client.post(
        "/api/App/DynamicRepair",
        json=filter_data.dict(exclude_none=True, by_alias=True),
        params=params
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_dynamic_yield(
    filter_data: PublicWatsFilter,
    dimensions: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Calculate yield by custom dimensions.
    
    PREVIEW endpoint - subject to changes.
    
    Args:
        filter_data: WATS filter
        dimensions: Custom dimensions separated by semicolon
        client: Optional WATS client instance
        
    Returns:
        Yield statistics data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if dimensions:
        params["dimensions"] = dimensions
    
    response = client.post(
        "/api/App/DynamicYield",
        json=filter_data.dict(exclude_none=True, by_alias=True),
        params=params
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_high_volume(
    days: Optional[int] = None,
    product_group_id: Optional[str] = None,
    level_id: Optional[str] = None,
    filter_data: Optional[PublicWatsFilter] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get high volume list or yield sorted by volume.
    
    Args:
        days: Number of days to include (for GET request)
        product_group_id: Product group filter (for GET request)
        level_id: Level filter (for GET request)
        filter_data: WATS filter (for POST request)
        client: Optional WATS client instance
        
    Returns:
        High volume data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    if filter_data:
        # POST request
        response = client.post(
            "/api/App/HighVolume",
            json=filter_data.dict(exclude_none=True, by_alias=True)
        )
    else:
        # GET request
        params = {}
        if days is not None:
            params["days"] = days
        if product_group_id:
            params["productGroupId"] = product_group_id
        if level_id:
            params["levelId"] = level_id
            
        response = client.get("/api/App/HighVolume", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_high_volume_by_product_group(
    filter_data: PublicWatsFilter,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get yield by product group sorted by volume.
    
    Args:
        filter_data: WATS filter
        client: Optional WATS client instance
        
    Returns:
        High volume by product group data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.post(
        "/api/App/HighVolumeByProductGroup",
        json=filter_data.dict(exclude_none=True, by_alias=True)
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_levels(client: Optional[WATSClient] = None) -> Dict[str, Any]:
    """
    Retrieve all ClientGroups.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        Client groups data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/App/Levels")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_measurements(
    filter_data: PublicWatsFilter,
    measurement_paths: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get numeric measurements by measurement path.
    
    PREVIEW endpoint - subject to changes.
    Maximum of 10000 measurements are returned.
    
    Args:
        filter_data: WATS filter (partnumber and testOperation required)
        measurement_paths: Measurement paths separated by semicolon
        client: Optional WATS client instance
        
    Returns:
        Measurements data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if measurement_paths:
        params["measurementPaths"] = measurement_paths
    
    response = client.post(
        "/api/App/Measurements",
        json=filter_data.dict(exclude_none=True, by_alias=True),
        params=params
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_oee_analysis(
    filter_data: PublicWatsFilter,
    available_time: str,
    min_connection_time: Optional[int] = None,
    max_connection_time: Optional[int] = None,
    min_execution_time: Optional[int] = None,
    max_execution_time: Optional[int] = None,
    target_output: Optional[int] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Overall Equipment Effectiveness analysis.
    
    Args:
        filter_data: WATS filter
        available_time: Available hours by weekday (e.g., "24,24,24,24,24,24,24")
        min_connection_time: Minimum connection time filter
        max_connection_time: Maximum connection time filter
        min_execution_time: Minimum execution time filter
        max_execution_time: Maximum execution time filter
        target_output: Target output per day
        client: Optional WATS client instance
        
    Returns:
        OEE analysis data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"availableTime": available_time}
    if min_connection_time is not None:
        params["minConnectionTime"] = min_connection_time
    if max_connection_time is not None:
        params["maxConnectionTime"] = max_connection_time
    if min_execution_time is not None:
        params["minExecutionTime"] = min_execution_time
    if max_execution_time is not None:
        params["maxExecutionTime"] = max_execution_time
    if target_output is not None:
        params["targetOutput"] = target_output
    
    response = client.post(
        "/api/App/OeeAnalysis",
        json=filter_data.dict(exclude_none=True, by_alias=True),
        params=params
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_processes(
    include_test_operations: Optional[bool] = None,
    include_repair_operations: Optional[bool] = None,
    include_wip_operations: Optional[bool] = None,
    include_inactive_processes: Optional[bool] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get processes.
    
    Args:
        include_test_operations: Include processes marked as IsTestOperation
        include_repair_operations: Include processes marked as IsRepairOperation
        include_wip_operations: Include processes marked as IsWipOperation
        include_inactive_processes: Include inactive processes
        client: Optional WATS client instance
        
    Returns:
        Processes data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if include_test_operations is not None:
        params["includeTestOperations"] = include_test_operations
    if include_repair_operations is not None:
        params["includeRepairOperations"] = include_repair_operations
    if include_wip_operations is not None:
        params["includeWipOperations"] = include_wip_operations
    if include_inactive_processes is not None:
        params["includeInactiveProcesses"] = include_inactive_processes
    
    response = client.get("/api/App/Processes", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_product_groups(
    include_filters: Optional[bool] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Retrieve all ProductGroups.
    
    Args:
        include_filters: Include or exclude product group filters
        client: Optional WATS client instance
        
    Returns:
        Product groups data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if include_filters is not None:
        params["includeFilters"] = include_filters
    
    response = client.get("/api/App/ProductGroups", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_version(client: Optional[WATSClient] = None) -> str:
    """
    Get server/API version.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        Version string
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/App/Version")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_uut_report(
    serial_number: Optional[str] = None,
    part_number: Optional[str] = None,
    revision: Optional[str] = None,
    batch_number: Optional[str] = None,
    station_name: Optional[str] = None,
    test_operation: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    product_group_id: Optional[str] = None,
    level_id: Optional[str] = None,
    filter_data: Optional[PublicWatsFilter] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get UUT report header info like Test Reports in Reporting.
    
    Args:
        serial_number: Serial number
        part_number: Part number  
        revision: Revision
        batch_number: Batch number
        station_name: Station name
        test_operation: Test operation name
        status: Status
        date_from: Date from (e.g., "2017-10-19T10:43:00")
        date_to: Date to (e.g., "2017-10-19T10:43:00")
        product_group_id: Product group id
        level_id: Level id (split multiple groups with ;)
        filter_data: WATS filter (for POST request)
        client: Optional WATS client instance
        
    Returns:
        UUT report data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    if filter_data:
        # POST request
        response = client.post(
            "/api/App/UutReport",
            json=filter_data.dict(exclude_none=True, by_alias=True)
        )
    else:
        # GET request
        params = {}
        if serial_number:
            params["serialNumber"] = serial_number
        if part_number:
            params["partNumber"] = part_number
        if revision:
            params["revision"] = revision
        if batch_number:
            params["batchNumber"] = batch_number
        if station_name:
            params["stationName"] = station_name
        if test_operation:
            params["testOperation"] = test_operation
        if status:
            params["status"] = status
        if date_from:
            params["dateFrom"] = date_from
        if date_to:
            params["dateTo"] = date_to
        if product_group_id:
            params["productGroupId"] = product_group_id
        if level_id:
            params["levelId"] = level_id
            
        response = client.get("/api/App/UutReport", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()