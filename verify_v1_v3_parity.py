"""
Final V1/V3 Parity Check

Verifies that V3 has all the classes from V1 that should be present.
"""
import importlib
import inspect
from typing import Set, Dict

def get_classes_from_module(module_name: str) -> Dict[str, type]:
    """Get all classes from a module."""
    try:
        module = importlib.import_module(module_name)
        classes = {}
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and obj.__module__.startswith(module_name.split('.')[0]):
                classes[name] = obj
        return classes
    except Exception as e:
        print(f"Error loading {module_name}: {e}")
        return {}

def main():
    print("=" * 80)
    print("V1/V3 PARITY CHECK - FINAL VERIFICATION")
    print("=" * 80)
    
    # Get all V1 classes
    v1_models = get_classes_from_module("pywats.domains.report.report_models")
    print(f"\nV1 has {len(v1_models)} classes")
    
    # Get all V3 classes
    v3_models = get_classes_from_module("pywats.domains.report.report_models_v3")
    print(f"V3 has {len(v3_models)} classes")
    
    # Classes to skip (design differences, not needed, or renamed)
    skip_classes = {
        'ContextType',  # User said drop this
        'DeserializationContext',  # Related to ContextType - drop as well
        'LimitMeasurement', 'Measurement',  # Design matter - V3 has different architecture
        'SubRepair',  # Different design in V3
        'BaseMeasurement', 'SingleMeasurementMixin',  # V3 implementation details
        'PassFailStep', 'StringValueStep',  # Renamed in V3 (V1 equivalents exist)
        'UURMiscInfo', 'UUTSubUnit',  # V3 specialized subclasses
    }
    
    # Classes that were renamed
    renamed_classes = {
        'ReportResult': 'ReportStatus',  # V3 uses ReportStatus (with ReportResult alias)
    }
    
    print("\n" + "=" * 80)
    print("CHECKING V1 CLASSES IN V3")
    print("=" * 80)
    
    missing_in_v3 = []
    found_in_v3 = []
    
    for class_name in sorted(v1_models.keys()):
        if class_name in skip_classes:
            print(f"✓ {class_name:40} - SKIPPED (design difference)")
            continue
            
        # Check if renamed
        check_name = renamed_classes.get(class_name, class_name)
        
        if check_name in v3_models:
            found_in_v3.append(class_name)
            if check_name != class_name:
                print(f"✓ {class_name:40} - FOUND as {check_name}")
            else:
                print(f"✓ {class_name:40} - FOUND")
        else:
            missing_in_v3.append(class_name)
            print(f"✗ {class_name:40} - MISSING")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"V1 classes checked: {len(v1_models)}")
    print(f"Found in V3: {len(found_in_v3)}")
    print(f"Skipped (design): {len(skip_classes)}")
    print(f"Missing in V3: {len(missing_in_v3)}")
    
    if missing_in_v3:
        print("\n" + "!" * 80)
        print("MISSING CLASSES:")
        for name in missing_in_v3:
            print(f"  - {name}")
        print("!" * 80)
        return False
    else:
        print("\n" + "=" * 80)
        print("✓ ALL V1 CLASSES ACCOUNTED FOR IN V3!")
        print("=" * 80)
        return True

if __name__ == "__main__":
    import sys
    sys.path.insert(0, "src")
    success = main()
    sys.exit(0 if success else 1)
