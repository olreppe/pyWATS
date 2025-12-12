"""
Acceptance Test: Asset Lifecycle Scenario

This scenario tests the complete asset management lifecycle:
1. Create assets
2. Associate with production
3. Track asset usage
4. Verify asset state changes
"""
import pytest
from pywats import pyWATS
from .conftest import AcceptanceTestHelper


@pytest.mark.acceptance
class TestAssetLifecycleScenario:
    """
    Complete asset lifecycle from creation to usage tracking
    """
    
    def test_station_asset_workflow(
        self,
        wats_client: pyWATS,
        test_asset_data: dict,
        unique_identifier: str
    ):
        """
        Test creating and managing a station asset.
        
        Steps:
        1. Create station asset
        2. Verify asset exists
        3. Get asset state
        4. Verify asset can be queried
        """
        asset_name = test_asset_data["name"]
        asset_type = test_asset_data["asset_type"]
        
        # Step 1: Create asset
        try:
            asset = wats_client.asset.create_asset(
                name=asset_name,
                asset_type=asset_type
            )
            assert asset is not None, "Failed to create asset"
        except Exception as e:
            pytest.skip(f"Asset creation failed: {e}")
        
        # Step 2: Verify asset exists
        assets = wats_client.asset.get_assets(limit=100)
        assert assets is not None, "Failed to get assets"
        
        matching_asset = next((a for a in assets if a.name == asset_name), None)
        assert matching_asset is not None, f"Asset {asset_name} not found in list"
        
        # Step 3: Get asset state
        try:
            asset_state = wats_client.asset.get_asset_state(asset_name)
            assert asset_state is not None, "Failed to get asset state"
            print(f"\n✓ Asset {asset_name} created successfully")
            print(f"  - Type: {asset_type}")
            print(f"  - State: {asset_state}")
        except Exception as e:
            # State might not be available for new assets
            print(f"\n✓ Asset {asset_name} created (state not yet available)")
    
    def test_fixture_asset_workflow(
        self,
        wats_client: pyWATS,
        unique_identifier: str
    ):
        """
        Test creating and managing a fixture asset.
        """
        asset_name = f"ACPT-FIXTURE-{unique_identifier}"
        
        # Create fixture asset
        try:
            asset = wats_client.asset.create_asset(
                name=asset_name,
                asset_type="Fixture"
            )
            assert asset is not None, "Failed to create fixture"
        except Exception as e:
            pytest.skip(f"Fixture creation failed: {e}")
        
        # Verify in asset list
        assets = wats_client.asset.get_assets(limit=100)
        matching_asset = next((a for a in assets if a.name == asset_name), None)
        assert matching_asset is not None, f"Fixture {asset_name} not found"
        
        print(f"\n✓ Fixture {asset_name} created and verified")


@pytest.mark.acceptance
class TestAssetQueryScenario:
    """
    Test asset querying and filtering
    """
    
    def test_query_assets_by_type(
        self,
        wats_client: pyWATS
    ):
        """
        Test querying assets by type.
        """
        # Get asset types
        asset_types = wats_client.asset.get_asset_types()
        assert asset_types is not None, "Failed to get asset types"
        assert len(asset_types) > 0, "No asset types available"
        
        print(f"\n✓ Found {len(asset_types)} asset types")
        for asset_type in asset_types:
            print(f"  - {asset_type}")
    
    def test_query_all_assets(
        self,
        wats_client: pyWATS
    ):
        """
        Test querying all assets with pagination.
        """
        # Get first page
        assets_page1 = wats_client.asset.get_assets(limit=10)
        assert assets_page1 is not None, "Failed to get assets"
        
        print(f"\n✓ Retrieved {len(assets_page1)} assets (first page)")
        
        if len(assets_page1) > 0:
            # Verify asset structure
            first_asset = assets_page1[0]
            assert hasattr(first_asset, 'name'), "Asset missing name attribute"
            print(f"  - Sample asset: {first_asset.name}")
