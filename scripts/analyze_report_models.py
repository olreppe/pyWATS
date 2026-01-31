"""
Comprehensive Report Model Analysis Script

Extracts all signatures from V1 and V3 report models including:
- All classes (base, inherited, contained)
- All methods and properties
- All fields/attributes with their aliases
- Generates comparison matrix to find naming differences and implementation gaps

Usage:
    python scripts/analyze_report_models.py
"""

import inspect
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, Type, get_type_hints
from dataclasses import dataclass, field
from pydantic import Field
from pydantic.fields import FieldInfo
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import V1 models
from pywats.domains.report.report_models import (
    Report as ReportV1,
    UUTReport as UUTReportV1,
    UURReport as UURReportV1,
    UUTInfo as UUTInfoV1,
    UURInfo as UURInfoV1,
    Step as StepV1,
    SequenceCall as SequenceCallV1,
    SubUnit as SubUnitV1,
    UURSubUnit as UURSubUnitV1,
    UURFailure as UURFailureV1,
    MiscInfo as MiscInfoV1,
    AdditionalData as AdditionalDataV1,
    BinaryData as BinaryDataV1,
    Asset as AssetV1,
    AssetStats as AssetStatsV1,
    Chart as ChartV1,
    ChartSeries as ChartSeriesV1,
    Attachment as AttachmentV1,
)

# Import V3 models
from pywats.domains.report.report_models_v3 import (
    Report as ReportV3,
    UUTReport as UUTReportV3,
    UURReport as UURReportV3,
)
from pywats.domains.report.report_models_v3.uut import (
    UUTInfo as UUTInfoV3,
    Step as StepV3,
)
from pywats.domains.report.report_models_v3.uut.steps import (
    SequenceCall as SequenceCallV3,
    NumericStep as NumericStepV3,
    BooleanStep as BooleanStepV3,
    StringStep as StringStepV3,
    ActionStep as ActionStepV3,
)
from pywats.domains.report.report_models_v3.uut.steps.measurement import (
    NumericMeasurement as NumericMeasurementV3,
    BooleanMeasurement as BooleanMeasurementV3,
    StringMeasurement as StringMeasurementV3,
)
from pywats.domains.report.report_models_v3.uur import (
    UURInfo as UURInfoV3,
    UURSubUnit as UURSubUnitV3,
    UURFailure as UURFailureV3,
)
from pywats.domains.report.report_models_v3 import (
    MiscInfo as MiscInfoV3,
    SubUnit as SubUnitV3,
    Asset as AssetV3,
    Chart as ChartV3,
)


@dataclass
class FieldSignature:
    """Represents a field/attribute signature"""
    name: str
    type_hint: str
    default: str
    validation_alias: str = ""
    serialization_alias: str = ""
    is_required: bool = False
    description: str = ""


@dataclass
class MethodSignature:
    """Represents a method signature"""
    name: str
    signature: str
    is_property: bool = False
    is_classmethod: bool = False
    is_staticmethod: bool = False
    return_type: str = ""


@dataclass
class ClassSignature:
    """Represents a complete class signature"""
    name: str
    module: str
    bases: List[str] = field(default_factory=list)
    fields: List[FieldSignature] = field(default_factory=list)
    methods: List[MethodSignature] = field(default_factory=list)
    properties: List[MethodSignature] = field(default_factory=list)


def extract_field_info(cls: Type, field_name: str, field_info: Any) -> FieldSignature:
    """Extract detailed information about a Pydantic field"""
    
    # Get type hint
    type_hints = get_type_hints(cls)
    type_hint = str(type_hints.get(field_name, "Unknown"))
    
    # Extract FieldInfo if it's a Pydantic field
    if isinstance(field_info, FieldInfo):
        validation_alias = field_info.validation_alias or ""
        serialization_alias = field_info.serialization_alias or ""
        is_required = field_info.is_required()
        description = field_info.description or ""
        default = str(field_info.default) if field_info.default is not None else ""
    else:
        validation_alias = ""
        serialization_alias = ""
        is_required = False
        description = ""
        default = str(field_info) if field_info is not inspect.Parameter.empty else ""
    
    return FieldSignature(
        name=field_name,
        type_hint=type_hint,
        default=default,
        validation_alias=validation_alias,
        serialization_alias=serialization_alias,
        is_required=is_required,
        description=description
    )


