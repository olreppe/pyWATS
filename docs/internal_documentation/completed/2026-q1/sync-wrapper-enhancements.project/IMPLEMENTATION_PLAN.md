# Sync Wrapper Enhancement - Implementation Plan

**Project:** sync-wrapper-enhancements  
**Date:** February 1, 2026  
**Sprint Duration:** 3-5 days  

---

## Implementation Phases

### Phase 1: Core Infrastructure (Day 1 - 4 hours)

Build the foundation for timeout, retry, and correlation support.

#### Task 1.1: Create SyncConfig Dataclass (1 hour)

**File:** `src/pywats/core/config.py`

**Add:**
```python
@dataclass
class RetryConfig:
    """Configuration for retry logic."""
    max_retries: int = 3
    backoff: float = 2.0  # Exponential backoff multiplier
    retry_on_errors: Tuple[Type[Exception], ...] = (
        ConnectionError,
        TimeoutError,
        # Add more transient errors as needed
    )

@dataclass
class SyncConfig:
    """Configuration for synchronous API wrapper."""
    timeout: Optional[float] = 30.0  # Default 30 second timeout
    retry_enabled: bool = False
    retry: RetryConfig = field(default_factory=RetryConfig)
    correlation_id_enabled: bool = True
```

**Tests:**
```python
def test_sync_config_defaults():
    config = SyncConfig()
    assert config.timeout == 30.0
    assert config.retry_enabled is False
    assert config.correlation_id_enabled is True
```

---

#### Task 1.2: Enhance _run_sync() with Timeout (1.5 hours)

**File:** `src/pywats/pywats.py`

**Current:**
```python
def _run_sync(coro: Coroutine[Any, Any, T]) -> T:
    loop = _get_or_create_event_loop()
    return loop.run_until_complete(coro)
```

**Enhanced:**
```python
def _run_sync(
    coro: Coroutine[Any, Any, T],
    timeout: Optional[float] = None,
    correlation_id: Optional[str] = None
) -> T:
    """Run coroutine synchronously with optional timeout and correlation tracking."""
    loop = _get_or_create_event_loop()
    
    # Apply timeout if specified
    if timeout is not None:
        coro = asyncio.wait_for(coro, timeout=timeout)
    
    # Set correlation ID in context if provided
    if correlation_id:
        token = correlation_id_var.set(correlation_id)
    else:
        token = None
    
    try:
        return loop.run_until_complete(coro)
    except asyncio.TimeoutError as e:
        raise TimeoutError(f"Operation timed out after {timeout}s") from e
    finally:
        if token:
            correlation_id_var.reset(token)
```

**Tests:**
```python
async def slow_operation():
    await asyncio.sleep(5)
    return "done"

def test_run_sync_with_timeout():
    with pytest.raises(TimeoutError):
        _run_sync(slow_operation(), timeout=1.0)
```

---

#### Task 1.3: Add Correlation ID Support (1.5 hours)

**File:** `src/pywats/pywats.py`

**Add at module level:**
```python
import contextvars
import uuid

# Context variable for correlation IDs
correlation_id_var = contextvars.ContextVar('correlation_id', default=None)

def generate_correlation_id() -> str:
    """Generate a unique correlation ID for request tracking."""
    return str(uuid.uuid4())[:8]  # Short UUID for readability
```

**File:** `src/pywats/core/logging.py`

**Add filter:**
```python
class CorrelationFilter(logging.Filter):
    """Add correlation ID to log records."""
    
    def filter(self, record):
        from ..pywats import correlation_id_var
        corr_id = correlation_id_var.get()
        record.correlation_id = corr_id if corr_id else "--------"
        return True

# Update default formatter
DEFAULT_FORMAT = "[%(levelname)s] [%(correlation_id)s] %(name)s: %(message)s"
```

**Tests:**
```python
def test_correlation_id_in_logs(caplog):
    from pywats.pywats import correlation_id_var
    
    token = correlation_id_var.set("test-123")
    logger.info("Test message")
    correlation_id_var.reset(token)
    
    assert "test-123" in caplog.text
```

---

### Phase 2: Retry Logic (Day 2 - 4 hours)

