# TODO: Logging, Error & Exception Handling

**Related Docs:**  
[README](README.md) | [Analysis](01_ANALYSIS.md) | [Plan](02_IMPLEMENTATION_PLAN.md) | [Progress](03_PROGRESS.md)

---

## 🎯 Project Phases

### Phase 1: Critical Fixes (Week 1) - Priority: CRITICAL

- [ ] **Fix ConversionLog exception bubbling (#1)**
  - Add `raise_after_log` parameter to error()
  - Default to True (re-raise exceptions)
  - Add backward compat flag
  - Test: Integration test for exception propagation
  - Files: `src/pywats_client/converters/conversion_log.py`

- [ ] **Surface queue fallback failures (#2)**
  - Raise combined exception on double failure
  - Add UI alert for unrecoverable errors
  - Test: Simulate double failure scenario
  - Files: `src/pywats_ui/framework/reliability/queue_manager.py`

- [ ] **Create exception handling guidelines (#3)**
  - Document: When to catch vs bubble
  - Document: Exception logging patterns
  - Document: Error recovery strategies
  - Location: `docs/guides/exception-handling.md` (new)

### Phase 2: Consistency Improvements (Week 2) - Priority: HIGH

- [ ] **Standardize logger initialization (#4)**
  - Change all `logging.getLogger()` to `get_logger()`
  - Verify: 30+ modules in API layer
  - Verify: 25+ modules in client layer
  - Verify: 20+ modules in GUI layer
  - Test: Verify correlation IDs work everywhere

- [ ] **Add exc_info to exception logging (#5)**
  - Audit: 45 files with `logger.error()` without exc_info
  - Change: Add `exc_info=True` or use `logger.exception()`
  - Test: Verify stack traces in logs
  - Priority: Start with API layer, then client, then GUI

- [ ] **Improve GUI ErrorHandlingMixin usage (#6)**
  - Audit: GUI pages not using ErrorHandlingMixin
  - Refactor: Use mixin instead of bare except Exception
  - Test: Verify error dialogs show correctly
  - Files: `src/pywats_ui/apps/configurator/pages/*.py`

### Phase 3: Consolidation (Week 3) - Priority: MEDIUM

- [ ] **Deprecate pywats/exceptions.py (#7)**
  - Add deprecation warnings to all classes
  - Create migration guide
  - Update all internal imports to `pywats.core.exceptions`
  - Schedule removal for v0.6.0

- [ ] **Add structured logging tests (#8)**
  - Test: JSON format output validation
  - Test: Correlation ID presence
  - Test: Structured context propagation
  - Files: `tests/core/test_logging.py` (enhance)

- [ ] **Create error propagation guide (#9)**
  - Document: Exception flow converter → client → GUI
  - Diagram: Error propagation architecture
  - Examples: Proper re-raise patterns
  - Location: `docs/guides/error-propagation.md` (new)

### Phase 4: Polish & Documentation (Week 4) - Priority: LOW

- [ ] **Update documentation (#10)**
  - Update: All logging examples to use `get_logger()`
  - Update: Exception hierarchy diagrams
  - Update: Troubleshooting guide
  - Files: `docs/guides/logging.md`, `docs/getting-started.md`

- [ ] **Add developer examples (#11)**
  - Example: Proper exception handling in new module
  - Example: Structured logging patterns
  - Example: Error recovery with retry
  - Location: `examples/observability/` 

- [ ] **Create developer checklist (#12)**
  - Checklist: New module setup (logging + exceptions)
  - Checklist: Exception testing requirements
  - Checklist: Error message quality
  - Location: `docs/guides/developer-checklist.md` (new)

---

## 📊 Progress Tracking

**Total Tasks:** 12  
**Completed:** 0  
**In Progress:** 0  
**Not Started:** 12  

**Critical (Week 1):** 3 tasks  
**High (Week 2):** 3 tasks  
**Medium (Week 3):** 3 tasks  
**Low (Week 4):** 3 tasks

---

## ⚠️ Blockers

None currently identified.

---

## 📝 Notes

### Key Dependencies
- Phase 1 (#1-#3) must complete before Phase 2
- Phase 2 (#4-#6) can run in parallel
- Phase 3 (#7-#9) depends on Phase 2 completion
- Phase 4 (#10-#12) is final cleanup

### Breaking Changes
- **v0.5.1:** ConversionLog default behavior (exceptions re-raised)
- **v0.6.0:** Remove `pywats/exceptions.py` module

---

**Last Updated:** February 7, 2026
