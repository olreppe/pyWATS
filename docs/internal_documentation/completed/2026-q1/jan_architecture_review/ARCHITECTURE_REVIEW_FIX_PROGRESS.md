# Architecture Review - Implementation Progress

**Created:** January 29, 2026  
**Based on:** [ARCHITECTURE_REVIEW.md](./ARCHITECTURE_REVIEW.md)  
**Final Grade Target:** A+ (95+/100)  
**Current Grade:** A- (88/100)

**🔴 IMPORTANT: NO BACKWARDS COMPATIBILITY POLICY**
> We are in BETA - NO backward compatibility code is needed!
> - No deprecated wrappers
> - No legacy aliases
> - No backward compatibility layers
> - Just clean, modern code

---

## Overview

This document tracks the implementation of fixes for architectural issues identified in the comprehensive architecture review. Issues are organized into logical stages that group related functionality and minimize disruption.

**Total Estimated Effort:** ~11 weeks (424 hours) for 1 developer  
**Parallel Work Possible:** Yes - Stages 1-3 have minimal dependencies

**Key Decisions:**
- IPC security: Pragmatic approach for trusted environment (no encryption needed)
- File safety: Apply to ALL client/GUI file operations, not just config
- Converter versioning: Not needed - unified API only
- Sync/Async: Keep wrapper approach, consider minor improvements only
- Station abstraction: Deferred - not in scope
- Code quality: Manual review task at end with user control

---

## Implementation Stages

### Stage 1: Security Hardening 🔴 CRITICAL
**Priority:** CRITICAL  
**Estimated Effort:** 5 weeks (200 hours)  
**Dependencies:** None - can start immediately  
**Status:** ✅ Complete

#### 1.1 IPC Authentication & Rate Limiting
**Effort:** 1 week (40 hours)  
**Severity:** MEDIUM  
**Status:** ✅ Complete

**Context:**
- pyWATS typically runs on secure stations behind machine authentication
- Environment and users generally "friendly" (not internet-facing)
- Pragmatic security approach: prevent accidents and basic abuse, not military-grade

**Current Issues:**
- ~~No authentication - any local process can connect~~ ✅ FIXED
- ~~No rate limiting - vulnerable to accidental DoS~~ ✅ FIXED

**Implementation Plan:**

1. **Design Simple Authentication** (2 hours) ✅ DONE
   - [x] Shared secret approach (256-bit hex token)
   - [x] Simple validation on connect
   - [x] Focus on preventing accidents, not sophisticated attacks

2. **Implement Shared Secret** (6 hours) ✅ DONE
   - [x] Generate secret on service start (via `secrets.token_hex(32)`)
   - [x] Store in user-specific location
     - Linux/macOS: `~/.config/pywats/secrets/<instance_id>.key` (0600 permissions)
     - Windows: `AppData\Local\pyWATS\secrets\<instance_id>.key`
   - [x] Load secret in IPC client
   - [x] Timing-safe validation via `secrets.compare_digest()`

3. **Update IPC Protocol** (8 hours) ✅ DONE
   - [x] Add `auth` command to AsyncIPCServer
   - [x] Simple token validation via `_handle_auth()` method
   - [x] Reject unauthenticated requests (when secret configured)
   - [x] Update AsyncIPCClient with `_authenticate()` method
   - [x] `ping` shows auth status, always allowed

4. **Rate Limiting** (8 hours) ✅ DONE
   - [x] Simple token bucket algorithm (`RateLimiter` class)
   - [x] Per-client rate limiting in AsyncIPCServer
   - [x] Reasonable limits (default: 100 req/min, burst: 20)
   - [x] Return error on rate limit exceeded

5. **Testing** (12 hours) ✅ DONE
   - [x] Unit tests for secret management (16 tests, all passing)
   - [x] Test rate limiting (5 tests, all passing)
   - [x] Integration tests for IPC auth flow (12 tests, all passing)

6. **Documentation** (4 hours) ✅ DONE
   - [x] Update architecture docs (docs/guides/ipc-security.md)
   - [x] Document security model (pragmatic approach)

**Files Created:**
- `src/pywats_client/core/security.py` ✅ (260 lines)
- `tests/client/test_security.py` ✅ (260 lines, 16 tests passing)
- `tests/client/test_ipc_auth.py` ✅ (330 lines, 12 tests passing)
- `docs/guides/ipc-security.md` ✅ (IPC security guide)

