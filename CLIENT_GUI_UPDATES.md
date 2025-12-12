# pyWATS Client GUI Updates - Summary

**Date:** December 12, 2025  
**Branch:** main  
**Status:** ✅ Complete - All tests passing (98 passed)

## Overview

Enhanced the pyWATS Client GUI with:
1. **pyWATS Library Logging Integration** - Automatic debug logging when client is in DEBUG mode
2. **Modular Tab Configuration** - Dynamic show/hide tabs based on user configuration
3. **Comprehensive Documentation** - New GUI configuration guide

## Files Modified

### 1. src/pywats_client/core/client.py
**Changes:**
- Added pyWATS library logging integration in `_setup_logging()` method
- When client log level is DEBUG, automatically enables pyWATS library debug logging
- Provides visibility into HTTP requests, API calls, and library operations

**Key Code:**
```python
# Enable pyWATS library logging if debug level
if log_level == logging.DEBUG:
    try:
        from pywats import enable_debug_logging
        enable_debug_logging()
        logger.debug("pyWATS library debug logging enabled")
    except ImportError:
        logger.warning("Could not enable pyWATS debug logging - library not found")
```

### 2. src/pywats_client/core/config.py
**Changes:**
- Added 5 new configuration fields for tab visibility:
  - `show_software_tab: bool = True`
  - `show_sn_handler_tab: bool = True`
  - `show_converters_tab: bool = True`
  - `show_location_tab: bool = True`
  - `show_proxy_tab: bool = True`
- Updated `to_dict()` method to serialize new fields
- `from_dict()` automatically handles deserialization

**Benefits:**
- Users can customize which tabs appear in the GUI
- Simplifies interface for specific use cases
- Configuration persists across restarts

### 3. src/pywats_client/gui/main_window.py
**Changes:**
- Modified navigation sidebar to dynamically build tabs based on config
- Modified page stack to only create pages that are visible
- Setup and General tabs are always shown
- Optional tabs (Location, Converters, SN Handler, Proxy, Software) respect config settings

**Key Code:**
```python
# Dynamically build navigation based on config visibility settings
nav_items = [
    ("Setup", "⚙️"),
    ("General", "⚙️"),
    ("Connection", "🔗"),
]

# Add optional tabs based on configuration
if self.config.show_location_tab:
    nav_items.append(("Location", "📍"))
# ... etc
```

### 4. src/pywats_client/gui/pages/general.py
**Changes:**
- Added "GUI Tab Visibility" section with checkboxes for each configurable tab
- Users can control tab visibility directly from the GUI
- Added note that restart is required for changes to take effect
- Updated `save_config()` to persist visibility settings
- Updated `load_config()` to restore visibility settings

**UI Elements:**
```
GUI Tab Visibility
├── Show Location tab          ☑
├── Show Converters tab        ☑
├── Show SN Handler tab        ☑
├── Show Proxy Settings tab    ☑
└── Show Software tab          ☑
Note: Changes require restart to take effect
```

### 5. README.md
**Changes:**
- Added new "GUI Configuration" section under "Running the GUI Client"
- Added reference to new GUI_CONFIGURATION.md documentation
- Links to comprehensive setup guide

### 6. src/pywats_client/GUI_CONFIGURATION.md (NEW)
**Created:** Comprehensive 300+ line documentation covering:
- Tab visibility configuration (GUI and config file methods)
- Logging configuration and pyWATS integration
- Configuration file structure and location
- Example configurations for different scenarios:
  - Minimal (essential tabs only)
  - Production line station
  - Development/debug station
  - Corporate environment (behind proxy)
- Best practices and troubleshooting

## Usage Examples

### Example 1: Simple Test Station (Minimal UI)
```json
{
  "show_location_tab": false,
  "show_converters_tab": false,
  "show_sn_handler_tab": false,
  "show_proxy_tab": false,
  "show_software_tab": false
}
```
Result: Shows only Setup, General, Connection tabs

### Example 2: Production Line Station
```json
{
  "show_location_tab": true,
  "show_converters_tab": true,
  "show_sn_handler_tab": true,
  "show_proxy_tab": false,
  "show_software_tab": true,
  "log_level": "INFO"
}
```
Result: Full production features, no proxy settings, INFO logging

### Example 3: Development Station (Full Debug)
```json
{
  "show_location_tab": true,
  "show_converters_tab": true,
  "show_sn_handler_tab": true,
  "show_proxy_tab": true,
  "show_software_tab": true,
  "log_level": "DEBUG"
}
```
Result: All tabs visible, full debug logging for both client and pyWATS library

## Logging Integration Details

