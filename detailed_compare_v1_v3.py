"""
Detailed comparison of V1 and V3 report models.
Focuses on functional differences, not cosmetic type annotations.
"""
import inspect
import importlib
import pkgutil
from typing import get_type_hints

def get_all_classes(package_name):
    """Get all classes from a package and its submodules"""
    classes = {}
    try:
        package = importlib.import_module(package_name)
        
        # Get classes from main package
        for name, obj in inspect.getmembers(package, inspect.isclass):
            if not name.startswith('_') and obj.__module__.startswith(package_name):
                classes[name] = {
                    'class': obj,
                    'module': obj.__module__,
                }
        
        # Walk through all submodules
        if hasattr(package, '__path__'):
            for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package_name + '.'):
                try:
                    module = importlib.import_module(modname)
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if not name.startswith('_') and obj.__module__ == modname:
                            classes[name] = {
                                'class': obj,
                                'module': obj.__module__,
                            }
                except Exception:
                    pass
    except Exception as e:
        print(f'Error loading package {package_name}: {e}')
    
    return classes

def get_public_methods(cls):
    """Get all public methods (excluding inherited from object/BaseModel)"""
    methods = {}
    for name, obj in inspect.getmembers(cls):
        if not name.startswith('_') and callable(obj):
            # Skip if defined in object or common base classes
            if hasattr(object, name):
                continue
            methods[name] = obj
    return methods

def get_method_params(method):
    """Get method parameter names (excluding 'self')"""
    try:
        sig = inspect.signature(method)
        return [p for p in sig.parameters.keys() if p != 'self']
    except:
        return []

print("="*80)
print("COMPREHENSIVE V1 vs V3 COMPARISON")
print("="*80)

# Get all classes
v1_classes = get_all_classes('pywats.domains.report.report_models')
v3_classes = get_all_classes('pywats.domains.report.report_models_v3')

print(f"\nV1 has {len(v1_classes)} classes")
print(f"V3 has {len(v3_classes)} classes")

# Classes only in one version
only_v1 = set(v1_classes.keys()) - set(v3_classes.keys())
only_v3 = set(v3_classes.keys()) - set(v1_classes.keys())

# Filter out known type imports and base classes
known_imports = {'ABC', 'Any', 'BaseModel', 'Enum', 'Union', 'UUID', 'datetime', 'timezone'}
only_v1 = only_v1 - known_imports
only_v3 = only_v3 - known_imports

if only_v1:
    print("\n" + "="*80)
    print("CLASSES ONLY IN V1:")
    print("="*80)
    for name in sorted(only_v1):
        print(f"  - {name:40} (from {v1_classes[name]['module']})")

if only_v3:
    print("\n" + "="*80)
    print("CLASSES ONLY IN V3:")
    print("="*80)
    for name in sorted(only_v3):
        print(f"  - {name:40} (from {v3_classes[name]['module']})")

# Compare common classes
common_classes = set(v1_classes.keys()) & set(v3_classes.keys())

print(f"\n{'='*80}")
print(f"COMPARING {len(common_classes)} COMMON CLASSES")
print("="*80)

functional_differences = []

for class_name in sorted(common_classes):
    v1_cls = v1_classes[class_name]['class']
    v3_cls = v3_classes[class_name]['class']
    
    v1_methods = get_public_methods(v1_cls)
    v3_methods = get_public_methods(v3_cls)
    
    only_v1_methods = set(v1_methods.keys()) - set(v3_methods.keys())
    only_v3_methods = set(v3_methods.keys()) - set(v1_methods.keys())
    
    # Filter out common pydantic/enum methods that don't matter
    pydantic_methods = {
        'model_dump', 'model_dump_json', 'model_validate', 'model_validate_json',
        'model_copy', 'model_fields', 'model_json_schema', 'model_rebuild',
        'model_construct', 'model_fields_set', 'model_extra', 'model_config',
        'parse_obj', 'parse_raw', 'parse_file', 'dict', 'json', 'copy', 'update_forward_refs',
        'construct', 'schema', 'schema_json', 'validate', '__class_getitem__',
        # String/Enum methods
        'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs',
        'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii',
        'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable',
        'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans',
        'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex',
        'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith',
        'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill'
    }
    
    only_v1_methods = only_v1_methods - pydantic_methods
    only_v3_methods = only_v3_methods - pydantic_methods
    
    if only_v1_methods or only_v3_methods:
        functional_differences.append({
            'class': class_name,
            'only_v1': sorted(only_v1_methods),
            'only_v3': sorted(only_v3_methods),
            'v1_module': v1_classes[class_name]['module'],
            'v3_module': v3_classes[class_name]['module'],
        })
    
    # Check parameter differences for common methods
    common_methods = set(v1_methods.keys()) & set(v3_methods.keys())
    for method_name in common_methods:
        # Skip pydantic internal methods
        if method_name in pydantic_methods:
            continue
            
        v1_params = get_method_params(v1_methods[method_name])
        v3_params = get_method_params(v3_methods[method_name])
        
        if v1_params != v3_params:
            functional_differences.append({
                'class': class_name,
                'method': method_name,
                'v1_params': v1_params,
                'v3_params': v3_params,
            })

# Print functional differences
if functional_differences:
    print("\n" + "="*80)
    print("FUNCTIONAL DIFFERENCES FOUND:")
    print("="*80)
    
    for diff in functional_differences:
        if 'method' in diff:
            # Parameter difference
            print(f"\n{diff['class']}.{diff['method']}() - PARAMETER MISMATCH:")
            print(f"  V1 params: {diff['v1_params']}")
            print(f"  V3 params: {diff['v3_params']}")
        else:
            # Method presence difference
            print(f"\n{diff['class']}:")
            if diff['only_v1']:
                print(f"  Methods ONLY in V1: {diff['only_v1']}")
            if diff['only_v3']:
                print(f"  Methods ONLY in V3: {diff['only_v3']}")
else:
    print("\n✅ No functional differences found!")

print("\n" + "="*80)
print("COMPARISON COMPLETE")
print("="*80)
