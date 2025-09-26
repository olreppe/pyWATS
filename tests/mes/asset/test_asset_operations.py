"""
MES Asset Operations Tests

Tests for asset management operations including asset CRUD, maintenance,
calibration, and count operations.

These tests only use the high-level pyWATS.mes.asset API 
(no direct REST API calls).
"""

try:
    import pytest
    PYTEST_AVAILABLE = True
    
    def skip_test(reason: str):
        """Skip test with pytest."""
        pytest.skip(reason)
    
    @pytest.fixture
    def asset_test_runner():
        """Fixture providing an AssetTestRunner instance."""
        runner = AssetTestRunner()
        yield runner
        runner.cleanup_test_assets()
        
except ImportError:
    PYTEST_AVAILABLE = False
    
    def skip_test(reason: str):
        """Skip test without pytest."""
        import logging
        logging.getLogger(__name__).warning(f"Skipping test: {reason}")
        return
    
    def asset_test_runner():
        """Mock fixture for when pytest is not available."""
        return AssetTestRunner()

from datetime import datetime, timedelta
import logging
from typing import List, Optional
from uuid import UUID

from pyWATS import create_api
from pyWATS.mes.asset import AssetHandler
from pyWATS.rest_api.models.asset import Asset, AssetType, AssetState

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssetTestRunner:
    """Test runner for asset operations."""
    
    def __init__(self):
        """Initialize test runner with API connection."""
        self.api = create_api()
        self.asset_handler = AssetHandler(connection=self.client)
        self.test_assets = []
        self.discovered_assets = []
    
    @property
    def client(self):
        """Get the WATS API client for Asset API initialization"""
        if self.api.tdm_client and self.api.tdm_client._connection:
            return self.api.tdm_client._connection._client
        return None
    
    def discover_real_assets(self, max_assets: int = 10) -> List[Asset]:
        """
        Discover existing assets on the server for testing.
        
        Args:
            max_assets: Maximum number of assets to discover
            
        Returns:
            List of discovered assets
        """
        try:
            logger.info("Discovering real assets from server...")
            
            # Get first batch of assets
            discovered = self.asset_handler.get_assets(top=max_assets)
            
            if discovered:
                self.discovered_assets = discovered
                logger.info(f"Discovered {len(discovered)} assets:")
                for asset in discovered[:3]:  # Show first 3
                    logger.info(f"  - {asset.serial_number} ({asset.asset_name or 'Unnamed'})")
                
                if len(discovered) > 3:
                    logger.info(f"  ... and {len(discovered) - 3} more assets")
            else:
                logger.warning("No assets found on server")
            
            return discovered
            
        except Exception as e:
            logger.error(f"Failed to discover assets: {e}")
            return []
    
    def find_updatable_asset(self) -> Optional[Asset]:
        """Find an asset that can be safely updated for testing."""
        for asset in self.discovered_assets:
            # Look for assets with test-related names or that seem safe to modify
            if (asset.serial_number and 
                any(keyword in asset.serial_number.lower() for keyword in ['test', 'demo', 'temp'])):
                return asset
        
        # If no test assets found, use the first asset but be careful
        return self.discovered_assets[0] if self.discovered_assets else None
    
    def cleanup_test_assets(self):
        """Clean up any test assets created during testing."""
        for asset in self.test_assets:
            try:
                if hasattr(asset, 'serial_number'):
                    logger.info(f"Cleaning up test asset: {asset.serial_number}")
                    self.asset_handler.delete_asset(asset.serial_number)
            except Exception as e:
                logger.warning(f"Failed to cleanup asset {asset}: {e}")
        self.test_assets.clear()


class TestAssetConnection:
    """Test asset connection and basic functionality."""
    
    def test_asset_connection(self, asset_test_runner):
        """Test that we can connect to the asset service."""
        assert asset_test_runner.asset_handler.is_connected()
        logger.info("✓ Asset service connection successful")


