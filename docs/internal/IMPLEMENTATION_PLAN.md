# Implementation Plan: Architecture Review Response

This document evaluates the third-party architecture review against the actual pyWATS implementation and provides a prioritized implementation plan.

---

## Review Summary: What's Already Implemented ✅

The architecture review identified concerns that are **already addressed** in the codebase:

### 1. Error Handling & Exception Taxonomy ✅ DONE

**Review concern:** Stable error taxonomy with metadata

**Current implementation:**
- Complete exception hierarchy in `core/exceptions.py`:
  - `PyWATSError` (base) with `message`, `operation`, `details`, `cause`
  - `NotFoundError`, `ValidationError`, `AuthenticationError`, `AuthorizationError`
  - `ConflictError`, `ServerError`, `EmptyResponseError`
  - `ConnectionError`, `TimeoutError`
- `ErrorHandler` class with STRICT/LENIENT modes
- Status code mapping: 400→ValidationError, 401→AuthenticationError, etc.
- All exceptions include operation context and structured details

**Status:** ✅ Complete

### 2. Rate Limiting ✅ DONE

**Review concern:** Clarify scope, document for multi-instance

**Current implementation (`core/throttle.py`):**
- Thread-safe `RateLimiter` with sliding window algorithm
- Configurable: `max_requests=500`, `window_seconds=60`
- Per-instance limiter (documented in client.py)
- Statistics tracking: `total_requests`, `total_wait_time`, `throttle_count`
- Global limiter with `configure_throttling()` helper

**Status:** ✅ Complete (per-instance is correct approach)

### 3. HttpClient vs Repository vs Service Boundaries ✅ DONE

**Review concern:** Repositories should be only layer interacting with HttpClient

**Current implementation:**
- Services receive only repository instances (enforced in recent cleanup)
- Repositories use `ErrorHandler.handle_response()` consistently
- Services never see transport details

**Status:** ✅ Complete

### 4. Authentication Boundaries ✅ DONE

**Review concern:** API library should be stateless, client handles persistence

**Current implementation:**
- `pywats` API accepts only `base_url`, `token`, `timeout`, `verify_ssl`
- `pywats_client` handles:
  - Password-to-token exchange (`ConnectionService.authenticate()`)
  - Encrypted token storage (`core/encryption.py`)
  - Persistent connection state (`ConnectionConfig`)

**Status:** ✅ Complete

### 5. Online/Offline State Authority ✅ DONE

**Review concern:** Single source of truth for connectivity

**Current implementation (`services/connection.py`):**
- `ConnectionService` owns all connectivity state
- `ConnectionStatus` enum: DISCONNECTED, CONNECTING, ONLINE, OFFLINE, ERROR
- Callbacks via `on_status_change()` - services subscribe, don't poll

**Status:** ✅ Complete

### 6. Timeout & Transport Policy ✅ DONE

**Review concern:** Define explicitly

**Current implementation:**
- Connect timeout: 30s default (configurable)
- Read timeout: same as connect (httpx unified timeout)
- Retries handled by queue service, not transport layer

**Status:** ✅ Complete

---

## Gaps Requiring Implementation 🔧

### Priority 1: Critical for Production

#### 1.1 Idempotency Keys for Submissions ⚠️ NOT IMPLEMENTED

**Risk:** Duplicate server-side operations on retry after partial failure

**Current state:**
- `QueuedReport` has `report_id` (UUID) but it's not sent to server
- No idempotency header in HttpClient

**Implementation plan:**

```
Phase 1: Add client-side idempotency key generation
├── File: src/pywats/core/client.py
│   └── Add Idempotency-Key header support to _make_request()
│
├── File: src/pywats/domains/report/repository.py
│   └── Generate UUID for each submission, pass as header
│
└── File: src/pywats_client/services/report_queue.py
    └── Persist idempotency key with queued payload
    └── Reuse same key on retry

Phase 2: Optional server field (if WATS supports it)
└── Add client_submission_id to WSJF payload
```

**Effort:** 2-3 days
**Files:** 3

#### 1.2 Crash-Safe Queue Persistence ⚠️ PARTIAL

**Risk:** Data loss or corruption on crash

**Current state (`report_queue.py`):**
- Basic file-based JSON queue
- No atomic writes (temp file → rename pattern)
- No fsync
- State transitions not crash-safe

**Implementation plan:**

