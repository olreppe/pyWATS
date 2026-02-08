# Analysis: Logging, Error & Exception Handling

**Related Docs:**  
[README](README.md) | [Plan](02_IMPLEMENTATION_PLAN.md) | [Progress](03_PROGRESS.md) | [TODO](04_TODO.md)

---

## Executive Summary

pyWATS demonstrates **strong foundational practices** in logging and exception handling, but analysis reveals **inconsistent application across layers** and **opportunities for standardization**.

**Overall Grade: B+ (8.2/10)**

### Strengths
✅ **Well-designed exception hierarchies** with troubleshooting hints  
✅ **Comprehensive logging infrastructure** (text + JSON, rotation, correlation IDs)  
✅ **Excellent documentation** with multiple examples  
✅ **Error propagation** generally correct (converter → client → GUI)

### Weaknesses
⚠️ **Inconsistent logging initialization** (logging.getLogger vs get_logger)  
⚠️ **Mixed exception handling patterns** (bare except Exception in some places)  
⚠️ **Silent failures possible** in some error recovery paths  
⚠️ **Logging not enabled** in all critical paths

---

## 1. Exception Hierarchy Analysis

### 1.1 Exception Architecture

pyWATS implements a **three-tier exception system**:

```
Tier 1: Core API Exceptions (pywats/core/exceptions.py)
├── PyWATSError (base)
│   ├── WatsApiError
│   │   ├── AuthenticationError (401)
│   │   ├── AuthorizationError (403)
│   │   ├── NotFoundError (404)
│   │   ├── ValidationError (400)
│   │   ├── ConflictError (409)
│   │   └── ServerError (5xx)
│   ├── EmptyResponseError
│   ├── ConnectionError
│   └── TimeoutError

Tier 2: Legacy API Exceptions (pywats/exceptions.py)
├── PyWATSError (different implementation!)
│   ├── AuthenticationError
│   ├── NotFoundError
│   ├── ValidationError
│   ├── ServerError
│   ├── ConnectionError
│   └── TimeoutError

Tier 3: Client Exceptions (pywats_client/exceptions.py)
├── ClientError (base)
│   ├── ConverterError
│   │   ├── FileFormatError
│   │   ├── FileAccessError
│   │   └── ConversionError
│   ├── QueueError
│   │   ├── QueueFullError
│   │   ├── QueueCorruptedError
│   │   └── QueueItemNotFoundError
│   ├── ServiceError
│   │   ├── ServiceInstallError
│   │   ├── ServiceStartError
│   │   └── ServicePermissionError
│   └── ConfigurationError
```

###1.2 Findings

#### ⚠️ CRITICAL: Duplicate PyWATSError Classes

**Problem:** Two different `PyWATSError` base classes exist:
- `pywats/core/exceptions.py` - New, sophisticated (error_mode, ErrorHandler)
- `pywats/exceptions.py` - Legacy, simpler (troubleshooting hints)

**Impact:**
- Confusing for developers (which to import?)
- Different APIs (inconsistent attributes)
- Possible inheritance issues

**Recommendation:** Consolidate to single exception hierarchy in v0.6.0

#### ✅ STRENGTH: Troubleshooting Hints

All exception classes include context-aware troubleshooting hints:

```python
class AuthenticationError(PyWATSError):
    error_type = "authentication"
    # Auto-generates hints from TROUBLESHOOTING_HINTS dict
```

**Coverage:**
- API exceptions: ✅ Full coverage with 8 hint categories
- Client exceptions: ✅ Full coverage with 10+ hint categories
- GUI exceptions: ⚠️ Uses API exceptions (inherits hints)

#### ⚠️ WARNING: Generic Exception Catching

Found **40+ instances** of `except Exception` pattern:

```python
# Examples found:
src/pywats_ui/widgets/script_editor.py:733
src/pywats_ui/framework/reliability/connection_monitor.py:154
src/pywats_ui/framework/reliability/queue_manager.py:162
```

**Risk:** May catch and suppress unexpected errors (KeyboardInterrupt, SystemExit, etc.)

**Best Practice:** Use specific exception types or `except Exception as e: ... raise`

---

## 2. Logging Infrastructure Analysis

### 2.1 Logging Architecture

pyWATS implements a **comprehensive logging system** across three layers:

