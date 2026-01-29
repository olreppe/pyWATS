# Changelog (Beta Archive)

This file contains the changelog for beta versions 0.1.0b1 through 0.1.0b38.
For current changes, see [CHANGELOG.md](CHANGELOG.md).

---

## [0.1.0b38] - 2026-01-26

### Added
- Raises documentation for all 8 domain services (147 methods)
- Practical code examples for Asset and Process domains
- Analytics models documentation with edge cases
- Report refactoring complete (Phases 1, 2, 4)
- Domain health documentation (all domains A or A-)
- Documentation reorganization (modules/, installation/, architecture guides)
- Type safety: return type hints, statistics models, client constants, enum consolidation
- Queue architecture refactoring (MemoryQueue/PersistentQueue separation)
- Configuration architecture refactoring (API layer pure, no file I/O)
- Standard converters (6 pre-installed)
- Report header validation (problematic character blocking)

### Changed
- Queue/cache return types now typed models instead of dicts
- Configuration enum types (ErrorMode, ConverterType)
- CompOp canonical location: `pywats.shared.enums`
- Converter models canonical location: `pywats_client.converters.models`
- Configuration moved to client layer
- Converter cleanup (renamed converters, removed debug code)
- GUI architecture aligned with C# WATS Client Configurator

### Deprecated
- SimpleQueue (use MemoryQueue or PersistentQueue)
- APIConfigManager (use pywats_client.core.ConfigManager)

### Removed
- Unused GUI pages (asset, product, production, rootcause) - moved to `gui/pages/unused/`
- Legacy application architecture (pyWATSApplication, AppFacade, Client, HTTP Control API)

### Added (continued)
- ReportBuilder tool for LLM-friendly report building
- Performance optimizations (TTL caching, connection pooling, request batching, MessagePack)
- Service dashboard page
- API settings page
- Default converter setup
- Consolidated converter architecture
- Cross-platform service installation (Windows/Linux/macOS)
- Service/GUI separation architecture
- Standard folder structure

### Fixed
- ReportBuilder multi-value step fixes
- HTTP/2 dependency
- Service initialization parameter errors

### Removed
- MCP Server (experimental, moved to recommendations doc)

---

## [0.1.0b35] - 2026-01-23

### Added
- Comprehensive client test suite (71 tests)
- Docker containerization with multi-architecture support
- Enhanced error catalog (814-line reference)

### Changed
- Documentation reorganization (docs/project/ for internal tracking)

---

## [0.1.0b34] - 2026-01-15

### Added
- Routes class with 170 endpoints
- Complete sync service layer (all 9 domains)
- Async-first architecture
- Async GUI infrastructure
- ErrorHandlingMixin
- Async page operations
- ReportType enum
- Unified report query endpoint
- Report query helper methods
- Batch operations (batch_execute)
- Pagination utilities
- Automatic retry for transient failures

### Changed
- All repositories use Routes class
- GUI pages use async execution
- Report query API now uses OData

### Deprecated
- repository_internal.py files

---

## [0.1.0b33] - 2025-01-15

### Added
- Type-safe query enums (StatusFilter, RunFilter, StepType, CompOperator, SortDirection)
- Analytics dimension/KPI enums
- Path utilities (StepPath, MeasurementPath)
- DimensionBuilder presets

### Changed
- WATSFilter enum support
- Analytics models enhanced with type-safe fields
- Analytics service path handling

### Fixed
- Restored public analytics get_aggregated_measurements() helper
- MCP Server critical bug (invalid WATSFilter field names)

---

## [0.1.0b32] - 2025-01-14

### Changed
- **BREAKING**: Unified API pattern - Removed api.*_internal accessors

### Added
- API design conventions documentation
- Internal analytics tests

---

## [0.1.0b31] - 2025-01-14

_Manual release._

---

## [0.1.0b30] - 2025-01-13

### Fixed
- MeasurementData API response parsing
- StepStatusItem and MeasurementListItem aliases

---

## [0.1.0b29] - 2025-01-22