#### Task 2.1: Implement Retry Wrapper (2 hours)

**File:** `src/pywats/pywats.py`

**Add:**
```python
import time
from typing import Callable, TypeVar

R = TypeVar('R')

def _with_retry(
    func: Callable[..., R],
    config: RetryConfig,
    correlation_id: str
) -> Callable[..., R]:
    """Wrap a function with retry logic."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> R:
        last_error = None
        
        for attempt in range(config.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except config.retry_on_errors as e:
                last_error = e
                
                if attempt < config.max_retries:
                    wait_time = config.backoff ** attempt
                    logger.warning(
                        f"[{correlation_id}] Attempt {attempt + 1}/{config.max_retries + 1} "
                        f"failed: {e}. Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(
                        f"[{correlation_id}] All {config.max_retries + 1} attempts failed"
                    )
        
        raise last_error
    
    return wrapper
```

**Tests:**
```python
def test_retry_success_after_failures():
    """Test that retry succeeds after transient failures."""
    call_count = 0
    
    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Transient error")
        return "success"
    
    config = RetryConfig(max_retries=3, backoff=0.1)
    wrapped = _with_retry(flaky_func, config, "test-123")
    
    result = wrapped()
    assert result == "success"
    assert call_count == 3

def test_retry_exhausted():
    """Test that retry gives up after max attempts."""
    def always_fails():
        raise ConnectionError("Permanent error")
    
    config = RetryConfig(max_retries=2, backoff=0.1)
    wrapped = _with_retry(always_fails, config, "test-456")
    
    with pytest.raises(ConnectionError):
        wrapped()
```

---

#### Task 2.2: Integrate Retry into SyncServiceWrapper (2 hours)

**File:** `src/pywats/pywats.py`

**Update SyncServiceWrapper:**
```python
class SyncServiceWrapper:
    """Generic synchronous wrapper for async services."""
    
    def __init__(
        self,
        async_service: Any,
        config: Optional['SyncConfig'] = None
    ) -> None:
        self._async = async_service
        self._config = config if config is not None else SyncConfig()
    
    def __getattr__(self, name: str) -> Any:
        """Dynamically wrap async methods as sync methods."""
        attr = getattr(self._async, name)
        
        if inspect.iscoroutinefunction(attr):
            @wraps(attr)
            def sync_wrapper(*args, **kwargs):
                # Generate correlation ID if enabled
                corr_id = None
                if self._config.correlation_id_enabled:
                    corr_id = generate_correlation_id()
                
                # Run async method
                result = _run_sync(
                    attr(*args, **kwargs),
                    timeout=self._config.timeout,
                    correlation_id=corr_id
                )
                return result
            
            # Apply retry if enabled
            if self._config.retry_enabled:
                corr_id = generate_correlation_id() if self._config.correlation_id_enabled else "no-corr-id"
                sync_wrapper = _with_retry(sync_wrapper, self._config.retry, corr_id)
            
            return sync_wrapper
        
        return attr
```

**Update pyWATS main class:**
```python
class pyWATS:
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        ...,
        sync_config: Optional[SyncConfig] = None  # NEW
    ):
        self._sync_config = sync_config
        ...
    
    @property
    def product(self) -> SyncProductServiceWrapper:
        if self._product is None:
            async_service = AsyncProductService(...)
            self._product = SyncProductServiceWrapper(
                async_service,
                config=self._sync_config  # Pass config to wrapper
            )
        return self._product
```

**Tests:**
```python
def test_sync_wrapper_with_retry(mock_server):
    """Test retry integration with sync wrapper."""
    # Mock server that fails 2 times then succeeds
    mock_server.set_failure_count(2)
    
    config = SyncConfig(
        retry_enabled=True,
        retry=RetryConfig(max_retries=3, backoff=0.1)
    )
    
    api = pyWATS(base_url="http://mock", sync_config=config)
    result = api.product.get_product("ABC123")
    
    assert result is not None
    assert mock_server.call_count == 3  # Failed 2x, succeeded on 3rd
```

---

### Phase 3: Configuration & Integration (Day 3 - 3 hours)

#### Task 3.1: Update pyWATS Constructor (1 hour)

