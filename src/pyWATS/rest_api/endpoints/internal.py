"""
Internal Endpoints

Internal API endpoints that require referrer headers and are typically used
by the WATS web interface. These endpoints provide additional functionality
beyond the public API.
"""

from typing import Optional, Dict, Any, List
import httpx

from ..client import get_default_client, WATSClient
from ..exceptions import handle_response_error
from ..models import PublicWatsFilter


# rest_api/endpoints/internal.py
class Internal:
    def __init__(self, client):
        self.client = client

    def get_available_system_languages(self) -> Dict[str, Any]:
        """
        Get a list of available system languages.

        Args:
            client: Optional WATS client instance

        Returns:
            Available system languages

        Raises:
            WATSAPIException: On API errors
        """
        response = self.client.get("/api/internal/App/GetAvailableSystemLanguages")

        if response.status_code != 200:
            handle_response_error(response)

        return response.json()
    """
    Get a list of available system languages.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        Available system languages
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/internal/App/GetAvailableSystemLanguages")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_aggregated_measurements_internal(
    product_group_id: str,
    level_id: str,
    days: int,
    step_filters: str,
    sequence_filters: str,
    measurement_name: Optional[str] = None,
    filter_data: Optional[PublicWatsFilter] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get aggregated measurement data (internal endpoint).
    
    Args:
        product_group_id: Product group ID
        level_id: Level ID
        days: Number of days
        step_filters: XML step filter
        sequence_filters: XML sequence filter
        measurement_name: Name of the measurement
        filter_data: WATS filter (for POST request)
        client: Optional WATS client instance
        
    Returns:
        Aggregated measurements data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    if filter_data:
        # POST request
        params = {
            "stepFilters": step_filters,
            "sequenceFilters": sequence_filters
        }
        if measurement_name:
            params["measurementName"] = measurement_name
            
        response = client.post(
            "/api/internal/App/AggregatedMeasurements",
            json=filter_data.dict(exclude_none=True, by_alias=True),
            params=params
        )
    else:
        # GET request
        params = {
            "productGroupId": product_group_id,
            "levelId": level_id,
            "days": days,
            "stepFilters": step_filters,
            "sequenceFilters": sequence_filters
        }
        if measurement_name:
            params["measurementName"] = measurement_name
            
        response = client.get("/api/internal/App/AggregatedMeasurements", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def create_dynamic_yield_excel_worksheet(
    filter_data: PublicWatsFilter,
    dimensions: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> bytes:
    """
    Create a dynamic yield Excel worksheet.
    
    Args:
        filter_data: WATS filter
        dimensions: Dimensions string
        client: Optional WATS client instance
        
    Returns:
        Excel file content as bytes
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if dimensions:
        params["dimensions"] = dimensions
    
    response = client.post(
        "/api/internal/App/CreateDynamicYieldExcelWorksheet",
        json=filter_data.dict(exclude_none=True, by_alias=True),
        params=params
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.content


def get_measurement_list(
    product_group_id: Optional[str] = None,
    level_id: Optional[str] = None,
    days: Optional[int] = None,
    step_filters: Optional[str] = None,
    sequence_filters: Optional[str] = None,
    filter_data: Optional[PublicWatsFilter] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get measurements for a step (internal endpoint).
    
    Args:
        product_group_id: Product group ID
        level_id: Level ID
        days: Number of days
        step_filters: XML step filter
        sequence_filters: XML sequence filter
        filter_data: WATS filter (for POST request)
        client: Optional WATS client instance
        
    Returns:
        Measurements list data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    if filter_data:
        # POST request
        params = {}
        if step_filters:
            params["stepFilters"] = step_filters
        if sequence_filters:
            params["sequenceFilters"] = sequence_filters
            
        response = client.post(
            "/api/internal/App/MeasurementList",
            json=filter_data.dict(exclude_none=True, by_alias=True),
            params=params
        )
    else:
        # GET request
        params = {}
        if product_group_id:
            params["productGroupId"] = product_group_id
        if level_id:
            params["levelId"] = level_id
        if days is not None:
            params["days"] = days
        if step_filters:
            params["stepFilters"] = step_filters
        if sequence_filters:
            params["sequenceFilters"] = sequence_filters
            
        response = client.get("/api/internal/App/MeasurementList", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_step_status_list(
    product_group_id: Optional[str] = None,
    level_id: Optional[str] = None,
    days: Optional[int] = None,
    step_filters: Optional[str] = None,
    sequence_filters: Optional[str] = None,
    filter_data: Optional[PublicWatsFilter] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get statuses for a step (internal endpoint).
    
    Args:
        product_group_id: Product group ID
        level_id: Level ID
        days: Number of days
        step_filters: XML step filter
        sequence_filters: XML sequence filter
        filter_data: WATS filter (for POST request)
        client: Optional WATS client instance
        
    Returns:
        Step status list data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    if filter_data:
        # POST request
        params = {}
        if step_filters:
            params["stepFilters"] = step_filters
        if sequence_filters:
            params["sequenceFilters"] = sequence_filters
            
        response = client.post(
            "/api/internal/App/StepStatusList",
            json=filter_data.dict(exclude_none=True, by_alias=True),
            params=params
        )
    else:
        # GET request
        params = {}
        if product_group_id:
            params["productGroupId"] = product_group_id
        if level_id:
            params["levelId"] = level_id
        if days is not None:
            params["days"] = days
        if step_filters:
            params["stepFilters"] = step_filters
        if sequence_filters:
            params["sequenceFilters"] = sequence_filters
            
        response = client.get("/api/internal/App/StepStatusList", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_top_failed_internal(
    part_number: Optional[str] = None,
    process_code: Optional[str] = None,
    product_group_id: Optional[str] = None,
    level_id: Optional[str] = None,
    days: Optional[int] = None,
    count: Optional[int] = None,
    filter_data: Optional[PublicWatsFilter] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get top failed steps (internal endpoint).
    
    Args:
        part_number: Part number of reports
        process_code: Process code of reports
        product_group_id: Product group of reports
        level_id: Level of reports
        days: Number of days ago reports were submitted
        count: Number of items to return
        filter_data: WATS filter (for POST request)
        client: Optional WATS client instance
        
    Returns:
        Top failed steps data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    if filter_data:
        # POST request
        response = client.post(
            "/api/internal/App/TopFailed",
            json=filter_data.dict(exclude_none=True, by_alias=True)
        )
    else:
        # GET request
        params = {}
        if part_number:
            params["partNumber"] = part_number
        if process_code:
            params["processCode"] = process_code
        if product_group_id:
            params["productGroupId"] = product_group_id
        if level_id:
            params["levelId"] = level_id
        if days is not None:
            params["days"] = days
        if count is not None:
            params["count"] = count
            
        response = client.get("/api/internal/App/TopFailed", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_logged_in_username(client: Optional[WATSClient] = None) -> Dict[str, Any]:
    """
    Get the logged in username.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        Username information
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/internal/Auth/GetLoggedInUsername")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_role_permissions(client: Optional[WATSClient] = None) -> Dict[str, Any]:
    """
    Get logged in user's allowed permissions.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        Role permissions data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/internal/Auth/GetRolePermissions")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def check_permissions(
    permissions: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Check permissions.
    
    Args:
        permissions: Comma separated list of RolePermissions enums (int)
        client: Optional WATS client instance
        
    Returns:
        Permission check result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"permissions": permissions}
    
    response = client.get("/api/internal/Auth/CheckPermissions", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_server_time(client: Optional[WATSClient] = None) -> Dict[str, Any]:
    """
    Get server time.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        Server time information
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/internal/Auth/GetServerTime")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


# Product-specific internal endpoints

def is_product_connected(client: Optional[WATSClient] = None) -> bool:
    """
    Check if product service is connected.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        True if connected, False otherwise
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/internal/Product/isConnected")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_product_info_internal(
    part_number: str,
    revision: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get product information (internal endpoint).
    
    Args:
        part_number: Product part number
        revision: Optional product revision
        client: Optional WATS client instance
        
    Returns:
        Product information
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"partNumber": part_number}
    if revision:
        params["revision"] = revision
    
    response = client.get("/api/internal/Product/GetProductInfo", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_products_internal(
    filter_text: str,
    include_non_serial: bool = True,
    include_revision: bool = True,
    top_count: int = 10,
    client: Optional[WATSClient] = None
) -> List[Dict[str, Any]]:
    """
    Get products with filter (internal endpoint).
    
    Args:
        filter_text: Filter string for product search
        include_non_serial: Include non-serialized products
        include_revision: Include revision information
        top_count: Maximum number of results
        client: Optional WATS client instance
        
    Returns:
        List of products matching criteria
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "filter": filter_text,
        "includeNonSerial": include_non_serial,
        "includeRevision": include_revision,
        "topCount": top_count
    }
    
    response = client.get("/api/internal/Product/GetProducts", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()