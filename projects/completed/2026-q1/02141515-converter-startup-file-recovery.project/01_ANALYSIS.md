# Gap Analysis: Converter Startup File Recovery

**Created:** February 14, 2026, 14:30  
**Last Updated:** February 14, 2026, 14:30  
**Analyst:** AI Agent (User Request)

---

## Executive Summary

**Critical Production Gap Identified**: AsyncConverterPool lacks startup directory scanning, creating risk of silent data loss when files are dropped during system downtime.

**Root Cause**: FileWatcher (watchdog Observer) only detects NEW file system events. Files existing before watcher starts are invisible.

**Impact**: High - Production data loss risk in crash/restart scenarios.

**Solution**: Implement startup scan similar to AsyncPendingQueue's `submit_all_pending()` pattern.

---

## Detailed Analysis

### 1. File Watcher Components Inventory

| Component | Location | Watcher Type | Startup Scan? | Status |
|-----------|----------|--------------|---------------|--------|
| **AsyncConverterPool** | `async_converter_pool.py:404` | watchdog.Observer | ❌ **NO** | **Gap Found** |
| **AsyncPendingQueue** | `async_pending_queue.py:303` | watchdog.Observer | ✅ YES | Already Fixed |
| **AsyncClientService** | `async_client_service.py:589` | Timer (health check) | N/A | Not Applicable |

### 2. AsyncConverterPool Startup Sequence

**Current Implementation** (`async_converter_pool.py` lines 207-230):

```python
async def run(self) -> None:
    """
    Main processing loop.
    
    Starts file watchers and processes conversion queue.
    """
    if self._running:
        logger.warning("Pool already running")
        return
    
    self._running = True
    self._stop_event.clear()
    
    # Store loop reference for thread-safe signaling from watchdog
    self._loop = asyncio.get_running_loop()
    
    logger.info("AsyncConverterPool starting...")
    
    try:
        # Load converters from config
        await self._load_converters()
        
        # Start file watchers
        await self._start_watchers()  # ⚠️ NO SCAN BEFORE THIS
        
        # Process queue until stopped
        while not self._stop_event.is_set():
            # ... queue processing
```

**Gap**: Between `_load_converters()` and `_start_watchers()`, existing files are not scanned.

### 3. AsyncPendingQueue Startup Sequence (CORRECT PATTERN)

**Reference Implementation** (`async_pending_queue.py` lines 188-220):

```python
async def run(self) -> None:
    """
    Main queue processing loop.
    
    Watches for new files and submits them concurrently.
    """
    if self.state == AsyncPendingQueueState.RUNNING:
        logger.warning("Queue already running")
        return
    
    self.state = AsyncPendingQueueState.RUNNING
    self._stop_event.clear()
    
    # Store loop reference for thread-safe signaling from watchdog
    self._loop = asyncio.get_running_loop()
    
    logger.info("AsyncPendingQueue starting...")
    
    try:
        # Start file watcher
        self._start_watcher()
        
        # ✅ Initial submission of existing queued files
        await self.submit_all_pending()  # <-- GOOD PATTERN
        
        # Main loop: wait for new files or periodic check
        while not self._stop_event.is_set():
            # ... event processing
```

**Key Method** (`async_pending_queue.py` lines 331-358):

```python
async def submit_all_pending(self) -> None:
    """Submit all pending (.queued) reports concurrently"""
    # Get all queued files, sorted by modification time
    queued_files = sorted(
        self.reports_dir.glob(self.FILTER_QUEUED),
        key=lambda p: p.stat().st_mtime
    )
    
    if not queued_files:
        return
    
    logger.info(f"Submitting {len(queued_files)} queued reports...")
    
    # Submit all files concurrently (semaphore limits actual concurrency)
    tasks = [
        asyncio.create_task(self._submit_with_limit(f))
        for f in queued_files
    ]
    
    # Add tasks to tracking set
    for task in tasks:
        self._active_uploads.add(task)
        task.add_done_callback(lambda t: self._active_uploads.discard(t))
    
    # Wait for all to complete
    await asyncio.gather(*tasks, return_exceptions=True)
```

**Pattern to Replicate**:
1. List files matching pattern (glob)
2. Sort by modification time (oldest first)
3. Create async tasks with semaphore limiting
4. Process all concurrently
5. Log results

### 4. C# CheckFolder Implementation (Historical Reference)

