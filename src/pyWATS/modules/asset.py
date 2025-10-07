"""
Asset module for WATS API.

This module provides functionality for managing assets, equipment,
and asset-related operations in the WATS system.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from enum import Enum
from .base import BaseModule
from ..exceptions import WATSException, WATSNotFoundError


class AssetState(Enum):
    """Asset state enumeration."""
    AVAILABLE = "Available"
    IN_USE = "InUse"
    MAINTENANCE = "Maintenance"
    UNAVAILABLE = "Unavailable"


class AssetResponse:
    """Response object for asset operations."""
    def __init__(self, success: bool = True, message: str = "", data: Any = None):
        self.success = success
        self.message = message
        self.data = data


class AssetInfo:
    """Asset information with comprehensive asset management capabilities."""
    
    def __init__(self, id: str, name: str = "", location: str = "", 
                 state: AssetState = AssetState.AVAILABLE, asset_type: str = "", **kwargs):
        self.id = id
        self.name = name
        self.location = location
        self.state = state
        self.asset_type = asset_type
        self.additional_properties = kwargs.get('additional_properties', {})
        self.serial_number = kwargs.get('serial_number', id)
        self.parent_asset_id = kwargs.get('parent_asset_id')
        self.description = kwargs.get('description', '')
        self.running_count = kwargs.get('running_count', 0)
        self.total_count = kwargs.get('total_count', 0)
        self.calibration_date = kwargs.get('calibration_date')
        self.maintenance_date = kwargs.get('maintenance_date')
        self.tags = kwargs.get('tags', [])
        self.configuration = kwargs.get('configuration', {})
        
        # Private module reference for REST operations
        self._asset_module = kwargs.get('_asset_module')
    
    def update_location(self, new_location: str) -> bool:
        """
        Update the asset location.
        
        Args:
            new_location: New location for the asset
            
        Returns:
            bool: True if update was successful
        """
        if self._asset_module:
            # This would call an update endpoint when available
            # For now, just update locally
            self.location = new_location
            return True
        return False
    
    def set_state(self, new_state: AssetState) -> bool:
        """
        Set the asset state.
        
        Args:
            new_state: New state for the asset
            
        Returns:
            bool: True if state change was successful
        """
        if self._asset_module:
            # This would call a state update endpoint when available
            # For now, just update locally
            self.state = new_state
            return True
        return False
    
    def add_tag(self, tag: str) -> bool:
        """
        Add a tag to the asset.
        
        Args:
            tag: Tag to add
            
        Returns:
            bool: True if tag was added successfully
        """
        if tag not in self.tags:
            self.tags.append(tag)
            # In a full implementation, this would call REST API
            return True
        return False
    
    def remove_tag(self, tag: str) -> bool:
        """
        Remove a tag from the asset.
        
        Args:
            tag: Tag to remove
            
        Returns:
            bool: True if tag was removed successfully
        """
        if tag in self.tags:
            self.tags.remove(tag)
            # In a full implementation, this would call REST API
            return True
        return False
    
    def get_tags(self) -> List[str]:
        """
        Get all tags for the asset.
        
        Returns:
            List[str]: List of tags
        """
        return self.tags.copy()
    
    def update_config(self, config: Dict[str, Any]) -> bool:
        """
        Update the asset configuration.
        
        Args:
            config: Configuration dictionary to update
            
        Returns:
            bool: True if configuration was updated successfully
        """
        if self._asset_module:
            # This would call a config update endpoint when available
            # For now, just update locally
            self.configuration.update(config)
            return True
        return False
    
    def track_usage(self, usage_data: Dict[str, Any]) -> bool:
        """
        Track asset usage.
        
        Args:
            usage_data: Usage tracking data
            
        Returns:
            bool: True if usage was tracked successfully
        """
        if self._asset_module:
            # This would call a usage tracking endpoint when available
            # For now, just increment running count
            increment = usage_data.get('increment', 1)
            self.running_count += increment
            return True
        return False
    
    def is_available(self) -> bool:
        """
        Check if the asset is available.
        
        Returns:
            bool: True if asset is available
        """
        return self.state == AssetState.AVAILABLE
    
    def get_configuration(self) -> Dict[str, Any]:
        """
        Get the asset configuration.
        
        Returns:
            Dict[str, Any]: Asset configuration
        """
        return self.configuration.copy()
    
    def perform_calibration(self, date_time: Optional[datetime] = None, comment: Optional[str] = None) -> bool:
        """
        Perform calibration on the asset.
        
        Args:
            date_time: Calibration date and time
            comment: Optional comment
            
        Returns:
            bool: True if calibration was successful
        """
        if self._asset_module:
            try:
                response = self._asset_module.calibration(self.serial_number, date_time, comment)
                if response.success:
                    self.calibration_date = date_time or datetime.now()
                    return True
            except Exception:
                pass
        return False
    
    def perform_maintenance(self, date_time: Optional[datetime] = None, comment: Optional[str] = None) -> bool:
        """
        Perform maintenance on the asset.
        
        Args:
            date_time: Maintenance date and time
            comment: Optional comment
            
        Returns:
            bool: True if maintenance was successful
        """
        if self._asset_module:
            try:
                response = self._asset_module.maintenance(self.serial_number, date_time, comment)
                if response.success:
                    self.maintenance_date = date_time or datetime.now()
                    return True
            except Exception:
                pass
        return False
    
    def reset_running_count(self, comment: Optional[str] = None) -> bool:
        """
        Reset the running count of the asset.
        
        Args:
            comment: Optional comment
            
        Returns:
            bool: True if reset was successful
        """
        if self._asset_module:
            try:
                response = self._asset_module.reset_running_count(self.serial_number, comment)
                if response.success:
                    self.running_count = 0
                    return True
            except Exception:
                pass
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert AssetInfo to dictionary.
        
        Returns:
            Dict[str, Any]: Asset information as dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'state': self.state.value if isinstance(self.state, AssetState) else self.state,
            'asset_type': self.asset_type,
            'serial_number': self.serial_number,
            'parent_asset_id': self.parent_asset_id,
            'description': self.description,
            'running_count': self.running_count,
            'total_count': self.total_count,
            'calibration_date': self.calibration_date.isoformat() if self.calibration_date else None,
            'maintenance_date': self.maintenance_date.isoformat() if self.maintenance_date else None,
            'tags': self.tags,
            'configuration': self.configuration,
            'additional_properties': self.additional_properties
        }


class Asset:
    """Asset data model."""
    def __init__(self, serial_number: str, asset_type: str, **kwargs):
        self.serial_number = serial_number
        self.asset_type = asset_type
        self.parent_asset_serial_number = kwargs.get('parent_asset_serial_number')
        self.asset_name = kwargs.get('asset_name')
        self.asset_description = kwargs.get('asset_description')
    
    def to_string(self) -> str:
        """Convert asset to string representation."""
        raise NotImplementedError("Asset.to_string not implemented")


class AssetModule(BaseModule):
    """
    Asset management module.
    
    Provides methods for:
    - Creating and managing assets
    - Asset type management
    - Asset hierarchy operations
    - Calibration and maintenance
    - Usage tracking
    """

    # Asset Handler Methods
    def is_connected(self) -> bool:
        """Check if asset handler is connected."""
        raise NotImplementedError("AssetHandler.is_connected not implemented")

    def create_asset(self, serial_number: str, asset_type: str,
                    parent_asset_serial_number: Optional[str] = None,
                    asset_name: Optional[str] = None,
                    asset_description: Optional[str] = None) -> AssetResponse:
        """
        Create a new asset.
        
        Args:
            serial_number: Serial number of the asset
            asset_type: Type of the asset
            parent_asset_serial_number: Optional parent asset serial number
            asset_name: Optional asset name
            asset_description: Optional asset description
            
        Returns:
            AssetResponse object
        """
        raise NotImplementedError("AssetHandler.create_asset not implemented")

    def create_asset_type(self, name: str,
                         calibration_interval: Optional[Decimal] = None,
                         maintenance_interval: Optional[Decimal] = None,
                         running_count_limit: Optional[int] = None,
                         total_count_limit: Optional[int] = None,
                         warning_threshold: Optional[Decimal] = None,
                         alarm_threshold: Optional[Decimal] = None) -> AssetResponse:
        """
        Create a new asset type.
        
        Args:
            name: Name of the asset type
            calibration_interval: Optional calibration interval
            maintenance_interval: Optional maintenance interval
            running_count_limit: Optional running count limit
            total_count_limit: Optional total count limit
            warning_threshold: Optional warning threshold
            alarm_threshold: Optional alarm threshold
            
        Returns:
            AssetResponse object
        """
        raise NotImplementedError("AssetHandler.create_asset_type not implemented")

    def get_asset(self, serial_number: str) -> AssetResponse:
        """
        Get an asset by serial number.
        
        Args:
            serial_number: Serial number of the asset
            
        Returns:
            AssetResponse object containing asset data
            
        Raises:
            WATSException: If the REST API call fails
            WATSNotFoundError: If the asset is not found
        """
        try:
            from ..rest_api.public.api.asset.asset_get_asset_by_serial_number import sync as asset_get_asset_by_serial_number
            from typing import cast
            from ..rest_api.public.client import Client
            
            # Cast the http_client to the expected Client type
            client = cast(Client, self.http_client)
            
            # Call the REST API to get asset by serial number
            response = asset_get_asset_by_serial_number(
                serial_number=serial_number,
                client=client
            )
            
            if response is None:
                raise WATSNotFoundError(f"Asset with serial number '{serial_number}' not found")
            
            # Convert the response to our AssetResponse format
            return AssetResponse(
                success=True,
                message=f"Asset '{serial_number}' retrieved successfully",
                data=response.to_dict() if hasattr(response, 'to_dict') else response
            )
            
        except Exception as e:
            if isinstance(e, (WATSException, WATSNotFoundError)):
                raise
            raise WATSException(f"Failed to get asset '{serial_number}': {str(e)}")

    def update_asset(self, asset: Asset) -> AssetResponse:
        """
        Update an existing asset.
        
        Args:
            asset: Asset object to update
            
        Returns:
            AssetResponse object
        """
        raise NotImplementedError("AssetHandler.update_asset not implemented")

    def set_parent(self, serial_number: str, parent_serial_number: str) -> AssetResponse:
        """
        Set the parent of an asset.
        
        Args:
            serial_number: Serial number of the asset
            parent_serial_number: Serial number of the parent asset
            
        Returns:
            AssetResponse object
        """
        raise NotImplementedError("AssetHandler.set_parent not implemented")

    def increment_asset_usage_count(self, serial_number: str,
                                   usage_count: int = 1,
                                   increment_sub_assets: bool = False) -> AssetResponse:
        """
        Increment the usage count of an asset.
        
        Args:
            serial_number: Serial number of the asset
            usage_count: Usage count to increment by (default: 1)
            increment_sub_assets: Whether to increment sub-assets (default: False)
            
        Returns:
            AssetResponse object
        """
        raise NotImplementedError("AssetHandler.increment_asset_usage_count not implemented")

    def get_assets(self, filter_str: str) -> AssetResponse:
        """
        Get assets by filter.
        
        Args:
            filter_str: OData filter string (e.g., "assetId eq '1'" or "runningCount gt 1000")
            
        Returns:
            AssetResponse object containing list of assets
            
        Raises:
            WATSException: If the REST API call fails
        """
        try:
            from ..rest_api.public.api.asset.asset_get_assets import sync as asset_get_assets
            from typing import cast
            from ..rest_api.public.client import Client
            
            # Cast the http_client to the expected Client type
            client = cast(Client, self.http_client)
            
            # Note: The REST API endpoint doesn't support filter parameters directly in the function signature
            # The filtering would typically be done through OData query parameters in the URL
            # For now, we'll call the basic endpoint and return all assets
            # In a real implementation, you might need to modify the REST client to support OData parameters
            response = asset_get_assets(client=client)
            
            if response is None:
                response = []
            
            # Convert the response to our AssetResponse format
            asset_list = []
            if isinstance(response, list):
                for asset in response:
                    if hasattr(asset, 'to_dict'):
                        asset_list.append(asset.to_dict())
                    else:
                        asset_list.append(asset)
            
            return AssetResponse(
                success=True,
                message=f"Retrieved {len(asset_list)} assets",
                data=asset_list
            )
            
        except Exception as e:
            if isinstance(e, WATSException):
                raise
            raise WATSException(f"Failed to get assets with filter '{filter_str}': {str(e)}")

    def get_assets_by_tag(self, tag: str) -> AssetResponse:
        """
        Get assets by tag.
        
        Args:
            tag: Tag to filter by
            
        Returns:
            AssetResponse object
        """
        raise NotImplementedError("AssetHandler.get_assets_by_tag not implemented")

    def get_sub_assets(self, serial_number: str, level: Optional[int] = None) -> AssetResponse:
        """
        Get sub-assets of an asset.
        
        Args:
            serial_number: Serial number of the parent asset
            level: Optional level depth
            
        Returns:
            AssetResponse object
        """
        raise NotImplementedError("AssetHandler.get_sub_assets not implemented")

    def calibration(self, serial_number: str,
                   date_time: Optional[datetime] = None,
                   comment: Optional[str] = None) -> AssetResponse:
        """
        Perform calibration on an asset.
        
        Args:
            serial_number: Serial number of the asset
            date_time: Optional calibration date and time (defaults to current time)
            comment: Optional comment
            
        Returns:
            AssetResponse object indicating success or failure
            
        Raises:
            WATSException: If the REST API call fails
            WATSNotFoundError: If the asset is not found
        """
        try:
            from ..rest_api.public.api.asset.asset_post_calibration import sync as asset_post_calibration
            from typing import cast
            from ..rest_api.public.client import Client
            from ..rest_api.public.types import UNSET
            
            # Cast the http_client to the expected Client type
            client = cast(Client, self.http_client)
            
            # Use current time if date_time is not provided
            if date_time is None:
                date_time = datetime.now()
            
            # Call the REST API to perform calibration
            response = asset_post_calibration(
                client=client,
                serial_number=serial_number,
                id=UNSET,  # We're using serial_number instead of id
                date_time=date_time,
                comment=comment if comment is not None else UNSET
            )
            
            if response is None:
                raise WATSNotFoundError(f"Asset with serial number '{serial_number}' not found or calibration failed")
            
            # Convert the response to our AssetResponse format
            return AssetResponse(
                success=True,
                message=f"Calibration performed on asset '{serial_number}' successfully",
                data=response.to_dict() if hasattr(response, 'to_dict') else response
            )
            
        except Exception as e:
            if isinstance(e, (WATSException, WATSNotFoundError)):
                raise
            raise WATSException(f"Failed to perform calibration on asset '{serial_number}': {str(e)}")

    def maintenance(self, serial_number: str,
                   date_time: Optional[datetime] = None,
                   comment: Optional[str] = None) -> AssetResponse:
        """
        Perform maintenance on an asset.
        
        Args:
            serial_number: Serial number of the asset
            date_time: Optional maintenance date and time (defaults to current time)
            comment: Optional comment
            
        Returns:
            AssetResponse object indicating success or failure
            
        Raises:
            WATSException: If the REST API call fails
            WATSNotFoundError: If the asset is not found
        """
        try:
            from ..rest_api.public.api.asset.asset_post_maintenance import sync as asset_post_maintenance
            from typing import cast
            from ..rest_api.public.client import Client
            from ..rest_api.public.types import UNSET
            
            # Cast the http_client to the expected Client type
            client = cast(Client, self.http_client)
            
            # Use current time if date_time is not provided
            if date_time is None:
                date_time = datetime.now()
            
            # Call the REST API to perform maintenance
            response = asset_post_maintenance(
                client=client,
                serial_number=serial_number,
                id=UNSET,  # We're using serial_number instead of id
                date_time=date_time,
                comment=comment if comment is not None else UNSET
            )
            
            if response is None:
                raise WATSNotFoundError(f"Asset with serial number '{serial_number}' not found or maintenance failed")
            
            # Convert the response to our AssetResponse format
            return AssetResponse(
                success=True,
                message=f"Maintenance performed on asset '{serial_number}' successfully",
                data=response.to_dict() if hasattr(response, 'to_dict') else response
            )
            
        except Exception as e:
            if isinstance(e, (WATSException, WATSNotFoundError)):
                raise
            raise WATSException(f"Failed to perform maintenance on asset '{serial_number}': {str(e)}")

    def reset_running_count(self, serial_number: str, comment: Optional[str] = None) -> AssetResponse:
        """
        Reset the running count of an asset.
        
        Args:
            serial_number: Serial number of the asset
            comment: Optional comment
            
        Returns:
            AssetResponse object indicating success or failure
            
        Raises:
            WATSException: If the REST API call fails
            WATSNotFoundError: If the asset is not found
        """
        try:
            from ..rest_api.public.api.asset.asset_reset_running_count import sync as asset_reset_running_count
            from typing import cast
            from ..rest_api.public.client import Client
            from ..rest_api.public.types import UNSET
            
            # Cast the http_client to the expected Client type
            client = cast(Client, self.http_client)
            
            # Call the REST API to reset running count
            response = asset_reset_running_count(
                client=client,
                serial_number=serial_number,
                id=UNSET,  # We're using serial_number instead of id
                comment=comment if comment is not None else UNSET
            )
            
            if response is None:
                raise WATSNotFoundError(f"Asset with serial number '{serial_number}' not found or running count reset failed")
            
            # Convert the response to our AssetResponse format
            return AssetResponse(
                success=True,
                message=f"Running count reset for asset '{serial_number}' successfully",
                data=response.to_dict() if hasattr(response, 'to_dict') else response
            )
            
        except Exception as e:
            if isinstance(e, (WATSException, WATSNotFoundError)):
                raise
            raise WATSException(f"Failed to reset running count for asset '{serial_number}': {str(e)}")

    def delete_asset(self, serial_number: str) -> AssetResponse:
        """
        Delete an asset.
        
        Args:
            serial_number: Serial number of the asset to delete
            
        Returns:
            AssetResponse object indicating success or failure
            
        Raises:
            WATSException: If the REST API call fails
            WATSNotFoundError: If the asset is not found
        """
        try:
            from ..rest_api.public.api.asset.asset_delete_asset import sync as asset_delete_asset
            from typing import cast
            from ..rest_api.public.client import Client
            from ..rest_api.public.types import UNSET
            
            # Cast the http_client to the expected Client type
            client = cast(Client, self.http_client)
            
            # Call the REST API to delete asset by serial number
            response = asset_delete_asset(
                client=client,
                serial_number=serial_number,
                id=UNSET  # We're using serial_number instead of id
            )
            
            if response is None:
                raise WATSNotFoundError(f"Asset with serial number '{serial_number}' not found or could not be deleted")
            
            # Convert the response to our AssetResponse format
            return AssetResponse(
                success=True,
                message=f"Asset '{serial_number}' deleted successfully",
                data=response.to_dict() if hasattr(response, 'to_dict') else response
            )
            
        except Exception as e:
            if isinstance(e, (WATSException, WATSNotFoundError)):
                raise
            raise WATSException(f"Failed to delete asset '{serial_number}': {str(e)}")

    # Legacy methods for backward compatibility
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all assets."""
        response = self.get_assets("")
        return response.data if response.data else []

    def get_by_id(self, asset_id: str) -> Dict[str, Any]:
        """Get a specific asset by ID."""
        self._validate_id(asset_id, "asset")
        response = self.get_asset(asset_id)
        return response.data if response.data else {}

    def get_tree(self) -> Dict[str, Any]:
        """Get the asset tree structure."""
        response = self.get_assets("")
        return response.data if response.data else {}