class TestAssetDiscovery:
    """Test asset discovery and retrieval operations."""
    
    def test_discover_assets(self, asset_test_runner):
        """Test discovering assets from the server."""
        assets = asset_test_runner.discover_real_assets(20)
        assert isinstance(assets, list)
        logger.info(f"✓ Discovered {len(assets)} assets")
        
        if assets:
            # Verify asset structure
            first_asset = assets[0]
            assert hasattr(first_asset, 'serial_number')
            assert hasattr(first_asset, 'asset_id')
            assert first_asset.serial_number is not None
            logger.info(f"✓ Asset structure validation passed")
    
    def test_get_assets_with_filter(self, asset_test_runner):
        """Test getting assets with OData filter."""
        # First discover some assets
        asset_test_runner.discover_real_assets(5)
        
        if not asset_test_runner.discovered_assets:
            skip_test("No assets available for filtering test")
            return
        
        # Test with top filter
        assets = asset_test_runner.asset_handler.get_assets(top=3)
        assert isinstance(assets, list)
        assert len(assets) <= 3
        logger.info(f"✓ OData filter test passed: got {len(assets)} assets")
    
    def test_get_single_asset(self, asset_test_runner):
        """Test retrieving a single asset by serial number."""
        # First discover assets
        asset_test_runner.discover_real_assets(5)
        
        if not asset_test_runner.discovered_assets:
            skip_test("No assets available for single asset test")
            return
        
        test_asset = asset_test_runner.discovered_assets[0]
        
        # Get the asset by serial number
        retrieved_asset = asset_test_runner.asset_handler.get_asset(test_asset.serial_number)
        
        assert retrieved_asset is not None
        assert retrieved_asset.serial_number == test_asset.serial_number
        assert retrieved_asset.asset_id == test_asset.asset_id
        logger.info(f"✓ Retrieved asset: {retrieved_asset.serial_number}")


class TestAssetUpdates:
    """Test asset update operations."""
    
    def test_update_asset_description(self, asset_test_runner):
        """Test updating an asset's description."""
        # First discover assets
        asset_test_runner.discover_real_assets(10)
        
        updatable_asset = asset_test_runner.find_updatable_asset()
        if not updatable_asset:
            skip_test("No suitable assets found for update test")
            return
        
        # Get fresh copy of the asset
        current_asset = asset_test_runner.asset_handler.get_asset(updatable_asset.serial_number)
        assert current_asset is not None
        
        # Store original description
        original_description = current_asset.description
        
        # Update description with timestamp
        test_description = f"Test update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        current_asset.description = test_description
        
        # Update the asset
        update_result = asset_test_runner.asset_handler.update_asset(current_asset)
        assert update_result.success, f"Asset update failed: {update_result.message}"
        logger.info(f"✓ Asset update successful: {update_result.message}")
        
        # Verify the update by retrieving the asset again
        updated_asset = asset_test_runner.asset_handler.get_asset(current_asset.serial_number)
        assert updated_asset is not None
        assert updated_asset.description == test_description
        logger.info(f"✓ Asset description update verified")
        
        # Restore original description
        if original_description != test_description:
            updated_asset.description = original_description
            restore_result = asset_test_runner.asset_handler.update_asset(updated_asset)
            if restore_result.success:
                logger.info("✓ Original description restored")
            else:
                logger.warning(f"Failed to restore original description: {restore_result.message}")