**Source**: `docs/internal_documentation/valuable_insights_for_backend_team/ConverterArchitectureAnalysis.md`

**Purpose**: Original C# WATS Client had TWO mechanisms for file detection:
1. FileSystemWatcher (reactive - like Python watchdog)
2. CheckFolder() timer (proactive - every 5s scan as backup)

**Serialization Guard**:
```csharp
private object _checkfolderLocker = new object();

public void CheckFolderSingleThread(object sender)
{
    if (!Monitor.TryEnter(_checkfolderLocker))
    {
        Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, 
            "Skipping CheckFolder (already running).");
        return;
    }

    try
    {
        if (ConverterState == ConverterStateEnum.FailedToStart)
            Start();
        else
            CheckFolder();  // <-- Scans directory for files

        Thread.Sleep(5000); // wait 5sec between CheckFolders
    }
    finally
    {
        Monitor.Exit(_checkfolderLocker);
    }
}
```

**Why C# Needed This**: FileSystemWatcher in .NET is unreliable under load (can drop events). CheckFolder() was safety net.

**Python watchdog**: More reliable than .NET FileSystemWatcher, but still vulnerable to:
- Files dropped during downtime (before watcher starts)
- Observer not yet initialized
- System crashes before event reaches handler

---

## Race Condition Analysis

### Potential Race Scenarios

#### Scenario 1: File Created During Startup Scan (LOW RISK)

```
Timeline:
T0: Startup scan begins
T1: Scan iterates directory (file A, B, C found)
T2: User drops file D
T3: Scan adds A, B, C to queue
T4: Scan completes
T5: Watchers start
T6: Watchdog detects file D → queues D
```

**Result**: ✅ File D queued by watcher (correct)  
**Risk**: None - sequence is safe

#### Scenario 2: Watchdog Buffers Events During Scan (HIGH RISK)

```
Timeline:
T0: Watchers start (Observer.start() called)
T1: Startup scan begins
T2: Scan finds file A (dropped at T-1, before startup)
T3: Watchdog internal buffer detects file A (delayed event)
T4: Scan queues file A → adds to _startup_scan_files set
T5: Scan completes
T6: Watchdog processes buffered event for file A
T7: _on_file_created(file A) called
T8: Check: Is file A in _startup_scan_files? YES → SKIP
```

**Result**: ✅ File A queued ONCE (deduplication works)  
**Risk**: Mitigated by _startup_scan_files tracking set

#### Scenario 3: Fast File Creation During Scan (MEDIUM RISK)

```
Timeline:
T0: Watchers start
T1: Scan begins, starts iterating directory
T2: User drops file X (new file, not in scan yet)
T3: Watchdog immediately detects file X → queues X
T4: Scan iteration reaches file X → attempts to queue X again
```

**Result**: ⚠️ File X queued TWICE (duplicate processing)  
**Risk**: **REAL ISSUE** - Need deduplication in scan logic

**Solution**: Check if file already in queue before adding during scan

#### Scenario 4: Watcher Event Arrives Before Scan Starts (LOW RISK)

**Not Possible**: Watchers don't start until after scan completes (sequential execution).

---

## Deduplication Strategies

### Strategy 1: Scan BEFORE Starting Watchers (RECOMMENDED)

**Sequence**:
1. Load converters
2. **Scan existing files** → Queue all
3. Start watchers
4. Process queue

**Pros**:
- Simplest design
- Clear separation of concerns
- No concurrent access to watch directories

**Cons**:
- Files dropped during scan won't be detected until watcher starts
- Need deduplication for scan → queue → watcher event sequence

**Race Condition**: If watcher internally buffers events from before Observer.start(), need tracking set.

**Implementation**:
```python
# Track files queued during startup scan
self._startup_scan_files: Set[Path] = set()
self._startup_scan_complete: bool = False

async def _scan_existing_files(self):
    for converter in self._converters:
        for file_path in converter.watch_path.glob(pattern):
            if file_path not in self._startup_scan_files:
                self._startup_scan_files.add(file_path)
                await self._queue_file(file_path, converter)
    
    # Start cleanup timer (clear set after 5s)
    asyncio.create_task(self._clear_startup_scan_set())

async def _clear_startup_scan_set(self):
    await asyncio.sleep(5.0)  # Buffer time for delayed events
    self._startup_scan_files.clear()
    self._startup_scan_complete = True

def _on_file_created(self, file_path, converter):
    # Deduplicate against startup scan
    if file_path in self._startup_scan_files:
        logger.debug(f"Skip {file_path.name} (already queued in startup scan)")
        return
    
    # Queue file normally
    self._queue.put_nowait(...)
```

