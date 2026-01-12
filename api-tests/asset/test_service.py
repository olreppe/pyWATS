from uuid import uuid4
from typing import List, Optional, Tuple

import pytest

from pywats.domains.asset.enums import AssetState
from pywats.domains.asset.models import Asset
from pywats.domains.asset.service import AssetService


class DummyAssetRepository:
    def __init__(self) -> None:
        self.saved: List[Asset] = []
        self.deleted: List[Tuple[str, Optional[str]]] = []
        self.state_updates: List[Tuple[AssetState, Optional[str], Optional[str]]] = []
        self._assets: dict[str, Asset] = {}

    def save(self, asset: Asset) -> Asset:
        asset.asset_id = asset.asset_id or str(uuid4())
        self._assets[asset.serial_number] = asset
        self.saved.append(asset)
        return asset

    def get_by_serial_number(self, serial_number: str) -> Optional[Asset]:
        existing = self._assets.get(serial_number)
        if existing:
            return existing
        return Asset(
            serial_number=serial_number,
            type_id=uuid4(),
            asset_id="resolved-id"
        )

    def delete(self, asset_id: str, serial_number: Optional[str] = None) -> bool:
        self.deleted.append((asset_id, serial_number))
        return True

    def set_state(
        self,
        state: AssetState,
        asset_id: Optional[str] = None,
        serial_number: Optional[str] = None
    ) -> bool:
        self.state_updates.append((state, asset_id, serial_number))
        return True


@pytest.fixture
def asset_service() -> AssetService:
    repository = DummyAssetRepository()
    return AssetService(repository=repository)


def test_create_asset_calls_repository(asset_service: AssetService) -> None:
    serial_number = "SN-123"
    type_id = uuid4()

    asset = asset_service.create_asset(
        serial_number=serial_number,
        type_id=type_id,
        asset_name="Test Asset"
    )

    repo = asset_service._repository
    assert asset is not None
    assert repo.saved[-1] is asset
    assert asset.serial_number == serial_number
    assert asset.type_id == type_id


def test_delete_asset_by_serial_number_resolves_identifier(asset_service: AssetService) -> None:
    repo = asset_service._repository
    repo._assets["SN-DEL"] = Asset(
        serial_number="SN-DEL",
        type_id=uuid4(),
        asset_id="ID-DEL"
    )

    deleted = asset_service.delete_asset(serial_number="SN-DEL")

    assert deleted is True
    assert repo.deleted[-1][0] == "ID-DEL"


def test_set_asset_state_updates_repository(asset_service: AssetService) -> None:
    result = asset_service.set_asset_state(
        state=AssetState.IN_MAINTENANCE,
        serial_number="SN-STATE"
    )

    repo = asset_service._repository
    assert result is True
    assert repo.state_updates[-1][0] == AssetState.IN_MAINTENANCE
    assert repo.state_updates[-1][2] == "SN-STATE"
