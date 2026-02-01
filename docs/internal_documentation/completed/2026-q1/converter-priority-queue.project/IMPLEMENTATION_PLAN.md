# Implementation Plan: Converter Priority Queue

**Related Docs:**
- [README](README.md) | [Analysis](ANALYSIS.md) | [Progress](PROGRESS.md) | [TODO](TODO.md)

---

## Overview

Implement priority-based scheduling at the base QueueItem level, ensuring ALL queue implementations (MemoryQueue, PersistentQueue, AsyncPendingQueue, future uses) benefit from priority ordering.

**Key Principle:** One implementation, universal benefit.

---

## Phase 1: QueueItem Enhancement (8 hours)

### Step 1.1: Add Priority Field to QueueItem
**File:** `src/pywats/queue/memory_queue.py`  
**Action:**
```python
@dataclass
class QueueItem:
    id: str
    data: Any
    priority: int = 5  # NEW: 1=highest, 10=lowest, default=5 (backward compatible)
    status: QueueItemStatus = QueueItemStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    # ... rest unchanged
    
    def __lt__(self, other: "QueueItem") -> bool:
        """Compare by priority first, then timestamp (FIFO within priority)."""
        return (self.priority, self.created_at) < (other.priority, other.created_at)
```
**Verification:** Run `python -m pytest tests/cross_cutting/test_memory_queue.py -v`

### Step 1.2: Update QueueItem.create() Method
**File:** `src/pywats/queue/memory_queue.py`  
**Action:** Add `priority` parameter to factory method
```python
@classmethod
def create(
    cls,
    data: Any,
    item_id: Optional[str] = None,
    priority: int = 5,  # NEW
    max_attempts: int = 3,
    metadata: Optional[Dict[str, Any]] = None,
) -> "QueueItem":
    return cls(
        id=item_id or str(uuid.uuid4()),
        data=data,
        priority=priority,  # NEW
        max_attempts=max_attempts,
        metadata=metadata or {},
    )
```
**Verification:** Check docstring updates, run type checker

### Step 1.3: Write QueueItem Priority Tests
**File:** `tests/cross_cutting/test_queue_priority.py` (NEW)  
**Action:** Create comprehensive tests for QueueItem priority
```python
def test_queue_item_default_priority():
    """Test default priority is 5"""
    item = QueueItem.create(data={"test": "data"})
    assert item.priority == 5

def test_queue_item_custom_priority():
    """Test custom priority values"""
    item = QueueItem.create(data={}, priority=1)
    assert item.priority == 1

def test_queue_item_comparison_by_priority():
    """Test items sort by priority"""
    high = QueueItem.create(data={}, priority=1)
    low = QueueItem.create(data={}, priority=10)
    assert high < low

def test_queue_item_fifo_within_priority():
    """Test FIFO ordering within same priority"""
    import time
    first = QueueItem.create(data={}, priority=5)
    time.sleep(0.001)
    second = QueueItem.create(data={}, priority=5)
    assert first < second
```
**Verification:** `pytest tests/cross_cutting/test_queue_priority.py -v`

---

## Phase 2: MemoryQueue Priority Implementation (16 hours)

### Step 2.1: Replace Deque with Heap
**File:** `src/pywats/queue/memory_queue.py`  
**Action:**
```python
import heapq  # ADD

class MemoryQueue(BaseQueue):
    def __init__(self, max_size: Optional[int] = None, default_max_attempts: int = 3):
        self._items: Dict[str, QueueItem] = {}
        self._heap: List[QueueItem] = []  # CHANGED from deque
        self._lock = threading.RLock()
        self._max_size = max_size
        self._default_max_attempts = default_max_attempts
        self._item_added_event = asyncio.Event()
```
**Verification:** Check all references to `self._order` are updated

### Step 2.2: Update add() Method
**File:** `src/pywats/queue/memory_queue.py`  
**Action:**
```python
def add(
    self,
    data: Any,
    item_id: Optional[str] = None,
    priority: int = 5,  # NEW parameter
    max_attempts: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> QueueItem:
    with self._lock:
        if self._max_size and len(self._items) >= self._max_size:
            raise QueueFullError(...)
        
        item = QueueItem.create(
            data=data,
            item_id=item_id,
            priority=priority,  # NEW
            max_attempts=max_attempts or self._default_max_attempts,
            metadata=metadata,
        )
        
        self._items[item.id] = item
        heapq.heappush(self._heap, item)  # CHANGED: heappush instead of append
        
        # Signal async waiters
        try:
            self._item_added_event.set()
        except:
            pass
        
        logger.debug(f"Added item {item.id} to queue with priority {priority}")
        return item
```
**Verification:** Test adding items with various priorities