### Strategy 2: Scan AFTER Starting Watchers (NOT RECOMMENDED)

**Issues**:
- Watchdog events might fire during scan
- Concurrent filesystem access (scan + watcher)
- More complex deduplication logic

### Strategy 3: Check Queue Before Adding (ALWAYS APPLY)

**Additional Safety**: Before queuing file, check if already in queue.

**Problem**: AsyncQueueAdapter doesn't expose "contains" check.

**Solution**: Track in-flight files separately OR add contains() method to queue.

---

## Performance Analysis

### Expected Workloads

| Scenario | File Count | Expected Scan Time | Risk Level |
|----------|------------|-------------------|------------|
| Typical startup | 0-10 files | <100ms | None |
| After short outage | 10-50 files | <500ms | Low |
| After long outage | 50-200 files | <2s | Medium |
| Extreme backlog | 200-1000 files | <10s | High |
| Pathological | 1000+ files | >10s | Critical |

### Performance Optimizations

1. **Async I/O**: Use `await` for file operations (already using aiofiles)
2. **Semaphore Limiting**: Same pattern as AsyncPendingQueue (max_concurrent)
3. **Configurable Timeout**: Add startup_scan_timeout config (default 30s)
4. **Skip Large Backlogs**: Option to skip if >N files (alert user instead)

### Memory Overhead

**Deduplication Set**:
- Average file path: 200 bytes
- 1000 files: ~200 KB in memory
- TTL: 5 seconds
- **Impact**: Negligible

---

## Configuration Design

### New Config Fields (ClientConfig)

```yaml
converter:
  # Enable startup scan for existing files (recommended)
  enable_startup_scan: true  # default: true
  
  # Maximum time to spend scanning on startup (seconds)
  startup_scan_timeout: 30  # default: 30
  
  # Maximum files to scan (0 = unlimited)
  startup_scan_max_files: 0  # default: 0 (unlimited)
  
  # Skip startup scan if backlog > N files (0 = never skip)
  startup_scan_skip_threshold: 0  # default: 0 (never skip)
```

### Backward Compatibility

- **Default**: `enable_startup_scan: true` (safer - prevents data loss)
- **Existing configs**: Missing field → defaults to true
- **No breaking changes**: All fields optional

---

## Related Gaps (Comprehensive Check)

### ✅ AsyncPendingQueue - Already Fixed

**Status**: HAS startup scan (`submit_all_pending()`)  
**Action**: None required (use as reference pattern)

### ❌ Archive Processing - Not Checked

**Component**: Archive file processing after conversion  
**Risk**: Unknown - needs investigation  
**Action**: Add to gap analysis in Phase 2

### ❌ Config File Watching - Not File Processing

**Component**: `AsyncClientService._config_watcher_loop()`  
**Purpose**: Detect config file changes (different use case)  
**Risk**: None - not file processing workflow  
**Action**: None required

---

## Recommendations

### Immediate Actions (This Project)

1. ✅ Implement `_scan_existing_files()` method in AsyncConverterPool
2. ✅ Add deduplication tracking set (_startup_scan_files)
3. ✅ Update run() sequence: load → scan → watch → process
4. ✅ Add configuration options (enable, timeout, max_files)
5. ✅ Add comprehensive tests (race conditions, deduplication, performance)
6. ✅ Document in converter-architecture.md

### Future Enhancements (Separate Projects)

1. **Periodic Scan**: Optional CheckFolder-style periodic scan (every 60s)
2. **Archive Processing**: Verify archive directory handling
3. **Queue Contains Check**: Add contains() method to AsyncQueueAdapter
4. **Startup Scan Stats**: Metrics (files found, queued, skipped, time)

---

## Conclusion

**Gap Confirmed**: AsyncConverterPool lacks startup file scanning, creating production data loss risk.

**Solution**: Implement startup scan using AsyncPendingQueue pattern with deduplication.

**Complexity**: Medium - requires race condition prevention and performance optimization.

**Priority**: **P0 Critical** - Blocks production deployment without data loss risk mitigation.

**Next Step**: Proceed to design phase (02_IMPLEMENTATION_PLAN.md).