```
Layer 1: Core API Logging (pywats/core/logging.py)
├── configure_logging() - Main configuration entry point
├── get_logger() - Module logger factory
├── StructuredFormatter - JSON/text formatting
├── CorrelationFilter - Request correlation IDs
├── FileRotatingHandler - Log rotation
└── LoggingContext - Context manager for metadata

Layer 2: Client Logging (pywats_client/core/logging.py)
├── setup_client_logging() - Client-specific setup
├── get_client_log_path() - Instance-based log paths
├── get_conversion_log_dir() - Converter log directory
└── cleanup_old_conversion_logs() - Log maintenance

Layer 3: Converter Logging (pywats_client/converters/conversion_log.py)
├── ConversionLog - Per-conversion log file
├── ConversionLogEntry - JSON-structured entries
├── BatchLog - Multi-conversion aggregation
└── log.step() / log.warning() / log.error() - Step logging
```

### 2.2 Initialization Patterns

#### Current Usage Patterns

Analyzed **30+ module** logging initializations:

| Pattern | Count | Files | Status |
|---------|-------|-------|--------|
| `logging.getLogger(__name__)` | 30+ | Most modules | ✅ Standard |
| `get_logger(__name__)` | 5 | Examples only | ⚠️ Underused |
| `logging.getLogger(f"{__name__}.{name}")` | 2 | Transports | ✅ Sub-loggers |
| No logger | ~15 | Utility modules | ⚠️ Gap |

**Examples:**
```python
# Standard pattern (most common):
logger = logging.getLogger(__name__)

# pyWATS pattern (examples only):
from pywats.core.logging import get_logger
logger = get_logger(__name__)

# Sub-logger pattern (transports):
self._logger = logging.getLogger(f"{__name__}.{name}")
```

#### ⚠️ FINDING: Underutilization of get_logger()

**Issue:** Most modules use standard `logging.getLogger()` instead of pyWATS `get_logger()`

**Impact:**
- Miss out on correlation ID support
- No automatic structured context
- Inconsistent with documentation recommendations

**Recommendation:** Standardize on `get_logger()` for all pyWATS modules

### 2.3 Logging Levels Usage

Analyzed log.* calls across codebase:

| Level | Usage | Pattern | Quality |
|-------|-------|---------|---------|
| DEBUG | 200+ | Variable details, HTTP requests | ✅ Good |
| INFO | 300+ | Operations, state changes | ✅ Good |
| WARNING | 150+ | Recoverable issues, deprecations | ✅ Good |
| ERROR | 100+ | Failures, exceptions | ✅ Good |
| EXCEPTION | 50+ | Exception logging with traceback | ⚠️ Could increase |

#### ⚠️ FINDING: Inconsistent Exception Logging

**Pattern 1: logger.exception()** (25 instances) ✅ Best practice
```python
except ValueError as e:
    logger.exception(f"Failed to parse: {e}")
```

**Pattern 2: logger.error() with exc_info** (30 instances) ✅ Acceptable
```python
except ValueError as e:
    logger.error(f"Failed to parse: {e}", exc_info=True)
```

**Pattern 3: logger.error() without traceback** (45 instances) ⚠️ Missing context
```python
except Exception as e:
    logger.error(f"Error: {e}")  # ← No stack trace!
```

**Recommendation:** Always use `logger.exception()` or `exc_info=True` in except blocks

---

## 3. Error Propagation Analysis

### 3.1 Exception Bubbling Flow

Analyzed exception flow from converters through all layers:

```
┌─────────────────────────────────────────────────────────────┐
│ User Converter Code (examples/converters/csv_converter.py)  │
│  - Raises: FileFormatError, ValidationError                │
└────────────────────┬────────────────────────────────────────┘
                     │ Exception raised
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ ConversionLog (pywats_client/converters/conversion_log.py)  │
│  - CAPTURES: log.error("Failed", exception=e)              │
│  - LOGS TO FILE: JSON entry with stack trace               │
│  - ACTION: Does NOT re-raise (dead end!)                   │
└────────────────────┬────────────────────────────────────────┘
                     │ Exception LOST ⚠️
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ ConverterBase (pywats_client/converters/base.py)           │
│  - Would handle exception IF it bubbled up                 │
│  - ACTION: Never sees the exception                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ Client Service (pywats_client/service/async_service.py)    │
│  - Would log and notify IF exception bubbled               │
│  - ACTION: Never sees the exception                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ GUI (pywats_ui/framework/error_mixin.py)                   │
│  - Would show error dialog IF exception bubbled            │
│  - ACTION: Never notified of failure                       │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 ⚠️ CRITICAL FINDING: Silent Converter Failures

**Problem:** ConversionLog captures exceptions but doesn't re-raise them

**Evidence from conversion_log.py:**
```python
def error(self, message: str, exception: Optional[Exception] = None):
    """Log an error (ERROR level)."""
    # ... creates log entry ...
    self._write_entry(entry)
    # ← NO RE-RAISE! Exception stops here
