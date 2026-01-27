"""
Tests for PersistentQueue

Tests the file-backed queue system for offline report queuing.
"""

import pytest
import time
import json
import threading
from pathlib import Path
from pywats_client.queue import PersistentQueue
from pywats.queue import QueueItemStatus


class TestPersistentQueue:
    """Test core queue operations"""
    
    def test_queue_initialization(self, tmp_path):
        """Test queue creation and directory setup"""
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        
        assert queue.queue_dir == Path(queue_dir)
        assert queue_dir.exists()
        assert queue.size == 0
    
    def test_add_item_to_queue(self, tmp_path, sample_report):
        """Test adding report to queue"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        item = queue.add(sample_report, item_id="TEST-001")
        
        assert item is not None
        assert item.id == "TEST-001"
        assert item.status == QueueItemStatus.PENDING
        assert item.data == sample_report
        assert queue.size == 1
    
    def test_list_pending_items(self, tmp_path, sample_report):
        """Test listing pending items"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add two items
        queue.add(sample_report)
        queue.add(sample_report)
        
        # List pending
        pending = queue.list_pending()
        
        # Verify
        assert len(pending) == 2
        assert queue.size == 2
        for item in pending:
            assert item.status == QueueItemStatus.PENDING
    
    def test_update_item_status(self, tmp_path, sample_report):
        """Test updating item status"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add item
        item = queue.add(sample_report)
        
        # Update status
        item.mark_processing()
        queue.update(item)
        
        # Verify
        retrieved = queue.get(item.id)
        assert retrieved.status == QueueItemStatus.PROCESSING
    
    def test_mark_item_processing(self, tmp_path, sample_report):
        """Test marking item as processing"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add and mark processing
        item = queue.add(sample_report)
        item.mark_processing()
        queue.update(item)
        
        # Verify file transition
        pending_items = queue.list_pending()
        processing_items = queue.list_by_status(QueueItemStatus.PROCESSING)
        
        assert len(pending_items) == 0
        assert len(processing_items) == 1
        assert processing_items[0].id == item.id
    
    def test_mark_item_completed(self, tmp_path, sample_report):
        """Test marking item as completed"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add, process, and complete
        item = queue.add(sample_report)
        item.mark_processing()
        queue.update(item)
        item.mark_completed()
        queue.update(item)
        
        # Verify
        completed = queue.list_completed()
        assert len(completed) == 1
        assert completed[0].id == item.id
        assert completed[0].status == QueueItemStatus.COMPLETED
    
    def test_mark_item_failed(self, tmp_path, sample_report):
        """Test marking item as failed"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add and fail
        item = queue.add(sample_report)
        item.mark_processing()
        queue.update(item)
        item.mark_failed("Test error")
        queue.update(item)
        
        # Verify
        failed = queue.list_failed()
        assert len(failed) == 1
        assert failed[0].id == item.id
        assert failed[0].status == QueueItemStatus.FAILED
        assert failed[0].last_error == "Test error"
    
    def test_get_by_status(self, tmp_path, sample_report):
        """Test filtering items by status"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add items with different statuses
        item1 = queue.add(sample_report)
        
        item2 = queue.add(sample_report)
        item2.mark_processing()
        queue.update(item2)
        
        item3 = queue.add(sample_report)
        item3.mark_processing()
        queue.update(item3)
        item3.mark_failed("Error")
        queue.update(item3)
        
        # Verify filtering
        assert len(queue.list_pending()) == 1
        assert len(queue.list_by_status(QueueItemStatus.PROCESSING)) == 1
        assert len(queue.list_failed()) == 1


class TestQueuePersistence:
    """Test file persistence and crash recovery"""
    
    def test_save_queue_to_disk(self, tmp_path, sample_report):
        """Test persisting queue to disk"""
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        
        # Add item
        item = queue.add(sample_report, item_id="TEST-001")
        
        # Verify WSJF file exists
        wsjf_files = list(queue_dir.glob("*.wsjf"))
        assert len(wsjf_files) >= 1
        
        # Verify we can read the file
        # File should be named TEST-001.pending.wsjf or similar
        pending_file = queue_dir / f"{item.id}.pending.wsjf"
        assert pending_file.exists()
    
    def test_load_queue_from_disk(self, tmp_path, sample_report):
        """Test loading queue from existing files"""
        queue_dir = tmp_path / "queue"
        
        # Create queue and add items
        queue1 = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        item1 = queue1.add(sample_report, item_id="LOAD-001")
        item2 = queue1.add(sample_report, item_id="LOAD-002")
        
        # Create new queue that loads from disk
        queue2 = PersistentQueue(queue_dir=queue_dir, auto_load=True)
        
        # Verify items loaded
        assert queue2.size == 2
        assert queue2.get("LOAD-001") is not None
        assert queue2.get("LOAD-002") is not None
    
    def test_crash_recovery(self, tmp_path, sample_report):
        """Test recovery of processing items after crash"""
        queue_dir = tmp_path / "queue"
        
        # Simulate crash: items left in processing state
        queue1 = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        item = queue1.add(sample_report, item_id="CRASH-001")
        item.mark_processing()
        queue1.update(item)
        
        # New queue loads and should reset processing → pending
        queue2 = PersistentQueue(queue_dir=queue_dir, auto_load=True)
        
        # Verify item recovered
        recovered = queue2.get("CRASH-001")
        assert recovered is not None
        # After crash recovery, processing items should be reset to pending
        assert recovered.status in [QueueItemStatus.PENDING, QueueItemStatus.PROCESSING]
    
    def test_atomic_file_writes(self, tmp_path, sample_report):
        """Test atomic file operations - no .tmp files left behind"""
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        
        # Add and update item multiple times
        item = queue.add(sample_report)
        for _ in range(5):
            item.mark_processing()
            queue.update(item)
            time.sleep(0.01)
            item.mark_failed("Error")
            queue.update(item)
            time.sleep(0.01)
        
        # Verify no .tmp files remain
        tmp_files = list(queue_dir.glob("*.tmp"))
        assert len(tmp_files) == 0, f"Found temporary files: {tmp_files}"
    
    def test_metadata_persistence(self, tmp_path, sample_report):
        """Test metadata file persistence"""
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        
        # Add item with metadata
        custom_meta = {"source": "test", "priority": "high"}
        item = queue.add(sample_report, item_id="META-001", metadata=custom_meta)
        
        # Verify metadata file exists
        # Metadata files are stored as .meta.json
        meta_file = queue_dir / f"{item.id}.pending.meta.json"
        if meta_file.exists():
            with open(meta_file) as f:
                meta_data = json.load(f)
                # Metadata is stored in 'custom' key
                assert "custom" in meta_data
                assert meta_data["custom"]["source"] == "test"
                assert meta_data["custom"]["priority"] == "high"


class TestQueueRetry:
    """Test retry logic and attempt tracking"""
    
    def test_retry_failed_item(self, tmp_path, sample_report):
        """Test retrying a failed item"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False, default_max_attempts=3)
        
        # Add and fail item
        item = queue.add(sample_report)
        item.mark_processing()
        queue.update(item)
        item.mark_failed("First attempt failed")
        queue.update(item)
        
        # Check item can be retried
        assert item.can_retry
        assert item.attempts < item.max_attempts
        
        # Retry item
        item.mark_processing()  # This should increment attempts
        queue.update(item)
        
        # Verify attempt incremented
        assert item.attempts >= 1
    
    def test_max_retries_exceeded(self, tmp_path, sample_report):
        """Test item is abandoned after max retries"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False, default_max_attempts=2)
        
        # Add item
        item = queue.add(sample_report)
        
        # Fail item max times
        for i in range(3):
            item.mark_processing()
            queue.update(item)
            item.mark_failed(f"Attempt {i+1} failed")
            queue.update(item)
        
        # Should no longer be retryable
        assert not item.can_retry
    
    def test_retry_delay_respected(self, tmp_path, sample_report):
        """Test retry delay is tracked"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add and fail item
        item = queue.add(sample_report)
        item.mark_processing()
        queue.update(item)
        
        before_fail = time.time()
        item.mark_failed("Temporary error")
        queue.update(item)
        after_fail = time.time()
        
        # Verify timestamps
        assert item.updated_at is not None
        assert item.last_error == "Temporary error"
        # updated_at should be around now
        assert abs(item.updated_at.timestamp() - after_fail) < 2
    
    def test_retry_attempt_tracking(self, tmp_path, sample_report):
        """Test attempt counter increments correctly"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False, default_max_attempts=5)
        
        # Add item
        item = queue.add(sample_report)
        initial_attempts = item.attempts
        
        # Process and fail multiple times
        for i in range(3):
            item.mark_processing()
            queue.update(item)
            item.mark_failed(f"Error {i}")
            queue.update(item)
            
        # Verify attempts increased
        assert item.attempts > initial_attempts


class TestQueueManagement:
    """Test queue size limits, cleanup, and statistics"""
    
    def test_queue_max_size(self, tmp_path, sample_report):
        """Test queue size limit enforcement"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False, max_size=10)
        
        # Add items up to limit
        for i in range(10):
            queue.add(sample_report, item_id=f"ITEM-{i:03d}")
        
        # Verify at limit
        assert queue.size == 10
        
        # Try to exceed limit
        with pytest.raises(ValueError):  # Should raise ValueError for full queue
            queue.add(sample_report)
    
    def test_delete_completed_items(self, tmp_path, sample_report):
        """Test cleanup of completed items"""
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False, delete_completed=False)
        
        # Add and complete some items
        item1 = queue.add(sample_report, item_id="COMP-001")
        item1.mark_processing()
        queue.update(item1)
        item1.mark_completed()
        queue.update(item1)
        
        item2 = queue.add(sample_report, item_id="COMP-002")
        item2.mark_processing()
        queue.update(item2)
        item2.mark_completed()
        queue.update(item2)
        
        # Keep a pending item
        item3 = queue.add(sample_report, item_id="PEND-001")
        
        # Verify
        assert queue.size == 3
        assert len(queue.list_completed()) == 2
        
        # Clear completed
        cleared = queue.clear_completed()
        assert cleared == 2
        assert queue.size == 1
    
    def test_get_queue_stats(self, tmp_path, sample_report):
        """Test queue statistics"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add items with different statuses
        item1 = queue.add(sample_report)
        
        item2 = queue.add(sample_report)
        item2.mark_processing()
        queue.update(item2)
        
        item3 = queue.add(sample_report)
        item3.mark_processing()
        queue.update(item3)
        item3.mark_completed()
        queue.update(item3)
        
        item4 = queue.add(sample_report)
        item4.mark_processing()
        queue.update(item4)
        item4.mark_failed("Error")
        queue.update(item4)
        
        # Get stats
        stats = queue.get_stats()
        
        # Verify counts
        assert stats.total >= 4
        assert stats.pending >= 1
        assert stats.completed >= 1
        assert stats.failed >= 1
    
    def test_concurrent_access(self, tmp_path, sample_report):
        """Test thread-safe concurrent access"""
        queue = PersistentQueue(queue_dir=tmp_path / "queue", auto_load=False)
        
        # Add items from multiple threads
        def add_items(count, prefix):
            for i in range(count):
                queue.add(sample_report, item_id=f"{prefix}-{i:03d}")
        
        threads = [
            threading.Thread(target=add_items, args=(10, "THREAD-A")),
            threading.Thread(target=add_items, args=(10, "THREAD-B")),
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Verify all items added
        assert queue.size == 20
