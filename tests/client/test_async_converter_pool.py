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
    
    @pytest.mark.asyncio
    async def test_stop_with_active_tasks(self, pool, temp_watch_dir, mock_converter):
        """Test stop waits for active tasks to complete"""
        pool._running = True
        
        # Create fake active task
        async def slow_task():
            await asyncio.sleep(0.1)
        
        task = asyncio.create_task(slow_task())
        pool._active_tasks = [task]
        
        await pool.stop()
        
        assert not pool.is_running
        assert len(pool._active_tasks) == 0
    
    @pytest.mark.asyncio
    async def test_stop_accepts_gracefully(self, pool):
        """Test stop_accepting stops new work"""
        pool._running = True
        
        await pool.stop_accepting()
        
        # Should have set stop event and cleared observers
        assert pool._stop_event.is_set()
        assert len(pool._observers) == 0
    
    @pytest.mark.asyncio
    async def test_get_active_count(self, pool):
        """Test active count tracking"""
        pool._active_count = 3
        
        count = await pool.get_active_count()
        
        assert count == 3


class TestAsyncConversionItemPriority:
    """Test conversion item priority ordering"""
    
    def test_priority_comparison_lower_is_higher(self, temp_watch_dir, mock_converter):
        """Test that lower priority number means higher priority"""
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item_high = AsyncConversionItem(test_file, mock_converter, priority=1)
        item_low = AsyncConversionItem(test_file, mock_converter, priority=5)
        
        # Priority 1 should come before priority 5
        assert item_high < item_low
    
    def test_priority_comparison_fifo_when_same(self, temp_watch_dir, mock_converter):
        """Test FIFO ordering when priorities are equal"""
        from datetime import timedelta
        import time
        
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item1 = AsyncConversionItem(test_file, mock_converter, priority=5)
        time.sleep(0.01)  # Ensure different timestamps
        item2 = AsyncConversionItem(test_file, mock_converter, priority=5)
        
        # item1 queued first, should come before item2
        assert item1 < item2


class TestAsyncConverterPoolConfigReload:
    """Test configuration reload"""
    
    @pytest.mark.asyncio
    async def test_reload_config_updates_converters(self, pool, mock_config, temp_watch_dir):
        """Test that reload_config updates converters list"""
        # Create mock converter config
        mock_config.converters = []
        
        await pool.reload_config(mock_config)
        
        assert pool.config == mock_config
        # Converters list should be updated (cleared if empty config)
        assert len(pool._converters) == 0


class TestAsyncConverterPoolSandbox:
    """Test sandboxed execution"""
    
    @pytest.mark.asyncio
    async def test_init_with_sandbox_disabled(self, mock_config, mock_api):
        """Test pool initialization with sandbox disabled"""
        pool = AsyncConverterPool(
            mock_config,
            mock_api,
            enable_sandbox=False
        )
        
        assert not pool._enable_sandbox
        assert pool.stats["sandbox_enabled"] is False
    
    @pytest.mark.asyncio
    async def test_init_with_sandbox_enabled(self, mock_config, mock_api):
        """Test pool initialization with sandbox enabled (default)"""
        pool = AsyncConverterPool(
            mock_config,
            mock_api,
            enable_sandbox=True
        )
        
        assert pool._enable_sandbox
        assert pool.stats["sandbox_enabled"] is True
    
    def test_should_use_sandbox_trusted_mode(self, pool, mock_converter):
        """Test that trusted_mode converters skip sandbox"""
        mock_converter.trusted_mode = True
        
        assert not pool._should_use_sandbox(mock_converter)
    
    def test_should_use_sandbox_no_source_path(self, pool):
        """Test that converters without source_path use sandbox"""
        # Create fresh mock without trusted_mode or source_path
        converter = MagicMock()
        converter.name = "TestConverter"
        # Explicitly ensure no trusted_mode or source_path
        if hasattr(converter, 'trusted_mode'):
            del converter.trusted_mode
        if hasattr(converter, 'source_path'):
            del converter.source_path
        
        # Should use sandbox by default for security
        assert pool._should_use_sandbox(converter)
    
    def test_should_use_sandbox_with_source_path(self, pool, temp_watch_dir):
        """Test that converters with source_path use sandbox"""
        # Create fresh mock with source_path but no trusted_mode
        converter = MagicMock()
        converter.name = "TestConverter"
        converter.source_path = temp_watch_dir / "converter.py"
        # Ensure no trusted_mode
        if hasattr(converter, 'trusted_mode'):
            del converter.trusted_mode
        
        assert pool._should_use_sandbox(converter)


