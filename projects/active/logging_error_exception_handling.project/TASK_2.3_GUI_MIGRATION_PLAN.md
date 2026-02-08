# Task 2.3: GUI ErrorHandlingMixin Migration Plan

**Created:** 2026-02-03  
**Status:** Ready to execute  
**Scope:** Migrate 77 QMessageBox calls across 10 configurator pages to ErrorHandlingMixin

---

## Audit Results

**Total QMessageBox calls:** 77  
- Exception handlers: 41 (53%)
- Confirmations: 6 (8%)
- Simple dialogs: 27 (35%)
- Complex (manual review): 3 (4%)

**Files by complexity** (calls count):

| Priority | File | Total | Exception | Confirm | Simple | Complex |
|----------|------|-------|-----------|---------|--------|---------|
| **P1 (Start)** | dashboard.py | 1 | 1 | 0 | 0 | 0 |
| **P1** | location.py | 2 | 2 | 0 | 0 | 0 |
| **P1** | log.py | 2 | 2 | 0 | 0 | 0 |
| **P1** | sn_handler.py | 2 | 2 | 0 | 0 | 0 |
| **P2** | proxy_settings.py | 3 | 2 | 0 | 1 | 0 |
| **P2** | software.py | 5 | 3 | 0 | 1 | 1 |
| **P3** | connection.py | 8 | 4 | 0 | 4 | 0 |
| **P3** | setup.py | 8 | 3 | 1 | 4 | 0 |
| **P3** | api_settings.py | 9 | 4 | 1 | 4 | 0 |
| **P4 (Last)** | converters.py | 37 | 18 | 4 | 13 | 2 |

**Strategy:** Start with simplest files (P1), build momentum, tackle converters.py last.

---

## Migration Patterns

### 1. Exception Handlers (41 locations)

**Pattern:**
```python
# BEFORE:
try:
    some_operation()
except SomeException as e:
    logger.exception(f"Failed to do X: {e}")
    QMessageBox.critical(
        self,
        "Title",
        f"Error message: {e}"
    )
    raise  # Optional

# AFTER:
try:
    some_operation()
except SomeException as e:
    self.handle_error(e, "doing X")  # Automatically logs with exc_info=True
    raise  # Optional - keep if re-raising
```

**Key points:**
- ErrorHandlingMixin.handle_error() automatically:
  - Logs with `logger.exception()` (includes stack trace)
  - Shows type-appropriate dialog (Auth, Validation, Server, etc.)
  - Uses context string in error message
- Remove manual logger.exception() call (redundant)
- Keep `raise` statement if present (preserve exception propagation)
- Choose meaningful context strings (what was being attempted)

### 2. Confirmation Dialogs (6 locations)

**Pattern:**
```python
# BEFORE:
reply = QMessageBox.question(
    self,
    "Confirm Action",
    "Are you sure?",
    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
)
if reply == QMessageBox.StandardButton.Yes:
    do_something()

# AFTER:
if self.confirm_action("Are you sure?", "Confirm Action"):
    do_something()
```

**Key points:**
- Returns bool (True = Yes, False = No)
- Much more concise
- Title is optional (defaults to "Confirm")

### 3. Simple Dialogs (27 locations)

**Pattern:**
```python
# BEFORE:
QMessageBox.warning(self, "Title", "Warning message")
QMessageBox.critical(self, "Title", "Error message")
QMessageBox.information(self, "Title", "Success message")

# AFTER:
self.show_warning("Warning message", "Title")
self.show_error("Error message", "Title")
self.show_success("Success message", "Title")
```

**Key points:**
- Title is optional (has sensible defaults)
- Use show_success for QMessageBox.information (positive messages)
- Use show_warning for QMessageBox.warning
- Use show_error for QMessageBox.critical

### 4. Complex Cases (3 locations) - Manual Review

**Need special handling:**

1. **converters.py line 1040** - Three-button dialog (Save/Discard/Cancel)
   - Not supported by ErrorHandlingMixin.confirm_action()
   - Keep as QMessageBox.question with custom button set

2. **converters.py line 1605** - Information dialog in unnamed except block
   - Review what exception is being caught
   - Consider if it should be an error dialog instead
   - Add proper exception variable name

3. **software.py line 154** - Question dialog (unclear pattern from audit)
   - Review context to determine if confirm_action() is appropriate
   - May need custom handling

---

## Execution Plan

### Phase 1: Simple Files (P1) - ~15 minutes

Files with only exception handlers, no confirmations or complex cases.

**Checklist:**

