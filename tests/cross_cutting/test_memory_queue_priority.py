"""
Tests for MemoryQueue priority-based ordering.

This test suite verifies that MemoryQueue correctly implements priority-based
item processing using a min-heap data structure. Tests cover:
- Priority-based ordering (highest priority first)
- FIFO ordering within the same priority
- Lazy cleanup of removed/status-changed items
- Retry operations (re-adding to heap)
- Thread safety with priorities
- Backward compatibility
"""

import time
from typing import Any
import pytest

from pywats.queue.memory_queue import MemoryQueue, QueueItem, QueueItemStatus


def test_priority_ordering_basic():
    """Test that items are retrieved in priority order (1=highest, 10=lowest)."""
    queue = MemoryQueue()
    
    # Add items with different priorities
    item_low = queue.add("low priority task", priority=10)
    item_high = queue.add("high priority task", priority=1)
    item_med = queue.add("medium priority task", priority=5)
    
    # Should get highest priority first
    next_item = queue.get_next()
    assert next_item is not None
    assert next_item.id == item_high.id
    assert next_item.data == "high priority task"
    
    # Then medium
    next_item = queue.get_next()
    assert next_item is not None
    assert next_item.id == item_med.id
    
    # Then low
    next_item = queue.get_next()
    assert next_item is not None
    assert next_item.id == item_low.id


def test_fifo_within_same_priority():
    """Test that items with the same priority are processed FIFO."""
    queue = MemoryQueue()
    
    # Add multiple items with the same priority
    item1 = queue.add("task 1", priority=5)
    time.sleep(0.01)  # Ensure different timestamps
    item2 = queue.add("task 2", priority=5)
    time.sleep(0.01)
    item3 = queue.add("task 3", priority=5)
    
    # Should get items in FIFO order
    next_item = queue.get_next()
    assert next_item.id == item1.id
    
    next_item = queue.get_next()
    assert next_item.id == item2.id
    
    next_item = queue.get_next()
    assert next_item.id == item3.id


def test_mixed_priorities_with_fifo():
    """Test complex scenario with mixed priorities and timestamps."""
    queue = MemoryQueue()
    
    # Add items in non-priority order
    item1 = queue.add("low 1", priority=8)
    time.sleep(0.01)
    item2 = queue.add("high 1", priority=2)
    time.sleep(0.01)
    item3 = queue.add("low 2", priority=8)
    time.sleep(0.01)
    item4 = queue.add("high 2", priority=2)
    time.sleep(0.01)
    item5 = queue.add("medium", priority=5)
    
    # Expected order: high 1, high 2, medium, low 1, low 2
    assert queue.get_next().id == item2.id  # high 1
    assert queue.get_next().id == item4.id  # high 2
    assert queue.get_next().id == item5.id  # medium
    assert queue.get_next().id == item1.id  # low 1
    assert queue.get_next().id == item3.id  # low 2


def test_lazy_cleanup_removed_items():
    """Test that removed items are correctly cleaned up during get_next()."""
    queue = MemoryQueue()
    
    item1 = queue.add("task 1", priority=1)
    item2 = queue.add("task 2", priority=2)
    item3 = queue.add("task 3", priority=3)
    
    # Remove item2 before processing
    queue.remove(item2.id)
    
    # Should get item1, then skip item2 (removed), then item3
    assert queue.get_next().id == item1.id
    assert queue.get_next().id == item3.id
    assert queue.get_next() is None


def test_lazy_cleanup_status_changed_items():
    """Test that items with changed status are skipped during get_next()."""
    queue = MemoryQueue()
    
    item1 = queue.add("task 1", priority=1)
    item2 = queue.add("task 2", priority=2)
    item3 = queue.add("task 3", priority=3)
    
    # Change item2 to PROCESSING before calling get_next()
    item2_obj = queue.get(item2.id)
    item2_obj.status = QueueItemStatus.PROCESSING
    queue.update(item2_obj)
    
    # Should get item1, then skip item2 (not pending), then item3
    assert queue.get_next().id == item1.id
    assert queue.get_next().id == item3.id
    assert queue.get_next() is None


def test_retry_adds_item_back_to_heap():
    """Test that updating an item to PENDING status re-adds it to the heap."""
    queue = MemoryQueue()
    
    item1 = queue.add("task 1", priority=5)
    item2 = queue.add("task 2", priority=10)
    
    # Process item1
    next_item = queue.get_next()
    assert next_item.id == item1.id
    
    # Mark it as failed
    next_item.status = QueueItemStatus.FAILED
    next_item.attempts += 1
    queue.update(next_item)
    
    # Verify item2 would be next
    assert queue.get_next().id == item2.id
    
    # Now retry item1 with higher priority
    item1_obj = queue.get(item1.id)
    item1_obj.status = QueueItemStatus.PENDING
    item1_obj.priority = 1  # Give it higher priority
    queue.update(item1_obj)
    
    # Should get retried item1 next (highest priority)
    next_item = queue.get_next()
    assert next_item.id == item1.id


def test_default_priority_in_add():
    """Test that items added without priority get default priority=5."""
    queue = MemoryQueue()
    
    item = queue.add("task with default priority")
    
    assert item.priority == 5


def test_priority_preserved_in_list_by_status():
    """Test that list_by_status returns items in priority order."""
    queue = MemoryQueue()
    
    item_low = queue.add("low", priority=10)
    item_high = queue.add("high", priority=1)
    item_med = queue.add("medium", priority=5)
    
    pending_items = queue.list_pending()
    
    assert len(pending_items) == 3
    assert pending_items[0].id == item_high.id
    assert pending_items[1].id == item_med.id
    assert pending_items[2].id == item_low.id


