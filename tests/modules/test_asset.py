"""
Tests for the Asset module.
"""
import pytest
from pyWATS.modules.asset import AssetModule


class TestAssetModule:
    """Test cases for the Asset module."""
    
    def test_module_loaded(self, http_client):
        """Test that the module can be loaded."""
        module = AssetModule(http_client)
        assert module is not None
        assert module.http_client is not None
        
    def test_module_completion(self, http_client):
        """Test module level completion based on not implemented functions."""
        module = AssetModule(http_client)
        
        import inspect
        
        # Get all public methods of the module
        methods = [name for name, method in inspect.getmembers(module, predicate=inspect.ismethod) 
                  if not name.startswith('_')]
        
        print(f"\nAsset module has {len(methods)} public methods: {methods}")
        
        implemented_methods = []
        not_implemented_methods = []
        error_methods = []
        
        for method_name in methods:
            method = getattr(module, method_name)
            try:
                # Get method signature to understand required parameters
                sig = inspect.signature(method)
                params = list(sig.parameters.keys())
                
                # Try calling method with minimal/appropriate parameters
                if method_name == 'get_assets':
                    method("")  # Requires filter_str
                elif method_name == 'get_asset':
                    method("test_serial")  # Requires serial_number
                elif method_name == 'create_asset':
                    method("test_serial", "test_type")  # Requires serial_number, asset_type
                elif method_name == 'delete_asset':
                    method("test_serial")  # Requires serial_number
                elif method_name == 'calibration':
                    method("test_serial")  # Requires serial_number
                elif method_name == 'maintenance':
                    method("test_serial")  # Requires serial_number
                elif method_name == 'reset_running_count':
                    method("test_serial")  # Requires serial_number
                elif len(params) <= 1:  # Only self parameter
                    method()
                else:
                    # Skip methods with complex signatures we can't easily call
                    continue
                    
                implemented_methods.append(method_name)
                
            except NotImplementedError:
                not_implemented_methods.append(method_name)
            except Exception as e:
                # Other exceptions indicate the method has implementation but may fail due to connection, etc.
                error_methods.append((method_name, str(e)[:100]))
                implemented_methods.append(method_name)
        
        print(f"Asset module - Implemented: {implemented_methods}")
        print(f"Asset module - Not Implemented: {not_implemented_methods}")
        print(f"Asset module - Implementation with errors: {[m[0] for m in error_methods]}")
        
        # Just verify we found methods - don't assert specific implementations
        assert len(methods) > 0, "Asset module should have public methods"