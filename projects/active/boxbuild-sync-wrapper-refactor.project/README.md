# Box Build Sync Wrapper Refactor

**Created:** February 18, 2026  
**Last Updated:** February 19, 2026  
**Status:** ✅ Complete (90% - code done, CHANGELOG pending)

---

## Problem Statement

The box build template has **three** separate implementations:

1. `box_build.py` → `BoxBuildTemplate` — sync class using `ProductServiceInternal` (phantom import)
2. `async_box_build.py` → `AsyncBoxBuildTemplate` — async class using `AsyncProductService`
3. `sync_box_build.py` → `SyncBoxBuildTemplate` — sync wrapper using `_run_sync()` around `AsyncBoxBuildTemplate`

This is inconsistent with every other domain in pyWATS where the pattern is:
- **One** async implementation (`async_service.py`, `async_repository.py`)
- The `SyncServiceWrapper` / `SyncProductServiceWrapper` in `pywats.py` handles sync wrapping automatically via `__getattr__`

The box build is the **only** feature where a concrete separate sync class exists alongside the async implementation. The old `box_build.py` (BoxBuildTemplate) also references `ProductServiceInternal` which doesn't exist as a file.

## Objective

Eliminate `sync_box_build.py` and `box_build.py`, keeping only `async_box_build.py` as the single implementation. The sync wrapping should be handled entirely by `SyncProductServiceWrapper` in `pywats.py` — the same pattern used for every other sync method.

## Success Criteria

1. ✅ `sync_box_build.py` deleted — no standalone sync box build class
2. ✅ `box_build.py` deleted — no legacy sync implementation
3. ✅ `async_box_build.py` (`AsyncBoxBuildTemplate`) is the sole implementation
4. ✅ `SyncProductServiceWrapper` in `pywats.py` wraps `AsyncBoxBuildTemplate` methods automatically (same as all other service methods)
5. ✅ `BoxBuildTemplate` name preserved as alias for backward compatibility
6. ✅ All existing tests pass
7. ✅ Integration test `tests/integration/test_boxbuild.py` passes
8. ✅ Example `examples/domains/box_build_examples.py` works unchanged
9. ✅ `service.pyi` type stub updated
10. ✅ `__init__.py` exports updated

## Scope

### Files to Modify
- `src/pywats/domains/product/async_box_build.py` — may need minor adjustments
- `src/pywats/pywats.py` — remove `SyncProductServiceWrapper` special-casing
- `src/pywats/domains/product/__init__.py` — update exports
- `src/pywats/domains/product/service.pyi` — fix return type

### Files to Delete
- `src/pywats/domains/product/sync_box_build.py`
- `src/pywats/domains/product/box_build.py`

### Files to Verify
- `tests/integration/test_boxbuild.py`
- `tests/domains/product/test_integration.py`
- `tests/domains/production/test_workflow.py`
- `examples/domains/box_build_examples.py`

## Risk Assessment

- **Low risk:** The `SyncProductServiceWrapper` already handles the async→sync wrapping correctly for `get_box_build_template`. The only question is whether the returned `AsyncBoxBuildTemplate` object's methods also need wrapping (they do — `add_subunit`, `save`, etc. are async).
- **Key insight:** The current `SyncProductServiceWrapper.box_build_wrapper` already returns a `SyncBoxBuildTemplate` that wraps individual methods. We need to keep this pattern but can simplify it by using the generic `SyncServiceWrapper` approach on the template object itself.
