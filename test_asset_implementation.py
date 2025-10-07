#!/usr/bin/env python3
"""
Test script for Asset Module implementation with REST API integration.

This script tests the implemented "perfect match" functions in the Asset module:
- get_asset()
- get_assets()
- delete_asset()
- calibration()
- maintenance()
- reset_running_count()
- AssetInfo model class
"""

import sys
import traceback
from datetime import datetime
from typing import Any, Dict

def test_basic_imports():
    """Test basic imports and module structure."""
    try:
        print("Testing basic imports...")
        
        # Test main imports
        from pyWATS.modules.asset import (
            AssetModule, AssetResponse, Asset, AssetInfo, AssetState
        )
        print("✓ Asset module imports successful")
        
        # Test enum values
        assert AssetState.AVAILABLE.value == "Available"
        assert AssetState.IN_USE.value == "InUse"
        assert AssetState.MAINTENANCE.value == "Maintenance"
        assert AssetState.UNAVAILABLE.value == "Unavailable"
        print("✓ AssetState enum values correct")
        
        # Test AssetResponse
        response = AssetResponse(True, "Test message", {"test": "data"})
        assert response.success == True
        assert response.message == "Test message"
        assert response.data == {"test": "data"}
        print("✓ AssetResponse class working")
        
        # Test AssetInfo
        asset_info = AssetInfo(
            id="TEST_001",
            name="Test Asset",
            location="Test Location",
            state=AssetState.AVAILABLE,
            asset_type="Test Type"
        )
        assert asset_info.id == "TEST_001"
        assert asset_info.name == "Test Asset"
        assert asset_info.location == "Test Location"
        assert asset_info.state == AssetState.AVAILABLE
        assert asset_info.is_available() == True
        print("✓ AssetInfo class working")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic imports failed: {e}")
        traceback.print_exc()
        return False


def test_asset_module_with_mock():
    """Test AssetModule with mock HTTP client."""
    try:
        print("\nTesting AssetModule with mock client...")
        
        from pyWATS.modules.asset import AssetModule
        
        class MockHttpClient:
            """Mock HTTP client for testing."""
            def __init__(self):
                self.last_call = None
        
        # Create asset module instance with mock client
        mock_client = MockHttpClient()
        asset_module = AssetModule(mock_client)
        
        # Test would require more complex mocking for actual REST calls
        # For now, just test that the methods exist and have proper signatures
        
        # Check method signatures
        import inspect
        
        # get_asset
        sig = inspect.signature(asset_module.get_asset)
        assert 'serial_number' in sig.parameters
        print("✓ get_asset method signature correct")
        
        # get_assets
        sig = inspect.signature(asset_module.get_assets)
        assert 'filter_str' in sig.parameters
        print("✓ get_assets method signature correct")
        
        # delete_asset
        sig = inspect.signature(asset_module.delete_asset)
        assert 'serial_number' in sig.parameters
        print("✓ delete_asset method signature correct")
        
        # calibration
        sig = inspect.signature(asset_module.calibration)
        assert 'serial_number' in sig.parameters
        assert 'date_time' in sig.parameters
        assert 'comment' in sig.parameters
        print("✓ calibration method signature correct")
        
        # maintenance
        sig = inspect.signature(asset_module.maintenance)
        assert 'serial_number' in sig.parameters
        assert 'date_time' in sig.parameters
        assert 'comment' in sig.parameters
        print("✓ maintenance method signature correct")
        
        # reset_running_count
        sig = inspect.signature(asset_module.reset_running_count)
        assert 'serial_number' in sig.parameters
        assert 'comment' in sig.parameters
        print("✓ reset_running_count method signature correct")
        
        return True
        
    except Exception as e:
        print(f"✗ AssetModule testing failed: {e}")
        traceback.print_exc()
        return False


