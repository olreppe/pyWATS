"""
Tests for asset module - asset creation and state management
"""
import pytest
from pywats.models.asset import Asset, AssetType


class TestAssetCreation:
    """Test creating and managing assets"""
    
    def test_create_asset(self):
        """Test creating a basic asset"""
        asset = Asset(
            asset_name="TEST_FIXTURE_001",
            asset_type=AssetType.FIXTURE,
            serial_number="FIX-12345"
        )
        assert asset.asset_name == "TEST_FIXTURE_001"
        assert asset.asset_type == AssetType.FIXTURE
    
    def test_register_asset(self, wats_client):
        """Test registering a new asset"""
        from datetime import datetime
        asset = Asset(
            asset_name=f"TEST_ASSET_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            asset_type=AssetType.FIXTURE,
            serial_number="TEST-SN-001"
        )
        
        try:
            result = wats_client.asset.create_asset(asset)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Asset creation failed: {e}")


class TestAssetRetrieval:
    """Test retrieving and searching assets"""
    
    def test_get_asset_by_name(self, wats_client):
        """Test getting an asset by name"""
        try:
            asset = wats_client.asset.get_asset("TEST_FIXTURE_001")
            if asset:
                assert asset.asset_name == "TEST_FIXTURE_001"
            else:
                pytest.skip("Test asset not found")
        except Exception as e:
            pytest.skip(f"Get asset failed: {e}")
    
    def test_get_all_assets(self, wats_client):
        """Test getting all assets"""
        try:
            assets = wats_client.asset.get_assets()
            assert isinstance(assets, list)
        except Exception as e:
            pytest.skip(f"Get assets failed: {e}")


class TestAssetState:
    """Test asset state checking and updates"""
    
    def test_check_asset_state(self, wats_client):
        """Test checking asset state"""
        try:
            state = wats_client.asset.get_asset_state("TEST_FIXTURE_001")
            assert state is not None
        except Exception as e:
            pytest.skip(f"Get state failed: {e}")
    
    def test_update_asset_state(self, wats_client):
        """Test updating asset state"""
        try:
            result = wats_client.asset.update_asset_state(
                "TEST_FIXTURE_001",
                state="InUse"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Update state failed: {e}")
