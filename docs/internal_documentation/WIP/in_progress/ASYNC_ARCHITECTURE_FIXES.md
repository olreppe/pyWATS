# Async Architecture Fixes Implementation Plan

**Created:** 2026-01-28  
**Status:** 🔄 IN PROGRESS  
**Priority:** High (Production Readiness)  
**Related:** CLIENT_ASYNC_ARCHITECTURE.md

---

## Executive Summary

Code review identified 7 issues in the async client architecture that need to be fixed before production deployment. This document tracks the implementation of all fixes.

---

## Issues to Fix

### 1. Thread-Unsafe asyncio.Event.set() in Watchdog Callbacks [HIGH]

**Problem:** Watchdog runs in a separate thread and calls `_new_file_event.set()` which is not thread-safe.

**Files Affected:**
- `src/pywats_client/service/async_pending_queue.py`
- `src/pywats_client/service/async_converter_pool.py`

**Solution:** Use `loop.call_soon_threadsafe()` to safely signal from watchdog thread.

**Status:** ⬜ Not Started

---

### 2. Private Semaphore._value Access [MEDIUM]

**Problem:** Accessing `_semaphore._value` is implementation-dependent and could break in future Python versions.

**Files Affected:**
- `src/pywats_client/service/async_pending_queue.py`
- `src/pywats_client/service/async_converter_pool.py`

**Solution:** Track active count explicitly with instance variable.

**Status:** ⬜ Not Started

---

### 3. Task Cleanup Race Condition [MEDIUM]

**Problem:** In `submit_all_pending`, the task list filtering can race with concurrent task additions.

**Files Affected:**
- `src/pywats_client/service/async_pending_queue.py`

**Solution:** Use a set for task tracking with explicit add/discard in task lifecycle.

**Status:** ⬜ Not Started

---

### 4. Improper API Context Manager Exit [MEDIUM]

**Problem:** Using `await api.close()` instead of `__aexit__` may skip cleanup logic.

**Files Affected:**
- `src/pywats_client/service/async_client_service.py`

**Solution:** Use proper `__aexit__(None, None, None)` for cleanup.

**Status:** ⬜ Not Started

---

### 5. Missing CancelledError Handling in Timer Loops [LOW]

**Problem:** Timer loops don't explicitly handle `asyncio.CancelledError`, which could interfere with graceful shutdown.

**Files Affected:**
- `src/pywats_client/service/async_client_service.py`

**Solution:** Add explicit `except asyncio.CancelledError: raise` in loops.

**Status:** ⬜ Not Started

---

### 6. GUI Mixin Missing Dependency Validation [LOW]

**Problem:** `AsyncAPIMixin` assumes certain attributes exist but doesn't validate at runtime.

**Files Affected:**
- `src/pywats_client/gui/async_api_mixin.py`

**Solution:** Add runtime validation in key methods.

**Status:** ⬜ Not Started

---

### 7. Misleading run_async_chain Naming [LOW]

**Problem:** Method name suggests sequential execution but actually runs calls in parallel.

**Files Affected:**
- `src/pywats_client/gui/async_api_mixin.py`

**Solution:** Rename to `run_async_parallel` and add true `run_async_sequence` method.

**Status:** ⬜ Not Started

---

## Implementation Progress

| # | Issue | Priority | Status |
|---|-------|----------|--------|
| 1 | Thread-unsafe Event.set() | HIGH | ✅ |
| 2 | Semaphore._value access | MEDIUM | ✅ |
| 3 | Task cleanup race condition | MEDIUM | ✅ |
| 4 | Context manager exit | MEDIUM | ✅ |
| 5 | CancelledError handling | LOW | ✅ |
| 6 | Mixin validation | LOW | ✅ |
| 7 | run_async_chain naming | LOW | ✅ |

---

## Testing Results

**Date:** 2026-01-28

- All 646 tests pass
- 41 async-specific tests verified
- No regressions

---

## Completion Criteria

- [x] All 7 issues fixed
- [x] All tests pass
- [x] Code committed and pushed
- [ ] Documentation updated if needed
