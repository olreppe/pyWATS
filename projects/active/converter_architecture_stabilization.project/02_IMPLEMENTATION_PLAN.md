# Implementation Plan: Converter Architecture Stabilization

**Created:** February 13, 2026  
**Estimated Duration:** 3 weeks  
**Target Completion:** March 6, 2026

---

## Overview

This document outlines the step-by-step execution plan for stabilizing and testing the converter architecture to achieve production-grade reliability.

**Approach:** Test-driven validation with incremental fixes
- Week 1: Unit tests + critical fixes
- Week 2: Integration tests + stress tests
- Week 3: Error injection + performance + documentation

---

## Prerequisites

### Test Data Strategy

**RECOMMENDATION: Hybrid Approach**

1. **Synthetic Test Files (Auto-Generated)** - For stress/performance testing
   - ✅ Can generate 1000+ files on demand
   - ✅ Reproducible scenarios
   - ✅ No sensitive data
   - ✅ Parameterizable (sizes, errors, patterns)
   - 🎯 **PRIMARY test data source**

2. **Real Sample Files (Collected)** - For validation only
   - ✅ Realistic edge cases
   - ✅ Validates against actual use
   - ⚠️ Small curated set (5-10 per converter type)
   - 🎯 **SECONDARY validation data**

**Decision:** Create test file generators (see Task 1.1) rather than collecting production files.

### Required Tools
- ✅ pytest with coverage plugin
- ✅ pytest-asyncio for async tests
- ✅ pytest-timeout for hanging test detection
- ✅ mock/unittest.mock for mocking
- ⏳ NEW: memory_profiler for leak detection
- ⏳ NEW: pytest-benchmark for performance tests

### Development Environment
- Python 3.8+ with virtual environment
- All dependencies installed (`pip install -r requirements.txt`)
- WATS test server (or mocks)

---

## Week 1: Unit Tests + Critical Fixes

### Task 1.1: Create Test File Generators ⏱️ 4 hours

**Priority:** CRITICAL (blocks all other testing)

**Create:** `tests/fixtures/test_file_generators.py`

**Generators to Implement:**

```python
class TestFileGenerator:
    """Generate synthetic test files for converter testing."""
    
    @staticmethod
    def generate_csv_file(
        output_path: Path,
        rows: int = 100,
        include_header: bool = True,
        corrupt: bool = False
    ) -> Path:
        """
        Generate CSV test file.
        
        Args:
            output_path: Where to save file
            rows: Number of data rows
            include_header: Include CSV header
            corrupt: Introduce random corruption
        
        Returns:
            Path to generated file
        """
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            if include_header:
                writer.writerow(['Serial', 'PartNumber', 'Status', 'Timestamp'])
            
            for i in range(rows):
                if corrupt and i == rows // 2:
                    # Corrupt middle row (missing field)
                    writer.writerow(['SN001', 'PN123'])
                else:
                    writer.writerow([
                        f'SN{i:06d}',
                        f'PN{i % 10:03d}',
                        random.choice(['PASS', 'FAIL']),
                        datetime.now().isoformat()
                    ])
        
        return output_path
    
    @staticmethod
    def generate_xml_file(
        output_path: Path,
        test_steps: int = 10,
        malformed: bool = False
    ) -> Path:
        """Generate XML test file (UUT report format)."""
        # XML with <UUT>, <Step>, <Measurement> elements
    
    @staticmethod
    def generate_txt_file(
        output_path: Path,
        size_kb: int = 10,
        encoding: str = 'utf-8'
    ) -> Path:
        """Generate text file with specific size."""
    
    @staticmethod
    def generate_batch(
        output_dir: Path,
        file_type: str,
        count: int,
        **kwargs
    ) -> List[Path]:
        """
        Generate multiple files at once.
        
        Args:
            output_dir: Directory for files
            file_type: 'csv', 'xml', 'txt'
            count: Number of files to generate
            **kwargs: Passed to individual generators
        
        Returns:
            List of generated file paths
        """
        generator = {
            'csv': cls.generate_csv_file,
            'xml': cls.generate_xml_file,
            'txt': cls.generate_txt_file
        }[file_type]
        
        files = []
        for i in range(count):
            path = output_dir / f"test_{i:04d}.{file_type}"
            files.append(generator(path, **kwargs))
        
        return files
```

**Usage in Tests:**
```python
def test_converter_handles_1000_files():
    # Generate 1000 CSV files
    files = TestFileGenerator.generate_batch(
        output_dir=temp_dir,
        file_type='csv',
        count=1000,
        rows=50
    )
    
    # Run conversion test
    assert len(files) == 1000
```

**Success Criteria:**
- ✅ Can generate CSV, XML, TXT files
- ✅ Can generate batches (1000+ files)
- ✅ Can inject corruption/errors
- ✅ Can control file sizes (1KB - 10MB)
- ✅ Generators are fast (<1 second for 1000 files)

---

### Task 1.2: Unit Tests - FileConverter & Base Classes ⏱️ 6 hours

