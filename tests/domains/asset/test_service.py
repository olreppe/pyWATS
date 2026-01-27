from uuid import uuid4, UUID
from typing import List, Optional, Tuple

import pytest

from pywats.domains.asset.enums import AssetState
from pywats.domains.asset.models import Asset
from pywats.domains.asset import AsyncAssetService


class DummyAssetRepository:
    """Mock repository for testing AssetService."""
    
    def __init__(self) -> None:
        self.saved: List[Asset] = []
        self.deleted: List[str] = []
        self.state_updates: List[Tuple[str, AssetState]] = []
        self._assets: dict[str, Asset] = {}

    async def save(self, asset: Asset) -> Asset:
        asset.asset_id = asset.asset_id or str(uuid4())
        self._assets[asset.serial_number] = asset
        self.saved.append(asset)
        return asset

    async def get_by_serial_number(self, serial_number: str) -> Optional[Asset]:
        existing = self._assets.get(serial_number)
        if existing:
            return existing
        return None

    async def get_by_id(self, asset_id: str) -> Optional[Asset]:
        for asset in self._assets.values():
            if asset.asset_id == asset_id:
                return asset
        return None

    async def delete(self, asset_id: str, serial_number: Optional[str] = None) -> bool:
        self.deleted.append(asset_id)
        return True

    async def set_state(
        self,
        asset_id: str,
        state: AssetState
    ) -> bool:
        self.state_updates.append((asset_id, state))
        return True


@pytest.fixture
def asset_service() -> AsyncAssetService:
    repository = DummyAssetRepository()
    return AsyncAssetService(repository=repository)


@pytest.mark.asyncio
async def test_create_asset_calls_repository(asset_service: AsyncAssetService) -> None:
    serial_number = "SN-123"

    asset = await asset_service.create_asset(
        serial_number=serial_number,
        asset_name="Test Asset",
        type_id=UUID("00000000-0000-0000-0000-000000000001")
    )

    repo = asset_service._repository
    assert asset is not None
    assert repo.saved[-1] is asset
    assert asset.serial_number == serial_number


@pytest.mark.asyncio
async def test_get_asset_returns_asset(asset_service: AsyncAssetService) -> None:
    repo = asset_service._repository
    # Pre-populate repository
    test_asset = Asset(
        serial_number="SN-GET",
        asset_id="ID-GET",
        name="Get Test Asset"
    )
    repo._assets["SN-GET"] = test_asset

    result = await asset_service.get_asset(serial_number="SN-GET")

    assert result is not None
    assert result.serial_number == "SN-GET"


@pytest.mark.asyncio
async def test_delete_asset_calls_repository(asset_service: AsyncAssetService) -> None:
    repo = asset_service._repository

    deleted = await asset_service.delete_asset(asset_id="ID-DEL")

    assert deleted is True
    assert "ID-DEL" in repo.deleted