### Step 2.3: Update get_next() Method with Lazy Cleanup
**File:** `src/pywats/queue/memory_queue.py`  
**Action:**
```python
def get_next(self) -> Optional[QueueItem]:
    """
    Get the next pending item for processing (priority order).
    
    Uses lazy cleanup: pops from heap, checks if valid and pending.
    Invalid/non-pending items are discarded from heap.
    
    Returns:
        Next pending QueueItem or None if queue is empty
    """
    with self._lock:
        while self._heap:
            item = heapq.heappop(self._heap)
            
            # Check if item still exists and is pending
            current_item = self._items.get(item.id)
            if current_item and current_item.status == QueueItemStatus.PENDING:
                # Item is valid and pending, return it
                # Note: We don't re-add to heap since it's being processed
                return current_item
            
            # Item was removed or status changed, continue to next
        
        return None
```
**Verification:** Test that only pending items are returned in priority order

### Step 2.4: Handle update() Method
**File:** `src/pywats/queue/memory_queue.py`  
**Action:** When item status changes from PENDING to something else, no heap removal needed (lazy cleanup handles it)
```python
def update(self, item: QueueItem) -> None:
    """Update an item's status in the queue."""
    with self._lock:
        if item.id not in self._items:
            raise KeyError(f"Item {item.id} not found in queue")
        
        item.updated_at = datetime.now()
        self._items[item.id] = item
        
        # If item is back to PENDING (e.g., retry), re-add to heap
        if item.status == QueueItemStatus.PENDING:
            heapq.heappush(self._heap, item)
        
        logger.debug(f"Updated item {item.id} status to {item.status}")
```
**Verification:** Test status transitions, especially failed → pending (retry)

### Step 2.5: Write MemoryQueue Priority Tests
**File:** `tests/cross_cutting/test_memory_queue_priority.py` (NEW)  
**Action:** 15+ tests for priority queue behavior
```python
def test_priority_ordering():
    """Items dequeued in priority order"""
    queue = MemoryQueue()
    queue.add("low", priority=10)
    queue.add("high", priority=1)
    queue.add("medium", priority=5)
    
    assert queue.get_next().data == "high"
    assert queue.get_next().data == "medium"
    assert queue.get_next().data == "low"

def test_fifo_within_priority():
    """Same priority uses FIFO"""
    queue = MemoryQueue()
    item1 = queue.add("first", priority=5)
    item2 = queue.add("second", priority=5)
    
    assert queue.get_next().id == item1.id
    assert queue.get_next().id == item2.id

def test_lazy_cleanup_removes_completed():
    """Completed items not returned by get_next"""
    queue = MemoryQueue()
    item = queue.add("test", priority=5)
    item.mark_completed()
    queue.update(item)
    
    assert queue.get_next() is None

def test_retry_re_adds_to_heap():
    """Failed → Pending re-adds to heap with original priority"""
    queue = MemoryQueue()
    item = queue.add("test", priority=2)
    item.mark_failed("error")
    queue.update(item)
    
    item.status = QueueItemStatus.PENDING
    queue.update(item)
    
    assert queue.get_next().id == item.id
```
**Verification:** `pytest tests/cross_cutting/test_memory_queue_priority.py -v`

---

## Phase 3: PersistentQueue Priority Support (8 hours)

### Step 3.1: Update File Serialization
**File:** `src/pywats_client/queue/persistent_queue.py`  
**Action:** Include priority in metadata JSON
```python
def add(self, data: Any, priority: int = 5, **kwargs) -> QueueItem:
    """Add item to persistent queue with priority"""
    item = super().add(data, priority=priority, **kwargs)
    
    # Save metadata with priority
    meta_file = self._get_meta_path(item.id)
    meta = {
        "id": item.id,
        "priority": item.priority,  # NEW
        "status": item.status.value,
        "created_at": item.created_at.isoformat(),
        "attempts": item.attempts,
        "max_attempts": item.max_attempts,
        "metadata": item.metadata,
    }
    meta_file.write_text(json.dumps(meta, indent=2))
    
    return item
```
**Verification:** Check files on disk include priority field