**Priority:** HIGH

**Create:** `tests/client/converters/test_file_converter.py`

**Tests to Write:**

```python
class TestFileConverter:
    """Test FileConverter base class."""
    
    def test_matches_file_with_valid_pattern(self):
        """Test file pattern matching"""
        converter = CSVConverter()  # Example converter
        assert converter.matches_file(Path("data.csv")) == True
        assert converter.matches_file(Path("data.xml")) == False
    
    def test_convert_valid_file(self, temp_dir):
        """Test successful conversion"""
        # Generate test file
        csv_file = TestFileGenerator.generate_csv_file(
            temp_dir / "test.csv",
            rows=10
        )
        
        # Create converter
        converter = CSVConverter()
        context = ConverterContext.from_config(converter.config)
        source = ConverterSource(file_path=csv_file)
        
        # Convert
        result = converter.convert(source, context)
        
        # Verify
        assert result.success == True
        assert result.report is not None
        assert result.post_action == PostProcessAction.MOVE
    
    def test_convert_missing_file(self, temp_dir):
        """Test error handling for missing file"""
        converter = CSVConverter()
        context = ConverterContext.from_config(converter.config)
        source = ConverterSource(file_path=temp_dir / "missing.csv")
        
        result = converter.convert(source, context)
        
        assert result.success == False
        assert "not found" in result.error.lower()
    
    def test_convert_corrupted_file(self, temp_dir):
        """Test error handling for corrupted file"""
        csv_file = TestFileGenerator.generate_csv_file(
            temp_dir / "corrupt.csv",
            rows=10,
            corrupt=True
        )
        
        converter = CSVConverter()
        context = ConverterContext.from_config(converter.config)
        source = ConverterSource(file_path=csv_file)
        
        result = converter.convert(source, context)
        
        # Should fail gracefully or succeed with warnings
        if not result.success:
            assert result.error is not None
    
    def test_validate_returns_confidence(self, temp_dir):
        """Test validation returns confidence score"""
        csv_file = TestFileGenerator.generate_csv_file(
            temp_dir / "test.csv",
            rows=10
        )
        
        converter = CSVConverter()
        context = ConverterContext.from_config(converter.config)
        source = ConverterSource(file_path=csv_file)
        
        validation = converter.validate(source, context)
        
        assert 0.0 <= validation.confidence <= 1.0
```

**Success Criteria:**
- ✅ 15+ tests for FileConverter
- ✅ Coverage >90% for file_converter.py
- ✅ All error paths tested

---

### Task 1.3: Unit Tests - AsyncConverterPool ⏱️ 8 hours

**Priority:** CRITICAL

**Create:** `tests/client/service/test_async_converter_pool_comprehensive.py`

**Tests to Write:**

```python
class TestAsyncConverterPoolFileWatch:
    """Comprehensive file watch tests."""
    
    @pytest.mark.asyncio
    async def test_file_watch_detects_single_file(self, pool, watch_dir):
        """Test single file detection"""
        # Start pool
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(0.5)  # Let watchers start
        
        # Drop file
        test_file = TestFileGenerator.generate_csv_file(
            watch_dir / "test.csv"
        )
        
        # Wait for queuing
        await asyncio.sleep(1.0)
        
        # Verify queued
        assert pool._queue.size >= 1
        
        # Cleanup
        pool.stop()
        await task
    
    @pytest.mark.asyncio
    async def test_file_watch_detects_100_files(self, pool, watch_dir):
        """Test batch file detection"""
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(0.5)
        
        # Drop 100 files
        files = TestFileGenerator.generate_batch(
            watch_dir,
            file_type='csv',
            count=100
        )
        
        # Wait for queuing
        await asyncio.sleep(5.0)
        
        # Verify all queued
        assert pool._queue.size >= 100
        
        pool.stop()
        await task
    
    @pytest.mark.asyncio
    async def test_priority_queue_ordering(self, pool):
        """Test files processed by priority"""
        # Queue 3 files with different priorities
        item_low = AsyncConversionItem(Path("low.csv"), mock_converter, priority=10)
        item_high = AsyncConversionItem(Path("high.csv"), mock_converter, priority=1)
        item_med = AsyncConversionItem(Path("med.csv"), mock_converter, priority=5)
        
        pool._queue.put_nowait(data=item_low, priority=10)
        pool._queue.put_nowait(data=item_high, priority=1)
        pool._queue.put_nowait(data=item_med, priority=5)
        
        # Dequeue
        first = await pool._queue.get()
        second = await pool._queue.get()
        third = await pool._queue.get()
        
        # Verify order
        assert first.data.priority == 1  # High priority first
        assert second.data.priority == 5
        assert third.data.priority == 10
    
    @pytest.mark.asyncio
    async def test_semaphore_limits_concurrent_conversions(self, pool, watch_dir):
        """Test max 10 concurrent conversions"""
        # Create slow converter (delays in convert())
        slow_converter = SlowConverterMock(delay=2.0)
        pool._converters = [slow_converter]
        
        # Queue 20 files
        files = TestFileGenerator.generate_batch(watch_dir, 'csv', count=20)
        for f in files:
            pool._on_file_created(f, slow_converter)
        
        # Start processing
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(0.5)
        
        # Check active count (should be ≤ 10)
        active = pool._get_active_conversion_count()
        assert active <= 10
        
        pool.stop()
        await task
```

