"""
Comprehensive V1 vs V3 Report Model Comparison
V1 is the REFERENCE - we check what's MISSING in V3
"""
import sys
sys.path.insert(0, 'src')

from pywats.domains.report.report_models import UUTReport as V1UUT, UURReport as V1UUR
from pywats.domains.report.report_models_v3 import UUTReport as V3UUT, UURReport as V3UUR
from pydantic.fields import FieldInfo
import inspect

def get_all_fields_with_aliases(cls, prefix=''):
    '''Get all fields including inherited ones with their aliases'''
    fields = {}
    for name, field_info in cls.model_fields.items():
        field_name = f'{prefix}{name}' if prefix else name
        
        # Get aliases
        val_alias = getattr(field_info, 'validation_alias', None)
        ser_alias = getattr(field_info, 'serialization_alias', None)
        
        aliases = []
        if val_alias: 
            aliases.append(f'val:{val_alias}')
        if ser_alias: 
            aliases.append(f'ser:{ser_alias}')
        
        field_type = field_info.annotation
        type_str = str(field_type).replace('typing.', '').replace('pywats.domains.report.report_models.', 'V1.').replace('pywats.domains.report.report_models_v3.', 'V3.')
        
        fields[field_name] = {
            'type': type_str,
            'aliases': aliases,
            'required': field_info.is_required()
        }
    return fields

def get_methods(cls):
    '''Get all methods and properties'''
    methods = {}
    for name, obj in inspect.getmembers(cls):
        if name.startswith('_'):
            continue
        if isinstance(obj, property):
            methods[name] = 'property'
        elif inspect.ismethod(obj) or inspect.isfunction(obj):
            if name not in ['model_validate', 'model_dump', 'model_fields', 'model_config']:
                methods[name] = 'method'
    return methods

print('=' * 80)
print('V1 vs V3 REPORT MODEL COMPARISON')
print('V1 = REFERENCE (what we want), V3 = IMPLEMENTATION (what might be missing)')
print('=' * 80)

print('\n' + '=' * 80)
print('UUTReport COMPARISON')
print('=' * 80)

v1_uut_fields = get_all_fields_with_aliases(V1UUT)
v1_uut_methods = get_methods(V1UUT)
v3_uut_fields = get_all_fields_with_aliases(V3UUT)
v3_uut_methods = get_methods(V3UUT)

print(f'\nV1 UUTReport: {len(v1_uut_fields)} fields, {len(v1_uut_methods)} methods/properties')
print(f'V3 UUTReport: {len(v3_uut_fields)} fields, {len(v3_uut_methods)} methods/properties')

# Field comparison
print('\n--- FIELD COMPARISON ---')
v1_field_names = set(v1_uut_fields.keys())
v3_field_names = set(v3_uut_fields.keys())

# Build V3 alias map
v3_alias_to_field = {}
for fname, finfo in v3_uut_fields.items():
    for alias in finfo['aliases']:
        alias_name = alias.split(':', 1)[1] if ':' in alias else alias
        v3_alias_to_field[alias_name] = fname

missing_fields = []
for v1_field in sorted(v1_field_names):
    if v1_field not in v3_field_names:
        # Check if V1 field name matches any V3 alias
        if v1_field in v3_alias_to_field:
            v3_match = v3_alias_to_field[v1_field]
            print(f'  ✓ {v1_field} -> V3.{v3_match} (via alias)')
        else:
            # Check if V1 has aliases that match V3 field names or V3 aliases
            v1_aliases = [a.split(':', 1)[1] for a in v1_uut_fields[v1_field]['aliases'] if ':' in a]
            found = False
            for v1_alias in v1_aliases:
                if v1_alias in v3_field_names:
                    print(f'  ✓ {v1_field} (alias:{v1_alias}) -> V3.{v1_alias}')
                    found = True
                    break
                elif v1_alias in v3_alias_to_field:
                    print(f'  ✓ {v1_field} (alias:{v1_alias}) -> V3.{v3_alias_to_field[v1_alias]}')
                    found = True
                    break
            
            if not found:
                missing_fields.append(v1_field)
                print(f'  ✗ MISSING: {v1_field} (type: {v1_uut_fields[v1_field]["type"]})')

