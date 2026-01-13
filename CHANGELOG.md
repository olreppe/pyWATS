# Changelog

All notable changes to PyWATS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0b30] - 2025-01-13

### Fixed
- **MeasurementData API response parsing** - Fixed `analytics.get_measurements()` returning all `None` values:
  - The API returns a nested structure: `[{measurementPath, measurements: [...]}]`
  - Added `id` → `report_id` alias mapping
  - Added `startUtc` → `timestamp` alias mapping  
  - Already had `limit1` → `limit_low` and `limit2` → `limit_high` aliases
  - Updated docstring with field mapping documentation

- **StepStatusItem and MeasurementListItem aliases** - Added consistent field aliases for API compatibility:
  - Added `id` → `report_id` alias mapping
  - Added `startUtc` → `timestamp` alias mapping

## [0.1.0b29] - 2025-01-22

### Added
- **SCIM Domain** - New domain for System for Cross-domain Identity Management (user provisioning):
  - `ScimToken` model - JWT token response for Azure AD provisioning
  - `ScimUser` model - SCIM user resource with name, emails, active status
  - `ScimUserName`, `ScimUserEmail` - User name/email components
  - `ScimPatchRequest`, `ScimPatchOperation` - SCIM RFC 7644 patch format
  - `ScimListResponse` - Paginated user list response
  - Service methods via `api.scim`:
    - `get_token(duration_days)` - Generate provisioning token for Azure AD
    - `get_users()` - List all SCIM users
    - `create_user(user)` - Create a new user
    - `get_user(id)` - Get user by ID
    - `delete_user(id)` - Delete user by ID
    - `update_user(id, patch)` - Update user with SCIM patch operations
    - `get_user_by_username(username)` - Get user by username
    - `deactivate_user(id)` - Convenience method to deactivate user
    - `set_user_active(id, active)` - Set user active/inactive
    - `update_display_name(id, name)` - Update user display name
  - Complete documentation in `docs/SCIM.md`
  - Example scripts in `examples/scim/`

- **Internal Analytics Endpoints** - New step/measurement filter endpoints (⚠️ internal API):
  - `StepStatusItem` model for step status data
  - `MeasurementListItem` model for measurement list data
  - `get_aggregated_measurements()` - Aggregated stats with step/sequence filters
  - `get_measurement_list()` - Measurement values with step/sequence filters
  - `get_step_status_list()` - Step statuses with step/sequence filters
  - Simple variants: `get_measurement_list_by_product()`, `get_step_status_list_by_product()`
  - All methods accept XML step/sequence filters (obtained from TopFailed endpoint)

### Changed
- **Window size** - Increased default startup window size from 900x650 to 1000x750
- **Default tab visibility** - Asset, RootCause, Production, and Product tabs now hidden by default

### Fixed
- **System tray icon** - Fixed missing tray icon on Windows
  - Added icon validation and logging for troubleshooting
  - Added package-data config in pyproject.toml for resource files
- **Application exit** - Fixed app sometimes getting stuck on exit
  - Added status timer stop in quit handler
- **Settings dialog layout** - Fixed buttons taking up half the screen
  - Buttons now stay at bottom with fixed height

## [0.1.0b28] - 2025-01-12

### Changed
- **Test suite restructured** - Reorganized 30+ flat test files into module-based folders:
  - Each domain now has its own folder: `analytics/`, `asset/`, `process/`, `product/`, `production/`, `report/`, `rootcause/`, `software/`
  - Consistent naming: `test_service.py` (unit), `test_integration.py` (server), `test_workflow.py` (E2E)
  - Cross-cutting tests in `cross_cutting/` folder
  - Debug scripts moved to `scripts/` folder (not run by pytest)
  - Updated README with new structure and commands

### Fixed
- **RootCause assignee preservation** - Fixed ticket operations losing assignee information:
  - WATS server does not return `assignee` field in API responses
  - Service methods (`create_ticket`, `assign_ticket`, `add_comment`, `change_status`) now preserve assignee by returning it from input parameters
  - Added comprehensive documentation in service.py, models.py, and ROOTCAUSE.md

- **Pydantic ClassVar annotation** - Fixed `Step.MAX_NAME_LENGTH` causing Pydantic validation errors:
  - Changed from `MAX_NAME_LENGTH: int = 100` to `MAX_NAME_LENGTH: ClassVar[int] = 100`
  - Prevents Pydantic 2.x from treating class constants as model fields

