# Sync Wrapper Enhancements

**Project ID:** sync-wrapper-enhancements  
**Sprint Size:** 3-5 days  
**Priority:** Low  
**Status:** ✅ Ready to Start - Full project documentation complete  

---

## 🎯 Goal

Add timeout control, retry logic, and correlation IDs to the synchronous wrapper for better production reliability and debugging.

**Key Constraint:** Type stubs are auto-generated from async services (see `scripts/generate_type_stubs.py`). All enhancements must work with the existing type stub generation without requiring changes to async service signatures.

---

## 📋 Background

The synchronous wrapper works well for basic use cases but lacks production-grade features. Adding these features improves reliability without changing the core API or requiring type stub modifications.

**Current Architecture:**
- Generic `SyncServiceWrapper` uses `__getattr__` to wrap async methods
- Type stubs (`.pyi` files) auto-generated from async services
- Event loop management in `_run_sync()` function

**What's Complete:**
- ✅ Basic sync wrapper functionality
- ✅ Async client fully featured
- ✅ Type safety via auto-generated stubs
- ✅ Type checking (mypy: 0 errors)

**What This Project Adds:**
- Configurable timeout control (default: 30s)
- Automatic retry with exponential backoff
- Request correlation IDs for debugging
- Config-based approach (backward compatible)

---

## ✅ Acceptance Criteria

**Must Have:**
- [ ] Sync wrapper accepts timeout via config (default: 30s)
- [ ] Retry logic with configurable max attempts (default: 3)
- [ ] Exponential backoff between retries (default: 2.0x multiplier)
- [ ] Correlation IDs automatically generated and logged
- [ ] Type stubs remain unchanged (verify with `--check`)
- [ ] All existing tests pass + 20+ new tests
- [ ] Backward compatible (existing code works)

**Should Have:**
- [ ] SyncClientConfig class for global configuration
- [ ] Retry only on specific error types (ConnectionError, TimeoutError)
- [ ] Correlation IDs in all log messages
- [ ] Clear error messages with context

**Nice to Have:**
- [ ] Request timing metrics (deferred)
- [ ] Circuit breaker pattern (future enhancement)
- [ ] Per-method timeout override (future enhancement)

---

## 🏗️ Solution Architecture

### Config-Based Approach

**Why:** Type stubs are generated from async signatures. Adding parameters to sync methods would require changing async signatures (bad). Instead, use configuration at client level.

```python
# Option 1: Simple timeout
api = pyWATS(base_url="...", timeout=60.0)

# Option 2: With retry
from pywats import RetryConfig
retry = RetryConfig(max_retries=3, backoff=2.0)
api = pyWATS(base_url="...", retry_config=retry)

# Option 3: Full config
from pywats import SyncConfig, RetryConfig
config = SyncConfig(
    timeout=45.0,
    retry_enabled=True,
    retry=RetryConfig(max_retries=5, backoff=1.5),
    correlation_id_enabled=True
)
api = pyWATS(base_url="...", sync_config=config)
```

### Key Implementation Points

1. **Timeout:** Enhanced `_run_sync()` uses `asyncio.wait_for()`
2. **Retry:** Decorator wraps sync methods with retry logic
3. **Correlation:** Context variables track request IDs
4. **Type Stubs:** Unaffected - no signature changes needed

---

## 📊 Work Breakdown

**Total Estimate:** 17 hours (~3 days)

### Phase 1: Core Infrastructure (4 hours)
- Create `SyncConfig` and `RetryConfig` dataclasses
- Enhance `_run_sync()` with timeout support
- Add correlation ID context variable
- Update logging to include correlation IDs

### Phase 2: Retry Logic (4 hours)
- Implement `_with_retry()` wrapper function
- Integrate retry into `SyncServiceWrapper`
- Test retry with exponential backoff

### Phase 3: Configuration & Integration (3 hours)
- Update `pyWATS.__init__()` with new parameters
- Pass config to all 9 service wrappers
- Test config propagation

### Phase 4: Testing & Documentation (4 hours)
- Write 20+ integration tests
- Update `docs/guides/sync-vs-async.md`
- Create `examples/sync_with_config.py`
- Verify type stubs unchanged

### Phase 5: Final Validation (2 hours)
- Full test suite (215+ tests)
- Manual testing with real server
- Verify backward compatibility

---

## 📂 Files Involved

**New Files (4):**
- `tests/integration/test_sync_timeout.py` (~150 lines)
- `tests/integration/test_sync_retry.py` (~200 lines)
- `tests/integration/test_sync_correlation.py` (~80 lines)
- `examples/sync_with_config.py` (~60 lines)

