"""
Tests for End-to-End Integration

Tests complete workflows including offline queuing, recovery, and error handling.
"""

import pytest
import time
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
from pywats_client.queue import PersistentQueue
from pywats_client.core.config import ClientConfig, ConverterConfig
from pywats.queue import QueueItemStatus


class TestEndToEndWorkflow:
    """Test complete conversion and upload workflows"""
    
    def test_offline_queue_workflow(self, tmp_path, sample_report):
        """Test complete offline queuing workflow"""
        queue_dir = tmp_path / "queue"
        
        # Step 1: Add report to queue (offline)
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        item = queue.add(sample_report, item_id="OFFLINE-001")
        
        assert item.status == QueueItemStatus.PENDING
        assert queue.size == 1
        
        # Step 2: Simulate processing
        item.mark_processing()
        queue.update(item)
        
        # Step 3: Simulate successful upload
        item.mark_completed()
        queue.update(item)
        
        # Verify workflow
        assert item.status == QueueItemStatus.COMPLETED
        assert queue.size == 1
    
    def test_restart_recovery_workflow(self, tmp_path, sample_report):
        """Test recovery after service restart"""
        queue_dir = tmp_path / "queue"
        
        # Step 1: Create queue and add items
        queue1 = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        item1 = queue1.add(sample_report, item_id="RESTART-001")
        item2 = queue1.add(sample_report, item_id="RESTART-002")
        
        # Step 2: Mark one as processing (simulate crash during upload)
        item1.mark_processing()
        queue1.update(item1)
        
        # Step 3: Simulate restart - new queue instance loads from disk
        queue2 = PersistentQueue(queue_dir=queue_dir, auto_load=True)
        
        # Verify both items recovered
        assert queue2.size == 2
        recovered1 = queue2.get("RESTART-001")
        recovered2 = queue2.get("RESTART-002")
        
        assert recovered1 is not None
        assert recovered2 is not None
    
    def test_error_handling_workflow(self, tmp_path, sample_report):
        """Test error handling and retry"""
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False, default_max_attempts=3)
        
        # Step 1: Add item
        item = queue.add(sample_report)
        
        # Step 2: Simulate failed upload attempts
        for attempt in range(2):
            item.mark_processing()
            queue.update(item)
            item.mark_failed(f"Network error on attempt {attempt + 1}")
            queue.update(item)
        
        # Verify retry is still possible
        assert item.can_retry
        assert item.attempts == 2
        assert item.status == QueueItemStatus.FAILED
        
        # Step 3: Successful retry
        item.mark_processing()
        queue.update(item)
        item.mark_completed()
        queue.update(item)
        
        assert item.status == QueueItemStatus.COMPLETED
    
    def test_config_validation_workflow(self, tmp_path):
        """Test configuration validation"""
        config_file = tmp_path / "config.json"
        
        # Create valid config
        config_data = {
            "instance_id": "test-workflow",
            "instance_name": "Test Workflow",
            "service_address": "https://test.wats.com",
            "api_token": "dGVzdDp0ZXN0",
            "converters": [],
            "offline_queue_enabled": True
        }
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        # Verify file exists and is valid JSON
        assert config_file.exists()
        
        with open(config_file) as f:
            loaded = json.load(f)
            assert loaded['instance_id'] == "test-workflow"
            assert loaded['offline_queue_enabled'] == True
    
    def test_converter_config_workflow(self, tmp_path):
        """Test converter configuration"""
        # Create converter config
        conv_config = ConverterConfig(
            name="Test Converter",
            module_path="converters/test_converter.py",
            watch_folder=str(tmp_path / "watch"),
            done_folder=str(tmp_path / "done"),
            error_folder=str(tmp_path / "error"),
            pending_folder=str(tmp_path / "pending"),
            converter_type="file",
            enabled=True,
            file_patterns=["*.csv", "*.txt"],
            max_retries=3,
            retry_delay_seconds=60
        )
        
        # Validate config
        assert conv_config.name == "Test Converter"
        assert conv_config.enabled == True
        assert len(conv_config.file_patterns) == 2
        assert conv_config.max_retries == 3
    
    def test_multi_report_queue_workflow(self, tmp_path, sample_report):
        """Test handling multiple reports"""
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        
        # Add multiple reports
        num_reports = 5
        items = []
        for i in range(num_reports):
            item = queue.add(sample_report, item_id=f"MULTI-{i:03d}")
            items.append(item)
        
        assert queue.size == num_reports
        
        # Process all
        for item in items:
            item.mark_processing()
            queue.update(item)
            item.mark_completed()
            queue.update(item)
        
        # Verify all completed
        completed = queue.list_completed()
        assert len(completed) == num_reports
    
    def test_queue_cleanup_workflow(self, tmp_path, sample_report):
        """Test automatic cleanup of completed items"""
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(
            queue_dir=queue_dir,
            auto_load=False,
            delete_completed=False  # Manual cleanup
        )
        
        # Add and complete items
        for i in range(3):
            item = queue.add(sample_report, item_id=f"CLEAN-{i:03d}")
            item.mark_processing()
            queue.update(item)
            item.mark_completed()
            queue.update(item)
        
        # Add pending item
        pending_item = queue.add(sample_report, item_id="CLEAN-PENDING")
        
        assert queue.size == 4
        
        # Clean up completed
        cleared = queue.clear_completed()
        assert cleared == 3
        assert queue.size == 1
        
        # Only pending should remain
        remaining = queue.list_pending()
        assert len(remaining) == 1
        assert remaining[0].id == "CLEAN-PENDING"
    
    def test_instance_isolation_workflow(self, tmp_path, sample_report):
        """Test multiple instances don't interfere"""
        # Create separate queues for different instances
        queue1_dir = tmp_path / "instance1" / "queue"
        queue2_dir = tmp_path / "instance2" / "queue"
        
        queue1 = PersistentQueue(queue_dir=queue1_dir, auto_load=False)
        queue2 = PersistentQueue(queue_dir=queue2_dir, auto_load=False)
        
        # Add to instance 1
        queue1.add(sample_report, item_id="INST1-001")
        queue1.add(sample_report, item_id="INST1-002")
        
        # Add to instance 2
        queue2.add(sample_report, item_id="INST2-001")
        
        # Verify isolation
        assert queue1.size == 2
        assert queue2.size == 1
        
        # Verify items are separate
        assert queue1.get("INST1-001") is not None
        assert queue1.get("INST2-001") is None
        assert queue2.get("INST2-001") is not None
        assert queue2.get("INST1-001") is None
    
    def test_concurrent_processing_workflow(self, tmp_path, sample_report):
        """Test concurrent report processing"""
        import threading
        
        queue_dir = tmp_path / "queue"
        queue = PersistentQueue(queue_dir=queue_dir, auto_load=False)
        
        # Add reports
        num_reports = 10
        for i in range(num_reports):
            queue.add(sample_report, item_id=f"CONCURRENT-{i:03d}")
        
        assert queue.size == num_reports
        
        # Process concurrently
        def process_item(item_id):
            item = queue.get(item_id)
            if item:
                item.mark_processing()
                queue.update(item)
                time.sleep(0.01)  # Simulate processing
                item.mark_completed()
                queue.update(item)
        
        threads = []
        for i in range(num_reports):
            t = threading.Thread(target=process_item, args=(f"CONCURRENT-{i:03d}",))
            threads.append(t)
            t.start()
        
        # Wait for all
        for t in threads:
            t.join()
        
        # Verify all completed
        completed = queue.list_completed()
        assert len(completed) == num_reports
