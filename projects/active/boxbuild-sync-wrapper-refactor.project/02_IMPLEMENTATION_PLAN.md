# Implementation Plan: Box Build Sync Wrapper Refactor

**Created:** February 18, 2026  
**Last Updated:** February 18, 2026

---

## Phase 1: Add Context Manager to SyncServiceWrapper

**Goal:** Make `SyncServiceWrapper` able to act as a context manager, so any wrapped async object with `__aenter__`/`__aexit__` works synchronously.

### Steps:
1. Add `__enter__` / `__exit__` to `SyncServiceWrapper` in `pywats.py`
2. `__enter__` returns `self`
3. `__exit__` checks if the wrapped async object has `has_pending_changes` and if so, calls `_run_sync(self._async.save())`
4. Ensure method chaining works — when a wrapped method returns the same async object, return `self` (the wrapper) instead

---

## Phase 2: Simplify SyncProductServiceWrapper

**Goal:** Replace the hardcoded `SyncBoxBuildTemplate` instantiation with generic `SyncServiceWrapper`.

### Steps:
1. Update `SyncProductServiceWrapper.__getattr__` to wrap the returned `AsyncBoxBuildTemplate` with `SyncServiceWrapper` instead of `SyncBoxBuildTemplate`
2. Remove the import of `SyncBoxBuildTemplate`

---

## Phase 3: Delete Legacy Files

**Goal:** Remove the two redundant box build files.

### Steps:
1. Delete `src/pywats/domains/product/sync_box_build.py`
2. Delete `src/pywats/domains/product/box_build.py`
3. Update `src/pywats/domains/product/__init__.py`:
   - Change `from .box_build import BoxBuildTemplate` → `from .async_box_build import AsyncBoxBuildTemplate as BoxBuildTemplate`
   - Add `AsyncBoxBuildTemplate` to `__all__`

---

## Phase 4: Update Type Stubs

**Goal:** Fix the `service.pyi` to return the correct type.

### Steps:
1. Update `get_box_build_template` return type in `service.pyi`
2. Add `BoxBuildTemplate` as type alias documentation

---

## Phase 5: Verify Tests

**Goal:** Ensure all existing tests pass without modification.

### Steps:
1. Run `pytest tests/domains/product/` — unit tests
2. Run `pytest tests/integration/test_boxbuild.py` — integration test (if server available)
3. Check `tests/domains/production/test_workflow.py` for box build references
4. Verify no import errors across codebase

---

## Phase 6: Verify Examples and Docs

**Goal:** Ensure examples and documentation work.

### Steps:
1. Check `examples/domains/box_build_examples.py` — uses `api.product.get_box_build_template()`
2. Verify `from pywats.domains.product import BoxBuildTemplate` still works (backward compat)
3. Update any docs that reference `SyncBoxBuildTemplate` or `sync_box_build.py`

---

## Execution Order

```
Phase 1 → Phase 2 → Phase 5 (verify) → Phase 3 → Phase 4 → Phase 5 (verify again) → Phase 6
```

We test after Phase 2 (before deleting files) to verify the new wrapping works. Then we delete and test again.