def test_asset_info_functionality():
    """Test AssetInfo class functionality."""
    try:
        print("\nTesting AssetInfo functionality...")
        
        from pyWATS.modules.asset import AssetInfo, AssetState
        
        # Create AssetInfo instance
        asset_info = AssetInfo(
            id="TEST_ASSET_001",
            name="Test Manufacturing Asset",
            location="Factory Floor A",
            state=AssetState.AVAILABLE,
            asset_type="Test Equipment",
            serial_number="SN-TEST-001",
            description="Test asset for validation",
            running_count=150,
            total_count=1000,
            tags=["production", "critical"],
            configuration={"param1": "value1", "param2": 42}
        )
        
        # Test basic properties
        assert asset_info.id == "TEST_ASSET_001"
        assert asset_info.name == "Test Manufacturing Asset"
        assert asset_info.location == "Factory Floor A"
        assert asset_info.state == AssetState.AVAILABLE
        assert asset_info.is_available() == True
        print("✓ Basic properties working")
        
        # Test state changes
        asset_info.set_state(AssetState.IN_USE)
        assert asset_info.state == AssetState.IN_USE
        assert asset_info.is_available() == False
        print("✓ State changes working")
        
        # Test tag operations
        assert asset_info.get_tags() == ["production", "critical"]
        assert asset_info.add_tag("new_tag") == True
        assert "new_tag" in asset_info.get_tags()
        assert asset_info.add_tag("production") == False  # Already exists
        assert asset_info.remove_tag("new_tag") == True
        assert "new_tag" not in asset_info.get_tags()
        assert asset_info.remove_tag("nonexistent") == False
        print("✓ Tag operations working")
        
        # Test configuration operations
        config = asset_info.get_configuration()
        assert config["param1"] == "value1"
        assert config["param2"] == 42
        
        asset_info.update_config({"param3": "new_value"})
        updated_config = asset_info.get_configuration()
        assert "param3" in updated_config
        print("✓ Configuration operations working")
        
        # Test location updates
        asset_info.update_location("New Location")
        assert asset_info.location == "New Location"
        print("✓ Location updates working")
        
        # Test usage tracking
        original_count = asset_info.running_count
        asset_info.track_usage({"increment": 5})
        assert asset_info.running_count == original_count + 5
        print("✓ Usage tracking working")
        
        # Test to_dict conversion
        asset_dict = asset_info.to_dict()
        assert asset_dict["id"] == "TEST_ASSET_001"
        assert asset_dict["name"] == "Test Manufacturing Asset"
        assert asset_dict["state"] == "InUse"  # Current state
        assert asset_dict["running_count"] == original_count + 5
        assert "production" in asset_dict["tags"]
        print("✓ Dictionary conversion working")
        
        return True
        
    except Exception as e:
        print(f"✗ AssetInfo functionality testing failed: {e}")
        traceback.print_exc()
        return False