**Files Modified:**
- `src/pywats_client/service/async_ipc_server.py` ✅ (444 lines, auth + rate limiting)
- `src/pywats_client/service/async_ipc_client.py` ✅ (auth foundation added)

**Test Results (Latest - 2026-01-29):**
- Full suite: **672 passed**, 14 skipped, **0 failed** ✅
- Security tests: 16 passed
- IPC auth tests: 12 passed
- Pre-existing test bugs fixed: 7 tests in test_ipc.py and test_async_client_service.py

**Note:** No encryption needed - trusted environment, local-only communication.

---

#### 1.2 Converter Sandboxing
**Effort:** 2-3 weeks (80-120 hours)  
**Severity:** CRITICAL  
**Status:** ✅ Complete (Pending Docs)

**Current Issues:**
- ~~Converters run with full service privileges~~ ✅ FIXED (process isolation)
- ~~No isolation - can access/modify service internals~~ ✅ FIXED (sandbox process)
- ~~No resource limits - can consume unlimited CPU/memory~~ ✅ FIXED (ResourceLimits)
- ~~Arbitrary code execution risk~~ ✅ FIXED (import blocking + static analysis)

**Implementation Plan:**

1. **Design Sandbox Architecture** (8 hours) ✅ DONE
   - [x] Choose isolation method: subprocess (stronger isolation than multiprocessing)
   - [x] Define restricted permissions model (SandboxCapability enum)
   - [x] Design converter IPC protocol (JSON messages via pipes)
   - [x] Document security boundaries

2. **Implement Process Isolation** (24 hours) ✅ DONE
   - [x] Create `SandboxProcess` class (separate process management)
   - [x] Implement converter loading in isolated process (`sandbox_runner.py`)
   - [x] Set up IPC channel (stdin/stdout pipes with JSON)
   - [x] Add process lifecycle management (start/stop/kill)
   - [x] Handle process crashes gracefully

3. **Permission Restrictions** (16 hours) ✅ DONE
   - [x] Define allowed operations (`SandboxCapability` enum)
   - [x] Implement filesystem access restrictions (`SafeFileHandler`)
   - [x] Block network access (blocked imports: socket)
   - [x] Restrict environment variables (`_create_restricted_env`)
   - [x] Add capability-based security (`SandboxConfig`)

4. **Resource Limits** (12 hours) ✅ DONE
   - [x] CPU time limits (Unix: RLIMIT_CPU, Windows: planned)
   - [x] Memory limits (Unix: RLIMIT_AS, configurable default 512MB)
   - [x] Execution timeout (configurable, default 5 minutes)
   - [x] Implement resource monitoring (via `ResourceLimits` class)
   - [x] Kill on limit exceeded (`_kill_process`)

5. **Converter Validation** (16 hours) ✅ DONE
   - [x] Static analysis before loading (AST inspection)
   - [x] Whitelist allowed imports (`allowed_imports` config)
   - [x] Detect dangerous patterns (eval, exec, __import__, subprocess, etc.)
   - [ ] Add converter signature verification (future)
   - [x] Create validation report (`ConverterValidator` class)

6. **Update Converter API** (16 hours) ✅ DONE
   - [x] Add `source_path` property to ConverterBase/FileConverter
   - [x] Add `trusted_mode` property for sandbox bypass
   - [x] Export sandbox classes from converters package
   - [x] AsyncConverterPool sandbox integration (enable_sandbox param)
   - [x] Add _ensure_sandbox(), _should_use_sandbox() methods

7. **Testing** (20 hours) ✅ DONE
   - [x] Unit tests for sandbox enforcement (34 tests)
   - [x] Integration tests (25 tests)
   - [x] Test resource limits configuration
   - [x] Test permission restrictions
   - [x] Test malicious converter scenarios
   - [x] Test AsyncConverterPool integration

8. **Documentation** (6 hours) ✅ DONE
   - [x] Update converter development guide (docs/guides/converter-security.md)
   - [x] Document security model
   - [x] Document sandbox API

**Files Created:**
- `src/pywats_client/converters/sandbox.py` ✅ (870+ lines)
  - `SandboxCapability` enum - capability-based permissions
  - `ResourceLimits` dataclass - CPU, memory, time limits
  - `SandboxConfig` dataclass - full sandbox configuration
  - `SandboxMessage` - IPC protocol messages
  - `SandboxProcess` - subprocess management
  - `ConverterValidator` - static code analysis
  - `ConverterSandbox` - high-level interface
