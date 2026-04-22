"""Dark theme token values for pyWATS GUI.

All hex values mapped from the WATS Design Document and the existing
DARK_STYLESHEET. This is the single source of truth for the dark theme.
"""

from .tokens import ThemeTokens

DARK = ThemeTokens(
    # --- Backgrounds ---
    bg_base="#1e1e1e",
    bg_sidebar="#252526",
    bg_surface="#2d2d2d",
    bg_elevated="#3c3c3c",
    bg_hover="#2a2d2e",
    bg_active_hover="#505050",
    bg_pressed="#404040",
    bg_disabled="#2d2d2d",

    # --- Borders ---
    border_default="#3c3c3c",
    border_input="#555555",
    border_header="#333333",
    border_hover="#666666",
    border_disabled="#404040",

    # --- Brand / Accent ---
    accent_primary="#f0a30a",
    accent_primary_hover="#ffb824",
    accent_primary_pressed="#d99200",
    accent_secondary="#4ec9b0",
    accent_link="#569cd6",
    accent_info="#0078d4",
    accent_selection="#094771",
    accent_selection_hover="#0a5a8a",

    # --- Text ---
    text_primary="#ffffff",
    text_secondary="#cccccc",
    text_disabled="#808080",
    text_muted="#606060",
    text_on_accent="#1e1e1e",

    # --- Status ---
    status_online="#4ec9b0",
    status_success="#5cb85c",
    status_success_bright="#10d010",
    status_error="#f14c4c",
    status_error_alt="#c42b1c",
    status_error_soft="#f48771",
    status_warning="#dcdcaa",
    status_warning_alt="#f0ad4e",

    # --- Danger actions ---
    danger_bg="#c42b1c",
    danger_hover="#e83929",

    # --- Scrollbar ---
    scrollbar_handle="#5a5a5a",
    scrollbar_hover="#6a6a6a",

    # --- Combo box arrow ---
    combo_arrow="#cccccc",

    # --- Tab ---
    tab_hover="#353535",

    # --- Syntax highlighting (VS Code Dark+ palette) ---
    syntax_keyword="#569cd6",
    syntax_string="#ce9178",
    syntax_comment="#6a9955",
    syntax_number="#b5cea8",
    syntax_function="#dcdcaa",
    syntax_class="#4ec9b0",
    syntax_decorator="#c586c0",
    syntax_builtin="#4fc1ff",
    syntax_self="#9cdcfe",

    # --- Sequence Designer step types ---
    step_sequence="#f5deb3",
    step_global_seq="#d4edda",
    step_numeric_limit="#cce5ff",
    step_pass_fail="#d4edda",
    step_string_value="#e2d5f1",
    step_wait="#fff3cd",
    step_utility="#d6d8db",
    step_message="#f8d7da",

    # --- Code editor area ---
    editor_bg="#1e1e1e",
    editor_gutter="#252526",
    editor_current_line="#2a2d2e",
    editor_selection="#094771",
    editor_text="#e0e0e0",
    editor_border="#3e3e3e",
    editor_line_number="#808080",

    # --- Dashboard / status indicators ---
    indicator_running="#4ec9b0",
    indicator_stopped="#808080",
    indicator_error="#f48771",
    indicator_unknown="#dcdcaa",

    # --- Definition tree status ---
    def_draft="#888888",
    def_pending="#f0ad4e",
    def_released="#5cb85c",
    def_revoked="#d9534f",

    # --- Tray icon ---
    tray_icon_color="#4ec9b0",

    # --- Typography (WATS Design Document: Open Sans) ---
    font_family='"Open Sans", "Segoe UI", "Helvetica Neue", "Arial", sans-serif',
    font_family_mono='"Cascadia Code", "Consolas", "Courier New", monospace',
    font_size_page_header="16px",
    font_size_sub_header="14px",
    font_size_body="12px",
    font_size_small="10px",
)
