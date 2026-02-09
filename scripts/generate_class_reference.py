"""
Auto-generate compact API reference documentation for all classes.

Creates one .md file per domain/component listing all classes with their
methods and member variables.

Usage:
    python scripts/generate_class_reference.py
"""

import ast
from pathlib import Path
from typing import Dict, List, Set
from dataclasses import dataclass, field


@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    module: str
    bases: List[str] = field(default_factory=list)
    methods: List[str] = field(default_factory=list)
    properties: List[str] = field(default_factory=list)
    class_vars: List[str] = field(default_factory=list)
    docstring: str = ""


class ClassExtractor(ast.NodeVisitor):
    """Extract class information from AST."""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.classes: List[ClassInfo] = []
        self.current_class: ClassInfo = None
    
    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit class definition."""
        # Create class info
        class_info = ClassInfo(
            name=node.name,
            module=self.module_name,
            bases=[self._get_base_name(base) for base in node.bases],
            docstring=ast.get_docstring(node) or ""
        )
        
        # Extract class variables, methods, and properties
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if any(isinstance(dec, ast.Name) and dec.id == 'property' 
                       for dec in item.decorator_list):
                    class_info.properties.append(item.name)
                elif not item.name.startswith('_'):  # Public methods only
                    class_info.methods.append(self._format_method(item))
            elif isinstance(item, ast.AnnAssign):
                # Type-annotated class variable
                if isinstance(item.target, ast.Name):
                    class_info.class_vars.append(f"{item.target.id}: {self._get_annotation(item.annotation)}")
            elif isinstance(item, ast.Assign):
                # Regular class variable
                for target in item.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith('_'):
                        class_info.class_vars.append(target.id)
        
        self.classes.append(class_info)
        self.generic_visit(node)
    
    def _get_base_name(self, base) -> str:
        """Get base class name."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{self._get_name(base.value)}.{base.attr}"
        return "Unknown"
    
    def _get_name(self, node) -> str:
        """Get name from node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return ""
    
    def _get_annotation(self, annotation) -> str:
        """Get type annotation as string."""
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Attribute):
            return f"{self._get_name(annotation.value)}.{annotation.attr}"
        elif isinstance(annotation, ast.Subscript):
            return f"{self._get_annotation(annotation.value)}[...]"
        return "Any"
    
    def _format_method(self, node: ast.FunctionDef) -> str:
        """Format method signature."""
        args = []
        for arg in node.args.args:
            if arg.arg == 'self':
                continue
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {self._get_annotation(arg.annotation)}"
            args.append(arg_str)
        
        returns = ""
        if node.returns:
            returns = f" -> {self._get_annotation(node.returns)}"
        
        return f"{node.name}({', '.join(args)}){returns}"


def extract_classes_from_file(file_path: Path, module_name: str) -> List[ClassInfo]:
    """Extract all classes from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        extractor = ClassExtractor(module_name)
        extractor.visit(tree)
        return extractor.classes
    except Exception as e:
        print(f"Warning: Could not parse {file_path}: {e}")
        return []


def scan_directory(base_path: Path, package_name: str) -> Dict[str, List[ClassInfo]]:
    """Scan directory for Python files and extract classes."""
    all_classes = {}
    
    for py_file in base_path.rglob("*.py"):
        if py_file.name.startswith("_") and py_file.name != "__init__.py":
            continue
        
        # Build module name
        relative = py_file.relative_to(base_path.parent)
        parts = list(relative.parts[:-1])  # Exclude filename
        if py_file.name != "__init__.py":
            parts.append(py_file.stem)
        module_name = ".".join(parts)
        
        # Extract classes
        classes = extract_classes_from_file(py_file, module_name)
        if classes:
            all_classes[module_name] = classes
    
    return all_classes


def generate_markdown(component_name: str, classes_by_module: Dict[str, List[ClassInfo]]) -> str:
    """Generate markdown documentation for a component."""
    lines = [
        f"# {component_name} - Class Reference",
        "",
        f"Auto-generated class reference for `{component_name}`.",
        "",
        "---",
        ""
    ]
    
    # Sort modules alphabetically
    for module_name in sorted(classes_by_module.keys()):
        classes = classes_by_module[module_name]
        
        lines.append(f"## `{module_name}`")
        lines.append("")
        
        for cls in sorted(classes, key=lambda c: c.name):
            # Class header
            bases = f"({', '.join(cls.bases)})" if cls.bases else ""
            lines.append(f"### `{cls.name}{bases}`")
            lines.append("")
            
            # Docstring (first line only)
            if cls.docstring:
                first_line = cls.docstring.split('\n')[0].strip()
                if first_line:
                    lines.append(f"_{first_line}_")
                    lines.append("")
            
            # Class variables
            if cls.class_vars:
                lines.append("**Class Variables:**")
                for var in cls.class_vars:
                    lines.append(f"- `{var}`")
                lines.append("")
            
            # Properties
            if cls.properties:
                lines.append("**Properties:**")
                for prop in sorted(cls.properties):
                    lines.append(f"- `{prop}`")
                lines.append("")
            
            # Methods
            if cls.methods:
                lines.append("**Methods:**")
                for method in sorted(cls.methods):
                    lines.append(f"- `{method}`")
                lines.append("")
            
            lines.append("---")
            lines.append("")
    
    return "\n".join(lines)