- `src/pywats_client/converters/sandbox_runner.py` ✅ (310+ lines)
  - Runs inside isolated subprocess
  - `SafeFileHandler` - restricted file access
  - `RestrictedImporter` - import blocking
  - `SandboxRunner` - main execution loop
- `tests/client/test_sandbox_integration.py` ✅ (580+ lines, 25 tests)
- `docs/guides/converter-security.md` ✅ (Converter security guide)

**Test Files:**
- `tests/client/test_sandbox.py` ✅ (530+ lines, 34 tests, 33 pass, 1 Unix-only skip)
- `tests/client/test_sandbox_integration.py` ✅ (580+ lines, 25 tests, all pass)

**Files Modified:**
- `src/pywats_client/converters/__init__.py` ✅ (added sandbox exports)
- `src/pywats_client/converters/base.py` ✅ (added source_path, trusted_mode)
- `src/pywats_client/converters/file_converter.py` ✅ (added source_path, trusted_mode)
- `src/pywats_client/service/async_converter_pool.py` ✅ (sandbox integration)

**Test Results (Latest - 2026-01-29):**
- Full suite: **730 passed**, 15 skipped, **0 failed** ✅
- Sandbox tests: 34 passed, 1 skipped (Unix resource limits)
- Sandbox integration tests: 25 passed

**Files Modified:**
- `src/pywats_client/service/async_converter_pool.py` ✅ 
  - Added sandbox integration (`_ensure_sandbox`, `_convert_sandboxed`)
  - Added `enable_sandbox` parameter (default: True)
  - Added `_should_use_sandbox` for per-converter opt-out
  - Updated stats to track sandbox errors
  - Proper sandbox shutdown in `stop()`

---

#### 1.3 Safe File Handling (Config & All Client/GUI Files)
**Effort:** 1.5 weeks (60 hours)  
**Severity:** HIGH  
**Status:** ✅ Complete

**Current Issues:**
- ~~Service and GUI can modify config.json concurrently~~ ✅ FIXED (file locking)
- ~~No locking mechanism - race conditions possible~~ ✅ FIXED (locked_file context manager)
- ~~No atomic writes - corruption on crash/interrupt~~ ✅ FIXED (SafeFileWriter)
- ~~No validation or auto-repair~~ ✅ FIXED (validate() and repair() methods)
- **Affects all file operations in client/GUI, not just config**

**Implementation Plan:**

1. **Implement File Locking Utility** (12 hours) ✅ DONE (pre-existing)
   - [x] Cross-platform locking (fcntl on Unix, msvcrt on Windows)
   - [x] Create `locked_file` context manager
   - [x] Add timeout on lock acquisition
   - [x] Handle lock failures gracefully
   - [x] Generic - works for any file

2. **Atomic Write Utility** (12 hours) ✅ DONE (pre-existing)
   - [x] Implement write-to-temp-then-rename pattern
   - [x] Create `SafeFileWriter` with atomic write methods
   - [x] Ensure proper error handling
   - [x] Add backup file support (.bak files)
   - [x] Generic - works for any file

3. **Apply to Config Management** (12 hours) ✅ DONE
   - [x] Update ConfigManager to use SafeFileWriter/SafeFileReader (bug fix)
   - [x] Use atomic_write() for config saves in ClientConfig
   - [x] Use SafeFileReader for config loads with backup recovery
   - [x] Track config source path (_config_path)

4. **Apply to Other File Operations** (12 hours) ✅ DONE (pre-existing)
   - [x] Audit all file writes in client - PersistentQueue already uses file_utils
   - [x] File locking applied to queue persistence
   - [x] Safe reads/writes throughout

5. **Config Validation** (8 hours) ✅ DONE
   - [x] Add validate() method to ClientConfig
   - [x] Add is_valid() convenience method
   - [x] Add repair() method for auto-fixing common issues
   - [x] Add load_and_repair() for robust loading
   - [x] Validate ConverterConfig nested objects

6. **Testing** (12 hours) ✅ DONE
   - [x] Unit tests for locking mechanism (34 tests in test_file_utils.py)
   - [x] Test concurrent access scenarios
   - [x] Test atomic writes
   - [x] Test backup recovery
   - [x] Validation/repair tests (19 tests in test_config.py)

