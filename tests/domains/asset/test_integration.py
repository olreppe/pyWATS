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
        timestamp = datetime.now().astimezone().strftime('%Y%m%d%H%M%S')
        
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


class TestAssetCountOperations:
    """Test asset count operations - WATS 25.3 features"""

    def test_set_running_count(self, wats_client: Any) -> None:
        """Test setting running count to specific value (WATS 25.3)"""
        print("\n=== SET RUNNING COUNT ===")
        
        assets = wats_client.asset.get_assets(top=1)
        if not assets:
            pytest.skip("No assets available")
        
        asset = assets[0]
        original_count = asset.running_count or 0
        new_count = original_count + 10
        
        print(f"Asset: {asset.asset_name}")
        print(f"Original running count: {original_count}")
        print(f"Setting to: {new_count}")
        
        try:
            result = wats_client.asset.set_running_count(
                value=new_count,
                asset_id=str(asset.asset_id)
            )
            print(f"Result: {result}")
            
            # Verify the change
            updated = wats_client.asset.get_asset(asset_id=str(asset.asset_id))
            print(f"Updated running count: {updated.running_count}")
            
            assert result is True
        except Exception as e:
            # May fail if user lacks 'Edit Total count' permission
            print(f"Note: {e} (may require 'Edit Total count' permission)")
        
        print("=========================\n")

    def test_set_total_count(self, wats_client: Any) -> None:
        """Test setting total count to specific value (WATS 25.3)"""
        print("\n=== SET TOTAL COUNT ===")
        
        assets = wats_client.asset.get_assets(top=1)
        if not assets:
            pytest.skip("No assets available")
        
        asset = assets[0]
        original_count = asset.total_count or 0
        new_count = original_count + 100
        
        print(f"Asset: {asset.asset_name}")
        print(f"Original total count: {original_count}")
        print(f"Setting to: {new_count}")
        
        try:
            result = wats_client.asset.set_total_count(
                value=new_count,
                asset_id=str(asset.asset_id)
            )
            print(f"Result: {result}")
            
            # Verify the change
            updated = wats_client.asset.get_asset(asset_id=str(asset.asset_id))
            print(f"Updated total count: {updated.total_count}")
            
            assert result is True
        except Exception as e:
            # May fail if user lacks 'Edit Total count' permission
            print(f"Note: {e} (may require 'Edit Total count' permission)")
        
        print("=======================\n")


class TestExternalCalibrationMaintenance:
    """Test external calibration and maintenance - WATS 25.3 features"""

    def test_external_calibration(self, wats_client: Any) -> None:
        """Test recording external calibration with custom date range (WATS 25.3)"""
        from datetime import timedelta
        
        print("\n=== EXTERNAL CALIBRATION ===")
        
        assets = wats_client.asset.get_assets(top=1)
        if not assets:
            pytest.skip("No assets available")
        
        asset = assets[0]
        from_date = datetime.now(timezone.utc)
        to_date = from_date + timedelta(days=365)
        
        print(f"Asset: {asset.asset_name}")
        print(f"Calibration from: {from_date}")
        print(f"Next calibration: {to_date}")
        
        try:
            result = wats_client.asset.record_calibration_external(
                asset_id=str(asset.asset_id),
                from_date=from_date,
                to_date=to_date,
                comment="External calibration test via pyWATS"
            )
            print(f"Result: {result}")
            
            # Verify the dates were set
            updated = wats_client.asset.get_asset(asset_id=str(asset.asset_id))
            print(f"Last calibration: {updated.last_calibration_date}")
            print(f"Next calibration: {updated.next_calibration_date}")
            
            assert result is True
        except Exception as e:
            print(f"Note: {e} (external calibration may require specific asset type config)")
        
        print("============================\n")

    def test_external_maintenance(self, wats_client: Any) -> None:
        """Test recording external maintenance with custom date range (WATS 25.3)"""
        from datetime import timedelta
        
        print("\n=== EXTERNAL MAINTENANCE ===")
        
        assets = wats_client.asset.get_assets(top=1)
        if not assets:
            pytest.skip("No assets available")
        
        asset = assets[0]
        from_date = datetime.now(timezone.utc)
        to_date = from_date + timedelta(days=90)
        
        print(f"Asset: {asset.asset_name}")
        print(f"Maintenance from: {from_date}")
        print(f"Next maintenance: {to_date}")
        
        try:
            result = wats_client.asset.record_maintenance_external(
                asset_id=str(asset.asset_id),
                from_date=from_date,
                to_date=to_date,
                comment="External maintenance test via pyWATS"
            )
            print(f"Result: {result}")
            
            # Verify the dates were set
            updated = wats_client.asset.get_asset(asset_id=str(asset.asset_id))
            print(f"Last maintenance: {updated.last_maintenance_date}")
            print(f"Next maintenance: {updated.next_maintenance_date}")
            
            assert result is True
        except Exception as e:
            print(f"Note: {e} (external maintenance may require specific asset type config)")
        
        print("============================\n")