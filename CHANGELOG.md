# Changelog

All notable changes to PyWATS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For detailed migration instructions, see [MIGRATION.md](MIGRATION.md).
For beta version history (b1-b38), see [CHANGELOG-BETA.md](CHANGELOG-BETA.md).

<!-- 
AGENT INSTRUCTIONS: See CONTRIBUTING.md for changelog management rules.
- Keep entries concise (one-liners, no code blocks)
- Add migration examples to MIGRATION.md, not here
- Link breaking changes to MIGRATION.md sections
-->

---

## [Unreleased]

### Added
- **HTTP Response Caching**: Automatic caching for HTTP GET requests in src/pywats/core/client.py
  - **Cache Key Generation**: Method + endpoint + sorted params for consistent cache keys
  - **Automatic Caching**: Successful GET responses (2xx) cached with configurable TTL (default: 5 minutes)
  - **Cache Invalidation**: POST/PUT/DELETE automatically invalidate related cache entries by endpoint prefix
  - **Manual Control**: `clear_cache()`, `invalidate_cache(pattern)`, and per-request `cache=False` option
  - **Cache Properties**: `cache`, `cache_enabled` properties for inspection and statistics access
  - **Configuration**: `enable_cache`, `cache_ttl`, `cache_max_size` constructor parameters
  - **Examples**: examples/performance/http_caching.py with 6 comprehensive examples (456 lines)
  - **Performance**: Domain services automatically benefit (no code changes required)
  - **Tests**: New comprehensive example demonstrating cache hits/misses, TTL expiration, invalidation

- **Metrics Integration**: HttpClient now supports MetricsCollector for request tracking
  - **Optional Parameter**: `metrics_collector` constructor parameter for Prometheus integration
  - **Automatic Tracking**: HTTP requests tracked by method, endpoint, status code, and duration
  - **Integrates With**: Existing src/pywats/core/metrics.py Prometheus metrics infrastructure
  - **No Breaking Changes**: Metrics collection is opt-in via parameter

- **Health & Metrics Endpoints**: Enhanced health_server.py with /metrics endpoint
  - **GET /metrics**: Prometheus text format (if MetricsCollector configured) or JSON summary
  - **HTTP Cache Metrics**: hit_rate, size, evictions, requests/hits/misses from HttpClient cache
  - **Converter Queue Metrics**: size, active_workers, total_processed from AsyncConverterPool
  - **Backward Compatible**: Existing /health endpoints unchanged, /metrics is new addition
  - **Location**: src/pywats_client/service/health_server.py

- **Async Queue Consolidation**: Unified queue architecture with priority support for converters
  - **AsyncQueueAdapter**: Bridge between thread-safe MemoryQueue and async/await patterns (289 lines, fully tested)
  - **Converter Priority**: All converters now support priority parameter (1=highest, 10=lowest, default=5)
  - **Configuration Support**: Priority field added to ConverterConfig for GUI/JSON configuration
  - **Priority-Based Processing**: AsyncConverterPool uses heap-based priority queue for converter task ordering
  - **Real-Time Protection**: High-priority converters (priority=1-2) processed before low-priority batch uploads (priority=8-10)
  - **Zero Duplication**: Eliminated duplicate queue implementations (removed asyncio.Queue usage in favor of MemoryQueue foundation)
  - **Test Coverage**: 13 AsyncConverterPool tests passing, leverages 29 existing MemoryQueue priority tests

### Changed
- **AsyncConverterPool**: Replaced plain asyncio.Queue with AsyncQueueAdapter + MemoryQueue (priority-based ordering)
- **ConverterBase**: Added priority field with documentation for real-time vs batch use cases
- **Test Compatibility**: Updated AsyncConverterPool tests for new API signatures (_process_with_limit, size property)