**Success Criteria:**
- ✅ 20+ tests for AsyncConverterPool
- ✅ Coverage >85% for async_converter_pool.py
- ✅ File watch, queue, semaphore, post-processing all tested

---

### Task 1.4: Fix CRITICAL Issue #10 - PostProcessing Order ⏱️ 6 hours

**Priority:** 🔴 CRITICAL (BLOCKER)

**Problem:** Source file deleted before archiving opportunity (data loss risk)

**Solution:** Change pipeline order

**Files to Modify:**
- `src/pywats_client/service/async_converter_pool.py`

**Current Flow:**
```python
async def _process_item(self, item):
    result = await converter.convert(source, context)
    if result.success:
        await self._submit_report(result.report)  # ← Submit first
        await self._post_process(item, result)    # ← Delete after
```

**New Flow:**
```python
async def _process_item(self, item):
    result = await converter.convert(source, context)
    if result.success:
        # CHANGE: Post-process BEFORE submission
        # This allows archive interceptor to run first
        await self._post_process(item, result)
        await self._submit_report(result.report)
```

**Rationale:**
- Archive system (future) can intercept post-processing
- Source preserved even if submission fails
- More logical: "finish local work before network call"

**Tests to Add:**
```python
async def test_post_processing_happens_before_submission(self, pool):
    """Verify post-processing runs before network submission"""
    submission_called = False
    postprocess_called = False
    
    async def mock_submit(report):
        nonlocal submission_called
        assert postprocess_called == True  # Must happen first!
        submission_called = True
    
    async def mock_postprocess(item, result):
        nonlocal postprocess_called
        postprocess_called = True
    
    pool._submit_report = mock_submit
    pool._post_process = mock_postprocess
    
    await pool._process_item(test_item)
    
    assert postprocess_called and submission_called
```

**Success Criteria:**
- ✅ Post-processing happens BEFORE submission
- ✅ Test validates new order
- ✅ No regressions (all existing tests pass)
- ✅ Documentation updated

---

### Task 1.5: Unit Tests - AsyncPendingQueue ⏱️ 4 hours

**Priority:** HIGH

**Create:** `tests/client/service/test_async_pending_queue_comprehensive.py`

**Tests to Write:**

```python
class TestAsyncPendingQueue:
    """Comprehensive pending queue tests."""
    
    @pytest.mark.asyncio
    async def test_detects_queued_file(self, queue, reports_dir):
        """Test .queued file detection"""
        # Start queue
        task = asyncio.create_task(queue.run())
        await asyncio.sleep(0.5)
        
        # Create .queued file
        queued_file = reports_dir / "test_report.json.queued"
        queued_file.write_text('{"test": "data"}')
        
        # Wait for detection
        await asyncio.sleep(1.0)
        
        # Verify detected
        assert queue.get_pending_count() >= 1
        
        queue.stop()
        await task
    
    @pytest.mark.asyncio
    async def test_submits_all_pending_concurrently(self, queue, reports_dir):
        """Test concurrent submission with semaphore limit"""
        # Create 20 .queued files
        for i in range(20):
            queued = reports_dir / f"report_{i}.json.queued"
            queued.write_text(f'{{"id": {i}}}')
        
        # Submit all
        await queue.submit_all_pending()
        
        # Verify all submitted (none left)
        assert queue.get_pending_count() == 0
    
    @pytest.mark.asyncio
    async def test_retry_on_network_failure(self, queue, reports_dir, mock_client):
        """Test retry behavior on submission failure"""
        # Mock client to fail once, then succeed
        mock_client.submit_uut_report = Mock(
            side_effect=[Exception("Network error"), "report_id_123"]
        )
        
        queued = reports_dir / "report.json.queued"
        queued.write_text('{"test": "data"}')
        
        # First submission fails
        with pytest.raises(Exception):
            await queue._submit_queued_file(queued)
        
        # File should still exist
        assert queued.exists()
        
        # Second submission succeeds
        await queue._submit_queued_file(queued)
        
        # File should be deleted
        assert not queued.exists()
```

**Success Criteria:**
- ✅ 10+ tests for AsyncPendingQueue
- ✅ Coverage >80% for async_pending_queue.py
- ✅ File watch, submission, retry all tested

---

## Week 2: Integration + Stress Testing

### Task 2.1: End-to-End Integration Tests ⏱️ 8 hours

**Priority:** CRITICAL

**Create:** `tests/integration/test_converter_pipeline_e2e.py`

**Tests to Write:**

