# Sync Wrapper Enhancement - Technical Analysis

**Project:** sync-wrapper-enhancements  
**Date:** February 1, 2026  
**Analyst:** AI Agent  

---

## Executive Summary

The pyWATS synchronous wrapper currently uses a **generic reflection-based approach** that wraps async methods at runtime. While this works, it lacks production-grade features like timeout control, retry logic, and debugging support.

**Key Discovery:** Type stubs (`.pyi` files) are **already auto-generated** from async services using `scripts/generate_type_stubs.py`. This provides full type safety without manual annotation.

**Project Impact:** We need to enhance the **wrapper mechanism itself** (in `pywats.py`), not individual service methods. The type stubs will automatically reflect any changes we make to the wrapper.

---

## Current Architecture Analysis

### 1. Sync Wrapper Implementation

**File:** [src/pywats/pywats.py](../../../src/pywats/pywats.py)

```python
class SyncServiceWrapper:
    """Generic synchronous wrapper for async services."""
    
    def __init__(self, async_service: Any) -> None:
        self._async = async_service
    
    def __getattr__(self, name: str) -> Any:
        """Dynamically wrap async methods as sync methods."""
        attr = getattr(self._async, name)
        
        if inspect.iscoroutinefunction(attr):
            @wraps(attr)
            def sync_wrapper(*args, **kwargs):
                return _run_sync(attr(*args, **kwargs))  # ← Core wrapping logic
            return sync_wrapper
        
        return attr
```

**How It Works:**
1. User calls `api.product.get_product("ABC123")`
2. `SyncServiceWrapper.__getattr__` intercepts the call
3. Checks if underlying method is async
4. Wraps it with `_run_sync()` that runs it in an event loop
5. Returns result synchronously

**Current Limitations:**
- ❌ No timeout control (runs indefinitely)
- ❌ No retry on transient failures
- ❌ No correlation IDs for debugging
- ❌ No error context (just raw exceptions)

---

### 2. Type Stub Auto-Generation

**File:** [scripts/generate_type_stubs.py](../../../scripts/generate_type_stubs.py)

**Process:**
1. Parses `domains/*/async_service.py` files using AST
2. Extracts method signatures (params, return types)
3. Generates `.pyi` stub files with sync signatures
4. Type checkers use stubs for autocomplete and validation

**Example Generated Stub:**
```python
# src/pywats/domains/product/service.pyi (AUTO-GENERATED)
class SyncProductService:
    def get_product(self, part_number: str) -> Optional[Product]: ...
    def create_product(self, part_number: str, ...) -> Optional[Product]: ...
```

**Implication:** We don't need to manually add type hints to sync wrapper - they're auto-generated!

---

### 3. Event Loop Management

**Function:** `_run_sync()` in [pywats.py](../../../src/pywats/pywats.py)

```python
def _run_sync(coro: Coroutine[Any, Any, T]) -> T:
    """Run a coroutine synchronously using a persistent event loop."""
    loop = _get_or_create_event_loop()
    return loop.run_until_complete(coro)  # ← No timeout control here
```

**Current Behavior:**
- Creates persistent event loop per thread
- Runs coroutine to completion
- No timeout mechanism
- No retry logic

---

## Problem Analysis

### Problem 1: No Timeout Control

**Current:**
```python
# This can run forever if server hangs
result = api.product.get_product("ABC123")
```

**Needed:**
```python
# Should timeout after 30 seconds
result = api.product.get_product("ABC123", timeout=30.0)
```

**Challenge:** Timeout needs to be injected **before** async call is made, but wrapper intercepts at `__getattr__` level.

---

### Problem 2: No Retry Logic

**Current:**
```python
# Fails immediately on transient network error
try:
    result = api.product.get_product("ABC123")
except ConnectionError:
    # User must manually retry
    pass
```