7. **Documentation** (4 hours) ✅ DONE
   - [x] Document safe file handling pattern
   - [x] Create docs/guides/safe-file-handling.md

**Files Created:**
- `tests/client/test_file_utils.py` ✅ (580+ lines, 36 tests, 34 pass, 2 Windows-skipped)
- `docs/guides/safe-file-handling.md` ✅ (comprehensive guide)

**Files Modified:**
- `src/pywats_client/core/config_manager.py` ✅ (fixed SafeFileWriter/SafeFileReader usage)
- `src/pywats_client/core/config.py` ✅ (added validate, is_valid, repair, load_and_repair)
- `tests/client/test_config.py` ✅ (19 new validation tests, 37 total)

**Pre-existing Files (already implemented correctly):**
- `src/pywats_client/core/file_utils.py` - SafeFileWriter, SafeFileReader, locked_file
- `src/pywats_client/core/persistent_queue.py` - already uses file_utils

**Test Results (Latest - 2026-01-29):**
- Full suite: **764 passed**, 17 skipped, **0 failed** ✅
- file_utils tests: 34 passed, 2 skipped (Windows locking behavior)
- config tests: 37 passed (including 19 new validation tests)

---

### Stage 2: Protocol & Versioning 🟡 HIGH
**Priority:** HIGH  
**Estimated Effort:** 1 week (40 hours)  
**Dependencies:** Can start in parallel with Stage 1  
**Status:** ✅ Complete

**Note:** Version fields added for *future* compatibility only. No backward compatibility layers.

#### 2.1 IPC Protocol Versioning
**Effort:** 3 days (24 hours)  
**Severity:** MEDIUM  
**Status:** ✅ Complete

**Current Issues:**
- ~~No version in protocol - hard to track compatibility~~ ✅ FIXED

**Implementation Plan:**

1. **Add Protocol Version Field** (4 hours) ✅ DONE
   - [x] Add `protocol_version` to handshake ("2.0")
   - [x] Server sends hello message on connect with version, capabilities
   - [x] Client checks version compatibility
   - [x] Reject incompatible versions with clear error

2. **Version Mismatch Handling** (4 hours) ✅ DONE
   - [x] VersionMismatchError exception with clear message
   - [x] Log version in connection info
   - [x] Server logs client version, client logs server version

3. **Testing** (12 hours) ✅ DONE
   - [x] Test version checking (33 tests)
   - [x] Test error messages
   - [x] Integration tests

4. **Documentation** (4 hours) ✅ DONE
   - [x] Protocol module includes comprehensive docstrings
   - [x] Document current version (2.0)

**Files Created:**
- `src/pywats_client/service/ipc_protocol.py` ✅ (320+ lines)
  - PROTOCOL_VERSION = "2.0"
  - MessageType enum
  - IPCMessage, IPCResponse dataclasses
  - HelloMessage, ConnectMessage
  - ServerCapability enum
  - VersionMismatchError exception
  - Version parsing and compatibility functions
- `tests/client/test_ipc_versioning.py` ✅ (350+ lines, 33 tests)

**Files Modified:**
- `src/pywats_client/service/async_ipc_server.py` ✅
  - Sends hello message on client connect
  - Checks client protocol version
  - Includes protocol_version in all responses
  - Lists server capabilities
- `src/pywats_client/service/async_ipc_client.py` ✅
  - Receives and validates hello message
  - Raises VersionMismatchError for incompatible servers
  - Includes protocol_version in all requests
  - Exposes server_version and server_capabilities properties
- `tests/client/test_ipc_auth.py` ✅ (fixed for new hello flow)

**Test Results (Latest - 2026-01-29):**
- IPC versioning tests: 33 passed
- IPC auth tests: 12 passed

---

#### 2.2 Config Schema Versioning
**Effort:** 2 days (16 hours)  
**Severity:** LOW  
**Status:** ✅ Complete

**Current Issues:**
- ~~No schema version in config.json~~ ✅ FIXED
- ~~Hard to track config format changes~~ ✅ FIXED

**Implementation Plan:**

1. **Add Schema Version** (4 hours) ✅ DONE
   - [x] Add `schema_version` field to ClientConfig (default "2.0")
   - [x] Add CURRENT_SCHEMA_VERSION and MIN_SCHEMA_VERSION constants
   - [x] Update serialization to include schema_version
   - [x] Auto-upgrade old configs via repair()