class TestAsyncConverterPoolQueueProcessing:
    """Test queue processing and priority"""
    
    @pytest.mark.asyncio
    async def test_process_item_updates_stats(self, pool, temp_watch_dir, mock_api, mock_converter):
        """Test that processing updates statistics"""
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item = AsyncConversionItem(test_file, mock_converter)
        
        # Setup converter to return valid report
        mock_converter.convert.return_value = {"report": "data"}
        mock_converter.trusted_mode = True  # Skip sandbox for this test
        mock_converter.post_process_action = None
        
        initial_successful = pool._stats["successful"]
        initial_total = pool._stats["total_processed"]
        
        await pool._process_item(item)
        
        assert pool._stats["successful"] == initial_successful + 1
        assert pool._stats["total_processed"] == initial_total + 1
    
    @pytest.mark.asyncio
    async def test_process_item_error_updates_stats(self, pool, temp_watch_dir, mock_api, mock_converter):
        """Test that errors update error statistics"""
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item = AsyncConversionItem(test_file, mock_converter)
        
        # Setup converter to fail
        mock_converter.convert.side_effect = Exception("Converter error")
        mock_converter.trusted_mode = True
        
        initial_errors = pool._stats["errors"]
        
        await pool._process_item(item)
        
        assert pool._stats["errors"] == initial_errors + 1
        assert item.error == "Converter error"


class TestAsyncConverterPoolPostProcessing:
    """Test post-processing actions"""
    
    @pytest.mark.asyncio
    async def test_post_process_delete(self, pool, temp_watch_dir, mock_converter):
        """Test DELETE post-processing action"""
        from pywats_client.converters.models import PostProcessAction
        
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item = AsyncConversionItem(test_file, mock_converter)
        mock_converter.post_process_action = PostProcessAction.DELETE
        
        await pool._post_process(item)
        
        # File should be deleted
        assert not test_file.exists()
    
    @pytest.mark.asyncio
    async def test_post_process_move(self, pool, temp_watch_dir, mock_converter):
        """Test MOVE post-processing action"""
        from pywats_client.converters.models import PostProcessAction
        
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        archive_dir = temp_watch_dir / "archive"
        
        item = AsyncConversionItem(test_file, mock_converter)
        mock_converter.post_process_action = PostProcessAction.MOVE
        mock_converter.archive_path = archive_dir
        
        await pool._post_process(item)
        
        # File should be moved to archive
        assert not test_file.exists()
        assert (archive_dir / "test.xml").exists()
    
    @pytest.mark.asyncio
    async def test_post_process_keep(self, pool, temp_watch_dir, mock_converter):
        """Test KEEP post-processing action (no action)"""
        from pywats_client.converters.models import PostProcessAction
        
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item = AsyncConversionItem(test_file, mock_converter)
        mock_converter.post_process_action = PostProcessAction.KEEP
        
        await pool._post_process(item)
        
        # File should still exist
        assert test_file.exists()


class TestAsyncConverterPoolErrorHandling:
    """Test error handling"""
    
    @pytest.mark.asyncio
    async def test_handle_error_moves_to_error_folder(self, pool, temp_watch_dir, mock_converter):
        """Test that error handling moves file to error folder"""
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        error_dir = temp_watch_dir / "error"
        
        item = AsyncConversionItem(test_file, mock_converter)
        mock_converter.error_path = error_dir
        
        await pool._handle_error(item, Exception("Test error"))
        
        # File should be moved to error folder
        assert not test_file.exists()
        assert (error_dir / "test.xml").exists()
    
    @pytest.mark.asyncio
    async def test_handle_error_no_error_path(self, pool, temp_watch_dir, mock_converter):
        """Test error handling when no error path configured"""
        test_file = temp_watch_dir / "test.xml"
        test_file.write_text("<test/>")
        
        item = AsyncConversionItem(test_file, mock_converter)
        mock_converter.error_path = None
        
        # Should not raise exception
        await pool._handle_error(item, Exception("Test error"))
        
        # File should still exist (not moved)
        assert test_file.exists()


