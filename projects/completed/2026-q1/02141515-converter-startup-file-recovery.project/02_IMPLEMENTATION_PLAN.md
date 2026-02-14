# Implementation Plan: Converter Startup File Recovery

**Created:** February 14, 2026, 14:30  
**Last Updated:** February 14, 2026, 14:30  
**Status:** Ready for Implementation

---

## Overview

Implement startup file scanning in AsyncConverterPool to prevent data loss when files are dropped during system downtime.

**Pattern**: Follow AsyncPendingQueue's `submit_all_pending()` design.  
**Key Challenge**: Race condition prevention (deduplication).  
**Estimated Effort**: 11 hours (~1.5 days).

---

## Phase 1: Core Implementation

### 1.1 Add Instance Variables

**File**: `src/pywats_client/service/async_converter_pool.py`  
**Location**: `__init__()` method

```python
def __init__(self, ...):
    # Existing code...
    
    # Startup scan deduplication (race condition prevention)
    self._startup_scan_files: Set[Path] = set()
    self._startup_scan_complete: bool = False
    self._startup_scan_enabled: bool = True  # Default enabled
```

**Purpose**:
- `_startup_scan_files`: Track files queued during startup (prevent duplicates)
- `_startup_scan_complete`: Flag to disable tracking after TTL expires
- `_startup_scan_enabled`: Configuration toggle

### 1.2 Implement Startup Scan Method

**File**: `src/pywats_client/service/async_converter_pool.py`  
**Location**: New method after `_start_watchers()`

```python
async def _scan_existing_files(self) -> Dict[str, int]:
    """
    Scan watch directories for existing files on startup.
    
    Prevents data loss when files are dropped during system downtime.
    Files are queued before watchers start to avoid race conditions.
    
    Returns:
        Dict with statistics:
        - 'scanned': Total files examined
        - 'queued': Files queued for processing
        - 'skipped': Files skipped (already queued, wrong extension)
        - 'errors': Files that caused errors
    """
    if not self._startup_scan_enabled:
        logger.info("Startup scan disabled in configuration")
        return {'scanned': 0, 'queued': 0, 'skipped': 0, 'errors': 0}
    
    logger.info("Starting scan for existing files in watch directories...")
    
    stats = {
        'scanned': 0,
        'queued': 0,
        'skipped': 0,
        'errors': 0
    }
    
    scan_start = datetime.now()
    
    try:
        for converter in self._converters:
            # Skip if no watch path configured
            if not converter.watch_path or not converter.watch_path.exists():
                logger.debug(f"Skip scan for {converter.name} (no watch path)")
                continue
            
            # Get all files matching converter's extensions
            files_to_scan = []
            for ext in converter.supported_extensions:
                pattern = f"*{ext}"
                files_to_scan.extend(
                    converter.watch_path.glob(pattern)
                    if not converter.watch_recursive
                    else converter.watch_path.rglob(pattern)
                )
            
            # Sort by modification time (oldest first - FIFO)
            files_to_scan = sorted(
                [f for f in files_to_scan if f.is_file()],
                key=lambda p: p.stat().st_mtime
            )
            
            logger.info(
                f"Found {len(files_to_scan)} existing files for {converter.name}"
            )
            
            # Queue each file
            for file_path in files_to_scan:
                stats['scanned'] += 1
                
                try:
                    # Check if file already marked as queued (.queued marker)
                    if self._is_file_queued(file_path):
                        logger.debug(f"Skip {file_path.name} (already queued)")
                        stats['skipped'] += 1
                        continue
                    
                    # Check if file in startup scan set (shouldn't happen, but safety)
                    if file_path in self._startup_scan_files:
                        logger.debug(f"Skip {file_path.name} (duplicate in scan)")
                        stats['skipped'] += 1
                        continue
                    
                    # Queue the file
                    priority = getattr(converter, 'priority', 5)
                    item = AsyncConversionItem(file_path, converter, priority=priority)
                    
                    self._queue.put_nowait(
                        data=item,
                        priority=priority,
                        metadata={'file': str(file_path), 'converter': converter.name}
                    )
                    
                    # Track in startup scan set (deduplicate watchdog events)
                    self._startup_scan_files.add(file_path)
                    stats['queued'] += 1
                    
                    logger.debug(
                        f"Queued from startup scan: {file_path.name} "
                        f"(priority={priority}, converter={converter.name})"
                    )
                    
                except Exception as e:
                    logger.exception(f"Error queuing {file_path.name}: {e}")
                    stats['errors'] += 1
        
        # Schedule cleanup of deduplication set (after watchdog event buffer clears)
        asyncio.create_task(self._clear_startup_scan_set())
        
    except Exception as e:
        logger.exception(f"Startup scan failed: {e}")
        stats['errors'] += 1
    
    scan_duration = (datetime.now() - scan_start).total_seconds()
    
    logger.info(
        f"Startup scan complete: {stats['queued']} files queued, "
        f"{stats['skipped']} skipped, {stats['errors']} errors ({scan_duration:.2f}s)"
    )
    
    return stats

def _is_file_queued(self, file_path: Path) -> bool:
    """
    Check if file is already queued (has .queued marker).
    
    This prevents re-processing files that were queued but not yet converted.
    """
    queued_marker = file_path.parent / f"{file_path.name}.queued"
    return queued_marker.exists()

async def _clear_startup_scan_set(self) -> None:
    """
    Clear startup scan tracking set after buffer time.
    
    Waits 5 seconds for watchdog to process any buffered events,
    then clears the deduplication set to free memory.
    """
    await asyncio.sleep(5.0)  # Buffer time for delayed watchdog events
    
    count = len(self._startup_scan_files)
    self._startup_scan_files.clear()
    self._startup_scan_complete = True
    
    logger.debug(f"Cleared startup scan set ({count} files tracked)")
```