```
Phase 1: Atomic file writes
├── File: src/pywats_client/services/report_queue.py
│   └── _save_report(): write to temp file, fsync, rename
│   └── _move_to_completed(): same pattern
│   └── _move_to_failed(): same pattern
│
└── Add corruption detection on load (try/except with quarantine)

Phase 2 (Optional): SQLite backend
├── Create: src/pywats_client/services/queue_storage.py
│   └── QueueStorage protocol/interface
│   └── FileQueueStorage (current, improved)
│   └── SQLiteQueueStorage (new, optional)
│
└── Migrate ReportQueueService to use storage abstraction
```

**Effort:** 3-4 days (Phase 1), +3 days (Phase 2)
**Files:** 1-2 (Phase 1), +2 (Phase 2)

#### 1.3 Retry Policy by Error Type ⚠️ PARTIAL

**Risk:** Retrying non-retryable errors, hammering down servers

**Current state:**
- Fixed retry count (`max_retries=5`)
- Fixed interval (`retry_interval=60`)
- No exponential backoff
- No differentiation by error type
- No circuit breaker

**Implementation plan:**

```
Phase 1: Error-aware retry policy
├── Create: src/pywats_client/core/retry_policy.py
│   └── RetryPolicy dataclass (max_attempts, backoff, jitter)
│   └── is_retryable(exception) → bool
│   └── get_delay(attempt) → float
│   └── Error categorization:
│       - Retryable: ConnectionError, TimeoutError, 5xx
│       - Not retryable: ValidationError, AuthenticationError, 4xx
│
├── File: src/pywats_client/services/report_queue.py
│   └── Use RetryPolicy instead of fixed retry_interval
│   └── Check is_retryable() before incrementing attempts
│   └── 401/403: trigger re-authentication, don't count as retry
│
Phase 2: Circuit breaker
├── Create: src/pywats_client/core/circuit_breaker.py
│   └── CircuitBreaker class (failure_threshold, reset_timeout)
│   └── States: CLOSED, OPEN, HALF_OPEN
│
└── Integrate with ReportQueueService
```

**Effort:** 2-3 days (Phase 1), +2 days (Phase 2)
**Files:** 2-3

### Priority 2: Important for Stability

#### 2.1 Graceful Shutdown Semantics ⚠️ PARTIAL

**Current state:**
- `ReportQueueService.stop()` cancels task, but no checkpoint
- No explicit shutdown order
- Potential for in-flight work loss

**Implementation plan:**

```
File: src/pywats_client/services/report_queue.py
└── stop():
    1. Set _running = False (stop accepting new work)
    2. Wait for in-flight upload to complete (with timeout)
    3. Persist current queue state
    4. Cancel background task

File: src/pywats_client/app.py (or main entry point)
└── shutdown_sequence():
    1. Stop file watchers (ConverterManager)
    2. Stop accepting new queue items
    3. Drain/checkpoint ReportQueueService
    4. Disconnect ConnectionService
    5. Release locks
```

**Effort:** 1-2 days
**Files:** 2

#### 2.2 Converter Plugin Safety ⚠️ PARTIAL

**Current state (`converters/base.py`):**
- Good abstraction (`ConverterBase`, `ConverterResult`)
- No API versioning
- No timeouts on conversion
- Exceptions caught but not isolated

**Implementation plan:**

```
Phase 1: Exception boundaries & versioning
├── File: src/pywats_client/converters/base.py
│   └── Add: CONVERTER_API_VERSION = 1
│   └── Add: api_version property to ConverterBase
│   └── Version check on load
│
├── File: src/pywats_client/services/converter_manager.py
│   └── Wrap convert() in try/except
│   └── Never propagate converter exceptions
│   └── Add conversion timeout (asyncio.wait_for)
│   └── Clear failure reporting to queue
│
Phase 2 (Future): Process isolation
└── Run converters in subprocess for full isolation
    └── Serialize input/output via JSON
    └── Process-level timeout via signal
```

**Effort:** 2 days (Phase 1)
**Files:** 2

### Priority 3: Nice to Have

#### 3.1 Observability / Health Snapshot ⚠️ NOT IMPLEMENTED

**Current state:**
- Logging only
- RateLimiter has stats, but not exposed
- No health endpoint or status file

**Implementation plan:**

