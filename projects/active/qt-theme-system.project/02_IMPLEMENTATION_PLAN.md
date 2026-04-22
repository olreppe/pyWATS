# Implementation Plan: Qt Centralized Theme System

**Created:** March 25, 2026  
**Last Updated:** March 25, 2026 - 15:00

**Related Docs:**
- [README](README.md) | [Analysis](01_ANALYSIS.md) | [Progress](03_PROGRESS.md) | [TODO](04_TODO.md)

---

## Overview

Five phases, each self-contained and testable. Each phase ends with "all tests pass + no visual regressions."

---

## Phase 1: Token System & Theme Infrastructure _(Foundation)_

### Step 1.1: Define the Theme Token Dataclass
**File:** `src/pywats_ui/framework/themes/tokens.py` (new)  
**Action:** Create a frozen dataclass/NamedTuple that holds every color token as a named field. Group by semantic role:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ThemeTokens:
    """All color + style tokens for a pyWATS theme."""
    
    # --- Backgrounds ---
    bg_base: str            # Main window background (#1e1e1e)
    bg_sidebar: str         # Navigation / sidebar (#252526)
    bg_surface: str         # Panels, tabs, cards (#2d2d2d)
    bg_elevated: str        # Inputs, buttons, tooltips (#3c3c3c)
    bg_hover: str           # List/tree hover (#2a2d2e)
    bg_active_hover: str    # Button hover (#505050)
    bg_pressed: str         # Button pressed (#404040)
    
    # --- Borders ---
    border_default: str     # Standard borders (#3c3c3c)
    border_input: str       # Input field borders (#555555)
    border_header: str      # Table/section headers (#333333)
    
    # --- Brand / Accent ---
    accent_primary: str     # Orange (#f0a30a) — WATS brand
    accent_primary_hover: str   # (#ffb824)
    accent_primary_pressed: str # (#d99200)
    accent_secondary: str   # Teal (#4ec9b0)
    accent_link: str        # Blue links/footer (#569cd6)
    accent_info: str        # Info blue (#0078d4)
    accent_selection: str   # Text selection blue (#094771)
    
    # --- Text ---
    text_primary: str       # (#ffffff)
    text_secondary: str     # (#cccccc)
    text_disabled: str      # (#808080)
    text_muted: str         # (#606060)
    
    # --- Status ---
    status_online: str      # (#4ec9b0)
    status_success: str     # (#5cb85c)
    status_success_bright: str  # (#10d010)
    status_error: str       # (#f14c4c)
    status_error_alt: str   # (#c42b1c)
    status_error_soft: str  # (#f48771)
    status_warning: str     # (#dcdcaa)
    status_warning_alt: str # (#f0ad4e)
    status_pending: str     # Same as warning_alt
    
    # --- Danger actions ---
    danger_bg: str          # (#c42b1c)
    danger_hover: str       # (#e83929)
    
    # --- Scrollbar ---
    scrollbar_handle: str   # (#5a5a5a)
    scrollbar_hover: str    # (#6a6a6a)
    
    # --- Syntax highlighting (editor) ---
    syntax_keyword: str     # (#569cd6)
    syntax_string: str      # (#ce9178)
    syntax_comment: str     # (#6a9955)
    syntax_number: str      # (#b5cea8)
    syntax_function: str    # (#dcdcaa)
    syntax_class: str       # (#4ec9b0)
    syntax_decorator: str   # (#c586c0)
    syntax_builtin: str     # (#4fc1ff)
    syntax_self: str        # (#9cdcfe)
    
    # --- Sequence Designer step types ---
    step_sequence: str      # (#f5deb3)
    step_global_seq: str    # (#d4edda)
    step_numeric_limit: str # (#cce5ff)
    step_pass_fail: str     # (#d4edda)
    step_string_value: str  # (#e2d5f1)
    step_wait: str          # (#fff3cd)
    step_utility: str       # (#d6d8db) — Set Unit, Attach File, Add Subunit
    step_message: str       # (#f8d7da)
    
    # --- Editor-specific ---
    editor_gutter: str      # (#252526)
    editor_current_line: str  # (#2a2d2e)
    editor_selection: str   # (#094771)
    editor_text: str        # (#e0e0e0)
    editor_border: str      # (#3e3e3e)
    editor_bg: str          # (#1e1e1e)
    
    # --- Tab hover ---
    tab_hover: str          # (#353535)
```

**Verification:** Import in Python REPL, instantiate with test values, verify all fields accessible.

### Step 1.2: Define Dark Theme Tokens
**File:** `src/pywats_ui/framework/themes/dark_tokens.py` (new)  
**Action:** Instantiate `ThemeTokens` with all current dark theme hex values (mapped from the WATS Design Document + existing `dark.py`).

```python
from .tokens import ThemeTokens