### Step 3.2: Load Priority from Metadata
**File:** `src/pywats_client/queue/persistent_queue.py`  
**Action:** Read priority when loading from disk
```python
def _load_item_from_file(self, file_path: Path) -> Optional[QueueItem]:
    """Load queue item from file with priority"""
    meta_file = file_path.with_suffix(".meta.json")
    if not meta_file.exists():
        # Migration: old files without metadata get default priority
        priority = 5
    else:
        meta = json.loads(meta_file.read_text())
        priority = meta.get("priority", 5)  # Default if missing
    
    # ... load data ...
    
    return QueueItem.create(
        data=data,
        item_id=item_id,
        priority=priority,  # NEW
        # ... rest
    )
```
**Verification:** Test loading old files (backward compatibility)

### Step 3.3: Write PersistentQueue Tests
**File:** `tests/client/test_persistent_queue_priority.py` (NEW)  
**Action:** Test file persistence with priority
**Verification:** `pytest tests/client/test_persistent_queue_priority.py -v`

---

## Phase 4: AsyncPendingQueue Priority (12 hours)

### Step 4.1: Add Priority Metadata Files
**File:** `src/pywats_client/service/async_pending_queue.py`  
**Action:** Create `.meta.json` alongside `.queued` files
```python
async def _queue_report(self, report_file: Path, priority: int = 5) -> None:
    """Queue a report with priority metadata"""
    # Create metadata file
    meta_file = report_file.with_suffix(".meta.json")
    meta = {
        "priority": priority,
        "queued_at": datetime.now().isoformat(),
    }
    
    if HAS_AIOFILES:
        async with aiofiles.open(meta_file, 'w') as f:
            await f.write(json.dumps(meta))
    else:
        meta_file.write_text(json.dumps(meta))
    
    # Rename to .queued (triggers watchdog)
    queued_file = report_file.with_suffix(".queued")
    report_file.rename(queued_file)
```
**Verification:** Check metadata files created on disk

### Step 4.2: Sort by Priority in submit_all_pending()
**File:** `src/pywats_client/service/async_pending_queue.py`  
**Action:**
```python
async def submit_all_pending(self) -> None:
    """Submit all pending (.queued) reports by priority"""
    queued_files = []
    
    for file in self.reports_dir.glob(self.FILTER_QUEUED):
        # Read priority from metadata
        meta_file = file.with_suffix(".meta.json")
        priority = 5  # default
        timestamp = file.stat().st_mtime
        
        if meta_file.exists():
            try:
                if HAS_AIOFILES:
                    async with aiofiles.open(meta_file, 'r') as f:
                        content = await f.read()
                        meta = json.loads(content)
                else:
                    meta = json.loads(meta_file.read_text())
                priority = meta.get("priority", 5)
                queued_at = meta.get("queued_at")
                if queued_at:
                    timestamp = datetime.fromisoformat(queued_at).timestamp()
            except Exception as e:
                logger.warning(f"Failed to read metadata for {file}: {e}")
        
        queued_files.append((priority, timestamp, file))
    
    if not queued_files:
        return
    
    # Sort by priority (lower=higher), then timestamp (FIFO within priority)
    queued_files.sort(key=lambda x: (x[0], x[1]))
    
    logger.info(f"Submitting {len(queued_files)} queued reports (priority order)...")
    
    tasks = [
        asyncio.create_task(self._submit_with_limit(f))
        for priority, timestamp, f in queued_files
    ]
    
    for task in tasks:
        self._active_uploads.add(task)
        task.add_done_callback(lambda t: self._active_uploads.discard(t))
    
    await asyncio.gather(*tasks, return_exceptions=True)
```
**Verification:** Test reports submitted in priority order

### Step 4.3: Add Priority Parameter to API
**File:** `src/pywats_client/service/async_client_service.py`  
**Action:** Add priority to report submission methods
```python
async def submit_report(
    self,
    report: Union[UUTReport, UURReport],
    priority: int = 5,  # NEW
    queue_if_offline: bool = True,
) -> SubmitResponse:
    """Submit report with priority for queue"""
    # If queuing, pass priority to pending queue
    if queue_if_offline and not await self._is_online():
        await self._queue.queue_report(report, priority=priority)
    
    # ... rest
```
**Verification:** Test API accepts priority parameter

