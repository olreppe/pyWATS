"""
Tests for AsyncConverterPool

Tests concurrent file conversion with asyncio.
"""

import asyncio
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import tempfile
import shutil

from pywats_client.service.async_converter_pool import (
    AsyncConverterPool,
    AsyncConversionItem,
    AsyncConversionItemState,
)


@pytest.fixture
def temp_watch_dir():
    """Create a temporary watch directory"""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_api():
    """Create a mock AsyncWATS client"""
    api = AsyncMock()
    api.report.submit = AsyncMock()
    return api


@pytest.fixture
def mock_config(temp_watch_dir):
    """Create a mock ClientConfig"""
    config = MagicMock()
    config.get_converters.return_value = []
    return config


@pytest.fixture
def mock_converter(temp_watch_dir):
    """Create a mock Converter"""
    converter = MagicMock()
    converter.name = "TestConverter"
    converter.watch_path = temp_watch_dir
    converter.watch_recursive = False
    converter.matches_file = MagicMock(return_value=True)
    converter.convert = MagicMock(return_value={"report": "data"})
    converter.post_process_action = MagicMock()
    converter.archive_path = None
    converter.error_path = None
    converter.process_archive_queue = MagicMock()
    return converter


@pytest.fixture
def pool(mock_config, mock_api):
    """Create a test pool instance"""
    return AsyncConverterPool(
        config=mock_config,
        api=mock_api,
        max_concurrent=5
    )


class TestAsyncConversionItemState:
    """Test conversion item state enum"""
    
    def test_state_values(self):
        assert AsyncConversionItemState.PENDING.value == "Pending"
        assert AsyncConversionItemState.PROCESSING.value == "Processing"
        assert AsyncConversionItemState.COMPLETED.value == "Completed"
        assert AsyncConversionItemState.ERROR.value == "Error"


class TestAsyncConversionItem:
    """Test AsyncConversionItem"""
    
    def test_init_with_existing_file(self, temp_watch_dir, mock_converter):
        """Test creating item with existing file"""
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item = AsyncConversionItem(test_file, mock_converter)
        
        assert item.file_path == test_file
        assert item.converter == mock_converter
        assert item.state == AsyncConversionItemState.PENDING
        assert item.queued_at is not None
        assert item.file_date is not None
    
    def test_processing_time(self, temp_watch_dir, mock_converter):
        """Test processing time calculation"""
        from datetime import datetime, timedelta
        
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item = AsyncConversionItem(test_file, mock_converter)
        
        # No processing time before completion
        assert item.processing_time is None
        
        # Set processing times
        item.process_start = datetime.now()
        item.process_end = item.process_start + timedelta(seconds=5)
        
        assert item.processing_time == pytest.approx(5.0, rel=0.1)


class TestAsyncConverterPoolInit:
    """Test pool initialization"""
    
    def test_init_defaults(self, mock_config, mock_api):
        """Test default initialization"""
        pool = AsyncConverterPool(mock_config, mock_api)
        
        assert pool._max_concurrent == 10
        assert not pool.is_running
    
    def test_init_custom_concurrent(self, mock_config, mock_api):
        """Test custom max_concurrent"""
        pool = AsyncConverterPool(mock_config, mock_api, max_concurrent=3)
        
        assert pool._max_concurrent == 3


class TestAsyncConverterPoolStats:
    """Test pool statistics"""
    
    def test_initial_stats(self, pool):
        """Test initial statistics"""
        stats = pool.stats
        
        assert stats["total_processed"] == 0
        assert stats["successful"] == 0
        assert stats["errors"] == 0
        assert stats["queue_size"] == 0


class TestAsyncConverterPoolProcessing:
    """Test file processing"""
    
    @pytest.mark.asyncio
    async def test_process_item_success(self, pool, temp_watch_dir, mock_api, mock_converter):
        """Test successful file processing"""
        # Create test file
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test>data</test>")
        
        item = AsyncConversionItem(test_file, mock_converter)
        
        # Process
        await pool._process_item(item)
        
        # Check state
        assert item.state == AsyncConversionItemState.COMPLETED
        assert item.process_start is not None
        assert item.process_end is not None
        
        # Check API was called
        mock_api.report.submit.assert_called_once()
        
        # Check stats
        assert pool._stats["successful"] == 1
    
    @pytest.mark.asyncio
    async def test_process_item_converter_error(self, pool, temp_watch_dir, mock_api, mock_converter):
        """Test handling converter error"""
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        mock_converter.convert.side_effect = Exception("Parse error")
        
        item = AsyncConversionItem(test_file, mock_converter)
        
        await pool._process_item(item)
        
        assert item.state == AsyncConversionItemState.ERROR
        assert pool._stats["errors"] == 1
    
    @pytest.mark.asyncio
    async def test_process_item_api_error(self, pool, temp_watch_dir, mock_api, mock_converter):
        """Test handling API error"""
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        mock_api.report.submit.side_effect = Exception("API error")
        
        item = AsyncConversionItem(test_file, mock_converter)
        
        await pool._process_item(item)
        
        assert item.state == AsyncConversionItemState.ERROR
        assert pool._stats["errors"] == 1


class TestAsyncConverterPoolConcurrency:
    """Test concurrent processing"""
    
    @pytest.mark.asyncio
    async def test_respects_max_concurrent(self, mock_config, mock_api, temp_watch_dir, mock_converter):
        """Test that max_concurrent is respected"""
        pool = AsyncConverterPool(mock_config, mock_api, max_concurrent=2)
        
        max_concurrent_seen = 0
        current_concurrent = 0
        
        async def slow_submit(report):
            nonlocal max_concurrent_seen, current_concurrent
            current_concurrent += 1
            max_concurrent_seen = max(max_concurrent_seen, current_concurrent)
            await asyncio.sleep(0.1)
            current_concurrent -= 1
        
        mock_api.report.submit = slow_submit
        
        # Queue multiple items
        items = []
        for i in range(5):
            test_file = temp_watch_dir / f"test{i}.xml"
            test_file.write_text(f"<test{i}/>")
            items.append(AsyncConversionItem(test_file, mock_converter))
        
        # Process all with semaphore - need to create queue items
        from pywats.queue import QueueItem
        queue_items = [QueueItem.create(item, priority=5) for item in items]
        tasks = [pool._process_with_limit(item, qi) for item, qi in zip(items, queue_items)]
        await asyncio.gather(*tasks)
        
        assert max_concurrent_seen <= 2


class TestAsyncConverterPoolFileWatching:
    """Test file watching"""
    
    def test_on_file_created_queues_item(self, pool, temp_watch_dir, mock_converter):
        """Test that file created event queues item"""
        pool._converters = [mock_converter]
        
        test_file = temp_watch_dir / "new.xml"
        test_file.write_text("<new/>")
        
        pool._on_file_created(test_file, mock_converter)
        
        # Should be in queue
        assert pool._queue.size == 1
    
    def test_on_file_created_ignores_non_matching(self, pool, temp_watch_dir, mock_converter):
        """Test that non-matching files are ignored"""
        mock_converter.matches_file.return_value = False
        pool._converters = [mock_converter]
        
        test_file = temp_watch_dir / "ignored.txt"
        test_file.write_text("text")
        
        pool._on_file_created(test_file, mock_converter)
        
        # Should not be in queue
        assert pool._queue.size == 0


class TestAsyncConverterPoolLifecycle:
    """Test pool lifecycle"""
    
    @pytest.mark.asyncio
    async def test_stop(self, pool):
        """Test stop cleans up"""
        pool._running = True
        
        await pool.stop()
        
        assert not pool.is_running
        assert len(pool._observers) == 0