# Method comparison
print('\n--- METHOD/PROPERTY COMPARISON ---')
v1_method_names = set(v1_uut_methods.keys())
v3_method_names = set(v3_uut_methods.keys())

missing_methods = []
for v1_method in sorted(v1_method_names):
    if v1_method not in v3_method_names:
        missing_methods.append(v1_method)
        print(f'  ✗ MISSING: {v1_method} ({v1_uut_methods[v1_method]})')
    else:
        # Silent - method exists
        pass

print('\n' + '=' * 80)
print('UURReport COMPARISON')
print('=' * 80)

v1_uur_fields = get_all_fields_with_aliases(V1UUR)
v1_uur_methods = get_methods(V1UUR)
v3_uur_fields = get_all_fields_with_aliases(V3UUR)
v3_uur_methods = get_methods(V3UUR)

print(f'\nV1 UURReport: {len(v1_uur_fields)} fields, {len(v1_uur_methods)} methods/properties')
print(f'V3 UURReport: {len(v3_uur_fields)} fields, {len(v3_uur_methods)} methods/properties')

# Field comparison
print('\n--- FIELD COMPARISON ---')
v1_uur_field_names = set(v1_uur_fields.keys())
v3_uur_field_names = set(v3_uur_fields.keys())

# Build V3 alias map
v3_uur_alias_to_field = {}
for fname, finfo in v3_uur_fields.items():
    for alias in finfo['aliases']:
        alias_name = alias.split(':', 1)[1] if ':' in alias else alias
        v3_uur_alias_to_field[alias_name] = fname

missing_uur_fields = []
for v1_field in sorted(v1_uur_field_names):
    if v1_field not in v3_uur_field_names:
        # Check if V1 field name matches any V3 alias
        if v1_field in v3_uur_alias_to_field:
            v3_match = v3_uur_alias_to_field[v1_field]
            print(f'  ✓ {v1_field} -> V3.{v3_match} (via alias)')
        else:
            # Check if V1 has aliases that match V3 field names or V3 aliases
            v1_aliases = [a.split(':', 1)[1] for a in v1_uur_fields[v1_field]['aliases'] if ':' in a]
            found = False
            for v1_alias in v1_aliases:
                if v1_alias in v3_uur_field_names:
                    print(f'  ✓ {v1_field} (alias:{v1_alias}) -> V3.{v1_alias}')
                    found = True
                    break
                elif v1_alias in v3_uur_alias_to_field:
                    print(f'  ✓ {v1_field} (alias:{v1_alias}) -> V3.{v3_uur_alias_to_field[v1_alias]}')
                    found = True
                    break
            
            if not found:
                missing_uur_fields.append(v1_field)
                print(f'  ✗ MISSING: {v1_field} (type: {v1_uur_fields[v1_field]["type"]})')

# Method comparison
print('\n--- METHOD/PROPERTY COMPARISON ---')
v1_uur_method_names = set(v1_uur_methods.keys())
v3_uur_method_names = set(v3_uur_methods.keys())

missing_uur_methods = []
for v1_method in sorted(v1_uur_method_names):
    if v1_method not in v3_uur_method_names:
        missing_uur_methods.append(v1_method)
        print(f'  ✗ MISSING: {v1_method} ({v1_uur_methods[v1_method]})')
    else:
        # Silent - method exists
        pass

print('\n' + '=' * 80)
print('SUMMARY')
print('=' * 80)
print(f'\nUUTReport:')
print(f'  Missing fields: {len(missing_fields)}')
print(f'  Missing methods/properties: {len(missing_methods)}')
if missing_fields:
    print(f'    Fields: {", ".join(missing_fields)}')
if missing_methods:
    print(f'    Methods: {", ".join(missing_methods)}')

print(f'\nUURReport:')
print(f'  Missing fields: {len(missing_uur_fields)}')
print(f'  Missing methods/properties: {len(missing_uur_methods)}')
if missing_uur_fields:
    print(f'    Fields: {", ".join(missing_uur_fields)}')
if missing_uur_methods:
    print(f'    Methods: {", ".join(missing_uur_methods)}')

total_issues = len(missing_fields) + len(missing_methods) + len(missing_uur_fields) + len(missing_uur_methods)
print(f'\nTOTAL ISSUES: {total_issues}')
if total_issues == 0:
    print('✓ V3 has complete coverage of V1!')
