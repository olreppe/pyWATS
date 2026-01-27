# Client Async Architecture Analysis & Implementation Plan

**Created:** 2026-01-28  
**Status:** 📋 Design Document  
**Priority:** High (Architecture Improvement)  
**Related:** CORE_ARCHITECTURE_ANALYSIS.md

---

## Executive Summary

The current `pywats_client` uses **sync-only `pyWATS`** throughout, despite having async infrastructure (`AsyncTaskRunner`) in place. This creates several inefficiencies:

1. **GUI pages block on API calls** - Freezes UI during network operations
2. **Converter workers create blocking calls** - Cannot leverage async I/O
3. **PendingWatcher submits reports sequentially** - No parallel uploads
4. **Service uses threading instead of async** - Higher memory, context switching overhead

### Current vs Proposed Architecture

```
CURRENT (Sync-Only):
┌─────────────────────────────────────────────────────────────────┐
│                        ClientService                             │
│  ┌──────────────┐                                               │
│  │   pyWATS()   │ ← sync only, blocks on every call             │
│  └──────┬───────┘                                               │
│         │                                                        │
│  ┌──────▼───────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │ConverterPool │  │ PendingWatcher  │  │     Timers      │    │
│  │ (threads)    │  │ (threading)     │  │ (threading)     │    │
│  └──────────────┘  └─────────────────┘  └─────────────────┘    │
└─────────────────────────────────────────────────────────────────┘

PROPOSED (Async-First):
┌─────────────────────────────────────────────────────────────────┐
│                    AsyncClientService                            │
│  ┌──────────────┐                                               │
│  │ AsyncWATS()  │ ← true async, auto-discovery                  │
│  └──────┬───────┘                                               │
│         │                                                        │
│  ┌──────▼───────┐  ┌─────────────────┐  ┌─────────────────┐    │
│  │AsyncConverter │  │AsyncPendingQueue│  │  asyncio.Task   │    │
│  │  Pool        │  │ (concurrent)    │  │  (timers)       │    │
│  └──────────────┘  └─────────────────┘  └─────────────────┘    │
│                                                                  │
│        ↓ asyncio event loop (single thread, concurrent I/O)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 1: Current Architecture Analysis

### 1.1 ClientService (client_service.py)

**Current State:**
```python
from pywats import pyWATS

class ClientService:
    def __init__(self, instance_id: str = "default"):
        self.api: Optional[pyWATS] = None  # SYNC ONLY
        
    def _initialize_api(self):
        self.api = pyWATS(
            base_url=service_address,
            token=api_token
        )
```

**Issues:**
- Uses sync `pyWATS` which blocks on every API call
- Runs Qt event loop for IPC but API calls still block
- Creates/joins threads for converters, timers, watchers

**Impact:**
- Health checks block while waiting for API response
- Ping timer blocks service responsiveness
- Configuration reload can't happen during API calls

### 1.2 ConverterPool (converter_pool.py)

**Current State:**
```python
class ConverterWorkerClass(threading.Thread):
    def run(self):
        while not self.shutdown_in_progress:
            item = self.pool.get_next_file_to_convert()
            if item:
                api_client = self.pool.create_api_client()  # Shared sync pyWATS
                item.converter.convert_file(item, api_client)  # BLOCKS
```

**Issues:**
- Each worker is a full thread (~1MB stack per thread)
- Workers share single sync API client (or would need thread-local clients)
- File I/O (reading test files) blocks workers
- API submission blocks workers
- Auto-scaling creates/destroys threads frequently

**Impact:**
- With 10 converters + 10 workers = 20+ threads
- Each API call blocks entire worker
- Cannot batch-submit reports efficiently

### 1.3 PendingWatcher (pending_watcher.py)

**Current State:**
```python
def _submit_pending_reports(self):
    queued_files = sorted(self.reports_directory.glob("*.queued"), ...)
    
    for file_path in queued_files:
        self._submit_report(file_path)  # SEQUENTIAL, BLOCKING
