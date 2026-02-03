# Implementation Plan: Logging Consolidation

**Version:** 1.0  
**Date:** February 3, 2026  
**Status:** Ready for Execution

---

## 🎯 Overview

Consolidate logging infrastructure across pyWATS ecosystem with unified framework, client persistence, and per-conversion logging capabilities.

**Timeline:** 2 weeks  
**Estimated Effort:** 40-60 hours

---

## 📋 Phases

### Phase 1: Enhance Core Logging Framework (Days 1-3)

**Objective:** Extend `pywats/core/logging.py` with unified configuration and utilities

**Tasks:**

1. **Add `configure_logging()` Function**
   - File: `src/pywats/core/logging.py`
   - Add comprehensive configuration function
   - Support text and JSON formats
   - Handle file rotation
   - Enable correlation IDs and context
   - Tests: `tests/cross_cutting/test_logging_config.py`
   ```python
   def configure_logging(
       level: Union[str, int] = "INFO",
       format: Literal["text", "json"] = "text",
       handlers: Optional[List[logging.Handler]] = None,
       file_path: Optional[Path] = None,
       rotate_size_mb: int = 10,
       rotate_backups: int = 5,
       enable_correlation_ids: bool = True,
       enable_context: bool = True
   ) -> None:
   ```

2. **Add `FileRotatingHandler` Class**
   - File: `src/pywats/core/logging.py`
   - Wrapper around `RotatingFileHandler`
   - pyWATS-specific defaults
   - Automatic directory creation
   - Tests: `tests/cross_cutting/test_file_rotating_handler.py`

3. **Add `LoggingContext` Context Manager**
   - File: `src/pywats/core/logging.py`
   - Scoped logging metadata
   - Clean enter/exit semantics
   - Thread-safe implementation
   - Tests: `tests/cross_cutting/test_logging_context.py`

4. **Enhance Existing Functions**
   - Update `enable_debug_logging()` to use `configure_logging()`
   - Update `enable_json_logging()` to use `configure_logging()`
   - Maintain backward compatibility
   - Tests: Update existing tests

**Deliverables:**
- Enhanced `pywats/core/logging.py` (~450 lines, +165 new)
- 15+ new unit tests
- Backward compatibility maintained

**Estimated Effort:** 2-3 days (12-18 hours)

---

### Phase 2: Client Logging Module (Days 3-5)

**Objective:** Create `pywats_client.core.logging` with top-level `pywats.log` support

**Tasks:**

1. **Create Client Logging Module**
   - File: `src/pywats_client/core/logging.py` (NEW)
   - Import and extend `pywats.core.logging`
   - Client-specific utilities
   - Tests: `tests/client/test_client_logging.py`

2. **Implement `setup_client_logging()`**
   ```python
   def setup_client_logging(
       instance_id: str = "default",
       log_level: str = "INFO",
       enable_file_logging: bool = True,
       enable_console: bool = True
   ) -> Path:
   ```
   - Determine log file location (installation directory)
   - Create `pywats_{instance_id}.log`
   - Configure rotating file handler (10MB, 5 backups)
   - Enable console handler if requested
   - Tests: Verify file creation, rotation, levels

3. **Implement `get_conversion_log_dir()`**
   ```python
   def get_conversion_log_dir(instance_id: str = "default") -> Path:
   ```
   - Return conversion logs directory
   - Create if doesn't exist
   - Tests: Directory creation, permissions

4. **Update Client Service**
   - File: `src/pywats_client/control/service.py`
   - Replace `_setup_logging()` with call to `setup_client_logging()`
   - Remove duplicate code
   - Tests: Update `tests/client/test_service.py`

5. **Update CLI**
   - File: `src/pywats_client/cli.py`
   - Replace `basicConfig` with `setup_client_logging()`
   - Add `--log-format` option (text/json)
   - Tests: Update `tests/client/test_cli.py`

**Deliverables:**
- `pywats_client/core/logging.py` (~200 lines)
- 12+ new unit tests
- Client service using unified logging
- CLI with enhanced logging options

**Estimated Effort:** 2-3 days (12-18 hours)

---

### Phase 3: Conversion Logging (Days 5-8)

**Objective:** Implement `ConversionLog` in `ConverterBase` for detailed tracking

**Tasks:**

1. **Add `ConversionLogEntry` Dataclass**
   - File: `src/pywats_client/converters/models.py`
   - Log entry structure
   - Tests: `tests/client/test_converter_models.py`

2. **Implement `ConversionLog` Class**
   - File: `src/pywats_client/converters/base.py` (or new `conversion_log.py`)
   - Per-conversion logging
   - Methods: `step()`, `warning()`, `error()`, `finalize()`
   - JSON line format
   - Auto-flush for crash safety
   - Tests: `tests/client/test_conversion_log.py`

3. **Integrate into `ConverterBase`**
   - File: `src/pywats_client/converters/base.py`
   - Rename existing `convert_file()` to `_convert_file_wrapper()`
   - Create new abstract method `convert_with_logging()`
   - Automatic `ConversionLog` creation
   - Exception capture and logging
   - Tests: Update `tests/client/test_converters.py`

