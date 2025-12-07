"""
Asset API Endpoints

Provides all REST API calls for asset management.
All methods return typed model objects instead of raw responses.

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

from typing import Optional, List, Dict, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..models import Asset, AssetType, AssetLog, AssetState


class AssetApi:
    """
    Asset API endpoints.
    
    Endpoints for managing assets (electronic instruments) including
    calibration, maintenance, and status tracking.
    All methods return typed model objects.
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
    ) -> List[Asset]:
        """
        Get all assets with optional OData filtering.
        
        GET /api/Asset
        
        Args:
            filter_str: OData filter string
            orderby: Order by clause
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            List of Asset objects
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
        
        response = self._http.get("/api/Asset", params=params if params else None)
        if response.is_success and response.data:
            return [Asset.model_validate(item) for item in response.data]
        return []
    
    def get_asset_by_id(self, asset_id: str) -> Optional[Asset]:
        """
        Get an asset by its ID.
        
        GET /api/Asset/{assetId}
        
        Args:
            asset_id: The asset ID (GUID)
            
        Returns:
            Asset object or None if not found
        """
        response = self._http.get(f"/api/Asset/{asset_id}")
        if response.is_success and response.data:
            return Asset.model_validate(response.data)
        return None
    
    def get_asset_by_serial_number(self, serial_number: str) -> Optional[Asset]:
        """
        Get an asset by its serial number.
        
        GET /api/Asset/{serialNumber}
        
        Args:
            serial_number: The asset serial number
            
        Returns:
            Asset object or None if not found
        """
        response = self._http.get(f"/api/Asset/{serial_number}")
        if response.is_success and response.data:
            return Asset.model_validate(response.data)
        return None
    
    def create_or_update_asset(self, asset: Union[Asset, Dict[str, Any]]) -> Optional[Asset]:
        """
        Create a new asset or update an existing one.
        
        PUT /api/Asset
        
        Note: Properties 'runningCount' and 'totalCount' must be updated 
        using api/Asset/Count. Properties 'lastCalibrationDate' and 
        'lastMaintenanceDate' must be updated using api/Asset/Calibration.
        The 'assetId' can be left empty. The 'typeId' must be specified.
        
        Args:
            asset: Asset object or data dictionary
            
        Returns:
            Created/updated Asset object
        """
        if isinstance(asset, Asset):
            data = asset.model_dump(by_alias=True, exclude_none=True)
        else:
            data = asset
        response = self._http.put("/api/Asset", data=data)
        if response.is_success and response.data:
            return Asset.model_validate(response.data)
        return None
    
    def delete_asset(self, asset_id: str) -> bool:
        """
        Delete an asset.
        
        DELETE /api/Asset
        
        Note: Log records for the asset will also be deleted.
        Any assets which have this asset as parent will not be deleted,
        but will change parent.
        
        Args:
            asset_id: The asset ID to delete (passed as query param)
            
        Returns:
            True if successful
        """
        response = self._http.delete("/api/Asset", params={"assetId": asset_id})
        return response.is_success
    
    # =========================================================================
    # Asset Status and State
    # =========================================================================
    
    def get_asset_status(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current status of an asset.
        
        GET /api/Asset/Status
        
        Args:
            asset_id: The asset ID (query parameter)
            
        Returns:
            Asset status data or None
        """
        response = self._http.get("/api/Asset/Status", params={"assetId": asset_id})
        if response.is_success and response.data:
            return response.data
        return None
    
    def set_asset_state(
        self,
        asset_id: str,
        state: Union[AssetState, int],
        comment: Optional[str] = None
    ) -> bool:
        """
        Set the state of an asset (e.g. "In Operation").
        
        PUT /api/Asset/State
        
        Args:
            asset_id: The asset ID
            state: The new state value (AssetState enum or int)
            comment: Optional comment
            
        Returns:
            True if successful
        """
        state_value = state.value if isinstance(state, AssetState) else state
        params: Dict[str, Any] = {"assetId": asset_id, "state": state_value}
        if comment:
            params["comment"] = comment
        response = self._http.put("/api/Asset/State", params=params)
        return response.is_success
    
    # =========================================================================
    # Asset Count
    # =========================================================================
    
    def update_asset_count(
        self,
        asset_id: str,
        total_count: Optional[int] = None,
        increment_by: Optional[int] = None
    ) -> bool:
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
            True if successful
        """
        params: Dict[str, Any] = {"assetId": asset_id}
        if total_count is not None:
            params["totalCount"] = total_count
        if increment_by is not None:
            params["incrementBy"] = increment_by
        response = self._http.put("/api/Asset/Count", params=params)
        return response.is_success
    
    def reset_running_count(self, asset_id: str) -> bool:
        """
        Reset the running count to 0.
        
        POST /api/Asset/ResetRunningCount
        
        Args:
            asset_id: The asset ID
            
        Returns:
            True if successful
        """
        response = self._http.post("/api/Asset/ResetRunningCount", params={"assetId": asset_id})
        return response.is_success
    
    # =========================================================================
    # Calibration
    # =========================================================================
    
    def post_calibration(self, calibration_data: Dict[str, Any]) -> bool:
        """
        Inform that an asset has been calibrated.
        
        POST /api/Asset/Calibration
        
        Args:
            calibration_data: Calibration data dictionary
            
        Returns:
            True if successful
        """
        response = self._http.post("/api/Asset/Calibration", data=calibration_data)
        return response.is_success
    
    # =========================================================================
    # Maintenance
    # =========================================================================
    
    def post_maintenance(self, maintenance_data: Dict[str, Any]) -> bool:
        """
        Inform that an asset has had maintenance.
        
        POST /api/Asset/Maintenance
        
        Args:
            maintenance_data: Maintenance data dictionary
            
        Returns:
            True if successful
        """
        response = self._http.post("/api/Asset/Maintenance", data=maintenance_data)
        return response.is_success
    
    # =========================================================================
    # Asset Log and Messages
    # =========================================================================
    
    def get_asset_log(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[AssetLog]:
        """
        Get asset log records matching the specified filter.
        
        GET /api/Asset/Log
        
        Args:
            filter_str: OData filter string
            orderby: Order by clause
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            List of AssetLog objects
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
        response = self._http.get("/api/Asset/Log", params=params if params else None)
        if response.is_success and response.data:
            return [AssetLog.model_validate(item) for item in response.data]
        return []
    
    def post_message(self, message_data: Dict[str, Any]) -> bool:
        """
        Post a message/comment to the asset log.
        
        POST /api/Asset/Message
        
        Args:
            message_data: Message data dictionary
            
        Returns:
            True if successful
        """
        response = self._http.post("/api/Asset/Message", data=message_data)
        return response.is_success
    
    # =========================================================================
    # Asset Types
    # =========================================================================
    
    def get_asset_types(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[AssetType]:
        """
        Get all asset types matching the specified filter.
        
        GET /api/Asset/Types
        
        Args:
            filter_str: OData filter string
            orderby: Order by clause  
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            List of AssetType objects
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
        response = self._http.get("/api/Asset/Types", params=params if params else None)
        if response.is_success and response.data:
            return [AssetType.model_validate(item) for item in response.data]
        return []
    
    def create_or_update_asset_type(
        self, asset_type: Union[AssetType, Dict[str, Any]]
    ) -> Optional[AssetType]:
        """
        Create or update an asset type.
        
        PUT /api/Asset/Types
        
        Args:
            asset_type: AssetType object or data dictionary
            
        Returns:
            Created/updated AssetType object
        """
        if isinstance(asset_type, AssetType):
            data = asset_type.model_dump(by_alias=True, exclude_none=True)
        else:
            data = asset_type
        response = self._http.put("/api/Asset/Types", data=data)
        if response.is_success and response.data:
            return AssetType.model_validate(response.data)
        return None
    
    # =========================================================================
    # Asset Hierarchy
    # =========================================================================
    
    def get_sub_assets(self, asset_id: str) -> List[Asset]:
        """
        Return a list of sub assets/children of the specified asset.
        
        GET /api/Asset/SubAssets
        
        Args:
            asset_id: The parent asset ID
            
        Returns:
            List of child Asset objects
        """
        response = self._http.get("/api/Asset/SubAssets", params={"assetId": asset_id})
        if response.is_success and response.data:
            return [Asset.model_validate(item) for item in response.data]
        return []
