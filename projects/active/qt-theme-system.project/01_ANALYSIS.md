# Analysis: Qt Centralized Theme System

**Created:** March 25, 2026  
**Last Updated:** March 25, 2026 - 15:00

**Related Docs:**
- [README](README.md) | [Plan](02_IMPLEMENTATION_PLAN.md) | [Progress](03_PROGRESS.md) | [TODO](04_TODO.md)

---

## Problem Statement
Styling is scattered across 40+ files as inline `setStyleSheet()` calls with 35+ hardcoded hex colors. Changing the look-and-feel requires editing every file individually. There is no way to switch themes, ensure consistency, or map the WATS Design Document branding to code in one place.

---

## Current State Inventory

### GUI Component Count
| Category | Count | Examples |
|----------|-------|---------|
| Main Windows | 7 | Configurator, Sequence Designer, Yield Monitor, Client Monitor, Package Manager, AI Chat, Template |
| Dialogs | 5 | LoginWindow, SettingsDialog, NewConverterDialog, ConnectDialog, InstanceSelectorDialog |
| Pages | 11 | Dashboard, Connection, Converters, Log, Setup, Location, APISettings, ProxySettings, SNHandler, Software, About |
| Custom Widgets | 15+ | ScriptEditorWidget, StepWidget, PropertyEditor, OutlineTree, DefinitionTree, FlowCanvas, DesignerTab, Toolbox |
| Framework Classes | 3 | BaseApplication, BaseMainWindow, BasePage |
| Support Classes | 20+ | Workers, monitors, indicators, mixins |

### Current Theme Infrastructure
| Item | Location | Status |
|------|----------|--------|
| `DARK_STYLESHEET` | `src/pywats_ui/framework/themes/dark.py` | 390-line QSS as Python f-string |
| `get_system_font_family()` | `src/pywats_ui/framework/themes/dark.py` | Platform-aware font selection |
| `__init__.py` | `src/pywats_ui/framework/themes/__init__.py` | Exports DARK_STYLESHEET |
| `.qss` files | None | No external stylesheets |
| `.ui` files | None | No Qt Designer files |
| `.qrc` files | None | No Qt resource files |

### Hardcoded Color Inventory (35+ unique colors)

#### Core Theme Colors
| Color | Hex | Usage |
|-------|-----|-------|
| Background (main) | `#1e1e1e` | QMainWindow, QWidget, editor backgrounds |
| Background (sidebar) | `#252526` | Navigation, status bar, table background |
| Background (panel) | `#2d2d2d` | Tabs, panels, input backgrounds |
| Background (elevated) | `#3c3c3c` | Input fields, buttons, tooltips |
| Border (standard) | `#3c3c3c` | GroupBox, tabs, tables, separators |
| Border (input) | `#555555` | LineEdit, ComboBox, CheckBox borders |
| Border (header) | `#333333` | Table headers, section dividers |
| Hover | `#2a2d2e` | List items, tree items, outline hover |
| Active hover | `#505050` | Button hover states |

#### Brand Colors
| Color | Hex | Usage |
|-------|-----|-------|
| **Primary accent** | `#f0a30a` | Buttons, selection, focus, progress bars, nav indicator |
| Primary hover | `#ffb824` | Primary button hover |
| Primary pressed | `#d99200` | Primary button pressed |
| **Secondary accent** | `#4ec9b0` | Online status, tray icon, dashboard teal |
| Link/footer | `#569cd6` | Footer labels, VS Code blue |

#### Text Colors
| Color | Hex | Usage |
|-------|-----|-------|
| Primary text | `#ffffff` | Headings, active items |
| Secondary text | `#cccccc` | Labels, list items, header sections |
| Disabled text | `#808080` | Disabled inputs, line numbers, draft status |
| Muted text | `#606060` | Disabled button text |

#### Status Colors
| Color | Hex | Usage |
|-------|-----|-------|
| Online/Success | `#4ec9b0` | Status indicator online |
| Success alt | `#10d010`, `#5cb85c` | Login success, released status, checked buttons |
| Error/Danger | `#f14c4c`, `#f04040`, `#c42b1c` | Offline, login error, danger buttons |
| Error alt | `#f48771`, `#d9534f` | Dashboard error, revoked status |
| Warning/Pending | `#dcdcaa`, `#f0ad4e` | Connecting status, pending status |
| Info | `#0078d4` | Status messages (blue) |

#### Syntax Highlighting (ScriptEditorWidget — VS Code Dark+ palette)
| Color | Hex | Token Type |
|-------|-----|-----------|
| Keyword blue | `#569cd6` | Keywords (def, class, return) |
| String orange | `#ce9178` | String literals |
| Comment green | `#6a9955` | Comments |
| Number green | `#b5cea8` | Numeric literals |
| Function yellow | `#dcdcaa` | Function names |
| Class cyan | `#4ec9b0` | Class names |
| Decorator purple | `#c586c0` | Decorators |
| Builtin blue | `#4fc1ff` | Built-in functions |
| Self cyan | `#9cdcfe` | self/cls references |

