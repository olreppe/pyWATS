"""Tests for shared statistics models.

Tests the dataclass-based statistics types used by queues, caches, and batch operations.
"""
import pytest
from pywats.shared.stats import (
    QueueProcessingResult,
    QueueStats,
    CacheStats,
    BatchResult,
)


class TestQueueProcessingResult:
    """Tests for QueueProcessingResult dataclass."""
    
    def test_default_values(self):
        """Test default values are zeros and empty list."""
        result = QueueProcessingResult()
        
        assert result.success == 0
        assert result.failed == 0
        assert result.skipped == 0
        assert result.errors == []
    
    def test_with_values(self):
        """Test creating with specific values."""
        result = QueueProcessingResult(
            success=10,
            failed=2,
            skipped=1,
            errors=["Error 1", "Error 2"]
        )
        
        assert result.success == 10
        assert result.failed == 2
        assert result.skipped == 1
        assert len(result.errors) == 2
    
    def test_total_property(self):
        """Test total property sums all counts."""
        result = QueueProcessingResult(success=5, failed=3, skipped=2)
        
        assert result.total == 10
    
    def test_success_rate_property(self):
        """Test success rate calculation."""
        result = QueueProcessingResult(success=8, failed=2, skipped=0)
        
        assert result.success_rate == 80.0
    
    def test_success_rate_with_zero_total(self):
        """Test success rate is 0 when total is 0."""
        result = QueueProcessingResult()
        
        assert result.success_rate == 0.0
    
    def test_to_dict(self):
        """Test dictionary serialization."""
        result = QueueProcessingResult(success=5, failed=1, skipped=0, errors=["Error"])
        
        d = result.to_dict()
        
        assert d["success"] == 5
        assert d["failed"] == 1
        assert d["skipped"] == 0
        assert d["errors"] == ["Error"]
        assert d["total"] == 6


class TestQueueStats:
    """Tests for QueueStats dataclass."""
    
    def test_default_values(self):
        """Test default values are zeros."""
        stats = QueueStats()
        
        assert stats.pending == 0
        assert stats.processing == 0
        assert stats.completed == 0
        assert stats.failed == 0
    
    def test_with_values(self):
        """Test creating with specific values."""
        stats = QueueStats(pending=10, processing=2, completed=5, failed=1)
        
        assert stats.pending == 10
        assert stats.processing == 2
        assert stats.completed == 5
        assert stats.failed == 1
    
    def test_total_property(self):
        """Test total property sums all counts."""
        stats = QueueStats(pending=10, processing=2, completed=5, failed=1)
        
        assert stats.total == 18
    
    def test_active_property(self):
        """Test active property sums pending and processing."""
        stats = QueueStats(pending=10, processing=2, completed=5, failed=1)
        
        assert stats.active == 12
    
    def test_to_dict(self):
        """Test dictionary serialization."""
        stats = QueueStats(pending=5, processing=1, completed=10, failed=2)
        
        d = stats.to_dict()
        
        assert d["pending"] == 5
        assert d["processing"] == 1
        assert d["completed"] == 10
        assert d["failed"] == 2
        assert d["total"] == 18


class TestCacheStats:
    """Tests for CacheStats dataclass."""
    
    def test_default_values(self):
        """Test default values."""
        stats = CacheStats()
        
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.size == 0
        assert stats.max_size is None
    
    def test_with_values(self):
        """Test creating with specific values."""
        stats = CacheStats(hits=100, misses=20, size=50, max_size=100)
        
        assert stats.hits == 100
        assert stats.misses == 20
        assert stats.size == 50
        assert stats.max_size == 100
    
    def test_total_requests_property(self):
        """Test total_requests property."""
        stats = CacheStats(hits=100, misses=20)
        
        assert stats.total_requests == 120
    
    def test_hit_rate_property(self):
        """Test hit rate calculation."""
        stats = CacheStats(hits=80, misses=20)
        
        assert stats.hit_rate == 80.0
    
    def test_hit_rate_with_zero_requests(self):
        """Test hit rate is 0 when no requests."""
        stats = CacheStats()
        
        assert stats.hit_rate == 0.0
    
    def test_utilization_property(self):
        """Test utilization calculation."""
        stats = CacheStats(size=50, max_size=100)
        
        assert stats.utilization == 50.0
    
    def test_utilization_unbounded(self):
        """Test utilization is None for unbounded cache."""
        stats = CacheStats(size=50, max_size=None)
        
        assert stats.utilization is None
    
    def test_utilization_zero_max_size(self):
        """Test utilization is None when max_size is 0."""
        stats = CacheStats(size=0, max_size=0)
        
        assert stats.utilization is None
    
    def test_to_dict(self):
        """Test dictionary serialization."""
        stats = CacheStats(hits=80, misses=20, size=50, max_size=100)
        
        d = stats.to_dict()
        
        assert d["hits"] == 80
        assert d["misses"] == 20
        assert d["size"] == 50
        assert d["max_size"] == 100
        assert d["hit_rate"] == 80.0


