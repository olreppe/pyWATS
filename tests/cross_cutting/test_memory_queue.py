"""Tests for MemoryQueue and QueueItem.

Tests the core in-memory queue implementation used by pyWATS.
"""
import pytest
import threading
import time
from datetime import datetime

from pywats.queue.memory_queue import MemoryQueue, QueueItem, BaseQueue
from pywats.shared.enums import QueueItemStatus


class TestQueueItem:
    """Tests for QueueItem dataclass."""
    
    def test_create_item(self):
        """Test creating a queue item via create method."""
        item = QueueItem.create(data={"key": "value"})
        
        assert item.id is not None
        assert len(item.id) == 36  # UUID format
        assert item.data == {"key": "value"}
        assert item.status == QueueItemStatus.PENDING
        assert item.attempts == 0
        assert item.max_attempts == 3
    
    def test_create_item_with_custom_id(self):
        """Test creating item with custom ID."""
        item = QueueItem.create(data="test", item_id="CUSTOM-001")
        
        assert item.id == "CUSTOM-001"
    
    def test_create_item_with_max_attempts(self):
        """Test setting custom max attempts."""
        item = QueueItem.create(data="test", max_attempts=5)
        
        assert item.max_attempts == 5
    
    def test_create_item_with_metadata(self):
        """Test setting metadata."""
        item = QueueItem.create(data="test", metadata={"source": "test"})
        
        assert item.metadata == {"source": "test"}
    
    def test_mark_processing(self):
        """Test marking item as processing."""
        item = QueueItem.create(data="test")
        original_time = item.updated_at
        
        time.sleep(0.01)  # Small delay to ensure time changes
        item.mark_processing()
        
        assert item.status == QueueItemStatus.PROCESSING
        assert item.attempts == 1
        assert item.updated_at > original_time
    
    def test_mark_completed(self):
        """Test marking item as completed."""
        item = QueueItem.create(data="test")
        item.mark_processing()
        item.mark_completed()
        
        assert item.status == QueueItemStatus.COMPLETED
        assert item.last_error is None
    
    def test_mark_failed(self):
        """Test marking item as failed."""
        item = QueueItem.create(data="test")
        item.mark_processing()
        item.mark_failed("Connection error")
        
        assert item.status == QueueItemStatus.FAILED
        assert item.last_error == "Connection error"
    
    def test_mark_suspended(self):
        """Test marking item as suspended."""
        item = QueueItem.create(data="test")
        item.mark_suspended("Server overloaded")
        
        assert item.status == QueueItemStatus.SUSPENDED
        assert item.last_error == "Server overloaded"
    
    def test_mark_suspended_no_reason(self):
        """Test marking suspended without reason."""
        item = QueueItem.create(data="test")
        item.mark_suspended()
        
        assert item.status == QueueItemStatus.SUSPENDED
    
    def test_reset_to_pending(self):
        """Test resetting item to pending."""
        item = QueueItem.create(data="test")
        item.mark_processing()
        item.mark_failed("Error")
        item.reset_to_pending()
        
        assert item.status == QueueItemStatus.PENDING
    
    def test_can_retry_property(self):
        """Test can_retry property."""
        item = QueueItem.create(data="test", max_attempts=2)
        
        assert item.can_retry is True
        
        item.mark_processing()
        assert item.can_retry is True
        
        item.mark_processing()
        assert item.can_retry is False
    
    def test_status_properties(self):
        """Test status check properties."""
        item = QueueItem.create(data="test")
        
        assert item.is_pending is True
        assert item.is_processing is False
        assert item.is_completed is False
        assert item.is_failed is False
        
        item.mark_processing()
        assert item.is_pending is False
        assert item.is_processing is True
        
        item.mark_completed()
        assert item.is_completed is True
        assert item.is_processing is False
    
    def test_to_dict(self):
        """Test serialization to dict."""
        item = QueueItem.create(data="test", item_id="TEST-001", metadata={"key": "val"})
        
        d = item.to_dict()
        
        assert d["id"] == "TEST-001"
        assert d["status"] == QueueItemStatus.PENDING.value
        assert d["attempts"] == 0
        assert d["max_attempts"] == 3
        assert d["metadata"] == {"key": "val"}
        assert "created_at" in d
        assert "updated_at" in d
    
    def test_from_dict(self):
        """Test deserialization from dict."""
        d = {
            "id": "TEST-002",
            "status": QueueItemStatus.PROCESSING.value,
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T11:00:00",
            "attempts": 2,
            "max_attempts": 5,
            "last_error": "Some error",
            "metadata": {"source": "test"}
        }
        
        item = QueueItem.from_dict(d, data="restored_data")
        
        assert item.id == "TEST-002"
        assert item.status == QueueItemStatus.PROCESSING
        assert item.data == "restored_data"
        assert item.attempts == 2
        assert item.max_attempts == 5
        assert item.last_error == "Some error"