- **Architecture cleanup** - Removed backward compatibility code that violated service layer pattern:
  - Removed `HttpClient` imports from `rootcause/service.py` and `software/service.py`
  - Service constructors now only accept repository instances (not HttpClient)
  - Enforces proper Service → Repository → HttpClient architecture

- **Test fixes** - Fixed 29 failing tests across multiple domains:
  - Product: `get_product_groups()` now uses correct HTTP GET method
  - Software: `delete_package_by_name()` test expects `None` return value
  - Report: Failing report fixture now sets `result="F"` for proper UUT status
  - RootCause: Tests now assign tickets before changing status (server requirement)

### Added
- **ImportMode for UUT reports** - New mode setting to control automatic status calculation and failure propagation:
  - `ImportMode.Import` (default): Passive mode - data stored exactly as provided
  - `ImportMode.Active`: Enables automatic behaviors for test report creation
  - Access via `api.report.import_mode = ImportMode.Active`
  
- **Automatic status calculation** - In Active mode, numeric measurements auto-calculate status:
  - Based on `comp_op` (comparison operator) and limits (`low_limit`, `high_limit`)
  - Supports all 15 CompOp types: EQ, NE, GT, LT, GE, LE, GTLT, GELE, GELT, GTLE, LTGT, LEGE, LEGT, LTGE, LOG
  - LOG comparison always passes (no limit check)
  - Status only auto-calculated when not explicitly provided
  
- **Failure propagation** - In Active mode, step failures propagate up hierarchy:
  - New `fail_parent_on_failure` property on Step class (default: `True`)
  - When step status is Failed and flag is True, parent SequenceCall also fails
  - Propagation continues recursively until flag is False or root is reached
  - `propagate_failure()` method on Step for manual propagation

### Fixed
- **Comprehensive exception handling overhaul** - Fixed ErrorHandler usage across ALL 7 domains (~139 methods):
  - **Asset domain** (20 methods): `get_asset()`, `get_assets()`, `get_asset_hierarchy()`, `create_asset()`, `update_asset()`, etc.
  - **Process domain** (5 methods): `get_processes()`, internal CRUD operations
  - **Product domain** (27 methods): `get_all()`, `save()`, `get_revision()`, `save_revision()`, batch operations, etc.
  - **Production domain** (39 methods): `get_unit()`, `save_units()`, serial number management, batch operations, etc.
  - **Report domain** (1 method): `post_wsxf()` - other methods already used ErrorHandler correctly
  - **RootCause domain** (7 methods): `get_ticket()`, `get_tickets()`, `create_ticket()`, `update_ticket()`, etc.
  - **Software domain** (28 methods): `get_packages()`, `create_package()`, folder management, history operations, etc.
  
  **Breaking behavior change**: Methods that previously returned empty lists/None on HTTP errors will now raise appropriate exceptions in STRICT mode (default):
  - HTTP 400 → `ValidationError`
  - HTTP 401 → `AuthenticationError`
  - HTTP 403 → `AuthorizationError`
  - HTTP 404 → `NotFoundError`
  - HTTP 409 → `ConflictError`
  - HTTP 5xx → `ServerError`
  
  For backwards compatibility with silent error handling, use LENIENT mode:
  ```python
  from pywats.core.exceptions import ErrorHandler, ErrorMode
  api = pyWATS(base_url, token, error_mode=ErrorMode.LENIENT)
  ```

### Changed
- **Magic numbers extracted to named constants**:
  - `ProcessService.DEFAULT_TEST_PROCESS_CODE` (100) and `DEFAULT_REPAIR_PROCESS_CODE` (500)
  - `ReportService.DEFAULT_REPAIR_PROCESS_CODE` (500) and `DEFAULT_RECENT_DAYS` (7)
  - `Step.MAX_NAME_LENGTH` (100) for step name validation