- [ ] **dashboard.py** (1 call)
  - [ ] Line 244: Exception handler
  - [ ] Test: Load dashboard page, trigger error if possible

- [ ] **location.py** (2 calls)
  - [ ] Line 99: Exception handler
  - [ ] Line 115: Exception handler
  - [ ] Test: Location page operations

- [ ] **log.py** (2 calls)
  - [ ] Line 150: Exception handler
  - [ ] Line 204: Exception handler
  - [ ] Test: Log viewing operations

- [ ] **sn_handler.py** (2 calls)
  - [ ] Line 200: Exception handler
  - [ ] Line 246: Exception handler
  - [ ] Test: Serial number handler operations

**After Phase 1:**
- Remove QMessageBox import if no longer used in file
- Run configurator app to verify pages still work
- Commit changes

---

### Phase 2: Medium Files (P2) - ~20 minutes

Files with exception handlers + simple dialogs + 0-1 complex cases.

**Checklist:**

- [ ] **proxy_settings.py** (3 calls)
  - [ ] Line 163: Simple dialog (show_warning)
  - [ ] Line 190: Exception handler
  - [ ] Line 223: Exception handler
  - [ ] Test: Proxy settings configuration

- [ ] **software.py** (5 calls - 1 complex)
  - [ ] Line 143: Simple dialog (show_warning)
  - [ ] Line 154: **COMPLEX - Manual review question dialog**
  - [ ] Line 170: Exception handler
  - [ ] Line 208: Exception handler
  - [ ] Line 232: Exception handler
  - [ ] Test: Software management operations

**After Phase 2:**
- Verify complex case in software.py works correctly
- Test error scenarios if possible
- Commit changes

---

### Phase 3: Large Files (P3) - ~30 minutes

Files with mixed patterns (exception handlers + confirmations + simple dialogs).

**Checklist:**

- [ ] **connection.py** (8 calls)
  - [ ] Lines 203, 219, 291, 550: Exception handlers (4)
  - [ ] Lines 274, 451, 483, 534: Simple dialogs (4)
  - [ ] Test: Connection testing, config save

- [ ] **setup.py** (8 calls)
  - [ ] Lines 328, 395, 446: Exception handlers (3)
  - [ ] Line 128: Confirmation (confirm_action)
  - [ ] Lines 119, 338, 350, 359: Simple dialogs (4)
  - [ ] Test: Setup wizard flow

- [ ] **api_settings.py** (9 calls)
  - [ ] Lines 313, 336, 400, 443: Exception handlers (4)
  - [ ] Line 322: Confirmation (confirm_action)
  - [ ] Lines 271, 300, 344, 358: Simple dialogs (4)
  - [ ] Test: API settings configuration

**After Phase 3:**
- Verify all error paths work correctly
- Test confirmation dialogs (accept and cancel paths)
- Commit changes

---

### Phase 4: Converters Page (P4) - ~45 minutes

**converters.py** (37 calls - largest file, 2 complex cases)

**Pre-work:**
- Read through converters.py to understand architecture
- Identify what triggers each error path
- Plan testing strategy for 37 different dialog locations

**Exception Handlers (18):**
- [ ] Lines 546, 560, 646: Watch folder validation
- [ ] Lines 832, 863: Config parsing errors
- [ ] Line 934: Delete converter error
- [ ] Line 1025: General save error
- [ ] Lines 1192, 1223, 1260: Add converter errors
- [ ] Line 1400: Test converter error
- [ ] Lines 1444, 1478, 1505: Customize converter errors
- [ ] Lines 1519, 1533, 1554: Import/export errors
- [ ] Line 1613: General operation error

**Confirmations (4):**
- [ ] Line 964: Delete confirmation
- [ ] Line 1232: Remove converter confirmation
- [ ] Line 1489: Overwrite confirmation
- [ ] Line 1572: Discard changes confirmation

**Simple Dialogs (13):**
- [ ] Lines 615, 619, 624: Validation warnings
- [ ] Line 853: Save failed
- [ ] Lines 905, 942: Warnings
- [ ] Lines 918, 928, 1014, 1214: Information messages
- [ ] Lines 1433, 1543, 1564: Warnings

**Complex Cases (2):**
- [ ] Line 1040: **COMPLEX - Three-button dialog (Save/Discard/Cancel)**
  - Review: Unsaved changes dialog
  - Keep as QMessageBox with custom buttons
  - Document why ErrorHandlingMixin not used
  
- [ ] Line 1605: **COMPLEX - Information in unnamed except block**
  - Review exception being caught
  - Add proper exception variable
  - Consider if show_error more appropriate than show_success

