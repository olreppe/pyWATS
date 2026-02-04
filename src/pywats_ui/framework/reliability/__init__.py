"""Reliability components for offline-capable Qt applications.

This module provides components for building resilient GUI applications that:
- Queue operations locally when server is unreachable (never lose data)
- Auto-reconnect to services with exponential backoff
- Support offline editing with automatic sync when connection restored
- Provide UI feedback for connection status and pending operations

Components:
    QueueManager: Local queue for failed operations with auto-retry
    ConnectionMonitor: Auto-reconnect logic with status events
    OfflineCapability: Mixin for offline-capable pages
"""

from .queue_manager import QueueManager, QueuedOperation, QueueStatus
from .connection_monitor import ConnectionMonitor, ConnectionStatus
from .offline_capability import OfflineCapability

__all__ = [
    'QueueManager',
    'QueuedOperation',
    'QueueStatus',
    'ConnectionMonitor',
    'ConnectionStatus',
    'OfflineCapability',
]
