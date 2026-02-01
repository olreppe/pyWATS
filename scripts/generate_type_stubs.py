#!/usr/bin/env python3
"""
Generate type stub files (.pyi) for synchronous service wrappers.

This script parses async service classes and generates corresponding type stubs
that allow type checkers to provide proper autocomplete and type checking for
the synchronous pyWATS API.

Usage:
    python scripts/generate_type_stubs.py              # Generate stubs
    python scripts/generate_type_stubs.py --check      # Verify stubs are up-to-date
    python scripts/generate_type_stubs.py --verbose    # Show detailed output
"""

import ast
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

@dataclass
class MethodSignature:
    """Represents a method signature extracted from async service."""
    name: str
    params: List[str]  # Full parameter strings with types
    return_type: str
    docstring: str = ""

@dataclass
class ServiceInfo:
    """Information about a service for stub generation."""
    name: str  # e.g., "report", "product"
    async_service_class: str  # e.g., "AsyncReportService"
    sync_service_class: str  # e.g., "SyncReportService"
    module_path: str  # e.g., "pywats.domains.report.async_service"
    methods: List[MethodSignature]


class AsyncServiceParser:
    """Parse async service files to extract method signatures."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.source = file_path.read_text(encoding='utf-8')
        self.tree = ast.parse(self.source)
        
    def extract_methods(self, class_name: str) -> List[MethodSignature]:
        """Extract all async method signatures from a class."""
        methods = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for item in node.body:
                    if isinstance(item, ast.AsyncFunctionDef):
                        # Skip private methods
                        if item.name.startswith('_'):
                            continue
                        
                        sig = self._parse_method(item)
                        if sig:
                            methods.append(sig)
        
        return methods
    
    def _parse_method(self, node: ast.AsyncFunctionDef) -> MethodSignature:
        """Parse a single async method into a MethodSignature."""
        # Extract parameters
        params = []
        for arg in node.args.args:
            if arg.arg == 'self':
                continue
            
            # Get parameter with type annotation
            param_str = arg.arg
            if arg.annotation:
                param_str += f": {ast.unparse(arg.annotation)}"
            
            params.append(param_str)
        
        # Handle defaults
        defaults = node.args.defaults
        if defaults:
            # Defaults apply to the last N parameters
            num_defaults = len(defaults)
            for i, default in enumerate(defaults):
                param_idx = len(params) - num_defaults + i
                if param_idx >= 0:
                    params[param_idx] += f" = {ast.unparse(default)}"
        
        # Extract return type
        return_type = "None"
        if node.returns:
            return_type = ast.unparse(node.returns)
        
        # Extract docstring
        docstring = ast.get_docstring(node) or ""
        
        return MethodSignature(
            name=node.name,
            params=params,
            return_type=return_type,
            docstring=docstring
        )
    
    def extract_imports(self) -> Set[str]:
        """Extract relevant type imports from the source file."""
        imports = set()
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and 'typing' in node.module:
                    for alias in node.names:
                        imports.add(alias.name)
        
        return imports


class StubGenerator:
    """Generate .pyi stub files for sync wrappers."""
    
    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        self.services = self._discover_services()
    
    def _discover_services(self) -> List[ServiceInfo]:
        """Discover all async services that need stubs."""
        domains_dir = self.src_dir / "pywats" / "domains"
        services = []
        
        # Define services to process
        service_configs = [
            ("report", "AsyncReportService"),
            ("product", "AsyncProductService"),
            ("asset", "AsyncAssetService"),
            ("production", "AsyncProductionService"),
            ("software", "AsyncSoftwareService"),
            ("analytics", "AsyncAnalyticsService"),
            ("rootcause", "AsyncRootCauseService"),
            ("scim", "AsyncScimService"),
            ("process", "AsyncProcessService"),
        ]
        
        for service_name, async_class in service_configs:
            service_file = domains_dir / service_name / "async_service.py"
            
            if not service_file.exists():
                print(f"Warning: {service_file} not found, skipping")
                continue
            
            parser = AsyncServiceParser(service_file)
            methods = parser.extract_methods(async_class)
            
            services.append(ServiceInfo(
                name=service_name,
                async_service_class=async_class,
                sync_service_class=f"Sync{async_class[5:]}",  # AsyncXxxService -> SyncXxxService
                module_path=f"pywats.domains.{service_name}.async_service",
                methods=methods
            ))
        
        return services
    
    def generate_service_stub(self, service: ServiceInfo) -> str:
        """Generate stub content for a single service."""
        lines = [
            "# Type stubs for synchronous service wrapper",
            "# AUTO-GENERATED - DO NOT EDIT MANUALLY",
            "# Generated by scripts/generate_type_stubs.py",
            "",
            "from typing import TYPE_CHECKING",
            "",
            "if TYPE_CHECKING:",
        ]
        
        # Add imports for types used in this service
        # We'll import everything from the async service module
        lines.append(f"    from .async_service import {service.async_service_class}")
        lines.append("")
        
        # Generate class definition
        lines.append(f"class {service.sync_service_class}:")
        lines.append('    """Synchronous wrapper for ' + service.async_service_class + '."""')
        lines.append("")
        
        # Generate method stubs
        for method in service.methods:
            # Format parameters
            params_str = ", ".join(method.params) if method.params else ""
            if params_str:
                params_str = ", " + params_str
            
            # Method signature
            lines.append(f"    def {method.name}(self{params_str}) -> {method.return_type}: ...")
        
        return "\n".join(lines) + "\n"
    
    def generate_main_stub(self) -> str:
        """Generate the main pywats.pyi stub file."""
        lines = [
            "# Type stubs for pyWATS synchronous API",
            "# AUTO-GENERATED - DO NOT EDIT MANUALLY",
            "# Generated by scripts/generate_type_stubs.py",
            "",
            "from typing import Optional",
            "from .config import ErrorMode, RetryConfig",
            "from .station import Station, StationRegistry",
            "",
        ]
        
        # Import all sync service classes
        for service in self.services:
            lines.append(
                f"from .domains.{service.name}.service import {service.sync_service_class}"
            )
        
        lines.extend([
            "",
            "class pyWATS:",
            '    """Type-safe synchronous WATS API client."""',
            "",
            "    def __init__(",
            "        self,",
            "        base_url: str,",
            "        *,",
            "        api_key: Optional[str] = None,",
            "        client_id: Optional[str] = None,",
            "        client_secret: Optional[str] = None,",
            "        username: Optional[str] = None,",
            "        password: Optional[str] = None,",
            "        timeout: int = 30,",
            "        error_mode: ErrorMode = ErrorMode.RAISE,",
            "        retry_config: Optional[RetryConfig] = None,",
            "        station: Optional[Station] = None,",
            "    ) -> None: ...",
            "",
        ])
        
        # Add service properties
        for service in self.services:
            lines.extend([
                "    @property",
                f"    def {service.name}(self) -> {service.sync_service_class}: ...",
                "",
            ])
        
        # Add other properties and methods
        lines.extend([
            "    @property",
            "    def base_url(self) -> str: ...",
            "",
            "    @property",
            "    def timeout(self) -> int: ...",
            "",
            "    @timeout.setter",
            "    def timeout(self, value: int) -> None: ...",
            "",
            "    @property",
            "    def error_mode(self) -> ErrorMode: ...",
            "",
            "    @property",
            "    def retry_config(self) -> RetryConfig: ...",
            "",
            "    @retry_config.setter",
            "    def retry_config(self, value: RetryConfig) -> None: ...",
            "",
            "    @property",
            "    def station(self) -> Optional[Station]: ...",
            "",
            "    @station.setter",
            "    def station(self, station: Optional[Station]) -> None: ...",
            "",
            "    @property",
            "    def stations(self) -> StationRegistry: ...",
            "",
            "    def test_connection(self) -> bool: ...",
            "",
            "    def get_version(self) -> Optional[str]: ...",
            "",
            "    def close(self) -> None: ...",
            "",
            "    def __enter__(self) -> 'pyWATS': ...",
            "",
            "    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...",
        ])
        
        return "\n".join(lines) + "\n"
    
    def generate_all(self, verbose: bool = False) -> Dict[Path, str]:
        """Generate all stub files and return mapping of path -> content."""
        stubs = {}
        
        # Generate individual service stubs
        for service in self.services:
            if verbose:
                print(f"Generating stub for {service.name} ({len(service.methods)} methods)")
            
            stub_path = (
                self.src_dir / "pywats" / "domains" / service.name / "service.pyi"
            )
            stub_content = self.generate_service_stub(service)
            stubs[stub_path] = stub_content
        
        # Generate main pywats.pyi
        if verbose:
            print("Generating main pywats.pyi")
        
        main_stub_path = self.src_dir / "pywats" / "pywats.pyi"
        main_stub_content = self.generate_main_stub()
        stubs[main_stub_path] = main_stub_content
        
        return stubs
    
    def write_stubs(self, stubs: Dict[Path, str], verbose: bool = False) -> None:
        """Write stub files to disk."""
        for path, content in stubs.items():
            if verbose:
                print(f"Writing {path}")
            
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    
    def check_stubs(self, stubs: Dict[Path, str], verbose: bool = False) -> bool:
        """Check if existing stubs match generated content."""
        all_match = True
        
        for path, expected_content in stubs.items():
            if not path.exists():
                print(f"❌ Missing: {path}")
                all_match = False
                continue
            
            actual_content = path.read_text(encoding='utf-8')
            if actual_content != expected_content:
                print(f"❌ Outdated: {path}")
                all_match = False
            elif verbose:
                print(f"✅ Up-to-date: {path}")
        
        return all_match


def main():
    parser = argparse.ArgumentParser(
        description="Generate type stub files for pyWATS sync wrappers"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if stubs are up-to-date instead of generating"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    args = parser.parse_args()
    
    # Find source directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    src_dir = repo_root / "src"
    
    if not src_dir.exists():
        print(f"Error: Source directory not found: {src_dir}")
        sys.exit(1)
    
    # Generate stubs
    generator = StubGenerator(src_dir)
    stubs = generator.generate_all(verbose=args.verbose)
    
    if args.check:
        # Check mode - verify stubs are up-to-date
        if generator.check_stubs(stubs, verbose=args.verbose):
            print("✅ All type stubs are up-to-date")
            sys.exit(0)
        else:
            print("\n❌ Type stubs are outdated. Run: python scripts/generate_type_stubs.py")
            sys.exit(1)
    else:
        # Generate mode - write stubs to disk
        generator.write_stubs(stubs, verbose=args.verbose)
        print(f"\n✅ Generated {len(stubs)} type stub files")
        
        # Summary
        total_methods = sum(len(s.methods) for s in generator.services)
        print(f"   Services: {len(generator.services)}")
        print(f"   Total methods: {total_methods}")


if __name__ == "__main__":
    main()