```

**Issues:**
- Submits reports one-by-one sequentially
- Each submission waits for server response
- File operations block
- Timer callbacks block main submission

**Impact:**
- 100 queued reports with 200ms latency = 20+ seconds to clear queue
- With async: Could submit 10 concurrently = 2 seconds

### 1.4 GUI Pages (gui/pages/*.py)

**Current State:**
```python
# production.py
def _lookup_unit(self, serial_number: str, part_number: str) -> None:
    client = self._get_api_client()
    unit = client.production.get_unit(serial_number, part_number)  # BLOCKS UI
```

**Issues:**
- API calls happen on GUI thread
- No use of existing `AsyncTaskRunner`
- Loading states not shown during operations

**Impact:**
- GUI freezes during any API operation
- User sees unresponsive application
- Cannot cancel long-running operations

### 1.5 AsyncTaskRunner (Already Exists!)

**Current State:**
```python
class AsyncTaskRunner(QObject):
    """Executes async coroutines in a background thread"""
    
    def run(self, coro: Awaitable[T], name: str = "task", ...):
        # Runs async code, signals completion to Qt
```

**The Infrastructure Exists** - but isn't being used with AsyncWATS!

---

## Part 2: Proposed Async Architecture

### 2.1 Core Change: AsyncWATS as Primary API

```python
# NEW: client_service.py
from pywats import AsyncWATS

class AsyncClientService:
    """Async-first client service with asyncio event loop."""
    
    def __init__(self, instance_id: str = "default"):
        self.instance_id = instance_id
        self.config = ClientConfig.load_for_instance(instance_id)
        self.api: Optional[AsyncWATS] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        
    async def start(self):
        """Start service (async entry point)."""
        # Initialize async API with auto-discovery
        self.api = AsyncWATS()  # Uses auto-discovery from config
        await self.api.__aenter__()
        
        # Start async components
        self.converter_pool = AsyncConverterPool(self.config, self.api)
        self.pending_queue = AsyncPendingQueue(self.api, self.config.get_reports_path())
        
        # Start background tasks
        self._tasks = [
            asyncio.create_task(self._watchdog_loop()),
            asyncio.create_task(self._ping_loop()),
            asyncio.create_task(self._ipc_server_loop()),
            asyncio.create_task(self.pending_queue.run()),
            asyncio.create_task(self.converter_pool.run()),
        ]
        
        # Wait until shutdown
        await self._shutdown_event.wait()
        
    async def stop(self):
        """Stop service gracefully."""
        self._shutdown_event.set()
        
        # Cancel all tasks
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        
        # Cleanup
        if self.api:
            await self.api.__aexit__(None, None, None)
```

### 2.2 Async Converter Pool

```python
class AsyncConverterPool:
    """
    Async converter pool using asyncio.Queue and semaphore-limited workers.
    
    Benefits:
    - Single-threaded (no thread overhead)
    - Concurrent I/O via asyncio
    - Automatic backpressure via semaphore
    - Efficient batch processing
    """
    
    def __init__(self, config: ClientConfig, api: AsyncWATS, max_concurrent: int = 10):
        self.config = config
        self.api = api
        self._max_concurrent = max_concurrent
        self._queue: asyncio.Queue[ConversionItem] = asyncio.Queue()
        self._semaphore = asyncio.Semaphore(max_concurrent)
        
    async def run(self):
        """Main processing loop."""
        # Start file watchers
        await self._start_watchers()
        
        # Process queue with bounded concurrency
        while True:
            item = await self._queue.get()
            
            # Limit concurrent conversions
            async with self._semaphore:
                asyncio.create_task(self._process_item(item))
    
    async def _process_item(self, item: ConversionItem):
        """Process single conversion item."""
        try:
            item.state = ConversionItemState.PROCESSING
            
            # Read file (async I/O)
            async with aiofiles.open(item.file_path, 'r') as f:
                content = await f.read()
            
            # Convert
            report = await asyncio.to_thread(
                item.converter.convert, content
            )
            
            # Submit to WATS (async HTTP)
            await self.api.report.submit(report)
            
            item.state = ConversionItemState.COMPLETED
            
        except Exception as e:
            item.state = ConversionItemState.ERROR
            logger.error(f"Conversion failed: {e}")
