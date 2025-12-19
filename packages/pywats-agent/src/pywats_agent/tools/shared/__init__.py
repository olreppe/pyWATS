"""
Shared utilities for agent tools.

This package contains utilities used across multiple tool domains:
- adaptive_time: Smart time window selection based on volume
- process_resolver: Fuzzy process name matching
- dimensional: Dimensional analysis for failure modes
"""

from .adaptive_time import (
    AdaptiveTimeFilter,
    AdaptiveTimeConfig,
    AdaptiveTimeResult,
    VolumeCategory,
)
from .process_resolver import (
    ProcessResolver,
    PROCESS_ALIASES,
    normalize_process_name,
    diagnose_mixed_process_problem,
)

__all__ = [
    # Adaptive time
    "AdaptiveTimeFilter",
    "AdaptiveTimeConfig",
    "AdaptiveTimeResult",
    "VolumeCategory",
    # Process resolver
    "ProcessResolver",
    "PROCESS_ALIASES",
    "normalize_process_name",
    "diagnose_mixed_process_problem",
]
