"""Usage analyzer - scans codebase for endpoint usage patterns."""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class UsageLocation:
    """Represents one usage of an endpoint."""
    file_path: str
    line_number: int
    context: str  # Code snippet showing usage
    function_name: str  # Function/method where used


@dataclass
class EndpointUsage:
    """Complete usage information for an endpoint."""
    endpoint_path: str
    domain: str
    endpoint_name: str
    usage_count: int = 0
    locations: List[UsageLocation] = field(default_factory=list)
    used_by_files: Set[str] = field(default_factory=set)
    used_by_functions: Set[str] = field(default_factory=set)


class UsageAnalyzer:
    """Analyzes codebase to find where endpoints are used."""
    
    def __init__(self, src_dir: Path):
        """Initialize analyzer.
        
        Args:
            src_dir: Path to src/pywats directory
        """
        self.src_dir = src_dir
        self.usage_map: Dict[str, EndpointUsage] = {}
    
    def analyze(self, endpoints: List) -> Dict[str, EndpointUsage]:
        """Analyze codebase for endpoint usage.
        
        Args:
            endpoints: List of RawEndpoint objects from scanner
            
        Returns:
            Dictionary mapping endpoint path to EndpointUsage
        """
        # Initialize usage map
        for ep in endpoints:
            key = f"{ep.domain}.{ep.name}"
            self.usage_map[key] = EndpointUsage(
                endpoint_path=ep.path,
                domain=ep.domain,
                endpoint_name=ep.name
            )
        
        # Scan all Python files
        python_files = list(self.src_dir.rglob("*.py"))
        
        for file_path in python_files:
            # Skip routes.py itself
            if file_path.name == "routes.py":
                continue
            
            self._scan_file(file_path)
        
        return self.usage_map
    
    def _scan_file(self, file_path: Path):
        """Scan a single Python file for endpoint usage.
        
        Args:
            file_path: Path to Python file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            return  # Skip files that can't be read
        
        current_function = "module-level"
        
        for line_num, line in enumerate(lines, start=1):
            # Track current function/method
            func_match = re.match(r'\s*(async\s+)?def\s+(\w+)', line)
            if func_match:
                current_function = func_match.group(2)
            
            # Look for Routes.Domain.Endpoint usage
            # Pattern 1: Routes.{Domain}.{Endpoint} (attribute access)
            # Pattern 2: Routes.{Domain}.{method}(...) (method call)
            
            # Match both attribute access and method calls
            route_pattern = r'Routes\.(\w+)\.(\w+)'
            matches = re.finditer(route_pattern, line)
            
            for match in matches:
                domain = match.group(1)
                endpoint = match.group(2)
                
                # Handle both Internal and normal domains
                # Check for Routes.Domain.Internal.Endpoint
                internal_pattern = r'Routes\.' + domain + r'\.Internal\.(\w+)'
                internal_match = re.search(internal_pattern, line)
                
                if internal_match:
                    # This is an Internal endpoint
                    endpoint = internal_match.group(1)
                    # Key includes domain but endpoint is from Internal class
                
                key = f"{domain}.{endpoint}"
                
                if key in self.usage_map:
                    # Record usage
                    usage = self.usage_map[key]
                    usage.usage_count += 1
                    usage.used_by_files.add(str(file_path.relative_to(self.src_dir.parent)))
                    usage.used_by_functions.add(f"{file_path.stem}.{current_function}")
                    
                    # Store location with context
                    context = line.strip()
                    usage.locations.append(UsageLocation(
                        file_path=str(file_path.relative_to(self.src_dir.parent)),
                        line_number=line_num,
                        context=context,
                        function_name=current_function
                    ))
    
    def get_usage(self, domain: str, endpoint: str) -> EndpointUsage:
        """Get usage info for specific endpoint.
        
        Args:
            domain: Domain name
            endpoint: Endpoint name
            
        Returns:
            EndpointUsage object
        """
        key = f"{domain}.{endpoint}"
        return self.usage_map.get(key, EndpointUsage(
            endpoint_path="",
            domain=domain,
            endpoint_name=endpoint
        ))
    
    def get_unused_endpoints(self) -> List[EndpointUsage]:
        """Find endpoints with zero usage.
        
        Returns:
            List of unused endpoints
        """
        return [
            usage for usage in self.usage_map.values()
            if usage.usage_count == 0
        ]
    
    def get_most_used_endpoints(self, top_n: int = 10) -> List[EndpointUsage]:
        """Get most frequently used endpoints.
        
        Args:
            top_n: Number of top endpoints to return
            
        Returns:
            List of EndpointUsage sorted by usage count (descending)
        """
        return sorted(
            self.usage_map.values(),
            key=lambda x: x.usage_count,
            reverse=True
        )[:top_n]
    
    def get_usage_summary(self) -> Dict[str, int]:
        """Get summary statistics.
        
        Returns:
            Dictionary with summary stats
        """
        total = len(self.usage_map)
        used = sum(1 for u in self.usage_map.values() if u.usage_count > 0)
        unused = total - used
        total_calls = sum(u.usage_count for u in self.usage_map.values())
        
        return {
            "total_endpoints": total,
            "used_endpoints": used,
            "unused_endpoints": unused,
            "total_usage_count": total_calls,
            "avg_usage_per_endpoint": total_calls / total if total > 0 else 0
        }
