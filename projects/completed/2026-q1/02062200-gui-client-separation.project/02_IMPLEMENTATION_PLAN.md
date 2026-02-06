# Implementation Plan: GUI/Client Separation

**Version:** 1.0  
**Date:** February 3, 2026  
**Status:** EXPERIMENTAL - Not Approved for Production

---

## ⚠️ EXPERIMENTAL PROJECT

**Status**: Concept validation phase - NOT approved for production  
**Constraints**:  
- DO NOT alter existing `pywats_client/` implementation
- DO NOT deprecate old GUI (must stay functional)
- DO NOT add user-facing documentation or examples
- Keep framework minimal (simple config/alarming GUIs only)
- Analyze existing framework patterns before extending

---

## 🎯 Overview

This plan outlines the execution strategy for separating GUI components from the pyWATS Client service. The actual implementation will depend on the architecture option selected in the analysis phase.

---

## 📋 Phases

### Phase 0: Analysis & Decision (Current)

**Duration:** 1 week  
**Objective:** Complete architecture analysis and make design decision

**Tasks:**
1. Review current GUI/client coupling points
2. Document all dependencies and interfaces
3. Evaluate three architecture options
4. Conduct stakeholder review
5. Select final architecture (ADR)
6. Update this plan based on decision

**Deliverables:**
- ✅ [01_ANALYSIS.md](01_ANALYSIS.md) completed
- ⏳ Architecture Decision Record (ADR)
- ⏳ Updated implementation plan for chosen option

**Success Criteria:**
- All stakeholders approve chosen architecture
- Trade-offs clearly documented
- Migration path defined

---

### Phase 1: Framework Foundation (Week 1-2)

**Prerequisites:** Phase 0 complete, architecture decided

**Objective:** Create reusable UI framework infrastructure

**Option 1 Implementation (Separate Package):**

1. **Create `pywats_ui` Package Structure**
   ```
   src/pywats_ui/
     __init__.py
     framework/
       __init__.py
       base_app.py          # Base application class
       window_manager.py    # Window lifecycle management
       dialog_utils.py      # Common dialog patterns
     widgets/
       __init__.py
       connection_status.py # Connection indicator widget
       log_viewer.py        # Reusable log viewer
     utils/
       __init__.py
       theme.py             # Theming support
       validators.py        # Form validation
     client/
       __init__.py
       ipc_client.py        # IPC wrapper for GUI apps
   ```

2. **Implement Base Framework Classes**
   - File: `src/pywats_ui/framework/base_app.py`
   - Content: Abstract base class for all GUI applications
   - Tests: `tests/ui/framework/test_base_app.py`

3. **Create IPC Client Wrapper**
   - File: `src/pywats_ui/client/ipc_client.py`
   - Content: High-level wrapper around pywats_client IPC
   - Tests: `tests/ui/client/test_ipc_client.py`

4. **Set Up Package Metadata**
   - File: `pyproject.toml`
   - Update: Add `pywats_ui` package configuration
   - Update: Add optional dependency group `[ui]`

**Option 2 Implementation (Subpackage):**
- Similar structure under `src/pywats_client/apps/common/`

**Testing Strategy:**
- Unit tests for all framework components
- Mock IPC client for GUI tests
- Integration tests with real client service

**Estimated Effort:** 3-5 days

---

### Phase 2: Migrate Client Configurator (Week 2-3)

**Objective:** Refactor existing GUI into new framework structure

**Steps:**

1. **Create Configurator App Structure**
   ```
   src/pywats_ui/apps/configurator/
     __init__.py
     main.py              # Application entry point
     main_window.py       # Main window (refactored)
     dialogs/
       connection.py      # Connection dialog
       settings.py        # Settings dialog
     models/
       config_model.py    # Configuration data models
   ```

2. **Refactor Main Window**
   - File: `src/pywats_ui/apps/configurator/main_window.py`
   - Action: Extract from current `pywats_client/gui/main_window.py`
   - Change: Inherit from framework base classes
   - Change: Use IPC wrapper instead of direct imports
   - Tests: Update existing tests

3. **Refactor Dialogs**
   - Files: Extract all dialogs from `pywats_client/gui/`
   - Action: Move to `configurator/dialogs/`
   - Change: Use framework dialog utilities
   - Tests: Update paths and imports

4. **Update CLI Integration**
   - File: `src/pywats_client/cli.py`
   - Action: Update `gui` command to launch new configurator
   - Change: `from pywats_ui.apps.configurator import main`
   - Tests: `tests/client/test_cli.py::TestGUICommand`

5. **Deprecation Path**
   - File: `src/pywats_client/gui/__init__.py`
   - Action: Add deprecation warnings
   - Message: "Import from pywats_ui.apps.configurator instead"
   - Timeline: Remove in v0.4.0

**Testing Strategy:**
- All existing GUI tests pass
- Manual testing of configurator app
- Verify headless client still works

**Estimated Effort:** 5-7 days

---

### Phase 3: Documentation & Examples (Week 3)

**Objective:** Document new architecture and provide examples

**Deliverables:**