2. **Version Validation** (4 hours) ✅ DONE
   - [x] Validate schema version on load
   - [x] _is_schema_version_compatible() helper
   - [x] Clear error for unsupported versions

3. **Testing** (4 hours) ✅ DONE
   - [x] Test version validation (12 tests)
   - [x] Test error messages
   - [x] Integration tests

4. **Documentation** (4 hours) ✅ DONE
   - [x] Docstrings in ClientConfig
   - [x] Schema version documented in class

**Files Modified:**
- `src/pywats_client/core/config.py` ✅
  - Added schema_version field (default "2.0")
  - Added CURRENT_SCHEMA_VERSION = "2.0", MIN_SCHEMA_VERSION = "1.0"
  - Added _parse_version(), _is_schema_version_compatible() helpers
  - validate() checks schema version
  - repair() upgrades old schema versions
  - to_dict() includes schema_version
- `tests/client/test_config.py` ✅ (12 new tests)

**Test Results (Latest - 2026-01-29):**
- Config tests: 49 passed (37 existing + 12 new schema tests)

---

**Stage 2 Summary:**
- Total new tests: 45 (33 IPC versioning + 12 config schema)
- Full test suite: **828 passed**, 17 skipped, **0 failed** ✅

---

### Stage 3 (Minimal): Queue Configuration 🟢 OPTIONAL
**Priority:** LOW  
**Estimated Effort:** 2 hours (minimal scope, evaluated as overkill)  
**Dependencies:** None - independent improvements  
**Status:** ✅ Complete

**Evaluation Result:** Most Stage 3 features already exist in the codebase:
- ✅ Health Server (397 lines, full K8s probes)
- ✅ Event Metrics (208 lines, EventMetrics class)
- ✅ Distributed Tracing (335 lines, EventTracer with spans)
- ✅ Queue Statistics (async_pending_queue.py, stats property)
- ✅ Logging Framework (pywats/core/logging.py, get_logger pattern)

**Implemented (Minimal Version):**

1. **Queue Size Configuration** (2 hours) ✅ DONE
   - [x] Added `max_queue_size` to ClientConfig (default: 10,000, 0 = unlimited)
   - [x] Added `max_concurrent_uploads` to ClientConfig (default: 5)
   - [x] Added `max_queue_size` parameter to AsyncPendingQueue constructor
   - [x] Added `queue_size` property (counts .queued files)
   - [x] Added `is_queue_full` property (checks if at limit)
   - [x] Added `can_accept_report()` method (returns bool + reason)
   - [x] Wired config values to service initialization
   - [x] Added to_dict() export
   - [x] Created 16 new tests (10 queue size tests + 6 config tests)

**Files Created:**
- No new files

**Files Modified:**
- `src/pywats_client/core/config.py` ✅
  - Added `max_queue_size: int = 10000`
  - Added `max_concurrent_uploads: int = 5`
  - Updated `to_dict()` to include queue settings
- `src/pywats_client/service/async_pending_queue.py` ✅
  - Added `DEFAULT_MAX_QUEUE_SIZE` constant
  - Added `max_queue_size` parameter to `__init__`
  - Added `queue_size` property
  - Added `is_queue_full` property
  - Added `can_accept_report()` method
  - Updated stats to include `max_queue_size`
  - Updated initialization logging to show queue limits
- `src/pywats_client/service/async_client_service.py` ✅
  - Wired config values to AsyncPendingQueue creation
- `tests/client/test_async_pending_queue.py` ✅ (10 new tests in TestQueueSizeLimits)
- `tests/client/test_config.py` ✅ (6 new tests in TestQueueConfigFields)

**Test Results (Latest - 2026-01-29):**
- Queue size tests: 10 passed
- Config queue field tests: 6 passed
- Full test suite: **844 passed**, 17 skipped, **0 failed** ✅
- Total new tests: 16

**What Was Not Done (Intentionally):**
- ❌ Priority queue system - no use case identified
- ❌ Prometheus metrics - EventMetrics already exists
- ❌ OpenTelemetry - EventTracer already exists
- ❌ SQLite optimization - file-based queue, not SQLite
- ❌ Structured JSON logging - standard logging sufficient for BETA

**Summary:**
Minimal Stage 3 implementation adds queue capacity management without bloat. The config fields allow operators to tune concurrency and queue limits. All existing infrastructure (health checks, metrics, tracing) already exists in the codebase.