**Needed:**
```python
# Auto-retry with exponential backoff
config = SyncClientConfig(
    max_retries=3,
    retry_backoff=2.0
)
api = pyWATS(..., config=config)
result = api.product.get_product("ABC123")  # Auto-retries on failure
```

---

### Problem 3: No Debugging Support

**Current:**
```python
# Logs show generic async execution
[INFO] Getting product ABC123
```

**Needed:**
```python
# Correlation IDs track requests across logs
[INFO] [req_id=abc-123-def] Getting product ABC123
[ERROR] [req_id=abc-123-def] Failed: Connection timeout
```

---

## Technical Constraints

### Constraint 1: Type Stub Compatibility

**Any changes must work with auto-generated stubs.**

The type stubs are generated from **async service signatures**, not the wrapper. If we add parameters to the wrapper (like `timeout`), they **won't appear in type stubs** unless we:
- Add them to async service signatures (bad - pollutes async API)
- OR use wrapper-level configuration (good - separate concern)

**Decision:** Use **config-based approach** for timeout/retry, not per-method parameters.

---

### Constraint 2: Backward Compatibility

**Existing code must continue to work:**
```python
# This must still work
api = pyWATS(base_url="...", token="...")
result = api.product.get_product("ABC123")
```

All enhancements must be **opt-in** via configuration.

---

### Constraint 3: Reflection-Based Wrapping

The `SyncServiceWrapper.__getattr__` approach is **powerful but limits** what we can do:
- Can't easily add per-method parameters
- Must inject features at wrapper level
- Need to preserve function signatures for type checking

---

## Proposed Solution Architecture

### Solution 1: Enhanced `_run_sync()` with Timeout

```python
def _run_sync(coro: Coroutine[Any, Any, T], timeout: Optional[float] = None) -> T:
    """Run coroutine with optional timeout."""
    loop = _get_or_create_event_loop()
    
    if timeout:
        # Wrap in asyncio.wait_for for timeout
        coro = asyncio.wait_for(coro, timeout=timeout)
    
    return loop.run_until_complete(coro)
```

**Access Timeout:**
```python
class SyncServiceWrapper:
    def __init__(self, async_service: Any, config: Optional[SyncConfig] = None):
        self._async = async_service
        self._config = config or SyncConfig()  # ← Store config
    
    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._async, name)
        
        if inspect.iscoroutinefunction(attr):
            @wraps(attr)
            def sync_wrapper(*args, **kwargs):
                return _run_sync(
                    attr(*args, **kwargs),
                    timeout=self._config.timeout  # ← Use config
                )
            return sync_wrapper
        
        return attr
```

---

### Solution 2: Retry Decorator

```python
def with_retry(func, config: RetryConfig):
    """Wrap function with retry logic."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        last_error = None
        for attempt in range(config.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except config.retry_on_errors as e:
                last_error = e
                if attempt < config.max_retries:
                    wait = config.backoff ** attempt
                    logger.warning(f"Retry attempt {attempt + 1} after {wait}s")
                    time.sleep(wait)
        raise last_error
    return wrapper
```

**Apply in Wrapper:**
```python
def __getattr__(self, name: str) -> Any:
    attr = getattr(self._async, name)
    
    if inspect.iscoroutinefunction(attr):
        @wraps(attr)
        def sync_wrapper(*args, **kwargs):
            result = _run_sync(attr(*args, **kwargs), timeout=self._config.timeout)
            return result
        
        # Apply retry if configured
        if self._config.retry_enabled:
            sync_wrapper = with_retry(sync_wrapper, self._config.retry)
        
        return sync_wrapper
    
    return attr
```

---

### Solution 3: Correlation IDs via Context

```python
import contextvars

correlation_id_var = contextvars.ContextVar('correlation_id', default=None)

def _run_sync(coro, timeout=None):
    """Run with correlation ID context."""
    # Generate correlation ID
    corr_id = str(uuid.uuid4())
    token = correlation_id_var.set(corr_id)
    
    try:
        loop = _get_or_create_event_loop()
        if timeout:
            coro = asyncio.wait_for(coro, timeout=timeout)
        return loop.run_until_complete(coro)
    finally:
        correlation_id_var.reset(token)
```