### Step 4.4: Write AsyncPendingQueue Tests
**File:** `tests/client/test_async_pending_queue_priority.py` (NEW)  
**Action:** 10+ tests for priority ordering in file-based queue
**Verification:** `pytest tests/client/test_async_pending_queue_priority.py -v`

---

## Phase 5: Priority Aging (Anti-Starvation) (10 hours)

### Step 5.1: Add Aging Configuration
**File:** `src/pywats/core/config.py`  
**Action:**
```python
@dataclass
class QueueConfig:
    """Queue configuration including priority aging"""
    enable_priority: bool = True
    default_priority: int = 5
    
    # Priority aging (anti-starvation)
    enable_aging: bool = True
    aging_threshold_seconds: int = 300  # 5 minutes
    aging_boost: int = 1  # Boost priority by 1 per threshold
    max_priority_boost: int = 4  # Max boost (priority can't go below 1)
```
**Verification:** Config loads correctly

### Step 5.2: Implement Aging in MemoryQueue
**File:** `src/pywats/queue/memory_queue.py`  
**Action:**
```python
def get_next(self, apply_aging: bool = True) -> Optional[QueueItem]:
    """Get next item with optional aging"""
    with self._lock:
        while self._heap:
            item = heapq.heappop(self._heap)
            current_item = self._items.get(item.id)
            
            if current_item and current_item.status == QueueItemStatus.PENDING:
                # Apply aging if enabled
                if apply_aging:
                    age_seconds = (datetime.now() - current_item.created_at).total_seconds()
                    if age_seconds > AGING_THRESHOLD:
                        boost = min(int(age_seconds / AGING_THRESHOLD), MAX_BOOST)
                        aged_priority = max(1, current_item.priority - boost)
                        if aged_priority != current_item.priority:
                            logger.info(
                                f"Item {current_item.id} aged: "
                                f"priority {current_item.priority} → {aged_priority}"
                            )
                            current_item.priority = aged_priority
                            # Re-add with boosted priority
                            heapq.heappush(self._heap, current_item)
                            continue
                
                return current_item
        
        return None
```
**Verification:** Test aging boosts priority over time

### Step 5.3: Write Aging Tests
**File:** `tests/cross_cutting/test_queue_aging.py` (NEW)  
**Action:** Test aging prevents starvation
**Verification:** `pytest tests/cross_cutting/test_queue_aging.py -v`

---

## Phase 6: Documentation & Examples (8 hours)

### Step 6.1: Create Priority Queue Guide
**File:** `docs/guides/queue-priority.md` (NEW)  
**Action:** Comprehensive guide with examples
**Verification:** Review guide for clarity

### Step 6.2: Create Examples
**File:** `examples/queue_priority_example.py` (NEW)  
**Action:** Demonstrate priority usage
**Verification:** Run example successfully

### Step 6.3: Update Existing Docs
**Files:** Various docs mentioning queues  
**Action:** Add priority information
**Verification:** Search for "queue" in docs, update references

---

## Testing Strategy

**Unit Tests (45 tests):**
- QueueItem priority comparison: 8 tests
- MemoryQueue priority ordering: 15 tests
- PersistentQueue priority persistence: 10 tests
- AsyncPendingQueue priority: 10 tests
- Aging mechanism: 8 tests

**Integration Tests (10 tests):**
- End-to-end priority flow: 5 tests
- Backward compatibility: 5 tests

**Performance Tests:**
- Heap operations overhead: < 10% vs FIFO
- Large queue (10,000 items): < 1s to add, < 100ms to get_next

---

## Rollback Plan

If critical issues discovered:
1. Set `enable_priority = False` in config (falls back to FIFO)
2. Revert QueueItem changes (remove priority field)
3. Restore deque-based implementation
4. Remove new test files

Git revert points:
- Before Phase 1: QueueItem unchanged
- Before Phase 2: MemoryQueue uses deque
- Before Phase 4: AsyncPendingQueue no metadata

---

## Success Criteria

- [ ] All existing tests pass (1570+ tests)
- [ ] 55 new priority tests passing
- [ ] Backward compatibility: default priority=5, old items work
- [ ] Performance: < 10% overhead
- [ ] Documentation complete
- [ ] Examples working
- [ ] Type stubs generated

---

**Estimated Total:** 62 hours (1.5-2 weeks)  
**Critical Path:** Phase 2 (MemoryQueue) blocks Phase 3 (PersistentQueue)  
**Ready to Implement:** ✅ All phases clearly defined