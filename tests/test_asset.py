"""
Tests for asset module - asset creation and state management

These tests make actual API calls to the WATS server.
"""
from typing import Any, Dict
from datetime import datetime, timezone
import pytest
from pywats.domains.asset import Asset


class TestServerConfiguration:
    """Verify test configuration"""

    def test_verify_asset_config(self, wats_config: Dict[str, str]) -> None:
        """Verify server URL for asset tests"""
        print(f"\n=== ASSET TEST CONFIG ===")
        print(f"Server: {wats_config['base_url']}")
        print(f"=========================\n")
        assert "wats.com" in wats_config['base_url']


class TestAssetModel:
    """Test Asset model creation (no server)"""

    def test_create_asset_model(self) -> None:
        """Test creating a basic asset model object"""
        asset = Asset(
            serial_number="FIX-12345",
            asset_name="TEST_FIXTURE_001"
        )
        assert asset.asset_name == "TEST_FIXTURE_001"
        assert asset.serial_number == "FIX-12345"


class TestAssetRetrieval:
    """Test retrieving assets from server"""

    def test_get_all_assets(self, wats_client: Any) -> None:
        """Test getting all assets from server"""
        print("\n=== GET ALL ASSETS ===")
        
        assets = wats_client.asset.get_assets()
        
        print(f"Retrieved {len(assets)} assets")
        if assets:
            print(f"First asset: {assets[0].asset_name}")
        print("======================\n")
        
        assert isinstance(assets, list)

    def test_get_assets_with_limit(self, wats_client: Any) -> None:
        """Test getting limited number of assets"""
        print("\n=== GET ASSETS (TOP 5) ===")
        
        assets = wats_client.asset.get_assets(top=5)
        
        print(f"Retrieved {len(assets)} assets (limit 5)")
        for asset in assets:
            print(f"  - {asset.asset_name}: {asset.serial_number}")
        print("==========================\n")
        
        assert isinstance(assets, list)
        assert len(assets) <= 5


class TestAssetTypes:
    """Test asset type operations"""

    def test_get_asset_types(self, wats_client: Any) -> None:
        """Test getting all asset types"""
        print("\n=== GET ASSET TYPES ===")
        
        types = wats_client.asset.get_asset_types()
        
        print(f"Retrieved {len(types)} asset types")
        for t in types[:5]:
            print(f"  - {t.type_name}: {t.type_id}")
        print("=======================\n")
        
        assert isinstance(types, list)


class TestAssetCreation:
    """Test creating assets on server"""

    def test_create_and_retrieve_asset(self, wats_client: Any) -> None:
        """Test creating a new asset and retrieving it"""
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        
        print("\n=== CREATE ASSET ===")
        
        # First, we need an asset type ID
        types = wats_client.asset.get_asset_types()
        if not types:
            pytest.skip("No asset types available - cannot create asset without type")
        
        type_id = types[0].type_id
        print(f"Using asset type: {types[0].type_name} ({type_id})")
        
        # Create asset using service method
        serial_number = f"PYTEST-{timestamp}"
        asset_name = f"PyTest Asset {timestamp}"
        
        result = wats_client.asset.create_asset(
            serial_number=serial_number,
            type_id=type_id,
            asset_name=asset_name,
            description="Created by pytest"
        )
        
        print(f"Create result: {result}")
        print("====================\n")
        
        assert result is not None, "Asset creation returned None"
        assert result.serial_number == serial_number


class TestAssetState:
    """Test asset state operations"""

    def test_get_asset_state(self, wats_client: Any) -> None:
        """Test getting asset state"""
        print("\n=== GET ASSET STATE ===")
        
        # Get an existing asset first
        assets = wats_client.asset.get_assets(top=1)
        if not assets:
            pytest.skip("No assets available to check state")
        
        asset = assets[0]
        print(f"Checking state for: {asset.asset_name} (ID: {asset.asset_id})")
        
        state = wats_client.asset.get_asset_state(str(asset.asset_id))
        
        print(f"Asset state: {state}")
        print("=======================\n")
        
        # State might be None if not set, but call should succeed
        # Just verify no exception was raised