1. **Architecture Documentation**
   - File: `docs/guides/ui_architecture.md`
   - Content: Framework overview, app structure, best practices
   
2. **Developer Guide**
   - File: `docs/guides/building_gui_apps.md`
   - Content: How to create new GUI applications using framework

3. **Migration Guide**
   - File: `MIGRATION.md` (update)
   - Section: "GUI Module Reorganization (v0.3.0)"
   - Content: Import changes, deprecations, new patterns

4. **Example Application**
   - File: `examples/ui/minimal_app/`
   - Content: Minimal GUI app using framework
   - Purpose: Template for future applications

5. **API Reference**
   - Files: Update Sphinx docs for `pywats_ui` package
   - Command: `python run_sphinx_build.py`

**Testing Strategy:**
- Documentation builds without errors
- Example app runs successfully
- All docstrings complete

**Estimated Effort:** 2-3 days

---

### Phase 4: Cleanup & Release (Week 3)

**Objective:** Final polish and prepare for release

**Tasks:**

1. **Code Cleanup**
   - Remove old GUI code (after deprecation period)
   - Update all imports across codebase
   - Run linting: `flake8 src/pywats_ui`

2. **Testing**
   - Full test suite: `pytest`
   - GUI manual testing checklist
   - Cross-platform verification (Windows, Linux, macOS)

3. **Package Distribution**
   - Update `pyproject.toml` with new package
   - Test installation: `pip install -e .[ui]`
   - Verify optional dependencies work

4. **Release Preparation**
   - Update `CHANGELOG.md` under v0.3.0b2
   - Tag release candidate: `v0.3.0b2-rc1`
   - Create release notes

**Success Criteria:**
- All 1700+ tests passing
- No import errors
- GUI works on all platforms
- Documentation complete

**Estimated Effort:** 2-3 days

---

## 🧪 Testing Strategy

### Unit Tests
- Framework components: `tests/ui/framework/`
- Widget library: `tests/ui/widgets/`
- IPC wrapper: `tests/ui/client/`
- Target coverage: 90%+

### Integration Tests
- Configurator app end-to-end: `tests/ui/apps/configurator/`
- GUI ↔ Client communication
- Configuration persistence

### Manual Testing
- [ ] Launch configurator from CLI
- [ ] Connect to running service
- [ ] Modify configuration settings
- [ ] View service status
- [ ] Stop/start service from GUI
- [ ] Verify headless client operation

### Platform Testing
- [ ] Windows 10/11
- [ ] Ubuntu 22.04 LTS
- [ ] macOS (if available)

---

## 🔄 Rollback Plan

### If Issues Discovered

**Minor Issues:**
1. Fix in feature branch
2. Additional testing
3. Merge when stable

**Major Issues:**
1. Create hotfix branch
2. Revert problematic commits
3. Release patch with revert
4. Re-evaluate architecture decision

**Compatibility Preservatio:**
- Keep old `pywats_client/gui/` as deprecated (not removed)
- Maintain CLI command compatibility
- No breaking changes to IPC protocol

---

## 📊 Risk Mitigation

### Risk: Breaking Existing Workflows
**Mitigation:**
- Maintain backward compatible imports (deprecated)
- Update CLI to work with both old and new structure
- Gradual deprecation over 2 releases

### Risk: Increased Complexity
**Mitigation:**
- Comprehensive documentation
- Clear module boundaries
- Automated testing

### Risk: Qt Dependency Issues
**Mitigation:**
- Optional installation `pip install pywats[ui]`
- Clear error messages if Qt missing
- Headless mode always available

---

## 📝 Notes

### Decision Points

**Awaiting Decision:**
- Which architecture option (1, 2, or 3)?
- Package naming (`pywats_ui` vs `pywats_apps` vs other)?
- Deprecation timeline (1 release? 2 releases?)

### Future Enhancements

**Post-v0.3.0:**
- Plugin system for GUI apps
- Theme customization
- Additional standalone tools (log viewer, etc.)
- Shared widget library expansion

---

## ✅ Completion Checklist

### Phase 0 (Analysis)
- [ ] Architecture analysis complete
- [ ] ADR written and approved
- [ ] This plan updated with chosen option

### Phase 1 (Framework)
- [ ] `pywats_ui` package structure created
- [ ] Base framework classes implemented
- [ ] IPC wrapper complete
- [ ] Framework unit tests passing

### Phase 2 (Migration)
- [ ] Configurator app refactored
- [ ] CLI integration updated
- [ ] All existing tests pass
- [ ] Manual testing complete

### Phase 3 (Documentation)
- [ ] Architecture guide written
- [ ] Developer guide complete
- [ ] Migration guide updated
- [ ] Example app created
- [ ] API docs generated

### Phase 4 (Release)
- [ ] Code cleanup complete
- [ ] Full test suite passing
- [ ] Cross-platform verification
- [ ] CHANGELOG updated
- [ ] Release tagged

---

**Total Estimated Timeline:** 2-3 weeks  
**Risk Level:** MEDIUM  
**Complexity:** HIGH