DARK = ThemeTokens(
    bg_base="#1e1e1e",
    bg_sidebar="#252526",
    bg_surface="#2d2d2d",
    bg_elevated="#3c3c3c",
    # ... all values from Analysis color inventory
)
```

**Verification:** `assert DARK.accent_primary == "#f0a30a"`

### Step 1.3: Define Light Theme Tokens (Skeleton)
**File:** `src/pywats_ui/framework/themes/light_tokens.py` (new)  
**Action:** Create a light theme variant based on WATS Design Document. This provides proof that the system supports theme switching.

**Verification:** Instantiate and verify contrasting values.

### Step 1.4: Extract QSS Template
**File:** `src/pywats_ui/framework/themes/base.qss` (new)  
**Action:** Extract the QSS from `dark.py`'s `DARK_STYLESHEET` string into an external `.qss` file. Replace all hardcoded hex values with Python `.format()` placeholders matching `ThemeTokens` field names.

Example transform:
```css
/* Before (in dark.py) */
QMainWindow {{ background-color: #1e1e1e; }}

/* After (in base.qss) */
QMainWindow {{ background-color: {bg_base}; }}
```

**Verification:** `base.qss.format(**asdict(DARK))` produces identical output to current `DARK_STYLESHEET`.

### Step 1.5: Create ThemeManager
**File:** `src/pywats_ui/framework/themes/theme_manager.py` (new)  
**Action:** Create the central manager class:

```python
from pathlib import Path
from dataclasses import asdict
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from .tokens import ThemeTokens

class ThemeManager:
    """Centralized theme management for all pyWATS GUI applications."""
    
    _QSS_TEMPLATE: str  # Loaded from base.qss
    _current: ThemeTokens
    _app: QApplication | None
    
    def __init__(self) -> None: ...
    def apply(self, app: QApplication, tokens: ThemeTokens) -> None:
        """Apply theme to the application. All widgets inherit automatically."""
    def switch(self, tokens: ThemeTokens) -> None:
        """Switch theme at runtime."""
    def color(self, token_name: str) -> QColor:
        """Get a QColor for use in paint events / syntax highlighting."""
    def hex(self, token_name: str) -> str:
        """Get hex string for a token."""
    @property
    def current(self) -> ThemeTokens: ...
    def _apply_palette(self, app: QApplication, tokens: ThemeTokens) -> None:
        """Set QPalette for system dialog consistency."""
```

**Verification:** Unit test — create QApplication, apply dark theme, verify `app.styleSheet()` contains expected selectors.

### Step 1.6: Update `__init__.py` Exports
**File:** `src/pywats_ui/framework/themes/__init__.py`  
**Action:** Export `ThemeManager`, `ThemeTokens`, `DARK`, `LIGHT`, and keep `DARK_STYLESHEET` as a deprecated alias.

**Verification:** `from pywats_ui.framework.themes import ThemeManager, DARK`

---

## Phase 2: Integration into Framework _(Wire up BaseApplication)_

### Step 2.1: Update BaseApplication
**File:** `src/pywats_ui/framework/__init__.py`  
**Action:** Instantiate `ThemeManager` in `BaseApplication.__init__()`. Apply dark theme by default. Expose `self.theme` for child access.

```python
class BaseApplication(QApplication):
    def __init__(self, ...):
        super().__init__(...)
        self.theme = ThemeManager()
        self.theme.apply(self, DARK)
```

**Verification:** Launch Configurator — visual output should be identical to current dark theme.

### Step 2.2: Update BaseMainWindow & BasePage
**File:** `src/pywats_ui/framework/__init__.py`, `src/pywats_ui/framework/base_page.py`  
**Action:** Add `self.theme` property that returns `QApplication.instance().theme`. Convenience for child classes.

**Verification:** In any page, `self.theme.hex("accent_primary")` returns `#f0a30a`.

### Step 2.3: Deprecate `DARK_STYLESHEET` Direct Usage
**File:** `src/pywats_ui/framework/themes/dark.py`  
**Action:** Keep `DARK_STYLESHEET` as a property that generates from tokens (backward compat), add deprecation warning.

**Verification:** Any code still importing `DARK_STYLESHEET` still works but shows deprecation.

---

## Phase 3: Migrate Inline Styles → Theme Tokens _(P1 files)_

### Step 3.1: Migrate LoginWindow
**File:** `src/pywats_ui/dialogs/login_window.py`  
**Action:** Replace all inline `setStyleSheet()` hex colors with `self.theme.hex("token_name")` calls. Keep structural CSS (padding, margins) inline, extract only colors.

**Before:**
```python
self.status_label.setStyleSheet("color: #f04040;")
```
**After:**
```python
self.status_label.setStyleSheet(f"color: {self.theme.hex('status_error')};")
```

**Verification:** Launch login dialog — visual match with screenshots.

### Step 3.2: Migrate SettingsDialog
**File:** `src/pywats_ui/dialogs/settings_dialog.py`  
**Action:** Same pattern — replace hex colors with theme tokens.

### Step 3.3: Migrate ScriptEditorWidget
**File:** `src/pywats_ui/widgets/script_editor.py`  
**Action:** 
- Syntax highlighting: Replace hardcoded `QColor("#569cd6")` with `self.theme.color("syntax_keyword")`
- Editor area colors: Replace hex with theme tokens
- This is the most color-dense widget — ~15 colors

### Step 3.4: Migrate Sequence Designer Models
**File:** `src/pywats_ui/apps/sequence_designer/models.py`  
**Action:** Replace `STEP_META` hardcoded colors. Since `STEP_META` is module-level data, it needs a function that reads from the active theme:

```python
def get_step_color(step_type: StepType) -> str:
    """Get step color from active theme."""
    theme = ThemeManager.instance()
    mapping = {
        StepType.SEQUENCE: "step_sequence",
        StepType.NUMERIC_LIMIT: "step_numeric_limit",
        # ...
    }
    return theme.hex(mapping[step_type])
```

### Step 3.5: Migrate Sequence Designer Widgets
**Files:**
- `widgets/flow_canvas.py` — StepWidget per-type colors
- `widgets/definition_tree.py` — Status indicator colors
- `widgets/designer_tab.py` — Toolbar + button colors
- `widgets/outline_tree.py` — Tree selection/hover colors
- `widgets/property_editor.py` — Form styling
- `main_window.py` — ConnectDialog colors

**Action:** Replace all inline hex references with theme token lookups.

**Verification:** Open Sequence Designer, create sequence with all step types, verify visual match.

### Step 3.6: Migrate Remaining Dialogs
**Files:** `NewConverterDialog`, `InstanceSelectorDialog`  
**Action:** Same pattern.

---

## Phase 4: Migrate P2/P3 Components

### Step 4.1: Configurator Pages
**Files:** All 11 pages in `src/pywats_ui/apps/configurator/pages/`  
**Action:** Migrate status indicator colors in `dashboard.py`. Most pages inherit from `BasePage` and should already work — verify and fix any outliers.

### Step 4.2: App Main Windows
**Files:**
- `apps/yield_monitor/main_window.py`
- `apps/client_monitor/main_window.py`
- `apps/package_manager/main_window.py`
- `apps/aichat/main.py`

**Action:** Replace inline label colors (`#888`, `#4ec9b0`, `#ccc`).

### Step 4.3: System Tray Icon
**File:** `src/pywats_ui/framework/system_tray.py`  
**Action:** Replace `#4ec9b0` in `create_default_icon()` with theme token.

### Step 4.4: Full Visual Audit
**Action:** Launch every app window, verify all colors come from theme. Search codebase for any remaining hardcoded hex patterns: `grep -rn "#[0-9a-fA-F]{6}" src/pywats_ui/`

---

## Phase 5: Polish & Validation

### Step 5.1: Light Theme Completion
**File:** `src/pywats_ui/framework/themes/light_tokens.py`  
**Action:** Complete the light theme with proper contrast ratios and WATS Design Document colors. Test all apps with light theme applied.

### Step 5.2: Theme Switching UI
**File:** `src/pywats_ui/dialogs/settings_dialog.py` (or new preference in config)  
**Action:** Add a theme selector (Dark / Light / System) to the settings dialog. Persist choice in config. Apply on startup.

### Step 5.3: Documentation
**Files:**
- `docs/guides/theming.md` — User/developer guide for the theme system
- Update `CHANGELOG.md` under `[Unreleased]`

### Step 5.4: Tests
**Files:** `tests/ui/test_theme_system.py` (new)  
**Action:**
- Unit tests for `ThemeTokens` (all fields present, correct types)
- Unit tests for `ThemeManager` (apply, switch, color lookup)
- Integration test: QSS template renders without missing tokens
- Regression test: `base.qss.format(**asdict(DARK))` produces valid QSS
- Verify no hardcoded hex colors remain in `src/pywats_ui/` (linting)

### Step 5.5: Hex Color Linting Rule
**File:** `scripts/lint_theme_colors.py` (new)  
**Action:** Script that scans `src/pywats_ui/` for hardcoded hex patterns and reports violations. Can be added to pre-commit.

---

## Testing Strategy
- **Unit tests:** ThemeTokens, ThemeManager, token completeness
- **Integration tests:** QSS template renders without KeyError for both dark and light
- **Visual tests:** Manual app launch for each phase — screenshot before/after
- **Regression:** `pytest` full suite after each phase
- **Linting:** No hardcoded hex colors in widget code after Phase 4

---

## Rollback Plan
- Phase 1 is additive-only (new files) — zero risk
- Phase 2 wraps existing behavior — revert `BaseApplication.__init__()` change
- Phases 3-4 are file-by-file — each file can be independently reverted via git
- `DARK_STYLESHEET` backward compatibility alias ensures nothing breaks mid-migration