### 1.3 Update _on_file_created (Deduplication)

**File**: `src/pywats_client/service/async_converter_pool.py`  
**Location**: `_on_file_created()` method

```python
def _on_file_created(
    self,
    file_path: Path,
    converter: 'Converter'
) -> None:
    """Handle new file detected (called from watchdog thread - NOT async safe!)"""
    # Validate file matches converter pattern
    if not converter.matches_file(file_path):
        return
    
    # ✅ NEW: Deduplicate against startup scan
    if not self._startup_scan_complete and file_path in self._startup_scan_files:
        logger.debug(
            f"Skip {file_path.name} (already queued in startup scan)"
        )
        return
    
    # Get priority from converter (default to 5 if not set)
    priority = getattr(converter, 'priority', 5)
    
    # Queue for conversion with priority
    # AsyncQueueAdapter.put_nowait is thread-safe, can call directly
    try:
        item = AsyncConversionItem(file_path, converter, priority=priority)
        self._queue.put_nowait(
            data=item,
            priority=priority,
            metadata={'file': str(file_path), 'converter': converter.name}
        )
        logger.debug(
            f"Queued (priority={priority}): {file_path.name} via {converter.name}"
        )
    except Exception as e:
        logger.warning(f"Cannot queue {file_path.name}: {e}", exc_info=True)
```

### 1.4 Update run() Sequence

**File**: `src/pywats_client/service/async_converter_pool.py`  
**Location**: `run()` method

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
        
        # ✅ NEW: Scan for existing files BEFORE starting watchers
        scan_stats = await self._scan_existing_files()
        
        # Start file watchers
        await self._start_watchers()
        
        # Process queue until stopped
        while not self._stop_event.is_set():
            # ... existing code
```

---

## Phase 2: Configuration Support

### 2.1 Update ClientConfig Schema

**File**: `src/pywats_client/core/config.py`  
**Location**: ClientConfig class

```python
class ConverterConfig:
    """Converter configuration"""
    
    # Existing fields...
    
    # Startup scan configuration
    enable_startup_scan: bool = True  # Scan for existing files on startup
    startup_scan_timeout: int = 30  # Timeout in seconds
    startup_scan_max_files: int = 0  # Max files to scan (0=unlimited)

class ClientConfig:
    """Client configuration"""
    
    converter: ConverterConfig
    # ... other fields
```

### 2.2 Load Config in __init__

**File**: `src/pywats_client/service/async_converter_pool.py`  
**Location**: `__init__()` method

```python
def __init__(
    self,
    api_client: 'AsyncWATS',
    config: 'ClientConfig',
    # ... other params
):
    # Existing code...
    
    # Load startup scan config
    self._startup_scan_enabled = config.converter.enable_startup_scan
    self._startup_scan_timeout = config.converter.startup_scan_timeout
    self._startup_scan_max_files = config.converter.startup_scan_max_files
```

---

## Phase 3: Testing

### 3.1 Unit Tests

**File**: `tests/client/service/test_async_converter_pool_startup_scan.py` (NEW)

**Tests**:
1. `test_scan_queues_all_existing_files` - Basic scan functionality
2. `test_scan_respects_extension_filter` - Only matching extensions
3. `test_scan_skips_queued_files` - Skip .queued markers
4. `test_scan_deduplication_watchdog_event` - Race condition prevention
5. `test_scan_sorted_by_mtime` - FIFO processing
6. `test_scan_disabled_via_config` - Configuration toggle
7. `test_scan_stats_accurate` - Statistics reporting
8. `test_scan_error_handling` - Graceful error recovery

### 3.2 Integration Tests

**File**: `tests/integration/test_converter_startup_recovery.py` (NEW)

**Tests**:
1. `test_end_to_end_startup_recovery` - Full workflow
2. `test_race_file_during_scan` - File dropped mid-scan
3. `test_crash_before_queue_recovery` - Crash simulation
4. `test_large_backlog_performance` - 100 files under 5s

### 3.3 Performance Tests

**File**: `tests/performance/test_startup_scan_performance.py` (NEW)

**Tests**:
1. `test_scan_100_files_under_5s` - Typical load
2. `test_scan_1000_files_memory_overhead` - Large backlog
3. `test_dedup_set_cleared_after_ttl` - Memory leak prevention

---

## Phase 4: Documentation

### 4.1 Update Architecture Guide

**File**: `docs/guides/converter-architecture.md`  
**Section**: Add "Startup File Recovery" after "File Watcher" section

```markdown
### Startup File Recovery

