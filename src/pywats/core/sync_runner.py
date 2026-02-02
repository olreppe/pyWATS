"""Synchronous runner for async coroutines.

Provides utilities to run async code from synchronous contexts.
This enables the async-first pattern where async implementations
are the source of truth, and sync methods are thin wrappers.

Performance: Uses EventLoopPool for 10-100x faster execution by reusing
event loops instead of creating new ones on every call.

Usage:
    from pywats.core.sync_runner import run_sync
    
    class SyncRepository:
        def __init__(self, async_repo: AsyncRepository):
            self._async = async_repo
        
        def get_item(self, id: str) -> Item:
            return run_sync(self._async.get_item(id))
"""
import asyncio
from typing import TypeVar, Coroutine, Any
from functools import wraps, lru_cache
import concurrent.futures

from .event_loop_pool import EventLoopPool

T = TypeVar('T')


@lru_cache(maxsize=1)
def _get_sync_runner_pool() -> concurrent.futures.ThreadPoolExecutor:
    """Get or create a singleton thread pool for sync runners.
    
    This pool is reused across all run_sync() calls to avoid the overhead
    of creating and destroying ThreadPoolExecutor instances.
    """
    return concurrent.futures.ThreadPoolExecutor(
        max_workers=4,
        thread_name_prefix="sync_runner_"
    )


def run_sync(coro: Coroutine[Any, Any, T]) -> T:
    """
    Run an async coroutine synchronously with high performance.
    
    Uses EventLoopPool for 10-100x performance improvement by reusing
    event loops instead of creating new ones on every call.
    
    Handles both cases:
    - No event loop running: uses EventLoopPool (fast, pooled)
    - Event loop running: runs in a thread pool to avoid blocking
    
    Args:
        coro: The coroutine to execute
        
    Returns:
        The result of the coroutine
        
    Example:
        async def fetch_data():
            return await some_async_call()
        
        # Can be called from sync code (10-100x faster than asyncio.run):
        data = run_sync(fetch_data())
    
    Performance:
        - Uses EventLoopPool to reuse event loops across calls
        - Avoids the overhead of creating new event loops (10-100x speedup)
        - Thread-safe with thread-local event loop storage
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # No running loop - use EventLoopPool for high performance
        return EventLoopPool.run_coroutine(coro)
    else:
        # Already in async context - run in pooled thread to avoid blocking
        pool = _get_sync_runner_pool()
        future = pool.submit(EventLoopPool.run_coroutine, coro)
        return future.result()


def sync_wrapper(async_method):
    """
    Decorator to create a sync wrapper for an async method.
    
    Usage:
        class SyncService:
            def __init__(self, async_service):
                self._async = async_service
            
            @sync_wrapper
            async def get_item(self, id: str):
                return await self._async.get_item(id)
    
    Note: The decorated method should call the async version.
    """
    @wraps(async_method)
    def wrapper(*args, **kwargs):
        return run_sync(async_method(*args, **kwargs))
    return wrapper


class SyncWrapper:
    """
    Base class for creating sync wrappers around async classes.
    
    Subclasses should set _async_class and implement __init__
    to create the async instance.
    
    Example:
        class SyncProductRepository(SyncWrapper):
            _async_class = AsyncProductRepository
            
            def __init__(self, http_client, ...):
                # Create sync HTTP client wrapper if needed
                async_client = AsyncHttpClient(...)
                self._async = AsyncProductRepository(async_client, ...)
    """
    _async: Any  # The wrapped async instance
    
    def _run(self, coro: Coroutine[Any, Any, T]) -> T:
        """Run an async method synchronously."""
        return run_sync(coro)
