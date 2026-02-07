"""Endpoint scanner - parses routes.py to extract all endpoint definitions."""

import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class RawEndpoint:
    """Raw endpoint extracted from routes.py."""
    domain: str
    name: str
    path: str
    is_internal: bool
    is_method: bool  # True if @staticmethod, False if class attribute


class EndpointScanner:
    """Scans routes.py and extracts all endpoint definitions."""
    
    def __init__(self, routes_file: Path):
        """Initialize scanner.
        
        Args:
            routes_file: Path to routes.py file
        """
        self.routes_file = routes_file
        self.endpoints: List[RawEndpoint] = []
    
    def scan(self) -> List[RawEndpoint]:
        """Scan routes.py and extract all endpoints.
        
        Returns:
            List of RawEndpoint objects
        """
        with open(self.routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse AST
        tree = ast.parse(content)
        
        # Find Routes class
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "Routes":
                self._parse_routes_class(node)
                break
        
        return self.endpoints
    
    def _parse_routes_class(self, routes_class: ast.ClassDef):
        """Parse the Routes class and extract domain classes.
        
        Args:
            routes_class: AST node for Routes class
        """
        for node in routes_class.body:
            if isinstance(node, ast.ClassDef):
                domain_name = node.name
                self._parse_domain_class(domain_name, node, is_internal=False)
    
    def _parse_domain_class(
        self,
        domain: str,
        domain_class: ast.ClassDef,
        is_internal: bool
    ):
        """Parse a domain class (e.g., Report, Production).
        
        Args:
            domain: Domain name
            domain_class: AST node for domain class
            is_internal: Whether this is an Internal nested class
        """
        for node in domain_class.body:
            # Handle nested Internal class
            if isinstance(node, ast.ClassDef) and node.name == "Internal":
                self._parse_domain_class(domain, node, is_internal=True)
                continue
            
            # Handle class attributes (endpoints)
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        endpoint_name = target.id  # Use .id not .name for ast.Name
                        path = self._extract_string_value(node.value)
                        if path and path.startswith("/api"):
                            self.endpoints.append(RawEndpoint(
                                domain=domain,
                                name=endpoint_name,
                                path=path,
                                is_internal=is_internal,
                                is_method=False
                            ))
            
            # Handle static methods (dynamic endpoints)
            if isinstance(node, ast.FunctionDef):
                # Check if decorated with @staticmethod
                is_static = any(
                    isinstance(d, ast.Name) and d.id == "staticmethod"
                    for d in node.decorator_list
                )
                
                if is_static:
                    method_name = node.name
                    # Try to extract return path from method
                    return_path = self._extract_method_return_path(node)
                    if return_path:
                        self.endpoints.append(RawEndpoint(
                            domain=domain,
                            name=method_name,
                            path=return_path,
                            is_internal=is_internal,
                            is_method=True
                        ))
    
    def _extract_string_value(self, node: ast.expr) -> Optional[str]:
        """Extract string value from AST node.
        
        Args:
            node: AST expression node
            
        Returns:
            String value or None
        """
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        
        # Handle f-strings
        if isinstance(node, ast.JoinedStr):
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    parts.append(str(value.value))
                elif isinstance(value, ast.FormattedValue):
                    # Use placeholder for f-string variables
                    parts.append("{...}")
            return "".join(parts)
        
        return None
    
    def _extract_method_return_path(self, func_node: ast.FunctionDef) -> Optional[str]:
        """Extract return path from static method.
        
        Args:
            func_node: AST node for function
            
        Returns:
            Return path template or None
        """
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return) and node.value:
                return self._extract_string_value(node.value)
        return None
    
    def get_internal_endpoints(self) -> List[RawEndpoint]:
        """Get only internal API endpoints.
        
        Returns:
            List of internal endpoints
        """
        return [ep for ep in self.endpoints if ep.is_internal]
    
    def get_public_endpoints(self) -> List[RawEndpoint]:
        """Get only public API endpoints.
        
        Returns:
            List of public endpoints
        """
        return [ep for ep in self.endpoints if not ep.is_internal]
    
    def get_by_domain(self, domain: str) -> List[RawEndpoint]:
        """Get endpoints for specific domain.
        
        Args:
            domain: Domain name (Report, Production, etc.)
            
        Returns:
            List of endpoints in domain
        """
        return [ep for ep in self.endpoints if ep.domain == domain]
    
    def get_critical_internal_endpoints(self) -> List[RawEndpoint]:
        """Get internal endpoints that need public alternatives.
        
        Returns:
            List of critical internal endpoints
        """
        # Import here to avoid circular dependency
        from .classifier import EndpointClassifier, Priority
        
        critical = []
        for ep in self.get_internal_endpoints():
            priority = EndpointClassifier.classify(
                ep.domain, ep.name, ep.is_internal, ep.path
            )
            if priority in (Priority.CRITICAL, Priority.HIGH):
                critical.append(ep)
        
        return critical