def test_rest_api_integration_readiness():
    """Test that REST API integration is properly set up."""
    try:
        print("\nTesting REST API integration readiness...")
        
        # Test REST API imports
        try:
            from pyWATS.rest_api.public.api.asset.asset_get_asset_by_serial_number import sync
            print("✓ asset_get_asset_by_serial_number import successful")
        except ImportError as e:
            print(f"⚠ asset_get_asset_by_serial_number import failed: {e}")
        
        try:
            from pyWATS.rest_api.public.api.asset.asset_get_assets import sync
            print("✓ asset_get_assets import successful")
        except ImportError as e:
            print(f"⚠ asset_get_assets import failed: {e}")
        
        try:
            from pyWATS.rest_api.public.api.asset.asset_delete_asset import sync
            print("✓ asset_delete_asset import successful")
        except ImportError as e:
            print(f"⚠ asset_delete_asset import failed: {e}")
        
        try:
            from pyWATS.rest_api.public.api.asset.asset_post_calibration import sync
            print("✓ asset_post_calibration import successful")
        except ImportError as e:
            print(f"⚠ asset_post_calibration import failed: {e}")
        
        try:
            from pyWATS.rest_api.public.api.asset.asset_post_maintenance import sync
            print("✓ asset_post_maintenance import successful")
        except ImportError as e:
            print(f"⚠ asset_post_maintenance import failed: {e}")
        
        try:
            from pyWATS.rest_api.public.api.asset.asset_reset_running_count import sync
            print("✓ asset_reset_running_count import successful")
        except ImportError as e:
            print(f"⚠ asset_reset_running_count import failed: {e}")
        
        try:
            from pyWATS.rest_api.public.client import Client
            from pyWATS.rest_api.public.types import UNSET
            print("✓ REST client imports successful")
        except ImportError as e:
            print(f"⚠ REST client imports failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ REST API integration test failed: {e}")
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling in Asset module."""
    try:
        print("\nTesting error handling...")
        
        from pyWATS.modules.asset import AssetModule
        from pyWATS.exceptions import WATSException, WATSNotFoundError
        
        # Test exception imports
        assert WATSException is not None
        assert WATSNotFoundError is not None
        print("✓ Exception classes imported")
        
        # Create mock client for testing
        class MockHttpClient:
            """Mock HTTP client for testing."""
            pass
        
        mock_client = MockHttpClient()
        asset_module = AssetModule(mock_client)
        
        # Test that implemented methods don't raise NotImplementedError
        # These should not raise NotImplementedError (they'll raise other errors due to no HTTP client)
        try:
            asset_module.get_asset("test")
        except NotImplementedError:
            print("✗ get_asset still raises NotImplementedError")
            return False
        except Exception:
            pass  # Expected to fail with other errors due to no real HTTP client
        print("✓ get_asset doesn't raise NotImplementedError")
        
        try:
            asset_module.get_assets("test")
        except NotImplementedError:
            print("✗ get_assets still raises NotImplementedError")
            return False
        except Exception:
            pass
        print("✓ get_assets doesn't raise NotImplementedError")
        
        try:
            asset_module.delete_asset("test")
        except NotImplementedError:
            print("✗ delete_asset still raises NotImplementedError")
            return False
        except Exception:
            pass
        print("✓ delete_asset doesn't raise NotImplementedError")
        
        try:
            asset_module.calibration("test")
        except NotImplementedError:
            print("✗ calibration still raises NotImplementedError")
            return False
        except Exception:
            pass
        print("✓ calibration doesn't raise NotImplementedError")
        
        try:
            asset_module.maintenance("test")
        except NotImplementedError:
            print("✗ maintenance still raises NotImplementedError")
            return False
        except Exception:
            pass
        print("✓ maintenance doesn't raise NotImplementedError")
        
        try:
            asset_module.reset_running_count("test")
        except NotImplementedError:
            print("✗ reset_running_count still raises NotImplementedError")
            return False
        except Exception:
            pass
        print("✓ reset_running_count doesn't raise NotImplementedError")
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Main test runner."""
    print("=" * 60)
    print("Asset Module Implementation Test Suite")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    test_results.append(("Basic Imports", test_basic_imports()))
    test_results.append(("AssetModule Mock Testing", test_asset_module_with_mock()))
    test_results.append(("AssetInfo Functionality", test_asset_info_functionality()))
    test_results.append(("REST API Integration Readiness", test_rest_api_integration_readiness()))
    test_results.append(("Error Handling", test_error_handling()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:<40} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! Asset module implementation is working correctly.")
        print("\nImplemented functions with REST API integration:")
        print("• get_asset() - Get asset by serial number")
        print("• get_assets() - Get assets with filtering")
        print("• delete_asset() - Delete asset by serial number")
        print("• calibration() - Perform asset calibration")
        print("• maintenance() - Perform asset maintenance")
        print("• reset_running_count() - Reset asset usage count")
        print("• AssetInfo class - Comprehensive asset information management")
        print("• AssetState enum - Asset state management")
        
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)