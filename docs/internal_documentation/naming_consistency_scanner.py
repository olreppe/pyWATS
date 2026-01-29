"""
Naming Consistency Scanner for pyWATS

Scans the codebase for violations of the naming convention:
- User-facing code (models, services) should use snake_case
- Backend API communication (serialization_alias) should use camelCase

Reports:
1. camelCase field names in Python models (should be snake_case)
2. snake_case in serialization_alias (should be camelCase)
3. Inconsistent patterns across similar models
"""
import re
from pathlib import Path
from collections import defaultdict

def scan_for_naming_violations():
    results = {
        'camel_in_python': [],
        'snake_in_serialization': [],
        'mixed_conventions': [],
        'good_examples': []
    }
    
    # Patterns
    # Field definition: captures field_name from "field_name: Type = ..."
    field_pattern = re.compile(r'^\s+([a-z_][a-z0-9_]*)\s*:\s*', re.MULTILINE)
    # serialization_alias pattern
    serialization_pattern = re.compile(r'serialization_alias\s*=\s*["\']([^"\']+)["\']')
    # validation_alias pattern  
    validation_pattern = re.compile(r'validation_alias\s*=\s*AliasChoices\s*\([^)]+\)')
    
    # Files to check
    model_files = list(Path('src/pywats/domains').rglob('models.py'))
    model_files += list(Path('src/pywats/domains/report/report_models').rglob('*.py'))
    model_files += list(Path('src/pywats/shared').glob('*.py'))
    model_files += list(Path('src/pywats_client/converters').glob('models.py'))
    
    # Track field-to-alias mappings
    field_alias_map = defaultdict(list)
    
    for fpath in model_files:
        if not fpath.is_file():
            continue
            
        try:
            content = fpath.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Find fields and their aliases
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Check for field definition
                field_match = field_pattern.match(line)
                if field_match:
                    field_name = field_match.group(1)
                    
                    # Skip special fields
                    if field_name in ['model_config', 'model_fields', 'id', 'cp', 'cpk', 'min', 'max', 'avg']:
                        i += 1
                        continue
                    
                    # Check if field_name is camelCase (has uppercase letters)
                    if any(c.isupper() for c in field_name) and '_' not in field_name:
                        line_no = i + 1
                        results['camel_in_python'].append({
                            'file': str(fpath),
                            'line': line_no,
                            'field': field_name,
                            'context': line.strip()
                        })
                    
                    # Look ahead for serialization_alias (within next 10 lines)
                    serialization_alias = None
                    for j in range(i, min(i + 10, len(lines))):
                        ser_match = serialization_pattern.search(lines[j])
                        if ser_match:
                            serialization_alias = ser_match.group(1)
                            break
                        # Stop at next field definition
                        if j > i and field_pattern.match(lines[j]):
                            break
                    
                    if serialization_alias:
                        # Check if serialization_alias is snake_case
                        if '_' in serialization_alias and serialization_alias.islower():
                            results['snake_in_serialization'].append({
                                'file': str(fpath),
                                'line': i + 1,
                                'field': field_name,
                                'alias': serialization_alias,
                                'issue': f'Field "{field_name}" has snake_case alias "{serialization_alias}" (should be camelCase)'
                            })
                        
                        # Track mapping
                        field_alias_map[field_name].append(serialization_alias)
                        
                        # Good example: snake_case field with camelCase alias
                        if '_' in field_name and not '_' in serialization_alias:
                            results['good_examples'].append({
                                'field': field_name,
                                'alias': serialization_alias
                            })
                
                i += 1
                
        except Exception as e:
            print(f"Error processing {fpath}: {e}")
            continue
    
    # Check for inconsistent aliases across codebase
    for field, aliases in field_alias_map.items():
        unique_aliases = set(aliases)
        if len(unique_aliases) > 1:
            results['mixed_conventions'].append({
                'field': field,
                'aliases': list(unique_aliases),
                'count': len(aliases)
            })
    
    return results

def print_report(results):
    print("=" * 80)
    print("NAMING CONSISTENCY SCAN REPORT")
    print("=" * 80)
    print()
    
    print("1. CAMELCASE FIELD NAMES IN PYTHON MODELS (should be snake_case):")
    print("-" * 80)
    if results['camel_in_python']:
        for item in results['camel_in_python'][:30]:
            print(f"   {item['file']}:{item['line']}")
            print(f"   Field: {item['field']}")
            print(f"   Context: {item['context']}")
            print()
        if len(results['camel_in_python']) > 30:
            print(f"   ... and {len(results['camel_in_python']) - 30} more violations")
    else:
        print("   ✅ No violations found!")
    print()
    
    print("2. SNAKE_CASE IN SERIALIZATION_ALIAS (should be camelCase for API):")
    print("-" * 80)
    if results['snake_in_serialization']:
        for item in results['snake_in_serialization'][:30]:
            print(f"   {item['file']}:{item['line']}")
            print(f"   Field: {item['field']} -> Alias: {item['alias']}")
            print(f"   Issue: {item['issue']}")
            print()
        if len(results['snake_in_serialization']) > 30:
            print(f"   ... and {len(results['snake_in_serialization']) - 30} more violations")
    else:
        print("   ✅ No violations found!")
    print()
    
    print("3. INCONSISTENT ALIAS MAPPINGS (same field name, different aliases):")
    print("-" * 80)
    if results['mixed_conventions']:
        for item in results['mixed_conventions'][:20]:
            print(f"   Field: {item['field']}")
            print(f"   Aliases used: {', '.join(item['aliases'])} ({item['count']} occurrences)")
            print()
        if len(results['mixed_conventions']) > 20:
            print(f"   ... and {len(results['mixed_conventions']) - 20} more inconsistencies")
    else:
        print("   ✅ No inconsistencies found!")
    print()
    
    print("SUMMARY:")
    print("-" * 80)
    print(f"   camelCase fields in Python: {len(results['camel_in_python'])}")
    print(f"   snake_case in API aliases: {len(results['snake_in_serialization'])}")
    print(f"   Inconsistent field mappings: {len(results['mixed_conventions'])}")
    print(f"   Good examples found: {len(results['good_examples'])}")
    print()
    
    # Overall assessment
    total_issues = (len(results['camel_in_python']) + 
                   len(results['snake_in_serialization']) + 
                   len(results['mixed_conventions']))
    
    if total_issues == 0:
        print("   ✅ EXCELLENT: All naming conventions are consistent!")
    elif total_issues < 10:
        print("   ⚠️  GOOD: Only minor naming inconsistencies found")
    elif total_issues < 50:
        print("   ⚠️  MODERATE: Some naming convention violations found")
    else:
        print("   ❌ NEEDS ATTENTION: Significant naming convention issues found")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    results = scan_for_naming_violations()
    print_report(results)