**Problem**: Files dropped during system downtime are not detected by FileWatcher.

**Solution**: AsyncConverter Pool scans watch directories on startup before activating watchers.

**Process**:
1. Load converters from configuration
2. Scan each converter's watch directory
3. Queue all existing files (sorted by mtime, oldest first)
4. Start file watchers
5. Process queue (including startup scan files)

**Deduplication**: Files queued during startup scan are tracked for 5 seconds to prevent duplicate processing if watchdog buffered events.

**Configuration**:
```yaml
converter:
  enable_startup_scan: true  # default: true
  startup_scan_timeout: 30   # seconds
  startup_scan_max_files: 0  # 0 = unlimited
```

**Performance**: Startup scan adds <5s delay for typical loads (100 files).
```

### 4.2 Update Configuration Reference

**File**: `docs/CLIENT_CONFIGURATION.md` (or similar)

Add converter startup scan configuration options with examples.

### 4.3 Update CHANGELOG.md

**File**: `CHANGELOG.md`  
**Section**: `[Unreleased]` → `Added`

```markdown
### Added
- **Converter Startup File Recovery**: AsyncConverterPool now scans watch directories on startup to queue existing files, preventing data loss when files are dropped during system downtime
  - Automatic deduplication to prevent race conditions with FileWatcher events
  - Configurable via `converter.enable_startup_scan` (default: true)
  - Performance: <5s for 100 files, configurable timeout
  - See `docs/guides/converter-architecture.md` for details
  - Tests: 12 new tests covering race conditions, deduplication, and performance
```

---

## Phase 5: Code Review Checklist

### 5.1 Functional Requirements

- [ ] Startup scan finds all files matching converter extensions
- [ ] Files sorted by mtime (FIFO - oldest first)
- [ ] Deduplication prevents double-queueing
- [ ] Configuration toggle works (enable/disable)
- [ ] Statistics accurate (scanned, queued, skipped, errors)
- [ ] Graceful error handling (per-file errors don't crash scan)

### 5.2 Race Condition Prevention

- [ ] Scan completes BEFORE watchers start
- [ ] Deduplication set tracks startup scan files
- [ ] _on_file_created checks dedup set
- [ ] Dedup set cleared after 5s TTL
- [ ] Thread-safe queue operations (put_nowait)

### 5.3 Performance

- [ ] Scan completes <5s for 100 files
- [ ] Semaphore limits concurrent processing
- [ ] Memory overhead <1MB for 1000 files
- [ ] Async I/O used (no blocking)

### 5.4 Backward Compatibility

- [ ] Default config enables startup scan (safe default)
- [ ] Existing configs work without changes
- [ ] No breaking changes to API

### 5.5 Testing

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Performance benchmarks meet targets
- [ ] Crash simulation validates recovery

### 5.6 Documentation

- [ ] Architecture guide updated
- [ ] Configuration reference updated
- [ ] CHANGELOG entry added
- [ ] Code comments clear and accurate

---

## Implementation Order

1. ✅ **Phase 1.1**: Add instance variables (5 min)
2. ✅ **Phase 1.2**: Implement _scan_existing_files() (1 hour)
3. ✅ **Phase 1.3**: Update _on_file_created deduplication (15 min)
4. ✅ **Phase 1.4**: Update run() sequence (10 min)
5. ⏸️ **Phase 2.1**: Update ClientConfig schema (15 min)
6. ⏸️ **Phase 2.2**: Load config in __init__ (10 min)
7. ⏸️ **Phase 3.1**: Unit tests (2 hours)
8. ⏸️ **Phase 3.2**: Integration tests (1.5 hours)
9. ⏸️ **Phase 3.3**: Performance tests (30 min)
10. ⏸️ **Phase 4**: Documentation (1 hour)

**Total**: ~7.5 hours implementation + 4 hours testing + 1 hour docs = **12.5 hours**

---

## Success Metrics

- [ ] Zero data loss in crash/restart scenarios
- [ ] Zero duplicate processing (race condition tests pass)
- [ ] Startup delay <5s for 100 files
- [ ] Memory overhead <1MB
- [ ] All tests passing (416 → 428 tests)
- [ ] Documentation complete and clear

---

## Dependencies

No new external dependencies required. Uses:
- `watchdog` (already installed)
- `asyncio` (stdlib)
- `pathlib` (stdlib)
- `AsyncQueueAdapter` (existing)

---

## Rollback Plan

If issues found after merge:

1. **Configuration**: Set `enable_startup_scan: false` to disable
2. **Code**: Revert commit (git revert)
3. **Monitoring**: Check logs for scan errors, duplicate processing

---

## Next Steps

1. Review this plan with stakeholders
2. Begin Phase 1.1 (instance variables)
3. Implement iteratively with continuous testing
4. Update progress in `03_PROGRESS.md`
5. Track tasks in `04_TODO.md`
