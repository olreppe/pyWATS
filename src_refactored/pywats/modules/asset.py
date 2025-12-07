"""Asset Module for pyWATS

Provides high-level operations for managing assets (test equipment, fixtures, etc.).
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from ..models import Asset, AssetType, AssetLog, AssetState
from ..rest_api import AssetApi

"""
    API INFO / SWAGGER LIST:
    delete /api/Asset
Delete the asset which has the specified identifier.

Log records for the asset will also be deleted.

Any assets which has the asset as parent will not be deleted, but will change parent.

get /api/Asset
Returns a list of assets matching the specified filter.

put /api/Asset
Create or update an asset.

Properties such as 'runningCount' and 'totalCount' must be updated using appropriate API methods (e.g. api/Asset/Count).

Properties such as 'lastCalibrationDate' and 'lastMaintenanceDate' must be updated using appropriate API methods (e.g. api/Asset/Calibration).

The 'assetId' property can be left empty.

The 'typeId' property must be specified. Use the 'typeId' of the desired asset type (see: api/Asset/Types).

get /api/Asset/{assetId}
Get an asset

get /api/Asset/{serialNumber}
Get an asset

post /api/Asset/Calibration
Inform that an asset has been calibrated.

put /api/Asset/Count
Increment the running and total count on an asset.

Use 'totalCount' or 'incrementBy' query parameters to increment the running count and total count.

get /api/Asset/Log
Returns a list of asset log records matching the specified filter.

post /api/Asset/Maintenance
Inform that an asset has had maintenance.

post /api/Asset/Message
Post a message/comment to the asset log.

post /api/Asset/ResetRunningCount
Reset running count to 0.

put /api/Asset/State
Set the state of an asset (e.g. "In Operation").

get /api/Asset/Status
Get the current status for an asset.

get /api/Asset/SubAssets
Return a list of sub assets/children of the specified asset.

get /api/Asset/Types
Returns a list of asset types matching the specified filter.

put /api/Asset/Types

    
    






