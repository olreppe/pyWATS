# TODO: Logging Consolidation

---

## 🧠 Planned

### Phase 1: Core Framework Enhancement (Days 1-3)
- [ ] **Add `configure_logging()` function** - Unified logging configuration
- [ ] **Implement `FileRotatingHandler` class** - Wrapper with pyWATS defaults
- [ ] **Create `LoggingContext` context manager** - Scoped logging metadata
- [ ] **Write tests for configure_logging** - All configuration options (15 tests)
- [ ] **Write tests for FileRotatingHandler** - Rotation behavior
- [ ] **Write tests for LoggingContext** - Context management
- [ ] **Update existing helpers** - Use configure_logging() internally
- [ ] **Verify backward compatibility** - All existing code works

### Phase 2: Client Logging Module (Days 3-5)
- [ ] **Create `pywats_client/core/logging.py`** - New module file
- [ ] **Implement `setup_client_logging()`** - Top-level pywats.log setup
- [ ] **Implement `get_conversion_log_dir()`** - Conversion log directory
- [ ] **Write tests for client logging** - Setup, paths, rotation (12 tests)
- [ ] **Update `ClientService._setup_logging()`** - Use new setup_client_logging()
- [ ] **Update CLI logging** - Replace basicConfig with new module
- [ ] **Add CLI --log-format option** - Support text/json
- [ ] **Test client service logging** - End-to-end verification

### Phase 3: Conversion Logging (Days 5-8)
- [ ] **Add `ConversionLogEntry` dataclass** - Log entry model
- [ ] **Implement `ConversionLog` class** - Per-conversion logging
- [ ] **Add step(), warning(), error() methods** - Logging API
- [ ] **Add finalize() method** - Complete conversion logging
- [ ] **Write ConversionLog tests** - All methods and scenarios (18 tests)
- [ ] **Integrate into `ConverterBase`** - Modify convert_file() method
- [ ] **Create `convert_with_logging()` abstract method** - New converter interface
- [ ] **Update converter template** - Show ConversionLog usage
- [ ] **Implement log cleanup utility** - cleanup_old_conversion_logs()
- [ ] **Test converter integration** - Full conversion with logging

### Phase 4: Exception Handling & Migration (Days 8-10)
- [ ] **Enhance exception capture in ConverterBase** - Full context logging
- [ ] **Update client service exception handling** - Structured error logging
- [ ] **Migrate domain service loggers** - Use get_logger() pattern
- [ ] **Update sync_with_config.py example** - Use configure_logging()
- [ ] **Create logging_patterns.py example** - Comprehensive patterns
- [ ] **Create conversion_logging.py example** - Converter logging demo
- [ ] **Add deprecation warnings** - Old patterns (if any)
- [ ] **Update MIGRATION.md** - Document logging changes

### Phase 5: Documentation & Testing (Days 10-12)
- [ ] **Write developer guide** - docs/guides/logging.md
- [ ] **Generate API reference** - docs/api/logging.rst
- [ ] **Update migration guide** - Logging section in MIGRATION.md
- [ ] **Write integration tests** - End-to-end scenarios (15 tests)
- [ ] **Write performance tests** - Measure overhead (10 tests)
- [ ] **Manual testing on Windows** - Full workflow verification
- [ ] **Manual testing on Linux** - Cross-platform check
- [ ] **Update examples README** - Document logging examples

### Phase 6: Cleanup & Release (Days 12-14)
- [ ] **Code review** - Review all changes
- [ ] **Run linting** - flake8 on all changed files
- [ ] **Run type checking** - mypy on logging modules
- [ ] **Full test suite** - pytest (all 1700+ tests)
- [ ] **Update CHANGELOG.md** - Document improvements
- [ ] **Create release notes** - Highlight logging enhancements
- [ ] **Cross-platform verification** - Windows, Linux, macOS
- [ ] **Tag release** - Version 0.3.0b2 or next

---

## 🚧 In Progress

- [🚧] Project planning and documentation - 95% complete
- [🚧] Analysis of current state - Complete
- [🚧] Architecture design - Complete

---

## ✅ Completed

- [✅] Project structure created - `logging-consolidation.project/`
- [✅] README.md drafted
- [✅] Comprehensive analysis (01_ANALYSIS.md) - 400+ lines
- [✅] Detailed implementation plan (02_IMPLEMENTATION_PLAN.md) - 650+ lines
- [✅] Progress tracking setup (03_PROGRESS.md)
- [✅] TODO checklist (04_TODO.md - this file)
- [✅] Identified all logging locations (6 patterns, 50+ files)
- [✅] Mapped code duplication (~150 lines)
- [✅] Designed architecture (enhance existing + client module + ConversionLog)
- [✅] Defined exception bubbling pipeline
- [✅] Estimated effort (2 weeks, 40-60 hours)

---

## ⏸️ Blocked

*None currently*

---

## 🔍 Research Tasks

- [✅] Audit current logging implementations
- [✅] Evaluate Python logging best practices
- [✅] Research structured logging patterns
- [✅] Review log rotation strategies
- [✅] Assess performance implications
- [ ] **Test async logging with QueueHandler** - Performance benefits
- [ ] **Evaluate log aggregation tools** - Future observability

---

## 📋 Implementation Notes

