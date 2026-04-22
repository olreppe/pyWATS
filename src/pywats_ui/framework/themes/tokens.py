"""
Theme token definitions for pyWATS GUI theming.

All colors and style values are defined as named tokens in a frozen dataclass.
The QSS template and all widgets reference tokens by name — never raw hex values.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ThemeTokens:
    """All color and style tokens for a pyWATS theme.

    Grouped by semantic role. Every color used anywhere in the GUI
    must be represented here. Widgets access tokens via ThemeManager.
    """

    # --- Backgrounds ---
    bg_base: str
    bg_sidebar: str
    bg_surface: str
    bg_elevated: str
    bg_hover: str
    bg_active_hover: str
    bg_pressed: str
    bg_disabled: str

    # --- Borders ---
    border_default: str
    border_input: str
    border_header: str
    border_hover: str
    border_disabled: str

    # --- Brand / Accent ---
    accent_primary: str
    accent_primary_hover: str
    accent_primary_pressed: str
    accent_secondary: str
    accent_link: str
    accent_info: str
    accent_selection: str
    accent_selection_hover: str

    # --- Text ---
    text_primary: str
    text_secondary: str
    text_disabled: str
    text_muted: str
    text_on_accent: str

    # --- Status ---
    status_online: str
    status_success: str
    status_success_bright: str
    status_error: str
    status_error_alt: str
    status_error_soft: str
    status_warning: str
    status_warning_alt: str

    # --- Danger actions ---
    danger_bg: str
    danger_hover: str

    # --- Scrollbar ---
    scrollbar_handle: str
    scrollbar_hover: str

    # --- Combo box arrow ---
    combo_arrow: str

    # --- Tab ---
    tab_hover: str

    # --- Syntax highlighting (code editor) ---
    syntax_keyword: str
    syntax_string: str
    syntax_comment: str
    syntax_number: str
    syntax_function: str
    syntax_class: str
    syntax_decorator: str
    syntax_builtin: str
    syntax_self: str

    # --- Sequence Designer step types ---
    step_sequence: str
    step_global_seq: str
    step_numeric_limit: str
    step_pass_fail: str
    step_string_value: str
    step_wait: str
    step_utility: str
    step_message: str

    # --- Code editor area ---
    editor_bg: str
    editor_gutter: str
    editor_current_line: str
    editor_selection: str
    editor_text: str
    editor_border: str
    editor_line_number: str

    # --- Dashboard / status indicators ---
    indicator_running: str
    indicator_stopped: str
    indicator_error: str
    indicator_unknown: str

    # --- Definition tree status ---
    def_draft: str
    def_pending: str
    def_released: str
    def_revoked: str

    # --- Tray icon ---
    tray_icon_color: str

    # --- Typography (WATS Design Document) ---
    font_family: str          # Primary font family with fallbacks
    font_family_mono: str     # Monospace font for code editor
    font_size_page_header: str    # 16px — Page header
    font_size_sub_header: str     # 14px — Page sub header, section header
    font_size_body: str           # 12px — Body text (default)
    font_size_small: str          # 10px — Small text, grid details
