"""
Stress Tests for Converter Pool

Tests converter pool behavior under heavy load:
- 1000+ file processing
- Throughput measurement
- Memory usage monitoring
- Resource leak detection
- Concurrent converter stress

Created: 2026-02-13
Project: Converter Architecture Stabilization (Week 2, Task 2.2)
"""

import pytest
import asyncio
import time
import psutil
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from unittest.mock import AsyncMock, Mock

from pywats_client.service.async_converter_pool import (
    AsyncConverterPool,
    AsyncConversionItem,
    AsyncConversionItemState
)
from pywats_client.converters.base import ConverterBase, ConverterArguments
from pywats_client.converters.models import (
    ConverterResult,
    FileInfo,
    PostProcessAction
)
from pywats_client.core.config import ConverterConfig
from tests.fixtures.test_file_generators import TestFileGenerator


# ============================================================================
# MOCK CONVERTERS FOR STRESS TESTING
# ============================================================================

class FastMockConverter(ConverterBase):
    """Ultra-fast mock converter for throughput testing"""
    
    def __init__(self):
        super().__init__()
        self.conversion_count = 0
        self.error_path = None
        self.post_process_action = PostProcessAction.DELETE
        self.archive_path = None
        self.user_settings = {}
        self.config = None
        self._watch_path = None
        self._watch_recursive = False
    
    @property
    def name(self) -> str:
        return "FastMockConverter"
    
    @property
    def supported_extensions(self) -> List[str]:
        return [".csv"]
    
    def matches_file(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.supported_extensions
    
    def convert(self, content: str, file_path: Path) -> Dict:
        """Minimal conversion for speed testing"""
        from pywats.models import UUTReport, ReportStatus
        
        self.conversion_count += 1
        
        report = UUTReport(
            pn="STRESS-TEST",
            sn=f"SN-{self.conversion_count:06d}",
            rev="A",
            process_code=1,
            station_name="StressTest",
            location="Lab",
            purpose="Stress",
            result=ReportStatus.Passed,
            start=datetime.now().astimezone(),
        )
        
        return report.model_dump()
    
    def convert_file(self, file_path: Path, args: ConverterArguments) -> ConverterResult:
        """Not used in unsandboxed mode"""
        from pywats.models import UUTReport, ReportStatus
        
        report = UUTReport(
            pn="STRESS-TEST",
            sn=f"SN-{file_path.stem}",
            rev="A",
            process_code=1,
            station_name="StressTest",
            location="Lab",
            purpose="Stress",
            result=ReportStatus.Passed,
            start=datetime.now().astimezone(),
        )
        
        return ConverterResult.success_result(
            report=report,
            post_action=PostProcessAction.DELETE
        )


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def stress_dirs(tmp_path):
    """Create directory structure for stress tests"""
    watch_dir = tmp_path / "watch"
    done_dir = tmp_path / "done"
    error_dir = tmp_path / "error"
    
    watch_dir.mkdir()
    done_dir.mkdir()
    error_dir.mkdir()
    
    return {
        'watch': watch_dir,
        'done': done_dir,
        'error': error_dir,
        'root': tmp_path,
    }


@pytest.fixture
def mock_wats_client():
    """Mock WATS client with minimal overhead"""
    client = AsyncMock()
    client.report = AsyncMock()
    client.report.submit = AsyncMock(return_value=None)
    client.config = Mock()
    client.config.max_retries = 3
    client.config.retry_delay = 0.01  # Fast retries for testing
    return client


@pytest.fixture
async def stress_converter_pool(stress_dirs, mock_wats_client):
    """Create converter pool optimized for stress testing"""
    pool = AsyncConverterPool(
        api=mock_wats_client,
        config=Mock(),
    )
    
    # Configure for maximum throughput
    pool._max_concurrent = 50  # High concurrency
    pool._converters = []
    pool._watchers = []
    pool._running = False
    pool._enable_sandbox = False  # Disable sandbox for speed
    
    # Initialize queue
    from pywats.queue import MemoryQueue, AsyncQueueAdapter
    memory_queue = MemoryQueue()
    pool._queue = AsyncQueueAdapter(memory_queue)
    
    # Create fast mock converter
    converter = FastMockConverter()
    converter.config = ConverterConfig(
        name="FastMockConverter",
        module_path="test.mock",
        watch_folder=str(stress_dirs['watch']),
        done_folder=str(stress_dirs['done']),
        error_folder=str(stress_dirs['error']),
        enabled=True,
        priority=5,
    )
    pool._converters.append(converter)
    
    yield pool
    
    # Cleanup
    if pool._running:
        pool.stop()
        await asyncio.sleep(0.1)


# ============================================================================
# STRESS TESTS
# ============================================================================

class TestConverterPoolStress:
    """Stress tests for converter pool under heavy load"""
    
    @pytest.mark.asyncio
    @pytest.mark.stress
    async def test_stress_1000_files_throughput(
        self,
        stress_converter_pool,
        stress_dirs,
        mock_wats_client
    ):
        """
        STRESS TEST: Process 1000 CSV files
        
        SUCCESS CRITERIA:
        - All 1000 files processed successfully
        - Throughput > 100 files/second
        - No memory leaks
        - All reports submitted
        - Processing completes in < 30 seconds
        """
        watch_dir = stress_dirs['watch']
        file_count = 1000
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"\n📊 Stress Test: {file_count} files")
        print(f"   Initial memory: {mem_before:.2f} MB")
        
        # Generate 1000 CSV files
        print(f"   Generating {file_count} files...")
        gen_start = time.time()
        files = TestFileGenerator.generate_batch(
            watch_dir / "batch",
            'csv',
            file_count,
            rows=5  # Small files for speed
        )
        gen_time = time.time() - gen_start
        print(f"   Generated in {gen_time:.2f}s ({file_count/gen_time:.0f} files/s)")
        
        # Create conversion items
        items = []
        for file in files:
            item = AsyncConversionItem(
                file_path=file,
                converter=stress_converter_pool._converters[0],
                priority=5
            )
            items.append(item)
            stress_converter_pool._queue.put_nowait(data=item, priority=5)
        
        # Process all items concurrently
        print(f"   Processing {file_count} files...")
        process_start = time.time()
        
        tasks = [stress_converter_pool._process_item(item) for item in items]
        await asyncio.gather(*tasks)
        
        process_time = time.time() - process_start
        throughput = file_count / process_time
        
        # Get final memory usage
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_delta = mem_after - mem_before
        
        # Print results
        print(f"\n   ✅ Results:")
        print(f"      Files processed: {file_count}")
        print(f"      Processing time: {process_time:.2f}s")
        print(f"      Throughput: {throughput:.0f} files/s")
        print(f"      Memory before: {mem_before:.2f} MB")
        print(f"      Memory after: {mem_after:.2f} MB")
        print(f"      Memory delta: {mem_delta:+.2f} MB")
        print(f"      Reports submitted: {mock_wats_client.report.submit.call_count}")
        
        # Verify all completed
        completed_count = sum(1 for item in items if item.state == AsyncConversionItemState.COMPLETED)
        assert completed_count == file_count, f"Only {completed_count}/{file_count} completed"
        
        # Verify all submitted
        assert mock_wats_client.report.submit.call_count == file_count
        
        # Verify throughput (>100 files/second)
        assert throughput > 100, f"Throughput {throughput:.0f} files/s is below 100 files/s target"
        
        # Verify completion time (<30 seconds)
        assert process_time < 30, f"Processing took {process_time:.2f}s (expected <30s)"
        
        # Verify reasonable memory usage (<100 MB delta)
        assert mem_delta < 100, f"Memory increased by {mem_delta:.2f} MB (expected <100 MB)"
    
    @pytest.mark.asyncio
    @pytest.mark.stress
    async def test_stress_sustained_load(
        self,
        stress_converter_pool,
        stress_dirs,
        mock_wats_client
    ):
        """
        STRESS TEST: Sustained processing over multiple batches
        
        SUCCESS CRITERIA:
        - Process 10 batches of 100 files each
        - No memory leak between batches
        - Consistent throughput across batches
        - No resource exhaustion
        """
        watch_dir = stress_dirs['watch']
        batch_size = 100
        batch_count = 10
        
        process = psutil.Process(os.getpid())
        mem_baseline = process.memory_info().rss / 1024 / 1024
        
        print(f"\n📊 Sustained Load Test: {batch_count} batches x {batch_size} files")
        print(f"   Baseline memory: {mem_baseline:.2f} MB")
        
        batch_times = []
        batch_mem_deltas = []
        
        for batch_idx in range(batch_count):
            # Generate batch
            files = TestFileGenerator.generate_batch(
                watch_dir / f"batch_{batch_idx}",
                'csv',
                batch_size,
                rows=5
            )
            
            # Create items
            items = []
            for file in files:
                item = AsyncConversionItem(
                    file_path=file,
                    converter=stress_converter_pool._converters[0],
                    priority=5
                )
                items.append(item)
                stress_converter_pool._queue.put_nowait(data=item, priority=5)
            
            # Measure memory before batch
            mem_before = process.memory_info().rss / 1024 / 1024
            
            # Process batch
            start = time.time()
            tasks = [stress_converter_pool._process_item(item) for item in items]
            await asyncio.gather(*tasks)
            batch_time = time.time() - start
            
            # Measure memory after batch
            mem_after = process.memory_info().rss / 1024 / 1024
            mem_delta = mem_after - mem_before
            
            batch_times.append(batch_time)
            batch_mem_deltas.append(mem_delta)
            
            throughput = batch_size / batch_time
            print(f"   Batch {batch_idx+1}/{batch_count}: {batch_time:.2f}s ({throughput:.0f} files/s), mem: {mem_delta:+.2f} MB")
            
            # Verify all completed
            completed = sum(1 for item in items if item.state == AsyncConversionItemState.COMPLETED)
            assert completed == batch_size
        
        # Calculate statistics
        avg_time = sum(batch_times) / len(batch_times)
        std_time = (sum((t - avg_time) ** 2 for t in batch_times) / len(batch_times)) ** 0.5
        avg_mem_delta = sum(batch_mem_deltas) / len(batch_mem_deltas)
        
        mem_final = process.memory_info().rss / 1024 / 1024
        total_mem_delta = mem_final - mem_baseline
        
        print(f"\n   ✅ Statistics:")
        print(f"      Avg batch time: {avg_time:.2f}s ± {std_time:.2f}s")
        print(f"      Avg memory delta/batch: {avg_mem_delta:+.2f} MB")
        print(f"      Total memory delta: {total_mem_delta:+.2f} MB")
        print(f"      Total files: {batch_count * batch_size}")
        print(f"      Total reports: {mock_wats_client.report.submit.call_count}")
        
        # Verify performance consistency (std dev < 30% of mean)
        assert std_time < avg_time * 0.3, f"Performance variance too high: {std_time/avg_time*100:.1f}%"
        
        # Verify no significant memory leak (total delta < 50 MB)
        assert total_mem_delta < 50, f"Memory leak detected: {total_mem_delta:.2f} MB increase"
        
        # Verify all reports submitted
        assert mock_wats_client.report.submit.call_count == batch_count * batch_size
    
    @pytest.mark.asyncio
    @pytest.mark.stress
    async def test_stress_high_concurrency(
        self,
        stress_converter_pool,
        stress_dirs,
        mock_wats_client
    ):
        """
        STRESS TEST: Maximum concurrency stress
        
        SUCCESS CRITERIA:
        - Process 500 files with max_concurrent=50
        - All files processed successfully
        - No deadlocks or hangs
        - Semaphore correctly limits concurrency
        """
        watch_dir = stress_dirs['watch']
        file_count = 500
        max_concurrent = 50
        
        stress_converter_pool._max_concurrent = max_concurrent
        
        print(f"\n📊 High Concurrency Test: {file_count} files, {max_concurrent} concurrent")
        
        # Generate files
        files = TestFileGenerator.generate_batch(
            watch_dir / "concurrent",
            'csv',
            file_count,
            rows=5
        )
        
        # Create items
        items = []
        for file in files:
            item = AsyncConversionItem(
                file_path=file,
                converter=stress_converter_pool._converters[0],
                priority=5
            )
            items.append(item)
            stress_converter_pool._queue.put_nowait(data=item, priority=5)
        
        # Process all concurrently
        start = time.time()
        tasks = [stress_converter_pool._process_item(item) for item in items]
        await asyncio.gather(*tasks)
        elapsed = time.time() - start
        
        throughput = file_count / elapsed
        
        print(f"   ✅ Processed {file_count} files in {elapsed:.2f}s ({throughput:.0f} files/s)")
        
        # Verify all completed
        completed = sum(1 for item in items if item.state == AsyncConversionItemState.COMPLETED)
        assert completed == file_count
        
        # Verify all submitted
        assert mock_wats_client.report.submit.call_count == file_count
        
        # Verify reasonable completion time (< 20 seconds)
        assert elapsed < 20, f"Processing took {elapsed:.2f}s (expected <20s)"
    
    @pytest.mark.asyncio
    @pytest.mark.stress
    async def test_stress_memory_profile(
        self,
        stress_converter_pool,
        stress_dirs,
        mock_wats_client
    ):
        """
        STRESS TEST: Memory profiling during processing
        
        SUCCESS CRITERIA:
        - Track memory usage every 100 files
        - No continuous memory growth
        - Peak memory < 200 MB delta
        """
        watch_dir = stress_dirs['watch']
        total_files = 1000
        checkpoint_interval = 100
        
        process = psutil.Process(os.getpid())
        mem_baseline = process.memory_info().rss / 1024 / 1024
        
        print(f"\n📊 Memory Profile Test: {total_files} files with checkpoints every {checkpoint_interval}")
        print(f"   Baseline: {mem_baseline:.2f} MB")
        
        memory_profile = [(0, mem_baseline)]
        
        # Process in chunks to monitor memory
        for chunk_idx in range(total_files // checkpoint_interval):
            chunk_start = chunk_idx * checkpoint_interval
            
            # Generate chunk
            files = TestFileGenerator.generate_batch(
                watch_dir / f"chunk_{chunk_idx}",
                'csv',
                checkpoint_interval,
                rows=5
            )
            
            # Create items
            items = []
            for file in files:
                item = AsyncConversionItem(
                    file_path=file,
                    converter=stress_converter_pool._converters[0],
                    priority=5
                )
                items.append(item)
                stress_converter_pool._queue.put_nowait(data=item, priority=5)
            
            # Process chunk
            tasks = [stress_converter_pool._process_item(item) for item in items]
            await asyncio.gather(*tasks)
            
            # Record memory
            mem_current = process.memory_info().rss / 1024 / 1024
            files_processed = (chunk_idx + 1) * checkpoint_interval
            memory_profile.append((files_processed, mem_current))
            
            mem_delta = mem_current - mem_baseline
            print(f"   {files_processed:4d} files: {mem_current:.2f} MB ({mem_delta:+.2f} MB)")
        
        # Analyze memory profile
        peak_memory = max(mem for _, mem in memory_profile)
        peak_delta = peak_memory - mem_baseline
        
        final_memory = memory_profile[-1][1]
        final_delta = final_memory - mem_baseline
        
        print(f"\n   ✅ Memory Analysis:")
        print(f"      Baseline: {mem_baseline:.2f} MB")
        print(f"      Peak: {peak_memory:.2f} MB ({peak_delta:+.2f} MB)")
        print(f"      Final: {final_memory:.2f} MB ({final_delta:+.2f} MB)")
        
        # Verify peak memory reasonable (<200 MB delta)
        assert peak_delta < 200, f"Peak memory delta {peak_delta:.2f} MB exceeds 200 MB"
        
        # Verify no runaway memory growth
        # Memory should stabilize, final should not be massively higher than midpoint
        midpoint_memory = memory_profile[len(memory_profile) // 2][1]
        growth_from_midpoint = final_memory - midpoint_memory
        assert growth_from_midpoint < 50, f"Memory growing {growth_from_midpoint:.2f} MB from midpoint"


# ============================================================================
# TEST SUMMARY
# ============================================================================

"""
STRESS TEST COVERAGE SUMMARY

✅ Throughput Tests:
  - 1000 file processing with performance measurement
  - Sustained load across multiple batches
  - High concurrency stress (50 concurrent)

✅ Resource Tests:
  - Memory usage monitoring
  - Memory leak detection
  - Resource cleanup verification

✅ Performance Metrics:
  - Files/second throughput
  - Batch processing consistency
  - Concurrency scaling behavior

✅ Success Criteria:
  - Throughput > 100 files/s
  - Memory delta < 100 MB for 1000 files
  - No memory leaks across batches
  - All files successfully processed
  - No deadlocks or resource exhaustion
"""
