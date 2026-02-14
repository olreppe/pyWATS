"""
Tests for AsyncConverterPool startup file scanning functionality.

This module tests the critical data recovery feature that scans watch
directories on startup to queue existing files, preventing data loss
when files are dropped during system downtime.
"""

import asyncio
import pytest
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
from unittest.mock import Mock, AsyncMock, MagicMock

from pywats_client.service.async_converter_pool import (
    AsyncConverterPool,
    AsyncConversionItem,
    AsyncConversionItemState,
)
from pywats_client.core.config import ClientConfig, ConverterConfig
from pywats import AsyncWATS
from pywats_client.converters.base import ConverterBase


class MockConverter(ConverterBase):
    """Mock converter for testing"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self._name = config.get('name', 'MockConverter')
        self.watch_path = Path(config.get('watch_path', '/tmp/test'))
        self.watch_recursive = config.get('watch_recursive', False)
        self.priority = config.get('priority', 5)
        self._supported_extensions = config.get('extensions', ['.csv'])
    
    @property
    def name(self) -> str:
        """Converter name"""
        return self._name
    
    @property
    def supported_extensions(self):
        """Supported file extensions"""
        return self._supported_extensions
    
    def matches_file(self, file_path: Path) -> bool:
        """Check if file matches converter"""
        return file_path.suffix.lower() in self.supported_extensions
    
    def convert_file(self, file_path: Path, args: Any) -> Any:
        """Mock conversion - returns success"""
        from pywats_client.converters.base import ConverterResult
        return ConverterResult(
            success=True,
            report={'pn': 'TEST-001', 'sn': file_path.stem, 'result': 'Passed'},
            file_path=file_path
        )


@pytest.fixture
def temp_watch_dir(tmp_path):
    """Create temporary watch directory"""
    watch_dir = tmp_path / "watch"
    watch_dir.mkdir()
    return watch_dir


@pytest.fixture
def mock_config():
    """Create mock client configuration"""
    config = Mock(spec=ClientConfig)
    config.converter = Mock(spec=ConverterConfig)
    config.converter.enable_startup_scan = True
    config.converter.startup_scan_timeout = 30
    config.converter.startup_scan_max_files = 0
    return config


@pytest.fixture
def mock_api():
    """Create mock AsyncWATS API"""
    api = AsyncMock(spec=AsyncWATS)
    api.submit_uut = AsyncMock(return_value={'success': True})
    return api


@pytest.fixture
async def converter_pool(mock_config, mock_api):
    """Create AsyncConverterPool for testing"""
    pool = AsyncConverterPool(
        config=mock_config,
        api=mock_api,
        max_concurrent=5,
        enable_sandbox=False  # Disable sandbox for testing
    )
    yield pool
    # Cleanup
    if pool.is_running:
        await pool.stop()


class TestStartupScan:
    """Tests for startup file scanning"""
    
    @pytest.mark.asyncio
    async def test_scan_queues_all_existing_files(self, converter_pool, temp_watch_dir):
        """Test that startup scan finds and queues all existing files"""
        # Create test files
        for i in range(5):
            test_file = temp_watch_dir / f"test_{i}.csv"
            test_file.write_text(f"Test data {i}")
        
        # Setup converter
        converter = MockConverter({
            'name': 'TestConverter',
            'watch_path': str(temp_watch_dir),
            'extensions': ['.csv'],
            'priority': 5
        })
        converter_pool._converters = [converter]
        
        # Run startup scan
        stats = await converter_pool._scan_existing_files()
        
        # Verify all files queued
        assert stats['scanned'] == 5
        assert stats['queued'] == 5
        assert stats['skipped'] == 0
        assert stats['errors'] == 0
        
        # Verify queue size
        assert converter_pool._queue.size == 5
    
    @pytest.mark.asyncio
    async def test_scan_respects_extension_filter(self, converter_pool, temp_watch_dir):
        """Test that only matching extensions are queued"""
        # Create mixed file types
        (temp_watch_dir / "test1.csv").write_text("CSV data")
        (temp_watch_dir / "test2.xml").write_text("<xml/>")
        (temp_watch_dir / "test3.txt").write_text("Text data")
        (temp_watch_dir / "test4.csv").write_text("More CSV")
        
        # Converter only handles .csv
        converter = MockConverter({
            'name': 'CSVConverter',
            'watch_path': str(temp_watch_dir),
            'extensions': ['.csv'],
            'priority': 5
        })
        converter_pool._converters = [converter]
        
        # Run scan
        stats = await converter_pool._scan_existing_files()
        
        # Only CSV files queued
        assert stats['queued'] == 2
        assert converter_pool._queue.size == 2
    
    @pytest.mark.asyncio
    async def test_scan_skips_queued_files(self, converter_pool, temp_watch_dir):
        """Test that files with .queued markers are skipped"""
        # Create files
        file1 = temp_watch_dir / "test1.csv"
        file2 = temp_watch_dir / "test2.csv"
        file1.write_text("Data 1")
        file2.write_text("Data 2")
        
        # Create .queued marker for file1
        marker = temp_watch_dir / "test1.csv.queued"
        marker.write_text("queued")
        
        # Setup converter
        converter = MockConverter({
            'name': 'TestConverter',
            'watch_path': str(temp_watch_dir),
            'extensions': ['.csv']
        })
        converter_pool._converters = [converter]
        
        # Run scan
        stats = await converter_pool._scan_existing_files()
        
        # Only file2 queued (file1 skipped due to marker)
        assert stats['scanned'] == 2
        assert stats['queued'] == 1
        assert stats['skipped'] == 1
    
    @pytest.mark.asyncio
    async def test_scan_sorted_by_mtime(self, converter_pool, temp_watch_dir):
        """Test that files are queued in FIFO order (oldest first)"""
        import time
        
        # Create files with known order
        files = []
        for i in range(3):
            file = temp_watch_dir / f"test_{i}.csv"
            file.write_text(f"Data {i}")
            files.append(file)
            time.sleep(0.01)  # Ensure different mtimes
        
        # Setup converter
        converter = MockConverter({
            'name': 'TestConverter',
            'watch_path': str(temp_watch_dir),
            'extensions': ['.csv']
        })
        converter_pool._converters = [converter]
        
        # Run scan
        await converter_pool._scan_existing_files()
        
        # Get queued items and verify order
        queued_files = []
        while not converter_pool._queue.is_empty:
            try:
                item = await asyncio.wait_for(
                    converter_pool._queue.get(timeout=1.0),
                    timeout=2.0
                )
                if item:  # Only append if not None
                    queued_files.append(item.data.file_path.name)
            except asyncio.TimeoutError:
                break  # No more items
        
        # Should be in order: test_0, test_1, test_2 (oldest first)
        assert queued_files == ['test_0.csv', 'test_1.csv', 'test_2.csv']
    
    @pytest.mark.asyncio
    async def test_scan_disabled_via_config(self, converter_pool, temp_watch_dir):
        """Test that scan can be disabled via configuration"""
        # Create test files
        (temp_watch_dir / "test.csv").write_text("Data")
        
        # Disable startup scan
        converter_pool._startup_scan_enabled = False
        
        # Setup converter
        converter = MockConverter({
            'name': 'TestConverter',
            'watch_path': str(temp_watch_dir),
            'extensions': ['.csv']
        })
        converter_pool._converters = [converter]
        
        # Run scan
        stats = await converter_pool._scan_existing_files()
        
        # No files scanned when disabled
        assert stats['scanned'] == 0
        assert stats['queued'] == 0
        assert converter_pool._queue.is_empty
    
    @pytest.mark.asyncio
    async def test_deduplication_prevents_double_queue(self, converter_pool, temp_watch_dir):
        """Test that deduplication prevents watchdog events from re-queueing scanned files"""
        # Create test file
        test_file = temp_watch_dir / "test.csv"
        test_file.write_text("Test data")
        
        # Setup converter
        converter = MockConverter({
            'name': 'TestConverter',
            'watch_path': str(temp_watch_dir),
            'extensions': ['.csv']
        })
        converter_pool._converters = [converter]
        
        # Run startup scan
        await converter_pool._scan_existing_files()
        
        # Verify file in dedup set
        assert test_file in converter_pool._startup_scan_files
        assert converter_pool._queue.size == 1
        
        # Simulate watchdog event for same file
        converter_pool._on_file_created(test_file, converter)
        
        # File should NOT be queued again (still only 1 item in queue)
        assert converter_pool._queue.size == 1
    
    @pytest.mark.asyncio
    async def test_dedup_set_cleared_after_ttl(self, converter_pool, temp_watch_dir):
        """Test that deduplication set is cleared after TTL"""
        # Create test file
        test_file = temp_watch_dir / "test.csv"
        test_file.write_text("Test data")
        
        # Setup converter
        converter = MockConverter({
            'name': 'TestConverter',
            'watch_path': str(temp_watch_dir),
            'extensions': ['.csv']
        })
        converter_pool._converters = [converter]
        
        # Run scan (schedules cleanup after 5s)
        await converter_pool._scan_existing_files()
        
        # Verify file in set
        assert len(converter_pool._startup_scan_files) == 1
        assert not converter_pool._startup_scan_complete
        
        # Wait for TTL (5s + buffer)
        await asyncio.sleep(5.5)
        
        # Set should be cleared
        assert len(converter_pool._startup_scan_files) == 0
        assert converter_pool._startup_scan_complete


class TestStartupScanStatistics:
    """Tests for startup scan statistics"""
    
    @pytest.mark.asyncio
    async def test_scan_stats_accurate(self, converter_pool, temp_watch_dir):
        """Test that scan statistics are accurate"""
        # Create variety of files
        (temp_watch_dir / "valid1.csv").write_text("Data 1")
        (temp_watch_dir / "valid2.csv").write_text("Data 2")
        (temp_watch_dir / "wrong.txt").write_text("Wrong type")
        (temp_watch_dir / "queued.csv").write_text("Already queued")
        (temp_watch_dir / "queued.csv.queued").write_text("marker")
        
        # Setup converter
        converter = MockConverter({
            'name': 'TestConverter',
            'watch_path': str(temp_watch_dir),
            'extensions': ['.csv']
        })
        converter_pool._converters = [converter]
        
        # Run scan
        stats = await converter_pool._scan_existing_files()
        
        # Verify stats
        assert stats['scanned'] == 3  # queued.csv, valid1.csv, valid2.csv
        assert stats['queued'] == 2   # valid1, valid2
        assert stats['skipped'] == 1  # queued.csv (has marker)
        assert stats['errors'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
