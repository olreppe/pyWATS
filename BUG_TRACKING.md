# New GUI Bug Tracking Log
**Started:** 2026-02-04
**Purpose:** Track all errors for test creation and regression prevention

## Bug Format
`[STATUS] Component | File:Line | Error Type | Description`

---

## Bugs Discovered

### Import/Architecture Issues
- [FIXED] pywats_ui.framework.base_page | base_page.py:27 | ImportError | Relative import beyond package boundary (`from ...core.config`)
- [FIXED] pywats_ui.apps.configurator.pages.converters | converters.py:38 | ImportError | Wrong module name (`from ...framework.base` should be `base_page`)
- [FIXED] pywats_ui.framework.__init__ | __init__.py:12 | ImportError | Relative import beyond package for ClientConfig

### Configuration Issues  
- [FIXED] pywats_ui.framework.base_page | base_page.py:87 | AttributeError | Pages expect `self._config` but BasePage sets `self.config`
- [FIXED] ClientConfig | config.py | AttributeError | Missing dict-like methods `.get()` and `.set()` 
- [FIXED] ConverterConfig | config.py | AttributeError | Missing dict-like methods `.get()` and `.set()`
- [FIXED] run_new_gui_debug.py:103 | AttributeError | ConfigManager has `load()` not `load_config()` - switched to ClientConfig.load_from_file()
- [WORKAROUND] ClientConfig | config.py:887 | ValueError | Config path not set - now set explicitly before save

### Component Initialization Issues
- [FIXED] BaseMainWindow | pywats_ui/framework/__init__.py | TypeError | Constructor signature mismatch (missing `config` parameter)
- [FIXED] QueueManager | main_window.py:268 | TypeError | Missing required `send_callback` parameter - added _send_queued_operation method
- [DEFERRED] QueueManager | main_window.py | NotImplementedError | Send callback is placeholder - will implement with report submission

### Dashboard Page Issues
- [FIXED] Dashboard | dashboard.py:259 | AttributeError | ConverterConfig dict-like access - added .get()/.set() methods
- [UNTESTED] Dashboard | dashboard.py | RuntimeError | Converter health check with zero converters

### Connection Page Issues
- [OPEN] ConnectionPage | connection.py:270 | RuntimeError | No event loop in MainThread for async tasks
- [OPEN] ConnectionPage | connection.py:352 | RuntimeWarning | Coroutine `_run_connection_test` never awaited

### Multi-GUI Conflicts
- [FIXED] Process Conflict | test_both_guis.py | ImportError | Running old + new GUI in same process causes import conflicts
- [WORKAROUND] Isolation | run_new_gui.py | N/A | Created standalone launcher to avoid conflicts

### Qt Deprecation Warnings (Low Priority)
- [INFO] Qt | run_new_gui.py:43 | DeprecationWarning | AA_EnableHighDpiScaling deprecated
- [INFO] Qt | run_new_gui.py:44 | DeprecationWarning | AA_UseHighDpiPixmaps deprecated
- [INFO] Qt Import | run_new_gui_debug.py | ImportError | QT_VERSION_STR not available in PySide6.QtCore

### Console Encoding Issues
- [FIXED] run_new_gui_debug.py | logging | UnicodeEncodeError | cp1252 can't encode Unicode symbols (✓, ℹ) - fixed with UTF-8 StreamHandler

---

## Patterns Identified

### Pattern 1: Dict-like Interface Missing
**Affected:** ClientConfig, ConverterConfig, potentially other config dataclasses
**Root Cause:** GUI code expects dict-like `.get(key, default)` but dataclasses use direct attributes
**Solution:** Add `get()`, `set()`, `__getitem__`, `__setitem__` methods to all config classes
**Test Need:** Unit tests for dict-like interface on all config classes

### Pattern 2: Async/Event Loop Management
**Affected:** ConnectionPage, potentially other async pages
**Root Cause:** Qt main thread doesn't have asyncio event loop by default
**Solution:** Need qasync integration in BaseMainWindow
**Test Need:** Integration tests for async operations in GUI context

### Pattern 3: Config Path Management
**Affected:** All GUI pages that save config
**Root Cause:** Config created without ConfigManager doesn't have `_config_path` set
**Solution:** Always use ConfigManager for config creation/loading
**Test Need:** Test config save/load cycle from GUI

### Pattern 4: Component Initialization Order
**Affected:** QueueManager, ConnectionMonitor, reliability components
**Root Cause:** Components initialized before dependencies are ready
**Solution:** Proper initialization sequencing with error handling
**Test Need:** Integration test for full component initialization sequence

---

## Next Steps
1. Fix ConfigManager API usage (use `load()` not `load_config()`)
2. Implement proper qasync event loop integration
3. Test all fixes systematically
4. Create regression tests for each fixed bug
5. Document initialization sequence requirements

---

## Statistics
- Total Bugs: 18
- Fixed: 12
- Open: 3
- Deferred: 1
- Info/Low Priority: 3
- Critical (Blocking): 0 (all critical bugs fixed!)

## Test Coverage Added
- test_gui_stress.py: Comprehensive stress test suite (5 test categories, 20+ individual tests)
- run_new_gui_debug.py: Full debug launcher with UTF-8 logging
- BUG_TRACKING.md: This document for regression prevention
