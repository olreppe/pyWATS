# Application Template

This folder contains a scaffolded template for creating new pyWATS GUI applications.

## Quick Start

To create a new application:

1. **Copy this template folder:**
   ```powershell
   Copy-Item -Recurse src/pywats_ui/template src/pywats_ui/apps/your_app_name
   ```

2. **Rename files and update code:**
   - Replace `{{app_name}}` with your app name (lowercase, underscores)
   - Replace `{{AppTitle}}` with your app title (human-readable)
   - Update `__init__.py`, `main.py`, `main_window.py`

3. **Add entry point to `pyproject.toml`:**
   ```toml
   [project.scripts]
   pywats-your-app = "pywats_ui.apps.your_app_name.main:main"
   ```

4. **Run your app:**
   ```bash
   python -m pywats_ui.apps.your_app_name.main
   ```

## Template Structure

```
template/
  __init__.py           # Package initialization
  main.py               # Entry point with BaseApplication
  main_window.py        # Main window extending BaseMainWindow
  config.py             # Application configuration
  README.md             # This file
  tests/
    test_{{app_name}}.py  # Unit tests template
```

## Customization Guide

See `docs/guides/creating_apps.md` for detailed instructions on:
- Adding custom tabs/panels
- Creating custom dialogs
- Integrating with pyWATS API
- Styling and themes
- Testing your application

## Examples

Check out existing apps for reference:
- `apps/aichat/` - AI-powered chat interface
- `apps/configurator/` - Configuration and settings (coming soon)
