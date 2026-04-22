"""Light theme token values for pyWATS GUI.

Provides a light alternative to the dark theme. All tokens map 1:1
with ThemeTokens fields — swap DARK for LIGHT to switch themes.
"""

from .tokens import ThemeTokens

LIGHT = ThemeTokens(
    # --- Backgrounds ---
    bg_base="#f5f5f5",
    bg_sidebar="#e8e8e8",
    bg_surface="#ffffff",
    bg_elevated="#ffffff",
    bg_hover="#e0e0e0",
    bg_active_hover="#d0d0d0",
    bg_pressed="#c8c8c8",
    bg_disabled="#f0f0f0",

    # --- Borders ---
    border_default="#d0d0d0",
    border_input="#b0b0b0",
    border_header="#c0c0c0",
    border_hover="#909090",
    border_disabled="#e0e0e0",

    # --- Brand / Accent ---
    accent_primary="#e69500",
    accent_primary_hover="#f0a30a",
    accent_primary_pressed="#cc8400",
    accent_secondary="#2b9f8f",
    accent_link="#0066cc",
    accent_info="#0066cc",
    accent_selection="#b3d7ff",
    accent_selection_hover="#99caff",

    # --- Text ---
    text_primary="#1e1e1e",
    text_secondary="#444444",
    text_disabled="#999999",
    text_muted="#aaaaaa",
    text_on_accent="#ffffff",

    # --- Status ---
    status_online="#2b9f8f",
    status_success="#3d8b37",
    status_success_bright="#28a745",
    status_error="#d32f2f",
    status_error_alt="#b71c1c",
    status_error_soft="#ef5350",
    status_warning="#f9a825",
    status_warning_alt="#e68a00",

    # --- Danger actions ---
    danger_bg="#d32f2f",
    danger_hover="#e53935",

    # --- Scrollbar ---
    scrollbar_handle="#c0c0c0",
    scrollbar_hover="#a0a0a0",

    # --- Combo box arrow ---
    combo_arrow="#444444",

    # --- Tab ---
    tab_hover="#e8e8e8",

    # --- Syntax highlighting (light-friendly palette) ---
    syntax_keyword="#0000ff",
    syntax_string="#a31515",
    syntax_comment="#008000",
    syntax_number="#098658",
    syntax_function="#795e26",
    syntax_class="#267f99",
    syntax_decorator="#af00db",
    syntax_builtin="#0070c1",
    syntax_self="#001080",

    # --- Sequence Designer step types (same pastel tones work on light) ---
    step_sequence="#f5deb3",
    step_global_seq="#d4edda",
    step_numeric_limit="#cce5ff",
    step_pass_fail="#d4edda",
    step_string_value="#e2d5f1",
    step_wait="#fff3cd",
    step_utility="#d6d8db",
    step_message="#f8d7da",

    # --- Code editor area ---
    editor_bg="#ffffff",
    editor_gutter="#f0f0f0",
    editor_current_line="#f0f0f0",
    editor_selection="#b3d7ff",
    editor_text="#1e1e1e",
    editor_border="#d0d0d0",
    editor_line_number="#999999",

    # --- Dashboard / status indicators ---
    indicator_running="#2b9f8f",
    indicator_stopped="#999999",
    indicator_error="#ef5350",
    indicator_unknown="#f9a825",

    # --- Definition tree status ---
    def_draft="#999999",
    def_pending="#e68a00",
    def_released="#3d8b37",
    def_revoked="#d32f2f",

    # --- Tray icon ---
    tray_icon_color="#2b9f8f",

    # --- Typography (WATS Design Document: Open Sans) ---
    font_family='"Open Sans", "Segoe UI", "Helvetica Neue", "Arial", sans-serif',
    font_family_mono='"Cascadia Code", "Consolas", "Courier New", monospace',
    font_size_page_header="16px",
    font_size_sub_header="14px",
    font_size_body="12px",
    font_size_small="10px",
)
