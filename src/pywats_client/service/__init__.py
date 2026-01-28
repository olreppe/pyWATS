"""
pyWATS Client Service

Background service for WATS Client operations.
Runs independently of GUI, provides IPC for remote control.

Provides both sync and async implementations:
- ClientService: Traditional sync service (uses threading)
- AsyncClientService: Async-first service (uses asyncio)

For new applications, prefer AsyncClientService for better performance
and resource utilization.
"""

# Sync implementations (legacy)
from .client_service import ClientService
from .converter_pool import ConverterPool, ConversionItem
from .pending_watcher import PendingWatcher

# Async implementations (recommended)
from .async_client_service import (
    AsyncClientService,
    AsyncServiceStatus,
    run_async_service,
    run_async_service_with_qt,
)
from .async_converter_pool import (
    AsyncConverterPool,
    AsyncConversionItem,
    AsyncConversionItemState,
)
from .async_pending_queue import (
    AsyncPendingQueue,
    AsyncPendingQueueState,
)

__all__ = [
    # Sync (legacy)
    'ClientService',
    'ConverterPool',
    'ConversionItem',
    'PendingWatcher',
    # Async (recommended)
    'AsyncClientService',
    'AsyncServiceStatus',
    'AsyncConverterPool',
    'AsyncConversionItem',
    'AsyncConversionItemState',
    'AsyncPendingQueue',
    'AsyncPendingQueueState',
    # Entry points
    'run_async_service',
    'run_async_service_with_qt',
]