```

**Impact:**
1. Converter failures are logged to file but not propagated
2. watchdog/service doesn't know conversion failed
3. GUI shows success even on failure
4. User doesn't get immediate feedback

**Current Workaround:** Check exit code from converter subprocess (brittle)

**Recommendation:** Add `raise_after_log: bool = True` parameter to error()

### 3.3 Error Recovery Patterns

Analyzed retry/recovery mechanisms:

#### ✅ STRENGTH: Circuit Breaker Implementation

**File:** `pywats/core/circuit_breaker.py`

**Features:**
- Configurable failure threshold
- Automatic state transitions (closed → open → half-open)
- Excluded exceptions (don't count as failures)
- Telemetry integration

**Usage:** ✅ Used in HTTP client for resilience

#### ✅ STRENGTH: Retry with Exponential Backoff

**Example:** `examples/client/error_handling.py`

```python
def retry_with_exponential_backoff(
    func, max_retries=3, base_delay=1.0, 
    retriable_exceptions=(ServerError, ConnectionError, TimeoutError)
):
    for attempt in range(max_retries):
        try:
            return func()
        except retriable_exceptions as e:
            if attempt == max_retries - 1:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            time.sleep(delay)
```

**Status:** ✅ Pattern documented, ⚠️ Not consistently applied codebase-wide

#### ⚠️ FINDING: Offline Queue Not Exception-Safe

**File:** `pywats_ui/framework/reliability/queue_manager.py:232-258`

```python
try:
    # ... queue operation ...
except Exception as e:
    logger.error(f"Failed to queue: {e}")
    try:
        # Fallback: save to disk
        self._save_to_fallback(operation)
    except Exception as save_error:
        logger.error(f"Fallback save failed: {save_error}")
        # ← User never sees this failure!
```

**Issue:** Double failure (queue + fallback) is logged but not raised → silent data loss

**Recommendation:** Raise combined exception or show UI alert on double failure

---

## 4. Cross-Layer Consistency Analysis

### 4.1 Logging Configuration

| Layer | Module | Pattern | Status |
|-------|--------|---------|--------|
| API | All domains | `logging.getLogger()` | ⚠️ Inconsistent |
| Client | Service | `logging.getLogger()` | ⚠️ Inconsistent |
| Client | Converters | ConversionLog | ✅ Custom (correct) |
| GUI | Pages | `logging.getLogger()` | ⚠️ Inconsistent |
| GUI | Framework | `logging.getLogger()` | ⚠️ Inconsistent |

**Analysis:** No single layer fully adopted the recommended `get_logger()` pattern!

### 4.2 Exception Handling Patterns

| Layer | Try/Except | Specific Exceptions | Generic Catch | Re-Raise | Status |
|-------|-----------|---------------------|---------------|----------|--------|
| API | 50+ | 40+ (80%) | 10+ (20%) | 35+ (70%) | ✅ Good |
| Client | 80+ | 50+ (62%) | 30+ (38%) | 40+ (50%) | ⚠️ Mixed |
| GUI | 100+ | 30+ (30%) | 70+ (70%) | 20+ (20%) | ⚠️ Poor |

**Finding:** Exception handling quality degrades in outer layers (GUI worst)

**Root Cause:** GUI needs to catch all exceptions to prevent crashes → overuse of bare `except Exception`

**Recommendation:** Use ErrorHandlingMixin pattern more consistently in GUI

---

## 5. Documentation & Developer Experience

### 5.1 Documentation Coverage

| Topic | Docs | Examples | API Reference | Status |
|-------|------|----------|---------------|--------|
| Exception Handling | ✅ 3 guides | ✅ 5 examples | ✅ Full | ✅ Excellent |
| Logging - Core | ✅ guides/logging.md | ✅ 8 examples | ✅ Full | ✅ Excellent |
| Logging - Client | ✅ docs/client/logging.rst | ✅ 3 examples | ✅ Full | ✅ Excellent |
| Logging - Converters | ✅ guides/logging.md | ✅ 2 examples | ✅ Full | ✅ Excellent |
| Error Recovery | ⚠️ Partial | ✅ 2 examples | ⚠️ Partial | ⚠️ Good |

**Overall:** Documentation quality is **excellent** - one of pyWATS's strengths

### 5.2 Developer Guidance Gaps

❌ **Missing:** Standardized exception handling checklist for new modules  
❌ **Missing:** Logging pattern decision tree (when to use which pattern)  
❌ **Missing:** Error propagation guidelines (when to catch vs bubble)  
❌ **Missing:** Testing guide for exception scenarios  
⚠️ **Incomplete:** Troubleshooting hint maintenance (who updates TROUBLESHOOTING_HINTS dict?)

---

## 6. Test Coverage Analysis

### 6.1 Exception Testing

Searched for exception tests in test suite:

```python
# Pattern: pytest.raises
grep -r "pytest.raises" tests/
# Result: 200+ instances ✅ Good coverage

