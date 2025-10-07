"""
Test script for the new WATSApi object-oriented structure.

This script demonstrates the new API design and verifies that all modules
are properly accessible and functional.
"""

import sys
import traceback
from src.pyWATS import WATSApi, PyWATSConfig
from src.pyWATS.exceptions import WATSException


def test_api_initialization():
    """Test API initialization with different methods."""
    print("🧪 Testing API initialization...")
    
    try:
        # Test with configuration
        config = PyWATSConfig()
        api1 = WATSApi(config=config)
        print(f"  ✅ Config initialization: {api1}")
        
        # Test with direct parameters
        api2 = WATSApi(base_url="https://test.wats.com", token="test_token")
        print(f"  ✅ Direct parameter initialization: {api2}")
        
        # Test invalid initialization
        try:
            api3 = WATSApi()
            print("  ❌ Should have failed with no parameters")
        except ValueError as e:
            print(f"  ✅ Properly rejected invalid initialization: {e}")
        
        return api1, api2
        
    except Exception as e:
        print(f"  ❌ API initialization failed: {e}")
        traceback.print_exc()
        return None, None


def test_module_access(api):
    """Test accessing all modules through properties."""
    print("\n🧪 Testing module access...")
    
    if api is None:
        print("  ❌ Cannot test modules - API is None")
        return False
    
    module_tests = [
        ("product", "Product management"),
        ("report", "Report and analytics"),
        ("unit", "Unit/device management"),
        ("workflow", "Workflow management"),
        ("production", "Production tracking"),
        ("asset", "Asset management"),
        ("app", "Application management")
    ]
    
    all_passed = True
    
    for module_name, description in module_tests:
        try:
            module = getattr(api, module_name)
            print(f"  ✅ {module_name}: {description} - {type(module).__name__}")
        except Exception as e:
            print(f"  ❌ {module_name}: Failed to access - {e}")
            all_passed = False
    
    return all_passed


def test_product_module_functionality(api):
    """Test basic Product module functionality.""" 
    print("\n🧪 Testing Product module functionality...")
    
    if api is None:
        print("  ❌ Cannot test product module - API is None")
        return False
    
    try:
        # Test get_all method (should return placeholder for now)
        products = api.product.get_all()
        print(f"  ✅ get_all() returned: {type(products)} with {len(products)} items")
        
        # Test get_count method
        count = api.product.get_count()
        print(f"  ✅ get_count() returned: {count}")
        
        # Test validation for invalid ID
        try:
            api.product.get_by_id("")
            print("  ❌ Should have failed with empty product ID")
        except WATSException as e:
            print(f"  ✅ Properly validated empty product ID: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Product module test failed: {e}")
        traceback.print_exc()
        return False


def test_report_module_functionality(api):
    """Test basic Report module functionality."""
    print("\n🧪 Testing Report module functionality...")
    
    if api is None:
        print("  ❌ Cannot test report module - API is None")
        return False
    
    try:
        # Test getting available reports
        reports = api.report.get_available_reports()
        print(f"  ✅ get_available_reports() returned {len(reports)} report types")
        
        # Test production statistics
        stats = api.report.get_production_statistics()
        print(f"  ✅ get_production_statistics() returned: {stats.get('type', 'unknown')}")
        
        # Test quality metrics
        metrics = api.report.get_quality_metrics()
        print(f"  ✅ get_quality_metrics() returned: {metrics.get('type', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Report module test failed: {e}")
        traceback.print_exc()
        return False


def test_exception_hierarchy():
    """Test custom exception classes."""
    print("\n🧪 Testing exception hierarchy...")
    
    try:
        from src.pyWATS.exceptions import (
            WATSException, WATSAPIError, WATSConnectionError, 
            WATSAuthenticationError, WATSValidationError, WATSNotFoundError
        )
        
        # Test base exception
        base_ex = WATSException("Test message", "TEST001", {"detail": "test"})
        print(f"  ✅ WATSException: {base_ex}")
        
        # Test derived exceptions
        api_ex = WATSAPIError("API error")
        print(f"  ✅ WATSAPIError: {api_ex}")
        
        conn_ex = WATSConnectionError("Connection error")
        print(f"  ✅ WATSConnectionError: {conn_ex}")
        
        # Test inheritance
        assert isinstance(api_ex, WATSException)
        assert isinstance(conn_ex, WATSException)
        print("  ✅ Exception inheritance works correctly")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Exception hierarchy test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 Testing new WATSApi object-oriented structure\n")
    
    # Test API initialization
    api1, api2 = test_api_initialization()
    
    # Test module access
    modules_ok = test_module_access(api1)
    
    # Test Product module functionality  
    product_ok = test_product_module_functionality(api1)
    
    # Test Report module functionality
    report_ok = test_report_module_functionality(api1)
    
    # Test exception hierarchy
    exceptions_ok = test_exception_hierarchy()
    
    # Summary
    print("\n📊 Test Summary:")
    tests = [
        ("API Initialization", api1 is not None and api2 is not None),
        ("Module Access", modules_ok),
        ("Product Module", product_ok),
        ("Report Module", report_ok),
        ("Exception Hierarchy", exceptions_ok)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The new API structure is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)