**Use in Logging:**
```python
# In pywats/core/logging.py
class CorrelationFilter(logging.Filter):
    def filter(self, record):
        corr_id = correlation_id_var.get()
        record.correlation_id = corr_id or "N/A"
        return True

# Format: [correlation_id=xxx] message
```

---

## Impact on Type Stubs

**Good News:** Type stubs are **unaffected** by these changes!

The stubs describe method signatures:
```python
def get_product(self, part_number: str) -> Optional[Product]: ...
```

Our changes are in the **wrapper mechanism**, not method signatures:
- Timeout: Configured at client level, not per-method
- Retry: Transparent wrapper, no signature change
- Correlation: Context-based, no signature change

**Type safety remains intact** with zero changes to stub generation.

---

## Files Requiring Changes

### Core Implementation (3 files)
1. **src/pywats/pywats.py** (~100 lines modified)
   - Enhance `_run_sync()` with timeout
   - Add `SyncConfig` dataclass
   - Update `SyncServiceWrapper` to use config
   - Add retry wrapper logic
   - Add correlation ID support

2. **src/pywats/core/config.py** (~50 lines added)
   - Create `SyncConfig` dataclass
   - Define `RetryConfig` dataclass

3. **src/pywats/core/logging.py** (~30 lines added)
   - Add `CorrelationFilter` for log formatting
   - Update logger configuration

### Tests (2 new files)
4. **tests/integration/test_sync_timeout.py** (~150 lines)
5. **tests/integration/test_sync_retry.py** (~200 lines)

### Documentation (2 files)
6. **docs/guides/sync-vs-async.md** (update)
7. **examples/sync_with_config.py** (new)

**Total Scope:** 5-7 files, ~530 lines of new/modified code

---

## Risk Assessment

### Low Risk
- ✅ Type stubs unchanged (auto-generation continues)
- ✅ Backward compatible (config is optional)
- ✅ Clear separation of concerns
- ✅ No changes to async services

### Medium Risk
- ⚠️ Event loop behavior with timeouts (needs thorough testing)
- ⚠️ Retry logic with correlation IDs (context propagation)

### Mitigation
- Comprehensive integration tests
- Test with real WATS server
- Validate correlation ID propagation
- Test timeout edge cases

---

## Alternative Approaches Considered

### ❌ Alternative 1: Add timeout parameter to each method
```python
def get_product(self, part_number: str, timeout: float = 30.0) -> Optional[Product]:
```

**Rejected:** Would require changing async service signatures and regenerating stubs. Too invasive.

### ❌ Alternative 2: Separate timeout wrapper class
```python
api_with_timeout = TimeoutWrapper(api, timeout=30.0)
```

**Rejected:** Adds complexity, user must remember to wrap. Config approach is cleaner.

### ✅ Chosen: Config-based approach
Clean separation, opt-in, no signature changes.

---

## Success Criteria

**Technical:**
- [ ] Timeout works reliably (tested with slow servers)
- [ ] Retry logic handles transient failures
- [ ] Correlation IDs appear in all logs
- [ ] All existing tests pass
- [ ] New integration tests pass (20+)
- [ ] Type stubs unchanged (verify with `generate_type_stubs.py --check`)

**User Experience:**
- [ ] Simple configuration API
- [ ] Clear error messages
- [ ] Debugging easier with correlation IDs
- [ ] Production reliability improved

---

## Next Steps

1. ✅ **ANALYSIS.md** - Complete (this document)
2. **IMPLEMENTATION_PLAN.md** - Detailed implementation steps
3. **TODO.md** - Task checklist
4. **Update README.md** - Reflect type stub findings

---

**Analysis Complete:** Ready to proceed with implementation planning.