```

### 2.3 Async Pending Queue with Concurrent Uploads

```python
class AsyncPendingQueue:
    """
    Async pending report queue with concurrent uploads.
    
    Benefits:
    - Uploads N reports concurrently (e.g., 5)
    - Uses asyncio.Semaphore for backpressure
    - Automatic retry with exponential backoff
    - Graceful shutdown (complete in-flight uploads)
    """
    
    def __init__(
        self, 
        api: AsyncWATS, 
        reports_dir: Path,
        max_concurrent: int = 5
    ):
        self.api = api
        self.reports_dir = reports_dir
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._stop_event = asyncio.Event()
        
    async def run(self):
        """Main queue processing loop."""
        # Watch for new files
        watcher_task = asyncio.create_task(self._watch_directory())
        
        # Periodic check (for error retries)
        timer_task = asyncio.create_task(self._periodic_check())
        
        await self._stop_event.wait()
        
        # Cleanup
        watcher_task.cancel()
        timer_task.cancel()
        
    async def submit_pending(self):
        """Submit all pending reports concurrently."""
        queued_files = sorted(
            self.reports_dir.glob("*.queued"),
            key=lambda p: p.stat().st_mtime
        )
        
        # Submit concurrently with semaphore limit
        tasks = [
            self._submit_with_limit(f) 
            for f in queued_files
        ]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _submit_with_limit(self, file_path: Path):
        """Submit single report with concurrency limit."""
        async with self._semaphore:
            await self._submit_report(file_path)
            
    async def _submit_report(self, file_path: Path):
        """Submit a single report file."""
        processing_path = file_path.with_suffix('.processing')
        
        try:
            # Atomic rename
            file_path.rename(processing_path)
            
            # Load report (async file I/O)
            async with aiofiles.open(processing_path, 'r') as f:
                report_data = json.loads(await f.read())
            
            # Submit to WATS (async HTTP!)
            await self.api.report.submit_raw(report_data)
            
            # Success
            processing_path.rename(processing_path.with_suffix('.completed'))
            
        except Exception as e:
            # Failed - mark for retry
            processing_path.rename(processing_path.with_suffix('.error'))
            logger.error(f"Submit failed: {file_path.name}: {e}")
```

### 2.4 GUI Integration with AsyncWATS

```python
# gui/pages/production.py (UPDATED)

class ProductionPage(BasePage):
    """Production page with proper async API calls."""
    
    def _get_async_api(self) -> Optional[AsyncWATS]:
        """Get AsyncWATS client from facade."""
        if self._facade and self._facade.has_api:
            return self._facade.async_api  # NEW: AsyncWATS instead of pyWATS
        return None
    
    def _on_lookup_unit(self):
        """Look up unit (async)."""
        serial = self._quick_serial.text()
        part = self._quick_part.text()
        
        if not serial or not part:
            return
        
        # Use existing AsyncTaskRunner with AsyncWATS!
        self.run_async(
            self._lookup_unit_async(serial, part),
            name=f"Looking up {serial}...",
            on_complete=self._on_unit_loaded,
            on_error=self._on_lookup_error,
            show_loading=True  # Shows loading indicator
        )
    
    async def _lookup_unit_async(self, serial: str, part: str):
        """Async unit lookup."""
        api = self._get_async_api()
        if not api:
            raise RuntimeError("Not connected to service")
        
        return await api.production.get_unit(serial, part)
    
    def _on_unit_loaded(self, result: TaskResult):
        """Handle successful unit lookup."""
        unit = result.result
        if unit:
            self._display_unit(unit)
        else:
            self.show_warning("Unit not found")
    
    def _on_lookup_error(self, result: TaskResult):
        """Handle lookup error."""
        self.handle_error(result.error, "looking up unit")
