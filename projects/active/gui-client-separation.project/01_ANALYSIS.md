# Analysis: GUI/Client Separation

**Date:** February 3, 2026  
**Type:** Architecture Analysis

---

## 🎯 Problem Statement

The current pyWATS architecture has GUI components tightly coupled with the client service:

1. **Naming Confusion:** "GUI" folder contains what is actually the "pyWATS Client Configurator"
2. **Monolithic Structure:** No reusable UI framework for future applications
3. **Code Duplication Risk:** Each new GUI app would start from scratch
4. **Unclear Boundaries:** GUI logic mixed with client service logic

**Goal:** Establish clean separation enabling:
- Multiple GUI applications sharing common framework
- Client service that can run headless (CLI only)
- Reusable UI components across different tools

---

## 📋 Requirements

### Functional Requirements

**Must Have:**
- GUI applications can run independently of client service
- Client service can run headless (no GUI dependencies)
- Shared UI framework for common patterns (dialogs, forms, validation)
- Client Configurator remains fully functional after refactoring
- Support for future standalone tools (log viewer, report analyzer, etc.)

**Should Have:**
- Consistent look & feel across all GUI applications
- Shared configuration/settings infrastructure
- Common authentication/connection handling
- Reusable data models and validators

**Nice to Have:**
- Plugin architecture for extending applications
- Theme support
- Shared widget library (custom controls)

### Non-Functional Requirements

**Performance:**
- GUI startup time < 2 seconds
- No performance degradation from separation

**Maintainability:**
- Clear module boundaries
- Documented interfaces
- Easy to add new GUI applications

**Compatibility:**
- No breaking changes to existing CLI users
- Backward compatible configuration

---

## 🔒 Constraints

### Technical Constraints

1. **Qt Dependency:** Currently using PySide6 - maintain or abstract?
2. **Python Version:** Must support Python 3.8+ (current target)
3. **Package Size:** Optional GUI dependencies (`pip install pywats[gui]`)
4. **IPC:** Existing IPC protocol must remain stable

### Time Constraints

- Analysis phase: 1 week
- Design/decision: 3 days
- Implementation (if approved): 2-3 weeks

### Breaking Changes

**Acceptable:**
- Import paths for GUI modules
- Internal GUI structure

**Not Acceptable:**
- CLI interface changes
- Client service configuration format
- IPC protocol changes

---

## 🏗️ Architecture Impact

### Current Structure
```
src/
  pywats_client/
    gui/                    # Tightly coupled
      main_window.py
      config_dialog.py
      ...
    cli.py                  # GUI command launches from here
    service.py
```

### Proposed Options

**Option 1: Separate Package (`pywats_ui`)**
```
src/
  pywats_client/           # Service only, no GUI
  pywats_ui/               # UI framework
    framework/             # Reusable components
    apps/
      configurator/        # Client Configurator app
      log_viewer/          # Future standalone app
      report_analyzer/     # Future standalone app
```

**Option 2: Subpackage (`pywats_client.apps`)**
```
src/
  pywats_client/
    service/               # Core service logic
    apps/                  # GUI applications
      common/              # Shared UI framework
      configurator/
      log_viewer/
```

**Option 3: Monorepo with Separate Packages**
```
packages/
  pywats-api/              # Core API
  pywats-client/           # Headless client service
  pywats-ui-framework/     # Reusable UI components
  pywats-configurator/     # Client Configurator app
```

### Impact Analysis

**Option 1 (Separate Package):**
- ✅ Clean separation
- ✅ UI framework reusable across projects
- ✅ Client can be truly headless
- ❌ More complex distribution
- ❌ Potential circular dependencies

**Option 2 (Subpackage):**
- ✅ Simpler distribution
- ✅ All in one repository
- ❌ Less clear separation
- ❌ Client still has GUI code (just organized differently)

**Option 3 (Monorepo):**
- ✅ Maximum separation and reusability
- ✅ Independent versioning
- ❌ Most complex to set up and maintain
- ❌ Requires monorepo tooling

---

## ⚠️ Risk Assessment

### HIGH Risk
- **Breaking existing workflows:** Users expect `pywats-client gui` to work
  - *Mitigation:* Maintain command compatibility, deprecate gracefully
  
- **Increased complexity:** More packages/modules to maintain
  - *Mitigation:* Clear documentation, automated tests

### MEDIUM Risk
- **Dependency management:** Qt dependencies need careful handling
  - *Mitigation:* Optional dependencies, clear install instructions

- **IPC changes:** GUI-service communication might need refactoring
  - *Mitigation:* Version IPC protocol, maintain backward compatibility

### LOW Risk
- **Performance impact:** Separation might add overhead
  - *Mitigation:* Measure before/after, optimize if needed

- **Learning curve:** Contributors need to understand new structure
  - *Mitigation:* Architecture documentation, contribution guide

---

## 🔍 Additional Considerations

### Reusable Framework Components

**What should be shared:**
1. **Core UI Framework:**
   - Application base class
   - Window management
   - Dialog utilities
   - Event handling patterns

2. **Common Widgets:**
   - Connection status indicator
   - Log viewer component
   - Settings panel
   - Progress dialogs

3. **Client Integration:**
   - IPC client wrapper
   - Authentication handling
   - Configuration management
   - Error handling patterns

4. **Utilities:**
   - Theme/styling
   - Icon management
   - Layout helpers
   - Validation patterns

### Future Applications

**Potential standalone tools:**
- Log Viewer (read client/WATS logs)
- Report Analyzer (visualize test data)
- Configuration Manager (edit configs without full client)
- Health Monitor (lightweight status dashboard)
- Converter Sandbox Manager (test/debug converters)

---

## 📊 Comparison Matrix

| Aspect | Option 1: Separate Pkg | Option 2: Subpackage | Option 3: Monorepo |
|--------|----------------------|---------------------|-------------------|
| Separation Clarity | ★★★★★ | ★★★☆☆ | ★★★★★ |
| Ease of Maintenance | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ |
| Distribution Complexity | ★★★☆☆ | ★★★★★ | ★★☆☆☆ |
| Reusability | ★★★★★ | ★★★☆☆ | ★★★★★ |
| Migration Effort | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ |
| **Overall** | **17/25** | **18/25** | **16/25** |

---

## 🎯 Recommendation (TBD)

*To be filled after stakeholder discussion*

**Preferred Option:** TBD  
**Rationale:** TBD  
**Trade-offs Accepted:** TBD