def extract_class_signature(cls: Type) -> ClassSignature:
    """Extract complete signature of a class"""
    
    signature = ClassSignature(
        name=cls.__name__,
        module=cls.__module__,
        bases=[base.__name__ for base in cls.__bases__ if base.__name__ != 'object']
    )
    
    # Extract fields (Pydantic model fields)
    if hasattr(cls, 'model_fields'):
        for field_name, field_info in cls.model_fields.items():
            signature.fields.append(extract_field_info(cls, field_name, field_info))
    
    # Extract methods and properties
    for name, obj in inspect.getmembers(cls):
        if name.startswith('_'):
            continue
            
        if isinstance(obj, property):
            signature.properties.append(MethodSignature(
                name=name,
                signature=f"@property {name}",
                is_property=True,
                return_type=str(get_type_hints(obj.fget).get('return', 'Unknown')) if obj.fget else ""
            ))
        elif inspect.ismethod(obj) or inspect.isfunction(obj):
            try:
                sig = inspect.signature(obj)
                is_classmethod = isinstance(inspect.getattr_static(cls, name), classmethod)
                is_staticmethod = isinstance(inspect.getattr_static(cls, name), staticmethod)
                
                signature.methods.append(MethodSignature(
                    name=name,
                    signature=f"{name}{sig}",
                    is_classmethod=is_classmethod,
                    is_staticmethod=is_staticmethod,
                    return_type=str(sig.return_annotation) if sig.return_annotation != inspect.Parameter.empty else ""
                ))
            except (ValueError, TypeError):
                pass
    
    return signature


def analyze_model_hierarchy(root_classes: List[Type]) -> Dict[str, ClassSignature]:
    """Analyze complete hierarchy of model classes"""
    
    analyzed = {}
    to_analyze = set(root_classes)
    processed = set()
    
    while to_analyze:
        cls = to_analyze.pop()
        
        if cls in processed or cls.__name__ in ['BaseModel', 'object', 'type']:
            continue
        
        processed.add(cls)
        
        # Extract signature
        sig = extract_class_signature(cls)
        analyzed[cls.__name__] = sig
        
        # Add base classes to analyze
        for base in cls.__bases__:
            if base.__name__ not in ['BaseModel', 'object', 'type']:
                to_analyze.add(base)
        
        # Add contained classes (from type hints)
        type_hints = get_type_hints(cls)
        for hint in type_hints.values():
            # Extract class from generic types like List[X], Optional[X], etc.
            origin = getattr(hint, '__origin__', None)
            args = getattr(hint, '__args__', ())
            
            for arg in args:
                if inspect.isclass(arg) and hasattr(arg, '__module__'):
                    if 'pywats.domains.report' in arg.__module__:
                        to_analyze.add(arg)
    
    return analyzed