**File:** `src/pywats/pywats.py`

**Enhanced constructor:**
```python
def __init__(
    self,
    base_url: str,
    token: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    station: Optional[Union[str, Station]] = None,
    api_settings: Optional['APISettings'] = None,
    retry_config: Optional[RetryConfig] = None,  # NEW
    error_mode: ErrorMode = ErrorMode.LOG,
    timeout: float = 30.0,  # NEW (can also set via sync_config)
    sync_config: Optional[SyncConfig] = None,  # NEW
):
    """
    Initialize pyWATS client.
    
    Args:
        base_url: WATS server URL
        token: API token
        ...
        timeout: Default timeout for all sync operations (seconds)
        retry_config: Retry configuration for transient failures
        sync_config: Full sync wrapper configuration (overrides timeout/retry_config)
    """
    # Build sync_config from individual params if not provided
    if sync_config is None:
        retry_cfg = retry_config or RetryConfig()
        sync_config = SyncConfig(
            timeout=timeout,
            retry_enabled=retry_config is not None,
            retry=retry_cfg
        )
    
    self._sync_config = sync_config
    ...
```

**Tests:**
```python
def test_pywats_with_timeout():
    api = pyWATS(base_url="...", timeout=60.0)
    assert api._sync_config.timeout == 60.0

def test_pywats_with_retry_config():
    retry = RetryConfig(max_retries=5, backoff=1.5)
    api = pyWATS(base_url="...", retry_config=retry)
    assert api._sync_config.retry_enabled is True
    assert api._sync_config.retry.max_retries == 5

def test_pywats_with_full_sync_config():
    config = SyncConfig(timeout=45.0, retry_enabled=True)
    api = pyWATS(base_url="...", sync_config=config)
    assert api._sync_config.timeout == 45.0
```

---

#### Task 3.2: Update All Service Properties (2 hours)

**File:** `src/pywats/pywats.py`

**Pattern to apply to all 9 service properties:**
```python
@property
def product(self) -> SyncProductServiceWrapper:
    if self._product is None:
        async_service = AsyncProductService(...)
        self._product = SyncProductServiceWrapper(
            async_service,
            config=self._sync_config  # ← Add this
        )
    return self._product
```

**Services to update:**
- product (special wrapper)
- asset
- production  
- report
- software
- analytics (also as 'app')
- rootcause
- scim
- process

**Tests:** Verify each service uses config:
```python
def test_all_services_use_sync_config():
    config = SyncConfig(timeout=99.0)
    api = pyWATS(base_url="...", sync_config=config)
    
    services = [
        api.product, api.asset, api.production, api.report,
        api.software, api.analytics, api.rootcause, api.scim, api.process
    ]
    
    for service in services:
        assert service._config.timeout == 99.0
```

---

### Phase 4: Testing & Documentation (Day 4-5 - 6 hours)

#### Task 4.1: Integration Tests (3 hours)

**File:** `tests/integration/test_sync_timeout.py` (NEW)

```python
"""Integration tests for sync wrapper timeout functionality."""
import pytest
from pywats import pyWATS, SyncConfig

def test_timeout_on_slow_server(slow_mock_server):
    """Verify timeout raises TimeoutError."""
    api = pyWATS(base_url=slow_mock_server.url, timeout=1.0)
    
    with pytest.raises(TimeoutError, match="timed out after 1.0s"):
        api.product.get_product("ABC123")

def test_timeout_per_call(mock_server):
    """Verify per-call timeout override works."""
    # Note: This would require additional design work
    # May defer to future enhancement
    pass

def test_no_timeout_completes():
    """Verify operations complete when no timeout."""
    api = pyWATS(base_url="...", timeout=None)
    result = api.product.get_product("ABC123")
    assert result is not None
```

**File:** `tests/integration/test_sync_retry.py` (NEW)