```python
@pytest.mark.integration
class TestConverterPipelineE2E:
    """End-to-end converter pipeline tests."""
    
    @pytest.mark.asyncio
    async def test_e2e_successful_conversion(self, integration_setup):
        """
        Test complete flow: file arrives → queued → converted → submitted → moved
        """
        pool, watch_dir, done_dir, client_mock = integration_setup
        
        # Drop file in watch folder
        test_file = TestFileGenerator.generate_csv_file(
            watch_dir / "test.csv",
            rows=50
        )
        
        # Start pool
        task = asyncio.create_task(pool.run())
        
        # Wait for processing (max 10 seconds)
        for _ in range(20):
            await asyncio.sleep(0.5)
            if not test_file.exists():
                break
        
        # Verify file no longer in watch folder
        assert not test_file.exists()
        
        # Verify file moved to Done folder
        done_file = done_dir / "test.csv"
        assert done_file.exists()
        
        # Verify report submitted
        assert client_mock.submit_uut_report.called
        
        pool.stop()
        await task
    
    @pytest.mark.asyncio
    async def test_e2e_conversion_failure(self, integration_setup):
        """Test flow when conversion fails"""
        pool, watch_dir, error_dir, _ = integration_setup
        
        # Drop corrupted file
        bad_file = TestFileGenerator.generate_csv_file(
            watch_dir / "bad.csv",
            corrupt=True
        )
        
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(5.0)
        
        # Verify file moved to Error folder
        error_file = error_dir / "bad.csv"
        assert error_file.exists() or not bad_file.exists()
        
        pool.stop()
        await task
    
    @pytest.mark.asyncio
    async def test_e2e_network_failure_retry(self, integration_setup):
        """Test retry when WATS server is down"""
        pool, watch_dir, pending_dir, client_mock = integration_setup
        
        # Mock network failure
        client_mock.submit_uut_report.side_effect = Exception("Network error")
        
        test_file = TestFileGenerator.generate_csv_file(
            watch_dir / "test.csv"
        )
        
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(5.0)
        
        # Verify .queued file created for retry
        queued_files = list(pending_dir.glob("*.queued"))
        assert len(queued_files) > 0
        
        pool.stop()
        await task
```

**Success Criteria:**
- ✅ 5+ end-to-end tests
- ✅ All pipeline stages tested
- ✅ Error paths validated
- ✅ Tests complete in <30 seconds

---

### Task 2.2: Stress Test - 1000 File Batch ⏱️ 6 hours

**Priority:** HIGH

**Create:** `tests/stress/test_file_watch_stress.py`

**Tests to Write:**

```python
@pytest.mark.stress
class TestFileWatchStress:
    """Stress tests for file watching."""
    
    @pytest.mark.asyncio
    @pytest.mark.timeout(60)  # Must complete in 60 seconds
    async def test_1000_files_simultaneous_drop(self, pool, watch_dir):
        """
        Drop 1000 files at once, verify none missed.
        
        SUCCESS CRITERIA:
        - All 1000 files queued
        - No files missed
        - Processing completes in <60 seconds
        """
        # Generate 1000 files
        files = TestFileGenerator.generate_batch(
            watch_dir,
            file_type='csv',
            count=1000,
            rows=10  # Small files for speed
        )
        
        assert len(files) == 1000
        
        # Start pool
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(1.0)  # Let watchers start
        
        # Track queued count
        initial_size = pool._queue.size
        
        # Wait for all files to be processed (max 60 seconds)
        start_time = time.time()
        while pool._queue.size < 1000 and (time.time() - start_time) < 60:
            await asyncio.sleep(0.5)
        
        elapsed = time.time() - start_time
        
        # Verify all files queued
        assert pool._queue.size >= 1000, f"Only {pool._queue.size} files queued"
        
        # Log performance
        print(f"\n✅ 1000 files queued in {elapsed:.2f} seconds")
        print(f"   Throughput: {1000 / elapsed:.0f} files/second")
        
        pool.stop()
        await task
    
    @pytest.mark.asyncio
    @pytest.mark.timeout(300)  # 5 minutes max
    async def test_sustained_file_arrival(self, pool, watch_dir):
        """
        Simulate sustained file arrival (10 files/second for 1 minute).
        
        SUCCESS CRITERIA:
        - No files missed
        - Queue doesn't grow unbounded
        - Memory stable
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(1.0)
        
        files_created = 0
        duration = 60  # seconds
        rate = 10  # files/second
        
        for _ in range(duration):
            # Create 10 files per second
            batch = TestFileGenerator.generate_batch(
                watch_dir,
                file_type='csv',
                count=rate,
                rows=10
            )
            files_created += len(batch)
            await asyncio.sleep(1.0)
        
        # Wait for queue to drain
        await asyncio.sleep(10.0)
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_growth = final_memory - initial_memory
        
        # Verify
        assert pool._queue.size < 100, "Queue grew unbounded!"
        assert memory_growth < 100, f"Memory grew {memory_growth:.1f} MB!"
        
        print(f"\n✅ Sustained: {files_created} files in {duration}s")
        print(f"   Memory growth: {memory_growth:.1f} MB")
        
        pool.stop()
        await task
```