def generate_comparison_matrix(v1_sigs: Dict[str, ClassSignature], 
                                v3_sigs: Dict[str, ClassSignature]) -> List[Dict[str, Any]]:
    """Generate comparison matrix between V1 and V3"""
    
    comparisons = []
    
    # Get all class names from both versions
    all_classes = set(v1_sigs.keys()) | set(v3_sigs.keys())
    
    for class_name in sorted(all_classes):
        v1_sig = v1_sigs.get(class_name)
        v3_sig = v3_sigs.get(class_name)
        
        comparison = {
            'class': class_name,
            'in_v1': v1_sig is not None,
            'in_v3': v3_sig is not None,
            'fields': {},
            'methods': {},
            'issues': []
        }
        
        if not v1_sig:
            comparison['issues'].append(f"Missing in V1")
        if not v3_sig:
            comparison['issues'].append(f"Missing in V3")
        
        if v1_sig and v3_sig:
            # Compare fields
            v1_field_names = {f.name for f in v1_sig.fields}
            v3_field_names = {f.name for f in v3_sig.fields}
            
            all_fields = v1_field_names | v3_field_names
            
            for field_name in sorted(all_fields):
                v1_field = next((f for f in v1_sig.fields if f.name == field_name), None)
                v3_field = next((f for f in v3_sig.fields if f.name == field_name), None)
                
                field_comp = {
                    'in_v1': v1_field is not None,
                    'in_v3': v3_field is not None,
                }
                
                if v1_field:
                    field_comp['v1_type'] = v1_field.type_hint
                    field_comp['v1_alias'] = v1_field.validation_alias or v1_field.serialization_alias
                if v3_field:
                    field_comp['v3_type'] = v3_field.type_hint
                    field_comp['v3_alias'] = v3_field.validation_alias or v3_field.serialization_alias
                
                # Check for issues
                if v1_field and v3_field:
                    if v1_field.validation_alias != v3_field.validation_alias:
                        field_comp['alias_mismatch'] = True
                    if v1_field.type_hint != v3_field.type_hint:
                        field_comp['type_mismatch'] = True
                
                comparison['fields'][field_name] = field_comp
            
            # Compare methods
            v1_method_names = {m.name for m in v1_sig.methods}
            v3_method_names = {m.name for m in v3_sig.methods}
            
            missing_in_v3 = v1_method_names - v3_method_names
            missing_in_v1 = v3_method_names - v1_method_names
            
            if missing_in_v3:
                comparison['methods']['missing_in_v3'] = sorted(missing_in_v3)
            if missing_in_v1:
                comparison['methods']['missing_in_v1'] = sorted(missing_in_v1)
        
        comparisons.append(comparison)
    
    return comparisons


def print_signature_report(signatures: Dict[str, ClassSignature], version: str):
    """Print detailed signature report"""
    
    print(f"\n{'='*80}")
    print(f" {version} Report Model Signatures")
    print(f"{'='*80}\n")
    
    for class_name in sorted(signatures.keys()):
        sig = signatures[class_name]
        
        print(f"\nClass: {class_name}")
        print(f"  Module: {sig.module}")
        if sig.bases:
            print(f"  Bases: {', '.join(sig.bases)}")
        
        if sig.fields:
            print(f"\n  Fields ({len(sig.fields)}):")
            for field in sorted(sig.fields, key=lambda f: f.name):
                alias_info = ""
                if field.validation_alias:
                    alias_info += f" [val_alias: {field.validation_alias}]"
                if field.serialization_alias:
                    alias_info += f" [ser_alias: {field.serialization_alias}]"
                required = " (required)" if field.is_required else ""
                print(f"    {field.name}: {field.type_hint}{alias_info}{required}")
        
        if sig.properties:
            print(f"\n  Properties ({len(sig.properties)}):")
            for prop in sorted(sig.properties, key=lambda p: p.name):
                print(f"    {prop.name} -> {prop.return_type}")
        
        if sig.methods:
            print(f"\n  Methods ({len(sig.methods)}):")
            for method in sorted(sig.methods, key=lambda m: m.name):
                prefix = ""
                if method.is_classmethod:
                    prefix = "@classmethod "
                elif method.is_staticmethod:
                    prefix = "@staticmethod "
                print(f"    {prefix}{method.signature}")


