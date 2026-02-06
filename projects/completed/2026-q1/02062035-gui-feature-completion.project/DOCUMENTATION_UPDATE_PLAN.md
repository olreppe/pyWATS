# Documentation Update Plan - GUI Feature Completion

**Date:** February 6, 2026 20:40  
**Status:** In Progress  
**Scope:** Full documentation review and update after GUI migration

---

## Issues Found

### CRITICAL: Broken Entry Point ❌
**File:** `src/pywats_client/__main__.py`  
**Lines:** 177, 275  
**Problem:** Imports `.gui.app.run_gui` which doesn't exist (old GUI was removed)  
**Impact:** `pywats-client gui` command is BROKEN  
**Fix:** Create proper configurator launcher function

### Documentation References to Update 📚

1. **README.md**
   - Line ~13: Mentions `run_gui.py` 
   - Line ~77: Installation section mentions GUI client
   - Status: Needs review

2. **docs/getting-started.md**
   - Line ~795: "GUI Client (Desktop)" section
   - Line ~805: References launching GUI
   - Line ~830: File menu documentation
   - Status: May reference old GUI features

3. **docs/CHEAT_SHEET.md**
   - Line ~13: Installation examples `pip install pywats-api[client]` ✅ (correct)
   - Status: Appears correct

4. **docs/CLI_REFERENCE.md**
   - Line ~125: `pywats-client gui` command documentation
   - Status: Documentation is correct, but command is BROKEN due to __main__.py issue

5. **examples/async_client_example.py**
   - Lines ~177-322: GUI integration with qasync example
   - Status: Needs review (may show old GUI pattern)

6. **Sphinx API docs**
   - Location: `docs/api/`
   - Status: Needs review

---

## Fix Strategy

### Phase 1: Fix Broken Entry Point (CRITICAL)
1. Create `src/pywats_client/gui/__init__.py` (minimal)  
2. Create `src/pywats_client/gui/app.py` with `run_gui()` function
3. Function launches ConfiguratorMainWindow with qasync

### Phase 2: Update Documentation
1. Update README.md - verify launcher instructions
2. Update docs/getting-started.md - GUI setup section
3. Update examples/async_client_example.py - GUI integration pattern  
4. Review Sphinx docs for GUI references

### Phase 3: Consistency Check
1. Verify all `run_*.py` files in root are documented
2. Remove/deprecate any obsolete launchers
3. Update CHANGELOG.md with documentation fixes

---

## Implementation Details

### New `run_gui()` Function
```python
def run_gui(config: ClientConfig, instance_id: str = "default") -> None:
    """Launch Configurator GUI with qasync integration.
    
    Args:
        config: ClientConfig instance
        instance_id: Instance ID for multi-station mode
    """
    from PySide6.QtWidgets import QApplication
    from pywats_ui.apps.configurator.main_window import ConfiguratorMainWindow
    import qasync
    import asyncio
    
    app = QApplication(sys.argv)
    app.setApplicationName("pyWATS Configurator")
    app.setOrganizationName("pyWATS")
    
    # Setup async event loop
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    # Create and show window
    window = ConfiguratorMainWindow(config=config)
    window.setWindowTitle(f"pyWATS Configurator - {instance_id}")
    window.show()
    
    with loop:
        loop.run_forever()
```

---

## Testing Plan

1. **Test `pywats-client gui`** - Should launch configurator correctly
2. **Test `python -m pywats_client gui`** - Same as above
3. **Test multi-instance** - `pywats-client gui --instance-id test`
4. **Verify all docs** - No broken references

---

## Status

- [x] Audit complete
- [ ] Fix entry point
- [ ] Update documentation
- [ ] Test commands
- [ ] Commit changes