---

### Stage 4: API Improvements 🔵 LOW
**Priority:** LOW  
**Estimated Effort:** 2 weeks (80 hours)  
**Dependencies:** None  
**Status:** 🔲 Not Started

**Note:** Code quality review task deferred - will be done at end with user control.

#### 4.1 Sync Wrapper Enhancements
**Effort:** 1 week (40 hours)  
**Severity:** LOW  
**Status:** 🔲 Not Started

**Current Issues:**
- No queue size limits - unbounded growth
- No priority system
- SQLite locking under high concurrency

**Implementation Plan:**

1. **Queue Size Limits** (8 hours)
   - [ ] Add `max_queue_size` config option (default: 10,000)
   - [ ] Implement size checking
   - [ ] Add eviction policy (FIFO/priority-based)
   - [ ] Emit warnings near limit

2. **Priority System** (12 hours)
   - [ ] Add priority field to queue items
   - [ ] Implement priority queue in AsyncPendingQueue
   - [ ] Update persistence layer
   - [ ] Add priority-based scheduling

3. **SQLite Optimization** (12 hours)
   - [ ] Enable WAL mode (Write-Ahead Logging)
   - [ ] Add connection pooling
   - [ ] Batch writes where possible
   - [ ] Add retry with exponential backoff

4. **Queue Monitoring** (8 hours)
   - [ ] Add queue metrics (size, age, throughput)
   - [ ] Expose via IPC
   - [ ] Add queue health checks
   - [ ] Create queue statistics endpoint

5. **Testing** (8 hours)
   - [ ] Test size limits
   - [ ] Test priority ordering
   - [ ] Test high concurrency scenarios
   - [ ] Performance benchmarks

6. **Documentation** (4 hours)
   - [ ] Update queue documentation
   - [ ] Document configuration options
   - [ ] Add troubleshooting guide

**Files to Modify:**
- `src/pywats_client/service/async_pending_queue.py`
- `src/pywats_client/core/persistent_queue.py`
- `src/pywats_client/core/config.py` (add queue config)
- `tests/client/test_async_pending_queue.py`
- `docs/guides/queue-management.md`

---

#### 3.2 Monitoring & Telemetry
**Effort:** 2 weeks (80 hours)  
**Severity:** MEDIUM  
**Status:** 🔲 Not Started

**Current Issues:**
- No metrics collection
- No health checks
- Hard to diagnose issues

**Implementation Plan:**

1. **Metrics Collection** (16 hours)
   - [ ] Choose metrics library (Prometheus client?)
   - [ ] Define key metrics:
     - API call latency
     - Queue depth/age
     - Converter execution time
     - Error rates
   - [ ] Implement metrics collectors
   - [ ] Add metrics endpoint

2. **Health Checks** (12 hours)
   - [ ] Create `HealthChecker` class
   - [ ] Check API connectivity
   - [ ] Check database health
   - [ ] Check queue status
   - [ ] Aggregate health status

3. **Structured Logging** (16 hours)
   - [ ] Add structured logging (JSON format)
   - [ ] Include context (request_id, user, etc.)
   - [ ] Add log levels properly
   - [ ] Implement log rotation

4. **Tracing** (16 hours)
   - [ ] Add distributed tracing (OpenTelemetry?)
   - [ ] Trace API calls end-to-end
   - [ ] Trace converter execution
   - [ ] Add correlation IDs

5. **Monitoring Dashboard** (12 hours)
   - [ ] Add metrics page in GUI
   - [ ] Display key health indicators
   - [ ] Show historical trends
   - [ ] Add alerting (optional)

6. **Testing** (8 hours)
   - [ ] Test metrics collection
   - [ ] Test health checks
   - [ ] Verify tracing works
   - [ ] Integration tests

7. **Documentation** (8 hours)
   - [ ] Document metrics available
   - [ ] Health check endpoints
   - [ ] Monitoring best practices

**Files to Modify:**
- `src/pywats_client/core/metrics.py` (new)
- `src/pywats_client/core/health.py` (new)
- `src/pywats_client/service/async_client_service.py`
- `src/pywats_client/gui/pages/monitoring_page.py` (new)
- `tests/client/test_metrics.py` (new)
- `docs/guides/monitoring.md` (new)

---