def generate_combined_api_reference(docs_dir: Path, repo_root: Path):
    """Generate a comprehensive combined reference for the entire pyWATS API."""
    print("\n  Generating combined API reference...")
    
    # Files to include in combined reference (pywats only, excluding client/ui/events)
    api_files = [
        'pywats_root.md',
        'pywats_core.md',
        'pywats_shared.md',
        'domain_analytics.md',
        'domain_asset.md',
        'domain_process.md',
        'domain_product.md',
        'domain_production.md',
        'domain_report.md',
        'domain_rootcause.md',
        'domain_scim.md',
        'domain_software.md'
    ]
    
    lines = [
        "# pyWATS API - Complete Class Reference",
        "",
        "**Complete reference for the pyWATS API library (excluding client, service, and UI layers)**",
        "",
        f"**Generated:** {Path(__file__).parent.parent.name}",
        "**Generator:** `scripts/generate_class_reference.py`",
        "",
        "---",
        "",
        "## 📚 Table of Contents",
        "",
        "1. [API Entry Points](#api-entry-points) - pyWATS, AsyncWATS",
        "2. [Core Infrastructure](#core-infrastructure) - HTTP client, caching, exceptions",
        "3. [Shared Models](#shared-models) - Base models and utilities",
        "4. [Domain Services](#domain-services) - All business domains",
        "   - [Analytics](#analytics-domain)",
        "   - [Asset](#asset-domain)",
        "   - [Process](#process-domain)",
        "   - [Product](#product-domain)",
        "   - [Production](#production-domain)",
        "   - [Report](#report-domain)",
        "   - [Root Cause](#rootcause-domain)",
        "   - [SCIM](#scim-domain)",
        "   - [Software](#software-domain)",
        "",
        "---",
        ""
    ]
    
    # Section mappings
    section_headers = {
        'pywats_root.md': ('api-entry-points', 'API Entry Points'),
        'pywats_core.md': ('core-infrastructure', 'Core Infrastructure'),
        'pywats_shared.md': ('shared-models', 'Shared Models'),
        'domain_analytics.md': ('analytics-domain', 'Analytics Domain'),
        'domain_asset.md': ('asset-domain', 'Asset Domain'),
        'domain_process.md': ('process-domain', 'Process Domain'),
        'domain_product.md': ('product-domain', 'Product Domain'),
        'domain_production.md': ('production-domain', 'Production Domain'),
        'domain_report.md': ('report-domain', 'Report Domain'),
        'domain_rootcause.md': ('rootcause-domain', 'RootCause Domain'),
        'domain_scim.md': ('scim-domain', 'SCIM Domain'),
        'domain_software.md': ('software-domain', 'Software Domain')
    }
    
    # Append content from each file
    for api_file in api_files:
        file_path = docs_dir / api_file
        if not file_path.exists():
            continue
        
        # Add section header
        if api_file in section_headers:
            anchor, title = section_headers[api_file]
            lines.append(f'<a name="{anchor}"></a>')
            lines.append("")
            lines.append(f"# {title}")
            lines.append("")
            lines.append(f"_Source: [{api_file}]({api_file})_")
            lines.append("")
        
        # Read and append content (skip title and header)
        content = file_path.read_text(encoding='utf-8')
        content_lines = content.split('\n')
        
        # Skip first few lines (title, auto-generated note, first separator)
        in_content = False
        for line in content_lines:
            if in_content:
                lines.append(line)
            elif line.strip() == '---' and not in_content:
                in_content = True
        
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Add footer
    lines.extend([
        "",
        "## Related Documentation",
        "",
        "- [Individual Component References](README.md) - Separate files per component",
        "- [API Documentation](../README.md) - Sphinx-generated API docs",
        "- [Architecture Analysis](../../projects/active/api-client-ui-communication-analysis.project/README.md)",
        "- [Developer Guides](../../guides/)",
        "- [Examples](../../examples/)",
        "",
        "---",
        "",
        "**Last Updated:** February 8, 2026",
        "**Maintainer:** Auto-generated by CI/development workflow"
    ])
    
    # Write combined file
    output_file = docs_dir / "pywats_api_complete.md"
    output_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"    → {output_file.relative_to(repo_root)}")


