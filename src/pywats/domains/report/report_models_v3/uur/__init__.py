"""
UUR Package - v3 Implementation

Unit Under Repair (UUR) report models for repair/rework documentation.
Simpler than UUT: no test steps, failures stored on sub-units.
"""
from __future__ import annotations

from .uur_failure import UURFailure
from .uur_sub_unit import UURSubUnit
from .uur_info import UURInfo
from .uur_report import UURReport

__all__ = [
    "UURFailure",
    "UURSubUnit",
    "UURInfo",
    "UURReport",
]