```

---

## Part 3: Migration Strategy

### Phase 1: Foundation (Week 1-2)

**Goal:** Create async infrastructure without breaking existing functionality.

1. **Create `AsyncClientService`** alongside existing `ClientService`
   - New file: `async_client_service.py`
   - Uses `AsyncWATS` with auto-discovery
   - Runs asyncio event loop with Qt integration

2. **Add async IPC commands**
   - Support both sync and async service backends
   - GUI doesn't need to know which is running

3. **Tests:**
   - Unit tests for AsyncClientService
   - Integration tests for async IPC

### Phase 2: Async Components (Week 3-4)

**Goal:** Create async versions of converter pool and pending watcher.

1. **Create `AsyncConverterPool`**
   - Async file watching
   - Semaphore-limited concurrent processing
   - Uses `asyncio.to_thread()` for CPU-bound converter code

2. **Create `AsyncPendingQueue`**
   - Concurrent report uploads
   - Async file I/O
   - Graceful shutdown

3. **Tests:**
   - Test concurrent conversions
   - Test queue with simulated failures
   - Performance benchmarks

### Phase 3: GUI Migration (Week 5-6)

**Goal:** Update GUI pages to use async API calls properly.

1. **Update `ServiceFacade`** to provide `async_api: AsyncWATS`

2. **Migrate pages one by one:**
   - production.py ✓
   - asset.py ✓
   - product.py ✓
   - rootcause.py ✓
   - software.py ✓
   - dashboard.py ✓

3. **Pattern:**
   ```python
   # OLD (blocking)
   result = client.domain.method()
   
   # NEW (async)
   self.run_async(
       self._async_method(),
       name="Loading...",
       on_complete=self._handle_result
   )
   ```

### Phase 4: Deprecation & Cleanup (Week 7-8)

1. **Add deprecation warnings** to sync ClientService
2. **Update documentation**
3. **Performance benchmarks** showing improvement
4. **Remove sync-only code paths** (optional, can keep for compatibility)

---

## Part 4: Implementation Details

### 4.1 asyncio + Qt Integration

The GUI uses Qt, which has its own event loop. We need to integrate asyncio:

**Option A: qasync (Recommended)**
```python
import qasync

class AsyncClientService:
    def run(self):
        app = QCoreApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)
        
        with loop:
            loop.run_until_complete(self.start())
```

**Option B: Separate Thread with Event Loop**
```python
class AsyncClientService:
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
    
    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()
```

### 4.2 Converter Threading Strategy

Converters do CPU-bound work (parsing files). Options:

**Option A: asyncio.to_thread() for CPU work**
```python
async def _process_item(self, item):
    # CPU-bound parsing in thread pool
    report = await asyncio.to_thread(
        item.converter.convert,
        item.file_content
    )
    # I/O-bound submission stays async
    await self.api.report.submit(report)
```

**Option B: ProcessPoolExecutor for heavy parsing**
```python
async def _process_item(self, item):
    loop = asyncio.get_event_loop()
    report = await loop.run_in_executor(
        self._process_pool,  # ProcessPoolExecutor
        item.converter.convert,
        item.file_content
    )
    await self.api.report.submit(report)
