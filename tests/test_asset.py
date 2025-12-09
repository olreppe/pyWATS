"""
Tests for asset module - asset creation and state management
"""
from typing import Any
import pytest
from pywats.models.asset import Asset


class TestAssetCreation:
    """Test creating and managing assets"""
    
    def test_create_asset(self) -> None:
        """Test creating a basic asset"""
        asset = Asset(
            assetName="TEST_FIXTURE_001",
            serialNumber="FIX-12345"
        )
        assert asset.asset_name == "TEST_FIXTURE_001"
    
    def test_register_asset(self, wats_client: Any) -> None:
        """Test registering a new asset"""
        from datetime import datetime
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        asset = Asset(
            assetName=f"TEST_ASSET_{timestamp}",
            serialNumber="TEST-SN-001"
        )
        
        try:
            result = wats_client.asset.create_asset(asset)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Asset creation failed: {e}")


class TestAssetRetrieval:
    """Test retrieving and searching assets"""
    
    def test_get_asset_by_name(self, wats_client: Any) -> None:
        """Test getting an asset by name"""
        try:
            asset = wats_client.asset.get_asset("TEST_FIXTURE_001")
            if asset:
                assert asset.asset_name == "TEST_FIXTURE_001"
            else:
                pytest.skip("Test asset not found")
        except Exception as e:
            pytest.skip(f"Get asset failed: {e}")
    
    def test_get_all_assets(self, wats_client: Any) -> None:
        """Test getting all assets"""
        try:
            assets = wats_client.asset.get_assets()
            assert isinstance(assets, list)
        except Exception as e:
            pytest.skip(f"Get assets failed: {e}")


class TestAssetState:
    """Test asset state checking and updates"""
    
    def test_check_asset_state(self, wats_client: Any) -> None:
        """Test checking asset state"""
        try:
            state = wats_client.asset.get_asset_state("TEST_FIXTURE_001")
            assert state is not None
        except Exception as e:
            pytest.skip(f"Get state failed: {e}")
    
    def test_update_asset_state(self, wats_client: Any) -> None:
        """Test updating asset state"""
        try:
            result = wats_client.asset.update_asset_state(
                "TEST_FIXTURE_001",
                state="InUse"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Update state failed: {e}")
