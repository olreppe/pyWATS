# Task Checklist: Converter Startup File Recovery

**Created:** February 14, 2026, 14:30  
**Last Updated:** February 14, 2026, 14:30

---

## Legend

- ✅ Completed
- 🚧 In Progress
- ⏸️ Blocked/Waiting
- ✗ Not Started
- ❌ Cancelled/Skipped

---

## Phase 1: Core Implementation

### 1.1 Instance Variables
- ✗ Add `_startup_scan_files: Set[Path]` to `__init__`
- ✗ Add `_startup_scan_complete: bool` to `__init__`
- ✗ Add `_startup_scan_enabled: bool` to `__init__`
- ✗ Verify no breaking changes in constructor signature

### 1.2 Scan Method Implementation
- ✗ Create `_scan_existing_files()` method
- ✗ Implement directory scanning logic (glob patterns)
- ✗ Implement file sorting (mtime, oldest first)
- ✗ Implement queue logic (put_nowait with priority)
- ✗ Add `_startup_scan_files` tracking
- ✗ Add statistics collection (scanned, queued, skipped, errors)
- ✗ Add logging (info on start/complete, debug per file)
- ✗ Schedule `_clear_startup_scan_set()` cleanup task

### 1.3 Helper Methods
- ✗ Create `_is_file_queued()` method (check .queued marker)
- ✗ Create `_clear_startup_scan_set()` method (5s delay + clear)
- ✗ Add logging for cleanup completion

### 1.4 Deduplication in FileWatcher
- ✗ Update `_on_file_created()` with deduplication check
- ✗ Test: Skip if file in `_startup_scan_files` and scan not complete
- ✗ Add debug logging for skipped files

### 1.5 Update Startup Sequence
- ✗ Update `run()` method: call `_scan_existing_files()` before `_start_watchers()`
- ✗ Capture and log scan statistics
- ✗ Verify sequence: load → scan → watch → process

---

## Phase 2: Configuration Support

### 2.1 Config Schema
- ✗ Add `enable_startup_scan: bool` to ConverterConfig
- ✗ Add `startup_scan_timeout: int` to ConverterConfig
- ✗ Add `startup_scan_max_files: int` to ConverterConfig
- ✗ Set defaults (true, 30, 0)
- ✗ Update ConverterConfig docstrings

### 2.2 Config Loading
- ✗ Load `enable_startup_scan` in `__init__`
- ✗ Load `startup_scan_timeout` in `__init__`
- ✗ Load `startup_scan_max_files` in `__init__`
- ✗ Store in instance variables
- ✗ Respect config in `_scan_existing_files()`

### 2.3 Timeout Implementation
- ✗ Add `asyncio.wait_for()` wrapper for scan with timeout
- ✗ Handle TimeoutError gracefully (log warning, continue)
- ✗ Test timeout behavior

### 2.4 Max Files Limit
- ✗ Check file count against `startup_scan_max_files`
- ✗ Stop scanning if limit reached
- ✗ Log warning if limit hit

---

## Phase 3: Testing

### 3.1 Unit Tests (8 tests)
- ✗ `test_scan_queues_all_existing_files` - Basic functionality
- ✗ `test_scan_respects_extension_filter` - Extension matching
- ✗ `test_scan_skips_queued_files` - .queued marker check
- ✗ `test_scan_deduplication_watchdog_event` - Race condition prevention
- ✗ `test_scan_sorted_by_mtime` - FIFO ordering
- ✗ `test_scan_disabled_via_config` - Configuration toggle
- ✗ `test_scan_stats_accurate` - Statistics validation
- ✗ `test_scan_error_handling` - Per-file error recovery

### 3.2 Integration Tests (4 tests)
- ✗ `test_end_to_end_startup_recovery` - Full workflow
- ✗ `test_race_file_during_scan` - File dropped mid-scan
- ✗ `test_crash_before_queue_recovery` - Crash simulation
- ✗ `test_large_backlog_performance` - 100 files <5s