### Stage 4: Architectural Improvements 🟢 LOW-MEDIUM
**Priority:** LOW-MEDIUM  
**Estimated Effort:** 1 week (40 hours)  
**Dependencies:** Should be done after Stages 1-3  
**Status:** 🔲 Not Started

#### 4.1 Sync/Async Wrapper Improvements (OPTIONAL)
**Effort:** 3 days (24 hours)  
**Severity:** LOW  
**Status:** 🔲 Not Started

**Context:**
- Current sync/async wrapper approach was **intentionally chosen** to support both modes with no duplication
- **KEEP the wrapper approach** - it works well
- Performance users can use fully async mode
- Focus on reducing overhead/complexity without dropping wrappers

**Potential Improvements:**

1. **Optimize Event Loop Management** (8 hours)
   - [ ] Profile current overhead
   - [ ] Reduce event loop creation overhead
   - [ ] Improve thread-local storage efficiency
   - [ ] Add caching where safe

2. **Better Error Messages** (4 hours)
   - [ ] Clearer errors when mixing sync/async contexts
   - [ ] Better stack traces through wrapper layers
   - [ ] Add context to exceptions

3. **Documentation Improvements** (8 hours)
   - [ ] Clarify when to use sync vs async
   - [ ] Document performance implications
   - [ ] Add best practices guide
   - [ ] Update all examples

4. **Testing** (4 hours)
   - [ ] Performance benchmarks
   - [ ] Verify improvements

**Files to Modify:**
- `src/pywats/core/sync_runner.py`
- `src/pywats/pywats.py`
- `docs/guides/sync-vs-async.md` (new)
- `examples/` (update)

**Decision:** Only implement if significant improvement possible. Otherwise, SKIP this task.

---

#### 4.2 Code Quality & TODO Cleanup
**Effort:** 1 week (40 hours)  
**Severity:** LOW  
**Status:** 🔲 Not Started

**Context:**
- ~20 TODO/FIXME markers in codebase
- User wants **full control** over each TODO - some may be old/not applicable
- This is a **manual review task at the end**

**Implementation Plan:**

1. **TODO Audit** (16 hours)
   - [ ] List all TODOs with context
   - [ ] Review each with user
   - [ ] Categorize: Fix, Convert to Issue, or Remove
   - [ ] Create issues for future work
   - [ ] Fix critical/easy ones

2. **Dead Code Cleanup** (8 hours)
   - [ ] Review unused pages
   - [ ] Clean up old imports
   - [ ] Remove confirmed dead code
   - [ ] Update comments

3. **Consistency Pass** (12 hours)
   - [ ] Standardize error handling
   - [ ] Consistent naming conventions
   - [ ] Docstring coverage
   - [ ] Type hints coverage

4. **Code Review** (4 hours)
   - [ ] Run linters (ruff, mypy)
   - [ ] Fix issues
   - [ ] Update pre-commit hooks

**Files to Modify:**
- Multiple files across codebase
- Focus on GUI widgets, converters, TODOs

**Note:** This is the **final task** - done at the end with user supervision.

---

## Progress Tracking

### Overall Progress
- **Stage 1 (Security):** ✅ Complete (3/3 subtasks)
  - 1.1 IPC Auth: ✅ Complete
  - 1.2 Converter Sandboxing: ✅ Complete
  - 1.3 Safe File Handling: ✅ Complete
- **Stage 2 (Versioning):** ✅ Complete (2/2 subtasks)
  - 2.1 IPC Protocol Versioning: ✅ Complete
  - 2.2 Config Schema Versioning: ✅ Complete
- **Stage 3 (Minimal Queue Config):** ✅ Complete (1/1 subtask)
  - 3.0 Queue Configuration: ✅ Complete (minimal scope)
- **Stage 4 (API Improvements):** 🔲 Not Started (0/2 subtasks)

**Total:** ✅ 6/9 subtasks complete (~67%)

### Recent Test Results (2026-01-29)
- **Full test suite:** 844 passed, 17 skipped, **0 failed** ✅
- **Queue size tests:** 10 passed (new)
- **Config queue field tests:** 6 passed (new)
- **IPC versioning tests:** 33 passed
- **Config schema tests:** 12 passed
- **Sandbox tests:** 33 passed, 1 skipped (Unix-only)
- **Security module tests:** 16 passed, 1 skipped (Unix permissions)
- **IPC auth tests:** 12 passed
- **File utils tests:** 34 passed