```python
"""Integration tests for sync wrapper retry functionality."""
import pytest
from pywats import pyWATS, RetryConfig

def test_retry_on_connection_error(flaky_mock_server):
    """Verify retry succeeds after transient failures."""
    flaky_mock_server.fail_count = 2
    
    retry = RetryConfig(max_retries=3, backoff=0.1)
    api = pyWATS(base_url=flaky_mock_server.url, retry_config=retry)
    
    result = api.product.get_product("ABC123")
    assert result is not None
    assert flaky_mock_server.attempts == 3

def test_retry_exhausted(always_failing_server):
    """Verify retry gives up after max attempts."""
    retry = RetryConfig(max_retries=2, backoff=0.1)
    api = pyWATS(base_url=always_failing_server.url, retry_config=retry)
    
    with pytest.raises(ConnectionError):
        api.product.get_product("ABC123")
    
    assert always_failing_server.attempts == 3  # Initial + 2 retries

def test_retry_disabled_by_default():
    """Verify retry is disabled unless explicitly configured."""
    api = pyWATS(base_url="...")
    assert api._sync_config.retry_enabled is False
```

**File:** `tests/integration/test_sync_correlation.py` (NEW)

```python
"""Integration tests for correlation ID functionality."""
import pytest
import logging
from pywats import pyWATS, SyncConfig

def test_correlation_id_in_logs(caplog):
    """Verify correlation IDs appear in logs."""
    caplog.set_level(logging.INFO)
    
    api = pyWATS(base_url="...")
    api.product.get_product("ABC123")
    
    # Check that correlation ID appears in logs
    assert any("[" in record.message for record in caplog.records)

def test_correlation_id_disabled():
    """Verify correlation IDs can be disabled."""
    config = SyncConfig(correlation_id_enabled=False)
    api = pyWATS(base_url="...", sync_config=config)
    
    # Should work without correlation IDs
    result = api.product.get_product("ABC123")
    assert result is not None
```

---

#### Task 4.2: Documentation Updates (2 hours)

**File:** `docs/guides/sync-vs-async.md` (UPDATE)

**Add section:**
```markdown
## Timeout Configuration

By default, all synchronous operations have a 30-second timeout:

\`\`\`python
# Default timeout
api = pyWATS(base_url="...", token="...")
result = api.product.get_product("ABC123")  # Times out after 30s
\`\`\`

Configure custom timeout:

\`\`\`python
# 60 second timeout
api = pyWATS(base_url="...", timeout=60.0)

# No timeout (run indefinitely)
api = pyWATS(base_url="...", timeout=None)
\`\`\`

## Retry Configuration

Enable automatic retry for transient failures:

\`\`\`python
from pywats import pyWATS, RetryConfig

retry = RetryConfig(
    max_retries=3,        # Retry up to 3 times
    backoff=2.0,          # Exponential backoff (2s, 4s, 8s)
)

api = pyWATS(base_url="...", retry_config=retry)
result = api.product.get_product("ABC123")  # Auto-retries on failure
\`\`\`

## Correlation IDs

All requests automatically get correlation IDs for debugging:

\`\`\`python
import logging
logging.basicConfig(level=logging.INFO)

api = pyWATS(base_url="...")
api.product.get_product("ABC123")

# Logs show:
# [INFO] [a1b2c3d4] Getting product ABC123
# [INFO] [a1b2c3d4] Product retrieved successfully
\`\`\`
```

**File:** `examples/sync_with_config.py` (NEW)

```python
"""
Example: Using sync wrapper with timeout and retry configuration.
"""
from pywats import pyWATS, SyncConfig, RetryConfig

def main():
    # Option 1: Simple timeout
    api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        timeout=45.0  # 45 second timeout
    )
    
    # Option 2: With retry
    retry = RetryConfig(max_retries=3, backoff=2.0)
    api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        retry_config=retry
    )
    
    # Option 3: Full configuration
    config = SyncConfig(
        timeout=60.0,
        retry_enabled=True,
        retry=RetryConfig(max_retries=5, backoff=1.5),
        correlation_id_enabled=True
    )
    api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        sync_config=config
    )
    
    # Use normally - timeout/retry happen automatically
    try:
        product = api.product.get_product("ABC123")
        print(f"Got product: {product.part_number}")
    except TimeoutError:
        print("Request timed out")
    except ConnectionError:
        print("Connection failed after retries")

if __name__ == "__main__":
    main()
```

---

#### Task 4.3: Verify Type Stubs Unchanged (1 hour)

