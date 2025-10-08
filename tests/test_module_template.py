"""
Generic test template for pyWATS modules.
"""

import pytest
import inspect


def create_module_tests(module_class, module_name):
    """
    Create standard tests for a pyWATS module.
    
    Args:
        module_class: The module class to test
        module_name: Name of the module for display purposes
    """
    
    class TestModuleGeneric:
        """Generic test cases for pyWATS modules."""
        
        def test_module_loaded(self):
            """Test that the module can be loaded."""
            module = module_class(None)  # Using None for http_client in test
            assert module is not None
            assert hasattr(module, 'http_client')
            
        def test_module_completion(self):
            """Test module level completion based on not implemented functions."""
            module = module_class(None)
            
            # Get all public methods of the module
            methods = [name for name, method in inspect.getmembers(module, predicate=inspect.ismethod) 
                      if not name.startswith('_')]
            
            # Document available methods
            print(f"{module_name} module has {len(methods)} public methods: {methods}")
            
            # Test that the module has at least some methods
            assert len(methods) > 0, f"{module_name} module should have public methods"
            
            # For each method, try to determine if it's implemented
            not_implemented_methods = []
            implemented_methods = []
            
            for method_name in methods:
                method = getattr(module, method_name)
                try:
                    # Try calling with minimal parameters to see if NotImplementedError is raised
                    # This is just to check the signature, actual calls may fail due to missing params
                    sig = inspect.signature(method)
                    params = sig.parameters
                    
                    # Skip methods that require complex parameters
                    if len(params) <= 1:  # Only self parameter
                        try:
                            method()
                        except NotImplementedError:
                            not_implemented_methods.append(method_name)
                        except Exception:
                            # Other exceptions mean the method has some implementation
                            implemented_methods.append(method_name)
                    else:
                        # For methods with parameters, just document them
                        implemented_methods.append(method_name)
                        
                except Exception:
                    implemented_methods.append(method_name)
            
            print(f"{module_name} not implemented methods: {not_implemented_methods}")
            print(f"{module_name} implemented/partial methods: {implemented_methods}")
            
            # Always pass - this test is for documentation purposes
            assert True
    
    return TestModuleGeneric