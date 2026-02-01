"""
Tests for PersistentQueue priority-based ordering.

This test suite verifies that PersistentQueue correctly implements priority-based
item processing with file persistence. Tests cover:
- Priority parameter in add() method
- Priority persistence in metadata files
- Priority restoration on queue reload
- Priority-based ordering after disk operations
"""

import time
import json
import tempfile
import shutil
from pathlib import Path
import pytest

from pywats_client.queue import PersistentQueue
from pywats.queue import QueueItemStatus


@pytest.fixture
def temp_queue_dir():
    """Create a temporary directory for queue files."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


def test_add_with_priority(temp_queue_dir):
    """Test that add() method accepts and persists priority parameter."""
    queue = PersistentQueue(queue_dir=temp_queue_dir)
    
    item = queue.add({"test": "data"}, priority=3)
    
    assert item.priority == 3
    
    # Verify priority is in metadata file
    meta_path = temp_queue_dir / f"{item.id}.pending.meta.json"
    assert meta_path.exists()
    
    with open(meta_path) as f:
        meta = json.load(f)
    
    assert meta['priority'] == 3


def test_default_priority_in_persistent_add(temp_queue_dir):
    """Test that items added without priority get default priority=5."""
    queue = PersistentQueue(queue_dir=temp_queue_dir)
    
    item = queue.add({"test": "data"})
    
    assert item.priority == 5
    
    # Verify in metadata
    meta_path = temp_queue_dir / f"{item.id}.pending.meta.json"
    with open(meta_path) as f:
        meta = json.load(f)
    
    assert meta['priority'] == 5


def test_priority_ordering_with_persistence(temp_queue_dir):
    """Test that items are retrieved in priority order from persistent queue."""
    queue = PersistentQueue(queue_dir=temp_queue_dir)
    
    item_low = queue.add({"task": "low"}, priority=10)
    item_high = queue.add({"task": "high"}, priority=1)
    item_med = queue.add({"task": "medium"}, priority=5)
    
    # Should get highest priority first
    next_item = queue.get_next()
    assert next_item.id == item_high.id
    
    next_item = queue.get_next()
    assert next_item.id == item_med.id
    
    next_item = queue.get_next()
    assert next_item.id == item_low.id


def test_priority_restored_on_reload(temp_queue_dir):
    """Test that priority is correctly restored when reloading from disk."""
    # Create queue and add items
    queue1 = PersistentQueue(queue_dir=temp_queue_dir)
    
    item_low = queue1.add({"task": "low"}, priority=8)
    item_high = queue1.add({"task": "high"}, priority=2)
    item_med = queue1.add({"task": "medium"}, priority=5)
    
    # Close and reload
    del queue1
    
    queue2 = PersistentQueue(queue_dir=temp_queue_dir, auto_load=True)
    
    # Verify items loaded with correct priorities
    high_item = queue2.get(item_high.id)
    assert high_item.priority == 2
    
    med_item = queue2.get(item_med.id)
    assert med_item.priority == 5
    
    low_item = queue2.get(item_low.id)
    assert low_item.priority == 8
    
    # Verify priority ordering still works
    next_item = queue2.get_next()
    assert next_item.id == item_high.id


def test_priority_ordering_after_reload(temp_queue_dir):
    """Test that heap-based priority ordering works correctly after reload."""
    # Add items
    queue1 = PersistentQueue(queue_dir=temp_queue_dir)
    
    for i in range(10):
        priority = (i % 3) + 1  # Priorities 1, 2, 3
        queue1.add({"task": f"task_{i}"}, priority=priority)
    
    del queue1
    
    # Reload and verify ordering
    queue2 = PersistentQueue(queue_dir=temp_queue_dir, auto_load=True)
    
    prev_priority = 0
    count = 0
    
    while True:
        item = queue2.get_next()
        if item is None:
            break
        
        count += 1
        # Verify priority is non-decreasing
        assert item.priority >= prev_priority
        prev_priority = item.priority
    
    assert count == 10


def test_priority_preserved_through_status_changes(temp_queue_dir):
    """Test that priority is maintained when item status changes."""
    queue = PersistentQueue(queue_dir=temp_queue_dir)
    
    item = queue.add({"task": "test"}, priority=3)
    
    # Change to processing
    item_obj = queue.get(item.id)
    item_obj.mark_processing()
    queue.update(item_obj)
    
    # Verify priority preserved in metadata
    meta_path = temp_queue_dir / f"{item.id}.processing.meta.json"
    with open(meta_path) as f:
        meta = json.load(f)
    
    assert meta['priority'] == 3
    
    # Change to failed
    item_obj.mark_failed("test error")
    queue.update(item_obj)
    
    # Verify priority still preserved
    meta_path = temp_queue_dir / f"{item.id}.failed.meta.json"
    with open(meta_path) as f:
        meta = json.load(f)
    
    assert meta['priority'] == 3


def test_backward_compatibility_missing_priority_in_metadata(temp_queue_dir):
    """Test that old metadata files without priority field work correctly."""
    queue = PersistentQueue(queue_dir=temp_queue_dir, auto_load=False)
    
    # Manually create old-style metadata file without priority
    item_id = "test_item_123"
    meta_path = temp_queue_dir / f"{item_id}.pending.meta.json"
    data_path = temp_queue_dir / f"{item_id}.pending.wsjf"
    
    # Write data file
    with open(data_path, 'w') as f:
        json.dump({"test": "data"}, f)
    
    # Write metadata without priority field
    with open(meta_path, 'w') as f:
        json.dump({
            'id': item_id,
            'status': 'pending',
            'created_at': '2024-01-01T12:00:00',
            'updated_at': '2024-01-01T12:00:00',
            'attempts': 0,
            'max_attempts': 3,
            # Note: no 'priority' field
        }, f)
    
    # Load queue
    queue._load_from_disk()
    
    # Verify item loaded with default priority
    item = queue.get(item_id)
    assert item is not None
    assert item.priority == 5


def test_list_by_status_respects_priority(temp_queue_dir):
    """Test that list_by_status returns items in priority order."""
    queue = PersistentQueue(queue_dir=temp_queue_dir)
    
    item_low = queue.add({"task": "low"}, priority=10)
    item_high = queue.add({"task": "high"}, priority=1)
    item_med = queue.add({"task": "medium"}, priority=5)
    
    pending_items = queue.list_pending()
    
    assert len(pending_items) == 3
    assert pending_items[0].id == item_high.id
    assert pending_items[1].id == item_med.id
    assert pending_items[2].id == item_low.id


def test_retry_readds_to_heap_with_priority(temp_queue_dir):
    """Test that retrying failed items re-adds them to heap with correct priority."""
    queue = PersistentQueue(queue_dir=temp_queue_dir)
    
    item1 = queue.add({"task": "task1"}, priority=5)
    item2 = queue.add({"task": "task2"}, priority=10)
    
    # Process and fail item1
    next_item = queue.get_next()
    assert next_item.id == item1.id
    
    next_item.mark_failed("test error")
    queue.update(next_item)
    
    # Process item2
    next_item = queue.get_next()
    assert next_item.id == item2.id
    
    # Retry item1 with higher priority
    item1_obj = queue.get(item1.id)
    item1_obj.reset_to_pending()
    item1_obj.priority = 1  # Higher priority
    queue.update(item1_obj)
    
    # Should get retried item1 next
    next_item = queue.get_next()
    assert next_item.id == item1.id
    assert next_item.priority == 1


def test_priority_with_delete_completed(temp_queue_dir):
    """Test that priority works correctly with delete_completed=True."""
    queue = PersistentQueue(queue_dir=temp_queue_dir, delete_completed=True)
    
    item1 = queue.add({"task": "task1"}, priority=1)
    item2 = queue.add({"task": "task2"}, priority=2)
    
    # Complete item1
    item1_obj = queue.get(item1.id)
    item1_obj.mark_completed()
    queue.update(item1_obj)
    
    # Verify item1 data file deleted (metadata may exist briefly)
    data_path = temp_queue_dir / f"{item1.id}.completed.wsjf"
    assert not data_path.exists(), "Completed data file should be deleted"
    
    # Verify item2 still works with correct priority
    next_item = queue.get_next()
    assert next_item.id == item2.id
    assert next_item.priority == 2


def test_heap_rebuilt_on_load_only_for_pending(temp_queue_dir):
    """Test that PENDING and recovered PROCESSING items are added to heap on reload."""
    queue1 = PersistentQueue(queue_dir=temp_queue_dir)
    
    item1 = queue1.add({"task": "pending"}, priority=1)
    item2 = queue1.add({"task": "will_process"}, priority=2)
    
    # Mark item2 as processing (it will be recovered to pending on reload)
    item2_obj = queue1.get(item2.id)
    item2_obj.mark_processing()
    queue1.update(item2_obj)
    
    del queue1
    
    # Reload - item2 should be recovered from PROCESSING to PENDING
    queue2 = PersistentQueue(queue_dir=temp_queue_dir, auto_load=True)
    
    # Both items should be pending (in priority order)
    next_item = queue2.get_next()
    assert next_item.id == item1.id
    assert next_item.priority == 1
    
    next_item = queue2.get_next()
    assert next_item.id == item2.id
    assert next_item.status == QueueItemStatus.PENDING
    assert next_item.priority == 2
    
    # No more pending items
    assert queue2.get_next() is None


def test_recovered_items_added_to_heap(temp_queue_dir):
    """Test that PROCESSING items recovered to PENDING are added to heap."""
    queue1 = PersistentQueue(queue_dir=temp_queue_dir)
    
    item1 = queue1.add({"task": "task1"}, priority=1)
    item2 = queue1.add({"task": "task2"}, priority=2)
    
    # Mark as processing (simulating crash)
    item1_obj = queue1.get(item1.id)
    item1_obj.mark_processing()
    queue1.update(item1_obj)
    
    del queue1
    
    # Reload - should recover processing item to pending
    queue2 = PersistentQueue(queue_dir=temp_queue_dir, auto_load=True)
    
    # Both items should be pending and in correct priority order
    next_item = queue2.get_next()
    assert next_item.id == item1.id
    assert next_item.status == QueueItemStatus.PENDING
    
    next_item = queue2.get_next()
    assert next_item.id == item2.id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