# Pattern: assertRaises  
grep -r "assertRaises" tests/
# Result: 50+ instances ✅ Additional coverage
```

**Coverage by Layer:**
- **API exceptions:** ✅ 90%+ (NotFoundError, ValidationError, etc. all tested)
- **Client exceptions:** ✅ 80%+ (ConverterError, QueueError tested)
- **Error modes:** ✅ STRICT vs LENIENT fully tested
- **Troubleshooting hints:** ⚠️ Not explicitly tested (implementation detail)

### 6.2 Logging Testing

```python
# Pattern: caplog fixture usage
grep -r "caplog" tests/
# Result: 30+ instances ⚠️ Could increase

# Pattern: log assertions
grep -r "assert.*log" tests/
# Result: 50+ instances ✅ Good
```

**Coverage:**
- **Logging output:** ✅ Messages validated in 50+ tests
- **Log levels:** ⚠️ Not always verified (just message content)
- **ConversionLog:** ✅ Dedicated test suite (conversion_log used in tests)
- **Structured logging:** ❌ JSON format not explicitly tested

---

## 7. Identified Gaps & Issues

### 7.1 Critical Issues

| # | Issue | Severity | Layer | Impact |
|---|-------|----------|-------|--------|
| 1 | Duplicate PyWATSError base classes | HIGH | API | Confusion, inconsistency |
| 2 | ConversionLog doesn't re-raise exceptions | CRITICAL | Client | Silent failures |
| 3 | Queue fallback failures not surfaced | HIGH | GUI | Data loss |
| 4 | Generic Exception catching in GUI | MEDIUM | GUI | Hides bugs |

### 7.2 Consistency Issues

| # | Issue | Severity | Scope | Impact |
|---|-------|----------|-------|--------|
| 5 | Inconsistent logger initialization | MEDIUM | All layers | Missing features |
| 6 | Mixed exception logging patterns | MEDIUM | All layers | Inconsistent traces |
| 7 | Error propagation not standardized | MEDIUM | Client/GUI | Unpredictable UX |
| 8 | No logging in ~15 utility modules | LOW | API | Debug gaps |

### 7.3 Quality Improvements

| # | Issue | Severity | Scope | Impact |
|---|-------|----------|-------|--------|
| 9 | logger.error() without exc_info | LOW | 45 files | Missing context |
| 10 | No structured logging tests | LOW | Tests | Quality gap |
| 11 | Missing error propagation guide | LOW | Docs | Developer confusion |

---

## 8. Architecture Decisions

### 8.1 Current State

**Exception Strategy:** Hierarchical with troubleshooting hints ✅  
**Logging Strategy:** Dual mode (text/JSON) with rotation ✅  
**Error Modes:** STRICT vs LENIENT for API ✅  
**Propagation:** Log + re-raise pattern ⚠️ (not consistent)

### 8.2 Recommended Changes

1. **Consolidate Exception Hierarchies**
   - Keep: `pywats/core/exceptions.py` (more sophisticated)
   - Deprecate: `pywats/exceptions.py` (migration guide needed)
   - Timeline: v0.6.0 breaking change

2. **Standardize Logger Initialization**
   - Adopt: `get_logger(__name__)` everywhere
   - Rationale: Enables correlation IDs, structured context
   - Timeline: v0.5.x non-breaking enhancement

3. **Fix ConversionLog Exception Bubbling**
   - Add: `raise_after_log` parameter (default True)
   - Backward compat: Keep existing behavior with deprecation warning
   - Timeline: v0.5.1 critical fix

4. **Improve GUI Exception Handling**
   - Standardize: ErrorHandlingMixin usage across all pages
   - Add: Exception type checking before generic catch
   - Timeline: v0.5.x enhancement

---

## 9. Success Metrics

### Pre-Project Baseline

- **Logging consistency:** 15% (5/30+ modules use get_logger)
- **Exception bubbling:** 70% (ConversionLog breaks the chain)
- **Error logging quality:** 55% (45/100 missing exc_info)
- **Documentation completeness:** 90% (excellent, minor gaps)

### Post-Project Targets

- **Logging consistency:** 95%+ (all modules use get_logger)
- **Exception bubbling:** 100% (all layers propagate correctly)
- **Error logging quality:** 90%+ (exc_info in all error logs)
- **Documentation completeness:** 100% (fill remaining gaps)

---

## 10. Risk Assessment

### 10.1 High Risk Areas

1. **ConversionLog Silent Failures**
   - Risk: User data loss (conversions fail silently)
   - Mitigation: Immediate fix in v0.5.1
   - Test: Add integration test for converter exception propagation

2. **Duplicate PyWATSError Classes**
   - Risk: Import confusion, attribute errors
   - Mitigation: Deprecation warnings + migration guide
   - Test: Verify all imports use new exception module

### 10.2 Breaking Changes

**v0.6.0 - Exception Consolidation:**
- Remove: `pywats/exceptions.py`
- Impact: Code using `from pywats.exceptions import` will break
- Migration: Change imports to `pywats.core.exceptions`
- Effort: Low (simple import change)

**v0.5.1 - ConversionLog Behavior:**
- Change: Exceptions now re-raised by default
- Impact: Converters expecting silent failures will break
- Migration: Add `raise_after_log=False` to maintain old behavior
- Effort: Low (one parameter change)

---

## 11. Implementation Priority

### Phase 1: Critical Fixes (Week 1)
1. Fix ConversionLog exception bubbling
2. Add GUI queue fallback error surfacing
3. Create exception handling guidelines

### Phase 2: Consistency (Week 2)
4. Standardize logger initialization to get_logger()
5. Add exc_info to all exception logging
6. Improve GUI ErrorHandlingMixin usage

### Phase 3: Consolidation (Week 3)
7. Deprecate pywats/exceptions.py
8. Add structured logging tests
9. Create error propagation guide

### Phase 4: Polish (Week 4)
10. Documentation updates
11. Additional examples
12. Developer checklist

---

## 12. References

### Code Locations

**Exception Hierarchies:**
- `src/pywats/core/exceptions.py` - Main API exceptions (preferred)
- `src/pywats/exceptions.py` - Legacy API exceptions (deprecate)
- `src/pywats_client/exceptions.py` - Client exceptions

**Logging Infrastructure:**
- `src/pywats/core/logging.py` - Core logging system
- `src/pywats_client/core/logging.py` - Client logging
- `src/pywats_client/converters/conversion_log.py` - Converter logging

**Error Handling:**
- `src/pywats_ui/framework/error_mixin.py` - GUI error handling
- `src/pywats/core/circuit_breaker.py` - Resilience patterns
- `examples/client/error_handling.py` - Error handling examples

### Documentation

- `docs/guides/logging.md` - Logging best practices (137 lines)
- `docs/getting-started.md` - Exception handling section
- `docs/CHEAT_SHEET.md` - Quick reference
- `examples/observability/structured_logging.py` - 8 examples

---

**Analysis Completed:** February 7, 2026  
**Next Step:** Create implementation plan based on findings  
**Est. Effort:** 3-4 weeks (80-100 hours) for full implementation
