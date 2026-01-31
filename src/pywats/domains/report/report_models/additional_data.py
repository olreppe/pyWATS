"""
Additional Data Compatibility Module

This module re-exports AdditionalData and related classes from binary_data.py
for backward compatibility with code that imports from additional_data.

In V3, these classes were consolidated into binary_data.py.
"""
from .binary_data import (
    AdditionalData,
    AdditionalDataProperty,
    AdditionalDataArray,
    AdditionalDataArrayIndex,
)

__all__ = [
    "AdditionalData",
    "AdditionalDataProperty",
    "AdditionalDataArray",
    "AdditionalDataArrayIndex",
]
