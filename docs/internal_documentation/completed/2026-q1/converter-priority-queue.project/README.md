# Converter Priority Queue

**Project ID:** converter-priority-queue  
**Sprint Size:** 1-2 weeks  
**Priority:** Medium  
**Status:** Ready to Start  

---

## 🎯 Goal

Add priority-based scheduling to the converter queue system, allowing high-priority conversions to run before low-priority ones.

---

## 📋 Problem Statement

**Current Behavior:**
The converter queue uses **FIFO (First-In-First-Out)** scheduling. All converters are treated equally regardless of urgency or importance.

**Issues:**
1. **No urgency control** - Critical conversions wait behind non-critical ones
2. **Resource contention** - Important work can be delayed by bulk operations
3. **No user control** - Cannot prioritize specific converters or conversion types
4. **Queue starvation risk** - Low-priority items might never run if queue stays full

**Example Scenario:**
```
Queue: [Bulk CSV (100 files), Important XML (1 file)]
         ↑                      ↑
         Runs first            Waits unnecessarily
```

**Desired:**
```
Queue: [Important XML (priority=1), Bulk CSV (priority=5)]
         ↑                           ↑
         Runs first                  Runs after high-priority
```

---

## ✅ Acceptance Criteria

**Must Have:**
- [ ] Queue items have integer priority field (1=highest, 10=lowest)
- [ ] Queue processes items by priority (highest first)
- [ ] Default priority is 5 (medium) for backward compatibility
- [ ] API to set converter-specific default priorities
- [ ] API to override priority per conversion request
- [ ] Low-priority items eventually run (no starvation)

**Should Have:**
- [ ] Priority visible in queue status/logs
- [ ] Metrics track priority distribution
- [ ] Configuration for max queue size per priority level
- [ ] Documentation on priority best practices

**Nice to Have:**
- [ ] Dynamic priority adjustment (aging)
- [ ] Priority-based timeout values
- [ ] Priority presets (CRITICAL, HIGH, NORMAL, LOW, BULK)

---

## 🏗️ Solution Architecture

### Priority Queue Implementation

**Replace FIFO queue with priority queue:**

```python
# Current (FIFO)
from collections import deque
queue = deque()  # First in, first out

# Proposed (Priority Queue)
import heapq
queue = []  # Min-heap: lowest priority value = highest priority
```

**Queue Item Structure:**
```python
@dataclass
class QueueItem:
    priority: int = 5  # NEW: 1=highest, 10=lowest
    timestamp: float = field(default_factory=time.time)  # For FIFO within same priority
    converter_type: str
    input_path: Path
    output_path: Path
    config: Dict[str, Any]
    
    def __lt__(self, other):
        # Compare by priority first, then timestamp (FIFO within priority)
        return (self.priority, self.timestamp) < (other.priority, other.timestamp)
```

### API Design

**Set default priority per converter:**
```python
# In converter config or registration
@converter(name="xml_to_json", priority=2)  # High priority
def xml_converter(...):
    pass

@converter(name="bulk_csv", priority=7)  # Lower priority
def bulk_csv_converter(...):
    pass
```

**Override priority per request:**
```python
# Client API
client.convert(
    file="important.xml",
    converter="xml_to_json",
    priority=1  # Override default, make this urgent
)

# Bulk operation with low priority
client.convert_batch(
    files=[...],
    converter="csv_to_json",
    priority=8  # Don't block other work
)
```

---

## 📊 Work Breakdown

**Total Estimate:** 40-60 hours (1-2 weeks)

### Phase 1: Queue Infrastructure (12 hours)

**Task 1.1: Update QueueItem Model (3 hours)**
- Add `priority: int` field to QueueItem dataclass
- Add `timestamp: float` for FIFO within same priority
- Implement `__lt__` for heap comparisons
- Update serialization/deserialization

**Task 1.2: Replace FIFO with Priority Queue (5 hours)**
- Replace `collections.deque` with `heapq`
- Update `enqueue()` to use `heapq.heappush()`
- Update `dequeue()` to use `heapq.heappop()`
- Maintain thread-safety with existing locks
- Test priority ordering

**Task 1.3: Default Priority Handling (4 hours)**
- Set default priority = 5 for all items
- Ensure backward compatibility (old items get default)
- Update queue persistence to include priority
- Migration for existing queued items