**Command:**
```bash
python scripts/generate_type_stubs.py --check
```

**Expected:** No changes to `.pyi` files

**If changes detected:**
- Review why stubs changed
- Ensure no unintended signature modifications
- Update if necessary

---

### Phase 5: Final Validation (Day 5 - 2 hours)

#### Task 5.1: Full Test Suite (1 hour)

```bash
# Run all tests
pytest tests/ -v

# Expected: 193+ tests passing (existing) + 20+ new tests
# Total: 215+ passing, 0 failures
```

**Key test suites:**
- `tests/integration/test_sync_timeout.py` (5-7 tests)
- `tests/integration/test_sync_retry.py` (7-10 tests)
- `tests/integration/test_sync_correlation.py` (3-5 tests)
- All existing tests should still pass

---

#### Task 5.2: Manual Testing (1 hour)

**Test with real WATS server:**

1. **Timeout Test:**
```python
# Set very short timeout and trigger it
api = pyWATS(base_url="https://slow-server", timeout=1.0)
try:
    api.analytics.get_yield(limit=10000)  # Slow query
except TimeoutError:
    print("✅ Timeout works")
```

2. **Retry Test:**
```python
# Temporarily disconnect network, reconnect
retry = RetryConfig(max_retries=5, backoff=1.0)
api = pyWATS(base_url="...", retry_config=retry)
result = api.product.get_product("ABC123")  # Should retry and succeed
```

3. **Correlation Test:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

api = pyWATS(base_url="...")
api.product.get_product("ABC123")
# Verify correlation IDs in logs
```

---

## File Change Summary

### New Files (3)
1. `tests/integration/test_sync_timeout.py` (~150 lines)
2. `tests/integration/test_sync_retry.py` (~200 lines)
3. `tests/integration/test_sync_correlation.py` (~80 lines)
4. `examples/sync_with_config.py` (~60 lines)

### Modified Files (3)
1. `src/pywats/pywats.py` (~100 lines modified, ~80 lines added)
2. `src/pywats/core/config.py` (~50 lines added)
3. `src/pywats/core/logging.py` (~30 lines added)
4. `docs/guides/sync-vs-async.md` (~100 lines added)

**Total:** 7 files, ~850 lines of code

---

## Dependencies

### Python Packages
No new dependencies! Uses stdlib only:
- `asyncio` (timeout via `wait_for`)
- `contextvars` (correlation IDs)
- `time` (retry backoff)
- `uuid` (correlation ID generation)

### Internal Dependencies
- Existing async services (no changes)
- Type stub generation (verify unchanged)
- Logging infrastructure (minor enhancement)

---

## Rollback Strategy

**If critical issues found:**

1. **Branch:** Work in feature branch `feature/sync-wrapper-enhancements`
2. **Incremental commits:** Commit after each phase
3. **Rollback point:** Can revert to any phase
4. **Testing gates:** Don't merge until all tests pass

**Rollback command:**
```bash
git revert <commit-hash>
# OR
git reset --hard origin/main
```

---

## Success Metrics

**Code Quality:**
- [ ] All new code has 100% test coverage
- [ ] 0 mypy errors
- [ ] 0 lint warnings
- [ ] Type stubs verified unchanged

**Functionality:**
- [ ] Timeout works reliably (10/10 manual tests)
- [ ] Retry succeeds after transient failures (10/10 tests)
- [ ] Correlation IDs in all logs
- [ ] Backward compatible (existing code works)

**Performance:**
- [ ] No performance regression on sync operations
- [ ] Retry overhead < 100ms per attempt
- [ ] Correlation ID overhead negligible

---

## Timeline

**Day 1:** Phase 1 (Core Infrastructure) - 4 hours  
**Day 2:** Phase 2 (Retry Logic) - 4 hours  
**Day 3:** Phase 3 (Configuration & Integration) - 3 hours  
**Day 4:** Phase 4 (Testing & Docs) - 4 hours  
**Day 5:** Phase 5 (Final Validation) - 2 hours  

**Total:** 17 hours (~2-3 days with testing/polish)

---

**Implementation Plan Complete:** Ready to create TODO checklist.
