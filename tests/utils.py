"""
Test utilities for pyWATS module testing.
"""

import inspect


def test_module_implementation_status(module, module_name):
    """
    Test a module's implementation status by checking which methods raise NotImplementedError.
    
    Args:
        module: The module instance to test
        module_name: Name of the module for reporting
        
    Returns:
        dict: Summary of implementation status
    """
    # Get all public methods of the module
    methods = [name for name, method in inspect.getmembers(module, predicate=inspect.ismethod) 
              if not name.startswith('_')]
    
    print(f"\n{module_name} module has {len(methods)} public methods: {methods}")
    
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
    
    print(f"{module_name} module - Implemented: {implemented_methods}")
    print(f"{module_name} module - Not Implemented: {not_implemented_methods}")
    print(f"{module_name} module - Implementation with errors: {[m[0] for m in error_methods]}")
    
    return {
        'total_methods': len(methods),
        'implemented': implemented_methods,
        'not_implemented': not_implemented_methods,
        'errors': error_methods,
        'methods': methods
    }