4. **Update Converter Template**
   - File: `examples/converters/converter_template.py`
   - Show `ConversionLog` usage
   - Document best practices
   - Example: Step tracking, error handling

5. **Add Conversion Log Cleanup**
   - File: `src/pywats_client/core/logging.py`
   - Function: `cleanup_old_conversion_logs(max_age_days: int = 30)`
   - Configurable retention
   - Tests: Verify cleanup logic

**Deliverables:**
- `ConversionLog` implementation (~200 lines)
- Updated `ConverterBase` with logging integration
- 18+ new tests
- Updated converter template
- Cleanup utility

**Estimated Effort:** 3-4 days (18-24 hours)

---

### Phase 4: Exception Bubbling & Migration (Days 8-10)

**Objective:** Implement exception pipeline and migrate existing code

**Tasks:**

1. **Enhance Exception Handling in ConverterBase**
   - File: `src/pywats_client/converters/base.py`
   - Capture all exceptions
   - Log to both `ConversionLog` and `pywats.log`
   - Add context (file info, step, etc.)
   - Preserve full stack trace
   - Tests: Exception scenarios

2. **Update Client Service Exception Handling**
   - File: `src/pywats_client/service/client_service.py`
   - Catch converter exceptions
   - Log with structured context
   - Update status/metrics
   - Tests: Error propagation

3. **Migrate Domain Services**
   - Files: `src/pywats/domains/*/async_service.py`
   - Replace standalone loggers with `get_logger()`
   - Add structured logging calls where beneficial
   - Tests: Verify no regressions

4. **Update Examples**
   - File: `examples/sync_with_config.py`
   - Use `configure_logging()` instead of `basicConfig()`
   - Show structured logging
   - File: `examples/observability/logging_patterns.py` (NEW)
   - Comprehensive logging examples
   - File: `examples/observability/conversion_logging.py` (NEW)
   - Converter logging demo

5. **Deprecate Old Patterns**
   - Add deprecation warnings to old helper functions (if any)
   - Update MIGRATION.md with logging changes
   - Timeline: Remove in v0.4.0

**Deliverables:**
- Enhanced exception handling
- Migrated domain services
- 2 new example files
- Updated MIGRATION.md

**Estimated Effort:** 2-3 days (12-18 hours)

---

### Phase 5: Documentation & Testing (Days 10-12)

**Objective:** Comprehensive documentation and full test coverage

**Tasks:**

1. **Developer Guide: Logging Best Practices**
   - File: `docs/guides/logging.md` (NEW)
   - When to use which logging level
   - Structured vs text logging
   - Correlation IDs and context
   - Performance considerations
   - Common patterns and anti-patterns

2. **API Reference**
   - File: `docs/api/logging.rst` (NEW)
   - Sphinx documentation for all logging APIs
   - `pywats.core.logging`
   - `pywats_client.core.logging`
   - `ConversionLog`
   - Command: `python run_sphinx_build.py`

3. **Migration Guide Update**
   - File: `MIGRATION.md`
   - Section: "Logging Changes (v0.3.0)"
   - Old → New patterns
   - Breaking changes (if any)
   - Deprecation timeline

4. **Integration Tests**
   - File: `tests/integration/test_logging_integration.py` (NEW)
   - End-to-end logging scenarios
   - Client service with file logging
   - Converter with ConversionLog
   - Exception bubbling
   - Log rotation

5. **Performance Tests**
   - File: `tests/cross_cutting/test_logging_performance.py` (NEW)
   - Measure overhead
   - Async vs sync logging
   - Structured vs text
   - Target: < 5% overhead

6. **Manual Testing Checklist**
   - [ ] Start client service, verify `pywats.log` created
   - [ ] Run conversion, verify conversion log created
   - [ ] Trigger converter error, verify exception in both logs
   - [ ] Verify log rotation at 10MB
   - [ ] Check structured JSON output
   - [ ] Test on Windows, Linux, macOS

**Deliverables:**
- 2 new documentation files
- Updated MIGRATION.md
- 25+ integration/performance tests
- Manual testing complete

**Estimated Effort:** 2-3 days (12-18 hours)

---

### Phase 6: Cleanup & Release (Days 12-14)

**Objective:** Final polish and prepare for release

**Tasks:**

1. **Code Review & Cleanup**
   - Review all changed files
   - Remove debug code
   - Consistent naming conventions
   - Type hints complete
   - Docstrings updated

2. **Linting & Type Checking**
   - Run: `flake8 src/pywats/core/logging.py src/pywats_client/core/`
   - Run: `mypy src/pywats/core/logging.py`
   - Fix all issues

3. **Full Test Suite**
   - Run: `pytest`
   - Target: All 1700+ tests passing
   - New tests: ~70 added
   - Coverage: Maintain 90%+