class TestMemoryQueue:
    """Tests for MemoryQueue class."""
    
    def test_initialization(self):
        """Test queue initialization."""
        queue = MemoryQueue()
        
        assert queue.size == 0
        assert queue.get_stats().pending == 0
    
    def test_initialization_with_max_size(self):
        """Test queue with max size."""
        queue = MemoryQueue(max_size=10)
        
        # Should work up to max size
        for i in range(10):
            queue.add(data=f"item_{i}")
        
        assert queue.size == 10
        
        # Should raise when full
        with pytest.raises(ValueError, match="Queue is full"):
            queue.add(data="overflow")
    
    def test_add_item(self):
        """Test adding items to queue."""
        queue = MemoryQueue()
        
        item = queue.add(data={"key": "value"})
        
        assert item is not None
        assert queue.size == 1
    
    def test_add_with_custom_id(self):
        """Test adding item with custom ID."""
        queue = MemoryQueue()
        
        item = queue.add(data="test", item_id="CUSTOM-001")
        
        assert item.id == "CUSTOM-001"
    
    def test_get_next(self):
        """Test getting next pending item."""
        queue = MemoryQueue()
        
        queue.add(data="first")
        queue.add(data="second")
        
        item = queue.get_next()
        
        assert item is not None
        assert item.data == "first"  # FIFO order
    
    def test_get_next_empty_queue(self):
        """Test get_next on empty queue returns None."""
        queue = MemoryQueue()
        
        item = queue.get_next()
        
        assert item is None
    
    def test_get_next_skips_non_pending(self):
        """Test get_next skips non-pending items."""
        queue = MemoryQueue()
        
        item1 = queue.add(data="first")
        queue.add(data="second")
        
        # Mark first as processing
        item1.mark_processing()
        queue.update(item1)
        
        # Should get second
        next_item = queue.get_next()
        assert next_item.data == "second"
    
    def test_get_item_by_id(self):
        """Test getting item by ID."""
        queue = MemoryQueue()
        
        item = queue.add(data="test", item_id="TEST-001")
        
        retrieved = queue.get("TEST-001")
        
        assert retrieved is not None
        assert retrieved.id == "TEST-001"
    
    def test_get_item_not_found(self):
        """Test getting non-existent item."""
        queue = MemoryQueue()
        
        item = queue.get("NONEXISTENT")
        
        assert item is None
    
    def test_update_item(self):
        """Test updating item in queue."""
        queue = MemoryQueue()
        
        item = queue.add(data="test")
        item.mark_processing()
        queue.update(item)
        
        retrieved = queue.get(item.id)
        assert retrieved.status == QueueItemStatus.PROCESSING
    
    def test_remove_item(self):
        """Test removing item from queue."""
        queue = MemoryQueue()
        
        item = queue.add(data="test", item_id="TO-REMOVE")
        assert queue.size == 1
        
        result = queue.remove("TO-REMOVE")
        
        assert result is True
        assert queue.size == 0
        assert queue.get("TO-REMOVE") is None
    
    def test_remove_nonexistent_item(self):
        """Test removing non-existent item returns False."""
        queue = MemoryQueue()
        
        result = queue.remove("NONEXISTENT")
        
        assert result is False
    
    def test_list_by_status(self):
        """Test listing items by status."""
        queue = MemoryQueue()
        
        item1 = queue.add(data="first")
        item2 = queue.add(data="second")
        item3 = queue.add(data="third")
        
        item1.mark_processing()
        item1.mark_completed()
        queue.update(item1)
        
        item2.mark_processing()
        queue.update(item2)
        
        pending = queue.list_by_status(QueueItemStatus.PENDING)
        processing = queue.list_by_status(QueueItemStatus.PROCESSING)
        completed = queue.list_by_status(QueueItemStatus.COMPLETED)
        
        assert len(pending) == 1
        assert len(processing) == 1
        assert len(completed) == 1
    
    def test_count_by_status(self):
        """Test counting items by status."""
        queue = MemoryQueue()
        
        for i in range(5):
            queue.add(data=f"item_{i}")
        
        assert queue.count_by_status(QueueItemStatus.PENDING) == 5
        assert queue.count_by_status(QueueItemStatus.PROCESSING) == 0
    
    def test_list_pending(self):
        """Test listing pending items."""
        queue = MemoryQueue()
        
        queue.add(data="first")
        queue.add(data="second")
        
        pending = queue.list_pending()
        
        assert len(pending) == 2
    
    def test_clear_all(self):
        """Test clearing all items."""
        queue = MemoryQueue()
        
        for i in range(5):
            queue.add(data=f"item_{i}")
        
        removed = queue.clear()
        
        assert removed == 5
        assert queue.size == 0
    
    def test_clear_by_status(self):
        """Test clearing items by status."""
        queue = MemoryQueue()
        
        item1 = queue.add(data="first")
        item2 = queue.add(data="second")
        queue.add(data="third")
        
        item1.mark_processing()
        item1.mark_completed()
        queue.update(item1)
        
        item2.mark_processing()
        item2.mark_completed()
        queue.update(item2)
        
        # Clear only completed
        removed = queue.clear(QueueItemStatus.COMPLETED)
        
        assert removed == 2
        assert queue.size == 1
    
    def test_get_stats(self):
        """Test getting queue statistics."""
        queue = MemoryQueue()
        
        item1 = queue.add(data="first")
        queue.add(data="second")
        queue.add(data="third")
        
        item1.mark_processing()
        queue.update(item1)
        
        stats = queue.get_stats()
        
        assert stats.pending == 2
        assert stats.processing == 1
        assert stats.completed == 0
        assert stats.failed == 0
        assert stats.total == 3