**Modified Files (4):**
- `src/pywats/pywats.py` (~180 lines modified/added)
- `src/pywats/core/config.py` (~50 lines added)
- `src/pywats/core/logging.py` (~30 lines added)
- `docs/guides/sync-vs-async.md` (~100 lines added)

**Verified Unchanged:**
- All `.pyi` type stub files (auto-generated)

**Total:** 8 files, ~850 lines of code

---

## 🧪 Testing Strategy

**Integration Tests (20+ tests):**
```python
# Timeout tests
def test_timeout_on_slow_server()
def test_no_timeout_completes()

# Retry tests
def test_retry_success_after_failures()
def test_retry_exhausted()
def test_retry_only_on_transient_errors()

# Correlation tests
def test_correlation_id_in_logs()
def test_correlation_id_unique_per_request()
```

**Manual Validation:**
- Timeout with real slow queries
- Retry with network interruption
- Correlation IDs in production logs

**Type Stub Verification:**
```bash
python scripts/generate_type_stubs.py --check
# Should show: No changes needed
```

---

## 🔗 Dependencies

**Blocked By:** None  
**Blocks:** None

**Python Stdlib Only (no new dependencies):**
- `asyncio` (timeout via `wait_for`)
- `contextvars` (correlation IDs)
- `time` (retry backoff)
- `uuid` (correlation ID generation)

---

## 📈 Success Metrics

**Quantitative:**
- [ ] All sync wrapper methods support timeout
- [ ] Retry tested with 10+ scenarios
- [ ] Correlation IDs in 100% of requests
- [ ] 215+ tests passing (193 existing + 20+ new)
- [ ] 0 mypy errors
- [ ] Type stubs verified unchanged

**Qualitative:**
- [ ] Production reliability improved
- [ ] Easier debugging with correlation IDs
- [ ] Backward compatible (no breaking changes)
- [ ] Developer experience enhanced

---

## 📝 Project Documentation

**Complete Documentation Available:**
- **[ANALYSIS.md](ANALYSIS.md)** - Technical analysis of current architecture, type stub generation, and proposed solutions
- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Detailed phase-by-phase implementation with code examples
- **[TODO.md](TODO.md)** - Complete task checklist with time estimates
- **[ORIGINAL_STAGE_4_ANALYSIS.md](ORIGINAL_STAGE_4_ANALYSIS.md)** - Historical context (deferred items)
- **[TYPE_SAFETY_CONTEXT.md](TYPE_SAFETY_CONTEXT.md)** - Background on type safety approach