When log level is set to **DEBUG**:
- Client logs: Detailed client operations
- pyWATS library logs: HTTP requests, API calls, serialization, error handling
- Combined view: Complete picture of client + library operations

Example debug output:
```
2025-12-12 14:30:15,123 - pywats_client.core.client - INFO - Initializing pyWATS Client
2025-12-12 14:30:15,125 - pywats_client.core.client - DEBUG - pyWATS library debug logging enabled
2025-12-12 14:30:15,234 - pywats.http_client - INFO - Initializing HttpClient
2025-12-12 14:30:15,345 - pywats.http_client - DEBUG - GET https://wats.example.com/api/Product/1234
2025-12-12 14:30:15,456 - pywats.http_client - DEBUG - Response: 200 OK (1234 bytes)
2025-12-12 14:30:15,567 - pywats.domains.product.repository - DEBUG - Retrieved product: TestProduct
```

## Configuration Location

Configuration files stored at:
- **Windows:** `%APPDATA%\pyWATS_Client\config.json`
- **Linux/Mac:** `~/.config/pywats_client/config.json`

Multiple instances supported:
- `config.json` - Default instance
- `config_station1.json` - Station 1
- `config_station2.json` - Station 2

## Benefits

### For End Users:
✅ Cleaner, simpler UI - show only needed tabs  
✅ Less confusion - hide unused features  
✅ Better performance - fewer pages to initialize  
✅ Customizable per station type  

### For Developers:
✅ Easy debugging - one setting enables full logging  
✅ Clear separation - client vs library logging  
✅ Troubleshooting - complete visibility into operations  
✅ Flexible configuration - JSON-based settings  

### For Administrators:
✅ Standardized configs - template-based deployment  
✅ User-appropriate UI - match skill level  
✅ Reduced support calls - simpler interfaces  
✅ Easy deployment - copy config files  

## Testing

All existing tests pass:
```
pytest results: 98 passed, 7 skipped
```

No breaking changes - all existing functionality preserved.

## Backward Compatibility

✅ **Fully backward compatible**
- New config fields have sensible defaults (all tabs shown)
- Existing config files work without modification
- Tab visibility automatically defaults to `true` if not specified
- Logging integration is opt-in (only at DEBUG level)

Old config files will:
1. Load successfully
2. Show all tabs (default behavior)
3. Continue working as before

## Migration Guide

### Existing Users
No action required! But you can:

1. **Enable debug logging** (if needed):
   - GUI: General → Logging → Select "DEBUG"
   - Config: Set `"log_level": "DEBUG"`

2. **Customize tab visibility** (optional):
   - GUI: General → GUI Tab Visibility → Check/uncheck tabs
   - Config: Add `show_*_tab` fields to config.json

3. **Review documentation**:
   - Read [GUI_CONFIGURATION.md](src/pywats_client/GUI_CONFIGURATION.md)

### New Users
Follow the setup guide in [GUI_CONFIGURATION.md](src/pywats_client/GUI_CONFIGURATION.md)

## Future Enhancements

Potential future improvements:
- [ ] Dynamic tab reloading (no restart required)
- [ ] Tab order customization
- [ ] Per-tab logging levels
- [ ] UI themes (dark/light mode)
- [ ] Tab groups/categories
- [ ] Export/import configuration templates

## Documentation

Complete documentation available at:
- [GUI_CONFIGURATION.md](src/pywats_client/GUI_CONFIGURATION.md) - Full configuration guide
- [README.md](README.md) - Quick reference
- [LOGGING_STRATEGY.md](LOGGING_STRATEGY.md) - Library logging details

## Commit Message

```
feat(client): Add logging integration and modular GUI tabs

- Integrate pyWATS library logging (auto-enabled in DEBUG mode)
- Add configurable tab visibility (Location, Converters, SN Handler, Proxy, Software)
- Add GUI Tab Visibility section to General settings page
- Create comprehensive GUI_CONFIGURATION.md documentation
- Update README.md with GUI configuration reference

All tabs default to visible for backward compatibility.
Changes require restart to take effect.

Closes: Internal ticket for logging and UI customization
Tests: All 98 tests passing
```

## Summary

This update provides:
1. **Integrated Logging:** Seamless pyWATS library logging for debugging
2. **Modular UI:** Configurable tab visibility for simplified interfaces
3. **Complete Documentation:** Comprehensive guides for setup and usage
4. **Backward Compatible:** Existing installations work without changes
5. **User Control:** Both GUI and config file control options

The client is now more flexible, easier to debug, and better suited for diverse deployment scenarios from simple test stations to complex production lines.