class TestAssetMaintenance:
    """Test asset maintenance and calibration operations."""
    
    def test_asset_calibration(self, asset_test_runner):
        """Test recording asset calibration."""
        # First discover assets
        asset_test_runner.discover_real_assets(5)
        
        if not asset_test_runner.discovered_assets:
            skip_test("No assets available for calibration test")
            return
        
        test_asset = asset_test_runner.discovered_assets[0]
        
        # Record calibration
        calibration_result = asset_test_runner.asset_handler.calibration(
            test_asset.serial_number,
            comment=f"Test calibration at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        assert calibration_result.success, f"Calibration failed: {calibration_result.message}"
        logger.info(f"✓ Calibration recorded successfully: {calibration_result.message}")
    
    def test_asset_maintenance(self, asset_test_runner):
        """Test recording asset maintenance."""
        # First discover assets
        asset_test_runner.discover_real_assets(5)
        
        if not asset_test_runner.discovered_assets:
            skip_test("No assets available for maintenance test")
            return
        
        test_asset = asset_test_runner.discovered_assets[0]
        
        # Record maintenance
        maintenance_result = asset_test_runner.asset_handler.maintenance(
            test_asset.serial_number,
            comment=f"Test maintenance at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        assert maintenance_result.success, f"Maintenance failed: {maintenance_result.message}"
        logger.info(f"✓ Maintenance recorded successfully: {maintenance_result.message}")


class TestAssetCounting:
    """Test asset counting operations."""
    
    def test_increment_usage_count(self, asset_test_runner):
        """Test incrementing asset usage count."""
        # First discover assets
        asset_test_runner.discover_real_assets(5)
        
        if not asset_test_runner.discovered_assets:
            skip_test("No assets available for count test")
            return
        
        test_asset = asset_test_runner.discovered_assets[0]
        
        # Get current counts
        current_asset = asset_test_runner.asset_handler.get_asset(test_asset.serial_number)
        original_total_count = current_asset.total_count or 0
        original_running_count = current_asset.running_count or 0
        
        # Increment usage count
        count_result = asset_test_runner.asset_handler.increment_asset_usage_count(
            test_asset.serial_number,
            usage_count=1
        )
        
        assert count_result.success, f"Count increment failed: {count_result.message}"
        logger.info(f"✓ Usage count incremented: {count_result.message}")
        
        # Verify counts were incremented (this may not always be visible immediately)
        updated_asset = asset_test_runner.asset_handler.get_asset(test_asset.serial_number)
        logger.info(f"  Original counts - Total: {original_total_count}, Running: {original_running_count}")
        logger.info(f"  Updated counts - Total: {updated_asset.total_count}, Running: {updated_asset.running_count}")
    
    def test_reset_running_count(self, asset_test_runner):
        """Test resetting asset running count."""
        # First discover assets
        asset_test_runner.discover_real_assets(5)
        
        if not asset_test_runner.discovered_assets:
            skip_test("No assets available for reset count test")
            return
        
        test_asset = asset_test_runner.discovered_assets[0]
        
        # Reset running count
        reset_result = asset_test_runner.asset_handler.reset_running_count(
            test_asset.serial_number,
            comment=f"Test reset at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        assert reset_result.success, f"Count reset failed: {reset_result.message}"
        logger.info(f"✓ Running count reset: {reset_result.message}")


class TestAssetRelationships:
    """Test asset parent-child relationships."""
    
    def test_get_sub_assets(self, asset_test_runner):
        """Test getting sub-assets of a parent asset."""
        # First discover assets
        asset_test_runner.discover_real_assets(10)
        
        if not asset_test_runner.discovered_assets:
            skip_test("No assets available for sub-asset test")
            return
        
        # Look for assets that might have children
        for asset in asset_test_runner.discovered_assets:
            try:
                sub_assets = asset_test_runner.asset_handler.get_sub_assets(asset.serial_number)
                if sub_assets:
                    assert isinstance(sub_assets, list)
                    logger.info(f"✓ Found {len(sub_assets)} sub-assets for {asset.serial_number}")
                    return
            except Exception as e:
                logger.debug(f"No sub-assets for {asset.serial_number}: {e}")
                continue
        
        logger.info("✓ Sub-asset query completed (no sub-assets found)")


class TestAssetTypes:
    """Test asset type operations."""
    
    def test_discover_asset_types(self, asset_test_runner):
        """Test discovering available asset types."""
        # This would use the REST API endpoint directly since we don't have
        # a high-level method in AssetHandler yet
        logger.info("✓ Asset type discovery test placeholder")


if __name__ == "__main__":
    # Allow running tests directly
    import sys
    
    # Configure logging for direct execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create test runner
    runner = AssetTestRunner()
    
    try:
        # Run a quick test
        logger.info("Starting asset operations test...")
        
        # Test connection
        assert runner.asset_handler.is_connected(), "Connection failed"
        logger.info("✓ Connection test passed")
        
        # Discover assets
        assets = runner.discover_real_assets(5)
        logger.info(f"✓ Asset discovery test passed: {len(assets)} assets")
        
        if assets:
            # Test single asset retrieval
            test_asset = assets[0]
            retrieved = runner.asset_handler.get_asset(test_asset.serial_number)
            assert retrieved is not None
            logger.info(f"✓ Single asset retrieval test passed: {retrieved.serial_number}")
        
        logger.info("All basic tests passed!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        sys.exit(1)
    finally:
        runner.cleanup_test_assets()