def main():

    """Generate class reference documentation."""
    repo_root = Path(__file__).parent.parent
    src_dir = repo_root / "src"
    docs_dir = repo_root / "docs" / "api" / "class_reference"
    
    # Create output directory
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating class reference documentation...")
    
    # Process pywats domains
    domains_dir = src_dir / "pywats" / "domains"
    if domains_dir.exists():
        for domain_path in sorted(domains_dir.iterdir()):
            if domain_path.is_dir() and not domain_path.name.startswith("_"):
                print(f"  Processing domain: {domain_path.name}")
                classes = scan_directory(domain_path, f"pywats.domains.{domain_path.name}")
                if classes:
                    md_content = generate_markdown(f"pywats.domains.{domain_path.name}", classes)
                    output_file = docs_dir / f"domain_{domain_path.name}.md"
                    output_file.write_text(md_content, encoding='utf-8')
                    print(f"    → {output_file.relative_to(repo_root)}")
    
    # Process pywats root module (PyWATS, AsyncWATS, etc.)
    pywats_dir = src_dir / "pywats"
    if pywats_dir.exists():
        print(f"  Processing pywats (root)")
        root_classes = {}
        # Process key root files
        for root_file in ['pywats.py', 'async_wats.py']:
            file_path = pywats_dir / root_file
            if file_path.exists():
                module_name = f"pywats.{file_path.stem}"
                classes = extract_classes_from_file(file_path, module_name)
                if classes:
                    root_classes[module_name] = classes
        
        if root_classes:
            md_content = generate_markdown("pywats (API Entry Points)", root_classes)
            output_file = docs_dir / "pywats_root.md"
            output_file.write_text(md_content, encoding='utf-8')
            print(f"    → {output_file.relative_to(repo_root)}")
    
    # Process pywats.shared
    shared_dir = src_dir / "pywats" / "shared"
    if shared_dir.exists():
        print(f"  Processing pywats.shared")
        classes = scan_directory(shared_dir, "pywats.shared")
        if classes:
            md_content = generate_markdown("pywats.shared", classes)
            output_file = docs_dir / "pywats_shared.md"
            output_file.write_text(md_content, encoding='utf-8')
            print(f"    → {output_file.relative_to(repo_root)}")
    
    # Process pywats core
    core_dir = src_dir / "pywats" / "core"
    if core_dir.exists():
        print(f"  Processing pywats.core")
        classes = scan_directory(core_dir, "pywats.core")
        if classes:
            md_content = generate_markdown("pywats.core", classes)
            output_file = docs_dir / "pywats_core.md"
            output_file.write_text(md_content, encoding='utf-8')
            print(f"    → {output_file.relative_to(repo_root)}")
    
    # Process pywats_client components
    client_dir = src_dir / "pywats_client"
    if client_dir.exists():
        for component in ['core', 'service', 'queue', 'converters', 'control']:
            comp_path = client_dir / component
            if comp_path.exists() and comp_path.is_dir():
                print(f"  Processing pywats_client.{component}")
                classes = scan_directory(comp_path, f"pywats_client.{component}")
                if classes:
                    md_content = generate_markdown(f"pywats_client.{component}", classes)
                    output_file = docs_dir / f"client_{component}.md"
                    output_file.write_text(md_content, encoding='utf-8')
                    print(f"    → {output_file.relative_to(repo_root)}")
    
    # Process pywats_ui components
    ui_dir = src_dir / "pywats_ui"
    if ui_dir.exists():
        for component in ['framework', 'widgets', 'dialogs']:
            comp_path = ui_dir / component
            if comp_path.exists() and comp_path.is_dir():
                print(f"  Processing pywats_ui.{component}")
                classes = scan_directory(comp_path, f"pywats_ui.{component}")
                if classes:
                    md_content = generate_markdown(f"pywats_ui.{component}", classes)
                    output_file = docs_dir / f"ui_{component}.md"
                    output_file.write_text(md_content, encoding='utf-8')
                    print(f"    → {output_file.relative_to(repo_root)}")
    
    # Process pywats_events
    events_dir = src_dir / "pywats_events"
    if events_dir.exists():
        print(f"  Processing pywats_events")
        classes = scan_directory(events_dir, "pywats_events")
        if classes:
            md_content = generate_markdown("pywats_events", classes)
            output_file = docs_dir / "pywats_events.md"
            output_file.write_text(md_content, encoding='utf-8')
            print(f"    → {output_file.relative_to(repo_root)}")
    
    # Generate combined API reference (pywats only, no client/ui/events)
    generate_combined_api_reference(docs_dir, repo_root)
    
    print(f"\n✅ Class reference documentation generated in: {docs_dir.relative_to(repo_root)}")
    print(f"   📖 Combined API reference: pywats_api_complete.md")


if __name__ == "__main__":
    main()
