"""Report generator - generates markdown risk assessment reports."""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict

from .scanner import RawEndpoint
from .analyzer import EndpointUsage
from .classifier import EndpointClassifier, Priority, EndpointInfo


class ReportGenerator:
    """Generates markdown reports for endpoint risk assessment."""
    
    def __init__(
        self,
        endpoints: List[RawEndpoint],
        usage_map: Dict[str, EndpointUsage]
    ):
        """Initialize report generator.
        
        Args:
            endpoints: List of raw endpoints from scanner
            usage_map: Usage data from analyzer
        """
        self.endpoints = endpoints
        self.usage_map = usage_map
        self._build_endpoint_info()
    
    def _build_endpoint_info(self):
        """Build complete EndpointInfo objects."""
        self.endpoint_infos: List[EndpointInfo] = []
        
        for ep in self.endpoints:
            key = f"{ep.domain}.{ep.name}"
            usage = self.usage_map.get(key, None)
            
            # Classify endpoint
            priority = EndpointClassifier.classify(
                ep.domain, ep.name, ep.is_internal, ep.path
            )
            
            # Get description
            description = EndpointClassifier.get_description(
                ep.domain, ep.name, ep.path
            )
            
            # Build used_by list
            used_by = []
            if usage:
                used_by = sorted(usage.used_by_functions)[:10]  # Limit to top 10
            
            info = EndpointInfo(
                path=ep.path,
                domain=ep.domain,
                method="Multiple",  # Would need HTTP method tracking
                is_internal=ep.is_internal,
                priority=priority,
                usage_count=usage.usage_count if usage else 0,
                used_by=used_by,
                description=description,
                public_alternative=self._find_public_alternative(ep) if ep.is_internal else None
            )
            
            self.endpoint_infos.append(info)
    
    def _find_public_alternative(self, internal_ep: RawEndpoint) -> Optional[str]:
        """Find public API alternative for internal endpoint.
        
        Args:
            internal_ep: Internal endpoint
            
        Returns:
            Public endpoint path or None
        """
        # Look for similar public endpoints in same domain
        for ep in self.endpoints:
            if (ep.domain == internal_ep.domain and
                not ep.is_internal and
                self._are_similar(internal_ep.path, ep.path)):
                return ep.path
        return None
    
    def _are_similar(self, path1: str, path2: str) -> bool:
        """Check if two paths are functionally similar.
        
        Args:
            path1: First path
            path2: Second path
            
        Returns:
            True if paths appear to serve similar purpose
        """
        # Simple heuristic: check if they share key words
        words1 = set(path1.lower().split('/'))
        words2 = set(path2.lower().split('/'))
        common = words1 & words2
        return len(common) >= 3
    
    def generate_full_report(self) -> str:
        """Generate complete endpoint risk assessment report.
        
        Returns:
            Markdown content
        """
        sections = []
        
        # Header
        sections.append(self._generate_header())
        
        # Executive Summary
        sections.append(self._generate_summary())
        
        # Critical Endpoints
        sections.append(self._generate_priority_table(Priority.CRITICAL))
        
        # High Priority Endpoints
        sections.append(self._generate_priority_table(Priority.HIGH))
        
        # Medium Priority Endpoints  
        sections.append(self._generate_priority_table(Priority.MEDIUM))
        
        # Low Priority Endpoints (collapsed)
        sections.append(self._generate_priority_table(Priority.LOW))
        
        # Internal API Gap Analysis
        sections.append(self._generate_gap_analysis())
        
        # Migration Recommendations
        sections.append(self._generate_migration_recommendations())
        
        # Usage Statistics
        sections.append(self._generate_usage_stats())
        
        return "\n\n".join(sections)
    
    def _generate_header(self) -> str:
        """Generate report header."""
        return f"""# Endpoint Risk Assessment Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Total Endpoints:** {len(self.endpoint_infos)}  
**Internal Endpoints:** {sum(1 for e in self.endpoint_infos if e.is_internal)}  
**Public Endpoints:** {sum(1 for e in self.endpoint_infos if not e.is_internal)}

---"""
    
    def _generate_summary(self) -> str:
        """Generate executive summary."""
        critical = [e for e in self.endpoint_infos if e.priority == Priority.CRITICAL]
        high = [e for e in self.endpoint_infos if e.priority == Priority.HIGH]
        critical_internal = [e for e in critical if e.is_internal]
        high_internal = [e for e in high if e.is_internal]
        
        return f"""## 📊 Executive Summary

### Priority Breakdown
- **CRITICAL:** {len(critical)} endpoints ({len(critical_internal)} internal)
- **HIGH:** {len(high)} endpoints ({len(high_internal)} internal)
- **MEDIUM:** {sum(1 for e in self.endpoint_infos if e.priority == Priority.MEDIUM)} endpoints
- **LOW:** {sum(1 for e in self.endpoint_infos if e.priority == Priority.LOW)} endpoints

### Risk Assessment
- **{len(critical_internal)}** critical internal endpoints need public alternatives
- **{len(high_internal)}** high-priority internal endpoints at risk
- **{sum(1 for e in self.endpoint_infos if e.is_internal and e.public_alternative)}** internal endpoints have identified alternatives

---"""
    
    def _generate_priority_table(self, priority: Priority) -> str:
        """Generate table for specific priority level.
        
        Args:
            priority: Priority level to generate
            
        Returns:
            Markdown table
        """
        endpoints = [e for e in self.endpoint_infos if e.priority == priority]
        
        if not endpoints:
            return f"## {priority.value} Priority Endpoints\n\n_No endpoints in this category._"
        
        # Sort by usage count (desc), then by domain
        endpoints.sort(key=lambda e: (-e.usage_count, e.domain, e.path))
        
        lines = [f"## {priority.value} Priority Endpoints ({len(endpoints)} total)"]
        lines.append("")
        lines.append("| Endpoint | Domain | Type | Usage | Used By (Sample) | Notes |")
        lines.append("|----------|--------|------|-------|------------------|-------|")
        
        for ep in endpoints:
            # Truncate path if too long
            path_display = ep.path if len(ep.path) < 50 else ep.path[:47] + "..."
            
            # Type indicator
            type_icon = "⚠️ Internal" if ep.is_internal else "✅ Public"
            
            # Used by sample (first 2 functions)
            used_by_sample = ", ".join(ep.used_by[:2])
            if len(ep.used_by) > 2:
                used_by_sample += f" (+{len(ep.used_by) - 2} more)"
            
            # Notes
            notes = []
            if ep.is_internal and ep.public_alternative:
                notes.append(f"Alt: `{ep.public_alternative}`")
            elif ep.is_internal and priority in (Priority.CRITICAL, Priority.HIGH):
                notes.append("⚠️ **No public alternative**")
            if ep.usage_count == 0:
                notes.append("_Unused_")
            
            notes_str = " ".join(notes) if notes else "-"
            
            lines.append(
                f"| `{path_display}` | {ep.domain} | {type_icon} | "
                f"{ep.usage_count}x | {used_by_sample or '-'} | {notes_str} |"
            )
        
        return "\n".join(lines)
    
    def _generate_gap_analysis(self) -> str:
        """Generate internal vs public API gap analysis.
        
        Returns:
            Markdown section
        """
        # Find critical internal endpoints without public alternatives
        critical_gaps = [
            e for e in self.endpoint_infos
            if e.is_internal
            and e.priority in (Priority.CRITICAL, Priority.HIGH)
            and not e.public_alternative
        ]
        
        if not critical_gaps:
            return """## 🎯 Public API Gap Analysis

✅ **All critical internal endpoints have public alternatives!**

---"""
        
        # Group by domain
        by_domain: Dict[str, List[EndpointInfo]] = defaultdict(list)
        for ep in critical_gaps:
            by_domain[ep.domain].append(ep)
        
        lines = [
            "## 🎯 Public API Gap Analysis",
            "",
            f"**{len(critical_gaps)} critical/high-priority internal endpoints need public alternatives**",
            ""
        ]
        
        for domain in sorted(by_domain.keys()):
            eps = by_domain[domain]
            lines.append(f"### {domain} Domain ({len(eps)} gaps)")
            lines.append("")
            lines.append("| Endpoint | Priority | Usage | Migration Effort |")
            lines.append("|----------|----------|-------|------------------|")
            
            for ep in sorted(eps, key=lambda x: -x.usage_count):
                effort = self._estimate_migration_effort(ep)
                lines.append(
                    f"| `{ep.path}` | {ep.priority.value} | "
                    f"{ep.usage_count}x | {effort} |"
                )
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _estimate_migration_effort(self, endpoint: EndpointInfo) -> str:
        """Estimate migration effort for creating public alternative.
        
        Args:
            endpoint: Endpoint to assess
            
        Returns:
            Effort estimate string
        """
        # Simple heuristic based on usage count and complexity
        if endpoint.usage_count > 20:
            return "High (20+ usages)"
        elif endpoint.usage_count > 5:
            return "Medium (5-20 usages)"
        else:
            return "Low (<5 usages)"
    
    def _generate_migration_recommendations(self) -> str:
        """Generate migration recommendations.
        
        Returns:
            Markdown section
        """
        # Find internal endpoints with high usage
        high_usage_internal = [
            e for e in self.endpoint_infos
            if e.is_internal and e.usage_count > 10
        ]
        
        high_usage_internal.sort(key=lambda e: -e.usage_count)
        
        lines = [
            "## 📋 Migration Recommendations",
            "",
            "### Phase 1: Critical Path (Immediate)",
            ""
        ]
        
        # Recommend critical endpoints first
        critical = [e for e in high_usage_internal if e.priority == Priority.CRITICAL][:5]
        for i, ep in enumerate(critical, 1):
            lines.append(
                f"{i}. **{ep.domain}.{ep.path}** ({ep.usage_count} usages) - "
                f"{ep.description}"
            )
        
        lines.extend([
            "",
            "### Phase 2: High Priority (Next Quarter)",
            ""
        ])
        
        # Recommend high priority next
        high = [e for e in high_usage_internal if e.priority == Priority.HIGH][:5]
        for i, ep in enumerate(high, 1):
            lines.append(
                f"{i}. **{ep.domain}.{ep.path}** ({ep.usage_count} usages) - "
                f"{ep.description}"
            )
        
        lines.extend([
            "",
            "### Migration Strategy",
            "",
            "1. **Create public endpoints** for Phase 1 critical path",
            "2. **Deprecate internal endpoints** with 6-month sunset period",
            "3. **Migrate usage** incrementally (domain by domain)",
            "4. **Remove internal endpoints** after migration complete",
            "",
            "---"
        ])
        
        return "\n".join(lines)
    
    def _generate_usage_stats(self) -> str:
        """Generate usage statistics section.
        
        Returns:
            Markdown section
        """
        # Calculate stats
        total = len(self.endpoint_infos)
        used = sum(1 for e in self.endpoint_infos if e.usage_count > 0)
        unused = total - used
        total_usage = sum(e.usage_count for e in self.endpoint_infos)
        
        # Most used endpoints
        most_used = sorted(self.endpoint_infos, key=lambda e: -e.usage_count)[:10]
        
        lines = [
            "## 📈 Usage Statistics",
            "",
            "### Overall",
            f"- **Total Endpoints:** {total}",
            f"- **Used Endpoints:** {used} ({used/total*100:.1f}%)",
            f"- **Unused Endpoints:** {unused} ({unused/total*100:.1f}%)",
            f"- **Total Usage Count:** {total_usage}",
            f"- **Average Usage:** {total_usage/total:.1f} calls per endpoint",
            "",
            "### Top 10 Most Used Endpoints",
            ""
        ]
        
        for i, ep in enumerate(most_used, 1):
            internal_marker = "⚠️" if ep.is_internal else "✅"
            lines.append(
                f"{i}. {internal_marker} `{ep.path}` - **{ep.usage_count}** usages "
                f"({ep.priority.value})"
            )
        
        return "\n".join(lines)
