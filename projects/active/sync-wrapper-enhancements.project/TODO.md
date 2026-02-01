# Sync Wrapper Enhancement - Implementation Checklist

**Project:** sync-wrapper-enhancements  
**Sprint:** 3-5 days  
**Status:** Not Started  

---

## Phase 1: Core Infrastructure (Day 1 - 4 hours)

### Task 1.1: Create SyncConfig Dataclass ⏱️ 1 hour
- [ ] Add `RetryConfig` dataclass to `src/pywats/core/config.py`
  - [ ] `max_retries: int = 3`
  - [ ] `backoff: float = 2.0`
  - [ ] `retry_on_errors: Tuple[Type[Exception], ...]`
- [ ] Add `SyncConfig` dataclass to `src/pywats/core/config.py`
  - [ ] `timeout: Optional[float] = 30.0`
  - [ ] `retry_enabled: bool = False`
  - [ ] `retry: RetryConfig`
  - [ ] `correlation_id_enabled: bool = True`
- [ ] Write unit tests for config dataclasses
- [ ] Verify defaults work correctly

### Task 1.2: Enhance _run_sync() with Timeout ⏱️ 1.5 hours
- [ ] Update `_run_sync()` signature in `src/pywats/pywats.py`
  - [ ] Add `timeout: Optional[float] = None` parameter
  - [ ] Add `correlation_id: Optional[str] = None` parameter
- [ ] Implement timeout using `asyncio.wait_for()`
- [ ] Convert `asyncio.TimeoutError` to stdlib `TimeoutError`
- [ ] Implement correlation ID context management
- [ ] Write tests for timeout functionality
  - [ ] Test timeout triggers TimeoutError
  - [ ] Test timeout None works (no timeout)
  - [ ] Test timeout with slow async operation

### Task 1.3: Add Correlation ID Support ⏱️ 1.5 hours
- [ ] Add correlation ID context var to `src/pywats/pywats.py`
  - [ ] Import `contextvars` and `uuid`
  - [ ] Create `correlation_id_var = contextvars.ContextVar('correlation_id')`
  - [ ] Add `generate_correlation_id()` function
- [ ] Update `src/pywats/core/logging.py`
  - [ ] Add `CorrelationFilter` class
  - [ ] Update `DEFAULT_FORMAT` to include correlation_id
  - [ ] Apply filter to default logger config
- [ ] Write tests for correlation ID
  - [ ] Test correlation ID appears in logs
  - [ ] Test correlation ID context isolation

---

## Phase 2: Retry Logic (Day 2 - 4 hours)

### Task 2.1: Implement Retry Wrapper ⏱️ 2 hours
- [ ] Add `_with_retry()` function to `src/pywats/pywats.py`
  - [ ] Accept `func`, `config: RetryConfig`, `correlation_id: str`
  - [ ] Implement retry loop with `range(config.max_retries + 1)`
  - [ ] Catch `config.retry_on_errors` exceptions
  - [ ] Calculate exponential backoff: `wait = config.backoff ** attempt`
  - [ ] Log retry attempts with correlation ID
  - [ ] Re-raise last error if all attempts fail
- [ ] Write tests for retry wrapper
  - [ ] Test success after N failures
  - [ ] Test exhaustion after max retries
  - [ ] Test backoff timing
  - [ ] Test only retries on specified errors

### Task 2.2: Integrate Retry into SyncServiceWrapper ⏱️ 2 hours
- [ ] Update `SyncServiceWrapper.__init__()` in `src/pywats/pywats.py`
  - [ ] Add `config: Optional[SyncConfig] = None` parameter
  - [ ] Store config in `self._config`
  - [ ] Set default `SyncConfig()` if none provided
- [ ] Update `SyncServiceWrapper.__getattr__()`
  - [ ] Generate correlation ID if enabled
  - [ ] Pass timeout and correlation ID to `_run_sync()`
  - [ ] Apply retry wrapper if `config.retry_enabled`
- [ ] Update `SyncProductServiceWrapper` similarly
- [ ] Write tests for wrapper integration
  - [ ] Test timeout passed to _run_sync
  - [ ] Test retry applied when enabled
  - [ ] Test retry not applied when disabled

---

## Phase 3: Configuration & Integration (Day 3 - 3 hours)

### Task 3.1: Update pyWATS Constructor ⏱️ 1 hour
- [ ] Update `pyWATS.__init__()` in `src/pywats/pywats.py`
  - [ ] Add `timeout: float = 30.0` parameter
  - [ ] Add `retry_config: Optional[RetryConfig] = None` parameter
  - [ ] Add `sync_config: Optional[SyncConfig] = None` parameter
  - [ ] Build `sync_config` from individual params if not provided
  - [ ] Store in `self._sync_config`
- [ ] Update docstring with new parameters
- [ ] Write tests for constructor
  - [ ] Test `timeout` parameter
  - [ ] Test `retry_config` parameter
  - [ ] Test `sync_config` overrides other params