- **Input validation with ValueError** - Added required parameter validation across Service layers:
  - **Asset** (5 methods): `get_asset()`, `get_asset_by_serial()`, `create_asset()`, `delete_asset()`, `get_status()`
  - **Product** (5 methods): `get_product()`, `create_product()`, `get_revision()`, `get_revisions()`, `create_revision()`
  - **Production** (4 methods): `get_unit()`, `verify_unit()`, `get_unit_grade()`, `is_unit_passing()`
  - **RootCause** (7 methods): `get_ticket()`, `create_ticket()`, `add_comment()`, `change_status()`, `assign_ticket()`, `get_attachment()`, `upload_attachment()`
  - **Software** (14 methods): `get_package()`, `get_package_by_name()`, `get_released_package()`, `get_packages_by_tag()`, `create_package()`, `delete_package()`, `delete_package_by_name()`, all status workflow methods, `get_package_files()`, `upload_zip()`, `update_file_attribute()`
  
  All validated methods now raise `ValueError` with descriptive messages for empty/None required parameters.

## [0.1.0b27] - 2026-01-08

### Added
- **End-user installation guide** - Comprehensive documentation for pyWATS Client installation and setup:
  - Platform-specific file locations (Windows, Linux, Mac)
  - GUI vs headless installation modes
  - First-time setup instructions
  - Configuration management
  - Running as Windows service or Linux systemd service
  - Troubleshooting guide

### Fixed
- **Linting warnings** - Cleaned up development tooling:
  - Suppressed markdown line length warnings in VS Code
  - Fixed PowerShell linting issues in bump script

### Added

- **Analytics GET parameters** - Additional filtering options for analytics endpoints:
  - `get_processes()`: `include_test_operations`, `include_repair_operations`, `include_wip_operations`, `include_inactive_processes`
  - `get_product_groups()`: `include_filters` parameter to include filter configuration

- **Report bandwidth optimization** - New parameters to reduce payload sizes:
  - `get_report()`: `detail_level` (0-7), `include_chartdata`, `include_attachments`
  - `get_report_xml()`: `include_attachments`, `include_chartdata`, `include_indexes`

- **Software internal API** - New `SoftwareRepositoryInternal` class for internal operations:
  - File management: `get_file()`, `check_file()`
  - Folder management: `create_package_folder()`, `update_package_folder()`, `delete_package_folder()`, `delete_package_folder_files()`
  - Package history: `get_package_history()`, `get_package_download_history()`, `get_revoked_packages()`, `get_available_packages()`
  - Entity details: `get_software_entity_details()`, `log_download()`
  - Connection: `is_connected()`

- **Production internal API** - Extended `ProductionRepositoryInternal` with full coverage:
  - Unit operations: `get_unit()`, `get_unit_info()`, `get_unit_hierarchy()`, `get_unit_state_history()`, `get_unit_phase()`, `get_unit_process()`, `get_unit_contents()`, `create_unit()`
  - Child unit operations: `add_child_unit()`, `remove_child_unit()`, `remove_all_child_units()`, `check_child_units()`
  - Serial number management: `find_serial_numbers()`, `get_serial_number_count()`, `free_serial_numbers()`, `delete_free_serial_numbers()`, `get_serial_number_ranges()`, `get_serial_number_statistics()`
  - Sites: `get_sites()`, `is_connected()`

- **Asset alarm state filtering** - New method `get_assets_by_alarm_state()` for multi-state filtering

### Changed

- **Asset performance documentation** - `get_assets_in_alarm()` and `get_assets_in_warning()` now include:
  - Clear performance warning about N+1 API calls
  - New `top` parameter to limit assets checked
  - Documentation pointing to internal API alternatives

### Fixed
- **Analytics error handling** - `AnalyticsRepository` now properly raises exceptions on HTTP errors in STRICT mode (default):
  - Added default `ErrorHandler(ErrorMode.STRICT)` initialization, matching all other repositories
  - HTTP 403 now raises `AuthorizationError` instead of silently returning `[]`
  - HTTP 404 now raises `NotFoundError` instead of silently returning `[]`
  - HTTP 400 now raises `ValidationError` instead of silently returning `[]`
  - HTTP 5xx now raises `ServerError` instead of silently returning `[]`
  - Fixes silent error swallowing that made debugging permission/config issues difficult
  
- **DynamicYield/DynamicRepair period filtering** - `get_dynamic_yield()` and `get_dynamic_repair()` now default `includeCurrentPeriod=True` when using period-based filtering (`period_count`/`date_grouping`). Previously, omitting this parameter would return empty results due to WATS server behavior.