**Success Criteria:**
- ✅ 1000 files processed without misses
- ✅ Performance baseline established (files/second)
- ✅ Memory growth <100 MB
- ✅ No crashes or hangs

---

### Task 2.3: Performance Benchmarks ⏱️ 4 hours

**Priority:** MEDIUM

**Create:** `tests/performance/test_benchmarks.py`

**Use:** `pytest-benchmark` plugin

**Benchmarks to Create:**

```python
@pytest.mark.benchmark
class TestPerformanceBenchmarks:
    """Performance benchmarks for critical paths."""
    
    def test_benchmark_queue_put(self, benchmark):
        """Benchmark queue put operation"""
        queue = PersistentQueue(temp_dir)
        item = AsyncConversionItem(Path("test.csv"), mock_converter)
        
        result = benchmark(queue.put_nowait, data=item, priority=5)
        
        # Target: <10ms per put
        assert benchmark.stats['mean'] < 0.01
    
    def test_benchmark_queue_get(self, benchmark):
        """Benchmark queue get operation"""
        queue = PersistentQueue(temp_dir)
        # Pre-populate
        for i in range(100):
            queue.put_nowait(data=test_item, priority=5)
        
        result = benchmark(queue.get_nowait)
        
        # Target: <5ms per get
        assert benchmark.stats['mean'] < 0.005
    
    @pytest.mark.asyncio
    async def test_benchmark_file_conversion(self, benchmark):
        """Benchmark single file conversion"""
        csv_file = TestFileGenerator.generate_csv_file(
            temp_dir / "bench.csv",
            rows=100
        )
        
        converter = CSVConverter()
        context = ConverterContext.from_config(converter.config)
        source = ConverterSource(file_path=csv_file)
        
        async def convert():
            return await converter.convert(source, context)
        
        result = benchmark(asyncio.run, convert())
        
        # Target: <1 second for 100-row CSV
        assert benchmark.stats['mean'] < 1.0
```

**Success Criteria:**
- ✅ Baselines established for queue ops, conversion, submission
- ✅ Benchmarks run in CI/CD
- ✅ Performance targets documented

---

## Week 3: Error Injection + Fixes + Documentation

### Task 3.1: Error Injection Tests ⏱️ 8 hours

**Priority:** HIGH

**Create:** `tests/integration/test_error_scenarios.py`

**Tests to Write:**

```python
@pytest.mark.integration
class TestErrorScenarios:
    """Test error handling and recovery."""
    
    @pytest.mark.asyncio
    async def test_file_locked_by_another_process(self, pool, watch_dir):
        """Test converter handles locked files gracefully"""
        # Create and lock file
        test_file = watch_dir / "locked.csv"
        TestFileGenerator.generate_csv_file(test_file)
        
        # Lock file (platform-specific)
        with open(test_file, 'r') as lock:
            # Start pool while file is locked
            task = asyncio.create_task(pool.run())
            await asyncio.sleep(5.0)
            
            # File should move to error or retry
            # (depends on implementation)
            
            pool.stop()
            await task
    
    @pytest.mark.asyncio
    async def test_disk_full_during_queue_persistence(self, pool, watch_dir):
        """Test queue handles disk full gracefully"""
        # Mock disk full error
        original_write = Path.write_text
        
        def mock_write_disk_full(self, content):
            raise OSError("[Errno 28] No space left on device")
        
        Path.write_text = mock_write_disk_full
        
        try:
            test_file = TestFileGenerator.generate_csv_file(
                watch_dir / "test.csv"
            )
            
            pool._on_file_created(test_file, mock_converter)
            
            # Should handle gracefully (log error, not crash)
            await asyncio.sleep(1.0)
            
        finally:
            Path.write_text = original_write
    
    @pytest.mark.asyncio
    async def test_wats_server_timeout(self, pool, watch_dir, client_mock):
        """Test submission timeout handling"""
        import asyncio
        
        async def slow_submit(report):
            await asyncio.sleep(60)  # 60 second delay
            return "report_id"
        
        client_mock.submit_uut_report = slow_submit
        
        test_file = TestFileGenerator.generate_csv_file(
            watch_dir / "test.csv"
        )
        
        task = asyncio.create_task(pool.run())
        
        # Should timeout and queue for retry
        await asyncio.sleep(10.0)
        
        pool.stop()
        await task
    
    @pytest.mark.asyncio
    async def test_invalid_converter_module_path(self, config):
        """Test error when converter module doesn't exist"""
        config.module_path = "non.existent.Converter"
        
        pool = AsyncConverterPool(config)
        
        # Should log error, not crash
        await pool._load_converters()
        
        # Verify converter not loaded
        assert len(pool._converters) == 0
    
    @pytest.mark.asyncio
    async def test_done_folder_deleted_mid_operation(self, pool, watch_dir, done_dir):
        """Test recovery when Done folder is deleted"""
        test_file = TestFileGenerator.generate_csv_file(
            watch_dir / "test.csv"
        )
        
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(1.0)
        
        # Delete Done folder
        import shutil
        shutil.rmtree(done_dir)
        
        # Wait for post-processing
        await asyncio.sleep(5.0)
        
        # Should either recreate folder OR move to error
        assert done_dir.exists() or (watch_dir / "Error" / "test.csv").exists()
        
        pool.stop()
        await task
```