class TestAsyncConverterPoolArchiveProcessing:
    """Test archive queue processing"""
    
    @pytest.mark.asyncio
    async def test_process_archive_queues(self, pool, mock_converter):
        """Test archive queue processing for all converters"""
        pool._converters = [mock_converter]
        
        await pool._process_archive_queues()
        
        # Archive queue processor should be called
        mock_converter.process_archive_queue.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_archive_queues_handles_errors(self, pool, mock_converter):
        """Test that archive processing continues on error"""
        mock_converter.process_archive_queue.side_effect = Exception("Archive error")
        pool._converters = [mock_converter]
        
        # Should not raise exception
        await pool._process_archive_queues()
        
        # Should have attempted the call
        mock_converter.process_archive_queue.assert_called_once()


class TestAsyncConverterPoolConverterLoading:
    """Test converter loading from configuration"""
    
    @pytest.mark.asyncio
    async def test_load_converters_empty_config(self, pool, mock_config):
        """Test loading converters from empty config"""
        mock_config.converters = []
        
        await pool._load_converters()
        
        assert len(pool._converters) == 0
    
    @pytest.mark.asyncio
    async def test_load_converters_skips_invalid(self, pool, mock_config):
        """Test that invalid converter configs are skipped"""
        # Config with no type field
        mock_config.converters = [{"name": "Invalid"}]
        
        await pool._load_converters()
        
        # Should have skipped invalid config
        assert len(pool._converters) == 0


class TestAsyncConverterPoolWatcherManagement:
    """Test file watcher management"""
    
    @pytest.mark.asyncio
    async def test_create_watcher_no_path(self, pool, mock_converter):
        """Test watcher creation skips converters without watch path"""
        mock_converter.watch_path = None
        
        watcher = pool._create_watcher(mock_converter)
        
        assert watcher is None
    
    @pytest.mark.asyncio
    async def test_create_watcher_nonexistent_path(self, pool, mock_converter, temp_watch_dir):
        """Test watcher creation skips nonexistent paths"""
        mock_converter.watch_path = temp_watch_dir / "nonexistent"
        
        watcher = pool._create_watcher(mock_converter)
        
        assert watcher is None
    
    @pytest.mark.asyncio
    async def test_create_watcher_valid_path(self, pool, mock_converter, temp_watch_dir):
        """Test watcher creation with valid path"""
        mock_converter.watch_path = temp_watch_dir
        mock_converter.watch_recursive = False
        
        watcher = pool._create_watcher(mock_converter)
        
        assert watcher is not None
        # Clean up
        watcher.stop()


class TestFileEventHandler:
    """Test watchdog file event handler"""
    
    def test_on_moved_queues_matching_file(self, pool, temp_watch_dir, mock_converter):
        """Test that file move events queue matching files"""
        from pywats_client.service.async_converter_pool import _FileEventHandler
        from watchdog.events import FileMovedEvent
        
        pool._converters = [mock_converter]
        mock_converter.matches_file.return_value = True
        
        handler = _FileEventHandler(pool, mock_converter)
        
        # Create move event
        src_path = str(temp_watch_dir / "old.xml")
        dest_path = str(temp_watch_dir / "new.xml")
        event = FileMovedEvent(src_path, dest_path)
        
        handler.on_moved(event)
        
        # Should queue the file
        assert pool._queue.size == 1
    
    def test_on_moved_ignores_non_matching(self, pool, temp_watch_dir, mock_converter):
        """Test that move events ignore non-matching files"""
        from pywats_client.service.async_converter_pool import _FileEventHandler
        from watchdog.events import FileMovedEvent
        
        pool._converters = [mock_converter]
        mock_converter.matches_file.return_value = False
        
        handler = _FileEventHandler(pool, mock_converter)
        
        src_path = str(temp_watch_dir / "old.txt")
        dest_path = str(temp_watch_dir / "new.txt")
        event = FileMovedEvent(src_path, dest_path)
        
        handler.on_moved(event)
        
        # Should not queue
        assert pool._queue.size == 0
    
    def test_on_moved_ignores_directory(self, pool, temp_watch_dir, mock_converter):
        """Test that directory move events are ignored"""
        from pywats_client.service.async_converter_pool import _FileEventHandler
        from watchdog.events import DirMovedEvent
        
        handler = _FileEventHandler(pool, mock_converter)
        
        src_path = str(temp_watch_dir / "old_dir")
        dest_path = str(temp_watch_dir / "new_dir")
        event = DirMovedEvent(src_path, dest_path)
        
        handler.on_moved(event)
        
        # Should not queue directories
        assert pool._queue.size == 0