```

### 4.3 Graceful Shutdown

```python
class AsyncClientService:
    async def stop(self):
        """Graceful shutdown with timeout."""
        self._stopping = True
        
        # Signal components to stop
        await self.converter_pool.stop()
        await self.pending_queue.stop()
        
        # Wait for in-flight operations (with timeout)
        try:
            await asyncio.wait_for(
                self._wait_for_completion(),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            logger.warning("Shutdown timeout - forcing stop")
        
        # Cleanup
        await self.api.__aexit__(None, None, None)
```

---

## Part 5: Expected Benefits

### Performance Improvements

| Scenario | Current (Sync) | Proposed (Async) | Improvement |
|----------|---------------|------------------|-------------|
| Upload 100 reports | ~20s (sequential) | ~4s (5 concurrent) | **5x faster** |
| GUI responsiveness | Freezes during API calls | Always responsive | **UX improvement** |
| Memory (10 workers) | ~10MB (thread stacks) | ~1MB (single thread) | **10x less** |
| Context switches | High (thread scheduling) | Low (cooperative) | **Lower CPU** |
| Converter throughput | 1 file at a time per worker | N files concurrent I/O | **Higher throughput** |

### Code Quality Improvements

1. **Simpler concurrency model** - No locks for thread-safe access
2. **Better error handling** - Structured exception propagation
3. **Easier testing** - Can use `pytest-asyncio`
4. **Modern Python** - Uses async/await patterns

### Resource Usage

```
CURRENT (10 converter workers + threads):
- 10+ threads @ ~1MB stack each = 10MB+
- Thread context switching overhead
- Blocking I/O means threads wait idle

PROPOSED (async with semaphore):
- 1 event loop thread
- Semaphore limits concurrent operations
- Non-blocking I/O = efficient resource use
```

---

## Part 6: Risk Mitigation

### Risk 1: Breaking Existing Functionality

**Mitigation:**
- Keep sync `ClientService` as fallback
- Feature flag to choose async vs sync
- Extensive integration tests
- Gradual rollout (async opt-in first)

### Risk 2: Converter Compatibility

**Mitigation:**
- Converters stay synchronous (use `asyncio.to_thread`)
- No changes required to converter implementations
- Only the orchestration layer becomes async

### Risk 3: Qt + asyncio Integration Issues

**Mitigation:**
- Use proven `qasync` library
- Fallback to thread-based async runner
- Test on all platforms (Windows, Linux, macOS)

### Risk 4: Deadlocks/Starvation

**Mitigation:**
- Semaphores with sensible limits
- Timeouts on all operations
- Circuit breakers for failing endpoints
- Health monitoring detects stuck tasks

---

## Part 7: Success Metrics

1. **Queue drain time:** 100 reports from ~20s → ~4s
2. **GUI frame time:** No frames >100ms during API calls
3. **Memory usage:** Reduce peak memory by 50%+
4. **Thread count:** Reduce from 20+ to <5
5. **Test coverage:** Maintain >80% coverage

---

## Appendix: Files to Modify/Create

### New Files
- `src/pywats_client/service/async_client_service.py`
- `src/pywats_client/service/async_converter_pool.py`
- `src/pywats_client/service/async_pending_queue.py`
- `tests/client/test_async_client_service.py`
- `tests/client/test_async_converter_pool.py`
- `tests/client/test_async_pending_queue.py`

### Modified Files
- `src/pywats_client/service/__init__.py` - Export new async classes
- `src/pywats_client/gui/pages/*.py` - Use AsyncTaskRunner properly
- `src/pywats_client/gui/main_window.py` - Provide AsyncWATS to pages
- `src/pywats_client/__main__.py` - Support async service mode
- `requirements.txt` - Add `qasync`, `aiofiles`

### Documentation
- `docs/guides/client-architecture.md` - Update for async
- `CHANGELOG.md` - Document breaking changes

---

## Decision Needed

**Recommended approach:** Phase 1-4 implementation over 6-8 weeks

**Alternative:** Minimal change - just update GUI pages to use AsyncTaskRunner with existing AsyncWATS, keep service sync.

**Stakeholder input needed on:**
1. Timeline priority
2. Acceptable breaking changes
3. Fallback strategy (keep sync service?)
