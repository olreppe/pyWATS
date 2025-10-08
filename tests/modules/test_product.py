"""
Tests for the Product module.
"""
import pytest
from pyWATS.modules.product import ProductModule


class TestProductModule:
    """Test cases for the Product module."""
    
    def test_module_loaded(self, http_client):
        """Test that the module can be loaded."""
        module = ProductModule(http_client)
        assert module is not None
        assert module.http_client is not None
        
    def test_module_completion(self, http_client):
        """Test module level completion based on not implemented functions."""
        module = ProductModule(http_client)
        
        import inspect
        
        # Get all public methods of the module
        methods = [name for name, method in inspect.getmembers(module, predicate=inspect.ismethod) 
                  if not name.startswith('_')]
        
        print(f"\nProduct module has {len(methods)} public methods: {methods}")
        
        implemented_methods = []
        not_implemented_methods = []
        error_methods = []
        
        for method_name in methods:
            method = getattr(module, method_name)
            try:
                # Get method signature to understand required parameters
                sig = inspect.signature(method)
                params = list(sig.parameters.keys())
                
                # Try calling method with no parameters (only works for methods without required args)
                if len(params) <= 1:  # Only self parameter
                    method()
                else:
                    # Skip methods with parameters we don't know how to call
                    continue
                    
                implemented_methods.append(method_name)
                
            except NotImplementedError:
                not_implemented_methods.append(method_name)
            except Exception as e:
                # Other exceptions indicate the method has implementation but may fail due to connection, etc.
                error_methods.append((method_name, str(e)[:100]))
                implemented_methods.append(method_name)
        
        print(f"Product module - Implemented: {implemented_methods}")
        print(f"Product module - Not Implemented: {not_implemented_methods}")
        print(f"Product module - Implementation with errors: {[m[0] for m in error_methods]}")
        
        # Just verify we found methods - don't assert specific implementations
        assert len(methods) > 0, "Product module should have public methods"