def print_comparison_report(comparisons: List[Dict[str, Any]]):
    """Print comparison matrix report"""
    
    print(f"\n{'='*80}")
    print(f" V1 vs V3 Comparison Matrix")
    print(f"{'='*80}\n")
    
    # Summary statistics
    v1_only = sum(1 for c in comparisons if c['in_v1'] and not c['in_v3'])
    v3_only = sum(1 for c in comparisons if c['in_v3'] and not c['in_v1'])
    both = sum(1 for c in comparisons if c['in_v1'] and c['in_v3'])
    
    print(f"Summary:")
    print(f"  Classes in both V1 and V3: {both}")
    print(f"  Classes only in V1: {v1_only}")
    print(f"  Classes only in V3: {v3_only}")
    print(f"  Total unique classes: {len(comparisons)}")
    
    # Detailed comparison
    for comp in comparisons:
        if not comp['in_v1'] or not comp['in_v3']:
            print(f"\n⚠️  {comp['class']}: {', '.join(comp['issues'])}")
            continue
        
        issues = []
        
        # Check field mismatches
        for field_name, field_comp in comp['fields'].items():
            if not field_comp['in_v1']:
                issues.append(f"  Field '{field_name}' missing in V1")
            elif not field_comp['in_v3']:
                issues.append(f"  Field '{field_name}' missing in V3")
            else:
                if field_comp.get('alias_mismatch'):
                    issues.append(f"  Field '{field_name}' has different aliases: V1={field_comp.get('v1_alias')}, V3={field_comp.get('v3_alias')}")
                if field_comp.get('type_mismatch'):
                    issues.append(f"  Field '{field_name}' has different types")
        
        # Check method mismatches
        if comp['methods'].get('missing_in_v3'):
            issues.append(f"  Methods missing in V3: {', '.join(comp['methods']['missing_in_v3'][:5])}")
        if comp['methods'].get('missing_in_v1'):
            issues.append(f"  Methods missing in V1: {', '.join(comp['methods']['missing_in_v1'][:5])}")
        
        if issues:
            print(f"\n⚠️  {comp['class']}:")
            for issue in issues:
                print(issue)
        else:
            print(f"\n✓  {comp['class']}: No issues found")


def main():
    """Main analysis function"""
    
    print("Analyzing Report Models...")
    print("=" * 80)
    
    # Define root classes for V1
    v1_roots = [
        ReportV1, UUTReportV1, UURReportV1,
        UUTInfoV1, UURInfoV1,
        StepV1, SequenceCallV1,
        SubUnitV1, UURSubUnitV1, UURFailureV1,
        MiscInfoV1, AdditionalDataV1, BinaryDataV1,
        AssetV1, AssetStatsV1,
        ChartV1, ChartSeriesV1,
        AttachmentV1,
    ]
    
    # Define root classes for V3
    v3_roots = [
        ReportV3, UUTReportV3, UURReportV3,
        UUTInfoV3, UURInfoV3,
        StepV3, SequenceCallV3,
        NumericStepV3, BooleanStepV3, StringStepV3, ActionStepV3,
        NumericMeasurementV3, BooleanMeasurementV3, StringMeasurementV3,
        SubUnitV3, UURSubUnitV3, UURFailureV3,
        MiscInfoV3,
        AssetV3,
        ChartV3,
    ]
    
    # Analyze V1
    print("\nAnalyzing V1 model hierarchy...")
    v1_signatures = analyze_model_hierarchy(v1_roots)
    print(f"Found {len(v1_signatures)} classes in V1")
    
    # Analyze V3
    print("Analyzing V3 model hierarchy...")
    v3_signatures = analyze_model_hierarchy(v3_roots)
    print(f"Found {len(v3_signatures)} classes in V3")
    
    # Print detailed reports
    print_signature_report(v1_signatures, "V1")
    print_signature_report(v3_signatures, "V3")
    
    # Generate and print comparison
    print("\nGenerating comparison matrix...")
    comparisons = generate_comparison_matrix(v1_signatures, v3_signatures)
    print_comparison_report(comparisons)
    
    # Save to JSON for further analysis
    output_dir = Path(__file__).parent.parent / "tests" / "report_model_testing" / "files_after_conversion_and_reload"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert signatures to dict for JSON serialization
    v1_dict = {k: v.__dict__ for k, v in v1_signatures.items()}
    v3_dict = {k: v.__dict__ for k, v in v3_signatures.items()}
    
    with open(output_dir / "v1_signatures.json", "w") as f:
        json.dump(v1_dict, f, indent=2, default=str)
    
    with open(output_dir / "v3_signatures.json", "w") as f:
        json.dump(v3_dict, f, indent=2, default=str)
    
    with open(output_dir / "comparison_matrix.json", "w") as f:
        json.dump(comparisons, f, indent=2, default=str)
    
    print(f"\n✓ Detailed analysis saved to {output_dir}")
    print(f"  - v1_signatures.json")
    print(f"  - v3_signatures.json")
    print(f"  - comparison_matrix.json")
    
    print(f"\n{'='*80}")
    print("Analysis complete!")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