---

### Phase 2: API Integration (16 hours)

**Task 2.1: Converter Registration with Priority (4 hours)**
- Add `priority` parameter to `@converter` decorator
- Store default priority in converter registry
- Update converter metadata model

**Task 2.2: Client API Enhancements (6 hours)**
- Add `priority` parameter to `convert()` method
- Add `priority` parameter to `convert_batch()` method
- Priority validation (1-10 range)
- Update API documentation

**Task 2.3: IPC Protocol Updates (6 hours)**
- Add priority field to IPC conversion requests
- Update protocol versioning
- Backward compatibility with old clients
- Test IPC priority propagation

---

### Phase 3: Anti-Starvation & Fairness (8 hours)

**Task 3.1: Priority Aging (5 hours)**
- Implement age-based priority boost
- Items waiting > threshold get priority bump
- Configurable aging rate (e.g., +1 priority per 5 minutes)
- Prevent starvation of low-priority items

**Task 3.2: Priority Limits (3 hours)**
- Max queue size per priority level
- Reject new low-priority items if queue full
- Metrics for rejected items by priority

---

### Phase 4: Observability (8 hours)

**Task 4.1: Metrics & Monitoring (4 hours)**
- Track queue size by priority level
- Track processing time by priority
- Track starvation events (aging triggers)
- Expose via health endpoint

**Task 4.2: Logging & Debugging (4 hours)**
- Log priority in queue operations
- Log priority changes (aging)
- Debug endpoint showing priority distribution
- Visual queue status in GUI

---

### Phase 5: Testing & Documentation (16 hours)

**Task 5.1: Unit Tests (6 hours)**
- Test priority ordering
- Test FIFO within same priority
- Test default priority
- Test priority validation

**Task 5.2: Integration Tests (6 hours)**
- Test end-to-end priority flow
- Test aging mechanism
- Test starvation prevention
- Test backward compatibility

**Task 5.3: Documentation (4 hours)**
- Update converter development guide
- Add priority best practices
- Document priority API
- Add examples

---

## 📂 Files Involved

**Core Queue System:**
- `src/pywats_cfx/queue/queue_item.py` - Add priority field
- `src/pywats_cfx/queue/priority_queue.py` - New priority queue implementation
- `src/pywats_cfx/queue/async_pending_queue.py` - Update to use priority queue

**Converter Framework:**
- `src/pywats_cfx/converter_decorator.py` - Add priority parameter
- `src/pywats_cfx/converter_registry.py` - Store default priorities

**Client API:**
- `src/pywats_client/converter_client.py` - Add priority to convert() methods
- `src/pywats_client/ipc/protocol.py` - Update IPC protocol

**Configuration:**
- `src/pywats_cfx/config.py` - Add priority config options

**Tests:**
- `tests/cfx/test_priority_queue.py` (NEW - 200 lines)
- `tests/cfx/test_priority_aging.py` (NEW - 150 lines)
- `tests/integration/test_converter_priority.py` (NEW - 200 lines)

**Documentation:**
- `docs/guides/converter-development.md` - Update with priority guide
- `examples/converters/priority_example.py` (NEW)

---

## 🧪 Testing Strategy

**Unit Tests:**
```python
def test_priority_ordering():
    """High priority items dequeued first."""
    queue.enqueue(QueueItem(priority=5, data="medium"))
    queue.enqueue(QueueItem(priority=1, data="high"))
    queue.enqueue(QueueItem(priority=10, data="low"))
    
    assert queue.dequeue().data == "high"
    assert queue.dequeue().data == "medium"
    assert queue.dequeue().data == "low"

def test_fifo_within_priority():
    """Same priority uses FIFO."""
    queue.enqueue(QueueItem(priority=5, data="first"))
    queue.enqueue(QueueItem(priority=5, data="second"))
    
    assert queue.dequeue().data == "first"
    assert queue.dequeue().data == "second"

def test_aging_prevents_starvation():
    """Low priority items eventually get boosted."""
    item = QueueItem(priority=10, timestamp=time.time() - 600)
    aged_priority = apply_aging(item, age_threshold=300, boost=1)
    
    assert aged_priority < 10  # Priority improved
```

