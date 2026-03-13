# Recent Changes — All Changes Since 0.3.0

This document summarises every notable change made after the **0.3.0b1** release (2026-02-02) up to and including the current version **0.5.0b5** (2026-03-12).

For the full, versioned history see [CHANGELOG.md](CHANGELOG.md).

---

## [0.5.0b5] — 2026-03-12

### Fixed
- **PyPI README Links**: Converted all 23 relative markdown links in `README.md` to absolute `https://github.com/olreppe/pyWATS/blob/main/` URLs. Relative links render correctly on GitHub but resolve to broken `pypi.org` paths on the PyPI project page, causing 404 errors for all documentation references.

---

## [0.5.0b4] — 2026-03-12

### Fixed
- **Runtime Annotation Compatibility (Python 3.10–3.13)**: Added `from __future__ import annotations` to `src/pywats/core/parallel.py`, fixing `TypeError: Union[Success[T], Failure] is not subscriptable` on Python 3.10–3.13. The crash occurred on any `from pywats import pyWATS` statement before user code ran. Python 3.14 was unaffected (PEP 649 lazy evaluation).
- **CI Matrix**: Added Python 3.14 to GitHub Actions test matrix.

### Added
- **Annotation Compatibility Regression Tests** (`tests/cross_cutting/test_annotation_compatibility.py`, 13 tests): Guards against future reintroduction of runtime annotation evaluation errors across Python 3.10–3.14.

---

## [0.5.0b1–0.5.0b3] — 2026-02-07 to 2026-02-19

### Added

#### Converters
- **Converter Startup File Recovery**: `AsyncConverterPool` now scans watch directories on startup to queue existing files, preventing data loss when files are dropped during system downtime. Features FIFO processing, deduplication with a 5 s buffer, statistics tracking, and configurable via `_startup_scan_enabled`.
- **Async Queue Consolidation**: Unified queue architecture with `AsyncQueueAdapter` bridging thread-safe `MemoryQueue` and async/await patterns. All converters now support a priority parameter (1=highest, 10=lowest, default=5) with heap-based ordering in `AsyncConverterPool`.

#### Logging
- **Unified Logging Infrastructure** (`pywats.core.logging`):
  - `configure_logging()` — single API for text/JSON formats, file rotation, correlation IDs, and custom handlers.
  - `FileRotatingHandler` — convenience wrapper with UTF-8 and auto directory creation.
  - `LoggingContext` — context manager for scoped logging metadata with nested support.
  - **Client Logging Module** (`pywats_client.core.logging`): `setup_client_logging()`, log-path helpers, and `cleanup_old_conversion_logs()`.
  - **ConversionLog**: Per-conversion JSON-line log with `step()` / `warning()` / `error()` / `finalize()`, auto-flush, context-manager support, and `ConverterBase` integration.
  - 63 new tests (26 core + 17 client + 20 conversion).
- **Structured Logging Foundation**: `StructuredFormatter` for ELK/Splunk/CloudWatch with ISO 8601 UTC timestamps, automatic correlation IDs, and context fields. 18 new tests.

#### Performance & Reliability
- **Circuit Breaker Pattern** (`pywats.core`): Three-state (`CLOSED → OPEN → HALF_OPEN`) fail-fast guard for `AsyncHttpClient`. Configurable thresholds; excluded exceptions (e.g. 404) don't count as failures. <0.001 ms fail-fast overhead. 19 new tests.
- **Async HTTP Response Caching**: `AsyncHttpClient` now caches successful GET responses with `AsyncTTLCache`. POST/PUT/DELETE automatically invalidate related cache entries. All 9 async domain repositories benefit with zero code changes.
- **HTTP Response Caching (sync)**: `HttpClient` gains the same caching behaviour — method + endpoint + sorted params as cache key, configurable TTL and max-size.
- **Event Loop Performance** (`EventLoopPool`): Thread-local event loop pooling gives 10–100× sync API speedup in real-world client usage. `run_sync()` updated to use `EventLoopPool.run_coroutine()`.
- **Service Integration**: `ClientConfig` gains `enable_cache`, `cache_ttl_seconds`, `cache_max_size`, `enable_metrics`, `metrics_port`. `AsyncClientService` wires cache and metrics end-to-end.
- **Health & Metrics Endpoints** (`health_server.py`): New `GET /metrics` Prometheus endpoint with HTTP cache stats, converter queue stats, and optional `MetricsCollector`.
- **Performance Benchmark Suite**: Regression tests for `EventLoopPool`, station auto-detection, circuit breaker, and JSON logging.