### Added
- SCIM domain (user provisioning)
- Internal analytics endpoints (step/measurement filters)

### Changed
- Window size increased to 1000x750
- Default tab visibility updated

### Fixed
- System tray icon on Windows
- Application exit stuck issue
- Settings dialog layout

---

## [0.1.0b28] - 2025-01-12

### Changed
- Test suite restructured into module-based folders

### Fixed
- RootCause assignee preservation
- Pydantic ClassVar annotation
- Architecture cleanup (removed backward compatibility code violating service layer)
- 29 failing tests across multiple domains

### Added
- ImportMode for UUT reports
- Automatic status calculation
- Failure propagation

### Fixed
- Comprehensive exception handling overhaul (~139 methods)

### Changed
- Magic numbers extracted to named constants
- Input validation with ValueError

---

## [0.1.0b27] - 2026-01-08

### Added
- End-user installation guide
- Analytics GET parameters
- Report bandwidth optimization
- Software internal API
- Production internal API
- Asset alarm state filtering

### Changed
- Asset performance documentation

### Fixed
- Analytics error handling

---

## [0.1.0b20] - 2025-12-22

Beta version bump.

---

## [0.1.0b19] - 2025-12-21

### Changed
- Agent tool surface unified
- Wrapped tool module renamed
- Experimental TSA module renamed

### Fixed
- Tool result robustness
- Mypy configuration

---

## [0.1.0b17] - 2025-12-21

### Added
- Agent execution core
- DynamicYield filter support

### Changed
- Agent public API (BETA)

---

## [0.1.0b15] - 2025-12-21

### Fixed
- Agent package bundling

---

## [0.1.0b14] - 2025-12-21

### Fixed
- Missing type imports

### Added
- Pre-release validation script

---

## [0.1.0b12] - 2025-12-21

### Fixed
- Import path issues (package shadowing)

---

## [0.1.0b11] - Previous Release

### Added
- Agent autonomy system (AnalyticalRigor, WriteMode, AgentConfig)
- Visualization sidecar system (VizBuilder)

---

## [0.1.0b10] - 2025-12-20

### Added
- UnitAnalysisTool
- ControlPanelTool
- SubUnitAnalysisTool
- Report service enhancements (OData expand)
- Report models (HeaderSubUnit, HeaderMiscInfo, HeaderAsset)

---

## [0.1.0b8] - 2025-12-19

### Added
- Agent tools in main package

### Fixed
- Tool selection patterns

---

## [0.1.0b7] - 2025-12-19

### Added
- Agent analysis tools (ProcessCapabilityTool, StepAnalysisTool, DimensionalAnalysisTool)
- AdaptiveTimeFilter
- ProcessResolver

---

## [0.1.0b6] - 2025-12-18

### Added
- Request throttling (rate limiting)
- Analytics typed models
- Analytics documentation

### Fixed
- RootCause acceptance tests

---

## [0.1.0b5] - 2025-12-17

### Fixed
- CI/CD permissions

---

## [0.1.0b4] - 2025-12-17

### Fixed
- Release pipeline (flake8 F821)

---

## [0.1.0b3] - 2025-12-17

### Fixed
- Cross-platform packaging
- Release hygiene
- UUT report parsing robustness
- Query filtering

---

## [0.1.0b2] - 2025-12-15

### Changed
- Architecture refactoring (internal API separation)

### Fixed
- CompOp export path handling
- TestInstanceConfig field mapping

---

## [0.1.0b1] - 2025-12-14

### Added
- **PyWATS API Library** (`pywats`)
  - Product, Asset, Report, Production, RootCause, Software management
  - Statistics and analytics endpoints
  - Station concept for multi-station deployments

- **PyWATS Client Application** (`pywats_client`)
  - Desktop GUI mode (PySide6/Qt)
  - Headless mode for servers and embedded systems
  - Converter framework
  - Report queue with offline support
  - HTTP control API

- **Developer Features**
  - Comprehensive type hints
  - Pydantic models
  - Structured logging
  - Async-ready architecture

### Requirements
- Python 3.10+
- WATS Server 2025.3.9.824+
