# Analysis: Converter Priority Queue

**Related Docs:**
- [README](README.md) | [Plan](IMPLEMENTATION_PLAN.md) | [Progress](PROGRESS.md) | [TODO](TODO.md)

---

## Problem Statement

Currently, all queue systems in pyWATS use FIFO (First-In-First-Out) scheduling. This affects:
1. **AsyncPendingQueue**: Report uploads (file-based, 5 concurrent)
2. **MemoryQueue**: Base queue for report submission (in-memory)
3. **PersistentQueue**: File-backed extension of MemoryQueue
4. **Any future queue uses**: All inherit FIFO behavior

Without priority support, critical operations must wait behind bulk/low-priority operations, leading to resource contention and poor user experience.

---

## Requirements

### Functional
- Priority queue ordering at the base QueueItem level (affects all implementations)
- Integer priority field (1=highest, 10=lowest)
- FIFO within same priority (timestamp tiebreaker)
- Default priority = 5 (backward compatible)
- Priority visible in logs, metrics, status
- Anti-starvation mechanism (aging)

### Non-Functional
- **Performance**: O(log n) heap operations (heapq)
- **Compatibility**: Existing code works without changes (default priority=5)
- **Thread Safety**: Maintain existing thread-safety in MemoryQueue
- **Async Safe**: Compatible with AsyncPendingQueue's asyncio usage

### Use Cases
1. **Report Uploads** (AsyncPendingQueue): Critical reports bypass bulk uploads
2. **Converter Queue** (Future CFX): High-priority conversions run first
3. **General Queuing**: Any system using MemoryQueue/PersistentQueue benefits

---

## Constraints

### Technical Limitations
1. **Type Stub Generation**: Cannot manually modify .pyi files - changes must be in source
2. **BaseQueue Interface**: Changes must maintain ABC compatibility
3. **File Format**: PersistentQueue must serialize priority field
4. **AsyncPendingQueue**: File-based (not using MemoryQueue directly), needs special handling

### Breaking Change Considerations
- **MUST BE BACKWARD COMPATIBLE**: Default priority=5, existing items work unchanged
- QueueItem dataclass changes require careful migration
- File format changes in PersistentQueue need version handling
- AsyncPendingQueue uses file extensions (.queued, .processing) - must preserve

---

## Research Findings

### Current Architecture

**Queue Hierarchy:**
```
BaseQueue (ABC)                     # Abstract interface
    ├── MemoryQueue                 # In-memory FIFO queue with deque
    │   └── PersistentQueue         # Extends MemoryQueue with file storage
    └── AsyncPendingQueue           # File-based report queue (NOT using MemoryQueue)
```

**Key Discovery:** AsyncPendingQueue is NOT a subclass of MemoryQueue! It's a separate file-based implementation.

### QueueItem Current Structure
```python
@dataclass
class QueueItem:
    id: str
    data: Any
    status: QueueItemStatus
    created_at: datetime
    updated_at: datetime
    attempts: int = 0
    max_attempts: int = 3
    last_error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### MemoryQueue Current Implementation
- Uses `deque` for FIFO ordering: `self._order: deque = deque()`
- `get_next()` iterates `_order` to find first pending item
- Thread-safe with `threading.RLock()`

### AsyncPendingQueue Current Implementation
- Uses file extensions for state: `.queued`, `.processing`, `.error`, `.completed`
- Sorts by modification time: `sorted(..., key=lambda p: p.stat().st_mtime)`
- No MemoryQueue integration - would need separate priority implementation

---

## Architecture Impact

### Approach: Base-Level Priority (Recommended)

**Add priority to QueueItem** - affects all implementations:

1. **MemoryQueue Changes:**
   - Replace `deque` with `heapq` for priority ordering
   - Implement `__lt__` in QueueItem for heap comparisons
   - Add timestamp to QueueItem for FIFO within priority

2. **PersistentQueue Changes:**
   - Update file serialization to include priority
   - Migration: add priority=5 to existing .pending.wsjf files

3. **AsyncPendingQueue Changes:**
   - Add priority to filename: `{name}.priority-{N}.queued`
   - Sort by priority, then timestamp
   - OR: Store priority in metadata JSON file alongside report

4. **Converter System (Future):**
   - Add priority parameter to converter API
   - Pass priority through to queue

---

## Solution Design

### Phase 1: QueueItem Enhancement

```python
@dataclass
class QueueItem:
    id: str
    data: Any
    priority: int = 5  # NEW: 1=highest, 10=lowest
    status: QueueItemStatus = QueueItemStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    attempts: int = 0
    max_attempts: int = 3
    last_error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __lt__(self, other: "QueueItem") -> bool:
        """Compare by priority, then timestamp (FIFO within priority)."""
        return (self.priority, self.created_at) < (other.priority, other.created_at)