**Success Criteria:**
- ✅ 10+ error scenarios tested
- ✅ All errors handled gracefully (no crashes)
- ✅ Clear error messages logged
- ✅ Recovery mechanisms validated

---

### Task 3.2: Fix Identified Issues ⏱️ 12 hours

**Priority:** HIGH

**Issues to Fix:**

**1. Add Queue Size Limits (Issue #5)**
```python
# src/pywats_client/core/config.py
@dataclass
class ClientConfig:
    # ...
    queue_max_size: int = 10000  # NEW: Prevent unbounded growth
    queue_reject_on_full: bool = False  # NEW: Reject or block
```

**2. Improve Error Messages (Issue #14)**
```python
# src/pywats_client/service/async_converter_pool.py
try:
    module = importlib.import_module(module_path)
except ModuleNotFoundError as e:
    logger.error(
        f"❌ Converter module not found: {module_path}\n"
        f"   Error: {e}\n"
        f"   Hint: Check module_path in converter config\n"
        f"   Example: 'my_converters.CSVConverter'"
    )
```

**3. Add Structured Logging (Issue #8)**
```python
# Add context to all logs
logger.info(
    "File queued for conversion",
    extra={
        'file': str(file_path),
        'converter': converter.name,
        'priority': priority,
        'queue_size': self._queue.size
    }
)
```

**4. Ensure Folder Recreation (Issue #11)**
```python
async def _post_process_file(self, item, result):
    if result.post_action == PostProcessAction.MOVE:
        # Ensure Done folder exists
        done_folder = Path(self._config.done_folder)
        done_folder.mkdir(parents=True, exist_ok=True)
        
        # Move file
        await self._move_file(item.file_path, done_folder)
```

**Success Criteria:**
- ✅ All CRITICAL and HIGH priority issues fixed
- ✅ Tests pass after fixes
- ✅ No regressions

---

### Task 3.3: 24-Hour Stress Test ⏱️ 2 hours (setup) + 24 hours (run)

**Priority:** HIGH

**Create:** `tests/stress/test_24hour_stability.py`

**Test Setup:**

```python
@pytest.mark.stress
@pytest.mark.slow
class Test24HourStability:
    """Long-running stability test."""
    
    @pytest.mark.timeout(86400 + 600)  # 24 hours + 10 min buffer
    async def test_24hour_conversion_stability(self, pool, watch_dir):
        """
        Run converter for 24 hours, monitor stability.
        
        PROFILE:
        - 1 file every 10 seconds
        - 8,640 total files
        - Monitor: memory, CPU, file handles
        
        SUCCESS CRITERIA:
        - All files converted
        - Memory growth <1% per hour (<24% total)
        - No file handle leaks (<100 handles)
        - No crashes
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Initial metrics
        initial_memory = process.memory_info().rss / 1024 / 1024
        initial_handles = process.num_fds() if hasattr(process, 'num_fds') else 0
        
        metrics_log = []
        
        task = asyncio.create_task(pool.run())
        await asyncio.sleep(5.0)
        
        duration_hours = 24
        interval_seconds = 10
        total_files = duration_hours * 3600 // interval_seconds
        
        for i in range(total_files):
            # Create file
            test_file = TestFileGenerator.generate_csv_file(
                watch_dir / f"file_{i:06d}.csv",
                rows=50
            )
            
            # Wait
            await asyncio.sleep(interval_seconds)
            
            # Log metrics every hour
            if i % 360 == 0:  # Every hour
                current_memory = process.memory_info().rss / 1024 / 1024
                current_handles = process.num_fds() if hasattr(process, 'num_fds') else 0
                cpu_percent = process.cpu_percent()
                
                metrics = {
                    'hour': i // 360,
                    'files_processed': i,
                    'memory_mb': current_memory,
                    'memory_delta_mb': current_memory - initial_memory,
                    'file_handles': current_handles,
                    'handle_delta': current_handles - initial_handles,
                    'cpu_percent': cpu_percent,
                    'queue_size': pool._queue.size
                }
                metrics_log.append(metrics)
                
                print(f"\nHour {metrics['hour']}: {metrics}")
        
        # Final metrics
        final_memory = process.memory_info().rss / 1024 / 1024
        final_handles = process.num_fds() if hasattr(process, 'num_fds') else 0
        
        memory_growth_pct = ((final_memory - initial_memory) / initial_memory) * 100
        handle_growth = final_handles - initial_handles
        
        # Verify stability
        assert memory_growth_pct < 24, f"Memory grew {memory_growth_pct:.1f}%!"
        assert handle_growth < 100, f"File handles grew by {handle_growth}!"
        assert pool._queue.size < 50, f"Queue backed up: {pool._queue.size}!"
        
        # Save metrics
        import json
        with open('24hour_stability_metrics.json', 'w') as f:
            json.dump(metrics_log, f, indent=2)
        
        print(f"\n✅ 24-Hour Test Complete")
        print(f"   Files: {total_files}")
        print(f"   Memory growth: {memory_growth_pct:.1f}%")
        print(f"   Handle growth: {handle_growth}")
        
        pool.stop()
        await task
```

**Run Command:**
```bash
pytest tests/stress/test_24hour_stability.py -v -s --timeout=87000
```

**Success Criteria:**
- ✅ Test completes without crashes
- ✅ Memory growth <24%
- ✅ File handle growth <100
- ✅ All files processed
- ✅ Metrics logged for analysis

---

### Task 3.4: Documentation ⏱️ 6 hours

**Priority:** MEDIUM

**Documents to Create:**

**1. Converter Behavior Specification**

Create: `docs/guides/converter-behavior-specification.md`

Content:
- Expected file watch behavior
- Queue guarantees (FIFO within priority)
- Error handling standards
- Post-processing order
- Performance expectations (throughput, latency)

**2. Testing Guide**

Create: `docs/guides/converter-testing-guide.md`

Content:
- How to run test suite
- How to add new tests
- Test file generators usage
- Stress test instructions
- Performance benchmark interpretation

**3. Update Architecture Docs**

Update: `docs/internal_documentation/converter_architecture.md`

Content:
- Current architecture diagram
- Component responsibilities
- Integration points
- Known limitations
- Performance characteristics

**Success Criteria:**
- ✅ All documents created
- ✅ Clear, actionable guidance
- ✅ Examples provided
- ✅ Reviewed by team

---

### Task 3.5: CHANGELOG Update ⏱️ 1 hour

**Priority:** LOW

**Update:** `CHANGELOG.md`

**Content:**

```markdown
## [Unreleased]

### Added
- **Converter Testing Suite**: 50+ new tests for converter architecture
  - Unit tests for FileConverter, FolderConverter base classes
  - Integration tests for end-to-end conversion pipeline
  - Stress tests (1000+ file batches, 24-hour stability)
  - Error injection tests (network failures, disk full, file locks)
  - Performance benchmarks (throughput, latency, resource usage)
  - Test file generators for CSV, XML, TXT formats
  - Tests: 416 → 466+ total (50 new converter tests)

### Changed
- **Post-processing order**: Now runs BEFORE report submission (enables future archiving)
  - Rationale: Prevents data loss if PostProcessAction.DELETE used
  - Breaking Change: No (functionally equivalent for current use cases)
  - File: `src/pywats_client/service/async_converter_pool.py`

### Improved
- **Error messages**: Clearer, actionable errors for common failures
  - Invalid converter module paths include hint with example
  - File lock errors specify retry behavior
  - Disk full errors include remediation steps
- **Structured logging**: All converter logs include file, converter name, priority
- **Folder resilience**: Done/Error/Pending folders recreated if deleted
- **Queue limits**: Added `queue_max_size` config to prevent unbounded growth

### Fixed
- **Queue size limits**: Prevent memory exhaustion in high-load scenarios
- **Folder recreation**: Done/Error folders now recreated if deleted mid-operation
- **Thread safety**: Validated all watchdog thread boundaries use thread-safe operations

### Performance
- **Baselines established**:
  - Throughput: 100+ files/minute (single converter)
  - Latency: <7 seconds (file arrival → submission)
  - Queue operations: <10ms put, <5ms get
  - Memory stability: <1% growth per hour
  - File handles: <20 stable count
- **24-hour stress test**: 8,640 files processed without leaks or crashes

### Documentation
- **Converter Behavior Specification** - Defines expected behavior and guarantees
- **Converter Testing Guide** - How to run tests and add new ones
- **Architecture Documentation** - Updated with current implementation details
```

---

## Test Data Strategy (Detailed)

### Synthetic Test Files (PRIMARY)

**Advantages:**
- ✅ **Scale:** Generate 1,000+ files instantly for stress tests
- ✅ **Reproducibility:** Same files every test run (deterministic)
- ✅ **Parameterization:** Control size, corruption, edge cases
- ✅ **No PII:** No sensitive customer data
- ✅ **Fast:** Generated in milliseconds
- ✅ **Version control:** Generators checked into git

**Implementation:**
```python
# tests/fixtures/test_file_generators.py
TestFileGenerator.generate_batch(
    output_dir=temp_dir,
    file_type='csv',
    count=1000,
    rows=50,
    corrupt_probability=0.01  # 1% corrupt files
)
```

**Usage Pattern:**
```python
@pytest.fixture
def test_csv_files(tmp_path):
    """Generate 100 test CSV files"""
    return TestFileGenerator.generate_batch(
        tmp_path,
        'csv',
        count=100,
        rows=random.randint(10, 1000)  # Varying sizes
    )

def test_converter_handles_batch(test_csv_files):
    assert len(test_csv_files) == 100
    # Use in test...
```

### Real Sample Files (SECONDARY)

**Advantages:**
- ✅ **Realistic:** Actual production data patterns
- ✅ **Edge cases:** Captures real-world anomalies you didn't anticipate
- ✅ **Validation:** Confirms converter handles actual files

**Limitations:**
- ⚠️ **Scale:** Hard to collect 1,000+ files
- ⚠️ **PII:** May contain sensitive data (sanitize first!)
- ⚠️ **Static:** Doesn't change without manual update

**Recommendation:**
Create: `tests/fixtures/sample_files/` directory

```
tests/fixtures/sample_files/
├── csv/
│   ├── basic_10rows.csv          # Small baseline
│   ├── large_10000rows.csv       # Large file test
│   ├── with_unicode.csv          # Unicode handling
│   ├── missing_header.csv        # Edge case
│   └── corrupt_middle_row.csv    # Error case
├── xml/
│   ├── valid_uut_report.xml
│   ├── with_comments.xml
│   ├── malformed_tag.xml
│   └── huge_10mb.xml
└── README.md                     # Documents each file's purpose
```

**Usage:**
```python
@pytest.fixture
def sample_csv_files():
    """Real sample files for validation"""
    samples_dir = Path(__file__).parent / "sample_files" / "csv"
    return list(samples_dir.glob("*.csv"))

def test_converter_validates_against_samples(sample_csv_files):
    """Ensure converter handles all real samples"""
    for csv_file in sample_csv_files:
        result = converter.convert(csv_file)
        assert result.success, f"Failed on {csv_file.name}"
```

### Hybrid Strategy

**For Each Test Type:**

| Test Type | Primary Data | Secondary Data |
|-----------|--------------|----------------|
| **Unit Tests** | 100% Synthetic | 0% Real |
| **Integration Tests** | 80% Synthetic | 20% Real (validation) |
| **Stress Tests** | 100% Synthetic | 0% Real (need 1000+) |
| **Validation Tests** | 0% Synthetic | 100% Real (verify actual files work) |
| **Error Injection** | 100% Synthetic | 0% Real (need controlled corruption) |

**Recommendation:**
1. **Start with generators** (Task 1.1) - Build comprehensive synthetic generators
2. **Add 5-10 real samples per format** - Manual collection/sanitization
3. **Use synthetic for 90% of tests** - Speed, scale, reproducibility
4. **Use real samples for final validation** - Confidence in production readiness

---

## Success Criteria Summary

### Code Quality
- ✅ Test coverage >90% for converter domain
- ✅ All tests passing (100% pass rate)
- ✅ No skipped tests without justification
- ✅ Type hints on all new code
- ✅ Docstrings on all public APIs

### Reliability
- ✅ 1000-file stress test passes (no files missed)
- ✅ 24-hour stability test passes (no leaks)
- ✅ All error scenarios handled gracefully
- ✅ No crashes under any tested condition
- ✅ Clear, actionable error messages

### Performance
- ✅ Throughput >100 files/minute
- ✅ Latency <7 seconds (arrival → submission)
- ✅ Memory growth <1% per hour
- ✅ File handle count stable (<100)
- ✅ Queue operations <10ms

### Documentation
- ✅ Behavior specification complete
- ✅ Testing guide complete
- ✅ Architecture docs updated
- ✅ CHANGELOG updated
- ✅ All public APIs documented

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Tests take too long | Parallelize with pytest-xdist, optimize generators |
| Flaky tests | Use deterministic data, mock time-sensitive operations |
| Resource leaks hard to detect | Use memory_profiler, run 24-hour test on dedicated machine |
| Real files contain PII | Use only synthetic files OR sanitize real files first |
| Test data becomes outdated | Version control generators, regenerate on demand |

---

## Timeline Summary

| Week | Focus | Deliverables |
|------|-------|--------------|
| **Week 1** | Unit tests + critical fixes | 30+ unit tests, Issue #10 fixed, generators created |
| **Week 2** | Integration + stress | 10+ integration tests, 1000-file stress test, benchmarks |
| **Week 3** | Error injection + docs | 10+ error tests, 24-hour test, 3 docs, CHANGELOG |

**Total:** 50+ new tests, 6 critical fixes, 4 documents, performance baselines

---

## Next Steps

1. ✅ Review this implementation plan
2. ⏳ Create progress tracking (03_PROGRESS.md, 04_TODO.md)
3. ⏳ Set up test infrastructure (pytest plugins, fixtures)
4. ⏳ **Start with Task 1.1: Create Test File Generators** (CRITICAL - blocks all other work)
5. ⏳ Execute weekly goals sequentially

---

**Last Updated:** February 13, 2026  
**Estimated Completion:** March 6, 2026 (3 weeks)  
**Owner:** Development Team

