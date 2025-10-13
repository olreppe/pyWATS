"""
Asset module for WATS API.

This module provides functionality for managing assets, equipment,
and asset-related operations in the WATS system.
"""

from typing import List, Optional, Dict, Any, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal
from enum import Enum
from .base import BaseModule
from ..exceptions import WATSException, WATSNotFoundError
from ..models.asset_model import AssetModel
from pydantic import Field, PrivateAttr  # Ensure this is imported

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


class AssetInfo(AssetModel):
    """Asset information model, extending the generated AssetModel with custom methods."""
    # Add additional fields not in AssetModel, with proper Pydantic defaults
    additional_properties: Dict[str, Any] = Field(default_factory=dict)
    configuration: Dict[str, Any] = Field(default_factory=dict)
    # Note: serial_number, parent_asset_id, etc., are already in AssetModel (via aliases)
    # If any are missing, add them here with aliases if needed

    _asset_module: Optional['AssetModule'] = PrivateAttr(default=None)  # Private attribute for module reference

    # No custom __init__ needed; Pydantic handles it

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
            # Convert to the correct AssetState enum from asset_model
            from ..models.asset_model import AssetState as ModelAssetState
            if isinstance(new_state, AssetState):
                # Map by value
                self.state = ModelAssetState(new_state.value)
            else:
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
        # Tags functionality not implemented yet - placeholder
        return False
    
    def remove_tag(self, tag: str) -> bool:
        """
        Remove a tag from the asset.
        
        Args:
            tag: Tag to remove
            
        Returns:
            bool: True if tag was removed successfully
        """
        # Tags functionality not implemented yet - placeholder
        return False
    
    def get_tags(self) -> List[str]:
        """
        Get all tags for the asset.
        
        Returns:
            List[str]: List of tags
        """
        # Tags functionality not implemented yet - placeholder
        return []
    
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
        # Use Pydantic's model_dump for proper serialization
        return self.model_dump()


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

    def get_asset(self, serial_number: str) -> Optional[AssetInfo]:
        """
        Get an asset by serial number.
        
        Args:
            serial_number: Serial number of the asset
            
        Returns:
            AssetInfo or None if not found
            
        Raises:
            WATSException: If the REST API call fails
        """
        try:
            from ..rest_api.public.api.asset.asset_get_asset_by_serial_number import sync as asset_get_asset_by_serial_number
            from typing import cast
            from ..rest_api.public.client import Client
            
            client = cast(Client, self.http_client)
            response = asset_get_asset_by_serial_number(
                serial_number=serial_number,
                client=client
            )
            
            if response is None:
                return None
            
            # Convert to AssetInfo
            asset_dict = response.to_dict() if hasattr(response, 'to_dict') else response
            asset_info = AssetInfo.model_validate(asset_dict)  # Or from API response
            asset_info._asset_module = self
            return asset_info
            
        except Exception as e:
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

    def get_assets(self, filter_str: Optional[str] = None, top: Optional[int] = None, 
                   skip: Optional[int] = None, orderby: Optional[str] = None) -> List[AssetInfo]:
        """
        Get assets with optional OData query parameters.
        
        Args:
            filter_str: Optional OData $filter expression (e.g., "state eq 'Available'")
            top: Optional $top parameter to limit results
            skip: Optional $skip parameter for pagination
            orderby: Optional $orderby parameter for sorting (e.g., "firstSeenDate desc")
            
        Returns:
            List[AssetInfo]: List of assets (empty if none found)
            
        Raises:
            WATSException: If the REST API call fails
            
        Examples:
            # Get all assets
            assets = module.get_assets()
            
            # Get assets with filter
            assets = module.get_assets(filter_str="state eq 'Available'")
            
            # Get top 10 assets ordered by date
            assets = module.get_assets(top=10, orderby="firstSeenDate desc")
        """
        try:
            from typing import cast
            from ..rest_api.public.client import Client
            from ..rest_api.public.models.virinco_wats_web_dashboard_models_mes_asset_o_data_asset import (
                VirincoWATSWebDashboardModelsMesAssetODataAsset
            )
            from urllib.parse import urlencode
            
            client = cast(Client, self.http_client)
            
            # Build OData query parameters
            params = {}
            if filter_str:
                params['$filter'] = filter_str
            if top is not None:
                params['$top'] = str(top)
            if skip is not None:
                params['$skip'] = str(skip)
            if orderby:
                params['$orderby'] = orderby
            
            # Construct URL with query parameters
            url = "/api/Asset"
            if params:
                url += "?" + urlencode(params)
            
            # Make the HTTP request directly using the client
            response = client.get_httpx_client().request(
                method="get",
                url=url,
            )
            
            # Check response status
            if response.status_code != 200:
                raise WATSException(f"API returned status {response.status_code}: {response.text}")
            
            # Parse response
            asset_list = []
            response_data = response.json()
            
            if isinstance(response_data, list):
                for asset_data in response_data:
                    # Use the generated model to parse the response
                    asset_obj = VirincoWATSWebDashboardModelsMesAssetODataAsset.from_dict(asset_data)
                    asset_dict = asset_obj.to_dict()
                    
                    # Convert to AssetInfo
                    asset_info = AssetInfo.model_validate(asset_dict)
                    asset_info._asset_module = self
                    asset_list.append(asset_info)
            
            return asset_list
            
        except Exception as e:
            if isinstance(e, WATSException):
                raise
            filter_msg = f" with filter '{filter_str}'" if filter_str else ""
            raise WATSException(f"Failed to get assets{filter_msg}: {str(e)}")

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
        assets = self.get_assets("")
        return [asset.to_dict() for asset in assets]

    def get_by_id(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific asset by ID."""
        self._validate_id(asset_id, "asset")
        asset = self.get_asset(asset_id)
        return asset.to_dict() if asset else None

    def get_tree(self) -> List[Dict[str, Any]]:
        """Get the asset tree structure."""
        assets = self.get_assets("")
        return [asset.to_dict() for asset in assets]