### Documentation
- **DynamicYield/DynamicRepair** - Enhanced documentation with:
  - Complete list of supported dimensions for both endpoints
  - Complete list of supported KPIs that can be ordered
  - Clear explanation that ordering is done via `dimensions` parameter with asc/desc hints (e.g., `"unitCount desc;partNumber"`)
  - Practical examples showing multi-level sorting and filtering patterns

## [0.1.0b20] - 2025-12-22

### Changed
- Beta version bump for ongoing development

## [0.1.0b19] - 2025-12-21

### Changed
- **Agent tool surface unified** - single canonical executor/tool interface (removed internal v1/v2 naming)
- **Wrapped tool module renamed** - internal wrapper module renamed to non-versioned name
- **Experimental TSA module renamed** - experimental TSA implementation renamed to non-versioned module

### Fixed
- **Tool result robustness** - tool execution guardrails to avoid blank/no-response outcomes (summary always present; empty data treated as explicit no-data)
- **Mypy configuration** - corrected `tool.mypy.python_version` to a real Python version

## [0.1.0b17] - 2025-12-21

### Added
- **Agent execution core** - LLM-safe tool results via bounded envelopes + out-of-band data handles
- **DynamicYield filter support** - Added misc-info and asset filter fields to `WATSFilter`

### Changed
- **Agent public API (BETA)** - canonical exports (breaking changes by design)

## [0.1.0b15] - 2025-12-21

### Fixed
- **Agent package bundling** - `pywats_agent` is now properly included in `pywats-api` package
  - Agent tools available via `from pywats_agent.tools import ...`
  - No separate package installation required

## [0.1.0b14] - 2025-12-21

### Fixed
- **Missing type imports** - Added missing `Any` imports to asset and product service modules
  - Fixed F821 linting errors that were blocking CI

### Added
- **Pre-release validation script** - New `scripts/pre_release_check.ps1` to catch errors before releasing
  - Runs flake8 linting checks (same as CI)
  - Optionally runs full test suite
  - Use `.\scripts\pre_release_check.ps1` before every release

## [0.1.0b12] - 2025-12-21

### Fixed
- **Import path issues** - Resolved package shadowing and import errors
  - Removed stale `src/pywats_agent/` directory that shadowed the correct package location
  - Fixed test imports to use public API (`pywats_agent.tools`) instead of internal paths (`pywats_agent.tools.shared.*`)
  - Added missing exports to `pywats_agent.tools.__init__.py` (TemporalMatrix, DeviationMatrix, DeviationCell, session creators)
  - All 877 tests now pass (589 agent tests + 288 API tests)

## [0.1.0b11] - Previous Release

### Added

- **Agent Autonomy System** - Configurable rigor and write safety controls
  - `AnalyticalRigor` enum: QUICK, BALANCED, THOROUGH, EXHAUSTIVE
    - Controls how thorough analytics operations are (data gathering, cross-validation)
    - Affects system prompt instructions and default parameters
  - `WriteMode` enum: BLOCKED, CONFIRM_ALL, CONFIRM_DESTRUCTIVE
    - Controls whether write operations (POST/PUT/DELETE) are allowed
    - Enforces confirmation requirements for mutations
  - `AgentConfig` class for unified configuration
    - `get_system_prompt()` - Generates rigor/write mode instructions
    - `get_default_parameters(rigor)` - Returns sample sizes scaled by rigor
    - `allows_write(operation)` - Checks if write operation is permitted
    - `requires_confirmation(operation)` - Checks if confirmation needed
  - 6 presets for common scenarios:
    - `viewer` - Read-only analytics, writes blocked
    - `quick_check` - Fast spot-checks, writes blocked  
    - `investigation` - Balanced analysis (default)
    - `audit` - Maximum thoroughness, all writes confirmed
    - `admin` - Balanced analysis with full write access
    - `power_user` - Quick analysis with full write access
  - `AgentContext` integration - Config flows through context to agent
  - 33 unit tests

- **Visualization Sidecar System** - Optional rich visualization for UI
  - `VisualizationPayload` - Bypasses LLM context, goes directly to UI
  - `VizBuilder` - Fluent builder for common chart types:
    - `line_chart()`, `area_chart()`, `bar_chart()` - Trends and comparisons
    - `pie_chart()`, `pareto_chart()` - Distribution analysis
    - `control_chart()` - SPC with UCL/LCL/target lines
    - `heatmap()`, `histogram()`, `scatter()` - Advanced analysis
    - `table()`, `kpi()`, `kpi_row()`, `dashboard()` - Data display
  - Reference lines, annotations, and drill-down support
  - `AgentResult.viz_payload` - Optional field (UI infers from data when absent)
  - `to_openai_response()` excludes viz (saves tokens)
  - `to_ui_response()` includes viz (for frontend rendering)
  - 37 unit tests

