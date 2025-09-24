"""
MES Asset Module

Manages test equipment, fixtures, and other assets.
This module mirrors the Interface.MES Asset functionality.
"""

from typing import Optional, List, Union
from datetime import datetime

from .base import MESBase
from .models import AssetResponse
from ..rest_api.client import WATSClient
from ..rest_api.models.asset import Asset, AssetType, AssetLog
from ..connection import WATSConnection


class AssetHandler(MESBase):
    """
    Asset management for WATS MES.
    
    Provides functionality for:
    - Asset creation and management
    - Asset type management
    - Asset relationships (parent/child)
    - Usage count tracking
    - Calibration and maintenance records
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize Asset module.
        
        Args:
            connection: WATS connection or client instance
        """
        super().__init__(connection)
    
    def is_connected(self) -> bool:
        """
        Check if connected to WATS MES Server.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            response = self._client.get("/api/internal/mes/isConnected")
            return response.status_code == 200
        except Exception:
            return False
    
    def create_asset(
        self,
        serial_number: str,
        asset_type: str,
        parent_asset_serial_number: Optional[str] = None,
        asset_name: Optional[str] = None,
        asset_description: Optional[str] = None
    ) -> AssetResponse:
        """
        Create a new asset in the system.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Asset serial number
            asset_type: Asset type name
            parent_asset_serial_number: Optional parent asset serial number
            asset_name: Optional asset name
            asset_description: Optional asset description
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "assetType": asset_type,
            "assetName": asset_name,
            "description": asset_description
        }
        
        if parent_asset_serial_number:
            data["parentAssetSerialNumber"] = parent_asset_serial_number
        
        try:
            response = self._rest_post_json(
                "/api/internal/Asset/CreateAsset",
                data,
                response_type=AssetResponse
            )
            return response if isinstance(response, AssetResponse) else AssetResponse.model_validate(response)
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to create asset: {str(e)}"
            )
    
    def create_asset_type(
        self,
        name: str,
        calibration_interval: Optional[float] = None,
        maintenance_interval: Optional[float] = None,
        running_count_limit: Optional[int] = None,
        total_count_limit: Optional[int] = None,
        warning_threshold: Optional[float] = None,
        alarm_threshold: Optional[float] = None
    ) -> AssetResponse:
        """
        Create a new asset type.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            name: Asset type name
            calibration_interval: Calibration interval in days
            maintenance_interval: Maintenance interval in days
            running_count_limit: Running count limit
            total_count_limit: Total count limit
            warning_threshold: Warning threshold
            alarm_threshold: Alarm threshold
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {"name": name}
        
        if calibration_interval is not None:
            data["calibrationInterval"] = str(calibration_interval)
        if maintenance_interval is not None:
            data["maintenanceInterval"] = str(maintenance_interval)
        if running_count_limit is not None:
            data["runningCountLimit"] = str(running_count_limit)
        if total_count_limit is not None:
            data["totalCountLimit"] = str(total_count_limit)
        if warning_threshold is not None:
            data["warningThreshold"] = str(warning_threshold)
        if alarm_threshold is not None:
            data["alarmThreshold"] = str(alarm_threshold)
        
        try:
            response = self._rest_post_json(
                "/api/internal/Asset/CreateAssetType",
                data,
                response_type=AssetResponse
            )
            return response if isinstance(response, AssetResponse) else AssetResponse.model_validate(response)
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to create asset type: {str(e)}"
            )
    
    def get_asset(self, serial_number: str) -> Optional[Asset]:
        """
        Retrieve an asset by serial number.
        
        Uses the public REST API endpoint.
        
        Args:
            serial_number: Asset serial number
            
        Returns:
            Asset object or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.asset import get_asset_by_serial_number
        
        try:
            asset_data = get_asset_by_serial_number(serial_number, client=self._client)
            return Asset.model_validate(asset_data) if asset_data else None
        except Exception:
            return None
    
    def update_asset(self, asset: Asset) -> AssetResponse:
        """
        Update an existing asset.
        
        Uses the public REST API endpoint.
        
        Args:
            asset: Asset object with updated information
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.asset import create_asset
        
        try:
            updated_asset = create_asset(asset, client=self._client)
            return AssetResponse(
                success=True,
                message="Asset updated successfully",
                assetId=updated_asset.get("assetId")
            )
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to update asset: {str(e)}"
            )
    
    def set_parent(
        self, 
        serial_number: str, 
        parent_serial_number: str
    ) -> AssetResponse:
        """
        Set parent-child relationship between assets.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Child asset serial number
            parent_serial_number: Parent asset serial number
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "parentSerialNumber": parent_serial_number
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Asset/SetParent",
                data,
                response_type=AssetResponse
            )
            return response if isinstance(response, AssetResponse) else AssetResponse.model_validate(response)
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to set parent: {str(e)}"
            )
    
    def increment_asset_usage_count(
        self,
        serial_number: str,
        usage_count: int = 1,
        increment_sub_assets: bool = False
    ) -> AssetResponse:
        """
        Increment usage count for an asset.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Asset serial number
            usage_count: Count to increment by (default: 1)
            increment_sub_assets: Also increment sub-assets
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "usageCount": usage_count,
            "incrementSubAssets": increment_sub_assets
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Asset/IncrementAssetUsageCount",
                data,
                response_type=AssetResponse
            )
            return response if isinstance(response, AssetResponse) else AssetResponse.model_validate(response)
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to increment usage count: {str(e)}"
            )
    
    def get_assets(self, filter_text: str) -> List[Asset]:
        """
        Get assets matching filter criteria.
        
        Uses the public REST API endpoint with OData filtering.
        
        Args:
            filter_text: OData filter string
            
        Returns:
            List of Asset objects matching criteria
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.asset import get_assets
        
        assets_data = get_assets(odata_filter=filter_text, client=self._client)
        return [Asset.model_validate(asset) for asset in assets_data]
    
    def get_assets_by_tag(self, tag: str) -> List[Asset]:
        """
        Get assets by tag value.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            tag: Tag value to search for
            
        Returns:
            List of Asset objects with matching tag
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {"tag": tag}
        
        response = self._rest_get_json("/api/internal/Asset/GetAssetsByTag")
        assets_data = response.get("assets", [])
        
        return [Asset.parse_obj(item) for item in assets_data]
    
    def get_sub_assets(
        self, 
        serial_number: str, 
        level: Optional[int] = None
    ) -> List[Asset]:
        """
        Get sub-assets of a parent asset.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Parent asset serial number
            level: Optional depth level
            
        Returns:
            List of sub-Asset objects
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {"serialNumber": serial_number}
        if level is not None:
            params["level"] = str(level)
        
        response = self._rest_get_json("/api/internal/Asset/GetSubAssets")
        assets_data = response.get("subAssets", [])
        
        return [Asset.model_validate(item) for item in assets_data]
    
    def calibration(
        self,
        serial_number: str,
        date_time: Optional[datetime] = None,
        comment: Optional[str] = None
    ) -> AssetResponse:
        """
        Record calibration event for asset.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Asset serial number
            date_time: Calibration date/time (default: now)
            comment: Optional calibration comment
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "dateTime": (date_time or datetime.now()).isoformat(),
            "comment": comment
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Asset/Calibration",
                data,
                response_type=AssetResponse
            )
            # When response_type is provided, _rest_post_json returns that type
            return response if isinstance(response, AssetResponse) else AssetResponse.model_validate(response)
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to record calibration: {str(e)}"
            )
    
    def maintenance(
        self,
        serial_number: str,
        date_time: Optional[datetime] = None,
        comment: Optional[str] = None
    ) -> AssetResponse:
        """
        Record maintenance event for asset.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Asset serial number
            date_time: Maintenance date/time (default: now)
            comment: Optional maintenance comment
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "dateTime": (date_time or datetime.now()).isoformat(),
            "comment": comment
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Asset/Maintenance",
                data,
                response_type=AssetResponse
            )
            return response if isinstance(response, AssetResponse) else AssetResponse.model_validate(response)
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to record maintenance: {str(e)}"
            )
    
    def reset_running_count(
        self,
        serial_number: str,
        comment: Optional[str] = None
    ) -> AssetResponse:
        """
        Reset running count for asset.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Asset serial number
            comment: Optional reset comment
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "comment": comment
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Asset/ResetRunningCount",
                data,
                response_type=AssetResponse
            )
            return response if isinstance(response, AssetResponse) else AssetResponse.model_validate(response)
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to reset running count: {str(e)}"
            )
    
    def delete_asset(self, serial_number: str) -> AssetResponse:
        """
        Delete an asset from the system.
        
        Uses the public REST API endpoint.
        
        Args:
            serial_number: Asset serial number
            
        Returns:
            AssetResponse indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.asset import delete_asset
        
        try:
            success = delete_asset(serial_number, client=self._client)
            return AssetResponse(
                success=success,
                message="Asset deleted successfully" if success else "Failed to delete asset"
            )
        except Exception as e:
            return AssetResponse(
                success=False,
                message=f"Failed to delete asset: {str(e)}"
            )