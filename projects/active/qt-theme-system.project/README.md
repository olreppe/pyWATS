# Qt Centralized Theme System

**Created:** March 25, 2026  
**Last Updated:** March 25, 2026 - 15:00  
**Status:** 🚧 In Progress  
**Priority:** HIGH

---

## Quick Links
- [Analysis](01_ANALYSIS.md)
- [Implementation Plan](02_IMPLEMENTATION_PLAN.md)
- [Progress Tracker](03_PROGRESS.md)
- [TODO List](04_TODO.md)
- **Design Reference:** `assets/WATS_Design_Document.pdf`

---

## Objective
Replace the current scattered inline `setStyleSheet()` approach with a centralized, token-based Qt theme system. All GUI components (7 apps, 4+ dialogs, 11 pages, 15+ widgets) must derive their styling from a single source of truth — a theme definition based on the WATS Design Document. Changing the theme definition should automatically propagate to every window, dialog, and widget.

---

## Success Criteria
- [ ] All hardcoded hex colors removed from widget code
- [ ] Single theme definition file controls all styling
- [ ] Theme can be swapped (dark/light) with one call at runtime
- [ ] Syntax highlighting colors managed by theme (ScriptEditorWidget)
- [ ] Sequence Designer step colors managed by theme (STEP_META)
- [ ] Status indicator colors (online/offline/error) managed by theme
- [ ] Zero visual regressions against current dark theme
- [ ] All existing tests still pass
- [ ] Design document colors mapped and documented

---

## Current Status
Analysis and component inventory complete. 35+ hardcoded hex colors identified across 40+ files. Ready for Phase 1 implementation.