**Testing:**
- [ ] Add converter configuration
- [ ] Edit converter settings
- [ ] Delete converter
- [ ] Test converter execution
- [ ] Customize system converter
- [ ] Import/export converters
- [ ] Trigger validation errors

**After Phase 4:**
- Comprehensive testing of all converter operations
- Verify no regressions
- Remove QMessageBox import (if no longer used)
- Commit with detailed message

---

## Context String Guidelines

**Good context strings** describe what was being attempted:

✅ **Good:**
- "saving connection configuration"
- "testing server connection"
- "loading converter list"
- "deleting converter"
- "validating API token"

❌ **Bad:**
- "error occurred" (too generic)
- "failed" (no context)
- "" (empty - always provide context!)

**Pattern:**
- Use gerund form (verb + -ing): "doing X"
- Be specific about the operation
- Match to user action (not internal implementation)
- Keep under 50 characters

---

## Import Cleanup

After migrating each file, check if QMessageBox import can be removed:

```python
# If all QMessageBox calls replaced, remove:
from PySide6.QtWidgets import QMessageBox  # ← Remove this line

# ErrorHandlingMixin is available via BasePage inheritance, no import needed!
```

**Check:** Search file for remaining `QMessageBox` usage before removing import.

---

## Testing Strategy

### Manual Testing (per file)

1. **Launch configurator:**
   ```powershell
   python run_configurator.py
   ```

2. **Navigate to migrated page**

3. **Test scenarios:**
   - Trigger validation errors (invalid input)
   - Test confirmations (both accept and cancel paths)
   - Trigger exception errors (disconnect from server, invalid config, etc.)
   - Verify success messages show correctly

4. **Verify error dialogs:**
   - Show appropriate title and message
   - Include context string in message
   - Logged with stack trace (check logs)

### Automated Testing

No automated GUI tests exist for configurator pages. Manual testing required.

### Regression Testing

After all migrations:
- [ ] Load each configurator page
- [ ] Verify no crashes or missing dialogs
- [ ] Check logs for proper error logging with exc_info=True

---

## Commit Strategy

**Commit after each phase:**

```
Phase 1 commit:
feat(gui): Migrate simple pages to ErrorHandlingMixin (4 files, 7 calls)

- dashboard.py: 1 exception handler
- location.py: 2 exception handlers  
- log.py: 2 exception handlers
- sn_handler.py: 2 exception handlers

All exception handlers now use self.handle_error(e, context) for:
- Consistent error dialogs
- Automatic stack trace logging
- Type-based error handling

Tests: Manual testing of all 4 pages - no regressions
```

**Final commit message template:**
```
feat(gui): Complete ErrorHandlingMixin migration (10 files, 77 calls)

Migrated all configurator pages from direct QMessageBox calls to
ErrorHandlingMixin methods:
- 41 exception handlers → self.handle_error(e, context)
- 6 confirmations → self.confirm_action(message, title)
- 27 simple dialogs → self.show_warning/error/success()
- 3 complex cases → manual review and custom handling

Benefits:
- Consistent error dialog presentation
- Automatic exception logging with stack traces
- Type-based error handling (Auth, Validation, Server, etc.)
- Simplified code (fewer lines, more maintainable)

Files updated:
- api_settings.py (9 calls)
- connection.py (8 calls)
- converters.py (37 calls)
- dashboard.py (1 call)
- location.py (2 calls)
- log.py (2 calls)
- proxy_settings.py (3 calls)
- setup.py (8 calls)
- sn_handler.py (2 calls)
- software.py (5 calls)

Tests: Manual testing of all configurator pages - no regressions
```

---

## Success Criteria

- ✅ All 77 QMessageBox calls migrated (or documented why kept)
- ✅ No QMessageBox imports in configurator pages (except complex cases)
- ✅ All exception handlers log with stack traces
- ✅ All error dialogs have meaningful context strings
- ✅ No regressions in configurator functionality
- ✅ All phases committed separately

---

## Estimated Time

- Phase 1 (P1 files): 15 minutes  
- Phase 2 (P2 files): 20 minutes  
- Phase 3 (P3 files): 30 minutes  
- Phase 4 (converters.py): 45 minutes  
- Testing & commits: 20 minutes  

**Total:** ~2 hours for complete migration

---

## Questions / Blockers

None identified. ErrorHandlingMixin is well-tested and ready to use.

---

## Next Steps

1. Start with dashboard.py (easiest - 1 call)
2. Build momentum through P1 files
3. Progress through P2, P3, P4 phases
4. Test thoroughly after each phase
5. Commit incrementally
6. Update CHANGELOG.md when complete
