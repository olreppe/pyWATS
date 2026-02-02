"""
Async Adapter for MemoryQueue

Bridges the thread-safe MemoryQueue to asyncio for use in async contexts.
This allows the same priority queue logic to be used in both sync and async code.

Design:
    MemoryQueue provides thread-safe heap-based priority queue
    AsyncQueueAdapter wraps it for async/await usage
    Uses asyncio.Event for async notification when items are added

This eliminates code duplication - one queue implementation used everywhere.
"""

import asyncio
import logging
from typing import Optional, Any, Generic, TypeVar
from datetime import datetime

from .memory_queue import MemoryQueue, QueueItem, QueueItemStatus

logger = logging.getLogger(__name__)

T = TypeVar('T')


class AsyncQueueAdapter(Generic[T]):
    """
    Async adapter for MemoryQueue.
    
    Wraps the thread-safe MemoryQueue to provide async/await interface.
    All priority queue logic is handled by MemoryQueue (heap-based, tested).
    
    This adapter just provides:
    - Async get() with await
    - Async notification when items added
    - Bridge between threading.RLock and asyncio
    
    Example:
        >>> from pywats.queue import MemoryQueue
        >>> from pywats.queue.async_adapter import AsyncQueueAdapter
        >>> 
        >>> # Create thread-safe queue
        >>> queue = MemoryQueue()
        >>> 
        >>> # Wrap for async use
        >>> async_queue = AsyncQueueAdapter(queue)
        >>> 
        >>> # Add items (thread-safe, can be called from sync code)
        >>> async_queue.put_nowait({"data": "report"}, priority=1)
        >>> 
        >>> # Get items (async, priority-first)
        >>> item = await async_queue.get()
    """
    
    def __init__(
        self,
        queue: Optional[MemoryQueue] = None,
        max_size: Optional[int] = None,
        default_max_attempts: int = 3,
    ) -> None:
        """
        Initialize async queue adapter.
        
        Args:
            queue: Existing MemoryQueue to wrap (creates new one if None)
            max_size: Maximum queue size (passed to MemoryQueue if creating new)
            default_max_attempts: Default max retry attempts for items
        """
        # Use existing queue or create new one
        if queue is not None:
            self._queue = queue
        else:
            self._queue = MemoryQueue(
                max_size=max_size,
                default_max_attempts=default_max_attempts
            )
        
        # Event for async notification when items added
        self._not_empty = asyncio.Event()
        
        # Store original add method
        self._original_add = self._queue.add
        
        # Monkey-patch add method to set asyncio event
        def add_with_notification(*args, **kwargs):
            """Wrapper to set asyncio event when item added"""
            result = self._original_add(*args, **kwargs)
            # Set event to wake up waiting get() calls
            # Note: This is thread-safe - asyncio.Event.set() can be called from any thread
            self._not_empty.set()
            return result
        
        # Install our wrapper
        self._queue.add = add_with_notification
        
        logger.debug(f"AsyncQueueAdapter initialized (max_size={max_size or 'unlimited'})")
    
    @property
    def queue(self) -> MemoryQueue:
        """Get underlying MemoryQueue (for direct access if needed)"""
        return self._queue
    
    # =========================================================================
    # Async Methods
    # =========================================================================
    
    async def get(self, timeout: Optional[float] = None) -> Optional[QueueItem]:
        """
        Get next item from queue (priority-first, then FIFO).
        
        Waits asynchronously until an item is available or timeout.
        
        Args:
            timeout: Maximum seconds to wait (None = wait forever)
            
        Returns:
            QueueItem with highest priority, or None if timeout
            
        Example:
            >>> item = await queue.get()
            >>> if item:
            >>>     print(f"Processing priority {item.priority}")
        """
        deadline = None
        if timeout is not None:
            deadline = asyncio.get_event_loop().time() + timeout
        
        while True:
            # Try to get item (thread-safe)
            item = self._queue.get_next()
            if item:
                return item
            
            # No items - wait for notification
            if deadline is not None:
                remaining = deadline - asyncio.get_event_loop().time()
                if remaining <= 0:
                    return None  # Timeout
                
                try:
                    await asyncio.wait_for(self._not_empty.wait(), timeout=remaining)
                except asyncio.TimeoutError:
                    return None
            else:
                await self._not_empty.wait()
            
            # Clear event for next wait (but check queue first in next iteration)
            self._not_empty.clear()
    
    async def get_batch(
        self,
        max_items: int,
        timeout: Optional[float] = 0.1
    ) -> list[QueueItem]:
        """
        Get multiple items from queue (up to max_items).
        
        Useful for batch processing. Returns immediately with available items,
        or waits up to timeout for first item.
        
        Args:
            max_items: Maximum items to retrieve
            timeout: Max seconds to wait for first item (0 = no wait)
            
        Returns:
            List of QueueItems (may be empty)
        """
        items = []
        
        # Get first item (with timeout)
        first_item = await self.get(timeout=timeout)
        if not first_item:
            return items
        
        items.append(first_item)
        
        # Get remaining items (non-blocking)
        while len(items) < max_items:
            item = self._queue.get_next()
            if not item:
                break
            items.append(item)
        
        return items
    
    # =========================================================================
    # Synchronous Methods (thread-safe, can be called from any thread)
    # =========================================================================
    
    def put_nowait(
        self,
        data: Any,
        priority: int = 5,
        item_id: Optional[str] = None,
        max_attempts: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> QueueItem:
        """
        Add item to queue immediately (thread-safe).
        
        Can be called from any thread (sync or async).
        Triggers async notification automatically.
        
        Args:
            data: Data payload for the item
            priority: Priority (1=highest, 10=lowest, default=5)
            item_id: Optional custom ID
            max_attempts: Max retry attempts (uses queue default if None)
            metadata: Optional metadata dict
            
        Returns:
            The created QueueItem
            
        Raises:
            QueueFullError: If queue is at max capacity
        """
        return self._queue.add(
            data=data,
            item_id=item_id,
            priority=priority,
            max_attempts=max_attempts,
            metadata=metadata,
        )
    
    def update(self, item: QueueItem) -> None:
        """
        Update item in queue (thread-safe).
        
        Args:
            item: QueueItem to update
        """
        self._queue.update(item)
    
    def remove(self, item_id: str) -> bool:
        """
        Remove item from queue (thread-safe).
        
        Args:
            item_id: ID of item to remove
            
        Returns:
            True if removed, False if not found
        """
        return self._queue.remove(item_id)
    
    # =========================================================================
    # Properties (thread-safe)
    # =========================================================================
    
    @property
    def size(self) -> int:
        """Get total number of items in queue"""
        return self._queue.size
    
    @property
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return self._queue.is_empty
    
    @property
    def is_full(self) -> bool:
        """Check if queue is at max capacity"""
        return self._queue.is_full
    
    def count_by_status(self, status: QueueItemStatus) -> int:
        """Count items with specific status"""
        return self._queue.count_by_status(status)
    
    @property
    def pending_count(self) -> int:
        """Get count of pending items"""
        return self._queue.count_by_status(QueueItemStatus.PENDING)
    
    @property
    def processing_count(self) -> int:
        """Get count of processing items"""
        return self._queue.count_by_status(QueueItemStatus.PROCESSING)
    
    def list_by_status(self, status: QueueItemStatus) -> list[QueueItem]:
        """Get all items with specific status"""
        return self._queue.list_by_status(status)
    
    def get_stats(self) -> dict:
        """Get queue statistics"""
        return self._queue.get_stats()
    
    def clear(self) -> None:
        """Clear all items from queue"""
        self._queue.clear()
    
    def __repr__(self) -> str:
        return f"AsyncQueueAdapter(size={self.size}, pending={self.pending_count})"
