"""Asset repository - data access layer.

Handles all API calls for asset management.
"""
from typing import Optional, List, Dict, Any, Union, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from ...core.client import HttpClient
    from ...core.exceptions import ErrorHandler

from .models import Asset, AssetType, AssetLog
from .enums import AssetState


class AssetRepository:
    """
    Asset data access layer.

    Handles all HTTP API calls for asset CRUD operations.
    """

    def __init__(
        self, 
        http_client: "HttpClient",
        error_handler: Optional["ErrorHandler"] = None
    ):
        """
        Initialize with HTTP client.

        Args:`n            http_client: HttpClient instance for making requests
            error_handler: Optional ErrorHandler for error handling (default: STRICT mode)
        """
        self._http_client = http_client
        # Import here to avoid circular imports
        from ...core.exceptions import ErrorHandler, ErrorMode
        self._error_handler = error_handler or ErrorHandler(ErrorMode.STRICT)

    # =========================================================================
    # Asset CRUD
    # =========================================================================

    def get_all(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[Asset]:
        """
        Get all assets with optional OData filtering.

        GET /api/Asset
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

        response = self._http_client.get(
            "/api/Asset",
            params=params if params else None
        )
        if response.is_success and response.data:
            return [Asset.model_validate(item) for item in response.data]
        return []

    def get_by_id(self, asset_id: str) -> Optional[Asset]:
        """
        Get an asset by its ID.

        GET /api/Asset/{assetId}
        """
        response = self._http_client.get(f"/api/Asset/{asset_id}")
        if response.is_success and response.data:
            return Asset.model_validate(response.data)
        return None

    def get_by_serial_number(self, serial_number: str) -> Optional[Asset]:
        """
        Get an asset by its serial number.

        GET /api/Asset/{serialNumber}
        """
        response = self._http_client.get(f"/api/Asset/{serial_number}")
        if response.is_success and response.data:
            return Asset.model_validate(response.data)
        return None

    def save(self, asset: Union[Asset, Dict[str, Any]]) -> Optional[Asset]:
        """
        Create a new asset or update an existing one.

        PUT /api/Asset
        """
        if isinstance(asset, Asset):
            data = asset.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            data = asset
        response = self._http_client.put("/api/Asset", data=data)
        if response.is_success and response.data:
            return Asset.model_validate(response.data)
        return None

    def delete(self, asset_id: str) -> bool:
        """
        Delete an asset.

        DELETE /api/Asset
        """
        response = self._http_client.delete(
            "/api/Asset",
            params={"assetId": asset_id}
        )
        return response.is_success

    # =========================================================================
    # Asset Status and State
    # =========================================================================

    def get_status(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the current status of an asset.

        GET /api/Asset/Status
        """
        response = self._http_client.get(
            "/api/Asset/Status",
            params={"assetId": asset_id}
        )
        if response.is_success and response.data:
            return cast(Dict[str, Any], response.data)
        return None

    def set_state(
        self,
        asset_id: str,
        state: Union[AssetState, int],
        comment: Optional[str] = None
    ) -> bool:
        """
        Set the state of an asset.

        PUT /api/Asset/State
        """
        state_value = state.value if isinstance(state, AssetState) else state
        params: Dict[str, Any] = {"assetId": asset_id, "state": state_value}
        if comment:
            params["comment"] = comment
        response = self._http_client.put("/api/Asset/State", params=params)
        return response.is_success

    # =========================================================================
    # Asset Count
    # =========================================================================

    def update_count(
        self,
        asset_id: str,
        total_count: Optional[int] = None,
        increment_by: Optional[int] = None
    ) -> bool:
        """
        Increment the running and total count on an asset.

        PUT /api/Asset/Count
        """
        params: Dict[str, Any] = {"assetId": asset_id}
        if total_count is not None:
            params["totalCount"] = total_count
        if increment_by is not None:
            params["incrementBy"] = increment_by
        response = self._http_client.put("/api/Asset/Count", params=params)
        return response.is_success

    def reset_running_count(self, asset_id: str) -> bool:
        """
        Reset the running count to 0.

        POST /api/Asset/ResetRunningCount
        """
        response = self._http_client.post(
            "/api/Asset/ResetRunningCount",
            params={"assetId": asset_id}
        )
        return response.is_success

    # =========================================================================
    # Calibration
    # =========================================================================

    def post_calibration(self, calibration_data: Dict[str, Any]) -> bool:
        """
        Inform that an asset has been calibrated.

        POST /api/Asset/Calibration
        """
        response = self._http_client.post(
            "/api/Asset/Calibration",
            data=calibration_data
        )
        return response.is_success

    # =========================================================================
    # Maintenance
    # =========================================================================

    def post_maintenance(self, maintenance_data: Dict[str, Any]) -> bool:
        """
        Inform that an asset has had maintenance.

        POST /api/Asset/Maintenance
        """
        response = self._http_client.post(
            "/api/Asset/Maintenance",
            data=maintenance_data
        )
        return response.is_success

    # =========================================================================
    # Asset Log
    # =========================================================================

    def get_log(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[AssetLog]:
        """
        Get asset log records.

        GET /api/Asset/Log
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
        response = self._http_client.get(
            "/api/Asset/Log",
            params=params if params else None
        )
        if response.is_success and response.data:
            return [AssetLog.model_validate(item) for item in response.data]
        return []

    def post_message(
        self,
        asset_id: str,
        message: str,
        user: Optional[str] = None
    ) -> bool:
        """
        Post a message to the asset log.

        POST /api/Asset/Message
        """
        data: Dict[str, Any] = {"assetId": asset_id, "comment": message}
        if user:
            data["user"] = user
        response = self._http_client.post("/api/Asset/Message", data=data)
        return response.is_success

    # =========================================================================
    # Asset Types
    # =========================================================================

    def get_types(
        self,
        filter_str: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[AssetType]:
        """
        Get all asset types.

        GET /api/Asset/Types
        """
        params: Dict[str, Any] = {}
        if filter_str:
            params["$filter"] = filter_str
        if top:
            params["$top"] = top
        response = self._http_client.get(
            "/api/Asset/Types",
            params=params if params else None
        )
        if response.is_success and response.data:
            return [AssetType.model_validate(item) for item in response.data]
        return []

    def save_type(
        self,
        asset_type: Union[AssetType, Dict[str, Any]]
    ) -> Optional[AssetType]:
        """
        Create or update an asset type.

        PUT /api/Asset/Types
        """
        if isinstance(asset_type, AssetType):
            data = asset_type.model_dump(by_alias=True, exclude_none=True)
        else:
            data = asset_type
        response = self._http_client.put("/api/Asset/Types", data=data)
        if response.is_success and response.data:
            return AssetType.model_validate(response.data)
        return None

    # =========================================================================
    # Sub-Assets
    # =========================================================================

    def get_sub_assets(self, parent_id: str) -> List[Asset]:
        """
        Get child assets of a parent asset.

        GET /api/Asset/SubAssets
        """
        response = self._http_client.get(
            "/api/Asset/SubAssets",
            params={"parentId": parent_id}
        )
        if response.is_success and response.data:
            return [Asset.model_validate(item) for item in response.data]
        return []