## [0.1.0b10] - 2025-12-20

### Added

- **UnitAnalysisTool** - Comprehensive individual unit analysis
  - Complete test history and status determination for any serial number
  - Production/MES tracking information (phase, batch, location)
  - Unit verification and grading (when rules configured)
  - Sub-unit (component) tracking from production and test reports
  - Multiple analysis scopes: quick, standard, full, history, verify
  - Status classification: passing, failing, in_progress, repaired, scrapped
  - 40+ unit tests

- **ControlPanelTool** - Unified administrative tool for managing WATS configuration
  - Single tool handles 5 domains: Asset, Product, Production, Software, Process
  - 12 operation types: list, get, search, create, update, delete, domain-specific
  - Entity support: assets, types, products, revisions, units, phases, packages, folders
  - Comprehensive input validation and confirmation for destructive operations
  - 50+ unit tests covering all domains and operations

- **SubUnitAnalysisTool** - Deep analysis of sub-unit (component) relationships
  - Uses query_header endpoint with OData expansion for efficient bulk queries
  - 4 query types:
    - `filter_by_subunit`: Find parent units containing a specific component
    - `get_subunits`: Get all sub-units for filtered parent reports
    - `statistics`: Aggregate sub-unit counts by type/part number/revision
    - `deviation`: Detect parents with missing, extra, or unexpected sub-units
  - Supports both UUT and UUR report types
  - Automatic baseline inference for deviation detection
  - 25 unit tests

- **Report Service Enhancements** - Extended query_header capabilities
  - OData $expand support for sub-units, misc info, assets, attachments
  - New service methods: `query_headers_with_subunits()`, `query_headers_by_subunit_part_number()`, `query_headers_by_subunit_serial()`
  - Support for OData $filter, $top, $orderby, $skip parameters

- **Report Models** - New models for expanded header data
  - `HeaderSubUnit`: serial_number, part_number, revision, part_type
  - `HeaderMiscInfo`: description, value
  - `HeaderAsset`: serial_number, running_count, total_count, calibration info

## [0.1.0b8] - 2025-12-19

### Added

- **Agent Tools in Main Package** - `pywats_agent` is now included in `pywats-api`
  - Install with `pip install pywats-api[agent]` for explicit dependency
  - Or just `pip install pywats-api` - agent tools are always included, no extra deps needed
  - LangChain integration available with `pip install pywats-api[langchain]`

### Fixed

- **Tool Selection Patterns** - Fixed regex patterns in `AgentTestHarness`
  - Added `\bwhat.?step\b` pattern for "What step is causing..." queries
  - Added `\bstep.*caus` pattern for step causation queries
  - Fixed plural forms `measurements?` for individual/raw measurements

## [0.1.0b7] - 2025-12-19

### Added

- **Agent Analysis Tools** (`pywats_agent.tools`) - Comprehensive root cause analysis workflow
  - **ProcessCapabilityTool** - Advanced SPC with:
    - Dual Cpk analysis (Cpk vs Cpk_wof - with/without failures)
    - Stability assessment before trusting Cpk values
    - Hidden mode detection (outliers, trends, drift, bimodal, centering, approaching limits)
    - Improvement priority matrix (critical → high → medium → low)
  - **StepAnalysisTool** - Test Step Analysis (TSA) for:
    - Root cause identification (steps causing unit failures)
    - Process capability (Cpk) analysis per measurement
    - Data integrity checks for SW versions and revisions
  - **DimensionalAnalysisTool** - Failure mode detection across dimensions:
    - Station, operator, fixture, batch, SW version analysis
    - Statistical significance assessment
    - Prioritized recommendations
  - **AdaptiveTimeFilter** - Dynamic time windows for varying production volumes:
    - Automatically adjusts query window based on volume
    - Prevents query overload for high-volume customers
  - **ProcessResolver** - Fuzzy matching for process/test operation names:
    - Handles imprecise user input ("PCBA" → "PCBA test")
    - Common alias expansion
    - Diagnoses mixed-test process issues