def test_priority_preserved_in_iteration():
    """Test that iterating over the queue returns items in priority order."""
    queue = MemoryQueue()
    
    item_low = queue.add("low", priority=10)
    item_high = queue.add("high", priority=1)
    item_med = queue.add("medium", priority=5)
    
    items_list = list(queue)
    
    assert len(items_list) == 3
    assert items_list[0].id == item_high.id
    assert items_list[1].id == item_med.id
    assert items_list[2].id == item_low.id


def test_clear_all_clears_heap():
    """Test that clear() clears both items and heap."""
    queue = MemoryQueue()
    
    queue.add("task 1", priority=1)
    queue.add("task 2", priority=5)
    queue.add("task 3", priority=10)
    
    assert len(queue) == 3
    
    cleared = queue.clear()
    
    assert cleared == 3
    assert len(queue) == 0
    assert queue.get_next() is None


def test_clear_by_status_with_lazy_cleanup():
    """Test that clear() by status works with lazy cleanup."""
    queue = MemoryQueue()
    
    item1 = queue.add("task 1", priority=1)
    item2 = queue.add("task 2", priority=2)
    item3 = queue.add("task 3", priority=3)
    
    # Mark item2 as completed
    item2_obj = queue.get(item2.id)
    item2_obj.status = QueueItemStatus.COMPLETED
    queue.update(item2_obj)
    
    # Clear completed items
    cleared = queue.clear(QueueItemStatus.COMPLETED)
    assert cleared == 1
    
    # Should still get item1 and item3
    assert queue.get_next().id == item1.id
    assert queue.get_next().id == item3.id
    assert queue.get_next() is None


def test_get_next_any_with_priority():
    """Test that get_next_any respects priority ordering."""
    queue = MemoryQueue()
    
    item1 = queue.add("low pending", priority=10)
    item2 = queue.add("high pending", priority=1)
    
    # Mark item2 as suspended but can retry
    item2_obj = queue.get(item2.id)
    item2_obj.status = QueueItemStatus.SUSPENDED
    item2_obj.attempts = 1
    item2_obj.max_attempts = 3
    queue.update(item2_obj)
    
    # get_next_any should get high priority suspended item
    next_item = queue.get_next_any(include_suspended=True)
    assert next_item.id == item2.id


def test_heap_operations_with_many_items():
    """Test that heap operations work correctly with many items."""
    queue = MemoryQueue()
    
    # Add 100 items with random priorities
    items = []
    for i in range(100):
        priority = (i % 10) + 1  # Priorities 1-10
        item = queue.add(f"task {i}", priority=priority)
        items.append((item, priority))
    
    # Process all items
    prev_priority = 0
    prev_timestamp = None
    count = 0
    
    while True:
        next_item = queue.get_next()
        if next_item is None:
            break
        
        count += 1
        
        # Verify priority ordering
        assert next_item.priority >= prev_priority
        
        # If same priority, verify FIFO (timestamp ordering)
        if next_item.priority == prev_priority and prev_timestamp:
            assert next_item.created_at >= prev_timestamp
        
        prev_priority = next_item.priority
        prev_timestamp = next_item.created_at
    
    assert count == 100


def test_concurrent_add_and_get_with_priority():
    """Test thread safety of priority operations."""
    import threading
    
    queue = MemoryQueue()
    results = []
    errors = []
    
    def add_items():
        try:
            for i in range(50):
                priority = (i % 10) + 1
                queue.add(f"task {i}", priority=priority)
        except Exception as e:
            errors.append(e)
    
    def get_items():
        try:
            for _ in range(50):
                item = queue.get_next()
                if item:
                    results.append(item)
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)
    
    # Start threads
    add_thread = threading.Thread(target=add_items)
    get_thread = threading.Thread(target=get_items)
    
    add_thread.start()
    get_thread.start()
    
    add_thread.join()
    get_thread.join()
    
    assert len(errors) == 0, f"Errors occurred: {errors}"


def test_backward_compatibility_with_old_queue_items():
    """Test that old queue items without priority field work correctly."""
    queue = MemoryQueue()
    
    # Simulate old QueueItem without priority (uses default)
    from datetime import datetime
    now = datetime.now()
    item_dict = {
        "id": "test-123",
        "data": {"key": "value"},
        "status": "pending",
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "attempts": 0,
        "max_attempts": 3,
        # Note: no "priority" field
    }
    
    # Create QueueItem from dict (should default to priority=5)
    item = QueueItem.from_dict(item_dict, data={"key": "value"})
    assert item.priority == 5
    
    # Add to queue
    queue._items[item.id] = item
    import heapq
    heapq.heappush(queue._heap, item)
    
    # Should be retrievable
    next_item = queue.get_next()
    assert next_item.id == item.id
    assert next_item.priority == 5


def test_priority_in_stats():
    """Test that queue stats work correctly with priority items."""
    queue = MemoryQueue()
    
    queue.add("pending 1", priority=1)
    queue.add("pending 2", priority=5)
    item3 = queue.add("pending 3", priority=10)
    
    # Mark one as processing
    item3_obj = queue.get(item3.id)
    item3_obj.status = QueueItemStatus.PROCESSING
    queue.update(item3_obj)
    
    stats = queue.get_stats()
    assert stats.pending == 2
    assert stats.processing == 1


def test_remove_during_processing():
    """Test that removing an item during processing is handled correctly."""
    queue = MemoryQueue()
    
    item1 = queue.add("task 1", priority=1)
    item2 = queue.add("task 2", priority=2)
    item3 = queue.add("task 3", priority=3)
    
    # Get first item (doesn't remove it)
    next_item = queue.get_next()
    assert next_item.id == item1.id
    
    # Remove it explicitly
    queue.remove(item1.id)
    
    # Next should be item2
    next_item = queue.get_next()
    assert next_item.id == item2.id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
