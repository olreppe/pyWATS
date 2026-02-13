# Technical Analysis: Converter Architecture Stabilization

**Created:** February 13, 2026  
**Status:** Analysis Complete  
**Target:** Production-grade reliability for v1.0 release

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Architecture](#current-architecture)
3. [Critical Components Analysis](#critical-components-analysis)
4. [Known Issues & "Loose Ends"](#known-issues--loose-ends)
5. [Testing Gaps](#testing-gaps)
6. [Risk Assessment](#risk-assessment)
7. [Testing Strategy](#testing-strategy)
8. [Performance Baseline](#performance-baseline)
9. [Technical Debt](#technical-debt)
10. [Recommendations](#recommendations)

---

## Executive Summary

### Current State
The converter architecture (`src/pywats_client/converters/`, `src/pywats_client/service/`) provides file-based test data conversion capabilities. The architecture is **functionally complete but not comprehensively tested** under production conditions.

### Key Findings
- ✅ **Architecture is sound** - Well-designed async pipeline with proper abstractions
- ❌ **Testing is insufficient** - <30% coverage in converter domain, no stress tests
- ⚠️ **Loose ends exist** - File watch edge cases, queue behavior under load, error recovery
- ⚠️ **Performance unknown** - No benchmarks for throughput, latency, or resource usage
- ❌ **Documentation gaps** - Expected behavior not fully specified

### Critical Risks
1. **File watch misses** - Files arriving too quickly may be missed (C# reference shows skip logic)
2. **Queue contention** - Concurrency behavior under high load not validated
3. **Error recovery** - Incomplete testing of network failures, disk full, invalid files
4. **Post-processing timing** - Reports may be lost if submitted before archiving (design issue)

### Recommendation
**Proceed with stabilization project** before implementing archive system or v1.0 release. Estimated 3 weeks to achieve production-grade reliability.

---

## Current Architecture

### High-Level Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    Converter Pipeline                        │
└─────────────────────────────────────────────────────────────┘

1. FileSystemWatcher (watchdog)
   ├─► Detects file created/modified events
   ├─► Filters by converter pattern (*.xml, *.csv, etc.)
   └─► Triggers _on_file_created()
          │
          ▼
2. Queue System (PersistentQueue)
   ├─► Thread-safe put_nowait() from watchdog thread
   ├─► Priority queue (1=highest, 10=lowest)
   ├─► Persistent storage (survives crashes)
   └─► AsyncQueueAdapter wraps synchronous queue
          │
          ▼
3. Converter Pool (AsyncConverterPool)
   ├─► Dequeues items asynchronously
   ├─► Semaphore limits concurrent conversions (max 10)
   ├─► Loads converter dynamically from module_path
   └─► Executes in sandbox (optional, for untrusted converters)
          │
          ▼
4. Conversion Process
   ├─► validate() - Optional pre-conversion validation
   ├─► convert() - Main conversion logic
   └─► Returns ConverterResult (status, report JSON, post_action)
          │
          ▼
5. Report Submission
   ├─► Submit to WATS server via Client.submit_uut_report()
   ├─► Returns report ID on success
   └─► On failure, queues to AsyncPendingQueue
          │
          ▼
6. Post-Processing (PostProcessAction)
   ├─► DELETE - Remove source file
   ├─► MOVE - Move to Done/ folder
   ├─► ZIP - Compress and move
   └─► KEEP - Leave in place
```

###  Key Components

**1. AsyncConverterPool** (`src/pywats_client/service/async_converter_pool.py`)
- Central orchestrator for conversion pipeline
- Manages file watchers (one per converter)
- Maintains conversion queue with priorities
- Enforces concurrency limits via semaphore
- Handles converter lifecycle (load, execute, cleanup)

**2. Converter Types**
- **FileConverter** - Triggered on individual file creation
- **FolderConverter** - Triggered when folder is "ready" (marker file exists)
- **ScheduledConverter** - Runs on timer/cron schedule

**3. Queue System**
- **PersistentQueue** - Survives process crashes, stores items on disk
- **AsyncPendingQueue** - Manages failed submissions, watches `.queued` files

**4. ConverterContext** (`src/pywats_client/converters/context.py`)
- Provides helpers for folder management (done_path, error_path, pending_path)
- Logging helpers (debug, info, warning, error)
- Factory methods for creating contexts

**5. ConverterConfig** (`src/pywats_client/core/config.py`)
- Defines converter settings (name, module_path, folders, priority, retry, etc.)
- Supports file/folder/scheduled converter types
- Per-converter configuration (not global)

---

## Critical Components Analysis

### 1. File Watching (`_FileEventHandler` + `watchdog.Observer`)

**How It Works:**
```python
# AsyncConverterPool creates one watcher per converter
def _create_watcher(self, converter: 'Converter') -> Optional[Observer]:
    watch_path = converter.watch_path
    handler = _FileEventHandler(self, converter)
    observer = Observer()
    observer.schedule(handler, str(watch_path), recursive=converter.watch_recursive)
    return observer
```

**Event Flow:**
1. Watchdog detects file created/modified
2. `_FileEventHandler.on_created()` called (from watchdog thread)
3. `_on_file_created()` validates pattern match
4. `queue.put_nowait()` adds item to queue (thread-safe)

**Known Issues (from C# reference):**
- **Skip Logic:** C# client had `Monitor.TryEnter(_checkfolderLocker)` to skip if already scanning
- **Throttling:** C# client limited to 10 pending files per converter + 10,000 file scan max
- **Orphan Cleanup:** C# client tracked "orphaned items" not in global queue

**Test Gaps:**
- ❌ What happens if 1000 files arrive simultaneously?
- ❌ What if file is deleted before converter reads it?
- ❌ What if file is locked by another process?
- ❌ Do we miss files during high load?

### 2. Queue Operations (`PersistentQueue` + `AsyncQueueAdapter`)

**How It Works:**
```python
# AsyncConverterPool uses AsyncQueueAdapter
self._queue = AsyncQueueAdapter(
    PersistentQueue(
        storage_dir=storage_dir,
        max_size=config.get('queue_max_size', 10000)
    )
)

# Enqueue from watchdog thread (thread-safe)
self._queue.put_nowait(data=item, priority=priority, metadata=...)

# Dequeue from async loop
queue_item = await self._queue.get(timeout=1.0)
```

**PersistentQueue Features:**
- Stores items as JSON files in `{storage_dir}/queue/`
- Priority-based retrieval (1=highest)
- Survives process crashes
- Thread-safe

**Test Gaps:**
- ❌ What happens if disk is full (queue persistence fails)?
- ❌ Concurrent put/get from multiple converters?
- ❌ Performance with 10,000+ items queued?
- ❌ Corruption recovery (invalid JSON in queue file)?

### 3. Conversion Processing (`AsyncConverterPool._process_item()`)

**How It Works:**
```python
async def _process_item(self, item: AsyncConversionItem) -> None:
    # Load converter dynamically
    converter = item.converter
    
    # Optional sandbox execution
    if self._should_use_sandbox(converter):
        result_json = await self._convert_sandboxed(item)
    else:
        result = await converter.convert(source, context)
    
    # Submit report
    if result.success and result.report:
        report_id = await self._client.submit_uut_report(result.report)
    
    # Post-process source file
    await self._post_process(item, result)
```

**Test Gaps:**
- ❌ Sandbox isolation actually works?
- ❌ Converter crash recovery (sandbox cleanup)?
- ❌ Network failure during submit (retry behavior)?
- ❌ Post-processing happens BEFORE or AFTER submission? (risk of data loss!)

### 4. Post-Processing (`_post_process_file()`)

**Current Implementation:**
```python
async def _post_process_file(self, item, result) -> None:
    if result.post_action == PostProcessAction.DELETE:
        await self._delete_source_file(item.file_path)
    elif result.post_action == PostProcessAction.MOVE:
        await self._move_to_done(item.file_path)
    elif result.post_action == PostProcessAction.ZIP:
        await self._compress_and_move(item.file_path)
    # KEEP - do nothing
```

**Critical Issue (from archive analysis):**
> **Post-processing happens AFTER submission.** If submission succeeds but post-processing fails, source file is orphaned.
> 
> **Data Loss Risk:** If converter returns DELETE and submission succeeds, source is deleted. No way to reprocess.

**Test Gaps:**
- ❌ What if Done/ folder doesn't exist?
- ❌ What if file is locked during MOVE?
- ❌ What if compression fails (ZIP)?
- ❌ Retry logic for post-processing failures?

### 5. Error Handling & Retry

**AsyncPendingQueue** (`src/pywats_client/service/async_pending_queue.py`)
- Watches `reports_dir/*.queued` files
- Automatically re-submits on file detection
- Uses semaphore to limit concurrent submissions
- Thread-safe file event handling via `loop.call_soon_threadsafe()`

**Test Gaps:**
- ❌ What happens if WATS server is down for hours?
- ❌ Retry backoff strategy (exponential? linear?)?
- ❌ Max retry count (prevent infinite retries)?
- ❌ Queue file corruption recovery?

---

## Known Issues & "Loose Ends"

### Category 1: File Watch Reliability

**Issue #1: Potential File Misses During High Load**
- **Description:** C# client had skip logic to avoid scanning during active scan
- **Evidence:** `Monitor.TryEnter(_checkfolderLocker)` in C# reference
- **Risk:** Files arriving during scan may be missed
- ** Status:** ⚠️ **Needs investigation** - Does Python implementation have same issue?

**Issue #2: No Throttling on File Watch**
- **Description:** C# client limited pending files to 10 per converter
- **Evidence:** `if (pendingcount_start >= 10) return;` in CheckFolder
- **Risk:** Unbounded queue growth if files arrive faster than conversion
- **Status:** ⚠️ **Needs testing** - What's Python behavior under stress?

**Issue #3: File Lock Handling**
- **Description:** What if watched file is locked by another process?
- **Evidence:** No explicit lock checking in `_on_file_created()`
- **Risk:** Conversion fails with unclear error
- **Status:** ❌ **Not tested** - Need to validate error handling

### Category 2: Queue Behavior

**Issue #4: Disk Full During Queue Persistence**
- **Description:** PersistentQueue writes JSON to disk - what if disk is full?
- **Evidence:** No explicit disk space check before write
- **Risk:** Queue operation fails, file lost from queue
- **Status:** ❌ **Not tested**

**Issue #5: Concurrent Queue Access**
- **Description:** Multiple converters queueing simultaneously
- **Evidence:** `put_nowait()` is thread-safe, but performance under load unknown
- **Risk:** Queue contention slows down file detection
- **Status:** ❌ **No stress tests**

**Issue #6: Queue Corruption Recovery**
- **Description:** What if queue JSON file is corrupted (disk error, crash)?
- **Evidence:** No corruption detection or recovery logic visible
- **Risk:** Queue fails to load, items lost
- **Status:** ❌ **Not tested**

### Category 3: Conversion Errors

**Issue #7: Converter Crash in Sandbox**
- **Description:** If converter crashes in sandbox, is cleanup guaranteed?
- **Evidence:** Sandbox cleanup in `finally` block - but not tested
- **Risk:** Resource leaks (processes, files)
- **Status:** ❌ **Not tested**

**Issue #8: Network Failure During Submission**
- **Description:** What if WATS server becomes unreachable mid-submit?
- **Evidence:** AsyncPendingQueue handles retries, but timeout behavior unclear
- **Risk:** Long hangs, unclear error messages
- **Status:** ❌ **Not tested**

**Issue #9: Invalid Report Data**
- **Description:** What if converter returns malformed JSON?
- **Evidence:** No schema validation before submission
- **Risk:** Server rejects report, unclear error to user
- **Status:** ❌ **Not tested**

### Category 4: Post-Processing

**Issue #10: Post-Processing Before Archiving**
- **Description:** **CRITICAL** - Source file deleted before archiving (if using DELETE)
- **Evidence:** Post-processing happens AFTER submission (see code flow)
- **Risk:** **Data loss** - No way to reprocess deleted source
- **Status:** 🚨 **BLOCKER for archive system**

**Issue #11: Done Folder Doesn't Exist**
- **Description:** What if Done folder is deleted while converter is running?
- **Evidence:** `ConverterContext.ensure_folders_exist()` called once at startup
- **Risk:** MOVE post-action fails with unclear error
- **Status:** ❌ **Not tested**

**Issue #12: Source File Locked During Post-Processing**
- **Description:** What if antivirus locks file during MOVE?
- **Evidence:** No retry logic for post-process failures
- **Risk:** Orphaned file (conversion succeeded, but file stuck in watch folder)
- **Status:** ❌ **Not tested**

### Category 5: Configuration

**Issue #13: Config Reload Behavior**
- **Description:** What happens if ConverterConfig changes while converter is running?
- **Evidence:** C# client had settings watcher with 500ms reload delay
- **Risk:** Undefined behavior (old config? new config? crash?)
- **Status:** ❌ **Not specified** - Need to document expected behavior

**Issue #14: Invalid Module Path**
- **Description:** What if `module_path` in ConverterConfig points to non-existent module?
- **Evidence:** Dynamic import in `_load_converters()` - error handling unclear
- **Risk:** Converter fails to load, unclear error to user
- **Status:** ⚠️ **Partial** - Need to validate error messages are clear

### Category 6: Performance

**Issue #15: No Throughput Limits**
- **Description:** Semaphore limits to 10 concurrent, but total throughput unknown
- **Evidence:** No performance benchmarking done
- **Risk:** Can't set customer expectations (files/minute)
- **Status:** ❌ **No baseline**

**Issue #16: Resource Leaks**
- **Description:** Are file handles, processes, threads properly cleaned up?
- **Evidence:** No long-running stress tests to detect leaks
- **Risk:** Memory/handle exhaustion after hours/days of operation
- **Status:** ❌ **Not tested**

---

## Testing Gaps

### Unit Test Coverage

**Current Coverage (estimated from test file analysis):**
- `async_converter_pool.py`: ~30% (basic queue operations, file watching)
- `async_pending_queue.py`: ~20% (minimal tests)
- `file_converter.py`, `folder_converter.py`: ~10% (virtually no tests)
- `context.py`, `models.py`: ~50% (data classes, some helpers)

**Critical Missing Tests:**
- ❌ No stress tests (1000+ files, concurrent converters)
- ❌ No error injection tests (network down, disk full, file locked)
- ❌ No long-running tests (resource leaks, memory growth)
- ❌ No performance benchmarks (throughput, latency)

### Integration Test Coverage

**Current State:**
- ✅ Basic end-to-end flow tested (`test_async_converter_pool.py`)
- ❌ No WATS server integration tests (submission, errors)
- ❌ No multi-converter concurrent tests
- ❌ No file watch stress tests

**Critical Missing Tests:**
1. **End-to-end with real WATS server** - Verify submission, post-processing, error handling
2. **Concurrent converters** - Multiple converters watching different folders
3. **Error recovery** - Network failures, server downtime, disk full
4. **Config reload** - Change configuration while running
5. **Orphan cleanup** - Files left in watch folder after crash

### Performance Test Coverage

**Current State:**
- ❌ No performance tests exist

**Required Benchmarks:**
1. **Throughput** - Files converted per minute (100+ files)
2. **Latency** - Time from file arrival to submission (<5 seconds)
3. **Queue performance** - Get/put operations under load
4. **Resource usage** - CPU, memory, file handles over time
5. **Stress limits** - Maximum concurrent files before degradation

---

## Risk Assessment

| Risk | Probability | Impact | Severity | Mitigation |
|------|-------------|--------|----------|------------|
| **File watch misses files** | Medium | HIGH | 🔴 CRITICAL | Add stress test (1000 files), validate no misses |
| **Queue corruption** | Low | HIGH | 🟠 HIGH | Add corruption recovery, validate with fault injection |
| **Converter crash locks resources** | Medium | Medium | 🟡 MEDIUM | Add long-running tests, monitor for leaks |
| **Network failure hangs submission** | High | Medium | 🟡 MEDIUM | Add timeout tests, validate retry behavior |
| **Post-processing loses data** | High | HIGH | 🔴 CRITICAL | **BLOCKER for DELETE action** - Document risk, add archive-first |
| **Config reload crashes** | Low | Medium | 🟡 MEDIUM | Specify behavior, add test for reload |
| **Invalid module path unclear** | Medium | Low | 🟢 LOW | Improve error messages, add validation |
| **Throughput unknown** | High | Low | 🟢 LOW | Run benchmarks, document limits |
| **Resource leaks over time** | Medium | Medium | 🟡 MEDIUM | Add 24-hour stress test, monitor resources |

**Legend:**
- 🔴 **CRITICAL** - Must fix before v1.0
- 🟠 **HIGH** - Should fix before v1.0
- 🟡 **MEDIUM** - Fix if time permits, document if not
- 🟢 **LOW** - Nice-to-have, can defer to v1.1

---

## Testing Strategy

### Phase 1: Unit Test Completion (Week 1)

**Goal:** Achieve >90% coverage for converter domain

**Tasks:**
1. **File Converter Tests**
   - Test `convert()` with valid/invalid files
   - Test `validate()` returning various confidence scores
   - Test error handling (missing files, locked files)

2. **Folder Converter Tests**
   - Test `is_folder_ready()` with/without marker file
   - Test `convert_folder()` with multiple files
   - Test error handling (partial folders, missing files)

3. **AsyncConverterPool Tests**
   - Test file watch with multiple files
   - Test queue priority ordering
   - Test semaphore limiting (max 10 concurrent)
   - Test converter loading (valid, invalid module paths)
   - Test post-processing (all 4 actions)

4. **AsyncPendingQueue Tests**
   - Test `.queued` file detection
   - Test concurrent submissions
   - Test retry behavior (network failures)
   - Test cleanup after success

5. **ConverterContext Tests**
   - Test folder helpers (get_done_path, etc.)
   - Test logging helpers
   - Test factory methods

**Acceptance Criteria:**
- ✅ `pytest --cov=src/pywats_client/converters --cov-report=term` shows >90%
- ✅ All tests pass
- ✅ No skipped tests

### Phase 2: Integration Testing (Week 2)

**Goal:** Validate end-to-end flows and integration points

**Test Scenarios:**

**1. End-to-End Happy Path**
```python
async def test_e2e_file_conversion_and_submission():
    """Test complete flow: file → queue → convert → submit → post-process"""
    # Setup: Watch folder, converter, WATS server mock
    # Action: Drop file in watch folder
    # Verify: File converted, report submitted, file moved to Done/
```

**2. End-to-End Error Recovery**
```python
async def test_e2e_network_failure_retry():
    """Test flow when WATS server is down"""
    # Setup: Watch folder, converter, WATS server mock (fail then succeed)
    # Action: Drop file, trigger network error
    # Verify: File moved to Pending/, retry queued, eventually succeeds
```

**3. Multi-Converter Concurrent**
```python
async def test_multiple_converters_concurrent():
    """Test 3 converters watching different folders"""
    # Setup: 3 converters (CSV, XML, TXT)
    # Action: Drop 100 files in each folder
    # Verify: All 300 files converted, no cross-contamination
```

**4. Config Reload**
```python
async def test_config_reload_while_running():
    """Test changing converter config mid-operation"""
    # Setup: Converter running
    # Action: Change watch_folder in config, reload
    # Verify: Watcher updates, new folder monitored
```

**5. Orphan Cleanup**
```python
async def test_orphan_file_cleanup_after_crash():
    """Test recovery from crash during conversion"""
    # Setup: Simulate crash (kill process mid-conversion)
    # Action: Restart converter pool
    # Verify: Files in watch folder re-queued and processed
```

**Acceptance Criteria:**
- ✅ All integration tests pass
- ✅ No flaky tests (run 10 times, 100% pass rate)
- ✅ Tests complete in <5 minutes

### Phase 3: Stress & Performance Testing (Week 2-3)

**Goal:** Validate behavior under high load and establish baselines

**Stress Tests:**

**1. File Watch Stress**
```python
async def test_file_watch_1000_files_simultaneous():
    """Drop 1000 files in watch folder at once"""
    # Action: Create 1000 test files rapidly (<1 second)
    # Verify: All 1000 files queued and converted, none missed
    # Baseline: <5 seconds total time
```

**2. Queue Performance**
```python
async def test_queue_put_get_10000_items():
    """Measure queue throughput"""
    # Action: Put 10,000 items, get 10,000 items
    # Verify: All items retrieved in FIFO priority order
    # Baseline: <1 second for put, <2 seconds for get
```

**3. Concurrent Conversions**
```python
async def test_max_concurrent_conversions():
    """Test semaphore limiting (max 10)"""
    # Action: Queue 100 files instantly
    # Verify: Max 10 conversions running simultaneously
    # Baseline: Measure throughput (files/minute)
```

**4. Resource Leak Detection**
```python
async def test_24hour_stress_conversion():
    """Long-running test (24 hours)"""
    # Action: Convert 1 file every 10 seconds for 24 hours (8,640 files)
    # Verify: Memory stable, no file handle leaks
    # Baseline: Memory growth <1% per hour
```

**5. Disk Full Simulation**
```python
async def test_queue_persistence_disk_full():
    """Simulate disk space exhaustion"""
    # Action: Fill disk, attempt to queue item (use temp mount)
    # Verify: Graceful error, item not lost (kept in memory)
    # Baseline: Clear error message to user
```

**Performance Benchmarks:**
| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Throughput | 100 files/min | <50 files/min |
| Latency (file arrival → submission) | <5 seconds | >15 seconds |
| Queue put (1,000 items) | <1 second | >5 seconds |
| Queue get (1,000 items) | <2 seconds | >10 seconds |
| Memory growth (24 hours) | <1% per hour | >5% per hour |
| File handles (after 1,000 conversions) | <20 | >100 |

**Acceptance Criteria:**
- ✅ All stress tests pass
- ✅ Performance meets target benchmarks
- ✅ No resource leaks detected
- ✅ Graceful degradation under extreme load

### Phase 4: Error Injection Testing (Week 3)

**Goal:** Validate error handling and recovery

**Error Scenarios:**

**1. File Locked**
```python
async def test_file_locked_by_another_process():
    """Simulate antivirus locking file"""
    # Action: Create file, hold lock, trigger converter
    # Verify: Graceful error, file moved to Error/ or retried
```

**2. Invalid JSON**
```python
async def test_converter_returns_invalid_json():
    """Converter returns malformed report"""
    # Action: Mock converter to return invalid JSON
    # Verify: Validation error, file moved to Error/
```

**3. Network Timeout**
```python
async def test_wats_server_timeout():
    """WATS server takes >60 seconds to respond"""
    # Action: Mock server with 60s delay
    # Verify: Timeout, file queued to Pending/, retry scheduled
```

**4. Invalid Module Path**
```python
async def test_converter_module_not_found():
    """ConverterConfig points to non-existent module"""
    # Action: Configure "non.existent.Converter"
    # Verify: Clear error message in logs, converter skipped
```

**5. Folder Deleted Mid-Operation**
```python
async def test_done_folder_deleted():
    """Delete Done/ folder while converter is running"""
    # Action: Delete folder, trigger MOVE post-processing
    # Verify: Folder recreated OR clear error
```

**Acceptance Criteria:**
- ✅ All error scenarios handled gracefully
- ✅ Error messages clear and actionable
- ✅ No crashes, hangs, or data loss
- ✅ Recovery mechanisms validated

---

## Performance Baseline

### Measurement Points

**1. File Detection Latency**
- **Metric:** Time from file created to queued
- **Target:** <500ms
- **Measurement:** Log timestamp diff

**2. Conversion Latency**
- **Metric:** Time from queued to conversion complete
- **Target:** <5 seconds (for typical 10 KB file)
- **Measurement:** ConverterResult.duration_ms

**3. Submission Latency**
- **Metric:** Time to submit report to WATS server
- **Target:** <2 seconds
- **Measurement:** Network time in `submit_uut_report()`

**4. Total Pipeline Latency**
- **Metric:** File arrival → report submitted
- **Target:** <7 seconds
- **Measurement:** End-to-end timestamping

**5. Throughput**
- **Metric:** Files converted per minute
- **Target:** >100 files/min (single converter)
- **Measurement:** Count over 1-minute window

**6. Resource Consumption**
- **Metrics:**
  - Memory (RSS)
  - CPU (avg %)
  - File handles
  - Thread count
- **Baseline:** TBD (establish via 24-hour test)

---

## Technical Debt

### Debt Items to Address

**1. PostProcessAction.DELETE Risk**
- **Issue:** Source file deleted before archiving opportunity
- **Impact:** Cannot reprocess deleted files
- **Fix:** Change pipeline to archive BEFORE post-processing
- **Priority:** 🔴 CRITICAL (blocks archive system)

**2. No Queue Size Limits**
- **Issue:** Unbounded queue growth if files arrive faster than conversion
- **Impact:** Memory exhaustion, disk full
- **Fix:** Add `max_queue_size` config, reject new files when full
- **Priority:** 🟠 HIGH

**3. Thread Safety in _on_file_created**
- **Issue:** Called from watchdog thread, must use thread-safe queue operations
- **Impact:** Potential race conditions
- **Fix:** Audit all thread boundaries, add thread-safety tests
- **Priority:** 🟠 HIGH

**4. No Converter Versioning**
- **Issue:** Can't track which converter version converted a file
- **Impact:** Unknown behavior if converter logic changes
- **Fix:** Add `converter_version` to ConverterResult
- **Priority:** 🟡 MEDIUM (needed for archive system)

**5. Incomplete Error Context**
- **Issue:** Errors logged but context unclear (which file? which converter?)
- **Impact:** Hard to debug production issues
- **Fix:** Add structured logging with converter name, file path, timestamps
- **Priority:** 🟡 MEDIUM

**6. No Telemetry/Metrics**
- **Issue:** No instrumentation for monitoring (Prometheus, StatsD, etc.)
- **Impact:** Can't monitor production health
- **Fix:** Add metrics for queue size, throughput, errors, latency
- **Priority:** 🟢 LOW (defer to v1.1)

### Refactoring Opportunities

**1. Extract Post-Processing Logic**
- Current: Inline in `AsyncConverterPool._post_process_file()`
- Proposed: Separate `PostProcessingEngine` class
- Benefit: Easier to test, extend with archive support

**2. Separate Watcher Logic**
- Current: `_FileEventHandler` nested in `AsyncConverterPool`
- Proposed: Separate `FileWatcherService` class
- Benefit: Easier to mock, test, reuse

**3. Standardize Error Types**
- Current: Generic `Exception` catching
- Proposed: `ConverterError`, `QueueError`, `SubmissionError` hierarchy
- Benefit: Structured error handling, clearer logging

---

## Recommendations

### Critical Path (Must-Do for v1.0)

1. ✅ **Fix PostProcessAction.DELETE risk** (BLOCKER)
   - Change pipeline: Archive → Submit → Post-Process
   - Or document risk and require archive system before DELETE

2. ✅ **Achieve >90% test coverage** (Quality Gate)
   - Write 50+ unit tests for converter domain
   - Focus on error paths and edge cases

3. ✅ **Validate file watch reliability** (Stress Test)
   - Test with 1,000 simultaneous files
   - Verify no files missed

4. ✅ **Document expected behavior** (Specification)
   - Create "Converter Behavior Specification" document
   - Define success criteria, error handling, recovery

5. ✅ **Run 24-hour stress test** (Resource Leak Detection)
   - Verify memory/handle stability
   - Establish performance baseline

### High Priority (Should-Do for v1.0)

6. ⚠️ **Add queue size limits** (Stability)
   - Prevent unbounded growth
   - Graceful degradation when full

7. ⚠️ **Improve error messages** (Usability)
   - Audit all error paths
   - Ensure messages are actionable

8. ⚠️ **Add structured logging** (Debugging)
   - Include converter name, file path in all logs
   - Use consistent log levels

### Medium Priority (Nice-to-Have)

9. 🟡 **Refactor post-processing** (Architecture)
   - Extract to separate engine
   - Prepare for archive integration

10. 🟡 **Add converter versioning** (Traceability)
    - Track which version converted each file
    - Enable version-specific reprocessing

### Low Priority (Defer to v1.1)

11. 🟢 **Add telemetry/metrics** (Monitoring)
    - Prometheus/StatsD integration
    - Dashboards for production monitoring

12. 🟢 **Optimize queue performance** (Performance)
    - Consider in-memory tier for hot items
    - Benchmark vs. Redis/RabbitMQ

---

## Next Steps

1. **Review this analysis** with team
2. **Prioritize fixes** (critical, high, medium, low)
3. **Create implementation plan** (02_IMPLEMENTATION_PLAN.md)
4. **Begin systematic testing** (start with unit tests)
5. **Document findings** (update 03_PROGRESS.md as we go)

---

**Last Updated:** February 13, 2026  
**Status:** Analysis Complete, Ready for Implementation Planning
