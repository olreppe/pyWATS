"""
Asset Endpoints

Asset management endpoints for CRUD operations on assets and asset types.
These endpoints are grouped by the "Asset" tag in the OpenAPI specification.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import httpx

from ..client import get_default_client, WATSClient
from ..exceptions import handle_response_error
from ..models import Asset, AssetType, AssetMessage, AssetState


def get_assets(
    odata_filter: Optional[str] = None,
    odata_top: Optional[int] = None,
    odata_orderby: Optional[str] = None,
    odata_skip: Optional[int] = None,
    client: Optional[WATSClient] = None
) -> List[Dict[str, Any]]:
    """
    Get a list of assets matching the specified filter.
    
    Supports OData query options such as $filter, $top, $orderby, $skip.
    Returns top 1000 assets unless $top is specified otherwise.
    
    Args:
        odata_filter: OData $filter parameter
        odata_top: OData $top parameter
        odata_orderby: OData $orderby parameter
        odata_skip: OData $skip parameter
        client: Optional WATS client instance
        
    Returns:
        List of assets
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if odata_filter:
        params["$filter"] = odata_filter
    if odata_top is not None:
        params["$top"] = odata_top
    if odata_orderby:
        params["$orderby"] = odata_orderby
    if odata_skip is not None:
        params["$skip"] = odata_skip
    
    response = client.get("/api/Asset", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def create_asset(
    asset: Asset,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Create or update an asset.
    
    Properties like 'runningCount' and 'totalCount' must be updated using
    appropriate API methods (e.g., update_asset_count).
    
    Args:
        asset: Asset to create or update
        client: Optional WATS client instance
        
    Returns:
        Created/updated asset data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.put(
        "/api/Asset",
        json=asset.dict(exclude_none=True, by_alias=True)
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def delete_asset(
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Delete an asset by ID or serial number.
    
    Log records for the asset will also be deleted.
    Any child assets will change parent but not be deleted.
    
    Args:
        asset_id: Asset ID
        serial_number: Asset serial number
        client: Optional WATS client instance
        
    Returns:
        Deletion result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    
    response = client.delete("/api/Asset", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_asset_by_id(
    asset_id: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get an asset by asset ID.
    
    Args:
        asset_id: Asset ID
        client: Optional WATS client instance
        
    Returns:
        Asset data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get(f"/api/Asset/{asset_id}")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_asset_by_serial_number(
    serial_number: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get an asset by serial number.
    
    Args:
        serial_number: Asset serial number
        client: Optional WATS client instance
        
    Returns:
        Asset data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get(f"/api/Asset/{serial_number}")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def calibrate_asset(
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    date_time: Optional[datetime] = None,
    comment: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Inform that an asset has been calibrated.
    
    Args:
        asset_id: Asset ID
        serial_number: Asset serial number
        date_time: Calibration date (default: now)
        comment: Asset log message
        client: Optional WATS client instance
        
    Returns:
        Calibration result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    if date_time:
        params["dateTime"] = date_time.isoformat()
    if comment:
        params["comment"] = comment
    
    response = client.post("/api/Asset/Calibration", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def update_asset_count(
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    total_count: Optional[int] = None,
    increment_by: Optional[int] = None,
    increment_children: Optional[bool] = None,
    culture_code: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Increment the running and total count on an asset.
    
    Args:
        asset_id: Asset ID
        serial_number: Asset serial number
        total_count: New total count
        increment_by: Increment running and total count by value
        increment_children: Also increment count on sub assets/children
        culture_code: Culture code for translations
        client: Optional WATS client instance
        
    Returns:
        Count update result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    if total_count is not None:
        params["totalCount"] = total_count
    if increment_by is not None:
        params["incrementBy"] = increment_by
    if increment_children is not None:
        params["incrementChildren"] = increment_children
    if culture_code:
        params["cultureCode"] = culture_code
    
    response = client.put("/api/Asset/Count", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_asset_log(
    odata_filter: Optional[str] = None,
    odata_top: Optional[int] = None,
    odata_orderby: Optional[str] = None,
    odata_skip: Optional[int] = None,
    client: Optional[WATSClient] = None
) -> List[Dict[str, Any]]:
    """
    Get asset log records matching the specified filter.
    
    Supports OData query options. Returns top 1000 logs unless $top is specified.
    Results are ordered by descending log date/time unless $orderby is specified.
    
    Args:
        odata_filter: OData $filter parameter
        odata_top: OData $top parameter
        odata_orderby: OData $orderby parameter
        odata_skip: OData $skip parameter
        client: Optional WATS client instance
        
    Returns:
        List of asset log records
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if odata_filter:
        params["$filter"] = odata_filter
    if odata_top is not None:
        params["$top"] = odata_top
    if odata_orderby:
        params["$orderby"] = odata_orderby
    if odata_skip is not None:
        params["$skip"] = odata_skip
    
    response = client.get("/api/Asset/Log", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def maintenance_asset(
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    date_time: Optional[datetime] = None,
    comment: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Inform that an asset has had maintenance.
    
    Args:
        asset_id: Asset ID
        serial_number: Asset serial number
        date_time: Maintenance date (default: now)
        comment: Asset log message
        client: Optional WATS client instance
        
    Returns:
        Maintenance result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    if date_time:
        params["dateTime"] = date_time.isoformat()
    if comment:
        params["comment"] = comment
    
    response = client.post("/api/Asset/Maintenance", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def post_asset_message(
    message: AssetMessage,
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    culture_code: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Post a message/comment to the asset log.
    
    Args:
        message: Asset message
        asset_id: Asset ID
        serial_number: Asset serial number
        culture_code: Culture code for error message translations
        client: Optional WATS client instance
        
    Returns:
        Message post result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    if culture_code:
        params["cultureCode"] = culture_code
    
    response = client.post(
        "/api/Asset/Message",
        json=message.dict(exclude_none=True, by_alias=True),
        params=params
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def reset_asset_running_count(
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    comment: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Reset running count to 0.
    
    Args:
        asset_id: Asset ID
        serial_number: Asset serial number
        comment: Asset log message
        client: Optional WATS client instance
        
    Returns:
        Reset result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    if comment:
        params["comment"] = comment
    
    response = client.post("/api/Asset/ResetRunningCount", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def set_asset_state(
    state: AssetState,
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Set the state of an asset.
    
    Args:
        state: Asset state (0=Unknown, 1=In Operation, 2=In Transit, etc.)
        asset_id: Asset ID
        serial_number: Asset serial number
        client: Optional WATS client instance
        
    Returns:
        State update result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"state": state.value}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    
    response = client.put("/api/Asset/State", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_asset_status(
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    translate: Optional[bool] = None,
    culture_code: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get the current status for an asset.
    
    Args:
        asset_id: Asset ID
        serial_number: Asset serial number
        translate: Use translations (defaults to true)
        culture_code: Culture code for translations
        client: Optional WATS client instance
        
    Returns:
        Asset status data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    if translate is not None:
        params["translate"] = translate
    if culture_code:
        params["cultureCode"] = culture_code
    
    response = client.get("/api/Asset/Status", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_asset_children(
    asset_id: Optional[str] = None,
    serial_number: Optional[str] = None,
    level: Optional[int] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Return a list of sub assets/children of the specified asset.
    
    Args:
        asset_id: Asset ID
        serial_number: Asset Serial Number
        level: How many sub assets of sub assets to get (0=all, 1=direct children)
        client: Optional WATS client instance
        
    Returns:
        Sub assets data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if asset_id:
        params["id"] = asset_id
    if serial_number:
        params["serialNumber"] = serial_number
    if level is not None:
        params["level"] = level
    
    response = client.get("/api/Asset/SubAssets", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_asset_types(
    odata_filter: Optional[str] = None,
    odata_top: Optional[int] = None,
    odata_orderby: Optional[str] = None,
    odata_skip: Optional[int] = None,
    client: Optional[WATSClient] = None
) -> List[Dict[str, Any]]:
    """
    Get a list of asset types matching the specified filter.
    
    Supports OData query options. Returns top 1000 types unless $top is specified.
    Results are ordered by name unless $orderby is specified.
    
    Args:
        odata_filter: OData $filter parameter
        odata_top: OData $top parameter
        odata_orderby: OData $orderby parameter
        odata_skip: OData $skip parameter
        client: Optional WATS client instance
        
    Returns:
        List of asset types
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if odata_filter:
        params["$filter"] = odata_filter
    if odata_top is not None:
        params["$top"] = odata_top
    if odata_orderby:
        params["$orderby"] = odata_orderby
    if odata_skip is not None:
        params["$skip"] = odata_skip
    
    response = client.get("/api/Asset/Types", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def create_asset_type(
    asset_type: AssetType,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Create or update an asset type.
    
    Args:
        asset_type: Asset type to create or update
        client: Optional WATS client instance
        
    Returns:
        Created/updated asset type data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.put(
        "/api/Asset/Types",
        json=asset_type.dict(exclude_none=True, by_alias=True)
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()