- **Documentation** - Enhanced domain knowledge documentation:
  - Process Capability Analysis section in WATS_DOMAIN_KNOWLEDGE.md
  - Workflow examples in YIELD_METRICS_GUIDE.md
  - Dual Cpk interpretation guide

## [0.1.0b6] - 2025-12-18

### Added

- **Request Throttling** - Built-in rate limiting to comply with WATS API limits (500 requests/minute)
  - New `RateLimiter` class with sliding window algorithm
  - Thread-safe implementation for concurrent usage
  - Configurable via `configure_throttling()` function
  - Can be disabled for testing with `configure_throttling(enabled=False)`
  - Statistics tracking (total requests, wait time, throttle count)

- **Analytics Typed Models** - New Pydantic models for analytics responses
  - `TopFailedStep` - Failed step statistics
  - `RepairStatistics` - Repair loop metrics
  - `RepairHistoryRecord` - Individual repair records
  - `MeasurementData` - Measurement values with statistics
  - `AggregatedMeasurement` - Time-series measurement aggregations
  - `OeeAnalysisResult` - OEE (Overall Equipment Effectiveness) analysis

- **Analytics Documentation** - Added docstrings with examples to all 23 analytics service methods

### Fixed

- **RootCause Acceptance Tests** - Fixed `DummyRootCauseRepository` to properly inherit from `RootCauseRepository`

## [0.1.0b5] - 2025-12-17

### Fixed

- **CI/CD** - Added `contents: read` permission to publish workflow for private repo checkout.

## [0.1.0b4] - 2025-12-17

### Fixed

- **Release pipeline** - Fixed flake8 `F821` (missing `Path` import) blocking the PyPI publish workflow.

## [0.1.0b3] - 2025-12-17

### Fixed

- **Cross-platform packaging** - Corrected package directory casing to `src/pywats` to avoid Linux/macOS import/install issues.
- **Release hygiene** - Ensured `tests/`, `docs/`, and other dev-only folders are excluded from PyPI artifacts and added publish-time guards.
- **UUT report parsing robustness** - Added a safe fallback for unknown step types and improved tolerance for null numeric values.
- **Query filtering** - Normalized `status=all` to omit the status filter (treat as “no status filter”).

## [0.1.0b2] - 2025-12-15

### Changed

- **Architecture Refactoring** - Internal API separation
  - All internal endpoint implementations now in separate `_internal` files
  - New `AssetRepositoryInternal` and `AssetServiceInternal` for file operations
  - New `ProductionRepositoryInternal` and `ProductionServiceInternal` for MES operations
  - Public repositories delegate to internal repositories for internal endpoints
  - Added `api.asset_internal` for asset file operations (upload, download, list, delete)
  - Added `api.production_internal` for MES unit phases

### Fixed

- CompOp export path handling for None values
- TestInstanceConfig field mapping for process_code/test_operation

## [0.1.0b1] - 2025-12-14

### Added

- **PyWATS API Library** (`pywats`)
  - Product management (get, create, update products and revisions)
  - Asset management (equipment tracking, calibration, maintenance)
  - Report submission and querying (UUT/UUR reports in WSJF format)
  - Production/serial number management (units, batches, assemblies)
  - RootCause ticket system (issue tracking and resolution)
  - Software distribution (package management, releases)
  - Statistics and analytics endpoints
  - Station concept for multi-station deployments

- **PyWATS Client Application** (`pywats_client`)
  - Desktop GUI mode (PySide6/Qt)
  - Headless mode for servers and embedded systems (Raspberry Pi)
  - Connection management with encrypted token storage
  - Converter framework for custom file format processing
  - Report queue with offline support
  - HTTP control API for remote management

- **Developer Features**
  - Comprehensive type hints throughout
  - Pydantic models for data validation
  - Structured logging with debug mode
  - Async-ready architecture

### Requirements

- Python 3.10 or later
- **WATS Server 2025.3.9.824 or later**

### Notes

This is a **beta release**. The API is stabilizing but may have breaking changes
before the 1.0 release. Please report issues on GitHub.

---

## Version History

| Version | Date | Status |
|---------|------|--------|
| 0.1.0b2 | 2025-12-15 | Beta - Architecture refactoring |
| 0.1.0b1 | 2025-12-14 | Beta - Initial public release |