**Start Here:**
1. Read [ANALYSIS.md](ANALYSIS.md) for architecture understanding
2. Follow [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for step-by-step guide
3. Track progress in [TODO.md](TODO.md)

---

## 🚨 Important Notes

**Type Stub Generation:**
- Type stubs are auto-generated from async services
- Do NOT modify `.pyi` files manually
- Verify stubs unchanged with `--check` after implementation
- See `scripts/generate_type_stubs.py` for details

**Backward Compatibility:**
- All enhancements are opt-in via configuration
- Existing code without config will work unchanged
- Default timeout is 30s (can be disabled with `timeout=None`)

**Out of Scope:**
- Per-method timeout override (requires signature changes)
- Circuit breaker pattern (separate project)
- Performance metrics (separate concern)
- GUI widget cleanup (unrelated)
- TODO/FIXME resolution (ongoing maintenance)

---

**Ready to Start:** ✅ All planning complete, architecture validated, dependencies verified


---

## 📋 Background

The synchronous wrapper works well for basic use cases but lacks production-grade features like timeout control and retry logic for transient failures. Adding these features improves reliability without changing the core API.

**What's Already Complete:**
- ✅ Basic sync wrapper functionality
- ✅ Async client fully featured
- ✅ Type safety (mypy: 0 errors)

**What This Project Adds:**
- Configurable timeout control
- Automatic retry with exponential backoff
- Request correlation IDs for debugging

---

## ✅ Acceptance Criteria

**Must Have:**
- [ ] Sync wrapper accepts timeout parameter (default: 30s)
- [ ] Retry logic with configurable max attempts (default: 3)
- [ ] Exponential backoff between retries
- [ ] Correlation IDs automatically generated and logged

**Should Have:**
- [ ] SyncClientConfig class for global configuration
- [ ] Per-request timeout override
- [ ] Retry on specific error types only (network, timeout)

**Nice to Have:**
- [ ] Request timing metrics
- [ ] Circuit breaker pattern
- [ ] Callback hooks for retry events

---

## 📊 Work Breakdown

### Task 1: Timeout Configuration (3 hours)

**Add timeout parameter:**
```python
# Before
result = client.get_product(part_number="ABC123")

# After
result = client.get_product(
    part_number="ABC123",
    timeout=30.0  # Configurable timeout in seconds
)
```

**Implementation:**
- Add timeout parameter to all sync wrapper methods
- Pass timeout to underlying async call
- Raise TimeoutError on expiration
- Test timeout behavior

**Files:**
- `src/pywats/sync_wrapper.py` - Add timeout support
- `tests/integration/test_sync_wrapper.py` - Test timeouts

---

### Task 2: Retry Logic (4 hours)

**Add retry with exponential backoff:**
```python
from pywats import SyncClientConfig

config = SyncClientConfig(
    max_retries=3,
    retry_backoff=2.0,  # Exponential backoff multiplier
    retry_on_errors=[TimeoutError, ConnectionError]
)

client = SyncWATSClient(config=config)
```

**Implementation:**
- Create SyncClientConfig dataclass
- Implement retry decorator
- Exponential backoff: wait = backoff^attempt (2s, 4s, 8s)
- Only retry on transient errors
- Log retry attempts

**Files:**
- `src/pywats/sync_wrapper.py` - Retry logic
- `src/pywats/config.py` - SyncClientConfig
- `tests/integration/test_sync_retry.py` - Test retries

---

### Task 3: Correlation IDs (3 hours)

**Auto-generate correlation IDs:**
```python
# Automatic correlation ID in logs
import logging

# Every sync request gets a correlation ID
result = client.get_product(part_number="ABC123")
# Logs show: [correlation_id=abc-123-def] Getting product ABC123
```

**Implementation:**
- Generate UUID for each request
- Store in context variable
- Include in all log statements
- Return in exceptions for debugging

**Files:**
- `src/pywats/core/correlation.py` - Correlation ID logic
- `src/pywats/sync_wrapper.py` - Integrate correlation IDs
- `src/pywats/core/logging.py` - Include in log format

---

## 🧪 Testing Strategy

**Unit Tests:**
```python
def test_sync_timeout():
    """Verify timeout raises TimeoutError"""
    
def test_sync_retry_success_after_failures():
    """Verify retry succeeds after transient errors"""
    
def test_sync_retry_exhausted():
    """Verify gives up after max retries"""
    
def test_correlation_id_in_logs():
    """Verify correlation ID appears in logs"""
```

**Integration Tests:**
- Real timeout scenarios
- Network failures with retry
- Correlation ID end-to-end

---

## 📂 Files Involved

**Create:**
- `src/pywats/core/correlation.py` (~50 lines)
- `tests/integration/test_sync_retry.py` (~100 lines)

**Modify:**
- `src/pywats/sync_wrapper.py` (~200 lines modified)
- `src/pywats/config.py` - Add SyncClientConfig (~30 lines)
- `src/pywats/core/logging.py` - Add correlation ID support (~20 lines)
- `tests/integration/test_sync_wrapper.py` - Add timeout tests (~50 lines)

**Document:**
- `docs/guides/sync-vs-async.md` - Document new features
- `examples/sync_with_retry.py` - Example usage

---

## 🚀 Implementation Steps

**Day 1: Timeout Support**
- Add timeout parameter to sync wrapper methods
- Test timeout behavior
- Document usage

**Day 2: Retry Logic**
- Create SyncClientConfig
- Implement retry decorator with exponential backoff
- Test retry scenarios

**Day 3: Correlation IDs & Polish**
- Add correlation ID generation
- Update logging
- Create examples
- Final testing and documentation

**Total Estimate:** 10-12 hours (2-3 days)

---

## 🔗 Dependencies

**Blocked By:** None  
**Blocks:** None

---

## 📈 Success Metrics

**Quantitative:**
- [ ] All sync wrapper methods support timeout parameter
- [ ] Retry logic tested with 10+ scenarios
- [ ] Correlation IDs in 100% of requests
- [ ] All tests passing

**Qualitative:**
- [ ] Production reliability improved
- [ ] Easier debugging with correlation IDs
- [ ] Developer experience enhanced

---

## 📝 Notes

**Out of Scope:**
The following items from the original "api-quality-sprint" were removed as too broad:
- GUI widget cleanup (needs separate user-supervised project)
- Converter decorator improvements (separate concern)
- TODO/FIXME resolution (ongoing maintenance, not a sprint)
- Pre-commit hook updates (maintenance task)

These should be tracked separately if needed.

---

**Ready to Start:** ✅ Clear scope, focused on sync wrapper only
