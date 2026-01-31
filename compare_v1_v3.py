import inspect
import importlib
import pkgutil

def get_all_classes(package_name):
    """Get all classes from a package and its submodules"""
    classes = {}
    try:
        package = importlib.import_module(package_name)
        
        # Get classes from main package
        for name, obj in inspect.getmembers(package, inspect.isclass):
            if not name.startswith('_'):
                classes[name] = {
                    'class': obj,
                    'module': obj.__module__,
                    'file': inspect.getfile(obj) if hasattr(obj, '__module__') else 'unknown'
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
                                'file': inspect.getfile(obj) if hasattr(obj, '__module__') else 'unknown'
                            }
                except Exception as e:
                    pass
    except Exception as e:
        print(f'Error loading package {package_name}: {e}')
    
    return classes

# Get all classes from V1 and V3
v1_classes = get_all_classes('pywats.domains.report.report_models')
v3_classes = get_all_classes('pywats.domains.report.report_models_v3')

print(f'V1 has {len(v1_classes)} classes')
print(f'V3 has {len(v3_classes)} classes')
print()

# Find classes only in V1
only_v1 = set(v1_classes.keys()) - set(v3_classes.keys())
if only_v1:
    print('CLASSES ONLY IN V1:')
    for name in sorted(only_v1):
        print(f'  - {name} (from {v1_classes[name]["module"]})')
    print()

# Find classes only in V3
only_v3 = set(v3_classes.keys()) - set(v1_classes.keys())
if only_v3:
    print('CLASSES ONLY IN V3:')
    for name in sorted(only_v3):
        print(f'  - {name} (from {v3_classes[name]["module"]})')
    print()

# Compare common classes
common_classes = set(v1_classes.keys()) & set(v3_classes.keys())
print(f'COMMON CLASSES TO COMPARE: {len(common_classes)}')
print()

# Now compare methods for common classes
differences = []
for class_name in sorted(common_classes):
    v1_cls = v1_classes[class_name]['class']
    v3_cls = v3_classes[class_name]['class']
    
    # Get public methods
    v1_methods = {name: obj for name, obj in inspect.getmembers(v1_cls) 
                  if callable(obj) and not name.startswith('_')}
    v3_methods = {name: obj for name, obj in inspect.getmembers(v3_cls) 
                  if callable(obj) and not name.startswith('_')}
    
    only_v1_methods = set(v1_methods.keys()) - set(v3_methods.keys())
    only_v3_methods = set(v3_methods.keys()) - set(v1_methods.keys())
    
    if only_v1_methods:
        differences.append(f'{class_name}: Methods ONLY in V1: {sorted(only_v1_methods)}')
    if only_v3_methods:
        differences.append(f'{class_name}: Methods ONLY in V3: {sorted(only_v3_methods)}')
    
    # Compare method signatures for common methods
    common_methods = set(v1_methods.keys()) & set(v3_methods.keys())
    for method_name in common_methods:
        try:
            v1_sig = inspect.signature(v1_methods[method_name])
            v3_sig = inspect.signature(v3_methods[method_name])
            
            if str(v1_sig) != str(v3_sig):
                differences.append(f'{class_name}.{method_name}(): SIGNATURE DIFF\\n  V1: {v1_sig}\\n  V3: {v3_sig}')
        except:
            pass

if differences:
    print('METHOD/SIGNATURE DIFFERENCES:')
    for diff in differences:
        print(f'  {diff}')
else:
    print('All common classes have identical methods and signatures!')
