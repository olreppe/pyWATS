# Analysis: Box Build Sync Wrapper Refactor

**Created:** February 18, 2026  
**Last Updated:** February 18, 2026

---

## Current Architecture (3 files, 3 classes)

### 1. `box_build.py` — `BoxBuildTemplate` (Legacy Sync)
- **503 lines** of synchronous code
- Depends on `ProductServiceInternal` (TYPE_CHECKING import — the file doesn't actually exist)
- Calls `self._service.get_revision()` (sync), `self._service._repo_internal.delete_revision_relation()`, etc.
- Has context manager (`__enter__`/`__exit__`)
- Imported in `__init__.py` and exported as `BoxBuildTemplate`
- **Not used at runtime** — the sync API goes through `SyncProductServiceWrapper` → `SyncBoxBuildTemplate` instead

### 2. `async_box_build.py` — `AsyncBoxBuildTemplate` (Primary)
- **433 lines** of async code
- Depends on `AsyncProductService`
- All builder methods are `async` (`add_subunit`, `update_subunit`, `remove_subunit`, `save`, `reload`, `set_quantity`)
- Non-async helpers: properties, `clear_all`, `discard`, `validate_subunit`, `get_matching_subunits`, `get_required_parts`
- Has async context manager (`__aenter__`/`__aexit__`)
- Has alias at bottom: `BoxBuildTemplate = AsyncBoxBuildTemplate` (but never imported)

### 3. `sync_box_build.py` — `SyncBoxBuildTemplate` (Sync Wrapper)
- **180 lines** — wraps every async method with `_run_sync()`
- Depends on `AsyncBoxBuildTemplate`
- Has sync context manager (`__enter__`/`__exit__`)
- Used only by `SyncProductServiceWrapper` in `pywats.py`

## How `SyncProductServiceWrapper` Currently Works

In `pywats.py` line 193-227:
```python
class SyncProductServiceWrapper(SyncServiceWrapper):
    def __getattr__(self, name):
        if name in ('get_box_build_template', 'get_box_build'):
            def box_build_wrapper(*args, **kwargs):
                async_template = _run_sync(attr(*args, **kwargs))
                from .domains.product.sync_box_build import SyncBoxBuildTemplate
                return SyncBoxBuildTemplate(async_template)
            return box_build_wrapper
        return super().__getattr__(name)
```

This is special-cased because:
- `get_box_build_template()` returns an `AsyncBoxBuildTemplate` object
- That object has async methods that can't be called synchronously
- So it wraps the returned object in `SyncBoxBuildTemplate`

## Standard Pattern (All Other Services)

Every other service uses the generic `SyncServiceWrapper`:
```python
class SyncServiceWrapper:
    def __getattr__(self, name):
        attr = getattr(self._async, name)
        if inspect.iscoroutinefunction(attr):
            def sync_wrapper(*args, **kwargs):
                result = _run_sync(attr(*args, **kwargs))
                return result
            return sync_wrapper
        return attr
```

This works because other service methods return simple data (models, lists, bools). BoxBuild is unique because it returns an **object with its own async methods**.

## The Real Problem

The issue isn't just naming — it's that returning an object with async methods from a sync wrapper requires **recursive wrapping**. The solution needs to:

1. Run `get_box_build_template()` synchronously (already done)
2. Wrap the returned `AsyncBoxBuildTemplate` so its async methods (`add_subunit`, `save`, etc.) are also callable synchronously

## Proposed Solution

Instead of a dedicated `SyncBoxBuildTemplate` class (180 lines of boilerplate), use the existing `SyncServiceWrapper` generically on the returned template object:

```python
class SyncProductServiceWrapper(SyncServiceWrapper):
    def __getattr__(self, name):
        if name in ('get_box_build_template', 'get_box_build'):
            def box_build_wrapper(*args, **kwargs):
                async_template = _run_sync(attr(*args, **kwargs))
                # Wrap the template object itself with SyncServiceWrapper
                return SyncServiceWrapper(async_template, self._config)
            return box_build_wrapper
        return super().__getattr__(name)
```

This means `SyncServiceWrapper.__getattr__` will handle:
- `add_subunit()` → `_run_sync(async_template.add_subunit())`  
- `save()` → `_run_sync(async_template.save())`
- `parent_part_number` → direct passthrough (property)
- etc.

### Context Manager Issue

`SyncServiceWrapper` doesn't have `__enter__`/`__exit__`. We need to add those so that `with api.product.get_box_build_template(...) as bb:` still works.

Options:
1. Add `__enter__`/`__exit__` to `SyncServiceWrapper` (general solution — benefits any future wrapped object)
2. Create a small `SyncBoxBuildWrapper` that extends `SyncServiceWrapper` with context manager support

**Option 1 is better** — it's general-purpose and follows DRY. The `__exit__` should check if the wrapped async object has `has_pending_changes` and call `save()` if so.

## Constraints

- Must not break `with api.product.get_box_build_template(...) as bb:` pattern
- Must preserve method chaining (`bb.add_subunit(...).add_subunit(...)`)
- `BoxBuildTemplate` name must remain importable for backward compatibility
- The `service.pyi` type stub currently returns `AsyncBoxBuildTemplate` — needs fixing

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Method chaining returns `AsyncBoxBuildTemplate` not wrapped | Medium | `SyncServiceWrapper.__getattr__` wraps the return value if it's the same type |
| Context manager breaks | High | Add `__enter__`/`__exit__` to `SyncServiceWrapper` |
| Existing tests import `SyncBoxBuildTemplate` directly | Low | No test imports it directly — only `pywats.py` does |
| `BoxBuildTemplate` import breaks | Medium | Keep alias in `__init__.py` pointing to `AsyncBoxBuildTemplate` |
