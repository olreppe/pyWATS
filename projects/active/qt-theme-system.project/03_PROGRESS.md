# Progress Tracker: Qt Centralized Theme System

**Created:** March 25, 2026  
**Last Updated:** March 25, 2026 - 15:00

**Related Docs:**
- [README](README.md) | [Analysis](01_ANALYSIS.md) | [Plan](02_IMPLEMENTATION_PLAN.md) | [TODO](04_TODO.md)

---

## Current Session: March 25, 2026

### ✅ Completed This Session
- [x] 15:00 - Full GUI component inventory (7 apps, 5 dialogs, 11 pages, 15+ widgets)
- [x] 15:00 - Color audit: 35+ hardcoded hex colors catalogued across 40+ files
- [x] 15:00 - Current theme infrastructure analyzed (dark.py, 390-line QSS)
- [x] 15:00 - Project created with analysis + 5-phase implementation plan
- [x] 15:00 - Design document referenced at `assets/WATS_Design_Document.pdf`

### 🚧 In Progress
- [ ] User to place WATS Design Document PDF at `assets/WATS_Design_Document.pdf`

### 🔍 Discoveries
- Existing `dark.py` is a good foundation — already centralized QSS, just needs tokenization
- `get_system_font_family()` already handles cross-platform fonts — keep as-is
- ScriptEditorWidget is the most color-dense component (15+ colors for syntax + editor)
- Sequence Designer has its own color system via `STEP_META` dict — needs special handling
- No `.ui`, `.qrc`, or `.qss` files exist — all code-driven (good for this migration)
- `assets/` folder is empty and ready for the design document

---

## Metrics
- Files to Modify: ~20 (inline styling)
- Files to Create: ~6 (tokens, theme_manager, qss template, light theme, tests, lint script)
- New Tests Needed: ~15-20 (theme unit + integration)
- Existing Tests Passing: 416 (must maintain)
