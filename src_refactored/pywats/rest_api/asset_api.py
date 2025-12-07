"""
Asset API Endpoints

Provides all REST API calls for asset management.

Public API Endpoints (from Swagger):
- DELETE /api/Asset - Delete asset by identifier
- GET /api/Asset - List assets with filter
- PUT /api/Asset - Create or update asset
- GET /api/Asset/{assetId} - Get asset by ID
- GET /api/Asset/{serialNumber} - Get asset by serial number
- POST /api/Asset/Calibration - Record calibration
- PUT /api/Asset/Count - Update count
- GET /api/Asset/Log - Get asset log
- POST /api/Asset/Maintenance - Record maintenance
- POST /api/Asset/Message - Post message to log
- POST /api/Asset/ResetRunningCount - Reset running count
- PUT /api/Asset/State - Set asset state
- GET /api/Asset/Status - Get asset status
- GET /api/Asset/SubAssets - Get child assets
- GET /api/Asset/Types - List asset types
- PUT /api/Asset/Types - Create/update asset type
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient, Response


class AssetApi:
    """
    Asset API endpoints.
    
    Endpoints for managing assets (electronic instruments) including
    calibration, maintenance, and status tracking.
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Asset CRUD
    # =========================================================================
    
    def get_assets(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> 'Response':
        """
        Get all assets with optional OData filtering.
        
        GET /api/Asset
        
        Args:
            filter_str: OData filter string
            orderby: Order by clause
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            Response with list of assets
        """
        params: Dict[str, Any] = {}
        if filter_str:
            params["$filter"] = filter_str
        if orderby:
            params["$orderby"] = orderby
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        
        return self._http.get("/api/Asset", params=params if params else None)
    
    def get_asset_by_id(self, asset_id: str) -> 'Response':
        """
        Get an asset by its ID.
        
        GET /api/Asset/{assetId}
        
        Args:
            asset_id: The asset ID (GUID)
            
        Returns:
            Response with asset data
        """
        return self._http.get(f"/api/Asset/{asset_id}")
    
    def get_asset_by_serial_number(self, serial_number: str) -> 'Response':
        """
        Get an asset by its serial number.
        
        GET /api/Asset/{serialNumber}
        
        Args:
            serial_number: The asset serial number
            
        Returns:
            Response with asset data
        """
        return self._http.get(f"/api/Asset/{serial_number}")
    
    def create_or_update_asset(self, asset_data: Dict[str, Any]) -> 'Response':
        """
        Create a new asset or update an existing one.
        
        PUT /api/Asset
        
        Note: Properties 'runningCount' and 'totalCount' must be updated 
        using api/Asset/Count. Properties 'lastCalibrationDate' and 
        'lastMaintenanceDate' must be updated using api/Asset/Calibration.
        The 'assetId' can be left empty. The 'typeId' must be specified.
        
        Args:
            asset_data: Asset data dictionary
            
        Returns:
            Response with created/updated asset
        """
        return self._http.put("/api/Asset", data=asset_data)
    
    def delete_asset(self, asset_id: str) -> 'Response':
        """
        Delete an asset.
        
        DELETE /api/Asset
        
        Note: Log records for the asset will also be deleted.
        Any assets which have this asset as parent will not be deleted,
        but will change parent.
        
        Args:
            asset_id: The asset ID to delete (passed as query param)
            
        Returns:
            Response with deletion result
        """
        return self._http.delete("/api/Asset", params={"assetId": asset_id})
    
    # =========================================================================
    # Asset Status and State
    # =========================================================================
    
    def get_asset_status(self, asset_id: str) -> 'Response':
        """
        Get the current status of an asset.
        
        GET /api/Asset/Status
        
        Args:
            asset_id: The asset ID (query parameter)
            
        Returns:
            Response with asset status
        """
        return self._http.get("/api/Asset/Status", params={"assetId": asset_id})
    
    def set_asset_state(
        self,
        asset_id: str,
        state: int,
        comment: Optional[str] = None
    ) -> 'Response':
        """
        Set the state of an asset (e.g. "In Operation").
        
        PUT /api/Asset/State
        
        Args:
            asset_id: The asset ID
            state: The new state value
            comment: Optional comment
            
        Returns:
            Response with result
        """
        params: Dict[str, Any] = {"assetId": asset_id, "state": state}
        if comment:
            params["comment"] = comment
        return self._http.put("/api/Asset/State", params=params)
    
    # =========================================================================
    # Asset Count
    # =========================================================================
    
    def update_asset_count(
        self,
        asset_id: str,
        total_count: Optional[int] = None,
        increment_by: Optional[int] = None
    ) -> 'Response':
        """
        Increment the running and total count on an asset.
        
        PUT /api/Asset/Count
        
        Use 'totalCount' or 'incrementBy' query parameters to increment
        the running count and total count.
        
        Args:
            asset_id: The asset ID
            total_count: Set total count to this value
            increment_by: Increment count by this value
            
        Returns:
            Response with result
        """
        params: Dict[str, Any] = {"assetId": asset_id}
        if total_count is not None:
            params["totalCount"] = total_count
        if increment_by is not None:
            params["incrementBy"] = increment_by
        return self._http.put("/api/Asset/Count", params=params)
    
    def reset_running_count(self, asset_id: str) -> 'Response':
        """
        Reset the running count to 0.
        
        POST /api/Asset/ResetRunningCount
        
        Args:
            asset_id: The asset ID
            
        Returns:
            Response with result
        """
        return self._http.post("/api/Asset/ResetRunningCount", params={"assetId": asset_id})
    
    # =========================================================================
    # Calibration
    # =========================================================================
    
    def post_calibration(self, calibration_data: Dict[str, Any]) -> 'Response':
        """
        Inform that an asset has been calibrated.
        
        POST /api/Asset/Calibration
        
        Args:
            calibration_data: Calibration data dictionary
            
        Returns:
            Response with result
        """
        return self._http.post("/api/Asset/Calibration", data=calibration_data)
    
    # =========================================================================
    # Maintenance
    # =========================================================================
    
    def post_maintenance(self, maintenance_data: Dict[str, Any]) -> 'Response':
        """
        Inform that an asset has had maintenance.
        
        POST /api/Asset/Maintenance
        
        Args:
            maintenance_data: Maintenance data dictionary
            
        Returns:
            Response with result
        """
        return self._http.post("/api/Asset/Maintenance", data=maintenance_data)
    
    # =========================================================================
    # Asset Log and Messages
    # =========================================================================
    
    def get_asset_log(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> 'Response':
        """
        Get asset log records matching the specified filter.
        
        GET /api/Asset/Log
        
        Args:
            filter_str: OData filter string
            orderby: Order by clause
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            Response with log entries
        """
        params: Dict[str, Any] = {}
        if filter_str:
            params["$filter"] = filter_str
        if orderby:
            params["$orderby"] = orderby
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        return self._http.get("/api/Asset/Log", params=params if params else None)
    
    def post_message(self, message_data: Dict[str, Any]) -> 'Response':
        """
        Post a message/comment to the asset log.
        
        POST /api/Asset/Message
        
        Args:
            message_data: Message data dictionary
            
        Returns:
            Response with result
        """
        return self._http.post("/api/Asset/Message", data=message_data)
    
    # =========================================================================
    # Asset Types
    # =========================================================================
    
    def get_asset_types(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> 'Response':
        """
        Get all asset types matching the specified filter.
        
        GET /api/Asset/Types
        
        Args:
            filter_str: OData filter string
            orderby: Order by clause  
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            Response with list of asset types
        """
        params: Dict[str, Any] = {}
        if filter_str:
            params["$filter"] = filter_str
        if orderby:
            params["$orderby"] = orderby
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        return self._http.get("/api/Asset/Types", params=params if params else None)
    
    def create_or_update_asset_type(self, type_data: Dict[str, Any]) -> 'Response':
        """
        Create or update an asset type.
        
        PUT /api/Asset/Types
        
        Args:
            type_data: Asset type data dictionary
            
        Returns:
            Response with asset type
        """
        return self._http.put("/api/Asset/Types", data=type_data)
    
    # =========================================================================
    # Asset Hierarchy
    # =========================================================================
    
    def get_sub_assets(self, asset_id: str) -> 'Response':
        """
        Return a list of sub assets/children of the specified asset.
        
        GET /api/Asset/SubAssets
        
        Args:
            asset_id: The parent asset ID
            
        Returns:
            Response with child assets
        """
        return self._http.get("/api/Asset/SubAssets", params={"assetId": asset_id})