#### CLI & Service Management
- **Cross-Platform Service Launcher** (`pywats-client` CLI): 11 service commands (start, stop, restart, status, gui …) and 6 config commands (show, get, set, reset, path, edit). Cross-platform via `psutil`. `ServiceManager` with platform-specific backends (Windows Service, systemd, launchd). `docs/CLI_REFERENCE.md` (400+ lines). 40+ tests.

#### GUI
- **GUI Application Suite**: System-tray launcher (`pywats-launcher`) and scaffold apps — Yield Monitor, Package Manager, Client Monitor. 4 new CLI entry points.
- **GUI Settings Dialog**: Performance panel (HTTP cache config) and Observability panel (Prometheus metrics config) integrated into Client Settings.
- **Shared Client Launcher** (`src/pywats_client/launcher.py`): Unified entry point replacing duplicate `run_client_a/b` scripts (312 lines removed). Includes tray icon, config migration, and token sharing.

#### Documentation
- **Exception Handling Guidelines** (`docs/guides/exception-handling.md`): DO/DON'T checklists, decision trees, 5 core patterns, layer-specific guidance, 20+ examples, and an 8-point validation checklist.
- **Converter Documentation Suite** (50+ pages): Architecture Guide (900+ lines), Development Guide (800+ lines), Best Practices (600+ lines), Known Issues (500+ lines).
- **Comprehensive Converter Testing Suite** (79 tests): File generators, end-to-end pipeline, stress (1 620 files/s), error scenarios, post-processing, performance benchmarks, error injection, concurrency edge cases, memory/resource leak tests.
- **Caching Documentation & Examples**: `docs/guides/performance.md` (350+ lines), caching section in Getting Started, `examples/getting_started/05_caching_performance.py` (200+ lines).

### Fixed
- **Result[T] Type Subscriptability**: Fixed `Result` type alias to use `TypeAlias` for Python 3.12+ compatibility (`src/pywats/shared/result.py`).
- **RetryConfig Type Annotations**: Corrected `pyWATS.retry_config` property type hints to use the imported `CoreRetryConfig` alias.
- **Product Category Field Mapping**: `Product` model now correctly maps API `"category"` field to `product_category_name` attribute.
- **WSJF Converter Format Compatibility**: Fixed four bugs in the WATS Standard JSON Format converter — hardcoded `type='Test'`, wrong field names (`partNumber`/`serialNumber` → `pn`/`sn`), wrong step-tree field names, and discarded measurement arrays.
- **Queue Manager Double-Failure Handling**: Added `QueueCriticalError` exception and a specialised GUI dialog so disk-full/permission failures are always surfaced to users.
- **ConversionLog Silent Failures**: `ConversionLog.error()` now re-raises exceptions after logging by default (`raise_after_log=True`). Set `raise_after_log=False` for the old (silent) behaviour. 5 new tests.
- **System Tray Icon Bug**: Fixed `RuntimeError: Internal C++ object (QAction) already deleted` in `SystemTrayIcon` by storing callbacks instead of `QAction` objects.
- **GUI Configurator — Schema Mapping & UX**: Fixed `ClientConfig` v2.0 field mappings in `setup.py`, `sn_handler.py`, `api_settings.py`, `software.py`. Fixed `ConnectionMonitor` signal signature. Removed spammy success popups. Fixed `pywats-client gui` entry point.
- **service_tray.py Syntax Error**: Fixed corrupted `_stop_service()` method (garbled code at line 312).
- **Endpoint Risk Assessment Tool** (`pywats-endpoint-scan`): Automated endpoint maintenance — AST-based scan of 60+ endpoints, usage analysis, priority classification, gap analysis, markdown reports.

