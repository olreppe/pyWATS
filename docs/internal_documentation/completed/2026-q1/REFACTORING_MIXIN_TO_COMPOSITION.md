# Mixin to Composition Refactoring

## Summary

Successfully refactored the async API pattern from **mixin inheritance** to **composition** pattern.

## What Changed

### Before (Mixin Pattern)
```python
from pywats_client.gui.async_api_mixin import AsyncAPIPageMixin

class ProductionPage(BasePage, AsyncAPIPageMixin):
    def _on_refresh(self):
        self.run_api_call(
            lambda api: api.production.get_units(),
            on_success=self._on_units_loaded
        )
```

**Problems:**
- Multiple inheritance complexity
- Implicit dependencies via mixin
- Harder to test (mocks complex)
- Tight coupling

### After (Composition Pattern)
```python
class ProductionPage(BasePage):
    def __init__(self, config, main_window=None, parent=None):
        super().__init__(config, parent, 
                        async_api_runner=getattr(main_window, 'async_api_runner', None))
    
    def _on_refresh(self):
        if self.async_api:
            self.async_api.run(
                self,
                lambda api: api.production.get_units(),
                on_success=self._on_units_loaded
            )
```

**Benefits:**
- Explicit dependency injection
- Cleaner class hierarchy
- Easy to test (mock the runner)
- Loose coupling

## Files Changed

### Created
- `src/pywats_client/gui/async_api_runner.py` - New composition-based helper

### Modified
- `src/pywats_client/gui/pages/base.py` - Added `async_api_runner` parameter
- `src/pywats_client/gui/pages/unused/production.py` - Uses composition
- `src/pywats_client/gui/pages/unused/asset.py` - Uses composition
- `src/pywats_client/gui/pages/unused/product.py` - Uses composition
- `src/pywats_client/gui/pages/unused/rootcause.py` - Uses composition
- `docs/guides/architecture.md` - Updated diagrams and docs
- `docs/guides/client-architecture.md` - Updated examples
- `MIGRATION.md` - Updated migration guide
- `src/pywats_client/service/README.md` - Updated examples

### Deleted
- `src/pywats_client/gui/async_api_mixin.py` - Removed mixin completely

## API Changes

### Old Mixin API
```python
# Called from page (self is the mixin)
self.run_api_call(api_call, on_success, on_error)
self.require_api(action)
self.run_async_parallel(*calls)
self.run_async_sequence(*calls)
```

### New Composition API
```python
# Called from runner (self is passed explicitly)
self.async_api.run(self, api_call, on_success, on_error)
self.async_api.require_api(self, action)
self.async_api.run_parallel(self, *calls)
self.async_api.run_sequence(self, *calls)
```

## Technical Details

### Memory Safety
- Uses `weakref` for page tracking to avoid circular references
- Runner doesn't hold strong references to pages

### Thread Safety
- All async operations run through `AsyncTaskRunner`
- Qt signals/slots ensure thread-safe UI updates
- Callbacks executed in main thread

### Backward Compatibility
**None** - This is a breaking change. Project is in BETA with explicit NO_BACKWARDS_COMPATIBILITY policy.

## Testing Recommendations

1. **Unit Test the Runner:**
   ```python
   def test_async_api_runner():
       mock_facade = Mock()
       runner = AsyncAPIRunner(mock_facade)
       # Test run(), require_api(), etc.
   ```

2. **Mock in Page Tests:**
   ```python
   def test_production_page():
       mock_runner = Mock(spec=AsyncAPIRunner)
       page = ProductionPage(config, async_api_runner=mock_runner)
       # Verify page calls runner correctly
   ```

## Migration Effort

- **Implementation:** 1 hour (completed)
- **Breaking Changes:** Yes (acceptable per NO_BACKWARDS_COMPATIBILITY.md)
- **Risk Level:** Low (unused pages, well-tested pattern)

## Future Considerations

1. **MainWindow Integration:** Currently unused pages don't have facade access. If activated:
   - Create `AsyncAPIRunner` in `MainWindow.__init__`
   - Pass to pages that need it via `async_api_runner` parameter

2. **Alternative Patterns:**
   - Could use QThread for pure Qt approach
   - Could use service locator pattern
   - Current composition is cleanest for testability

## Documentation

All documentation updated to reflect composition pattern:
- Architecture diagrams show `AsyncAPIRunner` instead of `AsyncAPIPageMixin`
- Code examples demonstrate dependency injection
- Migration guide updated with new pattern

## Notes

- These pages are in `pages/unused/` - not currently active in UI
- Current architecture uses IPC (no facade), so runner isn't used yet
- Pattern is ready when/if these pages are reactivated
