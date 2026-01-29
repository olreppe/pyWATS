"""
Tests for request coalescing utilities.
"""
import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from pywats.core.coalesce import (
    CoalesceConfig,
    CoalesceItem,
    RequestCoalescer,
    ChunkedProcessor,
    batch_map,
)


class TestCoalesceConfig:
    """Tests for CoalesceConfig dataclass."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = CoalesceConfig()
        assert config.max_batch_size == 100
        assert config.max_wait_time == 0.1
        assert config.max_concurrent_batches == 5
    
    def test_custom_values(self):
        """Test custom configuration values."""
        config = CoalesceConfig(
            max_batch_size=50,
            max_wait_time=0.5,
            max_concurrent_batches=3
        )
        assert config.max_batch_size == 50
        assert config.max_wait_time == 0.5
        assert config.max_concurrent_batches == 3


class TestCoalesceItem:
    """Tests for CoalesceItem dataclass."""
    
    @pytest.mark.asyncio
    async def test_creation_with_item(self):
        """Test creating a coalesce item with data."""
        item = CoalesceItem[str, int](item="test")
        assert item.item == "test"
        assert isinstance(item.future, asyncio.Future)
        assert isinstance(item.timestamp, datetime)
    
    @pytest.mark.asyncio
    async def test_future_can_be_set(self):
        """Test that future can receive a result."""
        item = CoalesceItem[str, int](item="test")
        item.future.set_result(42)
        assert item.future.done()
        assert item.future.result() == 42
    
    @pytest.mark.asyncio
    async def test_timestamp_is_set_automatically(self):
        """Test that timestamp is set at creation time."""
        before = datetime.now()
        item = CoalesceItem[str, int](item="test")
        after = datetime.now()
        assert before <= item.timestamp <= after


class TestRequestCoalescer:
    """Tests for RequestCoalescer class."""
    
    @pytest.fixture
    def mock_bulk_func(self):
        """Create a mock bulk function."""
        async def bulk_func(items: list[str]) -> list[int]:
            return [len(item) for item in items]
        return AsyncMock(side_effect=bulk_func)
    
    @pytest.fixture
    def coalescer(self, mock_bulk_func):
        """Create a coalescer for testing."""
        return RequestCoalescer(
            bulk_func=mock_bulk_func,
            config=CoalesceConfig(max_batch_size=5, max_wait_time=0.01)
        )
    
    @pytest.mark.asyncio
    async def test_start_stop(self, coalescer):
        """Test starting and stopping the coalescer."""
        await coalescer.start()
        assert coalescer._running is True
        assert coalescer._task is not None
        
        await coalescer.stop()
        assert coalescer._running is False
    
    @pytest.mark.asyncio
    async def test_start_already_running(self, coalescer):
        """Test starting when already running logs warning."""
        await coalescer.start()
        await coalescer.start()  # Should just log warning
        await coalescer.stop()
    
    @pytest.mark.asyncio
    async def test_stop_when_not_running(self, coalescer):
        """Test stopping when not running is safe."""
        await coalescer.stop()  # Should not raise
    
    @pytest.mark.asyncio
    async def test_add_when_not_running(self, coalescer):
        """Test adding item when not started raises error."""
        with pytest.raises(RuntimeError, match="Coalescer not started"):
            await coalescer.add("test")
    
    @pytest.mark.asyncio
    async def test_add_single_item(self, coalescer, mock_bulk_func):
        """Test adding a single item."""
        await coalescer.start()
        try:
            result = await coalescer.add("hello")
            # Result should be length of "hello" = 5
            assert result == 5
        finally:
            await coalescer.stop()
    
    @pytest.mark.asyncio
    async def test_add_multiple_items(self, coalescer, mock_bulk_func):
        """Test adding multiple items coalesces them."""
        await coalescer.start()
        try:
            # Add items concurrently
            results = await asyncio.gather(
                coalescer.add("a"),
                coalescer.add("bb"),
                coalescer.add("ccc"),
            )
            assert results == [1, 2, 3]
        finally:
            await coalescer.stop()
    
    @pytest.mark.asyncio
    async def test_batch_size_triggers_processing(self, mock_bulk_func):
        """Test that max batch size triggers immediate processing."""
        coalescer = RequestCoalescer(
            bulk_func=mock_bulk_func,
            config=CoalesceConfig(max_batch_size=3, max_wait_time=10)  # Long wait
        )
        await coalescer.start()
        try:
            # Add items up to batch size
            results = await asyncio.gather(
                coalescer.add("a"),
                coalescer.add("b"),
                coalescer.add("c"),
            )
            assert results == [1, 1, 1]
        finally:
            await coalescer.stop()
    
    @pytest.mark.asyncio
    async def test_stats(self, coalescer, mock_bulk_func):
        """Test statistics tracking."""
        await coalescer.start()
        try:
            await coalescer.add("hello")
            await coalescer.add("world")
            
            stats = coalescer.stats
            assert stats['total_items'] >= 2
        finally:
            await coalescer.stop()
    
    @pytest.mark.asyncio
    async def test_context_manager(self, mock_bulk_func):
        """Test async context manager usage."""
        coalescer = RequestCoalescer(
            bulk_func=mock_bulk_func,
            config=CoalesceConfig(max_batch_size=5, max_wait_time=0.01)
        )
        
        async with coalescer:
            result = await coalescer.add("test")
            assert result == 4
    
    @pytest.mark.asyncio
    async def test_flush_empty(self, coalescer):
        """Test flushing when no pending items."""
        await coalescer.start()
        await coalescer._flush()  # Should not raise
        await coalescer.stop()
    
    @pytest.mark.asyncio
    async def test_process_batch_with_error(self, mock_bulk_func):
        """Test error handling in batch processing."""
        async def failing_func(items):
            raise ValueError("Bulk operation failed")
        
        coalescer = RequestCoalescer(
            bulk_func=AsyncMock(side_effect=failing_func),
            config=CoalesceConfig(max_batch_size=5, max_wait_time=0.01)
        )
        
        await coalescer.start()
        try:
            with pytest.raises(ValueError, match="Bulk operation failed"):
                await coalescer.add("test")
        finally:
            await coalescer.stop()
    
    @pytest.mark.asyncio
    async def test_process_batch_wrong_result_count(self, mock_bulk_func):
        """Test error when bulk function returns wrong count."""
        async def wrong_count_func(items):
            return [1]  # Always returns 1 item
        
        coalescer = RequestCoalescer(
            bulk_func=AsyncMock(side_effect=wrong_count_func),
            config=CoalesceConfig(max_batch_size=5, max_wait_time=0.01)
        )
        
        await coalescer.start()
        try:
            with pytest.raises(ValueError, match="returned .* results"):
                await asyncio.gather(
                    coalescer.add("a"),
                    coalescer.add("b"),
                )
        finally:
            await coalescer.stop()


class TestChunkedProcessor:
    """Tests for ChunkedProcessor class."""
    
    @pytest.fixture
    def mock_process_func(self):
        """Create a mock process function."""
        async def process(items: list[int]) -> list[int]:
            return [item * 2 for item in items]
        return AsyncMock(side_effect=process)
    
    def test_initialization(self, mock_process_func):
        """Test initializing chunked processor."""
        processor = ChunkedProcessor(
            process_func=mock_process_func,
            chunk_size=50,
            max_concurrent=3
        )
        assert processor._chunk_size == 50
    
    def test_default_values(self, mock_process_func):
        """Test default initialization values."""
        processor = ChunkedProcessor(process_func=mock_process_func)
        assert processor._chunk_size == 100
    
    @pytest.mark.asyncio
    async def test_process_all_small_list(self, mock_process_func):
        """Test processing a list smaller than chunk size."""
        processor = ChunkedProcessor(
            process_func=mock_process_func,
            chunk_size=10
        )
        
        items = [1, 2, 3]
        results = await processor.process_all(items)
        assert results == [2, 4, 6]
    
    @pytest.mark.asyncio
    async def test_process_all_large_list(self, mock_process_func):
        """Test processing a list larger than chunk size."""
        processor = ChunkedProcessor(
            process_func=mock_process_func,
            chunk_size=3
        )
        
        items = [1, 2, 3, 4, 5, 6, 7]
        results = await processor.process_all(items)
        assert results == [2, 4, 6, 8, 10, 12, 14]
        
        # Should have called process_func 3 times
        assert mock_process_func.call_count == 3
    
    @pytest.mark.asyncio
    async def test_process_all_empty_list(self, mock_process_func):
        """Test processing an empty list."""
        processor = ChunkedProcessor(
            process_func=mock_process_func,
            chunk_size=10
        )
        
        results = await processor.process_all([])
        assert results == []
        mock_process_func.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_process_all_exact_chunks(self, mock_process_func):
        """Test processing a list that divides evenly into chunks."""
        processor = ChunkedProcessor(
            process_func=mock_process_func,
            chunk_size=2
        )
        
        items = [1, 2, 3, 4, 5, 6]
        results = await processor.process_all(items)
        assert results == [2, 4, 6, 8, 10, 12]
        assert mock_process_func.call_count == 3
    
    @pytest.mark.asyncio
    async def test_process_chunk_directly(self, mock_process_func):
        """Test processing a single chunk."""
        processor = ChunkedProcessor(
            process_func=mock_process_func,
            chunk_size=10
        )
        
        # Access internal method
        result = await processor._process_chunk([1, 2, 3])
        assert result == [2, 4, 6]
    
    @pytest.mark.asyncio
    async def test_concurrent_processing(self, mock_process_func):
        """Test that chunks are processed concurrently."""
        call_times = []
        
        async def slow_process(items):
            call_times.append(asyncio.get_event_loop().time())
            await asyncio.sleep(0.01)  # Small delay
            return [item * 2 for item in items]
        
        processor = ChunkedProcessor(
            process_func=AsyncMock(side_effect=slow_process),
            chunk_size=2,
            max_concurrent=5  # Allow concurrent execution
        )
        
        items = list(range(10))  # 5 chunks
        results = await processor.process_all(items)
        assert results == [item * 2 for item in items]


class TestBatchMap:
    """Tests for batch_map utility function."""
    
    @pytest.mark.asyncio
    async def test_batch_map_basic(self):
        """Test basic batch_map functionality."""
        async def double(x):
            return x * 2
        
        items = [1, 2, 3, 4, 5]
        results = await batch_map(items, double, batch_size=2)
        assert results == [2, 4, 6, 8, 10]
    
    @pytest.mark.asyncio
    async def test_batch_map_empty_list(self):
        """Test batch_map with empty list."""
        async def double(x):
            return x * 2
        
        results = await batch_map([], double)
        assert results == []
    
    @pytest.mark.asyncio
    async def test_batch_map_preserves_order(self):
        """Test batch_map preserves input order."""
        async def identity(x):
            await asyncio.sleep(0.01 * (5 - x))  # Longer delay for smaller numbers
            return x
        
        items = [1, 2, 3, 4, 5]
        results = await batch_map(items, identity, batch_size=2, max_concurrent=5)
        assert results == items
    
    @pytest.mark.asyncio
    async def test_batch_map_concurrency_control(self):
        """Test batch_map respects concurrency limit."""
        active_count = 0
        max_active = 0
        
        async def tracked_func(x):
            nonlocal active_count, max_active
            active_count += 1
            max_active = max(max_active, active_count)
            await asyncio.sleep(0.01)
            active_count -= 1
            return x
        
        items = list(range(20))
        await batch_map(items, tracked_func, batch_size=10, max_concurrent=3)
        
        # Max concurrent should be limited
        assert max_active <= 3
    
    @pytest.mark.asyncio
    async def test_batch_map_with_async_mock(self):
        """Test batch_map with AsyncMock."""
        func = AsyncMock(side_effect=lambda x: x * 2)
        
        items = [1, 2, 3]
        results = await batch_map(items, func, batch_size=2)
        
        assert results == [2, 4, 6]
        assert func.call_count == 3