### 3.3 Performance Tests (3 tests)
- ✗ `test_scan_100_files_under_5s` - Typical load
- ✗ `test_scan_1000_files_memory_overhead` - Large backlog
- ✗ `test_dedup_set_cleared_after_ttl` - Memory leak check

### 3.4 Test Execution
- ✗ Run all unit tests: `pytest tests/client/service/test_async_converter_pool_startup_scan.py`
- ✗ Run integration tests: `pytest tests/integration/test_converter_startup_recovery.py`
- ✗ Run performance tests: `pytest tests/performance/test_startup_scan_performance.py`
- ✗ Verify all 15 new tests passing
- ✗ Verify existing 416 tests still passing

---

## Phase 4: Documentation

### 4.1 Architecture Guide
- ✗ Add "Startup File Recovery" section to converter-architecture.md
- ✗ Explain problem statement
- ✗ Document scan process flow
- ✗ Document deduplication mechanism
- ✗ Add configuration examples
- ✗ Add performance notes

### 4.2 Configuration Reference
- ✗ Document `enable_startup_scan` option
- ✗ Document `startup_scan_timeout` option
- ✗ Document `startup_scan_max_files` option
- ✗ Add YAML examples
- ✗ Add use case recommendations

### 4.3 Troubleshooting Guide
- ✗ Add "Files Not Processed on Startup" troubleshooting entry
- ✗ Explain how to check if startup scan is enabled
- ✗ Explain how to check scan logs
- ✗ Add manual recovery steps if scan disabled

### 4.4 CHANGELOG
- ✗ Add entry under `[Unreleased]` → `Added`
- ✗ Describe feature and benefits
- ✗ List configuration options
- ✗ Reference documentation
- ✗ Note test coverage

---

## Phase 5: Code Review & Finalization

### 5.1 Self-Review
- ✗ Review all code changes for clarity
- ✗ Verify all logging is appropriate (info/debug levels)
- ✗ Check error handling is comprehensive
- ✗ Verify no performance regressions
- ✗ Check thread safety (watchdog interactions)

### 5.2 Quality Checks
- ✗ Run mypy type checking: `mypy src/pywats_client/service/async_converter_pool.py`
- ✗ Run flake8 linting: `flake8 src/pywats_client/service/async_converter_pool.py`
- ✗ Check test coverage: `pytest --cov=src/pywats_client/service/async_converter_pool`
- ✗ Verify no new errors in `get_errors()`

### 5.3 Manual Testing
- ✗ Drop 10 files in watch directory
- ✗ Stop AsyncConverterPool
- ✗ Restart AsyncConverterPool
- ✗ Verify all 10 files processed
- ✗ Check logs for scan statistics
- ✗ Verify no duplicate processing

### 5.4 Performance Validation
- ✗ Create 100 test files
- ✗ Measure startup scan time
- ✗ Verify <5s completion
- ✗ Check memory usage (before/after scan)

### 5.5 Documentation Review
- ✗ Proofread all documentation changes
- ✗ Verify examples are accurate and runnable
- ✗ Check cross-references are correct
- ✗ Verify CHANGELOG entry is complete

---

## Completion Criteria

- ✗ All 15 new tests passing
- ✗ All 416 existing tests passing
- ✗ Mypy errors not increased (<20 total)
- ✗ Flake8 clean
- ✗ Documentation complete (4 files updated)
- ✗ CHANGELOG updated
- ✗ Performance targets met (<5s for 100 files)
- ✗ Manual testing successful
- ✗ Code review completed
- ✗ All phases complete (1-5)

---

## Progress Summary

**Total Tasks**: 78  
**Completed**: 0 (0%)  
**In Progress**: 0 (0%)  
**Remaining**: 78 (100%)

**Estimated Time Remaining**: 12.5 hours

---

## Notes

- Priority order: Phase 1 → 3 → 2 → 4 → 5 (implement core, test, then config/docs)
- Can parallelize: Unit tests while implementing (TDD approach)
- Critical path: Phase 1.2 (_scan_existing_files method) - most complex
- Risk area: Race condition testing (Phase 3.2) - requires careful test design