### Changed
- **GUI Cleanup for Beta Release**: Configurator reduced from 11 to 7 essential tabs (removed Software, Location, API Settings, Proxy). Added File menu (Disconnect, Minimize to Tray, Exit). Minimum window size reduced to 800×600. Dashboard now shows station info. Proxy settings moved into Connection → Advanced.
- **AsyncConverterPool**: Replaced plain `asyncio.Queue` with `AsyncQueueAdapter` + `MemoryQueue` for priority-based ordering.

### Improved
- **Product Box Build Template Architecture**: `AsyncBoxBuildTemplate` consolidated into `async_service.py`, eliminating 4 dead-code files (1 121 lines). No breaking changes.
- **Logger Standardisation**: All 297 source files now use `get_logger()` — 101 files updated, zero breaking changes.
- **Exception Logging with Stack Traces**: 36 files updated — `logger.error()` → `logger.exception()` in `except` blocks, `exc_info=True` added to `logger.warning()` calls.
- **GUI Error Handling Standardisation**: All 10 Configurator pages migrated to `ErrorHandlingMixin` (`handle_error()`, `show_warning()`, `confirm_action()`). 76/77 `QMessageBox` calls replaced.
- **GUI Tooltips**: Added tooltips to 7 sidebar items, 3 File menu actions, 5 Connection page widgets, and the status bar indicator.
- **Station Auto-Detection** (`get_default_station()`): Environment variable priority — `PYWATS_STATION > COMPUTERNAME > socket.gethostname()`. `StationRegistry.auto_detect()` static method added. <0.01 ms overhead.
- **Sphinx API Documentation**: New `docs/api/logging.rst` (340 lines) and `docs/api/client/logging.rst` (450 lines). Fixed module imports in models index and analytics domain docs. Clean build with zero import errors.
- **Product API Documentation**: Clarified that `get_products()` / `get_active_products()` return lightweight list data; use `get_product(part_number)` for full details.
- **Config Persistence Tests**: 4 new tests for credential save/reload, env-var fallback, and proxy roundtrip.
- **Startup Order Tests**: 3 new tests enforcing config → window → tray creation order in launcher.
- **Getting-Started Guide**: Reflects 7-tab layout, Connection-first setup flow, and live-update workflow.
- **Architecture Reliability Fixes**: Two-phase shutdown (60 s graceful + 120 s force), exception handlers for all background tasks, config validation, IPC timeouts.
- **Type Stubs**: Regenerated `.pyi` stub files for all 9 domain services (257 methods).
- **UUR Failure API**: `add_failure()` gains optional `sub_unit_idx`; new `add_failure_to_sub_unit()` by serial or index. 10 new tests.
- **Example Code Quality**: 18+ type hints added, 14 enum-consistency fixes, 4 import corrections across 11 example files.

### Deprecated
- **`pywats.exceptions` Module**: Deprecated in favour of `pywats.core.exceptions`. Old module re-exports all classes with a deprecation warning. Will be removed in v0.6.0. Migration: `from pywats.core.exceptions import PyWATSError`.

### Removed
- **`report_builder` Module** (`src/pywats/tools/report_builder.py`): Experimental, incomplete — removed along with its tests and examples.
- **`UURReport.uur_info` Property**: Use `UURReport.info` instead. See [MIGRATION.md](MIGRATION.md#uur-report-property-changes).
- **Legacy Report Models** (`report_models_old/`): 37 files (~5 000 lines) of V1 implementation fully deleted. All code uses `pywats.domains.report.report_models` (V3).

