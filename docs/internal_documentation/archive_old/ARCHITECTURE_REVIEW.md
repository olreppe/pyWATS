
# Architecture Review – pyWATS Client & API

This document summarizes a focused architecture review of the pyWATS client and API prior to public release.
It highlights **improvements**, **responsibility boundary clarifications**, and **crucial missing pieces**
for a robust, production-ready CRUD + business-logic client.

---

## Executive Summary

The architecture is fundamentally sound and follows good separation of concerns:

- Clean layering (API library → client services → optional GUI)
- Clear domain boundaries
- Explicit offline/online handling

However, the main risks before release are **operational and correctness-related**, not structural:
idempotency, retries, persistence guarantees, observability, and plugin isolation.

---

## 1. Responsibility Boundaries to Tighten

### 1.1 HttpClient vs Repository vs Service

**Current**
- `HttpClient` returns raw responses
- Error handling delegated to repositories/services

**Risks**
- Error handling logic can drift or be forgotten
- Services may accidentally see transport details

**Recommended**
- Repositories are the *only* layer allowed to interact with `HttpClient`
- Services should only receive parsed models or domain exceptions
- Centralize `ErrorHandler.handle_response()` in a shared repository base

**Optional refinement**
- Add `request_json()` helper on `HttpClient` that:
  - Executes request
  - Validates status
  - Returns parsed JSON or raises `PyWATSError`

---

### 1.2 Authentication & Persistence Boundaries

**Rule to enforce**
- `pywats` API library must remain **stateless**
- It should accept only:
  - `base_url`
  - `auth token`
  - transport configuration

**Keep in client layer**
- Password-to-token exchange
- Encrypted credential storage
- Token refresh / persistence

This avoids tight coupling and keeps the API reusable.

---

### 1.3 GUI Isolation

- GUI must interact only with **facade-level services**
- No direct access to internal state of queues, converters, or connection internals
- Prefer **events/signals** over state polling

This prevents UI-driven coupling that becomes hard to refactor later.

---

## 2. Crucial Missing Pieces (Release-Critical)

### 2.1 Idempotency & De-duplication (Very Important)

**Problem**
- Offline queue retries can cause duplicate server-side operations
- Especially dangerous if a request succeeds but the client crashes before marking it complete

**Required**
- Client-generated idempotency key (UUID) per submission
- Persist idempotency key with queued payload
- Send as:
  - `Idempotency-Key` header (preferred), or
  - explicit `client_submission_id` field

This is critical for safe retries.

---

### 2.2 Queue Persistence Robustness

Folder-based JSON queues are acceptable initially, but must guarantee:

- Atomic writes (temp file → fsync → rename)
- Crash-safe state transitions (`pending → in-flight → completed/failed`)
- Corruption handling (partial or invalid JSON)
- Safe behavior under concurrent access

**Future-proof option**
- SQLite-based queue (solves atomicity, concurrency, indexing, recovery)

---

### 2.3 Retry Policy by Error Type

Retries should not be uniform.

**Add**
- Exponential backoff + jitter for network errors / 5xx
- No retries for validation errors (4xx → failed)
- Special handling for:
  - 401/403 → re-authenticate or invalidate connection
- Circuit breaker behavior to avoid hammering a down server

---

### 2.4 Graceful Shutdown Semantics

Define explicit shutdown behavior:

1. Stop file watchers
2. Stop producing new queue items
3. Finish or checkpoint in-flight uploads
4. Persist state
5. Release locks and resources

Ensure crashes do not lose or duplicate work.

---

### 2.5 Observability (Missing Today)

Logging alone is insufficient for unattended clients.

**Add**
- Counters:
  - uploads_success
  - uploads_failed
  - retries
  - queue_depth
  - offline_duration
- Timings:
  - upload_latency
  - conversion_duration
- Health snapshot:
  - CLI `status --json`
  - or periodic status file

This dramatically reduces support and debugging time.

---

## 3. Dependency & Coupling Concerns

### 3.1 Rate Limiting Scope

Clarify:
- Is the rate limit per instance?
- Per process?
- Per machine?

Multiple client instances can easily exceed server limits.

**Suggestion**
- Keep in-process limiter
- Document reduced per-instance limits for multi-instance setups
- Consider shared limiter later if needed

---

### 3.2 Online/Offline State Authority

Ensure **one single source of truth**:

- `ConnectionService` owns connectivity state
- Other services subscribe to state changes
- No duplicated “ping” or connectivity logic

---

### 3.3 Converter Plugin Safety

Dynamic plugin loading is powerful but dangerous.

**Minimum safeguards**
- Versioned converter API (`api_version = 1`)
- Strict exception boundaries (converter errors never crash client)
- Timeouts or watchdogs
- Clear failure reporting

**Future option**
- Run converters in a subprocess for isolation

---

## 4. CRUD + Business Logic Gaps in API Library

### 4.1 Pagination & Large Payloads

Add standard helpers for:
- Pagination iteration
- Page size defaults and limits
- Avoiding full in-memory loads for large responses

---

### 4.2 Stable Error Taxonomy

Public API should expose:
- Small, stable set of exception types
- Attached metadata:
  - HTTP status
  - operation name
  - server message
  - correlation ID (if available)
- Clear strict vs lenient behavior

---

### 4.3 Timeout & Transport Policy

Define explicitly:
- Connect timeout vs read timeout
- Retryable vs non-retryable failures
- Where retry logic lives (transport vs service)

Consistency matters more than the exact values.

---

## 5. High-ROI Changes Before Release

**Strongly recommended**
1. Idempotency keys for submissions
2. Backoff + jitter retry strategy
3. Crash-safe queue persistence
4. Single online/offline authority
5. Health + metrics snapshot
6. Converter isolation and failure containment

---

## Final Assessment

The architecture is well-designed and extensible.
No fundamental rewrite is needed.

The remaining work is about **correctness under failure**, **long-running stability**, and **operational clarity**.
Addressing the items above will significantly reduce production risk and support burden.

---

*Prepared for team review and release readiness discussion.*
