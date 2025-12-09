"""Asset service - business logic layer.

Provides high-level operations for asset management.
"""
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID

from .models import Asset, AssetType, AssetLog
from .enums import AssetState
from .repository import AssetRepository


class AssetService:
    """
    Asset business logic.

    Provides high-level operations for managing assets including
    validation, state management, and business rules.
    """

    def __init__(self, repository: AssetRepository):
        """
        Initialize with repository.

        Args:
            repository: AssetRepository for data access
        """
        self._repo = repository

    # =========================================================================
    # Asset Operations
    # =========================================================================

    def get_assets(
        self,
        filter_str: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[Asset]:
        """
        Get all assets.

        Args:
            filter_str: Optional OData filter string
            top: Optional max number of results

        Returns:
            List of Asset objects
        """
        return self._repo.get_all(filter_str=filter_str, top=top)

    def get_asset(self, identifier: str) -> Optional[Asset]:
        """
        Get an asset by ID or serial number.

        Args:
            identifier: Asset ID (GUID) or serial number

        Returns:
            Asset if found, None otherwise
        """
        return self._repo.get_by_id(identifier)

    def get_asset_by_serial(self, serial_number: str) -> Optional[Asset]:
        """
        Get an asset by serial number.

        Args:
            serial_number: Asset serial number

        Returns:
            Asset if found, None otherwise
        """
        return self._repo.get_by_serial_number(serial_number)

    def create_asset(
        self,
        serial_number: str,
        type_id: UUID,
        asset_name: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        **kwargs: Any
    ) -> Optional[Asset]:
        """
        Create a new asset.

        Args:
            serial_number: Unique serial number
            type_id: Asset type ID
            asset_name: Optional display name
            description: Optional description
            location: Optional location
            **kwargs: Additional asset fields

        Returns:
            Created Asset object
        """
        asset = Asset(
            serial_number=serial_number,
            type_id=type_id,
            asset_name=asset_name,
            description=description,
            location=location,
            **kwargs
        )
        return self._repo.save(asset)

    def update_asset(self, asset: Asset) -> Optional[Asset]:
        """
        Update an existing asset.

        Args:
            asset: Asset object with updated fields

        Returns:
            Updated Asset object
        """
        return self._repo.save(asset)

    def delete_asset(self, asset_id: str) -> bool:
        """
        Delete an asset.

        Args:
            asset_id: Asset ID to delete

        Returns:
            True if successful
        """
        return self._repo.delete(asset_id)

    # =========================================================================
    # State Management
    # =========================================================================

    def get_asset_state(self, asset_id: str) -> Optional[AssetState]:
        """
        Get the current state of an asset.

        Args:
            asset_id: Asset ID

        Returns:
            Current AssetState or None if not found
        """
        asset = self._repo.get_by_id(asset_id)
        return asset.state if asset else None

    def set_asset_state(
        self,
        asset_id: str,
        state: AssetState,
        comment: Optional[str] = None
    ) -> bool:
        """
        Set the state of an asset.

        Args:
            asset_id: Asset ID
            state: New state
            comment: Optional comment

        Returns:
            True if successful
        """
        return self._repo.set_state(asset_id, state, comment)

    def needs_calibration(self, asset: Asset) -> bool:
        """
        Check if an asset needs calibration.

        Args:
            asset: Asset to check

        Returns:
            True if asset needs calibration
        """
        return asset.state == AssetState.NEEDS_CALIBRATION

    def needs_maintenance(self, asset: Asset) -> bool:
        """
        Check if an asset needs maintenance.

        Args:
            asset: Asset to check

        Returns:
            True if asset needs maintenance
        """
        return asset.state == AssetState.NEEDS_MAINTENANCE

    def get_assets_needing_maintenance(self) -> List[Asset]:
        """
        Get all assets that need maintenance.

        Returns:
            List of assets needing maintenance
        """
        assets = self._repo.get_all()
        return [a for a in assets if a.state == AssetState.NEEDS_MAINTENANCE]

    def get_assets_needing_calibration(self) -> List[Asset]:
        """
        Get all assets that need calibration.

        Returns:
            List of assets needing calibration
        """
        assets = self._repo.get_all()
        return [a for a in assets if a.state == AssetState.NEEDS_CALIBRATION]

    # =========================================================================
    # Count Operations
    # =========================================================================

    def increment_count(self, asset_id: str, amount: int = 1) -> bool:
        """
        Increment the usage count of an asset.

        Args:
            asset_id: Asset ID
            amount: Amount to increment by (default 1)

        Returns:
            True if successful
        """
        return self._repo.update_count(asset_id, increment_by=amount)

    def reset_running_count(self, asset_id: str) -> bool:
        """
        Reset the running count of an asset.

        Args:
            asset_id: Asset ID

        Returns:
            True if successful
        """
        return self._repo.reset_running_count(asset_id)

    # =========================================================================
    # Calibration & Maintenance
    # =========================================================================

    def record_calibration(
        self,
        asset_id: str,
        user: str,
        comment: Optional[str] = None,
        calibration_date: Optional[datetime] = None
    ) -> bool:
        """
        Record a calibration event for an asset.

        Args:
            asset_id: Asset ID
            user: User who performed calibration
            comment: Optional comment
            calibration_date: Date of calibration (default: now)

        Returns:
            True if successful
        """
        data = {
            "assetId": asset_id,
            "user": user,
            "date": (calibration_date or datetime.now()).isoformat()
        }
        if comment:
            data["comment"] = comment
        return self._repo.post_calibration(data)

    def record_maintenance(
        self,
        asset_id: str,
        user: str,
        comment: Optional[str] = None,
        maintenance_date: Optional[datetime] = None
    ) -> bool:
        """
        Record a maintenance event for an asset.

        Args:
            asset_id: Asset ID
            user: User who performed maintenance
            comment: Optional comment
            maintenance_date: Date of maintenance (default: now)

        Returns:
            True if successful
        """
        data = {
            "assetId": asset_id,
            "user": user,
            "date": (maintenance_date or datetime.now()).isoformat()
        }
        if comment:
            data["comment"] = comment
        return self._repo.post_maintenance(data)

    # =========================================================================
    # Log Operations
    # =========================================================================

    def get_asset_log(
        self,
        filter_str: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[AssetLog]:
        """
        Get asset log entries.

        Args:
            filter_str: Optional OData filter
            top: Max number of entries

        Returns:
            List of AssetLog entries
        """
        return self._repo.get_log(filter_str=filter_str, top=top)

    def add_log_message(
        self,
        asset_id: str,
        message: str,
        user: Optional[str] = None
    ) -> bool:
        """
        Add a message to the asset log.

        Args:
            asset_id: Asset ID
            message: Message text
            user: Optional user name

        Returns:
            True if successful
        """
        return self._repo.post_message(asset_id, message, user)

    # =========================================================================
    # Asset Types
    # =========================================================================

    def get_asset_types(self) -> List[AssetType]:
        """
        Get all asset types.

        Returns:
            List of AssetType objects
        """
        return self._repo.get_types()

    def create_asset_type(
        self,
        type_name: str,
        calibration_interval: Optional[float] = None,
        maintenance_interval: Optional[float] = None,
        **kwargs: Any
    ) -> Optional[AssetType]:
        """
        Create a new asset type.

        Args:
            type_name: Name of the asset type
            calibration_interval: Days between calibrations
            maintenance_interval: Days between maintenance
            **kwargs: Additional fields

        Returns:
            Created AssetType object
        """
        asset_type = AssetType(
            type_name=type_name,
            calibration_interval=calibration_interval,
            maintenance_interval=maintenance_interval,
            **kwargs
        )
        return self._repo.save_type(asset_type)

    # =========================================================================
    # Sub-Assets
    # =========================================================================

    def get_child_assets(self, parent_id: str) -> List[Asset]:
        """
        Get child assets of a parent.

        Args:
            parent_id: Parent asset ID

        Returns:
            List of child Asset objects
        """
        return self._repo.get_sub_assets(parent_id)