"""



class AssetModule:
    """
    Asset management module.
    
    Provides operations for:
    - Getting assets and asset types
    - Creating and updating assets
    - Recording calibration and maintenance
    - Managing asset counters and state
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # Get all assets
        assets = api.asset.get_assets()
        
        # Get asset by serial number
        asset = api.asset.get_asset_by_serial("FIXTURE-001")
        
        # Record calibration
        api.asset.record_calibration(asset_id, "John Doe", "Annual calibration")
    """
    
    def __init__(self, api: AssetApi):
        """
        Initialize AssetModule with REST API client.
        
        Args:
            api: AssetApi instance for making HTTP requests
        """
        self._api = api
    
    # -------------------------------------------------------------------------
    # Get Operations
    # -------------------------------------------------------------------------
    
    def get_assets(
        self,
        filter_str: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Asset]:
        """
        Get all assets in the system.
        
        GET /api/Asset
        
        Args:
            filter_str: Optional OData filter string
            top: Optional max number of results
            
        Returns:
            List of Asset objects
        """
        response = self._api.get_assets(filter_str=filter_str, top=top)
        data = response.data if response.data else []
        return [Asset.from_dict(a) for a in data]
    
    def get_asset(self, asset_id: str) -> Optional[Asset]:
        """
        Get an asset by ID or serial number.
        
        GET /api/Asset/{assetId} or GET /api/Asset/{serialNumber}
        
        Args:
            asset_id: The asset ID (GUID) or serial number
            
        Returns:
            Asset object if found, None otherwise
        """
        response = self._api.get_asset_by_id(asset_id)
        return Asset.from_dict(response.data) if response.data else None
    
    def get_asset_by_serial(self, serial_number: str) -> Optional[Asset]:
        """
        Get an asset by serial number.
        
        GET /api/Asset/{serialNumber}
        
        Args:
            serial_number: The asset serial number
            
        Returns:
            Asset object if found, None otherwise
        """
        response = self._api.get_asset_by_serial_number(serial_number)
        return Asset.from_dict(response.data) if response.data else None
    
    def get_asset_types(
        self,
        filter_str: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[AssetType]:
        """
        Get all asset types.
        
        GET /api/Asset/Types
        
        Args:
            filter_str: Optional OData filter string
            top: Optional max number of results
            
        Returns:
            List of AssetType objects
        """
        response = self._api.get_asset_types(filter_str=filter_str, top=top)
        data = response.data if response.data else []
        return [AssetType.from_dict(t) for t in data]
    
    def get_asset_log(
        self,
        filter_str: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[AssetLog]:
        """
        Get asset log entries.
        
        GET /api/Asset/Log
        
        Args:
            filter_str: Optional OData filter string (e.g., "assetId eq 'xxx'")
            top: Optional max number of results
            
        Returns:
            List of AssetLog entries
        """
        response = self._api.get_asset_log(filter_str=filter_str, top=top)
        data = response.data if response.data else []
        return [AssetLog.from_dict(l) for l in data]
    
    def get_asset_status(self, asset_id: str) -> dict:
        """
        Get current status of an asset.
        
        GET /api/Asset/Status
        
        Args:
            asset_id: The asset ID
            
        Returns:
            Status information dictionary
        """
        response = self._api.get_asset_status(asset_id)
        return response.data
    
    def get_sub_assets(self, asset_id: str) -> List[Asset]:
        """
        Get child/sub assets of a parent asset.
        
        GET /api/Asset/SubAssets
        
        Args:
            asset_id: The parent asset ID
            
        Returns:
            List of child Asset objects
        """
        response = self._api.get_sub_assets(asset_id)
        data = response.data if response.data else []
        return [Asset.from_dict(a) for a in data]
    
    # -------------------------------------------------------------------------
    # Create/Update Operations
    # -------------------------------------------------------------------------
    
    def create_or_update_asset(
        self,
        serial_number: str,
        type_id: UUID,
        asset_name: Optional[str] = None,
        part_number: Optional[str] = None,
        revision: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        parent_serial_number: Optional[str] = None,
        asset_id: Optional[str] = None
    ) -> Asset:
        """
        Create a new asset or update an existing one.
        
        PUT /api/Asset
        
        Note: Properties 'runningCount', 'totalCount', 'lastCalibrationDate',
        'lastMaintenanceDate' must be updated using their respective methods.
        The 'assetId' can be left empty for new assets.
        The 'typeId' must be specified.
        
        Args:
            serial_number: Asset serial number (required)
            type_id: Asset type ID (required)
            asset_name: Asset name
            part_number: Part number
            revision: Revision
            description: Description
            location: Location
            parent_serial_number: Parent asset serial number
            asset_id: Asset ID (for updates, optional for creates)
            
        Returns:
            Created/Updated Asset object
        """
        asset = Asset(
            serial_number=serial_number,
            type_id=type_id,
            asset_name=asset_name,
            part_number=part_number,
            revision=revision,
            description=description,
            location=location,
            parent_serial_number=parent_serial_number,
            asset_id=asset_id
        )
        response = self._api.create_or_update_asset(asset.to_dict())
        return Asset.from_dict(response.data)
    
    def create_or_update_asset_type(
        self,
        type_name: str,
        type_id: Optional[str] = None,
        running_count_limit: Optional[int] = None,
        total_count_limit: Optional[int] = None,
        maintenance_interval: Optional[float] = None,
        calibration_interval: Optional[float] = None,
        warning_threshold: Optional[float] = None,
        alarm_threshold: Optional[float] = None
    ) -> AssetType:
        """
        Create or update an asset type.
        
        PUT /api/Asset/Types
        
        Args:
            type_name: Name of the asset type (required)
            type_id: Type ID (for updates)
            running_count_limit: Max count until next calibration
            total_count_limit: Total count limit
            maintenance_interval: Maintenance interval in days
            calibration_interval: Calibration interval in days
            warning_threshold: Warning threshold percentage
            alarm_threshold: Alarm threshold percentage
            
        Returns:
            Created/Updated AssetType object
        """
        asset_type = AssetType(
            type_name=type_name,
            type_id=UUID(type_id) if type_id else None,
            running_count_limit=running_count_limit,
            total_count_limit=total_count_limit,
            maintenance_interval=maintenance_interval,
            calibration_interval=calibration_interval,
            warning_threshold=warning_threshold,
            alarm_threshold=alarm_threshold
        )
        response = self._api.create_or_update_asset_type(asset_type.to_dict())
        return AssetType.from_dict(response.data)
    
    # -------------------------------------------------------------------------
    # State and Count Operations
    # -------------------------------------------------------------------------
    
    def set_state(
        self,
        asset_id: str,
        state: AssetState,
        comment: Optional[str] = None
    ) -> bool:
        """
        Set the state of an asset.
        
        PUT /api/Asset/State
        
        Args:
            asset_id: Asset ID
            state: New asset state
            comment: Optional comment
            
        Returns:
            True if successful
        """
        response = self._api.set_asset_state(asset_id, state.value, comment)
        return response.is_success
    
    def update_count(
        self,
        asset_id: str,
        total_count: Optional[int] = None,
        increment_by: Optional[int] = None
    ) -> bool:
        """
        Increment the running and total count on an asset.
        
        PUT /api/Asset/Count
        
        Args:
            asset_id: Asset ID
            total_count: Set total count to this value
            increment_by: Increment count by this value
            
        Returns:
            True if successful
        """
        response = self._api.update_asset_count(asset_id, total_count, increment_by)
        return response.is_success
    
    def reset_running_count(self, asset_id: str) -> bool:
        """
        Reset asset running count to zero.
        
        POST /api/Asset/ResetRunningCount
        
        Args:
            asset_id: Asset ID
            
        Returns:
            True if successful
        """
        response = self._api.reset_running_count(asset_id)
        return response.is_success
    
    # -------------------------------------------------------------------------
    # Calibration & Maintenance
    # -------------------------------------------------------------------------
    
    def record_calibration(
        self,
        asset_id: str,
        user: str,
        comment: Optional[str] = None,
        calibration_date: Optional[datetime] = None
    ) -> bool:
        """
        Record a calibration event for an asset.
        
        POST /api/Asset/Calibration
        
        Args:
            asset_id: Asset ID
            user: User performing the calibration
            comment: Calibration notes
            calibration_date: Date of calibration (default: now)
            
        Returns:
            True if successful
        """
        data = {
            "assetId": asset_id,
            "user": user
        }
        if comment:
            data["comment"] = comment
        if calibration_date:
            data["date"] = calibration_date.isoformat()
            
        response = self._api.post_calibration(data)
        return response.is_success
    
    def record_maintenance(
        self,
        asset_id: str,
        user: str,
        comment: Optional[str] = None,
        maintenance_date: Optional[datetime] = None
    ) -> bool:
        """
        Record a maintenance event for an asset.
        
        POST /api/Asset/Maintenance
        
        Args:
            asset_id: Asset ID
            user: User performing the maintenance
            comment: Maintenance notes
            maintenance_date: Date of maintenance (default: now)
            
        Returns:
            True if successful
        """
        data = {
            "assetId": asset_id,
            "user": user
        }
        if comment:
            data["comment"] = comment
        if maintenance_date:
            data["date"] = maintenance_date.isoformat()
            
        response = self._api.post_maintenance(data)
        return response.is_success
    
    def post_message(
        self,
        asset_id: str,
        message: str,
        user: Optional[str] = None
    ) -> bool:
        """
        Post a message/comment to the asset log.
        
        POST /api/Asset/Message
        
        Args:
            asset_id: Asset ID
            message: Message text
            user: Optional user name
            
        Returns:
            True if successful
        """
        data = {
            "assetId": asset_id,
            "message": message
        }
        if user:
            data["user"] = user
            
        response = self._api.post_message(data)
        return response.is_success
    
    # -------------------------------------------------------------------------
    # Delete Operations
    # -------------------------------------------------------------------------
    
    def delete_asset(self, asset_id: str) -> bool:
        """
        Delete an asset.
        
        DELETE /api/Asset
        
        Note: Log records for the asset will also be deleted.
        Any assets with this asset as parent will not be deleted,
        but will change parent.
        
        Args:
            asset_id: Asset ID
            
        Returns:
            True if deletion was successful
        """
        response = self._api.delete_asset(asset_id)
        return response.is_success
    
    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------
    
    def exists(self, serial_number: str) -> bool:
        """
        Check if an asset exists.
        
        Args:
            serial_number: Asset serial number
            
        Returns:
            True if asset exists, False otherwise
        """
        try:
            return self.get_asset_by_serial(serial_number) is not None
        except Exception:
            return False
    
    def needs_calibration(self, serial_number: str) -> bool:
        """
        Check if an asset needs calibration.
        
        Args:
            serial_number: Asset serial number
            
        Returns:
            True if asset needs calibration
        """
        asset = self.get_asset_by_serial(serial_number)
        if asset:
            return asset.state in (AssetState.NEEDS_CALIBRATION, AssetState.ALERT)
        return False
    
    def needs_maintenance(self, serial_number: str) -> bool:
        """
        Check if an asset needs maintenance.
        
        Args:
            serial_number: Asset serial number
            
        Returns:
            True if asset needs maintenance
        """
        asset = self.get_asset_by_serial(serial_number)
        if asset:
            return asset.state in (AssetState.NEEDS_MAINTENANCE, AssetState.WARNING)
        return False
