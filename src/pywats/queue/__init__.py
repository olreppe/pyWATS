"""
Queue Management for pyWATS

Provides simple file-based queue for offline report submission.
All queued reports are stored in WSJF (WATS JSON Format).

For production deployments, use pywats_client.ClientService instead,
which provides robust file watching, converter framework, and retry logic.

This module is designed for simple scripts that need basic offline capability.
"""

from .simple_queue import SimpleQueue, QueuedReport, QueueStatus
from .formats import WSJFConverter, convert_to_wsjf, convert_from_wsxf, convert_from_wstf

__all__ = [
    "SimpleQueue",
    "QueuedReport",
    "QueueStatus",
    "WSJFConverter",
    "convert_to_wsjf",
    "convert_from_wsxf",
    "convert_from_wstf",
]