```
Create: src/pywats_client/core/metrics.py
├── ClientMetrics class:
│   └── uploads_success: int
│   └── uploads_failed: int
│   └── uploads_retried: int
│   └── queue_depth: int
│   └── offline_duration_seconds: float
│   └── last_successful_upload: datetime
│   └── conversion_count: int
│   └── conversion_errors: int
│
├── to_dict() → dict (for JSON export)
├── Singleton or passed to services

File: src/pywats_client/app.py
├── CLI command: status --json
└── Or: periodic write to status.json file

Integration points:
├── ReportQueueService: update metrics on upload
├── ConnectionService: track offline duration
└── ConverterManager: track conversion stats
```

**Effort:** 2-3 days
**Files:** 3-4

#### 3.2 Pagination Helpers ⚠️ PARTIAL

**Current state:**
- Some domains have pagination support
- No standardized iterator pattern

**Implementation plan:**

```
Create: src/pywats/core/pagination.py
├── PagedIterator[T] class:
│   └── __iter__() yields items across pages
│   └── Configurable page_size
│   └── Lazy loading
│
├── PaginatedResponse[T] model:
│   └── items: List[T]
│   └── total: int
│   └── page: int
│   └── page_size: int
│   └── has_more: bool

Usage in repositories:
└── def get_all_products(page_size=100) -> PagedIterator[Product]
```

**Effort:** 2 days
**Files:** 1 + integration in repositories

---

## Implementation Roadmap

### Sprint 1: Critical Safety (Week 1-2)

| Task | Priority | Effort | Status |
|------|----------|--------|--------|
| 1.1 Idempotency keys | P1 | 2-3d | 🔴 Not started |
| 1.2 Atomic file writes | P1 | 2d | 🔴 Not started |
| 1.3 Error-aware retry | P1 | 2-3d | 🔴 Not started |
| 2.1 Graceful shutdown | P2 | 1-2d | 🔴 Not started |

**Deliverable:** Safe retry behavior, no data loss on crash

### Sprint 2: Stability & Isolation (Week 3)

| Task | Priority | Effort | Status |
|------|----------|--------|--------|
| 2.2 Converter safety | P2 | 2d | 🔴 Not started |
| 1.3 Circuit breaker | P1 | 2d | 🔴 Not started |

**Deliverable:** Robust converter handling, server protection

### Sprint 3: Observability (Week 4)

| Task | Priority | Effort | Status |
|------|----------|--------|--------|
| 3.1 Metrics & health | P3 | 2-3d | 🔴 Not started |
| 3.2 Pagination helpers | P3 | 2d | 🔴 Not started |

**Deliverable:** Production monitoring, cleaner API

---

## Files to Create

| File | Purpose |
|------|---------|
| `src/pywats_client/core/retry_policy.py` | Retry logic with backoff |
| `src/pywats_client/core/circuit_breaker.py` | Circuit breaker pattern |
| `src/pywats_client/core/metrics.py` | Observability metrics |
| `src/pywats/core/pagination.py` | Pagination helpers |

## Files to Modify

| File | Changes |
|------|---------|
| `src/pywats/core/client.py` | Add Idempotency-Key header support |
| `src/pywats/domains/report/repository.py` | Send idempotency key on submit |
| `src/pywats_client/services/report_queue.py` | Atomic writes, retry policy, graceful shutdown |
| `src/pywats_client/services/converter_manager.py` | Timeout, exception isolation |
| `src/pywats_client/converters/base.py` | API versioning |
| `src/pywats_client/app.py` | Shutdown sequence, status command |

---

## Summary

The architecture review correctly identified risks, but **overestimated the gaps**:

| Category | Review Assessment | Actual Status |
|----------|-------------------|---------------|
| Exception taxonomy | Missing | ✅ Complete |
| Error handling | Missing | ✅ Complete (ErrorHandler) |
| Rate limiting | Unclear scope | ✅ Complete (per-instance) |
| Service boundaries | Risky | ✅ Complete (repository-only) |
| Authentication | Unclear | ✅ Complete (client layer) |
| Online/offline | Multiple sources | ✅ Complete (ConnectionService) |
| Idempotency | Missing | 🔴 Needs implementation |
| Queue persistence | Missing | 🟡 Partial (needs atomic writes) |
| Retry policy | Missing | 🟡 Partial (needs error awareness) |
| Graceful shutdown | Missing | 🟡 Partial (needs sequence) |
| Converter safety | Missing | 🟡 Partial (needs timeout/isolation) |
| Observability | Missing | 🔴 Needs implementation |

**Bottom line:** The core API library is production-ready. The client application needs ~2-3 weeks of hardening work focused on **retry safety**, **crash recovery**, and **observability**.

---

*Document created: January 12, 2026*
*Based on: pyWATS Architecture Review (3rd party)*