class TestBatchResult:
    """Tests for BatchResult dataclass."""
    
    def test_default_values(self):
        """Test default values."""
        result = BatchResult()
        
        assert result.total == 0
        assert result.success == 0
        assert result.failed == 0
        assert result.results == []
        assert result.errors == {}
    
    def test_with_values(self):
        """Test creating with specific values."""
        result = BatchResult(
            total=10,
            success=8,
            failed=2,
            results=["r1", "r2"],
            errors={3: "Error at index 3", 7: "Error at index 7"}
        )
        
        assert result.total == 10
        assert result.success == 8
        assert result.failed == 2
        assert len(result.results) == 2
        assert len(result.errors) == 2
    
    def test_success_rate_property(self):
        """Test success rate calculation."""
        result = BatchResult(total=10, success=8, failed=2)
        
        assert result.success_rate == 80.0
    
    def test_success_rate_with_zero_total(self):
        """Test success rate is 0 when total is 0."""
        result = BatchResult()
        
        assert result.success_rate == 0.0
    
    def test_all_succeeded_property_true(self):
        """Test all_succeeded when all items pass."""
        result = BatchResult(total=10, success=10, failed=0)
        
        assert result.all_succeeded is True
    
    def test_all_succeeded_property_false(self):
        """Test all_succeeded when some items fail."""
        result = BatchResult(total=10, success=8, failed=2)
        
        assert result.all_succeeded is False
    
    def test_all_succeeded_empty_batch(self):
        """Test all_succeeded for empty batch."""
        result = BatchResult()
        
        assert result.all_succeeded is False


class TestStatsUsagePatterns:
    """Tests for common statistics usage patterns."""
    
    def test_queue_processing_summary(self):
        """Test creating a processing summary."""
        result = QueueProcessingResult(
            success=95,
            failed=3,
            skipped=2,
            errors=["Connection timeout", "Validation failed", "Server error"]
        )
        
        # Common summary pattern
        summary = f"Processed {result.total} reports: {result.success} success, {result.failed} failed ({result.success_rate:.1f}% success rate)"
        
        assert "100 reports" in summary
        assert "95 success" in summary
        assert "3 failed" in summary
        assert "95.0%" in summary
    
    def test_queue_status_check(self):
        """Test checking queue status."""
        stats = QueueStats(pending=10, processing=2, completed=50, failed=1)
        
        # Common status check pattern
        if stats.active > 0:
            status = f"Queue active: {stats.pending} pending, {stats.processing} processing"
        else:
            status = "Queue idle"
        
        assert "Queue active" in status
        assert "10 pending" in status
    
    def test_cache_efficiency_report(self):
        """Test creating a cache efficiency report."""
        stats = CacheStats(hits=9000, misses=1000, size=500, max_size=1000)
        
        # Common efficiency report pattern
        report = f"Cache: {stats.hit_rate:.1f}% hit rate, {stats.utilization:.1f}% full"
        
        assert "90.0% hit rate" in report
        assert "50.0% full" in report
    
    def test_batch_result_error_handling(self):
        """Test handling batch errors."""
        result = BatchResult(
            total=5,
            success=3,
            failed=2,
            results=["OK", "OK", None, "OK", None],
            errors={2: "Validation error", 4: "Server timeout"}
        )
        
        # Common error handling pattern
        if not result.all_succeeded:
            error_report = []
            for idx, msg in result.errors.items():
                error_report.append(f"  Item {idx}: {msg}")
            
            assert len(error_report) == 2
            assert "Item 2: Validation error" in error_report[0]