### Completion Status Legend
- 🔲 Not Started
- 🔄 In Progress
- ✅ Completed
- ⏸️ Blocked
- ⏭️ Skipped

---

## Testing Strategy

### Test Coverage Goals
- **Stage 1:** Security tests - 100% coverage for auth/sandbox
- **Stage 2:** Protocol tests - All version combinations
- **Stage 3:** Resource tests - Load testing, stress testing
- **Stage 4:** Regression tests - No breaking changes

### Integration Testing
- [ ] Create end-to-end test suite
- [ ] Test all components together
- [ ] Performance benchmarks
- [ ] Security penetration testing

---

## Release Strategy

### Version Bumps
**Current Version:** 0.1.0b38 (beta)

- **Stage 1 completion:** 0.1.0b38 → 0.2.0b1 (major security & sandboxing release)
- **Stage 2 completion:** Part of 0.2.0b1 (versioning added)
- **Stage 3 completion:** 0.2.0b1 → 0.2.1b1 (monitoring features)
- **Final Release:** 0.2.xbX → 1.0.0 (when ready to exit beta)

### Upgrade Guides (Forward-Only)
- [ ] 0.1.x → 0.2.0: Breaking changes doc
- [ ] Document all breaking changes clearly
- [ ] No backward compatibility code
- [ ] Clean installation recommended for major version bump

---

## Risk Management

### High-Risk Changes
1. **Converter Sandboxing** - WILL break existing converters
   - Mitigation: Clear documentation, update all examples
2. **IPC Protocol Changes** - WILL break GUI/Service communication
   - Mitigation: Version checking, clean error messages
3. **Sync/Async Decision** - May affect API users
   - Mitigation: Clear documentation, update all examples

### Rollback Plans
- [ ] Tag v1.4.x as "legacy" branch
- [ ] Users on v1.4.x stay there or upgrade to v2.0+
- [ ] No support for mixed versions

---

## Success Metrics

### Security
- [ ] No unauthenticated IPC access possible
- [ ] All converters run sandboxed
- [ ] Zero file corruption incidents
- [ ] Security audit passes

### Quality
- [ ] All TODOs resolved or tracked
- [ ] Test coverage >80%
- [ ] No critical bugs in production
- [ ] Documentation complete

### Performance
- [ ] No performance regression
- [ ] Queue handles 10k+ items
- [ ] IPC latency <10ms
- [ ] Converter overhead <5%

### Final Grade
- **Target:** A+ (95+/100)
- **Current:** A- (88/100)
- **Improvement:** +7 points

---

## Notes & Decisions

### Decision Log
- **2026-01-29:** Created implementation plan based on architecture review
- **2026-01-29:** Applied NO_BACKWARDS_COMPATIBILITY policy - removed ~160 hours of backward compat work
- **2026-01-29:** Started Stage 1.1 - Created security module with:
  - Secret generation/storage (256-bit, platform-specific paths)
  - Rate limiting (token bucket, 100 req/min default)
  - 16 unit tests (all passing)
  - Client authentication foundation
- **2026-01-29:** Completed Stage 1.1 - IPC Authentication fully implemented
  - Fixed 7 pre-existing test bugs in test_ipc.py and test_async_client_service.py
  - All 672 tests passing
- **2026-01-29:** Started Stage 1.2 - Converter Sandboxing:
  - Created `sandbox.py` (870+ lines) with full sandbox architecture
  - Created `sandbox_runner.py` (310+ lines) for isolated subprocess
  - Implemented: process isolation, resource limits, permission restrictions
  - Implemented: static code analysis (ConverterValidator)
  - Integrated with AsyncConverterPool (enable_sandbox parameter)
  - 33 new sandbox tests (all passing)
  - Full suite: 705 passed, 0 failed

### Open Questions
- ~~IPC encryption: TLS vs NaCl?~~ **RESOLVED:** No encryption needed (trusted environment)
- ~~Sync/Async strategy: Keep, Split, or Async-only?~~ **RESOLVED:** Keep wrapper approach

### BETA Policy Reminders
- ✅ No backward compatibility layers
- ✅ No deprecation warnings
- ✅ No multi-version support
- ✅ Clean, breaking changes OK

### Resources Needed
- Security audit (external, after Stage 1)
- Performance testing infrastructure
- User feedback on breaking changes

---

**Last Updated:** January 29, 2026  
**Next Review:** After Stage 1 completion
