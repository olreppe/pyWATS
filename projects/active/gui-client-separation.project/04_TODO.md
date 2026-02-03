# TODO: GUI/Client Separation

---

## 🧠 Planned

### Phase 0: Analysis & Decision
- [ ] **Review current GUI structure** - Audit all files in `src/pywats_client/gui/`
- [ ] **Map dependencies** - Document all imports and coupling points
- [ ] **Evaluate Qt framework patterns** - Research PySide6 best practices for app architecture
- [ ] **Create Architecture Decision Record (ADR)** - Document chosen option with rationale
- [ ] **Stakeholder review** - Present analysis and get approval
- [ ] **Update implementation plan** - Fill in details based on chosen architecture

### Phase 1: Framework Foundation (Pending Decision)
- [ ] Create `pywats_ui` package structure (or chosen alternative)
- [ ] Implement base application class
- [ ] Create IPC client wrapper for GUI apps
- [ ] Build reusable widget library
- [ ] Write framework unit tests
- [ ] Update `pyproject.toml` with new package

### Phase 2: Migrate Configurator
- [ ] Extract Client Configurator into new structure
- [ ] Refactor main window to use framework
- [ ] Migrate dialogs and components
- [ ] Update CLI `gui` command
- [ ] Add deprecation warnings to old imports
- [ ] Update all tests

### Phase 3: Documentation
- [ ] Write architecture guide (`docs/guides/ui_architecture.md`)
- [ ] Create developer guide for building GUI apps
- [ ] Update migration guide with import changes
- [ ] Build example minimal GUI application
- [ ] Generate Sphinx API docs for UI framework

### Phase 4: Release Preparation
- [ ] Code cleanup and linting
- [ ] Full test suite execution
- [ ] Cross-platform testing (Windows/Linux/macOS)
- [ ] Update CHANGELOG.md
- [ ] Create release candidate tag

---

## 🚧 In Progress

- [🚧] Comprehensive analysis document - 80% complete
- [🚧] Architecture options evaluation - In review

---

## ✅ Completed

- [✅] Project structure created - `gui-client-separation.project/`
- [✅] README.md drafted
- [✅] 01_ANALYSIS.md - Initial draft complete
- [✅] 02_IMPLEMENTATION_PLAN.md - Phased approach outlined
- [✅] 03_PROGRESS.md - Session tracking established
- [✅] 04_TODO.md (this file) - Task breakdown created

---

## ⏸️ Blocked

*None currently*

---

## 🔍 Research Tasks

- [ ] **Survey existing GUI frameworks** - Review how other Python projects handle multi-app GUI architectures
- [ ] **Qt application lifecycle** - Best practices for managing multiple windows/apps
- [ ] **IPC patterns** - Optimal GUI-to-service communication patterns
- [ ] **Theme/styling** - QSS (Qt Style Sheets) or other theming approaches
- [ ] **Distribution strategy** - How to package optional GUI dependencies

---

## 📋 Quick Actions

### Before Starting Implementation
1. Read through analysis document completely
2. Review current `pywats_client/gui/` code structure
3. Test current GUI functionality as baseline
4. Make architecture decision
5. Get stakeholder sign-off

### When Starting Implementation
1. Create feature branch: `git checkout -b feature/gui-client-separation`
2. Mark first TODO item with 🚧
3. Update PROGRESS.md with session start
4. Proceed with Phase 1 tasks

---

## 🎯 Success Tracking

**Definition of Done for Each Phase:**

✅ **Phase 0:** ADR approved, implementation plan finalized  
✅ **Phase 1:** Framework package functional, tests passing  
✅ **Phase 2:** Configurator migrated, all existing tests pass  
✅ **Phase 3:** Documentation complete, example app works  
✅ **Phase 4:** Release tagged, CHANGELOG updated  

---

*Last Updated: February 3, 2026*  
*Total Tasks: 35+*  
*Completed: 6*  
*In Progress: 2*  
*Blocked: 0*