### Task 3.2: Update All Service Properties ⏱️ 2 hours
- [ ] Update `product` property to pass `config=self._sync_config`
- [ ] Update `asset` property to pass config
- [ ] Update `production` property to pass config
- [ ] Update `report` property to pass config
- [ ] Update `software` property to pass config
- [ ] Update `analytics` property (and `app` alias) to pass config
- [ ] Update `rootcause` property to pass config
- [ ] Update `scim` property to pass config
- [ ] Update `process` property to pass config
- [ ] Write test verifying all services use config
  - [ ] Test each service has correct timeout
  - [ ] Test each service has correct retry config

---

## Phase 4: Testing & Documentation (Day 4-5 - 6 hours)

### Task 4.1: Integration Tests ⏱️ 3 hours

**Timeout Tests:**
- [ ] Create `tests/integration/test_sync_timeout.py`
- [ ] Test `test_timeout_on_slow_server()`
- [ ] Test `test_no_timeout_completes()`
- [ ] Test `test_timeout_with_different_values()`
- [ ] Run timeout tests: `pytest tests/integration/test_sync_timeout.py -v`

**Retry Tests:**
- [ ] Create `tests/integration/test_sync_retry.py`
- [ ] Test `test_retry_on_connection_error()`
- [ ] Test `test_retry_exhausted()`
- [ ] Test `test_retry_disabled_by_default()`
- [ ] Test `test_retry_with_custom_backoff()`
- [ ] Test `test_retry_only_on_specified_errors()`
- [ ] Run retry tests: `pytest tests/integration/test_sync_retry.py -v`

**Correlation Tests:**
- [ ] Create `tests/integration/test_sync_correlation.py`
- [ ] Test `test_correlation_id_in_logs()`
- [ ] Test `test_correlation_id_disabled()`
- [ ] Test `test_correlation_id_unique_per_request()`
- [ ] Run correlation tests: `pytest tests/integration/test_sync_correlation.py -v`

### Task 4.2: Documentation Updates ⏱️ 2 hours
- [ ] Update `docs/guides/sync-vs-async.md`
  - [ ] Add "Timeout Configuration" section with examples
  - [ ] Add "Retry Configuration" section with examples
  - [ ] Add "Correlation IDs" section explaining debugging
  - [ ] Add "Production Best Practices" section
- [ ] Create `examples/sync_with_config.py`
  - [ ] Example 1: Simple timeout
  - [ ] Example 2: With retry
  - [ ] Example 3: Full configuration
  - [ ] Add error handling examples
- [ ] Update README.md if needed (mention new features)

### Task 4.3: Verify Type Stubs Unchanged ⏱️ 1 hour
- [ ] Run `python scripts/generate_type_stubs.py --check`
- [ ] Verify no `.pyi` files changed
- [ ] If changes detected, investigate and ensure intentional
- [ ] Update type stub generation if necessary

---

## Phase 5: Final Validation (Day 5 - 2 hours)

### Task 5.1: Full Test Suite ⏱️ 1 hour
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] Verify all existing tests pass (193+ tests)
- [ ] Verify all new tests pass (20+ tests)
- [ ] Total expected: 215+ passing, 0 failures
- [ ] Run type checking: `mypy src/pywats/`
- [ ] Verify 0 mypy errors

### Task 5.2: Manual Testing ⏱️ 1 hour
- [ ] **Timeout Test:**
  - [ ] Set short timeout (1s)
  - [ ] Trigger slow operation
  - [ ] Verify TimeoutError raised
- [ ] **Retry Test:**
  - [ ] Simulate transient failures
  - [ ] Verify auto-retry succeeds
  - [ ] Check retry logs appear
- [ ] **Correlation Test:**
  - [ ] Enable debug logging
  - [ ] Make several requests
  - [ ] Verify correlation IDs in logs
  - [ ] Verify different requests have different IDs
- [ ] **Backward Compatibility Test:**
  - [ ] Run existing examples without changes
  - [ ] Verify they still work

---

## Completion Checklist

**Code Complete:**
- [ ] All code written and committed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Type stubs verified

**Quality Gates:**
- [ ] Code review (self or peer)
- [ ] No mypy errors
- [ ] No lint warnings
- [ ] Test coverage > 90% for new code

**Ready to Merge:**
- [ ] All tasks above completed
- [ ] Manual testing successful
- [ ] Branch rebased on main
- [ ] Merge request created

---

## Notes Section

**Blocked Items:**
- None currently

**Deferred Items:**
- Per-method timeout override (future enhancement)
- Circuit breaker pattern (future enhancement)
- Request timing metrics (future enhancement)

**Lessons Learned:**
(To be filled during implementation)

---

**Checklist Created:** February 1, 2026  
**Ready to Start:** ✅ All planning complete