#### Sequence Designer Step Colors
| Color | Hex | Step Type |
|-------|-----|----------|
| `#f5deb3` | Wheat | Sequence |
| `#d4edda` | Light green | Global Sequence, Pass/Fail |
| `#cce5ff` | Light blue | Numeric Limit |
| `#e2d5f1` | Light purple | String Value |
| `#fff3cd` | Light yellow | Wait |
| `#d6d8db` | Light gray | Set Unit Process, Attach File, Add Subunit |
| `#f8d7da` | Light pink | Message Box |

#### Editor-Specific Colors
| Color | Hex | Usage |
|-------|-----|-------|
| Selection blue | `#094771` | Text selection, primary buttons (designer) |
| Selection hover | `#0a5a8a` | Designer button hover |
| Tab hover | `#353535` | Tab bar hover |
| Gutter background | `#252526` | Code editor line number gutter |
| Current line | `#2a2d2e` | Code editor current line highlight |

### Files with Inline Styling (Must Be Refactored)
| File | Inline Colors | Priority |
|------|---------------|----------|
| `framework/themes/dark.py` | 25+ colors (central stylesheet) | P0 — Convert to token-based |
| `dialogs/login_window.py` | 5+ colors | P1 |
| `dialogs/settings_dialog.py` | 4+ colors | P1 |
| `widgets/script_editor.py` | 15+ colors (syntax + editor) | P1 |
| `apps/sequence_designer/models.py` | 10 step colors | P1 |
| `apps/sequence_designer/widgets/flow_canvas.py` | 10+ colors | P1 |
| `apps/sequence_designer/widgets/definition_tree.py` | 6+ colors | P1 |
| `apps/sequence_designer/widgets/designer_tab.py` | 5+ colors | P1 |
| `apps/sequence_designer/widgets/outline_tree.py` | 6+ colors | P1 |
| `apps/sequence_designer/widgets/property_editor.py` | 4+ colors | P1 |
| `apps/sequence_designer/main_window.py` | 5+ colors | P1 |
| `apps/configurator/pages/dashboard.py` | 4+ status colors | P2 |
| `apps/configurator/main_window.py` | 2+ colors | P2 |
| `apps/yield_monitor/main_window.py` | 3+ colors | P2 |
| `apps/client_monitor/main_window.py` | 3+ colors | P2 |
| `apps/package_manager/main_window.py` | 3+ colors | P2 |
| `apps/aichat/main.py` | 1+ colors | P2 |
| `framework/system_tray.py` | 1 color (icon) | P3 |

---

## Requirements

### Functional
- Single `ThemeManager` class that holds all color/style tokens
- All colors defined as named tokens, not hex literals
- QSS templates use `{token_name}` placeholders resolved at apply-time
- Theme applied once at `QApplication` level, inherited by all widgets
- Runtime theme switching (dark ↔ light) without restart
- Syntax highlighting colors part of theme (not hardcoded in highlighter)
- Sequence Designer step colors part of theme
- Status indicator colors part of theme
- QPalette integration for system dialog consistency

### Non-Functional
- Zero performance overhead (stylesheet applied once at startup)
- Backward compatible — no changes to widget constructors or public API
- WATS Design Document used as canonical color reference
- Platform-aware fonts preserved (existing `get_system_font_family()`)

---

## Constraints
- QSS does not support CSS custom properties (`var(--color)`) — must use Python string formatting
- Some widgets need `setStyleSheet()` overrides for complex selectors — those must also use theme tokens
- Syntax highlighting uses `QTextCharFormat.setForeground()`, not QSS — handled via theme color accessors
- Sequence Designer step colors are used in both QSS and paint events — need `QColor` accessors
- Must not break any existing tests (416+ test suite)

---

## Architecture Impact
- **New:** `src/pywats_ui/framework/themes/theme.py` — ThemeManager, Theme dataclass, token definitions
- **New:** `src/pywats_ui/framework/themes/dark_tokens.py` — Dark theme token values
- **New:** `src/pywats_ui/framework/themes/light_tokens.py` — Light theme token values
- **New:** `src/pywats_ui/framework/themes/base.qss` — External QSS template (extracted from dark.py)
- **Modified:** `src/pywats_ui/framework/themes/dark.py` — Refactored to use tokens
- **Modified:** `src/pywats_ui/framework/themes/__init__.py` — Export ThemeManager
- **Modified:** All files in "Files with Inline Styling" table above
- **Modified:** `src/pywats_ui/framework/__init__.py` — BaseApplication applies theme

---

## Risk Assessment
- **HIGH**: Visual regressions — Mitigate with screenshot comparison before/after each phase
- **MEDIUM**: Inline `setStyleSheet()` calls that combine structural layout + color — Must separate layout properties from color tokens
- **LOW**: Runtime theme switching edge cases (cached pixmaps, custom paint) — Test in all apps after switching