```

### Phase 2: MemoryQueue Priority Implementation

```python
class MemoryQueue(BaseQueue):
    def __init__(self, ...):
        self._items: Dict[str, QueueItem] = {}
        self._heap: List[QueueItem] = []  # CHANGED: heapq instead of deque
        self._lock = threading.RLock()
    
    def add(self, data, priority: int = 5, ...) -> QueueItem:
        item = QueueItem.create(data, priority=priority, ...)
        with self._lock:
            self._items[item.id] = item
            heapq.heappush(self._heap, item)  # CHANGED: heappush
        return item
    
    def get_next(self) -> Optional[QueueItem]:
        with self._lock:
            # Find first pending item in heap
            while self._heap:
                item = heapq.heappop(self._heap)  # CHANGED: heappop
                if item.id in self._items and item.status == QueueItemStatus.PENDING:
                    # Re-add non-pending items back to heap
                    heapq.heappush(self._heap, item)
                    return item
        return None
```

**Problem:** Heap contains ALL items (pending, processing, completed). Need to handle item removal from heap when status changes.

**Better Approach:** Separate heaps for each status or lazy cleanup.

### Phase 3: AsyncPendingQueue Priority

**Option A: Filename-based Priority**
```
report_{uuid}.priority-3.queued  # High priority
report_{uuid}.priority-8.queued  # Low priority
```

**Option B: Metadata File** (Recommended - cleaner)
```
report_{uuid}.queued          # Report file
report_{uuid}.meta.json       # {"priority": 3, "created_at": "..."}
```

**Implementation:**
```python
async def submit_all_pending(self):
    queued_files = []
    for file in self.reports_dir.glob(self.FILTER_QUEUED):
        meta_file = file.with_suffix(".meta.json")
        priority = 5  # default
        if meta_file.exists():
            meta = json.loads(meta_file.read_text())
            priority = meta.get("priority", 5)
        queued_files.append((priority, file.stat().st_mtime, file))
    
    # Sort by priority, then mtime
    queued_files.sort(key=lambda x: (x[0], x[1]))
    
    for priority, mtime, file in queued_files:
        await self._submit_with_limit(file)
```

---

## Risk Assessment

### HIGH Risks
- **Heap management complexity**: Removing items from heap when status changes is tricky
- **AsyncPendingQueue not using MemoryQueue**: Separate implementation needed
- **Backward compatibility**: Existing queued items, file formats, tests

### MEDIUM Risks
- **Performance**: Heap operations add overhead (but O(log n) is acceptable)
- **Migration**: Need to handle old queue items without priority field
- **Testing**: Complex edge cases (aging, same priority, starvation)

### LOW Risks
- **Type stubs**: Auto-generated, just need to run script
- **API changes**: Adding optional priority parameter is backward compatible

---

## Mitigation Strategies

1. **Heap Complexity**: Use lazy cleanup approach - remove from heap when popped, check if still valid
2. **AsyncPendingQueue**: Use metadata files for priority storage
3. **Migration**: Default priority=5 for all existing items, add in QueueItem.__post_init__
4. **Testing**: Comprehensive unit tests for all priority scenarios

---

## Open Questions

1. **Should AsyncPendingQueue use MemoryQueue?**  
   - NO - it's file-based, refactoring would be major change
   - DECISION: Add priority separately to AsyncPendingQueue

2. **How to handle heap removal when item status changes?**  
   - OPTION A: Lazy cleanup (check validity when popping)
   - OPTION B: Separate heaps per status
   - DECISION: Lazy cleanup is simpler

3. **Priority aging rate?**  
   - PROPOSAL: +1 priority boost per 5 minutes waiting
   - CONFIGURABLE: aging_threshold_seconds, aging_boost

---

## Success Metrics

- All existing tests pass (backward compatibility)
- New priority tests: 100% passing
- Performance: < 10% overhead vs current FIFO
- High-priority items processed first: 100% of cases
- No starvation: Low-priority items run within max_age threshold

---

**Analysis Complete:** Ready to create implementation plan
**Estimated Complexity:** HIGH - touches core queue infrastructure  
**Estimated Duration:** 2-3 weeks (80-120 hours)