4. **Update CHANGELOG**
   - File: `CHANGELOG.md`
   - Under `[Unreleased]` or `[0.3.0b2]`
   - Section: "Improved - Logging Infrastructure"
   - List all enhancements

5. **Create Examples Package**
   - Ensure all examples run successfully
   - Update README.md in examples/
   - Cross-platform verification

6. **Release Notes**
   - Draft release notes
   - Highlight logging improvements
   - Migration guide link
   - Breaking changes (if any)

**Deliverables:**
- Clean, linted code
- Full test suite passing
- CHANGELOG updated
- Release notes drafted

**Estimated Effort:** 2 days (12-15 hours)

---

## 🧪 Testing Strategy

### Unit Tests (Per Component)

**Core Logging:**
- `test_configure_logging.py` - Configuration options
- `test_file_rotating_handler.py` - File rotation
- `test_logging_context.py` - Context manager
- `test_structured_formatter.py` - JSON output (enhance existing)
- `test_correlation_filter.py` - Correlation IDs (enhance existing)

**Client Logging:**
- `test_client_logging.py` - Setup functions
- `test_log_paths.py` - Path resolution
- `test_log_rotation.py` - Rotation behavior

**Conversion Logging:**
- `test_conversion_log.py` - ConversionLog class
- `test_conversion_log_entry.py` - Entry dataclass
- `test_converter_logging_integration.py` - ConverterBase integration

### Integration Tests

**End-to-End Scenarios:**
1. Start client → verify log file created
2. Run converter → verify conversion log
3. Trigger error → verify exception in logs
4. Log rotation → verify backups created
5. Structured logging → verify JSON format
6. Cleanup → verify old logs removed

### Performance Tests

**Benchmarks:**
- Logging overhead (< 5% target)
- File I/O impact
- Structured vs text
- Async logging benefits

**Test Scenarios:**
- 1000 log messages/second
- Large log entries (10KB+)
- Concurrent logging (multi-threaded)

### Manual Testing

**Platform Coverage:**
- [x] Windows 10/11
- [ ] Ubuntu 22.04 LTS
- [ ] macOS (if available)

**Scenarios:**
- [ ] Client service startup
- [ ] Converter execution
- [ ] Error handling
- [ ] Log rotation
- [ ] GUI integration (if available)

---

## 🔄 Rollback Plan

### If Critical Issues Found

**Minor Issues (Non-blocking):**
1. Create issue in project tracker
2. Fix in feature branch
3. Additional testing
4. Merge when stable

**Major Issues (Blocking):**
1. Revert problematic commits
2. Release hotfix
3. Re-evaluate approach
4. Update implementation plan

**Backward Compatibility:**
- Keep old patterns working (deprecated)
- No breaking changes to public APIs
- Deprecation warnings only

---

## 📊 Success Metrics

**Code Quality:**
- [ ] Lines of duplicate code: 150 → < 10
- [ ] Logging locations: 6 patterns → 1 unified
- [ ] Test coverage: 90%+
- [ ] Type hints: 100%

**Functionality:**
- [ ] Client log file: `pywats.log` in installation dir
- [ ] Conversion logs: Per-conversion detail
- [ ] Exception bubbling: End-to-end pipeline
- [ ] Structured logging: All components

**Performance:**
- [ ] Overhead: < 5%
- [ ] File rotation: Working correctly
- [ ] Async logging: No blocking I/O

**Documentation:**
- [ ] Developer guide complete
- [ ] API reference complete
- [ ] Migration guide updated
- [ ] Examples functional

---

## ✅ Phase Completion Checklist

### Phase 1: Core Framework
- [ ] `configure_logging()` implemented
- [ ] `FileRotatingHandler` added
- [ ] `LoggingContext` added
- [ ] Tests: 15+ passing
- [ ] Backward compatibility verified

### Phase 2: Client Module
- [ ] `pywats_client/core/logging.py` created
- [ ] `setup_client_logging()` implemented
- [ ] Client service updated
- [ ] CLI updated
- [ ] Tests: 12+ passing

### Phase 3: Conversion Logging
- [ ] `ConversionLog` implemented
- [ ] `ConverterBase` updated
- [ ] Converter template updated
- [ ] Cleanup utility added
- [ ] Tests: 18+ passing

### Phase 4: Migration
- [ ] Exception handling enhanced
- [ ] Domain services migrated
- [ ] Examples updated
- [ ] MIGRATION.md updated
- [ ] Tests: All passing

### Phase 5: Documentation
- [ ] Developer guide written
- [ ] API reference generated
- [ ] Integration tests complete
- [ ] Performance tests complete
- [ ] Manual testing done

### Phase 6: Release
- [ ] Code cleanup complete
- [ ] Linting passing
- [ ] Full test suite passing
- [ ] CHANGELOG updated
- [ ] Release notes drafted

---

**Total Estimated Timeline:** 12-14 days (2 weeks)  
**Total Estimated Effort:** 40-60 hours  
**Risk Level:** MEDIUM  
**Complexity:** HIGH