### Critical Files to Modify

**Core API:**
- `src/pywats/core/logging.py` - Enhance with new functions (+165 lines)

**Client:**
- `src/pywats_client/core/logging.py` - NEW module (+200 lines)
- `src/pywats_client/control/service.py` - Update _setup_logging()
- `src/pywats_client/cli.py` - Replace basicConfig

**Converters:**
- `src/pywats_client/converters/base.py` - Integrate ConversionLog
- `src/pywats_client/converters/models.py` - Add ConversionLogEntry

**Examples:**
- `examples/sync_with_config.py` - Update to new pattern
- `examples/observability/logging_patterns.py` - NEW comprehensive example
- `examples/observability/conversion_logging.py` - NEW converter example
- `examples/converters/converter_template.py` - Show ConversionLog usage

**Documentation:**
- `docs/guides/logging.md` - NEW developer guide
- `docs/api/logging.rst` - NEW API reference
- `MIGRATION.md` - Add logging section

**Tests:**
- `tests/cross_cutting/test_logging_config.py` - NEW
- `tests/cross_cutting/test_file_rotating_handler.py` - NEW
- `tests/cross_cutting/test_logging_context.py` - NEW
- `tests/client/test_client_logging.py` - NEW
- `tests/client/test_conversion_log.py` - NEW
- `tests/integration/test_logging_integration.py` - NEW
- `tests/cross_cutting/test_logging_performance.py` - NEW

### Key Design Decisions

**1. ConversionLog Storage:**
```
{installation_dir}/logs/conversions/
  20260203_143022_test.csv.log
  20260203_143045_data.xml.log
```

**2. Log Format (JSON Lines):**
```json
{"timestamp": "2026-02-03T14:30:22Z", "level": "INFO", "message": "Starting conversion", "file": "test.csv"}
{"timestamp": "2026-02-03T14:30:23Z", "level": "INFO", "message": "Parsing CSV", "rows": 150}
{"timestamp": "2026-02-03T14:30:24Z", "level": "ERROR", "message": "Validation failed", "error": "Missing column"}
{"event": "conversion_complete", "success": false, "duration_seconds": 2.3}
```

**3. Exception Bubbling:**
```python
try:
    result = converter.convert_file(path, args)
except Exception as e:
    # ConversionLog captures it
    conversion_log.error("Conversion failed", exc=e)
    
    # ConverterBase logs it
    logger.error(f"Converter error: {e}", exc_info=True)
    
    # Re-raise to bubble to client
    raise
```

**4. Backward Compatibility:**
- Existing `get_logger(__name__)` calls continue to work
- `enable_debug_logging()` still functional (uses configure_logging internally)
- Deprecation warnings for any old patterns
- Remove deprecated code in v0.4.0

### Testing Checklist

**Unit Tests (70+ tests total):**
- [ ] Core logging configuration (15)
- [ ] Client logging setup (12)
- [ ] ConversionLog functionality (18)
- [ ] File rotation (5)
- [ ] Context management (5)
- [ ] Integration scenarios (15)

**Manual Tests:**
- [ ] Start client service → verify pywats.log created
- [ ] Run converter → verify conversion log created
- [ ] Trigger error → verify in both logs
- [ ] Fill log to 10MB → verify rotation
- [ ] JSON format → verify structure
- [ ] Text format → verify readability

**Performance Tests:**
- [ ] Measure logging overhead (< 5% target)
- [ ] Test with 1000 messages/second
- [ ] Compare text vs JSON
- [ ] Async vs sync logging

---

## 🎯 Success Tracking

### Phase Completion Criteria

✅ **Phase 1 Complete:**
- configure_logging() working
- FileRotatingHandler tested
- LoggingContext functional
- Backward compatibility verified
- 15+ tests passing

✅ **Phase 2 Complete:**
- pywats_client/core/logging.py created
- setup_client_logging() working
- pywats.log file rotating
- CLI updated
- 12+ tests passing

✅ **Phase 3 Complete:**
- ConversionLog implemented
- ConverterBase integrated
- Converter template updated
- Cleanup utility working
- 18+ tests passing

✅ **Phase 4 Complete:**
- Exceptions bubble correctly
- Domain services migrated
- Examples updated
- MIGRATION.md current
- All existing tests pass

✅ **Phase 5 Complete:**
- Developer guide published
- API reference generated
- Integration tests complete
- Performance < 5% overhead
- Manual testing done

✅ **Phase 6 Complete:**
- Code clean and linted
- Full test suite passing (1700+)
- CHANGELOG updated
- Release notes drafted
- Cross-platform verified

---

## 📊 Metrics to Track

**Before:**
- Logging patterns: 6 different
- Duplicate code: ~150 lines
- Files with logging: 50+
- Conversion logging: Missing
- Client log file: Not rotating
- Test coverage: Partial

**After (Target):**
- Logging patterns: 1 unified
- Duplicate code: < 10 lines
- Centralized config: Yes
- Conversion logging: Full detail
- Client log file: Rotating, persistent
- Test coverage: 90%+
- New tests: 70+
- Documentation: Comprehensive

---

*Last Updated: February 3, 2026*  
*Total Tasks: 65+*  
*Completed: 9*  
*In Progress: 3*  
*Blocked: 0*