**Integration Tests:**
```python
def test_high_priority_converter_runs_first():
    """High priority converter preempts normal priority."""
    # Queue low-priority bulk job
    client.convert_batch(files=[...], priority=8)
    
    # Queue high-priority urgent job
    client.convert(file="urgent.xml", priority=1)
    
    # Verify urgent runs first
    assert next_processed() == "urgent.xml"
```

---

## 🎯 Priority Guidelines

**Recommended Priority Levels:**

| Priority | Use Case | Examples |
|----------|----------|----------|
| **1-2 (CRITICAL)** | Production-blocking, time-sensitive | Real-time data ingestion, live dashboards |
| **3-4 (HIGH)** | Important but not urgent | User-requested conversions, reports |
| **5 (NORMAL)** | Default priority | Standard conversions |
| **6-7 (LOW)** | Background work, non-urgent | Cleanup, archival, optimization |
| **8-10 (BULK)** | Batch operations, off-hours | Large imports, data migrations |

**Best Practices:**
- Use priority=5 (default) unless you have a specific reason
- Reserve priority 1-2 for truly critical work
- Use priority 8-10 for bulk operations to avoid blocking others
- Document why a converter has non-default priority

---

## 🚨 Risks & Mitigations

### Risk 1: Queue Starvation
**Problem:** Low-priority items never run if queue stays full of high-priority work.

**Mitigation:**
- Implement aging: items gain priority over time
- Max items per priority level
- Monitoring/alerting for aged items

### Risk 2: Priority Abuse
**Problem:** Users set everything to priority=1.

**Mitigation:**
- Document priority guidelines
- Monitoring for priority distribution
- Consider requiring justification for priority < 3
- Rate limiting per priority level

### Risk 3: Backward Compatibility
**Problem:** Existing clients/converters don't set priority.

**Mitigation:**
- Default priority = 5 (medium)
- Existing queue items migrated with default priority
- Protocol versioning ensures compatibility

---

## 🔗 Dependencies

**Blocked By:** None  
**Blocks:** None

**Related Systems:**
- Converter queue (major changes)
- IPC protocol (minor version bump)
- Client API (new parameter)

---

## 📈 Success Metrics

**Functional:**
- [ ] Priority ordering works correctly (100% of test cases)
- [ ] No starvation events in production
- [ ] Backward compatible (existing converters work)
- [ ] All priority levels used appropriately

**Performance:**
- [ ] Priority queue operations O(log n) (heap operations)
- [ ] No performance regression on queue throughput
- [ ] High-priority items start < 5s after submission

**Usage:**
- [ ] 80% of items use default priority (5)
- [ ] < 10% of items use priority 1-2 (critical)
- [ ] Clear priority distribution in metrics

---

## 🔄 Migration Plan

**Phase 1: Add Priority (Backward Compatible)**
- Add priority field with default=5
- Existing items get default priority
- Queue behavior unchanged (all same priority)

**Phase 2: Enable Priority (Opt-In)**
- Document priority feature
- Let early adopters set priorities
- Monitor for issues

**Phase 3: Full Rollout**
- Update all internal converters with appropriate priorities
- Enable aging to prevent starvation
- Remove FIFO-only mode

---

## 📝 Configuration

**New Config Options:**
```python
[converter_queue]
# Priority queue settings
enable_priority_queue = true
default_priority = 5
priority_aging_enabled = true
priority_aging_threshold_seconds = 300  # 5 minutes
priority_aging_boost = 1  # Boost priority by 1 per threshold

# Per-priority limits
max_queue_size_priority_1_2 = 100   # Critical
max_queue_size_priority_3_5 = 500   # Normal
max_queue_size_priority_6_10 = 1000 # Low/Bulk
```

---

## 📚 References

**Related Documents:**
- Original analysis: `sync-wrapper-enhancements.project/ORIGINAL_STAGE_4_ANALYSIS.md`
- Queue implementation: `src/pywats_cfx/queue/async_pending_queue.py`
- Converter framework: `src/pywats_cfx/converter_decorator.py`

**External Resources:**
- Python heapq documentation: https://docs.python.org/3/library/heapq.html
- Priority queue algorithms
- Fair scheduling techniques

---

**Ready to Start:** ✅ Clear scope, well-defined requirements, focused on one concern (queue priority)
