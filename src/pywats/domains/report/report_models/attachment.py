"""
Attachment Compatibility Module

This module re-exports Attachment from binary_data.py
for backward compatibility with code that imports from attachment.

In V3, Attachment was consolidated into binary_data.py.
"""
from .binary_data import Attachment

__all__ = ["Attachment"]
