# TODO: Converter Priority Queue

**Related Docs:**
- [README](README.md) | [Analysis](ANALYSIS.md) | [Plan](IMPLEMENTATION_PLAN.md) | [Progress](PROGRESS.md)

---

## ✅ Completed

### Planning & Setup
- [x] Create project structure
- [x] Move from planned to active
- [x] Create ANALYSIS.md
- [x] Create IMPLEMENTATION_PLAN.md
- [x] Create PROGRESS.md
- [x] Create TODO.md

---

## 🚧 In Progress
- [ ] Phase 1, Step 1.1: Add priority field to QueueItem - **CURRENT**

---

## 🧠 Phase 1: QueueItem Enhancement (8 hours)

- [ ] Step 1.1: Add priority field and __lt__ to QueueItem dataclass
- [ ] Step 1.2: Update QueueItem.create() method with priority parameter
- [ ] Step 1.3: Create tests/cross_cutting/test_queue_priority.py (8 tests)
- [ ] Run tests: `pytest tests/cross_cutting/test_queue_priority.py -v`
- [ ] Commit: "feat(queue): Add priority field to QueueItem"

---

## 🧠 Phase 2: MemoryQueue Priority Implementation (16 hours)

- [ ] Step 2.1: Replace deque with heapq in MemoryQueue.__init__
- [ ] Step 2.2: Update MemoryQueue.add() - add priority parameter, use heappush
- [ ] Step 2.3: Rewrite MemoryQueue.get_next() - lazy cleanup approach
- [ ] Step 2.4: Update MemoryQueue.update() - re-add to heap if status → PENDING
- [ ] Step 2.5: Create tests/cross_cutting/test_memory_queue_priority.py (15 tests)
- [ ] Run all queue tests: `pytest tests/cross_cutting/test_memory_queue*.py -v`
- [ ] Verify backward compatibility: Run full test suite
- [ ] Commit: "feat(queue): Implement priority queue with heapq in MemoryQueue"

---

## 🧠 Phase 3: PersistentQueue Priority Support (8 hours)

- [ ] Step 3.1: Update PersistentQueue.add() - save priority in metadata JSON
- [ ] Step 3.2: Update _load_item_from_file() - read priority from metadata
- [ ] Step 3.3: Create tests/client/test_persistent_queue_priority.py (10 tests)
- [ ] Test migration: Load old files without priority (should get default=5)
- [ ] Run tests: `pytest tests/client/test_persistent_queue*.py -v`
- [ ] Commit: "feat(queue): Add priority support to PersistentQueue"

---

## 🧠 Phase 4: AsyncPendingQueue Priority (12 hours)

- [ ] Step 4.1: Add _queue_report() method - create .meta.json with priority
- [ ] Step 4.2: Update submit_all_pending() - sort by priority from metadata
- [ ] Step 4.3: Add priority parameter to async_client_service.submit_report()
- [ ] Step 4.4: Create tests/client/test_async_pending_queue_priority.py (10 tests)
- [ ] Run tests: `pytest tests/client/test_async_pending_queue*.py -v`
- [ ] Commit: "feat(queue): Add priority support to AsyncPendingQueue"

---

## 🧠 Phase 5: Priority Aging (Anti-Starvation) (10 hours)

- [ ] Step 5.1: Add QueueConfig dataclass with aging settings to core/config.py
- [ ] Step 5.2: Implement aging logic in MemoryQueue.get_next()
- [ ] Step 5.3: Create tests/cross_cutting/test_queue_aging.py (8 tests)
- [ ] Test aging prevents starvation (low-priority items eventually run)
- [ ] Run tests: `pytest tests/cross_cutting/test_queue_aging.py -v`
- [ ] Commit: "feat(queue): Add priority aging to prevent starvation"

---

## 🧠 Phase 6: Documentation & Examples (8 hours)

- [ ] Step 6.1: Create docs/guides/queue-priority.md guide
- [ ] Step 6.2: Create examples/queue_priority_example.py
- [ ] Step 6.3: Update relevant docs (search for "queue" references)
- [ ] Step 6.4: Run example script to verify it works
- [ ] Commit: "docs(queue): Add priority queue guide and examples"

---

## 🧠 Phase 7: Final Verification & Completion (8 hours)

- [ ] Run full test suite: `pytest` (all 1570+ tests must pass)
- [ ] Run new priority tests: `pytest tests/**/test_*priority*.py -v`
- [ ] Generate type stubs: `python scripts/generate_type_stubs.py`
- [ ] Check for errors: Verify no type/lint errors
- [ ] Performance test: Measure heap overhead vs deque
- [ ] Update CHANGELOG.md under [Unreleased]
- [ ] Move tests from project folder to active test suite
- [ ] Create COMPLETION_SUMMARY.md
- [ ] Move project to docs/internal_documentation/completed/2026-q1/
- [ ] Commit: "chore: Archive converter-priority-queue project"

---

## ⏸️ Blocked/Deferred
- None currently

---

## 📊 Progress Summary

**Phases Complete:** 0/7  
**Steps Complete:** 6/46 (planning only)  
**Estimated Remaining:** 62 hours

---

**Last Updated:** February 2, 2026 14:40