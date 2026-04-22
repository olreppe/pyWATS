# TODO: Qt Centralized Theme System

**Created:** March 25, 2026  
**Last Updated:** March 25, 2026 - 15:00

**Related Docs:**
- [README](README.md) | [Analysis](01_ANALYSIS.md) | [Plan](02_IMPLEMENTATION_PLAN.md) | [Progress](03_PROGRESS.md)

---

## ✅ Completed
- [x] Full GUI component inventory
- [x] Color audit (35+ hex colors identified)
- [x] Project documents created
- [x] Implementation plan (5 phases)

## 🚧 In Progress
- [ ] User to place design PDF at `assets/WATS_Design_Document.pdf` — **WAITING ON USER**

## 🧠 Planned

### Phase 1: Token System & Theme Infrastructure
- [ ] 1.1 Create `ThemeTokens` dataclass (`themes/tokens.py`)
- [ ] 1.2 Create dark theme token values (`themes/dark_tokens.py`)
- [ ] 1.3 Create light theme token skeleton (`themes/light_tokens.py`)
- [ ] 1.4 Extract QSS template to `themes/base.qss`
- [ ] 1.5 Create `ThemeManager` class (`themes/theme_manager.py`)
- [ ] 1.6 Update `themes/__init__.py` exports

### Phase 2: Framework Integration
- [ ] 2.1 Update `BaseApplication` to initialize ThemeManager
- [ ] 2.2 Add `theme` property to `BaseMainWindow` / `BasePage`
- [ ] 2.3 Deprecate direct `DARK_STYLESHEET` usage

### Phase 3: Migrate P1 Components (Inline Styles → Tokens)
- [ ] 3.1 Migrate `LoginWindow`
- [ ] 3.2 Migrate `SettingsDialog`
- [ ] 3.3 Migrate `ScriptEditorWidget` (syntax + editor colors)
- [ ] 3.4 Migrate Sequence Designer `STEP_META` colors
- [ ] 3.5 Migrate Sequence Designer widgets (6 files)
- [ ] 3.6 Migrate remaining dialogs (NewConverter, InstanceSelector)

### Phase 4: Migrate P2/P3 Components
- [ ] 4.1 Migrate Configurator pages (11 pages, focus on dashboard status colors)
- [ ] 4.2 Migrate app main windows (Yield Monitor, Client Monitor, Package Manager, AI Chat)
- [ ] 4.3 Migrate system tray icon color
- [ ] 4.4 Full codebase audit — zero remaining hardcoded hex colors

### Phase 5: Polish & Validation
- [ ] 5.1 Complete light theme token values
- [ ] 5.2 Add theme switcher to Settings dialog
- [ ] 5.3 Write theming guide (`docs/guides/theming.md`)
- [ ] 5.4 Write theme tests (`tests/ui/test_theme_system.py`)
- [ ] 5.5 Create hex-color linting script
- [ ] 5.6 Update CHANGELOG.md
- [ ] 5.7 Final visual audit across all apps

## ⏸️ Blocked/Deferred
- [ ] Map exact colors from WATS Design Document PDF — **BLOCKED:** PDF needs to be placed in repo and visually inspected for exact color values

---