### Removed
- **Legacy Report Models**: Completed cleanup of V1/V2/V3 report model implementations
  - **report_models_old/**: Deleted 37 files (~5,000 lines) - V1 implementation fully removed
  - **report_models_v1/**: Orphaned (no active imports) - available for future cleanup
  - **report_models_v2/**: Orphaned (no active imports) - available for future cleanup
  - **Current Production**: All code uses `pywats.domains.report.report_models` (V3 migration complete)
  - **Tests**: All 416 tests passing (97% pass rate maintained)

---

## [0.3.0b1] - 2026-02-02

### Added
- **Priority Queue System**: Universal priority-based processing for all queue implementations
  - **Priority Field**: Integer 1-10 (1=highest priority, 10=lowest, default=5) added to `QueueItem` base class
  - **Heap-Based Ordering**: MemoryQueue uses min-heap for priority-first, then FIFO processing (replaces deque)
  - **Lazy Cleanup**: Efficient heap management - invalid items discarded during retrieval rather than maintaining separate heaps
  - **File Persistence**: PersistentQueue stores priority in `.meta.json` files and rebuilds heap on reload
  - **Retry Support**: Failed items re-added to heap with original or updated priority
  - **Backward Compatible**: Default priority=5, `from_dict()` handles missing priority field, all existing tests pass
  - **Test Coverage**: 29 comprehensive tests (10 QueueItem + 17 MemoryQueue + 12 PersistentQueue) - all passing

>>>>>>> 232a9e8e33cd1b36208e6a384531b4effb69c0dd
- **Sync Wrapper Enhancements**: Comprehensive reliability features for synchronous API usage
  - **Timeout Control**: Configurable timeout for all sync operations (default 30s, customizable per-client or disabled via `timeout=None`)
  - **Retry Logic**: Exponential backoff retry with configurable max retries, backoff factor, and error types (disabled by default for safety)
  - **Correlation IDs**: Automatic 8-char UUID correlation IDs for request tracking across logs (enabled by default, can disable)
  - **Configuration**: New `SyncConfig` and `RetryConfig` dataclasses in `pywats.core.config` for centralized control
  - **Logging Integration**: `CorrelationFilter` adds correlation IDs to all log records for distributed tracing
  - **Documentation**: New guide at `docs/guides/sync-vs-async.md` with examples, troubleshooting, best practices
  - **Examples**: Comprehensive examples in `examples/sync_with_config.py` demonstrating all configuration patterns
  - **Tests**: 51 new tests covering timeout, retry, correlation, and configuration integration (all passing)

### Improved
- **Status Enums**: Enhanced `StepStatus`, `ReportStatus`, and `StatusFilter` with flexible string conversion and best practice enforcement
  - **Flexible Conversion**: Accepts multiple input formats via `_missing_` hook - exact values ("P", "F"), full names ("Passed", "Failed"), case-insensitive variants ("PASSED", "passed"), and 30+ common aliases ("OK", "pass", "fail", "NG", "success")
  - **Best Practices**: All examples, internal tools, and tests refactored to use enum members (`StepStatus.Passed`) instead of string literals (`"Passed"`)
  - **Type Safety**: Function signatures updated to use `StepStatus | str` for better IDE support and type checking
  - **Properties**: New helper properties - `full_name`, `is_passing`, `is_failure` for convenient status checking
  - **Backward Compatible**: String inputs still work via flexible conversion - zero breaking changes
  - **Serialization**: Format unchanged - StepStatus/ReportStatus use single letters ("P", "F"), StatusFilter uses full words
  - **Refactored**: 13 example files, 4 internal tools, 3 test files (150+ string-to-enum replacements)
  - **Test Coverage**: 29 comprehensive enum conversion tests added to active test suite

- **Configuration**: LogLevel enum properly used in GUI settings dialog and config validation (replaced hardcoded string lists)

- **Test Suite**: Total test count: 1567 tests (79 new tests from recent projects - priority queue and sync wrapper)

---

## [0.2.0b3] - 2026-01-29

### Added
- **Documentation**: Comprehensive architecture review documents for code quality and maintenance
  - API Architecture Review (650+ lines) - 9.5/10 rating
  - Client Architecture Review (850+ lines) - 9.0/10 rating
  - Cross-Platform Support Review (1000+ lines) - 9.0/10 rating
  - GUI Architecture Review (600+ lines) - 8.0/10 rating

### Removed
- Obsolete internal documentation (NAMING_CONSISTENCY_REPORT.md)

---

## [0.2.0b2] - 2026-01-29

### Added
- Test coverage improvements for pywats_client: new tests for `io.py`, `config_manager.py`, `connection_config.py`, `exceptions.py`, `converters/models.py`, and `exit_codes.py` modules
- Coverage configuration: excluded GUI code from coverage metrics (gui/, service_tray.py, windows_service.py, diagnostics.py) to focus on testable modules
- **Documentation**: AI coding attribution and project credits (Integration Architect: Ola Lund Reppe)
- **Documentation**: Critical test suite warning - tests must NEVER be run on production servers
- **Threading**: Comprehensive thread safety documentation (`docs/guides/thread-safety.md`)
- **Threading**: Thread safety tests for TTLCache (`tests/cross_cutting/test_cache_threading.py` - 8 tests)
- **Threading**: Parallel execution stress tests (`tests/integration/test_parallel_stress.py` - 16 tests)
- **Threading**: Enhanced docstrings with thread safety guarantees for `MemoryQueue`, `TTLCache`, `parallel_execute`

### Changed
- **Company branding**: Updated from Virinco AS to The WATS Company AS across all documentation, deployment configs, and copyright notices
- **Performance**: `run_sync()` now uses pooled ThreadPoolExecutor (4 workers) instead of creating new executor per call
- **Performance**: `MemoryQueue.__iter__()` returns snapshot to avoid holding lock during iteration
- **Threading**: `AsyncTTLCache` refactored to remove inheritance and dual locking (asyncio.Lock only, no threading.RLock)

### Fixed
- Python 3.11 typing compatibility: `Result[T]` type alias cannot be subscripted on Union types. Changed `parallel_execute` return type to use `Union[Success[T], Failure]` directly.

---

## [Unreleased]

### Added
- **Async Client Architecture**: Complete async-first implementation for WATS Client
  - `AsyncClientService`: Main async service controller using asyncio event loop
  - `AsyncConverterPool`: Concurrent file conversion with asyncio.Semaphore (10 concurrent)
  - `AsyncPendingQueue`: Concurrent report uploads (5 concurrent vs sequential)
  - `AsyncAPIMixin`: GUI helper for async API calls with auto sync/async detection
- `qasync` integration for Qt + asyncio in GUI mode
- GUI auto-test: Connection page automatically tests server connectivity on startup
- `AttachmentIO` class in `pywats_client.io` for file-based attachment operations
- `Step.add_attachment()` method for memory-only attachment handling
- `AttachmentMetadata` class (renamed from `Attachment` in models.py for clarity)
- `QueueItemStatus` enum for unified queue states
- `RetryHandler` class for unified retry execution
- Platform native installers (Windows MSI, macOS PKG/DMG, standalone executables)
- Multi-platform deployment infrastructure (systemd, launchd, Windows Service)
- Enhanced error messages with troubleshooting hints
- Layered event architecture (`pywats_events`, `pywats_cfx`)
- WATS 25.3 Asset module enhancements (calibration/maintenance, count management)
- Alarm and notification logs API

### Fixed
- GUI responsiveness: qasync event loop integration enables async operations without blocking UI
- Connection test now follows HTTP redirects (301/302)
- Connection page status colors: "Connected"/"Online" now display in green
- "Offline"/"Disconnected" states now display in gray instead of red
- **GUI navigation**: Dashboard and API Settings pages now visible in sidebar menu
- **GUI signal connection**: Fixed "Setup" vs "General" page name mismatch

### Changed
- **File I/O architecture**: `pywats` is now memory-only; file operations in `pywats_client`
- **GUI pages reorganized**: Unused domain pages (Asset, Product, Production, RootCause) moved to `pages/unused/`
- Documentation reorganized into `docs/guides/`, `docs/reference/`, `docs/platforms/`, `docs/domains/`
- Core modules renamed: `batch` → `parallel`, `batching` → `coalesce`
- Terminology standardized: "Module" → "Domain"
- Test suite reorganized into domain-based structure
- Domain health grading upgraded to 60-point scale

### Removed (Breaking)
- `Attachment.from_file()` - Use `AttachmentIO.from_file()` ([migration](MIGRATION.md#v010b40---file-io-separation))
- `Step.attach_file()` - Use `AttachmentIO.from_file()` + `step.add_attachment()`
- `UURReport.attach_file()` - Use `attach_bytes()` instead
- `SimpleQueue` - Use `pywats_client.ClientService` for queuing
- `AsyncReportService` offline methods (`submit_offline`, `process_queue`, `offline_fallback`)
- Legacy UUR classes: `UURAttachment`, `Failure`, `UURPartInfo`, `FailCode`, `MiscUURInfo` ([migration](MIGRATION.md#v010b40---deprecated-uur-classes-removed))
- `gui/widgets/instance_selector.py` - Unused widget removed

### Deprecated
- UUR legacy classes marked for removal (now removed - see above)

---

## Beta Archive

All beta releases (0.1.0b1 through 0.1.0b38) have been archived to [CHANGELOG-BETA.md](CHANGELOG-BETA.md).

Key milestones from beta:
- **b38** - Report refactoring, type safety, queue architecture
- **b35** - Docker containerization, client test suite
- **b34** - Async-first architecture, batch operations, pagination
- **b32** - Unified API pattern (removed `*_internal` accessors)
- **b28** - Exception handling overhaul, ImportMode
- **b10** - Agent analysis tools
- **b1** - Initial release with all core domains