class TestMemoryQueueThreadSafety:
    """Tests for thread safety of MemoryQueue."""
    
    def test_concurrent_add(self):
        """Test concurrent add operations."""
        queue = MemoryQueue()
        errors = []
        
        def add_items(start):
            try:
                for i in range(100):
                    queue.add(data=f"item_{start}_{i}")
            except Exception as e:
                errors.append(e)
        
        threads = [
            threading.Thread(target=add_items, args=(i,))
            for i in range(5)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
        assert queue.size == 500
    
    def test_concurrent_get_next(self):
        """Test concurrent get_next operations."""
        queue = MemoryQueue()
        
        # Add some items
        for i in range(100):
            queue.add(data=f"item_{i}")
        
        retrieved = []
        lock = threading.Lock()
        
        def get_items():
            while True:
                item = queue.get_next()
                if item is None:
                    break
                item.mark_processing()
                queue.update(item)
                with lock:
                    retrieved.append(item.id)
        
        threads = [threading.Thread(target=get_items) for _ in range(5)]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Should have processed all items
        assert len(retrieved) == 100
        # No duplicates
        assert len(set(retrieved)) == 100


class TestQueueIntegration:
    """Integration tests for queue workflows."""
    
    def test_processing_workflow(self):
        """Test typical processing workflow."""
        queue = MemoryQueue()
        
        # Add items
        for i in range(3):
            queue.add(data=f"item_{i}")
        
        # Process items
        processed = 0
        while (item := queue.get_next()) is not None:
            item.mark_processing()
            queue.update(item)
            
            # Simulate processing
            item.mark_completed()
            queue.update(item)
            processed += 1
        
        assert processed == 3
        assert queue.count_by_status(QueueItemStatus.COMPLETED) == 3
    
    def test_retry_workflow(self):
        """Test retry workflow with failures."""
        queue = MemoryQueue(default_max_attempts=3)
        
        item = queue.add(data="test")
        
        # First attempt - fails
        item.mark_processing()
        item.mark_failed("Error 1")
        queue.update(item)
        
        # Reset for retry
        item.reset_to_pending()
        queue.update(item)
        
        # Second attempt - succeeds
        item.mark_processing()
        item.mark_completed()
        queue.update(item)
        
        assert item.attempts == 2
        assert item.is_completed
