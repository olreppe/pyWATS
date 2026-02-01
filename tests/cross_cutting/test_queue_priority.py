"""
Tests for queue priority functionality in QueueItem.

Tests priority field, comparison operators, and FIFO within same priority.
"""
import time
import pytest
from pywats.queue import QueueItem, QueueItemStatus


class TestQueueItemPriority:
    """Test QueueItem priority field and comparison"""
    
    def test_default_priority(self):
        """Test default priority is 5"""
        item = QueueItem.create(data={"test": "data"})
        assert item.priority == 5
    
    def test_custom_priority(self):
        """Test custom priority values"""
        high = QueueItem.create(data={}, priority=1)
        low = QueueItem.create(data={}, priority=10)
        medium = QueueItem.create(data={}, priority=5)
        
        assert high.priority == 1
        assert low.priority == 10
        assert medium.priority == 5
    
    def test_priority_comparison_ordering(self):
        """Test items sort by priority (lower number = higher priority)"""
        high = QueueItem.create(data={}, priority=1)
        medium = QueueItem.create(data={}, priority=5)
        low = QueueItem.create(data={}, priority=10)
        
        # Lower priority number should compare as "less than"
        assert high < medium
        assert medium < low
        assert high < low
    
    def test_fifo_within_same_priority(self):
        """Test FIFO ordering within same priority level"""
        first = QueueItem.create(data={"order": "first"}, priority=5)
        time.sleep(0.002)  # Ensure different timestamp
        second = QueueItem.create(data={"order": "second"}, priority=5)
        time.sleep(0.002)
        third = QueueItem.create(data={"order": "third"}, priority=5)
        
        # Same priority, so created_at determines order
        assert first < second
        assert second < third
        assert first < third
    
    def test_priority_in_serialization(self):
        """Test priority included in to_dict()"""
        item = QueueItem.create(data={}, priority=3)
        d = item.to_dict()
        
        assert "priority" in d
        assert d["priority"] == 3
    
    def test_priority_in_deserialization(self):
        """Test priority loaded from from_dict()"""
        d = {
            "id": "test-id",
            "priority": 7,
            "status": "pending",
            "created_at": "2026-02-02T14:00:00",
            "updated_at": "2026-02-02T14:00:00",
            "attempts": 0,
            "max_attempts": 3,
            "last_error": None,
            "metadata": {},
        }
        
        item = QueueItem.from_dict(d, data={"test": "data"})
        assert item.priority == 7
    
    def test_backward_compatibility_missing_priority(self):
        """Test old dicts without priority get default=5"""
        d = {
            "id": "test-id",
            # No priority field
            "status": "pending",
            "created_at": "2026-02-02T14:00:00",
            "updated_at": "2026-02-02T14:00:00",
            "attempts": 0,
            "max_attempts": 3,
            "last_error": None,
            "metadata": {},
        }
        
        item = QueueItem.from_dict(d, data={})
        assert item.priority == 5  # Default
    
    def test_priority_preserved_through_status_changes(self):
        """Test priority unchanged when status changes"""
        item = QueueItem.create(data={}, priority=2)
        original_priority = item.priority
        
        item.mark_processing()
        assert item.priority == original_priority
        
        item.mark_completed()
        assert item.priority == original_priority
        
        item.mark_failed("error")
        assert item.priority == original_priority


class TestQueueItemHeapBehavior:
    """Test QueueItem works correctly in heap data structure"""
    
    def test_sorting_multiple_items(self):
        """Test multiple items sort correctly"""
        items = [
            QueueItem.create(data={}, priority=5),
            QueueItem.create(data={}, priority=1),
            QueueItem.create(data={}, priority=10),
            QueueItem.create(data={}, priority=3),
            QueueItem.create(data={}, priority=7),
        ]
        
        sorted_items = sorted(items)
        priorities = [item.priority for item in sorted_items]
        
        assert priorities == [1, 3, 5, 7, 10]
    
    def test_heap_ordering_with_heapq(self):
        """Test QueueItem works with heapq module"""
        import heapq
        
        heap = []
        heapq.heappush(heap, QueueItem.create(data="low", priority=10))
        heapq.heappush(heap, QueueItem.create(data="high", priority=1))
        heapq.heappush(heap, QueueItem.create(data="medium", priority=5))
        
        # Pop should give highest priority first
        first = heapq.heappop(heap)
        assert first.data == "high"
        assert first.priority == 1
        
        second = heapq.heappop(heap)
        assert second.data == "medium"
        assert second.priority == 5
        
        third = heapq.heappop(heap)
        assert third.data == "low"
        assert third.priority == 10
